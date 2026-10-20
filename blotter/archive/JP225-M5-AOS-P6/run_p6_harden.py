"""JP225-M5-AOS-P6 — L9 session soft veto · ±10% L2det bound stress · ATR band G3."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "JP225" / "tapes"
OUT = Path(__file__).resolve().parent
PRESETS_EXPERTS = BMRG / "Presets"
PRESETS_TESTER = BMRG / "Profiles" / "Tester" / "BMRG" / "JP225"

R = 2.00
BWR = 1.0 / (1.0 + R)
LEAK = 0.033  # prior 3.3pp authority
ATR_MIN = 7610.0
ATR_MAX = 11285.0
OVERLAY = "L2det_jp225_m5_v1c"


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
    df["is_h10"] = (df["hour"] == 10).astype(int)
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["is_h16"] = (df["hour"] == 16).astype(int)
    df["london_open"] = (df["hour"].isin([8, 9])).astype(int)
    df["buy_h08"] = ((df["side"] == "BUY") & (df["hour"] == 8)).astype(int)
    df["soft_h"] = (df["hour"].isin([9, 13, 16])).astype(int)
    df["is_match"] = df["cell_match"].astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
    df["is_sep"] = (df["month"] == "2026-09").astype(int)
    df["is_jul"] = (df["month"] == "2026-07").astype(int)
    df["is_thu"] = (df["dow"] == "Thu").astype(int)
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
    """JP225 M5 CF — Jul / SELL / Thu / H08 / H10 protect."""
    base = book(df)
    skips = df.loc[mask]
    kept = df.loc[~mask]
    kept_m = book(kept)
    prec = float((1 - skips["win"]).mean()) if len(skips) else None
    sell_fp = (
        int(((skips["side"] == "SELL") & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    jul_fp = (
        int(((skips["is_jul"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    thu_fp = (
        int(((skips["is_thu"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    h08_fp = (
        int(((skips["is_h08"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    h10_fp = (
        int(((skips["is_h10"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
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
        and sell_fp <= 1
        and jul_fp <= 1
        and h10_fp <= 1
        and thu_fp <= 2
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
        "false_skip_jul_winners": jul_fp,
        "false_skip_thu_winners": thu_fp,
        "false_skip_h08_winners": h08_fp,
        "false_skip_h10_winners": h10_fp,
    }


def v1c_mask(df: pd.DataFrame) -> np.ndarray:
    """(BUY ∧ MATCH) ∨ (BUY ∧ H09|13|16) — EA default."""
    return (
        ((df["buy"] == 1) & (df["is_match"] == 1))
        | ((df["buy"] == 1) & (df["soft_h"] == 1))
    ).to_numpy()


def buy_hours(df: pd.DataFrame, hours: set[int]) -> np.ndarray:
    return ((df["buy"] == 1) & df["hour"].isin(hours)).to_numpy()


def p6_t01(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — London open / spread / soft hours."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H08": tip["is_h08"] == 1,
        "skip_BUY_H08": tip["buy_h08"] == 1,
        "skip_london_open_H08_09": tip["london_open"] == 1,
        "skip_H10": tip["is_h10"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
        "skip_soft_H09_13_16_all": tip["soft_h"] == 1,  # overlaps L2det BUY∧
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_arm = tip.loc[~v1c_mask(tip)].copy()
    add = {}
    if len(kept_arm):
        add_map = {
            "skip_H08": kept_arm["is_h08"] == 1,
            "skip_BUY_H08": kept_arm["buy_h08"] == 1,
            "skip_london_open_H08_09": kept_arm["london_open"] == 1,
            "skip_H10": kept_arm["is_h10"] == 1,
            "skip_spread_gt_p66": kept_arm["spread_pts"] > p66 + 1e-9,
            "skip_soft_H09_13_16_all": kept_arm["soft_h"] == 1,
        }
        for k, m in add_map.items():
            add[k + "_on_v1c_kept"] = cf(kept_arm, m.to_numpy(), k + "_on_v1c_kept")

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
    """±10%-style bound stress on L2det v1c hour/MATCH (not SL/TP / not nearATR)."""
    base_mask = v1c_mask(tip)
    base = cf(tip, base_mask, "v1c_BUY_MATCH_OR_BUY_H09_13_16")

    stresses = {
        "BUY_MATCH_only": ((tip["buy"] == 1) & (tip["is_match"] == 1)).to_numpy(),
        "BUY_H09_13_16_only": buy_hours(tip, {9, 13, 16}),
        "BUY_MATCH_OR_BUY_H13_only": (
            ((tip["buy"] == 1) & (tip["is_match"] == 1))
            | ((tip["buy"] == 1) & (tip["hour"] == 13))
        ).to_numpy(),
        "BUY_MATCH_OR_BUY_H09_13": (
            ((tip["buy"] == 1) & (tip["is_match"] == 1))
            | buy_hours(tip, {9, 13})
        ),
        "BUY_MATCH_OR_BUY_H09_13_16_nominal": v1c_mask(tip),
        "BUY_MATCH_OR_BUY_H08_09_13_16_wide": (
            ((tip["buy"] == 1) & (tip["is_match"] == 1))
            | buy_hours(tip, {8, 9, 13, 16})
        ),
        "BUY_Aug_only_OR_BUY_H09_13_16": (
            ((tip["buy"] == 1) & (tip["is_aug"] == 1))
            | buy_hours(tip, {9, 13, 16})
        ),
        "BUY_Sep_only_OR_BUY_H09_13_16": (
            ((tip["buy"] == 1) & (tip["is_sep"] == 1))
            | buy_hours(tip, {9, 13, 16})
        ),
        "MATCH_all_OR_BUY_H09_13_16": (
            (tip["is_match"] == 1).to_numpy() | buy_hours(tip, {9, 13, 16})
        ),
        "REJECT_probe_BUY_near_atr": (
            (tip["buy"] == 1) & (tip["near"] == 1)
        ).to_numpy(),
        "REJECT_probe_MISMATCH_all": (tip["cell_mismatch"] == 1).to_numpy(),
    }
    rows = {}
    for name, m in stresses.items():
        row = cf(tip, m, name)
        row["delta_E_N_vs_v1c"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    ok = []
    fail = []
    for name, row in rows.items():
        if name.startswith("REJECT_probe"):
            d = row["delta_E_N_vs_v1c"]
            if d is not None and d < 0:
                ok.append(name)
            else:
                fail.append(name)
            continue
        d = row["delta_E_N_vs_v1c"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        if name in ("BUY_MATCH_OR_BUY_H09_13_16_nominal",):
            ok.append(name)
            continue
        if (
            d is not None
            and d > 0.02
            and row["false_skip_sell_winners"] <= 1
            and row["false_skip_jul_winners"] <= 1
        ):
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
        "baseline_v1c": base,
        "stresses": rows,
        "robust_pass": ok,
        "robust_fail": fail,
        "verdict": verdict,
        "note": (
            "Stresses L2det M5 MATCH/hour knobs only. nearATR / MISMATCH skip are "
            "REJECT probes (tip stars). Engine ATR band 7610–11285 is separate G3. "
            "SL/TP untouched. Keep defaults: (BUY∧MATCH)∨(BUY∧H09|13|16)."
        ),
    }


def _parse_preset(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "name": path.name, "exists": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    atr_on = re.search(r"InpUseATRRegime=(true|false)", text)
    atr_min = re.search(r"InpATRMinPoints=([0-9.]+)", text)
    atr_max = re.search(r"InpATRMaxPoints=([0-9.]+)", text)
    m5_l2 = re.search(r"InpAOS_JP_M5_L2detEnable=(true|false)", text)
    g3_ok = bool(
        atr_on
        and atr_on.group(1) == "true"
        and atr_min
        and atr_max
        and abs(float(atr_min.group(1)) - ATR_MIN) < 1.0
        and abs(float(atr_max.group(1)) - ATR_MAX) < 1.0
    )
    return {
        "path": str(path),
        "name": path.name,
        "exists": True,
        "InpUseATRRegime": atr_on.group(1) if atr_on else None,
        "InpATRMinPoints": float(atr_min.group(1)) if atr_min else None,
        "InpATRMaxPoints": float(atr_max.group(1)) if atr_max else None,
        "InpAOS_JP_M5_L2detEnable": m5_l2.group(1) if m5_l2 else "n/a",
        "g3_ok": g3_ok,
    }


def p6_t03() -> dict:
    """Confirm ATR band 7610–11285 declared on P0 engine + P4 research OS presets."""
    targets = [
        PRESETS_EXPERTS / "BMRG-M5-JP225-6M-P0_growth_chart.set",
        PRESETS_EXPERTS / "BMRG-M5-JP225-6M-P4_research_OS_W50.set",
        PRESETS_TESTER / "BMRG-M5-JP225-6M-P0_growth_chart.set",
        PRESETS_TESTER / "BMRG-M5-JP225-6M-P4_research_OS_W50.set",
    ]
    rows = [_parse_preset(p) for p in targets]
    existing = [r for r in rows if r.get("exists")]
    all_ok = bool(existing) and all(r.get("g3_ok") for r in existing)
    return {
        "declared_atr_band": [ATR_MIN, ATR_MAX],
        "presets": rows,
        "engine_filter": "ATR band checked before AOSAllowEntry",
        "aos_does_not_lift_atr": True,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via session 08–17 · skip Tue · ATR band "
            f"{ATR_MIN:.0f}–{ATR_MAX:.0f} remains declared for G3 when research OS armed."
        ),
    }


def main() -> None:
    tip = load("jp225_m5_tip_fire_tape_v0.csv")
    ytd = load("jp225_m5_ytd_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, ytd))
    t01["recommendation"] = {
        "spread_tercile": t01["tip_policies"]["skip_spread_gt_p66"]["verdict"],
        "skip_H08": t01["tip_policies"]["skip_H08"]["verdict"],
        "skip_BUY_H08": t01["tip_policies"]["skip_BUY_H08"]["verdict"],
        "skip_london_open": t01["tip_policies"]["skip_london_open_H08_09"]["verdict"],
        "skip_H10": t01["tip_policies"]["skip_H10"]["verdict"],
        "skip_soft_hours_all": t01["tip_policies"]["skip_soft_H09_13_16_all"]["verdict"],
        "wire": (
            "No new L9 LIVE veto. Prefer overlay L2det_jp225_m5_v1c over stacking L9. "
            "H08/H10 are protect stars — soft veto only if ARM_SOFT with clean Jul/SELL FP. "
            "Soft hours all-sides already covered by L2det BUY∧ — do not double-wire as L9 LIVE."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    phase_ok = t02["verdict"].startswith("PASS") and t03["verdict"] == "PASS"
    rep = {
        "task": "JP225-M5-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "Leak_prior_pp": LEAK * 100,
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
                "jul_fp": v["false_skip_jul_winners"],
                "h08_fp": v["false_skip_h08_winners"],
                "h10_fp": v["false_skip_h10_winners"],
            }
            for k, v in t01["tip_policies"].items()
        },
        "L9_add_v1c": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
                "sell_fp": v["false_skip_sell_winners"],
                "jul_fp": v["false_skip_jul_winners"],
            }
            for k, v in t01["additive_on_v1c_kept"].items()
        },
        "L9_armed": t01["armed"],
        "L9_hold": t01["hold"],
        "L9_disarm": t01["disarm"],
        "L9_rec": t01["recommendation"],
        "stress_vs_v1c": {
            k: {
                "kept_E_N": v["kept"]["E_N"],
                "d_vs_v1c": v["delta_E_N_vs_v1c"],
                "ret": v["fire_retention_pct"],
                "verdict": v["verdict"],
                "sell_fp": v["false_skip_sell_winners"],
                "jul_fp": v["false_skip_jul_winners"],
            }
            for k, v in t02["stresses"].items()
        },
        "v1c_kept_E_N": t02["baseline_v1c"]["kept"]["E_N"],
        "v1c_ret": t02["baseline_v1c"]["fire_retention_pct"],
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
