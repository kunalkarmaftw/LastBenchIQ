"""StudentProfile completeness.

`is_complete` gates `predict_placement`. If it is wrong, the Career Agent
predicts from nulls and returns a confident number built on nothing - which is
worse than refusing, because the student has no way to tell.
"""

import pytest

from app.models.user import CareerGoal, StudentProfile

pytestmark = pytest.mark.unit


def _profile(**overrides: object) -> StudentProfile:
    base = {
        "ssc_percentage": 78.0,
        "hsc_percentage": 72.5,
        "degree_percentage": 68.0,
        "degree_stream": "Sci&Tech",
        "work_experience": False,
    }
    base.update(overrides)
    return StudentProfile(**base)


def test_complete_profile_is_complete() -> None:
    assert _profile().is_complete is True
    assert _profile().missing_fields == []


def test_missing_field_blocks_completeness() -> None:
    profile = _profile(degree_percentage=None)
    assert profile.is_complete is False
    assert "degree_percentage" in profile.missing_fields


def test_work_experience_false_still_counts_as_provided() -> None:
    """False is a real answer, not a missing one.

    A truthiness check here would treat "no work experience" as unanswered and
    block every fresher - the majority of users.
    """
    profile = _profile(work_experience=False)
    assert profile.is_complete is True


def test_optional_fields_do_not_affect_completeness() -> None:
    """Fields the model does not consume must never block a prediction."""
    profile = _profile(entrance_test_percentage=None, specialisation=None)
    assert profile.is_complete is True


def test_career_goal_values_are_lowercase() -> None:
    """The database stores enum VALUES; the API speaks the same strings."""
    assert CareerGoal.MBA.value == "mba"
    assert {g.value for g in CareerGoal} == {"mba", "job", "undecided"}
