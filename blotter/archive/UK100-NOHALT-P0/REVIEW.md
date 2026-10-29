# UK100-NOHALT-P0 — P0 balanced chart · AOS OFF

**Verdict:** **HALT_IS_THE_DRAG (partial)** — no-halt tip prints more trades / slightly more R, but deeper DD; not an auto VPS promote  
**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M5-UK100-6M-P0_balanced_chart.set`  
**True magic:** **26101905** · AOS **OFF** (no L3)  
**Window:** 2026.01.01 → 2026.10.20 · final balance **555.23**  
**Contrast live:** `UK100_5m_stack` · magic **26121907** · AOS ON

## Sleeve comparison (designed R)

| Slice | Preset | n | sum_R | E_N | WR | maxDD | m_hit |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tip May–Oct | **P0 AOS-OFF** | **153** | **+22.5** | 0.15 | 51% | **−8.0** | **67%** |
| Tip May–Oct | Live stack AOS-ON | 121 | +20.8 | 0.17 | 52% | −5.8 | 60% |
| Jan–Oct | P0 AOS-OFF | 272 | +25.0 | 0.09 | 49% | −10.0 | 50% |

Δ tip no-halt vs live: **+32 trades · +1.75R · +7pp month hit · −2.25R deeper maxDD**.

## Monthly (P0 Jan–Oct)

| Month | sum_R | Hit |
| --- | ---: | --- |
| Jan | +11.75 | Y |
| Feb | −4.00 | N |
| Mar | −1.50 | N |
| Apr | −3.75 | N |
| May | +11.00 | Y |
| Jun | +6.75 | Y |
| Jul | +5.50 | Y |
| Aug | −2.00 | N |
| Sep | −2.50 | N |
| Oct | +3.75 | Y |

Early-year red (Feb–Apr) and Aug–Sep soft — halt was not the only path issue.

## USDJPY+UK100 (equal) with this UK tape

| Metric | No-halt UK Jan–Oct | Tip Pareto watch (live UK) |
| --- | ---: | ---: |
| sum_R | +20.2 | +17.8 |
| month_hit | **60%** | **83%** |
| boot hit p10 | **40%** | 67% |
| maxDD | −4.9 | −2.6 |

More R, **worse** cycle hit — keep as watch, not promote on halt-off alone.

## Read

1. Yes — **live AOS halt truncates** UK tip activity (~121 vs 153) and clips some expectancy.  
2. Cost of leaving it off: **deeper maxDD** and still mediocre Jan–Oct month hit (50%).  
3. P0 is a **different magic / AOS-OFF research chart** — not a drop-in replace for `UK100_5m_stack`.  
4. Next ops fork (HITL): retune live L3 so it doesn’t false-trip Sep, **or** keep UK off / light until a live-magic no-halt CF exists.

**Not** a live `f` / VPS attach change from this run alone.
