"""Idempotent load: adapter pack → Postgres raw/core (+ ops.eval_run)."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

INFRA = Path(__file__).resolve().parents[2]


def db_url() -> str:
    return os.environ.get(
        "BMRG_DATABASE_URL",
        "postgresql+psycopg2://bmrg:bmrg@localhost:54329/bmrg",
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pack_dir(pack_dir: Path, *, source: str = "fixture") -> dict:
    pack_dir = Path(pack_dir)
    meta = json.loads((pack_dir / "ea_metadata.json").read_text(encoding="utf-8"))
    manifests = [
        json.loads(line)
        for line in (pack_dir / "event_manifest.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    legs = [
        json.loads(line)
        for line in (pack_dir / "blotter_legs.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    digest = sha256_file(pack_dir / "event_manifest.jsonl")
    engine = create_engine(db_url())
    now = datetime.now(timezone.utc)

    with engine.begin() as conn:
        # raw landing idempotent on sha256
        existing = conn.execute(
            text("SELECT id FROM raw.landing_file WHERE sha256 = :s"),
            {"s": digest},
        ).fetchone()
        if existing:
            landing_id = existing[0]
            landed_new = False
        else:
            landing_id = conn.execute(
                text(
                    """
                    INSERT INTO raw.landing_file (path, sha256, bytes, source, landed_at, status)
                    VALUES (:p, :s, :b, :src, :t, 'loaded')
                    RETURNING id
                    """
                ),
                {
                    "p": str(pack_dir / "event_manifest.jsonl"),
                    "s": digest,
                    "b": (pack_dir / "event_manifest.jsonl").stat().st_size,
                    "src": source,
                    "t": now,
                },
            ).scalar_one()
            landed_new = True

        conn.execute(
            text(
                """
                INSERT INTO core.ea_metadata (
                  preset_id, magic, ea_name, ea_version, designed_rr, risk_definition,
                  regime_filtered, baseline_frequency, costs_defaulted, geometry_mode,
                  symbol, timeframe, pool_role, payload
                ) VALUES (
                  :preset_id, :magic, :ea_name, :ea_version, :designed_rr, :risk_definition,
                  :regime_filtered, :baseline_frequency, CAST(:costs_defaulted AS json), :geometry_mode,
                  :symbol, :timeframe, :pool_role, CAST(:payload AS json)
                )
                ON CONFLICT (preset_id, magic, ea_version) DO UPDATE SET
                  payload = EXCLUDED.payload,
                  costs_defaulted = EXCLUDED.costs_defaulted
                """
            ),
            {
                "preset_id": meta["preset_id"],
                "magic": meta["magic"],
                "ea_name": meta["ea_name"],
                "ea_version": meta["ea_version"],
                "designed_rr": meta["designed_rr"],
                "risk_definition": meta["risk_definition"],
                "regime_filtered": meta["regime_filtered"],
                "baseline_frequency": meta["baseline_frequency"],
                "costs_defaulted": json.dumps(meta["costs_defaulted"]),
                "geometry_mode": meta["geometry_mode"],
                "symbol": meta["symbol"],
                "timeframe": meta["timeframe"],
                "pool_role": meta.get("pool_role"),
                "payload": json.dumps(meta),
            },
        )

        for m in manifests:
            conn.execute(
                text(
                    """
                    INSERT INTO core.event_manifest (
                      event_id, risk_ccy, equity_at_open, signal_tag, exit_reason,
                      magic, symbol, side, sl_points, volume, tick_value_per_point,
                      equity_source, costs_defaulted
                    ) VALUES (
                      :event_id, :risk_ccy, :equity_at_open, :signal_tag, :exit_reason,
                      :magic, :symbol, :side, :sl_points, :volume, :tick_value_per_point,
                      :equity_source, CAST(:costs_defaulted AS json)
                    )
                    ON CONFLICT (event_id) DO UPDATE SET
                      risk_ccy = EXCLUDED.risk_ccy,
                      equity_at_open = EXCLUDED.equity_at_open,
                      exit_reason = EXCLUDED.exit_reason,
                      costs_defaulted = EXCLUDED.costs_defaulted
                    """
                ),
                {
                    "event_id": m["event_id"],
                    "risk_ccy": m["risk_ccy"],
                    "equity_at_open": m["equity_at_open"],
                    "signal_tag": m.get("signal_tag"),
                    "exit_reason": m.get("exit_reason"),
                    "magic": m.get("magic"),
                    "symbol": m.get("symbol"),
                    "side": m.get("side"),
                    "sl_points": m.get("sl_points"),
                    "volume": m.get("volume"),
                    "tick_value_per_point": m.get("tick_value_per_point"),
                    "equity_source": m.get("equity_source"),
                    "costs_defaulted": json.dumps(m.get("costs_defaulted") or []),
                },
            )

        for leg in legs:
            payload = {
                k: leg.get(k)
                for k in (
                    "costs_defaulted",
                    "cost_component_flags",
                    "spread_points_entry",
                    "bb_dev",
                    "signal_tag",
                    "level_index",
                )
            }
            conn.execute(
                text(
                    """
                    INSERT INTO core.blotter_leg (
                      leg_id, event_id, symbol, direction, entry_time, entry_price,
                      exit_time, exit_price, initial_stop, volume,
                      pnl_gross_ccy, cost_spread_ccy, cost_commission_ccy,
                      cost_swap_ccy, cost_slippage_ccy, pnl_net_ccy, exit_reason, payload
                    ) VALUES (
                      :leg_id, :event_id, :symbol, :direction, :entry_time, :entry_price,
                      :exit_time, :exit_price, :initial_stop, :volume,
                      :pnl_gross_ccy, :cost_spread_ccy, :cost_commission_ccy,
                      :cost_swap_ccy, :cost_slippage_ccy, :pnl_net_ccy, :exit_reason,
                      CAST(:payload AS json)
                    )
                    ON CONFLICT (leg_id) DO UPDATE SET
                      pnl_net_ccy = EXCLUDED.pnl_net_ccy,
                      payload = EXCLUDED.payload
                    """
                ),
                {
                    "leg_id": leg["leg_id"],
                    "event_id": leg["event_id"],
                    "symbol": leg["symbol"],
                    "direction": leg["direction"],
                    "entry_time": datetime.fromisoformat(leg["entry_time"].replace("Z", "+00:00")),
                    "entry_price": leg["entry_price"],
                    "exit_time": datetime.fromisoformat(leg["exit_time"].replace("Z", "+00:00")),
                    "exit_price": leg["exit_price"],
                    "initial_stop": leg.get("initial_stop"),
                    "volume": leg["volume"],
                    "pnl_gross_ccy": leg["pnl_gross_ccy"],
                    "cost_spread_ccy": leg["cost_spread_ccy"],
                    "cost_commission_ccy": leg["cost_commission_ccy"],
                    "cost_swap_ccy": leg["cost_swap_ccy"],
                    "cost_slippage_ccy": leg["cost_slippage_ccy"],
                    "pnl_net_ccy": leg["pnl_net_ccy"],
                    "exit_reason": leg.get("exit_reason"),
                    "payload": json.dumps(payload),
                },
            )

        run_id = f"load-{digest[:12]}-{now.strftime('%Y%m%d%H%M%S')}"
        conn.execute(
            text(
                """
                INSERT INTO ops.eval_run (run_id, recipe_id, baseline_id, scorecard_path, verdict)
                VALUES (:run_id, :recipe_id, :baseline_id, :path, :verdict)
                ON CONFLICT (run_id) DO NOTHING
                """
            ),
            {
                "run_id": run_id,
                "recipe_id": "INF-P2-T02_data_idempotentLoad_HarvestDump",
                "baseline_id": "ENGINE_BASELINE_v1",
                "path": str(pack_dir),
                "verdict": "LOADED",
            },
        )

        n_events = conn.execute(text("SELECT COUNT(*) FROM core.event_manifest")).scalar_one()
        n_legs = conn.execute(text("SELECT COUNT(*) FROM core.blotter_leg")).scalar_one()
        n_land = conn.execute(text("SELECT COUNT(*) FROM raw.landing_file")).scalar_one()

    return {
        "sha256": digest,
        "landing_id": landing_id,
        "landed_new": landed_new,
        "run_id": run_id,
        "n_events": n_events,
        "n_legs": n_legs,
        "n_landing_files": n_land,
        "n_pack_manifest": len(manifests),
        "n_pack_legs": len(legs),
    }


if __name__ == "__main__":
    pack = INFRA / "fixtures" / "blotter" / "harvest_long_v1"
    a = load_pack_dir(pack)
    b = load_pack_dir(pack)
    print(json.dumps({"first": a, "second": b, "idempotent": a["n_events"] == b["n_events"] == a["n_pack_manifest"]}, indent=2))
