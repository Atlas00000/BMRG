# EDX-P05-T01 — Integrity audit PASS

**Scored:** 2026-10-07  
**Preset:** `EDX-P05-T01_integrity_G0_AUDUSD-M5_MayAug.set` · magic **8230151**  
**Window:** 2026.05.01 → 2026.08.31  
**Source:** Tester log (no deal CSV in inbox)

## Checks

| Check | Result |
| --- | --- |
| Magic / SL/TP | **8230151** · **300/300** |
| G0 MaxLevels / MaxEntries | **1 / 1** |
| Concurrent tickets | **max = 1** (no ticket-WR inflation) |
| Measured SL pts | **300 only** (n=58) |
| Measured TP pts | **300 only** |
| Lots | 0.01 only |
| Opens / TP / SL / final | 59 / 36 / 22 / **444.39** (matches P0-T01) |
| 1R definition | hard SL distance = event 1R |

**Verdict:** **PASS** — blotter admissible for Stages 0–1 under AUDUSD edge framework.
