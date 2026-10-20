# AUDUSD-AOS-P6 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P6 COMPLETE / SIGNED** · HITL challenger pinned · **AUDUSD_stack** armed  
**Docs:** `doc/assets/AUDUSD/aos_p6_harden.md`  
**Artefact:** `P6_HARDEN.json` · `AUDUSD_stack.set`

| Task | Verdict |
| --- | --- |
| HITL (P5-T02) | **PASS** — CHALLENGER = `…145303` SHADOW |
| P6-T01 | PASS — BUY∧Thu ARM_SOFT shadow · spread DISARM |
| P6-T02 | PASS — keep BUY∧May · SkipBuyThu=false |
| P6-T03 | PASS — geometry freeze on engine + AUDUSD_stack |

## Armed preset

```text
Presets/AUDUSD_stack.set
Profiles/Tester/BMRG/AUDUSD/AUDUSD_stack.set
Magic 8231941 · L2det LIVE_WITHHOLD · L3/L4/W50/ledger · L2AI OFF
```

Compile `BMRG.mq5` before Tester. Never load on live **8230931**.

Next: **P7** promotion packet / paper checklist. Measured Leak+swap still OPEN.
