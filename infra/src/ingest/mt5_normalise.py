"""
MT5 / BMRG Print normaliser → adapter blotter + event manifest + metadata.

Inputs:
  - Tester log with [BMRG][TRADE] OPEN lines
  - Optional train matrix (exits / outcomes)
  - Optional deals CSV (future); Print path is primary for Harvest dumps

Costs: every cost component is flagged defaulted vs measured (never silent).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from schema_validate import validate

INFRA = Path(__file__).resolve().parents[2]
BMRG = INFRA.parent

OPEN_RE = re.compile(
    r"(?P<ts>\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"\[BMRG\]\[TRADE\] OPEN (?P<side>BUY|SELL) "
    r"lot=(?P<lot>[0-9.]+) price=(?P<price>[0-9.]+) "
    r"sl=(?P<sl>[0-9.]+) tp=(?P<tp>[0-9.]+) "
    r"level=(?P<level>\d+) riskMode=(?P<riskMode>\d+) "
    r"spread=(?P<spread>\d+) deal=(?P<deal>\d+)"
)

DEFAULT_COSTS_DEFAULTED = [
    "spread_proxy_3x",
    "commission_0",
    "swap_0",
    "slippage_in_proxy",
]
POINT = 1e-5


@dataclass
class NormaliseConfig:
    magic: int = 8210204
    symbol: str = "EURUSD"
    sl_points: float = 300.0
    tp_points: float = 300.0
    tick_value: float = 1.0
    deposit_ref: float = 400.0
    designed_rr: float = 1.0
    preset_id: str = "EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long"
    ea_version: str = "1.20"
    costs_defaulted: list[str] = field(default_factory=lambda: list(DEFAULT_COSTS_DEFAULTED))


@dataclass
class OpenRow:
    ts: datetime
    side: str
    lot: float
    price: float
    sl: float
    tp: float
    spread: int
    deal: int
    level: int = 0


@dataclass
class QuarantineRow:
    reason: str
    raw: str


def parse_opens(log_path: Path) -> tuple[list[OpenRow], list[QuarantineRow]]:
    rows: list[OpenRow] = []
    bad: list[QuarantineRow] = []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if "[BMRG][TRADE] OPEN" not in line:
            continue
        m = OPEN_RE.search(line)
        if not m:
            bad.append(QuarantineRow("open_regex_miss", line[-240:]))
            continue
        ts = datetime.strptime(m.group("ts"), "%Y.%m.%d %H:%M:%S").replace(tzinfo=timezone.utc)
        rows.append(
            OpenRow(
                ts=ts,
                side=m.group("side"),
                lot=float(m.group("lot")),
                price=float(m.group("price")),
                sl=float(m.group("sl")),
                tp=float(m.group("tp")),
                spread=int(m.group("spread")),
                deal=int(m.group("deal")),
                level=int(m.group("level")),
            )
        )
    return rows, bad


def load_exits(train_path: Path | None) -> dict[str, dict]:
    if not train_path or not train_path.exists():
        return {}
    out: dict[str, dict] = {}
    with train_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = row["t"].replace("T", " ")[:19]
            out[key] = row
    return out


def event_id(magic: int, symbol: str, side: str, ts: datetime, ticket: int) -> str:
    return f"{magic}-{symbol}-{side}-{ts.strftime('%Y%m%d%H%M%S')}-{ticket}"


def declared_1r(volume: float, sl_points: float, tick_value: float) -> float:
    return round(sl_points * volume * tick_value, 6)


def iso(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def spread_cost_ccy(spread_pts: float, volume: float, tick_value: float) -> float:
    """Defaulted round-turn proxy: 3 × spread points × volume × tick_value."""
    return round(3.0 * spread_pts * volume * tick_value, 6)


def c_r_from_spread(spread_pts: float, sl_points: float) -> float:
    return (3.0 * spread_pts) / sl_points if sl_points else 0.0


def normalise(
    log_path: Path,
    train_path: Path | None = None,
    cfg: NormaliseConfig | None = None,
    out_dir: Path | None = None,
) -> dict:
    cfg = cfg or NormaliseConfig()
    opens, quarantined = parse_opens(log_path)
    exits = load_exits(train_path)

    metadata = {
        "ea_name": "BMRG",
        "ea_version": cfg.ea_version,
        "designed_rr": cfg.designed_rr,
        "risk_definition": "hard_stop_points",
        "regime_filtered": True,
        "baseline_frequency": 60,
        "costs_defaulted": list(cfg.costs_defaulted),
        "preset_id": cfg.preset_id,
        "geometry_mode": "G0_SINGLE",
        "symbol": cfg.symbol,
        "timeframe": "M5",
        "magic": cfg.magic,
        "pool_role": "Harvest",
        "sl_points": cfg.sl_points,
        "tp_points": cfg.tp_points,
    }
    validate(metadata, "ea_metadata.schema.json")

    manifests: list[dict] = []
    legs: list[dict] = []
    equity = cfg.deposit_ref
    mapped = 0

    for op in opens:
        eid = event_id(cfg.magic, cfg.symbol, op.side, op.ts, op.deal)
        risk = declared_1r(op.lot, cfg.sl_points, cfg.tick_value)
        pts = round(abs(op.price - op.sl) / POINT, 4)
        key = op.ts.strftime("%Y-%m-%d %H:%M:%S")
        ex = exits.get(key)

        cost_flags = {
            "cost_spread": "defaulted_3x_spread",
            "cost_commission": "defaulted_0",
            "cost_swap": "defaulted_0",
            "cost_slippage": "defaulted_in_spread_proxy",
        }

        if ex:
            mapped += 1
            exit_ts = datetime.strptime(ex["exit_t"][:19], "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc
            )
            exit_reason = ex.get("outcome") if ex.get("outcome") in {"TP", "SL", "MID"} else "OTHER"
            y_lose = int(float(ex.get("y_lose", 0)))
            pnl_r = -1.0 if y_lose else 1.0
            pnl_gross = round(pnl_r * risk, 6)
        else:
            exit_ts = op.ts
            exit_reason = "OTHER"
            pnl_gross = 0.0
            quarantined.append(QuarantineRow("missing_exit_join", key))

        spread_ccy = spread_cost_ccy(op.spread, op.lot, cfg.tick_value)
        pnl_net = round(pnl_gross - spread_ccy, 6)
        direction = "long" if op.side == "BUY" else "short"
        exit_price = op.sl if exit_reason == "SL" else op.tp if exit_reason == "TP" else op.price

        manifest = {
            "event_id": eid,
            "risk_ccy": risk,
            "equity_at_open": round(equity, 6),
            "signal_tag": "BB_FADE",
            "exit_reason": exit_reason,
            "magic": cfg.magic,
            "symbol": cfg.symbol,
            "side": op.side,
            "sl_points": pts,
            "volume": op.lot,
            "tick_value_per_point": cfg.tick_value,
            "equity_source": "walk_forward_proxy",
            "costs_defaulted": list(cfg.costs_defaulted),
            "cost_component_flags": cost_flags,
            "c_r_proxy": round(c_r_from_spread(op.spread, cfg.sl_points), 6),
            "spread_points_entry": float(op.spread),
        }
        # schema allows listed fields; strip extras before validate
        manifest_for_schema = {k: v for k, v in manifest.items() if k in {
            "event_id", "risk_ccy", "equity_at_open", "signal_tag", "exit_reason",
            "magic", "symbol", "side", "sl_points", "volume", "tick_value_per_point",
            "equity_source", "costs_defaulted",
        }}
        validate(manifest_for_schema, "event_manifest.schema.json")
        manifests.append(manifest)

        leg = {
            "event_id": eid,
            "leg_id": f"{eid}-L0",
            "symbol": cfg.symbol,
            "direction": direction,
            "entry_time": iso(op.ts),
            "entry_price": op.price,
            "entry_requested": None,
            "exit_time": iso(exit_ts),
            "exit_price": exit_price,
            "exit_requested": None,
            "initial_stop": op.sl,
            "volume": op.lot,
            "pnl_gross_ccy": pnl_gross,
            "cost_spread_ccy": spread_ccy,
            "cost_commission_ccy": 0.0,
            "cost_swap_ccy": 0.0,
            "cost_slippage_ccy": 0.0,
            "pnl_net_ccy": pnl_net,
            "exit_reason": exit_reason,
            "level_index": op.level,
            "bb_dev": 2.2,
            "spread_points_entry": float(op.spread),
            "session_ok": True,
            "group_event_id": eid,
            "signal_tag": "BB_FADE",
            "costs_defaulted": list(cfg.costs_defaulted),
            "cost_component_flags": cost_flags,
        }
        leg_for_schema = {k: v for k, v in leg.items() if k != "cost_component_flags"}
        validate(leg_for_schema, "adapter_blotter.schema.json")
        legs.append(leg)
        equity = round(equity + pnl_net, 6)

    coverage = mapped / max(len(opens), 1)
    pack = {
        "metadata": metadata,
        "manifests": manifests,
        "legs": legs,
        "quarantine": [{"reason": q.reason, "raw": q.raw} for q in quarantined],
        "stats": {
            "n_opens": len(opens),
            "n_legs": len(legs),
            "n_manifest": len(manifests),
            "n_joined_exits": mapped,
            "open_coverage": round(coverage, 4),
            "n_quarantine": len(quarantined),
            "costs_defaulted": list(cfg.costs_defaulted),
        },
    }

    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "ea_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        with (out_dir / "event_manifest.jsonl").open("w", encoding="utf-8") as f:
            for row in manifests:
                f.write(json.dumps(row) + "\n")
        with (out_dir / "blotter_legs.jsonl").open("w", encoding="utf-8") as f:
            for row in legs:
                f.write(json.dumps(row) + "\n")
        (out_dir / "quarantine.jsonl").write_text(
            "\n".join(json.dumps(q) for q in pack["quarantine"]) + ("\n" if pack["quarantine"] else ""),
            encoding="utf-8",
        )
        (out_dir / "normalise_stats.json").write_text(json.dumps(pack["stats"], indent=2), encoding="utf-8")

    return pack


def default_harvest_paths() -> tuple[Path, Path, Path]:
    log = BMRG / "blotter" / "archive" / "EDX-POOL_WINDOWS" / "T04_Long_8210204.log"
    train = BMRG / "blotter" / "archive" / "AOS-P4-T01" / "harvest_train_matrix.csv"
    out = INFRA / "fixtures" / "blotter" / "harvest_long_v1"
    return log, train, out


if __name__ == "__main__":
    log, train, out = default_harvest_paths()
    pack = normalise(log, train, out_dir=out)
    print(json.dumps(pack["stats"], indent=2))
