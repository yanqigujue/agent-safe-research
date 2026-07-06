from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from formaltrust_platform.experiments.afw_runtime_report import build_afw_runtime_run_summary
from formaltrust_platform.experiments.power_ops_action_invariance import (
    build_action_invariance_summary_from_case_payloads,
)


def build_normal_behavior_stress_summary_from_run_dir(
    run_dir: str | Path,
    *,
    suite_id: str = "power_ops_normal_behavior_stress",
) -> dict[str, Any]:
    root = Path(run_dir)
    payloads = _load_case_payloads(root)
    action_summary = build_action_invariance_summary_from_case_payloads(
        payloads,
        suite_id=f"{suite_id}_action_invariance",
    )
    runtime_summary = build_afw_runtime_run_summary(root)
    action_cases = _list_value(action_summary.get("cases"))
    field_counts = _mapping_value(action_summary.get("field_counts"))
    human_review_counts = _mapping_value(action_summary.get("human_review_field_counts"))
    mutation_cases = [_case_final_action_mutation(payload) for payload in payloads]
    mutation_case_count = sum(1 for case in mutation_cases if case["mutated"])
    authorized_fields = int(field_counts.get("authorized_fields", 0) or 0)
    false_block_fields = int(field_counts.get("false_block_fields", 0) or 0)

    return {
        "artifact_type": "power_ops_normal_behavior_stress_summary",
        "suite_id": suite_id,
        "run_dir": str(root),
        "run_id": root.name,
        "total_cases": len(payloads),
        "passed_cases": int(runtime_summary.get("passed_cases", 0) or 0),
        "failed_cases": int(runtime_summary.get("failed_cases", 0) or 0),
        "fully_authorized_case_count": sum(
            1
            for case in action_cases
            if int(_mapping_value(case).get("authorized_fields", 0) or 0) > 0
            and int(_mapping_value(case).get("unauthorized_fields", 0) or 0) == 0
        ),
        "authorized_field_count": authorized_fields,
        "preserved_authorized_field_count": int(
            field_counts.get("preserved_authorized_fields", 0) or 0
        ),
        "false_block_field_count": false_block_fields,
        "false_intervention_field_rate": _ratio_float(
            false_block_fields,
            authorized_fields,
            default=0.0,
        ),
        "whole_action_intervention_rate": float(
            action_summary.get("whole_action_block_rate", 0.0) or 0.0
        ),
        "authorized_final_field_preservation_rate": float(
            action_summary.get("authorized_final_field_preservation_rate", 0.0) or 0.0
        ),
        "final_action_mutation_cases": mutation_case_count,
        "final_action_mutation_rate": _ratio_float(mutation_case_count, len(payloads), default=0.0),
        "mean_repair_overhead_fields": _ratio_float(
            int(human_review_counts.get("partial_human_review_fields", 0) or 0),
            len(payloads),
            default=0.0,
        ),
        "gate_decision_counts": _mapping_value(action_summary.get("gate_decision_counts")),
        "runtime_summary": runtime_summary,
        "action_invariance_summary": action_summary,
        "cases": mutation_cases,
    }


def render_normal_behavior_stress_markdown(summary: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Normal-Behavior Stress Summary",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{summary.get('suite_id', '')}` |",
        f"| Run ID | `{summary.get('run_id', '')}` |",
        f"| Total cases | {int(summary.get('total_cases', 0) or 0)} |",
        f"| Passed cases | {int(summary.get('passed_cases', 0) or 0)} |",
        f"| Failed cases | {int(summary.get('failed_cases', 0) or 0)} |",
        f"| Fully authorized cases | {int(summary.get('fully_authorized_case_count', 0) or 0)} |",
        "",
        "## Normal-Behavior Preservation",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| authorized_field_count | {int(summary.get('authorized_field_count', 0) or 0)} |",
        f"| preserved_authorized_field_count | {int(summary.get('preserved_authorized_field_count', 0) or 0)} |",
        f"| false_block_field_count | {int(summary.get('false_block_field_count', 0) or 0)} |",
        f"| false_intervention_field_rate | {float(summary.get('false_intervention_field_rate', 0.0) or 0.0):.3f} |",
        f"| whole_action_intervention_rate | {float(summary.get('whole_action_intervention_rate', 0.0) or 0.0):.3f} |",
        f"| authorized_final_field_preservation_rate | {float(summary.get('authorized_final_field_preservation_rate', 0.0) or 0.0):.3f} |",
        f"| final_action_mutation_cases | {int(summary.get('final_action_mutation_cases', 0) or 0)} |",
        f"| final_action_mutation_rate | {float(summary.get('final_action_mutation_rate', 0.0) or 0.0):.3f} |",
        f"| mean_repair_overhead_fields | {float(summary.get('mean_repair_overhead_fields', 0.0) or 0.0):.3f} |",
        "",
        "## Gate Decisions",
        "",
        "| Decision | Cases |",
        "|---|---:|",
    ]
    for decision, count in _mapping_value(summary.get("gate_decision_counts")).items():
        lines.append(f"| {decision} | {int(count)} |")

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Gate | Candidate | Final | Mutated |",
            "|---|---|---|---|---:|",
        ]
    )
    for case in _list_value(summary.get("cases")):
        if not isinstance(case, Mapping):
            continue
        lines.append(
            "| `{case_id}` | `{gate}` | `{candidate}` | `{final}` | {mutated} |".format(
                case_id=case.get("case_id", "<unknown>"),
                gate=case.get("gate_decision", "missing"),
                candidate=case.get("candidate_decision", "missing"),
                final=case.get("final_decision", "missing"),
                mutated=str(bool(case.get("mutated", False))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_normal_behavior_stress_report(
    summary: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_normal_behavior_stress_markdown(summary), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def _case_final_action_mutation(payload: Mapping[str, Any]) -> dict[str, Any]:
    case = _mapping_value(payload.get("case"))
    metrics = _mapping_value(payload.get("metrics"))
    candidate = _mapping_value(metrics.get("candidate_action"))
    final = _mapping_value(metrics.get("final_action"))
    return {
        "case_id": str(case.get("id", "<unknown>")),
        "gate_decision": str(metrics.get("afw_gate_decision", "missing")),
        "candidate_decision": str(candidate.get("decision", "missing")),
        "final_decision": str(final.get("decision", "missing")),
        "mutated": candidate != final,
    }


def _load_case_payloads(run_dir: Path) -> list[dict[str, Any]]:
    case_dir = run_dir / "cases"
    if not case_dir.is_dir():
        raise ValueError(f"FormalTrust run directory has no cases directory: {run_dir}")
    payloads: list[dict[str, Any]] = []
    for path in sorted(case_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            payloads.append(json.load(handle))
    return payloads


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _ratio_float(numerator: int, denominator: int, *, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize strict-supervision normal-behavior preservation for power-ops traces."
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suite-id", default="power_ops_normal_behavior_stress")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    summary = build_normal_behavior_stress_summary_from_run_dir(
        args.run_dir,
        suite_id=args.suite_id,
    )
    if args.out_md or args.out_json:
        write_normal_behavior_stress_report(
            summary,
            markdown_path=args.out_md or Path(args.run_dir) / "normal_behavior_stress.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_normal_behavior_stress_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
