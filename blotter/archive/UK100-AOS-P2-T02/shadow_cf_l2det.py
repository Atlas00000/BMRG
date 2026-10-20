"""UK100-AOS-P2-T01/T02 — parity + Thu/H08 SOFT skip shadow CF."""
from __future__ import annotations

import csv
import json
from pathlib import Path

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
OUT = Path(__file__).resolve().parent

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK_PROXY = 0.042667  # journal 2x entry spread tip
ATR_MAX = 1470.0


def load(name: str) -> list[dict]:
    path = TAPES / name
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["win"] = int(r["win"])
        r["hour"] = int(r["hour"])
        r["atr_pts"] = float(r["atr_pts"]) if r["atr_pts"] else None
        r["pnl_R_design"] = float(r["pnl_R_design"])
        for k in (
            "cell_dow_thu",
            "cell_hour_08",
            "cell_month_jul",
            "cell_buy",
            "near_atr_cap",
            "nights_held",
        ):
            r[k] = int(r[k])
    return rows


def score(rows: list[dict], label: str) -> dict:
    n = len(rows)
    if n == 0:
        return {"label": label, "n": 0}
    wins = sum(r["win"] for r in rows)
    wr = wins / n
    bm = wr - BWR
    en = wr * (R + 1) - 1
    ef = bm - LEAK_PROXY
    avg_r = sum(r["pnl_R_design"] for r in rows) / n
    wed = [r for r in rows if r["dow"] == "Wed"]
    wed_wr = (sum(r["win"] for r in wed) / len(wed)) if wed else None
    return {
        "label": label,
        "n": n,
        "wins": wins,
        "losses": n - wins,
        "WR": round(wr * 100, 2),
        "BM_pp": round(bm * 100, 3),
        "E_N": round(en, 4),
        "EF_proxy_pp": round(ef * 100, 3),
        "avgR": round(avg_r, 4),
        "wed_n": len(wed),
        "wed_WR": round(wed_wr * 100, 2) if wed_wr is not None else None,
    }


def skip_stats(base: list[dict], skipped: list[dict]) -> dict:
    n_skip = len(skipped)
    if n_skip == 0:
        return {
            "skips_n": 0,
            "precision_vs_losers": None,
            "recall_losers": None,
            "false_skip_winners": 0,
            "false_skip_wed_winners": 0,
            "false_skip_sell_winners": 0,
        }
    losers_skipped = sum(1 for r in skipped if r["win"] == 0)
    winners_skipped = sum(1 for r in skipped if r["win"] == 1)
    base_losers = sum(1 for r in base if r["win"] == 0)
    wed_w_skip = sum(1 for r in skipped if r["dow"] == "Wed" and r["win"] == 1)
    sell_w_skip = sum(1 for r in skipped if r["side"] == "SELL" and r["win"] == 1)
    return {
        "skips_n": n_skip,
        "precision_vs_losers": round(losers_skipped / n_skip, 4),
        "recall_losers": round(losers_skipped / base_losers, 4) if base_losers else None,
        "false_skip_winners": winners_skipped,
        "false_skip_wed_winners": wed_w_skip,
        "false_skip_sell_winners": sell_w_skip,
        "skipped_breakdown": {
            "Thu": sum(1 for r in skipped if r["cell_dow_thu"]),
            "H08": sum(1 for r in skipped if r["cell_hour_08"]),
            "Thu_and_H08": sum(
                1 for r in skipped if r["cell_dow_thu"] and r["cell_hour_08"]
            ),
        },
    }


def apply(base: list[dict], pred) -> tuple[list[dict], list[dict]]:
    kept, skipped = [], []
    for r in base:
        if pred(r):
            skipped.append(r)
        else:
            kept.append(r)
    return kept, skipped


