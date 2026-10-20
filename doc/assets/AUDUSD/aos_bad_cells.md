# AUDUSD — AIOS bad-cell registry (L2det seed)

**Version:** 0.1.1 · **Parent:** [`aios_roadmap.md`](./aios_roadmap.md) · [`aos_l2_policy.md`](./aos_l2_policy.md)  
**Frozen from:** M15 CHAMP tip May→Aug 2026 · mag **8230901** · `blotter/archive/AUDUSD-M15-EXP/`  
**P2 CF:** `blotter/archive/AUDUSD-AOS-P2/P2_CF.json` — preferred arm `BUY∧May`

**Use:** L2det SOFT skip / size candidates. Never permanent `AllowBuy=false`. Never geometry change.

---

## Priority cells (ARM candidates)

| Cell | Evidence | Stance |
| --- | --- | --- |
| **BUY ∧ May** | P2 tip CF: skips=2 · prec 100% · ΔE_N +0.065 · ret 95% | **ARM_SOFT** — `L2det_aud_m15_v1` |
| **BUY ∧ Thu** | P2 tip CF: ΔE_N +0.065 · ret 88% · 2 JunAug FP | **ARM_SOFT** alt atom |
| **Month ≈ May** (all sides) | Tip WR **37.5%** · blanket HOLD (SELL/WedFri FP) | Seed only — do not blanket arm |
| **Month ≈ Feb / Mar** | Long HOLD_SOFT · not tip arm | **SOFT** off-regime — L3/L5 diagnostic |
| **DOW = Thu** (all sides) | Tip WR **40%** · blanket HOLD (SELL/JunAug FP) | Seed only — prefer BUY∧Thu |
| **Loss streak ≥ 3** | Max L=4 on tip; containment=3 | Size-down / pause via L3–L4 bus (not L2 alone) |
| **Band-ride / failed fade** | Label-only in P2 — never arm outcome flags | L1 pre-trade proxy → L2 AI feature |

## Protect cells (false-skip report required)

| Cell | Evidence | Rule |
| --- | --- | --- |
| **Wed** | Tip WR **73.7%** · E_N +0.47R | Do not over-skip |
| **Fri** | Tip WR 66.7% | Protect |
| **SELL** | Tip WR 65.2% &gt; BUY 61.1% | Never blanket skip sells |
| **H15 / H18** | High WR (small-n) | Protect mid/late session |
| **Jun–Aug tip core** | WR 63–80% | Home edge — retention must stay high |

## Explicit non-cells

| Idea | Why not |
| --- | --- |
| Permanent AllowBuy=false | Both sides positive; sell-led only mildly |
| Skip all of session hour 13 | Tip H13 WR 56% ≥ BWR — not a drain like EUR H13 |
| Re-enable Mon/Tue | Already filtered by champ geometry |
| ATR max gate | P8-T03 SKIP — no n≥30 BM≤0 cell |

---

## Versioning

- **0.1.0** — Seed from M15 CHAMP system_profile (2026-10-19).  
- **0.1.1** — P2 CF: arm BUY∧May; blanket Thu/May demoted (2026-10-19).
