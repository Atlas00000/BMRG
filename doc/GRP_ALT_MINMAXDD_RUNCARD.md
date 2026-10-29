# GRP alternate — EURUSD+DE40+USDJPY+AAPL (25% each)

**Cluster:** EURUSD · DE40 · USDJPY · AAPL · equal weight (designed R)  
**Policy:** `min_maxDD` (Pareto / GRP-P5 alternate)  
**Window:** **2026.01.01 → 2026.10.20** (Jan–Oct extended CF — not the tip-6m freeze)

MT5 Tester is single-symbol. Run **four** passes. Offline panel applies **25% each** on designed `pnl_R` — leave live stack / `f` as frozen (do not quarter lots for this CF).

This window is **longer than** the GRP tip panel (May–Oct). Expect metrics ≠ frozen +20.7R tip row; treat as an extended-path check.

---

## Shared Tester settings

| Setting | Value |
| --- | --- |
| Expert | `Experts\BMRG\BMRG.ex5` |
| Model | Every tick (or 1-min OHLC if agreed) |
| Dates | **2026.01.01 → 2026.10.20** |
| Deposit | ACCOUNT CURRENCY |
| Rule | One chart · one preset · one magic per pass |

---

## Pass A — EURUSD

| Setting | Value |
| --- | --- |
| Symbol | **EURUSD** |
| Period | **M5** |
| Magic | **8210204** |
| Preset | `Presets/INF-LIVE_WITHHOLD_Harvest_long_ddl30.set` (or Tester twin under `Profiles/Tester/BMRG/`) |

---

## Pass B — DE40

| Setting | Value |
| --- | --- |
| Symbol | **DE30** |
| Period | **M5** |
| Magic | **26151907** |
| Preset | `Presets/DE40_5m_stack.set` |

---

## Pass C — USDJPY

| Setting | Value |
| --- | --- |
| Symbol | **USDJPY** |
| Period | **M15** |
| Magic | **26131807** |
| Preset | `Presets/USDJPYstack.set` |

---

## Pass D — AAPL

| Setting | Value |
| --- | --- |
| Symbol | **Apple** |
| Period | **M5** |
| Magic | **26162017** |
| Preset | `Presets/AAPL_5m_stack.set` |

---

## After all four

1. Drop Tester logs into `blotter/inbox/` (or leave in `Tester/logs/`).  
2. Say **score min_maxDD** — agent will parse with:

```bat
cd infra
python -m src.diversify.run_p2_scorer --log ..\..\..\Tester\logs\YYYYMMDD.log --from 2026-01-01 --to 2026-10-20 --match-tester-window
```

3. Score group `EURUSD+DE40+USDJPY+AAPL` at equal 25% on designed R (Jan–Oct panel).

---

## Checklist

| # | Sleeve | Symbol / TF | Magic | Done |
| --- | --- | --- | ---: | --- |
| A | EURUSD | EURUSD M5 | 8210204 | ☐ |
| B | DE40 | DE30 M5 | 26151907 | ☐ |
| C | USDJPY | USDJPY M15 | 26131807 | ☐ |
| D | AAPL | Apple M5 | 26162017 | ☐ |
