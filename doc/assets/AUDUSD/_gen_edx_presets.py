"""Generate AUDUSD EDX presets under Profiles/Tester/BMRG/AUDUSD/."""
from __future__ import annotations

from pathlib import Path
import re

SRC = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG"
    r"\BOOKA-Harvest_AUDUSD_M5_G0.set"
)
OUT = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\AUDUSD"
)

# name -> (magic, header_lines, overrides dict)
PRESETS: dict[str, tuple[int, list[str], dict[str, str]]] = {
    "EDX-P0-T01_baseline_G0_AUDUSD-M5_MayAug.set": (
        8230101,
        [
            "; EDX-P0-T01 — AUDUSD Book A baseline scorecard (no strategy change)",
            "; Window: 2026.05.01 -> 2026.08.31 · every tick · ACCOUNT CURRENCY · deposit 400+",
            "; Beat: N/A — this IS the baseline · archive EDX-P0-T01",
        ],
        {},
    ),
    "EDX-P0-T04_baseline_G0_AUDUSD-M5_MayOct.set": (
        8230104,
        [
            "; EDX-P0-T04 — longer tip stress (May->Oct) vs P0-T01",
            "; Window: 2026.05.01 -> 2026.10.03 · tip regime check",
        ],
        {},
    ),
    "EDX-P05-T01_integrity_G0_AUDUSD-M5_MayAug.set": (
        8230151,
        [
            "; EDX-P05-T01 — data integrity re-run (same geometry as P0-T01)",
            "; Window: 2026.05.01 -> 2026.08.31 · export deals for costs",
        ],
        {},
    ),
    "EDX-P1-T01_sessionCells_G0_AUDUSD-M5_MayAug.set": (
        8230111,
        [
            "; EDX-P1-T01 — session cell score (prefer offline on P0 blotter; re-run if needed)",
            "; Window: 2026.05.01 -> 2026.08.31 · no input change",
        ],
        {},
    ),
    "EDX-P1-T02_dowCells_G0_AUDUSD-M5_MayAug.set": (
        8230112,
        [
            "; EDX-P1-T02 — DOW cell score (prefer offline on P0 blotter)",
            "; Window: 2026.05.01 -> 2026.08.31 · no input change",
        ],
        {},
    ),
    "EDX-P2-T01_SLtighter240_RR1_AUDUSD-M5_MayAug.set": (
        8230201,
        [
            "; EDX-P2-T01 — SL/TP 240/240 (RR1) ATR-downscale · R-side / AL hypothesis",
            "; Target: AL, R, RR-R, E_N, EF · must not drop E_N vs P0",
        ],
        {"InpSL_Points": "240", "InpTP_Points": "240"},
    ),
    "EDX-P2-T02_SLwider360_RR1_AUDUSD-M5_MayAug.set": (
        8230202,
        [
            "; EDX-P2-T02 — SL/TP 360/360 (RR1) ATR-upscale",
            "; Target: WR/AL tradeoff · full health vector vs P0",
        ],
        {"InpSL_Points": "360", "InpTP_Points": "360"},
    ),
    "EDX-P2-T03_TPwider450_RR1.5_AUDUSD-M5_MayAug.set": (
        8230203,
        [
            "; EDX-P2-T03 — SL300/TP450 RR=1.5 Growth neighborhood · payoff test",
            "; Target: R, BWR, E_N, EF — reject if E_N or EF falls vs P0",
        ],
        {"InpSL_Points": "300", "InpTP_Points": "450"},
    ),
    "EDX-P2-T04_TPtighter240_RR0.8_AUDUSD-M5_MayAug.set": (
        8230204,
        [
            "; EDX-P2-T04 — SL300/TP240 RR=0.8 · hit-rate vs payoff trap check",
            "; Forbidden: accept on WR alone if E_N drops",
        ],
        {"InpSL_Points": "300", "InpTP_Points": "240"},
    ),
    "EDX-P3-T01_skipMon_G0_AUDUSD-M5_MayAug.set": (
        8230301,
        [
            "; EDX-P3-T01 — skip Monday (profile BM soft) · filter hygiene",
            "; FREQUENCY_STALL: n must stay >= 50% of P0 baseline",
        ],
        {"InpTradeMon": "false"},
    ),
    "EDX-P3-T02_startHour13_G0_AUDUSD-M5_MayAug.set": (
        8230302,
        [
            "; EDX-P3-T02 — StartHour 13 (cut hour-12 weak pocket)",
            "; Target: WR, BM, EF · freq >= 50% P0",
        ],
        {"InpStartHour": "13"},
    ),
    "EDX-P3-T03_BBDev2.5_G0_AUDUSD-M5_MayAug.set": (
        8230303,
        [
            "; EDX-P3-T03 — BBDev 2.5 stricter band · entry quality",
            "; Target: WR/BM; watch FREQUENCY_STALL",
        ],
        {"InpBBDev": "2.5"},
    ),
    "EDX-P3-T04_cooldown6_G0_AUDUSD-M5_MayAug.set": (
        8230304,
        [
            "; EDX-P3-T04 — CooldownBars 6 · reduce clustered re-entries",
            "; Target: DEPENDENCE / streak · E_N hold",
        ],
        {"InpCooldownBars": "6"},
    ),
    "EDX-P5-T01_stackBest_G0_AUDUSD-M5_MayAug.set": (
        8230501,
        [
            "; EDX-P5-T01 — PLACEHOLDER stack — update inputs after P2/P3 ACCEPTs",
            "; Default = P0 geometry until discovery fills winners",
        ],
        {},
    ),
    "EDX-P6-T01_candidate_G0_AUDUSD-M5_long.set": (
        8230601,
        [
            "; EDX-P6-T01 — validation candidate (copy best stack before G1-G5)",
            "; Window: 2026.03.23 -> 2026.09.21 (or longest available)",
            "; PLACEHOLDER — freeze inputs from EDX-P5-T01 ACCEPT",
        ],
        {},
    ),
}


def set_field(text: str, key: str, value: str) -> str:
    pat = re.compile(rf"^{re.escape(key)}=.*$", re.M)
    if not pat.search(text):
        raise KeyError(key)
    # preserve optimiser tail after ||
    def repl(m: re.Match[str]) -> str:
        old = m.group(0)
        if "||" in old:
            tail = old.split("||", 1)[1]
            return f"{key}={value}||{tail}"
        return f"{key}={value}"

    return pat.sub(repl, text, count=1)


def main() -> None:
    base = SRC.read_text(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (magic, headers, overrides) in PRESETS.items():
        text = base
        # strip old header comments through first blank after magic comment block
        body_start = text.find(";=== Indicators ===")
        body = text[body_start:] if body_start >= 0 else text
        hdr = [
            f"; {name}",
            "; AUDUSD Edge Discovery · engine only (AOS OFF) · G0",
            "; Expert: Experts\\BMRG\\BMRG.ex5",
            f"; Magic {magic}",
            *headers,
            ";",
        ]
        text = "\n".join(hdr) + "\n" + body
        text = set_field(text, "InpMagic", str(magic))
        for k, v in overrides.items():
            text = set_field(text, k, v)
        path = OUT / name
        path.write_text(text, encoding="utf-8", newline="\n")
        print("wrote", path.name)


if __name__ == "__main__":
    main()
