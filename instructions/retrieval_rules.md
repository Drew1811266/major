# Retrieval Rules for major

## 目录

- 一、硬性时效规则
- 二、中国大陆高校特殊规则
- 三、海外院校特殊规则
- 四、检索步骤
- 五、来源优先级
- 六、来源记录要求
- 七、回答输出规则
- 八、受监管专业和高影响事实

major 的检索原则是：当前事实优先检索、引用和整理当前招生周期、下一招生周期、当前/下一 academic year 或 active/current 官方页面；2025-01-01 只是最低时效底线，不等于“最新”。先保证当前性、权威性和适用范围，再总结事实。

## 一、硬性时效规则

当用户查询大学专业、招生专业、课程设置、录取要求、学费、申请截止日期、专业认证、就业数据、签证、工签、政策变化等信息时，major 默认先寻找：

1. 当前招生周期官方来源；
2. 下一招生周期官方来源；
3. 当前 academic year 官方来源；
4. 下一 academic year 官方来源；
5. active/current 官方项目页面，且没有 archived/outdated 标记。

如果以上来源不可得，才使用满足最低时效底线的来源：

- 发布于 2025-01-01 及以后；
- 更新于 2025-01-01 及以后；
- 明确适用于 2025 年及以后招生周期；
- 明确适用于 2025 年及以后入学年份；
- 明确适用于 2025-2026 或更晚 academic year。

如果只找到 2025 年及以后但未明确适用于当前/下一招生周期的来源，必须标注：

“目前只找到 2025 年及以后但未明确适用于当前/下一招生周期的来源，因此不能直接视为最新结论。”

找不到 current/next-cycle 可靠来源时，不得默认使用旧来源作为当前证据，必须先说明“当前信息无法确认”。如果连 2025-01-01 最低底线来源也找不到，必须说明：

“我没有找到满足 2025 年及以后时效要求的可靠来源。”

旧来源只能作为历史背景，并且必须标注为 historical/outdated。

## 二、中国大陆高校特殊规则

对中国大陆高校，本科专业、招生专业、招生计划、选科要求、专业组、培养方案必须优先使用当前或下一招生周期官方来源；2025+ 只是最低底线。

查询中国大陆专业组、选科要求、分省招生计划或招生目录时，必须记录 `schemas/admissions_scope.schema.json` 中的适用范围。缺少省份、目标入学年份、选科组合、批次/申请路径或专业组且这些字段会影响结论时，不得输出最终当前结论，只能说明范围限制并反问。

优先检索：

- 当前/下一招生周期本科招生章程；
- 当前/下一招生周期本科招生简章；
- 当前/下一招生周期招生专业目录；
- 当前/下一招生周期分省招生计划；
- 当前/下一招生周期选考科目要求；
- 当前/下一招生周期专业组；
- 当前/下一招生周期培养方案；
- 当前/下一招生周期普通本科招生；
- 2025 本科招生章程；
- 2025 本科招生简章；
- 2025 招生专业目录；
- 2025 分省招生计划；
- 2025 选考科目要求；
- 2025 专业组；
- 2025 培养方案；
- 2025 普通本科招生；
- 高校本科招生网；
- 教育部；
- 阳光高考；
- 省级考试院；
- 高校教务处；
- 院系官网。

不得把第三方志愿填报平台、中介页面、论坛、旧版招生页面作为当前招生专业或专业组结论的唯一依据。

## 三、海外院校特殊规则

对英国、美国、澳大利亚、日本、韩国，优先使用当前/下一入学年份或 academic year：

- 2026 entry；
- 2027 entry；
- current undergraduate course；
- current undergraduate programme；
- 2026-2027 undergraduate catalog；
- 2027-2028 undergraduate catalog；
- 2025 entry；
- 2025-2026 undergraduate catalog；
- latest admissions requirements；
- latest tuition fees；
- latest course handbook。

不要把 archived page、旧版 course catalog、旧版招生页面当作当前信息。

## 四、检索步骤

0. 如果查询对象是中国大陆院校或中国大陆本科专业，可以先运行 `china_major_repository_lookup` 生成候选专业或候选院校；如果使用软科 2025 等排名信息，只能作为第三方排名参考。随后仍必须对当前招生事实执行官方 current/next-cycle 检索。

1. 识别事实类型：programme availability、admissions、course structure、tuition、deadline、accreditation、qualification、employment、visa/policy、change claim。
2. 使用 `data/major_aliases.yaml` 做多语言专业名扩展。
3. 使用 `data/country_terms.yaml` 做国家术语映射。
4. 使用 `algorithms/time_aware_retrieval.md` 生成 current/next-cycle + 2025 最低底线检索词。
5. 使用 `algorithms/hybrid_retrieval.md` 执行关键词检索、语义检索、多语言检索、官方入口检索，并用 RRF/MMR 融合和去重。
6. 过滤不满足 current/next-cycle 或 2025-01-01 最低底线的来源。
7. 使用 `algorithms/source_scoring.md` 和 `data/authority_source_rules.yaml` 为来源评分。
8. 使用 `algorithms/claim_verification.md` 验证关键结论。
9. 使用 `algorithms/uncertainty_management.md` 标注确定性。

## 五、来源优先级

优先级从高到低：

1. 大学官网、大学本科招生网、教务处、官方课程目录；
2. 院系官网；
3. 教育部、政府教育部门、省级考试院、阳光高考、官方申请平台；
4. 专业认证机构；
5. 职业统计机构；
6. 行业协会；
7. 可信教育平台或媒体；
8. 论坛、博客、无来源内容。

论坛、博客和无来源内容不能作为事实依据。

## 六、来源记录要求

每条来源都应尽量记录到 `schemas/source_record.schema.json`：

- source_id、title、url、publisher、source_type；
- country、university、department、major；
- published_date、updated_date、accessed_date；
- applicable_year、admissions_cycle、entry_year、academic_year；
- is_2025_or_later、freshness_basis、archive_or_current_status、currentness_basis；
- authority_score、freshness_score、relevance_score、specificity_score、corroboration_score、country_match_score、source_score；
- reliability_level、supports_claims、limitations。

本地中国专业库记录必须标注为 `local_repository_record`，软科等第三方排名必须标注为 `ranking_reference`。这两类来源不得作为招生、选科、专业组、分省计划或培养方案 claim 的唯一依据。

## 七、回答输出规则

- 输出时必须说明来源时效性。
- `high` certainty 可以作为当前结论。
- `medium` certainty 可以输出，但必须提示限制。
- `low` certainty 只能作为参考，不得作为强结论。
- `unknown` 必须说明无法确认。
- `outdated` 或 `not_found` claim 不得作为确定结论输出。
- 对中国大陆排名参考，说明其为第三方专业实力评价，不等于当前招生、录取难度、就业保证、选科要求、专业组或分省计划。

## 八、受监管专业和高影响事实

医学、护理、心理、法律、建筑、工程、会计、社会工作、教育资格、签证、移民等路径必须额外核验认证机构、政府监管机构和大学官方项目页。

不得承诺录取、就业、薪资、签证、移民或职业资格结果。
