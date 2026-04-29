# risk_scoring

## 用途

`risk_scoring` 用于评估候选本科专业对用户的风险水平。它补充 fit_score：一个专业可能很有兴趣匹配，但如果学习压力、资格路径、预算或语言风险过高，推荐时必须降级或加警示。

## 触发场景

- 个性化专业推荐；
- 适配度判断；
- 用户有明显弱项或排斥任务；
- 候选专业涉及高数学、编程、实验、作品集、临床、读研、执照或高成本国家；
- 用户看重就业、稳定、预算或低风险。

## 输入

- `schemas/user_profile.schema.json`；
- `data/major_task_profiles.yaml`；
- `data/constraint_rules.yaml`；
- `data/scoring_weights.yaml`；
- 候选专业的 fit_score 和约束结果；
- 若涉及事实，来源 certainty。

## 输出

- `risk_level`: low / medium / high；
- `risk_score`；
- `top_risks`；
- `mitigation_strategies`；
- `warnings`；
- `verification_needed`。

## 风险评分公式

```text
risk_score =
  0.25 * skill_gap_risk
+ 0.20 * study_pressure_risk
+ 0.20 * admission_risk
+ 0.15 * employment_uncertainty_risk
+ 0.10 * qualification_risk
+ 0.10 * budget_or_language_risk
```

## 风险项解释

- `skill_gap_risk`: 用户能力与专业要求之间的差距。
- `study_pressure_risk`: 本科阶段学习压力是否与用户偏好冲突。
- `admission_risk`: 申请难度、先修要求、作品集、选科要求、语言要求等风险。
- `employment_uncertainty_risk`: 本科毕业后的就业路径是否不确定，是否需要研究生或额外实习。
- `qualification_risk`: 是否涉及执照、资格认证、临床训练、法律资格、教师资格、心理咨询执照等。
- `budget_or_language_risk`: 预算、语言、国家选择带来的风险。

## risk_level

- `low`: risk_score < 0.35；
- `medium`: 0.35 <= risk_score < 0.65；
- `high`: risk_score >= 0.65，或命中重大硬约束。

## 核心步骤

1. 读取专业任务画像和用户画像。
2. 识别用户弱项与专业要求差距。
3. 判断学习过程是否与用户 disliked_tasks 冲突。
4. 检查申请、作品集、先修、语言、预算和国家路径风险。
5. 检查就业路径、读研依赖和资格认证风险。
6. 计算 risk_score 和 risk_level。
7. 生成 mitigation_strategies，例如先修课程、项目体验、国家替代、相邻专业、官方核验。

## 失败处理

- 画像不足：列入 verification_needed 或 missing_profile_fields，不臆测风险。
- 风险依赖最新事实：调用 current/next-cycle retrieval 和 claim_verification；2025-01-01 只是最低时效底线。
- 高风险但用户强烈偏好：保留为 cautious_options，不直接否定。

## 与其他算法的关系

- 上游：`constraint_filtering`、`major_fit_scoring`。
- 下游：`recommendation_ranking`。
- 与 `uncertainty_management` 共同决定风险提示强度。
