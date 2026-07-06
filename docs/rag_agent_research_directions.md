# RAG-Agent 研究方向深度判断

## 2026-06-17 Active Direction Update

The active direction has shifted from broad "RAG poisoning + action pollution" to:

```text
EAIR-Bench + Evidence Sufficiency + Legitimate-vs-Hijack Evidence Influence
```

The central research question is:

> When should retrieved evidence be allowed to influence high-risk RAG-agent actions?

The current system evidence supports a narrower and cleaner claim:

- Retrieval exposure is not the same as action harm.
- Claim support is not enough when action parameters, tools, approvals, or source diversity fail.
- Evidence influence is not inherently malicious; the key distinction is legitimate, sufficient support versus hijack influence.
- Source-cluster saturation is necessary because near-duplicate documents from one source can make support look stronger than it is.
- Version-currentness is a separate sufficiency axis: fresh and trusted evidence can still be invalid if a trusted newer document supersedes its version.
- Claim extraction noise must be modeled explicitly: false negatives can remove required support claims and harm utility, while false positives can inject unsafe claims that create dangerous candidate actions.
- Retrieval perturbation must be modeled separately from claim extraction noise: top-k truncation, rank dropping, or seeded shuffling changes the evidence set before claims are read.
- Compounded robustness runs should preserve the action evaluator while adding normalized outcome summaries for retrieval-noise x claim-noise graphs.
- Robustness sweeps should export artifact-backed outcome distributions with Wilson 95% pass-rate intervals and support seed-grid expansion so graph-level perturbation results can scale beyond one-off checks.
- Case-level robustness reports should aggregate replayable perturbation outcomes across multiple benchmark conditions, support selector-driven benchmark slices, group them by benchmark case type, include Wilson 95% pass-rate intervals, gate declared coverage requirements, and export both machine-readable JSON/CSV and paper-facing Markdown summaries.

Use EAIR-Bench as the primary contribution, with EAIR-Full as the reference guardrail implementation.

日期：2026-06-14

面向框架：FormalTrust MVP

面向领域：电网知识问答、运行辅助、检修/审批/仿真类 Agent

## 一句话结论

最值得研究的不是单独的“RAG 投毒”或单独的“冲突检测”，而是：

**安全关键 RAG Agent 的 Evidence-to-Action Integrity：检索到的证据如何经过冲突判断、计划推理和工具选择，最终污染一个高风险动作。**

这个主题可以自然覆盖用户关心的三个方向：

1. **检索命中劫持**：攻击者让污染文档稳定进入 Top-K。
2. **证据冲突判断**：系统面对可信证据、污染证据、过期证据和模型先验冲突时，是否能识别、分型、拒绝或升级。
3. **工具/决策污染**：污染证据不只是改变文字答案，而是改变工具选择、参数设置、审批结论或电网操作建议。

## 推荐排序

### 第一优先级：Evidence-to-Action Integrity Graph

研究问题：

> 对安全关键 RAG Agent，能否检测并约束“低完整性证据影响高风险动作”的路径？

为什么最值得做：

- RAG 安全文献已经大量研究“污染文档是否进入检索”和“答案是否被改写”，但多数工作停在生成答案层。
- 冲突 RAG 文献关注“如何回答矛盾证据”，但通常不追踪矛盾证据是否改变工具调用或操作建议。
- Agent 安全文献关注 prompt injection、tool selection 和权限，但通常不把每个 tool call 绑定到可审计的证据支持链。
- 电网 Agent 的真实风险不是“说错一句话”，而是“基于似是而非的证据作出错误动作或错误报告结论”。

核心创新：

- 建立 `document -> claim -> conflict -> plan step -> tool/action` 的完整影响图。
- 用可计算风险函数刻画低信任、过期、冲突或疑似污染证据对高风险动作的贡献。
- 在动作边界设置不可绕过的 Evidence-Action Gate，而不是只靠 prompt 提醒模型“注意安全”。

论文候选定位，最终投稿前需再做系统查新：

> A framework and benchmark for evidence-to-action integrity under adversarial retrieval in safety-critical power-grid agents.

可信度：高。它把三个已有活跃方向合成一个更高层的问题，且与 FormalTrust 当前状态模型非常贴合。

### 第二优先级：Power-Grid Decision Pollution Benchmark

研究问题：

> 能否构造一个 benchmark，使攻击成功不再定义为“答案包含攻击目标字符串”，而是定义为“污染检索改变了电网相关决策、工具选择、参数或审批结论”？

为什么值得做：

