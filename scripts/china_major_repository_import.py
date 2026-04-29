#!/usr/bin/env python3
"""Import authorized China mainland university-major data into major's repository schema."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from algorithm_utils import make_stable_id  # noqa: E402
from validate_records import load_schema, validate_schema  # noqa: E402


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_structured(path: Path) -> Any:
    if not path.exists() and not path.is_absolute():
        path = ROOT / path
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            fail("PyYAML is required to read YAML files")
        return yaml.safe_load(text)
    fail(f"Unsupported file type: {path}")


def load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists() and not path.is_absolute():
        path = ROOT / path
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    data = load_structured(path)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("records", "rows", "data"):
            if isinstance(data.get(key), list):
                return data[key]
    fail("Input JSON/YAML must be a list or contain records/rows/data")


def load_mapping(path: Path | None = None) -> dict[str, Any]:
    mapping_path = path or ROOT / "data" / "china_major_repository" / "import_mapping.yaml"
    data = load_structured(mapping_path)
    if not isinstance(data, dict):
        fail("import_mapping.yaml must be a mapping")
    return data


def pick(row: dict[str, Any], aliases: list[str], default: Any = "") -> Any:
    for alias in aliases:
        if alias in row and row[alias] not in (None, ""):
            return row[alias]
    return default


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "y", "是", "招生", "当前招生"}


def normalize_record(row: dict[str, Any], mapping: dict[str, Any], default_source_id: str, authorization_status: str) -> dict[str, Any]:
    fields = mapping.get("canonical_fields", {})

    def field(name: str, default: Any = "") -> Any:
        spec = fields.get(name, {})
        return pick(row, spec.get("aliases", [name]), spec.get("default", default))

    university = str(field("university_name_zh")).strip()
    major = str(field("major_name_zh")).strip()
    data_year = str(field("data_year")).strip()
    if not university:
        fail("Import row missing university_name_zh")
    if not major:
        fail("Import row missing major_name_zh")
    if not data_year:
        fail("Import row missing data_year")

    repository_source_type = str(field("repository_source_type", "authorized_local_dataset")).strip() or "authorized_local_dataset"
    ranking_name = str(field("ranking_name")).strip()
    source_id = str(field("source_id", default_source_id)).strip() or default_source_id
    currently_admitting = normalize_bool(field("currently_admitting", False))
    record_usage = "candidate_only"
    if repository_source_type == "ranking_reference" or ranking_name:
        record_usage = "ranking_reference_only"
    if currently_admitting and repository_source_type in {"university_admissions_catalog", "provincial_enrollment_plan"}:
        record_usage = "official_verified_reference"
    if authorization_status in {"unknown", "not_for_user_facing_use"}:
        record_usage = "historical_context"

    ranking_reference = None
    if ranking_name:
        methodology_url = str(field("methodology_url")).strip()
        if not methodology_url:
            fail("Ranking reference rows must include methodology_url")
        ranking_reference = {
            "ranking_reference_id": make_stable_id("rank_china", university, major, ranking_name, year=data_year),
            "ranking_name": ranking_name,
            "ranking_year": data_year,
            "publisher": str(field("ranking_publisher", "unknown")).strip() or "unknown",
            "methodology_url": methodology_url,
            "ranking_url": str(field("ranking_url")).strip(),
            "university_name_zh": university,
            "university_name_en": str(field("university_name_en")).strip(),
            "major_name_zh": major,
            "major_code": str(field("major_code")).strip(),
            "discipline_category": str(field("discipline_category")).strip(),
            "major_category": str(field("major_category")).strip(),
            "rank_position": str(field("rank_position")).strip(),
            "rating": str(field("rating")).strip(),
            "ranking_scope": "China mainland undergraduate major ranking reference",
            "source_id": source_id,
            "not_admissions_evidence": True,
            "limitations": [
                "第三方排名参考，不是当前招生、录取、选科、专业组或分省计划依据。",
                "必须继续核验高校招生网、阳光高考、省级考试院或教育部等官方来源。"
            ]
        }

    record = {
        "record_id": str(field("record_id")).strip() or make_stable_id("cnmaj", university, major, year=data_year),
        "university_name_zh": university,
        "university_name_en": str(field("university_name_en")).strip(),
        "province_or_region": str(field("province_or_region")).strip(),
        "university_code": str(field("university_code")).strip(),
        "major_name_zh": major,
        "major_name_en": str(field("major_name_en")).strip(),
        "major_code": str(field("major_code")).strip(),
        "discipline_category": str(field("discipline_category")).strip(),
        "major_category": str(field("major_category")).strip(),
        "education_level": "undergraduate",
        "data_year": data_year,
        "repository_source_type": repository_source_type,
        "record_usage": record_usage,
        "currently_admitting": currently_admitting,
        "source_ids": [source_id],
        "claim_ids": [],
        "requires_official_verification": [
            "当前招生",
            "招生专业目录",
            "分省招生计划",
            "选科要求",
            "专业组",
            "培养方案"
        ],
        "limitations": [
            "本地导入记录只用于候选初筛。",
            "当前招生事实必须以官方 current/next-cycle 来源核验。"
        ]
    }
    if ranking_reference:
        record["ranking_reference"] = ranking_reference
    if currently_admitting and repository_source_type not in {"university_admissions_catalog", "provincial_enrollment_plan"}:
        fail("currently_admitting=true requires an official admissions source type")
    return record


def default_source(source_id: str, data_year: str, authorization_status: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": "Authorized China Major Repository Import",
        "url": "local://authorized-import",
        "publisher": "authorized local dataset",
        "source_type": "local_repository_record",
        "country": "China",
        "accessed_date": "2026-04-29",
        "applicable_year": data_year,
        "is_2025_or_later": int(data_year[:4]) >= 2025 if data_year[:4].isdigit() else False,
        "freshness_basis": "applicable_year",
        "currentness_basis": "minimum_2025_floor_only",
        "source_score": 0.30 if authorization_status == "authorized" else 0.20,
        "reliability_level": "low",
        "supports_claims": [],
        "limitations": "Local imported repository record; not official admissions evidence without matching official source.",
        "archive_or_current_status": "current"
    }


def validate_dataset(dataset: dict[str, Any]) -> None:
    validate_schema(dataset, load_schema("china_major_repository_dataset.schema.json"), "$")
    source_ids = {source["source_id"] for source in dataset.get("sources", [])}
    for record in dataset.get("records", []):
        for source_id in record.get("source_ids", []):
            if source_id not in source_ids:
                fail(f"Record {record['record_id']} references missing source_id {source_id}")
        if record.get("currently_admitting") and record.get("record_usage") != "official_verified_reference":
            fail(f"Record {record['record_id']} claims currently_admitting without official_verified_reference usage")
        ranking = record.get("ranking_reference")
        if ranking and not ranking.get("not_admissions_evidence"):
            fail(f"Ranking reference {ranking['ranking_reference_id']} must set not_admissions_evidence=true")


def build_dataset(args: argparse.Namespace) -> dict[str, Any]:
    rows = load_rows(Path(args.input))
    mapping = load_mapping(Path(args.mapping) if args.mapping else None)
    source_id = args.source_id or make_stable_id("source", "china", "authorized_import", year=args.data_year)
    records = [normalize_record(row, mapping, source_id, args.authorization_status) for row in rows]
    return {
        "dataset_id": make_stable_id("cnrepo", "authorized_import", year=args.data_year),
        "name": args.name,
        "version": args.version,
        "language": "zh-CN",
        "data_year": args.data_year,
        "updated_date": args.updated_date,
        "authorization_status": args.authorization_status,
        "source_statement": args.source_statement,
        "usage_policy": [
            "本地库用于候选专业和候选院校初筛，不等于当前招生事实。",
            "排名参考不得作为录取、选科、专业组或分省计划依据。",
            "当前招生相关事实必须继续核验官方 current/next-cycle 来源。"
        ],
        "sources": [default_source(source_id, args.data_year, args.authorization_status)],
        "records": records,
        "limitations": [
            "Imported local dataset depends on user-provided authorization and source quality.",
            "Official admissions verification remains required for current facts."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Authorized CSV/JSON/YAML input file")
    parser.add_argument("--output", help="Output dataset JSON path")
    parser.add_argument("--mapping", help="Optional import mapping YAML")
    parser.add_argument("--validate-only", help="Validate an existing dataset YAML/JSON")
    parser.add_argument("--authorization-status", choices=["authorized", "sample_only", "unknown", "not_for_user_facing_use"], default="unknown")
    parser.add_argument("--data-year", default="2025")
    parser.add_argument("--updated-date", default="2026-04-29")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--name", default="Authorized China Major Repository Import")
    parser.add_argument("--source-id")
    parser.add_argument("--source-statement", default="User-provided authorized local dataset.")
    args = parser.parse_args()

    if args.validate_only:
        data = load_structured(Path(args.validate_only))
        validate_dataset(data)
        print("china major repository dataset validation passed")
        return
    if not args.input or not args.output:
        fail("Provide --input and --output, or use --validate-only")
    dataset = build_dataset(args)
    validate_dataset(dataset)
    Path(args.output).write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
