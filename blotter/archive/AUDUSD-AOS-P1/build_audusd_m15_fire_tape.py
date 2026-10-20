"""AUDUSD M15 CHAMP: labeled fire tapes (tip + long) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\AUDUSD\tapes"
)

SL_PTS = 300.0
R_DESIGN = 1.0
BWR = 0.50
R_CCY = 3.0  # ~$3 / 1R @ 0.01 lot AUDUSD 300pt
MAGIC = "8230901"
PRESET = "AUDUSD-CHAMP_Harvest_start13_skipMon_G0"

WINDOWS = {
    "tip": {
        "id": "2026.05.01-2026.08.31",
        "expect_n": 41,
        "from": "2026.05.01",
        "to": "2026.08.31",
    },
    "long": {
        "id": "2026.01.01-2026.08.31",
        "expect_n": 95,
        "from": "2026.01.01",
        "to": "2026.08.31",
    },
}

# Soft regime map from system_profile / bad_cells
REGIME = {
    "2026-01": "MATCH",
    "2026-02": "MISMATCH",
    "2026-03": "MISMATCH",
    "2026-04": "MATCH",
    "2026-05": "MISMATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
}

START_RE = re.compile(
    r"AUDUSD,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:"
)
# Any Core "started with inputs" ends the previous run (other symbols too)
ANY_START_RE = re.compile(
    r"[A-Z0-9.]+,M\d+: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from \S+ 00:00 to \S+ 00:00 started with inputs:"
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


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def load_text() -> str:
    raw = LOG.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_chunk(text: str, fro: str, to: str) -> str | None:
    """Return the CHAMP (8230901) run chunk for the given window."""
    for s in START_RE.finditer(text):
        if s.group(1) != fro or s.group(2) != to:
            continue
        # Peek magic in the next ~4k chars of inputs
        head = text[s.start() : s.start() + 8000]
        mag = re.search(r"InpMagic=(\d+)", head)
        if not mag or mag.group(1) != MAGIC:
            continue
        # End at next any-symbol start, else first final balance after opens
        nxt = ANY_START_RE.search(text, s.end())
        end = nxt.start() if nxt else len(text)
        chunk = text[s.start() : end]
        # Trim after this run's final balance (keeps one test only)
        fb = re.search(r"final balance [0-9.]+", chunk)
        if fb:
            # keep a little after for safety
            chunk = chunk[: fb.end() + 200]
        return chunk
    return None


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

        for kind, rx in (("TP", re_tp), ("SL", re_sl)):
            mc = rx.search(line)
            if not (mc and open_t):
                continue
            od = parse_dt(open_t["open_time"])
            cd = parse_dt(mc.group(1))
            hold_h = (cd - od).total_seconds() / 3600.0
            win = kind == "TP"
            month = od.strftime("%Y-%m")
            rows.append(
                {
                    **open_t,
                    "close_time": mc.group(1),
                    "exit_reason": kind,
                    "win": int(win),
                    "y_lose": int(not win),
                    "pnl_R_design": R_DESIGN if win else -1.0,
                    "pnl_ccy_proxy": round(
                        (R_CCY * R_DESIGN) if win else -R_CCY, 4
                    ),
                    "hold_h": round(hold_h, 4),
                    "dow": od.strftime("%a"),
                    "hour": od.hour,
                    "month": month,
                    "regime_tag": REGIME.get(month, ""),
                    "nights_held": int(hold_h >= 12),
                    "cell_dow_thu": int(od.strftime("%a") == "Thu"),
                    "cell_month_may": int(month.endswith("-05")),
                    "cell_month_feb": int(month.endswith("-02")),
                    "cell_month_mar": int(month.endswith("-03")),
                    "cell_buy": int(open_t["side"] == "BUY"),
                    "fast_lose": int((not win) and hold_h < 6.0),
                    "band_ride_proxy": int((not win) and hold_h < 8.0),
                    "magic": int(MAGIC),
                    "symbol": "AUDUSD",
                    "tf": "M15",
                    "preset_id": PRESET,
                    "window": window_id,
                }
            )
            open_t = None
            break
    return rows


def add_near_atr(rows: list[dict], tip_atr_p75: float | None) -> None:
    thr = tip_atr_p75
    for r in rows:
        atr = r["atr_pts"]
        r["near_atr_high"] = int(
            atr is not None and thr is not None and atr >= thr
        )


def atr_p75(rows: list[dict]) -> float | None:
    atrs = sorted(r["atr_pts"] for r in rows if r["atr_pts"] is not None)
    if not atrs:
        return None
    idx = int(0.75 * (len(atrs) - 1))
    return float(atrs[idx])


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # stable column order
    keys = list(rows[0].keys())
    # ensure near_atr_high present near other cells
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def tip_cost(rows: list[dict]) -> dict:
    spreads = [r["spread_pts"] for r in rows]
    atrs = [r["atr_pts"] for r in rows if r["atr_pts"] is not None]
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    nights = sum(r["nights_held"] for r in rows) / len(rows)
    return {
        "task": "AUDUSD-AOS-P1 / P0-T03 proxy",
        "window": "2026.05.01-2026.08.31",
        "magic": int(MAGIC),
        "n": len(rows),
        "WR": round(wr, 6),
        "BM_pp": round(bm * 100, 4),
        "E_N": round(wr * (R_DESIGN + 1.0) - 1.0, 6),
        "spread_pts_entry": {
            "median": spr_med,
            "mean": round(spr_mean, 3),
            "min": min(spreads),
            "max": max(spreads),
        },
        "atr_pts_entry": {
            "median": round(float(median(atrs)), 2) if atrs else None,
            "mean": round(float(mean(atrs)), 2) if atrs else None,
            "p75": atr_p75(rows),
            "n_missing": sum(1 for r in rows if r["atr_pts"] is None),
        },
        "nights_held_share": round(nights, 4),
        "SL_pts": SL_PTS,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": 2.4,
        "EF_prior_pp": round((bm - 0.024) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Overnight swap still required for measured Leak."
        ),
        "zone": "Robust_proxy" if (bm - leak) > 0.05 else "Fragile",
    }


def cell_qa(rows: list[dict], label: str) -> dict:
    def slice_wr(key: str) -> dict:
        s = [r for r in rows if r.get(key) == 1]
        if not s:
            return {"n": 0}
        wr = sum(r["win"] for r in s) / len(s)
        return {
            "n": len(s),
            "WR": round(100 * wr, 1),
            "E_N": round(wr * (R_DESIGN + 1.0) - 1.0, 3),
        }

    return {
        "window": label,
        "n": len(rows),
        "WR": round(100 * sum(r["win"] for r in rows) / len(rows), 1),
        "atr_missing": sum(1 for r in rows if r["atr_pts"] is None),
        "cells": {
            "cell_buy": slice_wr("cell_buy"),
            "cell_dow_thu": slice_wr("cell_dow_thu"),
            "cell_month_may": slice_wr("cell_month_may"),
            "cell_month_feb": slice_wr("cell_month_feb"),
            "cell_month_mar": slice_wr("cell_month_mar"),
            "near_atr_high": slice_wr("near_atr_high"),
            "fast_lose": slice_wr("fast_lose"),
            "band_ride_proxy": slice_wr("band_ride_proxy"),
        },
        "regime": {
            tag: sum(1 for r in rows if r["regime_tag"] == tag)
            for tag in ("MATCH", "MISMATCH", "")
        },
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 3
        ),
        "fast_lose_share": round(
            sum(r["fast_lose"] for r in rows) / len(rows), 3
        ),
    }


def main() -> None:
    text = load_text()
    by_name: dict[str, list[dict]] = {}
    for name, cfg in WINDOWS.items():
        chunk = find_chunk(text, cfg["from"], cfg["to"])
        if not chunk:
            raise SystemExit(f"missing CHAMP chunk for {name} {cfg['id']}")
        rows = extract(chunk, cfg["id"])
        if len(rows) != cfg["expect_n"]:
            print(f"WARN {name}: expected {cfg['expect_n']}, got {len(rows)}")
        by_name[name] = rows
        print(f"{name}: n={len(rows)}")

    tip_p75 = atr_p75(by_name["tip"])
    for name in by_name:
        add_near_atr(by_name[name], tip_p75)
        # rebuild row dicts with near_atr in stable place — already mutated
        write_csv(OUT / f"audusd_m15_{name}_fire_tape.csv", by_name[name])
        write_csv(
            ASSETS_TAPES / f"audusd_m15_{name}_fire_tape_v0.csv", by_name[name]
        )

    seen: set[tuple] = set()
    combined: list[dict] = []
    for name in ("tip", "long"):
        for r in by_name[name]:
            key = (r["open_time"], r["side"], r["entry"])
            if key in seen:
                continue
            seen.add(key)
            combined.append(r)
    combined.sort(key=lambda r: r["open_time"])
    write_csv(OUT / "audusd_m15_tip_long_fire_tape.csv", combined)
    write_csv(ASSETS_TAPES / "audusd_m15_tip_long_fire_tape_v0.csv", combined)

    tip_rows = by_name["tip"]
    cost = tip_cost(tip_rows)
    (OUT / "COST_PROXY.json").write_text(
        json.dumps(cost, indent=2), encoding="utf-8"
    )

    qa = {
        "task": "AUDUSD-AOS-P1",
        "tip_atr_p75": tip_p75,
        "tip": cell_qa(tip_rows, "tip"),
        "long": cell_qa(by_name["long"], "long"),
        "combined_n": len(combined),
        "cost_proxy": cost,
        "p1_tasks": {
            "T01_schema": "DONE",
            "T02_builder": "DONE",
            "T03_labels": "DONE",
            "T04_structure": "DONE_proxy",
            "T05_regime": "DONE",
        },
    }
    (OUT / "TAPE_QA.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    print(json.dumps(qa, indent=2))
    print(f"combined unique n={len(combined)} tip_atr_p75={tip_p75}")


if __name__ == "__main__":
    main()