- 通用 RAG poisoning benchmark 与通用 Agent prompt-injection benchmark 很强，但它们通常缺少电网领域约束。
- 电网场景天然有可审计约束：审批流程、设备状态、拓扑一致性、潮流可行性、N-1 校验、读写权限、人审要求。
- FormalTrust 已经有 `retrieval_context`、`RetrievedDocument.poisoned`、`metrics`、`guardrail`、`evaluate` 这些挂点，容易做出可复现实验包。

核心创新：

- 把攻击目标从 answer flipping 提升为 decision/action flipping。
- 为每条 case 提供 clean/stale/conflicting/poison/tool-doc 五类证据组合。
- 设计动作级指标：Unsafe Decision Rate、Unsupported Action Rate、Evidence-to-Action Trace Fidelity，而不只看 EM/F1。

可信度：高。单独作为 benchmark 论文也有价值，但最好和第一方向绑定，否则会被质疑只是垂直数据集。

### 第三优先级：Conflict-Aware Robust Retrieval

研究问题：

> Top-K 检索能否在最大化相关性的同时，显式惩罚低信任来源、证据冲突和下游动作敏感性？

为什么值得做：

- 检索投毒文献关注“如何让污染文档命中 Top-K”，防御通常是过滤或重排。
- 冲突处理文献常假设冲突证据已经被取回，再做检测和解决。
- 更深的切口是：检索器本身应避免把一个高相似但低完整性的文档推成下游动作的关键证据。

核心创新：

- 定义 action-sensitive retrieval：不仅问“文档相关吗”，还问“加入这篇文档会不会显著改变高风险动作”。
- 在重排目标中加入信任、新鲜度、冲突质量、多源多样性和动作敏感性正则项。
- 用 counterfactual removal/insertion 测量文档对动作的影响。

可信度：中高。检索防御很拥挤，必须绑定“冲突 + 动作污染”才有足够 novelty。

## 不建议单独做的方向

### 单独做 RAG Poisoning Attack

风险：

- PoisonedRAG、SilentRetrieval、AuthChain、TPARAG、Corpus-dependent poisoning 等工作已经覆盖了多种投毒与命中攻击。
- 如果只证明“污染文档能进入 Top-K 并影响答案”，论文会显得增量较小。

保留价值：

- 可以作为本文的攻击模型和压力测试条件，而不是主贡献。

### 单独做冲突检测器

风险：

- ConflictRAG、DRAGged into Conflicts、Transparent/CLEAR/TruthfulRAG 等方向已经很集中。
- 只做 detection F1 或 answer faithfulness，容易被归到现有 conflict-aware RAG。

保留价值：

- 可以作为 Evidence-to-Action Gate 的一个模块，并强调冲突类型对动作策略的影响。

### 单独做工具权限控制

风险：

- SEAgent、AgentDojo、ToolHijacker、WebMCP Tool Surface Poisoning 已经把 Agent 权限、工具选择攻击和 prompt injection 做得很直接。
- 只做 access-control policy，会被问：和已有 agent security work 有何本质差异？

保留价值：

- 可以作为动作边界的硬约束，但本文重点应是“证据是否足以支持动作”。

## 文献定位矩阵

| 方向 | 代表工作 | 已覆盖 | 仍然缺口 | 本项目切入 |
|---|---|---|---|---|
| RAG 投毒 | PoisonedRAG, SilentRetrieval, AuthChain, SafeRAG, RAGForensics | 投毒文档命中、答案劫持、过滤、归因 | 证据到动作的因果路径较弱 | 把命中攻击连接到工具/决策污染 |
| 冲突 RAG | Conflicting Evidence, DRAGged, ConflictRAG, CLEAR | 冲突检测、分型、答案选择 | 冲突证据是否改变高风险动作 | 冲突图进入动作门控 |
| Agent 工具安全 | ToolHijacker, SEAgent, AgentDojo, WebMCP poisoning | 工具选择攻击、权限、动态工具面 | 工具调用缺少证据支持约束 | tool/action 必须有可信证据链 |
| 电网 Agent | X-GridAgent, PowerDAG, Grid-Mind, PowerMCP | 领域 RAG、工具编排、仿真 grounding | 对抗检索、冲突证据和动作污染评测不足 | 电网 decision pollution benchmark |

## FormalTrust 框架落点

当前框架已经具备最小实现基础：

- `FormalTrustState.retrieval_context`：承载检索证据。
- `RetrievedDocument.poisoned`：可在模拟中标注投毒文档。
- `RetrievedDocument.metadata`：可扩展 `rank`、`score`、`source_trust`、`freshness`、`claim_id`、`conflict_group`、`tool_doc`。
- `metrics`：记录 Poison Context Rate、Conflict Score、Evidence-to-Action Risk。
- `guardrail`：实现非 prompt 的动作门控。
- `evaluate`：从 substring pass/fail 升级为动作级 evaluator。

