"""
Rebuild G0 Harvest events + declared 1R from tester OPEN log + train matrix exits.

event_id = "{magic}-{symbol}-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
risk_ccy = sl_points * volume * tick_value_per_point  (EURUSD default tick_value=1.0)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from schema_validate import validate

INFRA = Path(__file__).resolve().parents[2]
BMRG = INFRA.parent
DEFAULT_LOG = BMRG / "blotter" / "archive" / "EDX-POOL_WINDOWS" / "T04_Long_8210204.log"
DEFAULT_TRAIN = BMRG / "blotter" / "archive" / "AOS-P4-T01" / "harvest_train_matrix.csv"
OUT_DIR = INFRA / "artefacts" / "rebuild" / "harvest_p1"

OPEN_RE = re.compile(
    r"(?P<ts>\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"\[BMRG\]\[TRADE\] OPEN (?P<side>BUY|SELL) "
    r"lot=(?P<lot>[0-9.]+) price=(?P<price>[0-9.]+) "
    r"sl=(?P<sl>[0-9.]+) tp=(?P<tp>[0-9.]+) "
    r"level=(?P<level>\d+) riskMode=(?P<riskMode>\d+) "
    r"spread=(?P<spread>\d+) deal=(?P<deal>\d+)"
)

MAGIC = 8210204
SYMBOL = "EURUSD"
SL_POINTS = 300.0
TICK_VALUE = 1.0  # USD per point per 1.0 lot (EURUSD convention used in INF)
DEPOSIT_REF = 400.0
POINT = 1e-5


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


def parse_opens(log_path: Path) -> list[OpenRow]:
    rows: list[OpenRow] = []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    for m in OPEN_RE.finditer(text):
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
            )
        )
    return rows


def load_exits(train_path: Path) -> dict[str, dict]:
    """Key by entry timestamp string YYYY-MM-DD HH:MM:SS."""
    out: dict[str, dict] = {}
    with train_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = row["t"].replace("T", " ")[:19]
            out[key] = row
    return out


def event_id(magic: int, symbol: str, side: str, ts: datetime, ticket: int) -> str:
    stamp = ts.strftime("%Y%m%d%H%M%S")
    return f"{magic}-{symbol}-{side}-{stamp}-{ticket}"


def declared_1r(volume: float, sl_points: float = SL_POINTS, tick_value: float = TICK_VALUE) -> float:
    return round(sl_points * volume * tick_value, 6)


def sl_points_from_prices(side: str, entry: float, sl: float) -> float:
    dist = abs(entry - sl)
    return round(dist / POINT, 4)


def iso(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rebuild(
    log_path: Path = DEFAULT_LOG,
    train_path: Path = DEFAULT_TRAIN,
    out_dir: Path = OUT_DIR,
) -> dict:
    opens = parse_opens(log_path)
    exits = load_exits(train_path) if train_path.exists() else {}

    metadata = {
        "ea_name": "BMRG",
        "ea_version": "1.20",
        "designed_rr": 1.0,
        "risk_definition": "hard_stop_points",
        "regime_filtered": True,
        "baseline_frequency": 60,
        "costs_defaulted": ["spread_proxy_3x", "commission_0", "swap_0", "slippage_in_proxy"],
        "preset_id": "EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long",
        "geometry_mode": "G0_SINGLE",
        "symbol": SYMBOL,
        "timeframe": "M5",
        "magic": MAGIC,
        "pool_role": "Harvest",
        "sl_points": SL_POINTS,
        "tp_points": 300.0,
    }
    validate(metadata, "ea_metadata.schema.json")

    manifests: list[dict] = []
    blotter: list[dict] = []
    equity = DEPOSIT_REF
    sl_ok = 0

    for i, op in enumerate(opens, start=1):
        side_key = op.side  # BUY/SELL in event_id per edge_framework examples
        eid = event_id(MAGIC, SYMBOL, side_key, op.ts, op.deal)
        risk = declared_1r(op.lot)
        pts = sl_points_from_prices(op.side, op.price, op.sl)
        if abs(pts - SL_POINTS) <= 1.0:
            sl_ok += 1

        key = op.ts.strftime("%Y-%m-%d %H:%M:%S")
        ex = exits.get(key)
        if ex:
            exit_ts = datetime.strptime(ex["exit_t"][:19], "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc
            )
            exit_reason = ex.get("outcome") or "OTHER"
            y_lose = int(float(ex.get("y_lose", 0)))
            # FIXED_RR proxy PnL in R then * risk_ccy
            pnl_r = -1.0 if y_lose else 1.0
            pnl_gross = round(pnl_r * risk, 6)
        else:
            exit_ts = op.ts
            exit_reason = "OTHER"
            pnl_gross = 0.0

        # cost proxy: 3× spread points → ccy via tick_value * volume
        spread_cost = round(3.0 * op.spread * op.lot * TICK_VALUE, 6)
        pnl_net = round(pnl_gross - spread_cost, 6)

        direction = "long" if op.side == "BUY" else "short"
        # exit price proxy from SL/TP geometry when unknown
        if exit_reason == "SL":
            exit_price = op.sl
        elif exit_reason == "TP":
            exit_price = op.tp
        else:
            exit_price = op.price

        manifest = {
            "event_id": eid,
            "risk_ccy": risk,
            "equity_at_open": round(equity, 6),
            "signal_tag": "BB_FADE",
            "exit_reason": exit_reason if exit_reason in {"TP", "SL", "MID", "OTHER"} else "OTHER",
            "magic": MAGIC,
            "symbol": SYMBOL,
            "side": op.side,
            "sl_points": pts,
            "volume": op.lot,
            "tick_value_per_point": TICK_VALUE,
            "equity_source": "walk_forward_proxy",
            "costs_defaulted": metadata["costs_defaulted"],
        }
        validate(manifest, "event_manifest.schema.json")
        manifests.append(manifest)

        leg = {
            "event_id": eid,
            "leg_id": f"{eid}-L0",
            "symbol": SYMBOL,
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
            "cost_spread_ccy": spread_cost,
            "cost_commission_ccy": 0.0,
            "cost_swap_ccy": 0.0,
            "cost_slippage_ccy": 0.0,
            "pnl_net_ccy": pnl_net,
            "exit_reason": manifest["exit_reason"],
            "level_index": 0,
            "bb_dev": 2.2,
            "spread_points_entry": float(op.spread),
            "session_ok": True,
            "group_event_id": eid,
            "signal_tag": "BB_FADE",
            "costs_defaulted": metadata["costs_defaulted"],
        }
        validate(leg, "adapter_blotter.schema.json")
        blotter.append(leg)

        equity = round(equity + pnl_net, 6)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ea_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    with (out_dir / "event_manifest.jsonl").open("w", encoding="utf-8") as f:
        for row in manifests:
            f.write(json.dumps(row) + "\n")
    with (out_dir / "blotter_legs.jsonl").open("w", encoding="utf-8") as f:
        for row in blotter:
            f.write(json.dumps(row) + "\n")

    summary = {
        "task_id": "INF-P1-T04",
        "recipe": "INF-P1-T04_store_eventId_1R_rebuild_Harvest",
        "n_opens": len(opens),
        "n_manifest": len(manifests),
        "n_blotter": len(blotter),
        "baseline_n": 530,
        "n_delta": len(manifests) - 530,
        "sl_points_match_300_count": sl_ok,
        "sl_points_match_pct": round(100.0 * sl_ok / max(len(opens), 1), 2),
        "risk_ccy_unique": sorted({m["risk_ccy"] for m in manifests}),
        "risk_ccy_expected_for_lot_0_01": declared_1r(0.01),
        "joined_exits": sum(1 for op in opens if op.ts.strftime("%Y-%m-%d %H:%M:%S") in exits),
        "event_id_sample": manifests[0]["event_id"] if manifests else None,
        "deterministic_check": manifests[0]["event_id"]
        == event_id(MAGIC, SYMBOL, opens[0].side, opens[0].ts, opens[0].deal)
        if opens
        else False,
        "out_dir": str(out_dir),
    }
    (out_dir / "rebuild_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    s = rebuild()
    print(json.dumps(s, indent=2))
