# workflow_orchestrator

## 用途

`workflow_orchestrator` 根据 `intent_router` 的结果选择工作流、算法序列、必需输入、缺失信息和失败处理策略。输出必须符合 `schemas/algorithm_decision.schema.json`。

## 触发场景

在 `intent_router` 完成后触发。每个用户请求都应经过一次编排。

## 输入

- `schemas/intent_result.schema.json`；
- 可选用户画像；
- 已有来源记录；
- 当前对话上下文；
- `data/algorithm_registry.yaml`。

## 输出

符合 `schemas/algorithm_decision.schema.json` 的对象。

## 工作流选择

| intent | selected_workflow |
|---|---|
| `explain_major` | `major_explanation_workflow` |
| `compare_majors` | `major_explanation_workflow` 或 `multi_country_comparison_workflow` |
| `compare_countries` | `multi_country_comparison_workflow` |
| `recommend_majors` | `major_recommendation_workflow` |
| `evaluate_fit` | `major_recommendation_workflow` |
| `university_program_lookup` | `university_program_lookup_workflow` |
| `admissions_lookup` | `university_program_lookup_workflow` |
| `source_check` | `source_verification_workflow` |
| `change_comparison` | `change_detection_workflow` |
| `report_generation` | 根据内容选择 explanation、recommendation 或 comparison workflow |
| `unclear` | 先澄清范围 |

## 核心步骤

1. 读取 intent、置信度和触发标记。
2. 选择一个主工作流。
3. 选择必须运行的算法：
   - 所有任务：`intent_router`、`workflow_orchestrator`、`uncertainty_management`；
   - 具体事实：`time_aware_retrieval`、`hybrid_retrieval`、`source_scoring`、`claim_verification`；
   - 推荐/适配：`active_profile_completion`、`major_fit_scoring`、`constraint_filtering`；
   - 跨国比较：`cross_country_alignment`；
   - 年份变化：`change_detection`；
   - 多专业比较：`major_similarity`。
4. 判断是否先反问用户。
5. 判断是否可以先给初步建议再反问。
6. 判断是否必须先检索。
7. 生成输出格式建议：表格、报告、咨询建议、来源摘要或分层推荐。

## 何时先反问用户

- 用户要求个性化推荐或适配判断，但缺少目标国家、年级/课程体系、擅长科目、兴趣、不喜欢任务、职业偏好等关键画像。
- 用户只说“我不知道选什么专业”“商科哪个好”“我喜欢 AI”，且没有任何背景。
- 用户要求比较，但没有说明比较对象或国家范围。

初次反问最多 5 个问题。

## 何时先给初步建议再反问

- 用户给了兴趣方向但画像不足；
- 用户焦虑选专业，希望先看到方向；
- 可以给 3-5 个暂定方向，并明确“基于当前信息，结论暂定”。

## 何时必须先检索

- 具体大学项目；
- 招生、录取、学费、截止日期、选科要求；
- 课程目录、专业认证；
- 就业数据、签证、工签、移民、政策变化；
- 中国大陆高校本科招生专业、专业组、分省计划、培养方案。

## 何时不得使用旧来源

- 用户要求“现在、今年、最新、当前、当前招生周期、下一招生周期、2025 年及以后”；
- 当前或下一招生周期信息存在；
- 来源为 archived、过期页面、中介宣传或未注明出处内容。

## 何时输出“不确定”

- 找不到可靠 current/next-cycle 来源；
- 只找到满足 2025-01-01 最低底线但无法确认当前/下一周期适用的来源；
- 来源之间冲突；
- 用户画像不足但用户要求强结论；
- 专业资格、签证、移民或就业结论缺少官方证据。

## 何时调用 claim_verification

- 回答中包含大学项目、招生、课程、费用、截止日期、认证、就业数据、签证、资格路径；
- 需要反驳或核查某个来源；
- 需要比较年份变化；
- 结论会影响用户重大教育或职业决策。

## 失败处理

- 意图不清：输出澄清问题和可选范围。
- 缺少画像：运行 `active_profile_completion`。
- 缺少来源：说明没有可靠来源，不编造。
- 来源冲突：列出冲突点并降低确定性。

## 与其他算法的关系

- 上游：`intent_router`。
- 下游：所有 workflow 和算法。
- 与 `uncertainty_management` 配合决定回答边界。
