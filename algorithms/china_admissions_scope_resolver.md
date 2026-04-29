# china_admissions_scope_resolver

## 用途

`china_admissions_scope_resolver` 用于解析中国大陆招生相关问题的适用范围，防止把全国专业目录、省级考试院数据、高校招生目录、分省招生计划、专业组、选科要求和培养方案混为同一事实。

## 触发场景

- 用户查询中国大陆高校本科招生专业；
- 用户查询专业组、选科要求、分省招生计划、招生章程、招生简章；
- 用户问“我这个省/选科能不能报某校某专业”；
- 用户比较 2025 与 2026 招生目录或专业组变化；
- `china_major_repository_lookup` 命中候选记录但需要转入官方核验。

## 输入

- `user_query`；
- `schemas/admissions_scope.schema.json`；
- `schemas/user_profile.schema.json`；
- `data/question_bank.yaml`；
- `data/source_priority.yaml`；
- `data/change_detection_rules.yaml`。

## 输出

- 标准化 `admissions_scope`；
- 缺失字段列表；
- 是否允许输出最终结论；
- 需要反问的问题；
- 后续检索关键词。

## 核心步骤

1. 从用户输入和用户画像中提取：
   - 省份或考试地区；
   - 目标入学年份；
   - 招生周期；
   - 选科组合；
   - 高考类型；
   - 批次；
   - 申请路径；
   - 专业组；
   - 分省计划口径；
   - 专业代码或院校专业组代码。
2. 判断问题类型：
   - 全国专业目录；
   - 高校招生目录；
   - 分省招生计划；
   - 选科要求；
   - 专业组；
   - 培养方案；
   - 软科或第三方排名参考。
3. 对高风险招生事实检查必填 scope：
   - 分省计划：省份、入学年份、批次或路径；
   - 选科要求：省份、入学年份、选科组合；
   - 专业组：省份、入学年份、批次或路径；
   - 当前招生状态：入学年份或招生周期；
   - 变化比较：old year、new year、source scope type。
4. 如果 scope 不完整，最多提出关键问题，不输出最终招生结论。
5. 生成官方检索关键词，例如：
   - `2026 <大学> 招生专业目录 <省份>`;
   - `2026 <大学> <省份> 专业组`;
   - `2026 <省份> 选考科目要求 <大学> <专业>`;
   - `2026 分省招生计划 <大学> <专业>`。

## 失败处理

- 缺少省份或入学年份：只能输出范围说明和需要补充的信息。
- 用户只提供专业排名问题：不要要求完整招生 scope，但要提示排名不等于可报考。
- 官方来源口径不一致：标注 limitations，不合并成单一结论。
- 用户拒绝补充信息：继续给通用核查路径和候选方向，明确不能判断可报考。

## 与其他算法的关系

- 上游：`intent_router`、`active_profile_completion`、`china_major_repository_lookup`。
- 下游：`time_aware_retrieval`、`hybrid_retrieval`、`claim_verification`、`change_detection`。
- 与 `source_verification_workflow` 和 `university_program_lookup_workflow` 共同保证中国大陆招生事实的 scope 正确。
