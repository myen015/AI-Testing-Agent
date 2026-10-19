
import json

from app.agent.llm_client import OllamaClient
from app.agent.test_case import TestCaseModel


class TestCaseGenerator:
    __test__ = False

    def __init__(self, llm_client: OllamaClient | None = None):
        self.llm_client = llm_client or OllamaClient()

    def generate(self, url: str, requirement: str) -> TestCaseModel:
        prompt = f"""
You are a professional QA engineer.

Create one test case for the following website and requirement.

Website URL: {url}
Requirement: {requirement}

Return ONLY a valid JSON object with this structure:
{{
    "name": "Short test case name",
    "url": "{url}",
    "steps": [
        {{
            "action": "check_title",
            "expected": "Example Domain"
        }}
    ]
}}

Rules:
- Use only these actions: check_title, check_text.
- For check_title, expected must contain the expected page title.
- For check_text, expected must contain text that should appear on the page.
- Do not use Markdown or code fences.
- Do not include explanations outside the JSON.
"""

        response = self.llm_client.generate(prompt)

        data = json.loads(response)
        test_case = TestCaseModel.model_validate(data)

        if test_case.url != url:
            raise ValueError("Generated test case URL does not match the requested URL.")

        return test_case
