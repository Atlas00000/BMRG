# BMRG · XAUUSD · M5 · ~6m balanced chart preset

**Status:** RESEARCH / UNTESTED design prior — not a live edge claim  
**Framework:** `docs/framework/unified_edge_framework.md` Stage 0–1  
**Hard rule:** never **TP < SL** (RR ≥ 1.0)

| Field | Value |
| --- | --- |
| Preset | `BMRG-M5-XAUUSD-6M-P0_balanced_chart.set` |
| Also under | `Experts/BMRG/Presets/` |
| Magic | **26101950** |
| TF | **M5** |
| Window | 2026.05.01 → 2026.10.07 tip |
| Geometry | SL **680** / TP **850** · **RR 1.25** |
| BWR (design) | **44.4%** |
| Selectivity | BBDev **2.2** · CD **3** · fade **OFF** |
| Regime | ATR max **575** (≈ M5 ATR p75) · session **12–20** · **Tue off** |
| Grid | G0 MaxLevels=1 · AOS OFF |

## Probe scorecard (M5* closed-bar FIXED_RR)

| Metric | Value |
| --- | ---: |
| n | ≈218 |
| WR | ≈45.9% |
| R ≈ RR | 1.25 |
| BWR | 44.4% |
| BM | +1.4pp |
| E_N | **+0.032R** |
| Leak prior (40pt/680) | ≈2.6pp |
| EF prior | ≈−1.2pp (re-score from blotter) |

Stage-0 clear: **WR > BWR**, **E_N > 0**, **RR ≥ 1**. EF soft under cost *prior* only — measure Leak on Tester blotter before Stage-1 claim.

## Regime context (H1 meanrev)

| Month | Tag |
| --- | --- |
| 2026-05 | MATCH |
| 2026-06 | FRAGILE (high-vol) |
| 2026-07 | MISMATCH |
| 2026-08 / 09 / 10 | MATCH |

ATR≤575 reduces trading in high-vol FRAGILE without starving (n≈218).

## Tester load

1. Symbol **XAUUSD** · period **M5**  
2. Load `BMRG-M5-XAUUSD-6M-P0_balanced_chart.set`  
3. Confirm: magic **26101950** · fade=0 · SL **680** · TP **850** · ATR max **575**  
4. Dates **2026.05.01 → tip** · deposit ≥ **1000** · every tick  

Accept: blotter WR > BWR (+ Leak) · E_N > 0 · realized R not crushed vs RR 1.25.

Machine audit: `research/assets/XAUUSD/bmrg_m5_6m_audit.json`  
Script: `server/scripts/bmrg_xauusd_m5_6m_audit.py`
