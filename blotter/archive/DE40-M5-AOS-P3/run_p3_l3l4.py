"""DE40-M5-AOS-P3 — L3/L4 offline sim on tip/YTD ± v1b L2det stack."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)
OUT = Path(__file__).resolve().parent

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.07  # prior authority (not journal proxy)
DEPOSIT = 500.0
DD_LIMIT = 25.0
EQUITY_HALT = 15.0
W15, W20, W50 = 15, 20, 50
BASELINE_TIP_EN = 0.207317
# Tip ~123 fires / ~165d → ~67 / 90d; stall at 50%
BASELINE_FIRES_90D = 65
SPREAD_BASELINE_MED = 84  # tip journal p50


def annotate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["close_dt"] = pd.to_datetime(df["close_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["hour"] = df["hour"].astype(int)
    df["cell_buy"] = df["cell_buy"].astype(int)
    buy_h14_16 = (df["cell_buy"] == 1) & (df["hour"].isin([14, 16]))
    buy_oct = (df["cell_buy"] == 1) & (df["month"].astype(str) == "2026-10")
    df["v1b_skip"] = (buy_h14_16 | buy_oct).astype(int)
    df["h14_16_skip"] = df["hour"].isin([14, 16]).astype(int)
    df["oct_skip"] = (df["month"].astype(str) == "2026-10").astype(int)
    return df


def load(name: str) -> pd.DataFrame:
    return annotate(pd.read_csv(TAPES / name))


def window_en(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float(wins.mean() * (R + 1) - 1)


def window_ef_pp(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float((wins.mean() - BWR - LEAK) * 100)


def lifecycle(en15: float, en15_prev: float | None, en20: float, ef15: float) -> str:
    if np.isnan(en15):
        return "WARMUP"
    if not np.isnan(en20) and en20 <= 0 and ef15 <= 0:
        return "BELOW"
    if ef15 <= 1.0 or en15 < 0:
        return "NEAR"
    if en15_prev is not None and en15 < en15_prev - 1e-9:
        return "COMPRESSING_CANDIDATE"
    if en15 > BASELINE_TIP_EN and (
        en15_prev is None or en15 >= en15_prev - 1e-9
    ):
        return "EXPANDING"
    if en15 >= 0:
        return "STABLE"
    return "NEAR"


def f_mult(life: str, derisk: bool, halt: bool) -> float:
    if halt:
        return 0.0
    table = {
        "EXPANDING": 1.0,
        "STABLE": 1.0,
        "COMPRESSING": 0.5,
        "COMPRESSING_CANDIDATE": 0.5,
        "NEAR": 0.25,
        "BELOW": 0.0,
        "WARMUP": 1.0,
    }
    f = table.get(life, 1.0)
    if derisk:
        f = min(f, 0.5)
    return f


def simulate(df: pd.DataFrame, label: str) -> dict:
    wins = df["win"].to_numpy()
    pnls = df["pnl"].to_numpy()
    times = df["close_dt"].to_list()
    spreads = df["spread_pts"].astype(int).to_numpy()

    equity = DEPOSIT
    peak = DEPOSIT
    start_eq = DEPOSIT
    path = []
    trips = []
    en15_hist: list[float | None] = []
    compress_streak = 0
    loss_streak = 0
    max_loss_streak = 0
    halt_latched = False
    halt_reason = ""

    for i in range(len(df)):
        equity += pnls[i]
        peak = max(peak, equity)
        dd_peak = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        dd_start = (start_eq - equity) / start_eq * 100.0 if start_eq > 0 else 0.0

        if wins[i] == 1:
            loss_streak = 0
        else:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)

        w15 = wins[max(0, i - W15 + 1) : i + 1]
        w20 = wins[max(0, i - W20 + 1) : i + 1]
        w50 = wins[max(0, i - W50 + 1) : i + 1]
        en15 = window_en(w15) if len(w15) >= W15 else float("nan")
        en20 = window_en(w20) if len(w20) >= W20 else float("nan")
        en50 = window_en(w50) if len(w50) >= W50 else float("nan")
        ef15 = window_ef_pp(w15) if len(w15) >= W15 else float("nan")
        prev = en15_hist[-1] if en15_hist else None
        life = lifecycle(en15, prev if prev is not None else None, en20, ef15)

        if (
            not np.isnan(en15)
            and prev is not None
            and not np.isnan(prev)
            and en15 < prev - 1e-9
        ):
            compress_streak += 1
        else:
            compress_streak = 0
        if life == "COMPRESSING_CANDIDATE" and compress_streak >= 2:
            life = "COMPRESSING"
        elif life == "COMPRESSING_CANDIDATE":
            life = "STABLE" if en15 >= 0 else "NEAR"

        en15_hist.append(en15 if not np.isnan(en15) else None)

        derisk = False
        halt = halt_latched
        reason = halt_reason if halt_latched else ""

        if dd_peak >= DD_LIMIT:
            halt = True
            reason = f"HALT_MAXDD dd={dd_peak:.2f}>={DD_LIMIT}"
        elif dd_peak >= 0.8 * DD_LIMIT:
            derisk = True
            reason = f"DERISK_0.8_DD dd={dd_peak:.2f}"

        equity_halt = dd_start >= EQUITY_HALT

        if len(w20) >= W20 and life == "BELOW":
            halt = True
            reason = f"HALT_f0_BELOW_FRONTIER EN20={en20:.3f} EF15={ef15:.2f}"

        streak_warn = loss_streak >= 3
        streak_l3 = loss_streak >= 5

        if halt and not halt_latched:
            halt_latched = True
            halt_reason = reason
            trips.append(
                {
                    "i": i,
                    "time": str(times[i]),
                    "reason": reason,
                    "equity": round(equity, 2),
                    "dd_peak": round(dd_peak, 2),
                    "en15": None if np.isnan(en15) else round(en15, 4),
                    "en20": None if np.isnan(en20) else round(en20, 4),
                    "en50": None if np.isnan(en50) else round(en50, 4),
                    "life": life,
                }
            )

        t1 = times[i]
        t0 = t1 - pd.Timedelta(days=30)
        n30 = int(sum(1 for t in times[: i + 1] if t >= t0))
        fires_90_equiv = n30 * 3
        freq_stall = fires_90_equiv < 0.5 * BASELINE_FIRES_90D

        spr_win = spreads[max(0, i - 19) : i + 1]
        spr_med = float(np.median(spr_win))
        cost_drift = spr_med > SPREAD_BASELINE_MED + 40

        bus = "NONE"
        if life == "BELOW" or halt:
            bus = "L3_HALT"
        elif life == "COMPRESSING":
            bus = "INVESTIGATE"
        elif life == "NEAR" or derisk:
            bus = "DERISK"
        elif streak_l3:
            bus = "STREAK_WATCH"
        elif freq_stall and len(w15) >= W15:
            bus = "FREQUENCY_STALL_WARN"

        path.append(
            {
                "i": i,
                "open_time": df.loc[i, "open_time"],
                "close_time": df.loc[i, "close_time"],
                "win": int(wins[i]),
                "equity": round(equity, 2),
                "dd_peak_pct": round(dd_peak, 3),
                "dd_start_pct": round(dd_start, 3),
                "en15": None if np.isnan(en15) else round(en15, 4),
                "en20": None if np.isnan(en20) else round(en20, 4),
                "en50": None if np.isnan(en50) else round(en50, 4),
                "ef15_pp": None if np.isnan(ef15) else round(ef15, 3),
                "life": life,
                "f_mult": f_mult(life, derisk, halt),
                "haltL3": halt,
                "deriskL3": derisk,
                "equity_halt_ea": equity_halt,
                "loss_streak": loss_streak,
                "streak_warn": streak_warn,
                "n30": n30,
                "freq_stall_warn": freq_stall,
                "cost_drift_warn": cost_drift,
                "spread_med20": round(spr_med, 1),
                "bus": bus,
                "reason": reason,
            }
        )

    lives = [p["life"] for p in path if p["life"] != "WARMUP"]
    buses = [p["bus"] for p in path]
    max_dd = max(p["dd_peak_pct"] for p in path) if path else 0
    freq_ticks = sum(1 for p in path if p["freq_stall_warn"])
    cost_ticks = sum(1 for p in path if p["cost_drift_warn"])
    return {
        "label": label,
        "n": len(df),
        "final_equity": round(equity, 2),
        "net_pnl": round(equity - DEPOSIT, 2),
        "max_dd_peak_pct": round(max_dd, 3),
        "max_loss_streak": max_loss_streak,
        "trips": trips,
        "trip_count": len(trips),
        "life_counts": {k: lives.count(k) for k in sorted(set(lives))},
        "bus_counts": {k: buses.count(k) for k in sorted(set(buses))},
        "freq_stall_ticks": freq_ticks,
        "cost_drift_ticks": cost_ticks,
        "halt_latched": halt_latched,
        "last_life": path[-1]["life"] if path else None,
        "last_en15": path[-1]["en15"] if path else None,
        "last_en20": path[-1]["en20"] if path else None,
        "last_en50": path[-1]["en50"] if path else None,
        "path": path,
    }


def path_csv(sim: dict, name: str) -> None:
    rows = sim["path"]
    if not rows:
        return
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def compact_sim(sim: dict) -> dict:
    return {
        "n": sim["n"],
        "final": sim["final_equity"],
        "max_dd": sim["max_dd_peak_pct"],
        "trips": sim["trip_count"],
        "trip_reasons": [t["reason"] for t in sim["trips"]],
        "life_counts": sim["life_counts"],
        "bus_counts": sim["bus_counts"],
        "max_loss_streak": sim["max_loss_streak"],
        "freq_stall_ticks": sim["freq_stall_ticks"],
        "cost_drift_ticks": sim["cost_drift_ticks"],
        "last_en15": sim["last_en15"],
        "last_en20": sim["last_en20"],
        "last_en50": sim["last_en50"],
        "last_life": sim["last_life"],
        "halt_latched": sim["halt_latched"],
    }


def main() -> None:
    tip = load("de40_m5_tip_fire_tape_v0.csv")
    ytd = load("de40_m5_ytd_fire_tape_v0.csv")
    v1b = tip[tip["v1b_skip"] == 0].reset_index(drop=True)
    h14 = tip[tip["h14_16_skip"] == 0].reset_index(drop=True)
    ytd_v1b = ytd[ytd["v1b_skip"] == 0].reset_index(drop=True)

    sims_raw = {
        "P0_tip": simulate(tip, "P0_tip"),
        "v1b_kept": simulate(v1b, "v1b_kept"),
        "H14_16_aggressive_kept": simulate(h14, "H14_16_aggressive_kept"),
        "P0_ytd": simulate(ytd, "P0_ytd"),
        "v1b_ytd_kept": simulate(ytd_v1b, "v1b_ytd_kept"),
    }

    sims = {}
    for k, sim in sims_raw.items():
        path_csv(sim, f"health_path_{k}.csv")
        sims[k] = {**sim, "path_len": len(sim["path"])}
        del sims[k]["path"]

    policy = {
        "task": "DE40-M5-AOS-P3",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "v1b_rule": "(BUY AND hour in {14,16}) OR (BUY AND month==Oct)",
        "bindings": {
            "DD_Limit_pct": DD_LIMIT,
            "derisk_at_pct": 0.8 * DD_LIMIT,
            "EquityHalt_pct": EQUITY_HALT,
            "BWR": 44.4,
            "R": R,
            "Leak_prior_pp": LEAK * 100,
            "Leak_source": "prior_7.0pp",
            "W_health": [W15, W20, W50],
            "W250_preset_note": (
                "Dense M5 tip n=123 — W20/W50 first-class. "
                "InpAOS_W250=50 for research OS .set when wiring."
            ),
            "baseline_fires_90d": BASELINE_FIRES_90D,
            "baseline_tip_E_N": BASELINE_TIP_EN,
            "spread_baseline_med": SPREAD_BASELINE_MED,
        },
        "sims": {k: {kk: vv for kk, vv in v.items() if kk != "path"} for k, v in sims.items()},
        "recommend_bus": {
            "BELOW": "L3_HALT f=0",
            "COMPRESSING": "INVESTIGATE (regime/execution) · f=0.5",
            "NEAR / DERISK_0.8_DD": "DERISK f<=0.5",
            "STREAK>=5": "STREAK_WATCH · align engine pause",
            "FREQUENCY_STALL": "WARN only — do not lift ATR max",
            "EXPANDING/STABLE": "NONE f=1.0",
            "L2det_v1b_WOULD_SKIP": "skip fire — not an L3 trip",
        },
    }
    (OUT / "P3_L3L4.json").write_text(json.dumps(policy, indent=2), encoding="utf-8")

    compact = {k: compact_sim(v) for k, v in sims.items()}
    (OUT / "P3_SUMMARY.json").write_text(
        json.dumps(compact, indent=2), encoding="utf-8"
    )
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
