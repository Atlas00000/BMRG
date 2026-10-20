"""UK100 M5 AIOS P2 — L2det shadow CF + L2skip_uk_m5 train + stack scorecard."""
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
MODEL = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG"
    r"\infra\artefacts\models\L2skip_uk_m5\LATEST"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK_PROXY = 0.059259  # 5.9259 pp from P1 COST_PROXY
ATR_MAX = 869.0
BASELINE_EN = 0.18319


def load(name: str) -> list[dict]:
    rows = []
    with (TAPES / name).open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["win"] = int(r["win"])
            r["hour"] = int(r["hour"])
            r["atr_pts"] = float(r["atr_pts"]) if r["atr_pts"] else None
            r["spread_pts"] = int(r["spread_pts"])
            r["near_atr_cap"] = int(r["near_atr_cap"])
            r["cell_dow_mon"] = int(r["cell_dow_mon"])
            r["cell_hour_12_13"] = int(r["cell_hour_12_13"])
            r["cell_month_aug"] = int(r["cell_month_aug"])
            r["cell_month_feb"] = int(r["cell_month_feb"])
            r["cell_month_apr"] = int(r["cell_month_apr"])
            r["cell_buy"] = int(r["cell_buy"])
            r["cell_sell"] = int(r["cell_sell"])
            r["y_lose"] = int(r["y_lose"])
            rows.append(r)
    return rows


def metrics(kept: list[dict]) -> dict:
    n = len(kept)
    if n == 0:
        return {"n": 0, "WR": None, "E_N": None, "BM_pp": None, "EF_proxy_pp": None}
    wr = sum(r["win"] for r in kept) / n
    bm = wr - BWR
    en = wr * (R + 1.0) - 1.0
    return {
        "n": n,
        "WR": round(wr, 6),
        "E_N": round(en, 6),
        "BM_pp": round(bm * 100, 4),
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
    # protect-cell false positives = winners skipped in protect sets
    fp_wed = sum(1 for r in skipped if r["dow"] == "Wed" and r["win"])
    fp_h08_11 = sum(
        1 for r in skipped if r["hour"] in (8, 9, 10, 11) and r["win"]
    )
    fp_buy = sum(1 for r in skipped if r["cell_buy"] and r["win"])
    ret = len(kept) / len(rows) if rows else 0.0
    d_en = None if after["E_N"] is None else round(after["E_N"] - base["E_N"], 6)
    d_ef = (
        None
        if after["EF_proxy_pp"] is None
        else round(after["EF_proxy_pp"] - base["EF_proxy_pp"], 4)
    )

    # iteration bar soft verdict
    verdict = "HOLD_SOFT"
    if n_skip == 0:
        verdict = "NO_OP"
    elif after["E_N"] is not None and after["E_N"] < BASELINE_EN - 0.05:
        verdict = "REJECT"
    elif ret < 0.50:
        verdict = "REJECT_FREQUENCY_STALL"
    elif d_en is not None and d_en < -0.02:
        verdict = "REJECT"
    elif d_en is not None and d_en >= 0.02 and (prec or 0) >= 0.55 and fp_wed <= 2:
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
        "ΔEF_proxy_pp": d_ef,
        "fp_wed_winners": fp_wed,
        "fp_h08_11_winners": fp_h08_11,
        "fp_buy_winners": fp_buy,
        "verdict": verdict,
    }


def parity(rows: list[dict]) -> dict:
    tue = sum(1 for r in rows if r["dow"] == "Tue")
    atr_breach = sum(
        1 for r in rows if r["atr_pts"] is not None and r["atr_pts"] > ATR_MAX
    )
    return {
        "tue_fires": tue,
        "atr_gt_869": atr_breach,
        "verdict": "PASS" if tue == 0 and atr_breach == 0 else "FAIL",
    }


