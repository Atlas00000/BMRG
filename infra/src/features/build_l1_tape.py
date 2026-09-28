"""
Build offline L1 tape + labels joined to Harvest events (INF-P3-T02…T04).

No skip policy. Fire count must match scoreable engine events.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

_FEAT = Path(__file__).resolve().parent
_INGEST = _FEAT.parent / "ingest"
sys.path.insert(0, str(_FEAT))
sys.path.insert(0, str(_INGEST))

from pit_builder import PitContext, build_features, parse_ts  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
BMRG = INFRA.parent
FIXTURE = INFRA / "fixtures" / "blotter" / "harvest_long_v1"
AOS_FIRES = BMRG / "blotter" / "archive" / "AOS-P1-T02" / "harvest_long_fires.csv"
OUT_TAPE = INFRA / "artefacts" / "tape"
LATEST = OUT_TAPE / "LATEST_REGIME_TAPE.parquet"


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_aos_fires() -> dict[str, dict]:
    if not AOS_FIRES.exists():
        return {}
    df = pd.read_csv(AOS_FIRES)
    out: dict[str, dict] = {}
    for _, row in df.iterrows():
        ts = parse_ts(str(row["t_close"]))
        out[ts.strftime("%Y-%m-%d %H:%M:%S")] = row.to_dict()
    return out


def build_tape(fixture_dir: Path = FIXTURE) -> dict:
    manifests = _load_jsonl(fixture_dir / "event_manifest.jsonl")
    legs = {r["event_id"]: r for r in _load_jsonl(fixture_dir / "blotter_legs.jsonl")}
    aos = _load_aos_fires()

    # Chronological for rolling prior spreads
    events = []
    for m in manifests:
        leg = legs[m["event_id"]]
        entry = parse_ts(leg["entry_time"])
        events.append((entry, m, leg))
    events.sort(key=lambda x: x[0])

    tape_rows: list[dict] = []
    label_rows: list[dict] = []
    prior_spreads: list[float] = []
    n_aos_hit = 0

    for entry, m, leg in events:
        key = entry.strftime("%Y-%m-%d %H:%M:%S")
        aos_row = aos.get(key)
        if aos_row:
            n_aos_hit += 1
        spread = float(leg.get("spread_points_entry") or m.get("spread_points_entry") or 0)
        side = m.get("side") or ("BUY" if leg["direction"] == "long" else "SELL")
        ctx = PitContext(
            entry_time=entry,
            symbol=m.get("symbol") or "EURUSD",
            side=side,
            spread_pts=spread,
            engine_magic=int(m.get("magic") or 8210204),
            structure_id=(aos_row.get("structure_id") if aos_row else None) or "UNK",
            atr_pts=aos_row.get("atr_pts") if aos_row else None,
            bb_width_pct=aos_row.get("bb_width_pct") if aos_row else None,
            prior_spreads=list(prior_spreads),
        )
        feats = build_features(ctx)
        if aos_row is not None:
            # Prefer AOS session tags when present (must still be PIT — derived from same bar)
            feats["session_id"] = aos_row.get("session_id") or feats["session_id"]
            feats["is_tue"] = bool(aos_row.get("is_tue")) if "is_tue" in aos_row else feats["is_tue"]
            if isinstance(aos_row.get("cell_ids"), str):
                feats["cell_ids"] = [c for c in str(aos_row["cell_ids"]).split("|") if c]
        feats["event_id"] = m["event_id"]
        feats["bar_index"] = len(tape_rows)
        tape_rows.append(feats)

        y_lose = 1 if m.get("exit_reason") == "SL" else 0 if m.get("exit_reason") == "TP" else None
        label_rows.append(
            {
                "event_id": m["event_id"],
                "entry_time": entry.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "exit_reason": m.get("exit_reason"),
                "y_lose": y_lose,
                "pnl_r": -1.0 if y_lose == 1 else 1.0 if y_lose == 0 else None,
                "side": side,
                "session_id": feats["session_id"],
                "is_tue": feats["is_tue"],
                "skip_applied": False,  # perception-only
            }
        )
        prior_spreads.append(spread)

    tape_df = pd.DataFrame(tape_rows)
    label_df = pd.DataFrame(label_rows)
    joined = tape_df.merge(label_df, on="event_id", suffixes=("", "_lbl"))

    OUT_TAPE.mkdir(parents=True, exist_ok=True)
    harvest_path = OUT_TAPE / "harvest_l1.parquet"
    labels_path = OUT_TAPE / "harvest_labels.parquet"
    joined_path = OUT_TAPE / "harvest_event_features.parquet"
    tape_df.to_parquet(harvest_path, index=False)
    label_df.to_parquet(labels_path, index=False)
    joined.to_parquet(joined_path, index=False)
    # LATEST pointer for trainer / agent
    joined.to_parquet(LATEST, index=False)

    n = len(tape_df)
    tue = int(tape_df["is_tue"].sum()) if n else 0
    sess_ok = float(tape_df["session_id"].isin(["LON_NY", "NY"]).mean()) if n else 0.0
    coverage = n / max(len(manifests), 1)

    manifest = {
        "task_ids": ["INF-P3-T02", "INF-P3-T03", "INF-P3-T04"],
        "tape_schema": "aos_l1_v0",
        "n_events_source": len(manifests),
        "n_tape_rows": n,
        "n_labels": len(label_df),
        "n_joined": len(joined),
        "coverage": round(coverage, 4),
        "aos_fire_enrich_hits": n_aos_hit,
        "tue_count": tue,
        "session_lon_ny_or_ny_share": round(sess_ok, 4),
        "skips_applied": 0,
        "fire_count_unchanged": True,
        "paths": {
            "tape": str(harvest_path),
            "labels": str(labels_path),
            "joined": str(joined_path),
            "latest_regime_tape": str(LATEST),
        },
        "accept": {
            "coverage_ge_0_95": coverage >= 0.95,
            "tue_eq_0": tue == 0,
            "session_ge_0_95": sess_ok >= 0.95,
            "no_skips": True,
        },
    }
    (OUT_TAPE / "TAPE_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT_TAPE / "LATEST_REGIME_TAPE.manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build_tape(), indent=2))
