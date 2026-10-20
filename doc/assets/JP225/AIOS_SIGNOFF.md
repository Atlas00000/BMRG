# JP225 — AIOS HITL sign-off

**Status:** **ARMED — RESEARCH OS**  
**Signed:** 2026-10-19 (operator HITL in chat — proceed with P7 + JPN225stack)  
**Research OS magic:** **26151907**  
**Engine baseline:** Growth P1 · **26101904** · AOS OFF (compare / rollback)  
**Preset:** **`JPN225stack.set`** (= `BMRG-M15-JP225-6M-P7_research_OS_ARMED.set`)  
**Packet:** [`promotion_packet.json`](./promotion_packet.json) · `JP225_M15_AOS_RESEARCH_v1`

---

## Checklist (P7)

- [x] Tip EF > 0 after **measured** Leak (2.45 pp → tip EF **+0.59 pp**)
- [x] L2det ARM map May∨Jul in `aos_l2_policy.md` · protect Jun/Aug reported
- [x] L3/L4 policy · L6 ledger offline complete (P3/P4)
- [x] Shadow CF holds iteration bar vs baseline (May∨Jul lifts tip)
- [x] HITL named + date (this file)
- [x] Explicit **not** live replace of FX / UK100 / DE40 books

---

## Armed stack

```text
Engine Growth P1 (fade · BB 2.3 · ATR 19670 · 08–17 · skip Tue)
+ L2det_jp225_v1_May_OR_Jul LIVE_WITHHOLD  (AOS_L2det_jp.mqh)
+ L3 DD25% / BELOW halt · L4 W50 size · L6 ledger
+ L2 AI DISARM · L9 London/H08/H14 SHADOW only
```

**Compile** `BMRG.mq5` (needs `AOS_L2det_jp.mqh`) before Strategy Tester.

---

## Paper / tiny-f attach (P7-T03)

1. Tester: symbol **JPN225** M15 · load **`JPN225stack`** · tip May→Aug first.  
2. Confirm ledger `COMMON\Files\BMRG_AOS_ledger_26151907.csv` writes L2DET skips on May/Jul.  
3. Tiny-f / paper only if Tester path matches offline CF (EF hold · no Wed LIVE).  
4. Rollback: `InpAOS_JP_L2detEnable=false` or `InpAOS_Enable=false` → P1 chart set · or `InpAiKillSwitch=true`.

**Not:** live capital · FX/EU book replace · PRODUCTION-WORTHY admit.
