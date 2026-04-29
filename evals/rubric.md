# Evaluation Rubric

Use this rubric to evaluate whether an answer correctly follows the `major` skill.

## Scoring Levels

- `excellent`: Fully satisfies the dimension with precise structure, correct caveats, and actionable next steps.
- `good`: Mostly satisfies the dimension with only minor omissions.
- `acceptable`: Handles the dimension at a basic level, but misses important nuance.
- `poor`: Attempts the dimension but is vague, incomplete, or partly misleading.
- `fail`: Missing, unsafe, unsupported, or directly contrary to major rules.

## Dimensions

### 1. Intent Recognition

- excellent: Correctly identifies primary and secondary intent, including explain_major, compare_majors, compare_countries, recommend_majors, evaluate_fit, university_program_lookup, admissions_lookup, source_check, change_comparison, report_generation, or unclear.
- fail: Answers a different task or ignores a required retrieval/recommendation/change workflow.

### 2. 2025+ Freshness Rule

- excellent: Treats 2025-01-01 as the minimum floor only, and prefers current-cycle, next-cycle, current academic-year, next academic-year, or active/current official sources for current facts.
- fail: Presents pre-2025 or archived information as current without caveat.

### 3. Official Source Priority

- excellent: Prioritizes university, department, catalog, admissions, government, exam authority, official application platform, accreditation body, and labor statistics sources.
- fail: Uses media, forums, blogs, agencies, or unsourced claims as primary current evidence.

### 4. China Mainland Handling

- excellent: For China mainland高校, asks for or uses province/exam region, intended entry year, subject combination, batch/pathway, and prioritizes current/next-cycle official sources including招生章程、招生专业目录、分省招生计划、选考科目要求、专业组、培养方案、高校本科招生网、教育部、阳光高考、省级考试院.
- fail: Ignores yearly changes or treats old招生目录 as current.

### 5. User Profile Completion

- excellent: For recommendation/fit tasks, evaluates profile completeness and asks only missing high-impact questions.
- fail: Gives personal recommendations without enough profile or boundary.

### 6. Question Limit

- excellent: Initial clarification asks at most 5 key questions and avoids repeating known information.
- fail: Asks too many questions or ignores known profile details.

### 7. Major Fit Explanation

- excellent: Explains interest, ability, study process, career goal, country system, and constraint fit.
- fail: Gives rankings or recommendations without fit rationale.

### 8. Risk Recognition

- excellent: Identifies skill gap, study pressure, admission, employment uncertainty, qualification, budget and language risks.
- fail: Omits material risks or overstates certainty.

### 9. Hard vs Soft Constraints

- excellent: Correctly distinguishes hard constraints from soft preferences and adjusts recommendation accordingly.
- fail: Treats soft preference as absolute exclusion or ignores hard constraints.

### 10. Similar Major Discovery

- excellent: Uses major_similarity to identify direct_match, adjacent_major, pathway_related, skill_related, interest_related, and misleading_match where relevant.
- fail: Provides only one professional direction for a broad interest word.

### 11. Knowledge Structure

- excellent: Connects major, courses, skills, careers, graduate paths, country terms, qualification pathways, user attributes, and sources.
- fail: Lists facts without explaining relationships or source support.

### 12. Cross-Country Alignment

- excellent: Correctly distinguishes China 本科专业, Korea 학과/전공/학부/모집단위, Japan 学部/学科/専攻/コース, UK course/programme/module, US major/minor/concentration, Australia course/degree/major/specialisation.
- fail: Treats translated labels as fully equivalent.

### 13. Change Detection

- excellent: Detects added, removed, renamed, moved_department, requirement_changed, enrollment_plan_changed, subject_selection_changed, curriculum_changed, tuition_changed, accreditation_changed, or unclear using old/new source sets.
- fail: Infers changes without comparable sources.

### 14. Claim Verification

- excellent: Breaks key facts into claims and labels supported, partially_supported, conflicting, not_found, outdated, or uncertain.
- fail: Presents claims without verification or status.

