"""EURUSD M15 L2skip train loop — pre-tip fit · tip OOS · store under L2skip_eur_m15/.

Does NOT arm LIVE_WITHHOLD. Writes SHADOW_ONLY pins only.
Promote to CHALLENGER requires aos_l5_retrain.md gates (HITL).

Usage:
  python infra/src/train/train_l2_eurusd_m15.py
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

BMRG = Path(__file__).resolve().parents[3]
TAPES = BMRG / "doc" / "assets" / "EURUSD" / "tapes"
MODELS = BMRG / "infra" / "artefacts" / "models" / "L2skip_eur_m15"
P2_OUT = BMRG / "blotter" / "archive" / "EURUSD-AOS-P2"

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.011852  # journal proxy until measured

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


def _featurize(df: pd.DataFrame, atr_mu: float, atr_sd: float) -> pd.DataFrame:
    d = df.copy()
    d["open_dt"] = pd.to_datetime(d["open_time"], format="%Y.%m.%d %H:%M:%S")
    d["win"] = d["win"].astype(int)
    d["y_lose"] = 1 - d["win"]
    d["side_buy"] = (d["side"] == "BUY").astype(int)
    d["is_thu"] = d["cell_dow_thu"].astype(int)
    d["is_h13"] = d["cell_hour_13"].astype(int)
    d["is_h19"] = d["cell_hour_19"].astype(int)
    d["is_aug"] = d["cell_month_aug"].astype(int)
    d["is_feb"] = d["cell_month_feb"].astype(int)
    d["is_jul"] = (d["month"] == "2026-07").astype(int)
    d["near_atr_cap"] = d["near_atr_cap"].astype(int)
    d["hour"] = d["hour"].astype(int)
    d["is_mon"] = (d["dow"] == "Mon").astype(int)
    d["is_fri"] = (d["dow"] == "Fri").astype(int)
    sd = atr_sd if atr_sd > 1e-9 else 1.0
    d["atr_z"] = (d["atr_pts"].astype(float) - atr_mu) / sd
    d["pnl_R"] = d["pnl_R_design"].astype(float)
    return d


def _load() -> tuple[pd.DataFrame, pd.DataFrame]:
    tip_raw = pd.read_csv(TAPES / "eurusd_m15_tip_fire_tape_v0.csv")
    ytd_raw = pd.read_csv(TAPES / "eurusd_m15_ytd_fire_tape_v0.csv")
    atr = pd.concat([tip_raw["atr_pts"], ytd_raw["atr_pts"]]).astype(float)
    atr_mu, atr_sd = float(atr.mean()), float(atr.std(ddof=0))
    tip = _featurize(tip_raw, atr_mu, atr_sd).sort_values("open_dt").reset_index(drop=True)
    ytd = _featurize(ytd_raw, atr_mu, atr_sd).sort_values("open_dt").reset_index(drop=True)
    # Pre-tip = YTD fires strictly before tip window start
    tip_start = tip["open_dt"].min()
    pre = ytd[ytd["open_dt"] < tip_start].copy().reset_index(drop=True)
    return pre, tip


def _book(df: pd.DataFrame) -> dict:
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


def _cf(tip: pd.DataFrame, mask: np.ndarray) -> dict:
    skips = tip.loc[mask]
    kept = tip.loc[~mask]
    base = _book(tip)
    kept_m = _book(kept)
    prec = float((1 - skips["win"]).mean()) if len(skips) else None
    sell_fp = (
        int(((skips["side"] == "SELL") & (skips["win"] == 1)).sum()) if len(skips) else 0
    )
    monfri_fp = (
        int(
            (
                ((skips["is_mon"] == 1) | (skips["is_fri"] == 1)) & (skips["win"] == 1)
            ).sum()
        )
        if len(skips)
        else 0
    )
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
    ret = 100.0 * len(kept) / len(tip) if len(tip) else 0.0
    # promote gates — see aos_l5_retrain.md (EURUSD collateral = SELL / MonFri)
    verdict = "DISARM"
    if mask.sum() == 0:
        verdict = "DISARM"
    elif ret < 50.0:
        verdict = "REJECT_FREQUENCY_STALL"
    elif (
        d_en is not None
        and d_en > 0
        and (prec or 0) >= 0.55
        and sell_fp <= 1
        and monfri_fp <= 1
    ):
        verdict = "SHADOW_CANDIDATE"
    elif d_en is not None and d_en > 0:
        verdict = "HOLD_SHADOW"
    return {
        "skips_n": int(mask.sum()),
        "precision_vs_losers": None if prec is None else round(prec, 4),
        "fire_retention_pct": round(ret, 1),
        "kept": kept_m,
        "baseline": base,
        "delta_E_N": d_en,
        "delta_EF_pp": d_ef,
        "false_skip_sell_winners": sell_fp,
        "false_skip_monfri_winners": monfri_fp,
        "verdict": verdict,
    }


def _write_pin(latest: Path, semver: str, mode: str, role: str, metrics: dict) -> None:
    pin = {
        "semver": semver,
        "mode": mode,
        "role": role,
        "overlay_champ": "L2det_eur_m15_v1b",
        "ai_champ": None,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "auc_tip_oos": metrics.get("auc_tip_oos"),
        "best_verdict": (metrics.get("best_row") or {}).get("verdict"),
        "chrono_holdout_verdict": (
            (metrics.get("chrono_holdout") or {}).get("report") or {}
        ).get("verdict"),
    }
    (latest / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    (latest / "META.json").write_text(
        json.dumps(
            {
                "semver": semver,
                "mode": mode,
                "role": role,
                "symbol": "EURUSD",
                "tf": "M15",
                "magic_engine": 26101817,
                "mqh_exported": False,
                "live_withhold": False,
                "policy": "doc/assets/EURUSD/aos_l5_retrain.md",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    pre, tip = _load()
    X_tr = pre[FEATS].to_numpy(float)
    y_tr = pre["y_lose"].to_numpy(int)
    X_te = tip[FEATS].to_numpy(float)
    y_te = tip["y_lose"].to_numpy(int)

    scaler = StandardScaler()
    X_trs = scaler.fit_transform(X_tr)
    X_tes = scaler.transform(X_te)
    clf = LogisticRegression(
        class_weight="balanced", C=0.5, max_iter=500, solver="lbfgs"
    )
    clf.fit(X_trs, y_tr)
    proba = clf.predict_proba(X_tes)[:, 1]
    try:
        auc = float(roc_auc_score(y_te, proba))
    except ValueError:
        auc = float("nan")

    rows = []
    best = None
    for thr in np.arange(0.45, 0.85, 0.025):
        mask = proba >= thr
        if mask.sum() == 0 or mask.sum() == len(tip):
            continue
        rep = _cf(tip, mask)
        row = {
            "thr": round(float(thr), 3),
            **{
                k: rep[k]
                for k in (
                    "verdict",
                    "skips_n",
                    "precision_vs_losers",
                    "fire_retention_pct",
                    "delta_E_N",
                    "delta_EF_pp",
                    "false_skip_sell_winners",
                    "false_skip_monfri_winners",
                )
            },
            "kept_E_N": rep["kept"]["E_N"],
        }
        rows.append(row)
        score = (
            row["verdict"] == "SHADOW_CANDIDATE",
            row["verdict"] == "HOLD_SHADOW",
            row["delta_E_N"] or -9,
            row["precision_vs_losers"] or 0,
            -(row["false_skip_sell_winners"] or 0),
            -(row["false_skip_monfri_winners"] or 0),
        )
        if best is None or score > best[0]:
            best = (score, row, float(thr))

    # Chrono holdout inside tip (prevent tip-thr optimism)
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
    thr_ch = best[2] if best else 0.55
    mask2 = p2 >= thr_ch
    rep_ch = _cf(test_ch, mask2)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semver = f"L2skip_eur_m15_p_pretip_{ts}"
    run_dir = MODELS / semver
    latest = MODELS / "LATEST"
    run_dir.mkdir(parents=True, exist_ok=True)
    latest.mkdir(parents=True, exist_ok=True)

    thr = best[2] if best else 0.55
    bundle = {
        "scaler": scaler,
        "clf": clf,
        "feats": FEATS,
        "thr": thr,
        "train_window": "pre_tip_ytd_before_tip",
        "semver": semver,
    }
    joblib.dump(bundle, run_dir / "model.joblib")
    joblib.dump(bundle, latest / "model.joblib")

    tip_scored = tip.copy()
    tip_scored["p_lose"] = proba
    tip_scored["would_skip"] = (proba >= thr).astype(int)
    if P2_OUT.exists():
        tip_scored.to_csv(P2_OUT / "tip_l2ai_scored.csv", index=False)

    metrics = {
        "semver": semver,
        "algo": "LogisticRegression balanced C=0.5 + StandardScaler",
        "feats": FEATS,
        "train_n": int(len(pre)),
        "test_n": int(len(tip)),
        "auc_tip_oos": auc,
        "thr_selected_on_tip": thr,
        "thr_selection_note": (
            "Thr swept on tip for shadow CF only; weights fit on pre-tip. "
            "Chrono holdout required for challenger. Not LIVE_WITHHOLD."
        ),
        "best_row": best[1] if best else None,
        "sweep": rows,
        "chrono_holdout": {
            "train_n": int(len(train_ch)),
            "test_n": int(len(test_ch)),
            "thr": thr_ch,
            "report": {
                k: rep_ch[k]
                for k in (
                    "skips_n",
                    "precision_vs_losers",
                    "fire_retention_pct",
                    "delta_E_N",
                    "delta_EF_pp",
                    "false_skip_sell_winners",
                    "false_skip_monfri_winners",
                    "verdict",
                )
            },
            "kept": rep_ch["kept"],
            "baseline_holdout": rep_ch["baseline"],
        },
        "leak_proxy_pp": LEAK * 100,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    for path in (run_dir, latest):
        (path / "metrics.json").write_text(
            json.dumps(metrics, indent=2), encoding="utf-8"
        )

    mode = "SHADOW_ONLY"
    role = "shadow_artifact"
    chrono_v = rep_ch["verdict"]
    if (
        best
        and best[1]["verdict"] == "SHADOW_CANDIDATE"
        and chrono_v in ("SHADOW_CANDIDATE", "HOLD_SHADOW")
    ):
        role = "shadow_candidate_eligible"
    _write_pin(latest, semver, mode, role, metrics)

    chall_path = MODELS / "CHALLENGER.json"
    if not chall_path.exists():
        chall_path.write_text(
            json.dumps(
                {
                    "semver": None,
                    "status": "EMPTY",
                    "role": "ai_challenger",
                    "note": (
                        "No AI challenger. Chrono holdout / tip thr optimism. "
                        "Overlay champ L2det_eur_m15_v1b."
                    ),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    readme = (
        f"# {semver}\n\n"
        f"| Field | Value |\n| --- | --- |\n"
        f"| Mode | **{mode}** |\n"
        f"| Tip OOS AUC | {auc:.3f} |\n"
        f"| Best tip CF | {(best[1]['verdict'] if best else 'n/a')} |\n"
        f"| Chrono holdout | {chrono_v} |\n"
        f"| MQH | not exported |\n\n"
        f"Overlay champ remains `L2det_eur_m15_v1b`. See `aos_l5_retrain.md`.\n"
    )
    (latest / "README.md").write_text(readme, encoding="utf-8")
    shutil.copy(latest / "README.md", run_dir / "README.md")

    print(
        json.dumps(
            {
                "semver": semver,
                "auc": auc,
                "best": best[1] if best else None,
                "chrono_holdout": chrono_v,
                "role": role,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
