# aistack — AI-enhanced AOS preset (EA-wired)

**EA version:** BMRG **1.20** (AOS overlay)  
**Preset:** `Profiles/Tester/BMRG/aistack.set` · magic **8399001**  
**Compile:** 0 errors (MetaEditor)

---

## Wired layers (live in tester)

| Layer | Behaviour |
| --- | --- |
| L2det | Engine `InpTradeTue=false` (unchanged) |
| L2 AI | `L2skip_v1` logistic in `Include/AOS_L2skip_v1.mqh` — hard skip when `InpAOS_L2AI_Enable=true` |
| L3 | Halt on MaxDD≥25% from peak **or** W250 E_N≤0; derisk ×0.5 at 0.8×DD |
| L4 | Lifecycle → `f_rec` lot multiplier |
| L6 | Ledger CSV → `COMMON\Files\BMRG_AOS_ledger_8399001.csv` |

L8/L9 remain spec-only (not in EA).

---

## aistack.set AOS inputs

```
InpAOS_Enable=true
InpAOS_L3_Enable=true
InpAOS_L4_SizeMod=true
InpAOS_L2AI_Enable=true      // hard AI skip for stack test
InpAOS_L2AI_Shadow=true
InpAOS_DD_Limit=25
InpAOS_W250=250
InpAOS_Ledger=true
```

Safer paper mode: set `InpAOS_L2AI_Enable=false` (shadow log only).

---

## How to test

1. Confirm `Experts\BMRG\BMRG.ex5` rebuilt (v1.20).  
2. Strategy Tester → load **`aistack`**.  
3. EURUSD M5 · every tick · **account currency** · 2025.01.01 → 2026.09.24.  
4. Watch Experts log for `AOS ON`, `AOS SHADOW skip` / `Entry blocked: AOS L2skip_v1`, `AOS L3 HALT_*`.  
5. After run: ledger under Terminal `COMMON\Files\`, drop blotter in `blotter/inbox/` for score.

Offline CF expectation (labels): n~317 EF~4.9 Fragile — live tester will differ (path-dependent L3/L4).

---

## Source

| File | Role |
| --- | --- |
| `Include/AOS.mqh` | Runtime overlay |
| `Include/AOS_L2skip_v1.mqh` | Model coeffs |
| `Include/Config.mqh` | AOS inputs |
| `BMRG.mq5` | Gate before `ExecutionOpen` |
