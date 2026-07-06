from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_PARAGRAPH_MAP = "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.json"

FORBIDDEN_CLAIM_PHRASES = (
    "first llm-agent guardrail",
    "first runtime enforcement framework",
    "first least-privilege llm-agent security framework",
    "solves prompt injection",
    "proves production safety",
    "outperforms official neighboring systems",
    "reduces real human workload",
)


def build_paragraph_evidence_packets(
    *,
    paragraph_map_path: str | Path = DEFAULT_PARAGRAPH_MAP,
) -> dict[str, Any]:
    paragraph_map = _load_json(paragraph_map_path)
    rows = [
        row
        for row in _list_value(paragraph_map.get("paragraph_rows"))
        if isinstance(row, Mapping)
    ]
    claim_packets = _claim_packets(rows)
    source_only_audit_rows = _source_only_audit_rows(rows)
    source_only_packet_count = len(
        {
            str(row.get("resolution", ""))
            for row in source_only_audit_rows
            if row.get("resolution") != "needs_stronger_claim_binding"
        }
    )
    reviewer_packet_count = len(claim_packets) + source_only_packet_count
    needs_stronger = [
        row
        for row in source_only_audit_rows
        if row.get("resolution") == "needs_stronger_claim_binding"
    ]
    forbidden_hits = _forbidden_hits(claim_packets, rows)

    blockers: list[str] = []
    if paragraph_map.get("map_status") != "PASS":
        blockers.append(f"paragraph map status is {paragraph_map.get('map_status')}")
    if needs_stronger:
        blockers.append(f"{len(needs_stronger)} source-only rows need stronger claim binding")
    if forbidden_hits:
        blockers.append(f"{len(forbidden_hits)} forbidden claim hits remain in packet text")

    paragraph_count = len(rows)
    return {
        "artifact_type": "power_ops_paragraph_evidence_packets",
        "paragraph_map_path": str(paragraph_map_path),
        "paragraph_map_content_sha256": _file_sha256(paragraph_map_path),
        "draft_content_sha256": str(paragraph_map.get("draft_content_sha256", "")),
        "packet_status": "PASS" if not blockers else "FAIL",
        "passed": not blockers,
        "blockers": blockers,
        "paragraph_count": paragraph_count,
        "claim_packet_count": len(claim_packets),
        "source_only_row_count": len(source_only_audit_rows),
        "source_only_packet_count": source_only_packet_count,
        "reviewer_packet_count": reviewer_packet_count,
        "audit_compression_ratio": _compression_ratio(paragraph_count, reviewer_packet_count),
        "needs_stronger_binding_count": len(needs_stronger),
        "boundary_only_source_row_count": sum(
            1 for row in source_only_audit_rows if row.get("resolution") == "boundary_only"
        ),
        "forbidden_claim_hits": forbidden_hits,
        "claim_packets": claim_packets,
        "source_only_audit_rows": source_only_audit_rows,
    }


