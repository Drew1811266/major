#!/usr/bin/env python3
"""Validate traceability and lightweight JSON Schema contracts for major records.

Usage:
  python3 scripts/validate_records.py records.json

The records file may contain keys: sources, claims, nodes, edges, changes.
This validator intentionally supports only the JSON Schema features used by
major's local schemas, so it does not need third-party dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def as_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "$ref" in schema:
        schema = load_schema(schema["$ref"])

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(type_matches(value, item) for item in expected_type):
            fail(f"{path} expected one of {expected_type}, got {type(value).__name__}")
    elif isinstance(expected_type, str) and not type_matches(value, expected_type):
        fail(f"{path} expected {expected_type}, got {type(value).__name__}")

    if "enum" in schema and value not in schema["enum"]:
        fail(f"{path} has invalid enum value {value!r}")

    if isinstance(value, str) and "pattern" in schema and not re.match(schema["pattern"], value):
        fail(f"{path} does not match pattern {schema['pattern']}: {value!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            fail(f"{path} is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            fail(f"{path} is above maximum {schema['maximum']}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                fail(f"{path} missing required field {key!r}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                fail(f"{path} has unsupported fields: {sorted(extra)}")
        for key, item in value.items():
            if key in properties:
                validate_schema(item, properties[key], f"{path}.{key}")
            elif isinstance(schema.get("additionalProperties"), dict):
                validate_schema(item, schema["additionalProperties"], f"{path}.{key}")

    if isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{index}]")


def validate_records(data: dict[str, Any]) -> None:
    sources = as_list(data.get("sources"))
    claims = as_list(data.get("claims"))
    nodes = as_list(data.get("nodes"))
    edges = as_list(data.get("edges"))
    changes = as_list(data.get("changes"))

    source_schema = load_schema("source_record.schema.json")
    claim_schema = load_schema("claim_verification.schema.json")
    node_schema = load_schema("knowledge_graph_node.schema.json")
    edge_schema = load_schema("knowledge_graph_edge.schema.json")
    change_schema = load_schema("change_record.schema.json")

    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        validate_schema(source, source_schema, f"$.sources[{index}]")
        source_id = source["source_id"]
        if source_id in source_ids:
            fail(f"Duplicate source_id: {source_id}")
        source_ids.add(source_id)

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        validate_schema(claim, claim_schema, f"$.claims[{index}]")
        claim_id = claim["claim_id"]
        if claim_id in claim_ids:
            fail(f"Duplicate claim_id: {claim_id}")
        claim_ids.add(claim_id)
        for source_id in claim.get("supporting_source_ids", []) + claim.get("conflicting_source_ids", []):
            if source_id not in source_ids:
                fail(f"Claim {claim_id} references missing source_id {source_id}")
        for embedded_source in claim.get("supporting_sources", []) + claim.get("conflicting_sources", []):
            embedded_id = embedded_source.get("source_id")
            if embedded_id not in source_ids:
                fail(f"Claim {claim_id} embeds source not present in source table: {embedded_id}")
            table_source = next(source for source in sources if source["source_id"] == embedded_id)
            if embedded_source != table_source:
                fail(f"Claim {claim_id} embedded source {embedded_id} differs from source table")

    for source in sources:
        for claim_id in source.get("supports_claims", []):
            if claim_id not in claim_ids:
                fail(f"Source {source['source_id']} references missing claim_id {claim_id}")

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        validate_schema(node, node_schema, f"$.nodes[{index}]")
        node_id = node["node_id"]
        if node_id in node_ids:
            fail(f"Duplicate node_id: {node_id}")
        node_ids.add(node_id)
        for source_id in node.get("source_ids", []):
            if source_id not in source_ids:
                fail(f"Node {node_id} references missing source_id {source_id}")

    for index, edge in enumerate(edges):
        validate_schema(edge, edge_schema, f"$.edges[{index}]")
        edge_id = edge["edge_id"]
        if edge.get("from_node_id") not in node_ids:
            fail(f"Edge {edge_id} references missing from_node_id")
        if edge.get("to_node_id") not in node_ids:
            fail(f"Edge {edge_id} references missing to_node_id")
        for source_id in edge.get("evidence_source_ids", []):
            if source_id not in source_ids:
                fail(f"Edge {edge_id} references missing source_id {source_id}")
        for claim_id in edge.get("evidence_claim_ids", []):
            if claim_id not in claim_ids:
                fail(f"Edge {edge_id} references missing claim_id {claim_id}")

    for index, change in enumerate(changes):
        validate_schema(change, change_schema, f"$.changes[{index}]")
        change_id = change["change_id"]
        for source_id in change.get("old_source_ids", []) + change.get("new_source_ids", []):
            if source_id not in source_ids:
                fail(f"Change {change_id} references missing source_id {source_id}")
        for claim_id in change.get("claim_ids", []):
            if claim_id not in claim_ids:
                fail(f"Change {change_id} references missing claim_id {claim_id}")


def main() -> None:
    if len(sys.argv) == 1:
        print("No records file supplied; traceability validator ready")
        return
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_records(data)
    print("record traceability validation passed")


if __name__ == "__main__":
    main()
