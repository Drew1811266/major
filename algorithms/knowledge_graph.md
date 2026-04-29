# knowledge_graph

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 节点类型
- 边类型
- 核心步骤
- 失败处理
- 与其他算法的关系

## 用途

`knowledge_graph` 用于把专业、课程模块、技能、职业方向、研究生方向、国家术语、大学项目、录取要求、专业认证、资格路径、来源和用户画像组织成可追踪关系网络。

知识图谱支持：

- 发现相近专业；
- 生成专业解释；
- 生成专业比较；
- 跨国专业对齐；
- 识别资格认证风险；
- 连接专业与职业方向；
- 连接用户画像与专业适配；
- 支持变化检测；
- 支持来源追踪。

## 触发场景

- 用户要求单专业报告、对比报告、咨询材料或表格；
- 一个问题涉及多个专业、多个国家、多个来源或多种资格路径；
- 需要解释专业和课程、技能、职业、资格之间的关系；
- 需要把 `major_profile`、来源记录和声明验证结果整合为结构化输出；
- 需要支持 `major_similarity`、`cross_country_alignment` 或 `change_detection`。

## 输入

- `schemas/major_profile.schema.json`；
- `schemas/source_record.schema.json`；
- `schemas/claim_verification.schema.json`；
- `schemas/user_profile.schema.json`；
- `schemas/knowledge_graph_node.schema.json`；
- `schemas/knowledge_graph_edge.schema.json`；
- `data/country_terms.yaml`；
- `data/professional_accreditation_rules.yaml`；
- `data/major_task_profiles.yaml`；
- `data/major_similarity_rules.yaml`；
- 可选：大学课程目录、培养方案、招生专业目录、认证机构页面和职业统计来源。

## 输出

输出由节点和边组成：

节点类型：

- `Major`;
- `CourseModule`;
- `Skill`;
- `CareerPath`;
- `GraduatePath`;
- `Country`;
- `UniversityProgram`;
- `AdmissionRequirement`;
- `ProfessionalAccreditation`;
- `QualificationPathway`;
- `Source`;
- `UserProfileAttribute`。

边类型：

- `studies`;
- `develops`;
- `leads_to`;
- `similar_to`;
- `differs_from`;
- `offered_in`;
- `requires`;
- `accredited_by`;
- `has_pathway`;
- `supported_by_source`;
- `suitable_for`;
- `risky_for`;
- `equivalent_to`;
- `partially_equivalent_to`;
- `changed_from`;
- `changed_to`。

每条边应尽量记录来源、确定性和限制；没有来源支持的关系不能包装成确定事实。

## 核心步骤

1. 建立实体节点。
   - 从用户问题和专业画像中抽取 Major、Country、CourseModule、Skill、CareerPath、GraduatePath。
   - 从检索结果中抽取 UniversityProgram、AdmissionRequirement、ProfessionalAccreditation、QualificationPathway、Source。
   - 从用户画像中抽取 UserProfileAttribute。

2. 建立核心学习关系。
   - Major `studies` CourseModule。
   - Major `develops` Skill。
   - Major `leads_to` CareerPath 或 GraduatePath。

3. 建立比较关系。
   - Major `similar_to` Major。
   - Major `differs_from` Major。
   - 跨国术语高度对齐时使用 `equivalent_to`。
   - 只部分重合时使用 `partially_equivalent_to`。

4. 建立国家和项目关系。
   - UniversityProgram `offered_in` Country。
   - UniversityProgram `requires` AdmissionRequirement。
   - UniversityProgram `accredited_by` ProfessionalAccreditation。
   - Major 或 UniversityProgram `has_pathway` QualificationPathway。

5. 建立用户适配关系。
   - Major `suitable_for` UserProfileAttribute。
   - Major `risky_for` UserProfileAttribute。
   - 这些关系必须来自用户画像和 `major_fit_scoring`/`risk_scoring`，不能凭空推断。

6. 建立来源追踪。
   - Claim、Major、UniversityProgram、CourseModule、Accreditation 等关键节点或边必须 `supported_by_source` Source。
   - 来源节点应保留 currentness_basis、2025-01-01 最低底线状态、source_score 和 limitations。

7. 支持变化检测。
   - old entity `changed_to` new entity。
   - new entity `changed_from` old entity。
   - 使用 `change_record` 保存变化类型、来源和影响。

## 失败处理

- 来源不足：将相关节点或边 certainty 标为 `unknown`，不输出强结论。
- 来源冲突：保留冲突边，交给 `claim_verification` 标注 `conflicting`。
- 信息过多：只输出与用户问题相关的子图，避免无关泛化。
- 国家术语不等价：调用 `cross_country_alignment`，不要强行建立 `equivalent_to`。
- 受监管路径不明：调用 current/next-cycle 检索和专业认证规则，输出官方核查提醒。

## 与其他算法的关系

- 上游：`source_scoring`、`claim_verification`、`major_similarity`、`cross_country_alignment`、`change_detection`。
- 下游：`report_generation`、`uncertainty_management`、`major_explanation_workflow`、`multi_country_comparison_workflow`。
- 与 `major_profile` 互补：`major_profile` 是专业摘要结构，`knowledge_graph` 是关系结构。