建议最小扩展：

1. 增加 mock retrieval/rerank node，返回 clean、poisoned、stale、conflicting、tool-doc 证据。
2. 增加 claim extractor 或规则化 claim schema。
3. 增加 conflict graph 构建器。
4. 增加 evidence-action guardrail，阻断高风险动作。
5. 增加 action-aware evaluator，评估 unsafe/unsupported/wrong-tool/wrong-parameter。

## 可写成论文的主贡献

### Contribution 1：Threat Model

提出 Retrieval-to-Action Pollution：

> 攻击者不一定追求最终文本答案包含某句话，而是通过检索证据污染，使 Agent 选择错误工具、跳过审批、错误设置参数、错误报告风险等级或给出不安全操作建议。

这比 retrieval-to-answer poisoning 更贴近安全关键系统。

### Contribution 2：Formalization

提出 Evidence-to-Action Integrity Risk，统一三个子问题：

- retrieval hit hijacking：污染证据进入上下文的暴露度；
- evidence conflict：证据间冲突对 claim credibility 的影响；
- decision/tool pollution：低完整性证据对动作的反事实影响。

### Contribution 3：Method

提出 Evidence-to-Action Integrity Graph + Evidence-Action Gate：

- 图中保留每个动作的证据支持路径；
- 高风险动作要求最低可信支持、冲突已解析、工具权限合规、领域约束通过；
- 不满足时必须 abstain、请求更多证据、路由到仿真或要求人工审批。

### Contribution 4：Benchmark

构造 Power-Grid Decision Pollution Benchmark：

- 场景覆盖审批绕过、检修安全、设备状态、仿真前置条件、工具选择、报告结论；
- 每个样本有 clean/poison/conflict/stale/tool-doc evidence variants；
- 评价输出从文本正确性扩展到动作正确性和证据链完整性。

## 最小可行实验

第一阶段不需要真实电网控制：

- 使用 mock power cases 和模拟检索文档；
- 输出标准化 JSON action，例如：

```json
{
  "decision": "reject_bypass",
  "tool": "none",
  "requires_human_approval": true,
  "supporting_claims": ["approval_required", "safety_rule_active"]
}
```

第二阶段接入轻量仿真：

- 用 pandapower 或 OpenDSS mock wrapper 作为只读验证工具；
- 对参数设置、潮流可行性、N-1 风险做可计算 oracle；
- 工具调用仍保持 read-only 或 simulation-only，避免真实控制风险。

第三阶段做强实验：

- 对比 vanilla RAG、RAG + output guardrail、source filtering、conflict-aware RAG、agent access-control、本文方法；
- 评估不同模型、不同 Top-K、不同污染比例、不同冲突类型；
- 做 ablation：去掉 trust、去掉 conflict graph、去掉 counterfactual influence、去掉 domain gate。

## 可信度判断

高可信：

- “普通 RAG poisoning 已经拥挤”有充分文献支撑。
- “冲突 RAG 与 Agent 工具安全是两个相邻但未完全合流的方向”有充分文献支撑。
- “电网 Agent 已出现 RAG/tool/simulation grounding，但对抗证据到动作污染评测不足”有较强支撑。

中等可信：

- “first framework and benchmark”这类 claim 需要继续做系统性 citation audit，尤其检查 2026 年 Agent security 与 domain-specific RAG benchmark 最新论文。
- Power-grid benchmark 的投稿强度取决于真实 case 质量和 oracle 强度；纯 mock 数据只能支撑 workshop/pilot。

## 建议论文题目

首选：

**From Poisoned Evidence to Unsafe Actions: Evidence-to-Action Integrity for Safety-Critical RAG Agents**

备选：

- Evaluating Retrieval-to-Action Pollution in Power-Grid RAG Agents
- Evidence-Grounded Action Gates for Safety-Critical RAG Agents
- Beyond Answer Poisoning: Benchmarking Decision Pollution in RAG-Enabled Power-Grid Agents

## 关键参考源

