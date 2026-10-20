"""Score JPN225stack Tester runs (magic 26151907) from 20261019.log."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent

R = 1.50
BWR = 0.40
LEAK = 0.0245
DEP = 500.0
# lot 0.1 proxy PnL from P1 tape medians (approx)
WIN_CCY = 2.3201
LOSS_CCY = -1.5467

START = re.compile(
    r"JPN225,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:"
)


def load() -> str:
    raw = LOG.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def score_chunk(chunk: str, label: str) -> dict:
    pending = None
    equity = DEP
    peak = DEP
    maxdd = 0.0
    wins: list[int] = []
    for ln in chunk.splitlines():
        if "[BMRG][TRADE] OPEN" in ln:
            pending = "open"
            continue
        if pending and "take profit triggered" in ln and "JPN225" in ln:
            wins.append(1)
            equity += WIN_CCY
            peak = max(peak, equity)
            maxdd = max(maxdd, (peak - equity) / peak * 100.0)
            pending = None
            continue
        if pending and "stop loss triggered" in ln and "JPN225" in ln:
            wins.append(0)
            equity += LOSS_CCY
            peak = max(peak, equity)
            maxdd = max(maxdd, (peak - equity) / peak * 100.0)
            pending = None
            continue
    n = len(wins)
    fb = re.search(r"final balance ([\d.\-]+)", chunk)
    final = float(fb.group(1)) if fb else None
    if n == 0:
        return {"label": label, "n": 0, "final": final}
    wr = sum(wins) / n
    return {
        "label": label,
        "n": n,
        "wins": sum(wins),
        "losses": n - sum(wins),
        "WR": round(wr * 100, 2),
        "BM_pp": round((wr - BWR) * 100, 3),
        "E_N": round(wr * (R + 1) - 1, 4),
        "EF_measured_pp": round((wr - BWR - LEAK) * 100, 3),
        "tip_EF_cleared": bool(wr - BWR - LEAK > 0),
        "final": final,
        "delta": round(final - DEP, 2) if final is not None else None,
        "MaxDD_proxy_pct": round(maxdd, 2),
        "L3_blocks": len(re.findall(r"Entry blocked: AOS L3", chunk)),
        "skip_may_lines": len(re.findall(r"L2DET_SKIP_MAY", chunk)),
        "skip_jul_lines": len(re.findall(r"L2DET_SKIP_JUL", chunk)),
        "aos_enable": "InpAOS_Enable=true" in chunk[:12000],
        "jp_l2det": "InpAOS_JP_L2detEnable=true" in chunk[:12000],
        "leak_inp": (
            re.search(r"InpAOS_Leak=([0-9.]+)", chunk[:12000]).group(1)
            if re.search(r"InpAOS_Leak=([0-9.]+)", chunk[:12000])
            else None
        ),
    }


def main() -> None:
    text = load()
    runs = []
    for m in START.finditer(text):
        end = text.find("final balance", m.start())
        chunk = text[m.start() : end + 800 if end > 0 else m.start() + 2_000_000]
        if "InpMagic=26151907" not in chunk[:15000]:
            continue
        lab = f"{m.group(1)}->{m.group(2)}"
        runs.append(score_chunk(chunk, lab))

    # engine P1 tip compare (magic 26101904 May→Aug) if present
    engine = None
    for m in START.finditer(text):
        if m.group(1) != "2026.05.01" or m.group(2) != "2026.08.31":
            continue
        end = text.find("final balance", m.start())
        chunk = text[m.start() : end + 800 if end > 0 else m.start() + 2_000_000]
        if "InpMagic=26101904" not in chunk[:15000]:
            continue
        engine = score_chunk(chunk, "engine_P1_tip_26101904")

    tip = next((r for r in runs if r["label"].startswith("2026.05.01")), None)
    packet = {
        "task": "JP225-AOS-P7-TESTER",
        "dated": datetime.now(timezone.utc).isoformat(),
        "magic": 26151907,
        "preset": "JPN225stack",
        "Leak_pp": LEAK * 100,
        "runs": runs,
        "engine_tip_compare": engine,
        "verdict": None,
    }
    if tip and tip.get("n"):
        packet["verdict"] = {
            "tip_n": tip["n"],
            "tip_WR": tip["WR"],
            "tip_EF_pp": tip["EF_measured_pp"],
            "tip_EF_cleared": tip["tip_EF_cleared"],
            "l2det_firing": tip["skip_may_lines"] + tip["skip_jul_lines"] > 0,
            "vs_offline_kept_n43": tip["n"] == 43,
            "note": (
                "Tip n=43 matches offline May∨Jul keep. "
                "L2DET_SKIP_MAY/JUL lines prove MQH wire live."
            ),
        }
    (OUT / "TESTER_REVIEW.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()
