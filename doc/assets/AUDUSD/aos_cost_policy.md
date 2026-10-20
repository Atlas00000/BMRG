# AUDUSD — AIOS cost / Leak policy

**Version:** 0.1.0 · **Task:** AUDUSD-AOS-P0-T03  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`edge_framework.md`](./edge_framework.md)

---

## Defaults (until deal-measured)

| Item | Value | Source |
| --- | --- | --- |
| Designed R | **1.0** | CHAMP RR=1 |
| BWR | **50%** | 1/(1+R) |
| Leak prior (entry-spread) | **2.4 pp** | EDX-P8 · `InpAOS_Leak=2.4` on live/FT presets |
| Leak_source | `prior_entry_spread` | Upgrade to `measured` after deal export |
| Commission / swap / slip | **unknown** | Must not claim Robust EF until filled |

**Identity:** `EF = BM − Leak` · `M` from unified framework once Leak filled.

---

## Rules

1. Journal WR / E_N alone → **gross** only; label `costs_fragile` until deals.  
2. OS ACCEPT may use E_N hold vs baseline when Leak pending; EF bar applies once `Leak_source=measured`.  
3. Overnight inventory is common (winners med ~23h) — swap belongs in measured Leak when available (L8-aware).  
4. Do not invent a tighter Leak to “pass” a layer.

---

## Journal proxy (P1 · tip May→Aug)

From `blotter/archive/AUDUSD-AOS-P1/COST_PROXY.json` (entry spread only):

| Item | Value |
| --- | ---: |
| spread median | **15** pts |
| c_R proxy (2×med/300) | 0.10 |
| Leak_proxy | **5.0 pp** |
| BM / EF_proxy | +13.4 / **+8.4 pp** |
| Leak_source | `journal_2x_entry_spread_median` |

Prior 2.4 pp remains the AOS input default; journal proxy is **wider** (use for OS caution until deals).

## Open work

| Item | Status |
| --- | --- |
| Export tip deals → measured c_R / Leak | **OPEN** |
| Swap-inclusive Leak on overnight winners | **OPEN** |
| Cost ×1.5 stress (G5-ish) | After measured Leak |

---

## Versioning

- **0.1.0** — Prior from P8 Leak 2.44≈2.4 pp (2026-10-19).
- **0.1.1** — P1 journal Leak_proxy 5.0 pp on tip tape (2026-10-19).
