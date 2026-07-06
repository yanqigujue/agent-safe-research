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


def build_evidence_bound_limitations_outline(
    *,
    paper_outline_path: str | Path,
    claim_ledger_readiness_path: str | Path,
    paper_claim_readiness_path: str | Path,
) -> dict[str, Any]:
    paper_outline = _load_json(paper_outline_path)
    claim_sync = _load_json(claim_ledger_readiness_path)
    paper_readiness = _load_json(paper_claim_readiness_path)

    if bool(paper_readiness.get("passed")) is not True:
        return {
            "artifact_type": "power_ops_evidence_bound_limitations_outline",
            "source_paper_outline": str(paper_outline_path),
            "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
            "source_paper_claim_readiness": str(paper_claim_readiness_path),
            "paper_section": "§6 Limitations and Next Experiments",
            "limitations_outline_status": "blocked_claim_readiness_failed",
            "paper_readiness_passed": False,
            "readiness_blockers": [
                str(blocker)
                for blocker in _list_value(paper_readiness.get("blockers"))
                if str(blocker)
            ],
            "limitations_outline": [],
            "forbidden_claim_hits": [],
        }

    forbidden_claims = [
        str(row.get("claim", ""))
        for row in _list_value(claim_sync.get("forbidden_claims"))
        if isinstance(row, Mapping) and str(row.get("claim", ""))
    ]
    if str(claim_sync.get("readiness_status", "")) != "PASS" or not forbidden_claims:
        return {
            "artifact_type": "power_ops_evidence_bound_limitations_outline",
            "source_paper_outline": str(paper_outline_path),
            "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
            "source_paper_claim_readiness": str(paper_claim_readiness_path),
            "paper_section": "§6 Limitations and Next Experiments",
            "limitations_outline_status": "blocked_no_forbidden_claim_boundary",
            "paper_readiness_passed": True,
            "limitations_outline": [],
            "forbidden_claim_hits": [],
        }

    section_goal = _section_goal(paper_outline, "Limitations")
    outline = [
        _item(
            slot="production_trace_gap",
            paragraph_goal=(
                "State that current trace evidence is fixture, bridge, span, OTLP, and import "
                "evidence, not production telemetry or live deployment evidence."
            ),
            excluded_claims=_pick_claims(forbidden_claims, ("production safety",)),
            future_work=[
                "Collect reviewed real or semi-real multi-step power-agent traces before any production-safety claim.",
            ],
            source_refs=[
                _paper_ref(paper_outline_path, section_goal),
                f"{claim_ledger_readiness_path}#forbidden_claims",
            ],
        ),
        _item(
            slot="latency_gap",
            paragraph_goal=(
                "State that the performance profile uses a field-check latency proxy and does not "
                "measure wall-clock latency."
            ),
            excluded_claims=[],
            future_work=[
                "Measure wall-clock latency with runtime instrumentation before reporting speed claims.",
            ],
            source_refs=[
                _paper_ref(paper_outline_path, section_goal),
                "docs/power_ops_action_invariance_performance_2026-07-02.json#latency_proxy_units",
            ],
        ),
        _item(
            slot="operator_workload_gap",
            paragraph_goal=(
                "State that the current artifact does not support real operator workload reduction "
                "because there is no operator-time or human-study evidence."
            ),
            excluded_claims=_pick_claims(forbidden_claims, ("human workload", "workload")),
            future_work=[
                "Run operator-time or reviewer-burden studies before any real workload-reduction claim.",
            ],
            source_refs=[
                _paper_ref(paper_outline_path, section_goal),
                f"{claim_ledger_readiness_path}#forbidden_claims",
            ],
        ),
        _item(
            slot="official_benchmark_gap",
            paragraph_goal=(
                "State that AgentDojo-style and semi-real bridge fixtures are expressibility "
                "evidence, not official benchmark superiority."
            ),
            excluded_claims=_pick_claims(forbidden_claims, ("official neighboring", "outperforms")),
            future_work=[
                "Run official external benchmarks and pre-register comparison rules before any superiority claim.",
            ],
            source_refs=[
                _paper_ref(paper_outline_path, section_goal),
                f"{claim_ledger_readiness_path}#forbidden_claims",
            ],
        ),
        _item(
            slot="forbidden_firstness_security_claims",
            paragraph_goal=(
                "List firstness, generic runtime-enforcement, least-privilege, and prompt-injection "
                "claims as excluded from the current paper."
            ),
            excluded_claims=_pick_claims(
                forbidden_claims,
                (
                    "first llm-agent",
                    "first runtime",
                    "first least-privilege",
                    "solves prompt injection",
                ),
            ),
            future_work=[
                "Keep novelty phrased as field-level action invariance with authority witnesses and repair validity.",
            ],
            source_refs=[
                f"{claim_ledger_readiness_path}#forbidden_claims",
                "docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Forbidden",
            ],
        ),
        _item(
            slot="next_experiments",
            paragraph_goal=(
                "Convert the limitations into next experiments: real or semi-real traces, "
                "wall-clock timing, operator workload, and official benchmark comparison."
            ),
            excluded_claims=[],
            future_work=[
                "Collect reviewed traces.",
                "Measure wall-clock latency.",
                "Run operator workload studies.",
                "Run official benchmark comparisons.",
            ],
            source_refs=[
                _paper_ref(paper_outline_path, section_goal),
                f"{paper_claim_readiness_path}#checks",
            ],
        ),
    ]
    outline_text = "\n".join(
        " ".join(
            [
                str(item.get("paragraph_goal", "")),
                " ".join(str(work) for work in _list_value(item.get("future_work"))),
            ]
        )
        for item in outline
    )
    forbidden_hits = _forbidden_claim_hits(outline_text)

    return {
        "artifact_type": "power_ops_evidence_bound_limitations_outline",
        "source_paper_outline": str(paper_outline_path),
        "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
        "source_paper_claim_readiness": str(paper_claim_readiness_path),
        "paper_section": "§6 Limitations and Next Experiments",
        "section_goal": section_goal,
        "limitations_outline_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paper_readiness_passed": True,
        "forbidden_claim_count": len(forbidden_claims),
        "limitations_outline": outline,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_limitations_outline_markdown(outline: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Limitations Outline",
        "",
        f"**Status:** {outline.get('limitations_outline_status', '')}",
        f"**Paper section:** {outline.get('paper_section', '')}",
        f"**Forbidden claim count:** {int(outline.get('forbidden_claim_count', 0) or 0)}",
        f"**Paper readiness passed:** {bool(outline.get('paper_readiness_passed', False))}",
        f"**Forbidden claim hits:** {len(_list_value(outline.get('forbidden_claim_hits')))}",
        "",
        "## Limitations Outline",
        "",
        "| Slot | Paragraph goal | Excluded claims | Future work | Source refs |",
        "|---|---|---|---|---|",
    ]
    for item in _list_value(outline.get("limitations_outline")):
        if not isinstance(item, Mapping):
            continue
        lines.append(
            "| {slot} | {goal} | {excluded} | {future} | {refs} |".format(
                slot=_escape_table_text(str(item.get("slot", ""))),
                goal=_escape_table_text(str(item.get("paragraph_goal", ""))),
                excluded=_escape_table_text("; ".join(str(claim) for claim in _list_value(item.get("excluded_claims")))),
                future=_escape_table_text("; ".join(str(work) for work in _list_value(item.get("future_work")))),
                refs=_escape_table_text("; ".join(str(ref) for ref in _list_value(item.get("source_refs")))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_limitations_outline(
    outline: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_limitations_outline_markdown(outline), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")


def _item(
    *,
    slot: str,
    paragraph_goal: str,
    excluded_claims: list[str],
    future_work: list[str],
    source_refs: list[str],
) -> dict[str, Any]:
    return {
        "slot": slot,
        "paragraph_goal": paragraph_goal,
        "excluded_claims": excluded_claims,
        "future_work": future_work,
        "source_refs": [ref for ref in source_refs if ref],
    }


def _pick_claims(claims: list[str], keywords: tuple[str, ...]) -> list[str]:
    picked: list[str] = []
    for claim in claims:
        lowered = claim.lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            picked.append(claim)
    return picked


def _section_goal(paper_outline: Mapping[str, Any], section_keyword: str) -> str:
    for item in _list_value(paper_outline.get("section_plan")):
        if not isinstance(item, Mapping):
            continue
        if section_keyword.lower() in str(item.get("section", "")).lower():
            return str(item.get("goal", ""))
    return ""


def _paper_ref(path: str | Path, section_goal: str) -> str:
    if not section_goal:
        return str(path)
    return f"{path}#§6 Limitations and Next Experiments"


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


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an evidence-bound limitations outline from power-ops claim boundaries."
    )
    parser.add_argument(
        "--paper-outline",
        default="docs/power_ops_action_invariance_paper_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--claim-ledger-readiness",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--paper-claim-readiness",
        default="docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    outline = build_evidence_bound_limitations_outline(
        paper_outline_path=args.paper_outline,
        claim_ledger_readiness_path=args.claim_ledger_readiness,
        paper_claim_readiness_path=args.paper_claim_readiness,
    )
    write_evidence_bound_limitations_outline(outline, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
