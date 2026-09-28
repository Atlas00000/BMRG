# BMRG System Profile

**EA:** Bollinger Mean-Reversion Grid (`BMRG.ex5` **v1.20** + optional AOS overlay)  
**Profile date:** 2026-09-27 (rev. AOS wire + aistack tester)  
**Framework:** `doc/unified_edge_framework.md` · `doc/edge_framework.md`  
**Discovery:** `doc/edge_discovery.md` · **Pool:** `doc/candidate_pool.md`  
**AI OS:** `doc/ai_OS.md` v0.2 · preset `aistack` (magic **8399001**)  
**Status:** Descriptive behaviour + class thesis. Gate / OS verdicts live in EDX + AOS archives — not in this file alone.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary (admissible)** | G0 currency blotters under champ filters — EDX-P0…P4, pool matrix `blotter/archive/EDX-POOL_WINDOWS/` |
| **OS overlay** | AOS archives `blotter/archive/AOS-*/` · live extract `AOS-aistack-run/` (magic 8399001) |
| **Normative scoring** | `doc/edge_framework.md` |
| **Deploy mix** | `doc/candidate_pool.md` (not a single max-$ winner) |
| **Legacy proxy** | Early multi-level / pips log — historical only; do not use for gates |

**Current champion (operational engine):** Harvest  
`Profiles/Tester/BMRG/EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` — SL300 / TP300 / RR=1.0 / BBDev 2.2 / session **12–20** / **skip Tue** / magic **8210204**.

**AI-enhanced paper stack:** `Profiles/Tester/BMRG/aistack.set` — same engine geometry + AOS L2AI/L3/L4 · magic **8399001** · **STAY_PAPER** (not production).

*(P25 hygiene was run on prior Growth base P4-T01; next hygiene/G5 should use Harvest unless task says otherwise.)*

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid |
| Short code | BMRG |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Optional adaptive grid / basket (multi-level) — **off for pool / gates** |
| Not | Trend-following, breakout, momentum-continuation |
| Market / TF | EURUSD, M5 |
| Execution | Closed-bar signal (shift 1) → market orders |
| Account | Hedging required |
| Geometry for evidence | **G0** MaxLevels=1, MaxEntries=1 |

### Strategy-class statement

