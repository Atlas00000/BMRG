"""
GRP-P2 — block bootstrap + May–Aug / Sep–Oct holdout + fuse stub → OOS-stable range.

Usage (from infra/):
  python -m src.grouping.run_bootstrap
  python -m src.grouping.run_bootstrap --n-boot 2000
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .bootstrap import bootstrap_group
from .fuse import score_with_fuse
from .holdout import holdout_group
from .load_panel import build_panel
from .universe import MONTH_HIT_FLOOR, P2_SLEEVES, REPO

OUT_P1 = REPO / "infra" / "artefacts" / "grouping" / "P1_LATEST"
OUT_P2 = REPO / "infra" / "artefacts" / "grouping" / "P2_LATEST"
ARCHIVE_P2 = REPO / "blotter" / "archive" / "GRP-P2-T01"

# OOS admission (clears provisional for tip panel)
BOOT_HIT_P10_FLOOR = 0.50  # month-block bootstrap 10th pct
VAL_SUM_FLOOR = 0.0  # Sep–Oct sum_R must be >= 0 (strict)
VAL_HIT_FLOOR = 0.50  # Sep–Oct month_hit must also clear when n_months >= 1
FUSE_HIT_DROP_MAX = 0.34  # fused month_hit may not fall > this vs base


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


def _members(g: dict) -> tuple[str, ...]:
    m = g.get("members")
    if isinstance(m, str):
        return tuple(m.split("|"))
    return tuple(m or [])


def evaluate_group(
    panel,
    g: dict,
    *,
    n_boot: int,
    seed: int,
) -> dict:
    members = _members(g)
    boot = bootstrap_group(panel, members, n_boot=n_boot, seed=seed)
    ho = holdout_group(panel, members)
    fuse = score_with_fuse(panel, members)

    boot_p10 = (boot.get("month") or {}).get("hit_p10")
    val_sum = ho.get("val_sum_R")
    val_hit = ho.get("val_month_hit")
    fit_hit = ho.get("fit_month_hit")

    reasons: list[str] = []
    if boot_p10 is None or boot_p10 < BOOT_HIT_P10_FLOOR:
        reasons.append(f"boot_month_hit_p10={boot_p10}<{BOOT_HIT_P10_FLOOR}")
    # holdout: require non-negative Sep–Oct sum_R AND hit floor when periods exist
    if val_sum is None or val_sum < VAL_SUM_FLOOR:
        reasons.append(f"holdout_val_sum={val_sum}<{VAL_SUM_FLOOR}")
    if val_hit is not None and val_hit < VAL_HIT_FLOOR:
        reasons.append(f"holdout_val_hit={val_hit}<{VAL_HIT_FLOOR}")
    # fuse: month hit should not collapse
    mh_b = fuse.get("month_hit_base")
    mh_f = fuse.get("month_hit_fused")
    if mh_b is not None and mh_f is not None and (mh_b - mh_f) > FUSE_HIT_DROP_MAX:
        reasons.append(f"fuse_hit_drop={round(mh_b - mh_f, 4)}>{FUSE_HIT_DROP_MAX}")

    oos_pass = len(reasons) == 0
    return {
        "group_id": g.get("group_id") or "+".join(members),
        "k": len(members),
        "members": list(members),
        "month_hit": g.get("month_hit"),
        "quarter_hit": g.get("quarter_hit"),
        "sum_R": g.get("sum_R"),
        "p1_penalty": g.get("p1_penalty"),
        "p1_tags": g.get("p1_tags") or g.get("soft_flags") or [],
        "clean": not (g.get("p1_soft_hits") or g.get("soft_flags")),
        "bootstrap": boot,
        "holdout": {
            "fit_month_hit": fit_hit,
            "val_month_hit": val_hit,
            "val_sum_R": val_sum,
            "fit_sum_R": (ho.get("fit") or {}).get("sum_R"),
            "fit": ho.get("fit"),
            "val": ho.get("val"),
        },
        "fuse": fuse,
        "oos_pass": oos_pass,
        "oos_reject_reasons": reasons,
        "boot_month_hit_p10": boot_p10,
        "provisional_pending_bootstrap": False if oos_pass else True,
    }


def run(
    *,
    sleeves_dir: Path | None = None,
    n_boot: int = 1000,
    seed: int = 42,
    source: str = "clean_resilient",
) -> dict:
    p1_path = OUT_P1 / "ACCEPTABLE_RANGE.json"
    if not p1_path.exists():
        raise SystemExit(
            f"Missing {p1_path} — run python -m src.grouping.run_stress first"
        )
    p1 = _load_json(p1_path)
    if source == "all":
        candidates = p1.get("groups") or []
    elif source == "resilient":
        candidates = p1.get("resilient_groups") or p1.get("groups") or []
    else:
        candidates = (
            p1.get("clean_resilient_groups")
            or p1.get("resilient_groups")
            or p1.get("groups")
            or []
        )

    panel = build_panel(sleeves_dir or P2_SLEEVES)
    evaluated: list[dict] = []
    for i, g in enumerate(candidates):
        evaluated.append(
            evaluate_group(panel, g, n_boot=n_boot, seed=seed + i)
        )

    passed = [e for e in evaluated if e["oos_pass"]]
    failed = [e for e in evaluated if not e["oos_pass"]]

    def rank_key(e: dict) -> tuple:
        return (
            1 if e.get("clean") else 0,
            e.get("boot_month_hit_p10") or 0.0,
            (e.get("holdout") or {}).get("val_sum_R") or 0.0,
            e.get("month_hit") or 0.0,
            e.get("sum_R") or 0.0,
        )

    passed.sort(key=rank_key, reverse=True)
    failed.sort(key=lambda e: e.get("sum_R") or 0, reverse=True)

    generated = datetime.now(timezone.utc).isoformat()
    thresholds = {
        "boot_hit_p10_floor": BOOT_HIT_P10_FLOOR,
        "val_sum_floor": VAL_SUM_FLOOR,
        "val_hit_floor": VAL_HIT_FLOOR,
        "fuse_hit_drop_max": FUSE_HIT_DROP_MAX,
        "month_hit_floor_ref": MONTH_HIT_FLOOR,
        "n_boot": n_boot,
        "seed": seed,
        "candidate_source": source,
    }

    # reject reason tallies
    from collections import Counter

    tallies: Counter[str] = Counter()
    for e in failed:
        for r in e.get("oos_reject_reasons") or []:
            tallies[r.split("=")[0] if "=" in r else r.split(" ")[0]] += 1

    scorecard = {
        "task_id": "GRP-P2-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "caveat": (
            "Block bootstrap of tip months/weeks + May-Aug/Sep-Oct holdout + "
            "fuse stub (next-day suppress after multi-sleeve R_p < -1R). "
            "OOS-stable clears provisional for tip panel only — still not a "
            "live f / attach promotion."
        ),
        "p1_ref": str(p1_path),
        "thresholds": thresholds,
        "panel": {
            "n_days": int(len(panel)),
            "date_min": str(panel.index.min()),
            "date_max": str(panel.index.max()),
        },
        "n_candidates": len(evaluated),
        "n_oos_stable": len(passed),
        "n_oos_fail": len(failed),
        "reject_tallies": dict(tallies),
    }

    def slim(e: dict) -> dict:
        return {
            k: v
            for k, v in e.items()
            if k
            not in (
                # keep bootstrap/holdout/fuse summaries but drop nested fit full if huge
            )
        }

    acceptable = {
        "task_id": "GRP-P2-T01",
        "generated_utc": generated,
        "provisional_pending_bootstrap": False,
        "n": len(passed),
        "thresholds": thresholds,
        "rank_order": "clean → boot_hit_p10 → val_sum_R → month_hit → sum_R",
        "groups": [slim(e) for e in passed],
    }

    OUT_P2.mkdir(parents=True, exist_ok=True)
    ARCHIVE_P2.mkdir(parents=True, exist_ok=True)

    _write_json(OUT_P2 / "SCORECARD.json", scorecard)
    _write_json(OUT_P2 / "ACCEPTABLE_RANGE.json", acceptable)
    _write_json(
        OUT_P2 / "OOS_FAILED.json",
        {"n": len(failed), "groups": [slim(e) for e in failed]},
    )
    _write_json(OUT_P2 / "THRESHOLDS.json", thresholds)

    rows = []
    for e in evaluated:
        ho = e.get("holdout") or {}
        boot_m = (e.get("bootstrap") or {}).get("month") or {}
        fuse = e.get("fuse") or {}
        rows.append(
            {
                "group_id": e["group_id"],
                "k": e["k"],
                "members": "|".join(e["members"]),
                "clean": e.get("clean"),
                "oos_pass": e["oos_pass"],
                "month_hit": e.get("month_hit"),
                "sum_R": e.get("sum_R"),
                "boot_hit_p10": boot_m.get("hit_p10"),
                "boot_hit_p50": boot_m.get("hit_p50"),
                "boot_hit_obs": boot_m.get("obs_hit"),
                "fit_month_hit": ho.get("fit_month_hit"),
                "val_month_hit": ho.get("val_month_hit"),
                "val_sum_R": ho.get("val_sum_R"),
                "fuse_sum_delta": fuse.get("sum_R_delta"),
                "fuse_hit_fused": fuse.get("month_hit_fused"),
                "fuse_triggers": (fuse.get("fuse") or {}).get("n_trigger_days"),
                "reject": "|".join(e.get("oos_reject_reasons") or []),
            }
        )
    _write_csv(OUT_P2 / "OOS_TABLE.csv", rows)

    review = _review(scorecard, passed, failed, thresholds)
    (OUT_P2 / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in (
        "SCORECARD.json",
        "ACCEPTABLE_RANGE.json",
        "OOS_FAILED.json",
        "THRESHOLDS.json",
        "OOS_TABLE.csv",
        "REVIEW.md",
    ):
        src = OUT_P2 / name
        if src.exists():
            shutil.copy2(src, ARCHIVE_P2 / name)

    print(
        f"P2 candidates {len(evaluated)} ({source}) -> "
        f"OOS-stable {len(passed)} · fail {len(failed)}"
    )
    if passed:
        t = passed[0]
        print(
            f"Top: {t['group_id']} boot_p10={t.get('boot_month_hit_p10')} "
            f"val_sum={(t.get('holdout') or {}).get('val_sum_R')} "
            f"sum_R={t.get('sum_R')}"
        )
    print(f"Wrote {OUT_P2}")
    print(f"Archived {ARCHIVE_P2}")
    return {"scorecard": scorecard, "acceptable": acceptable}


def _review(
    scorecard: dict,
    passed: list[dict],
    failed: list[dict],
    thresholds: dict,
) -> str:
    lines = [
        "# GRP-P2-T01 — Bootstrap + holdout + fuse (OOS-stable range)",
        "",
        f"**generated_utc:** {scorecard['generated_utc']}",
        f"**candidates:** {scorecard['n_candidates']} → "
        f"**OOS-stable:** {scorecard['n_oos_stable']} · "
        f"**fail:** {scorecard['n_oos_fail']}",
        "",
        "## Caveat",
        "",
        scorecard["caveat"],
        "",
        "## Thresholds",
        "",
        f"```\n{json.dumps(thresholds, indent=2)}\n```",
        "",
        "## OOS-stable groups",
        "",
        "| Rank | Group | boot_p10 | val_sum | val_hit | m_hit | sum_R | fuseΔ |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for i, e in enumerate(passed[:30], 1):
        ho = e.get("holdout") or {}
        fuse = e.get("fuse") or {}
        lines.append(
            f"| {i} | {e['group_id']} | {e.get('boot_month_hit_p10')} | "
            f"{ho.get('val_sum_R')} | {ho.get('val_month_hit')} | "
            f"{e.get('month_hit')} | {e.get('sum_R')} | "
            f"{fuse.get('sum_R_delta')} |"
        )
    if len(passed) > 30:
        lines.append(
            f"| … | ({len(passed) - 30} more in ACCEPTABLE_RANGE.json) | | | | | | |"
        )

    lines += [
        "",
        "## Reject tallies",
        "",
        "| Reason | n |",
        "| --- | ---: |",
    ]
    for reason, n in (scorecard.get("reject_tallies") or {}).items():
        lines.append(f"| {reason} | {n} |")

    if failed:
        lines += [
            "",
            "## Sample failures",
            "",
            "| Group | reasons | sum_R |",
            "| --- | --- | ---: |",
        ]
        for e in failed[:12]:
            lines.append(
                f"| {e['group_id']} | "
                f"{'; '.join(e.get('oos_reject_reasons') or [])} | "
                f"{e.get('sum_R')} |"
            )

    lines += [
        "",
        "## Next",
        "",
        "1. GRP-P3 — weights inside OOS-stable groups.",
        "2. HITL pick from this range (GRP-P5) — still no auto VPS attach.",
        "",
        "Artefacts: `infra/artefacts/grouping/P2_LATEST/` · "
        "`blotter/archive/GRP-P2-T01/`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="GRP-P2 bootstrap / holdout / fuse")
    ap.add_argument("--sleeves", type=Path, default=None)
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument(
        "--source",
        choices=("clean_resilient", "resilient", "all"),
        default="clean_resilient",
        help="Which P1 list to stress-test (default: clean_resilient)",
    )
    args = ap.parse_args()
    run(
        sleeves_dir=args.sleeves,
        n_boot=args.n_boot,
        seed=args.seed,
        source=args.source,
    )


if __name__ == "__main__":
    main()
