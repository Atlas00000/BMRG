# UK100 — L3v1c BELOW retune · live magic CF

**Goal:** Stop one-tick / EN-only false BELOW halts on live stack **26121907**, then re-confirm tip expectancy.  
**EA:** BMRG **≥ 1.26** (recompile required — 1.25 CF failed streak-latch)  
**Preset:** `Presets/UK100_5m_stack.set`  
**Contrast:** P0 AOS-OFF `BMRG-M5-UK100-6M-P0_balanced_chart.set` (26101905) · archive `UK100-NOHALT-P0` · failed CF `UK100-L3v1c-CF`

---

## 1. What was wrong

Signed M5 policy: **BELOW = W20 E_N ≤ 0 AND W15 EF ≤ 0**.

Live `AOS.mqh` (≤1.24) used **primary W50 E_N ≤ 0 alone** → immediate `HALT_f0_BELOW_FRONTIER`. Soft patches (Aug/Sep) looked like permanent dark while P0 AOS-OFF still printed (**153** tip trades / **+22.5R** vs live **121** / **+20.8R**).

## 2. L3v1c retune (wired)

| Input | Value | Effect |
| --- | --- | --- |
| `InpAOS_L3_BelowDualWindow` | **true** | Halt only if W20 EN≤0 **and** W15 EF≤0 |
| `InpAOS_L3_BelowConfirmN` | **2** | Need 2 consecutive BELOW **closes** |
| `InpAOS_L3_BelowSoftDerisk` | **true** | While confirming: f≤0.25 derisk, not f=0 |
| `InpAOS_L3_BelowHaltMaxBars` | **500** | After hard BELOW, probe unlatch (~2 M5 sessions) |
| MaxDD / 0.8 DD derisk | unchanged | Still hard halt at 25% |

EN≤0 on W50 alone (without dual BELOW) → **NEAR** (f=0.25), not hard halt.

**1.25 CF lesson:** streak must not increment every bar while halted (frozen ring → permanent dark). **1.26** counts closes only + MaxBars probe.

Defaults in `Config.mqh` match this (all L3 books inherit unless overridden).

## 3. Tester CF — magic **26121907**

| Setting | Value |
| --- | --- |
| Expert | `Experts\BMRG\BMRG.ex5` **(recompile 1.26 first)** |
| Symbol | **UK100** |
| Period | **M5** |
| Model | Every tick |
| Dates | **2026.05.01 → 2026.10.20** (tip) |
| Magic | **26121907** |
| Preset | `Presets/UK100_5m_stack.set` |

Optional second pass (same preset): **2026.01.01 → 2026.10.20** for extended path.

### Pass checklist

| # | Window | Done |
| --- | --- | --- |
| A | Tip May–Oct · 26121907 · L3v1c stack | ☐ |
| B | (optional) Jan–Oct · same | ☐ |

After run: drop log / say **score UK L3v1c**.

### Pass gates (vs prior)

| Gate | Target |
| --- | --- |
| n | ≥ live tip **121** (closer to P0 **153** is good) |
| sum_R | ≥ live tip **+20.8** (aim toward P0 **+22.5**) |
| month_hit | ≥ **60%** |
| L3 hard BELOW | fewer / shorter than pre-retune (ledger `HALT_f0_BELOW` vs `DERISK_BELOW_CONFIRM`) |
| maxDD_R | not worse than P0 tip **−8** by much; prefer ≤ live **−5.8** if possible |

**Not** a VPS promote until CF scored. MaxDD L3 stays armed.

---

## 4. Rollback

Set in `.set` (or inputs):

```text
InpAOS_L3_BelowDualWindow=false
InpAOS_L3_BelowConfirmN=1
InpAOS_L3_BelowSoftDerisk=false
```

Restores ≤1.24 EN-only immediate halt behaviour without downgrading EA.
