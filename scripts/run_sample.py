"""Run the 4-agent harness on sample questions and print a report."""
import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ee_agent.pipeline.config import PipelineConfig
from ee_agent.pipeline.runner import run_from_json, run_from_pdf

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def _print_summary(summary: dict, results_path: str) -> None:
    print("\n" + "=" * 60)
    print("EE-Agent Pipeline Results")
    print("=" * 60)
    print(f"Total questions : {summary['total']}")
    print(f"Correct         : {summary['correct']}")
    print(f"Accuracy        : {summary['accuracy']:.1%}")
    print(f"Output file     : {results_path}")
    print("=" * 60)

    # Print per-question breakdown
    if Path(results_path).exists():
        with open(results_path, encoding="utf-8") as f:
            results = json.load(f)
        print("\nPer-question breakdown:")
        for r in results:
            if "error" in r:
                print(f"  Q#{r.get('question_id', '?')}: ERROR — {r['error']}")
            else:
                mark = "✓" if r["is_correct"] else "✗"
                print(
                    f"  Q#{r['question_number']:02d} [{r['subject'][:8]}] "
                    f"predicted={r['predicted_choice']} correct={r['correct_choice']} "
                    f"{mark} (conf={r['final_confidence']:.2f})"
                )


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run EE-Agent on sample questions")
    parser.add_argument("--json", help="Path to sample_questions.json", default=None)
    parser.add_argument("--pdf", help="Path to exam PDF file", default=None)
    parser.add_argument("--year", type=int, default=2023, help="Exam year (for PDF mode)")
    parser.add_argument("--output", default=None, help="Output JSON path (default: output/results_{year}_{timestamp}.json)")
    parser.add_argument(
        "--solver", default="auto",
        choices=["auto", "pro", "api", "ollama"],
        help="LLM backend: pro(Claude Pro 구독), api(Anthropic API), ollama(로컬), auto(자동선택)"
    )
    args = parser.parse_args()

    config = PipelineConfig()

    # Generate default output path: output/results_{year}_{timestamp}.json
    if args.output:
        output = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"output/results_{args.year}_{timestamp}.json"
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    if args.json:
        summary = await run_from_json(args.json, output, config, solver_backend=args.solver)
    elif args.pdf:
        summary = await run_from_pdf(args.pdf, args.year, output, config, solver_backend=args.solver)
    else:
        # Default: use bundled sample fixtures
        default_json = Path(__file__).parent.parent / "tests/fixtures/sample_questions.json"
        if not default_json.exists():
            print("Error: No input specified. Use --json or --pdf, or ensure fixtures exist.")
            sys.exit(1)
        print(f"Using default fixture: {default_json}")
        summary = await run_from_json(str(default_json), output, config)

    _print_summary(summary, output)


if __name__ == "__main__":
    asyncio.run(main())
