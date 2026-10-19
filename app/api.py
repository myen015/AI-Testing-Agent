
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import AnyHttpUrl, BaseModel, Field

from app.agent.runner import AgentRunner

app = FastAPI(
    title="AI Testing Agent",
    description="Generate and execute browser tests using a local LLM.",
    version="0.1.0",
)


class TestRequest(BaseModel):
    url: AnyHttpUrl
    requirement: str = Field(min_length=5, max_length=2000)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "AI Testing Agent"}


@app.post("/run")
def run_test(request: TestRequest) -> dict[str, Any]:
    runner = AgentRunner()

    try:
        return runner.generate_and_run(
            url=str(request.url),
            requirement=request.requirement,
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail=(
                "The test could not be completed. "
                "Check the Ollama service, generated test case, "
                "browser connectivity, and server logs."
            ),
        ) from None
