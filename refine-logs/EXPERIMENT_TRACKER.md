# Experiment Tracker

日期：2026-06-14

## 阶段状态

| 阶段 | 状态 | 说明 |
|---|---|---|
| Literature map | done | 已锁定 RAG poisoning、conflict RAG、Agent tool security、电网 Agent 四条文献线 |
| Problem reframing | done | 主问题改为 Evidence-to-Action Integrity |
| Math abstraction | done | 已定义 EAIR、conflict graph、action influence、gate condition |
| Benchmark design | done | 已定义 power-grid decision pollution benchmark |
| Implementation | done | 已实现本地 deterministic evidence-to-action pilot 模块 |
| Pilot experiments | done | 已跑 49 samples x 7 baselines，本地输出在 `outputs/evidence_action_pilot/` |
| Claim audit | in_progress | 已建立初版 claim-evidence matrix；实验结果已新增 `EXPERIMENT_RESULTS.md` |
| Citation audit | partial | 已使用 arXiv/OpenReview/official pages/GitHub，仍需最终论文前系统审计 |

## Implementation TODO

- [x] Define `action_schema` in case metadata.
- [x] Add mock retrieval node with ranked evidence variants.
- [x] Add claim extraction node or deterministic claim metadata loader.
- [x] Add conflict graph builder.
- [x] Add evidence-action guardrail.
- [x] Add structured action evaluator.
- [ ] Expand mock power cases to at least 30 cases.
- [ ] Add baseline configs.
- [ ] Add report tables for PRR/CDF1/UDR/UAR/EATF/CUR/ORR.

## Experiment TODO

- [x] Run deterministic smoke test with local simulator.
- [x] Run B1/B2/B3/B4/B5/B6/B7 on pilot data.
- [x] Inspect per-case traces.
- [ ] Tune `eta_risk`, `gamma_cred`, `gamma_pois`.
- [ ] Run ablations.
- [ ] Run at least one OpenAI-compatible model.
- [ ] Produce result tables and failure taxonomy.

## Paper TODO

- [ ] Convert proposal to LaTeX.
- [ ] Add formal threat model figure.
- [ ] Add Evidence-to-Action graph figure.
- [ ] Add benchmark table.
- [ ] Add results table and safety-utility curve.
- [ ] Run final paper-claim audit.
- [ ] Run final citation audit.
