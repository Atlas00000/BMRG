# INF wiring eligibility — LIVE_WITHHOLD shipped

**Automated prove (P6):** metrics ACCEPT · skip-audit FAIL (edge FPs)  
**Operator:** accepted metrics → GO for design/retrain  
**EA hook auth (2026-09-28):** **EA_LIVE_AI_GATE_SHIP** authorised — BMRG **v1.21**

## What ships

| Item | Value |
| --- | --- |
| EA | `Experts/BMRG/BMRG.mq5` v1.21 |
| Mode input | `InpAiOsMode=LIVE_WITHHOLD` (2) |
| Model | baked `AOS_L2skip_inf.mqh` = `L2skip_inf_p92_20260927_223519` |
| Behaviour | L3 halt outranks; L2 WOULD_SKIP blocks new entry only; SL/TP/size unchanged |
| Kill-switch | `InpAiKillSwitch=true` → L2 OFF |
| Preset | `Profiles/Tester/BMRG/INF-LIVE_WITHHOLD_Harvest_long.set` |

## Still forbidden without extra auth

- **AOS_LIVE FT** as production sign-off / demo FT programme (separate from enabling the hook)

## Parity

`infra/artefacts/reports/INF_EA_LIVE_WITHHOLD_parity.json` — sklearn vs MQL formula max|Δ| ~0