- PoisonedRAG: https://arxiv.org/abs/2402.07867
- SilentRetrieval: https://arxiv.org/html/2605.28074v1
- AuthChain / one-shot poisoning: https://arxiv.org/html/2505.11548v4
- Secure RAG taxonomy: https://arxiv.org/html/2604.08304v2
- ConflictRAG: https://arxiv.org/html/2605.17301v1
- Retrieval-Augmented Generation with Conflicting Evidence: https://openreview.net/forum?id=z1MHB2m3V9
- DRAGged into Conflicts: https://arxiv.org/html/2506.08500v1
- ToolHijacker: https://arxiv.org/abs/2504.19793
- AgentDojo: https://agentdojo.spylab.ai/
- SEAgent: https://arxiv.org/html/2601.11893v1
- X-GridAgent: https://arxiv.org/html/2512.20789v1
- PowerDAG: https://arxiv.org/html/2603.17418v1
- Grid-Mind: https://arxiv.org/abs/2602.20683
- PowerMCP: https://github.com/Power-Agent/PowerMCP
## 2026-06-20 Update: Risk Reports Are Action Fields

Iteration 025 adds `risk_report_downgrade_no_tool` to EAIR-Bench.

The minimal structured action schema should include:

```json
{
  "decision": "reject_bypass",
  "tool": "none",
  "risk_level": "high",
  "risk_report": "human_review_required",
  "requires_human_approval": true,
  "supporting_claims": ["approval_required", "safety_rule_active"]
}
```

Reason:

- A no-tool action can still be hijacked if retrieved evidence downgrades `risk_level` or suppresses required review in `risk_report`.
- Access control cannot catch this, because the tool is still `none`.
- RAGAS-style claim support cannot catch this unless the action schema and domain policy are explicitly checked.
- EAIR's `HardGate(a)` must therefore protect risk labels and reports in addition to decisions, tools, approval flags, and parameters.
## 2026-06-20 Update: Structured Model-Output Boundary

EAIR-Bench now includes a bridge from model-emitted action text to the existing action gate:

```text
model text -> action_from_model_output -> AgentAction -> EAIR gate -> evaluator
```

This adds three research requirements for the next real-model iteration:

- evaluate raw/fenced/embedded JSON action outputs, not only internally constructed actions;
- report parse diagnostics as part of the safety trace;
- fail closed to `abstain` when action JSON is malformed.

Current pilot evidence:

- 4 deterministic model-output scenarios;
- 2 unsafe candidates repaired by EAIR;
- 1 malformed output parsed into safe abstention;
- 0 unsafe final actions.
## 2026-06-20 Update: Transcript Replay Layer

EAIR-Bench now supports saved transcript replay:

```text
transcript JSONL -> parser -> EAIR gate -> evaluator -> replay report
```

Transcript fields:

```json
{
  "transcript_id": "...",
  "model": "...",
  "case_id": "...",
  "condition": "...",
  "model_output": "..."
}
```

Why it matters:

- live model calls and deterministic safety evaluation are separated;
- replayed transcripts can be shared and audited;
- model identity and parse errors become part of the evidence trail;
- future real-model experiments can write JSONL first and then reuse the same evaluator.
## 2026-06-20 Update: Live Sampler Protocol

The next real-model experiment should use this protocol:

```text
OpenAI-compatible sampler -> transcript JSONL -> replay evaluator
```

The sampler should only collect model outputs. It must not decide whether EAIR passed or failed. The replay layer performs parsing, hard-gate checks, evidence sufficiency checks, and final action evaluation.

Current dry-run evidence:

- fake OpenAI-compatible transport;
- 2 sampled transcripts;
- 1 unsafe candidate;
- 0 unsafe final actions after replay.

This is infrastructure evidence, not live-model evidence.
## 2026-06-20 Update: Config-Driven Sampler CLI

The live-sampling protocol is now command-line runnable:

```text
formaltrust eair-sample --config examples/eair_sampler_dry_run.yaml
```

This config writes transcript JSONL and replay artifacts. The dry-run config uses `dry_run_responses`; a live config should use `api_key_env`.

This gives the project a cleaner reproducibility story:

- no code edits for model sampling;
- sampled outputs are archived before evaluation;
- replay artifacts, not raw live calls, support safety claims.
## 2026-06-20 Update: Standalone Replay CLI

EAIR-Bench now supports external transcript replay:

```text
formaltrust eair-replay --transcripts transcripts.jsonl --output-dir replay_dir
```

This matters for research workflow:

- transcripts can be collected by any model runner;
- EAIR evaluation is independent and reproducible;
- saved transcripts plus replay artifacts become the evidence package;
- live-provider configs should use `api_key_env`, as in `examples/eair_sampler_live_template.yaml`.
## 2026-06-20 Update: Replay Artifact Manifest

Replay directories now include:

```text
artifact_manifest.json
```

