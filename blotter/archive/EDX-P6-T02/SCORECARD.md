# EDX-P6-T02 — Gate G1 (EF > M)

**Scored:** 2026-10-07  
**Source:** freeze run EDX-P6-T01 (magic 8230601 · 2026.03.23→2026.09.21) — no new Tester run.

## G1 checklist

| Check | Full window | Recent (2026-09) | Result |
| --- | ---: | ---: | --- |
| EF | **+0.53** | ≪0 (E_N −0.429) | — |
| M | **±11.06** | — | — |
| EF > M | **0.53 ≯ 11.06** | fail | **FAIL** |
| WR > BWR + Leak | 57.5% vs ~57.5% | fail | **FAIL** |
| n_tier for gate | Insufficient (&lt;100) | — | blocks production claim |

## Verdict

**G1 FAIL** — Fragile on full freeze; tip/recent month negative.  
`PRODUCTION-WORTHY(AUDUSD) = false` (G1 ∧ … blocked). Remaining G2–G5 not production-blocking until n/EF improve; optional diagnostic only.

## Next

**EDX-P7-T01** — pool table (EXPANSION_KEEP sleeve; not live).
