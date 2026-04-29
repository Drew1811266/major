# Change Detection Workflow

Use when the user asks how a major, programme, admissions rule, course structure, professional accreditation, or policy changed across years.

## Steps

```text
用户输入
→ 识别目标大学、专业、年份
→ 检索 old_source_set 和 new_source_set
→ source_scoring
→ 过滤不满足时效要求的来源
→ change_detection
→ claim_verification
→ uncertainty_management
→ 输出变化表、影响分析、来源说明
```

1. Identify target.
   - Country, university, major/programme, old year, new year.
   - Fields to compare: name, code, department, admissions catalog, enrollment plan, subject selection, major group, curriculum, tuition, accreditation, deadlines, policy.
   - For China mainland changes, identify admissions_scope: province, intended_entry_year, subject_combination, admissions_batch or application_route, major_group, enrollment_plan_scope, major_code, programme_code, and source_scope_type.
   - Do not compare national catalog, provincial exam authority data, university admissions catalog, provincial enrollment plan, major group, and training programme as the same scope. If scopes differ, write limitations.

2. Retrieve old and new sources.
   - Historical sources may be pre-2025 only when the user asks for historical comparison.
   - `new_source_set` must satisfy current/next-cycle official-source requirements first; 2025-01-01 is only the minimum floor.
   - For China mainland universities, prioritize current/next-cycle undergraduate admissions regulations, admissions brochures, major catalogs, provincial enrollment plans, subject selection requirements, professional groups, training programmes, university admissions sites, Ministry of Education, Sunshine College Entrance Examination Platform, provincial exam authorities, academic affairs office, and department sites.
   - Local China repository records may help identify candidate old/new fields, but change claims must compare compatible source scopes and must not treat ranking changes as admissions changes.

3. Score and filter sources.
   - Run `source_scoring` for both source sets.
   - Label old sources as historical where appropriate.
   - Reject archived/outdated pages as current evidence.
   - If `new_source_set` has no reliable current/next-cycle source, say current change cannot be confirmed and label any minimum-floor source as limited.

4. Run `change_detection`.
   - Detect added, removed, renamed, merged, split, moved_department, requirement_changed, enrollment_plan_changed, subject_selection_changed, curriculum_changed, tuition_changed, accreditation_changed, or unclear.
   - If comparing China repository data with official admissions data, label the repository as candidate/reference context and explain the scope mismatch.
   - Generate `schemas/change_record.schema.json`.

5. Verify claims and uncertainty.
   - Run `claim_verification` for each important change.
   - Run `uncertainty_management`.
   - Source conflicts must be visible in the output.

6. Output user impact.
   - Explain what the change means for application, subject selection, major group, training plan, fee, accreditation, or qualification path.
   - Give next official pages to check.

## Default Output

```markdown
## 变化结论摘要

## 变化表
| 变化对象 | 变化类型 | 旧值 | 新值 | 确定性 | 对用户影响 | 建议动作 |
|---|---|---|---|---|---|---|

## 来源表
| source_id | 来源 | 年份 | 类型 | 当前性依据 | 是否仅满足最低底线 | 支持 claim_id | 局限 |
|---|---|---|---|---|---|---|

## 无法确认或来源冲突的信息

## 下一步核查建议
```
