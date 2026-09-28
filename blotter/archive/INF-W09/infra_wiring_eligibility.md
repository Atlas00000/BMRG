# INF wiring eligibility (INF-P6-T03)

**Recipe:** `INF-P6-T03_access_wiringEligibility_offline`
**Verdict:** **NO-GO**
**Source numbers:** `artefacts/reports/INF-P6-T01_phaseProve.json` only
**Live preset / AOS_LIVE:** FORBIDDEN until explicit post-GO authorisation of INF-P7 execution

## Gate inputs (P6-T01)

| Metric | Engine | Shadow CF | Δ |
| --- | ---: | ---: | ---: |
| n | 530 | 491 | -39 |
| EF_pp (long) | 2.3283 | 2.9935 | 0.6652 |
| E_N (long) | 0.090566 | 0.10387 | 0.013304 |
| MaxDD_pp | 20.9774 | 16.8403 | -4.1371 |
| fires_kept_pct | — | 92.6415 | — |
| skip_rate_pct | — | 7.3585 | — |

| W250 EF engine/shadow | 4.2 / 4.2 |
| W500 EF engine/shadow | 1.4 / 2.9935 |

## Checks

- `ef_held_or_lifted`: **True**
- `ef_lifted`: **True**
- `fires_ge_50pct`: **True**
- `fires_ge_70pct`: **True**
- `no_payoff_trap`: **True**
- `skip_audit_pass`: **False**
- `w250_present`: **True**
- `w500_present`: **True**
- `maxdd_not_worse_gt_2pp`: **True**

- prove_verdict: **REJECT**
- skip_audit_pass: **False**
- payoff_trap: **False**

## Decision

**NO-GO** — do not start INF-W10 wiring plan.

Reasons:

- skip-cluster audit FAIL — edge protect cells with low loser-precision skips: `LON_NY|Mon|BUY`, `LON_NY|Thu|SELL`, `NY|Mon|BUY`

**Return path:** INF-W05/W06 — reduce edge-cell false-positive skips (LON_NY/NY protect cells)
