"""
DIV-P1 — regime-conditioned dependence + stress calendar.

Usage (from infra/):
  python -m src.diversify.run_p1
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .dependence import (
    coloss_delta,
    conditioned_dependence,
    corr_active,
    do_not_combine,
)
from .load import load_all
from .manifest import REPO, SLEEVES
from .panel import daily_panel
from .regime import (
    align_book_regime_to_panel,
    book_day_regime,
    regime_counts,
    sleeve_day_regimes,
)
from .score import enumerate_clusters, portfolio_series, rank_clusters, score_cluster
from .stress import STRESS_MONTHS, day_stress_flags, stress_day_mask, stress_index

OUT_LATEST = REPO / "infra" / "artefacts" / "diversify" / "P1_LATEST"
ARCHIVE = REPO / "blotter" / "archive" / "DIV-P1-T01"
P0_SCORECARD = REPO / "blotter" / "archive" / "DIV-P0-T01" / "SCORECARD.json"


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


def _cluster_under_mask(
    panel: pd.DataFrame, members: list[str], mask: pd.Series, label: str
) -> dict:
    sub = panel.loc[mask.reindex(panel.index).fillna(False).astype(bool)]
    if sub.empty:
        return {"label": label, "members": members, "n_days": 0}
    sc = score_cluster(sub, tuple(members))
    sc["label"] = label
    # fraction of cluster days that are adverse while any member active
    rp = portfolio_series(panel, tuple(members))
    active = rp != 0
    m = mask.reindex(panel.index).fillna(False).astype(bool)
    sc["share_active_days_in_mask"] = (
        round(float((active & m).sum() / active.sum()), 4) if active.sum() else None
    )
    return sc


def run() -> dict:
    events = load_all(SLEEVES)
    panel = daily_panel(events)
    sleeve_reg = sleeve_day_regimes(events)
    book_raw = book_day_regime(sleeve_reg)
    book_reg = align_book_regime_to_panel(panel, book_raw)
    stress_flags = day_stress_flags(panel)
    stress_mask = stress_day_mask(panel)

    counts = regime_counts(book_reg)
    dep = conditioned_dependence(
        panel, book_reg, regimes=("MISMATCH", "FRAGILE", "MATCH"), stress_mask=stress_mask
    )

    deltas = {
        "ADVERSE_vs_full": coloss_delta(
            dep["full"]["coloss"], dep["regime_ADVERSE"]["coloss"]
        ),
        "MISMATCH_vs_full": coloss_delta(
            dep["full"]["coloss"], dep["regime_MISMATCH"]["coloss"]
        ),
        "stress_vs_full": coloss_delta(
            dep["full"]["coloss"], dep.get("stress_calendar", {}).get("coloss", [])
        ),
    }

    banned = do_not_combine(dep["full"]["coloss"])
    banned_pairs = {frozenset((b["a"], b["b"])) for b in banned}
    # also flag pairs whose ADVERSE co_loss jumps >= +0.10 with n_both>=5
    adverse_spikes = [
        d
        for d in deltas["ADVERSE_vs_full"]
        if d["n_both_cond"] >= 5 and (d["delta"] or 0) >= 0.10
    ]
    for d in adverse_spikes:
        banned_pairs.add(frozenset((d["a"], d["b"])))

    scored = enumerate_clusters(panel, ks=(2, 3))
    ranked = rank_clusters(
        scored, min_months=4, prefer_k=(2, 3), banned_pairs=banned_pairs
    )
    ranked_clean = [r for r in ranked if not r.get("contains_banned_pair")][:8]

    adverse_mask = book_reg.isin(("MISMATCH", "FRAGILE"))
    cluster_stress: list[dict] = []
    for r in ranked_clean:
        members = r["members"]
        cluster_stress.append(
            {
                "members": members,
                "full": score_cluster(panel, tuple(members)),
                "adverse": _cluster_under_mask(
                    panel, members, adverse_mask, "ADVERSE"
                ),
                "mismatch": _cluster_under_mask(
                    panel, members, book_reg == "MISMATCH", "MISMATCH"
                ),
                "stress": _cluster_under_mask(panel, members, stress_mask, "STRESS"),
            }
        )

    # Prefer clusters with non-negative adverse sum_R when n_days>=10
    resilient = []
    for c in cluster_stress:
        adv = c["adverse"]
        if adv.get("n_days", 0) >= 10 and (adv.get("sum_R") or 0) >= 0:
            resilient.append(
                {
                    "members": c["members"],
                    "adverse_sum_R": adv.get("sum_R"),
                    "adverse_n_days": adv.get("n_days"),
                    "full_month_hit": c["full"].get("month_hit"),
                    "full_sum_R": c["full"].get("sum_R"),
                }
            )
    resilient.sort(key=lambda x: (x["adverse_sum_R"], x["full_month_hit"] or 0), reverse=True)

    generated = datetime.now(timezone.utc).isoformat()
    scorecard = {
        "task_id": "DIV-P1-T01",
        "generated_utc": generated,
        "roadmap": "doc/diversification_roadmap.md",
        "caveat": (
            "Regime tags from fire-tape ouroboros/regime_tag (normalized). "
            "EURUSD Harvest labeled has no tag → UNTAGGED except stress months. "
            "Stress calendar is doc-curated months — not live L2."
        ),
        "panel": {
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
        },
        "book_regime_counts": counts,
        "stress_index": stress_index(),
        "stress_active_days": int(stress_mask.sum()),
        "dependence_n_days": {
            k: v.get("n_days")
            for k, v in dep.items()
            if isinstance(v, dict) and "n_days" in v
        },
        "coloss_deltas": {
            "ADVERSE_top": deltas["ADVERSE_vs_full"][:10],
            "MISMATCH_top": deltas["MISMATCH_vs_full"][:10],
            "stress_top": deltas["stress_vs_full"][:10],
        },
        "adverse_co_loss_spikes": adverse_spikes,
        "do_not_combine": banned,
        "top_clusters_clean": ranked_clean,
        "cluster_regime_stress": cluster_stress,
        "resilient_on_adverse": resilient[:8],
        "p0_ref": str(P0_SCORECARD) if P0_SCORECARD.exists() else None,
    }

    OUT_LATEST.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_LATEST / "SCORECARD.json", scorecard)
    _write_json(OUT_LATEST / "BOOK_REGIME_COUNTS.json", counts)
    _write_json(OUT_LATEST / "STRESS_INDEX.json", stress_index())
    _write_json(OUT_LATEST / "DEPENDENCE.json", {
        k: {
            "n_days": v.get("n_days"),
            "definition": v.get("definition"),
            "coloss": v.get("coloss"),
        }
        for k, v in dep.items()
        if isinstance(v, dict)
    })
    _write_json(OUT_LATEST / "COLOSS_DELTAS.json", deltas)
    _write_json(OUT_LATEST / "CLUSTER_REGIME_STRESS.json", cluster_stress)
    _write_json(OUT_LATEST / "RESILIENT_ADVERSE.json", resilient)

    # CSV helpers
    book_reg.to_csv(OUT_LATEST / "book_regime_daily.csv", header=True)
    stress_flags.to_csv(OUT_LATEST / "stress_flags_daily.csv")
    sleeve_reg.to_csv(OUT_LATEST / "sleeve_regime_daily.csv")
    corr_active(panel).to_csv(OUT_LATEST / "corr_active_full.csv")
    if dep["regime_ADVERSE"]["n_days"] >= 5:
        corr_active(
            panel.loc[adverse_mask.reindex(panel.index).fillna(False)]
        ).to_csv(OUT_LATEST / "corr_active_ADVERSE.csv")

    lines = [
        "# DIV-P1-T01 — Regime-conditioned diversification",
        "",
        f"**generated_utc:** {generated}",
        f"**panel:** {panel.index.min()} -> {panel.index.max()} · {len(panel)} days",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## Book regime day counts",
        "",
        "| Regime | days |",
        "| --- | ---: |",
    ]
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        f"**Stress-calendar active days:** {int(stress_mask.sum())} "
        f"(doc months × active sleeve)",
        "",
        "## Co-loss deltas (conditioned - full) — top adverse spikes",
        "",
        "| pair | co_loss full | co_loss adverse | delta | n_both adverse |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for d in deltas["ADVERSE_vs_full"][:10]:
        lines.append(
            f"| {d['a']}+{d['b']} | {d['co_loss_full']} | {d['co_loss_cond']} | "
            f"{d['delta']} | {d['n_both_cond']} |"
        )
    lines += ["", "## Clusters resilient on ADVERSE days (sum_R>=0, n>=10)", ""]
    if not resilient:
        lines.append("_none_")
    else:
        lines += [
            "| members | adverse sum_R | adverse days | full month_hit | full sum_R |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for r in resilient[:8]:
            lines.append(
                f"| {'+'.join(r['members'])} | {r['adverse_sum_R']} | "
                f"{r['adverse_n_days']} | {r['full_month_hit']} | {r['full_sum_R']} |"
            )
    lines += ["", "## Stress month registry (P1-T03)", ""]
    for s in STRESS_MONTHS:
        lines.append(f"- **{s.asset_id}** m={s.month:02d} · {s.label} · _{s.source}_")
    lines += ["", "## Verdict", ""]
    if resilient:
        top = resilient[0]
        lines.append(
            f"**ACCEPT P1 research** — most resilient clean cluster on ADVERSE: "
            f"`{'+'.join(top['members'])}` (adverse sum_R={top['adverse_sum_R']}, "
            f"full month_hit={top['full_month_hit']}). "
            "Use for DIV-P2 live-tape refresh; do not raise live f."
        )
    else:
        lines.append(
            "**HOLD P1** — no clean cluster stayed non-negative on ADVERSE days "
            "with n>=10. Inspect spikes; tighten stress calendar or await P2 tapes."
        )
    review = "\n".join(lines) + "\n"
    (OUT_LATEST / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in (
        "SCORECARD.json",
        "BOOK_REGIME_COUNTS.json",
        "STRESS_INDEX.json",
        "DEPENDENCE.json",
        "COLOSS_DELTAS.json",
        "CLUSTER_REGIME_STRESS.json",
        "RESILIENT_ADVERSE.json",
        "REVIEW.md",
        "book_regime_daily.csv",
        "stress_flags_daily.csv",
        "sleeve_regime_daily.csv",
        "corr_active_full.csv",
        "corr_active_ADVERSE.csv",
    ):
        src = OUT_LATEST / name
        if src.exists():
            shutil.copy2(src, ARCHIVE / name)

    print(
        f"DIV-P1-T01 done | regime={counts} | stress_days={int(stress_mask.sum())} | "
        f"resilient={len(resilient)} | top="
        f"{'+'.join(resilient[0]['members']) if resilient else 'none'}"
    )
    print(f"Wrote {OUT_LATEST}")
    print(f"Archived {ARCHIVE}")
    return scorecard


if __name__ == "__main__":
    run()
