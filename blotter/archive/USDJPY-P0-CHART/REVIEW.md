# USDJPY-P0-CHART — expand-book review (not live)

**Preset:** `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Log:** `Tester/logs/20261019.log`  
**Frame:** asset-list expansion research · AOS OFF · **not** a live replacement · own AIOS later  
**Deposit:** 500 USD · magic **26101828** · G0 · every tick  
**Reviewed:** 2026-10-19

## Geometry (confirmed in log)

| Input | Value |
| --- | --- |
| SL / TP | **100 / 120** (RR 1.20, TP>SL) |
| BB | 20 / 2.2 |
| Session | 12–20 · Tue off |
| ATR regime | ON · max **70** |
| MaxSpread | 25 |
| AOS | OFF (`aos=0`) |
| Init | `USDJPY PERIOD_M15 \| BB(20,2.2) \| magic=26101828` |

Yen ATR-scaled — not EURUSD 300pt / GBPJPY 160pt floors. Design prior: probe WR≈57.6% / EF≈+0.8pp (n≈66); **Tester is thinner**.

## Rolling windows (closed TP/SL; R=1.20 · BWR=45.5% · Leak prior 11.4pp)

| Window | n | WR | Final | Net | E_N | BM | EF† |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **2026.05.01 → 08.31** (design tip core) | 56 | 48.2% | 505.99 | **+6.0** | +0.061R | +2.8pp | −8.6pp |
| 2026.01.01 → 04.30 | 8 | 50.0% | 501.20 | +1.2 | +0.100R | +4.5pp | −6.9pp |
| 2026.01.01 → 08.31 | 64 | 48.4% | 505.90 | +5.9 | +0.066R | +3.0pp | −8.4pp |
| **2026.01.01 → 10.19** (YTD tip) | 68 | **51.5%** | **517.99** | **+18.0** | **+0.132R** | +6.0pp | −5.4pp |
| 2025.01.01 → 2026.10.19 | 83 | 49.4% | 514.29 | +14.3 | +0.087R | +3.9pp | −7.5pp |

† EF uses **design Leak prior** (25pt / SL100), not blotter-measured c_R. Duplicate re-runs identical → one row each.

All windows: **WR > BWR** and **E_N > 0**. None clear Stage-1 EF under the 25pt prior (thin BM).

## Monthly (from Jan→Oct / long run)

| Month | n | WR | Read |
| --- | ---: | ---: | --- |
| 2025.04–10 | thin | mostly SL | sparse hist fires — ignore as score |
| 2025.11–12 | 5+5 | 60% | soft support |
| 2026.01–04 | 2–5 | 40–50% | thin / starved under ATR≤70 |
| **2026.05** | 13 | **53.8%** | MATCH home |
| **2026.06** | 22 | **54.5%** | MATCH · best fire month |
| **2026.07** | 18 | **33.3%** | **regime mismatch hole** (Ouroboros MATCH but FRAGILE%↑) |
| 2026.08 | 3–4 | 67–75% | thin recover |
| 2026.09 | **0** | — | FRAGILE tip · ATR≤70 correctly starved |
| 2026.10 | 3 | 100% | stub tip |

Jul is the expansion drag — frame as **regime mismatch**, not geometry death. Sep silence = gate doing its job.

## Gate / system behaviour

- Session + weekday dominate blocks (healthy).
- ATR>70 fires regularly (70–140pt) — regime filter active.
- Fail-pause after loss-streak=3 appears lightly (containment, not wipeout).
- Side mix ~**37% buy / 63% sell** (sell-heavy yen fade).
- No EOT orphans on scored windows. No AOS path.

## Vs design probe

| | Probe (M15* closed-bar) | Tester May→Aug |
| --- | ---: | ---: |
| n | ~66 | 56 |
| WR | 57.6% | **48.2%** |
| E_N | +0.27R | **+0.061R** |
| EF (25pt prior) | +0.8pp | **−8.6pp** |

Tick + friction ate ~9pp WR vs probe — expected Stage-0→1 gap; do not treat probe as blotter.

## Expansion verdict

**KEEP_RESEARCH / EXPAND_CANDIDATE** — not live, not AIOS yet.

- Engine geometry holds (TP>SL · RR 1.20 · ATR-scaled · G0).
- Pass soft bar `WR>BWR` + `E_N>0` on every rolled window.
- Weak equity (+1–4% on $500) and **EF≤0 under cost prior** → research sleeve only.
- Jul WR collapse + Sep starve = regime path, not a cut from the asset list.
- Own AIOS only after measured Leak / Stage-1 EF re-score — do not copy EUR/UK L2.

**Next (still not live):** export deals → measured c_R; optional Jul skip / ATR tercile; fire-count alt (BB 2.0) if n starvation bothers. Live book stays elsewhere.
