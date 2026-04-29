# recommendation_ranking

## 用途

`recommendation_ranking` 用于把候选专业按照适配度、风险、约束、偏好更新、国家体系匹配、来源确定性和多样性进行最终分组排序。

## 触发场景

- 输出 Top 3-5 推荐专业；
- 比较多个候选专业；
- 用户多轮反馈后重新排序；
- 需要区分核心推荐、相邻备选、谨慎考虑和不推荐。

## 输入

- 候选专业池；
- `recommendation_score`；
- `risk_scoring` 输出；
- `constraint_filtering` 输出；
- `preference_learning` 更新；
- source certainty；
- 国家体系匹配；
- diversity 要求。

## 输出

最终推荐分组：

- `core_recommendations`: 核心推荐；
- `adjacent_alternatives`: 相邻备选；
- `cautious_options`: 谨慎考虑；
- `not_recommended`: 不太建议；
- `needs_more_information`: 需要补充信息后判断。

每个推荐必须包含：

- 推荐理由；
- 适合点；
- 风险点；
- 适合关注的国家或体系；
- 替代专业；
- 需要验证的信息；
- 下一步行动建议。

## 排序逻辑

综合考虑：

- fit_score；
- risk_score；
- hard constraints；
- soft constraints；
- preference updates；
- country system match；
- source certainty；
- diversity。

原则：

- 高 fit、低 risk、无硬约束冲突 → core_recommendations；
- 中高 fit、有可管理风险 → adjacent_alternatives；
- fit 尚可但风险高或事实不确定 → cautious_options；
- 命中硬约束或与用户核心目标冲突 → not_recommended；
- 画像缺失导致无法判断 → needs_more_information。

## 多样性规则

不要让 Top 推荐全部来自同一专业簇。除非用户明确只想看某一类，否则应在核心推荐和相邻备选中保留不同路径，例如技术、数据、商业、社会科学、设计或公共事务方向。

## 核心步骤

1. 收集每个候选专业的 fit_score、risk_score、约束状态和偏好更新。
2. 过滤或降级硬约束冲突项。
3. 用软约束调整排序。
4. 对高风险、低 certainty 或受监管路径降级。
5. 应用多样性规则。
6. 分配 recommendation_group。
7. 生成用户可读解释和下一步行动建议。

## 失败处理

- 候选全部被过滤：输出 needs_more_information 或建议放宽约束。
- 来源确定性低：不把当前事实作为推荐理由。
- 用户画像不足：输出初步排序，并说明缺失字段会改变结果。
- 不得把推荐包装成绝对结论。

## 与其他算法的关系

- 上游：`constraint_filtering`、`major_fit_scoring`、`risk_scoring`、`preference_learning`。
- 下游：最终推荐回答。
