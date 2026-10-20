# JP225 / JPN225 M5 — L2 size multipliers (spec)

**Task:** JP225-M5-AOS-P2-T06  
**Status:** Spec only — wire after L4 health bus  
**Parents:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) · [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)

| Lifecycle / state | f_mult | Note |
| --- | ---: | --- |
| Expanding / Stable | 1.0 | Default |
| Compressing | 0.5 | L4 recommend |
| Near frontier | 0.25 | Soft derisk |
| Below frontier | 0.0 | L3 halt outranks |
| L2det WOULD_SKIP | 0.0 | Skip outranks size |

Never size-up above 1.0 in OS. Never invent entries.
