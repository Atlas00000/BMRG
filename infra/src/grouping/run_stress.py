"""
GRP-P1 — dependence + twin stress · re-rank P0 provisional range.

Usage (from infra/):
  python -m src.grouping.run_stress
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .ban_matrix import build_ban_matrix
from .load_panel import build_panel
from .rerank import rerank_groups
from .stress import stress_snapshot
from .universe import OUT_LATEST, P2_SLEEVES, REPO

OUT_P1 = REPO / "infra" / "artefacts" / "grouping" / "P1_LATEST"
ARCHIVE_P1 = REPO / "blotter" / "archive" / "GRP-P1-T01"


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


def _slim(g: dict) -> dict:
    skip = {"period_M", "period_Q", "p1_tip_adverse"}
    out = {}
    for k, v in g.items():
        if k in skip:
            continue
        out[k] = v
    # keep tip adverse summary without period map
    tip = g.get("p1_tip_adverse") or {}
    out["p1_tip_adverse_hit"] = tip.get("hit_rate")
    out["p1_tip_adverse_sum_R"] = tip.get("sum_R")
    out["p1_tip_adverse_n_periods"] = tip.get("n_periods")
    return out


def run(sleeves_dir: Path | None = None) -> dict:
    p0_range_path = OUT_LATEST / "ACCEPTABLE_RANGE.json"
    if not p0_range_path.exists():
        raise SystemExit(
            f"Missing {p0_range_path} — run python -m src.grouping.run_enum first"
        )

    panel = build_panel(sleeves_dir or P2_SLEEVES)
    matrix = build_ban_matrix(panel)
    snap = stress_snapshot(panel)

    p0 = _load_json(p0_range_path)
    p0_groups = p0.get("groups") or []
    # members may be list already
    for g in p0_groups:
        if isinstance(g.get("members"), str):
            g["members"] = g["members"].split("|")

    kept, dropped = rerank_groups(p0_groups, panel, matrix)

    generated = datetime.now(timezone.utc).isoformat()
    # stress-resilient subset: kept + tip adverse hit >= 0.5 (or no tip periods)
    resilient = [
        g
        for g in kept
        if (g.get("p1_tip_adverse") or {}).get("hit_rate") is None
        or (g.get("p1_tip_adverse") or {}).get("hit_rate") >= 0.5
    ]
    clean_resilient = [g for g in resilient if not g.get("p1_soft_hits") and not g.get("soft_flags")]

    scorecard = {
        "task_id": "GRP-P1-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "caveat": (
            "Tip-panel dependence + twin stress. Soft EU-index pairs may escalate "
            "to hard if co_loss>=0.40. Adverse = Sep/Oct tip months + curated "
            "stress calendar. Still provisional until GRP-P2 bootstrap."
        ),
        "p0_ref": str(p0_range_path),
        "panel": {
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
        },
        "stress": snap,
        "ban_summary": {
            "n_hard": len(matrix["hard_bans"]),
            "n_soft": len(matrix["soft_penalties"]),
            "hard_ban_pairs": matrix["hard_ban_pairs"],
            "soft_penalty_pairs": matrix["soft_penalty_pairs"],
            "thresholds": matrix["thresholds"],
        },
        "p0_accepted": len(p0_groups),
        "p1_kept": len(kept),
        "p1_dropped_hard": len(dropped),
        "p1_resilient_tip_adverse": len(resilient),
        "p1_clean_resilient": len(clean_resilient),
    }

    acceptable = {
        "task_id": "GRP-P1-T01",
        "generated_utc": generated,
        "provisional_pending_bootstrap": True,
        "rank_order": "p1_penalty ASC → tip_adverse_hit → month_hit → q_hit → E_month → sum_R",
        "n": len(kept),
        "n_resilient": len(resilient),
        "n_clean_resilient": len(clean_resilient),
        "groups": [_slim(g) for g in kept],
        "resilient_groups": [_slim(g) for g in resilient],
        "clean_resilient_groups": [_slim(g) for g in clean_resilient],
    }

    OUT_P1.mkdir(parents=True, exist_ok=True)
    ARCHIVE_P1.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_P1 / "SCORECARD.json", scorecard)
    _write_json(OUT_P1 / "BAN_MATRIX.json", {
        "thresholds": matrix["thresholds"],
        "hard_bans": matrix["hard_bans"],
        "soft_penalties": matrix["soft_penalties"],
        "hard_ban_pairs": matrix["hard_ban_pairs"],
        "soft_penalty_pairs": matrix["soft_penalty_pairs"],
        "do_not_combine_raw": matrix["do_not_combine_raw"],
    })
    _write_json(OUT_P1 / "DEPENDENCE.json", {
        "coloss": matrix["coloss"],
        "corr_full": matrix["corr_full"],
        "corr_active": matrix["corr_active"],
    })
    _write_json(OUT_P1 / "ACCEPTABLE_RANGE.json", acceptable)
    _write_json(OUT_P1 / "DROPPED_HARD.json", {"n": len(dropped), "groups": [_slim(g) for g in dropped]})
    _write_json(OUT_P1 / "STRESS_INDEX.json", snap)

    # flat table
    rows = []
    for g in kept:
        tip = g.get("p1_tip_adverse") or {}
        rows.append(
            {
                "group_id": g.get("group_id"),
                "k": g.get("k"),
                "members": "|".join(g.get("members") or []),
                "month_hit": g.get("month_hit"),
                "quarter_hit": g.get("quarter_hit"),
                "sum_R": g.get("sum_R"),
                "p1_penalty": g.get("p1_penalty"),
                "p1_tip_adverse_hit": tip.get("hit_rate"),
                "p1_tip_adverse_sum_R": tip.get("sum_R"),
                "p1_max_pair_coloss": g.get("p1_max_pair_coloss"),
                "p1_tags": "|".join(g.get("p1_tags") or []),
                "soft_hits": "|".join("+".join(p) for p in (g.get("p1_soft_hits") or [])),
                "resilient": g.get("group_id") in {x["group_id"] for x in resilient},
                "clean_resilient": g.get("group_id")
                in {x["group_id"] for x in clean_resilient},
            }
        )
    _write_csv(OUT_P1 / "RERANK_TABLE.csv", rows)
    _write_csv(
        OUT_P1 / "coloss_pairs.csv",
        matrix["coloss"],
    )

    review = _review(scorecard, acceptable, matrix, kept, dropped, clean_resilient, resilient)
    (OUT_P1 / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in (
        "SCORECARD.json",
        "BAN_MATRIX.json",
        "DEPENDENCE.json",
        "ACCEPTABLE_RANGE.json",
        "DROPPED_HARD.json",
        "STRESS_INDEX.json",
        "RERANK_TABLE.csv",
        "coloss_pairs.csv",
        "REVIEW.md",
    ):
        src = OUT_P1 / name
        if src.exists():
            shutil.copy2(src, ARCHIVE_P1 / name)

    print(
        f"P1 kept {len(kept)}/{len(p0_groups)} "
        f"(dropped hard {len(dropped)}) · "
        f"resilient {len(resilient)} · clean_resilient {len(clean_resilient)}"
    )
    print(f"Hard bans: {matrix['hard_ban_pairs']}")
    print(f"Soft pens: {matrix['soft_penalty_pairs']}")
    if clean_resilient:
        t = clean_resilient[0]
        print(
            f"Top clean resilient: {t['group_id']} "
            f"pen={t.get('p1_penalty')} tip_adv_hit="
            f"{(t.get('p1_tip_adverse') or {}).get('hit_rate')} "
            f"sum_R={t.get('sum_R')}"
        )
    print(f"Wrote {OUT_P1}")
    print(f"Archived {ARCHIVE_P1}")
    return {"scorecard": scorecard, "acceptable": acceptable}


def _review(
    scorecard: dict,
    acceptable: dict,
    matrix: dict,
    kept: list,
    dropped: list,
    clean_resilient: list,
    resilient: list,
) -> str:
    lines = [
        "# GRP-P1-T01 — Dependence + twin stress",
        "",
        f"**generated_utc:** {scorecard['generated_utc']}",
        f"**P0 accepted:** {scorecard['p0_accepted']} → "
        f"**P1 kept:** {scorecard['p1_kept']} "
        f"(dropped hard {scorecard['p1_dropped_hard']})",
        f"**Resilient (tip Sep/Oct hit ≥ 0.5):** {scorecard['p1_resilient_tip_adverse']} · "
        f"**clean resilient:** {scorecard['p1_clean_resilient']}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## Ban matrix",
        "",
        f"- Hard: `{matrix['hard_ban_pairs']}`",
        f"- Soft: `{matrix['soft_penalty_pairs']}`",
        f"- Thresholds: {matrix['thresholds']}",
        "",
        "### Top co-loss pairs",
        "",
        "| a | b | n_both | co_loss | corr_active |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in (matrix.get("coloss") or [])[:12]:
        lines.append(
            f"| {row['a']} | {row['b']} | {row['n_both_active']} | "
            f"{row['co_loss_rate']} | {row.get('corr_active')} |"
        )

    lines += [
        "",
        "## Clean resilient (preferred ops shortlist)",
        "",
        "| Rank | Group | pen | tip_adv_hit | tip_adv_ΣR | m_hit | sum_R |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for i, g in enumerate(clean_resilient[:20], 1):
        tip = g.get("p1_tip_adverse") or {}
        lines.append(
            f"| {i} | {g['group_id']} | {g.get('p1_penalty')} | "
            f"{tip.get('hit_rate')} | {tip.get('sum_R')} | "
            f"{g.get('month_hit')} | {g.get('sum_R')} |"
        )

    lines += [
        "",
        "## Top kept (all, by penalty)",
        "",
        "| Rank | Group | pen | tip_adv_hit | tags | sum_R |",
        "| ---: | --- | ---: | ---: | --- | ---: |",
    ]
    for i, g in enumerate(kept[:20], 1):
        tip = g.get("p1_tip_adverse") or {}
        tags = ",".join(g.get("p1_tags") or []) or "—"
        lines.append(
            f"| {i} | {g['group_id']} | {g.get('p1_penalty')} | "
            f"{tip.get('hit_rate')} | {tags} | {g.get('sum_R')} |"
        )

    if dropped:
        lines += [
            "",
            "## Dropped (hard ban)",
            "",
            "| Group | hard_hits | sum_R |",
            "| --- | --- | ---: |",
        ]
        for g in dropped[:15]:
            lines.append(
                f"| {g['group_id']} | {g.get('p1_hard_hits')} | {g.get('sum_R')} |"
            )

    lines += [
        "",
        "## Next",
        "",
        "1. GRP-P2 — bootstrap + May–Aug / Sep–Oct holdout (clears provisional).",
        "2. Prefer **clean resilient** shortlist for weight trials (GRP-P3).",
        "",
        "Artefacts: `infra/artefacts/grouping/P1_LATEST/` · "
        "`blotter/archive/GRP-P1-T01/`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="GRP-P1 twin stress re-rank")
    ap.add_argument("--sleeves", type=Path, default=None)
    args = ap.parse_args()
    run(args.sleeves)


if __name__ == "__main__":
    main()
