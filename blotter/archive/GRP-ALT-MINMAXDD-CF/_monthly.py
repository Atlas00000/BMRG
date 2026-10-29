from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "infra" / "src"))

from diversify.load import TradeEvent
from diversify.panel import daily_panel
from grouping.enum_score import score_group

ARCH = Path(__file__).resolve().parent
MEMBERS = ["EURUSD", "DE40", "USDJPY", "AAPL"]


def parse_dt(s: str) -> datetime:
    s = (s or "").strip().strip('"')
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(s)


def main() -> None:
    events: dict[str, list[TradeEvent]] = {}
    for aid in MEMBERS:
        rows: list[TradeEvent] = []
        with (ARCH / "sleeves" / f"{aid}_live_fire_tape.csv").open(
            encoding="utf-8-sig", newline=""
        ) as f:
            for row in csv.DictReader(f):
                cd = parse_dt(row["close_time"]).date()
                pnl = float(row["pnl_R_design"])
                rows.append(
                    TradeEvent(
                        asset_id=aid,
                        close_date=cd,
                        open_dt=None,
                        pnl_R=pnl,
                        win=pnl > 0,
                        regime_tag=None,
                    )
                )
        events[aid] = rows

    panel = daily_panel(events)
    g = score_group(panel, tuple(MEMBERS))
    book = panel[MEMBERS].fillna(0.0).mean(axis=1)
    book.index = pd.to_datetime(book.index)
    m_book = book.groupby(book.index.to_period("M")).sum()

    sleeve_m: dict[str, pd.Series] = {}
    for a in MEMBERS:
        s = panel[a].fillna(0.0)
        s.index = pd.to_datetime(s.index)
        sleeve_m[a] = s.groupby(s.index.to_period("M")).sum()

    print(
        f"score_group sum_R={g['sum_R']} month_hit={g['month_hit']} "
        f"n_months={g['n_months']}"
    )
    print("month | group | EURUSD | DE40 | USDJPY | AAPL | hit")
    rows_out = []
    for per, gR in m_book.items():
        sm = {a: float(sleeve_m[a].get(per, 0.0)) for a in MEMBERS}
        hit = bool(gR > 0)
        print(
            f"{per} | {gR:+.2f} | {sm['EURUSD']:+.2f} | {sm['DE40']:+.2f} | "
            f"{sm['USDJPY']:+.2f} | {sm['AAPL']:+.2f} | {'Y' if hit else 'N'}"
        )
        rows_out.append(
            {
                "month": str(per),
                "group_R": round(float(gR), 4),
                **{a: round(sm[a], 4) for a in MEMBERS},
                "hit": hit,
            }
        )

    with (ARCH / "PERIOD_MONTHLY.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["month", "group_R", *MEMBERS, "hit"]
        )
        w.writeheader()
        w.writerows(rows_out)

    hits = sum(1 for v in m_book if v > 0)
    print(
        f"TOTAL group {float(m_book.sum()):+.4f}  "
        f"hits {hits}/{len(m_book)}"
    )


if __name__ == "__main__":
    main()
