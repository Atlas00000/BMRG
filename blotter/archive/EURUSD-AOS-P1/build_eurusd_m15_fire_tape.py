"""EURUSD M15 P2: labeled fire tapes (tip + YTD) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261018.log"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\EURUSD\tapes"
)

SL_PTS = 300.0
ATR_MAX = 74.0
R_DESIGN = 1.25
BWR = 1.0 / (1.0 + R_DESIGN)
R_CCY = 3.0  # ~$3 / 1R @ 0.01 lot (confirm on deals)

WINDOWS = {
    "ytd": {
        "id": "2026.01.01-2026.10.17",
        "expect_n": 72,
        "mark": re.compile(
            r"EURUSD,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.01\.01 00:00 to 2026\.10\.17 00:00 started with inputs"
        ),
    },
    "tip": {
        "id": "2026.05.01-2026.10.17",
        "expect_n": 45,
        "mark": re.compile(
            r"EURUSD,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.05\.01 00:00 to 2026\.10\.17 00:00 started with inputs"
        ),
    },
}

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
re_pass = re.compile(r"EURUSD,M15: .* Test passed|final balance")

OURO = {
    "2026-01": "",
    "2026-02": "",
    "2026-03": "",
    "2026-04": "",
    "2026-05": "MATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
    "2026-09": "MATCH",
    "2026-10": "FRAGILE",
}


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def extract(mark: re.Pattern, window_id: str) -> list[dict]:
    in_run = False
    last_bar = None
    open_t = None
    rows: list[dict] = []
    saw_final = False

    with LOG.open("r", encoding="utf-16", errors="replace") as f:
        for line in f:
            if mark.search(line):
                in_run = True
                open_t = None
                last_bar = None
                saw_final = False
                continue
            if not in_run:
                continue

            # End this run when another Core "started with inputs" begins
            if (
                "started with inputs" in line
                and "EURUSD,M15:" in line
                and not mark.search(line)
            ):
                break
            if "final balance" in line and "Core" in line:
                saw_final = True
                continue
            if saw_final and ("Test passed" in line or "test done" in line.lower()):
                break

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
                month = od.strftime("%Y-%m")
                atr = open_t["atr_pts"]
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
                        "ouroboros_tag": OURO.get(month, ""),
                        "nights_held": int(hold_h >= 12),
                        "near_atr_cap": int(
                            atr is not None and atr >= 0.9 * ATR_MAX
                        ),
                        "cell_dow_thu": int(od.strftime("%a") == "Thu"),
                        "cell_hour_13": int(od.hour == 13),
                        "cell_hour_19": int(od.hour == 19),
                        "cell_month_feb": int(month == "2026-02"),
                        "cell_month_aug": int(month == "2026-08"),
                        "cell_buy": int(open_t["side"] == "BUY"),
                        "magic": 26101817,
                        "symbol": "EURUSD",
                        "tf": "M15",
                        "preset_id": "BMRG-M15-EURUSD-6M-P2_light_selective_chart",
                        "window": window_id,
                    }
                )
                open_t = None
                break
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
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
        "task": "EURUSD-AOS-P1 / P0-T03 proxy",
        "window": "2026.05.01-2026.10.17",
        "magic": 26101817,
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
            "n_missing": sum(1 for r in rows if r["atr_pts"] is None),
        },
        "nights_held_share": round(nights, 4),
        "SL_pts": SL_PTS,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": 3.0,
        "EF_prior_pp": round((bm - 0.03) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Overnight swap still required for measured Leak."
        ),
        "zone": "Fragile" if (bm - leak) > 0 else "Negative_or_fragile",
    }


def cell_qa(rows: list[dict], label: str) -> dict:
    def slice_wr(key: str) -> dict:
        s = [r for r in rows if r[key] == 1]
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
            "cell_hour_13": slice_wr("cell_hour_13"),
            "cell_hour_19": slice_wr("cell_hour_19"),
            "cell_month_feb": slice_wr("cell_month_feb"),
            "cell_month_aug": slice_wr("cell_month_aug"),
            "near_atr_cap": slice_wr("near_atr_cap"),
        },
        "ouroboros": {
            tag: sum(1 for r in rows if r["ouroboros_tag"] == tag)
            for tag in ("MATCH", "FRAGILE", "")
        },
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 3
        ),
    }


def main() -> None:
    by_name: dict[str, list[dict]] = {}
    for name, cfg in WINDOWS.items():
        rows = extract(cfg["mark"], cfg["id"])
        if len(rows) != cfg["expect_n"]:
            print(f"WARN {name}: expected {cfg['expect_n']}, got {len(rows)}")
        by_name[name] = rows
        write_csv(OUT / f"eurusd_m15_{name}_fire_tape.csv", rows)
        write_csv(ASSETS_TAPES / f"eurusd_m15_{name}_fire_tape_v0.csv", rows)
        print(f"{name}: n={len(rows)}")

    # Combined tip+ytd with dedupe (prefer tip window label if duplicate open)
    seen: set[tuple] = set()
    combined: list[dict] = []
    for name in ("tip", "ytd"):
        for r in by_name[name]:
            key = (r["open_time"], r["side"], r["entry"])
            if key in seen:
                continue
            seen.add(key)
            combined.append(r)
    combined.sort(key=lambda r: r["open_time"])
    write_csv(OUT / "eurusd_m15_tip_ytd_fire_tape.csv", combined)
    write_csv(ASSETS_TAPES / "eurusd_m15_tip_ytd_fire_tape_v0.csv", combined)

    tip_rows = by_name["tip"]
    cost = tip_cost(tip_rows)
    (OUT / "COST_PROXY.json").write_text(json.dumps(cost, indent=2), encoding="utf-8")

    qa = {
        "task": "EURUSD-AOS-P1",
        "tip": cell_qa(tip_rows, "tip"),
        "ytd": cell_qa(by_name["ytd"], "ytd"),
        "combined_n": len(combined),
        "cost_proxy": cost,
    }
    (OUT / "TAPE_QA.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    print(json.dumps(qa, indent=2))
    print(f"combined unique n={len(combined)}")


if __name__ == "__main__":
    main()
