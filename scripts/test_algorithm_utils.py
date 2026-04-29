#!/usr/bin/env python3
"""Unit tests for deterministic major algorithm helpers."""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

import algorithm_utils as alg
import validate_records


class AlgorithmUtilsTests(unittest.TestCase):
    def test_source_score_prefers_current_official_source(self) -> None:
        result = alg.compute_source_score(
            {
                "source_type": "university_official",
                "is_2025_or_later": True,
                "currentness_basis": "current_admissions_cycle",
                "relevance_score": 1,
                "specificity_score": 1,
                "corroboration_score": 1,
                "country_match_score": 1,
                "archive_or_current_status": "current",
            }
        )
        self.assertGreaterEqual(result["source_score"], 0.8)
        self.assertEqual(result["reliability_level"], "high")

    def test_stale_2025_source_is_limited(self) -> None:
        result = alg.compute_source_score(
            {
                "source_type": "university_official",
                "is_2025_or_later": True,
                "currentness_basis": "minimum_2025_floor_only",
                "freshness_score": 1.0,
                "relevance_score": 1,
                "specificity_score": 1,
                "corroboration_score": 1,
                "country_match_score": 1,
                "archive_or_current_status": "current",
            }
        )
        self.assertLessEqual(result["freshness_score"], 0.6)
        self.assertNotEqual(result["reliability_level"], "high")

    def test_archived_official_source_is_downgraded(self) -> None:
        result = alg.compute_source_score(
            {
                "source_type": "university_official",
                "is_2025_or_later": True,
                "currentness_basis": "current_admissions_cycle",
                "relevance_score": 1,
                "specificity_score": 1,
                "corroboration_score": 1,
                "country_match_score": 1,
                "archive_or_current_status": "archived",
            }
        )
        self.assertNotEqual(result["reliability_level"], "high")

    def test_ranking_reference_cannot_be_high_reliability(self) -> None:
        result = alg.compute_source_score(
            {
                "source_type": "ranking_reference",
                "is_2025_or_later": True,
                "currentness_basis": "current_admissions_cycle",
                "relevance_score": 1,
                "specificity_score": 1,
                "corroboration_score": 1,
                "country_match_score": 1,
                "archive_or_current_status": "current",
            }
        )
        self.assertNotEqual(result["reliability_level"], "high")

    def test_local_repository_without_official_verification_is_downgraded(self) -> None:
        result = alg.compute_source_score(
            {
                "source_type": "local_repository_record",
                "is_2025_or_later": True,
                "currentness_basis": "minimum_2025_floor_only",
                "relevance_score": 1,
                "specificity_score": 1,
                "corroboration_score": 0,
                "country_match_score": 1,
                "archive_or_current_status": "current",
            }
        )
        self.assertLess(result["source_score"], 0.5)

    def test_yaml_config_changes_source_score(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as handle:
            handle.write(
                "source_scoring:\n"
                "  weights:\n"
                "    authority_score: 1.0\n"
                "    freshness_score: 0.0\n"
                "    relevance_score: 0.0\n"
                "    specificity_score: 0.0\n"
                "    corroboration_score: 0.0\n"
                "    country_match_score: 0.0\n"
                "  penalties: {}\n"
                "  reliability_thresholds:\n"
                "    high: 0.8\n"
                "    medium: 0.6\n"
                "    low: 0.3\n"
            )
            path = Path(handle.name)
        try:
            config = alg.load_scoring_config(path)
            result = alg.compute_source_score(
                {
                    "source_type": "media",
                    "authority_score": 0.2,
                    "is_2025_or_later": True,
                    "currentness_basis": "current_admissions_cycle",
                    "relevance_score": 1,
                    "specificity_score": 1,
                    "corroboration_score": 1,
                    "country_match_score": 1,
                    "archive_or_current_status": "current",
                },
                config=config,
            )
            self.assertAlmostEqual(result["source_score"], 0.2)
        finally:
            path.unlink(missing_ok=True)

    def test_fit_and_risk_scores(self) -> None:
        fit = alg.compute_fit_score(
            {
                "interest_match": 0.9,
                "ability_match": 0.8,
                "study_process_match": 0.7,
                "career_goal_match": 0.8,
                "country_system_match": 0.7,
                "constraint_match": 0.9,
            }
        )
        risk = alg.compute_risk_score({"skill_gap_risk": 0.1, "study_pressure_risk": 0.2})
        self.assertEqual(fit["fit_level"], "high")
        self.assertEqual(risk["risk_level"], "low")

    def test_similarity_and_diff(self) -> None:
        self.assertEqual(
            alg.classify_similarity_type(course_overlap=0.7, skill_overlap=0.7),
            "adjacent_major",
        )
        changes = alg.diff_change_records({"major_group": "A"}, {"major_group": "B"})
        self.assertEqual(changes[0]["change_type"], "subject_selection_changed")

    def test_traceability_validation(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "valid_traceability.json"
        validate_records.validate_records(json.loads(path.read_text(encoding="utf-8")))

    def test_traceability_validation_rejects_minimal_source(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "invalid_minimal_source.json"
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            validate_records.validate_records(json.loads(path.read_text(encoding="utf-8")))

    def test_traceability_validation_rejects_missing_reference(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals" / "fixtures" / "invalid_missing_reference.json"
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            validate_records.validate_records(json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
