from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence


DEFAULT_AUDIT_JSON = Path("docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json")
DEFAULT_PACKET_JSON = Path("docs/power_ops_afw_annotation_packet_2026-07-01.json")
DEFAULT_PACKET_JSONL = Path("docs/power_ops_afw_annotation_packet_2026-07-01.jsonl")
DEFAULT_SMOKE_A = Path("docs/power_ops_afw_annotation_smoke_annotator_a_2026-07-01.jsonl")
DEFAULT_SMOKE_B = Path("docs/power_ops_afw_annotation_smoke_annotator_b_2026-07-01.jsonl")
DEFAULT_AGREEMENT_JSON = Path("docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.json")
DEFAULT_AGREEMENT_MD = Path("docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.md")

REQUIRED_LABEL_FIELDS = [
    "security_category",
    "severity",
    "expected_behavior",
    "evaluation_standard",
]


def build_afw_annotation_packet(
    audit: dict[str, Any],
    *,
    packet_id: str = "power_ops_afw_annotation_packet",
) -> dict[str, Any]:
    """Build a double-annotation packet from a dataset annotation audit."""

    items = [_packet_item(item) for item in audit.get("items", [])]
    return {
        "artifact_type": "afw_annotation_packet",
        "inputs": audit.get("inputs", {}),
        "summary": {
            "packet_id": packet_id,
            "total_items": len(items),
            "required_label_fields": list(REQUIRED_LABEL_FIELDS),
            "human_annotation_status": "ready_for_double_annotation",
        },
        "instructions": {
            "format": "jsonl",
            "one_row_per_item": True,
            "required_fields": ["annotator_id", "item_id", *REQUIRED_LABEL_FIELDS, "notes"],
            "do_not_edit_fields": [
                "item_id",
                "sample_family",
                "source_type",
                "suggested_labels",
                "annotation_basis",
            ],
        },
        "items": items,
    }


def build_afw_annotation_agreement_report(
    *,
    annotator_a_path: str | Path,
    annotator_b_path: str | Path,
    packet: dict[str, Any] | None = None,
    threshold: float = 0.7,
    agreement_id: str = "power_ops_afw_annotation_agreement",
    agreement_source: str = "human_double_annotation",
) -> dict[str, Any]:
    """Compute field-level Cohen's Kappa for two annotation JSONL files."""

    annotator_a = _load_annotations(annotator_a_path)
    annotator_b = _load_annotations(annotator_b_path)
    paired_ids = sorted(set(annotator_a) & set(annotator_b))
    field_agreement = {
        field: _cohen_kappa([annotator_a[item_id][field] for item_id in paired_ids], [
            annotator_b[item_id][field] for item_id in paired_ids
        ])
        for field in REQUIRED_LABEL_FIELDS
    }
    kappas = [value["kappa"] for value in field_agreement.values()]
    min_kappa = min(kappas) if kappas else 0.0
    mean_kappa = sum(kappas) / len(kappas) if kappas else 0.0
    human_kappa_status = (
        "human_threshold_met"
        if agreement_source == "human_double_annotation" and min_kappa >= threshold
        else "human_threshold_not_met"
        if agreement_source == "human_double_annotation"
        else "not_human_double_annotation"
    )

    return {
        "artifact_type": "afw_annotation_agreement_report",
        "inputs": {
            "annotator_a_path": str(Path(annotator_a_path)),
            "annotator_b_path": str(Path(annotator_b_path)),
            "packet_id": (packet or {}).get("summary", {}).get("packet_id", ""),
        },
        "summary": {
            "agreement_id": agreement_id,
            "agreement_source": agreement_source,
            "paired_items": len(paired_ids),
            "missing_from_annotator_a": len(set(annotator_b) - set(annotator_a)),
            "missing_from_annotator_b": len(set(annotator_a) - set(annotator_b)),
            "threshold": threshold,
            "min_kappa": round(min_kappa, 6),
            "mean_kappa": round(mean_kappa, 6),
            "passes_threshold": min_kappa >= threshold,
            "human_kappa_status": human_kappa_status,
        },
        "field_agreement": field_agreement,
        "paired_item_ids": paired_ids,
    }


