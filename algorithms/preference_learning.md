# preference_learning

## 用途

`preference_learning` 是 major 的轻量偏好学习算法。它根据多轮对话中的用户反馈，更新用户偏好、硬约束、软约束和推荐权重，但不把一次反馈过度泛化为永久结论。

## 触发场景

- 用户表达喜欢、不喜欢、不能接受、优先考虑；
- 用户否定某个推荐；
- 用户修正目标，例如“我更看重就业”“我不想学太多数学”；
- 用户对专业价值观表达偏好，例如“不喜欢金融，感觉太功利”。

## 输入

- 用户新陈述；
- 当前 `schemas/user_profile.schema.json`；
- `data/preference_rules.yaml`；
- 历史 preference_history；
- 当前推荐结果。

## 输出

符合 `schemas/user_preference_update.schema.json` 的更新记录：

- user_statement；
- inferred_preference；
- affected_weights；
- affected_major_categories；
- hard_or_soft_constraint；
- confidence；
- update_reason。

## 示例规则

用户说“我不喜欢金融，感觉太功利”：

- 降低 income 和 business prestige 权重；
- 提高 interest、social impact、creativity 权重；
- 降低 finance 类推荐优先级。

用户说“我不想学太多数学”：

- 降低数学密集型专业；
- 提高信息系统、传媒、教育、管理、设计、社会科学等备选方向；
- 但不能绝对排除，除非用户表达为硬约束。

用户说“我更看重就业”：

- 提高 clear_employment_path、internship_opportunity、market_demand 权重；
- 对就业路径不清晰的专业增加风险提示。

## 核心步骤

1. 判断用户反馈是偏好、软约束还是硬约束。
2. 提取受影响权重和专业类别。
3. 判断置信度：
   - “完全不能接受”“绝对不想”通常为硬约束；
   - “不太喜欢”“希望少一点”通常为软约束；
   - 情绪性表达需要中等或低置信度。
4. 写入 preference_history。
5. 更新 inferred_hard_constraints 或 inferred_soft_constraints。
6. 触发 `constraint_filtering` 和 `recommendation_ranking` 重排。

## 失败处理

- 用户表达含糊：记录为低置信度软偏好，不直接过滤专业。
- 与历史偏好冲突：提示用户确认，而不是自动覆盖。
- 涉及价值判断：保持中立，不贬低专业，只调整匹配逻辑。

## 与其他算法的关系

- 上游：用户反馈、对话历史。
- 下游：`constraint_filtering`、`major_fit_scoring`、`risk_scoring`、`recommendation_ranking`。
