"""UK100-M5-AOS-P6 — L9 session soft veto · ±10% L2 bound stress · ATR G3."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
OUT = Path(__file__).resolve().parent
PRESETS = [
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\UK100"
        r"\BMRG-M5-UK100-6M-P0_balanced_chart.set"
    ),
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\UK100"
        r"\BMRG-M5-UK100-6M-P4_research_OS_W50.set"
    ),
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\Presets"
        r"\BMRG-M5-UK100-6M-P0_balanced_chart.set"
    ),
    Path(
        r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
        r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\Presets"
        r"\BMRG-M5-UK100-6M-P4_research_OS_W50.set"
    ),
]

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.059259
ATR_CAP = 869.0
NEAR_FRAC = 0.9


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["spread_pts"] = df["spread_pts"].astype(float)
    df["atr_pts"] = df["atr_pts"].astype(float)
    df["mon"] = df["cell_dow_mon"].astype(int)
    df["h12_13"] = df["cell_hour_12_13"].astype(int)
    df["sell"] = df["cell_sell"].astype(int)
    df["buy"] = df["cell_buy"].astype(int)
    df["near"] = df["near_atr_cap"].astype(int)
    return df.sort_values("open_dt").reset_index(drop=True)


def book(df: pd.DataFrame) -> dict:
    n = len(df)
    if n == 0:
        return {"n": 0, "WR": None, "E_N": None, "EF_proxy_pp": None}
    wr = float(df["win"].mean())
    return {
        "n": n,
        "WR": round(wr * 100, 2),
        "E_N": round(wr * (R + 1) - 1, 4),
        "EF_proxy_pp": round((wr - BWR - LEAK) * 100, 3),
    }


def cf(df: pd.DataFrame, mask: np.ndarray, label: str) -> dict:
    base = book(df)
    skips = df.loc[mask]
    kept = df.loc[~mask]
    kept_m = book(kept)
    prec = float((1 - skips["win"].mean())) if len(skips) else None
    if prec is not None:
        prec = float((1 - skips["win"]).mean())
    wed_fp = (
        int(((skips["open_dt"].dt.dayofweek == 2) & (skips["win"] == 1)).sum())
        if len(skips)
        else 0
    )
    h08_fp = (
        int(((skips["hour"].isin([8, 9, 10, 11])) & (skips["win"] == 1)).sum())
        if len(skips)
        else 0
    )
    buy_fp = (
        int(((skips["buy"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    ret = 100.0 * len(kept) / len(df) if len(df) else 0.0
    d_en = (
        None
        if kept_m["E_N"] is None or base["E_N"] is None
        else round(kept_m["E_N"] - base["E_N"], 4)
    )
    d_ef = (
        None
        if kept_m["EF_proxy_pp"] is None or base["EF_proxy_pp"] is None
        else round(kept_m["EF_proxy_pp"] - base["EF_proxy_pp"], 3)
    )
    verdict = "DISARM"
    if mask.sum() == 0:
        verdict = "NO_SKIPS"
    elif ret < 50:
        verdict = "REJECT_FREQUENCY_STALL"
    elif (
        d_en is not None
        and d_en > 0
        and (prec or 0) >= 0.55
        and wed_fp <= 2
        and h08_fp <= 2
    ):
        verdict = "ARM_SOFT"
    elif d_en is not None and d_en > 0:
        verdict = "HOLD_SHADOW"
    return {
        "label": label,
        "verdict": verdict,
        "skips_n": int(mask.sum()),
        "precision_vs_losers": None if prec is None else round(prec, 4),
        "fire_retention_pct": round(ret, 1),
        "kept": kept_m,
        "baseline": base,
        "delta_E_N": d_en,
        "delta_EF_pp": d_ef,
        "false_skip_wed_winners": wed_fp,
        "false_skip_h08_11_winners": h08_fp,
        "false_skip_buy_winners": buy_fp,
    }


def v1b_mask(df: pd.DataFrame) -> np.ndarray:
    return (
        ((df["mon"] == 1) & (df["h12_13"] == 1))
        | ((df["sell"] == 1) & (df["h12_13"] == 1))
    ).to_numpy()


def v1b_hours(df: pd.DataFrame, hours: set[int]) -> np.ndarray:
    in_h = df["hour"].isin(hours)
    return (
        ((df["mon"] == 1) & in_h) | ((df["sell"] == 1) & in_h)
    ).to_numpy()


def p6_t01(tip: pd.DataFrame) -> dict:
    """L9 — midday / late / spread; protect mornings."""
    spr_p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H14_plus": tip["hour"] >= 14,
        "skip_H12_13_BUY": (tip["buy"] == 1) & (tip["h12_13"] == 1),
        "skip_H12_13_all": tip["h12_13"] == 1,  # aggressive vs v1b
        "skip_morning_H08_11": tip["hour"].isin([8, 9, 10, 11]),  # protect — expect bad
        "skip_spread_gt_p66": tip["spread_pts"] > spr_p66 + 1e-9,
        "skip_Mon_all": tip["mon"] == 1,
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept = tip.loc[~v1b_mask(tip)].copy()
    add = {}
    if len(kept):
        add_pols = {
            "add_H14_plus": kept["hour"] >= 14,
            "add_H12_13_BUY": (kept["buy"] == 1) & (kept["h12_13"] == 1),
            "add_spread_gt_p66": kept["spread_pts"] > spr_p66 + 1e-9,
            "add_SELL_near_atr": (kept["sell"] == 1) & (kept["near"] == 1),
        }
        add = {k: cf(kept, m.to_numpy(), k) for k, m in add_pols.items()}

    return {
        "spread_tip_median": float(tip["spread_pts"].median()),
        "spread_tip_p66": spr_p66,
        "on_full_tip": tip_rows,
        "additive_on_v1b_kept": add,
    }


def p6_t02(tip: pd.DataFrame) -> dict:
    """±10% / bound stress on L2 hour window and optional nearATR."""
    base_mask = v1b_mask(tip)
    base = cf(tip, base_mask, "v1b_H12_13")

    stresses = {
        "hours_H12_only": v1b_hours(tip, {12}),
        "hours_H13_only": v1b_hours(tip, {13}),
        "hours_H11_14_wide": v1b_hours(tip, {11, 12, 13, 14}),  # looser / wider
        "hours_H12_13_nominal": v1b_hours(tip, {12, 13}),
        # nearATR additive stress on top of v1b (optional HOLD path)
        "v1b_OR_SELL_near_frac_0.81": base_mask
        | (
            (tip["sell"] == 1) & (tip["atr_pts"] >= 0.81 * ATR_CAP)
        ).to_numpy(),
        "v1b_OR_SELL_near_frac_0.99": base_mask
        | (
            (tip["sell"] == 1) & (tip["atr_pts"] >= 0.99 * ATR_CAP)
        ).to_numpy(),
        "v1b_OR_SELL_near_cap_782": base_mask
        | (
            (tip["sell"] == 1) & (tip["atr_pts"] >= NEAR_FRAC * (ATR_CAP * 0.9))
        ).to_numpy(),
        "v1b_OR_SELL_near_cap_956": base_mask
        | (
            (tip["sell"] == 1) & (tip["atr_pts"] >= NEAR_FRAC * (ATR_CAP * 1.1))
        ).to_numpy(),
    }
    rows = {}
    for k, m in stresses.items():
        rows[k] = cf(tip, m, k)
        rows[k]["delta_E_N_vs_v1b"] = (
            None
            if rows[k]["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(rows[k]["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
    return {"v1b_baseline": base, "stresses": rows}


def p6_t03() -> dict:
    """ATR max 869 declared on P0 + P4 presets."""
    out = []
    for p in PRESETS:
        if not p.exists():
            out.append({"path": str(p), "exists": False})
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        atr_on = re.search(r"InpUseATRRegime=(true|false)", text)
        atr_max = re.search(r"InpATRMaxPoints=([0-9.]+)", text)
        m5_l2 = re.search(r"InpAOS_UK_M5_L2detEnable=(true|false)", text)
        out.append(
            {
                "path": str(p),
                "exists": True,
                "InpUseATRRegime": atr_on.group(1) if atr_on else None,
                "InpATRMaxPoints": float(atr_max.group(1)) if atr_max else None,
                "InpAOS_UK_M5_L2detEnable": m5_l2.group(1) if m5_l2 else "n/a",
                "G3_ok": bool(
                    atr_on
                    and atr_on.group(1) == "true"
                    and atr_max
                    and abs(float(atr_max.group(1)) - 869.0) < 0.1
                ),
            }
        )
    return {
        "declared_atr_max": 869.0,
        "presets": out,
        "verdict": "PASS"
        if all(r.get("G3_ok") for r in out if r.get("exists"))
        else "FAIL",
    }


def main() -> None:
    tip = load("uk100_m5_tip_fire_tape_v0.csv")
    report = {
        "task": "UK100-M5-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "Leak_proxy_pp": LEAK * 100,
        "P6_T01_L9": p6_t01(tip),
        "P6_T02_stress": p6_t02(tip),
        "P6_T03_ATR_G3": p6_t03(),
    }
    (OUT / "P6_HARDEN.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    # compact summary
    t01 = report["P6_T01_L9"]
    compact = {
        "L9_full_tip": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
                "prec": v["precision_vs_losers"],
                "fpH": v["false_skip_h08_11_winners"],
            }
            for k, v in t01["on_full_tip"].items()
        },
        "L9_add_v1b": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
            }
            for k, v in t01["additive_on_v1b_kept"].items()
        },
        "stress_vs_v1b": {
            k: {
                "kept_E_N": v["kept"]["E_N"],
                "d_vs_v1b": v["delta_E_N_vs_v1b"],
                "ret": v["fire_retention_pct"],
                "verdict": v["verdict"],
            }
            for k, v in report["P6_T02_stress"]["stresses"].items()
        },
        "v1b_kept_E_N": report["P6_T02_stress"]["v1b_baseline"]["kept"]["E_N"],
        "ATR_G3": report["P6_T03_ATR_G3"]["verdict"],
    }
    (OUT / "P6_SUMMARY.json").write_text(
        json.dumps(compact, indent=2), encoding="utf-8"
    )
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
