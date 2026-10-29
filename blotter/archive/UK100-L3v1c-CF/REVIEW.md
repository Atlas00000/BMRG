# UK100-L3v1c-CF — tip re-test (EA 1.25)

**Verdict:** **PARTIAL_FAIL_STREAK_LATCH**  
**Run:** 2026-10-22 ~16:38 · final balance **548.79** · magic **26121907** · `dualBelow=1 confirmN=2 softDerisk=1`  
**Window:** 2026.05.01 → 2026.10.20

## Tip metrics (L3v1c chunk only)

| | L3v1c CF | Prior live (EN-only) | P0 AOS-OFF |
| --- | ---: | ---: | ---: |
| n | **112** | 121 | 153 |
| sum_R | **+20.75** | +20.75 | +22.5 |
| E_N | 0.185 | 0.172 | 0.147 |
| maxDD_R | **−5.0** | −5.75 | −8.0 |
| month_hit | 75% (4 mo) | 60% (5 mo) | 67% |
| last close | **2026-08-26** | ~Sep 4 | Oct 19 |

Monthly: May +11 · Jun +6.75 · Jul +5.5 · Aug **−2.5** · then dark.

## What worked

- EA **1.25** wired: init shows `dualBelow=1 confirmN=2 softDerisk=1`.
- Halt reason uses **EN20 / EF15** (policy-correct dual window).

## What failed

From **2026-08-26 14:55** hard `HALT_f0_BELOW_FRONTIER` → **81** block lines through **2026-10-19**, `streak` grew to **10204**.

**Root cause:** confirm streak incremented **every bar** while halted. With no new closes the WR ring freezes → EN20/EF15 stuck at −0.10 / −17 → permanent dark. Dual-window alone cannot self-heal.

## Follow-up shipped (EA **1.26** / L3v1d) — re-CF required

| Change | Purpose |
| --- | --- |
| Streak increments only on **new closes** (`ringN` change) | Stop bar-spam latch |
| `InpAOS_L3_BelowHaltMaxBars=500` | After ~2 M5 sessions halted → **probe unlatch** at f=0.25 |

Preset updated. **Recompile 1.26** · re-run tip CF · say **score UK L3v1d**.

## Gates

| Gate | Result |
| --- | --- |
| n ≥ 121 | **FAIL** (112) |
| sum_R ≥ +20.8 | FAIL (tied +20.75) |
| month_hit ≥ 60% | PASS on truncated path |
| fewer permanent BELOW | **FAIL** (latched Aug→Oct) |
