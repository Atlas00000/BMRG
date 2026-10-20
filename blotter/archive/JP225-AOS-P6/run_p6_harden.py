"""JP225-AOS-P6 — L9 session soft veto CF · L2det arm-width stress · ATR G3 note."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "JP225" / "tapes"
OUT = Path(__file__).resolve().parent
PRESETS_EXPERTS = BMRG / "Presets"
PRESETS_TESTER = BMRG.parents[1] / "Profiles" / "Tester" / "BMRG" / "JP225"

R = 1.50
BWR = 1.0 / (1.0 + R)
LEAK = 0.024471  # measured
ATR_MAX = 19670.0
NEAR_FRAC = 0.9
OVERLAY = "L2det_jp225_v1_May_OR_Jul"


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
    df["is_h14"] = (df["hour"] == 14).astype(int)
    df["london_open"] = (df["hour"].isin([8, 9])).astype(int)
    df["buy_h08"] = ((df["side"] == "BUY") & (df["hour"] == 8)).astype(int)
    df["is_may"] = df["month"].astype(str).str.endswith("-05").astype(int)
    df["is_jul"] = df["month"].astype(str).str.endswith("-07").astype(int)
    df["is_jun"] = df["month"].astype(str).str.endswith("-06").astype(int)
    df["is_aug"] = df["month"].astype(str).str.endswith("-08").astype(int)
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    if "cell_may_fragile" in df.columns:
        df["may_fragile"] = df["cell_may_fragile"].astype(int)
    else:
        df["may_fragile"] = (
            (df["is_may"] == 1) & (df["ouroboros_tag"] == "FRAGILE")
        ).astype(int)
    return df.sort_values("open_dt").reset_index(drop=True)


def book(df: pd.DataFrame) -> dict:
    n = len(df)
    if n == 0:
        return {"n": 0, "WR": None, "E_N": None, "EF_measured_pp": None}
    wr = float(df["win"].mean())
    return {
        "n": n,
        "WR": round(wr * 100, 2),
        "E_N": round(wr * (R + 1) - 1, 4),
        "EF_measured_pp": round((wr - BWR - LEAK) * 100, 3),
    }


def cf(df: pd.DataFrame, mask: np.ndarray, label: str) -> dict:
    """JP225 CF — protect Jun / Aug."""
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
    jun_fp = (
        int(((skips["is_jun"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    ret = 100.0 * len(kept) / len(df) if len(df) else 0.0
    d_en = (
        None
        if kept_m["E_N"] is None or base["E_N"] is None
        else round(kept_m["E_N"] - base["E_N"], 4)
    )
    d_ef = (
        None
        if kept_m["EF_measured_pp"] is None or base["EF_measured_pp"] is None
        else round(kept_m["EF_measured_pp"] - base["EF_measured_pp"], 3)
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
        and jun_fp <= 1
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
        "false_skip_jun_winners": jun_fp,
    }


def arm_mask(df: pd.DataFrame) -> np.ndarray:
    """Primary overlay: May∨Jul."""
    return ((df["is_may"] == 1) | (df["is_jul"] == 1)).to_numpy()


def p6_t01(tip: pd.DataFrame, janaug: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — London open / spread / H14."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H08": tip["is_h08"] == 1,
        "skip_BUY_H08": tip["buy_h08"] == 1,
        "skip_london_open_H08_09": tip["london_open"] == 1,
        "skip_H14": tip["is_h14"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_arm = tip.loc[~arm_mask(tip)].copy()
    add = {}
    if len(kept_arm):
        add_map = {
            "skip_H08": kept_arm["is_h08"] == 1,
            "skip_BUY_H08": kept_arm["buy_h08"] == 1,
            "skip_london_open_H08_09": kept_arm["london_open"] == 1,
            "skip_H14": kept_arm["is_h14"] == 1,
            "skip_spread_gt_p66": kept_arm["spread_pts"] > p66 + 1e-9,
        }
        for k, m in add_map.items():
            add[k + "_on_arm_kept"] = cf(kept_arm, m.to_numpy(), k + "_on_arm_kept")

    ja_p66 = float(janaug["spread_pts"].quantile(0.66))
    ja_spread = cf(
        janaug,
        (janaug["spread_pts"] > ja_p66 + 1e-9).to_numpy(),
        "janaug_skip_spread_gt_p66",
    )

    tip_spread_nunique = int(tip["spread_pts"].nunique())
    tip_spread_std = float(tip["spread_pts"].std(ddof=0))
    return {
        "tip_spread_nunique": tip_spread_nunique,
        "tip_spread_std": round(tip_spread_std, 2),
        "tip_spread_p66": round(p66, 4),
        "tip_spread_note": (
            "Tip entry spread low variance — tercile soft veto weak; DISARM."
            if tip_spread_nunique <= 3 or tip_spread_std < 50
            else "Tip spread varies — see policies."
        ),
        "tip_policies": tip_rows,
        "additive_on_arm_kept": add,
        "janaug_spread_diagnostic": ja_spread,
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
    """Arm-width + nearATR soft-threshold stress (not SL/TP)."""
    base_mask = arm_mask(tip)
    base = cf(tip, base_mask, "arm_May_OR_Jul")

    # Calendar width stress (May∨Jul has no continuous thr)
    stresses_det = {
        "may_fragile_only": (tip["may_fragile"] == 1).to_numpy(),
        "may_all": (tip["is_may"] == 1).to_numpy(),
        "jul_only": (tip["is_jul"] == 1).to_numpy(),
        "may_or_jul_or_wed": (
            (tip["is_may"] == 1) | (tip["is_jul"] == 1) | (tip["is_wed"] == 1)
        ).to_numpy(),
        "sell_and_may": (
            (tip["side"] == "SELL") & (tip["may_fragile"] == 1)
        ).to_numpy(),
    }

    # Soft nearATR feature stress (±10% of engine ATR max as soft gate)
    stresses_near = {}
    for name, (frac, cap) in {
        "near_frac_nominal": (NEAR_FRAC, ATR_MAX),
        "near_frac_minus10": (NEAR_FRAC * 0.9, ATR_MAX),
        "near_frac_plus10": (NEAR_FRAC * 1.1, ATR_MAX),
        "atr_cap_minus10": (NEAR_FRAC, ATR_MAX * 0.9),
        "atr_cap_plus10": (NEAR_FRAC, ATR_MAX * 1.1),
    }.items():
        m = (tip["atr_pts"] >= frac * cap).to_numpy()
        stresses_near[name] = m

    # AI thr ±10% if scored available
    scored = BMRG / "blotter" / "archive" / "JP225-AOS-P5" / "tip_l2ai_scored.csv"
    stresses_ai = {}
    if scored.exists():
        ai = pd.read_csv(scored)
        ai["open_dt"] = pd.to_datetime(ai["open_time"], format="%Y.%m.%d %H:%M:%S")
        tip2 = tip.merge(ai[["open_dt", "p_lose"]], on="open_dt", how="left")
        p = tip2["p_lose"].astype(float).fillna(0).to_numpy()
        # P5 best thr was 0.75
        thr0 = 0.75
        for name, thr in {
            "ai_thr_nominal": thr0,
            "ai_thr_minus10": thr0 * 0.9,
            "ai_thr_plus10": thr0 * 1.1,
        }.items():
            stresses_ai[name] = p >= thr

    rows = {}
    for name, m in {**stresses_det, **stresses_near, **stresses_ai}.items():
        row = cf(tip, np.asarray(m, dtype=bool), name)
        row["delta_E_N_vs_arm"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    ok, fail = [], []
    for name in stresses_det:
        row = rows[name]
        d_vs_tip = row["delta_E_N"]  # vs unfiltered tip
        # Narrowing: pass if still lifts tip E_N and does not stall
        # Wed widen: "robust fail" means correctly rejected as LIVE (stall) — track separately
        if name == "may_or_jul_or_wed":
            if row["verdict"] == "REJECT_FREQUENCY_STALL" or row["fire_retention_pct"] < 50:
                ok.append(name + "__correctly_rejected_widen")
            else:
                fail.append(name + "__unsafe_widen")
        elif (
            d_vs_tip is not None
            and d_vs_tip > 0
            and row["verdict"] not in ("DISARM", "REJECT_FREQUENCY_STALL")
        ):
            ok.append(name)
        else:
            fail.append(name)

    near_note = {}
    nom = rows.get("near_frac_nominal")
    if nom:
        for name in (
            "near_frac_minus10",
            "near_frac_plus10",
            "atr_cap_minus10",
            "atr_cap_plus10",
        ):
            r = rows[name]
            near_note[name] = {
                "delta_E_N_vs_near_nom": (
                    None
                    if r["kept"]["E_N"] is None or nom["kept"]["E_N"] is None
                    else round(r["kept"]["E_N"] - nom["kept"]["E_N"], 4)
                ),
                "ret": r["fire_retention_pct"],
                "verdict": r["verdict"],
            }

    ai_note = {}
    if "ai_thr_nominal" in rows:
        nom_ai = rows["ai_thr_nominal"]
        for name in ("ai_thr_minus10", "ai_thr_plus10"):
            r = rows[name]
            ai_note[name] = {
                "delta_E_N_vs_ai_nominal": (
                    None
                    if r["kept"]["E_N"] is None or nom_ai["kept"]["E_N"] is None
                    else round(r["kept"]["E_N"] - nom_ai["kept"]["E_N"], 4)
                ),
                "ret": r["fire_retention_pct"],
                "verdict": r["verdict"],
            }

    # Champ May∨Jul must lift tip; narrowing atoms still lift tip; Wed widen correctly stalled
    unsafe_widen = any(x.startswith("may_or_jul_or_wed__unsafe") for x in fail)
    narrow_ok = sum(1 for x in ok if not x.endswith("__correctly_rejected_widen"))
    if base["delta_E_N"] is None or base["delta_E_N"] <= 0:
        verdict = "FAIL"
    elif unsafe_widen or narrow_ok < 2:
        verdict = "FAIL"
    elif narrow_ok < 4 or any(x.startswith("may_or_jul_or_wed") for x in ok):
        verdict = "PASS_WITH_NOTES"  # Wed correctly rejected and/or some atoms thinner
    else:
        verdict = "PASS"

    return {
        "overlay": OVERLAY,
        "baseline_arm": base,
        "stresses": rows,
        "det_robust_pass": ok,
        "det_robust_fail": fail,
        "near_atr_soft_stress": near_note,
        "ai_thr_stress": ai_note,
        "verdict": verdict,
        "note": (
            "May∨Jul has no continuous threshold — stress calendar width + nearATR soft "
            "feature ±10% of ATR max 19670 + AI thr ±10%. Keep May∨Jul primary. "
            "Do not LIVE-wire Wed widen. SL/TP untouched. near_atr alone stays DISARM (P2)."
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
    g3_ok = (
        atr_on
        and atr_max is not None
        and abs(float(atr_max) - ATR_MAX) < 1e-3
    )
    return {
        "path": str(path),
        "name": path.name,
        "exists": True,
        "InpUseATRRegime": atr_on,
        "InpATRMaxPoints": atr_max,
        "g3_ok": g3_ok,
    }


def p6_t03() -> dict:
    """Confirm ATR max declared on OS baseline P0/P1 (P1.5 is alt · separate ATR)."""
    os_targets = [
        PRESETS_EXPERTS / "BMRG-M15-JP225-6M-P0_growth_chart.set",
        PRESETS_EXPERTS / "BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set",
        PRESETS_TESTER / "BMRG-M15-JP225-6M-P0_growth_chart.set",
        PRESETS_TESTER / "BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set",
    ]
    alt = _parse_preset(PRESETS_EXPERTS / "BMRG-M15-JP225-6M-P1p5_light_chart.set")
    rows = [_parse_preset(p) for p in os_targets]
    existing = [r for r in rows if r.get("exists")]
    all_ok = bool(existing) and all(r.get("g3_ok") for r in existing)
    return {
        "presets_os_baseline": rows,
        "preset_p1p5_alt": alt,
        "p1p5_note": (
            "P1.5 ATR max may differ (alt candidate) — not OS G3 until re-freeze."
        ),
        "engine_filter": "ATR max checked before AOSAllowEntry",
        "aos_does_not_lift_atr": True,
        "research_os_set": False,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via session 08–17 · skip Tue · ATR max 19670 "
            "remains declared for G3 when research OS armed (P7). No MQH / research .set yet."
        ),
    }


def main() -> None:
    tip = load("jp225_tip_fire_tape_v0.csv")
    janaug = load("jp225_tip_janaug_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, janaug))
    t01["recommendation"] = {
        "spread_tercile": (
            "DISARM_tip_low_variance"
            if t01["tip_spread_nunique"] <= 3 or t01["tip_spread_std"] < 50
            else t01["tip_policies"]["skip_spread_gt_p66"]["verdict"]
        ),
        "skip_H08": t01["tip_policies"]["skip_H08"]["verdict"],
        "skip_BUY_H08": t01["tip_policies"]["skip_BUY_H08"]["verdict"],
        "skip_london_open": t01["tip_policies"]["skip_london_open_H08_09"]["verdict"],
        "skip_H14": t01["tip_policies"]["skip_H14"]["verdict"],
        "wire": (
            "No new L9 LIVE veto. Prefer overlay May∨Jul over stacking L9. "
            "London-open / H08 soft veto only if ARM_SOFT with clean Jun/Aug FP — else SHADOW. "
            "H14 stays P2 HOLD. Spread tercile DISARM until tip fills show variance."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    rep = {
        "task": "JP225-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "Leak_measured_pp": LEAK * 100,
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
    print("T02", t02["verdict"], "fail", t02["det_robust_fail"], "ok", t02["det_robust_pass"])
    print(
        "T02 base E_N",
        t02["baseline_arm"]["kept"]["E_N"],
        "ret",
        t02["baseline_arm"]["fire_retention_pct"],
        "verdict",
        t02["baseline_arm"]["verdict"],
    )
    for name in (
        "may_fragile_only",
        "may_all",
        "jul_only",
        "may_or_jul_or_wed",
        "sell_and_may",
    ):
        row = t02["stresses"][name]
        print(
            name,
            "E_N",
            row["kept"]["E_N"],
            "d",
            row["delta_E_N_vs_arm"],
            "ret",
            row["fire_retention_pct"],
            row["verdict"],
        )
    print("T03", t03["verdict"])
    for r in t03["presets_os_baseline"]:
        print(r.get("name"), r.get("g3_ok"), r.get("InpATRMaxPoints"), r.get("exists"))
    alt = t03["preset_p1p5_alt"]
    print(
        "P1.5_alt",
        alt.get("g3_ok"),
        alt.get("InpATRMaxPoints"),
        alt.get("exists"),
    )


if __name__ == "__main__":
    main()
