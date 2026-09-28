# AOS-P0-T01 — Engine baseline lock REVIEW

**Scored / frozen:** 2026-09-25  
**Layer:** L0 (meta) — no OS code  
**Verdict:** **ACCEPT**

## What was done

Imported Harvest EDX health vectors into frozen `AOS_BASELINE_v1`. No Strategy Tester re-optimisation. Champion preset **unchanged**.

| Artifact | Path |
| --- | --- |
| Normative baseline | `doc/ai_OS_baseline.md` |
| Optional verify preset | `Profiles/Tester/BMRG/AOS-P0-T01_L0_baselineLock_Harvest_long.set` (magic **8310001**) |
| Engine champion | `EDX-P2-T04_…` magic **8210204** |
| Sources | `EDX-POOL_WINDOWS/SCORECARD_MATRIX.md` · `EDX-P2-T04/` |

## Locked primary (long)

n=530 · WR 54.5% · BWR 50% · R=1.0 · EF **1.77** · E_N **0.091** · Zone Fragile · ~$533

## Locked stress (3M)

n=49 · WR 59.2% · EF **6.43** · E_N **0.184** · $425.48

## Next

**AOS-P0-T02** — bad-cell registry from EDX (feeds L2).
