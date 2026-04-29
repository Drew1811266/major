#!/usr/bin/env python3
"""Validate the major skill package structure and machine-readable files."""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}")


def validate_single_skill_entrypoint() -> None:
    skill_files = sorted(ROOT.rglob("SKILL.md"))
    expected = ROOT / "SKILL.md"
    if skill_files != [expected]:
        listed = ", ".join(str(path.relative_to(ROOT)) for path in skill_files)
        fail(f"Expected only root SKILL.md; found: {listed}")

    text = expected.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError:
        fail("SKILL.md frontmatter is not closed")
    meta = yaml.safe_load(frontmatter)
    if meta.get("name") != ROOT.name:
        fail(f"SKILL.md name must match directory name {ROOT.name!r}")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        fail("SKILL.md description must be a non-empty string")
    if len(description) > 1024:
        fail("SKILL.md description must be 1024 characters or fewer")


def validate_machine_readable_files() -> None:
    forbidden_names = {".DS_Store", "Thumbs.db"}
    for path in ROOT.rglob("*"):
        if path.name in forbidden_names:
            fail(f"Remove generated system file: {path.relative_to(ROOT)}")
    for path in sorted(ROOT.rglob("*.json")):
        load_json(path)
    for path in sorted(ROOT.rglob("*.yaml")):
        load_yaml(path)


def validate_evals() -> None:
    evals_path = ROOT / "evals" / "evals.json"
    data = load_json(evals_path)
    if data.get("skill_name") != "major":
        fail("evals/evals.json must declare skill_name = major")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        fail("evals/evals.json must contain a non-empty evals list")
    required = {"id", "name", "prompt", "expected_behavior", "must_include", "must_not_include", "expected_algorithms", "grading_notes"}
    for index, case in enumerate(evals, start=1):
        missing = required - set(case)
        if missing:
            fail(f"Eval #{index} missing keys: {sorted(missing)}")
        if not isinstance(case["must_include"], list) or not case["must_include"]:
            fail(f"Eval {case['id']!r} must include non-empty must_include")
        if not isinstance(case["must_not_include"], list) or not case["must_not_include"]:
            fail(f"Eval {case['id']!r} must include non-empty must_not_include")
        for item in case["must_include"]:
            text = str(item).strip()
            negative = (
                text.startswith("暗示")
                or text.startswith("承诺")
                or text.startswith("忽视")
                or text.startswith("不提醒")
                or text.startswith("未询问")
                or text.startswith("只凭")
                or text.startswith("给出无来源")
                or text.startswith("用旧来源")
                or bool(__import__("re").search(r"^把.*说成", text))
            )
            if negative:
                fail(f"Eval {case['id']!r} has a negative assertion in must_include: {item}")

    yaml_cases = load_yaml(ROOT / "evals" / "test_cases.yaml").get("test_cases", [])
    if len(yaml_cases) != len(evals):
        fail("evals/test_cases.yaml and evals/evals.json must contain the same number of cases")
    if [case.get("id") for case in yaml_cases] != [case.get("id") for case in evals]:
        fail("evals/test_cases.yaml and evals/evals.json IDs must be synchronized")
    if len(evals) < 36:
        fail("Expected at least 36 eval cases after current-cycle and traceability additions")


