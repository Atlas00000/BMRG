"""DE40 M5 AIOS P2 — L2det shadow CF + L2skip_de40_m5 train + stack scorecard."""
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)
MODEL = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG"
    r"\infra\artefacts\models\L2skip_de40_m5\LATEST"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK_PRIOR = 0.07
LEAK_PROXY = 0.010667  # from P1 COST_PROXY (journal — report only)
ATR_MAX = 2380.0
BASELINE_EN = 0.207317  # tip May->Oct


def load(name: str) -> list[dict]:
    rows = []
    with (TAPES / name).open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["win"] = int(r["win"])
            r["hour"] = int(r["hour"])
            r["atr_pts"] = float(r["atr_pts"]) if r.get("atr_pts") else None
            r["spread_pts"] = int(r["spread_pts"])
            r["near_atr_cap"] = int(r["near_atr_cap"])
            r["cell_month_feb"] = int(r["cell_month_feb"])
            r["cell_month_may"] = int(r["cell_month_may"])
            r["cell_mismatch"] = int(r["cell_mismatch"])
            r["cell_fragile"] = int(r["cell_fragile"])
            r["cell_near_atr"] = int(r["cell_near_atr"])
            r["cell_buy"] = int(r["cell_buy"])
            r["cell_sell"] = int(r["cell_sell"])
            r["y_lose"] = int(r["y_lose"])
            r["month"] = r["month"]
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
            "EF_prior_pp": None,
            "EF_proxy_pp": None,
        }
    wr = sum(r["win"] for r in kept) / n
    bm = wr - BWR
    en = wr * (R + 1.0) - 1.0
    return {
        "n": n,
        "WR": round(wr, 6),
        "E_N": round(en, 6),
        "BM_pp": round(bm * 100, 4),
        "EF_prior_pp": round((bm - LEAK_PRIOR) * 100, 4),
        "EF_proxy_pp": round((bm - LEAK_PROXY) * 100, 4),
    }


def score_policy(rows: list[dict], skip_fn, name: str) -> dict:
    skipped = [r for r in rows if skip_fn(r)]
    kept = [r for r in rows if not skip_fn(r)]
    base = metrics(rows)
    after = metrics(kept)
    n_skip = len(skipped)
    losers_skipped = sum(1 for r in skipped if not r["win"])
    prec = (losers_skipped / n_skip) if n_skip else None
    # Protect-cell false positives (winners skipped)
    fp_aug = sum(1 for r in skipped if r["month"] == "2026-08" and r["win"])
    fp_sell = sum(1 for r in skipped if r["cell_sell"] and r["win"])
    fp_wed = sum(1 for r in skipped if r["dow"] == "Wed" and r["win"])
    fp_h08 = sum(1 for r in skipped if r["hour"] == 8 and r["win"])
    fp_h10 = sum(1 for r in skipped if r["hour"] == 10 and r["win"])
    fp_near = sum(1 for r in skipped if r["near_atr_cap"] and r["win"])
    ret = len(kept) / len(rows) if rows else 0.0
    d_en = None if after["E_N"] is None else round(after["E_N"] - base["E_N"], 6)
    d_ef = (
        None
        if after["EF_prior_pp"] is None
        else round(after["EF_prior_pp"] - base["EF_prior_pp"], 4)
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
        and fp_aug <= 2
        and fp_sell <= 3
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
        "ΔEF_prior_pp": d_ef,
        "fp_aug_winners": fp_aug,
        "fp_sell_winners": fp_sell,
        "fp_wed_winners": fp_wed,
        "fp_h08_winners": fp_h08,
        "fp_h10_winners": fp_h10,
        "fp_near_atr_winners": fp_near,
        "verdict": verdict,
    }


def parity(rows: list[dict]) -> dict:
    tue = sum(1 for r in rows if r["dow"] == "Tue")
    atr_breach = sum(
        1 for r in rows if r["atr_pts"] is not None and r["atr_pts"] > ATR_MAX
    )
    return {
        "tue_fires": tue,
        "atr_gt_2380": atr_breach,
        "verdict": "PASS" if tue == 0 and atr_breach == 0 else "FAIL",
    }


