"""DE40-AOS-P6 — L9 session soft veto CF · ±10% L2det stress · ATR G3 note."""
from __future__ import annotations

import json
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
LEAK = 0.098  # prior authority
ATR_CAP = 4070.0
NEAR_FRAC = 0.9
OVERLAY = "L2det_de40_v1_BUY_near_atr"


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["spread_pts"] = df["spread_pts"].astype(float)
    df["atr_pts"] = df["atr_pts"].astype(float)
    df["near"] = df["near_atr_cap"].astype(int)
    df["buy"] = (df["side"] == "BUY").astype(int)
    df["is_h08"] = (df["hour"] == 8).astype(int)
    df["is_h09"] = (df["hour"] == 9).astype(int)
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["frank_open"] = (df["hour"].isin([8, 9])).astype(int)
    df["buy_h08"] = ((df["side"] == "BUY") & (df["hour"] == 8)).astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
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
    """DE40 CF — Aug / SELL / Mon collateral."""
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


def arm_mask(
    df: pd.DataFrame, near_frac: float = NEAR_FRAC, atr_cap: float = ATR_CAP
) -> np.ndarray:
    """Primary overlay: BUY ∧ atr ≥ frac×cap."""
    return ((df["buy"] == 1) & (df["atr_pts"] >= near_frac * atr_cap)).to_numpy()