def validate_schema_contracts() -> None:
    source_schema = load_json(ROOT / "schemas" / "source_record.schema.json")
    source_required = set(source_schema.get("required", []))
    for key in ("source_id", "currentness_basis", "is_2025_or_later", "source_score"):
        if key not in source_required:
            fail(f"source_record.schema.json must require {key}")
    source_id = source_schema.get("properties", {}).get("source_id", {})
    if "src_" not in source_id.get("pattern", ""):
        fail("source_record.schema.json source_id must define a src_ pattern")
    supports_claims = source_schema.get("properties", {}).get("supports_claims", {}).get("items", {})
    if "clm_" not in supports_claims.get("pattern", ""):
        fail("source_record.schema.json supports_claims must contain claim_id pattern")
    source_types = set(source_schema.get("properties", {}).get("source_type", {}).get("enum", []))
    for key in ("ranking_reference", "local_repository_record"):
        if key not in source_types:
            fail(f"source_record.schema.json source_type must include {key}")

    intent_schema = load_json(ROOT / "schemas" / "intent_result.schema.json")
    intent_required = set(intent_schema.get("required", []))
    for key in ("requires_current_cycle_sources", "minimum_freshness_floor", "currentness_required"):
        if key not in intent_required:
            fail(f"intent_result.schema.json must require {key}")

    claim_schema = load_json(ROOT / "schemas" / "claim_verification.schema.json")
    claim_required = set(claim_schema.get("required", []))
    for key in ("claim_id", "admissions_scope", "supporting_source_ids", "conflicting_source_ids"):
        if key not in claim_required:
            fail(f"claim_verification.schema.json must require {key}")

    for schema_name, required_keys in {
        "china_university_major_record.schema.json": ("record_id", "university_name_zh", "major_name_zh", "education_level", "data_year", "source_ids"),
        "china_major_repository_dataset.schema.json": ("dataset_id", "authorization_status", "sources", "records"),
        "china_ranking_reference.schema.json": ("ranking_reference_id", "ranking_year", "methodology_url", "not_admissions_evidence"),
        "china_major_repository_lookup_result.schema.json": ("candidate_records", "ranking_references", "requires_official_verification"),
    }.items():
        schema = load_json(ROOT / "schemas" / schema_name)
        required = set(schema.get("required", []))
        for key in required_keys:
            if key not in required:
                fail(f"{schema_name} must require {key}")

    admissions_scope = load_json(ROOT / "schemas" / "admissions_scope.schema.json")
    scope_props = set(admissions_scope.get("properties", {}))
    for key in ("province", "intended_entry_year", "subject_combination", "admissions_batch", "application_route", "major_group", "source_scope_type"):
        if key not in scope_props:
            fail(f"admissions_scope.schema.json missing {key}")

    retrieval_schema = load_json(ROOT / "schemas" / "retrieval_result.schema.json")
    if "admissions_scope" not in retrieval_schema.get("properties", {}):
        fail("retrieval_result.schema.json must expose admissions_scope")

    edge_schema = load_json(ROOT / "schemas" / "knowledge_graph_edge.schema.json")
    edge_required = set(edge_schema.get("required", []))
    if "evidence_source_ids" not in edge_required:
        fail("knowledge_graph_edge.schema.json must require evidence_source_ids")
    if "evidence_claim_ids" not in edge_schema.get("properties", {}):
        fail("knowledge_graph_edge.schema.json must expose evidence_claim_ids")

    user_profile = load_json(ROOT / "schemas" / "user_profile.schema.json")
    profile_props = set(user_profile.get("properties", {}))
    for key in (
        "intended_entry_year",
        "exam_region_or_province",
        "subject_combination",
        "gaokao_track",
        "preferred_batch_or_application_route",
        "china_application_constraints",
    ):
        if key not in profile_props:
            fail(f"user_profile.schema.json missing China admissions profile field {key}")

    change_schema = load_json(ROOT / "schemas" / "change_record.schema.json")
    change_props = set(change_schema.get("properties", {}))
    for key in (
        "admissions_scope",
        "province",
        "admissions_batch",
        "major_group",
        "subject_selection_requirement",
        "enrollment_plan_scope",
        "major_code",
        "programme_code",
        "old_source_ids",
        "new_source_ids",
        "claim_ids",
    ):
        if key not in change_props:
            fail(f"change_record.schema.json missing traceability or China scope field {key}")