def verdict(base_s: dict, kept_s: dict, skip_s: dict) -> str:
    if kept_s["n"] == 0:
        return "REJECT"
    # iteration bar
    en_ok = kept_s["E_N"] >= base_s["E_N"] - 1e-9  # E_N hold preferred
    # EF: allow -1 pp vs baseline EF
    ef_ok = kept_s["EF_proxy_pp"] >= base_s["EF_proxy_pp"] - 1.0
    retention = kept_s["n"] / base_s["n"]
    ret_ok = retention >= 0.50
    # improve E_N or at least hold with better EF
    improved = kept_s["E_N"] > base_s["E_N"] + 1e-9
    # reject if WR up but E_N down
    if kept_s["WR"] > base_s["WR"] and kept_s["E_N"] < base_s["E_N"] - 1e-9:
        return "REJECT"
    if not ret_ok:
        return "REJECT_FREQUENCY_STALL"
    if not ef_ok and not en_ok:
        return "REJECT"
    if improved and ef_ok and skip_s["precision_vs_losers"] is not None:
        if skip_s["precision_vs_losers"] >= 0.55:
            return "ARM_SOFT"
        return "HOLD_SOFT"
    if en_ok and ef_ok and skip_s["skips_n"] > 0:
        return "HOLD_SOFT"
    return "DISARM"


def parity(tip: list[dict], prior: list[dict]) -> dict:
    both = tip + prior
    tue = [r for r in both if r["dow"] == "Tue"]
    atr_over = [
        r for r in both if r["atr_pts"] is not None and r["atr_pts"] > ATR_MAX
    ]
    return {
        "task": "UK100-AOS-P2-T01",
        "tue_fires": len(tue),
        "fires_with_atr_gt_max": len(atr_over),
        "near_atr_cap_fires": sum(r["near_atr_cap"] for r in both),
        "parity_tue": "PASS" if len(tue) == 0 else "FAIL",
        "parity_atr_note": (
            "Engine ATR max gates entries; fires may still show atr>max on "
            "the signal bar after entry or gate timing. Count atr>max on tape "
            "is diagnostic only."
        ),
        "atr_gt_max_detail": [
            {
                "open_time": r["open_time"],
                "atr": r["atr_pts"],
                "win": r["win"],
                "window": r["window"],
            }
            for r in atr_over[:20]
        ],
    }


def main() -> None:
    tip = load("uk100_tip_fire_tape_v0.csv")
    prior = load("uk100_prior_fire_tape_v0.csv")
    base = score(tip, "baseline_tip")

    policies = {
        "skip_Thu": lambda r: r["cell_dow_thu"] == 1,
        "skip_H08": lambda r: r["cell_hour_08"] == 1,
        "skip_Thu_OR_H08": lambda r: r["cell_dow_thu"] == 1 or r["cell_hour_08"] == 1,
        "skip_Thu_AND_H08": lambda r: r["cell_dow_thu"] == 1 and r["cell_hour_08"] == 1,
    }

    results = {
        "task": "UK100-AOS-P2-T02",
        "Leak_source": "journal_2x_entry_spread_median",
        "Leak_proxy_pp": LEAK_PROXY * 100,
        "baseline": base,
        "parity": parity(tip, prior),
        "policies": {},
    }

    for name, pred in policies.items():
        kept, skipped = apply(tip, pred)
        ks = score(kept, name + "_kept")
        ss = skip_stats(tip, skipped)
        v = verdict(base, ks, ss)
        results["policies"][name] = {
            "kept": ks,
            "skips": ss,
            "delta_E_N": round(ks["E_N"] - base["E_N"], 4),
            "delta_EF_pp": round(ks["EF_proxy_pp"] - base["EF_proxy_pp"], 3),
            "fire_retention_pct": round(100.0 * ks["n"] / base["n"], 1),
            "verdict": v,
        }

    # prior diagnostic for best tip policy (informational)
    best_name = max(
        results["policies"],
        key=lambda k: (
            results["policies"][k]["verdict"] == "ARM_SOFT",
            results["policies"][k]["delta_E_N"],
            results["policies"][k]["delta_EF_pp"],
        ),
    )
    results["recommended_for_shadow"] = best_name

    # also score prior under Thu_OR_H08
    kept_p, skip_p = apply(prior, policies["skip_Thu_OR_H08"])
    results["prior_diag_skip_Thu_OR_H08"] = {
        "baseline_prior": score(prior, "baseline_prior"),
        "kept": score(kept_p, "prior_kept"),
        "skips": skip_stats(prior, skip_p),
        "note": "Diagnostic only — tip is OS compare window",
    }

    out_json = OUT / "SHADOW_CF.json"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
