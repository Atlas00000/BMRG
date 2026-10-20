# UK100 M5 — L2size f multipliers (spec)

**Task:** UK100-M5-AOS-P2-T05  
**Status:** SPEC only — wire after L4 health bus  
**Parent:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md)

Skip (`L2det WOULD_SKIP` / v1b) **outranks** size. Never size up above 1.0 in research OS.

| Lifecycle / state | f_mult | Note |
| --- | ---: | --- |
| Expanding | 1.0 | Default |
| Stable | 1.0 | Default |
| Compressing | 0.5 | L4 recommend |
| Near frontier | 0.25 | Soft |
| Below frontier | 0.0 | Align L3 halt |
| L2det WOULD_SKIP (v1b) | 0.0 | Hard withhold |

Bump when L4 paths land in P3.
