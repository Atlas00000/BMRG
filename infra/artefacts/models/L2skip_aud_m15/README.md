# L2skip_aud_m15 model store

AUDUSD **M15**-native avoid-loser LR artefacts. **Not** live M5 `L2skip_aud/` · **not** EUR / UK100 / AAPL pins.

| Pointer | Meaning |
| --- | --- |
| `CHAMP.json` | AI champ for LIVE_WITHHOLD — currently **DISARM** |
| `CHALLENGER.json` | Shadow candidate under review — **EMPTY** until HITL |
| `LATEST/` | Last train shadow pin |
| Overlay | **`L2det_aud_m15_v1`** in EA (BUY∧May) |

Policy: [`doc/assets/AUDUSD/aos_l5_retrain.md`](../../../../doc/assets/AUDUSD/aos_l5_retrain.md)

```text
python infra/src/train/train_l2_audusd_m15.py
python infra/artefacts/models/L2skip_aud_m15/rollback_l2skip_aud_m15.py status
python infra/artefacts/models/L2skip_aud_m15/rollback_l2skip_aud_m15.py drill
```
