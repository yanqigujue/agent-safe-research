# Review Summary

日期：2026-06-14

说明：当前环境未暴露外部 reviewer backend，因此本文件是基于文献证据和自审标准形成的内部审查摘要。正式写论文前应再运行独立 citation audit、claim audit 和最好一次外部模型/同行审阅。

## Strong Points

1. 问题重构清晰：从 answer poisoning 转向 retrieval-to-action pollution。
2. 三条方向被统一到一个可计算对象：Evidence-to-Action Integrity Risk。
3. 与 FormalTrust 框架贴合，能落到 state、retrieval_context、metrics、guardrail、evaluator。
4. 电网 Agent 场景具体，有审批、仿真、工具、报告和参数等自然 oracle。
5. 指标不是单一 pass/fail，而是覆盖 retrieval、evidence、action、auditability、utility。

## Likely Reviewer Questions

Q1：这和 RAG poisoning defense 有什么不同？

回答要点：本文不是仅过滤污染文档，而是评估污染证据是否影响高风险动作；成功指标是 action/tool/parameter/approval/report pollution。

Q2：这和 ConflictRAG 有什么不同？

回答要点：ConflictRAG 关注冲突检测和解决，本文关注冲突 claim 是否支撑或阻断动作，并引入 action-level safety metrics。

Q3：这和 SEAgent/AgentDojo/ToolHijacker 有什么不同？

回答要点：已有 agent 安全主要看 prompt/tool 权限和工具选择攻击；本文增加 evidence support constraint，即工具权限通过仍不等于动作证据充分。

Q4：电网 benchmark 是否太小/太假？

回答要点：需要分两阶段：pilot mock benchmark 验证机制，强版本接入 pandapower/OpenDSS/PowerMCP 的只读仿真 oracle。

Q5：Evidence trace 是否可信？

回答要点：不能只信 LLM rationale；需要结构化 claim metadata、外部 conflict detector、规则/仿真 oracle 和 replayable trace。

Q6：Gate 是否过度拒绝？

回答要点：必须报告 clean utility retention、over-refusal rate 和 threshold sweep。

## Critical Risks

1. novelty 过度表述：不能轻易说 first，除非最终 citation audit 完成。
2. 实验只有 mock：会降低投稿层级。
3. 只靠 LLM judge：可信度不足。
4. 数学函数没有实验估计：会显得只是 conceptual framework。
5. 电网领域约束不够真实：会被能源领域 reviewer 挑战。

## Recommended Refinements

1. 在实现时强制结构化 action JSON，避免自然语言 evaluator。
2. 每个 case 都要有 oracle metadata。
3. 至少一组实验加入 deterministic domain oracle。
4. 把 `tau`、`rho`、`p_pois` 作为可控变量做 sensitivity analysis。
5. 把 tool-doc poisoning 单独作为强 case study，因为它连接 RAG 安全和 Agent 工具安全。
6. 写论文时把“动作边界外部门控”作为核心安全原则。

## Go / No-Go

Go 条件：

- pilot 能显示 B6/B7 在 mixed/conflict/tool-doc conditions 下 UDR/UAR 明显低于 B1-B4；
- clean utility retention 不严重下降；
- failure analysis 能说明各模块贡献。

No-Go 条件：

- 方法主要靠 prompt，外部 gate 不起作用；
- benchmark 不能稳定区分 safe vs unsafe action；
- 结果只有文本层指标，没有 action-level 指标；
- 与现有 conflict/tool security work 的差异说不清。

