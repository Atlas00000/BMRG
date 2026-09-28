We are building an MT5 Expert Advisor (EA) centred around the following trading concept and system architecture:
[# Bollinger Mean-Reversion Grid (BMRG)

EA Category: Mean Reversion | Adaptive Grid | Statistical Deviation

Primary objective: Monetise repeated price excursions away from a moving statistical mean through multiple entries, adaptive spacing, and systematic exits.

The BMRG is a suitable candidate for our individual MT5 EA research because its underlying hypothesis is straightforward to formalise, test, and progressively extend. The main challenge is distinguishing genuine mean-reverting conditions from markets that are transitioning into persistent trends.

For your account-flipping research, the focus should be on maximising trade opportunities and profit extraction, while measuring whether the mathematical edge survives transaction costs, adverse movement, and grid accumulation.

## 1. Mathematical foundation

The Bollinger Bands use a moving average and standard deviation:

MAt=1N∑i=0N−1Pt−iMA_t=\frac{1}{N}\sum_{i=0}^{N-1}P_{t-i}MAt=N1i=0∑N−1Pt−i

Uppert=MAt+kσtUpper_t=MA_t+k\sigma_tUppert=MAt+kσt

Lowert=MAt−kσtLower_t=MA_t-k\sigma_tLowert=MAt−kσt

Where:

* NNN = moving-average period.

* kkk = standard-deviation multiplier.

* σt\sigma_tσt = rolling price standard deviation.

The grid extends this concept by placing multiple entry levels around the mean.

σ=N1∑i=1N(xi−μ)2

The points have mean μ = 5 and σ = 1.5.

σ\sigmaσ

σ\sigmaσ

Adjust the population standard deviation to spread the points out or pull them toward the mean. You can also drag each point in the graph.

Drag points

μ − σμ + σμ0246810

Give feedback

A simple structure could use:

|
Level

|

Long Side

|

Short Side

|
| --- | --- | --- |
|

1

|

−1.0σ

|

+1.0σ

|
|

2

|

−1.5σ

|

+1.5σ

|
|

3

|

−2.0σ

|

+2.0σ

|
|

4

|

−2.5σ

|

+2.5σ

|
|

5

|

−3.0σ

|

+3.0σ

|

These are candidate grid levels, not guaranteed entry points. The EA needs to define whether it uses market orders, pending limits, or confirmation after the deviation.


## 2. Recommended trading strategy configurations

Rather than building a single BMRG, I recommend developing several variants that test different hypotheses.

|
Strategy

|

Indicators

|

Entry conditions

|

Exit structure

|

Theoretical edge

|
| --- | --- | --- | --- | --- |
|

BMRG-A: Pure Deviation Fade

|

SMA20 + σ20

|

Price reaches ±2σ

|

Mean or partial retracement

|

Statistical deviation

|
|

BMRG-B: Multi-Level Accumulation

|

SMA20 + σ20

|

Price reaches successive bands

|

Basket mean / weighted TP

|

Monetises deeper excursions

|
|

BMRG-C: RSI-Confirmed Fade

|

BB20,2 + RSI14

|

±2σ + RSI extreme

|

Mean or opposite band

|

Combined deviation and exhaustion

|
|

BMRG-D: ATR-Adaptive Grid

|

SMA20 + ATR14 + BB

|

Deviation scaled by ATR

|

Dynamic volatility target

|

Volatility-normalised entries

|
|

BMRG-E: VWAP-Bollinger Grid

|

Session VWAP + σ

|

Deviation from VWAP

|

VWAP / partial exits

|

Intraday fair-value reversion

|
|

BMRG-F: Trend-Filtered MR

|

EMA50 + BB20

|

Price extreme + weak trend

|

Mean / protective exit

|

Avoids some trending conditions

|
|

BMRG-G: Volatility-Regime Grid

|

BB20 + ATR percentile

|

Entry according to volatility regime

|

Regime-specific exit

|

Adaptive market conditions

|
|

BMRG-H: Z-Score Velocity Grid

|

Rolling Z-score + ΔZ

|

Extreme Z + reversal in Z

|

Mean / time-based exit

|

Reversion acceleration

|
|

BMRG-I: Asymmetric Grid

|

BB + ATR + directional volatility

|

Separate upper/lower spacing

|

Basket mean

|

Directional volatility asymmetry

|
|

BMRG-J: Rebuild Grid

|

BB + ATR

|

New-bar deviation

|

Re-anchor around new mean

|

Dynamic grid positioning

|

### Recommended initial baseline

BMRG-A: Pure Deviation Fade

* BB period: 20

* Standard deviation: 2.0

* Entry: deviation reaches a predefined band.

* Positioning: independent long and short signal logic.

* Exit: return toward the moving average.

* Re-entry: configurable cooldown or new signal.

* Grid: initially one entry per side, then extend to multiple levels.

This establishes a reference strategy. We can then compare the effect of grid depth, adaptive spacing, and entry confirmation against it.

## 3. Trading edge in theory

The theoretical edge is conditional mean reversion.

The assumption is that, under specific market conditions, price deviations from its recent equilibrium are partially reversed.

However, touching a Bollinger Band does not prove that price will revert. A band measures relative deviation and volatility; it is not a standalone probability of reversal. John Bollinger describes the bands as a way to assess whether prices are relatively high or low, with additional tools potentially providing confirmation.

![](https://www.google.com/s2/favicons?domain=https://www.bollingerbands.com\&sz=32)

bollingerbands

+1

A simplified expectancy model:

E=pW−(1−p)L−CE=pW-(1-p)L-CE=pW−(1−p)L−C

Where:

* ppp = probability of a profitable basket.

* WWW = average gross winning basket.

* LLL = average gross losing basket.

* CCC = transaction costs and other friction.

For a grid, the calculation must be done at the basket level, including all accumulated entries, not just individual winning trades.

Research on mean-reverting markets highlights the importance of transaction costs, and research on rebalancing similarly shows that trading friction can materially affect outcomes.

![](https://www.google.com/s2/favicons?domain=https://www.sciencedirect.com\&sz=32)

ScienceDirect

+1

## 4. Timeframe and trading frequency

For our MT5 research, I would test the following configurations:

|
Timeframe

|

Role

|

Frequency target

|
| --- | --- | --- |
|

M1

|

Ultra-short-term grid

|

High, dependent on volatility

|
|

M5

|

Primary initial research

|

Moderate to high

|
|

M15

|

Confirmation / slower grid

|

Moderate

|
|

M30

|

Regime comparison

|

Lower

|
|

H1

|

Wider deviations

|

Low to moderate

|

Recommended starting point: M5.

This provides a useful compromise for testing intraday deviations without making the EA entirely dependent on tick-level microstructure.

Frequency should be measured rather than forced:

* Signals per day.

* Filled entries per basket.

* Average basket duration.

* Re-entry frequency.

* Percentage of time with open exposure.

* Gross and net profit per completed basket.

A grid that generates more entries but lower net expectancy is not necessarily extracting more profit.

## 5. Lot size and position scaling

Since you want aggressive systems, we can test multiple sizing models, but lot size should remain an explicit experimental parameter rather than an arbitrary fixed value.

|
Model

|

Implementation

|
| --- | --- |
|

Fixed lot

|

Every entry uses the same lot size

|
|

Linear grid scaling

|

1×, 2×, 3×, 4×

|
|

Anti-martingale

|

Increase size after profitable baskets

|
|

Volatility-scaled

|

Reduce size as ATR rises

|
|

Basket-budget sizing

|

Allocate a defined maximum margin/notional budget

|
|

Equity-scaled

|

Lot size changes with account equity

|

For the first baseline EA, I recommend fixed micro-lot sizing with configurable basket limits. This isolates the strategy's entry/exit behaviour before adding aggressive scaling.

For research purposes, compare fixed sizing against linear and anti-martingale scaling independently. A martingale multiplier should not be considered evidence of edge creation; it changes the distribution of outcomes and exposure.

## 6. Strengths and weaknesses

### Strengths

* Simple mathematical formulation.

* Adaptive volatility bands.

* Easy to implement in MT5.

* Multiple entry levels can monetise repeated deviations.

* Suitable for bi-directional signal logic.

* Can be extended with OU, Kalman, VWAP, and regime filters.

* Clear separation between signal, grid, basket, and execution modules.

### Weaknesses

* Strong trends can produce prolonged band riding.

* Standard deviation expands during shocks, potentially delaying entries.

* The moving mean can shift before price returns.

* Multiple entries increase exposure and transaction costs.

* High win rates can coexist with large losing baskets.

* Fixed grid spacing becomes inappropriate when volatility changes.

## 7. Individual EA implementation plan

For the first BMRG, use the following structure:

```
BMRG/
├── BMRG.mq5                 // lifecycle only: OnInit / OnTick / OnDeinit / OnTradeTransaction
└── Include/
    ├── Config.mqh           // inputs + validation
    ├── Indicators.mqh       // BB (SMA + σ) handles
    ├── Signal.mqh           // entry / exit from closed bar
    ├── Grid.mqh             // level map + free levels
    ├── Basket.mqh           // positions grouped as one basket
    ├── Risk.mqh             // lot, max trades, spread, cooldown, equity halt
    ├── Execution.mqh        // validate → OrderSend wrappers
    ├── State.mqh            // runtime state; rebuild on restart
    └── Logger.mqh           // structured Print / Comment
```

Tick workflow: new bar? → refresh indicators → update basket state → risk gates → evaluate signal → place/close → log.

### Phase 1

* BMRG-A Pure Deviation Fade (baseline).
* SMA20 + standard deviation (k = 2.0).
* Closed-bar signals using shift 1.
* Market orders only (no pendings).
* Symmetric upper/lower logic; `MaxLevels` input with default = 1 (single fade first).
* Fixed lot size only.
* One symbol / current chart / one EA instance per chart.
* Basket tracking by magic + symbol.
* Configurable maximum entries.
* Explicit execution logs.

### Phase 1.1 (deferred)

* ATR-adaptive spacing (BMRG-D).
* RSI confirmation.
* Trend filter.
* Dynamic re-anchoring.
* Volatility regime detection (BMRG-G).
* Anti-martingale / risk-% / R:R / ATR stops.
* Expanded basket exit logic (partial, opposite band, time stop variants).

Preferred progression: BMRG-A → BMRG-D (ATR-adaptive) → BMRG-G (volatility-regime).

---

## 8. Phase 1 locked decisions (gaps filled)

These rules are frozen for the first build. Do not re-open them until the baseline has been backtested on M5 with fixed lots.

### Entry

* Closed bar (shift 1) closes beyond ±2σ → market entry.
* Long when close ≤ lower band; short when close ≥ upper band.
* No pending orders in Phase 1.

### Exit

* Closed bar touches/crosses the SMA (middle band) → close that side’s basket.
* Optional hard abort: fixed SL in points (`SL_Points`; 0 = off).
* No TP / R:R / ATR exits in Phase 1.

### Grid depth

* Product remains a grid, but Phase 1 default is **1 level per side**.
* Keep `MaxLevels` configurable; raise only after single-fade expectancy is measured.
* Spacing (when MaxLevels > 1): successive σ steps (e.g. 2.0, 2.5, 3.0…).

### Direction / sides

* `AllowBuy` / `AllowSell` permissions.
* **One direction at a time** — no simultaneous long + short baskets.
* New opposite signal while a basket is open: ignore (or flatten only via exit rule / SL / equity halt).

### Basket / account

* Basket = all open positions with this EA’s magic number on the chart symbol.
* **Hedging account required**; netting is unsupported in Phase 1 (document and refuse init if netting).
* On `OnInit`: rebuild basket state from open positions by magic + symbol.

### Flatten / abort rules

* Max entries per basket (`MaxEntries`).
* Max simultaneous open trades (same cap or separate input).
* Max spread filter + slippage + cooldown bars between new entries.
* Equity halt: stop new entries if account drawdown from session/start equity exceeds X%.
* Basket age / MAE abort: deferred to Phase 1.1 unless needed during testing.

### Risk in Phase 1 (minimal)

* Fixed lot only.
* Max spread, slippage, cooldown, magic, max entries.
* Optional fixed SL (points).
* Equity halt for new entries.
* **Out of scope for Phase 1:** risk-% sizing, ATR stops, take-profit, R:R, anti-martingale.

### Locked inputs

| Input | Default | Notes |
| --- | --- | --- |
| `BBPeriod` | 20 | SMA / σ lookback |
| `BBDev` | 2.0 | Entry band multiplier |
| `Lot` | micro (e.g. 0.01) | Fixed only |
| `MaxLevels` | 1 | Raise after baseline |
| `MaxEntries` | 1 | Cap fills per basket |
| `MaxSpread` | symbol-dependent | Points / points equivalent |
| `Slippage` | broker-dependent | |
| `CooldownBars` | configurable | Bars between new entries |
| `Magic` | unique | Basket identity |
| `SL_Points` | 0 | 0 = disabled |
| `EquityHaltPct` | configurable | Stop new entries |
| `AllowBuy` | true | |
| `AllowSell` | true | |

### Symbol / execution constraints

* Respect stops level, freeze level, lot step / min / max, and filling mode before `OrderSend`.
* Validate every order; fail closed (log + skip) on rejection.

### Logging schema (research)

Log at least: bar time, upper / mid / lower, signal side, basket id, entry or exit reason, fill price, spread, open count, costs where available.

### Scope rules

* Build the configurable execution foundation first — not strategy perfection.
* Do **not** add: advanced filters, AI, session filters, portfolio / multi-symbol, adaptive optimisation, or Phase 1.1 features.
* Keep modules separated (signal / execution / risk) so multi-symbol can come later without a rewrite.

### Build order

1. Implement against this locked spec only.
2. Backtest M5, fixed lots → measure **basket-level** expectancy (gross/net, fills, duration, exposure).
3. Then raise `MaxLevels` / `MaxEntries`.
4. Then Phase 1.1: ATR spacing, RSI, trend filter, richer exits.
