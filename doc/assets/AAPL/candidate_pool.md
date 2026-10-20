# AAPL — Candidate Pool

**Version:** 0.1.0  
**Updated:** 2026-10-12  
**Scope:** Expansion asset list only · **not** live replace for EURUSD / AUDUSD  

---

## Current candidate (locked)

| Field | Value |
| --- | --- |
| **Status** | **KEEP — expansion candidate** |
| **Sleeve** | Harvest (engine only) |
| **Preset** | `Profiles/Tester/BMRG/AAPL/BMRG-M15-AAPL-6M-Harvest_RR1.25.set` |
| **Alias / P0 freeze** | `AAPL-AOS-P0-T01_baseline_Harvest.set` (same geometry · AOS OFF) |
| **Magic** | **26092501** |
| **AOS** | **OFF** (`InpAOS_Enable=false`) |
| **TF / symbol** | M15 · Apple |
| **Geometry** | SL **300** / TP **375** · RR **1.25** · BWR **44.4%** |
| **Evidence** | [`system_profile.md`](./system_profile.md) · Tester `20261012.log` |
| **Score under** | [`edge_framework.md`](./edge_framework.md) |

**Decision (2026-10-12):** Use the **Harvest baseline** as the Apple candidate for now. Do **not** promote L2det shadow/live presets (`26101221` / `26101222`) or Balanced (`26092502`) as the book candidate.

AIOS work remains **research / optional** against this frozen baseline — it does not replace the candidate until HITL says otherwise.

| Stream | Roadmap / build |
| --- | --- |
| M15 Harvest OS | [`aios_roadmap.md`](./aios_roadmap.md) · [`BUILD_PLAN.md`](./BUILD_PLAN.md) |
| M5 Balanced OS | [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) · **`AAPL_5m_stack`** · magic **26162017** · P7 HITL |

---

## Pool table

| ID | Preset / magic | Role | Verdict |
| --- | --- | --- | --- |
| **AAPL-H0** | Harvest M15 · **26092501** | **Current candidate** | **KEEP** |
| AAPL-B0 | Balanced M15 · 26092502 | Reference sleeve | WATCH |
| **AAPL-M5-B** | Balanced M5 · engine **26102011** · OS **`AAPL_5m_stack` 26162017** | Tip expansion research HITL | **WATCH** (Stage-0 OK; Stage-1 Fragile) |
| AAPL-AOS-P2-shadow | L2det Thu/18 · 26101221 | OS experiment | NOT candidate |
| AAPL-AOS-P2-live | L2det Thu/18 · 26101222 | OS experiment | NOT candidate |

M5 profile: [`system_profile_M5.md`](./system_profile_M5.md).

---

## Operating rules

1. Tester / research default load = **Harvest baseline** (`26092501`, AOS OFF).  
2. Any AOS preset must keep a **different magic** and be scored as Δ vs baseline — never overwrite H0.  
3. Canvas / tip charts do not change this pool entry.  
4. Live attach remains **out of scope** until edge_framework production ladder is explicitly run and signed.

---

## One-line

**Apple expansion candidate = Harvest baseline magic 26092501 · AOS OFF; L2det and Balanced stay off-candidate until further notice.**
