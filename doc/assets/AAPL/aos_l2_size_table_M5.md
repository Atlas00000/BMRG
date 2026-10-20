# AAPL M5 — L2 size table (spec)

**Task:** AAPL-M5-AOS-P2-T04  
**Status:** SPEC only — wire after L4 lifecycle  
**Engine:** magic **26102011** · lot Fixed **1.0** (VOLUME_MIN)  
**Policy:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md)

Apple CFD min lot ≈ 1.0 → size-down is often **binary** (f=1 or f=0 via skip). Multipliers below are for future risk-% mode or if broker min allows finer lots.

| Lifecycle / cell | f multiplier | Note |
| --- | ---: | --- |
| Expanding / tip protect (May, Mon) | **1.00** | Never size-down protect cells |
| Stable | **1.00** | Default |
| Compressing (L4) | **0.50** | Spec — may floor to 0 at min lot |
| Jul / Wed (v1b skip) | **0.00** | Implemented as L2det skip, not size |
| H18 / spread / H1 (optional) | **0.00** when armed | Same |
| Below-frontier (L3) | **0.00** | Hard halt outranks |

**Do not** change SL/TP as a size substitute.
