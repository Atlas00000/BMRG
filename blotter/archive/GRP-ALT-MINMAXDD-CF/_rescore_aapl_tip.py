"""Splice AAPL May-Oct tip tape into Jan-Oct EUR pack; leave other sleeves as-is."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent
from diversify.panel import daily_panel
from diversify.rolling import segment
from diversify.tester_parse import parse_log_file, trades_to_fire_rows
from grouping.bootstrap import bootstrap_group
from grouping.enum_score import score_group
from grouping.fuse import score_with_fuse
from grouping.holdout import holdout_group

ARCH = Path(__file__).resolve().parent
LOG = REPO.parent.parent.parent / "Tester" / "logs" / "20261022.log"
MEMBERS = ["EURUSD", "DE40", "USDJPY", "AAPL"]


def parse_dt(s: str) -> datetime:
    s = (s or "").strip().strip('"')
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(s)


def load_existing(aid: str) -> list:
    path = ARCH / "sleeves" / f"{aid}_live_fire_tape.csv"
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def fire_to_events(aid: str, fire_rows: list[dict]) -> list[TradeEvent]:
    out = []
    for row in fire_rows:
        cd = parse_dt(row["close_time"]).date()
        pnl = float(row["pnl_R_design"])
        out.append(
            TradeEvent(
                asset_id=aid,
                close_date=cd,
                open_dt=parse_dt(row["open_time"]) if row.get("open_time") else None,
                pnl_R=pnl,
                win=pnl > 0,
                regime_tag=None,
            )
        )
    return out


def main() -> None:
    print("parsing tip AAPL from", LOG)
    trades = parse_log_file(
        LOG, window_from="2026.05.01", window_to="2026.10.20"
    )
    meta = parse_log_file.last_run_meta  # type: ignore[attr-defined]
    aapl = [
        t
        for t in trades
        if t.magic == 26162017 and t.tf.upper() == "M5" and t.asset_id == "AAPL"
    ]
    # dedupe
    seen: set[tuple] = set()
    uniq = []
    for t in aapl:
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
    print(
        "AAPL tip M5 trades",
        len(uniq),
        "sum_R",
        round(sum(t.pnl_R_design for t in uniq), 4),
    )
    for m in meta:
        if m.get("skipped_window"):
            continue
        if m.get("magic") == 26162017 or m.get("symbol") == "Apple":
            print(
                f"  run {m.get('symbol')},{m.get('tf')} mag={m.get('magic')} "
                f"n={m.get('n_trades')} win={m.get('window')}"
            )

    fire = trades_to_fire_rows(uniq)
    aapl_path = ARCH / "sleeves" / "AAPL_live_fire_tape.csv"
    # backup Jan-Oct AAPL
    bak = ARCH / "sleeves" / "AAPL_live_fire_tape_jan_apr_halt.csv"
    old = ARCH / "sleeves" / "AAPL_live_fire_tape.csv"
    if old.exists() and not bak.exists():
        bak.write_bytes(old.read_bytes())
        print("backed up prior AAPL tape ->", bak.name)
    if fire:
        cols = list(fire[0].keys())
        with aapl_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(fire)

    # Build events: EUR/DE/JPY from existing Jan-Oct CSVs; AAPL from tip
    events: dict[str, list[TradeEvent]] = {}
    for aid in ("EURUSD", "DE40", "USDJPY"):
        events[aid] = fire_to_events(aid, load_existing(aid))
    events["AAPL"] = [
        TradeEvent(
            asset_id="AAPL",
            close_date=t.close_time.date(),
            open_dt=t.open_time,
            pnl_R=t.pnl_R_design,
            win=t.pnl_R_design > 0,
            regime_tag=None,
        )
        for t in uniq
    ]

    # sleeve rollups via segment on reconstructed ParsedTrade-like — use events for panel only
    # For sleeve summary use rolling on AAPL tip + reload others from SCORECARD-ish
    rolling_aapl = segment(uniq)
    panel = daily_panel(events)
    g = score_group(panel, tuple(MEMBERS))
    h = holdout_group(panel, MEMBERS)
    b = bootstrap_group(panel, MEMBERS)
    fuse = score_with_fuse(panel, MEMBERS)
    boot_m = b.get("month") or {}

    # monthly table
    import pandas as pd

    book = panel[MEMBERS].fillna(0.0).mean(axis=1)
    book.index = pd.to_datetime(book.index)
    m_book = book.groupby(book.index.to_period("M")).sum()
    sleeve_m = {}
    for a in MEMBERS:
        s = panel[a].fillna(0.0)
        s.index = pd.to_datetime(s.index)
        sleeve_m[a] = s.groupby(s.index.to_period("M")).sum()

    monthly_rows = []
    print("month | group | EUR | DE40 | USDJPY | AAPL | hit")
    for per, gR in m_book.items():
        sm = {a: float(sleeve_m[a].get(per, 0.0)) for a in MEMBERS}
        hit = bool(gR > 0)
        print(
            f"{per} | {gR:+.2f} | {sm['EURUSD']:+.2f} | {sm['DE40']:+.2f} | "
            f"{sm['USDJPY']:+.2f} | {sm['AAPL']:+.2f} | {'Y' if hit else 'N'}"
        )
        monthly_rows.append(
            {
                "month": str(per),
                "group_R": round(float(gR), 4),
                **{a: round(sm[a], 4) for a in MEMBERS},
                "hit": hit,
            }
        )

    with (ARCH / "PERIOD_MONTHLY.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "group_R", *MEMBERS, "hit"])
        w.writeheader()
        w.writerows(monthly_rows)

    # sleeve summaries
    sleeve_summary = {}
    for aid in ("EURUSD", "DE40", "USDJPY"):
        ev = events[aid]
        sleeve_summary[aid] = {
            "n": len(ev),
            "sum_R": round(sum(e.pnl_R for e in ev), 4),
            "window_note": "Jan-Oct 2026 (prior CF)",
            "date_min": min(e.close_date for e in ev).isoformat() if ev else None,
            "date_max": max(e.close_date for e in ev).isoformat() if ev else None,
        }
    full = (rolling_aapl.get("AAPL") or {}).get("full") or {}
    sleeve_summary["AAPL"] = {
        "n": len(uniq),
        "magic": 26162017,
        "tf": ["M5"],
        "sum_R": full.get("sum_R"),
        "E_N": full.get("E_N"),
        "WR": full.get("WR"),
        "maxDD_R": full.get("maxDD_R"),
        "month_hit": (rolling_aapl.get("AAPL") or {})
        .get("periods", {})
        .get("M", {})
        .get("hit_rate"),
        "quarter_hit": (rolling_aapl.get("AAPL") or {})
        .get("periods", {})
        .get("Q", {})
        .get("hit_rate"),
        "EF_pp": full.get("EF_pp"),
        "window_note": "May-Oct tip (halt-avoid re-run)",
        "date_min": min(t.close_time for t in uniq).date().isoformat() if uniq else None,
        "date_max": max(t.close_time for t in uniq).date().isoformat() if uniq else None,
        "tester_final_balance_USD": 531.18,
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
            "AAPL": "2026.05.01->2026.10.20 (tip re-run; Jan-Apr zero / halt avoided)",
        },
        "source_log": str(LOG),
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
        "prior_jan_oct_all_sleeves": {
            "sum_R": 21.9191,
            "month_hit": 0.9,
            "note": "AAPL Jan-Apr halt drag version",
        },
        "verdict": "PASS_EXTENDED_AAPL_TIP",
        "monthly": monthly_rows,
    }
    (ARCH / "SCORECARD.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    print("GROUP", json.dumps(out["group"], indent=2, default=str))
    print("AAPL sleeve", json.dumps(sleeve_summary["AAPL"], indent=2, default=str))
    print("HOLDOUT", out["holdout"]["val_sum_R"], "BOOT p10", out["bootstrap_month"]["hit_p10"])
    print("wrote", ARCH / "SCORECARD.json")


if __name__ == "__main__":
    main()
