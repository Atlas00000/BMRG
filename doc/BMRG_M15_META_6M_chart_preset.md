# BMRG M15 META ~6M tip — Chart Preset (Growth Geometry + ATR/BBW Regime)

**Status:** RESEARCH CHART PRESET / UNTESTED  
**Not:** production sign-off · claimed live edge · AOS_LIVE  
**Preset:** `Presets/BMRG-M15-META-6M-P0_growth_chart.set`  
**Tester dir:** `Profiles/Tester/BMRG/META/` (own symbol folder · `.set` + README)  
**Framework:** Ouroboros `docs/framework/unified_edge_framework.md` · BMRG system profile  
**Ouroboros audit:** `Ouroboros/research/assets/META/bmrg_m15_6m_audit.json`

| Field | Value |
| --- | --- |
| EA | BMRG (Bollinger Mean-Reversion Grid) v1.21 |
| Class | Mean reversion fade (FIXED_RR) · **regime-filtered** |
| Symbol | META / MT5 `Meta` (equity · Point = 0.01) |
| Chart TF | **M15** |
| Window | **2026.07.06 → 2026.10.09** (available tip; full 6m not on feed) |
| Aggregation | G0 basket events (`MaxLevels=1`, `MaxEntries=1`) |
| Magic | **26101215** |

---

## 1. Last-~6m asset context (Ouroboros)

`regimes.rule_v1` → `fit.map_v0` **meanrev** on H1 (home cell for BMRG):

| Month | Tag | MATCH% | MISMATCH% | FRAGILE% |
| --- | --- | ---: | ---: | ---: |
| 2026-08 | MATCH | 58.9 | 30.6 | 10.5 |
| 2026-09 | MISMATCH | 34.0 | 46.9 | 19.0 |
| 2026-10 | MATCH | 57.1 | 42.9 | 0.0 |

**Read:** Aug / Oct on-home for meanrev. **Sep MISMATCH** (trending_up breakout month, +29.8% D1 path) is off-home — ATR + BB-width gates reduce trading in stretched / HV cells. Incomplete Jul warmup / Oct tip are not admission evidence.

**M15 ATR (points, Point=0.01):** p50 ≈ 335 · p75 ≈ 438 · p90 ≈ 535 · mean ≈ 365.

---

## 2. Unified Edge Framework geometry (design)

Hard rules from framework + factory:

```text
never TP < SL          →  InpTP_Points ≥ InpSL_Points
RR_design = TP / SL    →  1500 / 1000 = 1.50
BWR = 1 / (1 + R)      →  40.00% if R ≈ RR
E_N = WR × (R + 1) − 1
BM  = WR − BWR
Leak = c_R / (R + 1)
EF  = BM − Leak
```

| Piece | Choice | Intent |
| --- | --- | --- |
| SL | **1000** pts | Structural 1R on Meta M15 (~3.0× ATR p50) — not token |
| TP | **1500** pts | **TP > SL** · designed RR **1.50** |
| BB | 20 / **2.2σ** | Signal threshold |
| Session | **14:30–20:00** UTC approx | US cash RTH (verify broker TZ) |
| Skip Tue | **true** | Weekday cut (champ pattern) |
| ATR regime | **ON · 162–438** | ≈ 0.6×p25 … p75 — cut dead + HV FRAGILE |
| BB-width | **ON · 0.40–1.80%** | Required for positive EF on this tip |
| Grid | depth **1** | Clean G0 events |
| AOS | **OFF** | Chart sleeve = engine only |

**Why not ATR-only / unfiltered?** Probe EF negative (WR slips under BWR).  
**Why not Balanced RR=1.25 SL840?** Higher WR (~54%) but n≈11 on tip — underpowered; keep as future P1 if depth grows.  
**Why growth RR=1.50?** Only n≥20 sleeve with E_N&gt;0, EF&gt;0, WR&gt;BWR, TP&gt;SL on available tip — mix WR + returns target.

---

## 3. M15* probe scorecard (design evidence — not Tester blotter)

