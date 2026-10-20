# EDX-P1-T03 — ATR × ER regime tags

**Scored:** 2026-10-07 · offline  
**Trades:** mag **8230111** · n=58 · May→Aug  
**Price:** MT5 `copy_rates_range` AUDUSD M5 (31 363 bars)  
**Method:** ATR Wilder(14) percentile vs prior 5000 bars · ER(50) · trending if ER≥0.3 · shift-1 bar

## Cells (R=1 · BWR=50%)

| Cell | n | WR | BM | E_N |
| --- | ---: | ---: | ---: | ---: |
| **ATR_high \| ranging** | 25 | 72.0% | **+22.0 pp** | **+0.440R** |
| ATR_high \| trending | 11 | 54.5% | +4.5 pp | +0.091R |
| ATR_mid \| ranging | 17 | 47.1% | **−2.9 pp** | −0.059R |
| ATR_low \| ranging | 4 | 75.0% | +25.0 pp | +0.500R |
| ATR_low \| trending | 1 | 100% | — | thin |

### Marginal slices

| Slice | n | WR | BM | E_N |
| --- | ---: | ---: | ---: | ---: |
| ATR_high | 36 | 66.7% | +16.7 pp | +0.333R |
| ATR_mid | 17 | 47.1% | −2.9 pp | −0.059R |
| ATR_low | 5 | 80.0% | +30.0 pp | +0.600R |
| **ranging** | 46 | 63.0% | +13.0 pp | +0.261R |
| trending | 12 | 58.3% | +8.3 pp | +0.167R |

## Framework outputs

| Metric | Value |
| --- | --- |
| BM_worst (cells, provisional n≥8) | **ATR_mid\|ranging** BM −2.9 pp |
| No cell with n≥30 and BM≤0 | ATR gate **not** hard-justified yet |
| Concentration | best **ATR_high\|ranging** share **91.7%** → `REGIME_CONCENTRATED` |
| G3 note | Allowed with declared `regime_filtered=true` (session+Tue) — home regime is high-ATR range fade |

## Read for P2 / P3 / P4

1. **Home edge:** high-ATR **ranging** — matches meanrev class thesis.  
2. **Soft loss pocket:** mid-ATR ranging (provisional) — optional ATR band later, not before payoff/session filters.  
3. Do **not** filter to “only ranging” yet (trending still E_N>0; n thin).  
4. Concentration flag = expected for Harvest fade; not an auto DROP.

**Verdict:** **ACCEPT** — isolation complete for regime dimension.