FEATS = [
    "hour",
    "spread_pts",
    "atr_pts",
    "near_atr_cap",
    "cell_month_feb",
    "cell_month_may",
    "cell_mismatch",
    "cell_fragile",
    "cell_buy",
    "cell_sell",
    "hour_14",
    "hour_16",
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
                r["cell_month_feb"],
                r["cell_month_may"],
                r["cell_mismatch"],
                r["cell_fragile"],
                r["cell_buy"],
                r["cell_sell"],
                int(r["hour"] == 14),
                int(r["hour"] == 16),
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
        "pin": "L2skip_de40_m5",
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
    tip = load("de40_m5_tip_fire_tape_v0.csv")
    prior = load("de40_m5_prior_fire_tape_v0.csv")
    ytd = load("de40_m5_ytd_fire_tape_v0.csv")

    def is_oct(r):
        return r["month"] == "2026-10"

    def is_sep_oct(r):
        return r["month"] in ("2026-09", "2026-10")

    def is_h14(r):
        return r["hour"] == 14

    def is_h16(r):
        return r["hour"] == 16

    def is_h14_16(r):
        return r["hour"] in (14, 16)

    policies = {
        "P2_T01_parity_tip": parity(tip),
        "P2_T01_parity_ytd": parity(ytd),
        # T02 hours / soft session
        "skip_H14": score_policy(tip, is_h14, "skip_H14"),
        "skip_H16": score_policy(tip, is_h16, "skip_H16"),
        "skip_H14_16": score_policy(tip, is_h14_16, "skip_H14_16"),
        "skip_H11": score_policy(tip, lambda r: r["hour"] == 11, "skip_H11"),
        # T03 side caution (tip sell-led -> BUY first)
        "skip_BUY": score_policy(tip, lambda r: r["cell_buy"] == 1, "skip_BUY"),
        "skip_SELL": score_policy(tip, lambda r: r["cell_sell"] == 1, "skip_SELL"),
        "skip_BUY_if_H14_16": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["hour"] in (14, 16),
            "skip_BUY_if_H14_16",
        ),
        "skip_BUY_if_H14": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["hour"] == 14,
            "skip_BUY_if_H14",
        ),
        "skip_BUY_if_H16": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["hour"] == 16,
            "skip_BUY_if_H16",
        ),
        "skip_BUY_if_fragile": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["cell_fragile"] == 1,
            "skip_BUY_if_fragile",
        ),
        "skip_BUY_if_near_atr": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["near_atr_cap"] == 1,
            "skip_BUY_if_near_atr",
        ),
        "skip_BUY_if_Oct": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and is_oct(r),
            "skip_BUY_if_Oct",
        ),
        "skip_BUY_if_MISMATCH": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["cell_mismatch"] == 1,
            "skip_BUY_if_MISMATCH",
        ),
        # T04 regime / FRAGILE
        "skip_Oct": score_policy(tip, is_oct, "skip_Oct"),
        "skip_Sep_Oct": score_policy(tip, is_sep_oct, "skip_Sep_Oct"),
        "skip_FRAGILE_all": score_policy(
            tip, lambda r: r["cell_fragile"] == 1, "skip_FRAGILE_all"
        ),
        "skip_MISMATCH_all": score_policy(
            tip, lambda r: r["cell_mismatch"] == 1, "skip_MISMATCH_all"
        ),
        "skip_May": score_policy(
            tip, lambda r: r["cell_month_may"] == 1, "skip_May"
        ),
        "skip_near_atr_all": score_policy(
            tip, lambda r: r["near_atr_cap"] == 1, "skip_near_atr_all"
        ),
        "skip_FRAGILE_and_near_atr": score_policy(
            tip,
            lambda r: r["cell_fragile"] == 1 and r["near_atr_cap"] == 1,
            "skip_FRAGILE_and_near_atr",
        ),
        "skip_Oct_OR_H14_16": score_policy(
            tip,
            lambda r: is_oct(r) or is_h14_16(r),
            "skip_Oct_OR_H14_16",
        ),
        # YTD support
        "ytd_skip_Feb": score_policy(
            ytd, lambda r: r["cell_month_feb"] == 1, "ytd_skip_Feb"
        ),
        "ytd_skip_Oct": score_policy(ytd, is_oct, "ytd_skip_Oct"),
        "ytd_skip_H14_16": score_policy(ytd, is_h14_16, "ytd_skip_H14_16"),
        "ytd_skip_BUY_if_H14_16": score_policy(
            ytd,
            lambda r: r["cell_buy"] == 1 and r["hour"] in (14, 16),
            "ytd_skip_BUY_if_H14_16",
        ),
    }

    ai = train_ai(prior, tip)
    tip_ai_skip = ai.pop("tip_ai_skip")
    best_thr = ai.pop("best_thr")

    def ai_skip(r):
        return tip_ai_skip.get(r["open_time"] + r["side"], False)

    # Candidate stacks
    stacks = {
        "P0_engine": score_policy(tip, lambda r: False, "P0_engine"),
        "L2det_H14_16": policies["skip_H14_16"],
        "L2det_Oct": policies["skip_Oct"],
        "L2det_BUY_H14_16": policies["skip_BUY_if_H14_16"],
        "L2det_BUY_fragile": policies["skip_BUY_if_fragile"],
        "L2det_Oct_OR_H14_16": policies["skip_Oct_OR_H14_16"],
        "L2det_v1_BUY_H14_16_OR_Oct": score_policy(
            tip,
            lambda r: (r["cell_buy"] == 1 and r["hour"] in (14, 16)) or is_oct(r),
            "L2det_v1_BUY_H14_16_OR_Oct",
        ),
        "L2det_v1b_BUY_H14_16_OR_BUY_Oct": score_policy(
            tip,
            lambda r: (r["cell_buy"] == 1 and r["hour"] in (14, 16))
            or (r["cell_buy"] == 1 and is_oct(r)),
            "L2det_v1b_BUY_H14_16_OR_BUY_Oct",
        ),
        "L2det_v1c_H14_16_OR_BUY_Oct": score_policy(
            tip,
            lambda r: is_h14_16(r) or (r["cell_buy"] == 1 and is_oct(r)),
            "L2det_v1c_H14_16_OR_BUY_Oct",
        ),
        "L2AI_only": score_policy(tip, ai_skip, f"L2AI_thr_{best_thr}"),
    }
    stacks["L2det_v1_OR_L2AI"] = score_policy(
        tip,
        lambda r: (
            (r["cell_buy"] == 1 and r["hour"] in (14, 16)) or is_oct(r)
        )
        or ai_skip(r),
        "L2det_v1_OR_L2AI",
    )
    stacks["L2det_v1b_OR_L2AI"] = score_policy(
        tip,
        lambda r: (
            (r["cell_buy"] == 1 and r["hour"] in (14, 16))
            or (r["cell_buy"] == 1 and is_oct(r))
        )
        or ai_skip(r),
        "L2det_v1b_OR_L2AI",
    )

    size_table = {
        "Expanding_Stable": 1.0,
        "Compressing": 0.5,
        "Near_frontier": 0.25,
        "Below_frontier": 0.0,
        "L2det_WOULD_SKIP": 0.0,
        "note": "Spec only — wire after L4. Skip outranks size.",
    }

    out = {
        "task": "DE40-M5-AOS-P2",
        "baseline_ref": "DE40_M5_AOS_BASELINE_v1",
        "Leak_source_authority": "prior_7.0pp",
        "Leak_proxy_pp": round(LEAK_PROXY * 100, 4),
        "tip_n": len(tip),
        "prior_n": len(prior),
        "ytd_n": len(ytd),
        "parity": {
            "tip": policies["P2_T01_parity_tip"],
            "ytd": policies["P2_T01_parity_ytd"],
        },
        "policies": {k: v for k, v in policies.items() if not k.startswith("P2_T01")},
        "L2AI": ai,
        "stacks": stacks,
        "P2_T05_size_table": size_table,
    }
    (OUT / "P2_CF.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Pick preferred by max ΔE_N among ARM_SOFT / HOLD_SOFT with ret>=70% and fp_aug<=2
    candidates = []
    for k, v in stacks.items():
        if k == "P0_engine":
            continue
        if v.get("verdict") in ("ARM_SOFT", "HOLD_SOFT") and v.get("ΔE_N") is not None:
            if v["fire_retention_pct"] >= 70 and v["fp_aug_winners"] <= 2:
                candidates.append((k, v))
    candidates.sort(key=lambda x: x[1]["ΔE_N"], reverse=True)
    preferred_name = candidates[0][0] if candidates else "L2det_v1_BUY_H14_16_OR_Oct"
    preferred = stacks[preferred_name]

    summary = {
        "parity": out["parity"],
        "preferred_stack": preferred_name,
        "preferred": preferred,
        "top_candidates": [
            {
                "name": n,
                "verdict": v["verdict"],
                "ΔE_N": v["ΔE_N"],
                "ret": v["fire_retention_pct"],
                "prec": v["precision_losers"],
                "fp_aug": v["fp_aug_winners"],
                "fp_sell": v["fp_sell_winners"],
            }
            for n, v in candidates[:8]
        ],
        "L2AI_verdict": ai["verdict"],
        "L2AI_auc_tip": ai["auc_tip_oos"],
        "key_policies": {
            k: {
                "verdict": policies[k]["verdict"],
                "ΔE_N": policies[k]["ΔE_N"],
                "ret": policies[k]["fire_retention_pct"],
                "prec": policies[k]["precision_losers"],
                "fp_aug": policies[k]["fp_aug_winners"],
                "fp_sell": policies[k]["fp_sell_winners"],
            }
            for k in (
                "skip_H14_16",
                "skip_Oct",
                "skip_BUY",
                "skip_BUY_if_H14_16",
                "skip_BUY_if_near_atr",
                "skip_near_atr_all",
                "skip_MISMATCH_all",
                "skip_Sep_Oct",
                "ytd_skip_Feb",
            )
        },
    }
    (OUT / "P2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
