"""
GRP-P4 — tail co-loss · Pareto front · surrogate ranker on OOS-stable groups.

Usage (from infra/):
  python -m src.grouping.run_p4
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from src.diversify.dependence import pairwise_coloss
from src.diversify.score import fuse_days, score_cluster

from .load_panel import build_panel
from .pareto import label_policies, pareto_front
from .surrogate import fit_surrogate
from .tail import escalate_from_tail, group_max_tail, pairwise_tail
from .universe import HARD_BAN_PAIRS, P2_SLEEVES, REPO, SOFT_PENALTY_PAIRS

OUT_P2 = REPO / "infra" / "artefacts" / "grouping" / "P2_LATEST"
OUT_P1 = REPO / "infra" / "artefacts" / "grouping" / "P1_LATEST"
OUT_P4 = REPO / "infra" / "artefacts" / "grouping" / "P4_LATEST"
ARCHIVE_P4 = REPO / "blotter" / "archive" / "GRP-P4-T01"


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols: list[str] = []
    seen: set[str] = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _members(g: dict) -> list[str]:
    m = g.get("members")
    if isinstance(m, str):
        return m.split("|")
    return list(m or [])


def _pair_lookup(coloss: list[dict]) -> dict[frozenset[str], dict]:
    return {frozenset((r["a"], r["b"])): r for r in coloss}


def enrich_group(
    g: dict,
    panel,
    tail_rows: list[dict],
    coloss_map: dict,
) -> dict:
    members = _members(g)
    # refresh path metrics on equal weight for consistent Pareto inputs
    sc = score_cluster(panel, tuple(members))
    mx_tail = group_max_tail(members, tail_rows)
    pair_cols = []
    pair_corrs = []
    for i, a in enumerate(members):
        for b in members[i + 1 :]:
            row = coloss_map.get(frozenset((a, b)))
            if not row:
                continue
            if row.get("co_loss_rate") is not None:
                pair_cols.append(row["co_loss_rate"])
            if row.get("corr_active") is not None:
                pair_corrs.append(row["corr_active"])
    max_coloss = max(pair_cols) if pair_cols else None
    mean_corr = float(np.mean(pair_corrs)) if pair_corrs else None
    return {
        "group_id": g.get("group_id") or "+".join(members),
        "k": len(members),
        "members": members,
        "month_hit": sc.get("month_hit"),
        "quarter_hit": sc.get("quarter_hit"),
        "sum_R": sc.get("sum_R"),
        "E_month": sc.get("mean_daily_R"),  # placeholder; overwrite below
        "CVaR_m20": sc.get("CVaR_m20"),
        "maxDD": sc.get("maxDD"),
        "fuse_days": fuse_days(panel, tuple(members)),
        "worst_month": sc.get("worst_month"),
        "n_months": sc.get("n_months"),
        "val_sum_R": (g.get("holdout") or {}).get("val_sum_R"),
        "boot_month_hit_p10": g.get("boot_month_hit_p10"),
        "max_tail_dep": mx_tail,
        "max_coloss": max_coloss,
        "mean_pair_corr": None if mean_corr is None else round(mean_corr, 4),
        "oos_pass": g.get("oos_pass", True),
    }


def _fix_e_month(panel, members: list[str]) -> float | None:
    from src.diversify.score import portfolio_series
    import pandas as pd

    rp = portfolio_series(panel, tuple(members))
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    monthly = s.resample("ME").sum()
    monthly = monthly[monthly.abs() > 1e-12]
    if len(monthly) == 0:
        return None
    return round(float(monthly.mean()), 4)


def run(sleeves_dir: Path | None = None) -> dict:
    p2_path = OUT_P2 / "ACCEPTABLE_RANGE.json"
    fail_path = OUT_P2 / "OOS_FAILED.json"
    if not p2_path.exists():
        raise SystemExit(f"Missing {p2_path} — run run_bootstrap first")

    panel = build_panel(sleeves_dir or P2_SLEEVES)
    p2 = _load_json(p2_path)
    stable = p2.get("groups") or []
    failed = []
    if fail_path.exists():
        failed = _load_json(fail_path).get("groups") or []

    # --- T03 tail ---
    tail_rows = pairwise_tail(panel, q=0.2, min_n=8)
    coloss = pairwise_coloss(panel)
    coloss_map = _pair_lookup(coloss)
    hard = set(HARD_BAN_PAIRS)
    soft = set(SOFT_PENALTY_PAIRS)
    # include P1 soft JP225+AAPL if present in ban matrix
    if OUT_P1.exists() and (OUT_P1 / "BAN_MATRIX.json").exists():
        bm = _load_json(OUT_P1 / "BAN_MATRIX.json")
        for p in bm.get("soft_penalty_pairs") or []:
            soft.add(frozenset(p))
        for p in bm.get("hard_ban_pairs") or []:
            hard.add(frozenset(p))
    escalations = escalate_from_tail(tail_rows, soft_pairs=soft, hard_pairs=hard)

    # enrich stable + failed for surrogate / pareto
    enriched_stable = []
    for g in stable:
        e = enrich_group(g, panel, tail_rows, coloss_map)
        e["E_month"] = _fix_e_month(panel, e["members"])
        enriched_stable.append(e)

    enriched_fail = []
    for g in failed:
        e = enrich_group(g, panel, tail_rows, coloss_map)
        e["E_month"] = _fix_e_month(panel, e["members"])
        e["oos_pass"] = False
        enriched_fail.append(e)

    # --- T01 Pareto on stable ---
    front = label_policies(pareto_front(enriched_stable))
    front_ids = {r["group_id"] for r in front}

    # mark dominated
    for e in enriched_stable:
        e["on_pareto_front"] = e["group_id"] in front_ids

    # --- T02 surrogate on stable+fail ---
    sur = fit_surrogate(enriched_stable + enriched_fail)
    pred_map = {}
    if sur.get("ok"):
        pred_map = {p["group_id"]: p for p in sur["predictions"]}
        for e in enriched_stable:
            p = pred_map.get(e["group_id"])
            if p:
                e["surrogate"] = p

    generated = datetime.now(timezone.utc).isoformat()
    scorecard = {
        "task_id": "GRP-P4-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "caveat": (
            "P4 enhances OOS-stable tip groups: lower-tail dep (q=0.2), "
            "Pareto on hit/E/CVaR/DD/fuse/tail, ridge surrogate LOO. "
            "Does not invent membership. Not a live attach."
        ),
        "n_oos_stable": len(enriched_stable),
        "n_pareto": len(front),
        "tail": {
            "q": 0.2,
            "n_pairs": len(tail_rows),
            "escalations": escalations,
            "top_tail_pairs": tail_rows[:10],
        },
        "surrogate": {
            "ok": sur.get("ok"),
            "n": sur.get("n"),
            "loo_r2": sur.get("loo_r2"),
            "rmse": sur.get("rmse"),
            "coefficients": sur.get("coefficients"),
            "n_fragile_flags": sum(
                1 for p in (sur.get("predictions") or []) if p.get("fragile_flag")
            ),
            "n_optimistic_flags": sum(
                1 for p in (sur.get("predictions") or []) if p.get("optimistic_flag")
            ),
        },
        "policy_champions": {
            r["policy_label"]: r["group_id"]
            for r in front
            if r.get("policy_label")
        },
    }

    acceptable = {
        "task_id": "GRP-P4-T01",
        "generated_utc": generated,
        "n_pareto": len(front),
        "pareto_front": front,
        "oos_stable_enriched": enriched_stable,
    }

    OUT_P4.mkdir(parents=True, exist_ok=True)
    ARCHIVE_P4.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_P4 / "SCORECARD.json", scorecard)
    _write_json(OUT_P4 / "ACCEPTABLE_RANGE.json", acceptable)
    _write_json(OUT_P4 / "TAIL_PAIRS.json", {"q": 0.2, "pairs": tail_rows, "escalations": escalations})
    _write_json(OUT_P4 / "PARETO_FRONT.json", {"n": len(front), "groups": front})
    _write_json(OUT_P4 / "SURROGATE.json", sur)

    _write_csv(
        OUT_P4 / "tail_pairs.csv",
        [
            {
                "a": r["a"],
                "b": r["b"],
                "n_both": r["n_both_active"],
                "co_loss": r.get("co_loss_rate"),
                "tail_dep_q": r.get("tail_dep_q"),
                "corr": r.get("corr"),
                "joint_neg_days": r.get("joint_neg_days"),
            }
            for r in tail_rows
        ],
    )
    _write_csv(
        OUT_P4 / "PARETO_TABLE.csv",
        [
            {
                "group_id": r["group_id"],
                "k": r["k"],
                "members": "|".join(r["members"]),
                "policy_label": r.get("policy_label"),
                "month_hit": r.get("month_hit"),
                "quarter_hit": r.get("quarter_hit"),
                "sum_R": r.get("sum_R"),
                "E_month": r.get("E_month"),
                "CVaR_m20": r.get("CVaR_m20"),
                "maxDD": r.get("maxDD"),
                "fuse_days": r.get("fuse_days"),
                "max_tail_dep": r.get("max_tail_dep"),
                "val_sum_R": r.get("val_sum_R"),
            }
            for r in front
        ],
    )
    _write_csv(
        OUT_P4 / "OOS_ENRICHED.csv",
        [
            {
                "group_id": e["group_id"],
                "on_pareto": e.get("on_pareto_front"),
                "month_hit": e.get("month_hit"),
                "sum_R": e.get("sum_R"),
                "max_tail_dep": e.get("max_tail_dep"),
                "max_coloss": e.get("max_coloss"),
                "val_sum_R": e.get("val_sum_R"),
                "pred_hit": (e.get("surrogate") or {}).get("month_hit_pred"),
                "optimistic": (e.get("surrogate") or {}).get("optimistic_flag"),
            }
            for e in enriched_stable
        ],
    )

    review = _review(scorecard, front, escalations, sur, enriched_stable)
    (OUT_P4 / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in (
        "SCORECARD.json",
        "ACCEPTABLE_RANGE.json",
        "TAIL_PAIRS.json",
        "PARETO_FRONT.json",
        "SURROGATE.json",
        "tail_pairs.csv",
        "PARETO_TABLE.csv",
        "OOS_ENRICHED.csv",
        "REVIEW.md",
    ):
        src = OUT_P4 / name
        if src.exists():
            shutil.copy2(src, ARCHIVE_P4 / name)

    print(
        f"P4 tail pairs={len(tail_rows)} escalate_hard={len(escalations['escalate_hard'])} "
        f"new_soft={len(escalations['new_soft'])}"
    )
    print(f"Pareto front n={len(front)} · champions={scorecard['policy_champions']}")
    if sur.get("ok"):
        print(f"Surrogate LOO R2={sur.get('loo_r2')} rmse={sur.get('rmse')}")
    print(f"Wrote {OUT_P4}")
    print(f"Archived {ARCHIVE_P4}")
    return {"scorecard": scorecard, "front": front}


def _review(scorecard, front, escalations, sur, enriched) -> str:
    lines = [
        "# GRP-P4-T01 — Tail · Pareto · Surrogate",
        "",
        f"**generated_utc:** {scorecard['generated_utc']}",
        f"**OOS-stable:** {scorecard['n_oos_stable']} · **Pareto front:** {scorecard['n_pareto']}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## T03 — Tail dependence (q=0.2)",
        "",
        f"Escalate→hard: {len(escalations.get('escalate_hard') or [])} · "
        f"New soft: {len(escalations.get('new_soft') or [])}",
        "",
        "| a | b | co_loss | tail_dep | corr | action |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    actions = {
        frozenset((r["a"], r["b"])): r["action"]
        for r in (escalations.get("escalate_hard") or [])
        + (escalations.get("new_soft") or [])
    }
    for r in (scorecard.get("tail") or {}).get("top_tail_pairs") or []:
        key = frozenset((r["a"], r["b"]))
        lines.append(
            f"| {r['a']} | {r['b']} | {r.get('co_loss_rate')} | "
            f"{r.get('tail_dep_q')} | {r.get('corr')} | {actions.get(key, '—')} |"
        )

    lines += [
        "",
        "## T01 — Pareto front (policy champions)",
        "",
        f"Champions: `{scorecard.get('policy_champions')}`",
        "",
        "| Group | policy | m_hit | sum_R | CVaR | maxDD | tail | val_sum |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in front:
        lines.append(
            f"| {r['group_id']} | {r.get('policy_label') or '—'} | "
            f"{r.get('month_hit')} | {r.get('sum_R')} | {r.get('CVaR_m20')} | "
            f"{r.get('maxDD')} | {r.get('max_tail_dep')} | {r.get('val_sum_R')} |"
        )

    lines += [
        "",
        "## T02 — Surrogate",
        "",
    ]
    if sur.get("ok"):
        lines.append(
            f"LOO R²={sur.get('loo_r2')} · RMSE={sur.get('rmse')} · n={sur.get('n')}"
        )
        lines.append("")
        lines.append("Top |coef| features:")
        coefs = sorted(
            (sur.get("coefficients") or {}).items(),
            key=lambda kv: abs(kv[1]),
            reverse=True,
        )
        for name, c in coefs[:8]:
            lines.append(f"- `{name}`: {c}")
        opt = [p for p in sur.get("predictions") or [] if p.get("optimistic_flag")]
        if opt:
            lines += ["", "Optimistic flags (obs hit >> pred):", ""]
            for p in opt[:8]:
                lines.append(
                    f"- {p['group_id']}: obs={p['month_hit_obs']} pred={p['month_hit_pred']}"
                )
    else:
        lines.append(f"Surrogate skipped: {sur}")

    lines += [
        "",
        "## Next",
        "",
        "1. GRP-P5 HITL — pick from Pareto champions + equal weights (P3).",
        "2. Apply any tail escalate_hard into ban matrix before live attach.",
        "",
        "Artefacts: `infra/artefacts/grouping/P4_LATEST/` · "
        "`blotter/archive/GRP-P4-T01/`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="GRP-P4 tail / Pareto / surrogate")
    ap.add_argument("--sleeves", type=Path, default=None)
    args = ap.parse_args()
    run(args.sleeves)


if __name__ == "__main__":
    main()
