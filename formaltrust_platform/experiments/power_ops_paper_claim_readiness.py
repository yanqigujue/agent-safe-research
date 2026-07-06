from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_WRITING_ARTIFACT_PATHS = (
    "docs/power_ops_action_invariance_draft_skeleton_2026-07-02.json",
    "docs/power_ops_action_invariance_prose_draft_2026-07-02.json",
    "docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.json",
    "docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json",
)


def build_paper_claim_readiness(
    *,
    numeric_audit_path: str | Path,
    table_binding_path: str | Path,
    residual_triage_path: str | Path,
    writing_artifact_paths: Sequence[str | Path] = (),
) -> dict[str, Any]:
    numeric_audit = _load_json(numeric_audit_path)
    table_binding = _load_json(table_binding_path)
    residual_triage = _load_json(residual_triage_path)
    writing_artifacts = [_load_json(path) | {"_path": str(path)} for path in writing_artifact_paths]

    checks = {
        "numeric_claim_audit": _numeric_claim_check(numeric_audit, numeric_audit_path),
        "table_evidence_binding": _table_binding_check(table_binding, table_binding_path),
        "residual_numeric_triage": _residual_triage_check(residual_triage, residual_triage_path),
        "forbidden_claim_scan": _forbidden_claim_check(writing_artifacts),
    }
    blockers = [
        blocker
        for check in checks.values()
        for blocker in _list_value(check.get("blockers"))
        if isinstance(blocker, str) and blocker
    ]

    return {
        "artifact_type": "power_ops_paper_claim_readiness",
        "passed": not blockers,
        "status": "PASS" if not blockers else "FAIL",
        "blockers": blockers,
        "checks": checks,
    }


def render_paper_claim_readiness_markdown(readiness: Mapping[str, Any]) -> str:
    checks = _mapping_value(readiness.get("checks"))
    lines = [
        "# Power-Ops Paper Claim Readiness",
        "",
        f"**Status:** {readiness.get('status', 'FAIL')}",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(readiness.get("blockers"))
    if blockers:
        for blocker in blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Check | Status | Summary |",
            "|---|---|---|",
        ]
    )
    for name, check in checks.items():
        if not isinstance(check, Mapping):
            continue
        lines.append(
            "| {name} | {status} | {summary} |".format(
                name=name,
                status="PASS" if check.get("passed") else "FAIL",
                summary=_escape_table_text(str(check.get("summary", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_paper_claim_readiness(
    readiness: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paper_claim_readiness_markdown(readiness), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(readiness, ensure_ascii=False, indent=2), encoding="utf-8")


def _numeric_claim_check(audit: Mapping[str, Any], path: str | Path) -> dict[str, Any]:
    unsupported = int(audit.get("unsupported_numeric_claim_count", 0) or 0)
    blockers = []
    if unsupported:
        blockers.append(f"{unsupported} unsupported numeric claims remain in {path}")
    return {
        "passed": unsupported == 0,
        "source": str(path),
        "unsupported_numeric_claim_count": unsupported,
        "ignored_context_number_count": int(audit.get("ignored_context_number_count", 0) or 0),
        "supported_numeric_claim_count": int(audit.get("supported_numeric_claim_count", 0) or 0),
        "supported_by_table_binding_numeric_claim_count": int(
            audit.get("supported_by_table_binding_numeric_claim_count", 0) or 0
        ),
        "supported_by_context_rule_numeric_claim_count": int(
            audit.get("supported_by_context_rule_numeric_claim_count", 0) or 0
        ),
        "blockers": blockers,
        "summary": f"unsupported_numeric_claim_count={unsupported}",
    }


def _table_binding_check(binding: Mapping[str, Any], path: str | Path) -> dict[str, Any]:
    unsupported = int(binding.get("unsupported_row_count", 0) or 0)
    blockers = []
    if unsupported:
        blockers.append(f"{unsupported} unsupported table rows remain in {path}")
    return {
        "passed": unsupported == 0,
        "source": str(path),
        "unsupported_row_count": unsupported,
        "fully_supported_row_count": int(binding.get("fully_supported_row_count", 0) or 0),
        "table_count": int(binding.get("table_count", 0) or 0),
        "blockers": blockers,
        "summary": f"unsupported_row_count={unsupported}",
    }


def _residual_triage_check(triage: Mapping[str, Any], path: str | Path) -> dict[str, Any]:
    total = int(triage.get("total_needs_evidence_mentions", 0) or 0)
    categories = _mapping_value(triage.get("category_counts"))
    parser_extension = int(categories.get("parser_extension", 0) or 0)
    rewrite_needed = int(categories.get("rewrite_needed", 0) or 0)
    blockers = []
    if total:
        blockers.append(f"{total} residual needs-evidence mentions remain in {path}")
    if parser_extension:
        blockers.append(f"{parser_extension} parser-extension mentions remain in {path}")
    if rewrite_needed:
        blockers.append(f"{rewrite_needed} rewrite-needed mentions remain in {path}")
    return {
        "passed": not blockers,
        "source": str(path),
        "total_needs_evidence_mentions": total,
        "category_counts": categories,
        "blockers": blockers,
        "summary": (
            f"needs_evidence={total}; parser_extension={parser_extension}; "
            f"rewrite_needed={rewrite_needed}"
        ),
    }


def _forbidden_claim_check(writing_artifacts: list[Mapping[str, Any]]) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    for artifact in writing_artifacts:
        artifact_path = str(artifact.get("_path", ""))
        for hit in _list_value(artifact.get("forbidden_claim_hits")):
            if isinstance(hit, Mapping):
                hits.append({"artifact": artifact_path, **dict(hit)})
            else:
                hits.append({"artifact": artifact_path, "hit": str(hit)})
    blockers = []
    if hits:
        blockers.append(f"{len(hits)} forbidden claim hits remain in writing artifacts")
    return {
        "passed": not hits,
        "artifact_count": len(writing_artifacts),
        "artifact_paths": [str(artifact.get("_path", "")) for artifact in writing_artifacts],
        "forbidden_claim_hit_count": len(hits),
        "hits": hits,
        "blockers": blockers,
        "summary": f"forbidden_claim_hit_count={len(hits)}",
    }


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
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
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a pass/fail paper-claim readiness gate from power-ops audit artifacts."
    )
    parser.add_argument(
        "--numeric-audit",
        default="docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json",
    )
    parser.add_argument(
        "--table-binding",
        default="docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json",
    )
    parser.add_argument(
        "--residual-triage",
        default="docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json",
    )
    parser.add_argument(
        "--writing-artifact",
        action="append",
        default=list(DEFAULT_WRITING_ARTIFACT_PATHS),
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    readiness = build_paper_claim_readiness(
        numeric_audit_path=args.numeric_audit,
        table_binding_path=args.table_binding,
        residual_triage_path=args.residual_triage,
        writing_artifact_paths=args.writing_artifact,
    )
    write_paper_claim_readiness(readiness, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