BMRG **fades excursions** beyond ±kσ Bollinger bands toward the short-horizon mean. It wins when price **mean-reverts** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
```

It loses when price **band-rides** (trend / regime break) into the hard stop. It is **not** a trend system.

**Side diagnosis (EDX P0–P1, G0 currency):** weakness is **WR-side** (R ≈ RR on fixed TP/SL). Payoff compression was rejected as the primary claim; filters and entry hygiene matter more than “AL too large in points.” P2 still maps **survival / harvest** sleeves via RR geometry for regime blend.

---

## 2. Edge profile

### 2.1 Theoretical edge

**Champion Harvest** designed **RR = 1.0** (TP 300 / SL 300): **BWR = 50%**.  
Soft target after Leak: WR ≳ 52–55%, BM ≥ +2 pp, E_N ≥ +0.05R, ideally **EF > M** (Robust).

Pool also carries Growth at RR=1.5 (BWR 40%) — strongest *long* EF historically, secondary to Harvest for current deploy.

Edge is **regime-conditional**. Champ stack sets `regime_filtered=true` via **session 12:00–20:00** and **TradeTue=false**.

### 2.2 Structural win path

| Layer | Role |
| --- | --- |
| Signal | Fade: long ≤ lower band; short ≥ upper band (closed bar) |
| Exit | Fixed TP at designed RR **or** MID when TP=0 (rare on champion) |
| Risk G0 | Hard SL = **1R** per event |
| Leak control | Session, skip Tue, max spread, cooldown |
| Survival | Equity halt, daily loss %, loss-streak pause |

**Designed Harvest geometry (current champion):**

| Parameter | Value | Intent |
| --- | --- | --- |
| InpBBDev | 2.2 | Entry threshold |
| InpSL_Points / InpTP_Points | **300 / 300** | RR = 1.0 · BWR **50%** |
| InpStartHour–EndHour | **12–20** | Cut thin London morning |
| InpTradeTue | **false** | Cut BM≤0 weekday |
| MaxLevels / MaxEntries | 1 / 1 | Ticket ≈ event |
| InpRiskPercent | 0.5% | Operating f (often min-lot floored on $400) |

### 2.3 Realisation mode

On G0 Growth / Harvest / Survival sleeves, exits are almost entirely **TP/SL** → realisation **`FIXED_RR_FADE`** (mean-rev on entry). Mid-exit sleeve (P2-T05) is experimental and **costs_fragile**.

### 2.4 Class metric targets

| Metric | Soft target | Hard fail |
| --- | --- | --- |
| WR | > BWR after Leak | Persistently ≤ BWR |
| R | ≈ RR on FIXED_RR | R ≪ RR without WR compensation |
| BM / EF | BM>0; EF>0 (prefer EF>M) | EF ≤ 0 |
| E_N | > 0 | ≤ 0 on W250/W500 |

---

## 3. Candidate pool (behavioural map)

Discovery maintains a **pool**, not one champion. Admission: **E_N > 0** and **WR > BWR** (EF > 0 preferred). Detail: `doc/candidate_pool.md`.

| Role | Geometry (champ filters) | Long (currency) | 3M Jul–Sep | Deploy read |
| --- | --- | --- | --- | --- |
| **Harvest · champion** | SL300/TP300 · **8210204** | n=530 WR 54.5% E_N 0.091 EF 1.77 | n=49 EF **6.43** | **Primary** · hit-rate sleeve |
| **Balanced / Growth** | SL300/TP450 · 8210401 | n=420 WR 47.4% E_N 0.185 EF **5.18** Robust* | n=33 EF 0.22 thin | Secondary · best long EF · G0–G4 / G5 fail |
| **Survival** | SL200/TP450 · 8210201 | n=509 WR 34.2% E_N 0.111 EF 0.87 | EF −0.75 costs_fragile | Stress sleeve |
| **Balanced-scale** | SL200/TP300 · 8210202 | n=636 WR 43.4% E_N 0.085 EF 0.09 | EF 0.96 | Scale variant |
| **Mid-exit** | TP=0 · 8210205 | EF −3.1 costs_fragile | EF −2.6 | Watch only |

\*Leak L1 proxy (~2.2 pp). Incomplete current month excluded from admission.

**Dropped:** TP600 (WR&lt;BWR); G5 TP−10 on Growth (EF≤0); session-only 12–20 without skip-Tue (lost to P0).

**Blend:** primary **Harvest**; small-f with **Growth + Survival**; weight by 3M when retuning, size by long.

---

## 4. Trade profile (G0 Harvest champion)

### 4.1 Winners

- Fade into session 12–20 (non-Tue); TP **+1.0R** before SL (equal distance).  
- Higher hit-rate vs Growth (WR ~54–59% vs BWR 50%).  
- Both sides on; sell > buy asymmetry noted on Growth P25 — not re-run on Harvest yet.  
- Hold: minutes–hours on M5; overnight inventory possible.

### 4.2 Losers

- Fade into continuation → SL −1R.  
- Loss-streak pause (3) and daily loss flatten engage.  
- **WR-side class:** edge = WR margin above 50% BWR × R≈1; thicker WR, thinner R than Growth.

### 4.3 Exit mix (Harvest long)

Almost all **TP / SL**; MID ≈ 0 → FIXED_RR_FADE (RR=1).

---

## 5. Rolling / regime notes

| Window | Harvest (P2-T04) read |
| --- | --- |
| Long full | KEEP · EF 1.77 Fragile vs M · n=530 gate-eligible |
| Trailing 3M | Strong · EF **6.43** · WR 59% · primary regime weight |
| Incomplete Sep cell | Do not use for admission |
| vs Growth | Growth wins *long EF*; Harvest wins *recent* + hit-rate |
| Engine W250 path (labels) | Terminal EF ~4.2 Fragile; mid-sample dipped to **EF ≤ 0** (Below stress) |

Lifecycle: treat Near-frontier / Fragile sleeves with lower f; do not deepen grid.

### 5.1 AOS overlay (paper · aistack 8399001 · 2026-09-25)

| Window | Engine-only EF | aistack EF | Notes |
| --- | ---: | ---: | --- |
| Long | 2.33 Fragile | **5.45 Robust** | ΔEF +3.12 · skips ~53 fires · W250 path min +1.8 vs engine −3.8 |
| Jul→Sep | 1.58 Fragile | **4.05 Fragile** | ΔEF +2.47 · ledger skip rate ~32% |
| 2026 YTD | ~6.87 | **7.06 Robust** | Small lift; recent W100 ≈ engine |

AOS L4 end (Jul ledger): **Compressing** · f_rec 0.5 · W250 EF 4.2. L3 MaxDD/Below trips: 0 on that run. Min-lot floors L4 size mod (lots stayed 0.01). **Not production** — see `doc/ai_OS.md` / `doc/aos_p7_promotion.md`.

---

## 6. Performance snapshot (admissible)

| Setting | **Harvest P2-T04 (champion)** | Growth P4-T01 (secondary) |
| --- | --- | --- |
| Mode | Account **currency** · deposit 400 USD | same |
| Window | 2025.01.01 – 2026.09.24 | same |
| Final | **~$533** | ~$621 |
| n / WR / R | **530 / 54.5% / 1.0** | 420 / 47.4% / 1.5 |
| BM / Leak / EF / E_N | ~+4.5 / ~2.2 / **+1.77** / **+0.091R** | +7.4 / ~2.2 / +5.18 / +0.185R |
| 3M EF | **+6.43** | +0.22 thin |
| Gates | Pool KEEP both windows; **G5 not re-run on Harvest** | G0–G4 PASS · G5 FAIL |

---

## 7. Key metrics dictionary

| Symbol | Harvest long (champion) |
| --- | --- |
| RR / R / RR−R | 1.0 / 1.0 / ~0 |
| BWR / WR / BM | 50% / 54.5% / ~+4.5 pp |
| Leak / EF / Zone | ~2.2 pp / 1.77 / Fragile (long) · Robust* on 3M |
| E_N | +0.091R |
| Side diagnosis | **WR-side** (class) |
| regime_filtered | **true** (session 12–20 + skip Tue) |

---

## 8. Behavioural fingerprint

1. Mean-rev **entry**; FIXED_RR **exit** on Harvest/Growth/Survival.  
2. Champ filters are part of the edge claim (not optional cosmetics).  
3. Champion favours **hit-rate** (RR=1) over Growth’s long EF (RR=1.5).  
4. Pool still spans Harvest / Growth / Survival for blend.  
5. Grid off for all pool members until basket events re-validated.  
6. Optional AOS overlay (v1.20+) may **skip / halt / size** — never changes the fade signal.

---

## 9. Recommended use

- Deploy / paper from **Harvest P2-T04** as primary engine; keep Growth in blend.  
- Optional paper OS: run **`aistack`** (8399001) in Strategy Tester — do **not** treat as `AOS_LIVE`.  
- Next G5 / hygiene: hold Harvest payoff (300/300) + champ filters fixed.  
- Do not raise f or MaxLevels until G5 clears on the champion (or chosen KEEP).  
- OS promote path: stronger L1 features → retrain → Robust W250 hold → L10 (`doc/ai_OS.md`).  
- Retune sleeve weights on trailing 3M; do not re-fit a dead incomplete month.

---

## 10. One-line thesis

**BMRG is a session-filtered G0 Bollinger fade; current engine champion is Harvest (300/300, 12–20, skip Tue) for hit-rate and recent EF, with Growth retained secondary. An AI OS wrapper (aistack) can lift long EF in tester but remains STAY_PAPER until G5 clears on the sleeve and L10 signs `AOS_LIVE`.**
