from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence


def build_afw_requirement_coverage(root: str | Path = Path(".")) -> dict[str, Any]:
    """Map implementation-plan requirements to current AFW artifacts."""

    repo = Path(root)
    suite_metrics = _load_all_config_suite_metrics(repo)
    dataset_audit_metrics = _load_dataset_audit_metrics(repo)
    annotation_packet_metrics = _load_annotation_packet_metrics(repo)
    annotation_agreement_metrics = _load_annotation_agreement_metrics(repo)
    defense_loop_metrics = _load_defense_loop_metrics(repo)
    production_chain_metrics = _load_production_chain_metrics(repo)
    production_replay_metrics = _load_production_replay_metrics(repo)
    requirements = [
        _requirement(
            repo,
            "REQ-FORMAL-MODEL",
            "形式化建模",
            "PDF要求TCE/FormalTrust形式化建模；AFW补充字段授权形式化切片。",
            "supported",
            [
                "docs/power_ops_afw_formal_model_2026-07-01.md",
                "docs/action_field_authority_warrant_calculus_2026-07-01.md",
                "docs/power_ops_afw_trace_adapter_formal_mapping_2026-07-01.md",
            ],
        ),
        _requirement(
            repo,
            "REQ-TEST-FRAMEWORK",
            "插件式测评/攻击测试框架",
            "PDF要求插件式攻击测试框架；当前已有FormalTrust节点、runtime evaluator、trace adapter和suite runner。",
            "supported",
            [
                "docs/power_ops_afw_test_framework_2026-07-01.md",
                "formaltrust_platform/nodes/afw.py",
                "formaltrust_platform/experiments/afw_runtime_suite.py",
                "tests/test_afw_bench.py",
            ],
        ),
        _requirement(
            repo,
            "REQ-POWER-RAG-SCENE",
            "电力设备运维知识库RAG问答场景",
            "截图要求上传设备手册/规程、检索片段、rerank、生成回答；当前AFW样本覆盖该RAG场景中的字段授权洗白风险。",
            "supported",
            [
                "docs/power_ops_afw_test_samples_2026-07-01.md",
                "examples/afw_power_ops_rag_rows.json",
                "examples/afw_power_ops_trace_scenarios.json",
            ],
        ),
        _requirement(
            repo,
            "REQ-K1-BEHMATCH-80",
            "安全攸关行为一致率>=80%",
            "PDF要求安全相关行为一致率>=80%；当前AFW all-config runtime suite在字段授权切片上达到mean_afw_behmatch=1.0。",
            "supported" if suite_metrics.get("mean_afw_behmatch", 0.0) >= 0.8 else "partial",
            [
                "docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json",
                "docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md",
            ],
            metric_evidence={
                "mean_afw_behmatch": suite_metrics.get("mean_afw_behmatch", 0.0),
                "total_cases": suite_metrics.get("total_cases", 0),
                "passed_cases": suite_metrics.get("passed_cases", 0),
            },
        ),
        _requirement(
            repo,
            "REQ-POWER-ATTACK-TAXONOMY",
            "电力专项攻击分类",
            "PDF列出领域混淆、权限伪造、术语误用、规程规避、RAG中毒等专项攻击；当前AFW覆盖字段授权洗白相关子集。",
            "partial",
            [
                "examples/afw_boundary_role_rows.json",
                "examples/afw_power_ops_rag_rows.json",
                "docs/power_ops_afw_coverage_matrix_2026-07-01.md",
            ],
        ),
        _requirement(
            repo,
            "REQ-DATASET-CONSTRUCTION",
            "测试数据集建设",
            "PDF规划通用安全集+自建电力集，并要求四要素标注和Kappa>=0.7；当前已有AFW专项子集，尚非完整1050/800/700规模数据集。",
            "partial",
            [
                "docs/power_ops_afw_test_samples_2026-07-01.md",
                "docs/power_ops_afw_dataset_annotation_audit_2026-07-01.md",
                "docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json",
                "docs/power_ops_afw_annotation_packet_2026-07-01.json",
                "docs/power_ops_afw_annotation_packet_2026-07-01.jsonl",
                "docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.md",
                "docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.json",
                "examples/afw_power_ops_rag_rows.json",
                "examples/data/afw_runtime_power_ops_cases.jsonl",
            ],
            metric_evidence={
                "total_audited_items": dataset_audit_metrics.get("total_audited_items", 0),
                "fully_labeled_items": dataset_audit_metrics.get("fully_labeled_items", 0),
                "kappa_status": dataset_audit_metrics.get("kappa_status", "missing"),
                "dataset_scale_status": dataset_audit_metrics.get("dataset_scale_status", "missing"),
                "annotation_packet_items": annotation_packet_metrics.get("total_items", 0),
                "agreement_smoke_min_kappa": annotation_agreement_metrics.get("min_kappa", 0.0),
                "human_kappa_status": annotation_agreement_metrics.get(
                    "human_kappa_status",
                    "missing",
                ),
            },
        ),
        _requirement(
            repo,
            "REQ-DEFENSE-CLOSED-LOOP",
            "测评-定位-防护-再测评闭环",
            "PDF要求轻量防护与闭环验证；当前CapGuard可将未授权字段改写为human approval并进入runtime evaluator，但尚未完成完整防护前后大基准实验。",
            "partial",
            [
                "formaltrust_platform/nodes/afw.py",
                "examples/afw_runtime_validation.yaml",
                "docs/power_ops_afw_current_results_2026-07-01.md",
                "docs/power_ops_afw_defense_loop_report_2026-07-01.md",
                "docs/power_ops_afw_defense_loop_report_2026-07-01.json",
            ],
            metric_evidence={
                "k2_min_risk_discovery_lift": defense_loop_metrics.get(
                    "k2_min_risk_discovery_lift",
                    0.0,
                ),
                "k3_min_safety_issue_reduction": defense_loop_metrics.get(
                    "k3_min_safety_issue_reduction",
                    0.0,
                ),
                "k4_utility_preservation": defense_loop_metrics.get(
                    "k4_utility_preservation",
                    0.0,
                ),
                "general_ability_drop": defense_loop_metrics.get("general_ability_drop", 0.0),
                "passes_proxy_gates": defense_loop_metrics.get("passes_proxy_gates", False),
                "claim_scope": defense_loop_metrics.get("claim_scope", "missing"),
            },
        ),
        _requirement(
            repo,
            "REQ-K2-K3-K4-PROJECT-METRICS",
            "K2/K3/K4项目级指标",
            "PDF要求风险发掘提升>=10%、安全问题降低>=20%、通用能力下降<=10%；当前报告有AFW-subset proxy，尚非项目全量指标。",
            "partial",
            [
                "docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json",
                "docs/power_ops_afw_defense_loop_report_2026-07-01.json",
                "docs/action_field_authority_warrant_claim_firewall_2026-07-01.md",
            ],
            metric_evidence={
                "false_allow_fields": suite_metrics.get("field_counts", {}).get("false_allow_fields", 0),
                "false_block_fields": suite_metrics.get("field_counts", {}).get("false_block_fields", 0),
                "prevented_fields": suite_metrics.get("field_counts", {}).get("prevented_fields", 0),
                "k2_min_risk_discovery_lift": defense_loop_metrics.get(
                    "k2_min_risk_discovery_lift",
                    0.0,
                ),
                "k3_min_safety_issue_reduction": defense_loop_metrics.get(
                    "k3_min_safety_issue_reduction",
                    0.0,
                ),
                "k4_utility_preservation": defense_loop_metrics.get(
                    "k4_utility_preservation",
                    0.0,
                ),
            },
        ),
        _requirement(
            repo,
            "REQ-PRODUCTION-DEPLOYMENT",
            "生产部署与多模型链路",
            "截图强调embedding、generation、rerank多模型链路和生产显存/API约束；当前AFW验证了运行时trace与字段授权，尚未接真实embedding/rerank/generation服务。",
            "partial",
            [
                "examples/afw_power_ops_production_chain.yaml",
                "docs/power_ops_afw_production_chain_report_2026-07-01.md",
                "docs/power_ops_afw_production_chain_report_2026-07-01.json",
                "examples/afw_production_chain_replay_validation.yaml",
                "examples/data/afw_production_chain_replay_cases.jsonl",
                "docs/power_ops_afw_production_replay_report_2026-07-01.md",
                "docs/power_ops_afw_production_replay_report_2026-07-01.json",
                "examples/afw_trace_adapter_otlp_runtime_validation.yaml",
                "examples/afw_trace_adapter_otlp_envelope_runtime_validation.yaml",
                "docs/power_ops_afw_implementation_scheme_2026-07-01.md",
            ],
            metric_evidence={
                "required_model_roles_covered": production_chain_metrics.get(
                    "required_model_roles_covered",
                    False,
                ),
                "rag_flow_contains_guardrail": production_chain_metrics.get(
                    "rag_flow_contains_guardrail",
                    False,
                ),
                "memory_budget_passes": production_chain_metrics.get("memory_budget_passes", False),
                "api_compatibility_passes": production_chain_metrics.get(
                    "api_compatibility_passes",
                    False,
                ),
                "production_readiness_status": production_chain_metrics.get(
                    "production_readiness_status",
                    "missing",
                ),
                "production_replay_cases": production_replay_metrics.get("replay_cases", 0),
                "production_replay_legal_allow_cases": production_replay_metrics.get(
                    "legal_allow_cases",
                    0,
                ),
                "production_replay_laundering_block_cases": production_replay_metrics.get(
                    "laundering_block_cases",
                    0,
                ),
                "production_replay_claim_scope": production_replay_metrics.get(
                    "claim_scope",
                    "missing",
                ),
            },
        ),
        _requirement(
            repo,
            "REQ-FINAL-DELIVERABLES",
            "技术报告、原型系统、论文、专利、软著",
            "PDF列出最终交付物；当前AFW已有研究文档、可运行原型切片和论文材料，尚非完整结题交付包。",
            "partial",
            [
                "docs/power_ops_afw_deliverables_index_2026-07-01.md",
                "docs/action_field_authority_warrant_research_summary_2026-07-01.md",
                "docs/action_field_authority_warrant_claim_firewall_2026-07-01.md",
            ],
        ),
    ]
    summary = {
        "total_requirements": len(requirements),
        "supported": sum(1 for item in requirements if item["status"] == "supported"),
        "partial": sum(1 for item in requirements if item["status"] == "partial"),
        "missing": sum(1 for item in requirements if item["status"] == "missing"),
    }
    return {
        "artifact_type": "afw_requirement_coverage",
        "source_inputs": {
            "screenshot": "electric power equipment operations RAG QA production scene",
            "pdf": "实施方案_v2.0(1).pdf",
        },
        "summary": summary,
        "requirements": requirements,
    }


