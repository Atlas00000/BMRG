# DE40-M5-AOS-P2 — REVIEW

**Task:** DE40-M5-AOS-P2 (T01–T07)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — L2det **v1b ARM_SOFT** · L2 AI **DISARM** · next **P3 L3/L4**  
**Scope:** Expansion research · not live · not M15 pin

---

## Preferred stack — v1b

```text
SKIP if (BUY ∧ hour ∈ {14,16}) OR (BUY ∧ October)
```

| | Tip baseline | After v1b |
| --- | ---: | ---: |
| n | 123 | **110** |
| E_N | +0.207R | **+0.289R** |
| EF_prior | +2.21 pp | **+5.83 pp** |
| ΔE_N | — | **+0.081R** |
| Retention / prec | — | **89.4%** / **76.9%** |
| Aug / SELL FP | — | **1 / 0** |

Parity Tue/ATR: **PASS**. Blanket near_atr / BUY∧near_atr: **REJECT/DISARM** (tip near_atr star). L2AI AUC≈0.51: **DISARM**.

---

## Wire

- `Include/AOS_L2det_de_m5.mqh`
- Config `InpAOS_DE_M5_*` (default enable **false**)
- AOS.mqh: M5 path before M15 DE map; M15 gated `Period()!=M5`

Policy: `doc/assets/DE40/aos_l2_policy_M5.md` · CF: `P2_CF.json`

---

## Next

P3 — L3 MaxDD / L4 W15/W20 health bus on tip with v1b shadow.
