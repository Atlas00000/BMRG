# AOS-P7 Promotion Packet (paper)

**Phase:** AOS-P7 — full framework gates  
**Candidate:** `AOS_DET_STACK` (P6-T01 · L1+L2det+L3+L4+L6)  
**Engine ref:** Harvest 8210204 · `AOS_BASELINE_v1` EF **1.77**  
**Live hooks:** **DEFERRED** · **AOS_LIVE not signed**

---

## T01 — OS vs engine A/B

| Path | n | WR | EF | M | Zone |
| --- | ---: | ---: | ---: | ---: | --- |
| Engine labeled | 530 | 54.53 | 2.33 | 4.24 | Fragile |
| Official baseline | 530 | 54.5 | **1.77** | ~4.24 | Fragile |
| **OS det (L3 halt)** | **355** | 55.21 | **3.01** | 5.17 | Fragile |
| OS+AI CF (shadow) | 317 | 57.1 | 4.90 | 5.45 | Fragile |

Δ OS vs labeled engine: **+0.68 EF** · fires kept **67%**.

| Stage-1 check | Result |
| --- | --- |
| EF > 0 (keep iterating) | **PASS** |
| EF > M (promote target Robust) | **FAIL** (3.01 < 5.17) |

OS W250 EF **1.0** (Fragile). Verdict: **KEEP_ITERATING**.

---

## T02 — G3 + G4 light (OS blotter)

### G3 — **PASS**

`regime_filtered=true` (session 12–20 + skip Tue + OS L3 Below halt).  
DoW BM worst = Wed **+2.04 pp > 0**. Max DoW share 27.6% ≤ 70%.

### G4 light — **PASS** (MC-2)

| | MaxDD | Final | Ruin |
| --- | ---: | ---: | ---: |
| Observed | $28 | $474 | — |
| MC-2 block20 P95 | **$32** ≤ $100 | $474 | 0% |

MC-3 stress median final $351 &lt; $400 → stress warn (not required to fail G4 light).

---

## T03 — G5 stress on OS — **PASS** (core)

Engine geometry held; stress applied to OS-kept blotter.

| Stress | EF | EF>0 |
| --- | ---: | --- |
| base OS | 3.01 | Y |
| cost ×1.5 | **1.91** | Y |
| R −10% | 3.01 | Y |
| cost ×1.5 ∧ R −10% | **1.91** | Y |
| WR −10 pp (harsh proxy) | −7.13 | N (not a G5 param tag) |

Promote bar (EF>0 under cost ×1.5 + R−10 core): **PASS**.

---

## T04 — L10 HITL — **UNSIGNED**

| Item | Status |
| --- | --- |
| Promotion packet | `archive/AOS-P7-T04/promotion_packet.json` |
| `AOS_LIVE_v{N}` | **not issued** |
| Recommendation | **STAY_PAPER** |

### Blockers

1. Stage-1 still **Fragile** (EF &lt; M)  
2. Live EA hooks paused  
3. L10 human signature pending  

### Rollback (ready)

```text
python models/L2skip/rollback.py L2skip_v0_engine
engine: EDX-P2-T04 unchanged
OS: disable L3 halt / L2 AI → engine-only
```

---

## Gate stack summary

```text
G0 engine identity     PASS (frozen Harvest)
G1 EF>0 OS             PASS (iterate) · Robust FAIL
G3 regime_filtered     PASS
G4 light MC-2          PASS
G5 OS cost/R core      PASS
L10 sign-off           WAITING
LIVE HOOKS             DEFERRED

=> NOT PRODUCTION-WORTHY · STAY_PAPER
```

---

## Task verdicts

| Task | Verdict |
| --- | --- |
| P7-T01 | **ACCEPT** scorecard · **KEEP_ITERATING** (not promote) |
| P7-T02 | **ACCEPT** · G3/G4 light PASS |
| P7-T03 | **ACCEPT** · G5 core PASS |
| P7-T04 | **PACKET READY** · sign-off **WITHHELD** → STAY_PAPER |

Offline AOS P0–P7 paper path is **complete**. Unblock live only via hooks + Robust zone + L10 signature.
