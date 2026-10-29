# GRP primary — JP225 50% · DE40 50%

**Cluster:** JP225 + DE40 · equal weight (designed R)  
**Authority:** GRP-P5 · `live_asset_profile.md` §6.1  
**Window:** **2026.05.01 → 2026.10.20** (tip 6m)

MT5 Tester is single-symbol. Run **two** passes. Offline panel applies **50/50** on designed `pnl_R` — do **not** half lots in Tester for this CF (live `f` / stack as frozen).

---

## Pass A — JP225

| Setting | Value |
| --- | --- |
| Expert | `Experts\BMRG\BMRG.ex5` |
| Symbol | **JPN225** |
| Period | **M5** |
| Model | Every tick (or 1-min OHLC if agreed) |
| Dates | 2026.05.01 → 2026.10.20 |
| Deposit | ACCOUNT CURRENCY |
| Magic | **26161907** |
| Preset | `Presets/JPN225_5m_stack.set`  
| | (or `Profiles/Tester/BMRG/JP225/JPN225_5m_stack.set`) |

Load `.set` → Start. Save / note Tester log path when done.

---

## Pass B — DE40

| Setting | Value |
| --- | --- |
| Expert | `Experts\BMRG\BMRG.ex5` |
| Symbol | **DE30** |
| Period | **M5** |
| Model | same as Pass A |
| Dates | 2026.05.01 → 2026.10.20 |
| Deposit | ACCOUNT CURRENCY |
| Magic | **26151907** |
| Preset | `Presets/DE40_5m_stack.set`  
| | (or `Profiles/Tester/BMRG/DE40/DE40_5m_stack.set`) |

---

## After both runs

1. Drop both Tester logs (or report HTML / deal export) into `blotter/inbox/`.  
2. Say **score primary** — agent runs:

```bat
cd infra
python -m src.diversify.run_p2_scorer --inbox --from 2026-05-01 --to 2026-10-20 --match-tester-window
```

3. Recompute group row for `JP225+DE40` vs frozen tip: **sum_R +31.0 · m_hit 100% · maxDD −2.5 · Sep–Oct +3.0**.

---

## Pass checklist

| # | Sleeve | Magic | Done |
| --- | --- | ---: | --- |
| A | JP225 / JPN225 M5 | 26161907 | ☐ |
| B | DE40 / DE30 M5 | 26151907 | ☐ |

Do not mix tip + longer windows in one log. One chart · one preset · one magic per pass.
