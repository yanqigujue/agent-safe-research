# AFW Requirement Coverage Matrix

## Sources

| Source | Value |
|---|---|
| screenshot | electric power equipment operations RAG QA production scene |
| pdf | 实施方案_v2.0(1).pdf |

## Summary

| Status | Count |
|---|---:|
| supported | 4 |
| partial | 6 |
| missing | 0 |

## Requirements

| ID | Requirement | Status | Evidence | Note |
|---|---|---|---|---|
| REQ-FORMAL-MODEL | 形式化建模 | supported | docs/power_ops_afw_formal_model_2026-07-01.md<br>docs/action_field_authority_warrant_calculus_2026-07-01.md<br>docs/power_ops_afw_trace_adapter_formal_mapping_2026-07-01.md | PDF要求TCE/FormalTrust形式化建模；AFW补充字段授权形式化切片。 |
| REQ-TEST-FRAMEWORK | 插件式测评/攻击测试框架 | supported | docs/power_ops_afw_test_framework_2026-07-01.md<br>formaltrust_platform/nodes/afw.py<br>formaltrust_platform/experiments/afw_runtime_suite.py<br>tests/test_afw_bench.py | PDF要求插件式攻击测试框架；当前已有FormalTrust节点、runtime evaluator、trace adapter和suite runner。 |
| REQ-POWER-RAG-SCENE | 电力设备运维知识库RAG问答场景 | supported | docs/power_ops_afw_test_samples_2026-07-01.md<br>examples/afw_power_ops_rag_rows.json<br>examples/afw_power_ops_trace_scenarios.json | 截图要求上传设备手册/规程、检索片段、rerank、生成回答；当前AFW样本覆盖该RAG场景中的字段授权洗白风险。 |
| REQ-K1-BEHMATCH-80 | 安全攸关行为一致率>=80% | supported | docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json<br>docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md | PDF要求安全相关行为一致率>=80%；当前AFW all-config runtime suite在字段授权切片上达到mean_afw_behmatch=1.0。 |
| REQ-POWER-ATTACK-TAXONOMY | 电力专项攻击分类 | partial | examples/afw_boundary_role_rows.json<br>examples/afw_power_ops_rag_rows.json<br>docs/power_ops_afw_coverage_matrix_2026-07-01.md | PDF列出领域混淆、权限伪造、术语误用、规程规避、RAG中毒等专项攻击；当前AFW覆盖字段授权洗白相关子集。 |
| REQ-DATASET-CONSTRUCTION | 测试数据集建设 | partial | docs/power_ops_afw_test_samples_2026-07-01.md<br>docs/power_ops_afw_dataset_annotation_audit_2026-07-01.md<br>docs/power_ops_afw_dataset_annotation_audit_2026-07-01.json<br>docs/power_ops_afw_annotation_packet_2026-07-01.json<br>docs/power_ops_afw_annotation_packet_2026-07-01.jsonl<br>docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.md<br>docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.json<br>examples/afw_power_ops_rag_rows.json<br>examples/data/afw_runtime_power_ops_cases.jsonl | PDF规划通用安全集+自建电力集，并要求四要素标注和Kappa>=0.7；当前已有AFW专项子集，尚非完整1050/800/700规模数据集。 |
| REQ-DEFENSE-CLOSED-LOOP | 测评-定位-防护-再测评闭环 | partial | formaltrust_platform/nodes/afw.py<br>examples/afw_runtime_validation.yaml<br>docs/power_ops_afw_current_results_2026-07-01.md<br>docs/power_ops_afw_defense_loop_report_2026-07-01.md<br>docs/power_ops_afw_defense_loop_report_2026-07-01.json | PDF要求轻量防护与闭环验证；当前CapGuard可将未授权字段改写为human approval并进入runtime evaluator，但尚未完成完整防护前后大基准实验。 |
| REQ-K2-K3-K4-PROJECT-METRICS | K2/K3/K4项目级指标 | partial | docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.json<br>docs/power_ops_afw_defense_loop_report_2026-07-01.json<br>docs/action_field_authority_warrant_claim_firewall_2026-07-01.md | PDF要求风险发掘提升>=10%、安全问题降低>=20%、通用能力下降<=10%；当前报告有AFW-subset proxy，尚非项目全量指标。 |
| REQ-PRODUCTION-DEPLOYMENT | 生产部署与多模型链路 | partial | examples/afw_power_ops_production_chain.yaml<br>docs/power_ops_afw_production_chain_report_2026-07-01.md<br>docs/power_ops_afw_production_chain_report_2026-07-01.json<br>examples/afw_trace_adapter_otlp_runtime_validation.yaml<br>examples/afw_trace_adapter_otlp_envelope_runtime_validation.yaml<br>docs/power_ops_afw_implementation_scheme_2026-07-01.md | 截图强调embedding、generation、rerank多模型链路和生产显存/API约束；当前AFW验证了运行时trace与字段授权，尚未接真实embedding/rerank/generation服务。 |
| REQ-FINAL-DELIVERABLES | 技术报告、原型系统、论文、专利、软著 | partial | docs/power_ops_afw_deliverables_index_2026-07-01.md<br>docs/action_field_authority_warrant_research_summary_2026-07-01.md<br>docs/action_field_authority_warrant_claim_firewall_2026-07-01.md | PDF列出最终交付物；当前AFW已有研究文档、可运行原型切片和论文材料，尚非完整结题交付包。 |
