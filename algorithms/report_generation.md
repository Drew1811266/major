# report_generation

## 用途

`report_generation` 用于把 major 的检索、解释、比较、推荐、来源核查和变化检测结果整理成结构化报告，便于用户、家长、留学顾问或升学规划师使用。

支持报告类型：

- 单专业介绍报告；
- 多专业比较表；
- 多国家专业体系比较；
- 用户画像推荐报告；
- current/next-cycle 来源核查报告；
- 年份变化对比报告。

## 触发场景

- 用户要求“整理成表格”“做成报告”“给家长看的版本”“咨询建议”；
- 用户需要多专业、多国家、多来源结果的总结；
- 用户要求来源核查或年份变化对比；
- 工作流需要把 `major_profile`、`recommendation`、`source_record`、`change_record` 或 `cross_country_alignment` 转成可读输出。

## 输入

- 用户问题和目标受众；
- `schemas/major_profile.schema.json`；
- `schemas/recommendation.schema.json`；
- `schemas/source_record.schema.json`；
- `schemas/cross_country_alignment.schema.json`；
- `schemas/change_record.schema.json`；
- `schemas/uncertainty_record.schema.json`；
- `schemas/knowledge_graph_node.schema.json` 和 `schemas/knowledge_graph_edge.schema.json`；
- 来源验证结果和不确定性记录。

## 输出

报告必须包含：

- 结论摘要；
- 适用范围；
- 主要信息；
- 来源表；
- 时效说明；
- 不确定性；
- 风险提示；
- 下一步建议。

不同报告的默认结构：

1. 单专业介绍报告：定义、课程、技能、适合/不适合人群、相近专业、国家差异、职业/研究生方向、认证提醒、来源。
2. 多专业比较表：定位、课程、强度、适合人群、风险、替代路径、来源确定性。
3. 多国家专业体系比较：术语、层级、课程结构、申请单位、学制、认证、等价程度、风险。
4. 用户画像推荐报告：已知画像、缺失信息、推荐分组、适配理由、风险、下一步。
5. Current/next-cycle 来源核查报告：检索范围、来源表、currentness_basis、source_score、claim status、可确认结论、无法确认内容。
6. 年份变化对比报告：变化表、旧值、新值、来源、确定性、用户影响、行动建议。

## 核心步骤

1. 确定报告类型和读者。
   - 面向学生时更强调学习体验和行动建议。
   - 面向家长时更强调风险、路径和来源边界。
   - 面向顾问时更强调来源表、时效、验证状态和可追溯结构。

2. 汇总结构化输入。
   - 从 `knowledge_graph` 抽取相关子图。
   - 从 `claim_verification` 保留可输出结论。
   - 从 `uncertainty_management` 带入 certainty level。

3. 生成表格。
   - 比较类问题优先表格。
   - 来源核查和变化检测必须包含来源表。
   - 不确定或来源不足的字段直接标注，不留空或编造。

4. 加入时效说明。
   - 当前事实必须说明是否满足 2025+ 或当前/下一周期要求。
   - 旧来源只能作为历史背景。

5. 加入风险和下一步。
   - 对资格、临床、签证、就业、学费、截止日期和认证等高风险事项给官方核查建议。
   - 不承诺录取、就业、薪资、签证、移民或职业资格。

## 失败处理

- 信息不足：输出报告草案，列出缺失字段和需要补充的问题。
- 缺少 current/next-cycle 来源：明确说明当前来源不足；缺少 2025-01-01 最低底线来源时，不把旧来源当作当前证据。
- 来源冲突：列出冲突来源和无法确认的结论。
- 用户要求过大：先给报告框架和关键表格，再建议分国家或分专业细化。

## 与其他算法的关系

- 上游：`major_similarity`、`knowledge_graph`、`cross_country_alignment`、`change_detection`、`claim_verification`、`uncertainty_management`、`recommendation_ranking`。
- 下游：最终回答、咨询报告、表格输出和评估用例。
