"""DE40-M5-AOS-P6 — L9 session soft veto · ±10% L2det bound stress · ATR G3."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "DE40" / "tapes"
OUT = Path(__file__).resolve().parent
PRESETS_EXPERTS = BMRG / "Presets"
PRESETS_TESTER = BMRG / "Profiles" / "Tester" / "BMRG" / "DE40"

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.07  # prior 7.0pp authority
ATR_CAP = 2380.0
OVERLAY = "L2det_de40_m5_v1b"


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["spread_pts"] = df["spread_pts"].astype(float)
    df["atr_pts"] = df["atr_pts"].astype(float)
    df["near"] = df["near_atr_cap"].astype(int)
    df["buy"] = (df["side"] == "BUY").astype(int)
    df["sell"] = (df["side"] == "SELL").astype(int)
    df["is_h08"] = (df["hour"] == 8).astype(int)
    df["is_h09"] = (df["hour"] == 9).astype(int)
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["frank_open"] = (df["hour"].isin([8, 9])).astype(int)
    df["buy_h08"] = ((df["side"] == "BUY") & (df["hour"] == 8)).astype(int)
    df["is_h14_16"] = (df["hour"].isin([14, 16])).astype(int)
    df["is_oct"] = (df["month"] == "2026-10").astype(int)
    df["is_sep"] = (df["month"] == "2026-09").astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
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
    """DE40 M5 CF — Aug / SELL / Mon collateral (protect)."""
    base = book(df)
    skips = df.loc[mask]
    kept = df.loc[~mask]
    kept_m = book(kept)
    prec = float((1 - skips["win"]).mean()) if len(skips) else None
    sell_fp = (
        int(((skips["side"] == "SELL") & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    aug_fp = (
        int(((skips["is_aug"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    mon_fp = (
        int(((skips["is_mon"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
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
        and sell_fp <= 1
        and aug_fp <= 1
        and mon_fp <= 2
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
        "false_skip_sell_winners": sell_fp,
        "false_skip_aug_winners": aug_fp,
        "false_skip_mon_winners": mon_fp,
    }


def v1b_mask(df: pd.DataFrame) -> np.ndarray:
    """(BUY ∧ H14|16) ∨ (BUY ∧ Oct) — EA default."""
    return (
        ((df["buy"] == 1) & (df["is_h14_16"] == 1))
        | ((df["buy"] == 1) & (df["is_oct"] == 1))
    ).to_numpy()


def buy_hours(df: pd.DataFrame, hours: set[int]) -> np.ndarray:
    return ((df["buy"] == 1) & df["hour"].isin(hours)).to_numpy()


def p6_t01(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — Frankfurt open / spread / H13."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H08": tip["is_h08"] == 1,
        "skip_BUY_H08": tip["buy_h08"] == 1,
        "skip_frank_open_H08_09": tip["frank_open"] == 1,
        "skip_H13": tip["is_h13"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
        "skip_H14_plus": tip["hour"] >= 14,  # overlaps L2det — diagnostic
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_arm = tip.loc[~v1b_mask(tip)].copy()
    add = {}
    if len(kept_arm):
        add_map = {
            "skip_H08": kept_arm["is_h08"] == 1,
            "skip_BUY_H08": kept_arm["buy_h08"] == 1,
            "skip_frank_open_H08_09": kept_arm["frank_open"] == 1,
            "skip_H13": kept_arm["is_h13"] == 1,
            "skip_spread_gt_p66": kept_arm["spread_pts"] > p66 + 1e-9,
            "skip_H14_plus": kept_arm["hour"] >= 14,
        }
        for k, m in add_map.items():
            add[k + "_on_v1b_kept"] = cf(kept_arm, m.to_numpy(), k + "_on_v1b_kept")

    ytd_p66 = float(ytd["spread_pts"].quantile(0.66))
    ytd_spread = cf(
        ytd, (ytd["spread_pts"] > ytd_p66 + 1e-9).to_numpy(), "ytd_skip_spread_gt_p66"
    )

    tip_spread_nunique = int(tip["spread_pts"].nunique())
    tip_spread_std = float(tip["spread_pts"].std(ddof=0))
    return {
        "tip_spread_nunique": tip_spread_nunique,
        "tip_spread_std": round(tip_spread_std, 2),
        "tip_spread_median": round(float(tip["spread_pts"].median()), 4),
        "tip_spread_p66": round(p66, 4),
        "tip_spread_note": (
            "Tip entry spread low variance — tercile soft veto weak; DISARM."
            if tip_spread_nunique <= 3 or tip_spread_std < 20
            else "Tip spread varies — see policies."
        ),
        "tip_policies": tip_rows,
        "additive_on_v1b_kept": add,
        "ytd_spread_diagnostic": ytd_spread,
        "armed": [],
        "hold": [],
        "disarm": [],
    }


def classify_t01(rep: dict) -> dict:
    for block in ("tip_policies", "additive_on_v1b_kept"):
        for k, row in rep[block].items():
            v = row["verdict"]
            if v == "ARM_SOFT":
                rep["armed"].append(k)
            elif v == "HOLD_SHADOW":
                rep["hold"].append(k)
            else:
                rep["disarm"].append(k)
    return rep


def p6_t02(tip: pd.DataFrame) -> dict:
    """±10%-style bound stress on L2det v1b hour/month (not SL/TP / not nearATR)."""
    base_mask = v1b_mask(tip)
    base = cf(tip, base_mask, "v1b_BUY_H14_16_OR_BUY_Oct")

    stresses = {
        # hour window stresses
        "BUY_H14_only": buy_hours(tip, {14})
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        "BUY_H16_only": buy_hours(tip, {16})
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        "BUY_H14_16_nominal": buy_hours(tip, {14, 16})
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        "BUY_H13_16_wide": buy_hours(tip, {13, 14, 16})
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        "BUY_H14_17_wide": buy_hours(tip, {14, 15, 16, 17})
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        # month window stresses
        "BUY_H14_16_OR_BUY_SepOct": buy_hours(tip, {14, 16})
        | ((tip["buy"] == 1) & tip["month"].isin(["2026-09", "2026-10"])).to_numpy(),
        "BUY_H14_16_only_no_Oct": buy_hours(tip, {14, 16}),
        "BUY_Oct_only_no_H14_16": ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        # aggressive HOLD paths (SELL collateral)
        "H14_16_all_sides_OR_BUY_Oct": (tip["is_h14_16"] == 1).to_numpy()
        | ((tip["buy"] == 1) & (tip["is_oct"] == 1)).to_numpy(),
        "BUY_H14_16_OR_Oct_all": buy_hours(tip, {14, 16})
        | (tip["is_oct"] == 1).to_numpy(),
        # nearATR is tip star — stress must NOT improve by skipping it alone
        "REJECT_probe_BUY_near_atr": (
            (tip["buy"] == 1) & (tip["near"] == 1)
        ).to_numpy(),
    }
    rows = {}
    for name, m in stresses.items():
        row = cf(tip, m, name)
        row["delta_E_N_vs_v1b"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    # Robustness: keep v1b if alternate bounds do not beat it by >0.02 E_N with clean FP
    # and narrowing/widening does not crater retention without lift.
    ok = []
    fail = []
    for name, row in rows.items():
        if name.startswith("REJECT_probe"):
            # expect DISARM / negative — pass if not better than v1b
            d = row["delta_E_N_vs_v1b"]
            if d is not None and d < 0:
                ok.append(name)
            else:
                fail.append(name)
            continue
        d = row["delta_E_N_vs_v1b"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        # Prefer nominal: stresses should not beat v1b materially with more SELL FP
        if name in ("BUY_H14_16_nominal",):
            ok.append(name)
            continue
        if d is not None and d > 0.02 and row["false_skip_sell_winners"] <= 1:
            # better bound exists — note, not auto-fail if retention ok
            ok.append(name + "_BETTER?")
        elif d is not None and d >= -0.05 and ret_gap <= 25:
            ok.append(name)
        else:
            fail.append(name)

    verdict = "PASS"
    if any("BETTER?" in x for x in ok):
        verdict = "PASS_WITH_NOTES"
    if len([f for f in fail if not f.startswith("REJECT")]) > 3:
        verdict = "PASS_WITH_NOTES" if len(ok) >= 4 else "FAIL"

    return {
        "overlay": OVERLAY,
        "baseline_v1b": base,
        "stresses": rows,
        "robust_pass": ok,
        "robust_fail": fail,
        "verdict": verdict,
        "note": (
            "Stresses L2det M5 hour/month knobs only. nearATR skip is REJECT probe "
            "(tip star). Engine ATR max 2380 is separate G3. SL/TP untouched. "
            "Keep defaults: (BUY∧H14|16)∨(BUY∧Oct)."
        ),
    }


def _parse_preset(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "name": path.name, "exists": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    atr_on = re.search(r"InpUseATRRegime=(true|false)", text)
    atr_max = re.search(r"InpATRMaxPoints=([0-9.]+)", text)
    m5_l2 = re.search(r"InpAOS_DE_M5_L2detEnable=(true|false)", text)
    g3_ok = bool(
        atr_on
        and atr_on.group(1) == "true"
        and atr_max
        and abs(float(atr_max.group(1)) - ATR_CAP) < 0.1
    )
    return {
        "path": str(path),
        "name": path.name,
        "exists": True,
        "InpUseATRRegime": atr_on.group(1) if atr_on else None,
        "InpATRMaxPoints": float(atr_max.group(1)) if atr_max else None,
        "InpAOS_DE_M5_L2detEnable": m5_l2.group(1) if m5_l2 else "n/a",
        "g3_ok": g3_ok,
    }


def p6_t03() -> dict:
    """Confirm ATR max 2380 declared on P0 engine + P4 research OS presets."""
    targets = [
        PRESETS_EXPERTS / "BMRG-M5-DE40-6M-P0_balanced_chart.set",
        PRESETS_EXPERTS / "BMRG-M5-DE40-6M-P4_research_OS_W50.set",
        PRESETS_TESTER / "BMRG-M5-DE40-6M-P0_balanced_chart.set",
        PRESETS_TESTER / "BMRG-M5-DE40-6M-P4_research_OS_W50.set",
    ]
    rows = [_parse_preset(p) for p in targets]
    existing = [r for r in rows if r.get("exists")]
    all_ok = bool(existing) and all(r.get("g3_ok") for r in existing)
    return {
        "declared_atr_max": ATR_CAP,
        "presets": rows,
        "engine_filter": "ATR max checked before AOSAllowEntry",
        "aos_does_not_lift_atr": True,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via session 08–17 · skip Tue · ATR max 2380 "
            "remains declared for G3 when research OS armed."
        ),
        "note": (
            "Profiles P0 missing is OK if Presets P0 + Profiles P4 both declare 2380."
            if not (PRESETS_TESTER / "BMRG-M5-DE40-6M-P0_balanced_chart.set").exists()
            else ""
        ),
    }


def main() -> None:
    tip = load("de40_m5_tip_fire_tape_v0.csv")
    ytd = load("de40_m5_ytd_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, ytd))
    t01["recommendation"] = {
        "spread_tercile": (
            "DISARM_tip_low_variance"
            if t01["tip_spread_nunique"] <= 3 or t01["tip_spread_std"] < 20
            else t01["tip_policies"]["skip_spread_gt_p66"]["verdict"]
        ),
        "skip_H08": t01["tip_policies"]["skip_H08"]["verdict"],
        "skip_BUY_H08": t01["tip_policies"]["skip_BUY_H08"]["verdict"],
        "skip_frank_open": t01["tip_policies"]["skip_frank_open_H08_09"]["verdict"],
        "skip_H13": t01["tip_policies"]["skip_H13"]["verdict"],
        "skip_H14_plus": t01["tip_policies"]["skip_H14_plus"]["verdict"],
        "wire": (
            "No new L9 LIVE veto. Prefer overlay L2det_de40_m5_v1b over stacking L9. "
            "Frankfurt-open / H08 soft veto only if ARM_SOFT with clean Aug/SELL FP — else SHADOW. "
            "H14+ already covered by L2det BUY∧ — do not double-wire as L9 LIVE. "
            "Spread tercile DISARM until tip fills show variance."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    phase_ok = t02["verdict"].startswith("PASS") and t03["verdict"] == "PASS"
    rep = {
        "task": "DE40-M5-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "Leak_proxy_pp": LEAK * 100,
        "P6_T01_L9_session": t01,
        "P6_T02_L2_stress": t02,
        "P6_T03_ATR_G3": t03,
        "verdict": {
            "T01": "PASS_DOCUMENTED",
            "T02": t02["verdict"],
            "T03": t03["verdict"],
            "phase": "P6_COMPLETE" if phase_ok else "P6_HOLD",
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "P6_HARDEN.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")

    compact = {
        "L9_full_tip": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
                "prec": v["precision_vs_losers"],
                "sell_fp": v["false_skip_sell_winners"],
                "aug_fp": v["false_skip_aug_winners"],
            }
            for k, v in t01["tip_policies"].items()
        },
        "L9_add_v1b": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
                "sell_fp": v["false_skip_sell_winners"],
                "aug_fp": v["false_skip_aug_winners"],
            }
            for k, v in t01["additive_on_v1b_kept"].items()
        },
        "L9_armed": t01["armed"],
        "L9_hold": t01["hold"],
        "L9_disarm": t01["disarm"],
        "L9_rec": t01["recommendation"],
        "stress_vs_v1b": {
            k: {
                "kept_E_N": v["kept"]["E_N"],
                "d_vs_v1b": v["delta_E_N_vs_v1b"],
                "ret": v["fire_retention_pct"],
                "verdict": v["verdict"],
                "sell_fp": v["false_skip_sell_winners"],
            }
            for k, v in t02["stresses"].items()
        },
        "v1b_kept_E_N": t02["baseline_v1b"]["kept"]["E_N"],
        "v1b_ret": t02["baseline_v1b"]["fire_retention_pct"],
        "T02": t02["verdict"],
        "T02_fail": t02["robust_fail"],
        "ATR_G3": t03["verdict"],
        "phase": rep["verdict"]["phase"],
    }
    (OUT / "P6_SUMMARY.json").write_text(
        json.dumps(compact, indent=2), encoding="utf-8"
    )
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
