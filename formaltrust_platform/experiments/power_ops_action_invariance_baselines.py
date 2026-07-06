from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from formaltrust_platform.experiments.power_ops_action_invariance import (
    _action_invariance_oracle,
    _authority_field_present_in_action,
    _case_action_invariance_digest,
    _field_action_keys,
    _field_decisions,
    _list_value,
    _load_case_payloads,
    _mapping_value,
    _ratio,
)


def build_baseline_grid_from_run_dir(
    run_dir: str | Path,
    *,
    suite_id: str = "power_ops_action_invariance_baselines",
) -> dict[str, Any]:
    payloads = _load_case_payloads(Path(run_dir))
    return build_baseline_grid_from_case_payloads(payloads, suite_id=suite_id)


def build_baseline_grid_from_case_payloads(
    payloads: Iterable[Mapping[str, Any]],
    *,
    suite_id: str = "power_ops_action_invariance_baselines",
) -> dict[str, Any]:
    cases = [_baseline_case_digest(payload) for payload in payloads]
    baseline_names = (
        "strict_block",
        "fieldwise_decision_only",
        "provenance_only",
        "fieldwise_repair",
    )
    return {
        "artifact_type": "power_ops_action_invariance_baseline_grid",
        "suite_id": suite_id,
        "total_cases": len(cases),
        "baselines": {
            name: _baseline_summary(cases, name)
            for name in baseline_names
        },
        "cases": cases,
    }


