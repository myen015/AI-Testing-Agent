
from app.agent.report_writer import ReportWriter
from app.agent.test_case import TestCaseModel
from app.agent.test_case_generator import TestCaseGenerator
from app.agent.test_executor import TestExecutorService


class AgentRunner:
    def __init__(self):
        self.executor = TestExecutorService()
        self.report_writer = ReportWriter()
        self.generator = TestCaseGenerator()

    def run(self, test_case: TestCaseModel) -> dict:
        result = self.executor.run(test_case)
        self.report_writer.save(result)
        return result

    def generate_and_run(
        self,
        url: str,
        requirement: str,
    ) -> dict:
        test_case = self.generator.generate(
            url=url,
            requirement=requirement,
        )

        result = self.executor.run(test_case)
        result["generated_test_case"] = test_case.model_dump()

        self.report_writer.save(result)
        return result
