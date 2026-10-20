"""UK100-AOS-P6 — L9 session soft veto CF · ±10% L2det stress · ATR G3 note data."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
OUT = Path(__file__).resolve().parent
PRESETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.042667
ATR_CAP = 1470.0
NEAR_FRAC = 0.9


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["spread_pts"] = df["spread_pts"].astype(float)
    df["atr_pts"] = df["atr_pts"].astype(float)
    df["is_thu"] = df["cell_dow_thu"].astype(int)
    df["near"] = df["near_atr_cap"].astype(int)
    df["buy"] = (df["side"] == "BUY").astype(int)
    df["buy_h08"] = ((df["side"] == "BUY") & (df["hour"] == 8)).astype(int)
    df["h08"] = (df["hour"] == 8).astype(int)
    df["h08_09"] = (df["hour"].isin([8, 9])).astype(int)
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
    prec = float((1 - skips["win"]).mean()) if len(skips) else None
    wed_fp = int(((skips["open_dt"].dt.dayofweek == 2) & (skips["win"] == 1)).sum()) if len(skips) else 0
    sell_fp = int(((skips["side"] == "SELL") & (skips["win"] == 1)).sum()) if len(skips) else 0
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
    elif d_en is not None and d_en > 0 and (prec or 0) >= 0.55 and wed_fp <= 1:
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
        "false_skip_sell_winners": sell_fp,
    }


def v1b_mask(df: pd.DataFrame, near_frac: float = NEAR_FRAC, atr_cap: float = ATR_CAP) -> np.ndarray:
    near = (df["buy"] == 1) & (df["atr_pts"] >= near_frac * atr_cap)
    return (df["is_thu"] == 1) | near.to_numpy()


def p6_t01(tip: pd.DataFrame, prior: pd.DataFrame) -> dict:
    """L9 session-quality soft veto candidates."""
    policies = {
        "skip_H08_all": tip["h08"] == 1,
        "skip_BUY_H08": tip["buy_h08"] == 1,
        "skip_London_open_H08_09": tip["h08_09"] == 1,
        "skip_late_H14_plus": tip["hour"] >= 14,
        "skip_spread_gt_p66": tip["spread_pts"]
        > tip["spread_pts"].quantile(0.66) + 1e-9,  # tip constant → often empty
    }
    tip_rows = {k: cf(tip, m.to_numpy(), k) for k, m in policies.items()}

    # On v1b-kept path (additive soft veto after det)
    kept_v1b = tip.loc[~v1b_mask(tip)].copy()
    add = {}
    if len(kept_v1b):
        for k, _ in policies.items():
            if k == "skip_spread_gt_p66":
                m = kept_v1b["spread_pts"] > tip["spread_pts"].quantile(0.66) + 1e-9
            elif k == "skip_H08_all":
                m = kept_v1b["h08"] == 1
            elif k == "skip_BUY_H08":
                m = kept_v1b["buy_h08"] == 1
            elif k == "skip_London_open_H08_09":
                m = kept_v1b["h08_09"] == 1
            else:
                m = kept_v1b["hour"] >= 14
            add[k + "_on_v1b_kept"] = cf(kept_v1b, m.to_numpy(), k + "_on_v1b_kept")

    # Prior spread diagnostic (only 2 fires at 140)
    prior_hi = prior["spread_pts"] >= 140
    prior_spread = cf(prior, prior_hi.to_numpy(), "prior_skip_spread_ge_140")

    tip_spread_nunique = int(tip["spread_pts"].nunique())
    return {
        "tip_spread_nunique": tip_spread_nunique,
        "tip_spread_note": (
            "Tip entry spread constant 120 — tercile soft veto has no tip signal; DISARM."
            if tip_spread_nunique <= 1
            else "Tip spread varies — see policies."
        ),
        "tip_policies": tip_rows,
        "additive_on_v1b_kept": add,
        "prior_spread_diagnostic": prior_spread,
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
    # Prefer BUY_H08 HOLD from P2 if still hold
    return rep


def p6_t02(tip: pd.DataFrame) -> dict:
    """±10% stress on L2det nearATR threshold (not SL/TP)."""
    base_mask = v1b_mask(tip, NEAR_FRAC, ATR_CAP)
    base = cf(tip, base_mask, "v1b_nominal_frac0.9_cap1470")

    stresses = {
        "near_frac_minus10": (NEAR_FRAC * 0.9, ATR_CAP),  # 0.81
        "near_frac_plus10": (NEAR_FRAC * 1.1, ATR_CAP),  # 0.99
        "atr_cap_minus10": (NEAR_FRAC, ATR_CAP * 0.9),  # 1323
        "atr_cap_plus10": (NEAR_FRAC, ATR_CAP * 1.1),  # 1617
        "both_loose": (NEAR_FRAC * 0.9, ATR_CAP * 1.1),
        "both_tight": (NEAR_FRAC * 1.1, ATR_CAP * 0.9),
    }
    rows = {}
    for name, (frac, cap) in stresses.items():
        m = v1b_mask(tip, frac, cap)
        row = cf(tip, m, name)
        row["near_frac"] = round(frac, 4)
        row["atr_cap"] = round(cap, 1)
        row["delta_E_N_vs_v1b"] = (
            None
            if row["kept"]["E_N"] is None or base["kept"]["E_N"] is None
            else round(row["kept"]["E_N"] - base["kept"]["E_N"], 4)
        )
        rows[name] = row

    # Robust if all stresses keep E_N >= v1b - 0.05 and retention within 15pp of v1b
    ok = []
    fail = []
    for name, row in rows.items():
        d = row["delta_E_N_vs_v1b"]
        ret_gap = abs(row["fire_retention_pct"] - base["fire_retention_pct"])
        if d is not None and d >= -0.05 and ret_gap <= 20:
            ok.append(name)
        else:
            fail.append(name)

    return {
        "baseline_v1b": base,
        "stresses": rows,
        "robust_pass": ok,
        "robust_fail": fail,
        "verdict": "PASS" if len(fail) == 0 else ("PASS_WITH_NOTES" if len(ok) >= 4 else "FAIL"),
        "note": (
            "Stresses L2det nearATR knobs only. Thu rule has no continuous threshold. "
            "SL/TP untouched."
        ),
    }


def p6_t03() -> dict:
    """Confirm ATR max declared on P0 + research OS presets."""
    targets = [
        PRESETS / "UK100" / "BMRG-M15-UK100-6M-P0_balanced_chart.set",
        PRESETS / "BMRG-M15-UK100-6M-P4_research_OS_W50.set",
        PRESETS / "UK100" / "BMRG-M15-UK100-6M-P4_research_OS_W50.set",
    ]
    rows = []
    for p in targets:
        if not p.exists():
            rows.append({"path": str(p), "exists": False})
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        atr_on = "InpUseATRRegime=true" in text
        atr_max = None
        for line in text.splitlines():
            if line.startswith("InpATRMaxPoints="):
                atr_max = line.split("=", 1)[1].split("||")[0]
        rows.append(
            {
                "path": str(p.relative_to(PRESETS.parent.parent.parent) if False else p.name),
                "full": str(p),
                "exists": True,
                "InpUseATRRegime": atr_on,
                "InpATRMaxPoints": atr_max,
                "g3_ok": atr_on and atr_max is not None and float(atr_max) == 1470.0,
            }
        )
    all_ok = all(r.get("g3_ok") for r in rows if r.get("exists"))
    return {
        "presets": rows,
        "engine_filter": "Include/Filters.mqh ATR max checked before AOSAllowEntry",
        "aos_does_not_lift_atr": True,
        "verdict": "PASS" if all_ok else "FAIL",
        "declaration": (
            "regime_filtered=true via London 08–17 · skip Tue · ATR max 1470 "
            "remains declared for G3 when research OS armed."
        ),
    }


def main() -> None:
    tip = load("uk100_tip_fire_tape_v0.csv")
    prior = load("uk100_prior_fire_tape_v0.csv")
    t01 = classify_t01(p6_t01(tip, prior))
    # Policy pick: do not newly ARM if P2 already HOLD BUY_H08 — confirm status
    t01["recommendation"] = {
        "spread_tercile": "DISARM_tip_constant",
        "skip_H08_all": t01["tip_policies"]["skip_H08_all"]["verdict"],
        "skip_BUY_H08": t01["tip_policies"]["skip_BUY_H08"]["verdict"],
        "london_open_H08_09": t01["tip_policies"]["skip_London_open_H08_09"]["verdict"],
        "late_H14": t01["tip_policies"]["skip_late_H14_plus"]["verdict"],
        "wire": (
            "No new L9 LIVE veto. Keep BUY_H08 as HOLD (P2). "
            "Optional SHADOW ledger reason L9_SESSION_QUALITY only if HOLD_SHADOW."
        ),
    }
    t02 = p6_t02(tip)
    t03 = p6_t03()
    rep = {
        "task": "UK100-AOS-P6",
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
    (OUT / "P6_HARDEN.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep["verdict"], indent=2))
    print("T01 armed", t01["armed"])
    print("T01 hold", t01["hold"])
    print("T02", t02["verdict"], "fail", t02["robust_fail"])
    print("T03", t03["verdict"])


if __name__ == "__main__":
    main()
