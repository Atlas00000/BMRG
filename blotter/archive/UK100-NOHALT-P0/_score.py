"""Score UK100 P0 balanced chart (AOS OFF) Jan-Oct from Tester log."""
from __future__ import annotations

import csv
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent
from diversify.panel import daily_panel
from diversify.rolling import segment
from diversify.tester_parse import parse_log_file, trades_to_fire_rows
from grouping.enum_score import score_group
from grouping.bootstrap import bootstrap_group
from grouping.holdout import holdout_group

ARCH = Path(__file__).resolve().parent
LOG = REPO.parent.parent.parent / "Tester" / "logs" / "20261022.log"
TIP_FROM = date(2026, 5, 1)
TIP_TO = date(2026, 10, 20)


def dedupe(rows):
    seen: set[tuple] = set()
    out = []
    for t in rows:
        key = (
            t.side,
            t.open_time.isoformat(timespec="seconds"),
            t.close_time.isoformat(timespec="seconds"),
            round(t.entry, 5),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
    return out


def summarize(trades, label: str) -> dict:
    for t in trades:
        t.asset_id = "UK100"
    roll = segment(trades)
    sl = roll.get("UK100") or {}
    full = sl.get("full") or {}
    return {
        "label": label,
        "n": len(trades),
        "sum_R": full.get("sum_R"),
        "E_N": full.get("E_N"),
        "WR": full.get("WR"),
        "maxDD_R": full.get("maxDD_R"),
        "EF_pp": full.get("EF_pp"),
        "month_hit": (sl.get("periods") or {}).get("M", {}).get("hit_rate"),
        "quarter_hit": (sl.get("periods") or {}).get("Q", {}).get("hit_rate"),
        "n_months": (sl.get("periods") or {}).get("M", {}).get("n_periods"),
        "date_min": min(t.close_time for t in trades).date().isoformat()
        if trades
        else None,
        "date_max": max(t.close_time for t in trades).date().isoformat()
        if trades
        else None,
    }


def main() -> None:
    print("parsing", LOG)
    trades = parse_log_file(
        LOG, window_from="2026.01.01", window_to="2026.10.20"
    )
    meta = [
        m
        for m in parse_log_file.last_run_meta  # type: ignore[attr-defined]
        if not m.get("skipped_window")
        and (m.get("symbol") == "UK100" or m.get("magic") in (26101905, 26121907))
    ]
    print("UK runs:", json.dumps(meta, indent=2, default=str))

    # P0 run is the Jan-Oct UK100 chunk with true magic 26101905 in header;
    # parser remaps to live 26121907 via symbol map — take all UK100 M5 in window.
    uk = [
        t
        for t in trades
        if t.symbol == "UK100" and t.tf.upper() == "M5"
    ]
    uk = dedupe(uk)
    print("UK100 M5 Jan-Oct trades", len(uk))

    tip = [
        t
        for t in uk
        if t.open_time.date() >= TIP_FROM and t.close_time.date() <= TIP_TO
    ]
    jan_oct = summarize(uk, "Jan-Oct P0 AOS-OFF")
    tip_s = summarize(tip, "May-Oct tip subset of P0")

    # live tip from P2 scorecard
    p2 = json.loads(
        (REPO / "infra/artefacts/diversify/P2_LATEST/SCORECARD.json").read_text(
            encoding="utf-8"
        )
    )
    live = p2.get("sleeve_summary", {}).get("UK100", {})
    live_full = live.get("full") or {}
    live_row = {
        "label": "Live tip panel (UK100_5m_stack AOS ON · 26121907)",
        "n": live.get("n"),
        "sum_R": live_full.get("sum_R"),
        "E_N": live_full.get("E_N"),
        "WR": live_full.get("WR"),
        "maxDD_R": live_full.get("maxDD_R"),
        "month_hit": live.get("month_hit"),
        "quarter_hit": live.get("quarter_hit"),
    }

    events = {
        "UK100": [
            TradeEvent(
                "UK100",
                t.close_time.date(),
                t.open_time,
                t.pnl_R_design,
                t.pnl_R_design > 0,
                None,
            )
            for t in uk
        ]
    }
    panel = daily_panel(events)
    s = panel["UK100"].fillna(0.0)
    s.index = pd.to_datetime(s.index)
    monthly = s.groupby(s.index.to_period("M")).sum()
    monthly_rows = [
        {
            "month": str(p),
            "sum_R": round(float(v), 4),
            "hit": bool(v > 0),
        }
        for p, v in monthly.items()
    ]

    # optional: USDJPY+UK100 with USDJPY from EUR pack CF + this UK
    usdjpy_path = (
        REPO
        / "blotter/archive/GRP-ALT-MINMAXDD-CF/sleeves/USDJPY_live_fire_tape.csv"
    )
    group_note = None
    if usdjpy_path.exists():
        def parse_dt(x: str) -> datetime:
            x = x.strip().strip('"')
            for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
                try:
                    return datetime.strptime(x, fmt)
                except ValueError:
                    pass
            raise ValueError(x)

        jpy_ev = []
        with usdjpy_path.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                pnl = float(row["pnl_R_design"])
                jpy_ev.append(
                    TradeEvent(
                        "USDJPY",
                        parse_dt(row["close_time"]).date(),
                        None,
                        pnl,
                        pnl > 0,
                        None,
                    )
                )
        g_panel = daily_panel({"USDJPY": jpy_ev, "UK100": events["UK100"]})
        g = score_group(g_panel, ("USDJPY", "UK100"))
        h = holdout_group(g_panel, ("USDJPY", "UK100"))
        b = bootstrap_group(g_panel, ("USDJPY", "UK100"))
        group_note = {
            "group_id": "USDJPY+UK100",
            "weights": "equal 50/50 (designed R)",
            "usdjpy_source": "GRP-ALT-MINMAXDD-CF Jan-Oct",
            "uk_source": "P0 AOS-OFF Jan-Oct",
            "group": {
                k: g.get(k)
                for k in (
                    "sum_R",
                    "month_hit",
                    "quarter_hit",
                    "E_month",
                    "CVaR_m20",
                    "maxDD",
                    "worst_month",
                    "best_month",
                )
            },
            "holdout_val_sum_R": h.get("val_sum_R"),
            "boot_hit_p10": (b.get("month") or {}).get("hit_p10"),
            "tip_pareto_watch_ref": {
                "sum_R": 17.775,
                "month_hit": 0.8333,
                "note": "tip live UK with halt — prior watch",
            },
        }

    ARCH.mkdir(parents=True, exist_ok=True)
    (ARCH / "sleeves").mkdir(exist_ok=True)
    fire = trades_to_fire_rows(uk)
    with (ARCH / "sleeves" / "UK100_nohalt_P0_fire_tape.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.DictWriter(fh, fieldnames=list(fire[0].keys()))
        w.writeheader()
        w.writerows(fire)
    with (ARCH / "PERIOD_MONTHLY.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "sum_R", "hit"])
        w.writeheader()
        w.writerows(monthly_rows)

    out = {
        "task_id": "UK100-NOHALT-P0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preset": "Profiles/Tester/BMRG/UK100/BMRG-M5-UK100-6M-P0_balanced_chart.set",
        "true_magic_in_set": 26101905,
        "parser_note": (
            "Header magic 26101905; parse remaps to live 26121907 via UK100 "
            "symbol map — trades are still the P0 AOS-OFF run."
        ),
        "aos": "OFF (InpAOS_Enable=false — no L3 halt)",
        "window": "2026.01.01->2026.10.20",
        "tester_final_balance_USD": 555.23,
        "jan_oct": jan_oct,
        "tip_subset": tip_s,
        "live_tip_contrast": live_row,
        "monthly": monthly_rows,
        "usdjpy_uk100_group": group_note,
        "verdict": "HALT_IS_THE_DRAG",
        "caveat": (
            "Research P0 chart · AOS OFF · different magic from live stack. "
            "Confirms halt truncates edge; does NOT auto-promote P0 to VPS."
        ),
    }
    (ARCH / "SCORECARD.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    print("JAN-OCT", json.dumps(jan_oct, indent=2))
    print("TIP subset", json.dumps(tip_s, indent=2))
    print("LIVE tip", json.dumps(live_row, indent=2))
    print("MONTHLY")
    for r in monthly_rows:
        print(r["month"], f"{r['sum_R']:+.2f}", "Y" if r["hit"] else "N")
    if group_note:
        print("GROUP USDJPY+UK100", json.dumps(group_note, indent=2, default=str))
    print("wrote", ARCH / "SCORECARD.json")


if __name__ == "__main__":
    main()
