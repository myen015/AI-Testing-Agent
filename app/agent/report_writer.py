
import json
from pathlib import Path


class ReportWriter:
    def save(self, result: dict, path: str = "artifacts/reports/latest.json"):
        report_path = Path(path)
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with report_path.open("w", encoding="utf-8") as file:
            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return report_path