Closed-bar fade → next open · fixed TP/SL · US RTH · skip Tue · ~tip M1→M15* · cost prior 60 pts RT.

| Sleeve | n | WR | RR | BWR | BM | Leak† | EF | E_N | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **Growth 1000/1500 + ATR/BBW (chosen)** | 22 | 45.5% | 1.50 | 40.0% | +5.5pp | ~2.4pp | **+3.1pp** | **+0.14R** | design-viable |
| Growth 1000/1500 ATR≤p75 only | 41 | 39.0% | 1.50 | 40.0% | −1.0pp | ~2.4pp | −3.4pp | −0.02R | restricted |
| Growth 1000/1500 unfiltered | 53 | 39.6% | 1.50 | 40.0% | −0.4pp | ~2.4pp | −2.8pp | −0.01R | restricted |
| Balanced 840/1050 + ATR/BBW BB2.5 | 11 | 54.5% | 1.25 | 44.4% | +10.1pp | ~3.2pp | +6.9pp | +0.23R | thin-n alt |

† `c_R` prior ≈ 60 pts round-trip / SL pts (framework Stage 1 — replace with blotter).

---

## 4. Design-not-restricted checklist

| # | Rule | This preset |
| ---: | --- | --- |
| 1 | Never TP &lt; SL | **TP 1500 > SL 1000** |
| 2 | Designed RR ≥ 1.0 | **1.50** |
| 3 | WR can clear BWR after Leak prior | Probe WR 45.5% > BWR 40%; EF &gt; 0 |
| 4 | Not WR-theatre (token SL) | SL 1000 structural vs Meta M15 ATR |
| 5 | Not lottery RR | RR 1.50, not ≥3 |
| 6 | G0 single-leg events | MaxLevels=1 / MaxEntries=1 |
| 7 | Filters protect edge, not starve fires | ATR+BBW; n≈22 on tip |
| 8 | Regime filter declared | ATR band + BB-width · meanrev home |
| 9 | AOS not required for geometry claim | AOS OFF |
| 10 | Incomplete tip not used for admission | Jul/Oct noted only |

---

## 5. Load path

### Chart

1. Open **Meta M15** chart.  
2. Attach `Experts\BMRG\BMRG.ex5`.  
3. Inputs → **Load** →  
   `Experts\BMRG\Presets\BMRG-M15-META-6M-P0_growth_chart.set`  
4. Confirm: `SL=1000` · `TP=1500` · `BBDev=2.2` · time **14:30–20** · **Tue off** · **ATR 162–438** · **BBW 0.40–1.80** · magic **26101215** · AOS off.  
5. Optional visual: Bollinger(20, 2.2) on chart (EA uses its own handles).

### Tester

Load from **`Profiles/Tester/BMRG/META/BMRG-M15-META-6M-P0_growth_chart.set`**.  
Dates **2026.07.06 – 2026.10.09**. Model: every tick / real ticks if available. Deposit ≥ 1000. Symbol **Meta**.

---

## 6. Post-run fill (framework Stage 0–1)

After a logged run, score **basket events** (not ticket spam):

| Metric | Fill |
| --- | --- |
| n | |
| WR | |
| R = AW/AL | |
| BWR = 1/(1+R) | |
| BM = WR−BWR | |
| mean c_R / Leak | |
| EF = BM−Leak | |
| E_N = WR×(R+1)−1 | |
| MaxDD | |
| BM by ATR tercile / ER cell | |

**Accept to iterate:** `E_N>0`, `WR>BWR`, `EF>0` preferred, `RR−R` not crushed, fires not starved.  
**Reject geometry:** TP&lt;SL theatre, or WR≪BWR with OK R and no cost excuse, or EF≤0 after measured Leak.

---

## 7. Explicit non-claims

- Probe is a **design prior**, not a Strategy Tester blotter / G0–G5 gate.  
- Full calendar 6m not available on YWO Meta — tip only.  
- Do not raise `f` / MaxLevels until a scored blotter clears Stage 1.  
- `regime_filtered=true` for Gate G3 scoring — do not claim cross-regime robustness without re-open ATR/BBW tests.
