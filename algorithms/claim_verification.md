# claim_verification

## 用途

`claim_verification` 用于在 major 输出前，把关键结论拆成 claims，并逐条验证来源支持情况。它防止 major 把没有来源、来源过旧或来源冲突的信息作为确定事实输出。

## 触发场景

- 查询某大学是否开设某本科专业；
- 查询录取要求、课程结构、学费、截止日期；
- 查询专业认证、资格路径；
- 查询就业数据、签证、工签、政策变化；
- 比较年份变化；
- 核查来源或中介说法；
- 个性化推荐中包含事实性推荐理由。

## 输入

- 候选回答或待验证结论；
- 经过 `source_scoring` 的来源；
- 用户问题；
- 目标国家、大学、专业、年份；
- 招生或来源适用范围 `admissions_scope`，尤其是中国大陆省份、选科、入学年份、批次、专业组和来源口径；
- `schemas/claim_verification.schema.json`；
- `data/authority_source_rules.yaml`。

## 输出

符合 `schemas/claim_verification.schema.json` 的验证记录列表。

## claim 类型

- `programme_availability`: 某大学是否开设某本科专业；
- `admissions_requirement`: 录取要求；
- `course_structure`: 课程结构；
- `tuition_fee`: 学费；
- `deadline`: 申请截止日期；
- `accreditation`: 专业认证；
- `qualification_pathway`: 资格路径；
- `employment_data`: 就业数据；
- `country_system_rule`: 国家专业体系规则；
- `change_claim`: 年份变化；
- `recommendation_claim`: 推荐理由。

## claim 状态

每个 claim 的状态必须是以下之一：

- `supported`: current/next-cycle 可靠来源直接支持；若只满足 2025 最低底线，需要在 certainty 中降级或标注 limited；
- `partially_supported`: 来源可靠但只支持部分结论，或缺少关键字段；
- `conflicting`: 可靠来源之间存在冲突；
- `not_found`: 未找到可靠来源；
- `outdated`: 只找到过旧来源，且不适用于 2025-01-01 最低底线或当前/下一周期；
- `uncertain`: 来源间接、弱或无法充分判断。

如果 claim 是 `outdated` 或 `not_found`，不得作为确定结论输出。

## 核心步骤

1. 把候选回答拆成原子 claims。
2. 为每条 claim 标注 claim_type、entities、country、year 和 required_source_type。
3. 标注 admissions_scope。中国大陆招生目录、专业组、选科要求或分省计划 claim 必须明确省份、入学年份、选科、批次/路径、专业组或来源口径；缺失时不得作为最终当前结论。
4. 匹配支持来源和冲突来源。事实来源表是唯一权威事实表，claim 使用 supporting_source_ids 和 conflicting_source_ids 引用来源；嵌入 supporting_sources/conflicting_sources 只作为兼容快照。
5. 检查支持来源是否满足 current/next-cycle 当前性要求；2025-01-01 仅作为最低底线。
6. 检查来源类型是否满足 claim 的最低要求。
7. 给出 verification_status 和 certainty_level。
8. 设置 `output_allowed`：
   - `supported`: true；
   - `partially_supported`: true，但必须说明限制；
   - `conflicting`: false，除非输出为冲突说明；
   - `not_found`: false；
   - `outdated`: false，除非用户要求历史背景；
   - `uncertain`: true 仅可作为低确定性参考。
9. 生成 user_visible_note，用于最终回答。

## 失败处理

- 无来源支持：`verification_status = not_found`，输出“无法确认”。
- 只有 2024 或更早来源：`verification_status = outdated`，不作为当前事实。
- 来源冲突：`verification_status = conflicting`，列出差异并降低确定性。
- 只有间接来源：`verification_status = partially_supported` 或 `uncertain`。

## 与其他算法的关系

- 上游：`source_scoring`。
- 下游：`uncertainty_management` 和最终回答。
- 与 `source_record` 和 `retrieval_result` 共同构成事实可靠性链路。
