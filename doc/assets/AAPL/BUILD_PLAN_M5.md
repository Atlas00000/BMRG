# AAPL M5 AIOS — Build Plan (compile & test)

**Status:** Active research tooling · **pool candidate remains M15 Harvest** · M5 = tip WATCH  
**Engine lock:** [`AAPL_M5_AOS_BASELINE_v1.md`](./AAPL_M5_AOS_BASELINE_v1.md) · magic **26102011** · AOS OFF  
**Parent roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Score under:** [`edge_framework.md`](./edge_framework.md)  
**Sibling (M15):** [`BUILD_PLAN.md`](./BUILD_PLAN.md) — do not mix magics / L2det maps

> Converted from the Apple M5 enhancement thesis: gate the fade (Wed / H1 / Jul / fat-spread), protect May / Mon / tip BUY, measure Leak before Robust, elevate L8 for overnight gaps — never retune SL190/TP280 first, never arm M15 Thu/18 on M5.

---

## 1. Goal of this stream

Ship a **compileable** Apple **M5** AIOS path that:

1. Keeps Balanced M5 geometry frozen (**SL190 / TP280** · RR≈1.47).  
2. Adds **M5-native L2det** skips: **Wednesday** · **high-spread** · optional **H1 / Jul** SOFT (after tape CF).  
3. Runs **L3 + L4** observer/guard on Apple M5 without EUR/AUD/M15 L2 AI coeffs.  
4. Writes an **AOS ledger** CSV for shadow CF.  
5. Plans **L8** MAE/gap shadow after det stack.  
6. Does **not** invent entries, thin SL, or reuse `AOS_L2det_aapl.mqh` Thu/18 as the M5 map.

**P0 (docs) is done.** First code wire is **P2-T07**. Do not skip deal-Leak / P1 tape to chase L2 AI.

---

## 2. Code / artifact map

| Piece | Path | Role | Status |
| --- | --- | --- | --- |
| Engine preset | `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-Balanced_TPgtSL.set` | AOS OFF baseline | **EXISTS** |
| Baseline / bad-cells / cost | `doc/assets/AAPL/AAPL_M5_AOS_BASELINE_v1.md` · `aos_bad_cells_M5.md` · `aos_cost_policy_M5.md` | P0 stubs | **DONE** |
| L2det policy (M5) | `Include/AOS_L2det_aapl_m5.mqh` | Wed / spread / H1·Jul SOFT | **TO BUILD** (P2) |
| AOS router | `Include/AOS.mqh` | Route Apple **M5** → `aapl_m5` det; never INF/AUD; never M15 Thu/18 on M5 TF | **EXTEND** (P2) |
| Inputs | `Include/Config.mqh` | `InpAOS_AAPL_M5_*` toggles (separate from M15 `InpAOS_AAPL_*`) | **EXTEND** (P2) |
| P0 baseline `.set` copy | `…/AAPL-M5-AOS-P0-T01_baseline_Balanced.set` | Optional bookkeeping clone of engine | optional |
| P2 shadow | `…/AAPL-M5-AOS-P2-T02_L2det_shadow_Balanced.set` | AOS ON · SHADOW · magic **26162011** | **TO BUILD** |
| P2 live-withhold | `…/AAPL-M5-AOS-P2-T02_L2det_live_Balanced.set` | AOS ON · LIVE_WITHHOLD · magic **26162012** | **TO BUILD** |
| L2 AI pin | `infra/artefacts/models/L2skip_aapl_m5/` | Shadow · AUC≈0.501 DISARM | **DONE** P5 |
| Target arm | **`AAPL_5m_stack.set`** · magic **26162017** | P7 HITL research OS | **DONE** |

**Do not** enable `InpAOS_AAPL_L2detEnable` (M15 Thu/18) on M5 charts as a substitute for `AOS_L2det_aapl_m5.mqh`.

---

## 3. Build sequence (implementation order)

### Slice A — P0 complete (no compile required)

- [x] Baseline freeze  
- [x] Bad-cell registry  
- [x] Cost / Leak stub  
- [ ] Deal export → `Leak_source=measured` (preferred before P7; strongly preferred before Robust claims)

### Slice B — P1 offline (Python / CSV · no EA change required) — **DONE** 2026-10-20

1. [x] Tip / YTD / long fire tapes from Tester journal magic **26102011**.  
2. [x] Labels: win/lose · DOW · hour · side · ATR · BBw · overnight · spread · month · `regime_tag`.  
3. [x] `aos_l1_tape_contract_M5.md` + `blotter/archive/AAPL-M5-AOS-P1/` (builder · TAPE_QA · COST_PROXY · REVIEW).  
4. [ ] P1-T04 band-ride — deferred.

