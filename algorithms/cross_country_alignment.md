# cross_country_alignment

## 用途

`cross_country_alignment` 用于比较中国、韩国、日本、英国、美国、澳大利亚的本科专业体系和专业名称，不得简单假设不同国家同名专业完全等价。它按多维度判断专业、项目、课程结构、申请单位和资格路径是否相近。

## 触发场景

- 用户要求比较同一专业在多个国家的差异；
- 用户问某个中文专业在英国、美国、澳大利亚、日本、韩国或中国叫什么；
- 用户问 course、programme、major、学部、学科、전공、本科专业等术语是否等价；
- 用户想跨国选择专业或做咨询报告；
- 用户把某国专业经验套用到另一国，需要纠正；
- 受监管职业路径跨国差异明显，例如医学、护理、药学、心理、法律、教育、建筑、工程、会计、兽医、社工。

## 输入

- 输入专业或专业群；
- 待比较国家；
- `data/country_terms.yaml`；
- `data/country_alignment_rules.yaml`；
- `data/major_aliases.yaml`；
- `data/professional_accreditation_rules.yaml`；
- current/next-cycle 官方来源记录，或标明仅满足 2025-01-01 最低底线的来源记录；
- `schemas/cross_country_alignment.schema.json`；
- 可选用户画像，用于说明哪些差异影响选择。

## 输出

输出应符合 `schemas/cross_country_alignment.schema.json`：

- `input_major`;
- `countries_compared`;
- `local_names`;
- `terminology_notes`;
- `alignment_dimensions`;
- `equivalence_level`;
- `evidence_sources`;
- `uncertainty_level`;
- `cautions`;
- `user_visible_summary`。

`equivalence_level` 包括：

- `exact`: 高度等价；
- `close`: 大体相近；
- `partial`: 部分重合；
- `pathway_related`: 路径相关但不是同一专业；
- `not_equivalent`: 不等价；
- `unknown`: 信息不足。

## 核心步骤

1. 标准化国家和术语。
   - China: 本科专业、学科门类、专业类、专业目录、培养方案、招生专业。
   - South Korea: `학과`、`전공`、`학부`、`단과대학`、`모집단위`。
   - Japan: `学部`、`学科`、`専攻`、`コース`、`課程`。
   - United Kingdom: `course`、`programme`、`subject`、`degree`、`module`。
   - United States: `major`、`minor`、`concentration`、`department`、`undergraduate program`。
   - Australia: `course`、`degree`、`major`、`stream`、`specialisation`。

2. 确定比较层级。
   - 比较的是国家制度、大学项目、院系、专业、方向、课程模块还是招生单位。
   - 不得把中国本科招生专业、英国 course、美国 major、日本学部、澳洲 degree 直接视为同一层级。

3. 按维度对齐。
   - 名称是否相同或相近；
   - 本科申请单位是否相同；
   - 专业层级是否相同；
   - 课程结构是否相近；
   - 是否包含相同核心课程；
   - 学制是否相近；
   - 是否需要作品集、实验、临床、实习；
   - 职业路径是否相似；
   - 是否涉及专业认证；
   - 是否需要研究生或额外资格；
   - 国家术语是否可以直接翻译。

4. 计算等价等级。
   - 多数核心维度一致且同层级：`exact` 或 `close`。
   - 课程和职业方向有重叠但层级、申请单位或资格路径不同：`partial`。
   - 主要通过职业目标连接：`pathway_related`。
   - 名称相近但课程或资格路径不同：`not_equivalent` 或 `misleading` caution。
   - 来源不足：`unknown`。

5. 绑定证据和不确定性。
   - 当前项目、课程、认证和招生事实必须优先来自当前/下一周期官方来源；2025-01-01 只是最低时效底线。
   - 若只覆盖个别大学，不能推断为全国规则。
   - 若来源之间冲突，调用 `claim_verification` 并标注冲突。

## 失败处理

- 找不到某国对应专业：说明可能以其他名称、方向、学院或课程出现，并给检索关键词。
- 只有单校来源：标注适用范围，不能概括全国。
- 术语不可直接翻译：输出 `partial`、`pathway_related` 或 `unknown`，不要强行等价。
- 受监管路径差异大：调用 `professional_accreditation_rules` 和 current/next-cycle 官方核查。
- 找不到 current/next-cycle 来源：说明当前对齐结论无法确认；如果连 2025-01-01 最低底线来源也找不到，输出“我没有找到满足 2025 年及以后时效要求的可靠来源。”

## 与其他算法的关系

- 上游：`hybrid_retrieval`、`source_scoring`、`major_similarity`。
- 并行：`knowledge_graph` 用边表示 `equivalent_to` 或 `partially_equivalent_to`。
- 下游：`multi_country_comparison_workflow`、`claim_verification`、`uncertainty_management`、`report_generation`。
