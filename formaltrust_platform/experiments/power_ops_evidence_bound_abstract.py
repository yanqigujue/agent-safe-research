from __future__ import annotations

import argparse
import json
import re
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


def build_evidence_bound_abstract(*, skeleton_path: str | Path) -> dict[str, Any]:
    skeleton = _load_json(skeleton_path)
    skeleton_items = [
        item
        for item in _list_value(skeleton.get("abstract_skeleton"))
        if isinstance(item, Mapping)
    ]
    if str(skeleton.get("abstract_status", "")) != "ready" or not skeleton_items:
        return {
            "artifact_type": "power_ops_evidence_bound_abstract",
            "source_skeleton": str(skeleton_path),
            "abstract_status": "blocked_no_ready_skeleton",
            "abstract_text": "",
            "word_count": 0,
            "sentences": [],
            "forbidden_claim_hits": [],
        }

    by_slot = {str(item.get("slot", "")): item for item in skeleton_items}
    sentences = [
        _sentence(
            "High-risk power-operation LLM agents need supervision that preserves authorized action fields while removing fields without valid authority.",
            by_slot.get("problem", skeleton_items[0]),
        ),
        _sentence(
            "The current artifact implements fieldwise repair as an auditable final-action mode.",
            by_slot.get("method", skeleton_items[0]),
        ),
        _sentence(
            "Paper-ready evidence covers curated and expanded power-operation cases, metamorphic authority-confusion tests, skill-driven multi-source authority, baselines, and safety-preserving normal-behavior profiles.",
            by_slot.get("results", skeleton_items[0]),
        ),
        _sentence(
            "Trace evidence covers trace/span/OTLP replay, trace-import boundaries, planner-skill-tool-memory source chains, and bridge fixtures.",
            by_slot.get("trace coverage", skeleton_items[0]),
        ),
        _sentence(
            "We keep the boundary explicit: no production telemetry, no real operator workload reduction claim, and no official neighboring-system superiority claim.",
            by_slot.get("limitations", skeleton_items[0]),
        ),
    ]
    abstract_text = " ".join(sentence["text"] for sentence in sentences)
    forbidden_hits = _forbidden_claim_hits(abstract_text)

    return {
        "artifact_type": "power_ops_evidence_bound_abstract",
        "source_skeleton": str(skeleton_path),
        "abstract_status": "ready" if not forbidden_hits else "blocked_forbidden_claim",
        "abstract_text": abstract_text,
        "word_count": _word_count(abstract_text),
        "sentences": sentences,
        "forbidden_claim_hits": forbidden_hits,
    }


def render_evidence_bound_abstract_markdown(abstract: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Evidence-Bound Abstract",
        "",
        f"**Status:** {abstract.get('abstract_status', '')}",
        f"**Word count:** {int(abstract.get('word_count', 0))}",
        f"**Forbidden claim hits:** {len(_list_value(abstract.get('forbidden_claim_hits')))}",
        "",
        "## Abstract",
        "",
        str(abstract.get("abstract_text", "")),
        "",
        "## Sentence Evidence",
        "",
        "| Sentence | Source slot | Source claims |",
        "|---|---|---|",
    ]
    for sentence in _list_value(abstract.get("sentences")):
        if not isinstance(sentence, Mapping):
            continue
        lines.append(
            "| {sentence} | {slot} | {claims} |".format(
                sentence=_escape_table_text(str(sentence.get("text", ""))),
                slot=_escape_table_text(str(sentence.get("source_slot", ""))),
                claims=_escape_table_text(_source_claim_labels(sentence.get("source_claims"))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_evidence_bound_abstract(
    abstract: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_evidence_bound_abstract_markdown(abstract), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(abstract, ensure_ascii=False, indent=2), encoding="utf-8")


def _sentence(text: str, source_item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "text": text,
        "source_slot": str(source_item.get("slot", "")),
        "source_claims": [
            _source_claim_summary(claim)
            for claim in _list_value(source_item.get("source_claims"))
            if isinstance(claim, Mapping)
        ],
    }


def _source_claim_summary(claim: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "paper_ready": bool(claim.get("paper_ready", False)),
        "evidence": [str(item) for item in _list_value(claim.get("evidence")) if str(item)],
    }


def _forbidden_claim_hits(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9_/-]+", text))


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
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate concise abstract prose from readiness-bound abstract skeleton."
    )
    parser.add_argument(
        "--skeleton",
        default="docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    abstract = build_evidence_bound_abstract(skeleton_path=args.skeleton)
    write_evidence_bound_abstract(abstract, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
