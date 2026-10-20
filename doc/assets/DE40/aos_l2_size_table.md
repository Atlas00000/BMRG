# DE40 — L2 size multipliers (spec)

**Task:** DE40-AOS-P2-T05  
**Status:** SPEC only — wire after L4 health bus  
**Parent:** [`aos_l2_policy.md`](./aos_l2_policy.md)

Skip outranks size. If L2det would skip, `f_mult=0` (no size-down substitute for a hard skip).

| Lifecycle / state | f_mult | Note |
| --- | ---: | --- |
| Expanding / Stable | **1.0** | Default research f |
| Compressing | **0.5** | L4 recommend |
| Near frontier | **0.25** | Soft caution |
| Below frontier | **0.0** | L3 halt path |
| L2det WOULD_SKIP | **0.0** | Armed BUY∧near_atr / future maps |

Do not invent size curves from tip PnL alone. Revisit multipliers after L4 W15/W20 paths exist.
