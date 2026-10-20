# L2skip_de40 — model store

DE40 / DE30 M15 L2 AI shadow artifacts. **Not** LIVE_WITHHOLD.

| Pointer | Role |
| --- | --- |
| `LATEST/` | Active shadow pin |
| `CHAMP.json` | AI champ (DISARM until P7) |
| `CHALLENGER.json` | AI challenger (EMPTY until gates) |
| `L2skip_de40_p_pretip_<ts>/` | Immutable train runs |

**Overlay champ:** `L2det_de40_v1_BUY_near_atr` (offline CF — no `AOS_L2det_de.mqh` yet).

```text
python infra/src/train/train_l2_de40.py
python infra/artefacts/models/L2skip_de40/rollback_l2skip_de40.py status
python infra/artefacts/models/L2skip_de40/rollback_l2skip_de40.py drill
```

Policy: `doc/assets/DE40/aos_l5_retrain.md`
