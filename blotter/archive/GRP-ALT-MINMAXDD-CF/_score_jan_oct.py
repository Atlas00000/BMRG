"""Score EURUSD+DE40+USDJPY+AAPL on Jan-Oct 2026 Tester journal (one-shot)."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent  # noqa: E402
from diversify.panel import daily_panel  # noqa: E402
from diversify.rolling import segment  # noqa: E402
from diversify.tester_parse import parse_log_file, trades_to_fire_rows  # noqa: E402
from grouping.bootstrap import bootstrap_group  # noqa: E402
from grouping.enum_score import score_group  # noqa: E402
from grouping.fuse import score_with_fuse  # noqa: E402
from grouping.holdout import holdout_group  # noqa: E402

ARCH = Path(__file__).resolve().parent
LOG = REPO.parent.parent.parent / "Tester" / "logs" / "20261022.log"
WANT = {
    8210204: ("EURUSD", "M5"),
    26151907: ("DE40", "M5"),
    26131807: ("USDJPY", "M15"),
    26162017: ("AAPL", "M5"),
}
MEMBERS = ("EURUSD", "DE40", "USDJPY", "AAPL")
FROZEN_TIP = {
    "sum_R": 20.7,
    "month_hit": 1.0,
    "quarter_hit": 1.0,
    "maxDD": -1.13,
    "note": "tip May-Oct equal 25% — not comparable 1:1 to Jan-Oct",
}


def main() -> None:
    print("parsing", LOG, "mb", round(LOG.stat().st_size / 1e6, 1))
    trades = parse_log_file(
        LOG, window_from="2026.01.01", window_to="2026.10.20"
    )
    meta = parse_log_file.last_run_meta  # type: ignore[attr-defined]
    print("raw trades", len(trades), "runs", len(meta))

    for m in meta:
        if m.get("skipped_window"):
            continue
        if m.get("magic") in WANT or m.get("symbol") in (
            "EURUSD",
            "DE30",
            "USDJPY",
            "Apple",
        ):
            print(
                f"  run {m.get('symbol')},{m.get('tf')} mag={m.get('magic')} "
                f"n={m.get('n_trades')} asset={m.get('asset_id')} "
                f"mismatch={m.get('mismatch')}"
            )

    filt = []
    dropped_tf = 0
    dropped_magic = 0
    for t in trades:
        if t.magic not in WANT:
            dropped_magic += 1
            continue
        _aid, exp_tf = WANT[t.magic]
        if t.tf.upper() != exp_tf:
            dropped_tf += 1
            continue
        filt.append(t)
    print("after tf/magic filter", len(filt), "dropped_tf", dropped_tf)

    seen: set[tuple] = set()
    uniq = []
    for t in filt:
        key = (
            t.magic,
            t.side,
            t.open_time.isoformat(timespec="seconds"),
            t.close_time.isoformat(timespec="seconds"),
            round(t.entry, 5),
        )
        if key in seen:
            continue
        seen.add(key)
        uniq.append(t)
    print("deduped", len(uniq))

    by: dict[str, list] = defaultdict(list)
    for t in uniq:
        by[t.asset_id].append(t)

    sleeves_dir = ARCH / "sleeves"
    sleeves_dir.mkdir(parents=True, exist_ok=True)
    sleeve_summary = {}
    events: dict[str, list[TradeEvent]] = {}
    rolling = segment(uniq)

    for aid in MEMBERS:
        rows = by.get(aid, [])
        fire = trades_to_fire_rows(rows)
        if fire:
            path = sleeves_dir / f"{aid}_live_fire_tape.csv"
            cols = list(fire[0].keys())
            with path.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(fire)
        full = (rolling.get(aid) or {}).get("full") or {}
        sleeve_summary[aid] = {
            "n": len(rows),
            "magic": rows[0].magic if rows else None,
            "tf": sorted({t.tf for t in rows}),
            "sum_R": full.get("sum_R"),
            "E_N": full.get("E_N"),
            "WR": full.get("WR"),
            "maxDD_R": full.get("maxDD_R"),
            "month_hit": (rolling.get(aid) or {})
            .get("periods", {})
            .get("M", {})
            .get("hit_rate"),
            "quarter_hit": (rolling.get(aid) or {})
            .get("periods", {})
            .get("Q", {})
            .get("hit_rate"),
            "EF_pp": full.get("EF_pp"),
            "date_min": min(t.close_time for t in rows).date().isoformat()
            if rows
            else None,
            "date_max": max(t.close_time for t in rows).date().isoformat()
            if rows
            else None,
        }
        print(aid, sleeve_summary[aid])
        events[aid] = [
            TradeEvent(
                asset_id=aid,
                close_date=t.close_time.date(),
                open_dt=t.open_time,
                pnl_R=t.pnl_R_design,
                win=t.pnl_R_design > 0,
                regime_tag=None,
            )
            for t in rows
        ]

    missing = [a for a in MEMBERS if not events.get(a)]
    if missing:
        raise SystemExit(f"missing sleeves after filter: {missing}")

    panel = daily_panel(events)
    g = score_group(panel, MEMBERS)
    h = holdout_group(panel, MEMBERS)
    b = bootstrap_group(panel, MEMBERS)
    f = score_with_fuse(panel, MEMBERS)
    boot_m = b.get("month") or {}

    out = {
        "task_id": "GRP-ALT-MINMAXDD-CF",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "cluster": "EURUSD+DE40+USDJPY+AAPL",
        "weights": {a: 0.25 for a in MEMBERS},
        "window": "2026.01.01->2026.10.20",
        "source_log": str(LOG),
        "filters": {
            "magics": list(WANT.keys()),
            "tf_required": {str(k): v[1] for k, v in WANT.items()},
            "dropped_wrong_tf": dropped_tf,
            "note": "Apple M15 / wrong-magic USDJPY discarded",
        },
        "sleeves": sleeve_summary,
        "group": {
            k: g.get(k)
            for k in (
                "group_id",
                "k",
                "n_days",
                "active_days",
                "sum_R",
                "mean_daily_R",
                "month_hit",
                "n_months",
                "quarter_hit",
                "n_quarters",
                "year_hit",
                "E_month",
                "E_quarter",
                "CVaR_m20",
                "worst_month",
                "best_month",
                "maxDD",
                "fuse_days",
                "co_loss",
            )
        },
        "holdout": {
            "val_months": h.get("val_months"),
            "val_sum_R": h.get("val_sum_R"),
            "val_month_hit": h.get("val_month_hit"),
            "fit_month_hit": h.get("fit_month_hit"),
            "val": h.get("val"),
        },
        "bootstrap_month": {
            "hit_p10": boot_m.get("hit_p10"),
            "hit_mean": boot_m.get("hit_mean"),
            "obs_hit": boot_m.get("obs_hit"),
            "sum_p10": boot_m.get("sum_p10"),
        },
        "fuse": {
            k: f.get(k)
            for k in (
                "sum_R_fused",
                "sum_R_base",
                "sum_R_delta",
                "month_hit_fused",
                "maxDD_fused",
                "fuse",
            )
        },
        "frozen_tip_MayOct_reference": FROZEN_TIP,
        "verdict": None,
    }

    gsum = out["group"].get("sum_R") or 0
    mhit = out["group"].get("month_hit") or 0
    out["verdict"] = (
        "PASS_EXTENDED"
        if gsum > 0 and mhit >= 0.67
        else "REVIEW"
    )

    (ARCH / "SCORECARD.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    print("GROUP", json.dumps(out["group"], indent=2, default=str))
    print("HOLDOUT val_sum_R", out["holdout"]["val_sum_R"])
    print("BOOT hit_p10", out["bootstrap_month"]["hit_p10"])
    print("VERDICT", out["verdict"])
    print("wrote", ARCH / "SCORECARD.json")


if __name__ == "__main__":
    main()