def render_afw_requirement_coverage_markdown(coverage: dict[str, Any]) -> str:
    lines = [
        "# AFW Requirement Coverage Matrix",
        "",
        "## Sources",
        "",
        "| Source | Value |",
        "|---|---|",
    ]
    for key, value in coverage["source_inputs"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Status | Count |",
            "|---|---:|",
        ]
    )
    for key in ("supported", "partial", "missing"):
        lines.append(f"| {key} | {coverage['summary'][key]} |")

    lines.extend(
        [
            "",
            "## Requirements",
            "",
            "| ID | Requirement | Status | Evidence | Note |",
            "|---|---|---|---|---|",
        ]
    )
    for item in coverage["requirements"]:
        evidence = "<br>".join(item["evidence_paths"])
        lines.append(
            f"| {item['id']} | {item['requirement']} | {item['status']} | {evidence} | {item['note']} |"
        )

    lines.append("")
    return "\n".join(lines)


def write_afw_requirement_coverage(
    root: str | Path = Path("."),
    *,
    markdown_path: str | Path,
    json_path: str | Path,
) -> dict[str, Any]:
    coverage = build_afw_requirement_coverage(root)
    Path(markdown_path).write_text(render_afw_requirement_coverage_markdown(coverage), encoding="utf-8")
    Path(json_path).write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    return coverage


