"""
GRP-P0 — tip daily panel + exhaustive k=2…5 enum → acceptable range.

Usage (from infra/):
  python -m src.grouping.run_enum
  python -m src.grouping.run_enum --sleeves path\\to\\P2_LATEST\\sleeves
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .enum_score import (
    admit_provisional,
    enumerate_groups,
    period_table_rows,
    score_group,
)
from .load_panel import build_panel, load_tip_events
from .universe import (
    ARCHIVE,
    CVAR_TOLERANCE_R,
    EUR_HIT_SLACK,
    HARD_BAN_PAIRS,
    KS,
    MONTH_HIT_FLOOR,
    OUT_LATEST,
    P2_SLEEVES,
    QUARTER_HIT_FLOOR,
    SLEEVES,
    SOFT_PENALTY_PAIRS,
)


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


def run(sleeves_dir: Path | None = None) -> dict:
    root = sleeves_dir or P2_SLEEVES
    events = load_tip_events(root)
    panel = build_panel(root)
    if panel.empty:
        raise RuntimeError("empty daily panel")

    eur = score_group(panel, ("EURUSD",)) if "EURUSD" in panel.columns else None
    scored = enumerate_groups(panel, ks=KS)
    # also keep k=1 baselines for reference (not in range)
    singles = [
        score_group(panel, (aid,))
        for aid in panel.columns
    ]
    accepted, rejected = admit_provisional(scored, eur)

    # strip bulky period maps from RANGE / SCORECARD list copies
    def slim(rows: list[dict]) -> list[dict]:
        out = []
        for r in rows:
            d = {k: v for k, v in r.items() if k not in ("period_M", "period_Q")}
            out.append(d)
        return out

    generated = datetime.now(timezone.utc).isoformat()
    sleeve_n = {aid: len(rows) for aid, rows in events.items()}

    scorecard = {
        "task_id": "GRP-P0-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "caveat": (
            "Equal-weight tip 6m designed R. Admission rules 1–4 only — "
            "bootstrap/holdout (rule 5) is GRP-P2. Provisional range; do not "
            "raise live f or auto-attach."
        ),
        "panel": {
            "source": str(root),
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
            "sleeves": list(panel.columns),
            "sleeve_n_trades": sleeve_n,
        },
        "thresholds": {
            "month_hit_floor": MONTH_HIT_FLOOR,
            "quarter_hit_floor": QUARTER_HIT_FLOOR,
            "eur_hit_slack": EUR_HIT_SLACK,
            "cvar_tolerance_R": CVAR_TOLERANCE_R,
            "ks": list(KS),
            "hard_ban_pairs": [sorted(p) for p in HARD_BAN_PAIRS],
            "soft_penalty_pairs": [sorted(p) for p in SOFT_PENALTY_PAIRS],
        },
        "eur_baseline": {k: v for k, v in (eur or {}).items() if k not in ("period_M", "period_Q")},
        "n_enumerated": len(scored),
        "n_accepted_provisional": len(accepted),
        "n_rejected": len(rejected),
        "universe": [
            {
                "asset_id": s.asset_id,
                "magic": s.magic,
                "tier": s.tier,
                "trades_per_30d": s.trades_per_30d,
            }
            for s in SLEEVES
        ],
    }

    acceptable = {
        "task_id": "GRP-P0-T01",
        "generated_utc": generated,
        "provisional_pending_bootstrap": True,
        "n": len(accepted),
        "rank_order": "soft_clean → month_hit → quarter_hit → E_month → -|CVaR| → sum_R",
        "groups": slim(accepted),
    }

    OUT_LATEST.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    # daily panel CSV
    panel_out = panel.copy()
    panel_out.index = [str(d) for d in panel_out.index]
    panel_out.to_csv(OUT_LATEST / "daily_R_panel.csv", index_label="date")

    _write_json(OUT_LATEST / "SCORECARD.json", scorecard)
    _write_json(OUT_LATEST / "ACCEPTABLE_RANGE.json", acceptable)
    _write_json(OUT_LATEST / "ALL_GROUPS.json", {"n": len(scored), "groups": slim(scored)})
    _write_json(OUT_LATEST / "REJECTED.json", {"n": len(rejected), "groups": slim(rejected)[:80]})
    _write_json(OUT_LATEST / "SINGLES.json", {"groups": slim(singles)})
    _write_csv(OUT_LATEST / "PERIOD_GROUP_M.csv", period_table_rows(scored, "M"))
    _write_csv(OUT_LATEST / "PERIOD_GROUP_Q.csv", period_table_rows(scored, "Q"))

    # flat enum table
    enum_rows = slim(scored)
    for r in enum_rows:
        r["members"] = "|".join(r["members"])
        r["soft_flags"] = "|".join(r.get("soft_flags") or [])
        r["accepted"] = r["group_id"] in {a["group_id"] for a in accepted}
    _write_csv(OUT_LATEST / "ENUM_TABLE.csv", enum_rows)

    review = _build_review(scorecard, acceptable, eur, accepted, rejected)
    (OUT_LATEST / "REVIEW.md").write_text(review, encoding="utf-8")

    # archive
    for name in (
        "SCORECARD.json",
        "ACCEPTABLE_RANGE.json",
        "ALL_GROUPS.json",
        "REJECTED.json",
        "SINGLES.json",
        "ENUM_TABLE.csv",
        "PERIOD_GROUP_M.csv",
        "PERIOD_GROUP_Q.csv",
        "daily_R_panel.csv",
        "REVIEW.md",
    ):
        src = OUT_LATEST / name
        if src.exists():
            shutil.copy2(src, ARCHIVE / name)

    print(f"Panel {panel.index.min()} -> {panel.index.max()} · {len(panel)} days")
    print(f"Enumerated {len(scored)} groups (k={list(KS)})")
    print(f"Accepted provisional: {len(accepted)} · rejected: {len(rejected)}")
    print(f"Wrote {OUT_LATEST}")
    print(f"Archived {ARCHIVE}")
    if accepted:
        top = accepted[0]
        print(
            f"Top: {top['group_id']}  m_hit={top['month_hit']} "
            f"q_hit={top['quarter_hit']} sum_R={top['sum_R']}"
        )
    return {"scorecard": scorecard, "acceptable": acceptable}


def _build_review(
    scorecard: dict,
    acceptable: dict,
    eur: dict | None,
    accepted: list[dict],
    rejected: list[dict],
) -> str:
    lines = [
        "# GRP-P0-T01 — Asset group enum (tip 6m)",
        "",
        f"**generated_utc:** {scorecard['generated_utc']}",
        f"**panel:** {scorecard['panel']['date_min']} → {scorecard['panel']['date_max']} "
        f"({scorecard['panel']['n_days']} days)",
        f"**enumerated:** {scorecard['n_enumerated']} · "
        f"**accepted provisional:** {scorecard['n_accepted_provisional']} · "
        f"**rejected:** {scorecard['n_rejected']}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## EUR-only baseline",
        "",
    ]
    if eur:
        lines.append(
            f"| month_hit | quarter_hit | sum_R | CVaR_m20 | maxDD |"
        )
        lines.append("| ---: | ---: | ---: | ---: | ---: |")
        lines.append(
            f"| {eur.get('month_hit')} | {eur.get('quarter_hit')} | "
            f"{eur.get('sum_R')} | {eur.get('CVaR_m20')} | {eur.get('maxDD')} |"
        )
    lines += [
        "",
        "## Acceptable range (provisional)",
        "",
        "Rank: soft-clean first, then month_hit · quarter_hit · E_month · −|CVaR| · sum_R.",
        "",
        "### Soft-clean (no twin / freq / caution-only flags)",
        "",
        "| Rank | Group | k | m_hit | q_hit | E_month | sum_R | CVaR | fuse |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    clean = [g for g in accepted if not g.get("soft_flags")]
    flagged = [g for g in accepted if g.get("soft_flags")]
    for i, g in enumerate(clean[:20], 1):
        lines.append(
            f"| {i} | {g['group_id']} | {g['k']} | {g.get('month_hit')} | "
            f"{g.get('quarter_hit')} | {g.get('E_month')} | {g.get('sum_R')} | "
            f"{g.get('CVaR_m20')} | {g.get('fuse_days')} |"
        )
    if len(clean) > 20:
        lines.append(
            f"| … | ({len(clean) - 20} more soft-clean in ACCEPTABLE_RANGE.json) | | | | | | | |"
        )
    lines += [
        "",
        f"### Soft-flagged still admitted ({len(flagged)}) — need GRP-P1 stress",
        "",
        "| Rank | Group | k | m_hit | soft | sum_R |",
        "| ---: | --- | ---: | ---: | --- | ---: |",
    ]
    for i, g in enumerate(flagged[:15], 1):
        soft = ",".join(g.get("soft_flags") or [])
        lines.append(
            f"| {i} | {g['group_id']} | {g['k']} | {g.get('month_hit')} | "
            f"{soft} | {g.get('sum_R')} |"
        )
    if len(flagged) > 15:
        lines.append(f"| … | ({len(flagged) - 15} more flagged) | | | | |")

    # reject reason tallies
    from collections import Counter

    c: Counter[str] = Counter()
    for r in rejected:
        for reason in r.get("reject_reasons") or ["unknown"]:
            # normalize
            key = reason.split("=")[0] if "=" in reason else reason
            c[key] += 1
    lines += [
        "",
        "## Reject reason tallies",
        "",
        "| Reason | n |",
        "| --- | ---: |",
    ]
    for reason, n in c.most_common():
        lines.append(f"| {reason} | {n} |")

    lines += [
        "",
        "## Next",
        "",
        "1. GRP-P1 — co-loss / twin stress re-rank.",
        "2. GRP-P2 — bootstrap + May–Aug / Sep–Oct holdout (clears provisional).",
        "3. Do not promote to VPS from this range alone.",
        "",
        f"Artefacts: `infra/artefacts/grouping/LATEST/` · archive `blotter/archive/GRP-P0-T01/`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="GRP-P0 tip group enumerator")
    ap.add_argument(
        "--sleeves",
        type=Path,
        default=None,
        help="Directory of *_live_fire_tape.csv (default P2_LATEST/sleeves)",
    )
    args = ap.parse_args()
    run(args.sleeves)


if __name__ == "__main__":
    main()
