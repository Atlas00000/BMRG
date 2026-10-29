# LIVE-20261028 — VPS EA health check

**task_id:** LIVE-20261028  
**as_of:** 2026-10-28T22:43+01:00 · account `28435` · hosting `6917926`  
**sources:** `logs/hosting.6917926.{experts,terminal}/20261022–20261028.log`  
**verdict:** **DEGRADED — 3-day outage (Oct 26–28), recovered 22:42 Oct 28**

## Outage

| Time | Event |
| --- | --- |
| Sat 24 Oct 14:51:29 | VPS terminal restart (hosting), 7 EAs loaded |
| 14:51:37.946 | All 7 → `[ERROR] Init refused: Hedging account required (netting unsupported)` → init code 1 → removed |
| 14:51:38.065 | Terminal sync with broker completes (account **is** hedging) |
| 24 Oct → 28 Oct 22:41 | `7 charts, 0 EAs` — **Mon 26, Tue 27, Wed 28 sessions not traded** |
| 28 Oct 22:42:21 | Redeploy · all 7 `init OK` |

**Root cause:** `ConfigIsHedgingAccount()` (`Include/Config.mqh`) reads `ACCOUNT_MARGIN_MODE` in `OnInit` before the account is synchronized → default ≠ hedging → hard `INIT_FAILED`. Race recurs on any hosting restart.

## Positions during outage (broker-side SL/TP only)

| Sleeve | Opened | Result |
| --- | --- | --- |
| EURUSD SELL 0.01 @ 1.12071 | 23 Oct 14:55 | TP 1.11771 · 26 Oct 14:58 · +1R |
| AUDUSD SELL 0.01 @ 0.70303 | 23 Oct 15:55 | SL 0.70603 · 28 Oct 21:00 · −1R |

Both closes happened with no EA attached → not in AOS ring/ledger.

## Live activity before outage (Oct 22–23)

| Sleeve | Closes |
| --- | --- |
| UK100 | SL, SL (22) · SL (23) → `Failure pause loss streak=3` |
| DE30 | SL (22) |
| JPN225 | TP (23, 0.3 lot, +2R) |
| EURUSD / AUDUSD | TP (22) each |

Oct 22: account daily-loss halt ON across UK100/DE30/AUDUSD/JPN225/USDJPY after UK+DE SL cluster.

## Current posture (22:42 init)

| Symbol | TF | Magic | Risk | Note |
| --- | --- | ---: | ---: | --- |
| EURUSD | M5 | 8210204 | 0.5% | OK |
| AUDUSD | M5 | **8230931** | **3.0%** | Since 21 Oct 18:14 — conflicts GRP-P5 `ft_twin_only` @0.5% (8230921) |
| Apple | M5 | 26162017 | lotMode=0 lot=1.00 | Fixed lot (unchanged since 20 Oct) |
| UK100 | M5 | 26121907 | 0.5% | Still L3v1c (1.25); GRP-P5 says off pending halt review |
| JPN225 | M5 | 26161907 | 0.5% | OK |
| DE30 | M5 | 26151907 | 0.5% | OK |
| USDJPY | M15 | 26131807 | 0.5% | OK |

VPS binary = **1.25** (AOS line has no `haltMaxBars`); local `BMRG.ex5` 22 Oct 16:36 predates 1.26 source.

## Structural flag

AOS ring is in-memory and the ledger opens with `FILE_WRITE` (truncate) → every restart resets L3/L4 history (`n=1..3` after redeploys). With restarts on 20, 21, 24, 28 Oct, W50/W250 never fills — L3 halt is effectively inert live.

## Fix shipped — EA 1.27 (compiled 2026-10-28 22:57, 0 errors / 0 warnings)

- `ConfigValidate` no longer checks margin mode → `OnInit` cannot fail on a pre-sync read.
- New `ConfigAccountModeOK()` gate at top of `OnTick`: waits for connection + login, rechecks every tick until hedging confirmed (logs `Account check OK: hedging`). A real netting account still never trades (one WARN line, EA stays attached).
- **Note:** 1.27 also carries the uncompiled-until-now 1.26 L3v1d changes (BELOW streak on closes only + `InpAOS_L3_BelowHaltMaxBars=500` default) for **all** L3 sleeves. Not yet tip-CF'd.

## Actions

1. ~~Fix init race~~ — done in 1.27; **migrated 23:00:00** · 7/7 `init OK` · `haltMaxBars=500` in AOS line confirms 1.27 · `Account check OK: hedging` on 6/7 (Apple pending first tick — US cash closed).
2. Confirm AUDUSD 8230931 @3% is intended vs P5 attach policy.
3. Decide UK100 posture (attached despite P5 `off_pending_halt_review`).
4. Consider AOS ring rehydrate from deal history / append-mode ledger.