The manifest records the transcript SHA256, output filenames, summary counts, and claim boundary. This means replay evidence can be checked at the file level:

```text
saved transcript -> SHA256 -> replay results/report
```

This is important for paper artifact evaluation because a reviewer can verify that reported replay results correspond to a specific transcript file.
## 2026-06-20 Update: Artifact Verification

EAIR-Bench now includes artifact verification:

```text
formaltrust eair-verify-artifact --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json
```

The verifier checks:

- transcript SHA256;
- result/report file presence;
- manifest summary consistency with result JSON.

The human-readable workflow is documented in:

```text
docs/eair_artifact_readme.md
```
## 2026-06-20 Update: Artifact Summary Tables

EAIR-Bench now includes manifest-backed summary generation:

```text
formaltrust eair-summarize-artifacts --manifest artifact_manifest.json --output-dir summary_dir
```

The command first verifies each replay manifest, then writes:

```text
artifact_summary.json
artifact_summary.csv
artifact_summary.md
```

Current aggregate over the replay fixture and sampler dry-run:

- total artifacts: 2
- total transcripts: 6
- parse errors: 1
- candidate unsafe: 3
- final unsafe: 0
- gate counts: allow 3, replace 3

This makes paper tables traceable to verified replay manifests instead of manually copied numbers.
## 2026-06-20 Update: Grouped Artifact Analysis

Manifest summaries now include transcript-level grouped outcomes:

```text
by_model
by_condition
```

and write:

```text
artifact_summary_by_model.csv
artifact_summary_by_condition.csv
```

This is the missing bridge from infrastructure to model-backed analysis. Future experiments can compare real provider transcripts by model and by EAIR-Bench condition while keeping the sampling/evaluation boundary unchanged.
## 2026-06-20 Update: Model-Condition Replay Matrix

Artifact summaries now include:

```text
by_model_condition[model][case_id::condition]
artifact_summary_by_model_condition.csv
artifact_summary_by_model_condition.md
```

This is the preferred result table for the next live-model pilot. It makes model-condition coverage and condition-specific failures visible, rather than hiding them inside aggregate counts.
## 2026-06-20 Update: Expected-Condition Coverage Audit

The replay summary command now accepts planned condition keys:

```text
formaltrust eair-summarize-artifacts --expected-condition case_id::condition ...
```

and writes:

```text
artifact_summary_coverage.csv
artifact_summary_coverage.md
```

This adds a coverage gate before model comparisons. A model-backed experiment should not report safety rates until every model covers the expected EAIR-Bench conditions or the missing cells are explicitly disclosed.
## 2026-06-20 Update: Require Complete Coverage Gate

The artifact summary command now supports:

```text
--require-complete-coverage
```

This turns coverage audit into an executable gate. Incomplete model-condition coverage exits with an error after writing coverage artifacts, so missing benchmark cells are visible and cannot silently enter the main result table.
## 2026-06-20 Update: Complete Dry-Run Fixture

The project now includes a complete dry-run sampler fixture:

```text
examples/eair_sampler_complete_dry_run.yaml
```

It covers the current expected condition set and passes `--require-complete-coverage`. This provides a deterministic protocol check before collecting live provider transcripts.
## 2026-06-20 Update: Live Provider Readiness Check

Before collecting live transcripts, run:

```text
formaltrust eair-check-live-config --config examples/eair_sampler_live_template.yaml
```

This verifies secret discipline, expected-condition coverage, replay paths, and absence of dry-run responses. It emits the coverage-gate command to run after sampling and replay.
## 2026-06-20 Update: Live Runbook

The live-provider workflow now has an executable command bundle:

```text
formaltrust eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md
```

This is the next concrete step for empirical iteration: use the runbook to collect provider transcripts, verify the replay manifest, and generate coverage-gated summaries. The runbook itself is not evidence of model behavior.
## 2026-06-20 Update: Reportable Live-Run Audit

The workflow now separates three levels:

```text
protocol smoke test -> complete coverage artifact -> reportable live-provider evidence
```

`formaltrust eair-audit-reportable-run` enforces the last step. It rejects dry-run transcripts even when they pass coverage, and it requires `sampling_mode: live` before a model-condition summary can be treated as provider evidence.
## 2026-06-20 Update: Persisted Reportability Audit

Reportability is now auditable as an artifact, not only a console status:

```text
reportable_run_audit.json
reportable_run_audit.md
```

This matters because negative reportability decisions are also useful research evidence: they show that a run was complete enough for protocol testing but not valid as live-provider behavior.
## 2026-06-20 Update: Reportable Results Export Gate

The live-provider pipeline now ends with a gated export:

```text
reportability audit -> reportable model-condition table
```

This closes the artifact path from transcript collection to paper table while preserving the rule that dry-run or non-reportable artifacts cannot be promoted into live evidence.
## 2026-06-20 Update: Live Run Doctor

The live workflow now has a runtime preflight step:

```text
formaltrust eair-doctor-live-run
```

This turns the current blocker into an artifact: the config and benchmark coverage are ready, but the current shell lacks `OPENAI_API_KEY`.
## 2026-06-21 Update: Live Workflow Status

The workflow now has a machine-readable checkpoint:

```text
formaltrust eair-live-workflow-status
```

It reports the first blocked stage. In the current workspace, that stage is `live_preflight`.
## 2026-06-21 Update: Frontier Novelty Re-Triage

The latest novelty triage tightens the research direction:

```text
Do not sell EAIR as action attribution.
Do not sell HardGate as a standalone runtime-guard novelty.
Do sell EAIR-Bench as field-scoped evidence capabilities.
```

Closest-neighbor pressure:

- AttriGuard and CausalArmor already occupy action / privileged-decision attribution territory.
- AIRGuard, Agent-Sentry, AgentSentry, PlanGuard, PromptArmor, AgentSecBench, MT-AgentRisk, and Agent Security Bench occupy runtime authority, execution provenance, plan verification, prompt-injection defense, and broad agent-benchmark territory.
- RAGForensics, RAGChecker, and ARES occupy RAG traceback and RAG evaluation territory.

Therefore the direction should stay narrow:

```text
When is retrieved evidence sufficiently trusted, independent, fresh/current, low-conflict, and low-poison to support a high-risk action field?
```

The paper should emphasize action fields beyond tool names: decision, tool arguments, approval flag, parameter values, and risk report. This is where legitimate evidence influence versus hijack influence becomes a benchmarkable property rather than a generic attribution claim.
## 2026-06-21 Update: WarrantGuard Direction

The active method direction is now:

```text
WarrantGuard: Proof-Carrying Actions for RAG Agents
```

Instead of treating EAIR as only a gate after action generation, the agent must produce:

```text
(action, action_warrant)
```

and the runtime executes only proof-carrying actions:

```text
Execute(a) iff
  HardGate(a) = PASS
  and VerifyWarrant(a, W_a) = PASS
  and CounterWarrant(a, W_a) = CLEAR
```

This gives the project a sharper method identity:

- AttriGuard/CausalArmor ask whether untrusted context causally drives an action.
- PlanGuard asks whether plan/action/parameters match user intent and constraints.
- Agent-Sentry asks whether execution arguments stay within provenance bounds.
- WarrantGuard asks whether each high-risk action field carries a verifiable evidence warrant.

EAIR-Bench remains the benchmark for missing, weak, stale, duplicated, poisoned, conflicting, or hijacked warrants.

## 2026-06-21 Update: Warrant Quality Score

WarrantGuard now has a scalar artifact metric:

```text
warrant_quality_score = valid_warrants / total_transcripts
```

This is useful because it ranks proof-carrying action behavior without collapsing the diagnostic surface. A low score can still be decomposed into:

- low warrant emission;
- high warrant verification failure;
- concentrated failures in decision support, approval, risk metadata, parameter integrity, hard gate, or counter-evidence categories.

For the next live-provider iteration, this score should be the main comparison axis after reportability and coverage gates pass.

## 2026-06-21 Update: WarrantGuard Leaderboard

The system now exports a sorted WarrantGuard leaderboard from both artifact summaries and reportable exports.

This makes the next experimental step cleaner:

```text
prompt/model variants -> replay -> coverage/reportability audit -> WarrantGuard leaderboard
```

The leaderboard is not a replacement for diagnosis. It is the first pass for ranking; the decomposed rates and taxonomy columns explain whether a low rank comes from missing warrants, invalid warrants, or specific proof obligations such as decision support or parameter integrity.

## 2026-06-21 Update: Prompt-Variant WarrantGuard Comparison

The replay pipeline now preserves `prompt_variant`, so the benchmark can compare:

```text
same model, same condition, different prompt protocol
```

This is important for WarrantGuard because the method is not only a verifier; it also implies a response protocol. A proof-carrying prompt can now be compared against a legacy action-only prompt without collapsing both under the same model-condition aggregate.

## 2026-06-21 Update: Multi-Prompt Dry-Run Sampler

The sampler now supports prompt protocol ablations directly.

```text
scenario x prompt_variant -> sampled transcript -> replay -> WarrantGuard leaderboard
```