### Slice C — P2 compile wire (MetaEditor) — **DONE** 2026-10-20 (compile locally)

1. [x] `Include/AOS_L2det_aapl_m5.mqh` — v1b **Jul ∨ Wed** (H18/spread/H1 optional OFF).  
2. [x] `Config.mqh` — `InpAOS_AAPL_M5_*`.  
3. [x] `AOS.mqh` — Apple M5 path before M15 Thu/18.  
4. [x] Compile `BMRG.mq5` → **0 errors, 0 warnings** (2026-10-20).  
5. [x] Shadow **26162011** · live **26162012** presets.  
6. [x] Offline CF vs P0 tip → **ARM_SOFT** v1b (see `aos_l2_policy_M5.md`).

### Slice D — P3–P7

- [x] P3–P6 · **P7** HITL · **`AAPL_5m_stack`** · magic **26162017** (`AIOS_SIGNOFF_M5.md`)

Follow [`aios_roadmap_M5.md`](./aios_roadmap_M5.md). L8 remains primary upside after L2det for this equity CFD sleeve.

---

## 4. Compile steps (MetaEditor) — when Slice C starts

1. Open `Experts/BMRG/BMRG.mq5`.  
2. Compile (F7). Expect **0 errors**.  
3. Confirm `BMRG.ex5` timestamp updates.  
4. If include path fails, compile from the BMRG project folder.

---

## 5. Tester steps (Strategy Tester)

| Step | Action |
| --- | --- |
| 1 | Symbol **Apple** · TF **M5** · every tick · ACCOUNT CURRENCY · deposit ≥ 500 |
| 2 | Window: **2026.05.01 → 2026.10.19** (primary tip) · Jan→Oct = diagnostic only |
| 3 | Load engine / P0 preset → run → note final / n / WR (must match baseline ± noise) |
| 4 | Load **P2 shadow** → Journal `AOS SHADOW skip L2DET_AAPL_M5…` · ledger CSV |
| 5 | Optional **P2 live** → fewer Wed / high-spread (and armed H1/Jul) entries |
| 6 | Score E_N / EF / MaxDD / false-skip on May·Mon·BUY vs P0 under `edge_framework.md` |

**Inputs to confirm on P2 M5 presets (target)**

- Geometry still SL190 / TP280 / BBDev 2.5 / ATR 24–98 / BBw 0.30–2.00 / lot 1.0  
- `InpAOS_Enable=true`  
- `InpAiOsMode=1` (SHADOW) or `2` (LIVE_WITHHOLD)  
- `InpAOS_AAPL_M5_L2detEnable=true`  
- M15 `InpAOS_AAPL_L2detEnable=false` on M5 runs  
- `InpAOS_BWR=40.4` · `InpAOS_R=1.47` · `InpAOS_Leak=15.3` (proxy until measured)  
- Magic: engine `26102011` · shadow `26162011` · live `26162012`

---

## 6. Accept / reject (Slice C)

| Result | Verdict |
| --- | --- |
| Compiles; shadow logs M5 reason codes; engine still fires on SHADOW | **ACCEPT** slice |
| Live-withhold cuts bad cells; E_N/EF within loose bar vs P0 tip | **ACCEPT** L2det map (keep) |
| Live-withhold kills tip E_N or mass-skips May/Mon/BUY | **REJECT** map → disarm cell · do not retune SL/TP |
| Journal shows INF/AUD L2 proba or M15 Thu/18 reasons on M5 | **BUG** — M5 must stay on `aapl_m5` det-only until `L2skip_aapl_m5` exists |
| Claims Robust with Leak=2.1 meta | **REJECT** scoring — use measured or ~15.3 proxy |

---

## 7. What comes next (do not block P0)

| After | Roadmap |
| --- | --- |
| Deal Leak measured | Update `aos_cost_policy_M5.md` |
| Offline tape + labels | P1 |
| M5 L2det wire + CF | P2-T02…T07 |
| Train `L2skip_aapl_m5` | P2-T05 / **P5 DONE** (DISARM) |
| L8 MAE/gap shadow | P4-T04 **DONE** |
| Harden | **P6 DONE** |
| HITL / promote | **P7 DONE** · `AAPL_5m_stack` · **26162017** |

---

## 8. One-line

**Freeze Apple M5 Balanced → measure Leak → build M5-native L2det (Wed/spread/H1) + L8 gap path → shadow CF under edge_framework — no M15 Thu/18 transplant, no EUR model, no geometry change.**
