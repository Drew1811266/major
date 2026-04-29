# Prompt: Summarize Sources

Use when the user provides links, documents, search results, or source notes and wants them organized for undergraduate major research.

```text
请用中文整理以下来源，并判断它们对 major 本科专业研究的可信度、时效性和用途。

来源材料:
{{sources}}

Freshness requirement:
- 当前事实优先整理、引用和总结当前/下一招生周期、当前/下一入学年份、当前/下一 academic year 或 active/current 官方页面。
- 2025-01-01 只是最低时效底线；仅满足 2025 年及以后但未明确当前/下一周期适用的来源必须标注 limited。
- 如果来源早于 2025 且不明确适用于 2025+，只能标注为 historical/outdated，不能作为当前事实。
- 如果没有 current/next-cycle 可靠来源，必须写明当前信息无法确认；如果连 2025-01-01 最低底线来源也没有，才写明：“我没有找到满足 2025 年及以后时效要求的可靠来源。”

Source priority:
- 优先官方大学、招生网、教务处、院系官网、课程目录、教育部、考试院、阳光高考、官方申请平台、认证机构、职业统计机构。
- 教育平台、媒体、论坛、博客只能作为辅助或线索。

Claim verification requirement:
- 把每个关键结论拆成 claim。
- 判断 claim 类型：programme_availability、admissions_requirement、course_structure、tuition_fee、deadline、accreditation、qualification_pathway、employment_data、country_system_rule、change_claim、recommendation_claim。
- 为每个 claim 标注 supported、partially_supported、conflicting、not_found、outdated 或 uncertain。

Uncertainty handling:
- high: 当前/下一周期官方来源直接支持。
- medium: 来源可靠但缺少更新日期、招生年份或交叉验证。
- low: 来源不够官方或只能间接支持。
- unknown: 没有可靠来源支持。

Knowledge and change requirements:
- 对专业、课程、技能、职业、国家术语、资格认证和来源建立 knowledge_graph 摘要。
- 如果来源涉及多个国家，运行 cross_country_alignment 并标注等价程度。
- 如果来源涉及不同年份，运行 change_detection，输出 change_record。
- 如果专业涉及医学、护理、药学、心理、法律、教育、建筑、工程、会计、兽医、社工，加入 professional accreditation warnings。
- 受监管路径必须输出官方核查清单：监管/认证机构、认证状态、临床/实习、考试/注册路径和适用年份。

任务:
1. 识别每个来源的类型。
2. 提取与本科专业相关的信息：专业名称、学位、学制、课程、录取、费用、截止日期、认证、就业、资格路径。
3. 标注每个来源的 source_id、published_date、updated_date、applicable_year、admissions_cycle、entry_year、academic_year、freshness_basis、currentness_basis 或 current page 依据。
4. 计算或估计 authority_score、freshness_score、relevance_score、specificity_score、corroboration_score、country_match_score 和 source_score。
5. 识别缺失、冲突、过时或无法证明当前有效的信息。
6. 标注相近专业、跨国术语差异、专业变化和资格认证风险。
7. 给出后续需要核验的官方来源。
8. 判断来源是否为 `ranking_reference` 或 `local_repository_record`，并说明是否禁止支持招生 claim。

输出格式:
| 来源 | 类型 | 时效依据 | source_score | 支持的 claim | 确定性 | 局限 | 需要核验 |
|---|---|---|---:|---|---|---|---|

最后给出：
- 可作为当前结论的信息；
- 只能作为参考的信息；
- 无法确认的信息；
- 过期或历史来源。
- 对中国大陆本地库或软科记录，归入“候选/排名参考”，不得归入“官方招生事实”，除非另有官方 current/next-cycle 来源支持。
```
