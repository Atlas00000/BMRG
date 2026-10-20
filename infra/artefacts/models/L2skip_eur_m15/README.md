# L2skip_eur_m15 model store

EURUSD **M15**-native avoid-loser LR artefacts. **Not** M5 / AUD / UK100 / AAPL pins.

| Pointer | Meaning |
| --- | --- |
| `CHAMP.json` | AI champ for LIVE_WITHHOLD — currently **DISARM** |
| `CHALLENGER.json` | Shadow candidate under review — **EMPTY** |
| `LATEST/` | Last train shadow pin |
| Overlay | **`L2det_eur_m15_v1b`** in EA (separate from this store) |

Policy: [`doc/assets/EURUSD/aos_l5_retrain.md`](../../../../doc/assets/EURUSD/aos_l5_retrain.md)

```text
python infra/src/train/train_l2_eurusd_m15.py
python infra/artefacts/models/L2skip_eur_m15/rollback_l2skip_eur_m15.py status
python infra/artefacts/models/L2skip_eur_m15/rollback_l2skip_eur_m15.py drill
```
