"""JP225-AOS-P2-T01..T07 — parity, L2det SOFT CF, size stub, L2skip_jp225 train+stack."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

try:
    import joblib
except ImportError:  # pragma: no cover
    joblib = None

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\JP225\tapes"
)
OUT = Path(__file__).resolve().parent
MODELS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\infra\artefacts\models\L2skip_jp225"
)

R = 1.50
BWR = 1.0 / (1.0 + R)
ATR_MAX = 19670.0
LEAK_PRIOR = 0.043  # Stage-1 authority (~4.3 pp)
LEAK_PROXY = 0.048151  # journal 2x med from P1 COST_PROXY

FEATS = [
    "side_buy",
    "is_wed",
    "is_may",
    "is_jul",
    "is_jun",
    "is_aug",
    "is_mismatch",
    "is_fragile",
    "is_may_fragile",
    "near_atr_cap",
    "is_h08",
    "is_h09",
    "is_h14",
    "is_h13",
    "is_h15",
    "hour",
    "atr_z",
    "is_mon",
    "is_thu",
    "is_fri",
]


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(TAPES / name)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["win"] = df["win"].astype(int)
    df["y_lose"] = df["y_lose"].astype(int) if "y_lose" in df.columns else 1 - df["win"]
    df["hour"] = df["hour"].astype(int)
    df["atr_pts"] = pd.to_numeric(df["atr_pts"], errors="coerce")
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    df["near_atr_cap"] = df["near_atr_cap"].astype(int)
    df["side_buy"] = (df["side"] == "BUY").astype(int)
    df["is_h08"] = (df["hour"] == 8).astype(int)
    df["is_h09"] = (df["hour"] == 9).astype(int)
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["is_h14"] = (df["hour"] == 14).astype(int)
    df["is_h15"] = (df["hour"] == 15).astype(int)
    df["is_may"] = df["month"].str.endswith("-05").astype(int)
    df["is_jun"] = df["month"].str.endswith("-06").astype(int)
    df["is_jul"] = df["month"].str.endswith("-07").astype(int)
    df["is_aug"] = df["month"].str.endswith("-08").astype(int)
    df["is_oct"] = df["month"].str.endswith("-10").astype(int)
    df["is_mismatch"] = (df["ouroboros_tag"] == "MISMATCH").astype(int)
    df["is_fragile"] = (df["ouroboros_tag"] == "FRAGILE").astype(int)
    df["is_match"] = (df["ouroboros_tag"] == "MATCH").astype(int)
    df["is_may_fragile"] = (
        df["cell_may_fragile"].astype(int)
        if "cell_may_fragile" in df.columns
        else ((df["is_may"] == 1) & (df["is_fragile"] == 1)).astype(int)
    )
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_thu"] = (df["dow"] == "Thu").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    atr = df["atr_pts"]
    df["atr_z"] = (atr - atr.mean()) / (atr.std() + 1e-9)
    return df.sort_values("open_dt").reset_index(drop=True)


def metrics(sub: pd.DataFrame, label: str) -> dict:
    n = len(sub)
    if n == 0:
        return {"label": label, "n": 0}
    wr = float(sub["win"].mean())
    bm = wr - BWR
    en = wr * (R + 1) - 1
    return {
        "label": label,
        "n": int(n),
        "WR": round(wr * 100, 2),
        "E_N": round(en, 4),
        "EF_prior_pp": round((bm - LEAK_PRIOR) * 100, 3),
        "EF_proxy_pp": round((bm - LEAK_PROXY) * 100, 3),
        "avgR": round(float(sub["pnl_R"].mean()), 4),
        "tip_EF_cleared": bool((bm - LEAK_PRIOR) > 0),
    }


def skip_report(base: pd.DataFrame, mask_skip: np.ndarray) -> dict:
    skipped = base.loc[mask_skip]
    kept = base.loc[~mask_skip]
    n_skip = int(mask_skip.sum())
    losers_base = int((base["win"] == 0).sum())
    losers_skip = int((skipped["win"] == 0).sum()) if n_skip else 0
    base_m = metrics(base, "b")
    kept_m = metrics(kept, "k") if len(kept) else {"n": 0, "E_N": 0, "EF_prior_pp": 0, "WR": 0}

    def fp(cond) -> int:
        if n_skip == 0:
            return 0
        return int((cond & (skipped["win"] == 1)).sum())

    return {
        "skips_n": n_skip,
        "precision_vs_losers": round(losers_skip / n_skip, 4) if n_skip else None,
        "recall_losers": round(losers_skip / losers_base, 4) if losers_base else None,
        "false_skip_winners": int((skipped["win"] == 1).sum()) if n_skip else 0,
        "false_skip_aug_winners": fp(skipped["is_aug"] == 1),
        "false_skip_jun_winners": fp(skipped["is_jun"] == 1),
        "false_skip_match_winners": fp(skipped["is_match"] == 1),
        "false_skip_buy_winners": fp(skipped["side"] == "BUY"),
        "false_skip_mon_winners": fp(skipped["dow"] == "Mon"),
        "false_skip_thu_winners": fp(skipped["dow"] == "Thu"),
        "false_skip_h13_winners": fp(skipped["hour"] == 13),
        "false_skip_h15_winners": fp(skipped["hour"] == 15),
        "kept": kept_m,
        "delta_E_N": round(kept_m["E_N"] - base_m["E_N"], 4) if kept_m.get("n") else None,
        "delta_EF_prior_pp": round(kept_m["EF_prior_pp"] - base_m["EF_prior_pp"], 3)
        if kept_m.get("n")
        else None,
        "fire_retention_pct": round(100.0 * len(kept) / len(base), 1) if len(base) else 0,
    }


def verdict(base_m: dict, rep: dict) -> str:
    k = rep["kept"]
    if k.get("n", 0) == 0:
        return "REJECT"
    if k["n"] / base_m["n"] < 0.50:
        return "REJECT_FREQUENCY_STALL"
    if k["WR"] > base_m["WR"] and k["E_N"] < base_m["E_N"] - 1e-9:
        return "REJECT"
    ef_ok = k["EF_prior_pp"] >= base_m["EF_prior_pp"] - 1.0
    en_up = k["E_N"] > base_m["E_N"] + 1e-9
    en_hold = k["E_N"] >= base_m["E_N"] - 1e-9
    prec = rep["precision_vs_losers"] or 0
    tip_cleared = bool(k.get("tip_EF_cleared"))
    protect_fp = (
        rep["false_skip_aug_winners"]
        + rep["false_skip_jun_winners"]
        + rep["false_skip_match_winners"]
        + rep["false_skip_h13_winners"]
        + rep["false_skip_h15_winners"]
    )
    # Prefer policies that clear tip EF or lift E_N with decent precision
    if en_up and ef_ok and prec >= 0.55 and rep["skips_n"] > 0:
        if protect_fp >= 4 or rep["false_skip_jun_winners"] >= 3:
            return "HOLD_SOFT"
        if tip_cleared or (k["EF_prior_pp"] - base_m["EF_prior_pp"]) >= 1.0:
            return "ARM_SOFT"
        return "ARM_SOFT"
    if ef_ok and en_hold and rep["skips_n"] > 0:
        return "HOLD_SOFT"
    if tip_cleared and en_up and ef_ok:
        return "ARM_SOFT"
    if not ef_ok and not en_up:
        return "DISARM"
    return "DISARM"


def parity(tip: pd.DataFrame, janaug: pd.DataFrame) -> dict:
    both = pd.concat([tip, janaug], ignore_index=True)
    tue = both[both["dow"] == "Tue"]
    atr_over = both[both["atr_pts"].notna() & (both["atr_pts"] > ATR_MAX)]
    return {
        "task": "JP225-AOS-P2-T01",
        "tue_fires": int(len(tue)),
        "fires_with_atr_gt_max": int(len(atr_over)),
        "near_atr_cap_fires_tip": int(tip["near_atr_cap"].sum()),
        "near_atr_cap_fires_janaug": int(janaug["near_atr_cap"].sum()),
        "parity_tue": "PASS" if len(tue) == 0 else "FAIL",
        "parity_atr_note": (
            "Engine ATR max + Fade + Tue skip gate entries; "
            "do not re-gate Tue/ATR/Fade in L2det."
        ),
    }


def eval_policies(base: pd.DataFrame, policies: dict[str, pd.Series]) -> dict:
    base_m = metrics(base, "baseline")
    out = {"baseline": base_m, "policies": {}}
    for name, mask in policies.items():
        mask_np = mask.to_numpy() if hasattr(mask, "to_numpy") else np.asarray(mask)
        if mask_np.sum() == 0:
            out["policies"][name] = {
                "skips_n": 0,
                "verdict": "N/A_EMPTY",
                "note": "no matching fires in window",
            }
            continue
        rep = skip_report(base, mask_np)
        out["policies"][name] = {**rep, "verdict": verdict(base_m, rep)}
    return out


def size_table_spec() -> dict:
    return {
        "task": "JP225-AOS-P2-T05",
        "status": "SPEC_ONLY",
        "wire_after": "L4",
        "rule": "Skip outranks size; L2det WOULD_SKIP → f=0",
        "table": [
            {"state": "Expanding / Stable", "f_mult": 1.0},
            {"state": "Compressing", "f_mult": 0.5},
            {"state": "Near frontier", "f_mult": 0.25},
            {"state": "Below frontier", "f_mult": 0.0},
            {"state": "L2det WOULD_SKIP", "f_mult": 0.0},
        ],
    }


def train_l2ai(tip: pd.DataFrame, janaug: pd.DataFrame) -> dict:
    """Train on Jan–Apr (pre-tip) · OOS on tip."""
    train = janaug[janaug["month"].isin(["2026-01", "2026-02", "2026-03", "2026-04"])].copy()
    if len(train) < 20:
        cut = int(0.7 * len(tip))
        train = tip.iloc[:cut].copy()
        test = tip.iloc[cut:].copy()
    else:
        test = tip.copy()

    for col in FEATS:
        if col not in train.columns:
            train[col] = 0
        if col not in test.columns:
            test[col] = 0
        if col not in tip.columns:
            tip[col] = 0

    Xtr = train[FEATS].fillna(0).to_numpy()
    ytr = train["y_lose"].to_numpy()
    Xte = test[FEATS].fillna(0).to_numpy()
    yte = test["y_lose"].to_numpy()

    scaler = StandardScaler()
    Xtr_s = scaler.fit_transform(Xtr)
    Xte_s = scaler.transform(Xte)
    clf = LogisticRegression(class_weight="balanced", C=0.5, max_iter=500)
    clf.fit(Xtr_s, ytr)
    proba = clf.predict_proba(Xte_s)[:, 1]
    try:
        auc = float(roc_auc_score(yte, proba))
    except ValueError:
        auc = float("nan")

    tip_base = metrics(tip, "tip_base")
    best = None
    Xt = scaler.transform(tip[FEATS].fillna(0).to_numpy())
    p_tip = clf.predict_proba(Xt)[:, 1]
    for thr in np.arange(0.50, 0.90, 0.05):
        mask = p_tip >= thr
        if mask.sum() == 0:
            continue
        rep = skip_report(tip, mask)
        v = verdict(tip_base, rep)
        cand = {
            "thr": round(float(thr), 2),
            "verdict": v,
            "delta_E_N": rep["delta_E_N"],
            "delta_EF_prior_pp": rep["delta_EF_prior_pp"],
            "precision_vs_losers": rep["precision_vs_losers"],
            "fire_retention_pct": rep["fire_retention_pct"],
            "skips_n": rep["skips_n"],
            "false_skip_aug_winners": rep["false_skip_aug_winners"],
            "false_skip_jun_winners": rep["false_skip_jun_winners"],
            "kept_EF_prior_pp": rep["kept"].get("EF_prior_pp"),
            "tip_EF_cleared": rep["kept"].get("tip_EF_cleared"),
        }
        if best is None or (
            (cand["delta_E_N"] or -9) > (best["delta_E_N"] or -9)
            and cand["verdict"] in ("ARM_SOFT", "HOLD_SOFT")
        ):
            best = cand

    MODELS.mkdir(parents=True, exist_ok=True)
    latest = MODELS / "LATEST"
    latest.mkdir(parents=True, exist_ok=True)
    meta = {
        "model": "LogisticRegression",
        "feats": FEATS,
        "train_n": int(len(train)),
        "train_months": sorted(train["month"].unique().tolist()),
        "tip_oos_auc": round(auc, 4) if auc == auc else None,
        "pin": "L2skip_jp225",
        "status": "SHADOW_ONLY",
        "created": datetime.now(timezone.utc).isoformat(),
    }
    if joblib is not None:
        joblib.dump({"scaler": scaler, "clf": clf, "feats": FEATS}, latest / "model.joblib")
    (latest / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    arm = "DISARM"
    if best and best["verdict"] == "ARM_SOFT" and (meta["tip_oos_auc"] or 0) >= 0.55:
        arm = "ARM_SOFT"
    elif best and best["verdict"] in ("ARM_SOFT", "HOLD_SOFT"):
        arm = "HOLD_SOFT" if (meta["tip_oos_auc"] or 0) < 0.55 else best["verdict"]

    return {
        "task": "JP225-AOS-P2-T06",
        "meta": meta,
        "best_thr_on_tip": best,
        "arm_status": arm,
        "note": "DISARM if tip AUC < 0.55 or no thr clears protect cells / iteration bar",
    }


def stack_cf(tip: pd.DataFrame, ai: dict) -> dict:
    tip_base = metrics(tip, "P1")
    stacks = {
        "P1_engine": np.zeros(len(tip), dtype=bool),
        "L2det_May_fragile": (tip["is_may_fragile"] == 1).to_numpy(),
        "L2det_Jul": (tip["is_jul"] == 1).to_numpy(),
        "L2det_Wed": (tip["is_wed"] == 1).to_numpy(),
        "L2det_May_OR_Jul": ((tip["is_may_fragile"] == 1) | (tip["is_jul"] == 1)).to_numpy(),
        "L2det_May_OR_Jul_OR_Wed": (
            (tip["is_may_fragile"] == 1) | (tip["is_jul"] == 1) | (tip["is_wed"] == 1)
        ).to_numpy(),
        "L2det_H14": (tip["is_h14"] == 1).to_numpy(),
        "L2det_H08_OR_H09": ((tip["is_h08"] == 1) | (tip["is_h09"] == 1)).to_numpy(),
        "L2det_H14_OR_H08_OR_H09": (
            (tip["is_h14"] == 1) | (tip["is_h08"] == 1) | (tip["is_h09"] == 1)
        ).to_numpy(),
        "L2det_SELL_AND_MayJulWed": (
            (tip["side_buy"] == 0)
            & (
                (tip["is_may_fragile"] == 1)
                | (tip["is_jul"] == 1)
                | (tip["is_wed"] == 1)
            )
        ).to_numpy(),
        "L2det_SELL_AND_H14": ((tip["side_buy"] == 0) & (tip["is_h14"] == 1)).to_numpy(),
        "L2det_near_atr_alone": (tip["near_atr_cap"] == 1).to_numpy(),
        "L2det_FRAGILE_all": (tip["is_fragile"] == 1).to_numpy(),
        "L2det_v1_May_OR_Jul_OR_Wed": (
            (tip["is_may_fragile"] == 1) | (tip["is_jul"] == 1) | (tip["is_wed"] == 1)
        ).to_numpy(),
        "L2det_v1b_MayJulWed_OR_H14": (
            (tip["is_may_fragile"] == 1)
            | (tip["is_jul"] == 1)
            | (tip["is_wed"] == 1)
            | (tip["is_h14"] == 1)
        ).to_numpy(),
        "L2det_v1c_MayJul_OR_SELL_Wed": (
            (tip["is_may_fragile"] == 1)
            | (tip["is_jul"] == 1)
            | ((tip["side_buy"] == 0) & (tip["is_wed"] == 1))
        ).to_numpy(),
    }

    if ai.get("best_thr_on_tip") and ai["best_thr_on_tip"].get("thr") is not None:
        thr = ai["best_thr_on_tip"]["thr"]
        try:
            blob = joblib.load(MODELS / "LATEST" / "model.joblib") if joblib else None
        except Exception:
            blob = None
        if blob is not None:
            p = blob["clf"].predict_proba(
                blob["scaler"].transform(tip[FEATS].fillna(0).to_numpy())
            )[:, 1]
            stacks["L2AI_only"] = p >= thr
            stacks["L2det_v1_OR_L2AI"] = stacks["L2det_v1_May_OR_Jul_OR_Wed"] | (p >= thr)

    out = {"baseline": tip_base, "stacks": {}}
    for name, mask in stacks.items():
        if name == "P1_engine":
            out["stacks"][name] = {
                "kept": tip_base,
                "skips_n": 0,
                "delta_E_N": 0.0,
                "fire_retention_pct": 100.0,
                "verdict": "BASELINE",
            }
            continue
        if mask.sum() == 0:
            out["stacks"][name] = {"skips_n": 0, "verdict": "N/A_EMPTY"}
            continue
        rep = skip_report(tip, mask)
        out["stacks"][name] = {**rep, "verdict": verdict(tip_base, rep)}
    return out


def main() -> None:
    tip = load("jp225_tip_fire_tape_v0.csv")
    janaug = load("jp225_janaug_fire_tape_v0.csv")

    par = parity(tip, janaug)

    # T02 — May / Wed
    t02_tip = eval_policies(
        tip,
        {
            "skip_May_fragile": tip["is_may_fragile"] == 1,
            "skip_Wed": tip["is_wed"] == 1,
            "skip_May_OR_Wed": (tip["is_may_fragile"] == 1) | (tip["is_wed"] == 1),
            "skip_FRAGILE_all": tip["is_fragile"] == 1,
            "skip_Jun": tip["is_jun"] == 1,  # expect DISARM / protect damage
        },
    )
    t02_ja = eval_policies(
        janaug,
        {
            "skip_May_fragile": janaug["is_may_fragile"] == 1,
            "skip_Wed": janaug["is_wed"] == 1,
            "skip_May_OR_Wed": (janaug["is_may_fragile"] == 1) | (janaug["is_wed"] == 1),
            "skip_Feb": janaug["month"] == "2026-02",
            "skip_Mar": janaug["month"] == "2026-03",
        },
    )

    # T03 — Jul / hours
    t03 = eval_policies(
        tip,
        {
            "skip_Jul": tip["is_jul"] == 1,
            "skip_MISMATCH_all": tip["is_mismatch"] == 1,
            "skip_H14": tip["is_h14"] == 1,
            "skip_H08": tip["is_h08"] == 1,
            "skip_H09": tip["is_h09"] == 1,
            "skip_H08_OR_H09": (tip["is_h08"] == 1) | (tip["is_h09"] == 1),
            "skip_H14_OR_H08_OR_H09": (
                (tip["is_h14"] == 1) | (tip["is_h08"] == 1) | (tip["is_h09"] == 1)
            ),
            "skip_H13": tip["is_h13"] == 1,  # protect — expect DISARM/HOLD weak
            "skip_May_OR_Jul": (tip["is_may_fragile"] == 1) | (tip["is_jul"] == 1),
        },
    )

    # T04 — SELL conjunction / near_atr
    t04 = eval_policies(
        tip,
        {
            "skip_SELL_all": tip["side_buy"] == 0,
            "skip_BUY_all": tip["side_buy"] == 1,
            "skip_SELL_AND_MayJulWed": (tip["side_buy"] == 0)
            & (
                (tip["is_may_fragile"] == 1)
                | (tip["is_jul"] == 1)
                | (tip["is_wed"] == 1)
            ),
            "skip_SELL_AND_H14": (tip["side_buy"] == 0) & (tip["is_h14"] == 1),
            "skip_SELL_AND_May": (tip["side_buy"] == 0) & (tip["is_may_fragile"] == 1),
            "skip_near_atr_alone": tip["near_atr_cap"] == 1,
            "skip_near_atr_AND_MayJulWed": (tip["near_atr_cap"] == 1)
            & (
                (tip["is_may_fragile"] == 1)
                | (tip["is_jul"] == 1)
                | (tip["is_wed"] == 1)
            ),
        },
    )

    t05 = size_table_spec()
    t06 = train_l2ai(tip, janaug)
    t07 = stack_cf(tip, t06)

    preferred = []
    for block in (t02_tip, t03, t04):
        for name, pol in block["policies"].items():
            if pol.get("verdict") == "ARM_SOFT":
                preferred.append(name)
    for name, st in t07["stacks"].items():
        if st.get("verdict") == "ARM_SOFT":
            preferred.append(name)

    # Best tip-EF-clearing ARM among stacks
    best_clear = None
    for name, st in t07["stacks"].items():
        k = st.get("kept") or {}
        if not k.get("tip_EF_cleared"):
            continue
        if st.get("verdict") not in ("ARM_SOFT", "HOLD_SOFT"):
            continue
        score = (st.get("delta_E_N") or -9, -(st.get("false_skip_jun_winners") or 99))
        if best_clear is None or score > best_clear[1]:
            best_clear = (name, score, st)

    packet = {
        "task": "JP225-AOS-P2",
        "dated": datetime.now(timezone.utc).isoformat(),
        "compare_window": "tip 2026.05.01-2026.08.31",
        "Leak_prior_pp": LEAK_PRIOR * 100,
        "Leak_proxy_pp": LEAK_PROXY * 100,
        "Leak_source_authority": "prior_4.3pp_until_deals",
        "P2_T01_parity": par,
        "P2_T02_tip": t02_tip,
        "P2_T02_janaug": t02_ja,
        "P2_T03_jul_hours": t03,
        "P2_T04_sell_near_atr": t04,
        "P2_T05_size_table": t05,
        "P2_T06_L2AI": t06,
        "P2_T07_stacks": t07,
        "preferred_ARM_SOFT_candidates": preferred,
        "best_tip_EF_clear_stack": None
        if best_clear is None
        else {
            "name": best_clear[0],
            "delta_E_N": best_clear[2].get("delta_E_N"),
            "delta_EF_prior_pp": best_clear[2].get("delta_EF_prior_pp"),
            "fire_retention_pct": best_clear[2].get("fire_retention_pct"),
            "kept_EF_prior_pp": (best_clear[2].get("kept") or {}).get("EF_prior_pp"),
            "verdict": best_clear[2].get("verdict"),
            "false_skip_jun_winners": best_clear[2].get("false_skip_jun_winners"),
            "false_skip_aug_winners": best_clear[2].get("false_skip_aug_winners"),
        },
    }
    (OUT / "P2_CF.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")

    print("T01 parity", par["parity_tue"], "atr>max", par["fires_with_atr_gt_max"])
    print("baseline tip EF", t02_tip["baseline"]["EF_prior_pp"], "E_N", t02_tip["baseline"]["E_N"])
    for title, block in (
        ("T02 tip", t02_tip),
        ("T03", t03),
        ("T04", t04),
    ):
        print("---", title, "---")
        for k, v in block["policies"].items():
            print(
                k,
                v.get("verdict"),
                "dEN",
                v.get("delta_E_N"),
                "dEF",
                v.get("delta_EF_prior_pp"),
                "ret",
                v.get("fire_retention_pct"),
                "EF",
                (v.get("kept") or {}).get("EF_prior_pp"),
                "cleared",
                (v.get("kept") or {}).get("tip_EF_cleared"),
            )
    print("--- T06 ---", t06["arm_status"], "AUC", t06["meta"]["tip_oos_auc"])
    print("--- T07 stacks ---")
    for k, v in t07["stacks"].items():
        print(
            k,
            v.get("verdict"),
            "dEN",
            v.get("delta_E_N"),
            "ret",
            v.get("fire_retention_pct"),
            "EF",
            (v.get("kept") or {}).get("EF_prior_pp"),
            "cleared",
            (v.get("kept") or {}).get("tip_EF_cleared"),
        )
    print("ARM_SOFT:", preferred)
    print("best EF-clear:", packet["best_tip_EF_clear_stack"])


if __name__ == "__main__":
    main()
