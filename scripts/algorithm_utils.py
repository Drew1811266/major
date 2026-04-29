#!/usr/bin/env python3
"""Deterministic helper algorithms for the major skill.

These helpers mirror the formulas documented in algorithms/*.md. They are small
pure functions so validation and eval checks can exercise scoring behavior
without relying on a model's free-form reasoning.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is expected in the skill runtime.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]

SOURCE_WEIGHTS = {
    "authority_score": 0.30,
    "freshness_score": 0.25,
    "relevance_score": 0.20,
    "specificity_score": 0.10,
    "corroboration_score": 0.10,
    "country_match_score": 0.05,
}

SOURCE_PENALTIES = {
    "pre_2025_without_current_applicability": 0.50,
    "unofficial_without_cross_validation": 0.25,
    "no_publication_or_update_date": 0.10,
    "archived_or_outdated_page": 0.40,
}

AUTHORITY_BY_TYPE = {
    "university_official": 1.0,
    "admissions_official": 1.0,
    "course_catalog": 0.95,
    "government": 0.95,
    "exam_authority": 0.95,
    "official_application_platform": 0.9,
    "accreditation_body": 0.95,
    "department_official": 0.85,
    "labor_statistics": 0.8,
    "industry_association": 0.7,
    "education_platform": 0.45,
    "ranking_reference": 0.65,
    "local_repository_record": 0.30,
    "media": 0.35,
    "forum": 0.1,
    "blog": 0.1,
    "other": 0.2,
}

FIT_WEIGHTS = {
    "interest_match": 0.30,
    "ability_match": 0.20,
    "study_process_match": 0.15,
    "career_goal_match": 0.15,
    "country_system_match": 0.10,
    "constraint_match": 0.10,
}

RISK_WEIGHTS = {
    "skill_gap_risk": 0.25,
    "study_pressure_risk": 0.20,
    "admission_risk": 0.20,
    "employment_uncertainty_risk": 0.15,
    "qualification_risk": 0.10,
    "budget_or_language_risk": 0.10,
}

QUESTION_WEIGHTS = {
    "decision_impact": 0.40,
    "uncertainty_reduction": 0.30,
    "field_importance": 0.20,
    "user_burden_penalty": -0.10,
}

CURRENTNESS_STRONG_SIGNALS = {
    "current_admissions_cycle",
    "next_admissions_cycle",
    "current_academic_year",
    "next_academic_year",
    "current_calendar_year",
    "active_current_official_page",
}

HIGH_AUTHORITY_SOURCE_TYPES = {
    "university_official",
    "admissions_official",
    "course_catalog",
    "government",
    "exam_authority",
    "official_application_platform",
    "accreditation_body",
    "department_official",
}

REFERENCE_ONLY_SOURCE_TYPES = {
    "ranking_reference",
    "local_repository_record",
}


def load_scoring_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load scoring configuration from data/scoring_weights.yaml with fallbacks."""

    path = Path(config_path) if config_path else ROOT / "data" / "scoring_weights.yaml"
    if yaml is None or not path.exists():
        return {
            "source_scoring": {
                "weights": SOURCE_WEIGHTS,
                "penalties": SOURCE_PENALTIES,
                "reliability_thresholds": {"high": 0.80, "medium": 0.60, "low": 0.30},
            },
            "major_fit_scoring": {"weights": FIT_WEIGHTS},
            "risk_scoring": {"weights": RISK_WEIGHTS},
            "question_selection": {"weights": QUESTION_WEIGHTS},
        }
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.setdefault("source_scoring", {})
    data["source_scoring"].setdefault("weights", SOURCE_WEIGHTS)
    data["source_scoring"].setdefault("penalties", SOURCE_PENALTIES)
    data["source_scoring"].setdefault("reliability_thresholds", {"high": 0.80, "medium": 0.60, "low": 0.30})
    data.setdefault("major_fit_scoring", {}).setdefault("weights", FIT_WEIGHTS)
    data.setdefault("risk_scoring", {}).setdefault("weights", RISK_WEIGHTS)
    data.setdefault("question_selection", {}).setdefault("weights", QUESTION_WEIGHTS)
    return data


