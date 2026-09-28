# AOS-aistack-run REVIEW
**Magic filter:** 8399001 · Agent log ~1.2GB + Tester log ~383MB streamed (no full Select-String).

## Runs today (wall ~18:13–18:14)

| Run | Window | Opens | TP/SL | WR | EF | Zone |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | 2026.01→09 | 190 | 112/77 | 59.3% | **7.06** | **Robust** |
| 2 | 2025.01→2026.09 | 480 | 275/202 | 57.7% | **5.45** | **Robust** |
| 3 | 2025.07→2026.09 (ledger) | 294 | 162/126 | 56.3% | **4.05** | Fragile |

## AOS behaviour (ledger = last run #3)

- Decisions: FIRE **294** · SKIP **139** (skip rate **32.1%**) — L2skip_v1 hard gate working
- Terminal L4: life **Compressing** · f_rec **0.5** · W250 EF **4.2** · E_N **0.128**
- L3 halt/derisk trips in ledger: **0**
- Lots stayed **0.01** (min-lot floor eats L4 size mod)

## vs Harvest baseline (long EF 1.77 Fragile)

Long aistack run EF **5.45 Robust** — clear lift; fewer opens than engine 530 due to AI skips.

## Artifacts

- istack_runs_8399001.json
- BMRG_AOS_ledger_8399001.csv
- gent_ONLY_8399001.log (magic-segmented extract)

**Verdict: ACCEPT wiring** — AOS ON, L2AI skips, L4 observer live. Journal had almost no Entry blocked prints (ledger is source of truth for skips).
