#!/usr/bin/env python3
"""AOS phase verification — re-check P0–P7 artifacts + aistack offline path.

Exit 0 = all checks PASS. Writes blotter/archive/AOS-VERIFY/phase_report.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "blotter" / "archive"
OUT = ARCH / "AOS-VERIFY"
BWR, LEAK, R = 50.0, 2.2, 1.0
BASE_EF = 1.77


def score(outcomes, leak=LEAK, r=R):
    outcomes = np.asarray(outcomes)
    n = len(outcomes)
    if n == 0:
        return {"n": 0, "EF": None, "zone": None}
    tp = int((outcomes == "TP").sum())
    wr = 100.0 * tp / n
    bm = wr - BWR
    ef = bm - leak
    m = 100 * 1.96 * np.sqrt((wr / 100) * (1 - wr / 100) / n)
    zone = "Below" if ef <= 0 else ("Fragile" if ef <= m else "Robust")
    return {"n": n, "WR": round(wr, 2), "EF": round(ef, 2), "M": round(m, 2), "zone": zone}


def ok(cond: bool, msg: str, fails: list) -> None:
    if not cond:
        fails.append(msg)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    fails: list[str] = []
    report: dict = {"phases": {}}

    # --- P0 ---
    p0 = []
    ok((ROOT / "doc/ai_OS_baseline.md").exists(), "P0 missing ai_OS_baseline.md", p0)
    ok((ROOT / "doc/aos_bad_cells.md").exists(), "P0 missing aos_bad_cells.md", p0)
    ok((ARCH / "AOS-P0-T01/BASELINE.json").exists() or (ARCH / "AOS-P0-T01/REVIEW.md").exists(),
       "P0-T01 archive missing", p0)
    report["phases"]["P0"] = {"pass": len(p0) == 0, "fails": p0}
    fails.extend(p0)

    # --- P1 ---
    p1 = []
    ok((ROOT / "doc/aos_l1_feature_schema.md").exists(), "P1 schema missing", p1)
    ok((ROOT / "doc/aos_l1_tape_contract.md").exists(), "P1 tape contract missing", p1)
    fires = ARCH / "AOS-P1-T02/harvest_long_fires.csv"
    ok(fires.exists(), "P1 tape fires missing", p1)
    if fires.exists():
        n = len(pd.read_csv(fires))
        ok(n >= 500, f"P1 fires n={n} < 500", p1)
        report["phases"]["P1"] = {"pass": len(p1) == 0, "fails": p1, "n_fires": n}
    else:
        report["phases"]["P1"] = {"pass": False, "fails": p1}
    fails.extend(p1)

    # --- P2 ---
    p2 = []
    lab_path = ARCH / "AOS-P2-T03/harvest_long_labeled.csv"
    ok((ROOT / "doc/aos_l2_policy_v0.md").exists(), "P2 policy missing", p2)
    ok(lab_path.exists(), "P2 labeled csv missing", p2)
    lab = None
    if lab_path.exists():
        lab = pd.read_csv(lab_path)
        ok(len(lab) == 530, f"P2 n={len(lab)} != 530", p2)
        ok((lab["dow"] == "Tue").sum() == 0, "P2 Tue fires present", p2)
        s = score(lab["outcome"].values)
        ok(abs(s["EF"] - 2.33) < 0.05, f"P2 EF={s['EF']} != ~2.33", p2)
        report["phases"]["P2"] = {"pass": len(p2) == 0, "fails": p2, "score": s}
    else:
        report["phases"]["P2"] = {"pass": False, "fails": p2}
    fails.extend(p2)

    # --- P3 ---
    p3 = []
    ok((ROOT / "doc/aos_l3_l4_offline.md").exists(), "P3 doc missing", p3)
    life = ARCH / "AOS-P3-T03/rolling_W250_lifecycle.csv"
    trips = ARCH / "AOS-P3-T01/L3_trips_simulated.csv"
    ok(life.exists(), "P3 lifecycle missing", p3)
    ok(trips.exists(), "P3 trips missing", p3)
    if life.exists():
        lf = pd.read_csv(life)
        last = lf.iloc[-1]
        ok(float(last["W250_EF"]) > 0, f"P3 terminal W250 EF={last['W250_EF']}", p3)
        report["phases"]["P3"] = {
            "pass": len(p3) == 0,
            "fails": p3,
            "terminal_W250_EF": float(last["W250_EF"]),
            "terminal_lifecycle": str(last["lifecycle"]),
            "n_trips": int(len(pd.read_csv(trips))) if trips.exists() else 0,
        }
    else:
        report["phases"]["P3"] = {"pass": False, "fails": p3}
    fails.extend(p3)

    # --- P4 ---
    p4 = []
    ok((ROOT / "doc/aos_l2skip_v1.md").exists(), "P4 doc missing", p4)
    model = ARCH / "AOS-P4-T02/L2skip_v1.joblib"
    metrics = ARCH / "AOS-P4-T02/L2skip_v1_metrics.json"
    shadow = ARCH / "AOS-P4-T03/shadow_counterfactual.json"
    ok(model.exists(), "P4 model missing", p4)
    ok(metrics.exists(), "P4 metrics missing", p4)
    ok(shadow.exists(), "P4 shadow missing", p4)
    if metrics.exists():
        m = json.loads(metrics.read_text(encoding="utf-8"))
        ok(0.5 <= m["auc_oos"] <= 0.7, f"P4 AUC unexpected {m['auc_oos']}", p4)
    if shadow.exists():
        sh = json.loads(shadow.read_text(encoding="utf-8"))
        ok(sh["loose_bar"]["EF_hold_vs_AOS_BASELINE"], "P4 shadow EF hold fail", p4)
        report["phases"]["P4"] = {
            "pass": len(p4) == 0,
            "fails": p4,
            "auc_oos": m.get("auc_oos") if metrics.exists() else None,
            "cf_EF": sh["cf_apply_skips_all_tape"]["EF"],
        }
    else:
        report["phases"]["P4"] = {"pass": False, "fails": p4}
    # loadability
    if model.exists():
        try:
            blob = joblib.load(model)
            ok("pipeline" in blob and "thr" in blob, "P4 joblib schema bad", p4)
        except Exception as e:
            ok(False, f"P4 joblib load fail: {e}", p4)
    fails.extend(p4)

    # --- P5 ---
    p5 = []
    live = ROOT / "models/L2skip/LIVE.json"
    rb = ROOT / "models/L2skip/rollback.py"
    dry = ARCH / "AOS-P5-T02/champ_challenger_dryrun.json"
    ok((ROOT / "doc/aos_l5_retrain_loop.md").exists(), "P5 doc missing", p5)
    ok(live.exists(), "P5 LIVE.json missing", p5)
    ok(rb.exists(), "P5 rollback.py missing", p5)
    ok(dry.exists(), "P5 dryrun missing", p5)
    if live.exists():
        lj = json.loads(live.read_text(encoding="utf-8-sig"))
        ok(lj["pinned_version"] == "L2skip_v0_engine", f"P5 pin={lj.get('pinned_version')}", p5)
        ok(lj.get("shadow_version") == "L2skip_v1", "P5 shadow pin wrong", p5)
    if dry.exists():
        d = json.loads(dry.read_text(encoding="utf-8"))
        ok(d.get("dry_run_pass") is True, "P5 dry_run_pass false", p5)
    report["phases"]["P5"] = {"pass": len(p5) == 0, "fails": p5, "LIVE": lj if live.exists() else None}
    fails.extend(p5)

    # --- P6 ---
    p6 = []
    ok((ROOT / "doc/aos_p6_stack.md").exists(), "P6 doc missing", p6)
    det = ARCH / "AOS-P6-T01/stack_det_score.json"
    ai = ARCH / "AOS-P6-T02/stack_ai_shadow_score.json"
    ok(det.exists(), "P6 det score missing", p6)
    ok(ai.exists(), "P6 ai score missing", p6)
    if det.exists() and lab is not None:
        ds = json.loads(det.read_text(encoding="utf-8"))
        ok(ds.get("accept") is True, "P6 det accept false", p6)
        ok(abs(ds["det_after_L3_halts"]["EF"] - 3.01) < 0.05, "P6 det EF drift", p6)
        # recompute det path
        ledger = pd.read_csv(ARCH / "AOS-P6-T01/stack_det_ledger.csv")
        kept = lab.loc[ledger["decision"].values == "FIRE", "outcome"].values
        rs = score(kept)
        ok(abs(rs["EF"] - 3.01) < 0.05, f"P6 recompute EF={rs['EF']}", p6)
        report["phases"]["P6"] = {"pass": len(p6) == 0, "fails": p6, "det": ds["det_after_L3_halts"], "recompute": rs}
    else:
        report["phases"]["P6"] = {"pass": False, "fails": p6}
    fails.extend(p6)

    # --- P7 ---
    p7 = []
    ok((ROOT / "doc/aos_p7_promotion.md").exists(), "P7 doc missing", p7)
    pkt = ARCH / "AOS-P7-T04/promotion_packet.json"
    ab = ARCH / "AOS-P7-T01/ab_scorecard.json"
    g5 = ARCH / "AOS-P7-T03/g5_os_stress.json"
    ok(pkt.exists(), "P7 packet missing", p7)
    ok(ab.exists(), "P7 ab missing", p7)
    ok(g5.exists(), "P7 g5 missing", p7)
    if pkt.exists():
        pk = json.loads(pkt.read_text(encoding="utf-8"))
        ok(pk.get("AOS_LIVE_signed") is False, "P7 unexpectedly signed", p7)
        ok(pk.get("recommendation") == "STAY_PAPER", "P7 not STAY_PAPER", p7)
    if g5.exists():
        g5j = json.loads(g5.read_text(encoding="utf-8"))
        ok(g5j.get("verdict_T03") == "PASS", "P7 G5 not PASS", p7)
    report["phases"]["P7"] = {"pass": len(p7) == 0, "fails": p7}
    fails.extend(p7)

    # --- aistack offline (det L3 + AI skip CF) ---
    aistack = []
    if lab is not None and (ARCH / "AOS-P6-T01/stack_det_ledger.csv").exists() and (
        ARCH / "AOS-P4-T03/shadow_decisions.csv"
    ).exists():
        ledger = pd.read_csv(ARCH / "AOS-P6-T01/stack_det_ledger.csv")
        shd = pd.read_csv(ARCH / "AOS-P4-T03/shadow_decisions.csv")
        fire = ledger["decision"].values == "FIRE"
        ai_skip = shd["shadow_skip"].fillna(0).astype(int).values
        keep = fire & (ai_skip == 0)
        st = score(lab.loc[keep, "outcome"].values)
        ok(st["n"] >= 100, f"aistack n={st['n']}", aistack)
        ok(st["EF"] is not None and st["EF"] >= BASE_EF - 1.0, f"aistack EF={st['EF']} below loose", aistack)
        ok(st["EF"] > 0, "aistack EF<=0", aistack)
        report["aistack"] = {
            "pass": len(aistack) == 0,
            "fails": aistack,
            "score": st,
            "layers": "L1+L2det+L3+L4+L6 + L2skip_v1(CF) + L5pin_shadow + L7HarvestPrimary",
            "live_ai_armed": False,
            "expected_EF_approx": 4.9,
        }
        fails.extend(aistack)
    else:
        aistack.append("missing inputs for aistack")
        report["aistack"] = {"pass": False, "fails": aistack}
        fails.extend(aistack)

    report["all_pass"] = len(fails) == 0
    report["fail_count"] = len(fails)
    (OUT / "phase_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    # human summary
    lines = ["AOS PHASE VERIFY", "=" * 40]
    for ph, body in report["phases"].items():
        lines.append(f"{ph}: {'PASS' if body['pass'] else 'FAIL'} {body.get('fails') or ''}")
    if "aistack" in report:
        lines.append(
            f"aistack: {'PASS' if report['aistack']['pass'] else 'FAIL'} "
            f"{report['aistack'].get('score')}"
        )
    lines.append(f"ALL: {'PASS' if report['all_pass'] else 'FAIL'} ({report['fail_count']} fails)")
    summary = "\n".join(lines)
    (OUT / "SUMMARY.txt").write_text(summary, encoding="utf-8")
    print(summary)
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
