# LIVE-20261029 — VPS EA health check

**task_id:** LIVE-20261029  
**as_of:** 2026-10-29T15:34+01:00 · account `28435` · hosting `6917926` · EA **1.27**  
**sources:** `logs/hosting.6917926.{experts,terminal}/20261029.log` (+ 20261028 init dump)  
**verdict:** **HEALTHY — 7/7 running, no restarts, no errors; 0 trades today (gated)**

## Terminal

- `7 charts, 7 EAs` every hourly heartbeat 00:00 → 15:00 · ping ~1.21 ms · no reconnects / restarts since 1.27 migration (28 Oct 23:00).
- No `Trades` lines today · 0 open positions.

## Per sleeve (bars processed through server 14:25)

| Sleeve | Bars | Signals | Logged blocks | Notes |
| --- | ---: | ---: | --- | --- |
| EURUSD | 187 | 17 | — (block logging off) | 5 signals inside 12–20 session, none taken — reason not logged |
| AUDUSD | 187 | 19 | — (block logging off) | All in-session-relevant signals before 13:00 start |
| UK100 | 187 | 16 | outside session 9 · ATR > 869 ×7 | High-vol day (ATR ~1272) |
| DE30 | 187 | 6 | outside session 4 · `L2DET_SKIP_BUY_OCT` 1 · ATR 1 | |
| JPN225 | 187 | 4 | outside session 3 · ATR 1 | |
| USDJPY (M15) | 63 | 5 | outside session 5 | |
| Apple | 13 | 2 | outside session 2 | `Account check OK: hedging` 14:30 (first US tick) |

`halt=0 pause=0` on every sleeve's last bar. No WARN/ERROR lines today.

## 1.27 fix status

`Account check OK: hedging` now confirmed on **7/7** (Apple at US open). Init race closed.

## EURUSD investigation — 5 in-session signals not taken

**Cause: L2 INF AI withhold** (`L2skip_inf_p92_20260927_223519`, LIVE_WITHHOLD, skip if p ≥ 0.606). EUR L2det is off, so the FX AI path runs; block logging off hid it.

Offline replay with baked coeffs + logged spreads:

| Bar (server) | Side | spread | p(lose) | Decision |
| --- | --- | ---: | ---: | --- |
| 12:00 | BUY | 6 | 0.635 | SKIP |
| 12:55 | BUY | 7 | 0.643+ | SKIP |
| 13:00 | BUY | 6 | 0.643 | SKIP |
| 13:15 | BUY | 7 | 0.643+ | SKIP |
| 14:20 | SELL | 7 | 0.656+ | SKIP |
| Oct 23 14:55 (traded) | SELL | 6 | 0.599 | fired (uncertain band) |

**Why now:** model's largest drivers are calendar numerics — `month` (linear, coef +0.15/σ), week-of-month (+0.12/σ) — plus `spread_hi` (spread ≥ 6, +0.17/σ). Live in-session spread is mostly 6–7, so spread_hi is almost always on.

Session skip rate (12–20, both sides) at spread 6: Jan–May ~0% · Jul 14% · Sep 32% · **Oct 41% · Nov 51% · Dec 67%**; at spread 5 near 0% until Dec. Late-month weeks (wom 4–5) in Oct are skipped **100%**; Nov week 1 fires fully.

Read: working as coded, but the withhold is driven by a linear month trend + a 1-point spread flip → calendar overfit, and it will increasingly starve EURUSD into year-end.

Options: (a) keep; (b) temporarily SHADOW (`InpAiOsMode=1`) for EUR; (c) retrain without numeric month/wom (or month as categorical) and recheck spread_hi; (d) at minimum `InpLogGateBlocks=true` on EUR/AUD.

## Flags (carried)

1. EURUSD / AUDUSD presets have `InpLogGateBlocks=false` → in-session signal rejections are invisible.
2. AUDUSD still `8230931` @ 3% (vs P5 `ft_twin_only` @ 0.5%).
3. UK100 attached despite P5 `off_pending_halt_review`.
4. AOS ring resets on restart (L3/L4 windows start empty after 28 Oct redeploys).
