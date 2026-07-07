from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks.continuous_bench.continuous_bench import (  # noqa: E402
    DEFAULT_OLLAMA_URL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SEED_PATH,
    run_continuous_bench,
)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = run_continuous_bench(
        batch_size=args.batch_size,
        iterations=args.iterations,
        model=args.model,
        output_dir=args.output_dir,
        seed_path=args.seed_path,
        ollama_url=args.ollama_url,
        temperature=args.temperature,
        num_ctx=args.num_ctx,
        num_predict=args.num_predict,
        timeout_seconds=args.timeout_seconds,
    )
    print_report(result)
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append-only continuous benchmark generation, Ollama evaluation, and screening."
    )
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--model", default="qwen2.5:7b")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--seed-path", type=Path, default=DEFAULT_SEED_PATH)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--num-predict", type=int, default=256)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    return parser.parse_args(argv)


def print_report(result: dict) -> None:
    print(f"generated={result['generated']}")
    print(f"evaluated={result['evaluated']}")
    print(f"bench={result['bench']}")
    print(f"accepted={result['accepted']}")
    print(f"rejected={result['rejected']}")
    print(f"model_error_rate={result['model_error_rate']:.4f}")
    print(f"model_pass_rate={result['model_pass_rate']:.4f}")
    print(
        "failure_mode_distribution="
        + json.dumps(result["failure_mode_distribution"], ensure_ascii=False, sort_keys=True)
    )
    print("output_files=" + json.dumps(result["output_paths"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
