
import json

from app.agent.runner import AgentRunner
from app.agent.test_case import TestCaseModel, TestStepModel
from app.agent.report_writer import ReportWriter


def successful_result(test_case):
    return {
        "test_name": test_case.name,
        "url": str(test_case.url),
        "http_status": 200,
        "steps": [
            {
                "action": step.action,
                "expected": step.expected,
                "actual": step.expected,
                "passed": True,
            }
            for step in test_case.steps
        ],
        "passed": True,
        "console_errors": [],
        "page_errors": [],
    }


def test_runner_executes_test_and_saves_report(tmp_path):
    test_case = TestCaseModel(
        name="Check example page",
        url="https://example.com",
        steps=[
            TestStepModel(
                action="check_title",
                expected="Example Domain",
            ),
            TestStepModel(
                action="check_text",
                expected="This domain is for use in documentation examples",
            ),
        ],
    )

    runner = AgentRunner()
    runner.executor.run = lambda case: successful_result(case)
    runner.report_writer.save = lambda result: ReportWriter().save(
        result,
        str(tmp_path / "latest.json"),
    )

    result = runner.run(test_case)

    report_path = tmp_path / "latest.json"
    assert report_path.exists()

    saved_result = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert result["passed"] is True
    assert saved_result["test_name"] == "Check example page"
    assert saved_result["passed"] is True


class FakeGenerator:
    def generate(self, url: str, requirement: str) -> TestCaseModel:
        return TestCaseModel(
            name="Generated homepage test",
            url=url,
            steps=[
                TestStepModel(
                    action="check_title",
                    expected="Example Domain",
                )
            ],
        )


def test_runner_generates_executes_and_saves_report(tmp_path):
    runner = AgentRunner()
    runner.generator = FakeGenerator()
    runner.executor.run = lambda case: successful_result(case)

    runner.report_writer.save = lambda result: ReportWriter().save(
        result,
        str(tmp_path / "generated_report.json"),
    )

    result = runner.generate_and_run(
        url="https://example.com",
        requirement='The homepage title must be "Example Domain".',
    )

    report_path = tmp_path / "generated_report.json"
    assert report_path.exists()
    assert result["passed"] is True
    assert result["generated_test_case"]["name"] == "Generated homepage test"

    saved_result = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert saved_result["passed"] is True
    assert saved_result["generated_test_case"]["url"] == "https://example.com"
