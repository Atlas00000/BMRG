# BMRG Phase 1 Roadmap — Execution Engine Only

Source of truth: `concept.md` §7–§8 (locked Phase 1 decisions).  
Goal: a reliable, configurable **automated execution engine** for BMRG-A on the current chart. Not strategy perfection.

---

## 1. Objective

Ship a single-symbol, single-timeframe EA that:

* Reads BB (SMA + σ) on closed bars
* Evaluates entry / exit per locked rules
* Places / closes market orders with basic risk gates
* Tracks one basket by magic + symbol
* Logs enough data for M5 basket-level research

**Done means:** attach to a chart (or Strategy Tester), compile once for that week’s build, run, and see correct entries/exits without crashes or silent failures.

---

## 2. Hard scope boundary

### In scope (Phase 1)

* Modular layout under `BMRG/` + `Include/`
* Locked inputs from `concept.md` §8
* Closed-bar entry (±2σ) and SMA exit
* Market orders only
* Fixed lot, max entries, spread, slippage, cooldown, magic
* Optional fixed SL (`SL_Points`)
* Equity halt (block new entries)
* One direction at a time; hedging account required
* Restart rebuild of basket from open positions
* Structured logging

### Out of scope (do not build)

* ATR-adaptive spacing, RSI, trend filter, regime detection
* Pending orders, multi-symbol, portfolio, sessions, AI
* Risk-% sizing, R:R, TP, ATR stops, anti-martingale
* Optimisation frameworks, dashboards, UIs, charts objects beyond needs
* Partial exits, opposite-band exits, time stops (unless forced by a blocker)
* Raising grid depth as a “feature” — keep `MaxLevels` default **1**; multi-level only after Phase 1 acceptance

If a task is not listed in a weekly deliverable below, it waits.

---

## 3. Anti-overengineering rules

* Implement **only** what the locked spec requires.
* Prefer plain functions / thin structs over class hierarchies.
* No “future-proof” abstractions for Phase 1.1 — empty hooks are enough.
* No second indicator stack; one BB handle path.
* No dry-run framework, plugin system, or config files beyond `input` params.
* Fail closed: validate → log → skip; do not invent recovery strategies.
* Do not refactor for elegance mid-phase; fix only what blocks compile or correct execution.

---

## 4. Compile-once rule (per week)

Each week is one batch:

1. Finish **all** files listed for that week (no partial mid-week MetaEditor cycles required).
2. **Compile once** in MetaEditor.
3. Fix only compile errors if any (small repair loop — not feature work).
4. **Then** test against that week’s acceptance checklist.

Do not start the next week’s modules until the current week’s compile + checklist pass.

Suggested intra-week order (write top → bottom, still compile only at the end):

1. Headers / modules with no MT5 trade side effects
2. Modules that depend on them
3. Wire `BMRG.mq5` last so the project is whole before the single compile

---

## 5. Target tree (do not expand)

```
BMRG/
├── BMRG.mq5
├── concept.md
├── roadmap.md
└── Include/
    ├── Config.mqh
    ├── Logger.mqh
    ├── State.mqh
    ├── Indicators.mqh
    ├── Signal.mqh
    ├── Grid.mqh
    ├── Basket.mqh
    ├── Risk.mqh
    └── Execution.mqh
```

---

## 6. Weekly implementation plan

### Week 1 — Scaffolding & configuration (no trading)

**Write (batch, then compile once)**

| File | Responsibility |
| --- | --- |
| `Include/Config.mqh` | All locked `input`s; defaults; `ConfigValidate()` (ranges, hedging check refuse) |
| `Include/Logger.mqh` | `LogInfo` / `LogWarn` / `LogError`; optional Comment panel line |
| `Include/State.mqh` | Runtime fields only (last bar time, halt flag, basket side, entry count) — no trade logic |
| Stub bodies | Empty or no-op APIs in Indicators / Signal / Grid / Basket / Risk / Execution so includes resolve |
| `BMRG.mq5` | `#include`s; `OnInit` validate + log; `OnDeinit` cleanup; `OnTick` empty or “new bar detect” only |

**Compile once → test**

* [ ] Compiles clean
* [ ] Attaches on hedging demo; refuses/init-fails clearly on netting
* [ ] Invalid inputs rejected with log
* [ ] No orders sent

