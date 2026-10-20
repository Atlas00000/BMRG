"""Score EDX-P0-T01 AUDUSD from Tester log 20261007."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import math
import re
import statistics as st

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
MAGIC = "8230101"


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or (len(raw) > 2 and raw[1] == 0):
        return raw.decode("utf-16")
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    text = load(LOG)
    print(f"chars={len(text)} encoding_ok BOM/utf16={LOG.read_bytes()[:2]}")

    headers = list(
        re.finditer(
            r"Tester\tAUDUSD,M5 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
            r"from (\S+) 00:00 to (\S+) 00:00",
            text,
        )
    )
    print(f"AUDUSD headers: {len(headers)}")
    for i, h in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        chunk0 = text[h.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk0)
        init = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk0)
        opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk0))
        finals = re.findall(r"final balance ([\d.]+)", chunk0)
        im = re.search(r"magic=(\d+)", init.group(1)) if init else None
        print(
            f"  [{i}] {h.group(1)}->{h.group(2)} "
            f"InpMagic={mag.group(1) if mag else '?'} "
            f"init_magic={im.group(1) if im else '?'} "
            f"opens={opens} final={finals[-1] if finals else '?'} "
            f"chunk={len(chunk0)}"
        )

    # Prefer last run whose magic is EDX P0 (8230101) else last AUDUSD May-Aug run
    target_idx = None
    for i, h in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        chunk0 = text[h.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk0)
        init = re.search(r"magic=(\d+)", chunk0)
        mval = mag.group(1) if mag else (init.group(1) if init else "")
        if mval == MAGIC:
            target_idx = i
    if target_idx is None and headers:
        target_idx = len(headers) - 1
        print(f"NOTE: magic {MAGIC} not found — scoring LAST AUDUSD run (index {target_idx})")

    if target_idx is None:
        print("No AUDUSD runs found")
        return

    h = headers[target_idx]
    start = h.start()
    end = headers[target_idx + 1].start() if target_idx + 1 < len(headers) else len(text)
    chunk = text[start:end]
    m = re.search(r'Tester\t"BMRG\\BMRG\.ex5"', chunk[200:])
    if m:
        chunk = chunk[: 200 + m.start()]

    init_m = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk)
    init_line = init_m.group(1) if init_m else "?"
    print("init:", init_line[:200])
    win_from, win_to = h.group(1), h.group(2)
    print(f"window: {win_from} -> {win_to}")

    deposit_m = re.search(r"initial deposit ([\d.]+)", chunk)
    # deposit often before init — search back
    pre = text[max(0, start - 50000) : start]
    if not deposit_m:
        deposit_m = re.search(r"initial deposit ([\d.]+)", pre)
    finals = re.findall(r"final balance ([\d.]+)", chunk)
    if not finals:
        finals = re.findall(r"final balance ([\d.]+)", text[start : start + 200000])
    deposit = float(deposit_m.group(1)) if deposit_m else 400.0
    final = float(finals[-1]) if finals else None
    pnl = (final - deposit) if final is not None else None
    print(f"deposit={deposit} final={final} pnl={pnl}")

    # trades
    trades = []
    open_rec = None
    for line in chunk.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2),
                "lot": float(m.group(3)),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
            }
            # entry approx from next fill line or paren
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+deal #\d+ (buy|sell) "
            r"([\d.]+) AUDUSD at ([\d.]+)",
            line,
        )
        if m and open_rec and "entry" not in open_rec:
            # first deal after market is entry
            if m.group(2) == open_rec["side"]:
                open_rec["entry"] = float(m.group(4))
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            ct = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            win = "take" in m.group(2)
            # R approx: FIXED_RR → +1 or -1; refine with prices if exit deal follows
            open_rec["close"] = ct
            open_rec["win"] = win
            open_rec["hold_h"] = (ct - open_rec["t"]).total_seconds() / 3600.0
            trades.append(open_rec)
            open_rec = None

    # enrich pnl_R from exit deals
    # simpler: FIXED_RR journal → win +1R loss -1R; costs unknown
    n = len(trades)
    wins = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    wr = len(wins) / n if n else 0.0
    # Estimate R from SL/TP distances vs entry if present
    aw_list = []
    al_list = []
    for t in trades:
        entry = t.get("entry")
        if entry is None:
            # fallback designed
            pnl_r = 1.0 if t["win"] else -1.0
        else:
            if t["side"] == "buy":
                risk = abs(entry - t["sl"])
                reward = abs(t["tp"] - entry)
            else:
                risk = abs(t["sl"] - entry)
                reward = abs(entry - t["tp"])
            if risk <= 0:
                pnl_r = 1.0 if t["win"] else -1.0
            else:
                # designed R multiple at exit levels
                pnl_r = (reward / risk) if t["win"] else -(risk / risk)
                # for loss AL in R units = 1 by SL definition
                if not t["win"]:
                    pnl_r = -1.0
                else:
                    pnl_r = reward / risk
        t["pnl_r"] = pnl_r
        if t["win"]:
            aw_list.append(pnl_r)
        else:
            al_list.append(abs(pnl_r))

    aw = st.mean(aw_list) if aw_list else 0.0
    al = st.mean(al_list) if al_list else 1.0
    R = (aw / al) if al else 0.0
    RR = 1.0  # designed
    bwr = 1.0 / (1.0 + R) if R > 0 else 1.0
    bm = wr - bwr
    fmi = (bm / bwr) if bwr else 0.0
    e_n = wr * (R + 1) - 1
    pf = (wr * aw) / ((1 - wr) * al) if (1 - wr) * al > 0 else float("inf")
    # Leak proxy: spread from first trades ~ use 3*10/300 = 0.1 if unknown
    # Try measure spreads from market lines with paren
    spreads = []
    for line in chunk.splitlines():
        m = re.search(
            r"market (?:buy|sell) [\d.]+ AUDUSD sl: [\d.]+ tp: [\d.]+ \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            bid, ask = float(m.group(1)), float(m.group(2))
            spreads.append(round((ask - bid) / 0.00001))
    med_spread = st.median(spreads) if spreads else 10
    c_r = (3.0 * med_spread) / 300.0
    leak = c_r / (R + 1)  # fraction
    leak_pp = leak * 100
    bm_pp = bm * 100
    ef_pp = bm_pp - leak_pp
    m_pp = 1.96 * 100 * math.sqrt(wr * (1 - wr) / n) if n else 0
    # Wilson half-width
    z = 1.96
    if n:
        center = (wr + z * z / (2 * n)) / (1 + z * z / n)
        half = (z / (1 + z * z / n)) * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
        wilson_m_pp = half * 100
    else:
        wilson_m_pp = 0

    print("\n=== HEALTH VECTOR (gross + cost proxy) ===")
    print(f"n={n} WR={wr*100:.2f}% AW={aw:.3f}R AL={al:.3f}R R={R:.3f} RR={RR} RR-R={RR-R:+.3f}")
    print(f"BWR={bwr*100:.2f}% BM={bm_pp:+.2f}pp FMI={fmi:.3f}")
    print(f"med_spread_pts={med_spread} c_R={c_r:.3f} Leak={leak_pp:.2f}pp costs_defaulted=spread_proxy")
    print(f"EF={ef_pp:+.2f}pp M_normal={m_pp:.2f}pp M_wilson={wilson_m_pp:.2f}pp")
    print(f"E_N={e_n:+.3f}R PF={pf:.3f}")
    if final is not None:
        print(f"final={final} pnl={pnl:+.2f}")

    zone = "Negative" if ef_pp <= 0 else ("Fragile" if ef_pp <= wilson_m_pp else "Robust")
    if n < 100:
        zone_note = f"{zone} but n<{100} → Insufficient for production; expansion only"
    elif n < 385:
        zone_note = f"{zone} provisional (n<385)"
    else:
        zone_note = zone
    print(f"ZONE: {zone_note}")

    # side diagnosis
    if abs(RR - R) < 0.15 and aw > 0.85 and al < 1.15:
        side = "WR-side"
        r_side_claim = "REJECTED (AL≈AW≈1R; RR-R≈0)"
    elif R < RR - 0.25 or al > aw * 1.2:
        side = "R-side"
        r_side_claim = "SUPPORTED"
    else:
        side = "both"
        r_side_claim = "MIXED"
    print(f"SIDE: {side} | AL-too-large claim: {r_side_claim}")

    # monthly
    by_mo = defaultdict(lambda: {"w": 0, "l": 0})
    for t in trades:
        mo = t["t"].strftime("%Y-%m")
        if t["win"]:
            by_mo[mo]["w"] += 1
        else:
            by_mo[mo]["l"] += 1
    print("\nmonthly:")
    for mo in sorted(by_mo):
        w, l = by_mo[mo]["w"], by_mo[mo]["l"]
        nn = w + l
        wrr = w / nn
        en = wrr * (R + 1) - 1
        print(f"  {mo}: n={nn} WR={wrr*100:.1f}% E_N={en:+.3f}R")

    # rolling trade windows
    outcomes = [1 if t["win"] else 0 for t in trades]
    print("\nW20:")
    for i in range(0, max(1, n - 20 + 1), 10):
        win = outcomes[i : i + 20]
        if len(win) < 20:
            break
        wrr = sum(win) / 20
        en = wrr * (R + 1) - 1
        print(f"  [{i}:{i+20}] WR={wrr*100:.1f}% E_N={en:+.3f}R")

    # streaks
    max_l = cur_l = 0
    for t in trades:
        if not t["win"]:
            cur_l += 1
            max_l = max(max_l, cur_l)
        else:
            cur_l = 0
    exp_streak = math.log(n) / math.log(1 / (1 - wr)) if wr < 1 and n else 0
    print(f"\nmax_loss_streak={max_l} expected_worst≈{exp_streak:.1f} DEPENDENCE_thresh≈{1.5*exp_streak:.1f}")

    # side mix
    for side_n in ("buy", "sell"):
        sub = [t for t in trades if t["side"] == side_n]
        if not sub:
            continue
        ww = sum(1 for t in sub if t["win"])
        print(f"{side_n}: n={len(sub)} WR={100*ww/len(sub):.1f}%")

    # opens tag
    print("OPEN tags", len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk)))
    print("TP", len(wins), "SL", len(losses))

    # write compact scorecard path hint
    out = {
        "n": n,
        "wr": wr,
        "aw": aw,
        "al": al,
        "R": R,
        "RR": RR,
        "bwr": bwr,
        "bm_pp": bm_pp,
        "fmi": fmi,
        "c_r": c_r,
        "leak_pp": leak_pp,
        "ef_pp": ef_pp,
        "m_wilson_pp": wilson_m_pp,
        "e_n": e_n,
        "pf": pf,
        "final": final,
        "pnl": pnl,
        "zone": zone_note,
        "side": side,
        "r_claim": r_side_claim,
        "med_spread": med_spread,
        "max_loss_streak": max_l,
        "window": f"{win_from}->{win_to}",
    }
    Path(__file__).with_name("_score.json").write_text(
        __import__("json").dumps(out, indent=2), encoding="utf-8"
    )
    print("\nwrote _score.json")


if __name__ == "__main__":
    main()
