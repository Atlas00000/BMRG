"""Validate adapter contract payloads against INF-P1 JSON Schemas."""
from __future__ import annotations

import json
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pip install jsonschema") from exc

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate(instance: dict, schema_name: str) -> None:
    schema = load_schema(schema_name)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def assert_rejects(instance: dict, schema_name: str, *path_fragments: str) -> None:
    schema = load_schema(schema_name)
    try:
        Draft202012Validator(schema).validate(instance)
    except jsonschema.ValidationError as err:
        path = "/".join(str(p) for p in err.absolute_path)
        msg = f"{path} {err.message}"
        for frag in path_fragments:
            if frag in msg or frag in path:
                return
        raise AssertionError(f"rejected for unexpected reason: {msg}") from err
    raise AssertionError("expected validation failure")
