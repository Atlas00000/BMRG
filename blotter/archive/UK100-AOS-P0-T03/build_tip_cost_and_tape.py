"""UK100: journal Leak_proxy (tip) + labeled fire tapes (tip + prior)."""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261012.log"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)

SL_PTS = 2500.0
R_DESIGN = 1.25
BWR = 1.0 / (1.0 + R_DESIGN)

WINDOWS = {
    "tip": {
        "id": "2026.05.01-2026.08.31",
        "expect_n": 51,
        "mark": re.compile(
            r"UK100,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.05\.01 00:00 to 2026\.08\.31 00:00 started with inputs"
        ),
    },
    "prior": {
        "id": "2026.01.01-2026.04.30",
        "expect_n": 75,
        "mark": re.compile(
            r"UK100,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from 2026\.01\.01 00:00 to 2026\.04\.30 00:00 started with inputs"
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
re_pass = re.compile(r"UK100,M15: .* Test passed")

OURO = {
    "2026-05": "MATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
}


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


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
                            "pnl_R_design": R_DESIGN if win else -1.0,
                            "pnl_ccy_proxy": round(
                                (2.5 * R_DESIGN) if win else -2.5, 4
                            ),
                            "hold_h": round(hold_h, 4),
                            "dow": od.strftime("%a"),
                            "hour": od.hour,
                            "month": month,
                            "ouroboros_tag": OURO.get(month, ""),
                            "nights_held": int(hold_h >= 12),
                            "near_atr_cap": int(
                                atr is not None and atr >= 0.9 * 1470
                            ),
                            "cell_dow_thu": int(od.strftime("%a") == "Thu"),
                            "cell_hour_08": int(od.hour == 8),
                            "cell_month_jul": int(month == "2026-07"),
                            "cell_buy": int(open_t["side"] == "BUY"),
                            "magic": 26101201,
                            "symbol": "UK100",
                            "preset_id": "BMRG-M15-UK100-6M-P0_balanced_chart",
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
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    return {
        "task": "UK100-AOS-P0-T03",
        "window": "2026.05.01-2026.08.31",
        "magic": 26101201,
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
        "SL_pts": SL_PTS,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": 2.9,
        "EF_prior_pp": round((bm - 0.029) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Replace with measured deals when exported."
        ),
        "zone": "Fragile",
    }


def main() -> None:
    all_rows: list[dict] = []
    for name, cfg in WINDOWS.items():
        rows = extract(cfg["mark"], cfg["id"])
        assert len(rows) == cfg["expect_n"], (
            f"{name}: expected {cfg['expect_n']}, got {len(rows)}"
        )
        write_csv(OUT / f"uk100_{name}_fire_tape.csv", rows)
        write_csv(ASSETS_TAPES / f"uk100_{name}_fire_tape_v0.csv", rows)
        all_rows.extend(rows)
        print(f"{name}: n={len(rows)}")

    write_csv(OUT / "uk100_tip_prior_fire_tape.csv", all_rows)
    write_csv(ASSETS_TAPES / "uk100_tip_prior_fire_tape_v0.csv", all_rows)

    tip_rows = [r for r in all_rows if r["window"] == WINDOWS["tip"]["id"]]
    cost = tip_cost(tip_rows)
    (OUT / "COST_PROXY.json").write_text(json.dumps(cost, indent=2), encoding="utf-8")
    print(json.dumps(cost, indent=2))
    print(f"combined n={len(all_rows)}")


if __name__ == "__main__":
    main()
