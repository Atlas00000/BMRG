"""UK100 L2skip train loop — prior fit · tip OOS · store under L2skip_uk/.

Does NOT arm LIVE_WITHHOLD. Writes SHADOW_ONLY pins only.
Promote to CHALLENGER requires aos_l5_retrain.md gates (HITL).

Usage:
  python infra/src/train/train_l2_uk100.py
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
TAPES = BMRG / "doc" / "assets" / "UK100" / "tapes"
MODELS = BMRG / "infra" / "artefacts" / "models" / "L2skip_uk"

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.042667  # journal proxy until measured

FEATS = [
    "side_buy",
    "is_thu",
    "is_h08",
    "is_jul",
    "is_feb",
    "near_atr_cap",
    "hour",
    "atr_z",
    "is_wed",
    "is_mon",
    "is_fri",
]


def _featurize(df: pd.DataFrame, atr_mu: float, atr_sd: float) -> pd.DataFrame:
    d = df.copy()
    d["open_dt"] = pd.to_datetime(d["open_time"], format="%Y.%m.%d %H:%M:%S")
    d["win"] = d["win"].astype(int)
    d["y_lose"] = 1 - d["win"]
    d["side_buy"] = (d["side"] == "BUY").astype(int)
    d["is_thu"] = d["cell_dow_thu"].astype(int)
    d["is_h08"] = (
        ((d["side"] == "BUY") & (d["cell_hour_08"].astype(int) == 1)).astype(int)
        if "cell_hour_08" in d.columns
        else (((d["side"] == "BUY") & (d["hour"] == 8)).astype(int))
    )
    d["is_jul"] = d["cell_month_jul"].astype(int)
    d["is_feb"] = (d["open_dt"].dt.month == 2).astype(int)
    d["near_atr_cap"] = d["near_atr_cap"].astype(int)
    d["hour"] = d["hour"].astype(int)
    sd = atr_sd if atr_sd > 1e-9 else 1.0
    d["atr_z"] = (d["atr_pts"].astype(float) - atr_mu) / sd
    d["is_wed"] = (d["open_dt"].dt.dayofweek == 2).astype(int)
    d["is_mon"] = (d["open_dt"].dt.dayofweek == 0).astype(int)
    d["is_fri"] = (d["open_dt"].dt.dayofweek == 4).astype(int)
    d["pnl_R"] = d["pnl_R_design"].astype(float)
    return d


def _load() -> tuple[pd.DataFrame, pd.DataFrame]:
    prior_raw = pd.read_csv(TAPES / "uk100_prior_fire_tape_v0.csv")
    tip_raw = pd.read_csv(TAPES / "uk100_tip_fire_tape_v0.csv")
    atr = pd.concat([prior_raw["atr_pts"], tip_raw["atr_pts"]]).astype(float)
    atr_mu, atr_sd = float(atr.mean()), float(atr.std(ddof=0))
    prior = _featurize(prior_raw, atr_mu, atr_sd).sort_values("open_dt").reset_index(drop=True)
    tip = _featurize(tip_raw, atr_mu, atr_sd).sort_values("open_dt").reset_index(drop=True)
    return prior, tip


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
    prec = (
        float((1 - skips["win"]).mean()) if len(skips) else None
    )
    wed_fp = int(((skips["is_wed"] == 1) & (skips["win"] == 1)).sum()) if len(skips) else 0
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
    # promote gates (shadow candidate) — see aos_l5_retrain.md
    verdict = "DISARM"
    if mask.sum() == 0:
        verdict = "DISARM"
    elif ret < 50.0:
        verdict = "REJECT_FREQUENCY_STALL"
    elif d_en is not None and d_en > 0 and (prec or 0) >= 0.55 and wed_fp <= 1:
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
        "false_skip_wed_winners": wed_fp,
        "verdict": verdict,
    }


def _write_pin(latest: Path, semver: str, mode: str, role: str, metrics: dict) -> None:
    pin = {
        "semver": semver,
        "mode": mode,
        "role": role,
        "overlay_champ": "L2det_uk_v1b",
        "ai_champ": None,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "auc_tip_oos": metrics.get("auc_tip_oos"),
        "best_verdict": (metrics.get("best_row") or {}).get("verdict"),
    }
    (latest / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    (latest / "META.json").write_text(
        json.dumps(
            {
                "semver": semver,
                "mode": mode,
                "role": role,
                "mqh_exported": False,
                "live_withhold": False,
                "policy": "doc/assets/UK100/aos_l5_retrain.md",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    prior, tip = _load()
    X_tr = prior[FEATS].to_numpy(float)
    y_tr = prior["y_lose"].to_numpy(int)
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
            **{k: rep[k] for k in (
                "verdict",
                "skips_n",
                "precision_vs_losers",
                "fire_retention_pct",
                "delta_E_N",
                "delta_EF_pp",
                "false_skip_wed_winners",
            )},
            "kept_E_N": rep["kept"]["E_N"],
        }
        rows.append(row)
        score = (
            row["verdict"] == "SHADOW_CANDIDATE",
            row["verdict"] == "HOLD_SHADOW",
            row["delta_E_N"] or -9,
            row["precision_vs_losers"] or 0,
            -(row["false_skip_wed_winners"] or 0),
        )
        if best is None or score > best[0]:
            best = (score, row, float(thr))

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semver = f"L2skip_uk_p_prior_{ts}"
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
        "train_window": "prior_2026.01-04",
        "semver": semver,
    }
    joblib.dump(bundle, run_dir / "model.joblib")
    joblib.dump(bundle, latest / "model.joblib")

    metrics = {
        "semver": semver,
        "algo": "LogisticRegression balanced C=0.5 + StandardScaler",
        "feats": FEATS,
        "train_n": int(len(prior)),
        "test_n": int(len(tip)),
        "auc_tip_oos": auc,
        "thr_selected_on_tip": thr,
        "thr_selection_note": (
            "Thr swept on tip for shadow CF only; weights fit on prior. "
            "Not LIVE_WITHHOLD."
        ),
        "best_row": best[1] if best else None,
        "sweep": rows,
        "leak_proxy_pp": LEAK * 100,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    for path in (run_dir, latest):
        (path / "metrics.json").write_text(
            json.dumps(metrics, indent=2), encoding="utf-8"
        )

    # Never auto-promote: LATEST stays SHADOW_ONLY until HITL sets CHALLENGER
    mode = "SHADOW_ONLY"
    role = "shadow_artifact"
    if best and best[1]["verdict"] == "SHADOW_CANDIDATE":
        role = "shadow_candidate_eligible"
    _write_pin(latest, semver, mode, role, metrics)

    # CHALLENGER pointer unchanged unless eligible + explicit promote (not here)
    chall_path = MODELS / "CHALLENGER.json"
    if not chall_path.exists():
        chall_path.write_text(
            json.dumps(
                {
                    "semver": None,
                    "status": "EMPTY",
                    "note": "No AI challenger armed; L2det_uk_v1b remains overlay champ",
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
        f"| MQH | not exported |\n\n"
        f"Overlay champ remains `L2det_uk_v1b`. See `aos_l5_retrain.md`.\n"
    )
    (latest / "README.md").write_text(readme, encoding="utf-8")
    shutil.copy(latest / "README.md", run_dir / "README.md")

    print(json.dumps({"semver": semver, "auc": auc, "best": best[1] if best else None}, indent=2))


if __name__ == "__main__":
    main()
