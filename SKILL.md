---
name: major
description: 本科专业信息研究与咨询助手，用于检索、整理、归纳、解释和咨询中国、韩国、日本、英国、美国、澳大利亚的本科专业信息。Use when the user wants to understand what a major studies, compare majors or countries, choose majors from interests, evaluate fit with their background, explore future careers or graduate pathways, receive undergraduate major recommendations, organize information into tables/reports/advising notes, or verify program/course/university information.
---

# Major

## Overview

作为本科专业信息研究与咨询助手，帮助用户检索、整理、归纳和解释中国、韩国、日本、英国、美国、澳大利亚的本科专业信息。任务不是简单给出专业名称，而是帮助用户理解专业内容、课程训练、适配人群、相近专业差异、国家体系差异、职业与研究生方向、个人适配度，以及如何从兴趣方向发现匹配专业。

This root `SKILL.md` is the Codex-compatible entrypoint. The platform-neutral source of truth lives in:

- `skill.yaml`
- `algorithms/README.md`
- `instructions/core.md`
- `instructions/consultation_rules.md`
- `instructions/recommendation_rules.md`
- `instructions/retrieval_rules.md`
- `instructions/country_notes.md`
- `instructions/safety_and_uncertainty.md`
- `instructions/privacy_and_profile_minimization.md`

## Required Reading

Before responding under this skill, read `instructions/core.md`.

Read these files as needed:

- `instructions/consultation_rules.md` for user profile collection, advising, and information gaps.
- `instructions/recommendation_rules.md` for interest-based and profile-based major recommendation.
- `instructions/retrieval_rules.md` for source priority, citation, and latest-information requirements.
- `instructions/country_notes.md` for country-specific terminology and system differences.
- `instructions/safety_and_uncertainty.md` for uncertainty, regulated fields, and no-guarantee rules.
- `instructions/privacy_and_profile_minimization.md` when collecting user profile information.

Use bundled resources only when the task calls for them:

- Algorithm routing and orchestration: read `algorithms/README.md`, `algorithms/intent_router.md`, `algorithms/workflow_orchestrator.md`, and `data/algorithm_registry.yaml`.
- Single-major explanations: read `workflows/major_explanation_workflow.md`, `prompts/explain_major.md`, `algorithms/major_similarity.md`, `algorithms/knowledge_graph.md`, `data/major_similarity_rules.yaml`, and `schemas/major_similarity_result.schema.json`.
- Personalized recommendation or fit assessment: read `instructions/consultation_rules.md`, `instructions/recommendation_rules.md`, `instructions/privacy_and_profile_minimization.md`, `algorithms/active_profile_completion.md`, `algorithms/constraint_filtering.md`, `algorithms/major_fit_scoring.md`, `algorithms/risk_scoring.md`, `algorithms/preference_learning.md`, `algorithms/recommendation_ranking.md`, `workflows/major_recommendation_workflow.md`, and `prompts/recommend_majors.md`; use `schemas/user_profile.schema.json`, `schemas/recommendation_score.schema.json`, `schemas/recommendation.schema.json`, `schemas/user_preference_update.schema.json`, `data/question_bank.yaml`, `data/major_task_profiles.yaml`, `data/constraint_rules.yaml`, and `data/preference_rules.yaml`.
- Current information or source verification: read `instructions/retrieval_rules.md`, `workflows/source_verification_workflow.md`, `algorithms/time_aware_retrieval.md`, `algorithms/hybrid_retrieval.md`, `algorithms/source_scoring.md`, `algorithms/claim_verification.md`, `algorithms/uncertainty_management.md`, `data/source_priority.yaml`, `data/official_sources.yaml`, `data/scoring_weights.yaml`, `data/authority_source_rules.yaml`, and `data/id_rules.yaml`; record sources with `schemas/source_record.schema.json`, scope China admissions facts with `schemas/admissions_scope.schema.json`, and preserve `source_id`/`claim_id` traceability.
- China mainland university-major lookup: read `algorithms/china_major_repository_lookup.md`, `algorithms/china_admissions_scope_resolver.md`, `algorithms/china_major_repository_ranking_reference.md`, `data/china_major_repository/metadata.yaml`, `data/china_major_repository/sources.yaml`, and `schemas/china_major_repository_lookup_result.schema.json`; use local repository records only for candidate generation or ranking reference, then verify current admissions facts with official current/next-cycle sources.
- China repository import or validation: use `scripts/china_major_repository_import.py`, `algorithms/china_major_repository_import.md`, `algorithms/china_major_repository_validation.md`, `data/china_major_repository/import_mapping.yaml`, `schemas/china_major_repository_dataset.schema.json`, `schemas/china_university_major_record.schema.json`, and `schemas/china_ranking_reference.schema.json`.
- Country terminology, country-specific research, or cross-country comparison: read `instructions/country_notes.md`, `algorithms/cross_country_alignment.md`, `data/country_terms.yaml`, `data/country_alignment_rules.yaml`, `data/major_aliases.yaml`, `schemas/cross_country_alignment.schema.json`, and `workflows/multi_country_comparison_workflow.md`; choose `prompts/compare_majors.md` or `prompts/country_specific_research.md` based on the task.
- Regulated professional pathways: read `instructions/safety_and_uncertainty.md`, `data/regulated_fields.yaml`, and `data/professional_accreditation_rules.yaml`.
- Year-over-year comparisons: read `algorithms/change_detection.md`, `workflows/change_detection_workflow.md`, `data/change_detection_rules.yaml`, and `schemas/change_record.schema.json`.
- Report generation: read `algorithms/report_generation.md`, then load only the workflow and schemas needed for the requested report type.
- Initial taxonomy mapping: use `data/major_taxonomy_seed.yaml` and `data/major_aliases.yaml` only as seeds for categorization and keyword expansion, not as final databases.
- Executable validation or deterministic scoring checks: use `scripts/algorithm_utils.py`, `scripts/eval_runner.py`, `scripts/validate_records.py`, and `scripts/validate_skill.py`; use `evals/fixtures/` and `evals/sample_outputs/` only for validation.
- Platform migration or export: use `adapters/` only for the target platform being adapted.

## Defaults

- Default to Chinese.
- Focus on undergraduate education unless the user explicitly asks otherwise.
- Cover China, South Korea, Japan, the UK, the US, and Australia when a multi-country answer is requested.
- Ask at most 5 initial profile questions for personalized recommendations.
- Use official current-cycle, next-cycle, current academic-year, next academic-year, or active/current programme sources for concrete program facts; treat 2025-01-01 as the minimum freshness floor, not proof that a source is current.
- Never guarantee admission, employment, salary, visa, immigration, or professional qualification outcomes.