def validate_algorithm_registry() -> None:
    registry = load_yaml(ROOT / "data" / "algorithm_registry.yaml")
    algorithms = registry.get("algorithms", [])
    if not isinstance(algorithms, list) or not algorithms:
        fail("data/algorithm_registry.yaml must contain algorithms")
    required_sections = {
        "## 用途",
        "## 触发场景",
        "## 输入",
        "## 输出",
        "## 核心步骤",
        "## 失败处理",
        "## 与其他算法的关系",
    }
    names = set()
    for record in algorithms:
        name = record.get("name")
        file_path = record.get("file")
        if not name or not file_path:
            fail("Each algorithm registry item must include name and file")
        names.add(name)
        path = ROOT / file_path
        if not path.exists():
            fail(f"Algorithm file does not exist: {file_path}")
        text = path.read_text(encoding="utf-8")
        if path.name != "README.md":
            missing = [section for section in required_sections if section not in text]
            if missing:
                fail(f"Algorithm {name!r} missing sections: {missing}")
    expected = {
        "intent_router",
        "workflow_orchestrator",
        "time_aware_retrieval",
        "hybrid_retrieval",
        "source_scoring",
        "active_profile_completion",
        "major_fit_scoring",
        "constraint_filtering",
        "risk_scoring",
        "preference_learning",
        "recommendation_ranking",
        "china_admissions_scope_resolver",
        "china_major_repository_lookup",
        "china_major_repository_import",
        "china_major_repository_validation",
        "china_major_repository_ranking_reference",
        "major_similarity",
        "knowledge_graph",
        "cross_country_alignment",
        "claim_verification",
        "change_detection",
        "report_generation",
        "uncertainty_management",
    }
    missing_names = expected - names
    if missing_names:
        fail(f"Algorithm registry missing algorithms: {sorted(missing_names)}")


def validate_manifest_resource_paths() -> None:
    manifest = load_json(ROOT / "adapters" / "openai" / "tool_manifest.json")
    resources = manifest.get("resources", [])
    if not isinstance(resources, list):
        fail("OpenAI tool manifest resources must be a list")
    for resource in resources:
        if "*" in resource:
            fail(f"OpenAI tool manifest should not use glob resource paths: {resource}")
        path = ROOT / resource
        if not path.exists():
            fail(f"OpenAI tool manifest resource does not exist: {resource}")
    required_resources = {
        "algorithms/README.md",
        "algorithms/intent_router.md",
        "algorithms/workflow_orchestrator.md",
        "algorithms/hybrid_retrieval.md",
        "instructions/privacy_and_profile_minimization.md",
        "data/major_aliases.yaml",
        "data/official_sources.yaml",
        "data/regulated_fields.yaml",
        "data/scoring_weights.yaml",
        "data/authority_source_rules.yaml",
        "data/id_rules.yaml",
        "data/algorithm_registry.yaml",
        "data/question_bank.yaml",
        "data/major_task_profiles.yaml",
        "data/constraint_rules.yaml",
        "data/preference_rules.yaml",
        "data/major_similarity_rules.yaml",
        "data/country_alignment_rules.yaml",
        "data/professional_accreditation_rules.yaml",
        "data/change_detection_rules.yaml",
        "data/source_priority.yaml",
        "data/china_major_repository/metadata.yaml",
        "data/china_major_repository/sources.yaml",
        "data/china_major_repository/sample_records.yaml",
        "data/china_major_repository/import_mapping.yaml",
        "data/china_major_repository/README.md",
        "schemas/intent_result.schema.json",
        "schemas/admissions_scope.schema.json",
        "schemas/algorithm_decision.schema.json",
        "schemas/retrieval_result.schema.json",
        "schemas/recommendation_score.schema.json",
        "schemas/recommendation.schema.json",
        "schemas/user_preference_update.schema.json",
        "schemas/knowledge_graph_node.schema.json",
        "schemas/knowledge_graph_edge.schema.json",
        "schemas/cross_country_alignment.schema.json",
        "schemas/major_similarity_result.schema.json",
        "schemas/china_university_major_record.schema.json",
        "schemas/china_major_repository_dataset.schema.json",
        "schemas/china_ranking_reference.schema.json",
        "schemas/china_major_repository_lookup_result.schema.json",
        "schemas/claim_verification.schema.json",
        "schemas/uncertainty_record.schema.json",
        "schemas/change_record.schema.json",
        "schemas/source_record.schema.json",
        "scripts/algorithm_utils.py",
        "scripts/china_major_repository_import.py",
        "scripts/eval_runner.py",
        "scripts/validate_records.py",
        "scripts/validate_skill.py",
    }
    missing_required = required_resources - set(resources)
    if missing_required:
        fail(f"OpenAI tool manifest missing required resources: {sorted(missing_required)}")

    mcp = load_yaml(ROOT / "adapters" / "mcp" / "resources.yaml")
    mcp_resources = mcp.get("resources", {})
    for name, record in mcp.get("resources", {}).items():
        raw_path = record.get("path")
        if not raw_path:
            fail(f"MCP resource {name!r} is missing path")
        resolved = (ROOT / "adapters" / "mcp" / raw_path).resolve()
        if not resolved.exists():
            fail(f"MCP resource {name!r} path does not exist: {raw_path}")
    for key in (
        "major_aliases",
        "official_sources",
        "regulated_fields",
        "source_priority",
        "scoring_weights",
        "authority_source_rules",
        "algorithm_registry",
        "id_rules",
        "privacy_and_profile_minimization",
        "intent_result_schema",
        "admissions_scope_schema",
        "algorithm_decision_schema",
        "retrieval_result_schema",
        "recommendation_score_schema",
        "claim_verification_schema",
        "uncertainty_record_schema",
        "change_record_schema",
        "algorithms_readme",
        "intent_router_algorithm",
        "workflow_orchestrator_algorithm",
        "hybrid_retrieval_algorithm",
        "active_profile_completion_algorithm",
        "constraint_filtering_algorithm",
        "major_fit_scoring_algorithm",
        "risk_scoring_algorithm",
        "preference_learning_algorithm",
        "recommendation_ranking_algorithm",
        "china_admissions_scope_resolver_algorithm",
        "china_major_repository_lookup_algorithm",
        "china_major_repository_import_algorithm",
        "china_major_repository_validation_algorithm",
        "china_major_repository_ranking_reference_algorithm",
        "major_similarity_algorithm",
        "knowledge_graph_algorithm",
        "cross_country_alignment_algorithm",
        "change_detection_algorithm",
        "report_generation_algorithm",
        "algorithm_utils_script",
        "china_major_repository_import_script",
        "eval_runner_script",
        "validate_records_script",
        "validate_skill_script",
    ):
        if key not in mcp_resources:
            fail(f"MCP resources missing {key!r}")


