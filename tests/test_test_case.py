
import pytest
from pydantic import ValidationError

from app.agent.test_case import TestCaseModel, TestStepModel


def test_create_valid_test_case():
    test_case = TestCaseModel(
        name="Check example page",
        url="https://example.com",
        steps=[
            TestStepModel(
                action="check_title",
                expected="Example Domain",
            )
        ],
    )

    assert test_case.name == "Check example page"
    assert test_case.url == "https://example.com"
    assert len(test_case.steps) == 1
    assert test_case.steps[0].action == "check_title"


def test_test_case_requires_name():
    with pytest.raises(ValidationError):
        TestCaseModel(
            url="https://example.com",
            steps=[],
        )


def test_test_step_requires_expected_result():
    with pytest.raises(ValidationError):
        TestStepModel(action="check_title")
