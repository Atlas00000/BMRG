# EDX-P0-T02 — Rolling windows, lifecycle, ΔD

**Scored:** 2026-09-25  
**Source:** EDX-P0-T01 long segment (570 TP/SL events, R proxy = 1.5, Leak = 0)  
**Events CSV:** `events_Rproxy.csv`

## Latest window health vectors

| Window | n | WR | BM | EF (Leak=0) | M | E_N | Zone |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Full | 570 | 44.74% | +4.74 pp | +4.74 pp | ±4.08 pp | +0.118R | Robust* |
| W100 | 100 | 42.0% | +2.0 pp | +2.0 pp | ±9.67 pp | +0.050R | Fragile |
| W250 | 250 | 44.8% | +4.8 pp | +4.8 pp | ±6.16 pp | +0.120R | Fragile |
| W500 | 500 | 44.2% | +4.2 pp | +4.2 pp | ±4.35 pp | +0.105R | Fragile |

\*Full-sample gross only; W250/W500 (lifecycle keys) are **Fragile**. Any positive Leak flips full sample toward Fragile.

## W250 step series (step = 25 events)

| end event | WR | EF pp | M pp | E_N | Zone |
| ---: | ---: | ---: | ---: | ---: | --- |
| 250 | 46.8% | 6.8 | 6.19 | 0.17 | Robust |
| 275 | 46.4% | 6.4 | 6.18 | 0.16 | Robust |
| 300 | 44.0% | 4.0 | 6.15 | 0.10 | Fragile |
| 325–400 | ~43% | 2.8–3.2 | ~6.1 | 0.07–0.08 | Fragile |
| 450–475 | ~45% | 4.4–5.2 | ~6.2 | 0.11–0.13 | Fragile |
| 500 | 43.6% | 3.6 | 6.15 | 0.09 | Fragile |
| 525–550 | 44–46% | 4.0–5.6 | ~6.2 | 0.10–0.14 | Fragile |

Early sample was Robust; from ~event 300 onward the system sits in **Fragile** (EF ≤ M).

## Edge velocity ΔD

Non-overlapping W250 blocks:

| Block | Events | EF |
| --- | --- | ---: |
| Previous | n−500 … n−251 | +3.6 pp |
| Current | n−250 … n−1 | +4.8 pp |
| **ΔD** | | **+1.2 pp** |

Velocity mildly positive, but **level remains Fragile** on both blocks. Unified lifecycle: not Expanding (needs EF > M); closest label **Near frontier / Fragile** with slight recovery in ΔD.

## Lifecycle state (normative keys W250 + W500)

| Check | Result |
| --- | --- |
| W250 EF > M? | No (4.8 ≤ 6.16) |
| W500 EF > M? | No (4.2 ≤ 4.35) |
| EF ≤ 0 on W250 and W500? | No — do **not** halt |
| State | **Near frontier (Fragile)** |
| Mandatory action (framework) | De-risk bias for later phases; investigation allowed; **do not** raise f or MaxLevels |

## DEPENDENCE (preview for P1)

| Metric | Value |
| --- | ---: |
| Worst loss streak | 9 |
| Expected worst ≈ ln(n)/ln(1/(1−WR)) | ≈ 10.7 |
| 1.5× threshold | 17 |
| Flag | **No DEPENDENCE** (streak below threshold) |

## Accept

- Rolling vectors filled  
- Lifecycle = Near frontier / Fragile  
- ΔD = +1.2 pp (level still Fragile)  

## Notes

Leak still unmeasured (pips baseline). Adding Leak will widen Fragile / may push EF ≤ 0 on W500.
