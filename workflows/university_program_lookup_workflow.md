# University Program Lookup Workflow

Use when the user asks about a specific university, undergraduate programme, admissions requirement, tuition, deadline, course catalog, subject requirement, major list, or China mainland招生专业/专业组/分省计划.

## Steps

0. Run algorithms.
   - `intent_router`
   - `workflow_orchestrator`
   - `china_admissions_scope_resolver` for China mainland admissions scope.
   - `china_major_repository_lookup` for China mainland candidate major lookup, when useful.
   - `china_major_repository_ranking_reference` if the user asks which universities are strong in a major or explicitly mentions ShanghaiRanking/软科.
   - `time_aware_retrieval`
   - `hybrid_retrieval`
   - `source_scoring`
   - `claim_verification`
   - `uncertainty_management`

1. Confirm target scope.
   - University
   - Country
   - Undergraduate level
   - Programme or major
   - Admissions cycle or entry year
   - For China mainland admissions: province, intended entry year, subject combination, admissions batch or application route, major group if applicable, and enrollment plan scope.
   - If the user asks about 中国大陆专业组、选科要求、分省计划或招生目录 and one of these fields is missing, ask for the missing scope before giving a final current conclusion.

2. Apply freshness rules.
   - Prefer current or next admissions cycle.
   - Minimum floor: 2025-01-01.
   - For China mainland, prioritize current/next-cycle official admissions regulations, major catalogs, enrollment plans, subject selection requirements, professional groups, training programmes, university admissions sites, Ministry of Education, Sunshine College Entrance Examination Platform, and provincial exam authorities.

3. Use China repository only as candidate support.
   - If the target country is China, query `data/china_major_repository/` to create a preliminary candidate list.
   - Treat `local_repository_record` and `ranking_reference` as secondary evidence only.
   - Do not answer "currently admits", "can apply", "subject requirements", "major group", "provincial plan", "tuition", or "deadline" from repository records alone.

4. Retrieve official sources.
   - University official programme page.
   - Department or faculty page.
   - Course catalog or handbook.
   - Admissions page.
   - Accreditation or regulator page if relevant.

5. Score and verify.
   - Use `source_scoring`.
   - Verify every key claim with `claim_verification`.
   - Mark uncertain claims with `uncertainty_management`.

6. Output.
   - Answer in Chinese.
   - Include source table.
   - State freshness basis and limitations.
   - Do not guarantee admission, fees, deadlines, visa, employment, migration, or qualification outcomes.
   - For ranking references, state that rankings are third-party major-strength references and not admissions evidence.

## Source Table

```markdown
| 结论 | 来源 | 来源类型 | 时效依据 | 确定性 | 局限 |
|---|---|---|---|---|---|
```
