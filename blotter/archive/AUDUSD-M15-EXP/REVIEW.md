# AUDUSD-M15-EXP — Tester log review (expansion, not live replace)

**Source:** `Tester/logs/20261019.log`  
**Lens:** asset-list expansion · engine AOS OFF · **not** live replace of `8230931`  
**Preset authority (AUDUSD):** `Profiles/Tester/BMRG/AUDUSD/AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` · magic **8230901**

## Preset / geometry (AUDUSD CHAMP)

| Input | Value |
| --- | --- |
| TF | **M15** (Tester) |
| SL/TP | **300/300** RR=1 |
| Session | Start**13**–20 · Mon **off** · Tue **off** |
| Risk | 0.5% · MaxEntries 1 |
| BB/ATR | 20 / 2.2 / 14 |
| AOS | **OFF** |

## Runs in log

| # | Symbol | Geometry | Window | n | WR | E~ (RR1) | PnL@$400 | W20 min→last | path DD~ | Note |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| 7 | **AUDUSD** | CHAMP ✓ | May→Aug | 41 | **63.4%** | **+0.27** | +133 | 50→75 | 3.0% | primary tip |
| 8 | **AUDUSD** | CHAMP ✓ | Jan→Aug | 95 | 56.8% | +0.14 | +149 | 40→75 | 4.4% | longer mix |
| 6 | AUDUSD | **MISMATCH** 5000/6250 Start8 | May→Aug | — | — | — | +24 | — | — | **ignore** (DE30 inputs on AUD) |
| 0 | DE30 | own 5000/6250 Start8 | Jan→Oct | 145 | 51.0% | +0.02 | +212 | 30→50 | 7.8% | expansion xfer |
| 1 | DE30 | same | May→Oct | 77 | **58.4%** | +0.17 | +239 | 45→45 | 2.0% | better tip |
| 2–5 | DE30 | same | 2025 windows | ~36–38 | **~32%** | −0.33 | +24–35 | ≤25 | ~7% | **regime mismatch** |

## Rolling / monthly (AUDUSD CHAMP)

- W250 not applicable (AOS off; n≪250).
- May soft (WR 37.5%) inside an otherwise strong May→Aug — treat as pocket mismatch, not class reject.
- Jan→Aug: Feb/Mar below BWR — off-regime tax; engine still ends W20 at 75%.

## Expansion verdict

- **AUDUSD M15 CHAMP:** EXPANSION_KEEP candidate — WR-side intact on primary window; tip/off months = regime, not geometry failure.
- **DE30 M15:** WATCH — 2026 tip/mid OK; **2025 fails hard** (WR~32%) → do not promote on tip alone; needs own EDX / ATR scale before AIOS.
- **Not live replace.** Live remains `8230931` Risk3 M5 AIOS. These runs are list-expansion research only.