FEATS = [
    "hour",
    "spread_pts",
    "atr_pts",
    "near_atr_cap",
    "cell_dow_mon",
    "cell_hour_12_13",
    "cell_month_aug",
    "cell_month_feb",
    "cell_month_apr",
    "cell_buy",
    "cell_sell",
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
                r["cell_dow_mon"],
                r["cell_hour_12_13"],
                r["cell_month_aug"],
                r["cell_month_feb"],
                r["cell_month_apr"],
                r["cell_buy"],
                r["cell_sell"],
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
        def skip_fn(r, i=None, t=thr, probs=tip_proba, rows=tip):
            # bind by index — rebuild with zip
            return False

        # rebuild skip via parallel arrays
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
        "train": "prior Jan-Apr n=119",
        "auc_prior": auc_prior,
        "auc_tip_oos": auc_tip,
        "best_thr_tip": best,
        "status": "SHADOW_ONLY",
        "pin": "L2skip_uk_m5",
    }
    (MODEL / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    np.save(MODEL / "coef.npy", clf.coef_)
    np.save(MODEL / "intercept.npy", clf.intercept_)
    np.save(MODEL / "scaler_mean.npy", scaler.mean_)
    np.save(MODEL / "scaler_scale.npy", scaler.scale_)

    # attach tip proba skip at best thr for stack
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
    tip = load("uk100_m5_tip_fire_tape_v0.csv")
    prior = load("uk100_m5_prior_fire_tape_v0.csv")

    policies = {
        "P2_T01_parity_tip": parity(tip),
        "P2_T01_parity_prior": parity(prior),
        # T02
        "skip_Mon": score_policy(
            tip, lambda r: r["cell_dow_mon"] == 1, "skip_Mon"
        ),
        "skip_H12_13": score_policy(
            tip, lambda r: r["cell_hour_12_13"] == 1, "skip_H12_13"
        ),
        "skip_Mon_OR_H12_13": score_policy(
            tip,
            lambda r: r["cell_dow_mon"] == 1 or r["cell_hour_12_13"] == 1,
            "skip_Mon_OR_H12_13",
        ),
        "skip_Mon_AND_H12_13": score_policy(
            tip,
            lambda r: r["cell_dow_mon"] == 1 and r["cell_hour_12_13"] == 1,
            "skip_Mon_AND_H12_13",
        ),
        # T03 side
        "skip_SELL": score_policy(
            tip, lambda r: r["cell_sell"] == 1, "skip_SELL"
        ),
        "skip_SELL_if_H12_13": score_policy(
            tip,
            lambda r: r["cell_sell"] == 1 and r["cell_hour_12_13"] == 1,
            "skip_SELL_if_H12_13",
        ),
        "skip_SELL_if_Mon": score_policy(
            tip,
            lambda r: r["cell_sell"] == 1 and r["cell_dow_mon"] == 1,
            "skip_SELL_if_Mon",
        ),
        "skip_SELL_if_near_atr": score_policy(
            tip,
            lambda r: r["cell_sell"] == 1 and r["near_atr_cap"] == 1,
            "skip_SELL_if_near_atr",
        ),
        "skip_BUY": score_policy(
            tip, lambda r: r["cell_buy"] == 1, "skip_BUY"
        ),
        "skip_BUY_if_near_atr": score_policy(
            tip,
            lambda r: r["cell_buy"] == 1 and r["near_atr_cap"] == 1,
            "skip_BUY_if_near_atr",
        ),
        # T04 stress
        "skip_Aug": score_policy(
            tip, lambda r: r["cell_month_aug"] == 1, "skip_Aug"
        ),
        "skip_near_atr_all": score_policy(
            tip, lambda r: r["near_atr_cap"] == 1, "skip_near_atr_all"
        ),
        "skip_Mon_OR_Aug": score_policy(
            tip,
            lambda r: r["cell_dow_mon"] == 1 or r["cell_month_aug"] == 1,
            "skip_Mon_OR_Aug",
        ),
        "skip_H12_13_OR_Aug": score_policy(
            tip,
            lambda r: r["cell_hour_12_13"] == 1 or r["cell_month_aug"] == 1,
            "skip_H12_13_OR_Aug",
        ),
        # prior diagnostics
        "prior_skip_Feb": score_policy(
            prior, lambda r: r["cell_month_feb"] == 1, "prior_skip_Feb"
        ),
        "prior_skip_Apr": score_policy(
            prior, lambda r: r["cell_month_apr"] == 1, "prior_skip_Apr"
        ),
        "prior_skip_Mon": score_policy(
            prior, lambda r: r["cell_dow_mon"] == 1, "prior_skip_Mon"
        ),
        "prior_skip_H12_13": score_policy(
            prior, lambda r: r["cell_hour_12_13"] == 1, "prior_skip_H12_13"
        ),
    }

    # Preferred stacks to evaluate after initial sweep — fill after seeing results
    # Candidate v1: H12-13 alone; v1b: H12-13 OR Mon; v1c: H12-13 OR Aug

    ai = train_ai(prior, tip)
    tip_ai_skip = ai.pop("tip_ai_skip")
    best_thr = ai.pop("best_thr")

    # Stack CF
    def ai_skip(r):
        return tip_ai_skip.get(r["open_time"] + r["side"], False)

    stacks = {
        "P0_engine": score_policy(tip, lambda r: False, "P0_engine"),
        "L2det_H12_13": policies["skip_H12_13"],
        "L2det_Mon": policies["skip_Mon"],
        "L2det_Mon_OR_H12_13": policies["skip_Mon_OR_H12_13"],
        "L2det_H12_13_OR_Aug": policies["skip_H12_13_OR_Aug"],
        "L2det_Mon_OR_Aug": policies["skip_Mon_OR_Aug"],
        "L2AI_only": score_policy(tip, ai_skip, f"L2AI_thr_{best_thr}"),
    }
    # OR / AND with best det (pick H12_13 as primary candidate for stack)
    stacks["L2det_H12_13_OR_L2AI"] = score_policy(
        tip,
        lambda r: r["cell_hour_12_13"] == 1 or ai_skip(r),
        "L2det_H12_13_OR_L2AI",
    )
    stacks["L2det_H12_13_AND_L2AI"] = score_policy(
        tip,
        lambda r: r["cell_hour_12_13"] == 1 and ai_skip(r),
        "L2det_H12_13_AND_L2AI",
    )
    # Preferred v1b: (Mon∧H12-13) ∨ (SELL∧H12-13) — high ΔE_N, protects BUY mornings
    stacks["L2det_v1b_MonAndH12_OR_SellAndH12"] = score_policy(
        tip,
        lambda r: (r["cell_dow_mon"] == 1 and r["cell_hour_12_13"] == 1)
        or (r["cell_sell"] == 1 and r["cell_hour_12_13"] == 1),
        "L2det_v1b_MonAndH12_OR_SellAndH12",
    )
    stacks["L2det_v1b2_MonAndH12_OR_SellNearAtr"] = score_policy(
        tip,
        lambda r: (r["cell_dow_mon"] == 1 and r["cell_hour_12_13"] == 1)
        or (r["cell_sell"] == 1 and r["near_atr_cap"] == 1),
        "L2det_v1b2_MonAndH12_OR_SellNearAtr",
    )
    stacks["L2det_SELL_AND_H12_13"] = policies["skip_SELL_if_H12_13"]
    stacks["L2det_Mon_AND_H12_13"] = policies["skip_Mon_AND_H12_13"]
    # Aggressive full midday (Wed FP higher)
    stacks["L2det_v1_H12_13_aggressive"] = policies["skip_H12_13"]
    # Freq-stall unions (document reject)
    stacks["L2det_Mon_OR_H12_13"] = policies["skip_Mon_OR_H12_13"]
    stacks["L2det_H12_OR_Aug"] = policies["skip_H12_13_OR_Aug"]

    size_table = {
        "Expanding_Stable": 1.0,
        "Compressing": 0.5,
        "Near_frontier": 0.25,
        "Below_frontier": 0.0,
        "L2det_WOULD_SKIP": 0.0,
        "note": "Spec only — wire after L4. Skip outranks size.",
    }

    out = {
        "task": "UK100-M5-AOS-P2",
        "baseline_ref": "UK100_M5_AOS_BASELINE_v1",
        "Leak_source": "journal_2x_entry_spread_median",
        "Leak_proxy_pp": 5.9259,
        "tip_n": len(tip),
        "prior_n": len(prior),
        "parity": {
            "tip": policies["P2_T01_parity_tip"],
            "prior": policies["P2_T01_parity_prior"],
        },
        "policies": {k: v for k, v in policies.items() if not k.startswith("P2_T01")},
        "L2AI": ai,
        "stacks": stacks,
        "P2_T05_size_table": size_table,
    }
    (OUT / "P2_CF.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    summary = {
        "parity": out["parity"],
        "preferred_stack": "L2det_v1b_MonAndH12_OR_SellAndH12",
        "preferred": stacks["L2det_v1b_MonAndH12_OR_SellAndH12"],
        "L2AI_verdict": ai["verdict"],
        "L2AI_auc_tip": ai["auc_tip_oos"],
    }
    (OUT / "P2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
