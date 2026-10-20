# LIVE-20261019 — VPS live book inventory

**task_id:** LIVE-20261019  
**kind:** operator-declared VPS attach inventory (not a day P&L scorecard)  
**as_of:** 2026-10-19T21:33:52+01:00  
**source:** chat operator statement — assets currently trading on VPS  
**verdict:** LOGGED — 7-symbol live book accepted as current VPS composition  
**archived_at:** 2026-10-19T21:33:52+01:00  

Inbox was empty (no hosting logs / deals for this pass). Magics below are the **canonical attach targets from asset sign-off / candidate docs** — confirm on VPS Inputs if a chart uses a twin.

---

## Live book (n=7)

| # | Symbol (VPS) | Doc alias | Expected TF | Canonical magic | Expected preset / sleeve | Doc posture |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | **AAPL** | AAPL / Apple | M15 | **26092501** | `BMRG-M15-AAPL-6M-Harvest_RR1.25.set` · Harvest · AOS OFF | Expansion candidate KEEP — not FX replace |
| 2 | **EURUSD** | EURUSD | M5 (prod) *or* M15 OS | **8210204** (M5 INF) / **26121807** (M15 P7) | `INF-LIVE_WITHHOLD_Harvest_long_ddl30` · *or* P7 research OS | M5 = production FT; M15 P7 = research OS only |
| 3 | **AUDUSD** | AUDUSD | M5 SCALE | **8230931** | `AUDUSD-AIOS_SCALE_Risk3_champ_G0.set` · Risk 3% · LIVE_WITHHOLD | Track B live — do not mix with M15 `8231941` stack |
| 4 | **UK100** | UK100 | M15 | **26111307** | P7 `…UK100-6M-P7_research_OS_ARMED.set` · L2det_uk v1b | HITL research OS — not FX replace |
| 5 | **JPN225** | JP225 | M15 | **26151907** | **`JPN225stack.set`** · L2det_jp May∨Jul | HITL research OS — paper/tiny-f posture in sign-off |
| 6 | **USDJPY** | USDJPY | M15 | **26131807** | **`USDJPYstack.set`** · L2det_usdjpy v1c | HITL research OS — not FX replace |
| 7 | **DE30** | DE40 | M15 | **26141907** | **`DE40stack.set`** · L2det_de arm | HITL research OS — broker symbol **DE30** |

---

## Book split (policy reminder)

| Bucket | Symbols | Notes |
| --- | --- | --- |
| **Production live** | EURUSD (M5 INF **8210204**), AUDUSD (M5 SCALE **8230931**) | Signed live capital paths |
| **Research OS / expansion on VPS** | AAPL, UK100, JPN225, USDJPY, DE30 (+ EURUSD M15 only if P7 attached) | HITL-armed sleeves; docs still say not PRODUCTION-WORTHY / not FX-book replace |
| **Not on this list** | GBPxxx, US30, XAU, stocks other than AAPL, AUD M15 stack **8231941** | Out of current VPS book |

---

## Ops notes

- **DE30 ↔ DE40:** same index book; MT5 symbol is **DE30**; docs/presets use DE40 naming (`DE40stack`).
- **JPN225 ↔ JP225:** same Nikkei book; MT5 symbol **JPN225**; magics/docs use JP225.
- No deal blotter scored this pass — inventory only. Drop hosting experts/terminal logs into `blotter/inbox/` for a day scorecard (pattern: `LIVE-20261005`).
- If EURUSD on VPS is M15 P7 (**26121807**), that does **not** retire M5 Harvest **8210204** unless operator explicitly killed the M5 chart.

---

## Verdict

**LOGGED** — VPS live trading set = `{AAPL, EURUSD, AUDUSD, UK100, JPN225, USDJPY, DE30}` as of 2026-10-19.
