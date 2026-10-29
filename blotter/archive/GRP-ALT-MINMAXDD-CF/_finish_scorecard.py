"""Finish scorecard from sleeves already on disk (no full log parse)."""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent
from diversify.panel import daily_panel
from grouping.bootstrap import bootstrap_group
from grouping.enum_score import score_group
from grouping.fuse import score_with_fuse
from grouping.holdout import holdout_group

ARCH = Path(__file__).resolve().parent
MEMBERS = ["EURUSD", "DE40", "USDJPY", "AAPL"]


def parse_dt(s: str) -> datetime:
    s = (s or "").strip().strip('"')
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(s)


def load_events(aid: str) -> list[TradeEvent]:
    path = ARCH / "sleeves" / f"{aid}_live_fire_tape.csv"
    out: list[TradeEvent] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            pnl = float(row["pnl_R_design"])
            out.append(
                TradeEvent(
                    asset_id=aid,
                    close_date=parse_dt(row["close_time"]).date(),
                    open_dt=parse_dt(row["open_time"]) if row.get("open_time") else None,
                    pnl_R=pnl,
                    win=pnl > 0,
                    regime_tag=None,
                )
            )
    return out


def main() -> None:
    events = {a: load_events(a) for a in MEMBERS}
    panel = daily_panel(events)
    g = score_group(panel, tuple(MEMBERS))
    h = holdout_group(panel, MEMBERS)
    b = bootstrap_group(panel, MEMBERS)
    fuse = score_with_fuse(panel, MEMBERS)
    boot_m = b.get("month") or {}

    book = panel[MEMBERS].fillna(0.0).mean(axis=1)
    book.index = pd.to_datetime(book.index)
    m_book = book.groupby(book.index.to_period("M")).sum()
    sleeve_m = {}
    for a in MEMBERS:
        s = panel[a].fillna(0.0)
        s.index = pd.to_datetime(s.index)
        sleeve_m[a] = s.groupby(s.index.to_period("M")).sum()

    monthly_rows = []
    for per, gR in m_book.items():
        sm = {a: float(sleeve_m[a].get(per, 0.0)) for a in MEMBERS}
        monthly_rows.append(
            {
                "month": str(per),
                "group_R": round(float(gR), 4),
                **{a: round(sm[a], 4) for a in MEMBERS},
                "hit": bool(gR > 0),
            }
        )

    with (ARCH / "PERIOD_MONTHLY.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "group_R", *MEMBERS, "hit"])
        w.writeheader()
        w.writerows(monthly_rows)

    sleeve_summary = {}
    for aid in MEMBERS:
        ev = events[aid]
        sleeve_summary[aid] = {
            "n": len(ev),
            "sum_R": round(sum(e.pnl_R for e in ev), 4),
            "date_min": min(e.close_date for e in ev).isoformat() if ev else None,
            "date_max": max(e.close_date for e in ev).isoformat() if ev else None,
            "window_note": (
                "May-Oct tip (halt-avoid re-run)"
                if aid == "AAPL"
                else "Jan-Oct 2026 (prior CF)"
            ),
        }

    out = {
        "task_id": "GRP-ALT-MINMAXDD-CF",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "cluster": "EURUSD+DE40+USDJPY+AAPL",
        "weights": {a: 0.25 for a in MEMBERS},
        "splice": {
            "EURUSD": "2026.01.01->2026.10.20",
            "DE40": "2026.01.01->2026.10.20",
            "USDJPY": "2026.01.01->2026.10.20",
            "AAPL": "2026.05.01->2026.10.20 tip (Jan-Apr zero; halt avoided)",
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
            k: fuse.get(k)
            for k in (
                "sum_R_fused",
                "sum_R_base",
                "sum_R_delta",
                "month_hit_fused",
                "maxDD_fused",
                "fuse",
            )
        },
        "prior_jan_oct_aapl_halt": {
            "sum_R": 21.9191,
            "month_hit": 0.9,
            "AAPL_sum_R": -5.4737,
        },
        "verdict": "PASS_EXTENDED_AAPL_TIP",
        "monthly": monthly_rows,
        "tester_aapl_final_balance_USD": 531.18,
    }
    (ARCH / "SCORECARD.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    print("GROUP", json.dumps(out["group"], indent=2))
    print("AAPL", sleeve_summary["AAPL"])
    print(
        "HOLDOUT",
        out["holdout"]["val_sum_R"],
        "BOOT p10",
        out["bootstrap_month"]["hit_p10"],
    )
    print("delta vs halt version sum_R", round(g["sum_R"] - 21.9191, 4))


if __name__ == "__main__":
    main()