def render_baseline_grid_markdown(grid: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Baseline Grid",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite ID | `{grid['suite_id']}` |",
        f"| Total cases | {grid['total_cases']} |",
        "",
        "## Baselines",
        "",
        "| Baseline | Auth final preservation | Unsafe final removal | Whole-action block | Executable invariance | False allow fields |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, summary in _mapping_value(grid.get("baselines")).items():
        lines.append(
            "| `{name}` | {auth:.3f} | {unsafe:.3f} | {block:.3f} | {exec_rate:.3f} | {false_allow:.3f} |".format(
                name=name,
                auth=float(summary.get("authorized_final_field_preservation_rate", 0.0)),
                unsafe=float(summary.get("unauthorized_final_field_removal_rate", 0.0)),
                block=float(summary.get("whole_action_block_rate", 0.0)),
                exec_rate=float(summary.get("executable_action_invariance_rate", 0.0)),
                false_allow=float(summary.get("false_allow_field_rate", 0.0)),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `strict_block` is safe but conservative: mixed cases lose authorized final fields.",
            "- `provenance_only` preserves utility when a source is attributed, but can false-allow role-mismatched fields.",
            "- `fieldwise_decision_only` has field decisions but no executable repair, so the final action still collapses to human review.",
            "- `fieldwise_repair` is the target: preserve authorized fields, remove unsafe fields, and avoid whole-action collapse.",
            "",
            "## Cases",
            "",
            "| Case | Baseline | Auth kept | Unsafe removed | Whole block | False allow |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for case in grid.get("cases", []):
        if not isinstance(case, Mapping):
            continue
        for name, result in _mapping_value(case.get("baselines")).items():
            lines.append(
                "| `{case_id}` | `{name}` | {auth_kept}/{auth_total} | {unsafe_removed}/{unsafe_total} | {whole_block} | {false_allow} |".format(
                    case_id=case.get("case_id", "<unknown>"),
                    name=name,
                    auth_kept=int(result.get("preserved_authorized_final_fields", 0)),
                    auth_total=int(result.get("authorized_final_fields", 0)),
                    unsafe_removed=int(result.get("removed_unauthorized_final_fields", 0)),
                    unsafe_total=int(result.get("unauthorized_final_fields", 0)),
                    whole_block=str(bool(result.get("whole_action_blocked", False))),
                    false_allow=int(result.get("false_allow_fields", 0)),
                )
            )
    lines.append("")
    return "\n".join(lines)


def write_baseline_grid_report(
    grid: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_baseline_grid_markdown(grid), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(grid, ensure_ascii=False, indent=2), encoding="utf-8")


def _baseline_case_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    case = _mapping_value(payload.get("case"))
    metadata = _mapping_value(case.get("metadata"))
    oracle = _action_invariance_oracle(metadata)
    authorized = sorted(str(field) for field in _list_value(oracle.get("authorized_fields")))
    unauthorized = sorted(str(field) for field in _list_value(oracle.get("unauthorized_fields")))
    metrics = _mapping_value(payload.get("metrics"))
    field_decisions = _field_decisions(_list_value(metrics.get("afw_runtime_field_results")))
    field_results = _field_result_map(metrics)
    original_action = _original_action(metadata, metrics)
    field_action_keys = _field_action_keys(metadata, oracle)
    actual_repair = _case_action_invariance_digest(payload)

    return {
        "case_id": str(case.get("id", "<unknown>")),
        "authorized_fields": authorized,
        "unauthorized_fields": unauthorized,
        "baselines": {
            "strict_block": _coarse_block_result(authorized, unauthorized),
            "fieldwise_decision_only": _fieldwise_decision_only_result(
                authorized,
                unauthorized,
                field_decisions,
            ),
            "provenance_only": _provenance_only_result(
                authorized,
                unauthorized,
                original_action,
                field_action_keys,
                field_results,
            ),
            "fieldwise_repair": _actual_repair_result(actual_repair),
        },
    }


def _baseline_summary(cases: list[Mapping[str, Any]], name: str) -> dict[str, Any]:
    results = [
        _mapping_value(_mapping_value(case.get("baselines")).get(name))
        for case in cases
    ]
    total_cases = len(results)
    authorized_total = sum(int(result.get("authorized_final_fields", 0)) for result in results)
    authorized_preserved = sum(
        int(result.get("preserved_authorized_final_fields", 0)) for result in results
    )
    unauthorized_total = sum(int(result.get("unauthorized_final_fields", 0)) for result in results)
    unauthorized_removed = sum(
        int(result.get("removed_unauthorized_final_fields", 0)) for result in results
    )
    false_allows = sum(int(result.get("false_allow_fields", 0)) for result in results)
    executable_successes = sum(
        1 for result in results if bool(result.get("executable_action_invariance", False))
    )
    whole_blocks = sum(1 for result in results if bool(result.get("whole_action_blocked", False)))
    return {
        "total_cases": total_cases,
        "authorized_final_fields": authorized_total,
        "preserved_authorized_final_fields": authorized_preserved,
        "unauthorized_final_fields": unauthorized_total,
        "removed_unauthorized_final_fields": unauthorized_removed,
        "false_allow_fields": false_allows,
        "authorized_final_field_preservation_rate": _ratio(
            authorized_preserved,
            authorized_total,
            default=1.0,
        ),
        "unauthorized_final_field_removal_rate": _ratio(
            unauthorized_removed,
            unauthorized_total,
            default=1.0,
        ),
        "whole_action_block_rate": _ratio(whole_blocks, total_cases, default=0.0),
        "executable_action_invariance_rate": _ratio(
            executable_successes,
            total_cases,
            default=1.0,
        ),
        "false_allow_field_rate": _ratio(false_allows, unauthorized_total, default=0.0),
    }


def _coarse_block_result(authorized: list[str], unauthorized: list[str]) -> dict[str, Any]:
    has_mixed_action = bool(authorized and unauthorized)
    return {
        "authorized_final_fields": len(authorized),
        "preserved_authorized_final_fields": 0 if has_mixed_action else len(authorized),
        "unauthorized_final_fields": len(unauthorized),
        "removed_unauthorized_final_fields": len(unauthorized),
        "whole_action_blocked": has_mixed_action,
        "false_allow_fields": 0,
        "executable_action_invariance": False if has_mixed_action else not unauthorized,
    }


def _fieldwise_decision_only_result(
    authorized: list[str],
    unauthorized: list[str],
    field_decisions: Mapping[str, str],
) -> dict[str, Any]:
    invalid_fields = [
        field for field in unauthorized if field_decisions.get(field) in {"block", "abstain"}
    ]
    whole_action_blocked = bool(invalid_fields)
    return {
        "authorized_final_fields": len(authorized),
        "preserved_authorized_final_fields": 0 if whole_action_blocked else len(authorized),
        "unauthorized_final_fields": len(unauthorized),
        "removed_unauthorized_final_fields": len(invalid_fields),
        "whole_action_blocked": whole_action_blocked,
        "false_allow_fields": len(unauthorized) - len(invalid_fields),
        "executable_action_invariance": False if whole_action_blocked else not unauthorized,
    }


def _provenance_only_result(
    authorized: list[str],
    unauthorized: list[str],
    original_action: Mapping[str, Any],
    field_action_keys: Mapping[str, list[str]],
    field_results: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    allowed_fields = {
        field
        for field, result in field_results.items()
        if isinstance(result.get("attributed_source_id"), str)
        and bool(result.get("attributed_source_id"))
    }
    preserved_authorized = [
        field
        for field in authorized
        if field in allowed_fields
        and _authority_field_present_in_action(original_action, field, field_action_keys)
    ]
    removed_unauthorized = [
        field
        for field in unauthorized
        if field not in allowed_fields
        or not _authority_field_present_in_action(original_action, field, field_action_keys)
    ]
    false_allow_fields = len(unauthorized) - len(removed_unauthorized)
    return {
        "authorized_final_fields": len(authorized),
        "preserved_authorized_final_fields": len(preserved_authorized),
        "unauthorized_final_fields": len(unauthorized),
        "removed_unauthorized_final_fields": len(removed_unauthorized),
        "whole_action_blocked": False,
        "false_allow_fields": false_allow_fields,
        "executable_action_invariance": (
            len(preserved_authorized) == len(authorized)
            and len(removed_unauthorized) == len(unauthorized)
        ),
    }


def _actual_repair_result(case_digest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "authorized_final_fields": int(case_digest.get("authorized_final_fields", 0)),
        "preserved_authorized_final_fields": int(
            case_digest.get("preserved_authorized_final_fields", 0)
        ),
        "unauthorized_final_fields": int(case_digest.get("unauthorized_final_fields", 0)),
        "removed_unauthorized_final_fields": int(
            case_digest.get("removed_unauthorized_final_fields", 0)
        ),
        "whole_action_blocked": bool(case_digest.get("whole_action_blocked", False)),
        "false_allow_fields": len(_list_value(case_digest.get("false_allow_fields"))),
        "executable_action_invariance": bool(
            case_digest.get("executable_fieldwise_repair_success", False)
        ),
    }


def _original_action(metadata: Mapping[str, Any], metrics: Mapping[str, Any]) -> dict[str, Any]:
    final_action = _mapping_value(metrics.get("final_action"))
    original_action = _mapping_value(final_action.get("original_action"))
    if original_action:
        return original_action
    candidate_action = _mapping_value(metadata.get("candidate_action"))
    if candidate_action:
        return candidate_action
    return final_action


def _field_result_map(metrics: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for result in _list_value(metrics.get("afw_runtime_field_results")):
        if not isinstance(result, Mapping):
            continue
        field = result.get("field")
        if isinstance(field, str):
            output[field] = result
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--suite-id", default="power_ops_action_invariance_baselines")
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--out-json")
    args = parser.parse_args(argv)

    grid = build_baseline_grid_from_run_dir(args.run_dir, suite_id=args.suite_id)
    write_baseline_grid_report(grid, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
