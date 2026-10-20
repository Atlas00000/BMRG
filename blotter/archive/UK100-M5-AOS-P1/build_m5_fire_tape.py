"""UK100 M5: labeled fire tapes (tip + prior + long) + journal Leak_proxy."""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261020.log"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)

SL_PTS = 1800.0
ATR_MAX = 869.0
R_DESIGN = 1.25
BWR = 1.0 / (1.0 + R_DESIGN)
MAGIC = 26101905
PRESET = "BMRG-M5-UK100-6M-P0_balanced_chart"
# Design $ proxy: SL1800/2500 * $2.50 ≈ $1.80 per 1R
R_DOLLAR = 1.8

WINDOWS = {
    "tip": {
        "id": "2026.05.01-2026.08.31",
        "expect_n": 116,
        "mark": re.compile(
            r"UK100,M5: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.05\.01 00:00 to 2026\.08\.31 00:00 started with inputs"
        ),
    },
    "long": {
        "id": "2026.01.01-2026.08.31",
        "expect_n": 235,
        "mark": re.compile(
            r"UK100,M5: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.01\.01 00:00 to 2026\.08\.31 00:00 started with inputs"
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
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*take profit triggered.*UK100"
)
re_sl = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*stop loss triggered.*UK100"
)
re_eot = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*position closed due end of test.*UK100"
)
re_pass = re.compile(r"UK100,M5: .* Test passed")

OURO = {
    "2026-05": "MATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
    "2026-09": "MATCH",
    "2026-10": "FRAGILE",
}


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def row_from_open(open_t: dict, close_s: str, kind: str, window_id: str) -> dict:
    od = parse_dt(open_t["open_time"])
    cd = parse_dt(close_s)
    hold_h = (cd - od).total_seconds() / 3600.0
    win = kind == "TP"
    month = od.strftime("%Y-%m")
    atr = open_t["atr_pts"]
    hour = od.hour
    dow = od.strftime("%a")
    pnl_r = R_DESIGN if win else -1.0
    return {
        **open_t,
        "close_time": close_s,
        "exit_reason": kind,
        "win": int(win),
        "pnl_R_design": pnl_r,
        "pnl_ccy_proxy": round(R_DOLLAR * pnl_r, 4),
        "hold_h": round(hold_h, 4),
        "dow": dow,
        "hour": hour,
        "month": month,
        "ouroboros_tag": OURO.get(month, ""),
        "nights_held": int(hold_h >= 12),
        "near_atr_cap": int(atr is not None and atr >= 0.9 * ATR_MAX),
        "cell_dow_mon": int(dow == "Mon"),
        "cell_hour_12_13": int(hour in (12, 13)),
        "cell_month_aug": int(month == "2026-08"),
        "cell_month_feb": int(month == "2026-02"),
        "cell_month_apr": int(month == "2026-04"),
        "cell_buy": int(open_t["side"] == "BUY"),
        "cell_sell": int(open_t["side"] == "SELL"),
        "y_lose": int(not win),
        "magic": MAGIC,
        "symbol": "UK100",
        "tf": "M5",
        "preset_id": PRESET,
        "window": window_id,
    }


def extract(mark: re.Pattern, window_id: str) -> list[dict]:
    in_run = False
    last_bar = None
    open_t = None
    rows: list[dict] = []

    with LOG.open("r", encoding="utf-16", errors="replace") as f:
        for line in f:
            if mark.search(line):
                in_run = True
                open_t = None
                last_bar = None
                continue
            if not in_run:
                continue
            if re_pass.search(line):
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
                if kind != "EOT":
                    rows.append(row_from_open(open_t, mc.group(1), kind, window_id))
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
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    atr_ok = sum(1 for r in rows if r["atr_pts"] is not None)
    return {
        "task": "UK100-M5-AOS-P1",
        "window": "2026.05.01-2026.08.31",
        "magic": MAGIC,
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
        },
        "atr_pts_present": atr_ok,
        "near_atr_cap_n": sum(r["near_atr_cap"] for r in rows),
        "SL_pts": SL_PTS,
        "ATR_max": ATR_MAX,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": 4.0,
        "EF_prior_pp": round((bm - 0.04) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Replace with measured deals when exported."
        ),
    }


def cell_qa(rows: list[dict], name: str) -> dict:
    def wr(mask):
        xs = [r for r in rows if mask(r)]
        if not xs:
            return {"n": 0, "WR": None}
        return {"n": len(xs), "WR": round(sum(r["win"] for r in xs) / len(xs), 4)}

    return {
        "window": name,
        "n": len(rows),
        "WR": round(sum(r["win"] for r in rows) / len(rows), 4),
        "cell_dow_mon": wr(lambda r: r["cell_dow_mon"]),
        "cell_hour_12_13": wr(lambda r: r["cell_hour_12_13"]),
        "cell_month_aug": wr(lambda r: r["cell_month_aug"]),
        "protect_wed": wr(lambda r: r["dow"] == "Wed"),
        "protect_h08_11": wr(lambda r: r["hour"] in (8, 9, 10, 11)),
        "protect_buy": wr(lambda r: r["cell_buy"]),
        "tue_n": sum(1 for r in rows if r["dow"] == "Tue"),
        "ouroboros_nonempty": sum(1 for r in rows if r["ouroboros_tag"]),
        "atr_missing": sum(1 for r in rows if r["atr_pts"] is None),
    }


def main() -> None:
    tip = extract(WINDOWS["tip"]["mark"], WINDOWS["tip"]["id"])
    long = extract(WINDOWS["long"]["mark"], WINDOWS["long"]["id"])
    assert len(tip) == WINDOWS["tip"]["expect_n"], f"tip n={len(tip)}"
    assert len(long) == WINDOWS["long"]["expect_n"], f"long n={len(long)}"

    prior = [
        {**r, "window": "2026.01.01-2026.04.30"}
        for r in long
        if parse_dt(r["open_time"]).month <= 4
    ]

    write_csv(OUT / "uk100_m5_tip_fire_tape.csv", tip)
    write_csv(OUT / "uk100_m5_prior_fire_tape.csv", prior)
    write_csv(OUT / "uk100_m5_long_fire_tape.csv", long)
    tip_prior = tip + prior
    write_csv(OUT / "uk100_m5_tip_prior_fire_tape.csv", tip_prior)

    write_csv(ASSETS_TAPES / "uk100_m5_tip_fire_tape_v0.csv", tip)
    write_csv(ASSETS_TAPES / "uk100_m5_prior_fire_tape_v0.csv", prior)
    write_csv(ASSETS_TAPES / "uk100_m5_long_fire_tape_v0.csv", long)
    write_csv(ASSETS_TAPES / "uk100_m5_tip_prior_fire_tape_v0.csv", tip_prior)

    cost = tip_cost(tip)
    qa = {
        "task": "UK100-M5-AOS-P1",
        "log": str(LOG),
        "tip": cell_qa(tip, "tip"),
        "prior": cell_qa(prior, "prior"),
        "long": cell_qa(long, "long"),
        "cost_proxy": cost,
    }
    (OUT / "COST_PROXY.json").write_text(json.dumps(cost, indent=2), encoding="utf-8")
    (OUT / "TAPE_QA.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    print(json.dumps(qa, indent=2))
    print(
        f"tip={len(tip)} prior={len(prior)} long={len(long)} tip_prior={len(tip_prior)}"
    )


if __name__ == "__main__":
    main()
