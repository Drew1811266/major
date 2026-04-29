# Explain Major Prompt

Explain the undergraduate major: {{major}}

Country scope:
{{countries}}

Freshness requirement:
- General stable field explanation may use stable knowledge.
- Current university, course, admissions, tuition, accreditation, employment, visa, work-policy, or policy claims must use current/next-cycle or current/next academic-year official sources first.
- 2025-01-01 is only the minimum freshness floor. A 2025-or-later source that is not clearly current must be labeled as limited, not latest.
- If no reliable current/next-cycle source is found, state that current information cannot be confirmed. If no source meeting the 2025-01-01 minimum floor is found, state: “我没有找到满足 2025 年及以后时效要求的可靠来源。”

Source priority:
- Prefer university official, department official, course catalog, admissions official, government, exam authority, official application platform, accreditation body, and labor statistics sources.
- China mainland university facts must prioritize current/next-cycle official admissions regulations, major catalogs, enrollment plans, subject selection requirements, professional groups, training programmes, university admissions site, Ministry of Education, Sunshine College Entrance Examination Platform, and provincial exam authorities.
- For China mainland candidate discovery, local repository records and ShanghaiRanking/软科 references may be used only as candidate or major-strength reference signals. They must not be used as current admissions evidence.
- For regulated pathways, output an official verification checklist: regulator/body to check, accreditation status, clinical/practicum/internship requirement, exam or registration path, applicable year or cycle.

Claim verification requirement:
- Before presenting current facts, verify claims using `claim_verification`.
- Claims that are outdated or not_found cannot be stated as current conclusions.

Uncertainty handling:
- high can be stated as current conclusion with citation.
- medium can be stated with limitations.
- low is reference only.
- unknown must be stated as unable to confirm.

Knowledge structure requirement:
- Run `major_similarity` before explaining adjacent majors.
- Use `knowledge_graph` to connect courses, skills, careers, graduate paths, country terms, qualification pathways, and sources.
- Use `cross_country_alignment` when country differences are part of the answer.
- Use `change_detection` if the user asks how the major, admissions catalog, curriculum, professional group, subject selection, tuition, or accreditation changed.
- Apply `professional_accreditation_rules` for regulated fields and state that本科专业 does not automatically grant professional qualification.

Required output:

1. What this major is;
2. What undergraduate students usually study;
3. Typical courses or modules;
4. Suitable students;
5. Students who should be cautious;
6. Similar majors and differences;
7. Country-specific differences;
8. Career and graduate-study directions;
9. Professional accreditation or qualification notes;
10. Knowledge graph summary: courses, skills, career paths, qualifications, and sources;
11. Source summary with currentness basis, 2025 minimum-floor status, source_id, source_score, claim_id, claim status, and uncertainty;
12. Questions to ask the user if personalization is needed;
13. If using China ranking references, explain that they are third-party references, not admissions, selection-subject, major-group, enrollment-plan, or employment guarantees.

Personalization requirement:
- If the user asks “我适合吗” or includes personal background, run `active_profile_completion`, then use `major_fit_scoring`, `risk_scoring`, and `constraint_filtering`.
- If the profile is incomplete, ask up to 5 dynamic questions and mark the fit judgment as preliminary.
- If the explanation includes recommendation language, include fit reasons, risks, alternatives, and next steps.
