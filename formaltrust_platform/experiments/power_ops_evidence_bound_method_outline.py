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


def build_evidence_bound_method_outline(
    *,
    formal_model_path: str | Path,
    claim_ledger_readiness_path: str | Path,
    paper_outline_path: str | Path,
) -> dict[str, Any]:
    formal_text = Path(formal_model_path).read_text(encoding="utf-8")
    claim_sync = _load_json(claim_ledger_readiness_path)
    paper_outline = _load_json(paper_outline_path)
    ready_claims = [
        _claim_summary(claim)
        for claim in _list_value(claim_sync.get("supported_claims"))
        if isinstance(claim, Mapping) and bool(claim.get("paper_ready", False))
    ]
    if not ready_claims:
        return {
            "artifact_type": "power_ops_evidence_bound_method_outline",
            "source_formal_model": str(formal_model_path),
            "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
            "source_paper_outline": str(paper_outline_path),
            "paper_section": "§3 Formal Model and CapGuard",
            "method_outline_status": "blocked_no_ready_claims",
            "method_outline": [],
            "forbidden_claim_hits": [],
        }

    method_claims = _pick_claims(ready_claims, ("fieldwise repair final-action mode exists",))
    result_claims = _pick_claims(
        ready_claims,
        (
            "curated power-ops",
            "expanded 18-case",
            "metamorphic",
            "skill",
            "baseline grid",
            "trace/span",
            "trace import",
            "multi-step trace",
        ),
    )
    section_goal = _section_goal(paper_outline, "Formal Model and CapGuard")

    outline = [
        _item(
            slot="formal_objects",
            paragraph_goal=(
                "Define Cap(x) for source-derived capabilities and Need(s,f) for field-level "
                "authority needs in power-operation actions."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "1. Objects", formal_text, ("Cap(x)", "Need(s, f)")),
                _paper_ref(paper_outline_path, section_goal),
            ],
            source_claims=method_claims[:1],
        ),
        _item(
            slot="coverage_rule",
            paragraph_goal=(
                "Specify Covers(c,n) across role, field, operation, data scope, effect scope, "
                "delegation scope, time scope, and obligations."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "2. Coverage", formal_text, ("Covers(c, n)", "obligations_satisfied")),
            ],
            source_claims=method_claims[:1],
        ),
        _item(
            slot="minimal_witness_decision",
            paragraph_goal=(
                "Explain Minimal Authority Witness and the field decision rule: allow, abstain, "
                "or block."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "3. Minimal Authority Witness", formal_text, ("MinimalWitness",)),
                _formal_ref(formal_model_path, "4. Decision Rule", formal_text, ("FieldDecision",)),
            ],
            source_claims=method_claims[:1],
        ),
        _item(
            slot="repair_invariance",
            paragraph_goal=(
                "Define Preserve, Prevent, ActionInvariant, conservative collapse, and Repair(a) "
                "as the method's action-preservation target."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "5. Action Invariance", formal_text, ("ActionInvariant",)),
                _formal_ref(formal_model_path, "6. Conservative Collapse", formal_text, ("strict_block_collapse_rate",)),
                _formal_ref(formal_model_path, "9. Claim Boundary", formal_text, ("Repair(a)",)),
            ],
            source_claims=(method_claims + result_claims)[:3],
        ),
        _item(
            slot="implementation_binding",
            paragraph_goal=(
                "Map formal objects to FormalTrust runtime locations without adding new state "
                "schema fields."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "8. Current Implementation Binding", formal_text, ("metrics[", "afw_runtime_field_results")),
            ],
            source_claims=method_claims[:1],
        ),
        _item(
            slot="claim_boundary",
            paragraph_goal=(
                "State that the method section supports a local artifact and benchmark slice, not "
                "production telemetry or operator workload claims."
            ),
            source_refs=[
                _formal_ref(formal_model_path, "9. Claim Boundary", formal_text, ("live deployment safety", "human-label agreement")),
            ],
            source_claims=method_claims[:1],
            limitation_reason="No production telemetry; no real workload reduction; no official neighboring-system superiority.",
        ),
    ]
    outline_text = "\n".join(item["paragraph_goal"] for item in outline)
    forbidden_hits = _forbidden_claim_hits(outline_text)

    return {
        "artifact_type": "power_ops_evidence_bound_method_outline",
        "source_formal_model": str(formal_model_path),
        "source_claim_ledger_readiness": str(claim_ledger_readiness_path),
        "source_paper_outline": str(paper_outline_path),
        "paper_section": "§3 Formal Model and CapGuard",
        "section_goal": section_goal,
        "method_outline_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "paper_ready_claim_count": len(ready_claims),
        "method_outline": outline,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_method_outline_markdown(outline: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Method Outline",
        "",
        f"**Status:** {outline.get('method_outline_status', '')}",
        f"**Paper section:** {outline.get('paper_section', '')}",
        f"**Paper-ready claims:** {int(outline.get('paper_ready_claim_count', 0) or 0)}",
        f"**Forbidden claim hits:** {len(_list_value(outline.get('forbidden_claim_hits')))}",
        "",
        "## Method Outline",
        "",
        "| Slot | Paragraph goal | Source refs | Source claims | Limitation reason |",
        "|---|---|---|---|---|",
    ]
    for item in _list_value(outline.get("method_outline")):
        if not isinstance(item, Mapping):
            continue
        lines.append(
            "| {slot} | {goal} | {refs} | {claims} | {limitation} |".format(
                slot=_escape_table_text(str(item.get("slot", ""))),
                goal=_escape_table_text(str(item.get("paragraph_goal", ""))),
                refs=_escape_table_text("; ".join(str(ref) for ref in _list_value(item.get("source_refs")))),
                claims=_escape_table_text(_source_claim_labels(item.get("source_claims"))),
                limitation=_escape_table_text(str(item.get("limitation_reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_method_outline(
    outline: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_method_outline_markdown(outline), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")


def _item(
    *,
    slot: str,
    paragraph_goal: str,
    source_refs: list[str],
    source_claims: list[dict[str, Any]],
    limitation_reason: str = "",
) -> dict[str, Any]:
    return {
        "slot": slot,
        "paragraph_goal": paragraph_goal,
        "source_refs": [ref for ref in source_refs if ref],
        "source_claims": source_claims,
        "limitation_reason": limitation_reason,
    }


def _formal_ref(path: str | Path, section: str, formal_text: str, tokens: tuple[str, ...]) -> str:
    found = [token for token in tokens if token.lower() in formal_text.lower()]
    suffix = f" ({', '.join(found)})" if found else ""
    return f"{path}#{section}{suffix}"


def _paper_ref(path: str | Path, section_goal: str) -> str:
    if not section_goal:
        return str(path)
    return f"{path}#§3 Formal Model and CapGuard"


def _section_goal(paper_outline: Mapping[str, Any], section_keyword: str) -> str:
    for item in _list_value(paper_outline.get("section_plan")):
        if not isinstance(item, Mapping):
            continue
        section = str(item.get("section", ""))
        if section_keyword.lower() in section.lower():
            return str(item.get("goal", ""))
    return ""


def _claim_summary(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "paper_ready": bool(claim.get("paper_ready", False)),
        "evidence": [str(item) for item in _list_value(claim.get("evidence")) if str(item)],
    }


def _pick_claims(claims: list[dict[str, Any]], keywords: tuple[str, ...]) -> list[dict[str, Any]]:
    picked: list[dict[str, Any]] = []
    for claim in claims:
        lowered = claim["claim"].lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            picked.append(claim)
    return picked


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _source_claim_labels(source_claims: Any) -> str:
    labels = [
        f"{str(claim.get('level', ''))}:{str(claim.get('claim', ''))}"
        for claim in _list_value(source_claims)
        if isinstance(claim, Mapping)
    ]
    if not labels:
        return "none"
    return "; ".join(labels)


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
        description="Generate an evidence-bound method-section outline from power-ops formal artifacts."
    )
    parser.add_argument(
        "--formal-model",
        default="docs/power_ops_action_invariance_formal_model_2026-07-02.md",
    )
    parser.add_argument(
        "--claim-ledger-readiness",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--paper-outline",
        default="docs/power_ops_action_invariance_paper_outline_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    outline = build_evidence_bound_method_outline(
        formal_model_path=args.formal_model,
        claim_ledger_readiness_path=args.claim_ledger_readiness,
        paper_outline_path=args.paper_outline,
    )
    write_evidence_bound_method_outline(outline, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
