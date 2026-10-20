# AUDUSD M15 — L2 size / lifecycle f table (P2-T05)

**Status:** SPEC — **P3 L4 bus signed** (`aos_l3l4_policy.md`); wire in research `.set` with `InpAOS_L4_SizeMod=true`  
**Task:** AUDUSD-AOS-P2-T05 · confirmed AUDUSD-AOS-P3-T03/T04  
**f_declared baseline:** research preset risk (CHAMP Harvest · magic **8230901**); live Track B Risk 3% is separate

| State | Condition (expansion) | f_mult |
| --- | --- | ---: |
| Expanding | W15 E_N > baseline and rising | 1.0 |
| Stable | W15 E_N ≥ 0 · small Δ | 1.0 |
| Compressing | W15 E_N falling 2 evals or Fragile EF | 0.5 |
| Near frontier | EF_proxy ≤ 1 pp or W15 E_N < 0 | 0.25 |
| Below frontier | W20 E_N ≤ 0 and tip EF_proxy ≤ 0 | 0.0 |
| L2det WOULD_SKIP | Armed det map hit (`BUY∧May` v1) | 0.0 (skip > size) |

Do not size-live until L4 emits states and L3 halt policy (P3) is signed.  
Never apply this table to magic **8230931** without a separate Track B HITL.
