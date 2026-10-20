"""USDJPY-AOS-P6 — L9 session soft veto CF · ±10% L2det stress · ATR G3 note."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "USDJPY" / "tapes"
OUT = Path(__file__).resolve().parent
PRESETS_EXPERTS = BMRG / "Presets"
PRESETS_TESTER = (
    BMRG.parents[1] / "Profiles" / "Tester" / "BMRG" / "USDJPY"
)

R = 1.20
BWR = 1.0 / (1.0 + R)
LEAK = 0.114  # prior authority
ATR_CAP = 70.0
NEAR_FRAC = 0.9
OVERLAY = "L2det_usdjpy_v1c_near_atr_OR_H16"


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["spread_pts"] = df["spread_pts"].astype(float)
    df["atr_pts"] = df["atr_pts"].astype(float)
    df["near"] = df["near_atr_cap"].astype(int)
    df["is_h14"] = (df["hour"] == 14).astype(int)
    df["is_h16"] = (df["hour"] == 16).astype(int)
    df["is_h12"] = (df["hour"] == 12).astype(int)
    df["is_h15"] = (df["hour"] == 15).astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    df["is_may"] = (df["month"] == "2026-05").astype(int)
    df["is_jun"] = (df["month"] == "2026-06").astype(int)
    df["is_jul"] = (df["month"] == "2026-07").astype(int)
    return df.sort_values("open_dt").reset_index(drop=True)


def book(df: pd.DataFrame) -> dict:
    n = len(df)
    if n == 0:
        return {"n": 0, "WR": None, "E_N": None, "EF_prior_pp": None}
    wr = float(df["win"].mean())
    return {
        "n": n,
        "WR": round(wr * 100, 2),
        "E_N": round(wr * (R + 1) - 1, 4),
        "EF_prior_pp": round((wr - BWR - LEAK) * 100, 3),
    }


def cf(df: pd.DataFrame, mask: np.ndarray, label: str) -> dict:
    """USDJPY CF — BUY / Fri / H12 / H15 / May / Jun protect."""
    base = book(df)
    skips = df.loc[mask]
    kept = df.loc[~mask]
    kept_m = book(kept)
    prec = float((1 - skips["win"]).mean()) if len(skips) else None

    def fp(cond) -> int:
        if len(skips) == 0:
            return 0
        return int((cond & (skips["win"] == 1)).sum())

    buy_fp = fp(skips["side"] == "BUY")
    fri_fp = fp(skips["is_fri"] == 1)
    h12_fp = fp(skips["is_h12"] == 1)
    h15_fp = fp(skips["is_h15"] == 1)
    may_fp = fp(skips["is_may"] == 1)
    jun_fp = fp(skips["is_jun"] == 1)
    protect_fp = buy_fp + fri_fp + h12_fp + h15_fp + may_fp + jun_fp

    ret = 100.0 * len(kept) / len(df) if len(df) else 0.0
    d_en = (
        None
        if kept_m["E_N"] is None or base["E_N"] is None
        else round(kept_m["E_N"] - base["E_N"], 4)
    )
    d_ef = (
        None
        if kept_m["EF_prior_pp"] is None or base["EF_prior_pp"] is None
        else round(kept_m["EF_prior_pp"] - base["EF_prior_pp"], 3)
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
        and buy_fp <= 1
        and fri_fp <= 1
        and protect_fp <= 3
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
        "false_skip_buy_winners": buy_fp,
        "false_skip_fri_winners": fri_fp,
        "false_skip_h12_winners": h12_fp,
        "false_skip_h15_winners": h15_fp,
        "false_skip_may_winners": may_fp,
        "false_skip_jun_winners": jun_fp,
    }


def v1c_mask(
    df: pd.DataFrame, near_frac: float = NEAR_FRAC, atr_cap: float = ATR_CAP
) -> np.ndarray:
    """Preferred overlay: near_atr (atr ≥ frac×cap) OR hour==16."""
    near = df["atr_pts"] >= near_frac * atr_cap
    return (near | (df["is_h16"] == 1)).to_numpy()


def near_only_mask(
    df: pd.DataFrame, near_frac: float = NEAR_FRAC, atr_cap: float = ATR_CAP
) -> np.ndarray:
    return (df["atr_pts"] >= near_frac * atr_cap).to_numpy()


def p6_t01(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — H14 / spread tercile / mid-session."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H14": tip["is_h14"] == 1,
        "skip_H16": tip["is_h16"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
        "skip_spread_gt_MaxSpread_half": tip["spread_pts"] > 12.5,  # half of MaxSpread 25
        "skip_Jul": tip["is_jul"] == 1,
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_v1c = tip.loc[~v1c_mask(tip)].copy()
    add = {}
    if len(kept_v1c):
        add_map = {
            "skip_H14": kept_v1c["is_h14"] == 1,
            "skip_spread_gt_p66": kept_v1c["spread_pts"] > p66 + 1e-9,
            "skip_Jul": kept_v1c["is_jul"] == 1,
        }
        for k, m in add_map.items():
            add[k + "_on_v1c_kept"] = cf(
                kept_v1c, m.to_numpy(), k + "_on_v1c_kept"
            )

    ytd_p66 = float(ytd["spread_pts"].quantile(0.66))
    ytd_spread = cf(
        ytd,
        (ytd["spread_pts"] > ytd_p66 + 1e-9).to_numpy(),
        "ytd_skip_spread_gt_p66",
    )

    tip_spread_nunique = int(tip["spread_pts"].nunique())
    tip_spread_std = float(tip["spread_pts"].std(ddof=0))
    return {
        "tip_spread_nunique": tip_spread_nunique,
        "tip_spread_std": round(tip_spread_std, 2),
        "tip_spread_p66": round(p66, 4),
        "tip_spread_median": round(float(tip["spread_pts"].median()), 4),
        "tip_spread_note": (
            "Tip entry spread low variance (journal ~4pts) — tercile soft veto weak."
            if tip_spread_nunique <= 3 or tip_spread_std < 2
            else "Tip spread varies — see policies."
        ),
        "tip_policies": tip_rows,
        "additive_on_v1c_kept": add,
        "ytd_spread_diagnostic": ytd_spread,
        "armed": [],
        "hold": [],
        "disarm": [],
    }


def classify_t01(rep: dict) -> dict:
    for block in ("tip_policies", "additive_on_v1c_kept"):
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
    """±10% stress on L2det nearATR knobs inside v1c (not SL/TP; H16 fixed)."""
    base_mask = v1c_mask(tip, NEAR_FRAC, ATR_CAP)
    base = cf(tip, base_mask, "v1c_nominal_frac0.9_cap70")

    stresses = {
        "near_frac_minus10": (NEAR_FRAC * 0.9, ATR_CAP),  # 0.81
        "near_frac_plus10": (NEAR_FRAC * 1.1, ATR_CAP),  # 0.99
        "atr_cap_minus10": (NEAR_FRAC, ATR_CAP * 0.9),  # 63
        "atr_cap_plus10": (NEAR_FRAC, ATR_CAP * 1.1),  # 77
        "both_loose": (NEAR_FRAC * 0.9, ATR_CAP * 1.1),
        "both_tight": (NEAR_FRAC * 1.1, ATR_CAP * 0.9),
        "near_only_nominal": None,  # special
    }
    rows = {}
    for name, params in stresses.items():
        if name == "near_only_nominal":
            m = near_only_mask(tip, NEAR_FRAC, ATR_CAP)
            row = cf(tip, m, name)
            row["near_frac"] = NEAR_FRAC
            row["atr_cap"] = ATR_CAP
            row["note"] = "slim near_atr without H16 (P3 showed BELOW trip)"
        else:
            frac, cap = params  # type: ignore
            m = v1c_mask(tip, frac, cap)
            row = cf(tip, m, name)
            row["near_frac"] = round(frac, 4)
            row["atr_cap"] = round(cap, 1)
        row["delta_E_N_vs_v1c"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    ok = []
    fail = []
    for name, row in rows.items():
        if name == "near_only_nominal":
            continue  # diagnostic only
        d = row["delta_E_N_vs_v1c"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        if d is not None and d >= -0.05 and ret_gap <= 20:
            ok.append(name)
        else:
            fail.append(name)

    return {
        "overlay": OVERLAY,
        "baseline_v1c": base,
        "stresses": rows,
        "robust_pass": ok,
        "robust_fail": fail,
        "verdict": "PASS"
        if len(fail) == 0
        else ("PASS_WITH_NOTES" if len(ok) >= 3 else "FAIL"),
        "note": (
            "Stresses L2det nearATR knobs inside v1c only (H16 hour fixed). "
            "Engine ATR max (70) is separate G3. SL/TP untouched. "
            "Keep defaults frac=0.9 · nearATR ref cap=70 · OR H16."
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
    g3_ok = atr_on and atr_max is not None and abs(float(atr_max) - 70.0) < 1e-6
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
        PRESETS_EXPERTS / "BMRG-M15-USDJPY-6M-P0_balanced_chart.set",
        PRESETS_EXPERTS / "BMRG-M15-USDJPY-6M-P4_research_OS_W50.set",
        PRESETS_TESTER / "BMRG-M15-USDJPY-6M-P0_balanced_chart.set",
        PRESETS_TESTER / "BMRG-M15-USDJPY-6M-P4_research_OS_W50.set",
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
            "regime_filtered=true via session 12–20 · skip Tue · ATR max 70 "
            "remains declared for G3 when research OS armed. Do not reopen Tokyo."
        ),
    }


def main() -> None:
    tip = load("usdjpy_tip_fire_tape_v0.csv")
    ytd = load("usdjpy_ytd_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, ytd))
    t01["recommendation"] = {
        "spread_tercile": (
            "DISARM_tip_low_variance"
            if t01["tip_spread_nunique"] <= 3 or t01["tip_spread_std"] < 2
            else t01["tip_policies"]["skip_spread_gt_p66"]["verdict"]
        ),
        "skip_H14": t01["tip_policies"]["skip_H14"]["verdict"],
        "skip_H16": t01["tip_policies"]["skip_H16"]["verdict"],
        "skip_Jul": t01["tip_policies"]["skip_Jul"]["verdict"],
        "wire": (
            "No new L9 LIVE veto. Prefer overlay v1c (near_atr∨H16) over stacking L9. "
            "H14 soft veto only if ARM_SOFT with clean protect FP — else SHADOW/DISARM. "
            "H16 already inside v1c. Spread tercile DISARM until tip fills show variance. "
            "Jul stays P2 HOLD — not L9 LIVE."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    rep = {
        "task": "USDJPY-AOS-P6",
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
    print(
        "T01 spread nunique",
        t01["tip_spread_nunique"],
        "std",
        t01["tip_spread_std"],
        "p66",
        t01["tip_spread_p66"],
    )
    print("T02", t02["verdict"], "fail", t02["robust_fail"])
    print(
        "T02 base E_N",
        t02["baseline_v1c"]["kept"]["E_N"],
        "ret",
        t02["baseline_v1c"]["fire_retention_pct"],
    )
    for name, row in t02["stresses"].items():
        print(
            name,
            "E_N",
            row["kept"]["E_N"],
            "d",
            row["delta_E_N_vs_v1c"],
            "ret",
            row["fire_retention_pct"],
            row.get("verdict"),
        )
    print("T03", t03["verdict"])
    for r in t03["presets"]:
        print(r.get("name"), r.get("g3_ok"), r.get("InpATRMaxPoints"), r.get("exists"))


if __name__ == "__main__":
    main()
