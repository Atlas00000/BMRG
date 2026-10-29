# GRP OOS-stable cluster pool

**Panel:** tip designed-R · 2026.05.01 → 2026.10.20  
**Universe (7):** EURUSD · JP225 · DE40 · AUDUSD · USDJPY · UK100 · AAPL  
**Source:** GRP-P2 OOS-stable (**24** packs) · metrics enriched GRP-P4  
**Artefacts:** `blotter/archive/GRP-P2-T01/OOS_TABLE.csv` · `GRP-P4-T01/OOS_ENRICHED.csv` · `GRP-P5-T01/DECISION.json`

## HITL vs pool

HITL (GRP-P5) **selects a default capital map** — it does **not** discharge or delete the rest of the OOS-stable set.

| Layer | Meaning |
| --- | --- |
| **Pool** | All 24 OOS-stable clusters below — research / rotate / CF candidates |
| **Pareto front (5)** | Policy champions from P4 (subset of pool) |
| **HITL freeze** | Current default attach map (primary + secondaries) — one posture, not the only valid packs |

Re-promote anytime from this pool after sleeve refresh (esp. UK100 L3v1d, AAPL tip).

### Hard constraints that still apply

| Rule | Note |
| --- | --- |
| **EURUSD+AUDUSD** | Hard ban — never in pool |
| **AUDUSD** | Allowed in some OOS packs; attach posture remains `ft_twin_only` until HITL revisits |
| **UK100** | Packs stay in pool; tip halt ~4 Sep understates Sep–Oct path — flag before SCALE |
| **AAPL** | Light / caution — EF Below history |

---

## Full pool (24) — sorted by tip ΣR

Equal-weight tip metrics. `HITL` = role on frozen map · `Pareto` = P4 front.

| # | Cluster | k | ΣR | m_hit | maxDD | fuse | val (Sep–Oct) | tail_dep | co_loss | Pareto | HITL |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | JP225+DE40 | 2 | **31.0** | 1.00 | −2.50 | 0 | +3.00 | 0.33 | 0.12 | yes | **primary** |
| 2 | EURUSD+JP225+DE40 | 3 | 27.3 | 1.00 | −2.67 | 0 | +3.67 | 0.45 | 0.21 | — | pool |
| 3 | JP225+DE40+USDJPY | 3 | 25.6 | 1.00 | −1.60 | 0 | +2.80 | 0.45 | 0.15 | — | pool |
| 4 | EURUSD+JP225 | 2 | 25.0 | 1.00 | −4.00 | 2 | +3.50 | 0.45 | 0.21 | — | pool |
| 5 | JP225+DE40+AUDUSD | 3 | 25.0 | 0.83 | −2.00 | 0 | 0.00 | 0.53 | 0.19 | — | pool · AUD |
| 6 | EURUSD+JP225+DE40+USDJPY | 4 | 24.2 | 1.00 | −1.70 | 0 | +3.35 | 0.49 | 0.21 | — | pool |
| 7 | EURUSD+JP225+UK100 | 3 | 23.6 | 1.00 | −2.67 | 1 | +2.17 | 0.48 | 0.21 | — | pool · UK |
| 8 | DE40+USDJPY | 2 | 23.4 | 1.00 | −4.28 | 1 | **+3.20** | 0.38 | 0.15 | yes | **holdout alt** |
| 9 | JP225+DE40+AUDUSD+USDJPY | 4 | 22.5 | 0.83 | −1.50 | 0 | +0.60 | 0.53 | 0.19 | — | pool · AUD |
| 10 | JP225+USDJPY | 2 | 22.4 | 1.00 | −1.50 | 0 | +2.20 | 0.45 | **0.05** | yes | **path alt** |
| 11 | EURUSD+DE40+USDJPY | 3 | 22.3 | 1.00 | −1.67 | 1 | **+3.80** | 0.49 | 0.17 | — | pool |
| 12 | JP225+USDJPY+UK100 | 3 | 21.9 | 0.83 | −2.33 | 1 | +1.30 | 0.48 | 0.17 | — | pool · UK |
| 13 | EURUSD+JP225+USDJPY | 3 | 21.6 | 1.00 | −2.00 | 0 | +3.13 | 0.49 | 0.21 | — | pool |
| 14 | EURUSD+JP225+USDJPY+UK100 | 4 | 21.4 | 1.00 | −1.75 | 1 | +2.23 | 0.49 | 0.21 | — | pool · UK |
| 15 | DE40+USDJPY+AAPL | 3 | 20.9 | 1.00 | −2.36 | 0 | +2.08 | 0.45 | 0.19 | — | pool · AAPL |
| 16 | EURUSD+DE40+USDJPY+AAPL | 4 | 20.7 | 1.00 | **−1.13** | 0 | +2.81 | 0.49 | 0.19 | yes | **min_maxDD alt** |
| 17 | DE40+AUDUSD+USDJPY | 3 | 19.9 | 0.83 | −1.85 | 0 | +0.13 | 0.53 | 0.19 | — | pool · AUD |
| 18 | DE40+AUDUSD+USDJPY+AAPL | 4 | 18.9 | 0.83 | −2.09 | 0 | +0.06 | 0.53 | 0.26 | — | pool · AUD/AAPL |
| 19 | EURUSD+USDJPY+UK100 | 3 | 18.5 | 1.00 | −2.17 | 3 | +2.30 | 0.49 | 0.17 | — | pool · UK |
| 20 | EURUSD+USDJPY+UK100+AAPL | 4 | 17.8 | 1.00 | −1.56 | 0 | +1.69 | 0.49 | 0.17 | — | pool · UK/AAPL |
| 21 | USDJPY+UK100 | 2 | 17.8 | 0.83 | −2.63 | 1 | +0.95 | **0.25** | 0.07 | yes | **min_tail watch** |
| 22 | EURUSD+USDJPY | 2 | 17.4 | 1.00 | −2.00 | 1 | +3.70 | 0.49 | 0.17 | — | pool |
| 23 | USDJPY+UK100+AAPL | 3 | 17.1 | 0.83 | −1.83 | 0 | +0.58 | 0.45 | 0.10 | — | pool · UK/AAPL |
| 24 | EURUSD+USDJPY+AAPL | 3 | 16.9 | 1.00 | −1.18 | 0 | +2.41 | 0.49 | 0.17 | — | pool · AAPL |

