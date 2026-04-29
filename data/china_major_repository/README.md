# China Major Repository

This directory defines the local China mainland undergraduate major repository for `major`.

It ships metadata, source rules, import mappings, and synthetic sample records only. It does not bundle the full ShanghaiRanking 2025 China University Major Ranking or any other full third-party ranking dataset.

## Rules

- Use repository records for candidate generation and preliminary filtering only.
- Use ShanghaiRanking-style records only as third-party major-strength references.
- Do not use local repository records or ranking references as final evidence for current admissions, provincial enrollment plans, major groups, subject-selection requirements, tuition, deadlines, or training programmes.
- For current China mainland admissions facts, verify with current/next-cycle official sources: university admissions office, Sunshine College Entrance Examination Platform, provincial exam authority, Ministry of Education, academic affairs office, or college/department official pages.
- Authorized deployments may import CSV/JSON through `scripts/china_major_repository_import.py`.

## Expected Data Boundary

The repository may contain:

- university-major candidate records;
- official catalog references;
- authorized ranking references;
- source IDs and claim IDs;
- fields requiring official verification.

The repository must not contain:

- unauthorized full ranking snapshots;
- unverified claims that a major is currently admitting;
- province-specific admissions conclusions without province, entry year, subject combination, batch/pathway, and official source scope.
