# EDX-P05 — Data integrity, costs, RR−R

**Scored:** 2026-09-25 from T01 long archive  
**Artifacts:** `entries_parsed.csv`, `paired_events.csv`

---

## EDX-P05-T01 — Event aggregation audit

| Check | Result |
| --- | --- |
| MaxLevels / level index | All **572** opens at `level=0` |
| Opens | 572 |
| Exits TP/SL/MID | 255 / 315 / 1 |
| Opens − exits | **1** (open inventory / EOT residual) |
| FIFO paired events | 571 |
| SL distance | **300 pts exact** on all parsed entries |
| TP distance | **450 pts exact** |
| Designed RR | **1.500** |

**Accept:** G0 aggregation valid; ticket ≈ event; 1R declaration consistent.  
**Status:** DONE — PASS

---

## EDX-P05-T02 — Cost / Leak (defaults)

Entry spread mean ≈ **5.59 pts**.  
Proxy (edge_framework defaults): round-turn spread + slippage ≈ **3 × spread** = **16.8 pts**.

```
risk_distance = 300 pts
c_R = 16.8 / 300 = 0.056R
Leak = c_R / (R+1) = 0.056 / 2.5 = 0.0224 → 2.24 pp
```

| | Gross (Leak=0) | After default Leak |
| --- | ---: | ---: |
| BM | +4.74 pp | +4.74 pp |
| EF | +4.74 pp | **+2.50 pp** |
| M | ±4.08 pp | ±4.08 pp |
| Zone | barely Robust | **Fragile** |

Swap/overnight financing **not** in this proxy (pips run). True Leak ≥ 2.24 pp.

**Accept:** costs_defaulted flagged; EF after Leak → Fragile.  
**Status:** DONE

---

## EDX-P05-T03 — RR−R + side diagnosis

| Exit mix | Count | Share |
| --- | ---: | ---: |
| TP | 255 | 44.7% |
| SL | 315 | 55.2% |
| MID | 1 | ~0.2% |

| Metric | Value |
| --- | ---: |
| RR designed | 1.50 |
| R realised (proxy) | **≈ 1.50** |
| RR−R | **≈ 0** |
| AW | ≈ +1.5R |
| AL | ≈ 1.0R |

### Side diagnosis (locked for P0/P05)

**WR-side** — not R-side.

- Payoff geometry is intact (full SL/TP at design).  
- Hypothesis “AL too large compressing R” → **REJECTED** on G0 long sample.  
- Weakness = WR only ~5 pp above BWR gross, ~2.5 pp EF after default Leak → Fragile.

**Status:** DONE
