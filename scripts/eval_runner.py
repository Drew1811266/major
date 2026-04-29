#!/usr/bin/env python3
"""Structural and sample-output eval checks for the major skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NEGATIVE_PATTERNS = [
    r"^把.*说成",
    r"^暗示.*即可",
    r"^承诺",
    r"^忽视",
    r"^不提醒",
    r"^未询问",
    r"^只凭",
    r"^给出无来源",
    r"^用旧来源",
    r"^不说明",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_cases() -> tuple[list[dict], list[dict]]:
    yaml_cases = yaml.safe_load((ROOT / "evals" / "test_cases.yaml").read_text(encoding="utf-8"))["test_cases"]
    json_cases = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]
    return yaml_cases, json_cases


def normalize_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def is_negative_assertion(text: str) -> bool:
    stripped = text.strip()
    return any(re.search(pattern, stripped) for pattern in NEGATIVE_PATTERNS)


def validate_eval_sync(yaml_cases: list[dict], json_cases: list[dict]) -> None:
    yaml_ids = [case["id"] for case in yaml_cases]
    json_ids = [case["id"] for case in json_cases]
    if yaml_ids != json_ids:
        fail("evals/test_cases.yaml and evals/evals.json IDs are not synchronized")


def validate_yaml_cases(yaml_cases: list[dict]) -> None:
    required = {"id", "user_input", "expected_intent", "expected_algorithms", "expected_behavior", "failure_modes", "grading_notes"}
    currentness_cases = 0
    traceability_cases = 0
    china_scope_cases = 0
    privacy_cases = 0
    for case in yaml_cases:
        missing = required - set(case)
        if missing:
            fail(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
        text = " ".join(
            str(item)
            for key in ("user_input", "expected_behavior", "failure_modes", "grading_notes")
            for item in (case.get(key) if isinstance(case.get(key), list) else [case.get(key, "")])
        )
        lower = text.lower()
        if any(term in lower for term in ("current", "当前", "下一招生", "current-cycle", "next-cycle")):
            currentness_cases += 1
        if any(term in lower for term in ("source_id", "claim_id", "graph", "图谱", "追踪")):
            traceability_cases += 1
        if any(term in lower for term in ("省份", "选科", "专业组", "分省", "入学年份")):
            china_scope_cases += 1
        if any(term in lower for term in ("privacy", "隐私", "最小化", "敏感")):
            privacy_cases += 1
        if ("recommend" in case["expected_intent"] or case["expected_intent"] == "evaluate_fit") and not case["expected_algorithms"]:
            fail(f"{case['id']} recommendation-like case must list expected algorithms")
    if currentness_cases < 3:
        fail("Expected at least 3 current-cycle freshness eval cases")
    if traceability_cases < 1:
        fail("Expected at least 1 traceability eval case")
    if china_scope_cases < 3:
        fail("Expected at least 3 China province/scope eval cases")
    if privacy_cases < 1:
        fail("Expected at least 1 privacy/minimal-profile eval case")


def validate_json_cases(yaml_cases: list[dict], json_cases: list[dict]) -> None:
    yaml_by_id = {case["id"]: case for case in yaml_cases}
    required = {"id", "name", "prompt", "expected_behavior", "must_include", "must_not_include", "expected_algorithms", "grading_notes"}
    for case in json_cases:
        missing = required - set(case)
        if missing:
            fail(f"evals.json case {case.get('id', '<unknown>')} missing {sorted(missing)}")
        source = yaml_by_id[case["id"]]
        if case["prompt"] != source["user_input"]:
            fail(f"{case['id']} prompt does not match YAML user_input")
        if case["expected_algorithms"] != source["expected_algorithms"]:
            fail(f"{case['id']} expected_algorithms do not match YAML")
        if case["must_include"] != normalize_list(source["expected_behavior"]):
            fail(f"{case['id']} must_include does not match YAML expected_behavior")
        if case["must_not_include"] != normalize_list(source["failure_modes"]):
            fail(f"{case['id']} must_not_include does not match YAML failure_modes")
        for item in case["must_include"]:
            if is_negative_assertion(item):
                fail(f"{case['id']} has negative assertion in must_include: {item}")
        if not case["must_not_include"]:
            fail(f"{case['id']} must_not_include should not be empty")


def validate_structure() -> None:
    yaml_cases, json_cases = load_cases()
    validate_eval_sync(yaml_cases, json_cases)
    validate_yaml_cases(yaml_cases)
    validate_json_cases(yaml_cases, json_cases)
    print(f"major eval structural checks passed ({len(yaml_cases)} cases)")


def require_all(text: str, filename: str, terms: list[str]) -> None:
    missing = [term for term in terms if term not in text]
    if missing:
        fail(f"{filename} missing sample-output lint terms: {missing}")


def validate_sample_outputs() -> None:
    sample_dir = ROOT / "evals" / "sample_outputs"
    files = sorted(sample_dir.glob("*.md"))
    if len(files) < 8:
        fail("Expected at least 8 sample output lint files")

    checks = {
        "current-cycle-fallback": ["当前/下一周期", "无法确认", "2025-01-01"],
        "stale-2025-downgrade": ["minimum_2025_floor_only", "limited", "不能直接视为最新结论"],
        "china-missing-scope": ["省份", "选科", "入学年份", "批次"],
        "source-conflict": ["来源冲突", "conflicting_sources", "不确定"],
        "regulated-checklist": ["官方核查清单", "认证状态", "临床/实习", "注册路径", "适用年份"],
        "traceability": ["source_id", "claim_id", "evidence_source_ids"],
        "recommendation-five-questions": ["最多 5 个问题", "Q1", "Q5"],
        "no-guarantee": ["不承诺", "录取", "就业", "薪资", "签证", "职业资格"],
    }
    seen = set()
    for file in files:
        text = file.read_text(encoding="utf-8")
        stem = file.stem
        for name, terms in checks.items():
            if stem.startswith(name):
                require_all(text, file.name, terms)
                seen.add(name)
        if "recommendation-five-questions" in stem:
            question_count = len(re.findall(r"^Q[0-9]+[:：]", text, flags=re.MULTILINE))
            if question_count > 5:
                fail(f"{file.name} asks more than 5 questions")
    missing = set(checks) - seen
    if missing:
        fail(f"Missing sample output lint categories: {sorted(missing)}")
    print(f"major sample-output lint checks passed ({len(files)} files)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["structure", "sample-output-lint", "all"], default="all")
    args = parser.parse_args()
    if args.mode in {"structure", "all"}:
        validate_structure()
    if args.mode in {"sample-output-lint", "all"}:
        validate_sample_outputs()


if __name__ == "__main__":
    main()
