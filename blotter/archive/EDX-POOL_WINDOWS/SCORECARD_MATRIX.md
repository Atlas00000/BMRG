# Pool window matrix — Long × 3M

**Scored:** 2026-09-25 12:20–12:24  
**Long:** 2025.01.01 → 2026.09.24 · **3M:** 2026.07.01 → 2026.09.24  
**Artifacts:** `blotter/archive/EDX-POOL_WINDOWS/`

| Sleeve | Magic | Long n | Long WR/BWR | Long E_N | Long EF | Long $ | 3M n | 3M WR/BWR | 3M E_N | 3M EF | 3M $ | Dual-window |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| **Balanced** SL300/TP450 | 8210401 | 420 | 47.4/40 | 0.185 | **5.18** | 621 | 33 | 42.4/40 | 0.061 | 0.22 | 404 | KEEP / KEEP (thin 3M) |
| **Survival** SL200/TP450 | 8210201 | 509 | 34.2/31 | 0.111 | 0.87 | 514 | 43 | 32.6/31 | 0.058 | **−0.75** | 407 | KEEP / costs_fragile |
| **Scale** SL200/TP300 | 8210202 | **636** | 43.4/40 | 0.085 | 0.09 | 514 | 61 | 44.3/40 | 0.107 | 0.96 | 415 | **KEEP both** |
| **Harvest** SL300/TP300 | 8210204 | **530** | 54.5/50 | 0.091 | 1.77 | **533** | 49 | 59.2/50 | 0.184 | **6.43** | **425** | **KEEP both** |
| **Mid** TP=0 | 8210205 | 1042 | 62/62 | 0.005 | **−3.11** | 406 | 133 | 59/58 | 0.01 | **−2.64** | 401 | costs_fragile both |

## Gap-fill outcomes

- **T02 / T04** no longer thin-only — long admission **KEEP** (n≥385).  
- **Harvest** is the strongest *recent* sleeve; **Balanced** remains strongest *long* EF.  
- **Survival** survives long but fails Leak on 3M → use as stress sleeve, cut f when late-cycle WR compresses.  
- **Mid** stays out of deploy mix until EF>0.

## Blend suggestion (small-f)

| Regime read | Lean |
| --- | --- |
| **Default / current** | **Harvest (P2-T04) primary** |
| Need long EF / Robust* history | Growth (P4) secondary |
| Hit-rate collapsing toward 50% | Survival (T01) lower f |
| Avoid | Mid (T05); TP600 (T03 dropped) |