def render_afw_annotation_agreement_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AFW Annotation Agreement Report",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report["summary"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Field Agreement",
            "",
            "| Field | Items | Observed agreement | Expected agreement | Kappa |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for field, stats in report["field_agreement"].items():
        lines.append(
            "| {field} | {items} | {observed:.3f} | {expected:.3f} | {kappa:.3f} |".format(
                field=field,
                items=stats["items"],
                observed=stats["observed_agreement"],
                expected=stats["expected_agreement"],
                kappa=stats["kappa"],
            )
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This report may be generated from machine-prefilled smoke annotations. "
            "Only `agreement_source=human_double_annotation` should be used as evidence "
            "for the project Kappa target.",
            "",
        ]
    )
    return "\n".join(lines)


def write_afw_annotation_packet(
    audit_json_path: str | Path = DEFAULT_AUDIT_JSON,
    *,
    packet_json_path: str | Path = DEFAULT_PACKET_JSON,
    packet_jsonl_path: str | Path = DEFAULT_PACKET_JSONL,
    packet_id: str = "power_ops_afw_annotation_packet",
) -> dict[str, Any]:
    audit = json.loads(Path(audit_json_path).read_text(encoding="utf-8"))
    packet = build_afw_annotation_packet(audit, packet_id=packet_id)
    Path(packet_json_path).write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_packet_jsonl(packet, packet_jsonl_path)
    return packet


def write_afw_annotation_agreement_report(
    *,
    annotator_a_path: str | Path,
    annotator_b_path: str | Path,
    packet: dict[str, Any],
    markdown_path: str | Path = DEFAULT_AGREEMENT_MD,
    json_path: str | Path = DEFAULT_AGREEMENT_JSON,
    threshold: float = 0.7,
    agreement_id: str = "power_ops_afw_annotation_agreement_smoke",
    agreement_source: str = "machine_prefill_smoke_not_human",
) -> dict[str, Any]:
    report = build_afw_annotation_agreement_report(
        annotator_a_path=annotator_a_path,
        annotator_b_path=annotator_b_path,
        packet=packet,
        threshold=threshold,
        agreement_id=agreement_id,
        agreement_source=agreement_source,
    )
    Path(markdown_path).write_text(render_afw_annotation_agreement_markdown(report), encoding="utf-8")
    Path(json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def write_machine_prefill_smoke_annotations(
    packet: dict[str, Any],
    *,
    annotator_a_path: str | Path = DEFAULT_SMOKE_A,
    annotator_b_path: str | Path = DEFAULT_SMOKE_B,
) -> tuple[Path, Path]:
    _write_annotation_rows(packet, annotator_a_path, annotator_id="machine_prefill_a")
    _write_annotation_rows(packet, annotator_b_path, annotator_id="machine_prefill_b")
    return Path(annotator_a_path), Path(annotator_b_path)


def _packet_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": item["item_id"],
        "sample_family": item["sample_family"],
        "sample_origin": item["sample_origin"],
        "source_type": item["source_type"],
        "suggested_labels": {
            "security_category": item["security_category"],
            "severity": item["severity"],
            "expected_behavior": item["expected_behavior"],
            "evaluation_standard": item["evaluation_standard"],
        },
        "human_labels": {
            "security_category": "",
            "severity": "",
            "expected_behavior": "",
            "evaluation_standard": "",
            "notes": "",
        },
        "annotation_basis": item.get("annotation_basis", {}),
    }


def _load_annotations(path: str | Path) -> dict[str, dict[str, str]]:
    annotations: dict[str, dict[str, str]] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        item_id = str(row["item_id"])
        annotations[item_id] = {field: str(row.get(field, "")) for field in REQUIRED_LABEL_FIELDS}
    return annotations