Boot month-hit p10 = **1.0** for packs #1–16 & #19–20 & #22 & #24; **0.67** for AUD/UK-light packs with m_hit 0.83 (#5,9,12,17–18,21,23).

---

## By theme (same 24)

### With EURUSD (12) — production-anchored research

| Cluster | ΣR | val | HITL |
| --- | ---: | ---: | --- |
| EUR+JP+DE | 27.3 | +3.67 | pool |
| EUR+JP | 25.0 | +3.50 | pool |
| EUR+JP+DE+JPY | 24.2 | +3.35 | pool |
| EUR+JP+UK | 23.6 | +2.17 | pool · UK |
| EUR+DE+JPY | 22.3 | **+3.80** | pool (best EUR holdout) |
| EUR+JP+JPY | 21.6 | +3.13 | pool |
| EUR+JP+JPY+UK | 21.4 | +2.23 | pool · UK |
| **EUR+DE+JPY+AAPL** | 20.7 | +2.81 | **frozen min_maxDD** |
| EUR+JPY+UK | 18.5 | +2.30 | pool · UK |
| EUR+JPY+UK+AAPL | 17.8 | +1.69 | pool |
| EUR+JPY | 17.4 | +3.70 | pool |
| EUR+JPY+AAPL | 16.9 | +2.41 | pool |

### No EUR — research / diversifier (12)

| Cluster | ΣR | val | HITL |
| --- | ---: | ---: | --- |
| **JP+DE** | 31.0 | +3.00 | **frozen primary** |
| JP+DE+JPY | 25.6 | +2.80 | pool |
| JP+DE+AUD | 25.0 | 0.00 | pool · AUD |
| **DE+JPY** | 23.4 | +3.20 | **frozen holdout** |
| JP+DE+AUD+JPY | 22.5 | +0.60 | pool · AUD |
| **JP+JPY** | 22.4 | +2.20 | **frozen path** |
| JP+JPY+UK | 21.9 | +1.30 | pool · UK |
| DE+JPY+AAPL | 20.9 | +2.08 | pool |
| DE+AUD+JPY | 19.9 | +0.13 | pool · AUD |
| DE+AUD+JPY+AAPL | 18.9 | +0.06 | pool |
| **JPY+UK** | 17.8 | +0.95 | **frozen watch** |
| JPY+UK+AAPL | 17.1 | +0.58 | pool |

---

## Not in pool (OOS fail — holdout)

8 clean-resilient packs failed Sep–Oct `val_sum_R < 0` (mostly AUD-led). Kept out of this pool until a new panel:

`JP225+AUDUSD` · `JP225+AUDUSD+UK100` · `JP225+AUDUSD+USDJPY` · `JP225+AUDUSD+USDJPY+UK100` · `AUDUSD+USDJPY` · `AUDUSD+USDJPY+AAPL` · `AUDUSD+USDJPY+UK100` · `AUDUSD+USDJPY+UK100+AAPL`

---

## How to use

1. **Default ops** → HITL map in `GRP-P5-T01/DECISION.json` / `doc/live_asset_profile.md`.
2. **Rotate / CF another pack** → pick from this pool; equal weight unless P3 scheme re-run.
3. **After UK L3v1d / sleeve refresh** → re-score UK-tagged rows; may reorder pool without discarding non-UK packs.
4. **Do not** treat Pareto-only or HITL-only as the exclusive research set.

**Roadmap:** `doc/asset_grouping_roadmap.md` · promote script does not shrink this file.
