# Major Explanation Workflow

Use when the user wants to understand one undergraduate major, a country-specific version of a major, or the difference between a major and adjacent fields.

## Steps

```text
用户输入
→ intent_router
→ major_similarity 判断是否有相近专业需要解释
→ 如涉及具体国家或大学，执行 current/next-cycle retrieval
→ source_scoring
→ claim_verification
→ knowledge_graph 整理课程、技能、职业、相近专业
→ uncertainty_management
→ 输出专业介绍
```

1. Identify the major and scope.
   - Default to undergraduate.
   - Detect country, university, professional accreditation, and whether the user needs personalization.
   - If the major name is broad, use `major_similarity` and `data/major_aliases.yaml` to expand possible official names and adjacent fields.

2. Explain adjacent majors.
   - Use `major_similarity` to list direct matches, adjacent majors, pathway-related majors, skill-related majors, interest-related majors, and misleading matches.
   - Explain differences rather than only listing names.

3. Decide whether retrieval is required.
   - Stable field explanations can use stable knowledge.
   - Concrete facts about university programs, course lists, admissions, tuition, deadlines, accreditation, employment data, visa/work policy, or qualification pathways require current/next-cycle retrieval.
   - China mainland university facts must prioritize current/next-cycle undergraduate admissions regulations, admissions major catalogs, enrollment plans, subject selection requirements, professional groups, training programmes, university admissions pages, Ministry of Education, Sunshine College Entrance Examination Platform, and provincial exam authorities.

4. Score and verify sources.
   - Run `source_scoring`.
   - Run `claim_verification` for current facts.
   - Claims that are `outdated`, `not_found`, or `conflicting` cannot be presented as certain current conclusions.

5. Build knowledge graph.
   - Use `knowledge_graph` to connect Major, CourseModule, Skill, CareerPath, GraduatePath, Country, UniversityProgram, AdmissionRequirement, ProfessionalAccreditation, QualificationPathway, Source, and UserProfileAttribute.
   - Use graph links to support courses, skills, careers, adjacent majors, country terms, accreditation risk, and source traceability.

6. Add professional accreditation warnings.
   - Use `data/professional_accreditation_rules.yaml` for medicine-related, nursing, pharmacy, psychology, law, education, architecture, engineering, accounting, veterinary, and social work.
   - Never say that a本科专业 automatically grants professional qualification.

7. Output with uncertainty.
   - Mark source freshness and certainty level.
   - If no current/next-cycle source is found for concrete facts, say so clearly and label minimum-floor sources as limited.
   - If user asks for fit but profile is incomplete, ask up to 5 questions.

## Default Output

```markdown
## 1. 这个专业是什么

## 2. 本科阶段通常学什么

## 3. 适合什么样的学生

## 4. 不太适合什么样的学生

## 5. 和相近专业的区别

| 专业 | 相似类型 | 共同课程/技能 | 主要差异 | 风险提醒 |
|---|---|---|---|---|

## 6. 不同国家的差异

## 7. 未来方向

## 8. 资格认证与误区提醒

## 9. 给用户的建议

## 来源、时效与不确定性
```