def _requirement(
    repo: Path,
    requirement_id: str,
    requirement: str,
    note: str,
    status: str,
    evidence_paths: list[str],
    *,
    metric_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    existing = [path for path in evidence_paths if (repo / path).exists()]
    effective_status = status
    if not existing:
        effective_status = "missing"
    return {
        "id": requirement_id,
        "requirement": requirement,
        "note": note,
        "status": effective_status,
        "evidence_paths": evidence_paths,
        "existing_evidence_paths": existing,
        "missing_evidence_paths": [path for path in evidence_paths if path not in existing],
        "metric_evidence": metric_evidence or {},
    }


def _load_all_config_suite_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_dataset_audit_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return dict(payload.get("summary", {}))


def _load_annotation_packet_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_annotation_packet_2026-07-01.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return dict(payload.get("summary", {}))


def _load_annotation_agreement_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return dict(payload.get("summary", {}))


def _load_defense_loop_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_defense_loop_report_2026-07-01.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return dict(payload.get("summary", {}))


def _load_production_chain_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_production_chain_report_2026-07-01.json"
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return dict(payload.get("summary", {}))

    manifest_path = repo / "examples/afw_power_ops_production_chain.yaml"
    if not manifest_path.exists():
        return {}

    from formaltrust_platform.experiments.afw_production_chain import (
        build_afw_production_chain_report,
    )

    report = build_afw_production_chain_report(manifest_path)
    return dict(report.get("summary", {}))


def _load_production_replay_metrics(repo: Path) -> dict[str, Any]:
    path = repo / "docs/power_ops_afw_production_replay_report_2026-07-01.json"
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return dict(payload.get("summary", {}))

    manifest_path = repo / "examples/afw_power_ops_production_chain.yaml"
    if not manifest_path.exists():
        return {}

    from formaltrust_platform.experiments.afw_production_replay import (
        build_afw_production_replay_report,
    )

    report = build_afw_production_replay_report(manifest_path)
    return dict(report.get("summary", {}))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write AFW requirement coverage reports.")
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--markdown",
        default="docs/power_ops_afw_requirement_coverage_2026-07-01.md",
    )
    parser.add_argument(
        "--json",
        default="docs/power_ops_afw_requirement_coverage_2026-07-01.json",
    )
    args = parser.parse_args(argv)
    coverage = write_afw_requirement_coverage(
        args.root,
        markdown_path=args.markdown,
        json_path=args.json,
    )
    print(json.dumps(coverage["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
