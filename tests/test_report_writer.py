
import json

from app.agent.report_writer import ReportWriter


def test_report_is_saved_as_json(tmp_path):
    result = {
        "test_name": "Check example page",
        "http_status": 200,
        "passed": True,
        "steps": [
            {
                "action": "check_title",
                "expected": "Example Domain",
                "actual": "Example Domain",
                "passed": True,
            }
        ],
    }

    report_path = tmp_path / "reports" / "latest.json"

    saved_path = ReportWriter().save(result, str(report_path))

    assert saved_path.exists()

    with saved_path.open("r", encoding="utf-8") as file:
        loaded_result = json.load(file)

    assert loaded_result == result


def test_report_preserves_non_english_text(tmp_path):
    result = {
        "test_name": "Проверка страницы",
        "passed": False,
    }

    report_path = tmp_path / "report.json"

    ReportWriter().save(result, str(report_path))

    content = report_path.read_text(encoding="utf-8")

    assert "Проверка страницы" in content
    assert "\\u" not in content
