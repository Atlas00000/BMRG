# AOS bad-cell registry (L2 skip seeds)

**Task:** AOS-P0-T02  
**Frozen:** 2026-09-25  
**Purpose:** Feed **L2 deterministic skip map v0** — consume EDX, do not rediscover.  
**Engine:** Harvest champion (already applies session 12–20 + skip Tue).  
**Baseline:** `doc/ai_OS_baseline.md` (`AOS_BASELINE_v1`)  
**Archive:** `blotter/archive/AOS-P0-T02/`

**Rule (from `doc/ai_OS.md`):** skip cells with **BM_cell ≤ 0** and **n ≥ 30**.  
Do **not** skip merely weaker cells if cell EF / BM still &gt; 0 — unless marked soft-caution for AI threshold only.

BWR context for P1 isolation table: **40%** @ R=1.5 (Growth-era log `paired_events.csv` n=571).  
Harvest champion uses BWR **50%** @ R=1.0 — re-score cells on Harvest tape in AOS-P1 before promoting soft rules to hard skips.

---

## 1. Hard skip seeds (BM ≤ 0, n ≥ 30)

| Cell ID | Definition | n | WR | BM | E_N | Source | L2 action v0 |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `DOW_TUE` | Entry DoW = Tuesday | 99 | 38.4% | **−1.6 pp** | −0.040R | `EDX-P1_ISOLATION.md` T02 | **HARD SKIP** — already in engine (`TradeTue=false`); OS must parity-assert |
| `EXIT_INTRADAY` | Same-calendar-day round trip (entry day = exit day) | 300 | 37.7% | **−2.3 pp** | — | `EDX-P1_ISOLATION.md` side/overnight | **DEFER hard skip** — not a session gate; candidate for **L8** path/hold advisor + L2 AI feature only until designed |

---

## 2. Soft caution (BM &gt; 0 but thin / known weak)

| Cell ID | Definition | n | WR | BM | E_N | Source | L2 action v0 |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `SES_LON_AM` | Server entry hour 08–12 | 231 | 40.7% | **+0.7 pp** | +0.017R | `EDX-P1_ISOLATION.md` T01 | **SOFT** — do not hard-skip alone. P3-T01 session-only **REJECT** (cut AM hurt overall). Champ stack keeps 12–20 with skip-Tue. Optional soft veto only if OS widens session. |
| `SIDE_BUY_ONLY` | AllowBuy ∧ ¬AllowSell (Growth P25) | 318 | 41.8% | — | 0.046 · **EF −0.38** | `EDX-P25-T03/REVIEW.md` | **SOFT** — raise AI skip threshold on buys; **never** rewrite to sell-only |
| `CAL_LATE_CYCLE` | Calendar stress Aug–Sep 2026 / incomplete month | thin | — | collapse | — | `EDX-P0-T04` · P1 memo | **SOFT** — L4 lifecycle / L7 weight; not a static hour skip |
| `GEOM_BBDEV_20` | BBDev=2.0 on Growth hygiene | 3M n=34 | 41.2% | +1.2 | EF **−1.02** | `EDX-P25-T01` | **SOFT** — avoid narrowing k; not an L2 time skip |

---

## 3. Edge cells (protect — do not skip)

| Cell ID | Definition | n | BM / note | Source | L2 action |
| --- | --- | ---: | --- | --- | --- |
| `SES_LON_NY` | 12–17 | 236 | BM **+7.0** | P1-T01 | **FIRE allowed** |
| `SES_NY` | 17–20 | 104 | BM **+9.0** | P1-T01 | **FIRE allowed** |
| `DOW_WED` | Wednesday | 102 | BM **+14.9** | P1-T02 | **FIRE allowed** |
| `DOW_FRI` | Friday | 116 | BM **+9.1** | P1-T02 | **FIRE allowed** |
| `HOLD_OVERNIGHT` | Exit next calendar day+ | 271 | BM **+12.8** | P1 extra | **FIRE allowed** — do not force same-day scratch |
| `STACK_CHAMP` | Session 12–20 ∧ ¬Tue | — | Growth/Harvest champ | P3-T05 · P2-T04 | **Engine default** — OS assumes this stack |

---

## 4. Already encoded in champion engine

| Control | Engine input | EDX justification |
| --- | --- | --- |
| Skip Tuesday | `InpTradeTue=false` | `DOW_TUE` BM≤0 |
| Session 12–20 | `InpStartHour=12` `InpEndHour=20` | Edge in LON–NY/NY; stack beat P0 |
| Both sides | `AllowBuy=AllowSell=true` | Buy-only Leak fail (P25) |
| G0 | MaxLevels=1 MaxEntries=1 | Event = ticket |

**OS parity tasks:** `AOS-P2-T01` (Tue), `AOS-P2-T02` (LON AM soft only if session widened).

---

## 5. Geometry / sleeve cells (not L2 time skips)

| Cell | Verdict | Source | OS note |
| --- | --- | --- | --- |
| TP600 RR2 | **DROP** (3M WR&lt;BWR) | EDX-P2-T03 | Do not reintroduce via L2 |
| Mid TP=0 | costs_fragile EF≤0 | EDX-P2-T05 | L7 block Mid |
| G5 TP−10 on Growth | EF≤0 | EDX-P4-T05 | Promotion stress; not a skip cell |
| Survival 3M | costs_fragile | EDX-P2-T01 | L7 cut weight when Compressing |

---

## 6. Deferred (need L1 tape)

| Cell family | Why deferred | Unlocks |
| --- | --- | --- |
| ATR terciles | P1-T03 tooling | L1 vol tags |
| ER trend/range | P1-T04 | L1 structure |
| BB width | P1-T05 | L1 compression |
| MAE/MFE loser shapes | P1-T06 | L8 early-abort |
| Harvest-native BM by cell | P1 used Growth-era BWR 40% | Recompute under R=1 / BWR 50% |

---

## 7. L2 skip map v0 (machine-readable intent)

```text
HARD_SKIP:
  - DOW_TUE                    # parity with engine

SOFT_CAUTION (AI threshold / advisory only):
  - SES_LON_AM                 # only if session window expanded beyond champ
  - SIDE_BUY                   # higher P(skip|buy) than sell; never sell-only
  - EXIT_INTRADAY_FEATURE      # feature for L2/L8; no hard gate yet
  - CAL_LATE_CYCLE             # L4/L7 weight, not hour skip

NEVER_SKIP:
  - SES_LON_NY, SES_NY, DOW_WED, DOW_FRI, HOLD_OVERNIGHT
  - cells with BM_cell > 0 and EF_cell > 0 unless FREQUENCY allows and AOS task accepts
```

---

## 8. Accept criteria (this task)

| Check | Status |
| --- | --- |
| Each hard/soft cell cites EDX archive | **PASS** |
| BM / n recorded where available | **PASS** |
| Session-only pitfall documented (P3-T01 REJECT) | **PASS** |
| Feeds AOS-P2 without rediscovery | **PASS** |

**Verdict:** **ACCEPT** — registry ready for L1 tape + L2 gates.
