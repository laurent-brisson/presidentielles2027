#!/usr/bin/env python3
"""Validate the YAML data files.

Checks:
  - data/candidates.yaml against schema/candidates.schema.json
  - candidate ids are unique
  - every party reference exists in data/parties.yaml

Usage: python scripts/validate.py
Requires: pyyaml, jsonschema
"""

import datetime
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def stringify_dates(node):
    """YAML parses ISO dates into date objects; JSON Schema expects strings."""
    if isinstance(node, dict):
        return {k: stringify_dates(v) for k, v in node.items()}
    if isinstance(node, list):
        return [stringify_dates(v) for v in node]
    if isinstance(node, (datetime.date, datetime.datetime)):
        return node.isoformat()
    return node


def main():
    errors = []

    candidates = stringify_dates(load_yaml(ROOT / "data/candidates.yaml"))
    parties = load_yaml(ROOT / "data/parties.yaml")
    schema = json.loads((ROOT / "schema/candidates.schema.json").read_text(encoding="utf-8"))

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in validator.iter_errors(candidates):
        path = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"schema: {path}: {err.message}")

    party_ids = [p["id"] for p in parties["parties"]]
    if len(party_ids) != len(set(party_ids)):
        errors.append("parties: duplicate ids")

    seen = set()
    for c in candidates.get("candidates", []):
        cid = c.get("id")
        if cid in seen:
            errors.append(f"{cid}: duplicate candidate id")
        seen.add(cid)
        refs = [c.get("party")] + list(c.get("supporting_parties", []))
        for ref in refs:
            if ref is not None and ref not in party_ids:
                errors.append(f"{cid}: unknown party id '{ref}'")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(seen)} candidates, {len(party_ids)} parties")
    return 0


if __name__ == "__main__":
    sys.exit(main())
