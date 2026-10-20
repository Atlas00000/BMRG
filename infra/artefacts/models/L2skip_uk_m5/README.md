# L2skip_uk_m5 — UK100 M5 AI shadow store

**Overlay champ:** `L2det_uk_m5_v1b` (EA) — not this LR.  
**AI mode:** SHADOW_ONLY / DISARM until P7 HITL.  
**Policy:** `doc/assets/UK100/aos_l5_retrain_M5.md`

```text
python infra/src/train/train_l2_uk100_m5.py
python infra/artefacts/models/L2skip_uk_m5/rollback_l2skip_uk_m5.py status
python infra/artefacts/models/L2skip_uk_m5/rollback_l2skip_uk_m5.py drill
```

Do **not** reuse `L2skip_uk/` (M15) pins on M5.
