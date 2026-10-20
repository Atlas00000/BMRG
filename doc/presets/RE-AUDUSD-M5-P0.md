# RE-AUDUSD-M5-P0 — fresh AUDUSD expectancy preset

**Not a Harvest clone.** Engine-only (AOS OFF). Objective: **positive E_N** on AUDUSD M5 G0.

| Field | Value |
| --- | --- |
| Preset | `RE-AUDUSD-M5-P0_posEN_G0.set` |
| Magic | **8222101** |
| Tester | AUDUSD · **M5** · every tick · ACCOUNT CURRENCY |
| Window | **2026.03.23 → 2026.09.21** (~6m to Ouroboros tip) |

---

## Why fresh (vs Book A Harvest transfer)

| Evidence (~180d to 2026-09-21) | Implication |
| --- | --- |
| Profile ranging **54%**, ATR pct **~3** (quiet) | Meanrev-friendly, but shallow fades are noisy |
| H1 ATR p50 **~89 pts** (EUR ~98, GBP ~131) | Harvest SL**300** is oversized for AUD |
| M15 σ p50 ~41 → 2.2σ ~**90 pts** | Entry distance much tighter than EUR Harvest scale |
| Busy hours UTC: **12–15** + Asia **0–1, 6–7**; quiet **19–23** | Don’t use Harvest 12–20 only — include Asia, cut late NY |
| Book A clone Jan–Oct: WR **52.7%** @ RR=1 → BM **+2.7pp** | Thin vs Leak; RR=1 BWR 50% is a hard bar on quiet AUD |

## Geometry (expectancy / survival)

| Input | Value | Rationale |
| --- | ---: | --- |
| BBDev | **2.4** | Deeper fade on quiet AUD |
| SL / TP | **240 / 360** | ~RR **1.5** → BWR **40%**; SL ≈ 2.7× M15 ATR p50 |
| Session | **01:00–17:00** | Asia + London + overlap; skip thin late NY |
| TradeTue | **true** | Don’t import EUR skip-Tue without AUD proof |
| Cooldown | **4** | Fewer clustered re-entries |
| MaxSpread | **40** | AUD friction headroom |
| Equity / daily halt | **12% / 2.5%** | Tighter survival fuses than extract clone |
| AOS | **OFF** | Prove engine E_N first |

Score under unified edge framework: need **E_N > 0** and **EF > 0** after Leak — not max balance. If WR stays near 45%+ at R≈1.5, BM clears costs more easily than RR=1.
