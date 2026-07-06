from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def build_runtime_overhead_audit(
    *,
    action_summary_paths: Sequence[str | Path],
    paired_summary_paths: Sequence[str | Path] = (),
) -> dict[str, Any]:
    action_profiles = [_action_suite_profile(Path(path)) for path in action_summary_paths]
    paired_profiles = [_paired_authority_profile(Path(path)) for path in paired_summary_paths]
    profiles = action_profiles + paired_profiles

    total_field_checks = sum(int(profile["field_check_proxy_units"]) for profile in profiles)
    weighted_compression_sum = sum(
        int(profile["field_check_proxy_units"]) * float(profile["audit_compression_ratio"])
        for profile in profiles
    )
    max_checks_per_case = max(
        [int(profile["max_field_check_proxy_units_per_case"]) for profile in profiles] or [0]
    )

    return {
        "artifact_type": "power_ops_runtime_overhead_audit",
        "suite_count": len(profiles),
        "action_suite_count": len(action_profiles),
        "paired_authority_suite_count": len(paired_profiles),
        "total_field_check_proxy_units": total_field_checks,
        "action_suite_field_check_proxy_units": sum(
            int(profile["field_check_proxy_units"]) for profile in action_profiles
        ),
        "paired_suite_field_check_proxy_units": sum(
            int(profile["field_check_proxy_units"]) for profile in paired_profiles
        ),
        "max_field_check_proxy_units_per_case": max_checks_per_case,
        "weighted_mean_audit_compression_ratio": _round_ratio(
            weighted_compression_sum,
            total_field_checks,
        ),
        "wall_clock_latency_available": False,
        "reporting_status": "proxy_only_no_wall_clock",
        "interpretation": {
            "field_check_proxy_units": "number of field-level authority decisions; not wall-clock latency",
            "audit_compression_ratio": "fraction of full authority context omitted by the minimal witness",
            "status": "proxy-only overhead evidence until instrumented wall-clock timings are collected",
        },
        "action_suite_profiles": action_profiles,
        "paired_authority_profiles": paired_profiles,
    }


