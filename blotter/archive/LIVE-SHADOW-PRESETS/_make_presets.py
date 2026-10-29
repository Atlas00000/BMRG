"""Generate full-input SHADOW presets for every live VPS chart from the 2026-10-28 23:00 input dump.

Only changes vs live: InpAiOsMode=1 (SHADOW), InpLogGateBlocks=true.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BMRG = HERE.parents[2]
MQL5 = BMRG.parents[1]
DUMP = HERE / "vps_inputs_20261028_2300.json"
OUT_DIRS = [BMRG / "Presets", BMRG / "doc" / "presets", MQL5 / "Profiles" / "Tester" / "BMRG"]
OVERRIDES = {"InpAiOsMode": "1", "InpLogGateBlocks": "true"}
TESTER = MQL5 / "Profiles" / "Tester" / "BMRG"
LIVE_DIR = TESTER / "live"  # the 7 presets to load on the VPS charts
# Deployed posture per chart (mirror of `deploy` in infra/src/diversify/live_runs.py)
DEPLOY = {"EURUSD,M5": "SHADOW", "AUDUSD,M5": "SHADOW", "UK100,M5": "SHADOW", "DE30,M5": "SHADOW",
          "Apple,M5": "CURRENT", "JPN225,M5": "CURRENT", "USDJPY,M15": "CURRENT"}
# chart key -> (preset file name, doc alias)
NAMES = {
    "EURUSD,M5": ("LIVE-SHADOW_EURUSD_M5.set", "EURUSD"),
    "AUDUSD,M5": ("LIVE-SHADOW_AUDUSD_M5.set", "AUDUSD"),
    "Apple,M5": ("LIVE-SHADOW_Apple_M5.set", "AAPL"),
    "UK100,M5": ("LIVE-SHADOW_UK100_M5.set", "UK100"),
    "JPN225,M5": ("LIVE-SHADOW_JPN225_M5.set", "JP225"),
    "DE30,M5": ("LIVE-SHADOW_DE30_M5.set", "DE40"),
    "USDJPY,M15": ("LIVE-SHADOW_USDJPY_M15.set", "USDJPY"),
}


def main() -> None:
    dump = json.loads(DUMP.read_text(encoding="utf-8"))
    for chart, (fname, alias) in NAMES.items():
        inputs = dict(dump[chart])
        before = {k: inputs[k] for k in OVERRIDES}
        inputs.update(OVERRIDES)
        sym, tf = chart.split(",")
        lines = [
            f"; LIVE-SHADOW {sym} {tf} ({alias}) · magic {inputs['InpMagic']} · risk {inputs['InpRiskPercent']}%",
            "; Generated 2026-10-29 from VPS input dump logs/hosting.6917926.experts/20261028.log (23:00:00, EA 1.27)",
            f"; = exact live chart inputs except InpAiOsMode {before['InpAiOsMode']}->1 (SHADOW) · "
            f"InpLogGateBlocks {before['InpLogGateBlocks']}->true",
            "; SHADOW: L2 AI / L2det skips are logged ('AOS SHADOW skip') but entries still execute",
            f"; Chart: {sym} {tf} · Expert: Experts\\BMRG\\BMRG.ex5 (>= 1.27)",
            ";",
        ] + [f"{k}={v}" for k, v in inputs.items()]
        text = "\r\n".join(lines) + "\r\n"
        for d in OUT_DIRS:
            if d == TESTER:
                continue  # Tester copy placed below (live/ if deployed)
            d.mkdir(parents=True, exist_ok=True)
            (d / fname).write_bytes(text.encode("utf-16"))  # MT5-native UTF-16 LE + BOM
        _place(fname, text, DEPLOY[chart] == "SHADOW")
        print(f"{chart:12} -> {fname}  inputs={len(inputs)}  deploy={DEPLOY[chart]}")

        # Baseline twin for Tester comparison: exact current live inputs (LIVE_WITHHOLD), Tester profile only.
        base = dict(dump[chart])
        base_text = "\r\n".join(
            [
                f"; LIVE-CURRENT {sym} {tf} ({alias}) · exact VPS inputs 2026-10-28 23:00 · skips enforced (LIVE_WITHHOLD)",
                "; Deploy preset for sleeves kept on skips (Apple, JPN225, USDJPY) · Tester baseline for the others",
                ";",
            ]
            + [f"{k}={v}" for k, v in base.items()]
        ) + "\r\n"
        bname = fname.replace("LIVE-SHADOW_", "LIVE-CURRENT_")
        _place(bname, base_text, DEPLOY[chart] == "CURRENT")


def _place(fname: str, text: str, deployed: bool) -> None:
    """Deployed preset -> Profiles/Tester/BMRG/live/, comparison twin -> Profiles/Tester/BMRG/ (never both)."""
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    keep, drop = (LIVE_DIR, TESTER) if deployed else (TESTER, LIVE_DIR)
    (keep / fname).write_bytes(text.encode("utf-16"))
    (drop / fname).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
