# time_aware_retrieval

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 默认时效规则
- 中国大陆特殊规则
- 海外特殊规则
- 核心步骤
- 失败处理
- 与其他算法的关系

## 用途

`time_aware_retrieval` 是 major 的时效检索算法。它用于让 major 在查询大学专业、招生专业、课程设置、录取要求、学费、截止日期、专业认证、就业数据、签证、工签和政策变化时，默认优先执行当前/下一招生周期或当前/下一 academic year 检索；2025-01-01 只是最低时效底线，避免把过期院校专业信息包装成当前结论。

默认优先检索、引用和整理当前招生周期、下一招生周期、当前/下一 academic year 或 active/current 官方页面。2025-01-01 及以后发布、更新或适用的信息只是最低时效底线。对于中国大陆高校，本科专业和招生相关信息必须优先使用当前/下一周期官方来源。

## 触发场景

- 查询具体大学本科专业；
- 查询中国大陆高校本科招生专业；
- 查询招生章程、招生简章、招生专业目录、分省招生计划；
- 查询选考科目要求、专业组、培养方案；
- 查询海外大学本科 course、programme、major、catalog；
- 查询录取要求、学费、申请截止日期；
- 查询专业认证、执照路径；
- 查询就业数据、签证、工签、政策变化；
- 用户使用“现在”“最新”“今年”“当前”“2025”“2026”等词。

## 输入

- 用户问题；
- 目标国家、大学、专业、年份和事实类型；
- `data/source_priority.yaml`；
- `data/authority_source_rules.yaml`；
- `data/official_sources.yaml`；
- `schemas/source_record.schema.json`；
- 当前访问日期。

## 输出

输出必须能组织为 `schemas/retrieval_result.schema.json`，包括：

- 原始查询；
- 扩展查询；
- 目标国家、大学、专业；
- 最低时效日期 `2025-01-01`，但不把它当作当前性证明；
- currentness_basis：当前招生周期、下一招生周期、当前 academic year、下一 academic year、active/current official page、minimum_2025_floor_only；
- 已接受来源；
- 已拒绝来源；
- 来源时效摘要；
- 是否需要 claim verification；
- 局限说明。

## 默认时效规则

只使用以下任一条件满足的信息：

优先使用以下当前性信号：

1. 明确适用于当前招生周期；
2. 明确适用于下一招生周期；
3. 明确适用于当前 academic year；
4. 明确适用于下一 academic year；
5. 官方 current page 明确显示项目 active/current，且没有 archived/outdated 标记。

最低时效底线包括：

1. 发布于 2025-01-01 及以后；
2. 更新于 2025-01-01 及以后；
3. 明确适用于 2025 年及以后招生周期；
4. 明确适用于 2025 年及以后入学年份；
5. 明确适用于 2025-2026 或更晚 academic year；
6. 官方 current page 明确显示该项目仍 active/current，并且没有 archived/outdated 标记。

2024 年及以前来源默认不得作为当前结论依据。用户明确要求历史背景或年份变化比较时可以使用旧来源，但必须标注为 `historical` 或 `outdated`。

## 中国大陆特殊规则

查询中国大陆高校信息时，优先检索：

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

中国大陆高校本科招生专业、招生计划、选科要求、专业组和培养方案每年可能变化，不得用旧版招生网页、旧专业目录或第三方聚合页面替代当前/下一周期官方来源。

## 海外特殊规则

查询英国、美国、澳大利亚、日本、韩国时，优先检索：

- 2025 entry；
- 2026 entry；
- current undergraduate course；
- current undergraduate programme；
- 2025-2026 undergraduate catalog；
- 2026-2027 undergraduate catalog；
- latest admissions requirements；
- latest tuition fees；
- latest course handbook。

海外大学页面如果没有发布日期，只有在官方页面明确为 current、active、open for application 或当前 catalog/handbook 时才可作为当前证据，并必须记录 `freshness_basis = current_official_page`。

## 核心步骤

1. 判断用户问题是否属于时效敏感事实。
2. 识别目标国家、大学、专业、事实类型和年份。
3. 生成 current/next-cycle + 2025 最低底线检索词。
4. 对中国大陆高校加入“2025 本科招生章程”“2025 招生专业目录”“2025 分省招生计划”“2025 选考科目要求”“2025 专业组”“2025 培养方案”等关键词。
5. 对海外院校加入 `2025 entry`、`2026 entry`、`current undergraduate course`、`2025-2026 undergraduate catalog`、`latest course handbook` 等关键词。
6. 初步排除 2024 年及以前、archived、outdated、旧版招生页和无当前适用依据的来源。
7. 把通过时效过滤的来源交给 `hybrid_retrieval` 和 `source_scoring`。
8. 对关键结论设置 `verification_required = true`，交给 `claim_verification`。

## 失败处理

如果没有找到可靠当前/下一周期来源，必须说明当前信息无法确认，并标注任何仅满足 2025 最低底线来源的局限。如果连 2025-01-01 最低底线来源也没有找到，必须输出：

> 我没有找到满足 2025 年及以后时效要求的可靠来源。

不得默认使用 2024 年及以前来源作为当前结论。

只有用户明确接受历史背景时，才可使用旧来源，并必须标注为 `historical` 或 `outdated`。如果只找到第三方聚合或中介来源，不得输出确定结论，应说明需要目标大学、官方招生平台、教育部门、认证机构或职业统计机构核验。

## 与其他算法的关系

- 上游：`intent_router`、`workflow_orchestrator`。
- 并行/下游：`hybrid_retrieval` 用于多语言和多渠道检索扩展。
- 下游：`source_scoring` 计算来源可用性；`claim_verification` 验证关键结论；`uncertainty_management` 标注确定性。
