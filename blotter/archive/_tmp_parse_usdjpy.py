"""Parse Tester logs for USDJPY BMRG P0 expand-sleeve runs."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re

LOGS = [
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
    ),
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261018.log"
    ),
]

re_started = re.compile(
    r"USDJPY,M15: testing of Experts.BMRG.BMRG\.ex5 "
    r"from (\d{4}\.\d{2}\.\d{2})(?:\s+\d{2}:\d{2})?\s+to "
    r"(\d{4}\.\d{2}\.\d{2})(?:\s+\d{2}:\d{2})?\s+started with inputs",
    re.I,
)
re_other = re.compile(
    r"(EURUSD|GBPJPY|Meta|Apple|XAUUSD|EURGBP|XBRUSD|AUDUSD|UK100)"
    r"(?:,M15)?(?: \([^)]+\))?: testing of Experts\\BMRG\\BMRG\.ex5",
    re.I,
)
re_final = re.compile(r"final balance\s+([0-9.]+)\s+(\w+)")
re_init = re.compile(
    r"BMRG init OK \| (\S+) PERIOD_(\S+) \| BB\(([^)]+)\) .* magic=(\d+) aos=(\d+)"
)
re_tp = re.compile(r"take profit triggered")
re_sl = re.compile(r"stop loss triggered")
re_eot = re.compile(r"position closed due end of test")
re_block = re.compile(r"Entry blocked: (.+)")
re_hist = re.compile(
    r"USDJPY: history synchronized from (\d{4}\.\d{2}\.\d{2}) to (\d{4}\.\d{2}\.\d{2})"
)
re_start_chg = re.compile(r"USDJPY: start time changed to (\d{4}\.\d{2}\.\d{2})")
re_input2 = re.compile(r"\t\s*(Inp\w+)=([^\s]+)")
re_deal_month = re.compile(
    r"(\d{4}\.\d{2}\.\d{2}).*(?:take profit|stop loss) triggered"
)
re_open_month = re.compile(
    r"(\d{4}\.\d{2}\.\d{2}).*market (buy|sell) .* USDJPY sl:"
)
INPUT_KEYS = [
    "InpSL_Points",
    "InpTP_Points",
    "InpBBDev",
    "InpATRMaxPoints",
    "InpUseATRRegime",
    "InpStartHour",
    "InpEndHour",
    "InpTradeTue",
    "InpMaxLevels",
    "InpLot",
    "InpMagic",
    "InpAOS_Enable",
    "InpMaxSpread",
    "InpRiskPercent",
    "InpCooldownBars",
    "InpAllowBuy",
    "InpAllowSell",
]

R = 1.20
BWR = 1 / (1 + R)
LEAK = 11.4  # design prior pp (c_R≈0.25 / (R+1))


def parse_log(log: Path) -> list[dict]:
    runs: list[dict] = []
    cur = None
    in_jpy = False
    with log.open("r", encoding="utf-16", errors="replace") as f:
        for i, line in enumerate(f, 1):
            m = re_started.search(line)
            if m:
                if cur is not None:
                    runs.append(cur)
                cur = {
                    "log": log.name,
                    "line": i,
                    "from": m.group(1),
                    "to": m.group(2),
                    "inputs": {},
                    "tp": 0,
                    "sl": 0,
                    "eot": 0,
                    "blocks": Counter(),
                    "final": None,
                    "init": None,
                    "hist": None,
                    "start_chg": None,
                    "open_months": Counter(),
                    "close_tp_months": Counter(),
                    "close_sl_months": Counter(),
                    "open_by_side": Counter(),
                }
                in_jpy = True
                continue

            if re_other.search(line) and in_jpy:
                if cur is not None:
                    runs.append(cur)
                cur = None
                in_jpy = False
                continue

            if not in_jpy or cur is None:
                continue

            mh = re_hist.search(line)
            if mh:
                cur["hist"] = (mh.group(1), mh.group(2))
            ms = re_start_chg.search(line)
            if ms:
                cur["start_chg"] = ms.group(1)

            if "Inp" in line and "=" in line:
                mi = re_input2.search(line)
                if mi and mi.group(1) in INPUT_KEYS:
                    cur["inputs"][mi.group(1)] = mi.group(2)

            mi = re_init.search(line)
            if mi:
                cur["init"] = {
                    "sym": mi.group(1),
                    "tf": mi.group(2),
                    "bb": mi.group(3),
                    "magic": mi.group(4),
                    "aos": mi.group(5),
                }

            mm = re_open_month.search(line)
            if mm:
                cur["open_months"][mm.group(1)[:7]] += 1
                cur["open_by_side"][mm.group(2).upper()] += 1

            if re_tp.search(line):
                cur["tp"] += 1
                dm = re_deal_month.search(line)
                if dm:
                    cur["close_tp_months"][dm.group(1)[:7]] += 1
            if re_sl.search(line):
                cur["sl"] += 1
                dm = re_deal_month.search(line)
                if dm:
                    cur["close_sl_months"][dm.group(1)[:7]] += 1
            if re_eot.search(line):
                cur["eot"] += 1

            mb = re_block.search(line)
            if mb:
                cur["blocks"][mb.group(1).strip()] += 1

            mf = re_final.search(line)
            if mf:
                cur["final"] = (float(mf.group(1)), mf.group(2))

    if cur is not None:
        runs.append(cur)
    return runs


def score(r: dict) -> dict:
    closed = r["tp"] + r["sl"]
    wr = (r["tp"] / closed * 100) if closed else None
    en = (wr / 100 * (R + 1) - 1) if wr is not None else None
    bm = (wr - BWR * 100) if wr is not None else None
    ef = (bm - LEAK) if bm is not None else None
    net = (r["final"][0] - 500) if r["final"] else None
    months = sorted(set(list(r["close_tp_months"]) + list(r["close_sl_months"])))
    monthly = {}
    for mth in months:
        tw = r["close_tp_months"][mth]
        sw = r["close_sl_months"][mth]
        n = tw + sw
        monthly[mth] = {
            "n": n,
            "wr": round(tw / n * 100, 1) if n else None,
            "tp": tw,
            "sl": sw,
        }
    return {
        "log": r["log"],
        "window": f"{r['from']} → {r['to']}",
        "line": r["line"],
        "inputs": r["inputs"],
        "init": r["init"],
        "hist": r["hist"],
        "start_chg": r["start_chg"],
        "n_closed": closed,
        "tp": r["tp"],
        "sl": r["sl"],
        "eot": r["eot"],
        "wr": round(wr, 1) if wr is not None else None,
        "E_N": round(en, 3) if en is not None else None,
        "BM_pp": round(bm, 1) if bm is not None else None,
        "EF_pp_prior": round(ef, 1) if ef is not None else None,
        "final": r["final"][0] if r["final"] else None,
        "net": round(net, 2) if net is not None else None,
        "blocks": dict(r["blocks"].most_common(12)),
        "open_months": dict(r["open_months"]),
        "monthly": monthly,
        "sides": dict(r["open_by_side"]),
        "n_opens_market": sum(r["open_months"].values()),
    }


def main():
    all_runs = []
    for log in LOGS:
        if log.exists():
            all_runs.extend(parse_log(log))
    out = [score(r) for r in all_runs]
    print(json.dumps({"BWR_pct": round(BWR * 100, 2), "R": R, "LEAK_prior_pp": LEAK, "runs": out}, indent=2))


if __name__ == "__main__":
    main()