def _cohen_kappa(labels_a: list[str], labels_b: list[str]) -> dict[str, Any]:
    if len(labels_a) != len(labels_b):
        raise ValueError("Annotation lists must have the same length.")
    if not labels_a:
        return {"items": 0, "observed_agreement": 0.0, "expected_agreement": 0.0, "kappa": 0.0}

    total = len(labels_a)
    observed = sum(1 for left, right in zip(labels_a, labels_b) if left == right) / total
    categories = sorted(set(labels_a) | set(labels_b))
    expected = sum(
        (labels_a.count(category) / total) * (labels_b.count(category) / total)
        for category in categories
    )
    if expected == 1.0:
        kappa = 1.0 if observed == 1.0 else 0.0
    else:
        kappa = (observed - expected) / (1.0 - expected)
    return {
        "items": total,
        "observed_agreement": round(observed, 6),
        "expected_agreement": round(expected, 6),
        "kappa": round(kappa, 6),
    }


def _write_packet_jsonl(packet: dict[str, Any], path: str | Path) -> None:
    rows = [json.dumps(item, ensure_ascii=False) for item in packet["items"]]
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")


def _write_annotation_rows(packet: dict[str, Any], path: str | Path, *, annotator_id: str) -> None:
    rows = []
    for item in packet["items"]:
        labels = item["suggested_labels"]
        rows.append(
            json.dumps(
                {
                    "annotator_id": annotator_id,
                    "item_id": item["item_id"],
                    "security_category": labels["security_category"],
                    "severity": labels["severity"],
                    "expected_behavior": labels["expected_behavior"],
                    "evaluation_standard": labels["evaluation_standard"],
                    "notes": "machine-prefill smoke fixture; not a human label",
                },
                ensure_ascii=False,
            )
        )
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build AFW annotation packets and agreement reports.")
    parser.add_argument("--audit-json", default=str(DEFAULT_AUDIT_JSON))
    parser.add_argument("--packet-json", default=str(DEFAULT_PACKET_JSON))
    parser.add_argument("--packet-jsonl", default=str(DEFAULT_PACKET_JSONL))
    parser.add_argument("--packet-id", default="power_ops_afw_annotation_packet")
    parser.add_argument("--annotator-a")
    parser.add_argument("--annotator-b")
    parser.add_argument("--write-smoke-annotations", action="store_true")
    parser.add_argument("--smoke-annotator-a", default=str(DEFAULT_SMOKE_A))
    parser.add_argument("--smoke-annotator-b", default=str(DEFAULT_SMOKE_B))
    parser.add_argument("--agreement-md", default=str(DEFAULT_AGREEMENT_MD))
    parser.add_argument("--agreement-json", default=str(DEFAULT_AGREEMENT_JSON))
    parser.add_argument("--threshold", type=float, default=0.7)
    args = parser.parse_args(argv)

    packet = write_afw_annotation_packet(
        args.audit_json,
        packet_json_path=args.packet_json,
        packet_jsonl_path=args.packet_jsonl,
        packet_id=args.packet_id,
    )

    annotator_a = args.annotator_a
    annotator_b = args.annotator_b
    agreement_source = "human_double_annotation"
    agreement_id = "power_ops_afw_annotation_agreement"
    if args.write_smoke_annotations:
        smoke_a, smoke_b = write_machine_prefill_smoke_annotations(
            packet,
            annotator_a_path=args.smoke_annotator_a,
            annotator_b_path=args.smoke_annotator_b,
        )
        annotator_a = str(smoke_a)
        annotator_b = str(smoke_b)
        agreement_source = "machine_prefill_smoke_not_human"
        agreement_id = "power_ops_afw_annotation_agreement_smoke"

    output: dict[str, Any] = {
        "packet_json": str(Path(args.packet_json)),
        "packet_jsonl": str(Path(args.packet_jsonl)),
        "total_items": packet["summary"]["total_items"],
    }
    if annotator_a and annotator_b:
        report = write_afw_annotation_agreement_report(
            annotator_a_path=annotator_a,
            annotator_b_path=annotator_b,
            packet=packet,
            markdown_path=args.agreement_md,
            json_path=args.agreement_json,
            threshold=args.threshold,
            agreement_id=agreement_id,
            agreement_source=agreement_source,
        )
        output.update(
            {
                "agreement_md": str(Path(args.agreement_md)),
                "agreement_json": str(Path(args.agreement_json)),
                "min_kappa": report["summary"]["min_kappa"],
                "human_kappa_status": report["summary"]["human_kappa_status"],
            }
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
