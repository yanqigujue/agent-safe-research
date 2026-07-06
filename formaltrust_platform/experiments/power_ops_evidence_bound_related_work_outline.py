from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)

REQUIRED_NEIGHBORS = (
    "AgentSpec",
    "AgentVisor",
    "AgentSentry",
    "CaMeL",
    "ToolPrivBench",
    "RACG",
)


def build_evidence_bound_related_work_outline(
    *,
    lit_review_path: str | Path,
    novelty_firewall_path: str | Path,
) -> dict[str, Any]:
    lit_text = Path(lit_review_path).read_text(encoding="utf-8")
    firewall_text = Path(novelty_firewall_path).read_text(encoding="utf-8")
    missing_neighbors = [
        neighbor
        for neighbor in REQUIRED_NEIGHBORS
        if neighbor.lower() not in lit_text.lower()
    ]
    if missing_neighbors:
        return {
            "artifact_type": "power_ops_evidence_bound_related_work_outline",
            "source_lit_review": str(lit_review_path),
            "source_novelty_firewall": str(novelty_firewall_path),
            "paper_section": "§2 Related Work and Novelty Boundary",
            "related_work_outline_status": "blocked_no_related_work_sources",
            "missing_neighbors": missing_neighbors,
            "related_work_outline": [],
            "forbidden_claim_hits": [],
        }

    outline = [
        _item(
            slot="runtime_enforcement_neighbors",
            paragraph_goal=(
                "Position AgentSpec and formal-security-agent work as broad runtime enforcement "
                "neighbors that already cover general constraint monitoring."
            ),
            neighbor_papers=["AgentSpec", "AI Agents with Formal Security Guarantees"],
            pressure="Blocks broad runtime-enforcement novelty.",
            safe_delta=(
                "Field-level action invariance studies source-to-field authority coverage inside a "
                "candidate action, not a general policy DSL."
            ),
            claim_boundary="Do not present the artifact as a generic agent runtime monitor.",
            source_refs=[
                _source_ref(lit_review_path, "Closest Work Table", ("AgentSpec", "Formal Security")),
                _source_ref(novelty_firewall_path, "Closest Prior Work Delta", ("AgentSpec",)),
            ],
        ),
        _item(
            slot="prompt_injection_privilege_neighbors",
            paragraph_goal=(
                "Group AgentVisor, AgentSentry, and CaMeL as privilege separation, continuation, "
                "and capability-style prompt-injection neighbors."
            ),
            neighbor_papers=["AgentVisor", "AgentSentry", "CaMeL"],
            pressure="Blocks broad prompt-injection and semantic-privilege claims.",
            safe_delta=(
                "The current artifact repairs structured action fields after authority decisions "
                "and records witnesses for preserved fields."
            ),
            claim_boundary="Use these systems as close neighbors, not as failure cases.",
            source_refs=[
                _source_ref(lit_review_path, "Closest Work Table", ("AgentVisor", "AgentSentry", "CaMeL")),
                _source_ref(novelty_firewall_path, "Closest Prior Work Delta", ("AgentVisor", "AgentSentry", "CaMeL")),
            ],
        ),
        _item(
            slot="least_privilege_capability_neighbors",
            paragraph_goal=(
                "Position ToolPrivBench and RACG as closest least-privilege and capability "
                "minimization neighbors."
            ),
            neighbor_papers=["ToolPrivBench", "RACG"],
            pressure="Blocks simple least-privilege tool or capability-minimization novelty.",
            safe_delta=(
                "Those neighbors reason about tool choice or exposure; this slice checks whether "
                "each field in an already formed action is justified by its source authority."
            ),
            claim_boundary="Do not sell field repair as the first least-privilege agent method.",
            source_refs=[
                _source_ref(lit_review_path, "Closest Work Table", ("ToolPrivBench", "RACG")),
                _source_ref(novelty_firewall_path, "Closest Prior Work Delta", ("ToolPrivBench", "RACG")),
            ],
        ),
        _item(
            slot="over_conservatism_neighbors",
            paragraph_goal=(
                "Treat over-conservatism as established motivation through InjecGuard, "
                "AgentSentry, and AgentVisor."
            ),
            neighbor_papers=["InjecGuard", "AgentSentry", "AgentVisor"],
            pressure="Blocks claiming that over-defense itself is newly discovered.",
            safe_delta=(
                "The measurable object here is authorized final-field loss under intervention, "
                "not benign-prompt false positives."
            ),
            claim_boundary="Use over-conservatism as motivation only.",
            source_refs=[
                _source_ref(lit_review_path, "Landscape Summary", ("over-defense", "conservative blocking")),
                _source_ref(novelty_firewall_path, "Core Claims", ("C2", "C5")),
            ],
        ),
        _item(
            slot="action_invariance_delta",
            paragraph_goal=(
                "State the paper's defensible delta as field-level action invariance with authority "
                "witnesses and repair-frame validity."
            ),
            neighbor_papers=["AgentSpec", "AgentVisor", "AgentSentry", "CaMeL", "ToolPrivBench", "RACG"],
            pressure="Reviewers may collapse the idea into generic guardrails or capability security.",
            safe_delta=(
                "The safe claim is field-level action invariance: preserve authorized fields, "
                "remove invalid fields, and expose why each preserved field is allowed."
            ),
            claim_boundary="Limit empirical language to the current curated and trace-backed artifacts.",
            source_refs=[
                _source_ref(lit_review_path, "Positioning Takeaway", ("field-level action invariance",)),
                _source_ref(novelty_firewall_path, "Defensible Contribution Statement", ("field-level", "repair")),
            ],
        ),
        _item(
            slot="claim_boundary",
            paragraph_goal=(
                "End related work by naming unsupported claims before moving into the formal model."
            ),
            neighbor_papers=["AgentDojo", "AgentSpec", "AgentVisor", "AgentSentry", "CaMeL", "ToolPrivBench", "RACG"],
            pressure="Unsupported superiority or deployment-safety language would overstate the artifact.",
            safe_delta="",
            claim_boundary=(
                "No production telemetry, no official neighboring-system superiority, no generic "
                "agent-security firstness, and no real workload-reduction claim."
            ),
            source_refs=[
                _source_ref(lit_review_path, "Unsafe Headlines", ("Unsafe headlines",)),
                _source_ref(novelty_firewall_path, "Claim Boundary For Paper Draft", ("Forbidden",)),
            ],
        ),
    ]
    outline_text = "\n".join(
        " ".join(
            [
                item["paragraph_goal"],
                item["pressure"],
                item["safe_delta"],
                item["claim_boundary"],
            ]
        )
        for item in outline
    )
    forbidden_hits = _forbidden_claim_hits(outline_text)

    return {
        "artifact_type": "power_ops_evidence_bound_related_work_outline",
        "source_lit_review": str(lit_review_path),
        "source_novelty_firewall": str(novelty_firewall_path),
        "paper_section": "§2 Related Work and Novelty Boundary",
        "related_work_outline_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "neighbor_count": len(_unique_neighbor_names(outline)),
        "related_work_outline": outline,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_related_work_outline_markdown(outline: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Related Work Outline",
        "",
        f"**Status:** {outline.get('related_work_outline_status', '')}",
        f"**Paper section:** {outline.get('paper_section', '')}",
        f"**Neighbor count:** {int(outline.get('neighbor_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(outline.get('forbidden_claim_hits')))}",
        "",
        "## Related Work Outline",
        "",
        "| Slot | Goal | Neighbors | Pressure | Safe delta | Boundary | Source refs |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in _list_value(outline.get("related_work_outline")):
        if not isinstance(item, Mapping):
            continue
        lines.append(
            "| {slot} | {goal} | {neighbors} | {pressure} | {delta} | {boundary} | {refs} |".format(
                slot=_escape_table_text(str(item.get("slot", ""))),
                goal=_escape_table_text(str(item.get("paragraph_goal", ""))),
                neighbors=_escape_table_text("; ".join(str(x) for x in _list_value(item.get("neighbor_papers")))),
                pressure=_escape_table_text(str(item.get("pressure", ""))),
                delta=_escape_table_text(str(item.get("safe_delta", ""))),
                boundary=_escape_table_text(str(item.get("claim_boundary", ""))),
                refs=_escape_table_text("; ".join(str(x) for x in _list_value(item.get("source_refs")))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_related_work_outline(
    outline: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_related_work_outline_markdown(outline), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")


def _item(
    *,
    slot: str,
    paragraph_goal: str,
    neighbor_papers: list[str],
    pressure: str,
    safe_delta: str,
    claim_boundary: str,
    source_refs: list[str],
) -> dict[str, Any]:
    return {
        "slot": slot,
        "paragraph_goal": paragraph_goal,
        "neighbor_papers": neighbor_papers,
        "pressure": pressure,
        "safe_delta": safe_delta,
        "claim_boundary": claim_boundary,
        "source_refs": [ref for ref in source_refs if ref],
    }


def _source_ref(path: str | Path, section: str, tokens: tuple[str, ...]) -> str:
    suffix = ",".join(tokens)
    return f"{path}#{section} ({suffix})"


def _unique_neighbor_names(outline: list[Mapping[str, Any]]) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for item in outline:
        for name in _list_value(item.get("neighbor_papers")):
            text = str(name)
            if text and text not in seen:
                seen.add(text)
                names.append(text)
    return names


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an evidence-bound related-work outline from power-ops literature artifacts."
    )
    parser.add_argument(
        "--lit-review",
        default="docs/power_ops_action_invariance_lit_review_2026-07-02.md",
    )
    parser.add_argument(
        "--novelty-firewall",
        default="docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    outline = build_evidence_bound_related_work_outline(
        lit_review_path=args.lit_review,
        novelty_firewall_path=args.novelty_firewall,
    )
    write_evidence_bound_related_work_outline(outline, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
