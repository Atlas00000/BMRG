# EDX-P1 — Edge isolation (partial; log-based)

**Scored:** 2026-09-25 from `paired_events.csv` (n=571)  
**BWR reference:** 40% @ R=1.5  
**Rank rule:** cells with n≥30 only  
**Deferred:** ATR terciles / ER trend-range (need price series tagger) — P1-T03/T04/T05 pending tooling

---

## EDX-P1-T01 — Sessions (server hours of entry)

| Cell | n | WR | BM | E_N | Zone | Rank |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| LON 08–12 | 231 | 40.7% | **+0.7 pp** | +0.017R | Fragile | RANK |
| **LON–NY 12–17** | 236 | 47.0% | **+7.0 pp** | **+0.176R** | Robust* | RANK |
| NY 17–20 | 104 | 49.0% | **+9.0 pp** | **+0.226R** | Fragile† | RANK |
| Asia / other | 0 | — | — | — | — | filtered out by EA |

\*Gross Leak=0. †EF may still be ≤ M at this n.  
**BM_worst (sessions, n≥30):** LON (+0.7 pp) — still ≥ 0.  
**E_N concentration:** LON–NY ~60%, NY ~34%, LON ~6% → not >70% single-cell (G3 concentration OK on sessions alone).

**Where edge lives:** LON–NY overlap and NY afternoon.  
**Where edge is thin:** London morning.

---

## EDX-P1-T02 — Day-of-week

| Cell | n | WR | BM | E_N | Rank |
| --- | ---: | ---: | ---: | ---: | --- |
| Monday | 124 | 41.1% | +1.1 pp | +0.028R | RANK |
| **Tuesday** | 99 | 38.4% | **−1.6 pp** | −0.040R | RANK |
| **Wednesday** | 102 | 54.9% | **+14.9 pp** | **+0.373R** | RANK |
| Thursday | 130 | 41.5% | +1.5 pp | +0.038R | RANK |
| Friday | 116 | 49.1% | +9.1 pp | +0.228R | RANK |

**Loss cell:** Tuesday (BM≤0, n≥30) → filter candidate for P3.  
**Edge cell:** Wednesday (dominant), then Friday.

---

## Side / overnight / spread (extra isolation)

| Cell | n | WR | BM | Note |
| --- | ---: | ---: | ---: | --- |
| BUY | 270 | 44.4% | +4.4 pp | Balanced |
| SELL | 301 | 45.2% | +5.2 pp | Balanced |
| **Intraday exit** | 300 | 37.7% | **−2.3 pp** | Loss pocket |
| **Overnight hold** | 271 | 52.8% | **+12.8 pp** | Edge pocket |
| Spread low/mid/hi | 237/265/69 | ~44–51% | all BM>0 | Spread not the WR killer |

Hold time: winners avg **26.7h**, losers **17.6h** — winners more often survive overnight.

---

## EDX-P1-T06/T07 (partial)

| Check | Result |
| --- | --- |
| MAE/MFE path | Not available from deal log alone |
| Worst streak | 9 vs expected ~10.7 → no DEPENDENCE |
| TAIL_RISK | Need currency gross profit — deferred |
| Realisation mode | FIXED_RR_FADE (MID≈0) |

---

## EDX-P1-T08 — Isolation verdict memo

### WHERE the edge lives
1. **LON–NY (12–17)** and **NY (17–20)** sessions  
2. **Wednesday** (and Friday)  
3. Trades that **hold overnight** (higher WR)

### WHERE the losses live
1. **Tuesday** (BM ≤ 0)  
2. **Same-day round-trips** (intraday BM ≤ 0)  
3. **London morning** (barely above BE)  
4. Calendar hole **2026.08–09** (from P0-T04)

### Side diagnosis (reconfirmed)
**WR-side.** R ≈ RR; improve WR via session/DoW/hold filters before touching SL/TP geometry.

### Filter hypotheses for P3 (do not implement yet)
| Filter | Justification |
| --- | --- |
| Skip Tuesday | BM≤0, n=99≥30 |
| Prefer 12:00–20:00 (cut LON morning) | LON BM thin; concentration in afternoon |
| Optional: discourage quick intraday scratch | Intraday BM≤0 — needs careful design (not a simple session gate) |

### Deferred before P2
- P1-T03 ATR terciles  
- P1-T04 ER trend/range  
- P1-T05 BB width structure  
- Currency Leak + TAIL_RISK  

**P2 note:** Payoff experiments (SL/TP) are **lower priority** than P3 filters given WR-side diagnosis — unless ATR/ER later show R-side in a sub-cell.

---

## Status

| Task | Status |
| --- | --- |
| P1-T01 Session | DONE |
| P1-T02 DoW | DONE |
| P1-T03 ATR | PENDING (tooling) |
| P1-T04 ER | PENDING (tooling) |
| P1-T05 BB width | PENDING (tooling) |
| P1-T06 MAE/MFE | PENDING (ticks) |
| P1-T07 DEPENDENCE | DONE (clear) |
| P1-T08 Memo | DONE (this file) |
