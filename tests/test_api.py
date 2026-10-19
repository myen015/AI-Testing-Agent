
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "AI Testing Agent",
    }


def test_run_returns_agent_result():
    expected_result = {
        "test_name": "Homepage title",
        "url": "https://example.com",
        "http_status": 200,
        "steps": [],
        "passed": True,
        "console_errors": [],
        "page_errors": [],
    }

    with patch("app.api.AgentRunner") as runner_class:
        runner_class.return_value.generate_and_run.return_value = (
            expected_result
        )

        response = client.post(
            "/run",
            json={
                "url": "https://example.com",
                "requirement": "Check the homepage title",
            },
        )

    assert response.status_code == 200
    assert response.json() == expected_result
    runner_class.return_value.generate_and_run.assert_called_once_with(
        url="https://example.com/",
        requirement="Check the homepage title",
    )


def test_run_rejects_invalid_url():
    response = client.post(
        "/run",
        json={
            "url": "not-a-url",
            "requirement": "Check the homepage title",
        },
    )

    assert response.status_code == 422


def test_run_rejects_short_requirement():
    response = client.post(
        "/run",
        json={
            "url": "https://example.com",
            "requirement": "abc",
        },
    )

    assert response.status_code == 422
