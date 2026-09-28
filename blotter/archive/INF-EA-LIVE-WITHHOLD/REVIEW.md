# INF-EA-LIVE-WITHHOLD REVIEW

**Shipped:** 2026-09-28
**EA:** BMRG.mq5 v1.21
**Model:** L2skip_inf_p92_20260927_223519 (baked AOS_L2skip_inf.mqh)
**Parity:** sklearn vs MQL max|delta| ~ 0 (ACCEPT)
**Preset:** Profiles/Tester/BMRG/INF-LIVE_WITHHOLD_Harvest_long.set

## Operator steps
1. Compile BMRG.mq5 in MetaEditor (F7)
2. Attach with InpAOS_Enable=true, InpAiOsMode=LIVE_WITHHOLD
3. Kill-switch: InpAiKillSwitch=true to disable L2 instantly
4. After retrain: python infra/src/train/export_l2_mqh.py then recompile
