"""AAPL/Apple M5: labeled fire tapes (tip / YTD / prior / long) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG_DIR = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\AAPL\tapes"
)

SL_PTS = 190.0
ATR_MAX = 98.0
R_DESIGN = 280.0 / 190.0  # ≈1.47368
BWR = 1.0 / (1.0 + R_DESIGN)
LEAK_PROXY_PP = 15.3  # single-leg med~29/190 from profile
MAGIC = "26102011"
PRESET = "BMRG-M5-AAPL-6M-Balanced_TPgtSL"
# Tip +$44.50 / (n*E_N) ≈ $3.61 per 1R — label-time proxy only
R_CCY = 3.61

WINDOWS = {
    "ytd": {
        "id": "2026.01.01-2026.10.19",
        "from_prefix": "2026.01.01",
        "to_prefix": "2026.10.",
    },
    "tip": {
        "id": "2026.05.01-2026.10.19",
        "from_prefix": "2026.05.01",
        "to_prefix": "2026.10.",
    },
    "feb_oct": {
        "id": "2026.02.01-2026.10.19",
        "from_prefix": "2026.02.01",
        "to_prefix": "2026.10.",
    },
    "long": {
        "id": "2025.01.01-2026.10.19",
        "from_prefix": "2025.01.01",
        "to_prefix": "2026.10.",
    },
}

# Soft regime map from system_profile_M5 (P1-T05)
REGIME = {
    "2026-01": "HOSTILE",
    "2026-02": "HOSTILE",
    "2026-03": "HOSTILE",
    "2026-04": "HOSTILE",
    "2026-05": "MATCH",
    "2026-06": "SOFT",
    "2026-07": "FRAGILE",
    "2026-08": "SOFT",
    "2026-09": "SOFT",
    "2026-10": "SOFT",
    "2025-01": "SOFT",
    "2025-02": "SOFT",
    "2025-03": "SOFT",
    "2025-04": "SOFT",
    "2025-05": "SOFT",
    "2025-06": "SOFT",
    "2025-07": "SOFT",
    "2025-08": "SOFT",
    "2025-09": "SOFT",
    "2025-10": "SOFT",
    "2025-11": "SOFT",
    "2025-12": "SOFT",
}

HEADER_RE = re.compile(
    r"Tester\tApple,M5[^\n]*from (\d{4}\.\d{2}\.\d{2}) 00:00 to (\d{4}\.\d{2}\.\d{2}) 00:00"
)
re_open = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] OPEN "
    r"(BUY|SELL) lot=([0-9.]+) price=([0-9.]+) sl=([0-9.]+) tp=([0-9.]+)"
    r".*spread=(\d+)"
)
re_bar = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[INFO\] bar="
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}).*ATR=([0-9.]+)pt BBw=([0-9.]+)%"
)
re_tp = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*take profit triggered"
)
re_sl = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*stop loss triggered"
)
re_eot = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*position closed due end of test"
)


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def resolve_log() -> Path:
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.exists():
            raise SystemExit(f"log not found: {p}")
        return p
    preferred = LOG_DIR / "20261020.log"
    if preferred.exists():
        return preferred
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        raise SystemExit(f"no logs in {LOG_DIR}")
    return logs[0]


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_chunk(text: str, from_prefix: str, to_prefix: str) -> str | None:
    """Return last matching Apple M5 magic chunk for from/to prefixes."""
    headers = list(HEADER_RE.finditer(text))
    best: str | None = None
    for i, s in enumerate(headers):
        if not s.group(1).startswith(from_prefix):
            continue
        if not s.group(2).startswith(to_prefix):
            continue
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        ticks = re.search(r"Apple,M5: \d+ ticks", text[s.end() : end])
        if ticks:
            end = min(end, s.end() + ticks.end())
        else:
            tp = text.find("Test passed", s.end(), end)
            if tp != -1:
                end = tp + len("Test passed")
        chunk = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        if mag and mag.group(1) == MAGIC:
            best = chunk
    return best


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return float(sorted_vals[f])
    return float(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f))


def extract(chunk: str, window_id: str, spread_high_thr: int | None = None) -> list[dict]:
    last_bar = None
    open_t = None
    rows: list[dict] = []

    for line in chunk.splitlines():
        mb = re_bar.search(line)
        if mb:
            last_bar = {"atr": float(mb.group(3)), "bbw": float(mb.group(4))}

        mo = re_open.search(line)
        if mo:
            open_t = {
                "open_time": mo.group(1),
                "side": mo.group(2),
                "lot": float(mo.group(3)),
                "entry": float(mo.group(4)),
                "sl": float(mo.group(5)),
                "tp": float(mo.group(6)),
                "spread_pts": int(mo.group(7)),
                "atr_pts": last_bar["atr"] if last_bar else None,
                "bbw_pct": last_bar["bbw"] if last_bar else None,
            }
            continue

        for kind, rx in (("TP", re_tp), ("SL", re_sl), ("EOT", re_eot)):
            mc = rx.search(line)
            if not (mc and open_t):
                continue
            if kind == "EOT":
                open_t = None
                break
            od = parse_dt(open_t["open_time"])
            cd = parse_dt(mc.group(1))
            hold_h = (cd - od).total_seconds() / 3600.0
            win = kind == "TP"
            pnl_r = R_DESIGN if win else -1.0
            month = od.strftime("%Y-%m")
            atr = open_t["atr_pts"]
            tag = REGIME.get(month, "")
            near = int(atr is not None and atr >= 0.9 * ATR_MAX)
            dow = od.strftime("%a")
            hour = od.hour
            spr = open_t["spread_pts"]
            thr = spread_high_thr if spread_high_thr is not None else 10**9
            h1 = int(
                od.year == 2026 and od.month <= 4
            )
            rows.append(
                {
                    **open_t,
                    "close_time": mc.group(1),
                    "exit_reason": kind,
                    "win": int(win),
                    "y_lose": int(not win),
                    "pnl_R_design": round(pnl_r, 6),
                    "pnl_ccy_proxy": round(
                        (R_CCY * R_DESIGN) if win else -R_CCY, 4
                    ),
                    "hold_h": round(hold_h, 4),
                    "dow": dow,
                    "hour": hour,
                    "month": month,
                    "regime_tag": tag,
                    "nights_held": int(hold_h >= 12),
                    "near_atr_cap": near,
                    "cell_dow_wed": int(dow == "Wed"),
                    "cell_h1": h1,
                    "cell_month_jul": int(month == "2026-07"),
                    "cell_spread_high": int(spr >= thr),
                    "cell_month_may": int(month == "2026-05"),
                    "cell_dow_mon": int(dow == "Mon"),
                    "cell_buy": int(open_t["side"] == "BUY"),
                    "cell_sell": int(open_t["side"] == "SELL"),
                    "magic": int(MAGIC),
                    "symbol": "Apple",
                    "preset_id": PRESET,
                    "window": window_id,
                    "tf": "M5",
                }
            )
            open_t = None
            break
    return rows


def annotate_spread_high(rows: list[dict], thr: int) -> list[dict]:
    out = []
    for r in rows:
        rr = dict(r)
        rr["cell_spread_high"] = int(rr["spread_pts"] >= thr)
        out.append(rr)
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise SystemExit(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def cost_proxy(rows: list[dict], window: str, spread_high_thr: int) -> dict:
    spreads = [r["spread_pts"] for r in rows]
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    # single-leg (profile authority) + round-turn stress
    leak_1x = (spr_med / SL_PTS) / (R_DESIGN + 1.0)
    c_R_2x = (2.0 * spr_med) / SL_PTS
    leak_2x = c_R_2x / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    return {
        "task": "AAPL-M5-AOS-P1",
        "window": window,
        "magic": int(MAGIC),
        "symbol": "Apple",
        "tf": "M5",
        "n": len(rows),
        "WR": round(wr, 6),
        "BM_pp": round(bm * 100, 4),
        "E_N": round(wr * (R_DESIGN + 1.0) - 1.0, 6),
        "spread_pts_entry": {
            "median": spr_med,
            "mean": round(spr_mean, 3),
            "min": min(spreads),
            "max": max(spreads),
            "p66": round(percentile(sorted(float(s) for s in spreads), 2 / 3), 3),
            "p80": round(percentile(sorted(float(s) for s in spreads), 0.80), 3),
        },
        "spread_high_thr": spread_high_thr,
        "atr_pts_present": sum(1 for r in rows if r["atr_pts"] is not None),
        "near_atr_cap_n": sum(r["near_atr_cap"] for r in rows),
        "SL_pts": SL_PTS,
        "ATR_max": ATR_MAX,
        "R_design": round(R_DESIGN, 6),
        "BWR": round(BWR, 6),
        "Leak_1x_med_spread_pp": round(leak_1x * 100, 4),
        "Leak_2x_med_spread_pp": round(leak_2x * 100, 4),
        "Leak_profile_pp": LEAK_PROXY_PP,
        "EF_1x_pp": round((bm - leak_1x) * 100, 4),
        "EF_2x_pp": round((bm - leak_2x) * 100, 4),
        "EF_profile_pp": round((bm - LEAK_PROXY_PP / 100.0) * 100, 4),
        "Leak_source": "journal_1x_entry_spread_median",
        "note": (
            "Not full deal blotter. Preset meta Leak 2.1 pp inadmissible. "
            "Profile ~15.3 pp remains Stage-1 authority until measured deals."
        ),
    }


def profile_slices(rows: list[dict], title: str) -> dict:
    def slice_stats(subset: list[dict]) -> dict:
        if not subset:
            return {"n": 0}
        n = len(subset)
        wr = sum(r["win"] for r in subset) / n
        en = sum(r["pnl_R_design"] for r in subset) / n
        return {"n": n, "WR": round(wr, 4), "E_N": round(en, 4)}

    by_side = {
        s: slice_stats([r for r in rows if r["side"] == s]) for s in ("BUY", "SELL")
    }
    by_dow = {
        d: slice_stats([r for r in rows if r["dow"] == d])
        for d in ("Mon", "Tue", "Wed", "Thu", "Fri")
    }
    by_hour = {
        str(h): slice_stats([r for r in rows if r["hour"] == h])
        for h in sorted({r["hour"] for r in rows})
    }
    by_month = {}
    for m in sorted({r["month"] for r in rows}):
        by_month[m] = slice_stats([r for r in rows if r["month"] == m])
        by_month[m]["regime_tag"] = REGIME.get(m, "")
    return {
        "title": title,
        "n": len(rows),
        "WR": round(sum(r["win"] for r in rows) / len(rows), 4),
        "E_N": round(sum(r["pnl_R_design"] for r in rows) / len(rows), 4),
        "by_side": by_side,
        "by_dow": by_dow,
        "by_hour": by_hour,
        "by_month": by_month,
        "cell_dow_wed": slice_stats([r for r in rows if r["cell_dow_wed"] == 1]),
        "cell_h1": slice_stats([r for r in rows if r["cell_h1"] == 1]),
        "cell_month_jul": slice_stats([r for r in rows if r["cell_month_jul"] == 1]),
        "cell_spread_high": slice_stats(
            [r for r in rows if r["cell_spread_high"] == 1]
        ),
        "cell_month_may": slice_stats([r for r in rows if r["cell_month_may"] == 1]),
        "cell_dow_mon": slice_stats([r for r in rows if r["cell_dow_mon"] == 1]),
        "near_atr_cap": slice_stats([r for r in rows if r["near_atr_cap"] == 1]),
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 4
        ),
        "med_hold_h_win": round(
            median([r["hold_h"] for r in rows if r["win"] == 1] or [0]), 4
        ),
        "med_hold_h_lose": round(
            median([r["hold_h"] for r in rows if r["win"] == 0] or [0]), 4
        ),
        "tue_n": sum(1 for r in rows if r["dow"] == "Tue"),
        "atr_missing": sum(1 for r in rows if r["atr_pts"] is None),
        "regime_nonempty": sum(1 for r in rows if r["regime_tag"]),
        "tp_n": sum(1 for r in rows if r["exit_reason"] == "TP"),
        "sl_n": sum(1 for r in rows if r["exit_reason"] == "SL"),
    }


def main() -> None:
    log_path = resolve_log()
    print(f"log={log_path}")
    text = load_text(log_path)
    by_name: dict[str, list[dict]] = {}

    for name, cfg in WINDOWS.items():
        chunk = find_chunk(text, cfg["from_prefix"], cfg["to_prefix"])
        if chunk is None:
            print(f"MISSING chunk {name} {cfg['from_prefix']}->{cfg['to_prefix']}*")
            continue
        hm = HEADER_RE.search(chunk)
        wid = f"{hm.group(1)}-{hm.group(2)}" if hm else cfg["id"]
        # first pass without thr
        rows = extract(chunk, wid, spread_high_thr=None)
        by_name[name] = rows
        print(f"{name}: n={len(rows)} window={wid}")

    if "tip" not in by_name and "ytd" not in by_name:
        raise SystemExit(
            "No Apple M5 tip/ytd chunk (magic 26102011) in log. "
            "Re-run Tester tip May→Oct / YTD then re-run this builder."
        )

    tip_raw = by_name.get("tip")
    ytd_raw = by_name.get("ytd")
    long_raw = by_name.get("long")
    feb_raw = by_name.get("feb_oct")

    # Tip spread is tight (27–31). p66≈median≈29 saturates tip; use p80 (≥30)
    # so cell_spread_high discriminates upper tercile-ish without flagging all fires.
    tip_for_thr = tip_raw or ytd_raw
    assert tip_for_thr is not None
    spr_sorted = sorted(float(r["spread_pts"]) for r in tip_for_thr)
    thr = int(round(percentile(spr_sorted, 0.80)))
    thr = max(thr, 30)  # floor: above tip median 29
    print(f"spread_high_thr_p80_floor30={thr}")

    tip = annotate_spread_high(tip_raw, thr) if tip_raw else None
    ytd = annotate_spread_high(ytd_raw, thr) if ytd_raw else None
    long_rows = annotate_spread_high(long_raw, thr) if long_raw else None
    feb_oct = annotate_spread_high(feb_raw, thr) if feb_raw else None

    long = ytd or long_rows
    assert long is not None

    prior = [
        {**r, "window": "2026.01.01-2026.04.30"}
        for r in long
        if parse_dt(r["open_time"]).month <= 4
        and parse_dt(r["open_time"]).year == 2026
    ]
    tip_core = [
        {**r, "window": "2026.05.01-2026.08.31"}
        for r in (tip or long)
        if parse_dt(r["open_time"]).year == 2026
        and 5 <= parse_dt(r["open_time"]).month <= 8
    ]
    sep_oct = [
        {**r, "window": "2026.09.01-2026.10.19"}
        for r in (tip or long)
        if parse_dt(r["open_time"]).year == 2026
        and parse_dt(r["open_time"]).month >= 9
    ]

    # Archive copies
    write_csv(OUT / "aapl_m5_ytd_fire_tape.csv", long)
    write_csv(OUT / "aapl_m5_prior_fire_tape.csv", prior)
    write_csv(OUT / "aapl_m5_tip_core_fire_tape.csv", tip_core)
    if tip:
        write_csv(OUT / "aapl_m5_tip_fire_tape.csv", tip)
        write_csv(OUT / "aapl_m5_tip_prior_fire_tape.csv", tip + prior)
    if sep_oct:
        write_csv(OUT / "aapl_m5_sep_oct_fire_tape.csv", sep_oct)
    if long_rows:
        write_csv(OUT / "aapl_m5_long_fire_tape.csv", long_rows)
    if feb_oct:
        write_csv(OUT / "aapl_m5_feb_oct_fire_tape.csv", feb_oct)

    # Assets v0
    ASSETS_TAPES.mkdir(parents=True, exist_ok=True)
    write_csv(ASSETS_TAPES / "aapl_m5_ytd_fire_tape_v0.csv", long)
    write_csv(ASSETS_TAPES / "aapl_m5_prior_fire_tape_v0.csv", prior)
    write_csv(ASSETS_TAPES / "aapl_m5_tip_core_fire_tape_v0.csv", tip_core)
    if tip:
        write_csv(ASSETS_TAPES / "aapl_m5_tip_fire_tape_v0.csv", tip)
        write_csv(ASSETS_TAPES / "aapl_m5_tip_prior_fire_tape_v0.csv", tip + prior)
    if sep_oct:
        write_csv(ASSETS_TAPES / "aapl_m5_sep_oct_fire_tape_v0.csv", sep_oct)
    if long_rows:
        write_csv(ASSETS_TAPES / "aapl_m5_long_fire_tape_v0.csv", long_rows)

    cost_rows = tip if tip else tip_core
    cost_win = cost_rows[0]["window"] if cost_rows else "unknown"
    cost = cost_proxy(cost_rows, cost_win, thr)
    (OUT / "COST_PROXY.json").write_text(
        json.dumps(cost, indent=2), encoding="utf-8"
    )

    profiles: dict = {
        "task": "AAPL-M5-AOS-P1",
        "log": str(log_path),
        "spread_high_thr": thr,
        "ytd": profile_slices(long, "ytd"),
        "prior": profile_slices(prior, "prior") if prior else {"n": 0},
        "tip_core": profile_slices(tip_core, "tip_core") if tip_core else {"n": 0},
        "sep_oct": profile_slices(sep_oct, "sep_oct") if sep_oct else {"n": 0},
        "cost_proxy": cost,
        "qa": {
            "tip_n_ge_30": bool(tip and len(tip) >= 30),
            "tip_n": len(tip) if tip else 0,
            "tue_n_tip": sum(1 for r in tip if r["dow"] == "Tue") if tip else None,
            "atr_missing_tip": (
                sum(1 for r in tip if r["atr_pts"] is None) if tip else None
            ),
            "tip_tp_sl_sum": (
                sum(1 for r in tip if r["exit_reason"] in ("TP", "SL")) if tip else None
            ),
        },
    }
    if tip:
        profiles["tip"] = profile_slices(tip, "tip")
    if long_rows:
        profiles["long"] = profile_slices(long_rows, "long")
    (OUT / "TAPE_QA.json").write_text(
        json.dumps(profiles, indent=2), encoding="utf-8"
    )
    summary = {
        k: profiles[k]
        for k in profiles
        if k not in ("cost_proxy", "log")
    }
    print(json.dumps(summary, indent=2))
    print(json.dumps(cost, indent=2))
    print(
        f"ytd={len(long)} prior={len(prior)} tip_core={len(tip_core)} "
        f"tip={len(tip) if tip else 0} sep_oct={len(sep_oct)} "
        f"long={len(long_rows) if long_rows else 0}"
    )


if __name__ == "__main__":
    main()
