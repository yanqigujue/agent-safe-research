from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def build_readiness_bound_abstract(
    *,
    claim_ledger_readiness_path: str | Path,
) -> dict[str, Any]:
    sync = _load_json(claim_ledger_readiness_path)
    ready_claims = [
        _claim_summary(claim)
        for claim in _list_value(sync.get("supported_claims"))
        if isinstance(claim, Mapping) and bool(claim.get("paper_ready", False))
    ]
    forbidden_count = len(_list_value(sync.get("forbidden_claims")))
    if not ready_claims:
        return {
            "artifact_type": "power_ops_readiness_bound_abstract",
            "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
            "abstract_status": "blocked_no_ready_claims",
            "paper_ready_claim_count": 0,
            "forbidden_claim_count": forbidden_count,
            "abstract_skeleton": [],
            "intro_contribution_bullets": [],
            "limitations": _limitations(),
        }

    method_claims = _pick_claims(ready_claims, ("fieldwise repair final-action mode exists",))
    l2_claims = _pick_claims(
        ready_claims,
        (
            "curated power-ops",
            "expanded 18-case",
            "metamorphic",
            "skill",
            "performance profile",
            "baseline grid",
        ),
    )
    trace_claims = _pick_claims(
        ready_claims,
        (
            "trace/span/otlp",
            "trace import",
            "multi-step trace import",
            "agentdojo-style",
        ),
    )

    abstract_skeleton = [
        {
            "slot": "problem",
            "text": (
                "High-risk power-operation LLM agents need supervision that preserves authorized "
                "action fields while removing fields whose authority is not covered."
            ),
            "source_claims": method_claims[:1] or ready_claims[:1],
        },
        {
            "slot": "method",
            "text": (
                "The current artifact implements a fieldwise repair final-action mode and exposes "
                "the evidence attached to each paper-ready claim."
            ),
            "source_claims": method_claims[:1] or ready_claims[:1],
        },
        {
            "slot": "results",
            "text": (
                "The paper-ready result pool covers curated and expanded power-operation cases, "
                "metamorphic authority-confusion tests, skill-driven multi-source authority, baselines, and "
                "a safety-preserving normal-behavior profile."
            ),
            "source_claims": l2_claims[:6] or ready_claims[:3],
        },
        {
            "slot": "trace coverage",
            "text": (
                "The current trace evidence covers trace/span/OTLP replay, trace-import boundaries, "
                "planner-skill-tool-memory source chains, and bridge fixtures."
            ),
            "source_claims": trace_claims[:4] or ready_claims[-3:],
        },
        {
            "slot": "limitations",
            "text": (
                "Limitations remain explicit: no production telemetry, no real operator workload "
                "reduction claim, and no official neighboring-system superiority claim."
            ),
            "source_claims": ready_claims[:1],
        },
    ]

    intro_bullets = [
        {
            "slot": "formulation",
            "text": "Define field-level action invariance for supervised power-operation agent actions.",
            "source_claims": method_claims[:1] or ready_claims[:1],
        },
        {
            "slot": "implementation",
            "text": "Instantiate the property with a fieldwise repair mode and auditable claim ledger.",
            "source_claims": method_claims[:1] or ready_claims[:1],
        },
        {
            "slot": "evaluation",
            "text": "Report only paper-ready curated, expanded, metamorphic, skill, baseline, and trace evidence.",
            "source_claims": (l2_claims + trace_claims)[:6] or ready_claims[:4],
        },
        {
            "slot": "boundary",
            "text": "Keep production, workload, and official-baseline claims outside the abstract.",
            "source_claims": ready_claims[:1],
        },
    ]

    return {
        "artifact_type": "power_ops_readiness_bound_abstract",
        "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
        "abstract_status": "ready",
        "paper_ready_claim_count": len(ready_claims),
        "forbidden_claim_count": forbidden_count,
        "abstract_skeleton": abstract_skeleton,
        "intro_contribution_bullets": intro_bullets,
        "limitations": _limitations(),
    }


def render_readiness_bound_abstract_markdown(skeleton: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Readiness-Bound Abstract Skeleton",
        "",
        f"**Status:** {skeleton.get('abstract_status', '')}",
        f"**Paper-ready claims:** {int(skeleton.get('paper_ready_claim_count', 0))}",
        f"**Excluded forbidden claims:** {int(skeleton.get('forbidden_claim_count', 0))}",
        "",
        "## Abstract Skeleton",
        "",
    ]
    for item in _list_value(skeleton.get("abstract_skeleton")):
        if not isinstance(item, Mapping):
            continue
        lines.extend(
            [
                f"- **{item.get('slot', '')}:** {item.get('text', '')}",
                f"  Source claims: {_source_claim_labels(item.get('source_claims'))}",
            ]
        )

    lines.extend(
        [
            "",
            "## Introduction Contribution Bullets",
            "",
        ]
    )
    for item in _list_value(skeleton.get("intro_contribution_bullets")):
        if not isinstance(item, Mapping):
            continue
        lines.extend(
            [
                f"- **{item.get('slot', '')}:** {item.get('text', '')}",
                f"  Source claims: {_source_claim_labels(item.get('source_claims'))}",
            ]
        )

    lines.extend(
        [
            "",
            "## Limitations Kept Out Of Claims",
            "",
        ]
    )
    for limitation in _list_value(skeleton.get("limitations")):
        lines.append(f"- {limitation}")
    lines.append("")
    return "\n".join(lines)


def write_readiness_bound_abstract(
    skeleton: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_readiness_bound_abstract_markdown(skeleton), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(skeleton, ensure_ascii=False, indent=2), encoding="utf-8")


def _claim_summary(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "evidence": [str(item) for item in _list_value(claim.get("evidence")) if str(item)],
        "paper_ready": bool(claim.get("paper_ready", False)),
    }


def _pick_claims(claims: list[dict[str, Any]], keywords: tuple[str, ...]) -> list[dict[str, Any]]:
    picked: list[dict[str, Any]] = []
    for claim in claims:
        lowered = claim["claim"].lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            picked.append(claim)
    return picked


def _limitations() -> list[str]:
    return [
        "No production telemetry claim.",
        "No real operator workload reduction claim.",
        "No official neighboring-system superiority claim.",
        "No L5 production evidence.",
    ]


def _source_claim_labels(source_claims: Any) -> str:
    labels = [
        f"{str(claim.get('level', ''))}:{str(claim.get('claim', ''))}"
        for claim in _list_value(source_claims)
        if isinstance(claim, Mapping)
    ]
    if not labels:
        return "none"
    return "; ".join(f"`{label}`" for label in labels)


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
    parser = argparse.ArgumentParser(
        description="Generate abstract/introduction skeleton from paper-ready power-ops claims."
    )
    parser.add_argument(
        "--claim-ledger-readiness",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    skeleton = build_readiness_bound_abstract(
        claim_ledger_readiness_path=args.claim_ledger_readiness,
    )
    write_readiness_bound_abstract(skeleton, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
