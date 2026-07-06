from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def build_performance_profile(
    *,
    summary_paths: Sequence[str | Path],
    baseline_grid_path: str | Path,
) -> dict[str, Any]:
    suite_profiles: dict[str, dict[str, Any]] = {}
    for path in summary_paths:
        payload = _load_json(Path(path))
        profile = _suite_profile(payload, artifact_path=Path(path))
        suite_profiles[profile["suite_id"]] = profile

    baseline_payload = _load_json(Path(baseline_grid_path))
    baseline_profiles = {
        name: _baseline_profile(name, metrics, artifact_path=Path(baseline_grid_path))
        for name, metrics in _mapping_value(baseline_payload.get("baselines")).items()
    }

    best_baseline = _best_baseline_for_normal_behavior(baseline_profiles)
    return {
        "artifact_type": "power_ops_action_invariance_performance_profile",
        "suite_count": len(suite_profiles),
        "baseline_count": len(baseline_profiles),
        "suite_profiles": suite_profiles,
        "baseline_profiles": baseline_profiles,
        "best_baseline_for_normal_behavior": best_baseline,
        "interpretation": {
            "normal_behavior_preservation": "authorized final-field preservation",
            "safety_removal": "unauthorized final-field removal",
            "latency_proxy_units": "runtime field checks; not wall-clock latency",
            "audit_compression": "mean witness compression ratio",
        },
    }


def render_performance_profile_markdown(profile: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Action Invariance Performance Profile",
        "",
        "## Inputs",
        "",
        "| Item | Value |",
        "|---|---:|",
        f"| Suite profiles | {profile['suite_count']} |",
        f"| Baseline profiles | {profile['baseline_count']} |",
        "",
        "## Suite Profiles",
        "",
        "| Suite | Cases | Normal preservation | Safety removal | Whole-action block | Review fields/case | Latency proxy | Audit compression |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for suite_id, suite in _mapping_value(profile.get("suite_profiles")).items():
        lines.append(
            "| `{suite}` | {cases} | {normal:.3f} | {safety:.3f} | {block:.3f} | {review:.3f} | {latency} | {audit:.3f} |".format(
                suite=suite_id,
                cases=int(suite["total_cases"]),
                normal=float(suite["normal_behavior_preservation"]),
                safety=float(suite["safety_removal"]),
                block=float(suite["whole_action_block_rate"]),
                review=float(suite["review_burden_fields_per_case"]),
                latency=int(suite["latency_proxy_units"]),
                audit=float(suite["audit_compression"]),
            )
        )

    lines.extend(
        [
            "",
            "## Baseline Profiles",
            "",
            "| Baseline | Cases | Normal preservation | Safety removal | Whole-action block | False allow | Latency proxy |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for name, baseline in _mapping_value(profile.get("baseline_profiles")).items():
        lines.append(
            "| `{name}` | {cases} | {normal:.3f} | {safety:.3f} | {block:.3f} | {false_allow:.3f} | {latency} |".format(
                name=name,
                cases=int(baseline["total_cases"]),
                normal=float(baseline["normal_behavior_preservation"]),
                safety=float(baseline["safety_removal"]),
                block=float(baseline["whole_action_block_rate"]),
                false_allow=float(baseline["false_allow_rate"]),
                latency=int(baseline["latency_proxy_units"]),
            )
        )

    best = _mapping_value(profile.get("best_baseline_for_normal_behavior"))
    if best:
        lines.extend(
            [
                "",
                "## Best Current Baseline",
                "",
                f"- `{best['name']}` is the best current baseline under the safety-preserving normal-behavior score.",
                "- This does not claim production superiority; it only summarizes the current curated baseline grid.",
            ]
        )
    return "\n".join(lines) + "\n"


def write_performance_profile(
    profile: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    md_path = Path(markdown_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_performance_profile_markdown(profile), encoding="utf-8")
    if json_path is not None:
        json_out = Path(json_path)
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


def _suite_profile(payload: Mapping[str, Any], *, artifact_path: Path) -> dict[str, Any]:
    action_summary = _mapping_value(payload.get("action_invariance_summary")) or dict(payload)
    field_counts = _mapping_value(action_summary.get("field_counts"))
    latency_proxy_units = int(
        field_counts.get("authorized_fields", 0)
        + field_counts.get("unauthorized_fields", 0)
    )
    return {
        "suite_id": str(action_summary.get("suite_id", payload.get("suite_id", artifact_path.stem))),
        "artifact_path": str(artifact_path),
        "total_cases": int(action_summary.get("total_cases", 0)),
        "normal_behavior_preservation": float(
            action_summary.get("authorized_final_field_preservation_rate", 0.0)
        ),
        "safety_removal": float(
            action_summary.get("unauthorized_final_field_removal_rate", 0.0)
        ),
        "whole_action_block_rate": float(action_summary.get("whole_action_block_rate", 0.0)),
        "review_burden_fields_per_case": float(
            action_summary.get("mean_partial_human_review_fields", 0.0)
        ),
        "auto_executable_field_ratio": float(
            action_summary.get("auto_executable_field_ratio", 0.0)
        ),
        "audit_compression": float(action_summary.get("mean_witness_compression_ratio", 0.0)),
        "latency_proxy_units": latency_proxy_units,
    }


def _baseline_profile(
    name: str,
    metrics: Mapping[str, Any],
    *,
    artifact_path: Path,
) -> dict[str, Any]:
    latency_proxy_units = int(
        metrics.get("authorized_final_fields", 0)
        + metrics.get("unauthorized_final_fields", 0)
    )
    return {
        "name": name,
        "artifact_path": str(artifact_path),
        "total_cases": int(metrics.get("total_cases", 0)),
        "normal_behavior_preservation": float(
            metrics.get("authorized_final_field_preservation_rate", 0.0)
        ),
        "safety_removal": float(metrics.get("unauthorized_final_field_removal_rate", 0.0)),
        "whole_action_block_rate": float(metrics.get("whole_action_block_rate", 0.0)),
        "executable_action_invariance_rate": float(
            metrics.get("executable_action_invariance_rate", 0.0)
        ),
        "false_allow_rate": float(metrics.get("false_allow_field_rate", 0.0)),
        "latency_proxy_units": latency_proxy_units,
        "safety_preserving_normal_score": float(
            metrics.get("authorized_final_field_preservation_rate", 0.0)
        )
        * float(metrics.get("unauthorized_final_field_removal_rate", 0.0))
        * (1.0 - float(metrics.get("false_allow_field_rate", 0.0))),
    }


def _best_baseline_for_normal_behavior(
    baseline_profiles: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    if not baseline_profiles:
        return {}
    name, profile = max(
        baseline_profiles.items(),
        key=lambda item: (
            float(item[1].get("safety_preserving_normal_score", 0.0)),
            float(item[1].get("normal_behavior_preservation", 0.0)),
            -float(item[1].get("whole_action_block_rate", 0.0)),
            item[0],
        ),
    )
    return {"name": name, **dict(profile)}


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a safety-vs-normal-behavior profile for power-ops action invariance."
    )
    parser.add_argument("--summary-path", action="append", dest="summary_paths", required=True)
    parser.add_argument("--baseline-grid-path", required=True)
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    profile = build_performance_profile(
        summary_paths=args.summary_paths,
        baseline_grid_path=args.baseline_grid_path,
    )
    if args.out_md or args.out_json:
        write_performance_profile(
            profile,
            markdown_path=args.out_md or "power_ops_action_invariance_performance.md",
            json_path=args.out_json,
        )
        return 0

    if args.format == "json":
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(render_performance_profile_markdown(profile))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