### 15. Uncertainty Level

- excellent: Uses high, medium, low, unknown appropriately and explains limitations.
- fail: Hides uncertainty or overstates weak evidence.

### 16. Professional Accreditation Warnings

- excellent: For medicine-related, nursing, pharmacy, psychology, law, education, architecture, engineering, accounting, veterinary, and social work, distinguishes academic study from professional qualification and points to official regulators.
- fail: Suggests本科 automatically grants professional qualification.

### 17. No Over-Promise

- excellent: Never guarantees admission, employment, salary, visa, immigration, or professional qualification.
- fail: Makes any guarantee or near-guarantee in these areas.

### 18. Actionable Advice

- excellent: Gives specific next steps: official pages to check, profile fields to supply, courses/projects to try, or questions to ask universities.
- fail: Ends with vague advice.

### 19. Structured Output

- excellent: Uses tables for comparison/source/change tasks and concise sections for explanation or recommendation.
- fail: Unstructured, hard to scan, or missing required sections.

### 20. Source Table And Freshness Explanation

- excellent: Includes source title, publisher, source type, URL, applicable year/cycle, access date, 2025+ status, supported claims, limitations, and source freshness.
- fail: Provides links without explaining freshness or supported claims.

### 21. ID Traceability

- excellent: Uses stable `source_id`, `claim_id`, `node_id`, `edge_id`, and `change_id` where structured records are requested; source, claim, graph, and change records reference each other consistently.
- fail: Provides claims or graph edges that cannot be traced back to source records.

### 22. Current-Cycle Handling

- excellent: Clearly distinguishes current/next-cycle evidence from a stale-but-2025-or-later source and labels limited currentness.
- fail: Treats a 2025 source as latest when newer current-cycle evidence should be checked.

### 23. China Province And Scope Handling

- excellent: Distinguishes national catalogs, provincial exam authority data, university admissions catalogs, provincial enrollment plans, major groups, subject selection requirements, and training programmes.
- fail: Mixes these scopes without limitations or generalizes one province to all provinces.

### 24. Executable Algorithm Consistency

- excellent: Scoring, certainty, similarity type, and change diff explanations match the documented formulas and `scripts/algorithm_utils.py`.
- fail: Gives ad hoc scores or categories inconsistent with documented formulas.

### 25. Privacy And Profile Minimization

- excellent: Asks only necessary profile questions, avoids unrelated sensitive data, uses coarse budget levels, and continues with limited advice if the user declines sensitive details.
- fail: Requests身份证号、详细家庭资产、精确住址 or other unnecessary sensitive information.

### 26. China Major Repository Use

- excellent: Uses the local China repository only for candidate generation or structured lookup, then verifies current admissions facts with official current/next-cycle sources.
- fail: Treats a local repository record as proof that a major is currently admitting, available in a province, or valid for a subject combination.

### 27. China Ranking Reference Boundary

- excellent: Uses ShanghaiRanking/软科 or similar rankings only as third-party major-strength references, with clear limitations and official-verification next steps.
- fail: Treats rankings as official admissions evidence or implies ranking guarantees admission, employment, salary, or professional outcomes.

## Automatic Failure Conditions

Mark the answer as `fail` if it:

- Guarantees admission, employment, salary, visa, immigration, or professional qualification.
- Presents time-sensitive claims as current without source or caveat.
- Gives personalized recommendations without sufficient profile or clarifying questions.
- Ignores本科 scope when the user did not ask for graduate content.
- Uses non-official or marketing sources as the sole basis for program, accreditation, admissions, tuition, deadline, or policy claims.
- Treats an alias, translation, department, course, 학부, 学部, course, degree, concentration, stream, or specialisation as fully equivalent without verification.
- Uses old sources as current evidence when no 2025+ source is found.
- Asks for unnecessary sensitive personal data for major recommendations.
- Outputs source/claim/graph/change records with broken ID references.
- Uses a China local repository record or third-party ranking as the sole evidence for current招生专业、专业组、选科要求、分省计划 or培养方案.
