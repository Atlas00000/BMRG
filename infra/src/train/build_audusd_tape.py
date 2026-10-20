"""Build AUDUSD L2 train tape from Strategy Tester journal (AIOS FT / champ)."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INFRA = Path(__file__).resolve().parents[2]
LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261008.log"
)
OUT = INFRA / "artefacts" / "tape" / "AUDUSD_CHAMP_AIOS_TAPE.parquet"
POINT = 0.00001


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def session_id(hour: int) -> str:
    if 12 <= hour < 17:
        return "LON_NY"
    if 17 <= hour < 20:
        return "NY"
    return "OTHER"


def parse_run(chunk: str, magic: str) -> list[dict]:
    rows = []
    open_rec = None
    for line in chunk.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+) \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            bid, ask = float(m.group(6)), float(m.group(7))
            t = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S").replace(tzinfo=timezone.utc)
            open_rec = {
                "t": t,
                "side": "BUY" if m.group(2) == "buy" else "SELL",
                "spread_pts": (ask - bid) / POINT,
            }
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            win = "take" in m.group(2)
            t = open_rec["t"]
            dow_name = t.strftime("%a")
            hour = t.hour
            rows.append(
                {
                    "tape_schema": "aos_l1_aud_v0",
                    "symbol": "AUDUSD",
                    "tf": "M5",
                    "engine_magic": int(magic),
                    "hour_server": hour,
                    "dow": t.weekday(),  # Mon=0 .. aligned later via name
                    "dow_name": dow_name,
                    "session_id": session_id(hour),
                    "week_of_month": ((t.day - 1) // 7) + 1,
                    "month": t.month,
                    "spread_pts": float(open_rec["spread_pts"]),
                    "side": open_rec["side"],
                    "event_id": f"{magic}-AUDUSD-{open_rec['side']}-{t.strftime('%Y%m%d%H%M%S')}-{len(rows)}",
                    "entry_time": t.isoformat().replace("+00:00", "Z"),
                    "exit_reason": "TP" if win else "SL",
                    "y_lose": 0 if win else 1,
                    "pnl_r": 1.0 if win else -1.0,
                }
            )
            open_rec = None
    return rows


def main() -> None:
    text = load(LOG)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    # Prefer full Jan→Oct AIOS FT run (richest sample)
    chosen = None
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        if not mag or mag.group(1) != "8230921":
            continue
        if s.group(1).startswith("2026.01.01") and s.group(2).startswith("2026.10"):
            chosen = (s.group(1), s.group(2), c)
            break
    if not chosen:
        raise SystemExit("8230921 Jan→Oct run not found in 20261008.log")

    rows = parse_run(chosen[2], "8230921")
    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    meta = {
        "source_log": str(LOG),
        "window": f"{chosen[0]}->{chosen[1]}",
        "magic": 8230921,
        "n": len(df),
        "lose_rate": float(df["y_lose"].mean()),
        "path": str(OUT),
    }
    (OUT.with_suffix(".json")).write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
