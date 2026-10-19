
import argparse
import json

from app.agent.runner import AgentRunner


def main():
    parser = argparse.ArgumentParser(
        description="AI Testing Agent — generate and execute browser tests."
    )

    parser.add_argument(
        "--url",
        required=True,
        help="URL of the website to test",
    )

    parser.add_argument(
        "--requirement",
        required=True,
        help="What the agent should verify",
    )

    args = parser.parse_args()

    runner = AgentRunner()
    result = runner.generate_and_run(
        url=args.url,
        requirement=args.requirement,
    )

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
