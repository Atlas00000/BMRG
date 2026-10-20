# L2skip_uk model store

UK100-native avoid-loser LR artefacts. **Not** EUR/AUD/AAPL pins.

| Pointer | Meaning |
| --- | --- |
| `CHAMP.json` | AI champ for LIVE_WITHHOLD — currently **DISARM** |
| `CHALLENGER.json` | Shadow candidate under review — **EMPTY** |
| `LATEST/` | Last train shadow pin |
| Overlay | **`L2det_uk_v1b`** in EA (separate from this store) |

Policy: [`doc/assets/UK100/aos_l5_retrain.md`](../../../../doc/assets/UK100/aos_l5_retrain.md)

```text
python infra/src/train/train_l2_uk100.py
python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py status
python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py drill
```
