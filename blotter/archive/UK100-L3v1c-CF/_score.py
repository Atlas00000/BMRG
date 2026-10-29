"""Score UK100 L3v1c tip CF (magic 26121907) from Tester journal."""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent
from diversify.panel import daily_panel
from diversify.rolling import segment
from diversify.tester_parse import parse_log_file, trades_to_fire_rows

ARCH = Path(__file__).resolve().parent
LOG = REPO.parent.parent.parent / "Tester" / "logs" / "20261022.log"


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


def summarize(trades: list) -> dict:
    for t in trades:
        t.asset_id = "UK100"
    roll = segment(trades)
    sl = roll.get("UK100") or {}
    full = sl.get("full") or {}
    return {
        "n": len(trades),
        "sum_R": full.get("sum_R"),
        "E_N": full.get("E_N"),
        "WR": full.get("WR"),
        "maxDD_R": full.get("maxDD_R"),
        "EF_pp": full.get("EF_pp"),
        "month_hit": (sl.get("periods") or {}).get("M", {}).get("hit_rate"),
        "quarter_hit": (sl.get("periods") or {}).get("Q", {}).get("hit_rate"),
        "date_min": min(t.close_time for t in trades).date().isoformat()
        if trades
        else None,
        "date_max": max(t.close_time for t in trades).date().isoformat()
        if trades
        else None,
    }


def scan_halt_events(path: Path) -> dict:
    """Stream-decode utf-16 tail/full for L3v1c markers (tip window run ~16:38)."""
    # Read last 40MB — contains the CF run
    size = path.stat().st_size
    start = max(0, size - 40_000_000)
    if start % 2:
        start += 1
    with path.open("rb") as f:
        f.seek(start)
        text = f.read().decode("utf-16-le", errors="replace")

    # Prefer the 16:3x Core block if present
    init_lines = [
        ln
        for ln in text.splitlines()
        if "dualBelow=" in ln or ("BMRG init OK | UK100" in ln and "26121907" in ln)
    ]
    finals = [ln for ln in text.splitlines() if "final balance" in ln and "UK100" in text]
    # crude: last UK100 test passed
    passed = [ln for ln in text.splitlines() if "UK100,M5:" in ln and "Test passed" in ln]

    halt_pat = re.compile(
        r"Entry blocked: AOS L3 (HALT_f0_BELOW_FRONTIER|DERISK_BELOW_CONFIRM|HALT_MAXDD|DERISK_0\.8_DD|DERISK_BELOW)[^\n]*"
    )
    reasons = Counter()
    first_halt = None
    last_halt = None
    max_streak = 0
    streak_re = re.compile(r"streak=(\d+)")
    # only count tip calendar in sim messages
    for ln in text.splitlines():
        if "Entry blocked: AOS L3" not in ln:
            continue
        # extract sim date if present
        m = halt_pat.search(ln)
        if not m:
            continue
        # filter to tip months if date in line
        dm = re.search(r"2026\.(\d{2})\.", ln)
        if dm and int(dm.group(1)) < 5:
            continue
        reason = m.group(1)
        reasons[reason] += 1
        if first_halt is None:
            first_halt = ln[-180:]
        last_halt = ln[-180:]
        sm = streak_re.search(ln)
        if sm:
            max_streak = max(max_streak, int(sm.group(1)))

    return {
        "init_sample": init_lines[-3:] if init_lines else [],
        "test_passed_sample": passed[-2:] if passed else [],
        "halt_reason_counts": dict(reasons),
        "n_halt_block_lines": sum(reasons.values()),
        "first_halt_tipish": first_halt,
        "last_halt_tipish": last_halt,
        "max_below_streak_seen": max_streak,
    }


