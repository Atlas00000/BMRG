"""Parse Tester log for DE40stack (26141907) and P0 DE30 runs."""
from __future__ import annotations

import json
import re
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent


def main() -> None:
    runs: list[dict] = []
    cur = None
    # MT5 logs are often UTF-16; fall back to utf-8
    text = None
    for enc in ("utf-16", "utf-16-le", "utf-8", "cp1252"):
        try:
            text = LOG.read_text(encoding=enc)
            if "DE30" in text:
                break
        except Exception:
            continue
    if text is None:
        raise SystemExit("cannot decode tester log")

    for line in text.splitlines():
        if "Tester" in line and "DE30" in line and "testing of Experts" in line:
            m = re.search(r"from (\d{4}\.\d{2}\.\d{2}).*to (\d{4}\.\d{2}\.\d{2})", line)
            ts = re.search(r"\t(\d{2}:\d{2}:\d{2}\.\d+)\t", line)
            cur = {
                "tester_ts": ts.group(1) if ts else "?",
                "from": m.group(1) if m else "?",
                "to": m.group(2) if m else "?",
                "magic": None,
                "de_l2": None,
                "aos": None,
                "model": None,
                "final_balance": None,
                "l2_skips": 0,
                "entry_blocks_sample": [],
            }
            runs.append(cur)
            continue
        if cur is None:
            continue
        if "InpMagic=" in line:
            cur["magic"] = line.split("InpMagic=", 1)[1].strip().split()[0]
        if "InpAOS_DE_L2detEnable=" in line:
            cur["de_l2"] = line.split("=", 1)[1].strip().split()[0]
        if "InpAOS_Enable=" in line and cur.get("aos") is None:
            cur["aos"] = line.split("=", 1)[1].strip().split()[0]
        if "AOS ON |" in line and "sym=DE30" in line:
            mm = re.search(r"model=(\S+)", line)
            if mm:
                cur["model"] = mm.group(1)
        if "Entry blocked: AOS L2DET" in line:
            cur["l2_skips"] += 1
            if len(cur["entry_blocks_sample"]) < 5:
                cur["entry_blocks_sample"].append(line.split("\t")[-1][:120])
        if "final balance" in line:
            m = re.search(r"final balance ([0-9.]+)", line)
            if m:
                cur["final_balance"] = float(m.group(1))

    stack = [r for r in runs if r.get("magic") == "26141907"]
    p0 = [r for r in runs if r.get("magic") == "26101902"]
    report = {
        "log": str(LOG),
        "n_de30_runs": len(runs),
        "DE40stack_26141907": stack,
        "P0_26101902_sample": p0[:6],
        "deposit_assumed": 500.0,
    }
    for r in stack:
        if r["final_balance"] is not None:
            r["pnl"] = round(r["final_balance"] - 500.0, 2)
            r["ret_pct"] = round((r["final_balance"] / 500.0 - 1) * 100, 2)
    (OUT / "TESTER_LOG_REVIEW.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"stack_runs": len(stack), "p0_runs": len(p0)}, indent=2))
    for r in stack:
        print(
            f"{r['tester_ts']}  {r['from']}→{r['to']}  "
            f"bal={r['final_balance']} pnl={r.get('pnl')}  "
            f"L2skips={r['l2_skips']}  de_l2={r['de_l2']}  model={r['model']}"
        )


if __name__ == "__main__":
    main()
