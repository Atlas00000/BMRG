"""JP225 tip deal-fill Leak measure (magic 26101904 · May→Aug).

Sources entry spread from [BMRG][TRADE] OPEN and exit adverse slip from
trigger vs deal fill. Commission/swap absent in Tester journal → 0.
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent
ASSETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\JP225"
)

SL_PTS = 23260.0
R = 1.50
BWR = 1.0 / (1.0 + R)
POINT = 0.01
LEAK_PRIOR = 0.043
MAGIC = "26101904"

START_RE = re.compile(
    r"JPN225,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:"
)
re_open = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] OPEN "
    r"(BUY|SELL) lot=([0-9.]+) price=([0-9.]+) sl=([0-9.]+) tp=([0-9.]+)"
    r".*spread=(\d+) deal=(\d+)"
)
re_tp = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*take profit triggered #(\d+) "
    r"(buy|sell) .*JPN225 .* tp: ([\d.]+) \[#(\d+) "
)
re_sl = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*stop loss triggered #(\d+) "
    r"(buy|sell) .*JPN225 .* sl: ([\d.]+).*\[#(\d+)"
)
re_deal = re.compile(
    r"deal #(\d+) (buy|sell) .*JPN225 at ([\d.]+) done"
)


def load_text() -> str:
    raw = LOG.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_tip_chunk(text: str) -> str:
    for m in START_RE.finditer(text):
        if m.group(1) != "2026.05.01" or m.group(2) != "2026.08.31":
            continue
        end = text.find("final balance", m.start())
        chunk = text[m.start() : end if end > 0 else m.start() + 5_000_000]
        if f"InpMagic={MAGIC}" in chunk[:12000]:
            return chunk
    raise SystemExit("tip chunk not found")


def adverse_exit_slip(side: str, trigger: float, fill: float) -> float:
    """Points against trader on exit fill vs trigger."""
    if side == "BUY":
        # close = sell; lower fill is adverse
        return max(0.0, (trigger - fill) / POINT)
    # SELL close = buy; higher fill is adverse
    return max(0.0, (fill - trigger) / POINT)


def net_exit_slip(side: str, trigger: float, fill: float) -> float:
    """Signed: +adverse / −favorable in points."""
    if side == "BUY":
        return (trigger - fill) / POINT
    return (fill - trigger) / POINT


def extract(chunk: str) -> list[dict]:
    open_t = None
    pending_close = None  # wait for exit deal
    deals: dict[int, tuple[str, float]] = {}
    rows: list[dict] = []

    for line in chunk.splitlines():
        md = re_deal.search(line)
        if md:
            did = int(md.group(1))
            deals[did] = (md.group(2).upper(), float(md.group(3)))
            if pending_close and did == pending_close["exit_deal"]:
                side = pending_close["side"]
                trig = pending_close["trigger"]
                fill = float(md.group(3))
                adv = adverse_exit_slip(side, trig, fill)
                net = net_exit_slip(side, trig, fill)
                cost = pending_close["spread_pts"] + adv
                rows.append(
                    {
                        **{k: pending_close[k] for k in (
                            "open_time",
                            "close_time",
                            "side",
                            "entry",
                            "sl",
                            "tp",
                            "spread_pts",
                            "exit_reason",
                            "win",
                            "month",
                        )},
                        "exit_trigger": trig,
                        "exit_fill": fill,
                        "exit_adverse_slip_pts": round(adv, 2),
                        "exit_net_slip_pts": round(net, 2),
                        "commission_pts": 0.0,
                        "swap_pts": 0.0,
                        "cost_pts_rt": round(cost, 2),
                        "c_R": round(cost / SL_PTS, 6),
                    }
                )
                pending_close = None
                open_t = None
            continue

        mo = re_open.search(line)
        if mo:
            open_t = {
                "open_time": mo.group(1),
                "side": mo.group(2),
                "entry": float(mo.group(4)),
                "sl": float(mo.group(5)),
                "tp": float(mo.group(6)),
                "spread_pts": int(mo.group(7)),
                "open_deal": int(mo.group(8)),
            }
            continue

        for kind, rx in (("TP", re_tp), ("SL", re_sl)):
            mc = rx.search(line)
            if not (mc and open_t):
                continue
            trigger = float(mc.group(4))
            exit_deal = int(mc.group(5))
            od = datetime.strptime(open_t["open_time"], "%Y.%m.%d %H:%M:%S")
            pending_close = {
                **open_t,
                "close_time": mc.group(1),
                "exit_reason": kind,
                "win": int(kind == "TP"),
                "trigger": trigger,
                "exit_deal": exit_deal,
                "month": od.strftime("%Y-%m"),
            }
            # deal may already be in buffer if order differs — usually follows
            if exit_deal in deals:
                side = pending_close["side"]
                fill = deals[exit_deal][1]
                adv = adverse_exit_slip(side, trigger, fill)
                net = net_exit_slip(side, trigger, fill)
                cost = pending_close["spread_pts"] + adv
                rows.append(
                    {
                        **{k: pending_close[k] for k in (
                            "open_time",
                            "close_time",
                            "side",
                            "entry",
                            "sl",
                            "tp",
                            "spread_pts",
                            "exit_reason",
                            "win",
                            "month",
                        )},
                        "exit_trigger": trigger,
                        "exit_fill": fill,
                        "exit_adverse_slip_pts": round(adv, 2),
                        "exit_net_slip_pts": round(net, 2),
                        "commission_pts": 0.0,
                        "swap_pts": 0.0,
                        "cost_pts_rt": round(cost, 2),
                        "c_R": round(cost / SL_PTS, 6),
                    }
                )
                pending_close = None
                open_t = None
            break
    return rows


def score(rows: list[dict], leak: float) -> dict:
    n = len(rows)
    wr = sum(r["win"] for r in rows) / n
    bm = wr - BWR
    return {
        "n": n,
        "WR": round(wr * 100, 2),
        "BM_pp": round(bm * 100, 3),
        "E_N": round(wr * (R + 1) - 1, 4),
        "Leak_pp": round(leak * 100, 3),
        "EF_pp": round((bm - leak) * 100, 3),
        "tip_EF_cleared": bool(bm - leak > 0),
    }


def main() -> None:
    chunk = find_tip_chunk(load_text())
    rows = extract(chunk)
    if len(rows) != 79:
        raise SystemExit(f"expected 79 tip events, got {len(rows)}")

    costs = [r["cost_pts_rt"] for r in rows]
    spreads = [r["spread_pts"] for r in rows]
    adv = [r["exit_adverse_slip_pts"] for r in rows]
    c_R_med = median(costs) / SL_PTS
    c_R_mean = mean(costs) / SL_PTS
    leak_med = c_R_med / (R + 1)
    leak_mean = c_R_mean / (R + 1)

    # Authority = median RT cost (robust to outlier fills)
    leak_auth = leak_med

    may_jul = [
        r
        for r in rows
        if (r["month"] == "2026-05") or (r["month"] == "2026-07")
    ]
    kept = [r for r in rows if r not in may_jul]
    # May fragile = all May on tip (tag FRAGILE); Jul = all Jul
    kept_mj = [
        r
        for r in rows
        if not (r["month"] == "2026-05" or r["month"] == "2026-07")
    ]

    packet = {
        "task": "JP225-AOS-LEAK",
        "dated": datetime.now(timezone.utc).isoformat(),
        "window": "2026.05.01-2026.08.31",
        "magic": int(MAGIC),
        "symbol": "JPN225",
        "method": (
            "deal_fill: cost_pts = entry_spread_pts + max(0, adverse_exit_slip_pts); "
            "commission=0 swap=0 (absent in Tester journal); "
            "Leak = median(c_R)/(R+1); R=1.50 SL=23260"
        ),
        "n": len(rows),
        "entry_spread_pts": {
            "median": float(median(spreads)),
            "mean": round(mean(spreads), 2),
            "min": min(spreads),
            "max": max(spreads),
        },
        "exit_adverse_slip_pts": {
            "median": float(median(adv)),
            "mean": round(mean(adv), 2),
            "max": max(adv),
            "share_adverse": round(sum(1 for a in adv if a > 0) / len(adv), 4),
        },
        "cost_pts_rt": {
            "median": float(median(costs)),
            "mean": round(mean(costs), 2),
            "min": min(costs),
            "max": max(costs),
        },
        "c_R_median": round(c_R_med, 6),
        "c_R_mean": round(c_R_mean, 6),
        "Leak_measured_median_pp": round(leak_med * 100, 4),
        "Leak_measured_mean_pp": round(leak_mean * 100, 4),
        "Leak_prior_pp": LEAK_PRIOR * 100,
        "Leak_proxy_journal_2x_pp": 4.8151,
        "Leak_source_authority": "measured_median_deal_fill",
        "commission_swap_note": "Tester journal has no commission/swap lines → booked 0",
        "live_spread_footnote": (
            "Live snapshot ~2300 pts may exceed tester entry med 1400 — "
            "re-check before P7; measured here is Tester deal authority for tip."
        ),
        "tip_all": score(rows, leak_auth),
        "tip_May_OR_Jul_kept": score(kept_mj, leak_auth),
        "zone": None,
    }
    tip_ef = packet["tip_all"]["EF_pp"]
    arm_ef = packet["tip_May_OR_Jul_kept"]["EF_pp"]
    if tip_ef > 0:
        packet["zone"] = "tip_stage1_pass_measured"
    elif arm_ef > 0:
        packet["zone"] = "regime_fragile_engine_tip__arm_clears_measured"
    else:
        packet["zone"] = "costs_or_regime_fragile_measured"

    with (OUT / "tip_deal_costs.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    (OUT / "LEAK_MEASURED.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    (ASSETS / "LEAK_MEASURED.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()
