# BMRG M5 AAPL ~6M — Chart Preset (Balanced Geometry + ATR Regime)

**Status:** RESEARCH CHART PRESET / UNTESTED  
**Not:** production sign-off · claimed live edge · AOS_LIVE  
**Primary preset:** `BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`  
**Tester dir:** `MQL5/Profiles/Tester/BMRG/AAPL/`  
**Framework:** `docs/framework/unified_edge_framework.md` · Stage 0–1  
**Ouroboros audit:** `research/assets/AAPL/bmrg_m5_6m_audit.json`  
**Script:** `server/scripts/bmrg_aapl_m5_6m_audit.py`

| Field | Value |
| --- | --- |
| EA | BMRG (Bollinger Mean-Reversion Grid) v1.21 |
| Class | Mean reversion fade (FIXED_RR) · **regime-filtered** |
| Symbol | AAPL (MT5 `Apple` · Point = 0.01) |
| Chart TF | **M5** |
| Window | **2026.05.01 → 2026.10.07** (~6 months) |
| Aggregation | G0 (`MaxLevels=1`, `MaxEntries=1`) |
| Magic | **26102011** |

---

## 1. Last-6m asset context

H1 `regimes.rule_v1` → `fit.map_v0` **meanrev** (BMRG home):

| Month | Tag | MATCH% | FRAGILE% |
| --- | --- | ---: | ---: |
| 2026-05 | **MISMATCH** | 45.7 | 0.0 |
| 2026-06 | MATCH | 51.7 | **44.2** |
| 2026-07 | MATCH | 46.1 | 10.4 |
| 2026-08 | MATCH | 46.3 | 25.9 |
| 2026-09 | MATCH | 49.7 | 28.6 |
| 2026-10 | MATCH | 76.7 | 0.0 |

**Read:** Jun–Oct on-home for meanrev. May off-home; Jun FRAGILE share high → **ATR max gate ON**.  
Overall tip meanrev **MATCH**.

**M5 ATR (points, Point=0.01):** p50 ≈ **63** · p75 ≈ **80** · p90 ≈ **98**.  
Do **not** import M15 SL 320 (~5× M5 ATR).

---

## 2. Unified Edge Framework geometry

```text
never TP < SL          →  InpTP_Points (280) > InpSL_Points (190)
RR_design = TP / SL    →  280 / 190 ≈ 1.47
BWR = 1 / (1 + R)      →  ≈40.4% if R ≈ RR
E_N = WR × (R + 1) − 1
BM  = WR − BWR
Leak = c_R / (R + 1)   · c_R ≈ 40 / SL  (cost prior)
EF  = BM − Leak
```

| Piece | Choice | Intent |
| --- | --- | --- |
| SL | **190** pts | ~3.0× M5 ATR p50 — structural 1R |
| TP | **280** pts | **TP > SL** · designed RR **≈1.47** (WR + returns mix) |
| BB | 20 / **2.5σ** | Clears Stage-1; bb2.2 weaker EF |
| Session | **14:00–20:00** | US cash RTH approx |
| Skip Tue | **true** | Weekday cut |
| ATR regime | **ON · 24–98** | ≈ p25×0.5 → p90 — cut HV / off-home stretch |
| BB-width | ON · 0.30–2.00% | Light sleeve |
| Cooldown | **6** bars | ≈30m on M5 |
| MaxSpread | **40** | Cost prior **40 pts** RT |
| Grid | depth **1** | Clean G0 events |
| AOS | **OFF** | Chart sleeve = engine only |

**Why not Harvest RR=1.0 as primary?** Harvest 220/220 has high WR but EF≈0 under cost prior — no Stage-1 margin. Primary keeps mix WR + returns with EF+.  
**Why ATR gate ON?** May MISMATCH + Jun FRAGILE; gated sleeve remains Stage-1 viable (n=100).

---

## 3. M5* probe scorecard (design prior — not Tester blotter)

Closed-bar BB fade → next open · fixed TP/SL · session 14–20 · skip Tue · cost prior **40 pts** RT.

| Sleeve | n | WR | RR | EF | E_N | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **P0 190/280 bb2.5 + ATR≤98 (chosen)** | 100 | 51.0% | 1.47 | **+2.1pp** | **+0.26R** | Stage-1 viable · regime-filtered |
| Balanced 220/280 bb2.5 + ATR/BBW | 90 | 53.3% | 1.27 | +1.3pp | +0.21R | Viable alt (higher WR) |
| Ungated 190/280 bb2.5 | 110 | 50.9% | 1.47 | +2.0pp | +0.26R | Viable but no HV cut |
| Harvest 220/220 bb2.5 | 110 | 59.1% | 1.00 | ~0 | +0.18R | WR-only · weak EF |

---

## 4. Load checklist

1. Tester: **Apple · M5** · every tick · deposit ≥ 400  
2. Load `BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`  
3. Confirm `SL=190`, `TP=280`, `BBDev=2.5`, `ATR 24–98`, magic `26102011`, AOS OFF  
4. Window: **2026.05.01 → tip**  
5. Score trade events: WR > BWR · E_N > 0 · no TP < SL
