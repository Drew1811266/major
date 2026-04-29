# major_fit_scoring

## 用途

`major_fit_scoring` 用于评估某个本科专业或专业方向与用户画像的适配程度。它不是为了给出绝对分数，而是为了让推荐理由可解释、可追溯，并帮助 major 说明适合点、薄弱点、假设和需要补充的信息。

## 触发场景

- 推荐专业；
- 判断用户是否适合某专业；
- 根据兴趣选择专业；
- 比较多个专业的选择优先级；
- 输出 core_recommendations、adjacent_alternatives、cautious_options 等推荐分组。

## 输入

- `schemas/user_profile.schema.json`；
- 候选专业池；
- `data/major_task_profiles.yaml`；
- `data/scoring_weights.yaml`；
- `data/constraint_rules.yaml`；
- 目标国家或国家范围；
- 已验证来源的 certainty，如果涉及具体事实。

## 输出

输出应符合 `schemas/recommendation_score.schema.json`，至少包括：

- `fit_level`: high / medium / cautious / low；
- `fit_score`；
- `strongest_fit_reasons`；
- `weakest_fit_reasons`；
- `assumptions`；
- `missing_profile_fields`；
- `what_could_change_the_score`。

## 评分公式

```text
fit_score =
  0.30 * interest_match
+ 0.20 * ability_match
+ 0.15 * study_process_match
+ 0.15 * career_goal_match
+ 0.10 * country_system_match
+ 0.10 * constraint_match
```

## 评分项解释

- `interest_match`: 用户真实兴趣是否匹配该专业的核心任务，而不是只匹配专业名称或行业光环。
- `ability_match`: 用户的数学、编程、写作、阅读、实验、艺术、沟通、记忆、空间、逻辑、外语等能力是否支持该专业。
- `study_process_match`: 用户是否接受本科阶段真实学习过程，例如编程、统计、论文阅读、实验、studio、作品集、临床训练、案例分析等。
- `career_goal_match`: 专业是否匹配用户的就业、收入、稳定性、科研、创业、国际化、公共服务、创造性等目标。
- `country_system_match`: 该专业在目标国家的本科体系中是否存在合适路径，名称和结构是否匹配。
- `constraint_match`: 是否符合预算、语言、家庭意见、城市偏好、考试科目、身体条件、签证、资格认证等限制。

## fit_level

- `high`: fit_score >= 0.78，且没有明显硬约束冲突；
- `medium`: 0.60 <= fit_score < 0.78，适合探索但需要验证关键条件；
- `cautious`: 0.42 <= fit_score < 0.60，存在明显风险或信息缺口；
- `low`: fit_score < 0.42，或被硬约束显著降级。

## 核心步骤

1. 读取用户画像和候选专业任务画像。
2. 为每个候选专业计算六个分项。
3. 根据硬约束和软约束调整 constraint_match。
4. 生成 strongest_fit_reasons 和 weakest_fit_reasons。
5. 标注 assumptions 和 missing_profile_fields。
6. 说明 what_could_change_the_score，例如“如果你不能接受大量数学，该方向会降级”。
7. 把评分交给 `risk_scoring` 和 `recommendation_ranking`。

## 失败处理

- 画像不足：输出 `fit_level = cautious` 或标记需要更多信息，调用 `active_profile_completion`。
- 专业任务画像缺失：使用相近专业类别估计，并说明假设。
- 涉及当前项目事实：必须调用 current/next-cycle retrieval 和 claim verification；2025-01-01 只是最低时效底线。
- 不得把 fit_score 包装成科学测评或确定结论。

## 与其他算法的关系

- 上游：`active_profile_completion`、`constraint_filtering`。
- 并行：`risk_scoring`。
- 下游：`recommendation_ranking`。