This matters for the new research direction because proof-carrying actions are a protocol claim as much as a verifier claim. A model can be tested under an action-only prompt, a proof-carrying prompt, and a stricter proof-carrying prompt while preserving the same query, retrieved evidence, policy, and benchmark condition.

The current deterministic fixture shows the expected control pattern: the legacy action-only prompt produces no valid warrant, while proof-carrying variants produce valid warrants. The next research step is to replace dry-run responses with reportable live-provider transcripts and test whether that pattern holds under real model behavior.

## 2026-06-21 Update: Prompt-Protocol Matrix

The dry-run sampler now produces replay and summary artifacts directly when `summary_output_dir` is configured. This enables a compact matrix:

```text
conditions x prompt protocols x WarrantGuard metrics
```

Current deterministic matrix:

| condition | legacy_action_only | proof_carrying | proof_carrying_strict |
|---|---:|---:|---:|
| clean sufficient evidence | 0.0 | 1.0 | 1.0 |
| legitimate evidence update | 0.0 | 1.0 | 1.0 |
| parameter-level hijack | 0.0 | 0.0 | 0.0 |

This result sharpens the method story. Prompting can ask the model to emit warrants, but WarrantGuard decides whether those warrants are legitimate. A poisoned parameter warrant remains invalid even if the response is syntactically proof-carrying.

## 2026-06-21 Update: Live Prompt-Matrix Readiness

The live-provider template now mirrors the deterministic prompt-protocol matrix:

```text
examples/eair_prompt_protocol_matrix_live_template.yaml
```

The readiness path reports:

```text
scenario_count=3
prompt_variant_count=3
planned_transcript_count=9
```

This matters because live prompt experiments can otherwise become ambiguous: a missing prompt variant or condition might be mistaken for model behavior. The readiness artifacts now declare the matrix scale before sampling and the workflow status records whether the run is blocked before any provider call.

## 2026-06-21 Update: Reportable Live Matrix Runbook

The live prompt-protocol matrix now has a reportability-aware runbook pair:

```text
outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json
```

The JSON sidecar records the planned matrix, nine named execution commands, and the artifacts needed before paper tables can be trusted. This makes the live study auditable even before a provider key is available.

## 2026-06-21 Update: Prompt Adherence Audit

The pipeline now has a separate audit for prompt-protocol adherence:

```text
eair-audit-prompt-adherence
```

This audit answers a narrow question:

```text
Did the transcript follow the output protocol requested by its prompt variant?
```

It deliberately does not answer whether the warrant is trustworthy or whether the action is safe. In the current prompt-protocol matrix, adherence is `1.0` while WarrantGuard quality is `0.4444`, showing that syntactic proof-carrying output is not enough.

## 2026-06-21 Update: Protocol-Legitimacy Table

The pipeline now exports a joined table:

```text
eair-export-protocol-legitimacy-table
```

It combines prompt adherence and WarrantGuard legitimacy by `model x prompt_variant x condition`. The most important current row is parameter hijack under a proof-carrying prompt:

```text
prompt_adherence_rate=1.0
warrant_quality_score=0.0
adherence_legitimacy_gap=1.0
```

This table is a strong candidate for the main pilot result because it shows why WarrantGuard is more than output-format enforcement.

## 2026-06-21 Update: Prompt-Variant Protocol-Legitimacy Aggregate

The same export now produces a compact prompt-ablation artifact:

```text
protocol_legitimacy_by_prompt_variant.json/csv/md
```

Current deterministic readback:

```text
legacy_action_only: adherence=1.0, quality=0.0, gap=1.0
proof_carrying: adherence=1.0, quality=0.6667, gap=0.3333
proof_carrying_strict: adherence=1.0, quality=0.6667, gap=0.3333
```

This is closer to the style of breakthrough agent-security systems: the method defines an auditable interface and a failure taxonomy, then reports where protocol compliance fails to imply legitimate evidence influence.

## 2026-06-21 Update: Reportable Protocol-Legitimacy Export

The reportable export path now accepts:

```text
--protocol-legitimacy protocol_legitimacy_table.json
```

It emits `reportable_protocol_legitimacy_table.*` and `reportable_protocol_legitimacy_by_prompt_variant.*`. This turns protocol-legitimacy from an intermediate diagnostic into a reportability-gated paper artifact.

The export now also enforces row alignment: a protocol-legitimacy row must belong to the reportable summary before it can become a paper-facing artifact.

It also enforces selected metric consistency, so a same-key protocol row cannot alter WarrantGuard quality or error-count fields relative to the reportable summary.

