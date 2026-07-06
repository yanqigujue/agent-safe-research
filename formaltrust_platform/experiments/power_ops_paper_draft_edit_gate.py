from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_DRAFT_PATH = "docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json"
DEFAULT_PARAGRAPH_MAP = "docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.json"
DEFAULT_PARAGRAPH_PACKETS = "docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.json"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.json"


def build_paper_draft_edit_gate(
    *,
    draft_path: str | Path = DEFAULT_DRAFT_PATH,
    paragraph_map_path: str | Path = DEFAULT_PARAGRAPH_MAP,
    paragraph_packets_path: str | Path = DEFAULT_PARAGRAPH_PACKETS,
) -> dict[str, Any]:
    draft = _load_json(draft_path)
    paragraph_map = _load_json(paragraph_map_path)
    packets = _load_json(paragraph_packets_path)

    current_draft_hash = _draft_content_sha256(draft)
    map_recorded_draft_hash = str(paragraph_map.get("draft_content_sha256", ""))
    current_map_hash = _file_sha256(paragraph_map_path)
    packet_recorded_map_hash = str(packets.get("paragraph_map_content_sha256", ""))

    draft_map_hash_matches = bool(map_recorded_draft_hash) and current_draft_hash == map_recorded_draft_hash
    packet_map_hash_matches = bool(packet_recorded_map_hash) and current_map_hash == packet_recorded_map_hash
    stale_artifacts = []
    blockers: list[str] = []

    if draft.get("paper_draft_status") != "ready":
        blockers.append(f"paper draft status is {draft.get('paper_draft_status')}")
    if paragraph_map.get("map_status") != "PASS":
        blockers.append(f"paragraph map status is {paragraph_map.get('map_status')}")
    if packets.get("packet_status") != "PASS":
        blockers.append(f"paragraph packet status is {packets.get('packet_status')}")
    if not draft_map_hash_matches:
        stale_artifacts.append("paragraph_map")
        blockers.append("paragraph map is stale relative to the assembled paper draft")
    if not packet_map_hash_matches:
        stale_artifacts.append("paragraph_packets")
        blockers.append("paragraph packets are stale relative to the paragraph map")

    return {
        "artifact_type": "power_ops_paper_draft_edit_gate",
        "draft_path": str(draft_path),
        "paragraph_map_path": str(paragraph_map_path),
        "paragraph_packets_path": str(paragraph_packets_path),
        "gate_status": "PASS" if not blockers else "FAIL",
        "passed": not blockers,
        "blockers": blockers,
        "stale_artifacts": stale_artifacts,
        "stale_artifact_count": len(stale_artifacts),
        "current_draft_content_sha256": current_draft_hash,
        "map_recorded_draft_content_sha256": map_recorded_draft_hash,
        "draft_map_hash_matches": draft_map_hash_matches,
        "current_paragraph_map_sha256": current_map_hash,
        "packet_recorded_paragraph_map_sha256": packet_recorded_map_hash,
        "packet_map_hash_matches": packet_map_hash_matches,
    }


def render_paper_draft_edit_gate_markdown(gate: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Paper Draft Edit Gate",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Gate status | {gate.get('gate_status', 'FAIL')} |",
        f"| Draft-map hash matches | {bool(gate.get('draft_map_hash_matches', False))} |",
        f"| Packet-map hash matches | {bool(gate.get('packet_map_hash_matches', False))} |",
        f"| Stale artifact count | {int(gate.get('stale_artifact_count', 0) or 0)} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(gate.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Hash Chain",
            "",
            "| Link | Current | Recorded | Matches |",
            "|---|---|---|---:|",
            "| draft -> map | {current} | {recorded} | {matches} |".format(
                current=gate.get("current_draft_content_sha256", ""),
                recorded=gate.get("map_recorded_draft_content_sha256", ""),
                matches=bool(gate.get("draft_map_hash_matches", False)),
            ),
            "| map -> packets | {current} | {recorded} | {matches} |".format(
                current=gate.get("current_paragraph_map_sha256", ""),
                recorded=gate.get("packet_recorded_paragraph_map_sha256", ""),
                matches=bool(gate.get("packet_map_hash_matches", False)),
            ),
            "",
        ]
    )
    return "\n".join(lines)


def write_paper_draft_edit_gate(
    gate: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_paper_draft_edit_gate_markdown(gate), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")


def _draft_content_sha256(draft: Mapping[str, Any]) -> str:
    sections = [
        {
            "slot": str(section.get("slot", "")),
            "heading": str(section.get("heading", "")),
            "source_path": str(section.get("source_path", "")),
            "text": str(section.get("text", "")),
        }
        for section in _list_value(draft.get("sections"))
        if isinstance(section, Mapping)
    ]
    payload = {
        "paper_draft_status": str(draft.get("paper_draft_status", "")),
        "title": str(draft.get("title", "")),
        "sections": sections,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
        description="Check whether paper draft paragraph-map and packet artifacts are stale."
    )
    parser.add_argument("--draft", default=DEFAULT_DRAFT_PATH)
    parser.add_argument("--paragraph-map", default=DEFAULT_PARAGRAPH_MAP)
    parser.add_argument("--paragraph-packets", default=DEFAULT_PARAGRAPH_PACKETS)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    gate = build_paper_draft_edit_gate(
        draft_path=args.draft,
        paragraph_map_path=args.paragraph_map,
        paragraph_packets_path=args.paragraph_packets,
    )
    write_paper_draft_edit_gate(gate, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
