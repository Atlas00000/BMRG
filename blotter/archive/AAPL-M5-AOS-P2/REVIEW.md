# AAPL-M5-AOS-P2 — Review

**Date:** 2026-10-20  
**Tasks:** P2-T01…T07  
**Engine baseline:** magic **26102011** · tip May→Oct n=77  
**Compare:** offline CF on P1 tapes (not live Tester twin yet)

---

## Verdict

**ACCEPT P2** — L2det **v1b Jul ∨ Wed** **ARM_SOFT** · L2 AI **DISARM** · wire landed · presets authored.  
Next: **P3** L3/L4 (or Tester shadow confirm of v1b). Measured Leak still OPEN.

---

## P2-T01 parity

Tue=0 · ATR≤98 · BBw in-band on tip and YTD → **PASS**. No double-gate in L2det.

---

## Preferred stack (tip)

| | P0 | v1b Jul∨Wed |
| --- | ---: | ---: |
| n | 77 | 44 |
| E_N | +0.157R | **+0.349R** |
| ΔE_N | — | **+0.193R** |
| Retention | 100% | **57.1%** |
| Prec. losers | — | **63.6%** |
| May / Mon FP | — | **1 / 0** |
| Verdict | — | **ARM_SOFT** |

Jul alone also ARM_SOFT (+0.160R · 80.5% ret · 0 protect FP) — nested in v1b.

**REJECT:** May / Mon / BUY blankets · Jul∨Wed∨H18 (freq stall).  
**HOLD:** H18 · spread≥30 · H1 (YTD) · Jul∨H18 (2 May FP).  
**DISARM:** `L2skip_aapl_m5` AUC≈0.50.

---

## Wire / presets

| Artifact | Path |
| --- | --- |
| Include | `Include/AOS_L2det_aapl_m5.mqh` |
| Config / AOS router | `InpAOS_AAPL_M5_*` · M5 path before M15 |
| Policy | `doc/assets/AAPL/aos_l2_policy_M5.md` |
| Size spec | `doc/assets/AAPL/aos_l2_size_table_M5.md` |
| Shadow | `…/AAPL-M5-AOS-P2-T02_L2det_JulWed_shadow_Balanced.set` · **26162011** |
| Live | `…/AAPL-M5-AOS-P2-T02_L2det_JulWed_live_Balanced.set` · **26162012** |
| CF | `P2_CF.json` · `P2_SUMMARY.json` · `run_p2_cf.py` |
| AI pin | `infra/artefacts/models/L2skip_aapl_m5/LATEST/` (DISARM) |

Compile BMRG in MetaEditor before Tester shadow run.
