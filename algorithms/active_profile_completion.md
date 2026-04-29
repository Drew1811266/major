# active_profile_completion

## 用途

`active_profile_completion` 是 major 的主动用户画像补全算法。它用于在用户要求推荐专业、判断是否适合某专业、根据兴趣选择专业、比较专业选择时，动态选择“信息增益最大”的问题，而不是固定询问同一组问题。

初次最多问 5 个问题。问题必须根据当前用户输入、已知画像、任务类型和专业风险动态选择。

## 触发场景

1. 用户要求个性化推荐专业；
2. 用户要求判断自己是否适合某专业；
3. 用户根据兴趣选择专业；
4. 用户比较多个专业并要求选择建议；
5. 用户只给模糊兴趣，例如“我喜欢 AI”“我想学商科”“我喜欢心理学”；
6. 用户问题涉及作品集、临床、资格认证、编程、实验、长期读研等高风险因素。

## 输入

- 用户原始输入；
- 已有 `schemas/user_profile.schema.json`；
- `data/question_bank.yaml`；
- `data/scoring_weights.yaml` 中的 question_selection；
- intent_router 输出；
- 候选专业或专业类别；
- `data/major_task_profiles.yaml`；
- `data/constraint_rules.yaml`。

## 输出

- 缺失画像字段；
- 最多 5 个动态选择的问题；
- 每个问题的 question_score；
- 是否可以先给初步方向；
- 已知信息和判断边界；
- 继续推荐时必须标注的局限。

## 用户画像字段

需要逐步补全：target_countries、education_stage、academic_background、academic_strengths、academic_weaknesses、interests、preferred_tasks、disliked_tasks、career_preferences、language_profile、budget_level、risk_tolerance、constraints、priority_factors。

## 问题选择公式

```text
question_score =
  0.40 * decision_impact
+ 0.30 * uncertainty_reduction
+ 0.20 * field_importance
- 0.10 * user_burden_penalty
```

- `decision_impact`: 该问题的答案是否会显著改变推荐结果。
- `uncertainty_reduction`: 该问题是否能显著减少当前不确定性。
- `field_importance`: 该字段对当前任务是否重要。
- `user_burden_penalty`: 该问题是否太长、太私密、太复杂，或一次问太多造成负担。

## 核心步骤

1. 读取已知画像，标记已知字段和缺失字段。
2. 根据 intent 判断是否必须补全画像。
3. 根据候选专业类别读取 `major_task_profiles`，识别高风险学习任务。
4. 从 `question_bank` 中筛选适用问题。
5. 排除用户已经回答过的问题：
   - 如果用户已提供目标国家，不再问目标国家；
   - 如果用户已提供数学能力，不再问数学能力；
   - 如果用户已明确预算，不再重复问预算；
   - 如果用户已明确不接受某任务，把它作为约束，而不是再问。
6. 对每个候选问题计算 question_score。
7. 选择得分最高且不重复的最多 5 个问题。
8. 如果信息极少且用户只给模糊兴趣，先给 3-5 个初步方向，再反问。
9. 如果用户不愿补充信息，继续提供初步建议，但必须说明局限。

## 高风险优先确认规则

- AI/CS/数据：优先确认数学、编程、调试、长期项目接受度。
- 商科/金融/经济：优先确认数学、数据分析、就业竞争、实习压力接受度。
- 心理/医学/护理：优先确认统计、论文阅读、实验、临床、资格路径接受度。
- 设计/建筑：优先确认作品集、studio、长期迭代和空间能力。
- 法律/公共事务：优先确认大量阅读、写作、案例分析和国家资格差异。
- 工程：优先确认数学、物理、实验、项目和认证要求。

## 失败处理

- 用户画像严重不足：不得输出最终推荐，只输出初步方向和最多 5 个问题。
- 用户拒绝补充：继续回答，但标注“基于当前信息的初步判断”。
- 用户输入自相矛盾：指出冲突，例如“想学医学但完全不能接受长期学习和临床”。
- 用户要求确定结论：解释 major 不能在画像不足时严肃下定论。

## 与其他算法的关系

- 上游：`intent_router`、`workflow_orchestrator`。
- 下游：`major_fit_scoring`、`constraint_filtering`、`risk_scoring`、`recommendation_ranking`。
- 与 `preference_learning` 共享偏好和约束更新。
