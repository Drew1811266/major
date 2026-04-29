# intent_router

## 用途

`intent_router` 用于把用户输入转换为结构化意图结果，供 `workflow_orchestrator` 选择后续工作流和算法。输出必须符合 `schemas/intent_result.schema.json`。

## 触发场景

每次 major 接收用户请求时都先运行。尤其适用于：

- 单专业介绍；
- 多专业比较；
- 多国家体系比较；
- 个性化推荐或适配判断；
- 具体大学、本科项目、招生、学费、截止日期查询；
- 来源核查；
- 年份变化比较；
- 报告或表格生成；
- 用户问题不清楚。

## 输入

- 用户原始输入；
- 已知对话上下文；
- 可选用户画像；
- `data/country_terms.yaml`；
- `data/major_aliases.yaml`；
- `data/regulated_fields.yaml`。

## 输出

符合 `schemas/intent_result.schema.json` 的对象，至少包括：

- `intent`
- `confidence`
- `countries_detected`
- `universities_detected`
- `majors_detected`
- `education_level_detected`
- `requires_user_profile`
- `requires_retrieval`
- `requires_current_cycle_sources`
- `minimum_freshness_floor`
- `currentness_required`
- `requires_2025_plus_sources`（deprecated compatibility field；只表示 2025-01-01 最低底线适用，不作为主要判断字段）
- `requires_source_citation`
- `requires_professional_accreditation_warning`
- `recommended_workflow`
- `missing_information`
- `next_action`

## 可识别意图

| intent | 说明 |
|---|---|
| `explain_major` | 单专业介绍，例如“介绍心理学本科” |
| `compare_majors` | 多个专业比较，例如“CS 和数据科学区别” |
| `compare_countries` | 多国家专业体系比较 |
| `recommend_majors` | 根据兴趣或背景推荐专业 |
| `evaluate_fit` | 判断用户是否适合某专业 |
| `university_program_lookup` | 查询具体大学或院校项目 |
| `admissions_lookup` | 查询招生、录取、学费、截止日期、选科要求等 |
| `source_check` | 核查来源、说法或中介宣传 |
| `change_comparison` | 比较不同年份专业变化 |
| `report_generation` | 生成表格、报告或咨询材料 |
| `unclear` | 意图不明确 |

## 核心步骤

1. 识别任务动词：介绍、比较、推荐、适不适合、查、核实、变化、整理。
2. 识别实体：
   - 国家：中国、韩国、日本、英国、美国、澳大利亚；
   - 大学或院校名；
   - 专业名和别名；
   - 本科、研究生、执照、就业、移民等层级或主题。
3. 判断是否涉及个性化：
   - 推荐专业、适不适合、规划、选什么专业时，`requires_user_profile = true`。
4. 判断是否涉及具体事实：
   - 大学项目、招生、课程、学费、截止日期、认证、签证、就业数据、政策变化时，`requires_retrieval = true`。
5. 判断是否必须使用 current/next-cycle 来源：
   - 所有当前大学、招生、课程、认证、就业、签证和政策问题都必须设为 true；2025-01-01 只是最低底线。
6. 判断是否涉及受监管领域：
   - 医学、护理、心理、法律、建筑、工程、会计、社会工作、教育资格、签证、移民等设为 true。
7. 选择推荐工作流。
8. 如果置信度低于 0.60，设置 `intent = unclear`，并把 `next_action` 设为反问或范围确认。

## 失败处理

- 如果专业名模糊，保留多个候选专业，要求用户确认或先解释歧义。
- 如果国家缺失但任务需要国家，提出最多 3 个范围确认问题。
- 如果用户要求推荐但画像不足，输出 `requires_user_profile = true` 和缺失画像字段。
- 如果用户要求“最新”“现在”“今年”，但没有国家或大学，仍标记需要 current/next-cycle 检索，并要求补充范围。

## 与其他算法的关系

- 上游：无，作为入口算法。
- 下游：`workflow_orchestrator`。
- 辅助数据：`major_aliases` 帮助识别专业别名；`country_terms` 帮助识别国家术语；`regulated_fields` 帮助识别资格认证警告。
