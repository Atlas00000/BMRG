"""USDJPY M15: labeled fire tapes (tip + YTD + long) + journal Leak proxy.

Parses Tester journal for magic 26101828 Balanced P0.
Supports dedicated tip/YTD windows OR long re-smokes filtered by open_time.
"""
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\USDJPY\tapes"
)

SL_PTS = 100.0
ATR_MAX = 70.0
R_DESIGN = 1.20
BWR = 1.0 / (1.0 + R_DESIGN)
MAGIC = "26101828"
PRESET = "BMRG-M15-USDJPY-6M-P0_balanced_chart"
LEAK_PRIOR_PP = 11.4

# Date filters for OS compare windows (open_time)
TIP_FROM, TIP_TO = "2026.05.01", "2026.08.31"
YTD_FROM, YTD_TO = "2026.01.01", "2026.10.19"
BASELINE_TIP_N, BASELINE_YTD_N = 56, 68

OURO = {
    "2025-04": "MATCH",
    "2025-05": "MATCH",
    "2025-06": "MATCH",
    "2025-07": "MATCH",
    "2025-08": "MATCH",
    "2025-09": "FRAGILE",
    "2025-10": "MATCH",
    "2025-11": "MATCH",
    "2025-12": "MATCH",
    "2026-01": "MATCH",
    "2026-02": "MATCH",
    "2026-03": "MATCH",
    "2026-04": "MATCH",
    "2026-05": "MATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
    "2026-09": "FRAGILE",
    "2026-10": "FRAGILE",
}

