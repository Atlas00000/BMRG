"""
GRP-P5 — freeze HITL group promotion from P4 Pareto champions.

Usage (from infra/):
  python -m src.grouping.run_promote
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .universe import REPO, by_id

OUT_P3 = REPO / "infra" / "artefacts" / "grouping" / "P3_LATEST"
OUT_P4 = REPO / "infra" / "artefacts" / "grouping" / "P4_LATEST"
OUT_P5 = REPO / "infra" / "artefacts" / "grouping" / "P5_LATEST"
ARCHIVE_P5 = REPO / "blotter" / "archive" / "GRP-P5-T01"

# HITL freeze 2026-10-22 — policy menu from P4 Pareto + equal weights (P3)
PRIMARY = {
    "group_id": "JP225+DE40",
    "role": "primary_research_cluster",
    "policy": "max_sum_R",
    "rationale": (
        "Highest tip designed sum_R among OOS-stable/Pareto; clean tiers; "
        "equal 50/50; shallow fuse; keep EURUSD as separate production sleeve."
    ),
}

SECONDARIES = [
    {
        "group_id": "DE40+USDJPY",
        "role": "holdout_alternate",
        "policy": "max_holdout_val",
        "rationale": "Best Sep–Oct holdout among Pareto front; use when prioritizing recent tip resilience.",
    },
    {
        "group_id": "JP225+USDJPY",
        "role": "path_alternate",
        "policy": "best_CVaR",
        "rationale": "Best CVaR / shallow maxDD on front; Asia+JPY diversifier without DE.",
    },
    {
        "group_id": "EURUSD+DE40+USDJPY+AAPL",
        "role": "production_anchored_shallow_dd",
        "policy": "min_maxDD",
        "rationale": (
            "Only Pareto champion that includes production EURUSD; shallowest maxDD. "
            "AAPL at equal 25% — keep light / caution in attach policy."
        ),
    },
    {
        "group_id": "USDJPY+UK100",
        "role": "min_tail_watch",
        "policy": "min_tail",
        "rationale": (
            "Lowest max pairwise tail_dep on front but weaker tip hit / holdout; "
            "UK100 halt history — watch only, not default capital."
        ),
    },
]

# VPS sleeve posture when primary map is active (EUR production stays on)
ATTACH_POLICY = {
    "EURUSD": {
        "posture": "full",
        "bucket": "production",
        "note": "Standalone production INF — not inside primary JP225+DE40 cluster",
    },
    "JP225": {
        "posture": "full",
        "bucket": "research_cluster_primary",
        "note": "Primary cluster member · equal 0.50 with DE40",
    },
    "DE40": {
        "posture": "full",
        "bucket": "research_cluster_primary",
        "note": "Primary cluster member · equal 0.50 with JP225",
    },
    "USDJPY": {
        "posture": "light",
        "bucket": "research_optional",
        "note": "On for alternate maps (DE+JPY / JP+JPY); light until HITL picks alternate",
    },
    "AAPL": {
        "posture": "light",
        "bucket": "caution",
        "note": "Only if production-anchored map selected; EF Below / Leak 15.3",
    },
    "UK100": {
        "posture": "off_pending_halt_review",
        "bucket": "caution",
        "note": "Tip halt ~4 Sep; min_tail champion only — do not default-on",
    },
    "AUDUSD": {
        "posture": "ft_twin_only",
        "bucket": "fx_twin_excluded_from_groups",
        "note": "Hard-ban with EUR in groups; P2 holdout kills AUD packs; keep FT twin @ 0.5%, not SCALE in clusters",
    },
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


def _enrich(gid: str, p4_front: list, p3_groups: dict) -> dict:
    meta = next((g for g in p4_front if g["group_id"] == gid), {})
    p3 = p3_groups.get(gid) or {}
    rec = p3.get("recommended_f_budget") or {}
    return {
        "group_id": gid,
        "members": meta.get("members") or _members_from_id(gid),
        "policy_label": meta.get("policy_label"),
        "metrics": {
            "month_hit": meta.get("month_hit"),
            "quarter_hit": meta.get("quarter_hit"),
            "sum_R": meta.get("sum_R"),
            "E_month": meta.get("E_month"),
            "CVaR_m20": meta.get("CVaR_m20"),
            "maxDD": meta.get("maxDD"),
            "fuse_days": meta.get("fuse_days"),
            "max_tail_dep": meta.get("max_tail_dep"),
            "val_sum_R": meta.get("val_sum_R"),
            "boot_month_hit_p10": meta.get("boot_month_hit_p10"),
        },
        "weights": rec.get("weights"),
        "weight_scheme": rec.get("scheme"),
        "magics": {
            m: by_id[m].magic if m in by_id else None
            for m in (meta.get("members") or _members_from_id(gid))
        },
    }


def _members_from_id(gid: str) -> list[str]:
    return gid.split("+")


def run() -> dict:
    p4 = _load(OUT_P4 / "PARETO_FRONT.json")
    p3 = _load(OUT_P3 / "ACCEPTABLE_RANGE.json")
    p3_by = {g["group_id"]: g for g in p3.get("groups") or []}
    front = p4.get("groups") or []

    primary = {**PRIMARY, **_enrich(PRIMARY["group_id"], front, p3_by)}
    secondaries = [
        {**s, **_enrich(s["group_id"], front, p3_by)} for s in SECONDARIES
    ]

    generated = datetime.now(timezone.utc).isoformat()
    decision = {
        "task_id": "GRP-P5-T01",
        "generated_utc": generated,
        "roadmap": "doc/asset_grouping_roadmap.md",
        "hitl_status": "FROZEN",
        "caveat": (
            "HITL capital-map freeze from tip 6m grouping (P0–P4). Designed R. "
            "Does not raise live f. Canvas/display secondary to this scorecard + "
            "live_asset_profile.md."
        ),
        "panel": "2026.05.01 → 2026.10.20 tip",
        "primary": primary,
        "secondaries": secondaries,
        "attach_policy": ATTACH_POLICY,
        "hard_bans_remain": [["EURUSD", "AUDUSD"]],
        "soft_watch": [["DE40", "UK100"], ["JP225", "AAPL"]],
    }

    scorecard = {
        "task_id": "GRP-P5-T01",
        "generated_utc": generated,
        "primary_group": PRIMARY["group_id"],
        "n_secondaries": len(SECONDARIES),
        "attach_postures": {k: v["posture"] for k, v in ATTACH_POLICY.items()},
    }

    review = _review(decision)

    OUT_P5.mkdir(parents=True, exist_ok=True)
    ARCHIVE_P5.mkdir(parents=True, exist_ok=True)
    _write(OUT_P5 / "DECISION.json", decision)
    _write(OUT_P5 / "SCORECARD.json", scorecard)
    (OUT_P5 / "REVIEW.md").write_text(review, encoding="utf-8")

    for name in ("DECISION.json", "SCORECARD.json", "REVIEW.md"):
        shutil.copy2(OUT_P5 / name, ARCHIVE_P5 / name)

    print(f"P5 primary={PRIMARY['group_id']} secondaries={len(SECONDARIES)}")
    print(f"Wrote {OUT_P5}")
    print(f"Archived {ARCHIVE_P5}")
    return decision


def _review(d: dict) -> str:
    p = d["primary"]
    lines = [
        "# GRP-P5-T01 — HITL group promotion",
        "",
        f"**generated_utc:** {d['generated_utc']}",
        f"**status:** {d['hitl_status']}",
        f"**panel:** {d['panel']}",
        "",
        "## Caveat",
        "",
        d["caveat"],
        "",
        "## Primary",
        "",
        f"**{p['group_id']}** · policy `{p.get('policy')}` · weights `{p.get('weights')}`",
        "",
        p.get("rationale") or "",
        "",
        "| metric | value |",
        "| --- | ---: |",
    ]
    for k, v in (p.get("metrics") or {}).items():
        lines.append(f"| {k} | {v} |")

    lines += ["", "## Secondaries (policy menu)", ""]
    for s in d["secondaries"]:
        lines.append(
            f"- **{s['group_id']}** (`{s.get('policy')}`) — {s.get('rationale')}"
        )
        m = s.get("metrics") or {}
        lines.append(
            f"  sum_R={m.get('sum_R')} · m_hit={m.get('month_hit')} · "
            f"val={m.get('val_sum_R')} · maxDD={m.get('maxDD')} · "
            f"tail={m.get('max_tail_dep')} · w={s.get('weights')}"
        )

    lines += [
        "",
        "## VPS attach policy (primary map)",
        "",
        "| Sleeve | Posture | Bucket |",
        "| --- | --- | --- |",
    ]
    for aid, row in d["attach_policy"].items():
        lines.append(f"| {aid} | {row['posture']} | {row['bucket']} |")

    lines += [
        "",
        "## Next",
        "",
        "1. Operator confirms primary vs alternate on VPS.",
        "2. Update `doc/live_asset_profile.md` capital map (done with this task).",
        "3. No live f raise from tip grouping alone.",
        "",
        "Artefacts: `infra/artefacts/grouping/P5_LATEST/` · "
        "`blotter/archive/GRP-P5-T01/`",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    run()
