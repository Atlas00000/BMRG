from pathlib import Path
import re

log = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
raw = log.read_bytes()
text = raw.decode("utf-16") if raw[1] == 0 else raw.decode("utf-8", errors="replace")
headers = list(
    re.finditer(
        r"Tester\tAUDUSD,M5 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
        r"from (\S+) 00:00 to (\S+) 00:00",
        text,
    )
)
print("headers", len(headers))
h = headers[-1]
chunk = text[h.start() : h.start() + 50000]
for key in [
    "InpSL_Points",
    "InpTP_Points",
    "InpBBDev",
    "InpStartHour",
    "InpEndHour",
    "InpTradeTue",
    "InpTradeMon",
    "InpMagic",
    "InpMaxLevels",
    "InpMaxEntries",
    "InpAOS_Enable",
    "InpRiskPercent",
]:
    m = re.search(rf"{key}=([^\|\r\n]+)", chunk)
    print(f"{key}={m.group(1) if m else '?'}")

init = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk)
print("init", init.group(1) if init else None)
final = re.findall(r"final balance ([\d.]+)", text[h.start() :])
print("finals", final[:3], "...", final[-1] if final else None)
