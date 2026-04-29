# china_major_repository_ranking_reference

## 用途

`china_major_repository_ranking_reference` 用于管理软科 2025 中国大学专业排名等第三方排名信息在 major 中的使用边界。排名可以帮助用户初筛“某专业哪些学校值得看”，但不能替代官方招生、录取、选科、专业组、分省计划或培养方案来源。

## 触发场景

- 用户问“某专业哪些学校强”；
- 用户要求参考软科 2025 中国大学专业排名；
- 中国大陆专业推荐需要候选院校排序辅助；
- 报告中需要列出第三方排名参考和局限；
- 来源核查发现某结论来自 ranking_reference 或 local repository。

## 输入

- `schemas/china_ranking_reference.schema.json`；
- `schemas/china_university_major_record.schema.json`；
- `data/china_major_repository/sources.yaml`；
- `data/source_priority.yaml`；
- `data/authority_source_rules.yaml`；
- 软科排名方法页面 URL。

## 输出

- ranking reference records；
- ranking signal strength；
- not-admissions-evidence warning；
- required official verification checklist；
- user-visible limitations。

## 核心步骤

1. 确认排名来源、年份和方法链接。
2. 标记排名用途：
   - `major_strength_reference`；
   - `candidate_pool_expansion`；
   - `comparison_context`；
   - 不可用于 `admissions_fact`。
3. 识别排名字段：
   - 排名年份；
   - 专业；
   - 院校；
   - 评级；
   - 位次或区间；
   - 方法链接；
   - 数据限制。
4. 输出时必须说明：
   - 排名是第三方评价；
   - 不等于录取难度；
   - 不等于就业、薪资或资格保证；
   - 不等于当前招生；
   - 不替代省份、选科、专业组和分省计划核查。
5. 对需要最终事实的结论调用官方 current/next-cycle 检索。

## 失败处理

- 没有排名方法链接：不能引用排名为可靠参考。
- 没有授权数据：不能内置或展示完整榜单。
- 只有排名但没有官方招生来源：只能输出候选和核查建议。
- 排名来源与官方招生来源冲突：官方招生事实优先，排名只保留为背景。

## 与其他算法的关系

- 上游：`china_major_repository_lookup`、`source_scoring`。
- 下游：`claim_verification`、`uncertainty_management`、`recommendation_ranking`、`report_generation`。
- 与 `china_admissions_scope_resolver` 共同防止把排名误用为报考结论。
