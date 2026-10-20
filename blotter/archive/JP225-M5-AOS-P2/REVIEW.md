# JP225-M5-AOS-P2 — Review

**Dated:** 2026-10-20  
**Verdict:** **ACCEPT** — L2det **v1c ARM_SOFT** · L2 AI **DISARM** · proceed P3

## Preferred stack

```text
SKIP if (BUY ∧ MATCH Aug/Sep)  OR  (BUY ∧ hour ∈ {9,13,16})
```

| | Baseline tip | After v1c |
| --- | ---: | ---: |
| n | 94 | **69** |
| E_N | +0.245R | **+0.478R** |
| EF_prior | +4.9 pp | **+12.6 pp** |
| ΔE_N / ret / prec | — | **+0.234** / 73.4% / 80% |
| Jul / SELL / H08 / H10 FP | — | 1 / 0 / 0 / 0 |

## Rejected

Blanket MATCH (SELL FP) · Mon · all-side hours · BUY · FRAGILE · MISMATCH · near_atr · M15 May∨Jul

## Wire

- `Include/AOS_L2det_jp_m5.mqh` · Config `InpAOS_JP_M5_*` (enable **false**)
- M15 `InpAOS_JP_L2detEnable` gated `Period()!=M5`

## L2 AI

AUC tip ≈0.49 · **DISARM** · pin `L2skip_jp225_m5` shadow only

## Next

**JP225-M5-AOS-P3** — L3 halt / L4 health bus on tip + v1c path.