def main() -> None:
    print("scanning halt markers...")
    halt_meta = scan_halt_events(LOG)
    print("halt counts", halt_meta["halt_reason_counts"])
    print("max streak", halt_meta["max_below_streak_seen"])
    for ln in halt_meta["init_sample"]:
        print("INIT", ln[-220:])

    print("parsing tip window trades...")
    trades = parse_log_file(
        LOG, window_from="2026.05.01", window_to="2026.10.20"
    )
    meta = [
        m
        for m in parse_log_file.last_run_meta  # type: ignore[attr-defined]
        if not m.get("skipped_window")
        and m.get("symbol") == "UK100"
    ]
    print("UK tip-window runs:", json.dumps(meta, indent=2, default=str))

    # Take UK100 M5 trades; prefer those attributed to live magic after remap
    uk = [
        t
        for t in trades
        if t.symbol == "UK100" and t.tf.upper() == "M5"
    ]
    uk = dedupe(uk)
    # Keep only tip open+close (already window-filtered at run level)
    tip = [
        t
        for t in uk
        if t.open_time.date() >= date(2026, 5, 1)
        and t.close_time.date() <= date(2026, 10, 20)
    ]
    tip = dedupe(tip)
    print("tip trades", len(tip))

    stats = summarize(tip)
    print("STATS", json.dumps(stats, indent=2))

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
            for t in tip
        ]
    }
    panel = daily_panel(events)
    s = panel["UK100"].fillna(0.0)
    s.index = pd.to_datetime(s.index)
    monthly = s.groupby(s.index.to_period("M")).sum()
    monthly_rows = [
        {"month": str(p), "sum_R": round(float(v), 4), "hit": bool(v > 0)}
        for p, v in monthly.items()
    ]

    live_prior = {
        "n": 121,
        "sum_R": 20.75,
        "month_hit": 0.6,
        "maxDD_R": -5.75,
        "label": "pre-retune live tip (L3 EN-only)",
    }
    p0 = {
        "n": 153,
        "sum_R": 22.5,
        "month_hit": 0.6667,
        "maxDD_R": -8.0,
        "label": "P0 AOS-OFF tip",
    }

    gates = {
        "n_ge_121": (stats["n"] or 0) >= 121,
        "n_toward_153": (stats["n"] or 0) >= 130,
        "sum_R_ge_20_8": (stats["sum_R"] or 0) >= 20.8,
        "sum_R_toward_22_5": (stats["sum_R"] or 0) >= 22.0,
        "month_hit_ge_60": (stats["month_hit"] or 0) >= 0.6,
        "maxDD_not_worse_than_p0": (stats["maxDD_R"] or 0) >= -8.0 - 1e-9,
    }
    # streak latch finding
    latch_bug = (halt_meta.get("max_below_streak_seen") or 0) > 100

    verdict = "PASS" if all(
        [
            gates["n_ge_121"],
            gates["sum_R_ge_20_8"],
            gates["month_hit_ge_60"],
        ]
    ) else "REVIEW"
    if latch_bug:
        verdict = "PARTIAL_PASS_STREAK_LATCH" if verdict == "PASS" else "FAIL_STREAK_LATCH"

    ARCH.mkdir(parents=True, exist_ok=True)
    (ARCH / "sleeves").mkdir(exist_ok=True)
    if tip:
        fire = trades_to_fire_rows(tip)
        with (ARCH / "sleeves" / "UK100_L3v1c_tip_fire_tape.csv").open(
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
        "task_id": "UK100-L3v1c-CF",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preset": "UK100_5m_stack.set",
        "magic": 26121907,
        "ea_version_target": "1.25",
        "window": "2026.05.01->2026.10.20",
        "tip": stats,
        "monthly": monthly_rows,
        "halt_meta": halt_meta,
        "gates": gates,
        "contrast": {"live_prior": live_prior, "p0_nohalt": p0},
        "findings": {
            "dual_window_wired": True,
            "streak_latch_without_new_closes": latch_bug,
            "note": (
                "Once dual-BELOW trips, no new closes → ring frozen → EN20/EF15 "
                "stuck → belowStreak grows forever. Need time-decay / unlatch or "
                "health eval without new fires."
            ),
        },
        "verdict": verdict,
    }
    (ARCH / "SCORECARD.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    print("GATES", json.dumps(gates, indent=2))
    print("MONTHLY")
    for r in monthly_rows:
        print(r["month"], f"{r['sum_R']:+.2f}", "Y" if r["hit"] else "N")
    print("VERDICT", verdict)


if __name__ == "__main__":
    main()
