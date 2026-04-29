# Source Verification Workflow

Use when the user asks major to verify a program, summarize sources, check admissions facts, or answer time-sensitive factual questions about undergraduate majors.

## Workflow

```text
用户问题
→ 识别需要验证的具体事实
→ 生成 current/next-cycle + 2025 最低底线检索词
→ 执行 hybrid retrieval
→ 过滤不满足 current/next-cycle 或 2025-01-01 最低底线的来源
→ source_scoring
→ claim_verification
→ uncertainty_management
→ 输出来源表和可用结论
→ 标注无法确认或过期信息
```

## Steps

1. Identify facts that need verification.
   - programme_availability: 某大学是否开设某本科专业；
   - admissions_requirement: 录取要求；
   - course_structure: 课程结构；
   - tuition_fee: 学费；
   - deadline: 申请截止日期；
   - accreditation: 专业认证；
   - qualification_pathway: 资格路径；
   - employment_data: 就业数据；
   - country_system_rule: 国家专业体系规则；
   - change_claim: 年份变化；
   - recommendation_claim: 推荐理由。
   - For China mainland admissions claims, also identify admissions_scope fields: province, intended_entry_year, subject_combination, admissions_batch or application_route, major_group, enrollment_plan_scope, major_code, programme_code, and source_scope_type.
   - If the user asks about 中国大陆专业组、选科要求、分省招生计划或招生目录 and missing scope would change the conclusion, do not output a final current conclusion. Ask for the missing scope and provide only a limited explanation.

2. Generate currentness-aware search terms.
   - Prefer current/next admissions cycle, current/next entry year, current/next academic year, or active/current official pages.
   - Minimum freshness floor: 2025-01-01.
   - Use `data/major_aliases.yaml` for multilingual major names.
   - Use `data/country_terms.yaml` for local terminology.
   - China mainland examples:
     - 2025 本科招生章程
     - 2025 招生专业目录
     - 2025 分省招生计划
     - 2025 选考科目要求
     - 2025 专业组
     - 2025 培养方案
   - Overseas examples:
     - 2025 entry
     - 2026 entry
     - current undergraduate course
     - current undergraduate programme
     - 2025-2026 undergraduate catalog
     - latest course handbook
   - If a local China repository record is relevant, include its `source_id` and `record_id` only as secondary context; generate official verification terms from its university, major, province, year, and source scope.

3. Execute hybrid retrieval.
   - Run keyword retrieval.
   - Run semantic retrieval.
   - Run multilingual expansion.
   - Use official source entry points from `data/official_sources.yaml`.
   - Fuse candidate rankings with RRF.
   - Use MMR to reduce duplicate or same-platform results and improve source diversity.

4. Filter sources.
   - Keep current/next-cycle sources first; keep 2025-or-later minimum-floor sources only with limitations when not clearly current.
   - Keep official current active pages without archived/outdated marks.
   - Reject old admissions pages, archived pages, pre-2025 pages without 2025+ applicability, and unofficial sources without cross-validation.
   - Downgrade `ranking_reference` and `local_repository_record` sources when the claim is admissions, subject-selection, major-group, enrollment-plan, tuition, deadline, or training-programme related.
   - Record rejected sources in `schemas/retrieval_result.schema.json`.

5. Score sources.
   - Use `algorithms/source_scoring.md`.
   - Use the formula in `data/scoring_weights.yaml`.
   - Use country and source-type authority rules in `data/authority_source_rules.yaml`.
   - Record scores in `schemas/source_record.schema.json`.

6. Verify claims.
   - Use `algorithms/claim_verification.md`.
   - Every key claim must become a claim record in `schemas/claim_verification.schema.json`.
   - Every source must have source_id, and claims must keep supporting_source_ids or conflicting_source_ids.
   - Claims with `outdated` or `not_found` status cannot be output as certain current conclusions.

7. Manage uncertainty.
   - Use `algorithms/uncertainty_management.md`.
   - Assign high, medium, low, or unknown certainty.
   - high can be stated as current conclusion.
   - medium can be stated with limitations.
   - low is reference only.
   - unknown must be stated as unable to confirm.

8. Output source table and usable conclusions.
   - Answer in Chinese unless the user asks otherwise.
   - Summarize; do not paste long excerpts.
   - Include access date or verification date.
   - Explain source freshness.
   - Separate verified conclusions from uncertain, outdated, or unconfirmed information.
   - For China repository hits, include a note that repository and ranking records are candidate/reference signals and require official current/next-cycle confirmation.

## Default Source Table

```markdown
| Claim | 结论是否可用 | 来源 | 类型 | 时效依据 | source_score | 确定性 | 局限 |
|---|---|---|---|---|---:|---|---|
```

## Fallback

If no reliable current/next-cycle source is found, say current information cannot be confirmed. If no source meeting the 2025-01-01 minimum floor is found, say:

> 我没有找到满足 2025 年及以后时效要求的可靠来源。

Do not silently substitute pre-2025 information. If the user explicitly accepts historical background, label older sources as historical/outdated and do not present them as current facts.
