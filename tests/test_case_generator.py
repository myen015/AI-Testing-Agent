import json
import pytest
from app.agent.test_case_generator import TestCaseGenerator


class FakeLLMClient:
    def generate(self, prompt: str) -> str:
        return json.dumps({
            "name": "Check homepage title",
            "url": "https://example.com",
            "steps": [
                {
                    "action": "check_title",
                    "expected": "Example Domain"
                }
            ]
        })


def test_generates_valid_test_case():
    generator = TestCaseGenerator(llm_client=FakeLLMClient())

    result = generator.generate(
        url="https://example.com",
        requirement='The page title should be "Example Domain".',
    )

    assert result.name == "Check homepage title"
    assert result.url == "https://example.com"
    assert result.steps[0].action == "check_title"
    assert result.steps[0].expected == "Example Domain"


@pytest.mark.integration
def test_generates_test_case_with_real_llm():
    generator = TestCaseGenerator()

    result = generator.generate(
        url="https://example.com",
        requirement='The homepage title must be "Example Domain".',
    )

    assert result.url == "https://example.com"
    assert len(result.steps) > 0
    assert any(
        step.action == "check_title"
        for step in result.steps
    )

class InvalidJSONLLMClient:
    def generate(self, prompt: str) -> str:
        return "This is not valid JSON"


def test_rejects_invalid_llm_response():
    generator = TestCaseGenerator(llm_client=InvalidJSONLLMClient())

    with pytest.raises(ValueError):
        generator.generate(
            url="https://example.com",
            requirement="Check the homepage title.",
        )
