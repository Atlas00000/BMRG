# Harvest long fixture v1

**Source log:** `blotter/archive/EDX-POOL_WINDOWS/T04_Long_8210204.log`  
**Exits:** `blotter/archive/AOS-P4-T01/harvest_train_matrix.csv`  
**Built by:** `infra/src/ingest/mt5_normalise.py`  
**Recipe:** `INF-P2-T01` / `INF-P2-T04`

| File | Role |
| --- | --- |
| `ea_metadata.json` | Adapter metadata |
| `event_manifest.jsonl` | Declared 1R + equity_at_open + cost flags |
| `blotter_legs.jsonl` | Adapter legs |
| `quarantine.jsonl` | Unjoined / parse misses |
| `normalise_stats.json` | Coverage stats |
| `health_vector.json` | Stage 0–1 score (baseline Leak proxy) |