def clamp(value: Any, minimum: float = 0.0, maximum: float = 1.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0
    return max(minimum, min(maximum, number))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "unknown"


def stable_hash(parts: Iterable[Any], length: int = 8) -> str:
    raw = "|".join("" if part is None else str(part) for part in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:length]


def make_stable_id(kind: str, *parts: Any, year: str | int | None = None) -> str:
    """Create a deterministic ID matching data/id_rules.yaml style."""

    prefix = {
        "source": "src",
        "claim": "clm",
        "node": "node",
        "edge": "edge",
        "change": "chg",
    }.get(kind, kind)
    slugs = [slugify(str(part)) for part in parts if part not in (None, "")]
    if year is not None:
        slugs.append(slugify(str(year)))
    digest = stable_hash([kind, *parts, year])
    return "_".join([prefix, *slugs, digest])


def infer_freshness_score(source: Mapping[str, Any]) -> float:
    currentness = source.get("currentness_basis")
    if currentness in CURRENTNESS_STRONG_SIGNALS:
        return 1.0
    if source.get("is_2025_or_later") is True:
        return 0.60 if currentness == "minimum_2025_floor_only" else 0.85
    if source.get("freshness_basis") == "historical_user_requested":
        return 0.30
    return 0.0


def compute_source_score(
    source: Mapping[str, Any],
    weights: Mapping[str, float] | None = None,
    config: Mapping[str, Any] | None = None,
) -> dict[str, float | str]:
    """Compute source_score using the documented source_scoring formula."""

    scoring_config = dict(config or load_scoring_config())
    source_config = scoring_config.get("source_scoring", {})
    weights = dict(weights or source_config.get("weights", SOURCE_WEIGHTS))
    penalties = dict(source_config.get("penalties", SOURCE_PENALTIES))
    thresholds = dict(source_config.get("reliability_thresholds", {"high": 0.80, "medium": 0.60, "low": 0.30}))
    inferred_freshness = infer_freshness_score(source)
    provided_freshness = source.get("freshness_score")
    freshness_score = inferred_freshness if provided_freshness is None else min(clamp(provided_freshness), inferred_freshness)
    components = {
        "authority_score": clamp(source.get("authority_score", AUTHORITY_BY_TYPE.get(str(source.get("source_type")), 0.2))),
        "freshness_score": freshness_score,
        "relevance_score": clamp(source.get("relevance_score", 0.0)),
        "specificity_score": clamp(source.get("specificity_score", 0.0)),
        "corroboration_score": clamp(source.get("corroboration_score", 0.0)),
        "country_match_score": clamp(source.get("country_match_score", 0.0)),
    }
    penalty = 0.0
    if source.get("is_2025_or_later") is False and source.get("freshness_basis") != "historical_user_requested":
        penalty += penalties.get("pre_2025_without_current_applicability", SOURCE_PENALTIES["pre_2025_without_current_applicability"])
    if source.get("source_type") in {"education_platform", "media", "forum", "blog", "other"} and components["corroboration_score"] < 0.5:
        penalty += penalties.get("unofficial_without_cross_validation", SOURCE_PENALTIES["unofficial_without_cross_validation"])
    if source.get("source_type") == "local_repository_record" and not source.get("officially_verified"):
        penalty += penalties.get("local_repository_without_official_verification", 0.35)
    if not source.get("published_date") and not source.get("updated_date") and source.get("currentness_basis") in {None, "unknown"}:
        penalty += penalties.get("no_publication_or_update_date", SOURCE_PENALTIES["no_publication_or_update_date"])
    if source.get("archive_or_current_status") in {"archived", "outdated"}:
        penalty += penalties.get("archived_or_outdated_page", SOURCE_PENALTIES["archived_or_outdated_page"])

    raw_score = sum(components[key] * weights[key] for key in weights) - penalty
    score = clamp(raw_score)
    high_allowed = (
        source.get("source_type") in HIGH_AUTHORITY_SOURCE_TYPES
        and source.get("currentness_basis") in CURRENTNESS_STRONG_SIGNALS
        and source.get("archive_or_current_status") not in {"archived", "outdated", "historical"}
    )
    if score >= thresholds.get("high", 0.80) and high_allowed:
        reliability = "high"
    elif score >= thresholds.get("medium", 0.60):
        reliability = "medium"
    elif score >= thresholds.get("low", 0.30):
        reliability = "low"
    else:
        reliability = "unknown"
    if source.get("currentness_basis") == "minimum_2025_floor_only" and reliability == "high":
        reliability = "medium"
    if source.get("source_type") in REFERENCE_ONLY_SOURCE_TYPES and reliability == "high":
        reliability = "medium"
    return {**components, "outdated_penalty": round(penalty, 4), "source_score": round(score, 4), "reliability_level": reliability}


def compute_question_score(values: Mapping[str, Any]) -> float:
    weights = load_scoring_config().get("question_selection", {}).get("weights", QUESTION_WEIGHTS)
    score = (
        clamp(values.get("decision_impact")) * weights["decision_impact"]
        + clamp(values.get("uncertainty_reduction")) * weights["uncertainty_reduction"]
        + clamp(values.get("field_importance")) * weights["field_importance"]
        + clamp(values.get("user_burden_penalty")) * weights["user_burden_penalty"]
    )
    return round(clamp(score), 4)


def compute_fit_score(values: Mapping[str, Any]) -> dict[str, float | str]:
    weights = load_scoring_config().get("major_fit_scoring", {}).get("weights", FIT_WEIGHTS)
    score = sum(clamp(values.get(key)) * weight for key, weight in weights.items())
    score = round(clamp(score), 4)
    if score >= 0.75:
        level = "high"
    elif score >= 0.60:
        level = "medium"
    elif score >= 0.45:
        level = "cautious"
    else:
        level = "low"
    return {"fit_score": score, "fit_level": level}


def compute_risk_score(values: Mapping[str, Any]) -> dict[str, float | str]:
    weights = load_scoring_config().get("risk_scoring", {}).get("weights", RISK_WEIGHTS)
    score = sum(clamp(values.get(key)) * weight for key, weight in weights.items())
    score = round(clamp(score), 4)
    if score >= 0.70:
        level = "high"
    elif score >= 0.35:
        level = "medium"
    else:
        level = "low"
    return {"risk_score": score, "risk_level": level}


def classify_certainty(
    verification_status: str | None = None,
    source_score: float | None = None,
    current_or_next_cycle: bool = False,
    official_source: bool = False,
) -> str:
    if verification_status in {"not_found", "outdated"}:
        return "unknown"
    if verification_status == "conflicting":
        return "low"
    score = clamp(source_score)
    if verification_status == "supported" and official_source and current_or_next_cycle and score >= 0.80:
        return "high"
    if verification_status in {"supported", "partially_supported"} and score >= 0.60:
        return "medium"
    if score >= 0.30:
        return "low"
    return "unknown"


def classify_similarity_type(
    *,
    direct_name_match: bool = False,
    course_overlap: float = 0.0,
    skill_overlap: float = 0.0,
    career_overlap: float = 0.0,
    interest_overlap: float = 0.0,
    misleading: bool = False,
) -> str:
    if misleading:
        return "misleading_match"
    if direct_name_match and course_overlap >= 0.65:
        return "direct_match"
    if course_overlap >= 0.55 and skill_overlap >= 0.55:
        return "adjacent_major"
    if career_overlap >= 0.60:
        return "pathway_related"
    if skill_overlap >= 0.60:
        return "skill_related"
    if interest_overlap >= 0.50:
        return "interest_related"
    return "misleading_match" if direct_name_match else "interest_related"


def diff_change_records(
    old: Mapping[str, Any],
    new: Mapping[str, Any],
    fields: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Return field-level changes between old and new records."""

    fields = list(fields or sorted(set(old) | set(new)))
    changes: list[dict[str, Any]] = []
    for field in fields:
        old_value = old.get(field)
        new_value = new.get(field)
        if old_value == new_value:
            continue
        if old_value in (None, "", []):
            change_type = "added"
        elif new_value in (None, "", []):
            change_type = "removed"
        elif field in {"major_name", "programme_name", "name"}:
            change_type = "renamed"
        elif field in {"college_or_department", "department_or_school"}:
            change_type = "moved_department"
        elif field in {"subject_selection_requirement", "major_group"}:
            change_type = "subject_selection_changed"
        elif field in {"provincial_enrollment_plan", "enrollment_plan", "enrollment_plan_scope"}:
            change_type = "enrollment_plan_changed"
        elif field in {"training_programme", "core_courses", "course_structure", "core_modules"}:
            change_type = "curriculum_changed"
        elif field in {"tuition", "tuition_fees"}:
            change_type = "tuition_changed"
        elif field in {"accreditation_status"}:
            change_type = "accreditation_changed"
        else:
            change_type = "requirement_changed"
        changes.append({"field": field, "change_type": change_type, "old_value": old_value, "new_value": new_value})
    return changes


if __name__ == "__main__":
    example = {
        "source_type": "university_official",
        "is_2025_or_later": True,
        "currentness_basis": "current_admissions_cycle",
        "relevance_score": 1,
        "specificity_score": 1,
        "corroboration_score": 0.8,
        "country_match_score": 1,
        "archive_or_current_status": "current",
    }
    print(compute_source_score(example))
