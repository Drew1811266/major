# major_similarity

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 相似度来源
- 相似度类型
- 核心步骤
- 失败处理
- 与其他算法的关系

## 用途

`major_similarity` 用于发现相近专业、替代路径和容易误导的表面匹配。当用户只给出兴趣词、热门方向或一个模糊专业名时，major 不应只返回一个专业名，而应扩展出相邻专业并解释差异。

典型目标：

- 从兴趣词扩展可检索专业；
- 区分同名、近名和跨国术语的实际差异；
- 为推荐、比较、报告和跨国对齐提供候选集合；
- 标注 `misleading_match`，避免把“看起来相关”当作“学习内容相同”。

## 触发场景

- 用户只说“我喜欢 AI”“我想学传媒”“我想学商科”“我喜欢心理学”；
- 用户要求“还有哪些类似专业”“替代专业是什么”；
- 用户比较 Computer Science、AI、Data Science、Software Engineering、Information Systems 等邻近方向；
- 用户查询的中文专业名可能对应多个英文、韩文、日文或国家术语；
- 推荐流程需要从兴趣或能力生成候选专业池；
- 专业名称相近但学习过程差异较大，需要提醒用户谨慎。

## 输入

- 用户输入中的兴趣词或专业名；
- `schemas/user_profile.schema.json`，用于识别能力、约束、偏好和排斥任务；
- `data/major_taxonomy_seed.yaml`，作为专业分类种子；
- `data/major_similarity_rules.yaml`，作为邻近专业和误导匹配规则；
- `data/major_aliases.yaml`，作为多语言检索别名；
- `data/country_terms.yaml`，用于国家术语层级；
- `data/major_task_profiles.yaml`，用于课程、任务、技能和风险差异；
- 可选来源记录和课程目录，用于具体大学或国家场景。

## 输出

输出应符合 `schemas/major_similarity_result.schema.json`，至少包含：

- `input_interest_or_major`;
- `matched_majors`;
- `similarity_type`;
- `similarity_score`;
- `shared_courses`;
- `shared_skills`;
- `shared_career_paths`;
- `differences`;
- `user_fit_notes`;
- `caution_notes`。

`similarity_type` 必须从以下类型中选择：

- `direct_match`: 直接匹配；
- `adjacent_major`: 相邻专业；
- `pathway_related`: 职业路径相关；
- `skill_related`: 技能相关；
- `interest_related`: 兴趣相关；
- `misleading_match`: 表面相关但学习内容差异大。

## 核心步骤

1. 标准化输入。
   - 提取兴趣词、专业名、国家、大学和用户画像字段。
   - 将中文宽泛词扩展为英文、韩文、日文和国家术语候选。

2. 生成候选专业集合。
   - 使用 `major_taxonomy_seed` 找到学科群。
   - 使用 `major_similarity_rules` 加入邻近、路径相关、技能相关和误导匹配项。
   - 使用 `major_task_profiles` 加入课程、技能、学习任务和风险信息。

3. 计算相似度来源。
   - 专业分类 taxonomy 相似度；
   - 课程内容相似度；
   - 技能要求相似度；
   - 职业路径相似度；
   - 研究生方向相似度；
   - 国家术语相似度；
   - 语义相似度；
   - 用户能力与约束条件匹配度。

4. 标注相似类型。
   - 与输入专业或兴趣高度一致的标为 `direct_match`。
   - 同课程和技能高度重叠但定位不同的标为 `adjacent_major`。
   - 通过职业目标连接的标为 `pathway_related`。
   - 主要共享技能但课程不同的标为 `skill_related`。
   - 主要共享兴趣主题的标为 `interest_related`。
   - 名称或行业光环相似但本科训练差异大的标为 `misleading_match`。

5. 输出差异解释。
   - 不只输出相似度分数。
   - 对每个候选说明共享课程、共享技能、共享职业路径和核心差异。
   - 如果有用户画像，补充 `user_fit_notes` 和 `caution_notes`。

6. AI 示例扩展。
   - 用户兴趣为 AI 时，应扩展：
     - Computer Science；
     - Artificial Intelligence；
     - Data Science；
     - Software Engineering；
     - Statistics；
     - Mathematics；
     - Electrical Engineering；
     - Robotics；
     - Cognitive Science；
     - Information Systems；
     - Business Analytics；
     - Human-Computer Interaction；
     - Digital Media。
   - 需要说明：
     - Computer Science 更偏底层、算法、系统和软件基础；
     - Artificial Intelligence 更偏算法、模型、数据和实验；
     - Data Science 更偏统计、数据处理、建模和解释；
     - Information Systems 更偏技术与商业管理结合；
     - Human-Computer Interaction 更偏用户体验、产品和研究方法；
     - Business Analytics 更偏商业问题和数据决策；
     - Digital Media 可能使用 AI 工具或交互技术，但不等于 AI 技术专业。

## 失败处理

- 如果专业或兴趣过于模糊：输出 3-5 个初步方向，并调用 `active_profile_completion` 询问最多 5 个关键问题。
- 如果候选专业缺少课程信息：标注为初步相似，不作为当前大学课程结论。
- 如果国家术语不等价：调用 `cross_country_alignment`，不得把翻译当作等价专业。
- 如果用户要求具体大学项目：调用 current/next-cycle 检索、`source_scoring` 和 `claim_verification`；2025-01-01 只是最低时效底线。
- 如果相似度来自非官方或旧来源：通过 `uncertainty_management` 降低确定性。

## 与其他算法的关系

- 上游：`intent_router`、`active_profile_completion`、`hybrid_retrieval`。
- 并行：`knowledge_graph` 可把相似专业连接为 `similar_to`、`differs_from`、`partially_equivalent_to` 边。
- 下游：`major_fit_scoring`、`constraint_filtering`、`recommendation_ranking`、`cross_country_alignment`、`report_generation`。
