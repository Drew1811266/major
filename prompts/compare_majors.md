# Prompt: Compare Majors

Use when the user wants to compare undergraduate majors or compare one major across countries.

```text
请用中文比较以下本科专业或国家体系:
{{comparison_targets}}

比较范围:
- 国家: {{countries_or_default_six}}
- 教育阶段: 本科
- 用户背景: {{user_profile_if_any}}

Freshness requirement:
- 当前大学项目、课程、招生、费用、截止日期、认证、就业数据、签证或政策比较必须优先使用当前/下一招生周期、当前/下一入学年份或当前/下一 academic year 官方来源。
- 2025-01-01 只是最低时效底线；仅有 2025 年及以后但未明确当前/下一周期适用的来源，必须标注局限。
- 找不到 current/next-cycle 可靠来源时，必须说明当前信息无法确认；如果连 2025-01-01 最低底线来源也找不到，才说明：“我没有找到满足 2025 年及以后时效要求的可靠来源。”

Source priority:
- 优先官方大学、院系、课程目录、招生平台、教育部门、考试院、认证机构、职业统计机构。
- 中国大陆高校比较必须优先当前/下一招生周期官方招生章程、招生专业目录、分省招生计划、选考科目要求、专业组和培养方案；缺省份、选科、入学年份或批次时必须先说明缺口。
- 中国大陆本地专业库和软科排名只能用于候选初筛或专业实力参考，不得作为当前招生、选科、专业组、分省计划或培养方案事实。
- 海外院校优先 2026 entry、2027 entry、current undergraduate course、current undergraduate programme、2026-2027 或更新 catalog、latest course handbook。
- 受监管路径必须输出官方核查清单：监管/认证机构、认证状态、临床/实习、考试/注册路径和适用年份。

Claim verification requirement:
- 对每个关键差异结论进行 claim verification，并在来源表中保留 source_id、claim_id 和 currentness_basis。
- 对 programme_availability、course_structure、admissions_requirement、accreditation、employment_data、change_claim 等 claim 标注状态。

Uncertainty handling:
- high: 可作为当前结论；
- medium: 可输出但说明限制；
- low: 仅作参考；
- unknown: 说明无法确认。

Personalized comparison requirement:
- 如果用户是在“选专业”而不是单纯比较概念，先运行 active_profile_completion。
- 根据用户画像执行 constraint_filtering、major_fit_scoring、risk_scoring、preference_learning 和 recommendation_ranking。
- 比较结论必须说明推荐分组、适合点、风险点、替代专业和下一步，不得只按热门程度排序。

Knowledge structure requirement:
- 先运行 major_similarity，识别 direct_match、adjacent_major、pathway_related、skill_related、interest_related 和 misleading_match。
- 使用 knowledge_graph 连接专业、课程模块、技能、职业、研究生方向、国家术语、资格认证和来源。
- 跨国家比较时运行 cross_country_alignment，输出 equivalence_level。
- 如果用户要求比较年份变化，运行 change_detection。
- 对医学、护理、药学、心理、法律、教育、建筑、工程、会计、兽医、社工等路径加入 professional accreditation warnings。

输出要求:
1. 先用表格比较关键维度。
2. 再解释差异背后的学习内容、训练方式和适合人群。
3. 明确相近专业容易混淆的地方。
4. 给出选择建议、风险点和替代选择。
5. 对具体事实加入来源和时效说明。
6. 信息不足时明确缺口，不假装确定。

建议表格维度:
- 专业定位
- 本科核心课程
- 数学/编程/实验/写作/作品集要求
- 适合学生
- 不适合学生
- 典型职业方向
- 研究生方向
- 国家或院校差异
- 跨国等价程度
- 主要风险
- 资格认证提醒
- 来源确定性
- 第三方排名参考与局限
```
