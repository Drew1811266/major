# Multi Country Comparison Workflow

Use when the user asks to compare one undergraduate major across China, South Korea, Japan, the UK, the US, and Australia, or compare different majors across countries.

## Steps

```text
用户输入
→ 识别国家和专业
→ 对每个国家执行术语映射
→ 执行 current/next-cycle 检索
→ cross_country_alignment
→ 对齐维度比较
→ 输出等价程度、差异、风险和来源
```

1. Identify countries and majors.
   - If countries are not specified, default to the six supported countries only when a broad cross-country answer is useful.
   - Keep the scope本科阶段 unless the user explicitly asks otherwise.

2. Map terminology for each country.
   - China: 本科专业、学科门类、专业类、专业目录、培养方案、招生专业。
   - South Korea: `학과`、`전공`、`학부`、`단과대학`、`모집단위`。
   - Japan: `学部`、`学科`、`専攻`、`コース`、`課程`。
   - United Kingdom: `course`、`programme`、`subject`、`degree`、`module`。
   - United States: `major`、`minor`、`concentration`、`department`、`undergraduate program`。
   - Australia: `course`、`degree`、`major`、`stream`、`specialisation`。
   - Use `data/country_terms.yaml` and `data/country_alignment_rules.yaml`.

3. Retrieve current sources when facts are specific.
   - Run `time_aware_retrieval` and `hybrid_retrieval`.
   - Prefer current/next-cycle official sources; use 2025-01-01 only as the minimum freshness floor.
   - Do not use archived or older pages as current evidence.

4. Run `cross_country_alignment`.
   - Compare local names, application unit, professional level, curriculum structure, core courses, duration, portfolio/lab/clinical/internship requirements, career path, professional accreditation, graduate or extra qualification needs, and terminology translatability.
   - Assign `equivalence_level`: exact, close, partial, pathway_related, not_equivalent, or unknown.

5. Verify and mark uncertainty.
   - Run `source_scoring`, `claim_verification`, and `uncertainty_management`.
   - If only one university source is available, state that it is not a national rule.
   - For regulated pathways, add professional accreditation warnings.

## Default Table

```markdown
| 维度 | 中国 | 韩国 | 日本 | 英国 | 美国 | 澳大利亚 |
|---|---|---|---|---|---|---|
| 常见名称/术语 | | | | | | |
| 申请或培养单位 | | | | | | |
| 专业层级 | | | | | | |
| 本科学制/学位 | | | | | | |
| 课程结构 | | | | | | |
| 实践训练 | | | | | | |
| 认证/资格关联 | | | | | | |
| 等价程度 | | | | | | |
| 主要风险 | | | | | | |
| 来源确定性 | | | | | | |
```

After the table, explain which differences matter for student choice and what must be verified with current/next-cycle official sources.
