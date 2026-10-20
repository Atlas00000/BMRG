"""One-shot parse of Tester log for Book A review."""
from pathlib import Path
import re

log = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261006.log"
)
raw = log.read_bytes()
if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or (len(raw) > 2 and raw[1] == 0):
    text = raw.decode("utf-16")
else:
    text = raw.decode("utf-8", errors="replace")

# Pair Tester header (window) with following Core init/stats
headers = list(
    re.finditer(
        r"Tester\t(\w+),M5 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
        r"from (\S+) 00:00 to (\S+) 00:00",
        text,
    )
)

blocks = []
for i, h in enumerate(headers):
    start = h.start()
    end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
    chunk = text[start:end]
    init = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk)
    if not init:
        continue
    info = init.group(1)
    mag = re.search(r"magic=(\d+)", info)
    aos = re.search(r"aos=(\d+)", info)
    opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk))
    tp = len(re.findall(r"close TP", chunk, flags=re.I))
    sl = len(re.findall(r"close SL", chunk, flags=re.I))
    finals = re.findall(r"final balance ([\d.]+)", chunk)
    deposit_m = re.search(r"initial deposit ([\d.]+)", chunk)
    deposit = float(deposit_m.group(1)) if deposit_m else 400.0
    final = float(finals[-1]) if finals else None
    n = tp + sl
    wr = (tp / n * 100.0) if n else 0.0
    # R=1 geometry: E_N ≈ 2*WR-1 in R units when n closes
    en = (2.0 * tp / n - 1.0) if n else None
    pnl = (final - deposit) if final is not None else None
    blocks.append(
        {
            "symbol": h.group(1),
            "from": h.group(2),
            "to": h.group(3),
            "magic": mag.group(1) if mag else "?",
            "aos": aos.group(1) if aos else "?",
            "opens": opens,
            "tp": tp,
            "sl": sl,
            "n": n,
            "wr": wr,
            "en": en,
            "final": final,
            "pnl": pnl,
            "deposit": deposit,
        }
    )

# Dedupe identical consecutive runs (GBP May duplicate)
seen = set()
for b in blocks:
    key = (b["symbol"], b["from"], b["to"], b["magic"], b["final"], b["opens"])
    if key in seen:
        b["dup"] = True
        continue
    seen.add(key)
    b["dup"] = False
    en_s = f"{b['en']:+.3f}R" if b["en"] is not None else "—"
    pnl_s = f"{b['pnl']:+.2f}" if b["pnl"] is not None else "—"
    print(
        f"{b['symbol']:7} {b['from']}->{b['to']} mag={b['magic']} aos={b['aos']} "
        f"opens={b['opens']:3} tp={b['tp']:3} sl={b['sl']:3} n={b['n']:3} "
        f"WR={b['wr']:5.1f}% final={b['final']} pnl={pnl_s} E_N={en_s}"
    )
