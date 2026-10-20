"""Parse DE30 M5 magic 26101903 runs from Tester log 20261020."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261020.log"
)
OUT = Path(__file__).resolve().parent

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.07  # prior
TAGS = {
    "2026-01": "pre-tip",
    "2026-02": "pre-tip soft",
    "2026-03": "pre-tip",
    "2026-04": "pre-tip",
    "2026-05": "MISMATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
    "2026-09": "FRAGILE",
    "2026-10": "FRAGILE",
}


def score(tp: int, sl: int) -> dict:
    n = tp + sl
    if n == 0:
        return {"n": 0}
    wr = tp / n
    return {
        "n": n,
        "TP": tp,
        "SL": sl,
        "WR_pct": round(wr * 100, 1),
        "E_N": round(wr * (R + 1) - 1, 3),
        "EF_prior_pp": round((wr - BWR - LEAK) * 100, 1),
        "BM_pp": round((wr - BWR) * 100, 1),
    }


def main() -> None:
    text = LOG.read_text(encoding="utf-16")
    headers = list(
        re.finditer(
            r"Tester\tDE30,M5[^\n]*from (\d{4}\.\d{2}\.\d{2})[^\n]*to (\d{4}\.\d{2}\.\d{2})",
            text,
        )
    )
    runs = []
    for h in headers:
        s = h.start()
        # Prefer DE30 "Test passed" / tick summary as end bound (avoids early final-balance hits)
        passed = re.search(r"DE30,M5: \d+ ticks", text[s : s + 50_000_000])
        bal_m = re.search(r"final balance ([0-9.]+) USD", text[s : s + 50_000_000])
        if passed and bal_m and bal_m.start() < passed.start():
            e = s + passed.end()
        elif passed:
            e = s + passed.end()
        elif bal_m:
            e = s + bal_m.end()
        else:
            e = s + 20_000_000
        chunk = text[s:e]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        if not mag or mag.group(1) != "26101903":
            continue
        # Re-find balance inside chunk (last one)
        bals = re.findall(r"final balance ([0-9.]+) USD", chunk)
        bal_val = float(bals[-1]) if bals else None
        by: dict[str, dict[str, int]] = defaultdict(lambda: {"TP": 0, "SL": 0})
        for line in chunk.splitlines():
            mt = re.search(
                r"(2026\.\d{2}\.\d{2}) .*?(take profit triggered|stop loss triggered)",
                line,
            )
            if mt:
                mon = mt.group(1)[:7].replace(".", "-")
                key = "TP" if "take profit" in mt.group(2) else "SL"
                by[mon][key] += 1
        ab: dict[str, int] = defaultdict(int)
        for line in chunk.splitlines():
            mt = re.search(r"(2026\.\d{2}\.\d{2}).*ATR .* > max", line)
            if mt:
                ab[mt.group(1)[:7].replace(".", "-")] += 1
        buys = len(re.findall(r"CTrade::OrderSend: market buy 0\.10 DE30", chunk))
        sells = len(re.findall(r"CTrade::OrderSend: market sell 0\.10 DE30", chunk))
        diffs = []
        for line in chunk.splitlines():
            m2 = re.search(
                r"market (buy|sell) 0\.1 DE30[^\n]*\((\d+\.\d+) / (\d+\.\d+) /",
                line,
            )
            if m2:
                bid, ask = float(m2.group(2)), float(m2.group(3))
                diffs.append((ask - bid) / 0.01)
        months = {}
        tot_tp = tot_sl = 0
        for mon in sorted(by):
            sc = score(by[mon]["TP"], by[mon]["SL"])
            sc["tag"] = TAGS.get(mon, "")
            months[mon] = sc
            tot_tp += by[mon]["TP"]
            tot_sl += by[mon]["SL"]
        tip_tp = tip_sl = 0
        for mon in ("2026-05", "2026-06", "2026-07", "2026-08"):
            tip_tp += by[mon]["TP"]
            tip_sl += by[mon]["SL"]
        match_tp = match_sl = 0
        for mon in ("2026-06", "2026-07", "2026-08"):
            match_tp += by[mon]["TP"]
            match_sl += by[mon]["SL"]
        pre_tp = pre_sl = 0
        for mon in ("2026-01", "2026-02", "2026-03", "2026-04"):
            pre_tp += by[mon]["TP"]
            pre_sl += by[mon]["SL"]
        bal = bal_val
        run = {
            "window": {"from": h.group(1), "to": h.group(2)},
            "magic": 26101903,
            "geometry": {
                "SL": re.search(r"InpSL_Points=([0-9.]+)", chunk).group(1),
                "TP": re.search(r"InpTP_Points=([0-9.]+)", chunk).group(1),
                "ATR_max": re.search(r"InpATRMaxPoints=([0-9.]+)", chunk).group(1),
                "BBDev": re.search(r"InpBBDev=([0-9.]+)", chunk).group(1),
                "CooldownBars": re.search(r"InpCooldownBars=(\d+)", chunk).group(1),
                "AOS": re.search(r"InpAOS_Enable=(\w+)", chunk).group(1),
            },
            "final_balance": bal,
            "pnl": None if bal is None else round(bal - 500.0, 2),
            "entries_buy": buys,
            "entries_sell": sells,
            "entries": buys + sells,
            "overall_closes": score(tot_tp, tot_sl),
            "pre_Jan_Apr_closes": score(pre_tp, pre_sl),
            "tip_May_Aug_closes": score(tip_tp, tip_sl),
            "match_Jun_Aug_closes": score(match_tp, match_sl),
            "monthly_closes": months,
            "atr_blocks_by_month": dict(sorted(ab.items())),
            "atr_blocks_total": int(sum(ab.values())),
            "open_spread_pts": {
                "n": len(diffs),
                "p50": round(sorted(diffs)[len(diffs) // 2], 0) if diffs else None,
                "min": round(min(diffs), 0) if diffs else None,
                "max": round(max(diffs), 0) if diffs else None,
            },
        }
        runs.append(run)

    report = {
        "task": "DE40-M5-P0-LOG-REVIEW",
        "scope": "expansion_not_live_replace",
        "preset": "BMRG-M5-DE40-6M-P0_balanced_chart.set",
        "Leak_prior_pp": 7.0,
        "design_probe": {"n": 141, "WR": 54.6, "E_N": 0.229, "EF_pp": 3.2},
        "runs": runs,
        "note": (
            "Only Jan-Aug 2026 window found in 20261020.log so far. "
            "Design tip May-Oct / Sep-Oct FRAGILE not yet in this log. "
            "Journal open spreads ≪ live ~1020 — keep Leak prior 7.0pp."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SCORE.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
