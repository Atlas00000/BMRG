# AUDUSD — System Profile

**Asset:** AUDUSD · **TF:** M15 (research primary) · M5 (live / EDX support)  
**Sleeve:** Research **CHAMP** Harvest · **engine only (AOS OFF)**  
**Magic (research):** **8230901**  
**Preset:** `Profiles/Tester/BMRG/AUDUSD/AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set`  
**Profile date:** 2026-10-19  
**Evidence window (primary):** **2026.05.01 → 2026.08.31** · M15 · every tick · ACCOUNT CURRENCY · deposit **$400**  
**Source:** Tester `logs/20261019.log` · review `blotter/archive/AUDUSD-M15-EXP/`  
**Framework:** `doc/unified_edge_framework.md` (maths) · **binding:** [`edge_framework.md`](./edge_framework.md) · **discovery:** [`edge_discovery.md`](./edge_discovery.md)  
**Docs home:** [`doc/assets/AUDUSD/`](./README.md)

**Scope:** Research **asset-list expansion** + TF probe (M15). **Not** a live replace. Live AUDUSD remains AIOS SCALE mag **8230931** Risk 3% M5 ([`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)). Own AIOS for an M15 sleeve is planned later — **not** required for expansion keep.

**Do not mix** with root `system_profile.md` (EURUSD champion) · DE40 / UK100 / stock asset dirs · live INF magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary (this profile)** | M15 · May→Aug 2026 · magic **8230901** · AOS OFF · n=**41** · final **533.27** |
| **Supporting long** | M15 · Jan→Aug 2026 · same magic · n=**95** · final **549.30** |
| **Supporting M5 EDX** | Champ stack May→Aug · E_N **+0.404R** · WR **70.2%** (`blotter/archive/EDX-P5-T01/`) · mag lineage → **8230901** freeze |
| **Book A baseline** | M5 · mag **8221103** · Start12 · May→Aug WR 62.1% E_N +0.241R — pre-champ geometry |
| **Normative scoring** | `doc/unified_edge_framework.md` · [`edge_framework.md`](./edge_framework.md) |
| **Not admissible here** | DE30 inputs on AUDUSD (log run #6) · tip-only promo · treating soft months as class death · live Risk3 AIOS as this engine fingerprint |

### Cross-window scoreboard (FIXED_RR design R=1.0 · BWR **50%**)

| Window | TF | Final | Δ vs $400 | N | WR | E_N† | W20 min→last | path DD~ | Max L-streak |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| **Tip May→Aug 2026** | **M15** | **533.27** | **+$133.27** | **41** | **63.4%** | **+0.268R** | 50→**75** | **3.0%** | 4 |
| Long Jan→Aug 2026 | M15 | 549.30 | +$149.30 | 95 | 56.8% | +0.137R | 40→75 | 4.4% | 7 |
| EDX champ tip (support) | M5 | — | +$57-class | ~47 | 70.2% | **+0.404R** | — | — | — |
| Book A baseline tip | M5 | 444.39 | +$44.39 | 58 | 62.1% | +0.241R | — | — | 3 |

† E_N from RR=1 identity `E_N = 2·WR − 1` (FIXED_RR journal). Replace with deal-exported AW/AL before Stage-1 production gate. Leak / EF pending deal costs.

**Stage 0 (M15 tip):** n≥30 · WR ≫ BWR · E_N ≫ 0 · MaxDD path contained → **PASS** for expansion keep. Soft months (May, and Feb/Mar on long) = **regime mismatch**, not reject.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid (Harvest CHAMP on AUDUSD) |
| Short code | BMRG · AUDUSD CHAMP |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **AUDUSD** · research **M15** (this profile) · live path **M5** |
| Execution | Closed-bar signal (shift 1) → market orders |
| Geometry | **G0** MaxLevels=1 · MaxEntries=1 (ticket ≈ event) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL exits) |
| Regime posture | **`regime_filtered=true`** (session 13–20 + skip Mon + skip Tue) |

### Strategy-class statement

On AUDUSD the EA **fades excursions** past ±kσ Bollinger bands toward the short-horizon mid-band. Same **mean-reversion** class as EURUSD Harvest / Book A — **not** a trend system.

It should win when AUDUSD **mean-reverts inside the session filter** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.0** → **R ≈ 1.0** → **BWR = 50%**. Soft research targets after costs: WR ≳ **55–60%** on the home tip, BM ≥ **+5–10 pp**, E_N ≥ **+0.10R** (prefer ≥ **+0.20R** on clean May→Aug).

It loses when price **band-rides** (USD impulse, risk-on/off continuation, tip FRAGILE cells) into the hard SL — classic meanrev failure. Soft calendar months and tip dilution are read first as **regime / points mismatch** (EUR-calibrated 300-pt wings on AUD ATR), not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Harvest RR=1)

| Concept | Designed | Implication |
| --- | --- | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, not trend capture |
| Geometry | SL **300** / TP **300** pts | Equal wings; TP = SL always |
| Designed RR / R | **1.0** | Harvest hit-rate sleeve |
| BWR | **50%** | Higher bar than Balanced RR=1.25 (44.4%) |
| Side of edge | **WR-side** | Need WR > 50%; R stays ≈ RR if FIXED_RR |
| vs Growth (RR 1.5) | Lower BWR (40%) but thicker R | **Not** this sleeve |
| vs Balanced (RR 1.25) | Mid BWR | Used on index CFDs (e.g. DE40) — not AUD CHAMP |
| Regime filter | Session **13–20** + **skip Mon** + **skip Tue** | Champ freeze (EDX P3/P5) |
| AOS | **OFF** on research mag | Pure engine; AIOS is a separate sleeve |

**Why RR=1 for this sleeve:** Harvest is the **hit-rate** sleeve. Metric targets prioritize WR margin over large R. Keep RR locked until Leak / RR−R gap says points are mis-scaled to AUD ATR.

**Why Start13 + skip Mon (not Book A Start12):** EDX cells showed hour-12 and Mon as WR drains. Champ filters raise tip E_N (M5 stack +0.404R) without changing class.

**Why M15 in this profile:** Expansion / list TF probe with the same geometry. Cooldown is in **bars**, so M15 fires less often than M5 — frequency drop is structural, not a reject. Live remains M5 AIOS until an M15 sleeve is separately signed.

### 2.2 Structural win path

| Layer | Role on AUDUSD |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed bar · **BBDev 2.2** |
| Entry hygiene | MaxSpread **30** · cooldown **3** bars · session + weekday gates |
| Exit | Fixed TP **+1R** or SL **−1R** (300 pts) |
| Risk G0 | One event · MaxEntries 1 · risk% **0.5** (research) |
| Containment | Loss-streak pause (3) · daily loss % · equity halt |
| ATR regime | **OFF** (P8-T03 SKIP — no n≥30 BM≤0 cell for gate) |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 50% (BWR); prefer ≥ **55–63%** on tip | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.0 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+5–10 pp** on tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.20R** on tip | ≤ 0 on tip and W20 |
| Soft stress month | WR ≳ 45–50% or recoverable via next months | Wipeout month → regime / ATR retune, not auto-cut |
| Leak / EF | Deal export → EF = BM − Leak | Skip Robust EF from journal WR alone |
| MaxDD path | Comfortably under equity halt 15% | Path DD approaching halt on research risk |

### 2.4 Realised edge — M15 May→Aug 2026 (primary)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **41** | Usable Stage-0 |
| WR | **63.4%** | Well above BWR 50% |
| R (design / FIXED_RR) | **≈ 1.0** | On-thesis |
| BWR | **50%** | Designed |
| BM | **+13.4 pp** | Strong gross margin |
| E_N | **+0.268R** | Clears +0.20R soft prefer |
| PnL | **+$133.27** (+33.3%) | Equity confirms direction of E_N |
| W20 | min 50% · last **75%** | Never below BWR on tip sample |
| path DD~ | **3.0%** | Far under 15% halt |
| Max loss streak | **4** | Near containment (3) — watch |

**Leak / EF:** not scored from journal alone. Treat BM/E_N as **gross**; export deals before Stage-1 production gate.

### 2.5 Regime / transfer caveat

Geometry is **EURUSD-calibrated** (300 pts). AUDUSD ATR and tick value differ — soft months (M15 **May** WR 37.5%; long-window **Feb/Mar**) are expected as **regime / points mismatch**, not class failure. Do not cut AUDUSD from the expansion list on tip softness alone.

---

## 3. Trade profile

Evidence: **41** closed events · M15 · May→Aug 2026 · magic **8230901** · TP/SL only.

### 3.1 Winners (n=26 · 63.4%)

- Fade completes to TP **+1R** before SL.  
- **Sell slightly stronger** than buy (sell WR **65.2%** vs buy **61.1%**).  
- Hold much longer than losers (med **23.4h** vs **4.6h**) — meanrev needs time; **~77%** of winners hold ≥12h (overnight inventory common).  
- Best DOW: **Wed** (WR 73.7%, E_N +0.47R); **Fri** solid (66.7%).  
- Best hours: mid/late session (**15**, **18**) — small-n but high WR; session open **13** still above BWR (56.2%).

### 3.2 Losers (n=15 · 36.6%)

- Continuation through the band → SL **−1R**.  
- Fast resolution (med hold **4.6h**) — impulse hits stop sooner than winners mean-revert.  
- Weak pocket: **Thu** (WR **40%**, E_N −0.20R) on this M15 tip — watch, not a preset change yet.  
- Soft month: **May** (WR 37.5%) — regime pocket inside an otherwise strong tip.  
- Max loss streak **4** (one above containment threshold 3); no equity-halt / daily-loss wipe in this window.

### 3.3 Exit mix

| Exit | Count | Share |
| --- | ---: | ---: |
| Take profit | 26 | 63.4% |
| Stop loss | 15 | 36.6% |
| MID / other | 0 | 0% |

→ Realisation stays **`FIXED_RR_FADE`**.

### 3.4 Side balance

| Side | n | WR | E_N |
| --- | ---: | ---: | ---: |
| Buy | 18 | 61.1% | +0.222R |
| Sell | 23 | 65.2% | +0.304R |

Both sides contribute; no one-sided engine.

### 3.5 Weekday (entry) — Mon/Tue filtered

| DOW | n | WR | E_N |
| --- | ---: | ---: | ---: |
| Mon | 0 | — | filtered |
| Tue | 0 | — | filtered |
| Wed | 19 | **73.7%** | **+0.474R** |
| Thu | 10 | 40.0% | −0.200R |
| Fri | 12 | 66.7% | +0.333R |

### 3.6 Entry hour (server, n≥3)

| Hour | n | WR | E_N |
| --- | ---: | ---: | ---: |
| 13 | 16 | 56.2% | +0.125R |
| 14 | 8 | 62.5% | +0.250R |
| 15 | 6 | 83.3% | +0.667R |
| 18 | 3 | 100% | +1.000R |
| 19 | 5 | 60.0% | +0.200R |

### 3.7 Streaks

| | Value |
| --- | ---: |
| Max win streak | 12 |
| Max loss streak | 4 |

---

## 4. Rolling windows

### 4.1 Calendar months — M15 tip (May→Aug)

| Month | n | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| 2026-05 | 8 | **37.5%** | **−0.250R** | Regime pocket |
| 2026-06 | 15 | 66.7% | **+0.333R** | Strong |
| 2026-07 | 10 | 80.0% | **+0.600R** | Strong |
| 2026-08 | 8 | 62.5% | **+0.250R** | Soft-stress pass |

Three of four months E_N > 0; May softness absorbed by Jun–Aug.

### 4.2 Calendar months — M15 long (Jan→Aug)

| Month | n | WR | E_N |
| --- | ---: | ---: | ---: |
| 2026-01 | 11 | 63.6% | +0.273R |
| 2026-02 | 13 | 46.2% | −0.077R |
| 2026-03 | 17 | 41.2% | −0.176R |
| 2026-04 | 13 | 61.5% | +0.231R |
| 2026-05 | 8 | 37.5% | −0.250R |
| 2026-06 | 15 | 66.7% | +0.333R |
| 2026-07 | 10 | 80.0% | +0.600R |
| 2026-08 | 8 | 62.5% | +0.250R |

Off-regime tax concentrated in **Feb/Mar/May**; tip core still carries the sleeve.

### 4.3 Rolling trade windows (expectancy path)

| Window | Tip May→Aug | Long Jan→Aug | Read |
| --- | --- | --- | --- |
| W10 WR min→last | 30→60% | 20→60% | Soft floors exist; recover |
| W20 WR min→last | **50→75%** | 40→75% | Tip never &lt; BWR |
| W30 WR min→last | 63→73% | 40→73% | Tip stable above BWR |
| Path E_N (RR1) | **+0.268R** | +0.137R | Tip preferred for keep |

W250 lifecycle not applicable on research AOS-OFF runs (n≪250).

### 4.4 Frequency

| Metric | M15 tip | M15 long |
| --- | ---: | ---: |
| Span | ~4 months | ~8 months |
| Closed trades | 41 | 95 |
| Trades / 30d | ~10 | ~12 |
| vs M5 Book A (~14–15 / 30d) | Lower (bar cooldown) | Expected |

---

## 5. Performance

| Setting | Value |
| --- | --- |
| Symbol / TF | AUDUSD **M15** |
| Mode | Every tick · ACCOUNT CURRENCY |
| Deposit / leverage | $400 / (tester default) |
| Window (primary) | 2026.05.01 → 2026.08.31 |
| Final balance | **533.27** |
| Net PnL | **+$133.27** (+33.3%) |
| History quality | 100% (tester) |
| AOS | Off (`aos=0`) |
| Containment | No equity halt · no daily-loss flatten observed |

### Cross-window context (expansion lens)

| Window | PnL | N | WR | Read |
| --- | ---: | ---: | ---: | --- |
| May→Aug M15 (this profile) | **+$133** | 41 | 63.4% | **Primary KEEP** |
| Jan→Aug M15 | +$149 | 95 | 56.8% | Keep with off-regime tax |
| M5 EDX champ tip (support) | +$57-class | ~47 | 70.2% | Geometry parent |
| Book A M5 tip (pre-champ) | +$44 | 58 | 62.1% | Baseline |

**Interpretation:** CHAMP geometry on M15 realises a clear WR-side edge on the home tip. Longer mix dilutes via Feb/Mar/May mismatch — do **not** treat that as “cut AUDUSD from expansion.” Live AIOS M5 is a separate attach path.

---

## 6. Key metrics (scorecard snapshot)

| Symbol | M15 May→Aug 2026 (**8230901**) |
| --- | --- |
| RR / R / RR−R | 1.0 / ≈1.0 / ~0 |
| BWR / WR / BM | 50% / **63.4%** / **+13.4 pp** |
| E_N | **+0.268R** |
| n | 41 |
| PF (approx WR@R=1) | WR/(1−WR) ≈ **1.73** |
| W20 last / min | **75%** / 50% |
| path DD~ | **3.0%** |
| Side diagnosis | **WR-side** meanrev (class) |
| regime_filtered | **true** (13–20 + skip Mon + skip Tue) |
| Leak / EF / Zone | Pending deal export |
| Live boundary | **Separate** · mag **8230931** Risk 3% M5 AIOS · see [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) |

---

## 7. Behavioural fingerprint (AUDUSD)

1. Same class as EURUSD Harvest: **mean-rev entry · FIXED_RR exit**.  
2. Hit-rate sleeve works on M15 May→Aug (WR ≫ BWR · E_N +0.27R).  
3. Both sides on; sell slightly ahead of buy.  
4. Inventory often overnight on winners — not a scalp profile; losers die fast.  
5. Weak structural pockets to watch (not yet retuned): **Thu**, tip month **May**, long-window **Feb/Mar**.  
6. Champ filters are part of the claim; Mon/Tue skip active (n=0).  
7. AOS OFF on **8230901** — fingerprint is pure engine; do not score L2/L3 from this blotter.  
8. M15 frequency &lt; M5 by design (cooldown in bars).

---

## 8. Locked geometry (research CHAMP)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.2** |
| InpSL_Points / InpTP_Points | **300 / 300** |
| InpMaxLevels / InpMaxEntries | 1 / 1 |
| Session | **13:00–20:00** server |
| InpTradeMon / InpTradeTue | **false** / **false** |
| InpRiskPercent | 0.5% (research) |
| InpMagic | **8230901** |
| InpAOS_Enable / kill-switch | false / true |
| InpUseATRRegime | **false** |

Live twin (not this fingerprint): mag **8230931** · Risk **3%** · AOS LIVE_WITHHOLD · M5.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep AUDUSD on **expansion queue** (M15 CHAMP tip KEEP) | Treat M15 research as live replace of **8230931** |
| Export deals → Leak / EF / MaxDD Stage-1 | Claim Robust EF from journal WR alone |
| Read May / Feb–Mar softness as **regime mismatch** | Hard-reject the asset on tip regime alone |
| Optional: Thu / May hygiene experiments | Change RR or SL/TP without EDX task |
| Plan own AIOS later on a frozen M15 (or keep M5 live) | Score L2 on research mag **8230901** |
| Compare vs Book A / EDX M5 as geometry parents | Mix magics with EURUSD INF `8210204` |

---

## 10. One-line thesis

**AUDUSD CHAMP is a session-filtered G0 Bollinger mean-reversion fade (Harvest RR=1 · Start13 · skip Mon/Tue); on M15 May→Aug 2026 it realises a WR-side edge (WR 63% · E_N +0.27R · +$133) suitable for asset-list expansion — not a live replace, and soft months should be read as regime/points mismatch until deal-scored EF and any optional ATR/session retune.**