def validate_scripts() -> None:
    for relative in (
        "scripts/algorithm_utils.py",
        "scripts/china_major_repository_import.py",
        "scripts/eval_runner.py",
        "scripts/validate_records.py",
        "scripts/validate_skill.py",
        "scripts/test_algorithm_utils.py",
    ):
        path = ROOT / relative
        if not path.exists():
            fail(f"Missing script: {relative}")
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"Script does not compile: {relative}: {exc.msg}")


def run_script(args: list[str], expect_success: bool = True) -> None:
    result = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
    if expect_success and result.returncode != 0:
        fail(f"Command failed: python {' '.join(args)}\n{result.stdout}{result.stderr}")
    if not expect_success and result.returncode == 0:
        fail(f"Command unexpectedly succeeded: python {' '.join(args)}")


def validate_behavioral_checks() -> None:
    run_script(["scripts/eval_runner.py", "--mode", "structure"])
    run_script(["scripts/eval_runner.py", "--mode", "sample-output-lint"])
    run_script(["scripts/validate_records.py", "evals/fixtures/valid_traceability.json"])
    run_script(["scripts/validate_records.py", "evals/fixtures/invalid_minimal_source.json"], expect_success=False)
    run_script(["scripts/validate_records.py", "evals/fixtures/invalid_missing_reference.json"], expect_success=False)
    run_script(["scripts/china_major_repository_import.py", "--validate-only", "data/china_major_repository/sample_records.yaml"])


def validate_agents_metadata() -> None:
    metadata_path = ROOT / "agents" / "openai.yaml"
    data = load_yaml(metadata_path)
    default_prompt = data.get("interface", {}).get("default_prompt", "")
    if "$major" not in default_prompt:
        fail("agents/openai.yaml interface.default_prompt must mention $major")
    if "使用" not in default_prompt:
        fail("agents/openai.yaml interface.default_prompt should be Chinese")


def main() -> None:
    validate_single_skill_entrypoint()
    validate_machine_readable_files()
    validate_evals()
    validate_schema_contracts()
    validate_algorithm_registry()
    validate_manifest_resource_paths()
    validate_scripts()
    validate_behavioral_checks()
    validate_agents_metadata()
    print("major skill validation passed")


if __name__ == "__main__":
    main()
