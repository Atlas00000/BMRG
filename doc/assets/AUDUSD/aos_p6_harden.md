# AUDUSD M15 — P6 hardening (L9 · L2 stress · geometry freeze)

**Version:** 1.0.0  
**Tasks:** AUDUSD-AOS-P6-T01 … T03  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/AUDUSD-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1 · armed preset [`AUDUSD_stack.set`](../../../Presets/AUDUSD_stack.set)  
**HITL:** AI challenger `L2skip_aud_m15_p_pretip_20261019_145303` SHADOW (not LIVE)

**Mode:** Policy + offline CF. No geometry change. Overlay champ **L2det LIVE_WITHHOLD** on research magic **8231941**.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — BUY∧Thu **ARM_SOFT** (already P2 alt) · blanket Thu/spread/H19 HOLD · keep L9 SHADOW |
| P6-T02 ±10% L2 stress | **PASS** — keep BUY∧May · SkipBuyThu=false · AI thr stress documented |
| P6-T03 geometry freeze | **PASS** — 300/300 · BB 2.2 · Start13 · skip Mon/Tue · ATR OFF on engine + **AUDUSD_stack** |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip spread nunique low → tercile soft veto weak → **DISARM** for LIVE.

| Policy | Tip verdict | Note |
| --- | --- | --- |
| **skip BUY∧Thu** | **ARM_SOFT** | Already P2 alt atom — optional; **off** on AUDUSD_stack |
| skip Thu (all) | HOLD_SHADOW | SELL / JunAug collateral |
| skip H19 / late | HOLD | Thin / weak on AUD tip |
| spread > tip p66 | HOLD / DISARM | Low variance |

**Wire:** No new L9 LIVE veto. Prefer L2det BUY∧May. `InpAOS_AUD_SkipBuyThu=false` on champion stack.

---

## 2. P6-T02 — L2 threshold stress

Baseline tip v1 BUY∧May: ARM_SOFT · ret **95.1%** · ΔE_N **+0.065**.

| Stress | Stance |
| --- | --- |
| BUY∧May ∨ BUY∧Thu | Wider calendar — document only; keep Thu **off** on stack |
| May all sides | Must stay HOLD/DISARM (collateral) |
| AI thr ±10% | Shadow store only — L2AI OFF in EA while det path armed |

Keep EA: `SkipBuyMay=true` · `SkipBuyThu=false`. Do not stress-test by changing SL/TP.

---

## 3. P6-T03 — Geometry freeze

| Preset | Geometry freeze |
| --- | --- |
| `AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` | OK |
| `BMRG-M15-AUDUSD-6M-P4_research_OS_W50.set` | OK |
| **`AUDUSD_stack.set`** | OK |

Declaration: `geometry_frozen=true` · ATR regime **OFF** (P8-T03) · OS gates/sizes only.

---

## 4. Armed champion stack — `AUDUSD_stack`

```text
Engine CHAMP geometry (8230901 freeze)
+ L2det_aud_m15_v1 LIVE_WITHHOLD   ← BUY ∧ May
+ L3 / L4 W50 / L6 ledger
+ L2 AI OFF (challenger SHADOW in store after HITL)
+ L9 soft veto NOT LIVE
Magic 8231941
```

| Path | File |
| --- | --- |
| Presets | `Presets/AUDUSD_stack.set` |
| Tester | `Profiles/Tester/BMRG/AUDUSD/AUDUSD_stack.set` |
| Doc copy | `doc/presets/AUDUSD_stack.set` |

**Compile** `BMRG.mq5` before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_8231941.csv`.  
**Do not** load on live M5 SCALE **8230931**.

---

## 5. Sign-off

P6 complete. Next: **P7** promotion packet / paper checklist. Measured Leak+swap still OPEN.
