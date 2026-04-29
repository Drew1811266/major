# Major Recommendation Workflow

Use when the user asks what undergraduate major to choose, whether a major fits them, how to map interests to majors, or how to compare majors for a personal decision.

## Trigger

- `intent_router` returns `recommend_majors`, `evaluate_fit`, or a `compare_majors` request with personal decision criteria.
- The user says they like an interest area but does not know which本科专业 to choose.
- The user compares majors and asks “哪个更适合我”.

## Workflow

```text
用户输入
→ intent_router 判断是否推荐类问题
→ 读取已有 user_profile
→ active_profile_completion 判断缺失字段
→ 如果缺失严重，提出最多 5 个问题，同时给初步方向
→ 生成候选专业池
→ constraint_filtering
→ major_fit_scoring
→ risk_scoring
→ preference_learning 更新偏好
→ recommendation_ranking
→ 如涉及具体事实，调用 current/next-cycle retrieval 和 claim_verification
→ 输出推荐结果
```

## Step Details

1. Identify intent and scope.
   - Confirm the task is本科专业 recommendation, fit assessment, or major choice.
   - Keep scope undergraduate unless the user explicitly asks about graduate study.
   - Detect countries among China, South Korea, Japan, United Kingdom, United States, and Australia.

2. Read or construct `user_profile`.
   - Use `schemas/user_profile.schema.json`.
   - Preserve known facts from prior turns.
   - Record preference updates, hard constraints, soft constraints, missing fields, and profile completeness.

3. Run `active_profile_completion`.
   - Use `data/question_bank.yaml` and `data/scoring_weights.yaml`.
   - Ask at most 5 initial questions.
   - Do not repeat known information.
   - If input is vague, first give 3-5 preliminary directions with risks, then ask the highest-value questions.

4. Generate candidate major pool.
   - Use `data/major_taxonomy_seed.yaml`, `data/major_aliases.yaml`, and `data/major_task_profiles.yaml` as seeds.
   - Do not treat seed data as final factual evidence about a specific university or country.
   - If the user primarily considers China mainland, use `china_major_repository_lookup` to expand candidate universities or majors, but only as candidate support.
   - Treat ShanghaiRanking/软科 references as secondary major-strength signals, not as admissions or fit evidence.

5. Run `constraint_filtering`.
   - Apply hard constraints before scoring.
   - Use `data/constraint_rules.yaml`.
   - Downgrade or exclude majors with unresolved hard conflicts.
   - Treat soft constraints as ranking adjustments, not automatic exclusions.

6. Run `major_fit_scoring`.
   - Score interest, ability, study process, career goal, country system, and constraints.
   - Return `fit_score`, `fit_level`, strongest fit reasons, weakest fit reasons, assumptions, missing fields, and what could change the score.

7. Run `risk_scoring`.
   - Score skill gap, study pressure, admission risk, employment uncertainty, qualification risk, and budget/language risk.
   - Return `risk_score`, `risk_level`, top risks, mitigation strategies, warnings, and verification needed.

8. Run `preference_learning`.
   - Convert new user feedback into `schemas/user_preference_update.schema.json`.
   - Adjust ranking weights without silently overwriting user-stated constraints.
   - If preference inference is uncertain, label it and ask for confirmation.

9. Run `recommendation_ranking`.
   - Group results into `core_recommendations`, `adjacent_alternatives`, `cautious_options`, `not_recommended`, and `needs_more_information`.
   - Preserve diversity across professional, technical, business, creative, and social-science alternatives when appropriate.

10. Verify current facts when needed.
   - For specific university programmes, admissions requirements, tuition, deadlines, course structures, accreditation, employment statistics, visa/work policy, or China mainland admissions major lists, run `time_aware_retrieval`, `hybrid_retrieval`, `source_scoring`, `claim_verification`, and `uncertainty_management`.
   - Default to current/next-cycle official sources; 2025-01-01 is only the minimum freshness floor.
   - For China mainland admissions, run `china_admissions_scope_resolver` and verify official current/next-cycle sources before stating whether a candidate is currently admitting or available to the user's province/subject combination.

## Default Output

```markdown
## 已知画像与判断边界

## 还需要确认的信息

## 初步或最终推荐分组
| 分组 | 专业方向 | 适合国家/体系 | 适合点 | 主要风险 | 替代专业 | 下一步 |
|---|---|---|---|---|---|---|

## 核心推荐

## 相邻备选

## 谨慎考虑或暂不建议

## 需要用当前/下一周期来源验证的信息

## 下一步行动建议
```

## Failure Handling

- If profile is insufficient: ask up to 5 questions and mark all recommendations as preliminary.
- If hard constraints conflict with all candidates: explain the conflict and suggest adjacent alternatives.
- If current factual claims cannot be verified: say the claim cannot be confirmed with reliable current/next-cycle sources; label any 2025 minimum-floor sources as limited.
- If user asks for a recommendation without answering questions: provide broad directions only and state limitations.
