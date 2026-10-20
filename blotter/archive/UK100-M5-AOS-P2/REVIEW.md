# UK100-M5-AOS-P2 — REVIEW

**Task:** UK100-M5-AOS-P2 (T01–T07)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — L2det **v1b ARM_SOFT** (shadow) · L2AI **DISARM** · proceed P3  

---

## Parity (T01)

Tue=0 · ATR&gt;869=0 on tip and prior → **PASS**.

---

## Preferred stack (T02–T04 · T07)

```text
L2det_uk_m5_v1b = (Mon ∧ H12–13) ∨ (SELL ∧ H12–13)
```

| Metric | P0 tip | v1b kept |
| --- | ---: | ---: |
| n | 116 | 83 |
| WR | 52.6% | 61.4% |
| E_N | +0.183R | **+0.383R** |
| EF_proxy | +2.22 pp | **+11.08 pp** |
| ΔE_N | — | **+0.199R** |
| Retention | 100% | 71.6% |
| Prec. losers | — | 69.7% |
| Wed / H08–11 / BUY winner FP | — | 4 / 0 / 1 |

HITL: ARM_SOFT despite auto HOLD on Wed FP=4 (midday cell overlap; mornings protected).

**Rejected:** Mon∨H12 · H12∨Aug (FREQUENCY_STALL) · blanket BUY · blanket near_atr · M15 map imports.

---

## L2AI (T06)

AUC_tip≈0.40 · best thr hurts E_N → **DISARM**. Pin: `infra/artefacts/models/L2skip_uk_m5/LATEST/` SHADOW_ONLY.

---

## Artifacts

| Path | Role |
| --- | --- |
| `P2_CF.json` | Full policy + stack CF |
| `P2_SUMMARY.json` | Preferred stack snapshot |
| `run_p2_cf.py` | Builder |
| `doc/assets/UK100/aos_l2_policy_M5.md` | Normative pack |
| `doc/assets/UK100/aos_l2_size_table_M5.md` | f table spec |

---

## Next

`UK100-M5-AOS-P3` — L3 halt + L4 W20/W50 on v1b kept path.
