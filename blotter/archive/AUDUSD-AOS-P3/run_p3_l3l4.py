"""AUDUSD-AOS-P3 — L3/L4 offline sim on tip ± L2det v1 (BUY∧May)."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\AUDUSD\tapes"
)
OUT = Path(__file__).resolve().parent

R = 1.0
BWR = 1.0 / (1.0 + R)  # 0.50
LEAK = 0.05  # journal_2x_entry_spread_median proxy
DEPOSIT = 400.0  # Tester baseline
DD_LIMIT = 25.0
EQUITY_HALT = 15.0
W15, W20 = 15, 20
BASELINE_TIP_EN = 0.2683
BASELINE_FIRES_90D = 30  # ~10/30d tip → ~30/90d
SPREAD_BASELINE_MED = 15.0  # tip median


def load_tip() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "audusd_m15_tip_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["close_dt"] = pd.to_datetime(df["close_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["spread_pts"] = df["spread_pts"].astype(int)
    df["nights_held"] = df["nights_held"].astype(int)
    df["v1_skip"] = (
        (df["side"] == "BUY") & (df["cell_month_may"].astype(int) == 1)
    ).astype(int)
    df["alt_buy_thu_skip"] = (
        (df["side"] == "BUY") & (df["cell_dow_thu"].astype(int) == 1)
    ).astype(int)
    return df


def load_long() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "audusd_m15_long_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["close_dt"] = pd.to_datetime(df["close_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["spread_pts"] = df["spread_pts"].astype(int)
    df["nights_held"] = df["nights_held"].astype(int)
    df["v1_skip"] = (
        (df["side"] == "BUY") & (df["cell_month_may"].astype(int) == 1)
    ).astype(int)
    return df


def window_en(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float(wins.mean() * (R + 1) - 1)


def window_ef_pp(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    wr = wins.mean()
    return float((wr - BWR - LEAK) * 100)


def lifecycle(en15: float, en15_prev: float | None, en20: float, ef15: float) -> str:
    if np.isnan(en15):
        return "WARMUP"
    if en20 <= 0 and ef15 <= 0:
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
    spreads = df["spread_pts"].to_numpy()
    nights = df["nights_held"].to_numpy()

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
    overnight_cluster = 0
    max_overnight_cluster = 0

    for i in range(len(df)):
        equity += pnls[i]
        peak = max(peak, equity)
        dd_peak = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        dd_start = (start_eq - equity) / start_eq * 100.0 if start_eq > 0 else 0.0

        if nights[i] == 1:
            overnight_cluster += 1
            max_overnight_cluster = max(max_overnight_cluster, overnight_cluster)
        else:
            overnight_cluster = 0

        if wins[i] == 1:
            loss_streak = 0
        else:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)

        w15 = wins[max(0, i - W15 + 1) : i + 1]
        w20 = wins[max(0, i - W20 + 1) : i + 1]
        en15 = window_en(w15) if len(w15) >= W15 else float("nan")
        en20 = window_en(w20) if len(w20) >= W20 else float("nan")
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
                    "life": life,
                }
            )

        t1 = times[i]
        t0 = t1 - pd.Timedelta(days=30)
        n30 = int(sum(1 for t in times[: i + 1] if t >= t0))
        fires_90_equiv = n30 * 3
        freq_stall = fires_90_equiv < 0.5 * BASELINE_FIRES_90D

        cost_drift = float(spreads[i]) > SPREAD_BASELINE_MED + 4  # >19 pts

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
        elif cost_drift:
            bus = "COST_DRIFT_WARN"

        path.append(
            {
                "i": i,
                "open_time": df.loc[i, "open_time"],
                "close_time": df.loc[i, "close_time"],
                "win": int(wins[i]),
                "nights_held": int(nights[i]),
                "spread_pts": int(spreads[i]),
                "equity": round(equity, 2),
                "dd_peak_pct": round(dd_peak, 3),
                "dd_start_pct": round(dd_start, 3),
                "en15": None if np.isnan(en15) else round(en15, 4),
                "en20": None if np.isnan(en20) else round(en20, 4),
                "ef15_pp": None if np.isnan(ef15) else round(ef15, 3),
                "life": life,
                "f_mult": f_mult(life, derisk, halt),
                "haltL3": halt,
                "deriskL3": derisk,
                "equity_halt_ea": equity_halt,
                "loss_streak": loss_streak,
                "streak_warn": streak_warn,
                "overnight_cluster": overnight_cluster,
                "n30": n30,
                "freq_stall_warn": freq_stall,
                "cost_drift_warn": cost_drift,
                "bus": bus,
                "reason": reason,
            }
        )

    lives = [p["life"] for p in path if p["life"] != "WARMUP"]
    buses = [p["bus"] for p in path]
    max_dd = max(p["dd_peak_pct"] for p in path) if path else 0
    overnight_share = float(nights.mean()) if len(nights) else 0
    return {
        "label": label,
        "n": len(df),
        "final_equity": round(equity, 2),
        "net_pnl": round(equity - DEPOSIT, 2),
        "max_dd_peak_pct": round(max_dd, 3),
        "max_loss_streak": max_loss_streak,
        "max_overnight_cluster": max_overnight_cluster,
        "overnight_share": round(overnight_share, 3),
        "trips": trips,
        "trip_count": len(trips),
        "life_counts": {k: lives.count(k) for k in sorted(set(lives))},
        "bus_counts": {k: buses.count(k) for k in sorted(set(buses))},
        "halt_latched": halt_latched,
        "last_life": path[-1]["life"] if path else None,
        "last_en15": path[-1]["en15"] if path else None,
        "last_en20": path[-1]["en20"] if path else None,
        "last_ef15_pp": path[-1]["ef15_pp"] if path else None,
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


def main() -> None:
    tip = load_tip()
    long = load_long()
    v1 = tip[tip["v1_skip"] == 0].reset_index(drop=True)
    alt = tip[tip["alt_buy_thu_skip"] == 0].reset_index(drop=True)
    long_v1 = long[long["v1_skip"] == 0].reset_index(drop=True)

    sims = {
        "P0_tip": simulate(tip, "P0_tip"),
        "v1_BUY_May_kept": simulate(v1, "v1_BUY_May_kept"),
        "alt_BUY_Thu_kept": simulate(alt, "alt_BUY_Thu_kept"),
        "P0_long_diagnostic": simulate(long, "P0_long_diagnostic"),
        "v1_long_kept_diagnostic": simulate(long_v1, "v1_long_kept_diagnostic"),
    }

    for k, sim in sims.items():
        path_csv(sim, f"health_path_{k}.csv")
        sims[k] = {**sim, "path_len": len(sim["path"])}
        del sims[k]["path"]

    policy = {
        "task": "AUDUSD-AOS-P3",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "l2det_preferred": "L2det_aud_m15_v1 = BUY AND month==May",
        "bindings": {
            "DD_Limit_pct": DD_LIMIT,
            "derisk_at_pct": 0.8 * DD_LIMIT,
            "EquityHalt_pct": EQUITY_HALT,
            "BWR": 50.0,
            "R": R,
            "Leak_proxy_pp": LEAK * 100,
            "deposit": DEPOSIT,
            "W_health": [W15, W20],
            "W250_preset": 250,
            "W250_research_floor": 50,
            "W250_note": (
                "Preset InpAOS_W250=250 will not arm lifecycle on tip n~41. "
                "Expansion OS uses W15/W20; set InpAOS_W250=50 when wiring research .set. "
                "Live Track B (8230931) already uses W250 — do not collide."
            ),
            "baseline_tip_E_N": BASELINE_TIP_EN,
            "baseline_fires_90d": BASELINE_FIRES_90D,
            "spread_baseline_med": SPREAD_BASELINE_MED,
            "overnight_note": (
                "AUDUSD M15 tip overnight_share ~0.59 — L3 MaxDD path includes "
                "multi-session inventory; measured swap still OPEN. "
                "Roadmap L8 overnight MAE advisor is P4."
            ),
        },
        "sims": sims,
        "recommend_bus": {
            "BELOW": "L3_HALT f=0",
            "COMPRESSING": "INVESTIGATE (regime/execution) · f=0.5",
            "NEAR / DERISK_0.8_DD": "DERISK f<=0.5",
            "STREAK>=5": "STREAK_WATCH · align engine pause",
            "FREQUENCY_STALL": "WARN only — do not lift ATR max / drop CD / re-enable MonTue",
            "COST_DRIFT": "INVESTIGATE (spread ≫ tip median 15)",
            "EXPANDING/STABLE": "NONE f=1.0",
            "L2det WOULD_SKIP": "skip fire (not an L3 trip)",
            "OVERNIGHT_CLUSTER": "note for L8 / measured swap (P4) — not auto-halt",
        },
        "unlatch": {
            "HALT_f0_BELOW_FRONTIER": (
                "Clear latch only when W20 E_N > 0 for 2 consecutive evals "
                "and dd_peak < 20%."
            )
        },
    }
    (OUT / "P3_L3L4.json").write_text(json.dumps(policy, indent=2), encoding="utf-8")

    compact = {
        k: {
            "n": v["n"],
            "final": v["final_equity"],
            "max_dd": v["max_dd_peak_pct"],
            "trips": v["trip_count"],
            "trip_reasons": [t["reason"] for t in v["trips"]],
            "life_counts": v["life_counts"],
            "bus_counts": v["bus_counts"],
            "max_loss_streak": v["max_loss_streak"],
            "max_overnight_cluster": v["max_overnight_cluster"],
            "overnight_share": v["overnight_share"],
            "last_life": v["last_life"],
            "last_en15": v["last_en15"],
            "last_en20": v["last_en20"],
            "last_ef15_pp": v["last_ef15_pp"],
        }
        for k, v in sims.items()
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
