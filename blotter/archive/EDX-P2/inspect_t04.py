from pathlib import Path
import re

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
raw = LOG.read_bytes()
text = raw.decode("utf-16-le") if raw[:2] == b"\xff\xfe" else raw.decode("utf-8", errors="replace")
print("size", len(raw), "mtime", LOG.stat().st_mtime)

starts = list(
    re.finditer(
        r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
        text,
    )
)
for i, s in enumerate(starts):
    end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
    c = text[s.start() : end]
    mag = re.search(r"InpMagic=(\d+)", c)
    if not mag or mag.group(1) != "8230204":
        continue
    opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", c))
    mkt = len(re.findall(r"\smarket (?:buy|sell) ", c))
    tp = len(re.findall(r"take profit triggered", c, flags=re.I))
    sl = len(re.findall(r"stop loss triggered", c, flags=re.I))
    finals = re.findall(r"final balance ([\d.]+)", c)
    init = re.search(r"BMRG init OK[^\r\n]+", c)
    print("--- run", i, "chunk_len", len(c))
    print(" opens", opens, "mkt", mkt, "tp", tp, "sl", sl, "final", finals)
    print(" init", init.group(0)[:140] if init else None)
    # errors
    for pat in ("stopped", "error", "tester stopped", "connection closed", "thread finished"):
        print(" ", pat, len(re.findall(pat, c, flags=re.I)))
    lines = [ln for ln in c.splitlines() if ln.strip()][-12:]
    for ln in lines:
        print(" ", ln[:180].encode("ascii", "replace").decode())