START_RE = re.compile(
    r"USDJPY,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+)(?:\s+\d{2}:\d{2})?\s+to (\S+)(?:\s+\d{2}:\d{2})?"
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
re_final = re.compile(r"final balance\s+([0-9.]+)")


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def latest_log() -> Path:
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        raise SystemExit(f"no logs in {LOG_DIR}")
    return logs[0]


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    if b"\x00" in raw[:200]:
        try:
            return raw.decode("utf-16-le")
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def iter_chunks(text: str) -> list[tuple[str, str, str]]:
    """Return list of (from, to, chunk) for magic matches."""
    starts = list(START_RE.finditer(text))
    out: list[tuple[str, str, str]] = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        chunk = text[s.start() : end]
        other = re.search(
            r"(?:EURUSD|DE30|AUDUSD|UK100|Apple|GBPJPY|XAUUSD),M15: testing of Experts\\BMRG",
            chunk[2000:],
        )
        if other:
            chunk = chunk[: 2000 + other.start()]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        if mag and mag.group(1) == MAGIC:
            out.append((s.group(1), s.group(2), chunk))
    return out


def extract(chunk: str, window_id: str) -> list[dict]:
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
            tag = OURO.get(month, "")
            near = int(atr is not None and atr >= 0.9 * ATR_MAX)
            sell = int(open_t["side"] == "SELL")
            rows.append(
                {
                    **open_t,
                    "close_time": mc.group(1),
                    "exit_reason": kind,
                    "win": int(win),
                    "y_lose": int(not win),
                    "pnl_R_design": pnl_r,
                    "hold_h": round(hold_h, 4),
                    "dow": od.strftime("%a"),
                    "hour": od.hour,
                    "month": month,
                    "ouroboros_tag": tag,
                    "nights_held": int(hold_h >= 12),
                    "near_atr_cap": near,
                    "cell_dow_thu": int(od.strftime("%a") == "Thu"),
                    "cell_hour_14": int(od.hour == 14),
                    "cell_month_jul": int(month == "2026-07"),
                    "cell_sell": sell,
                    "cell_sell_near_atr": int(sell and near),
                    "cell_fragile": int(tag == "FRAGILE"),
                    "magic": int(MAGIC),
                    "symbol": "USDJPY",
                    "preset_id": PRESET,
                    "window": window_id,
                    "tf": "M15",
                }
            )
            open_t = None
            break
    return rows


def in_range(open_time: str, fro: str, to: str) -> bool:
    d = open_time[:10]
    return fro <= d <= to


def filter_rows(rows: list[dict], fro: str, to: str, window_id: str) -> list[dict]:
    out = []
    for r in rows:
        if in_range(r["open_time"], fro, to):
            rr = dict(r)
            rr["window"] = window_id
            out.append(rr)
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise SystemExit(f"refusing empty write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def tip_cost(rows: list[dict]) -> dict:
    spreads = [r["spread_pts"] for r in rows]
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    return {
        "task": "USDJPY-AOS-P1",
        "window": f"{TIP_FROM}-{TIP_TO}",
        "magic": int(MAGIC),
        "symbol": "USDJPY",
        "n": len(rows),
        "baseline_tip_n": BASELINE_TIP_N,
        "WR": round(wr, 6),
        "BM_pp": round(bm * 100, 4),
        "E_N": round(wr * (R_DESIGN + 1.0) - 1.0, 6),
        "spread_pts_entry": {
            "median": spr_med,
            "mean": round(spr_mean, 3),
            "min": min(spreads),
            "max": max(spreads),
        },
        "SL_pts": SL_PTS,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": LEAK_PRIOR_PP,
        "EF_prior_pp": round((bm - LEAK_PRIOR_PP / 100.0) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter. Journal 2×spread proxy is diagnostic only. "
            "Prior 11.4 pp remains Stage-1 authority until deal export. "
            "Tip filtered from long re-smoke may differ from dedicated May→Aug n=56 "
            "(path dependency) — report n and use for L1/P2 CF with note."
        ),
        "zone": "costs_fragile_until_measured",
    }


def profile_slices(rows: list[dict], title: str) -> dict:
    def slice_stats(subset: list[dict]) -> dict:
        if not subset:
            return {"n": 0}
        n = len(subset)
        wr = sum(r["win"] for r in subset) / n
        en = sum(r["pnl_R_design"] for r in subset) / n
        return {"n": n, "WR": round(wr, 4), "E_N": round(en, 4)}

    return {
        "title": title,
        "n": len(rows),
        "by_side": {
            s: slice_stats([r for r in rows if r["side"] == s]) for s in ("BUY", "SELL")
        },
        "by_dow": {
            d: slice_stats([r for r in rows if r["dow"] == d])
            for d in ("Mon", "Tue", "Wed", "Thu", "Fri")
        },
        "by_hour": {
            str(h): slice_stats([r for r in rows if r["hour"] == h])
            for h in sorted({r["hour"] for r in rows})
        },
        "by_month": {
            m: {
                **slice_stats([r for r in rows if r["month"] == m]),
                "ouroboros_tag": OURO.get(m, ""),
            }
            for m in sorted({r["month"] for r in rows})
        },
        "near_atr_cap": slice_stats([r for r in rows if r["near_atr_cap"] == 1]),
        "cell_dow_thu": slice_stats([r for r in rows if r["cell_dow_thu"] == 1]),
        "cell_hour_14": slice_stats([r for r in rows if r["cell_hour_14"] == 1]),
        "cell_month_jul": slice_stats([r for r in rows if r["cell_month_jul"] == 1]),
        "cell_sell_near_atr": slice_stats(
            [r for r in rows if r["cell_sell_near_atr"] == 1]
        ),
        "nights_held_share": round(sum(r["nights_held"] for r in rows) / len(rows), 4),
        "med_hold_h_win": round(
            median([r["hold_h"] for r in rows if r["win"] == 1] or [0]), 4
        ),
        "med_hold_h_lose": round(
            median([r["hold_h"] for r in rows if r["win"] == 0] or [0]), 4
        ),
        "atr_missing": sum(1 for r in rows if r["atr_pts"] is None),
    }


def dedupe_combined(tip: list[dict], ytd: list[dict]) -> list[dict]:
    keys = {(r["open_time"], r["side"]) for r in tip}
    out = list(tip)
    for r in ytd:
        k = (r["open_time"], r["side"])
        if k not in keys:
            out.append(r)
            keys.add(k)
    out.sort(key=lambda r: r["open_time"])
    return out


def pick_source_chunk(
    chunks: list[tuple[str, str, str]],
) -> tuple[str, str, list[dict]]:
    """Prefer longest covering run that includes tip+YTD calendar."""
    scored: list[tuple[int, str, str, list[dict]]] = []
    for fro, to, chunk in chunks:
        wid = f"{fro}-{to}"
        rows = extract(chunk, wid)
        tip_n = sum(1 for r in rows if in_range(r["open_time"], TIP_FROM, TIP_TO))
        ytd_n = sum(1 for r in rows if in_range(r["open_time"], YTD_FROM, YTD_TO))
        score = tip_n * 1000 + ytd_n * 10 + len(rows)
        scored.append((score, fro, to, rows))
        fin = re_final.search(chunk)
        print(
            f"chunk {fro}->{to}: n={len(rows)} tip_range={tip_n} ytd_range={ytd_n} "
            f"final={fin.group(1) if fin else '?'}"
        )
    if not scored:
        raise SystemExit("no magic chunks")
    scored.sort(key=lambda x: x[0], reverse=True)
    _, fro, to, rows = scored[0]
    print(f"selected source {fro}->{to} n={len(rows)}")
    return fro, to, rows


def main() -> None:
    log = (
        Path(sys.argv[1])
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-")
        else latest_log()
    )
    print(f"log={log} size={log.stat().st_size}")
    text = load_text(log)
    chunks = iter_chunks(text)
    print(f"USDJPY magic={MAGIC} chunks: {len(chunks)}")
    if not chunks:
        raise SystemExit(
            "No USDJPY magic=26101828 chunks. Re-smoke tip/YTD then re-run."
        )

    src_from, src_to, all_rows = pick_source_chunk(chunks)
    tip = filter_rows(all_rows, TIP_FROM, TIP_TO, f"{TIP_FROM}-{TIP_TO}")
    ytd = filter_rows(all_rows, YTD_FROM, YTD_TO, f"{YTD_FROM}-{YTD_TO}")

    if len(tip) != BASELINE_TIP_N:
        print(
            f"WARN tip n={len(tip)} vs baseline {BASELINE_TIP_N} "
            f"(long-window path dependency — OK for L1 with note)"
        )
    if len(ytd) != BASELINE_YTD_N:
        print(
            f"WARN ytd n={len(ytd)} vs baseline {BASELINE_YTD_N} "
            f"(long-window path dependency — OK for L1 with note)"
        )

    write_csv(OUT / "usdjpy_tip_fire_tape.csv", tip)
    write_csv(ASSETS_TAPES / "usdjpy_tip_fire_tape_v0.csv", tip)
    write_csv(OUT / "usdjpy_ytd_fire_tape.csv", ytd)
    write_csv(ASSETS_TAPES / "usdjpy_ytd_fire_tape_v0.csv", ytd)
    write_csv(OUT / "usdjpy_long_fire_tape.csv", all_rows)
    write_csv(ASSETS_TAPES / "usdjpy_long_fire_tape_v0.csv", all_rows)

    combined = dedupe_combined(tip, ytd)
    write_csv(OUT / "usdjpy_tip_ytd_fire_tape.csv", combined)
    write_csv(ASSETS_TAPES / "usdjpy_tip_ytd_fire_tape_v0.csv", combined)

    cost = tip_cost(tip)
    cost["source_tester_window"] = f"{src_from}-{src_to}"
    (OUT / "COST_PROXY.json").write_text(json.dumps(cost, indent=2), encoding="utf-8")
    print(json.dumps(cost, indent=2))

    profiles = {
        "source_tester_window": f"{src_from}-{src_to}",
        "tip": profile_slices(tip, "tip"),
        "ytd": profile_slices(ytd, "ytd"),
        "long": profile_slices(all_rows, "long"),
    }
    (OUT / "TAPE_QA.json").write_text(json.dumps(profiles, indent=2), encoding="utf-8")
    print(f"combined n={len(combined)}")
    print("tip side", profiles["tip"]["by_side"])
    print("tip dow", {k: v for k, v in profiles["tip"]["by_dow"].items() if v.get("n")})
    print("tip jul", profiles["tip"]["cell_month_jul"])
    print("atr_missing tip", profiles["tip"]["atr_missing"])


if __name__ == "__main__":
    main()
