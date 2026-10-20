# JP225 M5 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** JP225-M5-AOS-P6-T01 … T03  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/JP225-M5-AOS-P6/P6_HARDEN.json` · `P6_SUMMARY.json`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1c · P4/P5 wire  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.  
**L9 focus:** London open / H08 / H10 / spread tercile — **protect Jul / SELL / H08·H10 stars**.  
**Sibling:** M15 [`aos_p6_harden.md`](./aos_p6_harden.md) — **do not merge** ATR (19670 vs 7610–11285) or May∨Jul maps.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no new LIVE veto · H08/London/H10 **DISARM** · BUY∧H08 / spread / soft-hours **HOLD_SHADOW** |
| P6-T02 ±10% L2det bound stress | **PASS_WITH_NOTES** — keep **(BUY∧MATCH)∨(BUY∧H09\|13\|16)**; narrowing MATCH-only / hours-only hurts; never skip nearATR / MISMATCH-all |
| P6-T03 ATR band G3 | **PASS** — **7610–11285** on P0 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

H08 / H10 are tip **protect** cells on M5 — soft-vetoing them burns Jul/SELL FP. Soft hours all-sides already covered by L2det BUY∧ — do not double-wire LIVE.

### On full tip

| Policy | Tip verdict | ΔE_N | Prec | Ret% | Jul FP | SELL FP |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| skip H08 | **DISARM** | −0.085 | 0.47 | 79.8 | 5 | **7** |
| skip BUY∧H08 | HOLD_SHADOW | +0.011 | 0.63 | 91.5 | 2 | 0 |
| skip London open H08–09 | **DISARM** | −0.027 | 0.56 | 73.4 | 6 | **7** |
| skip H10 | **DISARM** | −0.151 | 0.11 | 90.4 | 3 | 3 |
| skip spread > p66 | HOLD_SHADOW | +0.017 | 0.67 | 93.6 | 0 | 2 |
| skip soft H09\|13\|16 (all) | HOLD_SHADOW | +0.255 | 0.75 | 66.0 | 2 | 4 |

### Additive on **v1c-kept** path

| Policy | Verdict | ΔE_N | Ret% | Note |
| --- | --- | ---: | ---: | --- |
| add H08 / London / H10 | **DISARM** | negative | — | Jul / SELL collateral |
| add BUY∧H08 | **DISARM** | −0.002 | 91.3 | no lift on kept |
| add spread > p66 | **DISARM** | −0.001 | 94.2 | no lift on kept |
| add soft H09\|13\|16 all | HOLD_SHADOW | +0.188 | 78.3 | already in L2det BUY∧ |

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **HOLD_SHADOW** — not LIVE (no additive lift on v1c) |
| `L9_skip_H08` / London open | **DISARM** — Jul / SELL protect |
| `L9_skip_BUY_H08` | **HOLD_SHADOW** — not LIVE |
| `L9_skip_H10` | **DISARM** — protect star |
| `L9_skip_soft_H09_13_16_all` | **DISARM as L9** — already in L2det BUY∧; do not double-wire |

Overlay `L2det_jp225_m5_v1c` remains the research L2 path. L9 is additive soft layer, not a replace. **No L9 LIVE veto** at P6.

---

## 2. P6-T02 — L2 bound stress (MATCH / hour · not nearATR)

Baseline tip v1c: kept E_N **+0.478R** · ret **73.4%** · SELL FP **0** · Jul FP **1**.

| Stress | kept E_N | Δ vs v1c | Ret% | Read |
| --- | ---: | ---: | ---: | --- |
| **v1c nominal** | **0.478** | **0** | **73.4** | **keep** |
| BUY∧MATCH only | 0.385 | −0.094 | 83.0 | hours leg earns keep |
| BUY∧H09\|13\|16 only | 0.364 | −0.115 | 81.9 | MATCH leg earns keep |
| BUY∧MATCH ∨ BUY∧H13 only | 0.458 | −0.020 | 76.6 | H09\|16 earn keep |
| BUY∧MATCH ∨ BUY∧H09\|13 | 0.457 | −0.021 | 74.5 | H16 earns keep |
| BUY∧MATCH ∨ BUY∧H08\|09\|13\|16 wide | 0.476 | −0.002 | 67.0 | HOLD — Jul FP↑ · ret cost |
| BUY∧Aug only ∨ BUY∧H09\|13\|16 | 0.419 | −0.059 | 78.7 | do not drop Sep MATCH |
| BUY∧Sep only ∨ BUY∧H09\|13\|16 | 0.417 | −0.062 | 76.6 | do not drop Aug MATCH |
| MATCH all sides ∨ BUY∧H09\|13\|16 | 0.647 | +0.169 | 54.3 | HOLD — **6 SELL FP** |
| **REJECT probe BUY∧nearATR** | **0.265** | **−0.213** | 88.3 | tip star — never soft-veto |
| **REJECT probe MISMATCH-all** | **0.031** | **−0.447** | 68.1 | **DISARM** — OFFHOME home |

**Read:** Keep EA defaults **(BUY∧MATCH)∨(BUY∧H09\|13\|16)**. Do not narrow to one leg. Do not arm all-sides MATCH. Never soft-veto nearATR or MISMATCH-all. Do not stress-test by changing SL/TP / ATR band 7610–11285.

---

## 3. P6-T03 — ATR band / G3 declaration

| Preset | ATR regime | Band pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_growth_chart.set` (Presets + Profiles) | true | **7610–11285** | OK |
| `…P4_research_OS_W50.set` (Presets + Profiles) | true | **7610–11285** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR band.  
Declaration: `regime_filtered=true` · session 08–17 · skip Tue · ATR band **7610–11285**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
Engine Growth P0 M5 (26101906 geometry · ATR 7610–11285 · RR=2.0)
+ L2det_jp225_m5_v1c LIVE_WITHHOLD (research magic 26161904)
+ L3/L4/W50/ledger
+ L9 BUY∧H08 / spread SHADOW only (not wired LIVE)
+ L2 AI DISARM (L2skip_jp225_m5)
```

Next: **P7** · HITL · **`JPN225_5m_stack`** · magic **26161907**.
