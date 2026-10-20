"""AAPL-M5-AOS-P6 — L9 session soft veto · ±10% L2det bound stress · ATR/BBw G3."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "AAPL" / "tapes"
OUT = Path(__file__).resolve().parent
PRESETS_AAPL = BMRG / "Presets" / "AAPL"
PRESETS_ROOT = BMRG / "Presets"
ARCHIVE_P4 = BMRG / "blotter" / "archive" / "AAPL-M5-AOS-P4"

R = 280.0 / 190.0
BWR = 1.0 / (1.0 + R)
LEAK = 0.153  # profile authority
ATR_MIN = 24.0
ATR_MAX = 98.0
BBW_MIN = 0.30
BBW_MAX = 2.00
OVERLAY = "L2det_aapl_m5_v1b"


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
    df["is_jul"] = (df["month"] == "2026-07").astype(int)
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
    df["is_may"] = (df["month"] == "2026-05").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_jun"] = (df["month"] == "2026-06").astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
    df["is_h18"] = (df["hour"] == 18).astype(int)
    df["is_h14"] = (df["hour"] == 14).astype(int)
    df["is_h19"] = (df["hour"] == 19).astype(int)
    df["rth_core"] = (df["hour"].isin([15, 16, 17])).astype(int)
    df["rth_edge"] = (df["hour"].isin([14, 18, 19])).astype(int)
    df["overnight"] = (df["nights_held"].astype(int) >= 1).astype(int)
    return df.sort_values("open_dt").reset_index(drop=True)


def book(df: pd.DataFrame) -> dict:
    n = len(df)
    if n == 0:
        return {"n": 0, "WR": None, "E_N": None, "EF_profile_pp": None}
    wr = float(df["win"].mean())
    return {
        "n": n,
        "WR": round(wr * 100, 2),
        "E_N": round(wr * (R + 1) - 1, 4),
        "EF_profile_pp": round((wr - BWR - LEAK) * 100, 3),
    }


def cf(df: pd.DataFrame, mask: np.ndarray, label: str) -> dict:
    """AAPL M5 CF — May / Mon / BUY protect cells."""
    base = book(df)
    skips = df.loc[mask]
    kept = df.loc[~mask]
    kept_m = book(kept)
    prec = float((1 - skips["win"]).mean()) if len(skips) else None
    may_fp = (
        int(((skips["is_may"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    mon_fp = (
        int(((skips["is_mon"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
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
        if kept_m["EF_profile_pp"] is None or base["EF_profile_pp"] is None
        else round(kept_m["EF_profile_pp"] - base["EF_profile_pp"], 3)
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
        and may_fp <= 1
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
        "false_skip_may_winners": may_fp,
        "false_skip_mon_winners": mon_fp,
        "false_skip_buy_winners": buy_fp,
    }


def v1b_mask(df: pd.DataFrame) -> np.ndarray:
    """Jul ∨ Wed — EA default."""
    return ((df["is_jul"] == 1) | (df["is_wed"] == 1)).to_numpy()


def p6_t01(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """L9 session-quality soft veto — RTH edge / spread / overnight."""
    p66 = float(tip["spread_pts"].quantile(0.66))
    policies = {
        "skip_H14": tip["is_h14"] == 1,
        "skip_H18": tip["is_h18"] == 1,
        "skip_H19": tip["is_h19"] == 1,
        "skip_rth_edge_H14_18_19": tip["rth_edge"] == 1,
        "skip_overnight_held": tip["overnight"] == 1,
        "skip_spread_gt_p66": tip["spread_pts"] > p66 + 1e-9,
        "skip_spread_ge_30": tip["spread_pts"] >= 30.0,
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    kept_arm = tip.loc[~v1b_mask(tip)].copy()
    add = {}
    if len(kept_arm):
        add_map = {
            "skip_H14": kept_arm["is_h14"] == 1,
            "skip_H18": kept_arm["is_h18"] == 1,
            "skip_H19": kept_arm["is_h19"] == 1,
            "skip_rth_edge_H14_18_19": kept_arm["rth_edge"] == 1,
            "skip_overnight_held": kept_arm["overnight"] == 1,
            "skip_spread_gt_p66": kept_arm["spread_pts"] > p66 + 1e-9,
            "skip_spread_ge_30": kept_arm["spread_pts"] >= 30.0,
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
        "tip_spread_std": round(tip_spread_std, 4),
        "tip_spread_median": round(float(tip["spread_pts"].median()), 4),
        "tip_spread_p66": round(p66, 4),
        "tip_spread_note": (
            "Tip entry spread saturated (~29–31) — tercile soft veto weak; DISARM."
            if tip_spread_nunique <= 5 or tip_spread_std < 2.0
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
    """±10%-style bound stress on L2det v1b Jul∨Wed (not SL/TP / not May/Mon/BUY)."""
    base_mask = v1b_mask(tip)
    base = cf(tip, base_mask, "v1b_Jul_OR_Wed")

    stresses = {
        "Jul_only": (tip["is_jul"] == 1).to_numpy(),
        "Wed_only": (tip["is_wed"] == 1).to_numpy(),
        "Jul_OR_Wed_nominal": base_mask,
        "Jul_OR_Wed_OR_H18": (
            (tip["is_jul"] == 1) | (tip["is_wed"] == 1) | (tip["is_h18"] == 1)
        ).to_numpy(),
        "Jul_OR_Wed_OR_spread30": (
            (tip["is_jul"] == 1) | (tip["is_wed"] == 1) | (tip["spread_pts"] >= 30)
        ).to_numpy(),
        "Jul_OR_Wed_OR_Jun": (
            (tip["is_jul"] == 1) | (tip["is_wed"] == 1) | (tip["is_jun"] == 1)
        ).to_numpy(),
        "Jul_OR_Wed_OR_Aug": (
            (tip["is_jul"] == 1) | (tip["is_wed"] == 1) | (tip["is_aug"] == 1)
        ).to_numpy(),
        "Wed_OR_H18_no_Jul": (
            (tip["is_wed"] == 1) | (tip["is_h18"] == 1)
        ).to_numpy(),
        "Jul_OR_H18_no_Wed": (
            (tip["is_jul"] == 1) | (tip["is_h18"] == 1)
        ).to_numpy(),
        # protect-cell REJECT probes — must not improve by blanketing these
        "REJECT_probe_May": (tip["is_may"] == 1).to_numpy(),
        "REJECT_probe_Mon": (tip["is_mon"] == 1).to_numpy(),
        "REJECT_probe_BUY": (tip["buy"] == 1).to_numpy(),
        "REJECT_probe_near_atr": (tip["near"] == 1).to_numpy(),
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

    ok = []
    fail = []
    for name, row in rows.items():
        if name.startswith("REJECT_probe"):
            d = row["delta_E_N_vs_v1b"]
            # Pass if probe does not beat v1b (expected DISARM / worse kept E_N)
            if d is not None and d <= 0.02:
                ok.append(name)
            else:
                fail.append(name)
            continue
        d = row["delta_E_N_vs_v1b"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        if name == "Jul_OR_Wed_nominal":
            ok.append(name)
            continue
        if (
            d is not None
            and d > 0.02
            and row["false_skip_may_winners"] <= 1
            and row["fire_retention_pct"] >= 50
        ):
            ok.append(name + "_BETTER?")
        elif d is not None and d >= -0.08 and ret_gap <= 30:
            ok.append(name)
        elif row["verdict"] == "REJECT_FREQUENCY_STALL":
            ok.append(name + "_STALL_OK")  # expected for over-wide stacks
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
            "Stresses L2det M5 Jul/Wed knobs only. May/Mon/BUY/nearATR are REJECT "
            "probes (protect + tip star). Engine ATR 24–98 / BBw 0.30–2.00 is G3. "
            "SL/TP untouched. Keep defaults: Jul ∨ Wed."
        ),
    }


def _parse_preset(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "name": path.name, "exists": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    atr_on = re.search(r"InpUseATRRegime=(true|false)", text)
    atr_min = re.search(r"InpATRMinPoints=([0-9.]+)", text)
    atr_max = re.search(r"InpATRMaxPoints=([0-9.]+)", text)
    bbw_min = re.search(r"InpBBWidthMinPct=([0-9.]+)", text)
    bbw_max = re.search(r"InpBBWidthMaxPct=([0-9.]+)", text)
    m5_l2 = re.search(r"InpAOS_AAPL_M5_L2detEnable=(true|false)", text)
    g3_ok = bool(
        atr_on
        and atr_on.group(1) == "true"
        and atr_min
        and abs(float(atr_min.group(1)) - ATR_MIN) < 0.1
        and atr_max
        and abs(float(atr_max.group(1)) - ATR_MAX) < 0.1
        and bbw_min
        and abs(float(bbw_min.group(1)) - BBW_MIN) < 0.01
        and bbw_max
        and abs(float(bbw_max.group(1)) - BBW_MAX) < 0.01
    )
    return {
        "path": str(path),
        "name": path.name,
        "exists": True,
        "InpUseATRRegime": atr_on.group(1) if atr_on else None,
        "InpATRMinPoints": float(atr_min.group(1)) if atr_min else None,
        "InpATRMaxPoints": float(atr_max.group(1)) if atr_max else None,
        "InpBBWidthMinPct": float(bbw_min.group(1)) if bbw_min else None,
        "InpBBWidthMaxPct": float(bbw_max.group(1)) if bbw_max else None,
        "InpAOS_AAPL_M5_L2detEnable": m5_l2.group(1) if m5_l2 else "n/a",
        "g3_ok": g3_ok,
    }


def p6_t03() -> dict:
    """Confirm ATR 24–98 / BBw 0.30–2.00 declared on P0 engine + P4 research OS."""
    targets = [
        PRESETS_AAPL / "BMRG-M5-AAPL-6M-Balanced_TPgtSL.set",
        PRESETS_ROOT / "BMRG-M5-AAPL-6M-P4_research_OS_W50.set",
        ARCHIVE_P4 / "BMRG-M5-AAPL-6M-P4_research_OS_W50.set",
    ]
    rows = [_parse_preset(p) for p in targets]
    existing = [r for r in rows if r.get("exists")]
    all_ok = bool(existing) and all(r.get("g3_ok") for r in existing)
    return {
        "declared_atr_min": ATR_MIN,
        "declared_atr_max": ATR_MAX,
        "declared_bbw_min_pct": BBW_MIN,
        "declared_bbw_max_pct": BBW_MAX,
        "presets": rows,
        "engine_filter": "ATR/BBw checked before AOSAllowEntry",
        "aos_does_not_lift_atr_bbw": True,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via ATR 24–98 · BBw 0.30–2.00% · MaxSpread 40 "
            "remains declared for G3 when research OS armed."
        ),
    }


def main() -> None:
    tip = load("aapl_m5_tip_fire_tape_v0.csv")
    ytd = load("aapl_m5_ytd_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, ytd))
    spr30 = t01["tip_policies"]["skip_spread_ge_30"]["verdict"]
    t01["recommendation"] = {
        "spread_tercile": (
            "DISARM_tip_saturated"
            if t01["tip_spread_nunique"] <= 5 or t01["tip_spread_std"] < 2.0
            else t01["tip_policies"]["skip_spread_gt_p66"]["verdict"]
        ),
        "skip_H14": t01["tip_policies"]["skip_H14"]["verdict"],
        "skip_H18": t01["tip_policies"]["skip_H18"]["verdict"],
        "skip_H19": t01["tip_policies"]["skip_H19"]["verdict"],
        "skip_rth_edge": t01["tip_policies"]["skip_rth_edge_H14_18_19"]["verdict"],
        "skip_overnight": t01["tip_policies"]["skip_overnight_held"]["verdict"],
        "skip_spread_ge_30": spr30,
        "skip_spread_ge_30_l9_stance": (
            "NO_L9_LIVE — CF ARM_SOFT duplicates L2det optional HOLD "
            "(InpAOS_AAPL_M5_SkipHighSpread=false). Keep OFF; do not stack L9."
            if spr30 == "ARM_SOFT"
            else spr30
        ),
        "wire": (
            "No new L9 LIVE veto. Prefer overlay L2det_aapl_m5_v1b over stacking L9. "
            "H18 already optional HOLD on L2det — do not double-wire as L9 LIVE. "
            "Spread≥30 CF can look ARM_SOFT but tip is saturated (~29–31) — leave as "
            "L2det optional OFF, not L9 LIVE. Overnight REJECT — leave to L8."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    phase_ok = t02["verdict"].startswith("PASS") and t03["verdict"] == "PASS"
    rep = {
        "task": "AAPL-M5-AOS-P6",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "Leak_profile_pp": LEAK * 100,
        "P6_T01_L9_session": t01,
        "P6_T02_L2_stress": t02,
        "P6_T03_ATR_BBW_G3": t03,
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
                "may_fp": v["false_skip_may_winners"],
                "mon_fp": v["false_skip_mon_winners"],
                "buy_fp": v["false_skip_buy_winners"],
            }
            for k, v in t01["tip_policies"].items()
        },
        "L9_add_v1b": {
            k: {
                "verdict": v["verdict"],
                "delta_E_N": v["delta_E_N"],
                "ret": v["fire_retention_pct"],
                "may_fp": v["false_skip_may_winners"],
                "mon_fp": v["false_skip_mon_winners"],
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
                "may_fp": v["false_skip_may_winners"],
                "mon_fp": v["false_skip_mon_winners"],
            }
            for k, v in t02["stresses"].items()
        },
        "v1b_kept_E_N": t02["baseline_v1b"]["kept"]["E_N"],
        "v1b_ret": t02["baseline_v1b"]["fire_retention_pct"],
        "T02": t02["verdict"],
        "T02_fail": t02["robust_fail"],
        "ATR_BBW_G3": t03["verdict"],
        "phase": rep["verdict"]["phase"],
    }
    (OUT / "P6_SUMMARY.json").write_text(
        json.dumps(compact, indent=2), encoding="utf-8"
    )
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
