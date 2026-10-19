
from app.agent.test_case import TestCaseModel
from app.browser.browser_client import BrowserClient


class TestExecutorService:
    __test__ = False

    def run(self, test_case: TestCaseModel) -> dict:
        browser = BrowserClient().open()

        try:
            response = browser.navigate(test_case.url)

            if response is None:
                raise AssertionError("The page did not return an HTTP response")

            if response.status != 200:
                raise AssertionError(
                    f"Expected HTTP 200, got {response.status}"
                )

            results = []

            for step in test_case.steps:
                if step.action == "check_title":
                    actual = browser.get_title()
                    passed = actual == step.expected

                elif step.action == "check_text":
                    page_text = browser.get_body_text()
                    passed = step.expected in page_text
                    actual = step.expected if passed else (
                        f"Expected text not found: {step.expected}"
                    )

                else:
                    results.append({
                        "action": step.action,
                        "expected": step.expected,
                        "actual": None,
                        "passed": False,
                        "error": f"Unsupported action: {step.action}",
                    })
                    continue

                results.append({
                    "action": step.action,
                    "expected": step.expected,
                    "actual": actual,
                    "passed": passed,
                })

            return {
                "test_name": test_case.name,
                "url": test_case.url,
                "http_status": response.status,
                "steps": results,
                "passed": all(step["passed"] for step in results),
                "console_errors": browser.console_errors,
                "page_errors": browser.page_errors,
            }

        finally:
            browser.close()
