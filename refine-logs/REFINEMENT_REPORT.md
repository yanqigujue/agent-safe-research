# Refinement Report

日期：2026-06-14

## 初始问题

用户希望研究三个方向：

1. 检索命中劫持；
2. 证据冲突判断；
3. 工具/决策污染。

并要求：

- 有创新点；
- 有创新性解决办法；
- 能抽象为数学表示；
- 可信度高；
- 深度足以写论文。

## 关键重构

最初三个方向如果分开做，会分别落入已有拥挤领域：

- RAG poisoning；
- conflict-aware RAG；
- Agent prompt injection / tool security。

重构后，主问题变为：

> 检索证据的完整性如何影响安全关键 Agent 的最终动作？

这形成一个统一研究对象：

```text
Evidence-to-Action Integrity
```

## 为什么这比单点方向更强

单独做 retrieval hit hijacking：

- novelty 中等偏低；
- 容易被 PoisonedRAG/SilentRetrieval/AuthChain 比较。

单独做 conflict judgment：

- novelty 中等；
- 容易被 ConflictRAG/DRAGged/CLEAR 比较。

单独做 tool pollution：

- novelty 中等；
- 容易被 ToolHijacker/SEAgent/AgentDojo 比较。

合起来做 evidence-to-action：

- 研究对象更贴近安全关键 Agent；
- 可解释为什么三类已有工作各自不足；
- 与 FormalTrust 状态流天然契合；
- 能提出新的 action-level benchmark 和指标。

## 最终推荐方向

1. 主方向：Evidence-to-Action Integrity Graph and Gate。
2. 配套 benchmark：Power-Grid Decision Pollution Benchmark。
3. 技术增强：Conflict-Aware / Action-Sensitive Robust Retrieval。

## 产物文件

- `docs/rag_agent_research_directions.md`：方向判断与文献定位。
- `DERIVATION_PACKAGE.md`：数学抽象与指标。
- `refine-logs/FINAL_PROPOSAL.md`：论文级 proposal。
- `refine-logs/EXPERIMENT_PLAN.md`：实验计划。
- `refine-logs/EXPERIMENT_TRACKER.md`：执行 tracker。
- `PAPER_PLAN.md`：论文结构。
- `refine-logs/CLAIM_EVIDENCE_AUDIT.md`：主张-证据审计。
- `refine-logs/REVIEW_SUMMARY.md`：内部审查与风险。

## 下一步建议

第一周：

- 实现 mock retrieval + structured action evaluator；
- 扩展 30 个 case；
- 跑 B1/B2/B4/B6。

第二周：

- 加 ablation；
- 接入一个真实 LLM；
- 写 main result tables。

第三周：

- 接入轻量仿真 oracle；
- 补 failure analysis；
- 开始 LaTeX 初稿。

