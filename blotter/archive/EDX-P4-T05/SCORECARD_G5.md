# EDX-P4-T05 — G5 perturbation scorecard

**Scored:** 2026-09-25 ~11:17–11:21  
**Mode:** account currency · window 2025.01.01–2026.09.24  
**Champion ref:** EF 5.18 · E_N 0.185R · final $620.63 · Leak L1 ~2.2 pp  

## Load integrity

`.set` files on disk are correct, but **tester logs show magic≠intended params** (inputs shifted across runs). Scored by **actual** `Inp*` in each segment, not filename/magic.

| Magic in log | Actual tag | Notes |
| --- | --- | --- |
| 8210501 | BBDev−10 | set `a` was BBDev+10 |
| 8210502 | SL−10 | |
| 8210503 | — | **not run** |
| 8210504 | TP+10 | |
| 8210505 | TP−10 | |
| 8210506 | Risk+10 | |
| 8210507 | Risk−10 | |
| 8210508 | Risk−10 / no Inp block | duplicate-ish |

**Missing perturbations:** BBDev+10, SL+10.

## Results (by actual tag)

| Tag | n | WR | R | E_N | EF | Final | E_N>0 | EF>0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| BBDev−10 | 365 | 46.6% | 1.50 | +0.164 | **+4.37** | $577.95 | Y | Y |
| SL−10 | 461 | 45.3% | 1.67 | +0.209 | **+5.54** | $577.88 | Y | Y |
| TP+10 | 447 | 43.6% | 1.65 | +0.156 | **+3.81** | $585.54 | Y | Y |
| **TP−10** | 388 | 43.3% | 1.35 | +0.018 | **−1.60** | $559.57 | Y | **N** |
| Risk+10 | 448 | 48.9% | 1.50 | +0.222 | +6.68 | $587.35 | Y | Y |
| Risk−10 | 420 | 47.4% | 1.50 | +0.185 | +5.18 | $620.63 | Y | Y |
| BBDev+10 | — | — | — | — | — | — | — | **MISSING** |
| SL+10 | — | — | — | — | — | — | — | **MISSING** |

Cost ×1.5: already PASS from G4 MC-3 / EF proxy +4.07 > 0 (no new blotter required).

## Gate G5 criteria

```
E_N > 0 in ≥ 80% of perturbed runs
no single perturbation flips EF ≤ 0
EF > 0 at cost ×1.5
```

| Check | Result |
| --- | --- |
| Coverage | **6/8** material tags (75%) — incomplete |
| E_N > 0 | 6/6 scored (100% of available) |
| EF never ≤ 0 | **FAIL** — TP−10 EF = −1.60 pp |
| Cost ×1.5 | PASS (prior) |

## Verdict

**G5 FAIL** — TP−10 (`InpTP_Points=405`) flips EF negative (payoff compression: R 1.35, WR 43.3% ≈ BWR 42.6%, Leak eats margin).

Also incomplete: BBDev+10 and SL+10 never appeared in the log.

```
PRODUCTION-WORTHY = G0∧G1∧G2∧G3∧G4∧G5 → FAIL (G5)
```

Champion stack remains **G0–G4 PASS**; not production-worthy until G5 cleared (e.g. TP neighborhood / re-run missing arms with verified `.set` load).
