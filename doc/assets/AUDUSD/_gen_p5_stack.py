from pathlib import Path
import re

src = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\AUDUSD"
    r"\EDX-P3-T02_startHour13_G0_AUDUSD-M5_MayAug.set"
)
out = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\AUDUSD"
    r"\EDX-P5-T01_stack_start13_skipMon_G0_AUDUSD-M5_MayAug.set"
)
text = src.read_text(encoding="utf-8")
body_i = text.index(";=== Indicators ===")
body = text[body_i:]
hdr = """; EDX-P5-T01_stack_start13_skipMon_G0_AUDUSD-M5_MayAug.set
; AUDUSD Edge Discovery · stack: StartHour=13 + TradeMon=false · SL/TP 300/300
; Expert: Experts\\BMRG\\BMRG.ex5
; Magic 8230501
; Beat: P3-T02 alone preferred; must beat P0 E_N+0.241 / EF+4.57
;
"""
text = hdr + body


def setf(t: str, k: str, v: str) -> str:
    def repl(m: re.Match[str]) -> str:
        old = m.group(0)
        if "||" in old:
            return f"{k}={v}||{old.split('||', 1)[1]}"
        return f"{k}={v}"

    return re.sub(rf"^{re.escape(k)}=.*$", repl, t, count=1, flags=re.M)


text = setf(text, "InpMagic", "8230501")
text = setf(text, "InpStartHour", "13")
text = setf(text, "InpTradeMon", "false")
out.write_text(text, encoding="utf-8", newline="\n")
print("wrote", out)
for k in ("InpMagic", "InpStartHour", "InpTradeMon", "InpSL_Points", "InpTP_Points"):
    m = re.search(rf"^{k}=([^\|\r\n]+)", text, flags=re.M)
    print(k, m.group(1) if m else "?")
