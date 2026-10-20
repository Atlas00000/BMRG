"""DE40-AOS-P2-T01..T07 — parity, L2det SOFT CF, size stub, L2skip_de40 train+stack."""
from __future__ import annotations

import csv
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)
OUT = Path(__file__).resolve().parent
MODELS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\infra\artefacts\models\L2skip_de40"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
ATR_MAX = 4070.0
# Stage-1 authority until deals (live spread prior)
LEAK_PRIOR = 0.098
# Journal proxy (understates live) — report only
LEAK_PROXY = 0.014933

FEATS = [
    "side_buy",
    "is_h13",
    "is_feb",
    "is_mar",
    "is_mismatch",
    "is_fragile",
    "near_atr_cap",
    "hour",
    "atr_z",
    "is_wed",
    "is_mon",
    "is_fri",
    "is_aug",
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
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["is_h08"] = (df["hour"] == 8).astype(int)
    df["is_feb"] = (df["month"] == "2026-02").astype(int)
    df["is_mar"] = (df["month"] == "2026-03").astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
    df["is_may"] = (df["month"] == "2026-05").astype(int)
    df["is_mismatch"] = (df["ouroboros_tag"] == "MISMATCH").astype(int)
    df["is_fragile"] = (df["ouroboros_tag"] == "FRAGILE").astype(int)
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    atr = df["atr_pts"]
    df["atr_z"] = (atr - atr.mean()) / (atr.std() + 1e-9)
    return df.sort_values("open_dt").reset_index(drop=True)


def metrics(sub: pd.DataFrame, label: str, leak: float = LEAK_PRIOR) -> dict:
    n = len(sub)
    if n == 0:
        return {"label": label, "n": 0}
    wr = float(sub["win"].mean())
    bm = wr - BWR
    en = wr * (R + 1) - 1
    ef = bm - leak
    return {
        "label": label,
        "n": int(n),
        "WR": round(wr * 100, 2),
        "E_N": round(en, 4),
        "EF_prior_pp": round((bm - LEAK_PRIOR) * 100, 3),
        "EF_proxy_pp": round((bm - LEAK_PROXY) * 100, 3),
        "avgR": round(float(sub["pnl_R"].mean()), 4),
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
        return int(((cond) & (skipped["win"] == 1)).sum())

    return {
        "skips_n": n_skip,
        "precision_vs_losers": round(losers_skip / n_skip, 4) if n_skip else None,
        "recall_losers": round(losers_skip / losers_base, 4) if losers_base else None,
        "false_skip_winners": int((skipped["win"] == 1).sum()) if n_skip else 0,
        "false_skip_aug_winners": fp(skipped["is_aug"] == 1),
        "false_skip_sell_winners": fp(skipped["side"] == "SELL"),
        "false_skip_mon_winners": fp(skipped["dow"] == "Mon"),
        "false_skip_h08_winners": fp(skipped["hour"] == 8),
        "false_skip_may_winners": fp(skipped["is_may"] == 1),
        "kept": kept_m,
        "delta_E_N": round(kept_m["E_N"] - base_m["E_N"], 4) if kept_m["n"] else None,
        "delta_EF_prior_pp": round(kept_m["EF_prior_pp"] - base_m["EF_prior_pp"], 3)
        if kept_m["n"]
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
    # Stage-1 bar uses prior Leak EF
    ef_ok = k["EF_prior_pp"] >= base_m["EF_prior_pp"] - 1.0
    en_up = k["E_N"] > base_m["E_N"] + 1e-9
    en_hold = k["E_N"] >= base_m["E_N"] - 1e-9
    prec = rep["precision_vs_losers"] or 0
    # Heavy protect-cell damage → HOLD not ARM
    protect_fp = (
        rep["false_skip_aug_winners"]
        + rep["false_skip_sell_winners"]
        + rep["false_skip_mon_winners"]
        + rep["false_skip_h08_winners"]
    )
    if en_up and ef_ok and prec >= 0.55 and rep["skips_n"] > 0:
        if protect_fp >= 3 and rep["false_skip_aug_winners"] >= 2:
            return "HOLD_SOFT"
        return "ARM_SOFT"
    if ef_ok and en_hold and rep["skips_n"] > 0:
        return "HOLD_SOFT"
    if not ef_ok and not en_up:
        return "DISARM"
    return "DISARM"


def parity(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    both = pd.concat([tip, ytd], ignore_index=True)
    tue = both[both["dow"] == "Tue"]
    atr_over = both[both["atr_pts"].notna() & (both["atr_pts"] > ATR_MAX)]
    return {
        "task": "DE40-AOS-P2-T01",
        "tue_fires": int(len(tue)),
        "fires_with_atr_gt_max": int(len(atr_over)),
        "near_atr_cap_fires_tip": int(tip["near_atr_cap"].sum()),
        "near_atr_cap_fires_ytd": int(ytd["near_atr_cap"].sum()),
        "parity_tue": "PASS" if len(tue) == 0 else "FAIL",
        "parity_atr_note": (
            "Engine ATR max gates entries; atr>max on tape is diagnostic. "
            "Do not re-gate Tue/ATR in L2det."
        ),
        "atr_gt_max_sample": [
            {
                "open_time": str(r.open_time),
                "atr": float(r.atr_pts),
                "win": int(r.win),
                "window": r.window,
            }
            for r in atr_over.head(10).itertuples()
        ],
    }


def eval_policies(base: pd.DataFrame, policies: dict[str, pd.Series]) -> dict:
    base_m = metrics(base, "baseline")
    out = {"baseline": base_m, "policies": {}}
    for name, mask in policies.items():
        mask_np = mask.to_numpy()
        if mask_np.sum() == 0:
            out["policies"][name] = {
                "skips_n": 0,
                "verdict": "N/A_EMPTY",
                "note": "no matching fires in window",
            }
            continue
        rep = skip_report(base, mask_np)
        out["policies"][name] = {
            **rep,
            "verdict": verdict(base_m, rep),
        }
    return out


def size_table_spec() -> dict:
    return {
        "task": "DE40-AOS-P2-T05",
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


def train_l2ai(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    """Train on YTD∖tip months (Jan–Apr) + soft; OOS on tip. Fallback: tip chronological holdout."""
    ytd_only = ytd[~ytd["open_time"].isin(set(tip["open_time"]))].copy()
    # Prefer pre-tip months as train
    train = ytd[ytd["month"].isin(["2026-01", "2026-02", "2026-03", "2026-04"])].copy()
    if len(train) < 20:
        train = ytd_only if len(ytd_only) >= 20 else tip.iloc[: int(0.7 * len(tip))].copy()
        test = tip if train is not tip.iloc[: int(0.7 * len(tip))] else tip.iloc[int(0.7 * len(tip)) :]
    else:
        test = tip.copy()

    for col in FEATS:
        if col not in train.columns:
            train[col] = 0
            test[col] = 0

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
    for thr in np.arange(0.50, 0.90, 0.05):
        # Map tip rows: need proba on tip
        Xt = scaler.transform(tip[FEATS].fillna(0).to_numpy())
        p_tip = clf.predict_proba(Xt)[:, 1]
        mask = p_tip >= thr
        if mask.sum() == 0:
            continue
        rep = skip_report(tip, mask)
        v = verdict(tip_base, rep)
        cand = {
            "thr": round(float(thr), 2),
            "verdict": v,
            "delta_E_N": rep["delta_E_N"],
            "precision_vs_losers": rep["precision_vs_losers"],
            "fire_retention_pct": rep["fire_retention_pct"],
            "skips_n": rep["skips_n"],
            "false_skip_aug_winners": rep["false_skip_aug_winners"],
            "false_skip_sell_winners": rep["false_skip_sell_winners"],
        }
        if best is None or (
            (cand["delta_E_N"] or -9) > (best["delta_E_N"] or -9)
            and cand["verdict"] in ("ARM_SOFT", "HOLD_SOFT")
        ):
            best = cand
        if best is None:
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
        "pin": "L2skip_de40",
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
        "task": "DE40-AOS-P2-T06",
        "meta": meta,
        "best_thr_on_tip": best,
        "arm_status": arm,
        "note": "DISARM if tip AUC < 0.55 or no thr clears protect cells / iteration bar",
    }


def stack_cf(tip: pd.DataFrame, ai: dict) -> dict:
    tip_base = metrics(tip, "P0")
    stacks = {
        "P0_engine": np.zeros(len(tip), dtype=bool),
        "L2det_H13": (tip["is_h13"] == 1).to_numpy(),
        "L2det_BUY_near_atr": ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1)).to_numpy(),
        "L2det_MISMATCH_not_May": (
            (tip["is_mismatch"] == 1) & (tip["is_may"] == 0)
        ).to_numpy(),
        "L2det_FRAGILE_and_near_atr": (
            (tip["is_fragile"] == 1) & (tip["near_atr_cap"] == 1)
        ).to_numpy(),
        "L2det_v1b_H13_OR_BUY_near_atr": (
            (tip["is_h13"] == 1)
            | ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1))
        ).to_numpy(),
        "L2det_v1c_H13_OR_FRAGILE_near_atr": (
            (tip["is_h13"] == 1)
            | ((tip["is_fragile"] == 1) & (tip["near_atr_cap"] == 1))
        ).to_numpy(),
    }

    # AI overlay if model exists
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
            stacks["L2det_v1b_OR_L2AI"] = stacks["L2det_v1b_H13_OR_BUY_near_atr"] | (
                p >= thr
            )

    out = {"baseline": tip_base, "stacks": {}}
    for name, mask in stacks.items():
        if name == "P0_engine":
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
    tip = load("de40_tip_fire_tape_v0.csv")
    ytd = load("de40_ytd_fire_tape_v0.csv")

    # --- T01 parity ---
    par = parity(tip, ytd)

    # --- T02 tip maps ---
    t02_tip = eval_policies(
        tip,
        {
            "skip_H13": tip["is_h13"] == 1,
            "skip_Feb": tip["is_feb"] == 1,  # empty on tip
            "skip_H13_OR_Feb": (tip["is_h13"] == 1) | (tip["is_feb"] == 1),
            "skip_Wed": tip["is_wed"] == 1,
        },
    )
    t02_ytd = eval_policies(
        ytd,
        {
            "skip_Feb": ytd["is_feb"] == 1,
            "skip_H13": ytd["is_h13"] == 1,
            "skip_Feb_OR_H13": (ytd["is_feb"] == 1) | (ytd["is_h13"] == 1),
            "skip_Mar": ytd["is_mar"] == 1,
        },
    )

    # --- T03 buy-caution ---
    t03 = eval_policies(
        tip,
        {
            "skip_BUY": tip["side_buy"] == 1,
            "skip_BUY_if_H13": (tip["side_buy"] == 1) & (tip["is_h13"] == 1),
            "skip_BUY_if_near_atr": (tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1),
            "skip_BUY_if_fragile": (tip["side_buy"] == 1) & (tip["is_fragile"] == 1),
        },
    )

    # --- T04 mismatch / fragile ---
    t04 = eval_policies(
        tip,
        {
            "skip_MISMATCH_all": tip["is_mismatch"] == 1,
            "skip_MISMATCH_not_May": (tip["is_mismatch"] == 1) & (tip["is_may"] == 0),
            "skip_FRAGILE_all": tip["is_fragile"] == 1,
            "skip_near_atr_cap": tip["near_atr_cap"] == 1,
            "skip_FRAGILE_and_near_atr": (tip["is_fragile"] == 1)
            & (tip["near_atr_cap"] == 1),
            "skip_Sep_Oct": tip["month"].isin(["2026-09", "2026-10"]),
        },
    )

    t05 = size_table_spec()
    t06 = train_l2ai(tip, ytd)
    t07 = stack_cf(tip, t06)

    # Preferred armed set (post-hoc selection from CF)
    preferred = []
    for name, pol in {**t02_tip["policies"], **t03["policies"], **t04["policies"]}.items():
        if pol.get("verdict") == "ARM_SOFT":
            preferred.append(name)
    for name, st in t07["stacks"].items():
        if st.get("verdict") == "ARM_SOFT":
            preferred.append(name)

    packet = {
        "task": "DE40-AOS-P2",
        "dated": datetime.now(timezone.utc).isoformat(),
        "compare_window": "tip 2026.05.01-2026.10.18",
        "Leak_prior_pp": LEAK_PRIOR * 100,
        "Leak_proxy_pp": LEAK_PROXY * 100,
        "Leak_source_authority": "prior_9.8pp_until_deals",
        "P2_T01_parity": par,
        "P2_T02_tip": t02_tip,
        "P2_T02_ytd": t02_ytd,
        "P2_T03_buy_caution": t03,
        "P2_T04_regime": t04,
        "P2_T05_size_table": t05,
        "P2_T06_L2AI": t06,
        "P2_T07_stacks": t07,
        "preferred_ARM_SOFT_candidates": preferred,
    }
    (OUT / "P2_CF.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")

    # Console summary
    print("T01 parity", par["parity_tue"], "atr>max", par["fires_with_atr_gt_max"])
    print("--- T02 tip ---")
    for k, v in t02_tip["policies"].items():
        print(k, v.get("verdict"), "dEN", v.get("delta_E_N"), "ret", v.get("fire_retention_pct"))
    print("--- T02 ytd Feb ---")
    for k, v in t02_ytd["policies"].items():
        if "Feb" in k or k == "skip_Mar":
            print(k, v.get("verdict"), "dEN", v.get("delta_E_N"), "ret", v.get("fire_retention_pct"))
    print("--- T03 ---")
    for k, v in t03["policies"].items():
        print(k, v.get("verdict"), "dEN", v.get("delta_E_N"), "ret", v.get("fire_retention_pct"))
    print("--- T04 ---")
    for k, v in t04["policies"].items():
        print(k, v.get("verdict"), "dEN", v.get("delta_E_N"), "ret", v.get("fire_retention_pct"))
    print("--- T06 ---", t06["arm_status"], "AUC", t06["meta"]["tip_oos_auc"])
    print("--- T07 stacks ---")
    for k, v in t07["stacks"].items():
        print(k, v.get("verdict"), "dEN", v.get("delta_E_N"), "ret", v.get("fire_retention_pct"))
    print("ARM_SOFT candidates:", preferred)


if __name__ == "__main__":
    main()
