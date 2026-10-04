# BMRG Client — Product Brief

**Task:** `UI-P0-T01`  
**Status:** DONE  
**Companions:** `doc/client_ia.md` · `doc/client_roadmap.md` · `client/design/UI_PHILOSOPHY.md`  
**Engine / OS lock:** Harvest magic **8210204** · EA **v1.21** · L2 pin `L2skip_inf_p92_20260927_223519` · mode **LIVE_WITHHOLD**

---

## 1. One-liner

A **read-first operator console** for BMRG: observe health, EA/OS state, prove artefacts, and ops pins — without placing trades or bypassing wiring auth.

---

## 2. Personas

| Persona | Primary job | Needs | Must not |
| --- | --- | --- | --- |
| **Operator** | Run demo attach / prep FT | Live identity, mode, fuses, journal tail, next action | Remote-toggle MT5 kill; order ticket |
| **Researcher** | Prove L2 / CF / skip audit | Health vector, baseline Δ, CF vs engine, skip clusters | Treat CF as live equity; reopen EDX |
| **Viewer** | Audit status read-only | Same surfaces, mutate controls hidden/disabled | See enabled promote / FT ship without role |

Roles are UI stubs until `UI-P1-T04`; Viewer is the default safe posture.

---

## 3. Jobs to be done

1. **Am I looking at the champion?** — magic · preset · ea_version · model pin in one glance.  
2. **Is the book healthy?** — WR / R / BM / Leak / EF / E_N / MaxDD / n / zone (edge vocabulary only).  
3. **What is the OS doing?** — mode OFF/SHADOW/LIVE_WITHHOLD · L2 decisions · L3 halt outranks.  
4. **Did prove pass?** — CF deltas · skip audit · ACCEPT/REJECT · path≠paper callouts.  
5. **What do I do next?** — Home composition: status + single next action (not a widget dump).  
6. **Where is the blotter?** — inbox / archive / CURRENT without mixing task IDs.

---

## 4. Success metrics (product)

| Signal | Pass |
| --- | --- |
| Vocabulary | Primary cards use EF-framework fields only |
| Time-to-identity | Magic + mode visible from any route (shell meta) |
| Honesty | CF vs live path clearly separated when both shown |
| Agency | No trade buttons; mutate gated by `WIRE_AUTHORISATION` |
| Chrome | Ledger Noir + Signal Teal inherited globally |

---

## 5. Non-goals (hard)

| Non-goal | Rationale |
| --- | --- |
| Chart trading / order tickets | EA executes; UI observes |
| EDX reopen as a campaign | Discovery closed — consume archives only |
| Balance-only hero | Vanity equity ≠ edge score |
| “AI confidence” KPI | Forbidden label; use proba only in ledger context |
| Purple SaaS / crypto-neon UI | Philosophy kill list |
| Live FT ship without `AOS_LIVE_FT` | Separate auth boundary |
| Section content overhaul in P0 | Foundations + IA only; feature pages later weeks |

---

## 6. Auth boundary

| Flag / allow | UI behaviour |
| --- | --- |
| Viewer | Read all shipped surfaces |
| Operator | See gated actions; enabled only if auth allows |
| `EA_LIVE_AI_GATE_SHIP` | Hook already shipped — display mode truthfully |
| `AOS_LIVE_FT` | FT route visible but ship/mutate blocked until authorised |

Source of truth: `infra/artefacts/ops/WIRE_AUTHORISATION.json` (wired in UI-W02+).

---

## 7. Design system lock

**Ledger Noir + Signal Teal** — `client/design/UI_PHILOSOPHY.md`.  
P0 ships tokens, primitives, shells, Home proof. Feature layouts compose these; they do not redefine them.

---

## 8. Exit (P0 product)

- [x] Personas + JTBD documented  
- [x] Non-goals include: no chart trading, no EDX reopen, no balance-only hero  
- [x] Auth / FT boundary named for later weeks  
