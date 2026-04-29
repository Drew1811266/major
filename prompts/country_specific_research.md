# Country-Specific Major Research Prompt

When researching a major in a specific country, default to current/next-cycle official sources, with 2025-01-01 only as the minimum freshness floor.

Research target:
- Major: {{major}}
- Country: {{country}}
- User profile: {{user_profile}}

Freshness requirement:
- Use current/next admissions-cycle, current/next entry-year, current/next academic-year, or active/current official pages first.
- Treat 2025-01-01 as the minimum floor only; 2025-or-later but not clearly current sources must be labeled as limited.
- Accept official current pages only when they clearly show the programme is active/current and are not archived/outdated.
- If no reliable current/next-cycle source is found, state that current information cannot be confirmed. If no source meeting the 2025-01-01 minimum floor is found, state: “我没有找到满足 2025 年及以后时效要求的可靠来源。”
- Do not use pre-2025 sources as current evidence unless the user explicitly accepts historical background.

Source priority:
- China: prioritize current/next-cycle 本科招生章程、招生简章、招生专业目录、分省招生计划、选考科目要求、专业组、培养方案、高校本科招生网、教育部、阳光高考、省级考试院、高校教务处、院系官网。
- China candidate discovery may use the local China major repository before retrieval, but repository records and ShanghaiRanking/软科 references are only candidate or ranking-reference signals.
- UK/US/Australia/Japan/South Korea: prioritize 2026 entry, 2027 entry, current undergraduate course/programme, 2026-2027 or later undergraduate catalog, latest admissions requirements, latest tuition fees, latest course handbook.
- Prefer university official pages, department official pages, course catalogs, admissions pages, government, official application platforms, accreditation bodies, and labor statistics.
- Regulated pathways must include an official verification checklist covering regulator/body, accreditation status, clinical/practicum/internship requirement, exam or registration path, and applicable year or cycle.

Claim verification requirement:
- Verify programme availability, admissions requirements, course structure, tuition, deadlines, accreditation, qualification pathway, employment data, country system rules, and change claims before presenting them as current facts.
- Do not present unsupported, outdated, or not_found claims as certain.

Uncertainty handling:
- Use high/medium/low/unknown certainty labels.
- Explain source limitations and what official source would be needed.

Knowledge and alignment requirements:
- Run `major_similarity` when the major name is broad, translated, or ambiguous.
- Run `knowledge_graph` to connect local programme names, course modules, skills, careers, qualifications, and sources.
- Run `cross_country_alignment` if the answer compares this country with another country.
- Run `change_detection` if the user asks about changes across years or current vs historical information.
- Apply `professional_accreditation_rules` for regulated fields and remind the user to verify official regulator requirements.

Output:
- Current major/programme names;
- Country-specific terminology;
- Undergraduate structure;
- Typical courses or modules;
- Admission or application notes, if available from current/next-cycle sources or clearly labeled minimum-floor sources;
- Professional accreditation or license notes, if relevant;
- Similar or misleading nearby majors;
- Knowledge graph summary of courses, skills, careers, qualifications, and sources;
- Source table with source_id, freshness, currentness_basis, source_score, and supported claim_id fields;
- Verified claims;
- Uncertainties and limitations.
- China repository or ranking-reference notes, if used, with official-verification checklist.
