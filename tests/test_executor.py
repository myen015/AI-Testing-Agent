
from unittest.mock import patch

from app.agent.test_case import TestCaseModel, TestStepModel
from app.agent.test_executor import TestExecutorService


class FakeResponse:
    status = 200


class FakeBrowser:
    console_errors = []
    page_errors = []

    def navigate(self, url):
        return FakeResponse()

    def get_title(self):
        return "Example Domain"

    def get_body_text(self):
        return "This domain is for use in documentation examples"

    def close(self):
        pass


def run_test_case(test_case):
    with patch(
        "app.agent.test_executor.BrowserClient"
    ) as browser_class:
        browser_class.return_value.open.return_value = FakeBrowser()
        return TestExecutorService().run(test_case)


def test_executor_passes_when_title_matches():
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

    result = run_test_case(test_case)

    assert result["http_status"] == 200
    assert result["passed"] is True
    assert result["steps"][0]["actual"] == "Example Domain"


def test_executor_fails_when_title_does_not_match():
    test_case = TestCaseModel(
        name="Check incorrect title",
        url="https://example.com",
        steps=[
            TestStepModel(
                action="check_title",
                expected="Wrong Title",
            )
        ],
    )

    result = run_test_case(test_case)

    assert result["passed"] is False
    assert result["steps"][0]["actual"] == "Example Domain"


def test_executor_reports_unsupported_action():
    test_case = TestCaseModel(
        name="Check unsupported action",
        url="https://example.com",
        steps=[
            TestStepModel(
                action="click_button",
                expected="Button clicked",
            )
        ],
    )

    result = run_test_case(test_case)

    assert result["passed"] is False
    assert "Unsupported action" in result["steps"][0]["error"]


def test_executor_checks_text_on_page():
    test_case = TestCaseModel(
        name="Check page content",
        url="https://example.com",
        steps=[
            TestStepModel(
                action="check_text",
                expected="This domain is for use in documentation examples",
            )
        ],
    )

    result = run_test_case(test_case)

    assert result["passed"] is True
    assert result["steps"][0]["passed"] is True
