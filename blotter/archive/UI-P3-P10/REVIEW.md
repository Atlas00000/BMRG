# UI-P3→P10 — ACCEPT (P9 BLOCKED)

**task_id:** UI-P3-P10  
**archived_at:** 2026-09-28  
**verdict:** DONE for P3–P8 + P10 · P9 FT mutate **BLOCKED** (no AOS_LIVE_FT)

## Exit criteria

| Phase | Exit | Met |
| --- | --- | --- |
| P3 Live | Demo journal · kill display-only | yes |
| P4 Layers | Ledger · WOULD_SKIP ≠ smarter entry · L3 outrank | yes |
| P5 Prove | CF ≠ live equity · skip audit link | yes |
| P6 Ops | Mutate gated · dry-run fixture | yes |
| P7 Blotter | Magic↔preset · CURRENT.md | yes |
| P8 FT design | Doc + AuthGate · AOS_LIVE_FT forbidden | yes |
| P9 FT ship | BLOCKED stubs only | yes (blocked) |
| P10 Polish | a11y skip-link · exports · README | yes |

## Artefacts

- `client/src/routes/{Live,Layers,Prove,Ops,Blotter,FT}.tsx`
- `client/src/features/auth/AuthGate.tsx`
- `doc/client_p3_p10_plan.md` · `doc/client_ft_console.md`
- `npm run build` green

Next: enable P9 only when WIRE allows `AOS_LIVE_FT`.
