# major Algorithms

`major` 的算法模块把本科专业咨询从“提示词集合”提升为可解释、可测试、可迁移的决策流程。算法规则不绑定 Claude、OpenAI、MCP 或任何具体搜索引擎；它们描述 major 在不同任务中如何判断意图、选择工作流、补全用户画像、检索 current/next-cycle 信息（2025-01-01 为最低时效底线）、评估来源、验证结论、标注不确定性，并输出结构化中文回答。

## 算法总览

| 算法 | 职责 | MVP |
|---|---|---|
| `intent_router` | 判断用户意图、国家、大学、专业、是否需要画像和检索 | 是 |
| `workflow_orchestrator` | 根据意图选择工作流和后续算法 | 是 |
| `time_aware_retrieval` | 执行 2025-01-01 及以后、当前/下一周期优先的时效检索规则 | 是 |
| `hybrid_retrieval` | 执行中文、英文、韩文、日文和多渠道检索扩展 | 是 |
| `source_scoring` | 按权威性、时效性、相关性、具体性、交叉验证等评分来源 | 是 |
| `active_profile_completion` | 为推荐和适配判断选择最多 5 个关键反问 | 是 |
| `major_fit_scoring` | 根据兴趣、能力、学习过程、职业目标、国家体系和约束评分专业适配度 | 是 |
| `constraint_filtering` | 过滤预算、语言、作品集、数学、临床、签证、资格等硬约束 | 是 |
| `risk_scoring` | 评估能力差距、学习压力、申请、就业、资格、预算和语言风险 | 是 |
| `preference_learning` | 根据多轮反馈更新偏好权重和硬软约束 | 是 |
| `recommendation_ranking` | 综合适配度、风险、约束、偏好、来源确定性和多样性进行推荐分组 | 是 |
| `china_admissions_scope_resolver` | 解析中国大陆省份、入学年份、选科、批次、路径、专业组和分省计划口径 | 是 |
| `china_major_repository_lookup` | 查询中国大陆本地专业候选库，生成院校/专业候选和排名参考 | 是 |
| `china_major_repository_validation` | 校验中国专业库记录、授权、来源 ID 和官方核验边界 | 是 |
| `china_major_repository_import` | 导入用户授权 CSV/JSON，不内置未授权完整排名榜单 | 否 |
| `china_major_repository_ranking_reference` | 管理软科等第三方排名参考的使用边界 | 是 |
| `claim_verification` | 对关键结论逐条核验来源和证据强度 | 是 |
| `uncertainty_management` | 标注 high/medium/low/unknown 确定性和回答边界 | 是 |
| `major_similarity` | 识别相近专业、差异维度和替代专业 | 否 |
| `knowledge_graph` | 组织专业、课程、能力、职业、国家术语和资格之间的关系 | 否 |
| `cross_country_alignment` | 对齐六国专业名称、学制、课程结构、申请和资格路径 | 否 |
| `change_detection` | 比较不同年份专业目录、课程、招生或政策变化 | 否 |
| `report_generation` | 将专业介绍、比较、推荐、来源核查和变化检测整理成报告 | 否 |

## 调用顺序

默认顺序：

1. `intent_router` 解析用户输入，输出 `schemas/intent_result.schema.json`。
2. `workflow_orchestrator` 选择工作流，输出 `schemas/algorithm_decision.schema.json`。
3. 如果需要个性化推荐或适配判断，运行 `active_profile_completion`。
4. 如果涉及具体大学、招生、课程、学费、截止日期、认证、签证、就业数据或最新政策，运行 `time_aware_retrieval`。
5. 如果是中国大陆院校或专业高频查询，运行 `china_admissions_scope_resolver`、`china_major_repository_lookup` 和必要的 `china_major_repository_ranking_reference`，只生成候选和排名参考。
6. 如果用户用中文宽泛词、跨国比较或非英文国家术语，运行 `hybrid_retrieval`。
7. 对检索结果运行 `source_scoring`，弱来源不得作为唯一依据。
8. 对关键结论运行 `claim_verification`。
9. 运行 `uncertainty_management` 标注确定性、缺口和限制。
10. 根据任务进入：
   - 推荐或适配：`constraint_filtering`、`major_fit_scoring`、`risk_scoring`、`preference_learning`、`recommendation_ranking`、必要时 `major_similarity`
   - 多专业比较：`major_similarity`、`knowledge_graph`
   - 多国家比较：`cross_country_alignment`
   - 年份变化：`change_detection`
   - 结构化知识整理或报告：`knowledge_graph`、`report_generation`
11. 输出默认中文、结构化、带来源和边界的回答。

## MVP 算法

MVP 必须覆盖 major 的核心可靠性：

- `intent_router`
- `workflow_orchestrator`
- `time_aware_retrieval`
- `hybrid_retrieval`
- `source_scoring`
- `active_profile_completion`
- `major_fit_scoring`
- `constraint_filtering`
- `risk_scoring`
- `preference_learning`
- `recommendation_ranking`
- `china_admissions_scope_resolver`
- `china_major_repository_lookup`
- `china_major_repository_validation`
- `china_major_repository_ranking_reference`
- `claim_verification`
- `uncertainty_management`

## 进阶增强

进阶算法用于提高解释深度、跨国一致性和长期维护能力：

- `major_similarity`
- `knowledge_graph`
- `cross_country_alignment`
- `change_detection`
- `report_generation`
- `china_major_repository_import`

这些算法不改变 major 的安全底线：本科优先、中文默认、六国覆盖、2025+ 最低时效、当前/下一周期优先、不承诺录取/就业/薪资/签证/移民/职业资格。

## 整体决策流程

```text
用户输入
→ intent_router 判断意图
→ workflow_orchestrator 选择工作流
→ 判断是否需要补全用户画像
→ 判断是否需要检索 current/next-cycle 信息
→ 如果是中国大陆院校/专业查询，先用 china_major_repository_lookup 生成候选，并用 china_admissions_scope_resolver 检查招生 scope
→ time_aware_retrieval 执行时效检索
→ hybrid_retrieval 执行多语言、多渠道检索
→ source_scoring 评分来源
→ claim_verification 验证关键结论
→ uncertainty_management 标注确定性
→ 根据任务进入 constraint_filtering、major_fit_scoring、risk_scoring、preference_learning、recommendation_ranking、major_similarity、knowledge_graph、cross_country_alignment、change_detection 或 report_generation
→ 输出结构化回答
```

## 输出原则

- 默认使用中文。
- 默认聚焦本科阶段，除非用户明确询问研究生信息。
- 覆盖中国、韩国、日本、英国、美国、澳大利亚。
- 对具体事实先检索再总结。
- 对关键结论先验证再表达。
- 对来源不足、不确定或过旧的信息明确标注。
- 不保证录取、就业、薪资、签证、移民或职业资格结果。