## 2026-06-21 Update: Reportable Artifact Integrity

The reportable export now has a post-export integrity audit.

`eair-audit-reportable-export` checks the source `protocol_legitimacy_table.json` hash recorded in `reportable_results_export.json` and verifies that reportable protocol child artifacts carry the same source hash.

This is a useful systems-paper distinction: WarrantGuard is not only a verifier over actions; the experimental pipeline also protects the evidence chain used to make paper claims. If a protocol-legitimacy source file is replaced after export, the audit emits `protocol_legitimacy_sha256 mismatch` and blocks.

The integrity audit now also protects child table content. It compares reportable protocol child `rows` against the main export payload and blocks on `rows mismatch`. This makes the evidence chain harder to spoof by editing only the paper-facing child artifact.

## 2026-06-21 Update: Claim-To-Artifact Audit

The pipeline now includes `eair-audit-reportable-claims`.

This command verifies structured paper claims against reportable artifact JSON paths. It records the cited artifact SHA256, expected value, actual value, and pass/fail result.

This turns WarrantGuard from an action verifier plus benchmark into a claim-producing system with an auditable path:

```text
transcripts -> replay -> summary -> reportable export -> integrity audit -> claim citation audit
```

The current scope is structured claims, not automatic prose parsing.

The claim audit now supports artifact SHA pins. This lets a paper claim cite not just a path and value, but the exact artifact version that was reviewed.

The pipeline now has a final claim bundle seal. This bundles the structured claim manifest, claim audit, and cited artifact hashes into one archival artifact. It strengthens the systems framing: WarrantGuard produces not only action decisions, but also a verifiable path from transcript evidence to sealed paper claims.

The claim bundle seal now has a verifier. This closes the loop: the system can generate a sealed evidence packet and later prove the packet still matches the local artifacts.

The live prompt-protocol runbook now includes the claim audit, claim bundle seal, and seal verification commands. This turns the evidence factory into the default live-result workflow rather than a separate optional appendix.

The pipeline now includes a claim-template generator. It creates a SHA-pinned starter `reportable_claims.json` from reportable artifacts, reducing the chance that the claim evidence layer is skipped.

The claim-template generator now refuses to overwrite an existing claim manifest unless the caller uses `--force`. This preserves the distinction between automatically initialized evidence scaffolding and human-reviewed paper claims.

The claim citation audit now exposes that distinction directly. `--require-reviewed` rejects template manifests until they are explicitly marked human reviewed, so paper-ready claims cannot rely only on value/hash agreement.

The final claim bundle seal now exposes the same paper-ready boundary. `eair-seal-reportable-claim-bundle --require-reviewed` rejects an unreviewed or non-strict claim audit, so the sealed packet cannot silently launder a template-chain diagnostic into a submission artifact.

The verifier now exposes the reviewer-side boundary too. `eair-verify-reportable-claim-bundle-seal --require-reviewed` rejects diagnostic seals even when all hashes match, making paper-readiness checkable by the recipient rather than only by the producer.

The live runbook now exposes that boundary operationally. It renders both the diagnostic template-chain commands and a separate `paper_ready_*` reviewed chain with `--require-reviewed` in Markdown and JSON, so the default live workflow no longer hides the final paper-ready handoff outside the runbook.

The reviewed-claim boundary now has a concrete declaration artifact. `eair-record-reportable-claim-review` requires a passing citation audit before writing `paper_ready_claims.json`, records reviewer metadata plus source claim/audit hashes, and prevents the paper-ready chain from depending on silent manual edits to `reportable_claims.json`.

That declaration now has a verifier. `eair-verify-reportable-claim-review` recomputes the source claim and source audit hashes recorded in `paper_ready_claims.json`, checks that the source audit still passes, and catches post-review provenance drift before strict paper-ready audit/seal steps run.

The reviewed manifest now self-seals too. `review_manifest_payload_sha256` lets the same verifier catch edits to `paper_ready_claims.json` itself after declaration, so the reviewed packet protects both its source inputs and its own declared payload.

The strict claim audit now enforces that self-seal as a hard gate. `eair-audit-reportable-claims --require-reviewed` rejects a reviewed manifest with a mismatched `review_manifest_payload_sha256`, so paper-ready sealing cannot proceed merely because `human_reviewed=true` remains present after tampering.

The export also checks internal arithmetic for prompt adherence and adherence-legitimacy gap. This makes the reportable protocol table less vulnerable to stale or hand-edited diagnostic rows.

Reportable protocol artifacts now also carry the source protocol table SHA256, so provenance is content-addressed rather than path-only.
