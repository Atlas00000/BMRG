# INF-P6-T02 — Skip-cluster audit

**Recipe:** `INF-P6-T02_obs_skipClusterAudit_lowBar`
**OOS skips:** 39 · **clusters:** 12
**Audit:** `FAIL`

Justify via BM_cell≤0 / aos_bad_cells / modest-confidence loser precision — never WR-only

| Cluster | n_skip | cell BM_pp | hostile | loser_prec | justification |
| --- | ---: | ---: | --- | ---: | --- |
| `LON_NY|Wed|SELL` | 9 | 8.1818 | False | 0.6667 | modest-confidence losers: precision=0.667 mean_p_lose=0.694≥thr |
| `LON_NY|Fri|SELL` | 8 | 7.6271 | False | 0.75 | modest-confidence losers: precision=0.750 mean_p_lose=0.712≥thr |
| `LON_NY|Mon|SELL` | 7 | 3.7037 | False | 0.5714 | modest-confidence losers: precision=0.571 mean_p_lose=0.729≥thr |
| `LON_NY|Thu|SELL` | 4 | 6.3636 | False | 0.25 | UNJUSTIFIED edge overfilter — BM_cell=6.3636pp>0 loser_precision=0.250 (protect cell; not WR-only path claim) |
| `LON_NY|Thu|BUY` | 2 | -0.8772 | True | 0.5 | BM_cell=-0.8772pp≤0 n=57≥30 (hostile); modest-confidence losers: precision=0.500 mean_p_lose=0.686≥thr |
| `LON_NY|Wed|BUY` | 2 | 1.8519 | False | 0.5 | modest-confidence losers: precision=0.500 mean_p_lose=0.666≥thr |
| `NY|Wed|SELL` | 2 | -2.6316 | False | 0.5 | BM_cell=-2.6316pp≤0 n=19<30 (thin hostile); modest-confidence losers: precision=0.500 mean_p_lose=0.706≥thr |
| `LON_NY|Fri|BUY` | 1 | 5.5556 | False | 1.0 | modest-confidence losers: precision=1.000 mean_p_lose=0.680≥thr |
| `LON_NY|Mon|BUY` | 1 | 6.5217 | False | 0.0 | UNJUSTIFIED edge overfilter — BM_cell=6.5217pp>0 loser_precision=0.000 (protect cell; not WR-only path claim) |
| `NY|Mon|BUY` | 1 | 25.0 | False | 0.0 | UNJUSTIFIED edge overfilter — BM_cell=25.0pp>0 loser_precision=0.000 (protect cell; not WR-only path claim) |
| `NY|Thu|SELL` | 1 | -4.5455 | False | 0.0 | BM_cell=-4.5455pp≤0 n=11<30 (thin hostile) |
| `NY|Wed|BUY` | 1 | -10.0 | False | 0.0 | BM_cell=-10.0pp≤0 n=20<30 (thin hostile) |

## Unjustified

- `LON_NY|Mon|BUY`
- `LON_NY|Thu|SELL`
- `NY|Mon|BUY`

## WR-only ban

No cluster is accepted solely because overall WR rose. Path-level payoff-trap check is separate (P6-T01).
