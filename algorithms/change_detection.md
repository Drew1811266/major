# change_detection

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 变化类型
- 中国大陆比较口径
- 核心步骤
- 失败处理
- 与其他算法的关系

## 用途

`change_detection` 用于对比不同年份的大学本科专业、招生目录、招生计划、选科要求、专业组、培养方案、课程结构、学费、认证要求和政策变化。它特别支持中国大陆高校每年变化的本科招生场景。

## 触发场景

- 用户问“这几年变化大吗”；
- 用户要求比较 2023、2024、2025、2026 或之后年份；
- 用户查询中国大陆高校本科招生专业、招生专业目录、专业组、选科要求、分省招生计划、培养方案变化；
- 用户查询海外大学 course、programme、major、catalog、tuition、deadline 或 accreditation 的年份变化；
- 用户问某专业是否新增、停招、改名、换学院、调整课程或认证状态。

## 输入

- `old_source_set`;
- `new_source_set`;
- `target_university`;
- `target_major`;
- `old_year`;
- `new_year`;
- `schemas/change_record.schema.json`;
- `data/change_detection_rules.yaml`;
- 来源评分结果和声明验证结果。

`old_source_set` 和 `new_source_set` 都必须经过 `source_scoring`。`new_source_set` 如果不满足当前/下一周期要求，只能作为最低底线或历史背景标注，不得输出为最新变化结论。

## 输出

输出一个或多个 `change_record`：

- `change_id`;
- `target_entity`;
- `country`;
- `university`;
- `major`;
- `old_year`;
- `new_year`;
- `change_type`;
- `old_value`;
- `new_value`;
- `old_sources`;
- `new_sources`;
- `certainty_level`;
- `user_impact`;
- `action_recommended`;
- `limitations`。

变化类型：

- `added`;
- `removed`;
- `renamed`;
- `merged`;
- `split`;
- `moved_department`;
- `requirement_changed`;
- `enrollment_plan_changed`;
- `subject_selection_changed`;
- `curriculum_changed`;
- `tuition_changed`;
- `accreditation_changed`;
- `unclear`。

## 核心步骤

1. 识别比较对象。
   - 国家、大学、专业、招生单位、年份、字段类型。
   - 如果用户只说“现在”或“今年”，优先解释当前日期下应查询当前或下一招生周期。

2. 检索来源。
   - 历史侧可以使用旧来源，但必须标注为 historical。
   - 当前侧默认必须优先使用当前/下一招生周期或当前/下一 academic year 官方来源；2025-01-01 只是最低底线。
   - 中国大陆高校优先检索当前/下一周期本科招生章程、招生简章、招生专业目录、分省招生计划、选考科目要求、专业组、培养方案、普通本科招生网、教育部、阳光高考、省级考试院、高校教务处和院系官网。

3. 评分和过滤来源。
   - 对 old_source_set 和 new_source_set 运行 `source_scoring`。
   - 排除 archived/outdated 页面作为当前证据。
   - 如果 new_source_set 不满足当前/下一周期，必须标注局限；如果连 2025 最低底线都不满足，不得推断当前变化。

4. 结构化字段。
   - 抽取专业名称、专业代码、学院、招生类别、大类招生、专业组、选考科目、招生计划、培养方案、课程模块、学费、认证状态、特殊项目。

5. 对比字段。
   - 新增专业；
   - 停招专业；
   - 专业更名；
   - 专业代码变化；
   - 专业归属学院变化；
   - 大类招生变化；
   - 专业组变化；
   - 分省招生计划变化；
   - 选科要求变化；
   - 培养方案变化；
   - 学费变化；
   - 中外合作项目变化；
   - 实验班、拔尖班、强基、专项计划变化；
   - 课程模块变化；
   - 认证状态变化。

6. 验证关键变化。
   - 对每条 change claim 运行 `claim_verification`。
   - 来源冲突时标为 `conflicting` 或 `unclear`。
   - 未找到当前官方来源时标为 `unknown`，不输出强结论。

7. 分析用户影响。
   - 对申请者说明影响：可选范围、选科要求、志愿组、培养方向、费用、认证或资格路径。
   - 给出下一步：查目标省份招生计划、目标院校招生网、教务处培养方案或认证机构页面。

## 失败处理

- 缺少历史来源：说明无法完整比较旧年份，只能描述当前状态。
- 缺少当前/下一周期来源：说明当前变化无法确认；连 2025-01-01 最低底线来源也缺少时输出“我没有找到满足 2025 年及以后时效要求的可靠来源”，不得把旧信息当作当前变化结论。
- 旧来源和新来源口径不同：标注适用范围，不直接比较全国目录和单校项目。
- 名称变化但实质不明：标注 `unclear`，要求进一步核查专业代码、学院和培养方案。
- 来源冲突：输出冲突来源表，不给单一确定结论。

## 与其他算法的关系

- 上游：`time_aware_retrieval`、`hybrid_retrieval`、`source_scoring`。
- 并行：`knowledge_graph` 使用 `changed_from` 和 `changed_to` 表示变化关系。
- 下游：`claim_verification`、`uncertainty_management`、`report_generation`。