**Exit:** scaffold is the permanent skeleton; stubs exist; config is the single source of parameters.

---

### Week 2 — Indicators, signal, grid (signals only)

**Write (batch, then compile once)**

| File | Responsibility |
| --- | --- |
| `Include/Indicators.mqh` | Create/release BB handle; read upper / mid / lower at shift 1 |
| `Include/Signal.mqh` | Entry: close beyond ±2σ; Exit: close crosses/touches mid; honour `AllowBuy` / `AllowSell` |
| `Include/Grid.mqh` | Level map from σ; default `MaxLevels = 1`; expose next free level only |
| `BMRG.mq5` | On new bar: refresh indicators → evaluate signal → **log only** (no `OrderSend`) |

**Compile once → test**

* [ ] Compiles clean
* [ ] Strategy Tester or chart: logs show band values and entry/exit signals on known bars
* [ ] No trades
* [ ] One-direction rule reflected in signal output (e.g. no dual signals while “virtual” side set if you track it in State)

**Exit:** signal path trusted; execution still off.

---

### Week 3 — Basket, risk, execution (engine goes live)

**Write (batch, then compile once)**

| File | Responsibility |
| --- | --- |
| `Include/Basket.mqh` | Positions by magic + symbol; side; count; rebuild from market; close-all for side |
| `Include/Risk.mqh` | Fixed lot; max entries; max spread; slippage; cooldown bars; equity halt; optional SL points on entry |
| `Include/Execution.mqh` | Symbol constraints (lot step, stops/freeze, filling); market buy/sell; close position(s); fail closed |
| `BMRG.mq5` | Full tick path: new bar → indicators → basket refresh → risk gates → signal → execute → log |
| `OnTradeTransaction` (optional but preferred) | Confirm fills / update state without polling complexity beyond need |

**Compile once → test**

* [ ] Compiles clean
* [ ] Demo or Tester: entry at ±2σ, exit at SMA, market orders only
* [ ] MaxEntries / spread / cooldown / AllowBuy|Sell respected
* [ ] No simultaneous long + short
* [ ] Rejected orders logged, no crash

**Exit:** automated execution engine working for Phase 1 path.

---

### Week 4 — Harden & Phase 1 completion

**Write (batch, then compile once)**

* Restart recovery: `OnInit` rebuild basket from open positions (magic + symbol)
* Equity halt behaviour verified (block new entries only; do not force-close unless already required by exit/SL)
* SL path verified when `SL_Points > 0`
* Logging schema complete: bar time, bands, side, basket id/side, reason, fill, spread, open count
* Remove leftover stubs / dead code from Weeks 1–2
* No new features

**Compile once → test**

* [ ] Compiles clean
* [ ] Restart with open positions: EA resumes same basket, no duplicate spam entries
* [ ] M5 Strategy Tester smoke run completes without init/runtime errors
* [ ] Manual checklist vs `concept.md` §8 all green
* [ ] `MaxLevels` still default 1; Phase 1.1 items still absent

**Exit — Phase 1 complete:** execution engine accepted; research backtests may begin. Grid depth / Phase 1.1 only after that.

---

## 7. Weekly cadence (how to work)

| Step | Action |
| --- | --- |
| Start of week | Read that week’s table; touch only those files |
| During week | Implement fully; do not MetaEditor-compile for “curiosity” |
| End of week | **One compile** → fix compile errors only → run checklist |
| Pass | Commit mental/note checkpoint; start next week |
| Fail | Stay on same week; fix checklist gaps only — no scope adds |

---

## 8. Definition of Phase 1 completion

All must be true:

* Matches locked entry/exit/risk rules in `concept.md` §8
* Single chart symbol/TF; hedging; fixed lot; market orders
* Basket rebuild on init; structured logs
* No out-of-scope modules or inputs beyond the locked list
* Week 4 checklist passed after a single final compile

**After completion (not this roadmap):** measure basket expectancy on M5 → optionally raise `MaxLevels` → then Phase 1.1 per `concept.md`.

---

## 9. Explicit non-goals reminder

Do not schedule, spike, or “quickly add”:

* Multi-level grid behaviour beyond default-1 plumbing
* Adaptive indicators, filters, sessions, AI
* Portfolio / multi-symbol
* Fancy risk models

The only product of this roadmap is the **Phase 1 automated execution engine**.
