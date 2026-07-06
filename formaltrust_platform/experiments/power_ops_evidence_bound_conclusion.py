from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_CLAIM_LEDGER_READINESS = "docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json"
DEFAULT_PAPER_READINESS = "docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json"
DEFAULT_LIMITATIONS_PROSE = "docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.json"
DEFAULT_DRAFT_CONSISTENCY_AUDIT = "docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.json"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


def build_evidence_bound_conclusion(
    *,
    claim_ledger_readiness_path: str | Path = DEFAULT_CLAIM_LEDGER_READINESS,
    paper_readiness_path: str | Path = DEFAULT_PAPER_READINESS,
    limitations_prose_path: str | Path = DEFAULT_LIMITATIONS_PROSE,
    draft_consistency_audit_path: str | Path = DEFAULT_DRAFT_CONSISTENCY_AUDIT,
) -> dict[str, Any]:
    claim_readiness = _load_json(claim_ledger_readiness_path)
    paper_readiness = _load_json(paper_readiness_path)
    limitations = _load_json(limitations_prose_path)
    draft_audit = _load_json(draft_consistency_audit_path)

    blockers = _readiness_blockers(claim_readiness, paper_readiness, limitations, draft_audit)
    if blockers:
        return {
            "artifact_type": "power_ops_evidence_bound_conclusion",
            "conclusion_status": "blocked_incomplete_evidence",
            "blockers": blockers,
            "paragraphs": [],
            "conclusion_text": "",
            "forbidden_claim_hits": [],
        }

    paths = {
        "claim_readiness": str(claim_ledger_readiness_path),
        "paper_readiness": str(paper_readiness_path),
        "limitations": str(limitations_prose_path),
        "draft_audit": str(draft_consistency_audit_path),
    }
    paragraphs = [
        {
            "slot": "takeaway",
            "text": (
                "The main takeaway is field-level action invariance: strict supervision can preserve authorized "
                "power-operation action fields while removing or routing fields whose authority needs are not covered."
            ),
            "source_paths": [paths["claim_readiness"], paths["paper_readiness"]],
        },
        {
            "slot": "supported_evidence",
            "text": (
                "The current paper-ready claim set supports the final-action repair mode, curated and expanded "
                "power-operation fixtures, metamorphic authority-confusion tests, skill-driven multi-source authority, "
                "baseline comparisons, safety-preserving normal-behavior profiles, and trace replay or planner-chain import checks."
            ),
            "source_paths": [paths["claim_readiness"], paths["paper_readiness"], paths["draft_audit"]],
        },
        {
            "slot": "scope_boundary",
            "text": (
                "The conclusion inherits the limitation boundary: production telemetry, deployment safety, wall-clock "
                "latency, operator workload reduction, and official benchmark superiority remain outside the current "
                "supported claim set."
            ),
            "source_paths": [paths["limitations"], paths["paper_readiness"]],
        },
        {
            "slot": "next_work",
            "text": (
                "The next empirical step is to collect reviewed traces, measure timing, run operator workload studies, "
                "and compare on official benchmarks under pre-registered rules."
            ),
            "source_paths": [paths["limitations"], paths["claim_readiness"]],
        },
    ]
    conclusion_text = "\n\n".join(str(paragraph["text"]) for paragraph in paragraphs)
    forbidden_hits = _forbidden_claim_hits(conclusion_text)
    return {
        "artifact_type": "power_ops_evidence_bound_conclusion",
        "conclusion_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "blockers": [f"{len(forbidden_hits)} forbidden claim hits"] if forbidden_hits else [],
        "paper_ready_supported_claim_count": int(claim_readiness.get("paper_ready_supported_claim_count", 0) or 0),
        "forbidden_claim_count": int(claim_readiness.get("forbidden_claim_count", 0) or 0),
        "draft_section_count": int(draft_audit.get("section_count", 0) or 0),
        "paragraph_count": len(paragraphs),
        "paragraphs": paragraphs,
        "conclusion_text": conclusion_text,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_conclusion_markdown(conclusion: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Conclusion",
        "",
        f"**Status:** {conclusion.get('conclusion_status', '')}",
        "",
        "## 7 Conclusion",
        "",
    ]
    for paragraph in _list_value(conclusion.get("paragraphs")):
        if not isinstance(paragraph, Mapping):
            continue
        lines.extend(
            [
                str(paragraph.get("text", "")),
                "",
                "<!-- slot: {slot}; sources: {sources} -->".format(
                    slot=paragraph.get("slot", ""),
                    sources=", ".join(str(path) for path in _list_value(paragraph.get("source_paths"))),
                ),
                "",
            ]
        )
    return "\n".join(lines)


def write_evidence_bound_conclusion(
    conclusion: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_conclusion_markdown(conclusion), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(conclusion, ensure_ascii=False, indent=2), encoding="utf-8")


def _readiness_blockers(
    claim_readiness: Mapping[str, Any],
    paper_readiness: Mapping[str, Any],
    limitations: Mapping[str, Any],
    draft_audit: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if not bool(claim_readiness.get("readiness_passed", False)):
        blockers.append("claim ledger readiness is not passed")
    if int(claim_readiness.get("paper_ready_supported_claim_count", 0) or 0) <= 0:
        blockers.append("no paper-ready supported claims")
    if not bool(paper_readiness.get("passed", False)):
        blockers.append("paper claim readiness is not passed")
    if limitations.get("limitations_prose_status") != "ready":
        blockers.append("limitations prose is not ready")
    if draft_audit.get("audit_status") != "PASS":
        blockers.append("paper draft consistency audit is not passed")
    return blockers


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build bounded conclusion prose for the power-ops paper draft.")
    parser.add_argument("--claim-ledger-readiness", default=DEFAULT_CLAIM_LEDGER_READINESS)
    parser.add_argument("--paper-readiness", default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--limitations-prose", default=DEFAULT_LIMITATIONS_PROSE)
    parser.add_argument("--draft-consistency-audit", default=DEFAULT_DRAFT_CONSISTENCY_AUDIT)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    conclusion = build_evidence_bound_conclusion(
        claim_ledger_readiness_path=args.claim_ledger_readiness,
        paper_readiness_path=args.paper_readiness,
        limitations_prose_path=args.limitations_prose,
        draft_consistency_audit_path=args.draft_consistency_audit,
    )
    write_evidence_bound_conclusion(conclusion, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
