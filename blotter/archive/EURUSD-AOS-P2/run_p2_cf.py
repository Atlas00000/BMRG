"""EURUSD-AOS-P2-T01..T07 — parity, L2det shadow CF, size spec, L2skip_eur_m15 train+stack."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\EURUSD\tapes"
)
OUT = Path(__file__).resolve().parent
MODELS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\infra\artefacts\models\L2skip_eur_m15"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.011852  # journal 2x spread tip (COST_PROXY)
ATR_MAX = 74.0

TIP_WIN = "2026.05.01-2026.10.17"
YTD_WIN = "2026.01.01-2026.10.17"

FEATS = [
    "side_buy",
    "is_thu",
    "is_h13",
    "is_h19",
    "is_aug",
    "is_feb",
    "near_atr_cap",
    "hour",
    "atr_z",
    "is_mon",
    "is_fri",
    "is_jul",
]


def load() -> pd.DataFrame:
    tip = pd.read_csv(TAPES / "eurusd_m15_tip_fire_tape_v0.csv")
    ytd = pd.read_csv(TAPES / "eurusd_m15_ytd_fire_tape_v0.csv")
    tip["split"] = "tip"
    ytd["split"] = "ytd"
    # Prefer tip rows for overlapping opens when building combined train set
    df = pd.concat([tip, ytd], ignore_index=True)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["y_lose"] = 1 - df["win"].astype(int)
    df["side_buy"] = (df["side"] == "BUY").astype(int)
    df["is_thu"] = df["cell_dow_thu"].astype(int)
    df["is_h13"] = df["cell_hour_13"].astype(int)
    df["is_h19"] = df["cell_hour_19"].astype(int)
    df["is_aug"] = df["cell_month_aug"].astype(int)
    df["is_feb"] = df["cell_month_feb"].astype(int)
    df["is_jul"] = (df["month"] == "2026-07").astype(int)
    df["near_atr_cap"] = df["near_atr_cap"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    atr = df["atr_pts"].astype(float)
    df["atr_z"] = (atr - atr.mean()) / (atr.std() + 1e-9)
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    return df.sort_values("open_dt").reset_index(drop=True)


def metrics(sub: pd.DataFrame, label: str) -> dict:
    n = len(sub)
    if n == 0:
        return {"label": label, "n": 0}
    wr = float(sub["win"].mean())
    bm = wr - BWR
    en = wr * (R + 1) - 1
    ef = bm - LEAK
    return {
        "label": label,
        "n": int(n),
        "WR": round(wr * 100, 2),
        "E_N": round(en, 4),
        "EF_proxy_pp": round(ef * 100, 3),
        "avgR": round(float(sub["pnl_R"].mean()), 4),
    }


def skip_report(base: pd.DataFrame, mask_skip: np.ndarray) -> dict:
    skipped = base.loc[mask_skip]
    kept = base.loc[~mask_skip]
    n_skip = int(mask_skip.sum())
    losers_base = int((base["win"] == 0).sum())
    losers_skip = int((skipped["win"] == 0).sum()) if n_skip else 0
    # protect cells: Mon/Fri winners, SELL winners, H12 winners, Jul winners
    monfri_w = (
        int(
            (
                ((skipped["dow"] == "Mon") | (skipped["dow"] == "Fri"))
                & (skipped["win"] == 1)
            ).sum()
        )
        if n_skip
        else 0
    )
    sell_w = int(((skipped["side"] == "SELL") & (skipped["win"] == 1)).sum()) if n_skip else 0
    h12_w = int(((skipped["hour"] == 12) & (skipped["win"] == 1)).sum()) if n_skip else 0
    jul_w = int(((skipped["month"] == "2026-07") & (skipped["win"] == 1)).sum()) if n_skip else 0
    return {
        "skips_n": n_skip,
        "precision_vs_losers": round(losers_skip / n_skip, 4) if n_skip else None,
        "recall_losers": round(losers_skip / losers_base, 4) if losers_base else None,
        "false_skip_winners": int((skipped["win"] == 1).sum()) if n_skip else 0,
        "false_skip_monfri_winners": monfri_w,
        "false_skip_sell_winners": sell_w,
        "false_skip_h12_winners": h12_w,
        "false_skip_jul_winners": jul_w,
        "kept": metrics(kept, "kept"),
        "delta_E_N": round(metrics(kept, "k")["E_N"] - metrics(base, "b")["E_N"], 4)
        if len(kept)
        else None,
        "delta_EF_pp": round(
            metrics(kept, "k")["EF_proxy_pp"] - metrics(base, "b")["EF_proxy_pp"], 3
        )
        if len(kept)
        else None,
        "fire_retention_pct": round(100.0 * len(kept) / len(base), 1) if len(base) else 0,
    }


def verdict(base_m: dict, rep: dict) -> str:
    k = rep["kept"]
    if k["n"] == 0:
        return "REJECT"
    if k["n"] / base_m["n"] < 0.50:
        return "REJECT_FREQUENCY_STALL"
    if k["WR"] > base_m["WR"] and k["E_N"] < base_m["E_N"] - 1e-9:
        return "REJECT"
    ef_ok = k["EF_proxy_pp"] >= base_m["EF_proxy_pp"] - 1.0
    en_up = k["E_N"] > base_m["E_N"] + 1e-9
    prec = rep["precision_vs_losers"] or 0
    # heavy collateral on protect cells → HOLD not ARM
    collateral = (
        (rep["false_skip_sell_winners"] or 0)
        + (rep["false_skip_monfri_winners"] or 0)
        + (rep["false_skip_jul_winners"] or 0)
    )
    if en_up and ef_ok and prec >= 0.55 and rep["skips_n"] > 0:
        if collateral >= 3:
            return "HOLD_SOFT"
        return "ARM_SOFT"
    if ef_ok and (k["E_N"] >= base_m["E_N"] - 1e-9) and rep["skips_n"] > 0:
        return "HOLD_SOFT"
    if not ef_ok and not en_up:
        return "DISARM"
    return "DISARM"


def parity(tip: pd.DataFrame, ytd: pd.DataFrame) -> dict:
    both = pd.concat([tip, ytd], ignore_index=True)
    tue = both[both["dow"] == "Tue"]
    atr_over = both[both["atr_pts"].astype(float) > ATR_MAX]
    return {
        "task": "EURUSD-AOS-P2-T01",
        "tue_fires": int(len(tue)),
        "fires_with_atr_gt_max": int(len(atr_over)),
        "near_atr_cap_fires_tip": int(tip["near_atr_cap"].sum()),
        "parity_tue": "PASS" if len(tue) == 0 else "FAIL",
        "parity_atr": "PASS" if len(atr_over) == 0 else "WARN_DIAG",
        "note": "Do not re-gate Tue/ATR in L2det — engine already filters.",
    }


def run_policies(base: pd.DataFrame, policies: dict) -> dict:
    base_m = metrics(base, "baseline")
    out = {"baseline": base_m, "policies": {}}
    for name, mask in policies.items():
        mask = np.asarray(mask)
        if mask.sum() == 0:
            out["policies"][name] = {
                "skips_n": 0,
                "verdict": "N/A_EMPTY",
                "note": "no fires",
            }
            continue
        rep = skip_report(base, mask)
        rep["verdict"] = verdict(base_m, rep)
        out["policies"][name] = rep
    return out


def size_table_spec(tip: pd.DataFrame) -> dict:
    wins = tip["win"].to_numpy()
    ens = []
    for i in range(len(tip)):
        if i < 14:
            ens.append(None)
            continue
        w = wins[i - 14 : i + 1]
        ens.append(float(w.mean() * (R + 1) - 1))
    return {
        "task": "EURUSD-AOS-P2-T05",
        "status": "SPEC_ONLY",
        "note": "Wire after L4 health bus; do not size-live yet",
        "f_declared_baseline": 0.005,
        "table": [
            {"state": "Expanding", "cond": "W15 E_N > baseline and rising", "f_mult": 1.0},
            {"state": "Stable", "cond": "W15 E_N >= 0 and |Δ| small", "f_mult": 1.0},
            {
                "state": "Compressing",
                "cond": "W15 E_N falling 2 evals or Fragile EF",
                "f_mult": 0.5,
            },
            {
                "state": "Near frontier",
                "cond": "EF_proxy <= 1 pp or W15 E_N < 0",
                "f_mult": 0.25,
            },
            {
                "state": "Below frontier",
                "cond": "W20 E_N <= 0 and tip EF_proxy <= 0",
                "f_mult": 0.0,
            },
            {
                "state": "L2det WOULD_SKIP",
                "cond": "Armed det map hit",
                "f_mult": 0.0,
                "note": "skip outranks size",
            },
        ],
        "w15_E_N_tail": [round(x, 4) if x is not None else None for x in ens[-10:]],
    }


def train_l2skip(tip: pd.DataFrame, ytd: pd.DataFrame) -> tuple[dict, pd.DataFrame, tuple | None]:
    """Train on YTD-only non-tip months (Jan–Apr) + optional; OOS = tip."""
    # Pre-tip months from YTD for train (Jan–Apr); tip is OOS
    pre = ytd[ytd["month"].isin(["2026-01", "2026-02", "2026-03", "2026-04"])].copy()
    # If too thin, train on YTD excluding tip months May+ and score tip
    if len(pre) < 20:
        pre = ytd[~ytd["month"].isin(["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"])].copy()
    if len(pre) < 15:
        # fallback: chronological first 40% of YTD unique opens
        ytd_u = ytd.drop_duplicates(subset=["open_time", "side"], keep="first")
        cut = max(15, int(len(ytd_u) * 0.4))
        pre = ytd_u.iloc[:cut].copy()

    X_tr = pre[FEATS].to_numpy(dtype=float)
    y_tr = pre["y_lose"].to_numpy(dtype=int)
    X_te = tip[FEATS].to_numpy(dtype=float)
    y_te = tip["y_lose"].to_numpy(dtype=int)

    scaler = StandardScaler()
    X_trs = scaler.fit_transform(X_tr)
    X_tes = scaler.transform(X_te)

    clf = LogisticRegression(
        class_weight="balanced", C=0.5, max_iter=500, solver="lbfgs"
    )
    clf.fit(X_trs, y_tr)
    proba_te = clf.predict_proba(X_tes)[:, 1]
    try:
        auc = float(roc_auc_score(y_te, proba_te))
    except ValueError:
        auc = float("nan")

    base_m = metrics(tip, "baseline_tip")
    rows = []
    best = None
    for thr in np.arange(0.45, 0.85, 0.025):
        mask = proba_te >= thr
        if mask.sum() == 0 or mask.sum() == len(tip):
            continue
        rep = skip_report(tip, mask)
        v = verdict(base_m, rep)
        row = {
            "thr": round(float(thr), 3),
            "verdict": v,
            "skips_n": rep["skips_n"],
            "precision_vs_losers": rep["precision_vs_losers"],
            "fire_retention_pct": rep["fire_retention_pct"],
            "kept_E_N": rep["kept"]["E_N"],
            "delta_E_N": rep["delta_E_N"],
            "delta_EF_pp": rep["delta_EF_pp"],
            "false_skip_sell_winners": rep["false_skip_sell_winners"],
            "false_skip_monfri_winners": rep["false_skip_monfri_winners"],
        }
        rows.append(row)
        score = (
            v == "ARM_SOFT",
            rep["delta_E_N"] or -9,
            rep["precision_vs_losers"] or 0,
            -(rep["false_skip_sell_winners"] or 0),
            -(rep["false_skip_monfri_winners"] or 0),
            rep["fire_retention_pct"],
        )
        if best is None or score > best[0]:
            best = (score, row, mask, float(thr))

    # chrono holdout inside tip
    tip_sorted = tip.sort_values("open_dt")
    cut = int(len(tip_sorted) * 0.6)
    train_ch = pd.concat([pre, tip_sorted.iloc[:cut]], ignore_index=True)
    test_ch = tip_sorted.iloc[cut:].copy()
    scaler2 = StandardScaler()
    Xc = scaler2.fit_transform(train_ch[FEATS].to_numpy(float))
    yc = train_ch["y_lose"].to_numpy(int)
    clf2 = LogisticRegression(
        class_weight="balanced", C=0.5, max_iter=500, solver="lbfgs"
    )
    clf2.fit(Xc, yc)
    p2 = clf2.predict_proba(scaler2.transform(test_ch[FEATS].to_numpy(float)))[:, 1]
    thr_ch = best[3] if best else 0.55
    mask2 = p2 >= thr_ch
    rep_ch = skip_report(test_ch, mask2)
    base_ch = metrics(test_ch, "tip_holdout")
    rep_ch["verdict"] = verdict(base_ch, rep_ch)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semver = f"L2skip_eur_m15_p_pretip_{ts}"
    run_dir = MODELS / semver
    run_dir.mkdir(parents=True, exist_ok=True)
    latest = MODELS / "LATEST"
    latest.mkdir(parents=True, exist_ok=True)

    bundle = {
        "scaler": scaler,
        "clf": clf,
        "feats": FEATS,
        "thr": best[3] if best else 0.55,
        "train_window": "pre_tip_2026.01-04",
        "semver": semver,
    }
    joblib.dump(bundle, run_dir / "model.joblib")
    joblib.dump(bundle, latest / "model.joblib")

    tip_scored = tip.copy()
    tip_scored["p_lose"] = proba_te
    tip_scored["would_skip"] = (
        (proba_te >= (best[3] if best else 0.55)).astype(int) if best else 0
    )
    tip_scored.to_csv(OUT / "tip_l2ai_scored.csv", index=False)

    meta = {
        "semver": semver,
        "algo": "LogisticRegression balanced C=0.5 + StandardScaler",
        "feats": FEATS,
        "train_n": int(len(pre)),
        "test_n": int(len(tip)),
        "auc_tip_oos": auc,
        "thr_selected_on_tip": best[3] if best else None,
        "thr_selection_note": (
            "Threshold swept on tip for shadow CF; weights fit on pre-tip only. "
            "SHADOW_ONLY — not production-ready."
        ),
        "best_row": best[1] if best else None,
        "sweep": rows,
        "chrono_holdout": {
            "train_n": int(len(train_ch)),
            "test_n": int(len(test_ch)),
            "thr": thr_ch,
            "report": rep_ch,
            "baseline_holdout": base_ch,
        },
    }
    (run_dir / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (latest / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (latest / "META.json").write_text(
        json.dumps(
            {
                "semver": semver,
                "mode": "SHADOW_ONLY",
                "symbol": "EURUSD",
                "tf": "M15",
                "magic_engine": 26101817,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (latest / "PIN.json").write_text(
        json.dumps({"semver": semver, "mode": "SHADOW_ONLY"}, indent=2), encoding="utf-8"
    )
    return meta, tip_scored, best


def stack_cf(tip: pd.DataFrame, tip_scored: pd.DataFrame, thr: float, armed_det) -> dict:
    base_m = metrics(tip, "baseline")
    tip = tip.reset_index(drop=True)
    tip_scored = tip_scored.reset_index(drop=True)
    ai = tip_scored["p_lose"].to_numpy() >= thr
    det = armed_det(tip)

    configs = {
        "P0_engine": np.zeros(len(tip), dtype=bool),
        "L2det_primary": det,
        "L2AI_only": ai,
        "L2det_OR_L2AI": det | ai,
        "L2det_AND_L2AI": det & ai,
    }
    out = {"baseline": base_m, "stacks": {}}
    for name, mask in configs.items():
        if name == "P0_engine":
            out["stacks"][name] = {
                "kept": base_m,
                "skips_n": 0,
                "delta_E_N": 0.0,
                "verdict": "BASELINE",
            }
            continue
        rep = skip_report(tip, mask)
        rep["verdict"] = verdict(base_m, rep)
        out["stacks"][name] = rep
    return out


def main() -> None:
    df = load()
    tip = df[df["split"] == "tip"].copy().reset_index(drop=True)
    ytd = df[df["split"] == "ytd"].copy().reset_index(drop=True)

    # --- T01 parity ---
    par = parity(tip, ytd)

    # --- T02 hour/DOW maps ---
    t02 = run_policies(
        tip,
        {
            "skip_Thu": tip["is_thu"] == 1,
            "skip_H13": tip["is_h13"] == 1,
            "skip_H19": tip["is_h19"] == 1,
            "skip_Thu_OR_H13": (tip["is_thu"] == 1) | (tip["is_h13"] == 1),
            "skip_Thu_OR_H19": (tip["is_thu"] == 1) | (tip["is_h19"] == 1),
            "skip_H13_OR_H19": (tip["is_h13"] == 1) | (tip["is_h19"] == 1),
            "skip_Thu_OR_H13_OR_H19": (tip["is_thu"] == 1)
            | (tip["is_h13"] == 1)
            | (tip["is_h19"] == 1),
        },
    )

    # --- T03 buy-caution ---
    t03 = run_policies(
        tip,
        {
            "skip_BUY": tip["side_buy"] == 1,
            "skip_BUY_if_Thu": (tip["side_buy"] == 1) & (tip["is_thu"] == 1),
            "skip_BUY_if_H13": (tip["side_buy"] == 1) & (tip["is_h13"] == 1),
            "skip_BUY_if_near_atr": (tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1),
            "skip_BUY_if_H19": (tip["side_buy"] == 1) & (tip["is_h19"] == 1),
        },
    )

    # --- T04 stress ---
    t04 = run_policies(
        tip,
        {
            "skip_Aug": tip["is_aug"] == 1,
            "skip_near_atr_cap": tip["near_atr_cap"] == 1,
            "skip_Feb_on_tip": tip["is_feb"] == 1,  # empty on tip
        },
    )
    # YTD Feb diagnostic
    t04_ytd = run_policies(
        ytd,
        {
            "skip_Feb": ytd["is_feb"] == 1,
            "skip_Aug": ytd["is_aug"] == 1,
            "skip_BUY": ytd["side_buy"] == 1,
            "skip_Thu": ytd["is_thu"] == 1,
        },
    )

    # Candidate stacks for preferred det map
    stacks_det = run_policies(
        tip,
        {
            "skip_Thu_PLUS_BUY_near_atr": (tip["is_thu"] == 1)
            | ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1)),
            "skip_Thu_PLUS_BUY_H13": (tip["is_thu"] == 1)
            | ((tip["side_buy"] == 1) & (tip["is_h13"] == 1)),
            "skip_Thu_OR_H13_PLUS_BUY_near_atr": (tip["is_thu"] == 1)
            | (tip["is_h13"] == 1)
            | ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1)),
            "skip_BUY_near_atr_PLUS_Aug": (
                ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1))
                | (tip["is_aug"] == 1)
            ),
        },
    )

    size_spec = size_table_spec(tip)
    meta, tip_scored, best = train_l2skip(tip, ytd)
    thr = best[3] if best else 0.55

    # Choose primary det mask from CF (prefer ARM_SOFT with best ΔE_N, low collateral)
    candidates = []
    for block in (t02, t03, t04, stacks_det):
        for name, v in block["policies"].items():
            if not isinstance(v, dict) or v.get("delta_E_N") is None:
                continue
            if v.get("verdict") not in ("ARM_SOFT", "HOLD_SOFT"):
                continue
            candidates.append((name, v))

    def cand_key(kv):
        name, v = kv
        return (
            v.get("verdict") == "ARM_SOFT",
            v.get("delta_E_N") or -9,
            v.get("precision_vs_losers") or 0,
            -(v.get("false_skip_sell_winners") or 0),
            v.get("fire_retention_pct") or 0,
        )

    preferred = max(candidates, key=cand_key) if candidates else None

    # Build armed_det lambda from preferred name
    def make_det(name: str):
        mapping = {
            "skip_Thu": lambda t: (t["is_thu"] == 1).to_numpy(),
            "skip_H13": lambda t: (t["is_h13"] == 1).to_numpy(),
            "skip_H19": lambda t: (t["is_h19"] == 1).to_numpy(),
            "skip_Thu_OR_H13": lambda t: ((t["is_thu"] == 1) | (t["is_h13"] == 1)).to_numpy(),
            "skip_Thu_OR_H19": lambda t: ((t["is_thu"] == 1) | (t["is_h19"] == 1)).to_numpy(),
            "skip_H13_OR_H19": lambda t: ((t["is_h13"] == 1) | (t["is_h19"] == 1)).to_numpy(),
            "skip_Thu_OR_H13_OR_H19": lambda t: (
                (t["is_thu"] == 1) | (t["is_h13"] == 1) | (t["is_h19"] == 1)
            ).to_numpy(),
            "skip_BUY": lambda t: (t["side_buy"] == 1).to_numpy(),
            "skip_BUY_if_Thu": lambda t: (
                (t["side_buy"] == 1) & (t["is_thu"] == 1)
            ).to_numpy(),
            "skip_BUY_if_H13": lambda t: (
                (t["side_buy"] == 1) & (t["is_h13"] == 1)
            ).to_numpy(),
            "skip_BUY_if_near_atr": lambda t: (
                (t["side_buy"] == 1) & (t["near_atr_cap"] == 1)
            ).to_numpy(),
            "skip_BUY_if_H19": lambda t: (
                (t["side_buy"] == 1) & (t["is_h19"] == 1)
            ).to_numpy(),
            "skip_Aug": lambda t: (t["is_aug"] == 1).to_numpy(),
            "skip_near_atr_cap": lambda t: (t["near_atr_cap"] == 1).to_numpy(),
            "skip_Thu_PLUS_BUY_near_atr": lambda t: (
                (t["is_thu"] == 1)
                | ((t["side_buy"] == 1) & (t["near_atr_cap"] == 1))
            ).to_numpy(),
            "skip_Thu_PLUS_BUY_H13": lambda t: (
                (t["is_thu"] == 1) | ((t["side_buy"] == 1) & (t["is_h13"] == 1))
            ).to_numpy(),
            "skip_Thu_OR_H13_PLUS_BUY_near_atr": lambda t: (
                (t["is_thu"] == 1)
                | (t["is_h13"] == 1)
                | ((t["side_buy"] == 1) & (t["near_atr_cap"] == 1))
            ).to_numpy(),
            "skip_BUY_near_atr_PLUS_Aug": lambda t: (
                ((t["side_buy"] == 1) & (t["near_atr_cap"] == 1)) | (t["is_aug"] == 1)
            ).to_numpy(),
        }
        return mapping.get(name, lambda t: np.zeros(len(t), dtype=bool))

    pref_name = preferred[0] if preferred else "skip_Thu"
    stacks = stack_cf(tip, tip_scored, thr, make_det(pref_name))

    # Arm summary helpers
    def summarize_block(block: dict) -> dict:
        return {
            k: {
                "verdict": v.get("verdict"),
                "delta_E_N": v.get("delta_E_N"),
                "retention": v.get("fire_retention_pct"),
                "prec": v.get("precision_vs_losers"),
                "skips": v.get("skips_n"),
                "sell_FP": v.get("false_skip_sell_winners"),
                "monfri_FP": v.get("false_skip_monfri_winners"),
                "kept_E_N": (v.get("kept") or {}).get("E_N"),
            }
            for k, v in block["policies"].items()
            if isinstance(v, dict)
        }

    report = {
        "task": "EURUSD-AOS-P2",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "Leak_source": "journal_2x_entry_spread_median",
        "Leak_proxy_pp": LEAK * 100,
        "P2_T01_parity": par,
        "P2_T02_dow_hour": t02,
        "P2_T03_buy_caution": t03,
        "P2_T04_stress_tip": t04,
        "P2_T04_ytd_diag": t04_ytd,
        "P2_T02_T04_stacks": stacks_det,
        "P2_T05_size_table": size_spec,
        "P2_T06_L2skip_eur_m15": {
            "semver": meta["semver"],
            "auc_tip_oos": meta["auc_tip_oos"],
            "thr": meta["thr_selected_on_tip"],
            "best_row": meta["best_row"],
            "chrono_holdout": meta["chrono_holdout"],
            "model_dir": str(MODELS / meta["semver"]),
        },
        "P2_T07_stack_cf": stacks,
        "preferred_det": {
            "name": pref_name,
            "cf": preferred[1] if preferred else None,
        },
        "summaries": {
            "T02": summarize_block(t02),
            "T03": summarize_block(t03),
            "T04": summarize_block(t04),
            "stacks_det": summarize_block(stacks_det),
            "T07": {
                k: {
                    "verdict": v.get("verdict"),
                    "delta_E_N": v.get("delta_E_N"),
                    "kept_E_N": (v.get("kept") or {}).get("E_N"),
                    "retention": v.get("fire_retention_pct"),
                    "prec": v.get("precision_vs_losers"),
                }
                for k, v in stacks["stacks"].items()
            },
        },
    }
    (OUT / "P2_CF.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "parity": par,
                "preferred_det": report["preferred_det"]["name"],
                "summaries": report["summaries"],
                "l2ai": {
                    "auc": meta["auc_tip_oos"],
                    "best": meta["best_row"],
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
