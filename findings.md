# RAG 投毒重点调研发现

本文件记录本次调研中的关键论文、项目和电网结合点。

## 近半年 RAG 投毒/检索安全论文
- SilentRetrieval（2026-05）：语义保持的隐蔽数据投毒，强调污染文档可保持流畅性和可检索性。
- PIDP-Attack（2026-03）：将提示注入和数据库投毒组合，不要求预先知道用户真实查询。
- AdversarialCoT（2026-04）：单文档检索投毒，利用目标模型推理框架构造对抗 CoT，直接打击推理链路。
- Hidden-in-Plain-Text / OpenRAG-Soc（2026-01）：面向社交 Web 载体的间接提示注入与检索投毒 benchmark。
- FilterRAG / ML-FilterRAG（2026-03 修订）：从检索数据源中过滤对抗文本，属于防御方向。

## 电网/电力 Agent 近半年相关项目与论文
- X-GridAgent（2025-12）：三层架构，包含 schema-adaptive hybrid RAG，用于大规模结构化电网数据检索。
- Grid-Mind（2026-02）：面向连接影响评估，LLM 调度 11 类工具并用仿真输出做 grounding validation。
- PowerDAG（2026-03/04）：配电网分析 Agent，使用 adaptive retrieval 和 JIT supervision 提升可靠性。
- Grid-Orch（2026-05）：通过 MCP 连接 OpenDSS，36 个领域工具，支持隔离环境中的电网仿真分析。
- PowerAgent（Harvard SEAS）：电力系统 Agentic AI 开源社区，包含 PowerFM、PowerMCP、PowerWF、PowerSkills 等方向。

## 初步判断
- RAG 投毒最适合解释为 S2 外部知识检索/记忆读取阶段的知识完整性风险，并向 S3 推理、S4 计划、S5 工具调用、S6 输出传播。
- 电网场景中，风险重点不是“说错一句话”，而是污染文档进入上下文后，让运维辅助建议、仿真工具选择、参数设置或报告结论看似有证据但实际不可靠。

## 优质工具/项目线索
- SafeRAG：RAG 安全 benchmark，覆盖索引、检索、过滤、生成多阶段攻击。
- garak：LLM 漏洞扫描/红队工具，可用于 prompt injection、泄露等安全探测。
- NeMo Guardrails：支持 input/dialog/retrieval/execution/output rails，retrieval rails 可拒绝或改写 RAG 检索片段。
- LlamaIndex/LangSmith/RAGAS：用于 RAG 检索质量、faithfulness、context precision/recall、端到端质量评估。
- PowerAgent：电力系统 Agentic AI 开源社区，方向包括 PowerMCP、PowerWF、PowerSkills，可作为电网 Agent 生态背景。
