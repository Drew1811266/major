# Recommend Majors Prompt

Recommend undergraduate majors based on the user profile.

User profile:
{{user_profile}}

## Personalization Algorithm

1. Run `active_profile_completion`.
   - If profile is incomplete, ask up to 5 dynamic questions.
   - If the user gives only vague interests, provide preliminary directions first, then ask questions.
2. Generate a candidate major pool from `major_taxonomy_seed`, `major_aliases`, and `major_task_profiles`.
3. If China mainland is a target, use `china_major_repository_lookup` only to expand candidate majors/universities; use ShanghaiRanking/软科 only as a secondary major-strength reference signal.
4. Run `constraint_filtering`.
   - Hard constraints can filter or downgrade.
   - Soft constraints adjust ranking.
5. Run `major_fit_scoring`.
   - Use interest, ability, study process, career goal, country system, and constraints.
6. Run `risk_scoring`.
   - Identify skill, study pressure, admission, employment, qualification, budget and language risks.
7. Run `preference_learning`.
   - Update weights from current user statements.
8. Run `recommendation_ranking`.
   - Group results into core recommendations, adjacent alternatives, cautious options, not recommended, and needs more information.

## Freshness Requirement

- Recommendation reasoning can use user profile and stable field knowledge.
- Any current claim about university programmes, admissions requirements, tuition, deadlines, course structures, accreditation, employment statistics, visa/work policy, or country-specific policy must use current/next-cycle or current/next academic-year official sources first. 2025-01-01 is only the minimum freshness floor.
- If no reliable current/next-cycle source is found, state that current information cannot be confirmed. If no source meeting the 2025-01-01 minimum floor is found, state: “我没有找到满足 2025 年及以后时效要求的可靠来源。”
- Do not use pre-2025 sources as current evidence unless historical context is explicitly requested.

## Source Priority

- Prefer official university, department, course catalog, admissions, government, exam authority, official application platform, accreditation body, and labor statistics sources.
- China mainland undergraduate admissions claims must prioritize current/next-cycle official sources and must confirm province, subject combination, intended entry year, and batch/pathway when those fields affect the conclusion.
- Local China repository records and ranking references are not official admissions evidence.
- Regulated pathways must include an official verification checklist covering regulator/body, accreditation status, clinical/practicum/internship requirement, exam or registration path, and applicable year or cycle.

## Claim Verification Requirement

- Verify factual recommendation claims before presenting them as evidence.
- If a recommendation depends on accreditation, employment data, visa, work policy, or qualification pathway, verify those claims and label uncertainty.

## Uncertainty Handling

- Mark recommendations as preliminary when profile information is missing.
- `high` evidence can support current claims; `medium` requires caveat; `low` is reference only; `unknown` must be stated as unable to confirm.
- Do not promise admission, employment, salary, visa, immigration, or professional qualification outcomes.

## Required Output

- 已知画像与判断边界；
- 最多 5 个需要补充的问题，如果必要；
- `core_recommendations`;
- `adjacent_alternatives`;
- `cautious_options`;
- `not_recommended`;
- `needs_more_information`;
- 每个推荐包含推荐理由、适合点、风险点、适合关注的国家或体系、替代专业、需要验证的信息、下一步行动建议；
- 对当前事实加入 source_id、currentness_basis、claim verification 和 uncertainty notes。
- 如果中国排名参考影响候选排序，标注其为第三方参考信号并解释局限。