def render_paragraph_evidence_packets_markdown(packets: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Paragraph Evidence Packets",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Packet status | {packets.get('packet_status', 'FAIL')} |",
        f"| Paragraph rows | {int(packets.get('paragraph_count', 0) or 0)} |",
        f"| Claim packets | {int(packets.get('claim_packet_count', 0) or 0)} |",
        f"| Source-only rows | {int(packets.get('source_only_row_count', 0) or 0)} |",
        f"| Reviewer packets | {int(packets.get('reviewer_packet_count', 0) or 0)} |",
        f"| Audit compression ratio | {float(packets.get('audit_compression_ratio', 0.0) or 0.0):.3f} |",
        f"| Needs stronger binding | {int(packets.get('needs_stronger_binding_count', 0) or 0)} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(packets.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Claim Packets",
            "",
            "| Claim | Level | Paragraphs | Evidence refs | Boundary flags |",
            "|---|---|---:|---:|---|",
        ]
    )
    for packet in _list_value(packets.get("claim_packets")):
        if not isinstance(packet, Mapping):
            continue
        lines.append(
            "| {claim} | {level} | {paragraphs} | {refs} | {flags} |".format(
                claim=_escape_table_text(str(packet.get("claim", ""))),
                level=_escape_table_text(str(packet.get("level", ""))),
                paragraphs=len(_list_value(packet.get("paragraph_refs"))),
                refs=len(_list_value(packet.get("evidence_refs"))),
                flags=_escape_table_text(",".join(_list_value(packet.get("boundary_flags")))),
            )
        )

    lines.extend(
        [
            "",
            "## Source-Only Audit",
            "",
            "| Section | Para | Resolution | Evidence refs | Boundary flags |",
            "|---|---:|---|---:|---|",
        ]
    )
    for row in _list_value(packets.get("source_only_audit_rows")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| {slot} | {para} | {resolution} | {refs} | {flags} |".format(
                slot=_escape_table_text(str(row.get("slot", ""))),
                para=int(row.get("paragraph_index", 0) or 0),
                resolution=_escape_table_text(str(row.get("resolution", ""))),
                refs=len(_list_value(row.get("evidence_refs"))),
                flags=_escape_table_text(",".join(_list_value(row.get("boundary_flags")))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_paragraph_evidence_packets(
    packets: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paragraph_evidence_packets_markdown(packets), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(packets, ensure_ascii=False, indent=2), encoding="utf-8")


def _claim_packets(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        paragraph_ref = {
            "slot": str(row.get("slot", "")),
            "paragraph_index": int(row.get("paragraph_index", 0) or 0),
            "source_path": str(row.get("source_path", "")),
            "boundary_flags": _string_values(row.get("boundary_flags")),
        }
        for claim in _list_value(row.get("source_claims")):
            if not isinstance(claim, Mapping):
                continue
            claim_text = str(claim.get("claim", ""))
            if not claim_text:
                continue
            packet = grouped.setdefault(
                claim_text,
                {
                    "claim": claim_text,
                    "level": str(claim.get("level", "")),
                    "paper_ready": bool(claim.get("paper_ready", False)),
                    "paragraph_refs": [],
                    "evidence_refs": [],
                    "boundary_flags": [],
                },
            )
            packet["paragraph_refs"].append(paragraph_ref)
            packet["evidence_refs"].extend(_string_values(claim.get("evidence")))
            packet["evidence_refs"].extend(_string_values(row.get("evidence_refs")))
            packet["boundary_flags"].extend(_string_values(row.get("boundary_flags")))

    packets = []
    for packet in grouped.values():
        packet["evidence_refs"] = _dedupe_strings(packet["evidence_refs"])
        packet["boundary_flags"] = _dedupe_strings(packet["boundary_flags"])
        packet["paragraph_refs"] = _dedupe_paragraph_refs(packet["paragraph_refs"])
        packet["paragraph_count"] = len(packet["paragraph_refs"])
        packet["evidence_ref_count"] = len(packet["evidence_refs"])
        packets.append(packet)
    packets.sort(key=lambda packet: (str(packet.get("level", "")), str(packet.get("claim", ""))))
    return packets


def _source_only_audit_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    audit_rows = []
    for row in rows:
        if row.get("claim_binding_status") != "source_mapped":
            continue
        boundary_flags = _string_values(row.get("boundary_flags"))
        evidence_refs = _string_values(row.get("evidence_refs"))
        resolution = _source_only_resolution(
            slot=str(row.get("slot", "")),
            evidence_refs=evidence_refs,
            boundary_flags=boundary_flags,
        )
        audit_rows.append(
            {
                "slot": str(row.get("slot", "")),
                "paragraph_index": int(row.get("paragraph_index", 0) or 0),
                "source_path": str(row.get("source_path", "")),
                "evidence_refs": evidence_refs,
                "boundary_flags": boundary_flags,
                "resolution": resolution,
                "paragraph_text": str(row.get("paragraph_text", "")),
            }
        )
    return audit_rows


def _source_only_resolution(*, slot: str, evidence_refs: Sequence[str], boundary_flags: Sequence[str]) -> str:
    if boundary_flags:
        return "boundary_only"
    if slot == "related_work" and evidence_refs:
        return "related_work_context"
    if slot == "evaluation_setup" and evidence_refs:
        return "evaluation_audit_context"
    if slot in {"limitations", "conclusion"} and evidence_refs:
        return "limitation_or_next_work_context"
    if evidence_refs:
        return "source_context"
    return "needs_stronger_claim_binding"


def _forbidden_hits(claim_packets: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    texts = [str(packet.get("claim", "")) for packet in claim_packets]
    texts.extend(str(row.get("paragraph_text", "")) for row in rows)
    lowered = "\n".join(texts).lower()
    return [
        {"phrase": phrase}
        for phrase in FORBIDDEN_CLAIM_PHRASES
        if phrase in lowered
    ]


def _compression_ratio(paragraph_count: int, reviewer_packet_count: int) -> float:
    if paragraph_count <= 0:
        return 0.0
    return round(1.0 - (reviewer_packet_count / paragraph_count), 6)


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _string_values(value: Any) -> list[str]:
    values: list[str] = []
    for item in _list_value(value):
        if isinstance(item, str) and item:
            values.append(item)
    return values


def _dedupe_strings(values: Sequence[str]) -> list[str]:
    seen = set()
    deduped = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


def _dedupe_paragraph_refs(refs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    deduped = []
    for ref in refs:
        key = (str(ref.get("slot", "")), int(ref.get("paragraph_index", 0) or 0))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(dict(ref))
    return deduped


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compress power-ops paragraph evidence map into reviewer-facing claim packets."
    )
    parser.add_argument("--paragraph-map", default=DEFAULT_PARAGRAPH_MAP)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    packets = build_paragraph_evidence_packets(paragraph_map_path=args.paragraph_map)
    write_paragraph_evidence_packets(packets, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
