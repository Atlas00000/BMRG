# L2skip_jp225 — model store

JP225 / JPN225 M15 L2 AI shadow artifacts. **Not** LIVE_WITHHOLD.

| Pointer | Role |
| --- | --- |
| `LATEST/` | Active shadow pin |
| `CHAMP.json` | AI champ (DISARM until P7) |
| `CHALLENGER.json` | AI challenger (EMPTY until gates) |
| `L2skip_jp225_p_pretip_<ts>/` | Immutable train runs |

**Overlay champ:** `L2det_jp225_v1_May_OR_Jul` (offline CF — no `AOS_L2det_jp225.mqh`).

```text
python infra/src/train/train_l2_jp225.py
python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py status
python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py drill
```

Policy: `doc/assets/JP225/aos_l5_retrain.md`
