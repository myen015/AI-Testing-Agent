
from pydantic import BaseModel, Field


class TestStepModel(BaseModel):
    __test__ = False

    action: str
    expected: str


class TestCaseModel(BaseModel):
    __test__ = False

    name: str
    url: str
    steps: list[TestStepModel] = Field(default_factory=list)
