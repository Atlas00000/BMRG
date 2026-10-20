"""AAPL M5 AIOS P2 — L2det shadow CF + L2skip_aapl_m5 train + stack scorecard."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parent
TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\AAPL\tapes"
)
MODEL = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG"
    r"\infra\artefacts\models\L2skip_aapl_m5\LATEST"
)

R = 280.0 / 190.0
BWR = 1.0 / (1.0 + R)
LEAK_PROFILE = 0.153  # Stage-1 authority (med/SL shorthand)
LEAK_2X = 0.123404  # P1 COST_PROXY
ATR_MAX = 98.0
BASELINE_EN = 0.156528  # tip May→Oct from P1
SPREAD_THR = 30


def load(name: str) -> list[dict]:
    rows = []
    with (TAPES / name).open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["win"] = int(r["win"])
            r["hour"] = int(r["hour"])
            r["atr_pts"] = float(r["atr_pts"]) if r.get("atr_pts") else None
            r["bbw_pct"] = float(r["bbw_pct"]) if r.get("bbw_pct") else None
            r["spread_pts"] = int(r["spread_pts"])
            r["near_atr_cap"] = int(r["near_atr_cap"])
            r["cell_dow_wed"] = int(r["cell_dow_wed"])
            r["cell_h1"] = int(r["cell_h1"])
            r["cell_month_jul"] = int(r["cell_month_jul"])
            r["cell_spread_high"] = int(r["cell_spread_high"])
            r["cell_month_may"] = int(r["cell_month_may"])
            r["cell_dow_mon"] = int(r["cell_dow_mon"])
            r["cell_buy"] = int(r["cell_buy"])
            r["cell_sell"] = int(r["cell_sell"])
            r["y_lose"] = int(r["y_lose"])
            r["nights_held"] = int(r["nights_held"])
            r["month"] = r["month"]
            r["dow"] = r["dow"]
            r["side"] = r["side"]
            r["regime_tag"] = r.get("regime_tag", "")
            rows.append(r)
    return rows


def metrics(kept: list[dict]) -> dict:
    n = len(kept)
    if n == 0:
        return {
            "n": 0,
            "WR": None,
            "E_N": None,
            "BM_pp": None,
            "EF_profile_pp": None,
            "EF_2x_pp": None,
        }
    wr = sum(r["win"] for r in kept) / n
    bm = wr - BWR
    en = wr * (R + 1.0) - 1.0
    return {
        "n": n,
        "WR": round(wr, 6),
        "E_N": round(en, 6),
        "BM_pp": round(bm * 100, 4),
        "EF_profile_pp": round((bm - LEAK_PROFILE) * 100, 4),
        "EF_2x_pp": round((bm - LEAK_2X) * 100, 4),
    }


def score_policy(rows: list[dict], skip_fn, name: str) -> dict:
    skipped = [r for r in rows if skip_fn(r)]
    kept = [r for r in rows if not skip_fn(r)]
    base = metrics(rows)
    after = metrics(kept)
    n_skip = len(skipped)
    losers_skipped = sum(1 for r in skipped if not r["win"])
    prec = (losers_skipped / n_skip) if n_skip else None
    fp_may = sum(1 for r in skipped if r["cell_month_may"] == 1 and r["win"])
    fp_mon = sum(1 for r in skipped if r["cell_dow_mon"] == 1 and r["win"])
    fp_buy = sum(1 for r in skipped if r["cell_buy"] == 1 and r["win"])
    ret = len(kept) / len(rows) if rows else 0.0
    d_en = None if after["E_N"] is None else round(after["E_N"] - base["E_N"], 6)
    d_ef = (
        None
        if after["EF_profile_pp"] is None
        else round(after["EF_profile_pp"] - base["EF_profile_pp"], 4)
    )

    verdict = "HOLD_SOFT"
    if n_skip == 0:
        verdict = "NO_OP"
    elif after["E_N"] is not None and after["E_N"] < BASELINE_EN - 0.05:
        verdict = "REJECT"
    elif ret < 0.50:
        verdict = "REJECT_FREQUENCY_STALL"
    elif d_en is not None and d_en < -0.02:
        verdict = "REJECT"
    elif (
        d_en is not None
        and d_en >= 0.02
        and (prec or 0) >= 0.55
        and fp_may <= 1
        and fp_mon <= 2
    ):
        verdict = "ARM_SOFT"
    elif d_en is not None and d_en >= 0 and (prec or 0) >= 0.50:
        verdict = "HOLD_SOFT"
    else:
        verdict = "DISARM"

    return {
        "policy": name,
        "baseline": base,
        "kept": after,
        "skips_n": n_skip,
        "fire_retention_pct": round(ret * 100, 2),
        "precision_losers": None if prec is None else round(prec, 4),
        "ΔE_N": d_en,
        "ΔEF_profile_pp": d_ef,
        "fp_may_winners": fp_may,
        "fp_mon_winners": fp_mon,
        "fp_buy_winners": fp_buy,
        "verdict": verdict,
    }


def parity(rows: list[dict]) -> dict:
    tue = sum(1 for r in rows if r["dow"] == "Tue")
    atr_breach = sum(
        1 for r in rows if r["atr_pts"] is not None and r["atr_pts"] > ATR_MAX
    )
    bbw_hi = sum(
        1 for r in rows if r["bbw_pct"] is not None and r["bbw_pct"] > 2.0
    )
    bbw_lo = sum(
        1 for r in rows if r["bbw_pct"] is not None and r["bbw_pct"] < 0.30
    )
    return {
        "tue_fires": tue,
        "atr_gt_98": atr_breach,
        "bbw_out_of_band": bbw_hi + bbw_lo,
        "verdict": (
            "PASS"
            if tue == 0 and atr_breach == 0 and (bbw_hi + bbw_lo) == 0
            else "FAIL"
        ),
    }


FEATS = [
    "hour",
    "spread_pts",
    "atr_pts",
    "near_atr_cap",
    "cell_dow_wed",
    "cell_month_jul",
    "cell_spread_high",
    "cell_buy",
    "cell_sell",
    "hour_18",
    "dow_wed",
]


def feat_matrix(rows: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for r in rows:
        X.append(
            [
                r["hour"],
                r["spread_pts"],
                r["atr_pts"] or 0.0,
                r["near_atr_cap"],
                r["cell_dow_wed"],
                r["cell_month_jul"],
                int(r["spread_pts"] >= SPREAD_THR),
                r["cell_buy"],
                r["cell_sell"],
                int(r["hour"] == 18),
                int(r["dow"] == "Wed"),
            ]
        )
        y.append(r["y_lose"])
    return np.asarray(X, dtype=float), np.asarray(y, dtype=int)


def train_ai(prior: list[dict], tip: list[dict]) -> dict:
    Xp, yp = feat_matrix(prior)
    Xt, yt = feat_matrix(tip)
    scaler = StandardScaler()
    Xp_s = scaler.fit_transform(Xp)
    Xt_s = scaler.transform(Xt)
    clf = LogisticRegression(class_weight="balanced", C=0.5, max_iter=500)
    clf.fit(Xp_s, yp)
    tip_proba = clf.predict_proba(Xt_s)[:, 1]
    prior_proba = clf.predict_proba(Xp_s)[:, 1]
    try:
        auc_tip = float(roc_auc_score(yt, tip_proba))
    except ValueError:
        auc_tip = None
    try:
        auc_prior = float(roc_auc_score(yp, prior_proba))
    except ValueError:
        auc_prior = None

    thr_results = []
    best = None
    for thr in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]:
        skip_mask = tip_proba >= thr
        skipped = [r for r, m in zip(tip, skip_mask) if m]
        kept = [r for r, m in zip(tip, skip_mask) if not m]
        after = metrics(kept)
        base = metrics(tip)
        n_skip = len(skipped)
        prec = (
            sum(1 for r in skipped if not r["win"]) / n_skip if n_skip else None
        )
        d_en = after["E_N"] - base["E_N"] if after["E_N"] is not None else None
        row = {
            "thr": thr,
            "skips_n": n_skip,
            "retention_pct": round(100 * len(kept) / len(tip), 2),
            "precision_losers": None if prec is None else round(prec, 4),
            "kept_E_N": after["E_N"],
            "ΔE_N": None if d_en is None else round(d_en, 6),
        }
        thr_results.append(row)
        if d_en is not None and n_skip > 0:
            if best is None or d_en > best["ΔE_N"]:
                best = row

    MODEL.mkdir(parents=True, exist_ok=True)
    meta = {
        "model": "LogisticRegression",
        "features": FEATS,
        "train": f"prior Jan-Apr n={len(prior)}",
        "auc_prior": auc_prior,
        "auc_tip_oos": auc_tip,
        "best_thr_tip": best,
        "status": "SHADOW_ONLY",
        "pin": "L2skip_aapl_m5",
    }
    (MODEL / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    np.save(MODEL / "coef.npy", clf.coef_)
    np.save(MODEL / "intercept.npy", clf.intercept_)
    np.save(MODEL / "scaler_mean.npy", scaler.mean_)
    np.save(MODEL / "scaler_scale.npy", scaler.scale_)

    best_thr = best["thr"] if best else 0.70
    tip_ai_skip = {
        r["open_time"] + r["side"]: bool(p >= best_thr)
        for r, p in zip(tip, tip_proba)
    }

    return {
        "auc_prior": None if auc_prior is None else round(auc_prior, 4),
        "auc_tip_oos": None if auc_tip is None else round(auc_tip, 4),
        "thr_sweep": thr_results,
        "best_thr_tip": best,
        "artifact": str(MODEL),
        "tip_ai_skip": tip_ai_skip,
        "best_thr": best_thr,
        "verdict": (
            "DISARM"
            if (auc_tip is None or auc_tip < 0.55 or (best and best["ΔE_N"] < 0.02))
            else "HOLD_SOFT"
        ),
    }


def main() -> None:
    tip = load("aapl_m5_tip_fire_tape_v0.csv")
    prior = load("aapl_m5_prior_fire_tape_v0.csv")
    ytd = load("aapl_m5_ytd_fire_tape_v0.csv")

    def is_wed(r):
        return r["dow"] == "Wed"

    def is_h18(r):
        return r["hour"] == 18

    def is_jul(r):
        return r["month"] == "2026-07"

    def is_spread(r):
        return r["spread_pts"] >= SPREAD_THR

    def is_h1(r):
        return r["cell_h1"] == 1

    policies = {
        "P2_T01_parity_tip": parity(tip),
        "P2_T01_parity_ytd": parity(ytd),
        # T02 Wed ± spread
        "skip_Wed": score_policy(tip, is_wed, "skip_Wed"),
        "skip_spread_ge30": score_policy(tip, is_spread, "skip_spread_ge30"),
        "skip_Wed_OR_spread": score_policy(
            tip, lambda r: is_wed(r) or is_spread(r), "skip_Wed_OR_spread"
        ),
        "skip_Wed_AND_spread": score_policy(
            tip, lambda r: is_wed(r) and is_spread(r), "skip_Wed_AND_spread"
        ),
        "skip_H18": score_policy(tip, is_h18, "skip_H18"),
        "skip_Wed_OR_H18": score_policy(
            tip, lambda r: is_wed(r) or is_h18(r), "skip_Wed_OR_H18"
        ),
        "skip_H18_OR_spread": score_policy(
            tip, lambda r: is_h18(r) or is_spread(r), "skip_H18_OR_spread"
        ),
        # T03 Jul / H1 (H1 is prior-only on tip=0)
        "skip_Jul": score_policy(tip, is_jul, "skip_Jul"),
        "skip_Jul_OR_Wed": score_policy(
            tip, lambda r: is_jul(r) or is_wed(r), "skip_Jul_OR_Wed"
        ),
        "skip_Jul_OR_H18": score_policy(
            tip, lambda r: is_jul(r) or is_h18(r), "skip_Jul_OR_H18"
        ),
        "skip_Jul_OR_spread": score_policy(
            tip, lambda r: is_jul(r) or is_spread(r), "skip_Jul_OR_spread"
        ),
        "skip_Jul_OR_Wed_OR_H18": score_policy(
            tip,
            lambda r: is_jul(r) or is_wed(r) or is_h18(r),
            "skip_Jul_OR_Wed_OR_H18",
        ),
        "skip_SELL": score_policy(tip, lambda r: r["cell_sell"] == 1, "skip_SELL"),
        "skip_BUY": score_policy(tip, lambda r: r["cell_buy"] == 1, "skip_BUY"),
        "skip_SELL_AND_H18": score_policy(
            tip,
            lambda r: r["cell_sell"] == 1 and is_h18(r),
            "skip_SELL_AND_H18",
        ),
        "skip_SELL_AND_Wed": score_policy(
            tip,
            lambda r: r["cell_sell"] == 1 and is_wed(r),
            "skip_SELL_AND_Wed",
        ),
        "skip_BUY_AND_H18": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and is_h18(r),
            "skip_BUY_AND_H18",
        ),
        # Protect checks (should REJECT / DISARM)
        "skip_May": score_policy(
            tip, lambda r: r["cell_month_may"] == 1, "skip_May"
        ),
        "skip_Mon": score_policy(
            tip, lambda r: r["cell_dow_mon"] == 1, "skip_Mon"
        ),
        # YTD / prior support
        "ytd_skip_Wed": score_policy(ytd, is_wed, "ytd_skip_Wed"),
        "ytd_skip_H18": score_policy(ytd, is_h18, "ytd_skip_H18"),
        "ytd_skip_Jul": score_policy(ytd, is_jul, "ytd_skip_Jul"),
        "ytd_skip_H1": score_policy(ytd, is_h1, "ytd_skip_H1"),
        "ytd_skip_Wed_OR_H18": score_policy(
            ytd, lambda r: is_wed(r) or is_h18(r), "ytd_skip_Wed_OR_H18"
        ),
        "ytd_skip_Jul_OR_Wed_OR_H18": score_policy(
            ytd,
            lambda r: is_jul(r) or is_wed(r) or is_h18(r),
            "ytd_skip_Jul_OR_Wed_OR_H18",
        ),
        "ytd_skip_H1_OR_Jul_OR_Wed_OR_H18": score_policy(
            ytd,
            lambda r: is_h1(r) or is_jul(r) or is_wed(r) or is_h18(r),
            "ytd_skip_H1_OR_Jul_OR_Wed_OR_H18",
        ),
        "prior_skip_Wed": score_policy(prior, is_wed, "prior_skip_Wed"),
        "prior_skip_H18": score_policy(prior, is_h18, "prior_skip_H18"),
    }

    ai = train_ai(prior, tip)
    tip_ai_skip = ai.pop("tip_ai_skip")
    best_thr = ai.pop("best_thr")

    def ai_skip(r):
        return tip_ai_skip.get(r["open_time"] + r["side"], False)

    stacks = {
        "P0_engine": score_policy(tip, lambda r: False, "P0_engine"),
        "L2det_Wed": policies["skip_Wed"],
        "L2det_H18": policies["skip_H18"],
        "L2det_spread": policies["skip_spread_ge30"],
        "L2det_Jul": policies["skip_Jul"],
        "L2det_Wed_OR_H18": policies["skip_Wed_OR_H18"],
        "L2det_Jul_OR_H18": policies["skip_Jul_OR_H18"],
        "L2det_Jul_OR_Wed": policies["skip_Jul_OR_Wed"],
        "L2det_v1_Jul_OR_Wed_OR_H18": policies["skip_Jul_OR_Wed_OR_H18"],
        "L2det_v1a_Jul_OR_H18": policies["skip_Jul_OR_H18"],
        "L2det_v1b_Wed_OR_H18": policies["skip_Wed_OR_H18"],
        "L2det_v1c_Jul_OR_Wed_OR_spread": score_policy(
            tip,
            lambda r: is_jul(r) or is_wed(r) or is_spread(r),
            "L2det_v1c_Jul_OR_Wed_OR_spread",
        ),
        "L2det_v1d_SELL_AND_H18": policies["skip_SELL_AND_H18"],
        "L2AI_only": score_policy(tip, ai_skip, f"L2AI_thr_{best_thr}"),
    }
    stacks["L2det_v1_OR_L2AI"] = score_policy(
        tip,
        lambda r: (is_jul(r) or is_wed(r) or is_h18(r)) or ai_skip(r),
        "L2det_v1_OR_L2AI",
    )
    stacks["L2det_v1b_OR_L2AI"] = score_policy(
        tip,
        lambda r: (is_wed(r) or is_h18(r)) or ai_skip(r),
        "L2det_v1b_OR_L2AI",
    )

    # Rank ARM_SOFT / HOLD by ΔE_N among tip stacks with retention>=50%
    ranked = []
    for k, v in stacks.items():
        if k == "P0_engine":
            continue
        if not isinstance(v, dict) or "ΔE_N" not in v:
            continue
        ranked.append(
            {
                "stack": k,
                "verdict": v["verdict"],
                "ΔE_N": v["ΔE_N"],
                "ΔEF_profile_pp": v["ΔEF_profile_pp"],
                "retention_pct": v["fire_retention_pct"],
                "precision_losers": v["precision_losers"],
                "fp_may": v["fp_may_winners"],
                "fp_mon": v["fp_mon_winners"],
                "fp_buy": v["fp_buy_winners"],
                "kept_E_N": v["kept"]["E_N"],
                "kept_n": v["kept"]["n"],
            }
        )
    ranked.sort(key=lambda x: (x["ΔE_N"] is None, -(x["ΔE_N"] or -99)))

    out = {
        "task": "AAPL-M5-AOS-P2",
        "baseline_tip_E_N": BASELINE_EN,
        "R": R,
        "BWR": BWR,
        "Leak_profile": LEAK_PROFILE,
        "policies": policies,
        "stacks": stacks,
        "L2AI": ai,
        "ranked_stacks": ranked,
    }
    (OUT / "P2_CF.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Preferred pick: best ARM_SOFT else best HOLD_SOFT with ΔE_N>0 and ret>=55
    preferred = None
    for row in ranked:
        if row["verdict"] == "ARM_SOFT" and (row["retention_pct"] or 0) >= 55:
            preferred = row
            break
    if preferred is None:
        for row in ranked:
            if (
                row["verdict"] in ("ARM_SOFT", "HOLD_SOFT")
                and (row["ΔE_N"] or 0) > 0
                and (row["retention_pct"] or 0) >= 55
                and (row["fp_may"] or 0) <= 1
            ):
                preferred = row
                break

    summary = {
        "task": "AAPL-M5-AOS-P2",
        "parity_tip": policies["P2_T01_parity_tip"],
        "parity_ytd": policies["P2_T01_parity_ytd"],
        "L2AI_verdict": ai["verdict"],
        "L2AI_auc_tip": ai["auc_tip_oos"],
        "preferred_stack": preferred,
        "top5": ranked[:5],
    }
    (OUT / "P2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