def render_runtime_overhead_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Runtime Overhead Audit",
        "",
        "This is a proxy-only overhead audit. It reports field-check units and audit-compression ratios, not wall-clock latency.",
        "",
        "## Aggregate",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| suite_count | {int(audit.get('suite_count', 0) or 0)} |",
        f"| action_suite_count | {int(audit.get('action_suite_count', 0) or 0)} |",
        f"| paired_authority_suite_count | {int(audit.get('paired_authority_suite_count', 0) or 0)} |",
        f"| total_field_check_proxy_units | {int(audit.get('total_field_check_proxy_units', 0) or 0)} |",
        f"| max_field_check_proxy_units_per_case | {int(audit.get('max_field_check_proxy_units_per_case', 0) or 0)} |",
        f"| weighted_mean_audit_compression_ratio | {float(audit.get('weighted_mean_audit_compression_ratio', 0.0) or 0.0):.6f} |",
        f"| wall_clock_latency_available | {str(bool(audit.get('wall_clock_latency_available', False))).lower()} |",
        "",
        "## Action Suites",
        "",
        "| Suite | Cases | Field checks | Max checks/case | Audit compression |",
        "|---|---:|---:|---:|---:|",
    ]
    for profile in _list_value(audit.get("action_suite_profiles")):
        if not isinstance(profile, Mapping):
            continue
        lines.append(
            "| `{suite}` | {cases} | {checks} | {max_checks} | {compression:.6f} |".format(
                suite=profile.get("suite_id", ""),
                cases=int(profile.get("case_count", 0) or 0),
                checks=int(profile.get("field_check_proxy_units", 0) or 0),
                max_checks=int(profile.get("max_field_check_proxy_units_per_case", 0) or 0),
                compression=float(profile.get("audit_compression_ratio", 0.0) or 0.0),
            )
        )

    lines.extend(
        [
            "",
            "## Paired Authority Suites",
            "",
            "| Suite | Rows | Field checks | Audit compression |",
            "|---|---:|---:|---:|",
        ]
    )
    for profile in _list_value(audit.get("paired_authority_profiles")):
        if not isinstance(profile, Mapping):
            continue
        lines.append(
            "| `{suite}` | {rows} | {checks} | {compression:.6f} |".format(
                suite=profile.get("suite_id", ""),
                rows=int(profile.get("paired_row_count", 0) or 0),
                checks=int(profile.get("field_check_proxy_units", 0) or 0),
                compression=float(profile.get("audit_compression_ratio", 0.0) or 0.0),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_runtime_overhead_audit(
    audit: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_runtime_overhead_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _action_suite_profile(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    action_summary = _mapping_value(payload.get("action_invariance_summary")) or payload
    field_counts = _mapping_value(action_summary.get("field_counts")) or _mapping_value(
        payload.get("field_counts")
    )
    runtime_summary = _mapping_value(payload.get("runtime_summary"))
    runtime_field_counts = _mapping_value(runtime_summary.get("field_counts"))

    field_checks = int(
        runtime_field_counts.get(
            "total_runtime_fields",
            int(field_counts.get("authorized_fields", 0) or 0)
            + int(field_counts.get("unauthorized_fields", 0) or 0),
        )
        or 0
    )
    case_count = int(action_summary.get("total_cases", payload.get("total_cases", 0)) or 0)
    case_checks = [
        int(case.get("total_runtime_fields", 0) or 0)
        for case in _list_value(action_summary.get("cases"))
        if isinstance(case, Mapping)
    ]
    if not case_checks and case_count:
        case_checks = [int(round(field_checks / case_count))]

    compression = _action_audit_compression(payload, action_summary)
    return {
        "suite_id": str(payload.get("suite_id", action_summary.get("suite_id", path.stem))),
        "artifact_path": str(path),
        "case_count": case_count,
        "field_check_proxy_units": field_checks,
        "max_field_check_proxy_units_per_case": max(case_checks or [0]),
        "audit_compression_ratio": compression,
        "wall_clock_latency_available": False,
    }


def _paired_authority_profile(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    capguard = _mapping_value(payload.get("capguard_summary"))
    row_results = [
        row for row in _list_value(capguard.get("row_results")) if isinstance(row, Mapping)
    ]
    paired_rows = int(capguard.get("total_rows", payload.get("generated_row_count", 0)) or 0)
    field_checks = paired_rows * 2
    compression_values: list[float] = []
    for row in row_results:
        for key in ("legal_witness_audit", "laundered_witness_audit"):
            audit = _mapping_value(row.get(key))
            if "compression_ratio" in audit:
                compression_values.append(float(audit.get("compression_ratio", 0.0) or 0.0))
    compression = (
        round(sum(compression_values) / len(compression_values), 6)
        if compression_values
        else float(capguard.get("legal_witness_compression_rate", 0.0) or 0.0)
    )
    return {
        "suite_id": str(payload.get("suite_id", path.stem)),
        "artifact_path": str(path),
        "paired_row_count": paired_rows,
        "field_check_proxy_units": field_checks,
        "max_field_check_proxy_units_per_case": 2 if paired_rows else 0,
        "audit_compression_ratio": compression,
        "wall_clock_latency_available": False,
    }


def _action_audit_compression(
    payload: Mapping[str, Any], action_summary: Mapping[str, Any]
) -> float:
    runtime_summary = _mapping_value(payload.get("runtime_summary"))
    witness_compression = _mapping_value(runtime_summary.get("witness_audit_compression"))
    if "mean_compression_ratio" in witness_compression:
        return float(witness_compression.get("mean_compression_ratio", 0.0) or 0.0)
    return float(action_summary.get("mean_witness_compression_ratio", 0.0) or 0.0)


def _round_ratio(numerator: float, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return payload


def _mapping_value(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate proxy-only runtime overhead and audit-compression metrics."
    )
    parser.add_argument("--action-summary", action="append", dest="action_summary_paths", required=True)
    parser.add_argument("--paired-summary", action="append", dest="paired_summary_paths", default=[])
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    audit = build_runtime_overhead_audit(
        action_summary_paths=args.action_summary_paths,
        paired_summary_paths=args.paired_summary_paths,
    )
    if args.out_md or args.out_json:
        write_runtime_overhead_audit(
            audit,
            markdown_path=args.out_md or "docs/power_ops_runtime_overhead_audit_2026-07-02.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(audit, ensure_ascii=False, indent=2))
    else:
        print(render_runtime_overhead_audit_markdown(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
