# LIVE-20261005 — VPS day review

**task_id:** LIVE-20261005  
**window:** 2026-10-05 (Mon) broker day · magic 8210204 · EURUSD M5  
**preset:** INF-LIVE_WITHHOLD_Harvest_long_ddl30 (session 12–20 server, AOS LIVE_WITHHOLD)  
**verdict:** ACCEPT — healthy day; 1/1 fill hit full TP  
**archived_at:** 2026-10-06T12:44:49+01:00  
**sources:** hosting.6917926.experts/{20261005,20261006}.log · terminal same dates

## Scorecard

| Metric | Value |
| --- | --- |
| Closed trades | 1 |
| Wins / losses | 1 / 0 |
| Win rate | 100% |
| Gross (price) | +300 pts (TP full) |
| Est. P&L (0.01 EURUSD) | ~+$3 before swap/commission |
| Hold | ~11.5h (overnight) |
| Signals (enter L0) | 11 |
| In-session signals (server 12–20) | 1 → filled |
| Outside-session signals | 10 → blocked (silent; LogGateBlocks=false) |
| halt=1 / pause=1 bars | 0 / 0 |
| Entry failed / rejected | 0 |
| AOS L3 halt | none observed |

## Trade blotter

| Side | Open (hosting / ~server) | Close (hosting / ~server) | Entry | Exit | SL / TP | Result |
| --- | --- | --- | --- | --- | --- | --- |
| BUY 0.01 | 15:35 / bar 13:30 server | 03:00:27 next day / ~01:00 server | 1.11973 | 1.12273 (TP) | 1.11673 / 1.12273 | TP win |

Deal tickets: open #7583399 · close #7589845 (terminal).  
EA: `[BMRG][TRADE] OPEN BUY` then `AOS close TP | n=1 life=Stable f=0.75`.

## Ops notes

- EA flat and clean all morning; first in-session BB buy at server 13:30 filled immediately (AOS did not withhold).
- Position rode overnight; TP filled at 1.12273 early Mon 6 Oct hosting time.
- No equity/daily-loss halt; spreads at fill ~7 pts (under max 30).
