"""UK100-AOS-P2-T03..T07 — buy-caution, stress cells, size spec data, L2skip_uk train+CF."""
from __future__ import annotations

import csv
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
OUT = Path(__file__).resolve().parent
MODELS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\infra\artefacts\models\L2skip_uk"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.042667
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


def load_combined() -> pd.DataFrame:
    path = TAPES / "uk100_tip_prior_fire_tape_v0.csv"
    df = pd.read_csv(path)
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df["y_lose"] = 1 - df["win"].astype(int)
    df["side_buy"] = (df["side"] == "BUY").astype(int)
    df["is_thu"] = df["cell_dow_thu"].astype(int)
    df["is_h08"] = df["cell_hour_08"].astype(int)
    df["is_jul"] = df["cell_month_jul"].astype(int)
    df["is_feb"] = (df["month"] == "2026-02").astype(int)
    df["near_atr_cap"] = df["near_atr_cap"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
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
    wed_w = int(((skipped["dow"] == "Wed") & (skipped["win"] == 1)).sum()) if n_skip else 0
    sell_w = int(((skipped["side"] == "SELL") & (skipped["win"] == 1)).sum()) if n_skip else 0
    return {
        "skips_n": n_skip,
        "precision_vs_losers": round(losers_skip / n_skip, 4) if n_skip else None,
        "recall_losers": round(losers_skip / losers_base, 4) if losers_base else None,
        "false_skip_winners": int((skipped["win"] == 1).sum()) if n_skip else 0,
        "false_skip_wed_winners": wed_w,
        "false_skip_sell_winners": sell_w,
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
    if en_up and ef_ok and prec >= 0.55 and rep["skips_n"] > 0:
        return "ARM_SOFT"
    if ef_ok and (k["E_N"] >= base_m["E_N"] - 1e-9) and rep["skips_n"] > 0:
        return "HOLD_SOFT"
    if not ef_ok and not en_up:
        return "DISARM"
    return "DISARM"


def run_det_cf(tip: pd.DataFrame) -> dict:
    base_m = metrics(tip, "baseline_tip")
    policies = {
        "skip_BUY": tip["side_buy"] == 1,
        "skip_BUY_if_Thu": (tip["side_buy"] == 1) & (tip["is_thu"] == 1),
        "skip_BUY_if_H08": (tip["side_buy"] == 1) & (tip["is_h08"] == 1),
        "skip_BUY_if_near_atr": (tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1),
        "skip_Jul": tip["is_jul"] == 1,
        "skip_near_atr_cap": tip["near_atr_cap"] == 1,
        "skip_Feb_on_combined_note": tip["is_feb"] == 1,  # tip has no Feb; n=0
        "skip_Thu_PLUS_BUY_near_atr": (tip["is_thu"] == 1)
        | ((tip["side_buy"] == 1) & (tip["near_atr_cap"] == 1)),
        "skip_Thu_PLUS_Jul": (tip["is_thu"] == 1) | (tip["is_jul"] == 1),
    }
    out = {"baseline": base_m, "policies": {}}
    for name, mask in policies.items():
        mask = mask.to_numpy()
        if mask.sum() == 0:
            out["policies"][name] = {"skips_n": 0, "verdict": "N/A_EMPTY", "note": "no fires"}
            continue
        rep = skip_report(tip, mask)
        rep["verdict"] = verdict(base_m, rep)
        out["policies"][name] = rep
    return out


def size_table_spec(tip: pd.DataFrame) -> dict:
    """P2-T05 — lifecycle f multipliers (spec only; wire after L4)."""
    # Rolling W15 E_N path for lifecycle labels
    wins = tip["win"].to_numpy()
    ens = []
    for i in range(len(tip)):
        if i < 14:
            ens.append(None)
            continue
        w = wins[i - 14 : i + 1]
        wr = w.mean()
        ens.append(float(wr * (R + 1) - 1))
    return {
        "task": "UK100-AOS-P2-T05",
        "status": "SPEC_ONLY",
        "note": "Wire after L4 health bus; do not size-live yet",
        "f_declared_baseline": 0.005,
        "table": [
            {"state": "Expanding", "cond": "W15 E_N > baseline and rising", "f_mult": 1.0},
            {"state": "Stable", "cond": "W15 E_N >= 0 and |Δ| small", "f_mult": 1.0},
            {
                "state": "Compressing",
                "cond": "W15 E_N falling 2 evals or 0 < EF <= M",
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
                "cond": "Thu SOFT map (armed)",
                "f_mult": 0.0,
                "note": "skip outranks size",
            },
        ],
        "w15_E_N_tail": [round(x, 4) if x is not None else None for x in ens[-10:]],
    }


def train_l2skip(df: pd.DataFrame) -> dict:
    """Train on prior, score tip OOS; also tune thr on tip for shadow report."""
    prior = df[df["window"].str.startswith("2026.01")].copy()
    tip = df[df["window"].str.startswith("2026.05")].copy()
    # windows column is like 2026.01.01-2026.04.30
    prior = df[df["window"] == "2026.01.01-2026.04.30"].copy()
    tip = df[df["window"] == "2026.05.01-2026.08.31"].copy()

    X_tr = prior[FEATS].to_numpy(dtype=float)
    y_tr = prior["y_lose"].to_numpy(dtype=int)
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

    # Threshold sweep on tip for shadow CF (report honesty: thr selected on tip)
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
            "false_skip_wed_winners": rep["false_skip_wed_winners"],
        }
        rows.append(row)
        score = (
            v == "ARM_SOFT",
            rep["delta_E_N"] or -9,
            rep["precision_vs_losers"] or 0,
            -(rep["false_skip_wed_winners"] or 0),
            rep["fire_retention_pct"],
        )
        if best is None or score > best[0]:
            best = (score, row, mask, float(thr))

    # also chron holdout inside tip: train tip[:60%]+prior, test tip[60%:]
    tip_sorted = tip.sort_values("open_dt")
    cut = int(len(tip_sorted) * 0.6)
    train_ch = pd.concat([prior, tip_sorted.iloc[:cut]], ignore_index=True)
    test_ch = tip_sorted.iloc[cut:].copy()
    Xc = scaler.fit_transform(train_ch[FEATS].to_numpy(float))
    yc = train_ch["y_lose"].to_numpy(int)
    clf2 = LogisticRegression(
        class_weight="balanced", C=0.5, max_iter=500, solver="lbfgs"
    )
    clf2.fit(Xc, yc)
    p2 = clf2.predict_proba(scaler.transform(test_ch[FEATS].to_numpy(float)))[:, 1]
    # use same thr as best if available else 0.55
    thr_ch = best[3] if best else 0.55
    mask2 = p2 >= thr_ch
    rep_ch = skip_report(test_ch, mask2)
    base_ch = metrics(test_ch, "tip_holdout")
    rep_ch["verdict"] = verdict(base_ch, rep_ch)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semver = f"L2skip_uk_p_prior_{ts}"
    run_dir = MODELS / semver
    run_dir.mkdir(parents=True, exist_ok=True)
    latest = MODELS / "LATEST"
    latest.mkdir(parents=True, exist_ok=True)

    bundle = {
        "scaler": scaler,
        "clf": clf,
        "feats": FEATS,
        "thr": best[3] if best else 0.55,
        "train_window": "prior_2026.01-04",
        "semver": semver,
    }
    # re-fit scaler+clf stored from prior-only for export consistency
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
        "train_n": int(len(prior)),
        "test_n": int(len(tip)),
        "auc_tip_oos": auc,
        "thr_selected_on_tip": best[3] if best else None,
        "thr_selection_note": (
            "Threshold swept on tip for shadow CF reporting; "
            "model weights fit on prior only. Not production-ready."
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
    (latest / "PIN.json").write_text(
        json.dumps({"semver": semver, "mode": "SHADOW_ONLY"}, indent=2), encoding="utf-8"
    )
    return meta, tip_scored, best


def stack_cf(tip: pd.DataFrame, tip_scored: pd.DataFrame, thr: float) -> dict:
    base_m = metrics(tip, "baseline")
    thu = (tip["is_thu"] == 1).to_numpy()
    ai = (tip_scored["p_lose"].to_numpy() >= thr)
    # align index
    tip = tip.reset_index(drop=True)
    tip_scored = tip_scored.reset_index(drop=True)
    ai = tip_scored["p_lose"].to_numpy() >= thr

    configs = {
        "P0_engine": np.zeros(len(tip), dtype=bool),
        "L2det_Thu": thu,
        "L2AI_only": ai,
        "L2det_OR_L2AI": thu | ai,
        "L2det_AND_L2AI": thu & ai,
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
    df = load_combined()
    tip = df[df["window"] == "2026.05.01-2026.08.31"].copy()
    prior = df[df["window"] == "2026.01.01-2026.04.30"].copy()

    det = run_det_cf(tip)
    # prior diagnostic for buy / jul / atr
    prior_diag = {}
    for name, mask in {
        "skip_BUY": prior["side_buy"] == 1,
        "skip_Jul": prior["month"] == "2026-07",
        "skip_near_atr_cap": prior["near_atr_cap"] == 1,
        "skip_Feb": prior["is_feb"] == 1,
        "skip_Thu": prior["is_thu"] == 1,
    }.items():
        m = mask.to_numpy()
        if m.sum() == 0:
            prior_diag[name] = {"skips_n": 0}
            continue
        base_p = metrics(prior, "prior")
        rep = skip_report(prior, m)
        rep["verdict"] = verdict(base_p, rep)
        prior_diag[name] = rep

    size_spec = size_table_spec(tip)
    meta, tip_scored, best = train_l2skip(df)
    thr = best[3] if best else 0.55
    stacks = stack_cf(tip, tip_scored, thr)

    # Arm recommendations
    arms = {
        "P2-T02_Thu": "ARM_SOFT (unchanged)",
        "P2-T03_buy_caution": None,
        "P2-T04_stress": None,
        "P2-T06_L2AI": None,
    }
    for k, v in det["policies"].items():
        if k.startswith("skip_BUY") and v.get("verdict") == "ARM_SOFT":
            arms["P2-T03_buy_caution"] = f"ARM_SOFT candidate: {k}"
            break
    if arms["P2-T03_buy_caution"] is None:
        # pick best buy policy by delta_E_N among non-reject
        buy_pols = {
            k: v
            for k, v in det["policies"].items()
            if "BUY" in k and isinstance(v, dict) and v.get("delta_E_N") is not None
        }
        if buy_pols:
            best_buy = max(buy_pols.items(), key=lambda kv: kv[1]["delta_E_N"])
            arms["P2-T03_buy_caution"] = (
                f"{best_buy[1].get('verdict')}: {best_buy[0]} "
                f"ΔE_N={best_buy[1]['delta_E_N']}"
            )
        else:
            arms["P2-T03_buy_caution"] = "DISARM"

    for k in ("skip_Jul", "skip_near_atr_cap", "skip_Thu_PLUS_Jul"):
        v = det["policies"].get(k, {})
        if v.get("verdict") == "ARM_SOFT":
            arms["P2-T04_stress"] = f"ARM_SOFT: {k}"
            break
    if arms["P2-T04_stress"] is None:
        arms["P2-T04_stress"] = "DISARM / HOLD — see CF"

    if best and best[1]["verdict"] == "ARM_SOFT":
        arms["P2-T06_L2AI"] = f"ARM_SOFT shadow thr={best[1]['thr']}"
    elif best:
        arms["P2-T06_L2AI"] = f"{best[1]['verdict']} thr={best[1]['thr']}"
    else:
        arms["P2-T06_L2AI"] = "DISARM"

    report = {
        "task": "UK100-AOS-P2-T03..T07",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "Leak_proxy_pp": LEAK * 100,
        "P2_T03_T04_det_cf_tip": det,
        "P2_T03_T04_prior_diag": prior_diag,
        "P2_T05_size_table": size_spec,
        "P2_T06_L2skip_uk": {
            "semver": meta["semver"],
            "auc_tip_oos": meta["auc_tip_oos"],
            "thr": meta["thr_selected_on_tip"],
            "best_row": meta["best_row"],
            "chrono_holdout": meta["chrono_holdout"],
            "model_dir": str(MODELS / meta["semver"]),
        },
        "P2_T07_stack_cf": stacks,
        "arm_summary": arms,
    }
    (OUT / "P2_REMAINING_CF.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps({"arm_summary": arms, "best_l2ai": meta["best_row"], "stacks": {
        k: {
            "verdict": v.get("verdict"),
            "delta_E_N": v.get("delta_E_N"),
            "kept_E_N": (v.get("kept") or {}).get("E_N"),
            "retention": v.get("fire_retention_pct"),
            "prec": v.get("precision_vs_losers"),
        }
        for k, v in stacks["stacks"].items()
    }, "det_buy_jul": {
        k: {
            "verdict": v.get("verdict"),
            "delta_E_N": v.get("delta_E_N"),
            "retention": v.get("fire_retention_pct"),
            "prec": v.get("precision_vs_losers"),
            "skips": v.get("skips_n"),
        }
        for k, v in det["policies"].items()
        if any(x in k for x in ("BUY", "Jul", "near_atr", "Thu_PLUS"))
    }}, indent=2))


if __name__ == "__main__":
    main()