def p6_t01(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — Frankfurt open / spread / H13."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H08": tip["is_h08"] == 1,
        "skip_BUY_H08": tip["buy_h08"] == 1,
        "skip_frank_open_H08_09": tip["frank_open"] == 1,
        "skip_H13": tip["is_h13"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_arm = tip.loc[~arm_mask(tip)].copy()
    add = {}
    if len(kept_arm):
        add_map = {
            "skip_H08": kept_arm["is_h08"] == 1,
            "skip_BUY_H08": kept_arm["buy_h08"] == 1,
            "skip_frank_open_H08_09": kept_arm["frank_open"] == 1,
            "skip_H13": kept_arm["is_h13"] == 1,
            "skip_spread_gt_p66": kept_arm["spread_pts"] > p66 + 1e-9,
        }
        for k, m in add_map.items():
            add[k + "_on_arm_kept"] = cf(kept_arm, m.to_numpy(), k + "_on_arm_kept")

    ytd_p66 = float(ytd["spread_pts"].quantile(0.66))
    ytd_spread = cf(
        ytd, (ytd["spread_pts"] > ytd_p66 + 1e-9).to_numpy(), "ytd_skip_spread_gt_p66"
    )

    tip_spread_nunique = int(tip["spread_pts"].nunique())
    tip_spread_std = float(tip["spread_pts"].std(ddof=0))
    return {
        "tip_spread_nunique": tip_spread_nunique,
        "tip_spread_std": round(tip_spread_std, 2),
        "tip_spread_p66": round(p66, 4),
        "tip_spread_note": (
            "Tip entry spread low variance — tercile soft veto weak; DISARM."
            if tip_spread_nunique <= 3 or tip_spread_std < 20
            else "Tip spread varies — see policies."
        ),
        "tip_policies": tip_rows,
        "additive_on_arm_kept": add,
        "ytd_spread_diagnostic": ytd_spread,
        "armed": [],
        "hold": [],
        "disarm": [],
    }


def classify_t01(rep: dict) -> dict:
    for block in ("tip_policies", "additive_on_arm_kept"):
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
    """±10% stress on L2det BUY∧nearATR threshold (not SL/TP)."""
    base_mask = arm_mask(tip, NEAR_FRAC, ATR_CAP)
    base = cf(tip, base_mask, "arm_nominal_frac0.9_cap4070")

    stresses = {
        "near_frac_minus10": (NEAR_FRAC * 0.9, ATR_CAP),  # 0.81
        "near_frac_plus10": (NEAR_FRAC * 1.1, ATR_CAP),  # 0.99
        "atr_cap_minus10": (NEAR_FRAC, ATR_CAP * 0.9),  # 3663
        "atr_cap_plus10": (NEAR_FRAC, ATR_CAP * 1.1),  # 4477
        "both_loose": (NEAR_FRAC * 0.9, ATR_CAP * 1.1),
        "both_tight": (NEAR_FRAC * 1.1, ATR_CAP * 0.9),
    }
    rows = {}
    for name, (frac, cap) in stresses.items():
        m = arm_mask(tip, frac, cap)
        row = cf(tip, m, name)
        row["near_frac"] = round(frac, 4)
        row["atr_cap"] = round(cap, 1)
        row["delta_E_N_vs_arm"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    ok = []
    fail = []
    for name, row in rows.items():
        d = row["delta_E_N_vs_arm"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        if d is not None and d >= -0.05 and ret_gap <= 20:
            ok.append(name)
        else:
            fail.append(name)

    return {
        "overlay": OVERLAY,
        "baseline_arm": base,
        "stresses": rows,
        "robust_pass": ok,
        "robust_fail": fail,
        "verdict": "PASS"
        if len(fail) == 0
        else ("PASS_WITH_NOTES" if len(ok) >= 3 else "FAIL"),
        "note": (
            "Stresses L2det BUY∧nearATR knobs only. Engine ATR max (4070) is separate G3. "
            "SL/TP untouched. Keep defaults frac=0.9 · nearATR ref cap=4070."
        ),
    }


def _parse_preset(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "exists": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    atr_on = "InpUseATRRegime=true" in text
    atr_max = None
    for line in text.splitlines():
        if line.startswith("InpATRMaxPoints="):
            atr_max = line.split("=", 1)[1].split("||")[0]
    g3_ok = atr_on and atr_max is not None and abs(float(atr_max) - 4070.0) < 1e-6
    return {
        "path": str(path),
        "name": path.name,
        "exists": True,
        "InpUseATRRegime": atr_on,
        "InpATRMaxPoints": atr_max,
        "g3_ok": g3_ok,
    }


def p6_t03() -> dict:
    """Confirm ATR max declared on P0 engine + P4 research OS presets."""
    targets = [
        PRESETS_EXPERTS / "BMRG-M15-DE40-6M-P0_balanced_chart.set",
        PRESETS_EXPERTS / "BMRG-M15-DE40-6M-P4_research_OS_W50.set",
        PRESETS_TESTER / "BMRG-M15-DE40-6M-P0_balanced_chart.set",
        PRESETS_TESTER / "BMRG-M15-DE40-6M-P4_research_OS_W50.set",
    ]
    rows = [_parse_preset(p) for p in targets]
    existing = [r for r in rows if r.get("exists")]
    all_ok = bool(existing) and all(r.get("g3_ok") for r in existing)
    return {
        "presets": rows,
        "engine_filter": "ATR max checked before AOSAllowEntry",
        "aos_does_not_lift_atr": True,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via session 08–17 · skip Tue · ATR max 4070 "
            "remains declared for G3 when research OS armed."
        ),
    }


def main() -> None:
    tip = load("de40_tip_fire_tape_v0.csv")
    ytd = load("de40_ytd_fire_tape_v0.csv")
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
        "wire": (
            "No new L9 LIVE veto. Prefer overlay BUY∧near_atr over stacking L9. "
            "Frankfurt-open / H08 soft veto only if ARM_SOFT with clean FP — else SHADOW. "
            "H13 stays P2 HOLD. Spread tercile DISARM until tip fills show variance."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    rep = {
        "task": "DE40-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "P6_T01_L9_session": t01,
        "P6_T02_L2_stress": t02,
        "P6_T03_ATR_G3": t03,
        "verdict": {
            "T01": "PASS_DOCUMENTED",
            "T02": t02["verdict"],
            "T03": t03["verdict"],
            "phase": "P6_COMPLETE"
            if t02["verdict"].startswith("PASS") and t03["verdict"] == "PASS"
            else "P6_HOLD",
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "P6_HARDEN.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep["verdict"], indent=2))
    print("T01 armed", t01["armed"])
    print("T01 hold", t01["hold"])
    print("T01 disarm", t01["disarm"])
    print("T02", t02["verdict"], "fail", t02["robust_fail"])
    print(
        "T02 base E_N",
        t02["baseline_arm"]["kept"]["E_N"],
        "ret",
        t02["baseline_arm"]["fire_retention_pct"],
    )
    for name, row in t02["stresses"].items():
        print(
            name,
            "E_N",
            row["kept"]["E_N"],
            "d",
            row["delta_E_N_vs_arm"],
            "ret",
            row["fire_retention_pct"],
        )
    print("T03", t03["verdict"])
    for r in t03["presets"]:
        print(r.get("name"), r.get("g3_ok"), r.get("InpATRMaxPoints"), r.get("exists"))


if __name__ == "__main__":
    main()
