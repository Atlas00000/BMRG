# L2skip_usdjpy — model store

USDJPY M15 avoid-loser shadow store. **Not** LIVE_WITHHOLD.

| Pointer | Role |
| --- | --- |
| `LATEST/` | Active SHADOW_ONLY pin |
| `CHAMP.json` | AI champ (null / DISARM until P7) |
| `CHALLENGER.json` | AI challenger (EMPTY until HITL) |
| `L2skip_usdjpy_p_pretip_*` | Immutable train runs |
| `rollback_l2skip_usdjpy.py` | Pin control + P5 drill |

**Overlay champ:** `L2det_usdjpy_v1c_near_atr_OR_H16` (offline CF — no MQH yet).  
**Policy:** `doc/assets/USDJPY/aos_l5_retrain.md`  
**Train:** `python infra/src/train/train_l2_usdjpy.py`
