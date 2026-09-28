"""
INF-P6 phase-prove: engine vs L2 shadow CF on W250/W500 + long.
Still offline — no live preset.
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL))
SCORE = Path(__file__).resolve().parents[1] / "score"
sys.path.insert(0, str(SCORE))

from cf_eval import (  # noqa: E402
    FIXTURE,
    PIN,
    _load_jsonl,
    equity_path_and_maxdd,
    load_oos_skips,
)
from health import health_vector, load_baseline  # noqa: E402
from l3_l4_sim import apply_l3_over_l2, sim_to_dict, simulate_l3_l4  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
TAPE = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"
REPORTS = INFRA / "artefacts" / "reports"


def _pairs(fixture_dir: Path = FIXTURE) -> tuple[list[tuple[dict, dict]], float]:
    manifests = _load_jsonl(fixture_dir / "event_manifest.jsonl")
    legs = _load_jsonl(fixture_dir / "blotter_legs.jsonl")
    meta = json.loads((fixture_dir / "ea_metadata.json").read_text(encoding="utf-8"))
    by_leg = {leg["event_id"]: leg for leg in legs}
    pairs = []
    for m in manifests:
        if m.get("exit_reason") not in {"TP", "SL"}:
            continue
        leg = by_leg.get(m["event_id"])
        if not leg:
            continue
        pairs.append((m, leg))
    pairs.sort(key=lambda x: x[1]["entry_time"])
    return pairs, float(meta.get("designed_rr", 1.0))


def window_vector(pairs: list[tuple[dict, dict]], n: int, designed_rr: float) -> dict:
    if len(pairs) < 100:
        return {"n": len(pairs), "thin": True}
    window = pairs[-n:] if len(pairs) >= n else pairs
    hv = health_vector(
        [m for m, _ in window],
        [leg for _, leg in window],
        leak_policy="baseline_proxy",
        designed_rr=designed_rr,
    )
    dd = equity_path_and_maxdd(window)
    return {
        "thin": False,
        "window_n_requested": n,
        "n": hv["n"],
        "wr_pct": hv["wr_pct"],
        "bm_pp": hv["bm_pp"],
        "leak_pp": hv["leak_pp"],
        "ef_pp": hv["ef_pp"],
        "e_n": hv["e_n"],
        "m_pp": hv["m_pp"],
        "zone": hv["zone"],
        "maxdd_pp": dd["maxdd_pp"],
        "health_vector": hv,
    }


def path_scorecard(pairs: list[tuple[dict, dict]], designed_rr: float) -> dict:
    long_ = window_vector(pairs, len(pairs), designed_rr)
    return {
        "long": long_,
        "w250": window_vector(pairs, 250, designed_rr),
        "w500": window_vector(pairs, 500, designed_rr),
        "n_events": len(pairs),
    }


def _cell_bm(df: pd.DataFrame, mask: pd.Series) -> dict:
    sub = df.loc[mask]
    n = len(sub)
    if n == 0:
        return {"n": 0, "wr": None, "bm_pp": None, "hostile": False}
    wins = (sub["exit_reason"] == "TP").sum() if "exit_reason" in sub.columns else (sub["y_lose"] == 0).sum()
    wr = float(wins) / n
    bwr = 0.5  # Harvest R≈1
    bm_pp = 100.0 * (wr - bwr)
    return {
        "n": int(n),
        "wr": round(wr, 6),
        "bm_pp": round(bm_pp, 4),
        "hostile": bool(bm_pp <= 0 and n >= 30),
        "thin_hostile": bool(bm_pp <= 0 and n < 30),
    }


def audit_skip_clusters(skip_ids: set[str], model_dir: Path) -> dict:
    """
    Cluster OOS WOULD_SKIP by session×dow×side.
    Justify via BM_cell≤0 (hostile) or modest-confidence loser precision — never WR-only.
    """
    ledger = pd.read_csv(model_dir / "shadow_ledger_oos.csv")
    skips = ledger.loc[ledger["decision"] == "WOULD_SKIP"].copy()
    tape = pd.read_parquet(TAPE) if TAPE.exists() else None
    if tape is not None:
        tape["event_id"] = tape["event_id"].astype(str)
        skips = skips.merge(
            tape[["event_id", "session_id", "dow_name", "side", "hour_server", "exit_reason", "y_lose"]],
            on="event_id",
            how="left",
            suffixes=("", "_tape"),
        )
        engine_cells = tape.copy()
    else:
        engine_cells = None
        skips["session_id"] = "UNK"
        skips["dow_name"] = "UNK"
        skips["side"] = "UNK"

    clusters = []
    keys = ["session_id", "dow_name", "side"]
    for k in keys:
        if k not in skips.columns:
            skips[k] = "UNK"
    for (session, dow, side), g in skips.groupby(keys, dropna=False):
        n_skip = len(g)
        loser_hits = int(g["y_lose"].sum()) if "y_lose" in g.columns else 0
        precision = loser_hits / n_skip if n_skip else 0.0
        mean_p = float(g["p_lose"].mean()) if "p_lose" in g.columns else None
        mean_thr = float(g["thr"].mean()) if "thr" in g.columns else None
        cell = {"n": 0, "bm_pp": None, "hostile": False, "thin_hostile": False}
        if engine_cells is not None:
            mask = (
                (engine_cells["session_id"].astype(str) == str(session))
                & (engine_cells["dow_name"].astype(str) == str(dow))
                & (engine_cells["side"].astype(str) == str(side))
            )
            cell = _cell_bm(engine_cells, mask)

        modest_conf = bool(
            precision >= 0.5
            and mean_p is not None
            and mean_thr is not None
            and mean_p >= mean_thr - 1e-9
        )
        # Map known bad cells from aos_bad_cells.md
        registry_hit = None
        dow_s = str(dow)
        if dow_s.lower().startswith("tue"):
            registry_hit = "DOW_TUE"
        sess_s = str(session)
        if "LON" in sess_s.upper() and ("AM" in sess_s.upper() or "08" in sess_s):
            registry_hit = registry_hit or "SES_LON_AM"

        justified = bool(
            cell.get("hostile") or cell.get("thin_hostile") or modest_conf or registry_hit
        )
        justification = []
        if cell.get("hostile"):
            justification.append(f"BM_cell={cell['bm_pp']}pp≤0 n={cell['n']}≥30 (hostile)")
        elif cell.get("thin_hostile"):
            justification.append(f"BM_cell={cell['bm_pp']}pp≤0 n={cell['n']}<30 (thin hostile)")
        if modest_conf:
            justification.append(
                f"modest-confidence losers: precision={precision:.3f} mean_p_lose={mean_p:.3f}≥thr"
            )
        if registry_hit:
            justification.append(f"aos_bad_cells.md:{registry_hit}")
        if not justification:
            # Protect-edge overfilter (false-positive skip in BM>0 cell)
            if cell.get("bm_pp") is not None and cell["bm_pp"] > 0:
                justification.append(
                    f"UNJUSTIFIED edge overfilter — BM_cell={cell['bm_pp']}pp>0 "
                    f"loser_precision={precision:.3f} (protect cell; not WR-only path claim)"
                )
            else:
                justification.append("UNJUSTIFIED — needs evidence beyond WR")

        clusters.append(
            {
                "cluster_id": f"{session}|{dow}|{side}",
                "session_id": session,
                "dow_name": dow,
                "side": side,
                "n_skip": int(n_skip),
                "loser_precision": round(precision, 4),
                "mean_p_lose": round(mean_p, 6) if mean_p is not None else None,
                "cell_n": cell.get("n"),
                "cell_bm_pp": cell.get("bm_pp"),
                "hostile_cell": cell.get("hostile"),
                "registry_hit": registry_hit,
                "modest_confidence": modest_conf,
                "justified": justified,
                "justification": justification,
                "wr_only_forbidden": True,
            }
        )

    unjustified = [c for c in clusters if not c["justified"]]
    return {
        "n_skip_oos": int(len(skips)),
        "n_clusters": len(clusters),
        "clusters": sorted(clusters, key=lambda c: -c["n_skip"]),
        "unjustified_clusters": [c["cluster_id"] for c in unjustified],
        "audit_pass": len(unjustified) == 0,
        "rule": "Justify via BM_cell≤0 / aos_bad_cells / modest-confidence loser precision — never WR-only",
    }


def run_phase_prove() -> dict:
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    model_dir = Path(pin["path"])
    skip_ids = load_oos_skips(model_dir)
    pairs, designed_rr = _pairs()
    engine = path_scorecard(pairs, designed_rr)
    kept = [(m, leg) for m, leg in pairs if m["event_id"] not in skip_ids]
    shadow = path_scorecard(kept, designed_rr)

    n_eng = len(pairs)
    n_sh = len(kept)
    fires_kept_pct = 100.0 * n_sh / max(n_eng, 1)
    skip_rate_pct = 100.0 * (n_eng - n_sh) / max(n_eng, 1)

    eng_ef = engine["long"]["ef_pp"]
    sh_ef = shadow["long"]["ef_pp"]
    eng_en = engine["long"]["e_n"]
    sh_en = shadow["long"]["e_n"]
    eng_wr = engine["long"]["wr_pct"]
    sh_wr = shadow["long"]["wr_pct"]

    payoff_trap = (sh_wr > eng_wr) and (sh_en < eng_en or sh_ef < eng_ef)
    ef_held = sh_ef + 1e-9 >= eng_ef - 1.0  # protect bar floor
    ef_lifted = sh_ef + 1e-9 >= eng_ef
    starving = fires_kept_pct < 50.0
    fires_ok_pref = fires_kept_pct >= 70.0

    audit = audit_skip_clusters(skip_ids, model_dir)

    # L3 sim on shadow W250
    w250 = shadow["w250"]
    sim = simulate_l3_l4(
        w250_ef_pp=w250.get("ef_pp"),
        w250_e_n=w250.get("e_n"),
        maxdd_pp=w250.get("maxdd_pp") or 0.0,
        fires_90d=None,
    )
    over = apply_l3_over_l2("WOULD_SKIP", sim)

    checks = {
        "ef_held_or_lifted": ef_held,
        "ef_lifted": ef_lifted,
        "fires_ge_50pct": not starving,
        "fires_ge_70pct": fires_ok_pref,
        "no_payoff_trap": not payoff_trap,
        "skip_audit_pass": audit["audit_pass"],
        "w250_present": not engine["w250"].get("thin", True),
        "w500_present": not engine["w500"].get("thin", True),
        "maxdd_not_worse_gt_2pp": (shadow["long"]["maxdd_pp"] or 0)
        <= (engine["long"]["maxdd_pp"] or 0) + 2.0 + 1e-6,
    }
    metrics_accept = all(
        [
            checks["ef_held_or_lifted"],
            checks["fires_ge_50pct"],
            checks["no_payoff_trap"],
            checks["maxdd_not_worse_gt_2pp"],
        ]
    )
    prove_accept = metrics_accept and checks["skip_audit_pass"]

    # GO only if full prove (metrics + clean skip audit) and fires ≥70%
    go = prove_accept and checks["fires_ge_70pct"]

    baseline_doc = load_baseline()["windows"]["long"]

    report = {
        "task_id": "INF-P6-T01",
        "recipe": "INF-P6-T01_obs_phaseProve_W250W500_shadowVsEngine",
        "model_semver": pin.get("shadow_semver"),
        "model_path": str(model_dir),
        "engine": engine,
        "shadow_cf": shadow,
        "frequency": {
            "n_engine": n_eng,
            "n_shadow": n_sh,
            "n_skipped": n_eng - n_sh,
            "skip_rate_pct": round(skip_rate_pct, 4),
            "fires_kept_pct": round(fires_kept_pct, 4),
        },
        "deltas_long": {
            "ef_pp": round(sh_ef - eng_ef, 4),
            "e_n": round(sh_en - eng_en, 6),
            "wr_pct": round(sh_wr - eng_wr, 4),
            "maxdd_pp": round(
                (shadow["long"]["maxdd_pp"] or 0) - (engine["long"]["maxdd_pp"] or 0), 4
            ),
        },
        "deltas_w250": {
            "ef_pp": round(shadow["w250"]["ef_pp"] - engine["w250"]["ef_pp"], 4)
            if not shadow["w250"].get("thin") and not engine["w250"].get("thin")
            else None,
            "e_n": round(shadow["w250"]["e_n"] - engine["w250"]["e_n"], 6)
            if not shadow["w250"].get("thin") and not engine["w250"].get("thin")
            else None,
        },
        "deltas_w500": {
            "ef_pp": round(shadow["w500"]["ef_pp"] - engine["w500"]["ef_pp"], 4)
            if not shadow["w500"].get("thin") and not engine["w500"].get("thin")
            else None,
            "e_n": round(shadow["w500"]["e_n"] - engine["w500"]["e_n"], 6)
            if not shadow["w500"].get("thin") and not engine["w500"].get("thin")
            else None,
        },
        "skip_audit": audit,
        "l3_sim_shadow_w250": {
            "state": sim_to_dict(sim),
            "apply_would_skip": over,
        },
        "bars": {
            "engine_baseline_doc_ef": baseline_doc.get("ef_pp"),
            "ef_floor_engine_minus_1": eng_ef - 1.0,
        },
        "checks": checks,
        "payoff_trap": payoff_trap,
        "metrics_verdict": "ACCEPT" if metrics_accept else "REJECT",
        "prove_verdict": "ACCEPT" if prove_accept else "REJECT",
        "wiring_eligibility_hint": "GO" if go else "NO-GO",
        "retrain_path": None
        if go
        else "INF-W05/W06 — reduce edge-cell false-positive skips (LON_NY/NY protect cells)",
        "live_preset": "FORBIDDEN",
    }
    return report


def write_skip_audit_md(audit: dict, path: Path) -> None:
    lines = [
        "# INF-P6-T02 — Skip-cluster audit",
        "",
        f"**Recipe:** `INF-P6-T02_obs_skipClusterAudit_lowBar`",
        f"**OOS skips:** {audit['n_skip_oos']} · **clusters:** {audit['n_clusters']}",
        f"**Audit:** `{'PASS' if audit['audit_pass'] else 'FAIL'}`",
        "",
        audit["rule"],
        "",
        "| Cluster | n_skip | cell BM_pp | hostile | loser_prec | justification |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for c in audit["clusters"]:
        lines.append(
            f"| `{c['cluster_id']}` | {c['n_skip']} | {c['cell_bm_pp']} | "
            f"{c['hostile_cell']} | {c['loser_precision']} | {'; '.join(c['justification'])} |"
        )
    lines += [
        "",
        "## Unjustified",
        "",
    ]
    if audit["unjustified_clusters"]:
        for u in audit["unjustified_clusters"]:
            lines.append(f"- `{u}`")
    else:
        lines.append("_None — every skip cluster cites hostile cell / registry / modest-confidence losers._")
    lines += [
        "",
        "## WR-only ban",
        "",
        "No cluster is accepted solely because overall WR rose. Path-level payoff-trap check is separate (P6-T01).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_eligibility_md(report: dict, path: Path) -> None:
    go = report["wiring_eligibility_hint"] == "GO"
    freq = report["frequency"]
    eng = report["engine"]["long"]
    sh = report["shadow_cf"]["long"]
    lines = [
        "# INF wiring eligibility (INF-P6-T03)",
        "",
        f"**Recipe:** `INF-P6-T03_access_wiringEligibility_offline`",
        f"**Verdict:** **{'GO' if go else 'NO-GO'}**",
        f"**Source numbers:** `artefacts/reports/INF-P6-T01_phaseProve.json` only",
        f"**Live preset / AOS_LIVE:** FORBIDDEN until explicit post-GO authorisation of INF-P7 execution",
        "",
        "## Gate inputs (P6-T01)",
        "",
        "| Metric | Engine | Shadow CF | Δ |",
        "| --- | ---: | ---: | ---: |",
        f"| n | {freq['n_engine']} | {freq['n_shadow']} | {freq['n_shadow']-freq['n_engine']} |",
        f"| EF_pp (long) | {eng['ef_pp']} | {sh['ef_pp']} | {report['deltas_long']['ef_pp']} |",
        f"| E_N (long) | {eng['e_n']} | {sh['e_n']} | {report['deltas_long']['e_n']} |",
        f"| MaxDD_pp | {eng['maxdd_pp']} | {sh['maxdd_pp']} | {report['deltas_long']['maxdd_pp']} |",
        f"| fires_kept_pct | — | {freq['fires_kept_pct']} | — |",
        f"| skip_rate_pct | — | {freq['skip_rate_pct']} | — |",
        "",
        f"| W250 EF engine/shadow | {report['engine']['w250'].get('ef_pp')} / {report['shadow_cf']['w250'].get('ef_pp')} |",
        f"| W500 EF engine/shadow | {report['engine']['w500'].get('ef_pp')} / {report['shadow_cf']['w500'].get('ef_pp')} |",
        "",
        "## Checks",
        "",
    ]
    for k, v in report["checks"].items():
        lines.append(f"- `{k}`: **{v}**")
    lines += [
        "",
        f"- prove_verdict: **{report['prove_verdict']}**",
        f"- skip_audit_pass: **{report['skip_audit']['audit_pass']}**",
        f"- payoff_trap: **{report['payoff_trap']}**",
        "",
        "## Decision",
        "",
    ]
    if go:
        lines += [
            "**GO** for INF-W10 wiring **design** (INF-P7 docs only).",
            "",
            "Does **not** authorise live AI gate, forward test, or champion `.set` mutation.",
            "User must explicitly authorise any P7 code attach after reviewing `doc/infra_wiring_plan.md`.",
            "",
        ]
    else:
        reason = []
        if not report["checks"]["skip_audit_pass"]:
            reason.append(
                "skip-cluster audit FAIL — edge protect cells with low loser-precision skips: "
                + ", ".join(f"`{u}`" for u in report["skip_audit"]["unjustified_clusters"])
            )
        if not report["checks"]["ef_held_or_lifted"]:
            reason.append("EF not held vs engine−1pp")
        if not report["checks"]["fires_ge_50pct"]:
            reason.append("FREQUENCY_STALL fires <50%")
        if not report["checks"]["fires_ge_70pct"] and report["checks"]["skip_audit_pass"]:
            reason.append("fires <70% (preferred bar for GO)")
        if report.get("payoff_trap"):
            reason.append("payoff trap")
        lines += [
            "**NO-GO** — do not start INF-W10 wiring plan.",
            "",
            "Reasons:",
            "",
        ]
        for r in reason or ["see checks"]:
            lines.append(f"- {r}")
        lines += [
            "",
            f"**Return path:** {report.get('retrain_path') or 'INF-W05/W06'}",
            "",
        ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run() -> dict:
    report = run_phase_prove()
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "INF-P6-T01_phaseProve.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    audit_path = REPORTS / "INF-P6-T02_skip_audit.md"
    write_skip_audit_md(report["skip_audit"], audit_path)
    # also under infra/ root alias expected by roadmap
    (INFRA / "INF-P6-T02_skip_audit.md").write_text(
        audit_path.read_text(encoding="utf-8"), encoding="utf-8"
    )
    elig = INFRA.parent / "doc" / "infra_wiring_eligibility.md"
    # INFRA is Experts/BMRG/infra → parent is BMRG
    write_eligibility_md(report, elig)

    summary = {
        "task_ids": ["INF-P6-T01", "INF-P6-T02", "INF-P6-T03"],
        "recipe": "INF-P6_phaseProve_skipAudit_eligibility",
        "metrics_verdict": report["metrics_verdict"],
        "prove_verdict": report["prove_verdict"],
        "wiring_eligibility": report["wiring_eligibility_hint"],
        "retrain_path": report.get("retrain_path"),
        "frequency": report["frequency"],
        "deltas_long": report["deltas_long"],
        "checks": report["checks"],
        "skip_audit_pass": report["skip_audit"]["audit_pass"],
        "n_clusters": report["skip_audit"]["n_clusters"],
        "unjustified": report["skip_audit"]["unjustified_clusters"],
        "artefacts": {
            "phase_prove": str(REPORTS / "INF-P6-T01_phaseProve.json"),
            "skip_audit": str(audit_path),
            "eligibility": str(elig),
        },
        "live_preset": "FORBIDDEN",
        # Week ACCEPT = gate completed with explicit GO or NO-GO; metrics must hold
        "verdict": "ACCEPT" if report["metrics_verdict"] == "ACCEPT" else "REJECT",
    }

    (REPORTS / "INF-P6_scorecard.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (REPORTS / "LATEST_EVAL.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
