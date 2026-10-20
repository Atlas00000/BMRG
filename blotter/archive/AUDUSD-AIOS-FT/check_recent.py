"""Summarise recent AUDUSD AIOS / champ tester runs from latest log(s)."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

LOG_DIR = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs"
)
OUT = Path(__file__).resolve().parent / "recent_runs.json"


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:2]
    all_runs = []
    for log in logs:
        text = load(log)
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
            if not mag:
                continue
            mval = mag.group(1)
            if mval not in ("8230921", "8230901", "8230501"):
                continue
            aos = re.search(r"InpAOS_Enable=(true|false)", c)
            mode = re.search(r"InpAiOsMode=(\d+)", c)
            w = re.search(r"InpAOS_W250=([0-9.]+)", c)
            pin = re.search(r"InpAiModelSemver=([^|\n]+)", c)
            sh = re.search(r"InpStartHour=([0-9.]+)", c)
            mon = re.search(r"InpTradeMon=(true|false)", c)
            finals = re.findall(r"final balance ([\d.]+)", c)
            # AOS banner / model line
            model_line = re.search(r"AOS ON \|[^\n]+", c)
            semver_warn = "semver mismatch" in c
            baked = re.search(r"model=(L2skip_[^\s|]+)", c)
            # interventions
            skips = len(re.findall(r"WOULD_SKIP|L2AUD WOULD_SKIP|L2AI.*SKIP", c))
            halts = len(re.findall(r"halt=1|HALT_MAXDD|HALT_f0|L3 HALT", c))
            closes = len(re.findall(r"AOS close (TP|SL)", c))
            life = Counter(re.findall(r"life=(\w+)", c))
            halt_vals = Counter(re.findall(r"halt=(\d+)", c))
            f_vals = Counter(re.findall(r" f=([\d.]+)", c))
            # trade count from market orders
            orders = len(re.findall(r"market (?:buy|sell) [\d.]+ AUDUSD sl:", c))
            # W250 EF after window filled
            efs = re.findall(r"W250 EF=([-\d.]+) EN=([-\d.]+)", c)
            non_zero_ef = [(a, b) for a, b in efs if float(a) != 0.0 or float(b) != 0.0]

            all_runs.append(
                {
                    "log": log.name,
                    "run_i": i,
                    "window": f"{s.group(1)}->{s.group(2)}",
                    "magic": mval,
                    "AOS": aos.group(1) if aos else "?",
                    "AiOsMode": mode.group(1) if mode else "?",
                    "W": w.group(1) if w else "?",
                    "pin_input": (pin.group(1).strip() if pin else "?"),
                    "StartHour": sh.group(1) if sh else "?",
                    "TradeMon": mon.group(1) if mon else "?",
                    "final": finals[-1] if finals else None,
                    "pnl": round(float(finals[-1]) - 400.0, 2) if finals else None,
                    "orders": orders,
                    "aos_closes_logged": closes,
                    "L2_skip_hits": skips,
                    "halt_signal_hits": halts,
                    "halt_value_counts": dict(halt_vals),
                    "life_counts": dict(life),
                    "f_counts": dict(f_vals),
                    "semver_mismatch_warn": semver_warn,
                    "model_from_banner": baked.group(1) if baked else None,
                    "aos_banner": model_line.group(0) if model_line else None,
                    "w250_nonzero_samples": len(non_zero_ef),
                    "w250_sample_tail": non_zero_ef[-3:] if non_zero_ef else efs[-3:],
                }
            )

    # Prefer newest log's runs last
    OUT.write_text(json.dumps({"logs": [p.name for p in logs], "runs": all_runs}, indent=2), encoding="utf-8")
    # Print concise table
    print("logs:", [p.name for p in logs])
    print(f"{'log':10} {'i':>3} {'window':28} {'mag':8} {'W':>4} {'AOS':5} {'final':>8} {'pnl':>7} {'ord':>4} {'skip':>4} {'halt':>4} model")
    for r in all_runs:
        print(
            f"{r['log']:10} {r['run_i']:3d} {r['window']:28} {r['magic']:8} {r['W']:>4} "
            f"{r['AOS']:5} {str(r['final'] or '?'):>8} {str(r['pnl'] if r['pnl'] is not None else '?'):>7} "
            f"{r['orders']:4d} {r['L2_skip_hits']:4d} {r['halt_signal_hits']:4d} "
            f"{r['model_from_banner'] or r['pin_input']}"
        )
        if r["aos_banner"]:
            print("   ", r["aos_banner"][:120])
        if r["life_counts"] or r["f_counts"]:
            print("    life=", r["life_counts"], "f=", r["f_counts"], "halt=", r["halt_value_counts"])
        if r["w250_sample_tail"]:
            print("    W50/250 EF,EN tail=", r["w250_sample_tail"])


if __name__ == "__main__":
    main()
