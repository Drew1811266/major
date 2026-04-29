# Recommendation Rules

## 目录

- 推荐前置步骤
- 专业适配度评分
- 风险评分
- 约束过滤
- 轻量偏好学习
- 推荐排序
- 推荐输出要求
- 不得过度承诺

major 的专业推荐不是简单列专业名称，而是基于用户画像、专业真实学习任务、国家体系、硬软约束、风险和来源确定性的咨询式判断。推荐结果必须可解释、可追溯、不过度承诺。

## 推荐前置步骤

推荐专业、判断适配度、根据兴趣选专业、比较专业选择时，必须先执行：

1. `intent_router` 判断是否为推荐、适配或专业选择类问题。
2. `active_profile_completion` 判断用户画像是否足够。
3. 信息不足时，最多问 5 个动态问题；可以同时给初步方向。
4. 生成候选专业池。
5. 执行 `constraint_filtering`、`major_fit_scoring`、`risk_scoring`、`preference_learning` 和 `recommendation_ranking`。
6. 如果用户主要关注中国大陆院校，可以运行 `china_major_repository_lookup` 扩展候选院校或专业；本地库和软科排名只作为候选池/专业实力参考，不能覆盖用户画像、硬约束、适配度、风险或官方招生核验。
7. 如涉及具体大学项目、录取要求、课程设置、学费、截止日期、专业认证、就业数据、签证或政策，调用 current/next-cycle 检索、来源评分、声明验证和不确定性标注；2025-01-01 只是最低时效底线。

## 专业适配度评分

使用 `algorithms/major_fit_scoring.md`：

```text
fit_score =
  0.30 * interest_match
+ 0.20 * ability_match
+ 0.15 * study_process_match
+ 0.15 * career_goal_match
+ 0.10 * country_system_match
+ 0.10 * constraint_match
```

评分项含义：

- `interest_match`: 用户真实兴趣是否匹配专业核心任务，而不是只匹配专业名称或行业光环。
- `ability_match`: 数学、编程、写作、阅读、实验、艺术、沟通、记忆、空间、逻辑、外语等能力是否支持该专业。
- `study_process_match`: 用户是否接受本科阶段真实学习过程，例如编程、统计、论文阅读、实验、studio、作品集、临床训练、案例分析等。
- `career_goal_match`: 专业是否匹配就业、收入、稳定、科研、创业、国际化、公共服务、创造性等目标。
- `country_system_match`: 专业在目标国家本科体系中是否存在合适路径，名称和结构是否匹配。
- `constraint_match`: 是否符合预算、语言、家庭意见、城市偏好、考试科目、身体条件、签证、资格认证等限制。

输出不得只给分数，必须给 `fit_level`、核心理由、弱点、假设、缺失字段和哪些信息会改变判断。

## 风险评分

使用 `algorithms/risk_scoring.md`：

```text
risk_score =
  0.25 * skill_gap_risk
+ 0.20 * study_pressure_risk
+ 0.20 * admission_risk
+ 0.15 * employment_uncertainty_risk
+ 0.10 * qualification_risk
+ 0.10 * budget_or_language_risk
```

必须说明：

- `risk_level`: low / medium / high；
- 主要风险；
- 降低风险的策略；
- 需要核查的信息；
- 对执照、临床、资格、签证和就业数据的官方核实提醒。

## 约束过滤

使用 `algorithms/constraint_filtering.md` 区分硬约束和软约束。

硬约束示例：

- 完全不能接受作品集；
- 完全不能接受大量编程；
- 完全不能接受大量数学；
- 预算无法支持目标国家；
- 不能接受长期读研，但目标职业通常需要研究生或执照；
- 目标国家没有合适本科路径；
- 不满足关键先修或选科要求。

软约束示例：

- 希望高收入；
- 希望稳定；
- 希望创造性；
- 希望申请难度较低；
- 希望本科毕业后就业；
- 希望国际化；
- 希望少写论文；
- 希望少做实验。

硬约束优先于软约束。软约束用于调整排序，不应直接排除专业，除非用户明确表达为绝对不能接受。

## 偏好学习

使用 `algorithms/preference_learning.md` 在多轮对话中更新权重。

例子：

- 用户说“我不喜欢金融，感觉太功利”：降低 income 和 business prestige 权重，提高 interest、social impact、creativity 权重，降低 finance 类推荐优先级。
- 用户说“我不想学太多数学”：降低数学密集型专业，提高信息系统、传媒、教育、管理、设计、社会科学等备选方向；除非用户表达为硬约束，否则不能绝对排除。
- 用户说“我更看重就业”：提高 clear_employment_path、internship_opportunity、market_demand 权重；对就业路径不清晰的专业增加风险提示。

偏好更新应记录到 `schemas/user_preference_update.schema.json`，并在推荐解释中体现。

## 推荐排序

使用 `algorithms/recommendation_ranking.md`，结合：

- `fit_score`；
- `risk_score`；
- 硬/软约束；
- preference updates；
- country system match；
- source certainty；
- diversity。
- China repository candidate signals, when relevant, as secondary candidate-expansion signals only.

最终推荐分组：

- `core_recommendations`: 核心推荐；
- `adjacent_alternatives`: 相邻备选；
- `cautious_options`: 谨慎考虑；
- `not_recommended`: 不太建议；
- `needs_more_information`: 需要补充信息后判断。

推荐时不要只给专业名，必须给：

- 推荐理由；
- 适合点；
- 风险点；
- 适合关注的国家或体系；
- 替代专业；
- 需要验证的信息；
- 下一步行动建议。

## 常见兴趣拆解

- 喜欢 AI，不等于一定适合计算机科学；需要区分算法、软件工程、机器人、游戏、产品、商业应用、医学应用、伦理治理或数据分析。
- 喜欢心理学，不等于一定适合临床心理；本科常有统计、实验设计、论文阅读，咨询资格通常另有路径。
- 喜欢赚钱，不等于一定适合金融；金融常伴随竞争性实习、量化分析和压力。
- 喜欢画画，不等于一定适合建筑或设计；需要确认作品集、studio、长期项目迭代和就业风险。
- 喜欢医学，不等于一定能接受长期学习、资格认证和临床压力。

## 输出边界

- 推荐不得包装成绝对结论。
- 不要说“你一定适合”“肯定应该选”“这个专业未来一定高薪”。
- 不承诺录取、就业、薪资、签证、移民或职业资格结果。
- 不把热门、排名、高薪、移民传闻当作充分推荐理由。
- 涉及医学、法律、护理、心理咨询、建筑、工程认证、会计认证、教育资格、药学、社工等受监管路径时，必须提醒用户核实官方和专业监管机构要求。
