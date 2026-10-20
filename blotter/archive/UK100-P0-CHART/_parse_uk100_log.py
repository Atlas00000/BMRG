"""Parse 20261012 Tester log for UK100 BMRG runs (research expand sleeve)."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261012.log"
)

re_test = re.compile(
    r"(UK100)(?:,M15)?(?: \([^)]+\))?: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\d{4}\.\d{2}\.\d{2}).*?to (\d{4}\.\d{2}\.\d{2})",
    re.I,
)
re_started = re.compile(
    r"(UK100),M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\d{4}\.\d{2}\.\d{2}).*?to (\d{4}\.\d{2}\.\d{2}) started with inputs",
    re.I,
)
re_other = re.compile(
    r"(Meta|Apple|XAUUSD|EURUSD|EURGBP|XBRUSD|AUDUSD)(?:,M15)?(?: \([^)]+\))?: "
    r"testing of Experts\\BMRG\\BMRG\.ex5",
    re.I,
)
re_final = re.compile(r"final balance\s+([0-9.]+)\s+(\w+)")
re_init = re.compile(
    r"BMRG init OK \| (\S+) PERIOD_(\S+) \| BB\(([^)]+)\) .* magic=(\d+) aos=(\d+)"
)
re_open = re.compile(
    r"\[BMRG\]\[TRADE\] OPEN (BUY|SELL) lot=([0-9.]+) price=([0-9.]+) "
    r"sl=([0-9.]+) tp=([0-9.]+)"
)
re_tp = re.compile(r"take profit triggered")
re_sl = re.compile(r"stop loss triggered")
re_eot = re.compile(r"position closed due end of test")
re_block = re.compile(r"Entry blocked: (.+)")
re_pass = re.compile(r"UK100,M15: .* Test passed")
re_hist = re.compile(
    r"UK100: history synchronized from (\d{4}\.\d{2}\.\d{2}) to (\d{4}\.\d{2}\.\d{2})"
)
re_start_chg = re.compile(r"UK100: start time changed to (\d{4}\.\d{2}\.\d{2})")
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
    "InpMinLotOverride",
    "InpMagic",
    "InpAOS_Enable",
    "InpMaxSpread",
    "InpRiskPercent",
    "InpLotMode",
    "InpAllowBuy",
    "InpAllowSell",
    "InpCooldownBars",
]


def flush(runs, cur):
    if cur is not None:
        runs.append(cur)


def main():
    runs = []
    cur = None
    in_uk = False

    with LOG.open("r", encoding="utf-16", errors="replace") as f:
        for i, line in enumerate(f, 1):
            m = re_test.search(line) or re_started.search(line)
            if m:
                flush(runs, cur)
                cur = {
                    "line": i,
                    "from": m.group(2),
                    "to": m.group(3),
                    "inputs": {},
                    "opens": [],
                    "tp": 0,
                    "sl": 0,
                    "eot": 0,
                    "blocks": Counter(),
                    "final": None,
                    "init": None,
                    "hist": None,
                    "start_chg": None,
                    "passed": False,
                    "open_months": Counter(),
                    "close_months": Counter(),
                    "open_by_side": Counter(),
                }
                in_uk = True
                continue

            if re_other.search(line) and in_uk and cur and cur.get("final") is not None:
                flush(runs, cur)
                cur = None
                in_uk = False
                continue

            if not in_uk or cur is None:
                continue

            mh = re_hist.search(line)
            if mh:
                cur["hist"] = (mh.group(1), mh.group(2))
            ms = re_start_chg.search(line)
            if ms:
                cur["start_chg"] = ms.group(1)

            if "Inp" in line and "=" in line and len(cur["inputs"]) < 80:
                for key in INPUT_KEYS:
                    if key + "=" in line:
                        mm = re.search(re.escape(key) + r"=([^\s]+)", line)
                        if mm:
                            cur["inputs"][key] = mm.group(1)

            mi = re_init.search(line)
            if mi:
                cur["init"] = {
                    "sym": mi.group(1),
                    "tf": mi.group(2),
                    "bb": mi.group(3),
                    "magic": mi.group(4),
                    "aos": mi.group(5),
                }

            mo = re_open.search(line)
            if mo:
                side, lot, px, sl, tp = mo.groups()
                md = re.search(r"(\d{4}\.\d{2}\.\d{2})", line)
                d = md.group(1) if md else "?"
                cur["opens"].append(
                    {
                        "side": side,
                        "lot": float(lot),
                        "px": float(px),
                        "sl": float(sl),
                        "tp": float(tp),
                        "date": d,
                    }
                )
                cur["open_months"][d[:7]] += 1
                cur["open_by_side"][side] += 1

            if "UK100" in line or "[BMRG]" in line:
                if re_tp.search(line):
                    cur["tp"] += 1
                    md = re.search(r"(\d{4}\.\d{2}\.\d{2})", line)
                    if md:
                        cur["close_months"][md.group(1)[:7] + ":TP"] += 1
                if re_sl.search(line):
                    cur["sl"] += 1
                    md = re.search(r"(\d{4}\.\d{2}\.\d{2})", line)
                    if md:
                        cur["close_months"][md.group(1)[:7] + ":SL"] += 1
                if re_eot.search(line):
                    cur["eot"] += 1

            mb = re_block.search(line)
            if mb:
                reason = mb.group(1).strip()
                rl = reason.lower()
                if "atr" in rl:
                    cur["blocks"]["ATR"] += 1
                elif "session" in rl:
                    cur["blocks"]["session"] += 1
                elif "spread" in rl:
                    cur["blocks"]["spread"] += 1
                elif any(x in rl for x in ("day", "tue", "weekday", "trade day")):
                    cur["blocks"]["weekday"] += 1
                elif any(x in rl for x in ("pause", "streak", "fail")):
                    cur["blocks"]["pause/fail"] += 1
                elif any(x in rl for x in ("halt", "daily", "equity", "margin")):
                    cur["blocks"]["halt"] += 1
                else:
                    cur["blocks"][reason[:60]] += 1

            mf = re_final.search(line)
            if mf:
                cur["final"] = (float(mf.group(1)), mf.group(2))

            if re_pass.search(line):
                cur["passed"] = True
                flush(runs, cur)
                cur = None
                in_uk = False

    flush(runs, cur)

    # Deduplicate overlapping start+started pairs (same window, keep richer)
    deduped = []
    for r in runs:
        if (
            deduped
            and deduped[-1]["from"] == r["from"]
            and deduped[-1]["to"] == r["to"]
            and abs(deduped[-1]["line"] - r["line"]) < 50
        ):
            # merge into richer
            prev = deduped[-1]
            if len(r["opens"]) >= len(prev["opens"]):
                deduped[-1] = r
            continue
        deduped.append(r)

    print(f"UK100 runs found: {len(deduped)}")
    for idx, r in enumerate(deduped):
        print("\n" + "=" * 70)
        print(f"RUN {idx + 1} line={r['line']} window={r['from']} -> {r['to']}")
        print(f"  hist={r['hist']} start_chg={r['start_chg']} passed={r['passed']}")
        print(f"  init={r['init']}")
        print(f"  inputs={r['inputs']}")
        print(f"  final_balance={r['final']}")
        n = len(r["opens"])
        tp, sl, eot = r["tp"], r["sl"], r["eot"]
        closed = tp + sl
        wr = (tp / closed * 100) if closed else 0.0
        deposit_guess = 500.0
        bal = r["final"][0] if r["final"] else None
        net = (bal - deposit_guess) if bal is not None else None
        print(
            f"  opens={n} sides={dict(r['open_by_side'])} "
            f"TP={tp} SL={sl} EOT={eot} WR={wr:.1f}% (excl EOT)"
        )
        if net is not None:
            print(f"  net_vs_500={net:+.2f} ({net / deposit_guess * 100:+.2f}%)")
        print(f"  opens_by_month={dict(sorted(r['open_months'].items()))}")
        print(f"  closes={dict(sorted(r['close_months'].items()))}")
        print(f"  blocks={dict(r['blocks'].most_common(15))}")
        if r["opens"]:
            o = r["opens"][0]
            if o["side"] == "SELL":
                sl_pts = round((o["sl"] - o["px"]) / 0.01)
                tp_pts = round((o["px"] - o["tp"]) / 0.01)
            else:
                sl_pts = round((o["px"] - o["sl"]) / 0.01)
                tp_pts = round((o["tp"] - o["px"]) / 0.01)
            rr = (tp_pts / sl_pts) if sl_pts else 0
            print(
                f"  first_trade_geom: side={o['side']} "
                f"SL_pts~{sl_pts} TP_pts~{tp_pts} RR={rr:.3f}"
            )
            # realized R proxy if fixed geometry: R_design=1.25, E_N from WR
            R = 1.25
            BWR = 1 / (1 + R)
            BM = (wr / 100) - BWR
            # leak prior from preset ~2.9pp
            leak = 0.029
            EF = BM - leak
            EN = (wr / 100) * (R + 1) - 1
            print(
                f"  framework_proxy (design R=1.25, leak prior 2.9pp): "
                f"BWR={BWR*100:.1f}% BM={BM*100:+.1f}pp EF={EF*100:+.1f}pp E_N={EN:+.3f}R"
            )

        # monthly WR from closes
        months = sorted({k.split(":")[0] for k in r["close_months"]})
        if months:
            print("  monthly_wr:")
            for mo in months:
                t = r["close_months"].get(mo + ":TP", 0)
                s = r["close_months"].get(mo + ":SL", 0)
                c = t + s
                w = (t / c * 100) if c else 0
                print(f"    {mo}: n={c} WR={w:.1f}% (TP={t} SL={s})")


if __name__ == "__main__":
    main()
