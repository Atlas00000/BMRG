# DE40-M5-AOS-P0 — REVIEW

**Task:** DE40-M5-AOS-P0 (T01–T03)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — engine baseline + bad-cells + cost stub frozen · next **P1-T00** tip May→Oct Tester  
**Scope:** Expansion research OS plan only · not live replace · not M15 DE40stack transplant

---

## Deliverables

| Task | Artifact | Status |
| --- | --- | --- |
| P0-T01 | `doc/assets/DE40/DE40_M5_AOS_BASELINE_v1.md` | DONE |
| P0-T02 | `doc/assets/DE40/aos_bad_cells_M5.md` | DONE |
| P0-T03 | `doc/assets/DE40/aos_cost_policy_M5.md` | DONE |
| Plan | `doc/assets/DE40/aios_roadmap_M5.md` v0.1.0 | DONE |

Evidence base: `blotter/archive/DE40-M5-P0/` · [`system_profile_M5.md`](../../../doc/assets/DE40/system_profile_M5.md).

---

## Frozen compare (May→Aug tip-core · Leak prior 7.0 pp)

| Metric | Value |
| --- | ---: |
| Magic | **26101903** |
| n / WR / E_N | **93** / **57.0%** / **+0.282R** |
| EF_prior | **+5.5 pp** |
| MATCH Jun→Aug E_N | **+0.350R** |
| Jan→Aug final | **850.64** (+$350.64) |

Tip May→Oct / Sep–Oct / measured Leak / MaxDD path: **OPEN**.

---

## OS stance

- **Accept** edge under prior on tip-core and Jan–Aug.  
- **Target** conditional cells: Feb · May MISMATCH · soft Jun · FRAGILE Sep–Oct (once scored).  
- **Protect** Aug / Jul–Aug MATCH.  
- **Reject** borrowing M15 `AOS_L2det_de` / `DE40stack` without M5 tape CF.  
- Target research OS magic **26151907** (`DE40M5stack`) at P7 only.

---

## Next

1. P1-T00 — Tester tip **2026.05.01 → 2026.10.18** (and Sep–Oct alone).  
2. P1-T01…T05 — M5 L1 tape contract + labeled fires.  
3. Deal-measured Leak when deals available.
