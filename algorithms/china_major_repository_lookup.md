# china_major_repository_lookup

## 用途

`china_major_repository_lookup` 用于在本地中国大陆大学专业数据存储库中快速查找候选院校、候选本科专业、专业代码、专业类、学科门类、软科排名参考和待官方核验字段。

该算法只生成候选和参考，不生成最终招生结论。任何关于当前招生、分省计划、专业组、选科要求、学费、培养方案、录取要求或是否仍开设的结论，必须继续执行 current/next-cycle 官方检索、`source_scoring` 和 `claim_verification`。

## 触发场景

- 用户查询中国大陆某大学有哪些本科专业或某类相关专业；
- 用户查询某个本科专业有哪些中国大陆高校可关注；
- 用户要求参考软科 2025 中国大学专业排名做专业实力初筛；
- 用户要求在中国大陆范围内做专业推荐、院校候选池或专业对比；
- `intent_router` 判断国家为 China，且意图为 `university_program_lookup`、`admissions_lookup`、`recommend_majors`、`compare_majors`、`change_comparison` 或 `source_check`。

## 输入

- `user_query`；
- `schemas/admissions_scope.schema.json`；
- `schemas/china_university_major_record.schema.json`；
- `schemas/china_major_repository_dataset.schema.json`；
- `data/china_major_repository/metadata.yaml`；
- `data/china_major_repository/sample_records.yaml` 或用户授权导入的数据集；
- `data/china_major_repository/sources.yaml`；
- `data/major_aliases.yaml`；
- `data/country_terms.yaml`。

## 输出

输出必须符合 `schemas/china_major_repository_lookup_result.schema.json`，至少包含：

- 查询条件；
- 命中的候选专业记录；
- 排名参考记录；
- 需要官方核验的字段；
- 被拒绝或降级的记录；
- 来源 ID 和 claim ID；
- 局限说明。

## 核心步骤

1. 识别用户查询中的中国大陆院校、专业、专业类、学科门类、专业代码、省份、入学年份、选科、批次、招生路径和专业组。
2. 用 `major_aliases` 扩展专业关键词，例如“计算机相关”扩展到计算机科学与技术、软件工程、人工智能、数据科学与大数据技术、网络空间安全等。
3. 在本地库中按以下字段检索：
   - `university_name_zh` / `university_name_en`;
   - `major_name_zh` / `major_name_en`;
   - `major_code`;
   - `major_category`;
   - `discipline_category`;
   - `ranking_reference`;
   - `admissions_scope`;
   - `source_ids`。
4. 将命中结果分组：
   - `candidate_records`: 可作为候选池；
   - `ranking_references`: 只能作为专业实力参考；
   - `requires_official_verification`: 必须查官方 current/next-cycle 来源；
   - `rejected_records`: 年份、范围、来源或授权不满足要求。
5. 对每条候选记录标注 `record_usage`：
   - `candidate_only`：只作为候选；
   - `ranking_reference_only`：只作为第三方排名参考；
   - `official_verified_reference`：已有官方来源支持，但仍需按用户 scope 核验；
   - `historical_context`：只能作为历史背景。
6. 如果用户问题涉及当前招生、专业组、选科要求、分省计划或培养方案，调用 `china_admissions_scope_resolver` 检查 scope 完整度。
7. 将候选交给 `time_aware_retrieval` 和 `claim_verification`，不得直接输出为最终事实。

## 失败处理

- 如果本地库为空或没有授权数据，只说明“本地中国专业库暂无可用授权数据”，然后回退到官方检索。
- 如果只命中排名参考而没有官方招生来源，不得回答“当前开设”或“可以报考”。
- 如果缺少省份、入学年份、选科、批次或招生路径，不得给出分省计划、专业组或选科最终结论。
- 如果来源授权状态不明，记录只能用于内部结构测试，不得作为用户可见事实依据。

## 与其他算法的关系

- 上游：`intent_router`、`workflow_orchestrator`、`major_similarity`。
- 并行：`china_admissions_scope_resolver`。
- 下游：`time_aware_retrieval`、`hybrid_retrieval`、`source_scoring`、`claim_verification`、`uncertainty_management`、`recommendation_ranking`、`change_detection`。
