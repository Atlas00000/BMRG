"""
GRP-P3 — equal / inv-vol / risk-parity / HRP weights + f-budget caps
on OOS-stable groups from P2.

Usage (from infra/):
  python -m src.grouping.run_weights
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .f_budget import apply_f_budget
from .load_panel import build_panel
from .universe import P2_SLEEVES, REPO
from .weights import SCHEMES, compute_weights, score_weighted

OUT_P2 = REPO / "infra" / "artefacts" / "grouping" / "P2_LATEST"
OUT_P3 = REPO / "infra" / "artefacts" / "grouping" / "P3_LATEST"
ARCHIVE_P3 = REPO / "blotter" / "archive" / "GRP-P3-T01"


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


def _rank_key(s: dict) -> tuple:
    return (
        s.get("month_hit") or 0.0,
        s.get("quarter_hit") or 0.0,
        s.get("sum_R") or 0.0,
        -(abs(s.get("CVaR_m20") or 0.0)),
        -(abs(s.get("maxDD") or 0.0)),
    )


def evaluate_group(panel, g: dict) -> dict:
    members = _members(g)
    schemes_out: list[dict] = []
    for scheme in SCHEMES:
        raw = compute_weights(panel, members, scheme)
        metrics = score_weighted(panel, raw["weights"])
        budgeted = apply_f_budget(raw["weights"])
        metrics_b = score_weighted(panel, budgeted["weights"])
        schemes_out.append(
            {
                "scheme": scheme,
                "weights": raw["weights"],
                "metrics": metrics,
                "f_budget": {
                    "weights": budgeted["weights"],
                    "notes": budgeted["notes"],
                    "budget_mix": budgeted["budget_mix"],
                    "metrics": metrics_b,
                },
            }
        )

    # best raw scheme + best f-budget scheme
    best_raw = max(schemes_out, key=lambda s: _rank_key(s["metrics"]))
    best_fb = max(
        schemes_out, key=lambda s: _rank_key(s["f_budget"]["metrics"])
    )

    equal = next(s for s in schemes_out if s["scheme"] == "equal")
    return {
        "group_id": g.get("group_id") or "+".join(members),
        "k": len(members),
        "members": members,
        "p2_sum_R": g.get("sum_R"),
        "p2_month_hit": g.get("month_hit"),
        "p2_val_sum_R": (g.get("holdout") or {}).get("val_sum_R"),
        "schemes": schemes_out,
        "recommended": {
            "scheme": best_raw["scheme"],
            "weights": best_raw["weights"],
            "metrics": best_raw["metrics"],
            "vs_equal_sum_R": round(
                (best_raw["metrics"].get("sum_R") or 0)
                - (equal["metrics"].get("sum_R") or 0),
                4,
            ),
        },
        "recommended_f_budget": {
            "scheme": best_fb["scheme"],
            "weights": best_fb["f_budget"]["weights"],
            "metrics": best_fb["f_budget"]["metrics"],
            "notes": best_fb["f_budget"]["notes"],
            "budget_mix": best_fb["f_budget"]["budget_mix"],
            "vs_equal_sum_R": round(
                (best_fb["f_budget"]["metrics"].get("sum_R") or 0)
                - (equal["metrics"].get("sum_R") or 0),
                4,
            ),
        },
    }


def run(sleeves_dir: Path | None = None) -> dict:
    p2_path = OUT_P2 / "ACCEPTABLE_RANGE.json"
    if not p2_path.exists():
        raise SystemExit(
            f"Missing {p2_path} — run python -m src.grouping.run_bootstrap first"
        )
    p2 = _load_json(p2_path)
    groups = p2.get("groups") or []
    panel = build_panel(sleeves_dir or P2_SLEEVES)

    results = [evaluate_group(panel, g) for g in groups]
    # rank groups by recommended f-budget metrics
    results.sort(
        key=lambda r: _rank_key(r["recommended_f_budget"]["metrics"]),
        reverse=True,
    )

    generated = datetime.now(timezone.utc).isoformat()
    # scheme win counts
    from collections import Counter

    win_raw = Counter(r["recommended"]["scheme"] for r in results)
    win_fb = Counter(r["recommended_f_budget"]["scheme"] for r in results)

    scorecard = {
        "task_id": "GRP-P3-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "caveat": (
            "Weights from tip daily R cov. f_budget caps are research hints "
            "(EURUSD floor/cap · research/caution caps) — not VPS attach policy. "
            "Still HITL for GRP-P5."
        ),
        "p2_ref": str(p2_path),
        "n_groups": len(results),
        "schemes": list(SCHEMES),
        "scheme_wins_raw": dict(win_raw),
        "scheme_wins_f_budget": dict(win_fb),
        "panel": {
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
        },
    }

    # slim for ACCEPTABLE - keep recommended weights
    acceptable = {
        "task_id": "GRP-P3-T01",
        "generated_utc": generated,
        "n": len(results),
        "rank_order": "recommended_f_budget metrics: m_hit → q_hit → sum_R → -|CVaR| → -|maxDD|",
        "groups": [
            {
                "group_id": r["group_id"],
                "k": r["k"],
                "members": r["members"],
                "recommended": r["recommended"],
                "recommended_f_budget": r["recommended_f_budget"],
                "equal_metrics": next(
                    s["metrics"] for s in r["schemes"] if s["scheme"] == "equal"
                ),
                "scheme_summary": [
                    {
                        "scheme": s["scheme"],
                        "weights": s["weights"],
                        "sum_R": s["metrics"].get("sum_R"),
                        "month_hit": s["metrics"].get("month_hit"),
                        "maxDD": s["metrics"].get("maxDD"),
                        "f_budget_sum_R": s["f_budget"]["metrics"].get("sum_R"),
                        "f_budget_weights": s["f_budget"]["weights"],
                    }
                    for s in r["schemes"]
                ],
            }
            for r in results
        ],
    }

    OUT_P3.mkdir(parents=True, exist_ok=True)
    ARCHIVE_P3.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_P3 / "SCORECARD.json", scorecard)
    _write_json(OUT_P3 / "ACCEPTABLE_RANGE.json", acceptable)
    _write_json(OUT_P3 / "ALL_WEIGHTED.json", {"n": len(results), "groups": results})

    rows = []
    for r in results:
        rec = r["recommended_f_budget"]
        eq = next(s for s in r["schemes"] if s["scheme"] == "equal")
        rows.append(
            {
                "group_id": r["group_id"],
                "k": r["k"],
                "members": "|".join(r["members"]),
                "rec_scheme": rec["scheme"],
                "rec_sum_R": rec["metrics"].get("sum_R"),
                "rec_month_hit": rec["metrics"].get("month_hit"),
                "rec_maxDD": rec["metrics"].get("maxDD"),
                "rec_vs_equal": rec.get("vs_equal_sum_R"),
                "equal_sum_R": eq["metrics"].get("sum_R"),
                "prod_w": (rec.get("budget_mix") or {}).get("production_w"),
                "research_w": (rec.get("budget_mix") or {}).get("research_w"),
                "caution_w": (rec.get("budget_mix") or {}).get("caution_w"),
                "weights": "|".join(
                    f"{a}:{w:.3f}" for a, w in sorted(rec["weights"].items())
                ),
            }
        )
    _write_csv(OUT_P3 / "WEIGHTS_TABLE.csv", rows)

    # per-scheme comparison long
    long_rows = []
    for r in results:
        for s in r["schemes"]:
            long_rows.append(
                {
                    "group_id": r["group_id"],
                    "scheme": s["scheme"],
                    "sum_R": s["metrics"].get("sum_R"),
                    "month_hit": s["metrics"].get("month_hit"),
                    "quarter_hit": s["metrics"].get("quarter_hit"),
                    "maxDD": s["metrics"].get("maxDD"),
                    "CVaR_m20": s["metrics"].get("CVaR_m20"),
                    "f_sum_R": s["f_budget"]["metrics"].get("sum_R"),
                    "f_month_hit": s["f_budget"]["metrics"].get("month_hit"),
                    "weights": "|".join(
                        f"{a}:{w:.3f}" for a, w in sorted(s["weights"].items())
                    ),
                }
            )
    _write_csv(OUT_P3 / "SCHEME_COMPARE.csv", long_rows)

    review = _review(scorecard, results)
    (OUT_P3 / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in (
        "SCORECARD.json",
        "ACCEPTABLE_RANGE.json",
        "ALL_WEIGHTED.json",
        "WEIGHTS_TABLE.csv",
        "SCHEME_COMPARE.csv",
        "REVIEW.md",
    ):
        src = OUT_P3 / name
        if src.exists():
            shutil.copy2(src, ARCHIVE_P3 / name)

    top = results[0]
    print(
        f"P3 weighted {len(results)} OOS groups · "
        f"scheme wins (f_budget)={dict(win_fb)}"
    )
    print(
        f"Top: {top['group_id']} scheme={top['recommended_f_budget']['scheme']} "
        f"sum_R={top['recommended_f_budget']['metrics'].get('sum_R')} "
        f"w={top['recommended_f_budget']['weights']}"
    )
    print(f"Wrote {OUT_P3}")
    print(f"Archived {ARCHIVE_P3}")
    return {"scorecard": scorecard, "acceptable": acceptable}


def _review(scorecard: dict, results: list[dict]) -> str:
    lines = [
        "# GRP-P3-T01 — Weights inside OOS-stable groups",
        "",
        f"**generated_utc:** {scorecard['generated_utc']}",
        f"**groups:** {scorecard['n_groups']}",
        f"**scheme wins (raw):** {scorecard['scheme_wins_raw']}",
        f"**scheme wins (f_budget):** {scorecard['scheme_wins_f_budget']}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## Recommended (f_budget) shortlist",
        "",
        "| Rank | Group | scheme | sum_R | m_hit | maxDD | vs_eq | prod_w | weights |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for i, r in enumerate(results[:20], 1):
        rec = r["recommended_f_budget"]
        wstr = ", ".join(f"{a}:{w:.2f}" for a, w in sorted(rec["weights"].items()))
        lines.append(
            f"| {i} | {r['group_id']} | {rec['scheme']} | "
            f"{rec['metrics'].get('sum_R')} | {rec['metrics'].get('month_hit')} | "
            f"{rec['metrics'].get('maxDD')} | {rec.get('vs_equal_sum_R')} | "
            f"{(rec.get('budget_mix') or {}).get('production_w')} | {wstr} |"
        )

    # highlight core packs
    lines += [
        "",
        "## Core packs (EUR / JP / DE focus)",
        "",
    ]
    focus = [
        r
        for r in results
        if set(r["members"]) <= {"EURUSD", "JP225", "DE40", "USDJPY", "AAPL", "UK100"}
        and "AUDUSD" not in r["members"]
    ]
    for r in focus[:10]:
        rec = r["recommended_f_budget"]
        lines.append(
            f"- **{r['group_id']}** · {rec['scheme']} · "
            f"sum_R={rec['metrics'].get('sum_R')} · w={rec['weights']}"
        )

    lines += [
        "",
        "## Next",
        "",
        "1. GRP-P5 HITL — pick 1–N groups + weights for live profile.",
        "2. GRP-P4 remains paused.",
        "",
        "Artefacts: `infra/artefacts/grouping/P3_LATEST/` · "
        "`blotter/archive/GRP-P3-T01/`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="GRP-P3 weight schemes")
    ap.add_argument("--sleeves", type=Path, default=None)
    args = ap.parse_args()
    run(args.sleeves)


if __name__ == "__main__":
    main()
