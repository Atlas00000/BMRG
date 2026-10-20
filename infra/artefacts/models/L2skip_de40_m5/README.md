# L2skip_de40_m5

DE40/DE30 **M5** avoid-loser shadow store. Overlay champ is **`L2det_de40_m5_v1b`** (EA), not this LR.

- Train: `python infra/src/train/train_l2_de40_m5.py`
- Rollback: `python infra/artefacts/models/L2skip_de40_m5/rollback_l2skip_de40_m5.py …`
- Policy: `doc/assets/DE40/aos_l5_retrain_M5.md`

Do **not** merge with M15 `L2skip_de40/` or foreign asset pins.
