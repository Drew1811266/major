# Major Skill

Use this skill when the user asks about undergraduate majors, university programs, academic major selection, cross-country major comparison, or personalized major recommendations for China, South Korea, Japan, the United Kingdom, the United States, or Australia.

Default freshness rule:
For current university major information, admissions requirements, course structures, tuition, deadlines, accreditation, employment statistics, visa/work policies, and China mainland undergraduate admissions data, prefer current-year, current admissions-cycle, next admissions-cycle, current/next academic-year, or active/current official programme pages. Treat 2025-or-later as the minimum freshness floor, not proof that a source is current.

For China mainland universities, prioritize:
- latest undergraduate admissions regulations;
- latest admissions major catalogs;
- latest enrollment plans;
- latest subject selection requirements;
- current official university undergraduate admissions pages;
- current or latest training programmes, if available.

If no reliable current/next-cycle source is found, say so clearly. If only 2025-or-later but not clearly current sources are found, label the limitation. Do not silently use older information as current evidence.

Load `instructions/core.md` first.

Load additional files only when the task calls for them:
- Algorithm routing: `algorithms/README.md`, `algorithms/intent_router.md`, `algorithms/workflow_orchestrator.md`, `data/algorithm_registry.yaml`.
- Personalized advising: `instructions/consultation_rules.md`, `instructions/recommendation_rules.md`, `instructions/privacy_and_profile_minimization.md`, `algorithms/active_profile_completion.md`, `algorithms/constraint_filtering.md`, `algorithms/major_fit_scoring.md`, `algorithms/risk_scoring.md`, `algorithms/preference_learning.md`, `algorithms/recommendation_ranking.md`, `workflows/major_recommendation_workflow.md`, `prompts/recommend_majors.md`, `schemas/user_profile.schema.json`, `schemas/recommendation_score.schema.json`, `schemas/recommendation.schema.json`, `schemas/user_preference_update.schema.json`, `data/question_bank.yaml`, `data/major_task_profiles.yaml`, `data/constraint_rules.yaml`, `data/preference_rules.yaml`.
- Single-major explanation: `workflows/major_explanation_workflow.md`, `prompts/explain_major.md`.
- Current source verification: `instructions/retrieval_rules.md`, `workflows/source_verification_workflow.md`, `algorithms/time_aware_retrieval.md`, `algorithms/hybrid_retrieval.md`, `algorithms/source_scoring.md`, `algorithms/claim_verification.md`, `algorithms/uncertainty_management.md`, `data/source_priority.yaml`, `data/official_sources.yaml`, `data/scoring_weights.yaml`, `data/authority_source_rules.yaml`, `data/id_rules.yaml`, `schemas/source_record.schema.json`, `schemas/admissions_scope.schema.json`. Preserve `source_id`, `claim_id`, and admissions scope traceability.
- China mainland repository lookup: `algorithms/china_admissions_scope_resolver.md`, `algorithms/china_major_repository_lookup.md`, `algorithms/china_major_repository_ranking_reference.md`, `data/china_major_repository/metadata.yaml`, `data/china_major_repository/sources.yaml`, `schemas/china_major_repository_lookup_result.schema.json`. Use repository records and ShanghaiRanking/软科 references only as candidate or ranking-reference signals, then verify admissions facts with official current/next-cycle sources.
- China repository import or validation: `scripts/china_major_repository_import.py`, `algorithms/china_major_repository_import.md`, `algorithms/china_major_repository_validation.md`, `data/china_major_repository/import_mapping.yaml`, `schemas/china_major_repository_dataset.schema.json`, `schemas/china_university_major_record.schema.json`, `schemas/china_ranking_reference.schema.json`.
- Country comparison or terminology: `instructions/country_notes.md`, `algorithms/cross_country_alignment.md`, `data/country_terms.yaml`, `data/country_alignment_rules.yaml`, `data/major_aliases.yaml`, `schemas/cross_country_alignment.schema.json`, `workflows/multi_country_comparison_workflow.md`, `prompts/compare_majors.md`, `prompts/country_specific_research.md`.
- Similar majors and knowledge structure: `algorithms/major_similarity.md`, `algorithms/knowledge_graph.md`, `data/major_similarity_rules.yaml`, `schemas/major_similarity_result.schema.json`, `schemas/knowledge_graph_node.schema.json`, `schemas/knowledge_graph_edge.schema.json`.
- Change detection and reports: `algorithms/change_detection.md`, `algorithms/report_generation.md`, `data/change_detection_rules.yaml`, `workflows/change_detection_workflow.md`, `schemas/change_record.schema.json`.
- Safety or regulated pathways: `instructions/safety_and_uncertainty.md`, `data/regulated_fields.yaml`, `data/professional_accreditation_rules.yaml`.
- Executable validation or deterministic scoring checks: `scripts/algorithm_utils.py`, `scripts/eval_runner.py`, `scripts/validate_records.py`, `scripts/validate_skill.py`.
