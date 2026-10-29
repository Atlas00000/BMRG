"""Score EURUSD M15 P2 (magic 26101817) + sibling chart sleeves from 20261018.log."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261018.log"
)
OUT = Path(__file__).resolve().parent / "_tmp_eurusd_p2_parse.json"

POINT = 0.00001  # EURUSD
LEAK_PRIOR_PTS = 20.0  # RT cost prior


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or (len(raw) > 2 and raw[1] == 0):
        return raw.decode("utf-16")
    return raw.decode("utf-8", errors="replace")


def score_chunk(chunk: str, win_from: str, win_to: str, magic: str) -> dict:
    init = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk)
    finals = re.findall(r"final balance ([\d.]+)", chunk)
    deposit_m = re.search(r"initial deposit ([\d.]+)", chunk)
    deposit = float(deposit_m.group(1)) if deposit_m else 500.0
    final = float(finals[-1]) if finals else None

    # Geometry from inputs if present
    sl_pts = re.search(r"InpSL_Points=(\d+)", chunk)
    tp_pts = re.search(r"InpTP_Points=(\d+)", chunk)
    bb = re.search(r"InpBBDev=([\d.]+)", chunk)
    atr_max = re.search(r"InpATRMaxPoints=([\d.]+)", chunk)
    cd = re.search(r"InpCooldownBars=(\d+)", chunk)

    trades: list[dict] = []
    open_rec = None
    for line in chunk.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+"
            r"\[BMRG\]\[TRADE\] OPEN (BUY|SELL) lot=([\d.]+) price=([\d.]+) "
            r"sl=([\d.]+) tp=([\d.]+)",
            line,
        )
        if m:
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2).lower(),
                "lot": float(m.group(3)),
                "entry": float(m.group(4)),
                "sl": float(m.group(5)),
                "tp": float(m.group(6)),
            }
            continue

        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+"
            r"(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            ct = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            win = "take" in m.group(2)
            entry = open_rec["entry"]
            sl_d = abs(entry - open_rec["sl"]) / POINT
            tp_d = abs(open_rec["tp"] - entry) / POINT
            r_realized = (tp_d / sl_d) if (win and sl_d > 0) else (-1.0 if sl_d > 0 else 0.0)
            # tiny adjustment: if distances weird keep sign
            trades.append(
                {
                    **{k: v for k, v in open_rec.items() if k != "t"},
                    "t": open_rec["t"].isoformat(sep=" "),
                    "close": ct.isoformat(sep=" "),
                    "win": win,
                    "sl_pts": round(sl_d, 1),
                    "tp_pts": round(tp_d, 1),
                    "R": round(r_realized, 3),
                    "month": open_rec["t"].strftime("%Y-%m"),
                    "exit": "TP" if win else "SL",
                }
            )
            open_rec = None
            continue

        # end-of-test close — exclude from WR (not TP/SL)
        if open_rec and "position closed due end of test" in line:
            open_rec = None

    n = len(trades)
    wins = sum(1 for t in trades if t["win"])
    wr = wins / n if n else 0.0
    # average realized R on wins / |R| on losses (should be ~RR / 1)
    win_rs = [t["R"] for t in trades if t["win"]]
    loss_rs = [abs(t["R"]) for t in trades if not t["win"]]
    avg_win_r = sum(win_rs) / len(win_rs) if win_rs else 0.0
    avg_loss_r = sum(loss_rs) / len(loss_rs) if loss_rs else 1.0
    # payoff R used for BWR: mean |TP|/|SL| on opens
    rr_list = [
        (t["tp_pts"] / t["sl_pts"]) for t in trades if t["sl_pts"] > 0
    ]
    R = sum(rr_list) / len(rr_list) if rr_list else (
        float(tp_pts.group(1)) / float(sl_pts.group(1))
        if sl_pts and tp_pts
        else 1.25
    )
    bwr = 1.0 / (1.0 + R)
    e_n = wr * (R + 1.0) - 1.0
    bm = wr - bwr
    leak = (LEAK_PRIOR_PTS / (float(sl_pts.group(1)) if sl_pts else 300.0)) / (R + 1.0)
    # framework Leak = c_R / (R+1); c_R = cost/SL
    c_r = LEAK_PRIOR_PTS / (float(sl_pts.group(1)) if sl_pts else 300.0)
    leak = c_r / (R + 1.0)
    ef = bm - leak

    by_month: dict[str, dict] = {}
    for t in trades:
        mth = t["month"]
        d = by_month.setdefault(mth, {"n": 0, "wins": 0, "sumR": 0.0})
        d["n"] += 1
        d["wins"] += 1 if t["win"] else 0
        d["sumR"] += t["R"]
    monthly = []
    for mth in sorted(by_month):
        d = by_month[mth]
        mwr = d["wins"] / d["n"] if d["n"] else 0
        monthly.append(
            {
                "month": mth,
                "n": d["n"],
                "WR": round(100 * mwr, 1),
                "sumR": round(d["sumR"], 2),
                "vs_BWR": "ok" if mwr > bwr else "fail",
            }
        )

    # Gate / block tallies (INFO lines)
    blocks = Counter()
    for line in chunk.splitlines():
        if "Entry blocked:" in line:
            reason = line.split("Entry blocked:", 1)[-1].strip()
            # normalize
            reason = re.sub(r"\s+", " ", reason)[:80]
            blocks[reason] += 1

    tp_lt_sl = sum(1 for t in trades if t["tp_pts"] < t["sl_pts"])

    return {
        "magic": magic,
        "window": f"{win_from}->{win_to}",
        "init": init.group(1) if init else None,
        "deposit": deposit,
        "final": final,
        "pnl": round(final - deposit, 2) if final is not None else None,
        "geometry": {
            "SL": int(sl_pts.group(1)) if sl_pts else None,
            "TP": int(tp_pts.group(1)) if tp_pts else None,
            "BBDev": float(bb.group(1)) if bb else None,
            "ATRMax": float(atr_max.group(1)) if atr_max else None,
            "CooldownBars": int(cd.group(1)) if cd else None,
            "RR_design": round(R, 3),
        },
        "n": n,
        "wins": wins,
        "losses": n - wins,
        "WR": round(100 * wr, 1),
        "R": round(R, 3),
        "BWR": round(100 * bwr, 1),
        "BM_pp": round(100 * bm, 1),
        "Leak_pp": round(100 * leak, 1),
        "EF_pp": round(100 * ef, 1),
        "E_N": round(e_n, 3),
        "avg_win_R": round(avg_win_r, 3),
        "avg_loss_R": round(avg_loss_r, 3),
        "tp_lt_sl_count": tp_lt_sl,
        "stage0": "PASS" if (n >= 30 and wr > bwr and e_n > 0) else "FAIL",
        "monthly": monthly,
        "top_blocks": blocks.most_common(12),
        "opens_logged": len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk)),
    }


def main() -> None:
    text = load(LOG)
    print(f"chars={len(text)}")

    # All EURUSD BMRG tester headers
    headers = list(
        re.finditer(
            r"Tester\tEURUSD,M15 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from (\S+) 00:00 to (\S+) 00:00",
            text,
        )
    )
    # Also Core-start form
    if not headers:
        headers = list(
            re.finditer(
                r"EURUSD,M15 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
                r"from (\S+) 00:00 to (\S+) 00:00",
                text,
            )
        )
    print(f"EURUSD M15 headers: {len(headers)}")

    results = []
    for i, h in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        chunk = text[h.start() : end]
        # trim if another expert starts
        mcut = re.search(r'Tester\t"[^"]+\.ex5"', chunk[500:])
        if mcut:
            chunk = chunk[: 500 + mcut.start()]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        magic = mag.group(1) if mag else "?"
        if magic not in {"26101815", "26101816", "26101817"}:
            continue
        r = score_chunk(chunk, h.group(1), h.group(2), magic)
        results.append(r)
        print(
            f"[{len(results)-1}] magic={magic} {r['window']} n={r['n']} "
            f"WR={r['WR']}% BWR={r['BWR']}% E_N={r['E_N']} EF={r['EF_pp']}pp "
            f"final={r['final']} stage0={r['stage0']}"
        )

    # Multi-asset expansion context: list other symbols tested today with BMRG
    asset_headers = list(
        re.finditer(
            r"Tester\t([A-Z0-9.]+),M15 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from (\S+) 00:00 to (\S+) 00:00",
            text,
        )
    )
    asset_summary = []
    for i, h in enumerate(asset_headers):
        end = asset_headers[i + 1].start() if i + 1 < len(asset_headers) else min(
            len(text), h.start() + 2_000_000
        )
        chunk = text[h.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        finals = re.findall(r"final balance ([\d.]+)", chunk)
        opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk))
        tps = len(re.findall(r"take profit triggered", chunk))
        sls = len(re.findall(r"stop loss triggered", chunk))
        n = tps + sls
        wr = (100.0 * tps / n) if n else None
        asset_summary.append(
            {
                "symbol": h.group(1),
                "window": f"{h.group(2)}->{h.group(3)}",
                "magic": mag.group(1) if mag else None,
                "opens": opens,
                "n_tpsl": n,
                "WR_approx": round(wr, 1) if wr is not None else None,
                "final": float(finals[-1]) if finals else None,
            }
        )

    # Dedupe last occurrence per symbol+window+magic for expansion view
    by_key = {}
    for a in asset_summary:
        key = (a["symbol"], a["window"], a["magic"])
        by_key[key] = a
    expansion = list(by_key.values())
    expansion.sort(key=lambda x: (x["symbol"], x["window"]))

    OUT.write_text(
        json.dumps(
            {
                "eurusd_sleeves": results,
                "expansion_assets": expansion,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("wrote", OUT)
    print("\n=== Expansion asset snapshot (BMRG M15 today) ===")
    for a in expansion:
        print(
            f"  {a['symbol']:8} {a['window']} magic={a['magic']} "
            f"n={a['n_tpsl']} WR~{a['WR_approx']} final={a['final']}"
        )


if __name__ == "__main__":
    main()
