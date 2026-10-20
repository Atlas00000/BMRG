# AAPL AIOS — Build Plan (compile & test)

**Status:** Optional research tooling · **candidate remains P0 / Harvest baseline**  
**Candidate lock:** [`candidate_pool.md`](./candidate_pool.md) · magic **26092501** · AOS OFF  
**Parent roadmap:** [`aios_roadmap.md`](./aios_roadmap.md)  
**Score under:** [`edge_framework.md`](./edge_framework.md)  
**Sibling (M5):** [`BUILD_PLAN_M5.md`](./BUILD_PLAN_M5.md) · [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) — separate L2det pin

> For now, Apple’s book candidate is the **baseline Harvest** preset. P2 L2det shadow/live presets are experiments only — do not treat them as the candidate. Do **not** run M15 Thu/18 L2det as a substitute on M5 charts.

This is the **implementation plan** converted from the weekly roadmap into something you can compile in MetaEditor and run in Strategy Tester.

---

## 1. Goal of this slice

Ship a **compileable** Apple AIOS path that:

1. Keeps Harvest geometry frozen (SL300/TP375).  
2. Adds **L2det** skips: **Thursday** · **hour 18** (server time).  
3. Runs **L3 + L4** observer/guard on Apple without calling EUR/AUD L2 AI coeffs.  
4. Writes an **AOS ledger** CSV for shadow CF.  
5. Does **not** invent entries or change SL/TP.

Later weeks (tape / `L2skip_aapl` train) stay on the roadmap — not required to compile this slice.

---

## 2. Code / artifact map

| Piece | Path | Role |
| --- | --- | --- |
| L2det policy | `Include/AOS_L2det_aapl.mqh` | Thu / hour-18 skip decisions |
| AOS router | `Include/AOS.mqh` | `AOSIsApple()` · det before AI · **no INF/AUD model on Apple** |
| Inputs | `Include/Config.mqh` | `InpAOS_AAPL_*` toggles |
| Baseline preset | `Profiles/Tester/BMRG/AAPL/AAPL-AOS-P0-T01_baseline_Harvest.set` | Engine-only |
| Shadow preset | `Profiles/Tester/BMRG/AAPL/AAPL-AOS-P2-T02_L2det_ThuHour18_shadow_Harvest.set` | AOS ON · SHADOW |
| Live-withhold preset | `Profiles/Tester/BMRG/AAPL/AAPL-AOS-P2-T02_L2det_ThuHour18_live_Harvest.set` | AOS ON · LIVE_WITHHOLD |

---

## 3. Compile steps (MetaEditor)

1. Open `Experts/BMRG/BMRG.mq5`.  
2. Compile (F7). Expect **0 errors**.  
3. Confirm `BMRG.ex5` timestamp updates.  
4. If include path fails, compile from the BMRG project / same folder (includes are relative `Include/`).

---

## 4. Tester steps (Strategy Tester)

| Step | Action |
| --- | --- |
| 1 | Symbol **Apple** · TF **M15** · model every tick · ACCOUNT CURRENCY · deposit ≥ 500 |
| 2 | Window: **2025.01.01 → 2026.08.31** (primary) or **2020.01.01 → 2026.08.31** (extensive) |
| 3 | Load **P0** preset → run → note final balance / trades (baseline) |
| 4 | Load **P2 shadow** preset → run → check Journal for `AOS SHADOW skip L2DET_AAPL…` and ledger `COMMON\Files\BMRG_AOS_ledger_<magic>.csv` |
| 5 | Optional: **P2 live** preset → expect fewer Thu / hour-18 entries vs baseline |
| 6 | Compare: E_N / WR / MaxDD vs P0 under `edge_framework.md` loose bar (EF hold −1 pp, MaxDD +2 pp) |

**Inputs to confirm on P2 presets**

- `InpAOS_Enable=true`  
- `InpAiKillSwitch=false`  
- `InpAiOsMode=1` (SHADOW) or `2` (LIVE_WITHHOLD)  
- `InpAOS_AAPL_L2detEnable=true`  
- `InpAOS_AAPL_SkipThu=true` · `InpAOS_AAPL_SkipHour18=true`  
- `InpAOS_W250=50` (Apple n is small; L4/L3 can arm)  
- `InpAOS_BWR=44.4` · `InpAOS_R=1.25` · `InpAOS_Leak=9.0` (true-leak proxy)  
- Magic: baseline `26092501` · shadow `26101221` · live `26101222`

---

## 5. Accept / reject (this slice)

| Result | Verdict |
| --- | --- |
| Compiles; shadow logs skips; engine still fires on SHADOW | **ACCEPT** slice |
| Live-withhold cuts Thu/18; E_N/EF within loose bar vs P0 | **ACCEPT** L2det map (keep) |
| Live-withhold kills tip/long E_N | **REJECT** map → disarm hour-18 or Thu · do not retune SL/TP |
| Journal shows INF/AUD L2 proba on Apple | **BUG** — Apple must stay det-only until `L2skip_aapl` exists |

---

## 6. What comes next (do not block compile)

| After this slice | Roadmap |
| --- | --- |
| Offline tape + labels | P1 |
| Train `L2skip_aapl` | P2-T05 |
| Full det+L3+L4 stack CF | P4 |

---

## 7. One-line

**Compile BMRG → Tester Apple M15 → P0 baseline vs P2 L2det shadow/live presets → score skips under edge_framework — no EUR model, no geometry change.**
