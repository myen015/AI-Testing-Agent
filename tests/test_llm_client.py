
from app.agent.llm_client import OllamaClient


def test_ollama_generates_response():
    client = OllamaClient()

    result = client.generate(
        "Reply with exactly one word: SUCCESS"
    )

    assert isinstance(result, str)
    assert "SUCCESS" in result.upper()
