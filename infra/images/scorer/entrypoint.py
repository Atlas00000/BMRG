"""Scorer image entrypoint: score harvest fixture pack."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/infra/src/score")))
sys.path.insert(0, str(Path("/infra/src/ingest")))
from health import score_pack_dir  # noqa: E402

r = score_pack_dir(Path("/infra/fixtures/blotter/harvest_long_v1"))
print(json.dumps({"verdict": r["verdict"], "ef": r["health_vector"]["ef_pp"]}))
