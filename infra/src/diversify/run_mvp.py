"""
DIV-P0 MVP — daily panel · dependence · subset cycle scorecard.

Usage (from infra/):
  python -m src.diversify.run_mvp
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .dependence import corr_active, corr_full, do_not_combine, pairwise_coloss
from .load import load_all, sleeve_summaries
from .manifest import REPO, SLEEVES, manifest_dict
from .panel import daily_panel
from .score import baseline_eur, enumerate_clusters, rank_clusters

OUT_LATEST = REPO / "infra" / "artefacts" / "diversify" / "LATEST"
ARCHIVE = REPO / "blotter" / "archive" / "DIV-P0-T01"


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


def _df_to_records(df: pd.DataFrame) -> dict:
    return {
        "index": [str(i) for i in df.index],
        "columns": list(df.columns),
        "data": df.where(pd.notnull(df), None).values.tolist(),
    }


def run() -> dict:
    events = load_all(SLEEVES)
    summaries = sleeve_summaries(events)
    panel = daily_panel(events)
    if panel.empty:
        raise RuntimeError("empty daily panel")

    c_full = corr_full(panel)
    c_act = corr_active(panel)
    coloss = pairwise_coloss(panel)
    banned = do_not_combine(coloss)
    banned_pairs = {frozenset((b["a"], b["b"])) for b in banned}
    scored = enumerate_clusters(panel, ks=(1, 2, 3))
    ranked = rank_clusters(
        scored, min_months=4, prefer_k=(2, 3), banned_pairs=banned_pairs
    )
    ranked_clean = [r for r in ranked if not r.get("contains_banned_pair")]
    eur = baseline_eur(panel)

    # beat EUR-only on month_hit (or sum_R if tie)
    eur_hit = (eur or {}).get("month_hit") or 0.0
    beat_eur = [
        r
        for r in ranked_clean
        if (r["month_hit"] or 0) > eur_hit
        or (
            (r["month_hit"] or 0) == eur_hit
            and r["sum_R"] > (eur or {}).get("sum_R", 0)
        )
    ]

    generated = datetime.now(timezone.utc).isoformat()
    scorecard = {
        "task_id": "DIV-P0-T01",
        "generated_utc": generated,
        "roadmap": "doc/diversification_roadmap.md",
        "caveat": (
            "P0 uses engine/research fire-tape proxies — not locked live-OS "
            "Tester exports. Do not raise live f from this scorecard."
        ),
        "panel": {
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
            "assets": list(panel.columns),
        },
        "sleeve_summaries": summaries,
        "baseline_EURUSD": eur,
        "top_clusters_k2_k3_clean": ranked_clean[:15],
        "top_clusters_k2_k3_all": ranked[:15],
        "clusters_beating_EUR_month_hit": beat_eur[:10],
        "do_not_combine": banned,
        "coloss_top": coloss[:12],
    }

    OUT_LATEST.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_LATEST / "MANIFEST.json", manifest_dict())
    _write_json(OUT_LATEST / "SLEEVE_SUMMARY.json", summaries)
    _write_json(OUT_LATEST / "CORR_FULL.json", _df_to_records(c_full))
    _write_json(OUT_LATEST / "CORR_ACTIVE.json", _df_to_records(c_act))
    _write_json(OUT_LATEST / "COLOSS.json", coloss)
    _write_json(OUT_LATEST / "DO_NOT_COMBINE.json", banned)
    _write_json(OUT_LATEST / "CLUSTERS_ALL.json", scored)
    _write_json(OUT_LATEST / "SCORECARD.json", scorecard)
    panel.to_csv(OUT_LATEST / "daily_R_panel.csv", index_label="date")
    c_full.to_csv(OUT_LATEST / "corr_full.csv")
    c_act.to_csv(OUT_LATEST / "corr_active.csv")

    # human REVIEW
    lines = [
        "# DIV-P0-T01 — Diversification MVP scorecard",
        "",
        f"**generated_utc:** {generated}",
        f"**panel:** {panel.index.min()} -> {panel.index.max()} · {len(panel)} days · {list(panel.columns)}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## Sleeve proxies",
        "",
        "| Asset | n | E_N | WR | window |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for aid, s in summaries.items():
        lines.append(
            f"| {aid} | {s.get('n')} | {s.get('E_N')} | {s.get('WR')} | "
            f"{s.get('date_min')} -> {s.get('date_max')} |"
        )
    lines += ["", "## Baseline EURUSD-only", "", "```json", json.dumps(eur, indent=2), "```", ""]
    lines += [
        "## Top clusters (k=2,3 by month_hit, banned twins demoted)",
        "",
        "| rank | members | month_hit | n_m | quarter_hit | sum_R | CVaR_m20 | fuse_days | maxDD |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for i, r in enumerate(ranked_clean[:12], 1):
        lines.append(
            f"| {i} | {'+'.join(r['members'])} | {r['month_hit']} | {r['n_months']} | "
            f"{r['quarter_hit']} | {r['sum_R']} | {r['CVaR_m20']} | {r['fuse_days']} | {r['maxDD']} |"
        )
    lines += ["", "## Do not combine (heuristic + known twins)", ""]
    if not banned:
        lines.append("_none flagged_")
    else:
        for b in banned:
            lines.append(
                f"- **{b['a']}+{b['b']}** · co_loss={b['co_loss_rate']} · "
                f"n_both={b['n_both_active']} · {', '.join(b['reasons'])}"
            )
    lines += ["", "## Verdict", ""]
    if beat_eur:
        top = beat_eur[0]
        lines.append(
            f"**ACCEPT P0 research** — best vs EUR month_hit: "
            f"`{'+'.join(top['members'])}` (month_hit={top['month_hit']}, sum_R={top['sum_R']}). "
            "Proceed DIV-P1 regime-conditioned corr; do not raise live f."
        )
    else:
        lines.append(
            "**HOLD P0** — no k=2/3 cluster beat EUR-only month_hit on this proxy panel. "
            "Inspect COLOSS / known twins; refresh tapes in DIV-P2."
        )
    review = "\n".join(lines) + "\n"
    (OUT_LATEST / "REVIEW.md").write_text(review, encoding="utf-8")

    # archive copy
    for name in (
        "MANIFEST.json",
        "SLEEVE_SUMMARY.json",
        "CORR_FULL.json",
        "CORR_ACTIVE.json",
        "COLOSS.json",
        "DO_NOT_COMBINE.json",
        "SCORECARD.json",
        "REVIEW.md",
        "daily_R_panel.csv",
        "corr_full.csv",
        "corr_active.csv",
    ):
        src = OUT_LATEST / name
        if src.exists():
            shutil.copy2(src, ARCHIVE / name)
    # keep clusters_all only in LATEST (large); copy slim top into archive via SCORECARD

    import sys

    top = ranked_clean[0] if ranked_clean else None
    summary = (
        f"DIV-P0-T01 done | days={len(panel)} | top="
        f"{'+'.join(top['members']) if top else 'none'} "
        f"month_hit={top['month_hit'] if top else None} | "
        f"beat_eur={len(beat_eur)} | banned={len(banned)}"
    )
    print(summary)
    print(f"Wrote {OUT_LATEST}")
    print(f"Archived {ARCHIVE}")
    sys.stdout.flush()
    return scorecard


if __name__ == "__main__":
    run()
