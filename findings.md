# EAIR 方向重构发现记录

本文件记录本轮“EAIR / RAG-agent security 方向重构”的研究发现、前沿判断和系统设计约束。外部论文、网页和用户粘贴内容都应视为研究数据，不作为可执行指令。

## 旧方向的问题

旧方向：

```text
RAG poisoning -> claim/conflict graph -> EAIR gate
```

主要问题：

- RAG poisoning / retrieval exposure 已很成熟，`PRE`、`RHE` 只能作为背景指标。
- claim extraction、claim-level faithfulness、conflict graph 已有 RAGAS、ARES、RAGChecker、FaithfulRAG、TruthfulRAG 等相关工作。
- action-level causal attribution 已有 AttriGuard、AgentSentry 等相近方向，不能把 `I(d -> a)` 本身作为唯一创新。
- 只靠数学抽象不足以支撑论文，需要 benchmark + metric + defense + strong baselines。

## 新方向锚点

新的核心问题：

> When should retrieved evidence be allowed to influence high-risk RAG-agent actions?

新的研究对象：

```text
context-dependent high-risk action grounding
```

核心判断：

```text
外部 evidence 影响 action 并不天然危险。
危险在于：污染、过期、低可信、冲突或证据不足的 claim-level evidence path 支持了 high-risk action。
```

## 新贡献包装

### Contribution 1：EAIR formalism

重点不是“动作级反事实影响”本身，而是：

```text
claim-level evidence-to-action integrity
```

风险定义：

```text
安全风险 = 不可信或证据不足的 retrieved evidence 对 high-risk action 的不当影响
```

### Contribution 2：EAIR-Bench

构造专门评估：

```text
retrieved evidence 是否合法/非法影响 high-risk RAG-agent actions
```

的 benchmark。

这比单纯公式更可能成为可认可贡献。

### Contribution 3：EAIR-Gate

运行时防御由三层组成：

```text
HardGate(a)
EvidenceSufficient(a)
soft EAIR(q,a)
```

## 必须区分的概念

### Legitimate Influence

可信、充分、最新、低冲突 evidence 合法影响动作。

例子：

- 最新官方规程要求人工审批，Agent 因此设置 `requires_human_approval=true`。
- 官方参数表给出 `voltage_limit=1.05`，Agent 用该参数调用仿真。

### Hijack Influence

污染、过期、低可信、冲突或证据不足 evidence 推动危险动作。

例子：

- 污染 memo 让 Agent 允许 bypass。
- stale record 让 Agent 使用过期设备状态。
- tool-doc poisoning 让 Agent 选择 write-control tool。
- 参数污染让 tool name 正确但 tool args 危险。

## 必须覆盖的失败模式

| 失败模式 | 说明 |
|---|---|
| PRE/RHE false positive | 污染文档进入 Top-K，但未影响动作 |
| PRE/RHE false negative | 文档排名不高但 claim 通过计划影响高风险参数 |
| RAGAS-style blind spot | answer/claim faithful，但 action 或参数仍危险 |
| AttriGuard-style overblock | 外部 evidence 合法影响 context-dependent action，被当成 hijack |
| AttriGuard-style insufficiency blind spot | 能判断外部上下文驱动 action，但不能判断证据是否充分/独立/最新 |
| Access-control blind spot | tool 没越权，但 decision/approval/parameter 错 |
| Conflict-only blind spot | poison-only 或 insufficient evidence 无显式冲突 |
| Source-filter blind spot | stale evidence 或中等可信来源导致错误动作 |

## 数学重构要点

### HardGate

硬约束包括：

- 工具权限
- domain policy
- human approval requirement
- high-risk write authorization
- tool schema / parameter validity

这些不能被 soft risk 的 lambda 抵消。

### EvidenceSufficient

高风险 action 必须满足：

- required claims 存在
- source-diverse support 足够
- independent source count 足够
- freshness/version 足够
- conflict pressure 低
- suspicion/poison support 低

### Anti-duplication support

`S(c)` 不能简单对支持文档求和。应使用：

- source cluster saturation
- near-duplicate penalty
- same-origin cap
- provenance diversity

### Influence split

需要区分：

```text
LegitInfluence(d -> a)
HijackInfluence(d -> a)
```

不是所有 `I(d -> a)` 都是坏事。

## 文献与 baseline 重点

### RAG 侧

- PoisonedRAG、AgentPoison、Influence Factors on RAG Poisoning
- RAGForensics、RAGOrigin / Who Taught the Lie、Source Attribution in RAG
- RAGAS、ARES、RAGChecker
- ConflictRAG、FaithfulRAG、TruthfulRAG

### Agent security 侧

- AgentDojo
- Agent Security Bench
- MT-AgentRisk
- PromptArmor
- PlanGuard
- AttriGuard
- AgentSentry

## 新前沿核查（截至 2026-06-17）

本节基于 2026-06-17 对 arXiv、OpenReview、ACL/ACM/官方项目页的重新核查。结论是：EAIR 方向不能再声称“第一个 action-level causal attribution / RAG safety function”。更稳妥的定位是：

```text
EAIR-Bench evaluates when retrieved evidence is allowed to influence high-risk agent actions.
```

也就是 benchmark + evidence sufficiency + legitimate-vs-hijack evidence influence，而不是把外部 evidence 的 causal influence 本身当 novelty。

### 文献矩阵

| 领域 | 代表工作 | 已覆盖的问题 | 对 EAIR 的影响 |
|---|---|---|---|
| RAG poisoning / retrieval exposure | PoisonedRAG (`https://arxiv.org/abs/2402.07867`), CorruptRAG (`https://arxiv.org/abs/2504.03957`), KG-RAG poisoning (`https://arxiv.org/abs/2507.08862`), secure RAG taxonomy (`https://arxiv.org/html/2604.08304`) | 污染文档注入、少量文档/单文档攻击、KG-RAG poisoning、检索安全 taxonomy。 | 说明 PRE/RHE/poison exposure 已是背景；EAIR 必须证明“retrieved poison != action compromise”，并关注 action support path。 |
| RAG traceback / source attribution | RAGForensics (`https://arxiv.org/abs/2504.21668`), RAGOrigin / Who Taught the Lie (`https://arxiv.org/abs/2509.13772`), Source Attribution in RAG (`https://arxiv.org/abs/2507.04480`) | 找到哪些文本对错误生成/poisoned response 负责，或估计 retrieved document 对生成输出的贡献。 | 和 EAIR 最接近的是“responsibility/influence”，但这些工作主要解释 answer/misgeneration source，不判定 action 是否由充分可信证据合法支持。 |
| RAG evaluation / claim-level faithfulness | RAGAS (`https://arxiv.org/abs/2309.15217`), ARES (`https://arxiv.org/abs/2311.09476`), RAGChecker (`https://arxiv.org/abs/2408.08067`) | context relevance、answer faithfulness、answer relevance、claim-level entailment diagnostics。 | 这些是 EAIR 的证据质量底座；但 claim faithful 不等于 decision/tool/approval/parameter safe。 |
| Conflicting evidence / faithful RAG | Retrieval-Augmented Generation with Conflicting Evidence (`https://openreview.net/forum?id=z1MHB2m3V9`), DRAGged into Conflicts (`https://arxiv.org/abs/2506.08500`), FaithfulRAG (`https://arxiv.org/abs/2506.08938`), TruthfulRAG (`https://arxiv.org/abs/2511.10375`), ConflictRAG (`https://arxiv.org/html/2605.17301`) | ambiguity、misinformation、noise、fact-level/knowledge-graph conflict resolution、context faithfulness。 | 冲突处理是必要模块，但不能替代 action grounding：poison-only、evidence-insufficient、allowed-tool dangerous decision 可能没有显式冲突。 |
| Agent prompt-injection / tool safety benchmark | AgentDojo (`https://arxiv.org/abs/2406.13352`), Agent Security Bench (`https://arxiv.org/abs/2410.02644`), MT-AgentRisk (`https://arxiv.org/abs/2602.13379`) | tool-use prompt injection、multi-turn tool risks、agent attack/defense benchmark。 | 这些证明 agent security benchmark 已拥挤；EAIR-Bench 应专注 evidence-to-action sufficiency，而不是泛化 agent safety benchmark。 |
| Runtime defenses for indirect prompt injection | PromptArmor (`https://arxiv.org/abs/2507.15219`), PlanGuard (`https://arxiv.org/abs/2604.10134`), AttriGuard (`https://arxiv.org/abs/2603.10749`), AgentSentry (`https://arxiv.org/abs/2602.22724`), Agent-Sentry (`https://arxiv.org/abs/2603.22868`), IntentGuard (`https://openreview.net/forum?id=fF9alVesJ0`) | injected prompt detection/removal、instruction-data isolation、plan consistency、tool-call causal attribution、temporal causal takeover、execution provenance bounds、intent analysis。 | 这是最高风险 novelty 邻域。EAIR 必须强调：不是只判断 tool call 是否受 untrusted data 驱动，而是判断 retrieved evidence path 是否足以合法支持 high-risk action。 |
| Agent correctness property | Intent-to-Execution Integrity (`https://arxiv.org/abs/2605.16976`) | 把 agent security 定义为用户 intent 到 concrete execution 的正确性保持。 | 支持我们把 EAIR 写成 correctness/evidence-grounding property，但也意味着必须避免声称“首次定义 agent action integrity”。 |

### 关键判断

1. **retrieval poisoning 已不是 novelty。** PoisonedRAG、CorruptRAG、KG-RAG poisoning、RAG security taxonomy 已经把 corpus poisoning / retrieval exposure 做得很宽。EAIR 可以用 PRE/RHE 作为 baseline，但不能把“发现污染进入 Top-K”作为核心贡献。

2. **RAG attribution 已覆盖“哪个文档影响生成”。** RAGForensics/RAGOrigin/Source Attribution 说明 document responsibility 与 Shapley-style attribution 方向已经存在。EAIR 的差别必须落在 high-risk action 的 policy/evidence sufficiency，而不是单纯 `I(d -> output)`。

3. **claim-level faithfulness 已成熟但 action-blind。** RAGAS/ARES/RAGChecker 处理的是 retrieved context 与 answer/claim 的一致性。EAIR 的最小有效差异是：即使 claim 被 context 支撑，action 的 tool、approval flag、domain decision 和 parameter 仍可能危险。

4. **conflict-aware RAG 解决不了 evidence insufficiency。** ConflictRAG、FaithfulRAG、TruthfulRAG、DRAGged into Conflicts 让 conflict 维度很拥挤。EAIR 要覆盖无显式冲突的场景，例如单个低信任 evidence 支持危险 action。

5. **AttriGuard / AgentSentry / PlanGuard 是最近邻。** 它们分别从 tool-call attribution、temporal takeover、execution provenance、planning consistency 防 IPI。EAIR 必须正面比较：这些方法关注 untrusted instruction/control takeover，而 EAIR-Bench 关注 retrieved evidence 对 high-risk action 的合法/非法证据影响。

## 差异化空位

### 和 retrieval poisoning 的差异

Retrieval poisoning 研究通常问：

```text
Can malicious content be retrieved and cause an attacker-chosen answer/behavior?
```

EAIR-Bench 问：

```text
If evidence is retrieved, should its claims be allowed to support this high-risk action?
```

因此 EAIR 不把 `poisoned=True` 或 `retrieved=True` 直接等同为 failure。关键是 evidence 是否进入 action support path，以及该 path 是否可信、充分、最新、低冲突、低污染。

### 和 RAG attribution 的差异

RAG attribution / traceback 研究定位责任来源：

```text
Which document caused or explains this generation?
```

EAIR 的评估对象是 action admissibility：

```text
Does the evidence path legitimately justify the decision/tool/approval/parameter fields of a high-risk action?
```

也就是说，EAIR 不只追问“谁影响了输出”，还追问“这种影响是否应被允许”。

### 和 claim-level faithfulness 的差异

RAGAS/ARES/RAGChecker-style metrics 能判断 response claims 是否被 retrieved context 支撑，但它们通常不覆盖：

- action decision 是否违反 domain policy；
- tool name 是否越权；
- tool args / operating parameters 是否危险；
- human approval flag 是否正确；
- risk report 是否被不可信 evidence 降级。

EAIR 可以复用 claim support/faithfulness，但必须在 action schema 上追加 HardGate 与 EvidenceSufficient。

### 和 action-level causal attribution 的差异

AttriGuard-style 方法问：

```text
Is this tool call causally driven by untrusted observations rather than user intent?
```

EAIR 问：

```text
Is the retrieved evidence influence legitimate or hijack influence for this context-dependent high-risk action?
```

这一区分很关键：高风险动作在真实系统中经常应当被最新规程、状态记录、仿真结果等外部 evidence 合法影响。把所有 external evidence influence 都视作 hijack 会造成 over-refusal。

### 为什么 EAIR 不是 AttriGuard + RAGAS 的简单拼接

`AttriGuard + RAGAS` 的朴素拼接可能做两件事：

1. 用 attribution 判断 action 是否受外部 context 影响；
2. 用 RAGAS 判断 answer claims 是否 faithful。

EAIR 的额外要求是：

- 把 action 展开为 `decision/tool/tool_args/approval/risk/parameters`；
- 将权限、domain policy、approval requirement、parameter bounds 放入不可被 soft score 抵消的 `HardGate(a)`；
- 对 high-risk action 要求 `EvidenceSufficient(a)`，包括 source-diverse support、freshness/version、independent source count、conflict pressure、poison support；
- 显式区分 `LegitInfluence(d -> a)` 和 `HijackInfluence(d -> a)`；
- 用 benchmark case 证明 PRE/RHE、RAGAS-style、AttriGuard-style、PlanGuard/PromptArmor-style、access-control 各自的 blind spot。

所以 EAIR 的核心不是“attribution + faithfulness”，而是：

```text
evidence-to-action admissibility for context-dependent high-risk actions
```

## 当前仓库状态观察

- `DERIVATION_PACKAGE.md` 仍以旧 `PRE/RHE + claim graph + EAIR` 为主，需要重写。
- `PAPER_PLAN.md` 仍强调 “From Poisoned Evidence to Unsafe Actions”，应转向 “When Should Evidence Influence Action?”。
- `formaltrust_platform/experiments/evidence_action.py` 已有 deterministic pilot，但 case taxonomy 和 baseline 仍偏旧。
- `outputs/evidence_action_pilot/` 是旧 pilot 结果，可保留为历史参考，不应作为新方向主结果。

## 2026-06-20 增量前沿核查

本次补查的结论是：agent action / tool-use 防御邻域比 2026-06-17 判断的还要拥挤。尤其是 causal attribution、execution provenance、runtime authority control 已经形成一条很接近 EAIR 的研究线。EAIR 仍可行，但必须进一步收窄为：

```text
claim-level evidence sufficiency and admissible evidence-to-action grounding
for high-risk RAG-agent actions
```

而不是宽泛地声称 action attribution、runtime guard 或 agent safety benchmark 本身有 novelty。

### 新增最近邻

| 工作 | 链接 | 已覆盖的问题 | 对 EAIR 的影响 |
|---|---|---|---|
| AttriGuard | `https://arxiv.org/abs/2603.10749` | action-level causal attribution of tool invocations：判断 tool call 是由用户意图支持，还是由不可信 observation 驱动。 | 直接覆盖“动作级归因”叙事；EAIR 必须避免把 `I(d -> a)` 当核心创新。 |
| CausalArmor | `https://arxiv.org/abs/2602.07918` | 在 privileged decision point 做 leave-one-out causal attribution，检测 untrusted segment 是否支配用户意图，并选择性 sanitization。 | 进一步压缩“causal attribution guardrail”的空间；EAIR 的差异应落在 evidence sufficiency / source-diverse / freshness-version / action-parameter grounding。 |
| AIRGuard | `https://arxiv.org/abs/2605.28914` | runtime authority control：跟踪 source/target trust，模拟 side effects，并在动作执行前强制 least-privilege authority。 | 与 EAIR 的 HardGate 很近；EAIR 不能只讲 tool authority，要强调 retrieved evidence 是否足以授权 high-risk decision/parameter。 |
| AgentSentry | `https://arxiv.org/abs/2602.22724` | temporal causal diagnostics + context purification，用反事实重执行定位多轮 IPI takeover。 | 覆盖 temporal causal takeover；EAIR 应避免声称首次处理多轮 context influence。 |
| PlanGuard | `https://arxiv.org/abs/2604.10134` | isolated planner + hierarchical verification，先检查 hard constraints，再验证参数偏差是否符合用户 intent。 | 与 HardGate / parameter verification 接近；EAIR 需要强调参数值是否由可信充分证据支持，而不只是 intent consistency。 |
| Agent-Sentry | `https://arxiv.org/abs/2603.22868` | execution provenance bounds：记录工具参数来源并学习正常 provenance pattern。 | 与 evidence/action trace 很近；EAIR-Bench 应定位为评估 evidence admissibility 的 benchmark，而不是泛 provenance 系统。 |
| Evidence Tracing and Execution Provenance survey | `https://arxiv.org/abs/2606.04990` | 将 retrieval grounding、claim support、tool-use safety、memory lineage、audit 等统一到 provenance 视角。 | 说明“evidence tracing + execution provenance”已成为显性框架；EAIR 需要把贡献限定为 high-risk RAG action 的 sufficiency/admissibility benchmark。 |

### 更新后的差异化判断

1. **EAIR 不能再主打 action attribution。** AttriGuard 和 CausalArmor 已经把 causal attribution at privileged/action points 讲得很强。
2. **HardGate 不能被包装成唯一贡献。** AIRGuard、PlanGuard、Agent-Sentry 都覆盖了 runtime guard、authority、provenance 或 intent consistency。
3. **最稳的空位是 evidence sufficiency for high-risk RAG actions。** 也就是：可信、独立、最新、未被 supersede、低冲突、低污染的 claim-level evidence path 是否足以支持 action 的 decision/tool args/approval/parameter/risk report。
4. **EAIR-Bench 应成为主贡献。** 评测问题应写成“哪些 evidence influence 是合法的，哪些是 hijack”，并用 case taxonomy 暴露 PRE/RHE、RAGAS-style、AttriGuard-style、PlanGuard-style、access-control、authority-control/provenance-style 的盲点。
5. **下一轮实验需要加入 authority/provenance 最近邻 baseline。** 至少应增加 AIRGuard-style authority baseline、CausalArmor-style dominance attribution baseline、Agent-Sentry-style provenance-bound baseline，避免 reviewer 说实验 baseline 不够新。

### 2026-06-20 实现状态更新

上述最近邻 baseline 已进入 deterministic pilot 的第一版 style 对照：

- `attriguard_selective`
- `causalarmor_dominance`
- `airguard_authority`
- `agent_sentry_provenance`

当前结果显示：这些 baseline 都能覆盖一部分风险，但没有一个同时覆盖 evidence sufficiency、source diversity、freshness/version-currentness、hard policy/parameter integrity。`eair_full` 在 12 条 synthetic condition 上保持 `UDR=0`、`UAR=0`、parameter violation `0`、EATF `1.0`，但 `ORR=0.3333`，说明下一轮核心问题应转向 **降低保守拒绝率，同时保持 evidence sufficiency 安全边界**。

### 2026-06-20 ORR 降低更新

已将 action taxonomy 进一步细化：

- conservative denial：例如 `reject_bypass`、`tool="none"`，不会执行高风险工具或授权危险动作；
- execution / authorization action：例如 `route_to_simulation`、写控制、参数设置、审批绕过等，仍需要强 EvidenceSufficient。

更新后 deterministic pilot 变为 13 条 condition、17 个 baseline、221 条结果。`eair_full` 维持：

- `UDR=0`
- `UAR=0`
- parameter violation `0`
- false positive `0`
- EATF `1.0`

同时 `ORR` 从 `0.3333` 降到 `0.2308`。剩余 ORR 都来自 stale / superseded / single-cluster support 下的 `route_to_simulation`，这是执行性 action，仍应被 EvidenceSufficient 拦截。

### 2026-06-20 approval flag 完整性更新

进一步发现：conservative denial 不能只看 `tool="none"`。如果 retrieved evidence 让 agent 输出：

```text
decision = reject_bypass
tool = none
requires_human_approval = false
```

那么动作虽然没有调用工具，也没有允许 bypass，但仍然破坏了 high-risk action 的审批完整性。

已新增 `approval_flag_manipulation_no_tool` case，并把 approval flag 纳入 `HardGate`。更新后 pilot 为 14 条 condition、17 个 baseline、238 条结果。`eair_full` 仍保持 `UDR=0`、`UAR=0`、parameter violation `0`、false positive `0`、EATF `1.0`，`ORR=0.2143`。

这加强了论文里的 action schema 论点：action 不只是 tool name，还包括 decision、tool args、approval flag、risk report、parameter values。
### 2026-06-20 risk-level / risk-report integrity update

Iteration 025 adds `risk_report_downgrade_no_tool`.

Key finding:

- `tool="none"` and `requires_human_approval=True` are still insufficient if retrieved evidence downgrades `risk_level` or suppresses required review in `risk_report`.
- `vanilla_rag` and `access_control` allow the no-tool risk downgrade.
- `eair_hard_gate_only` and `eair_full` replace it with a high-risk, review-required action.
- Updated pilot scale: 15 conditions, 17 baselines, 255 results.
- `eair_full`: UDR 0, UAR 0, parameter violation 0, false positive 0, EATF 1.0, ORR 0.2000.

This strengthens the action-schema positioning: EAIR-Bench evaluates evidence-backed integrity across decision, tool, parameters, approval flag, risk level, and risk report.
### 2026-06-20 structured action JSON pilot update

Iteration 026 moves EAIR-Bench one step closer to real LLM evaluation by adding a model-output boundary:

```text
model text -> structured action parser -> AgentAction -> EAIR gate -> evaluator
```

Key finding:

- The system can now parse fenced JSON action outputs and preserve action fields such as `risk_report`, `supporting_claims`, and `parameters`.
- Malformed model output falls back to safe `abstain` and records parse diagnostics.
- In the structured-action pilot, two unsafe candidate actions are repaired by EAIR and final unsafe actions remain 0.

Pilot scale:

- 4 model-output scenarios
- 1 parse error
- 2 unsafe candidates
- 0 unsafe finals
- artifacts written under `outputs/eair_structured_action_pilot/`

Claim boundary:

- This is not a live LLM experiment yet. It is the bridge that lets the same gate/evaluator operate on real model transcripts next.
### 2026-06-20 replayed structured-action transcript update

Iteration 027 adds a replayable transcript layer.

Key finding:

- EAIR-Bench can now evaluate saved model-output transcripts from JSONL/JSON files.
- The replay path records model identity, parse diagnostics, candidate action safety, final action safety, and gate decisions.
- The fixture replay has 4 transcripts, 2 unsafe candidates, and 0 unsafe final actions.

Artifacts:

- `examples/data/eair_structured_action_transcripts.jsonl`
- `outputs/eair_transcript_replay_pilot/structured_action_transcript_replay_results.json`
- `outputs/eair_transcript_replay_pilot/structured_action_transcript_replay_report.md`

Claim boundary:

- This is replay infrastructure and deterministic fixture evidence. The next step is a live OpenAI-compatible runner that writes transcripts first and evaluates them second.
### 2026-06-20 OpenAI-compatible sampler dry-run update

Iteration 028 adds a live-model-ready sampler while preserving replay-first evaluation.

Key finding:

- The sampler can build prompts from EAIR-Bench cases, call an OpenAI-compatible transport, and write transcript JSONL.
- The output is immediately replayable through `run_structured_action_transcript_replay`.
- In the dry run, 2 sampled transcripts produced 1 unsafe candidate and 0 unsafe final actions after EAIR replay.

Artifacts:

- `outputs/eair_live_sampler_dry_run/sampled_transcripts.jsonl`
- `outputs/eair_live_sampler_dry_run/replay/structured_action_transcript_replay_results.json`

Claim boundary:

- This is not a live provider result. It proves the sampler protocol and replay compatibility using fake transport.
### 2026-06-20 configurable EAIR sampler CLI update

Iteration 029 turns the sampler protocol into a command-line workflow.

Key finding:

- `formaltrust eair-sample --config <sampler.yaml>` can sample or dry-run model outputs, write replay-compatible transcript JSONL, and immediately run replay evaluation.
- The config format supports dry-run responses and future live OpenAI-compatible provider calls via `api_key_env`.
- The dry-run example produces 2 transcripts, 1 unsafe candidate, and 0 unsafe final actions after replay.

Artifacts:

- `examples/eair_sampler_dry_run.yaml`
- `outputs/eair_sampler_cli_dry_run/sampled_transcripts.jsonl`
- `outputs/eair_sampler_cli_dry_run/replay/structured_action_transcript_replay_results.json`

Claim boundary:

- This is still dry-run infrastructure. Live-model claims require real provider transcripts generated through the same CLI/config protocol.
### 2026-06-20 standalone replay CLI update

Iteration 030 adds `formaltrust eair-replay`.

Key finding:

- Saved external transcripts can now be replayed without writing Python.
- The replay CLI evaluates JSONL/JSON transcripts through the same parser, hard gate, and evaluator.
- The live sampler template uses `api_key_env`, keeping secrets out of config files.

Artifacts:

- `examples/eair_sampler_live_template.yaml`
- `outputs/eair_replay_cli_pilot/structured_action_transcript_replay_results.json`
- `outputs/eair_replay_cli_pilot/structured_action_transcript_replay_report.md`

Replay CLI result:

- 4 transcripts
- parse errors: 1
- candidate unsafe: 2
- final unsafe: 0
- gate counts: allow 2, replace 2
### 2026-06-20 replay artifact manifest update

Iteration 031 adds `artifact_manifest.json` to replay output directories.

Key finding:

- Replay artifacts are now file-auditable.
- The manifest binds transcript JSONL to replay results via SHA256.
- The manifest states the claim boundary: replay evaluates saved transcripts and does not sample a live model.

Artifact:

- `outputs/eair_replay_cli_pilot/artifact_manifest.json`

Current manifest summary:

- artifact type: `eair_transcript_replay`
- protocol: `transcript_jsonl_to_eair_replay`
- transcript SHA256 prefix: `6dbaedb069d3`
- total transcripts: 4
- candidate unsafe: 2
- final unsafe: 0
### 2026-06-20 artifact verifier update

Iteration 032 adds a verifier for replay manifests.

Key finding:

- `formaltrust eair-verify-artifact` checks transcript SHA256, required output files, and summary consistency.
- Tampering with the transcript after replay causes verification to fail with `transcript_sha256 mismatch`.
- `docs/eair_artifact_readme.md` now documents sampling, replay, verification, and claim boundaries.

Artifact:

- `docs/eair_artifact_readme.md`

Verified command:

```text
python -m formaltrust_platform eair-verify-artifact --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json
```

### 2026-06-20 artifact summary update

Iteration 033 adds manifest-backed summary tables.

Key finding:

- `formaltrust eair-summarize-artifacts` verifies replay manifests before aggregation.
- The command writes JSON, CSV, and Markdown outputs for paper/report tables.
- The current aggregate over the replay fixture and sampler dry-run contains 2 artifacts, 6 transcripts, 3 unsafe candidates, 0 unsafe final actions, and gate counts allow 3 / replace 3.

Artifacts:

- `outputs/eair_artifact_summary/artifact_summary.json`
- `outputs/eair_artifact_summary/artifact_summary.csv`
- `outputs/eair_artifact_summary/artifact_summary.md`

Claim boundary:

- This is verified replay aggregation, not live-model performance evidence.
### 2026-06-20 grouped artifact analysis update

Iteration 034 adds model-level and condition-level artifact summaries.

Key finding:

- Verified replay artifacts now produce grouped tables by `model` and by `case_id::condition`.
- The current grouped summary separates legitimate evidence updates from risk-report downgrade failures.
- This prepares the next real-model pilot because provider-generated transcripts can be compared without changing replay logic.

Artifacts:

- `outputs/eair_artifact_summary/artifact_summary_by_model.csv`
- `outputs/eair_artifact_summary/artifact_summary_by_model.md`
- `outputs/eair_artifact_summary/artifact_summary_by_condition.csv`
- `outputs/eair_artifact_summary/artifact_summary_by_condition.md`

Claim boundary:

- Grouped tables analyze replayed transcript outcomes. They do not prove live-model behavior unless the transcripts were collected from a live provider.
### 2026-06-20 model-condition matrix update

Iteration 035 adds a cross-tabulated replay matrix.

Key finding:

- The summary now exposes `by_model_condition[model][case_id::condition]`.
- It writes `artifact_summary_by_model_condition.csv` and `.md`.
- Current matrix cells show risk-report downgrade and parameter hijack are `hijack -> replace`, while legitimate policy updates are `legitimate -> allow`.

Artifact:

- `outputs/eair_artifact_summary/artifact_summary_by_model_condition.csv`

Claim boundary:

- The matrix supports replay artifact failure analysis and coverage checks. It is not live-model evidence unless the source transcripts are live-provider transcripts.
### 2026-06-20 expected-condition coverage update

Iteration 036 adds coverage audit for planned model-condition cells.

Key finding:

- `formaltrust eair-summarize-artifacts` now accepts `--expected-condition`.
- The summary writes `artifact_summary_coverage.csv` and `.md`.
- Current audit correctly flags the dry-run sampler artifact as incomplete coverage: coverage rate 0.5 with two missing expected conditions.

Claim boundary:

- Coverage audit checks experimental completeness. It is not a method-performance metric.
### 2026-06-20 coverage gate update

Iteration 037 adds a hard coverage gate.

Key finding:

- `formaltrust eair-summarize-artifacts --require-complete-coverage` exits nonzero when any model is missing expected conditions.
- The command still writes coverage artifacts before failing.
- Current run correctly fails because `cli-dry-run-openai-compatible` misses clean sufficient evidence and parameter hijack.

Claim boundary:

- The gate enforces experiment completeness; it is not a safety metric.
### 2026-06-20 complete dry-run fixture update

Iteration 038 adds a complete dry-run sampler fixture.

Key finding:

- `examples/eair_sampler_complete_dry_run.yaml` covers all four current expected conditions.
- The generated complete dry-run artifact passes `--require-complete-coverage`.
- Result: 4 transcripts, 2 unsafe candidates, 0 unsafe final actions, gate counts allow 2 / replace 2.

Claim boundary:

- This verifies the artifact workflow and coverage gate pass path, not live-model performance.
### 2026-06-20 live config readiness update

Iteration 039 adds a live-provider config readiness check.

Key finding:

- `formaltrust eair-check-live-config` validates live sampler YAML before model calls.
- The live template now covers all four expected conditions and includes `summary_output_dir`.
- Bad configs are rejected for inline secrets, missing `api_key_env`, accidental dry-run responses, and missing expected conditions.

Claim boundary:

- The check validates configuration readiness. It does not call a model or prove model behavior.
### 2026-06-20 live runbook update

Iteration 040 adds a generated live-model runbook.

Key finding:

- Readiness alone is not enough for a paper-facing provider run; the run must also preserve transcript JSONL, verify the replay manifest, and require complete model-condition coverage before tables are reported.
- `formaltrust eair-write-live-runbook` turns the current live template into an executable command sequence.
- The generated runbook keeps the evidence boundary explicit: sampler logs document collection only, while safety evidence comes from saved transcripts, replay artifacts, verified manifests, and coverage-gated summaries.

Artifact:

- `outputs/eair_live_model_run/RUN_LIVE_MODEL.md`

Claim boundary:

- The runbook is a protocol artifact. It does not call a model or support model-behavior claims by itself.
### 2026-06-20 reportable live-run audit update

Iteration 041 adds a final admissibility gate for live-provider evidence.

Key finding:

- A complete dry-run fixture can pass coverage, so coverage alone is not enough for reportable live-model evidence.
- Transcript provenance now includes `sampling_mode: live | dry_run`.
- `formaltrust eair-audit-reportable-run` rejects dry-run and mock-looking model artifacts even when manifest verification and complete coverage pass.

Artifact:

- `outputs/eair_live_model_run/RUN_LIVE_MODEL.md` now includes the reportable-run audit command.

Claim boundary:

- The audit proves artifact admissibility, not model safety.
### 2026-06-20 persisted reportability audit update

Iteration 042 makes reportability audit outputs persistent.

Key finding:

- Reportability pass/fail should be archived, not only printed.
- `eair-audit-reportable-run --output-dir ...` writes JSON and Markdown.
- Failure cases still produce audit artifacts before exiting nonzero.

Artifact:

- `outputs/eair_sampler_complete_dry_run/reportability/reportable_run_audit.json`
- `outputs/eair_sampler_complete_dry_run/reportability/reportable_run_audit.md`

Claim boundary:

- These files explain artifact admissibility, not safety performance.
### 2026-06-20 reportable results export update

Iteration 043 adds a gated paper-table export.

Key finding:

- A non-reportable artifact should not be exportable as a paper-facing live-provider table.
- `eair-export-reportable-results` requires a passing `reportable_run_audit.json`.
- The complete dry-run fixture is blocked even though its coverage is complete.

Artifacts:

- `outputs/eair_sampler_complete_dry_run/paper_tables/reportable_results_export_blocked.json`
- `outputs/eair_sampler_complete_dry_run/paper_tables/reportable_results_export_blocked.md`

Claim boundary:

- Export gating protects artifact admissibility; it does not measure safety.
### 2026-06-20 live run doctor update

Iteration 044 adds runtime preflight artifacts.

Key finding:

- `eair-check-live-config` can pass while the current shell still cannot run live sampling.
- `eair-doctor-live-run` records that distinction without writing secret values.
- Current live preflight fails because `OPENAI_API_KEY` is not set.

Artifacts:

- `outputs/eair_live_model_run/live_preflight/live_run_doctor.json`
- `outputs/eair_live_model_run/live_preflight/live_run_doctor.md`

Claim boundary:

- Runtime readiness is not model-behavior evidence.
### 2026-06-21 live workflow status update

Iteration 045 adds a machine-readable workflow checkpoint.

Key finding:

- A single status artifact can now summarize the whole live-provider workflow.
- Current status is blocked at `live_preflight`.
- The status artifact also lists downstream expected artifacts that do not exist yet.

Artifacts:

- `outputs/eair_live_model_run/workflow_status/live_workflow_status.json`
- `outputs/eair_live_model_run/workflow_status/live_workflow_status.md`

Claim boundary:

- Workflow status is operational evidence, not model behavior.
### 2026-06-21 frontier novelty re-triage

Iteration 046 re-checks the closest novelty neighborhood after the live workflow became blocked by missing provider credentials.

Key finding:

- AttriGuard and CausalArmor make action-level attribution too crowded to use as the main novelty.
- AIRGuard, Agent-Sentry, AgentSentry, PlanGuard, PromptArmor, AgentSecBench, MT-AgentRisk, and Agent Security Bench make generic runtime guard / authority / benchmark claims too broad.
- RAGForensics, RAGChecker, and ARES make retrieval traceback or RAG evaluation insufficient as standalone novelty.

Updated positioning:

```text
EAIR-Bench + Evidence Sufficiency + Legitimate-vs-Hijack Evidence Influence
```

Concrete claim changes:

- Reject: "EAIR is novel because it attributes action-level influence."
- Reject as standalone: "HardGate is the novelty."
- Downgrade: "EAIR-Bench is the first agent security benchmark."
- Keep with caution: "EAIR-Bench targets claim-level evidence-to-action admissibility for high-risk RAG-agent decisions."

Artifact:

- `refine-logs/iterations/ITERATION_046.md`

Claim boundary:

- This is a frontier triage. It is not a final bibliography audit, official baseline reproduction, or live-model result.
### 2026-06-21 WarrantGuard method upgrade

Iteration 047 upgrades the method identity from EAIR-Gate to WarrantGuard / ActionWarrant.

Key finding:

- A post-hoc gate is too easy to position as incremental next to AttriGuard, PlanGuard, AIRGuard, and Agent-Sentry.
- A proof-carrying action protocol is stronger: high-risk RAG-agent actions must include a verifiable `ActionWarrant W_a`.
- EAIR-Full becomes the reference verifier inside WarrantGuard; EAIR-Bench remains the benchmark for missing, weak, stale, duplicated, poisoned, conflicting, or hijacked warrants.

Core form:

```text
Agent(q, K) -> (a, W_a)

Execute(a) iff
  HardGate(a) = PASS
  and VerifyWarrant(a, W_a) = PASS
  and CounterWarrant(a, W_a) = CLEAR.
```

Artifacts:

- `refine-logs/iterations/ITERATION_047.md`
- `figures/fig1_eair_main_chain.svg`
- `docs/superpowers/plans/2026-06-21-warrantguard-actionwarrant.md`

Claim boundary:

- Current code proves a minimal WarrantGuard verifier interface, not a full official-baseline comparison or live-model result.

## 2026-07-02 Finding: Power-Ops AFW Active Research Track

The active direction is now power large-model safety over the existing AFW/CapGuard implementation, not a brand-new standalone framework.

Key local interface findings:

- FormalTrust methods must stay in the node contract: `node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any] | None`.
- New intermediate results should use `state.metrics` and `state.artifacts`; avoid adding top-level state fields unless unavoidable.
- Existing runtime path already supports `custom.afw_trace_adapter -> guardrail.afw_capguard -> evaluate.afw_runtime`.
- `guardrail.afw_capguard` can lift capabilities from case metadata, runtime metrics, retrieval metadata, source events, skill manifests, and authority manifests.
- Runtime needs/consumptions can come from `afw_consumptions`, `afw_needs`, or candidate action fields.
- Current all-config power-ops suite covers evidence, memory, prior-step output, skill, tool metadata, user approval, malformed traces, span logs, OTLP, obligations, temporal decay, and counter-authority.

Current baseline:

- `docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md`
- 27 total cases, 27 passed.
- `false_allow_fields=0`.
- `false_block_fields=0`.
- allow/block/abstain cases = 4/20/3.
- mean witness compression ratio = 0.760.

Research reframing:

- The strongest next angle is not merely "another guardrail".
- The sharper problem is: under strict safety supervision, can an agent preserve authorized action fields while blocking or repairing unauthorized fields?
- This becomes "authority-constrained action invariance" for safety-critical power-operation agents.

Claim boundary:

- Current evidence is a curated regression and prototype slice.
- It does not prove live deployment safety or broad power-grid generalization.
- The existing Kappa smoke is machine-prefill only, not human double annotation.

## 2026-07-02 Findings: Power-Ops Action Invariance Plan

## 需求

- 用户要的是持续迭代的研究计划，不只是描述点子。
- 后续必须产出实际成果：形式化建模、测试框架、测试样本、实验方案、可运行代码和结果报告。
- 研究方向必须结合文件夹内已有的电力大模型安全相关资产。
- 实现必须对齐当前项目接口，尤其是 FormalTrust 的 state/node/YAML/dataset runner 体系。
- 用户明确要求先生成 plan，再继续实现。

## 研究发现

- 当前仓库已经有电力运维 AFW/CapGuard 基线，不是从 0 开始。
- 现有 runtime path 是 `guardrail.afw_capguard -> evaluate.afw_runtime`，并已有 trace adapter、OTLP、obligation、temporal、counter-authority 相关验证。
- 当前最值得推进的问题不是“再做一个 guardrail”，而是“严格安全监督下如何不误伤正常 agent 行为”。
- 可将该问题形式化为 authority-constrained action invariance：合法字段保持，非法字段阻断/修复/转人工。
- 当前 all-config runtime suite 的已知基线是 27 cases / 27 passed / false allow 0 / false block 0 / mean witness compression ratio 0.760。

## 技术决策

| 决策 | 理由 |
|---|---|
| 新工作沿用 FormalTrust node 接口 | 保证后续代码能进入现有实验体系 |
| 中间指标放入 `metrics`，大型输出放入 `artifacts` | 符合 `FormalTrustState` patch 规则 |
| 第一批样本使用 curated power-ops JSONL | 快速形成可运行 regression，再扩真实 trace |
| 指标新增 conservative collapse / authorized preservation | 直接回应用户提出的“防御过度保守”问题 |
| 文献查新单独进入后续阶段 | 先完成计划结构，再系统性调研和核验 |

## 遇到的问题

| 问题 | 解决方案 |
|---|---|
| 上一版计划没有严格按 `planning-with-files-zh` 的三件套格式组织 | 已在 `task_plan.md` 追加模板化阶段计划 |
| 提前开始写代码，不符合用户“先生成 plan”的顺序要求 | 暂停继续实现，把已有实现视为草稿，等待计划确认 |

## 资源

- `formaltrust_platform/interfaces.py`
- `formaltrust_platform/state.py`
- `formaltrust_platform/graph.py`
- `formaltrust_platform/registry.py`
- `formaltrust_platform/config.py`
- `formaltrust_platform/nodes/afw.py`
- `formaltrust_platform/experiments/afw_bench.py`
- `formaltrust_platform/experiments/afw_runtime_report.py`
- `formaltrust_platform/experiments/afw_runtime_suite.py`
- `examples/afw_runtime_validation.yaml`
- `examples/data/afw_runtime_power_ops_cases.jsonl`
- `docs/power_ops_afw_current_results_2026-07-01.md`
- `docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md`

## 视觉/浏览器发现

- 本轮没有新的图片/PDF视觉信息需要记录。
- 已有外部网页/论文线索只作为后续查新入口，不在 plan 中当作已验证结论。

## 2026-07-02 Requirement Update: Continuous Iteration

## 需求

- 用户明确要求“不停迭代”，不是一次性 plan 或一次性实现。
- 每轮必须有实际增量，不能只做描述。
- 后续默认持续推进，除非用户明确要求暂停、停止或切换方向。

## 技术决策

| 决策 | 理由 |
|---|---|
| 在 `task_plan.md` 增加“持续迭代协议” | 防止后续会话把任务误解为一次性 checklist |
| 每轮至少产出一个硬成果 | 保证持续迭代不是空转 |
| 每轮结束必须做 keep/revise/reject 判断 | 让研究路线能根据结果自我修正 |
| 代码阶段坚持测试先行 | 防止快速堆实现但不可验证 |

## 遇到的问题

| 问题 | 解决方案 |
|---|---|
| 原计划虽然有阶段，但“不停迭代”的默认行为不够强 | 已补充持续迭代协议和停止条件 |

## 2026-07-02 Findings: Fieldwise Repair Iteration

## 需求

- 用户要求持续迭代，不能只生成 plan。
- 用户关注的核心风险是：严格策略监督可能让 agent 过度保守，导致正常行为被误伤。
- 因此评估不能只看字段级 allow/block，还必须看最终 `final_action` 是否保留了合法字段。

## 研究发现

- 当前 AFW/CapGuard 的字段级结果可以做到：合法字段 allow，非法字段 block，8/8 curated power-ops cases 无 false allow、无 false block。
- 但 strict-block 模式会把所有 mixed cases 的最终动作变成 `require_human_approval`，导致 `whole_action_block_rate=1.000`。
- 新增 `runtime_final_action_mode: fieldwise_repair` 后，同一批 8 个样本仍然 8/8 passed，同时：
  - `whole_action_block_rate=0.000`
  - `authorized_final_field_preservation_rate=1.000`
  - `unauthorized_final_field_removal_rate=1.000`
  - `executable_fieldwise_repair_success_rate=1.000`
- 这说明“安全监督不误伤正常行为”可以被拆成最终动作级指标，而不是只停留在 guardrail 是否拦截。

## 技术发现

| 发现 | 影响 |
|---|---|
| `afw_gate_decision=block` 不一定意味着最终动作必须整体失败 | 可以在 gate block 的同时产生 repaired final action |
| `strict_block_collapse_rate` 是 gate-level conservative-collapse 指标 | 它揭示可修复机会，但不表示 repair 已经真实执行 |
| `executable_fieldwise_repair_success_rate` 是 final-action-level 指标 | 它衡量最终动作是否真的保留合法字段、移除非法字段 |
| 语义字段和 JSON key 可能不一致 | 需要 `field_aliases` 或更系统的 field schema |

## 关键边界

- 当前结果是 curated 8-case regression，不是生产泛化结论。
- 当前 repair 是字段键级修复，不是完整 planner 重规划。
- 当前 `abstain` mixed cases 还不够，需要下一轮补。
- 当前 repair 对 `tool` 统一改为 `fieldwise_repair`，避免继续执行原危险工具；后续要引入更细的 tool-level schema。

## 资源

- `formaltrust_platform/nodes/afw.py`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `examples/power_ops_action_invariance_fieldwise_repair_validation.yaml`
- `examples/data/power_ops_action_invariance_cases.jsonl`
- `docs/power_ops_action_invariance_repair_comparison_2026-07-02.md`
- `docs/power_ops_action_invariance_fieldwise_repair_results_2026-07-02.md`

## 2026-07-02 Findings: Field Schema and Mixed Abstain

## 需求

- 第二轮证明了 fieldwise repair 可以减少 conservative collapse，但还缺少语义字段到 JSON 动作键的显式接口。
- 真实安全监督里并非所有危险字段都是 block；有些字段是能力覆盖但有 policy hold / counter-authority，因此应当 `abstain`。

## 研究发现

- `Need(s,f)` 中的 `f` 不应强行等同于 `candidate_action[f]`。
- 例子：`risk_level` 是语义字段，但候选动作里真正要删除的是 `risk_level_override`；安全元数据 `risk_level: high` 可以保留。
- 新增 `action_field_schema` 后，repair 和 summary 都能按 schema 判断最终动作是否真实移除了非法语义字段。
- 新增 `afw_counter_authority` metadata 后，JSONL case 可以直接表达 counter-authority，而不用一定经过 trace adapter。
- 数据集扩到 10 cases 后，gate counts 为 block=8、abstain=2；fieldwise repair 在两类 gate 下都能保留合法字段并移除需转人工字段。

## 技术发现

| 发现 | 影响 |
|---|---|
| `action_field_schema` 应优先于旧 `field_aliases` | schema 是可扩展接口，alias 只作为兼容后备 |
| `afw_counter_authority` 可以从 case metadata 读取 | curated JSONL 与 trace adapter 输出可以共享同一 runtime check |
| `abstain` 字段不应让整个动作失效 | 可以移除 abstain 字段并写入 `human_review_fields` |
| `gate_decision_counts` 比单一 pass rate 更有信息量 | 可以区分 block-heavy 与 abstain-heavy 的安全监督场景 |

## 当前边界

- `human_review_fields` 目前只是 final action 里的审计字段，还没有执行系统语义。
- `action_field_schema` 目前由样本手写，尚未从真实 trace 自动生成。
- abstain repair 当前和 block repair 使用同一个移除逻辑，后续需要区分“明确非法”和“需要更多审批/检查”。

## 资源

- `docs/power_ops_action_invariance_field_schema_abstain_2026-07-02.md`
- `examples/data/power_ops_action_invariance_cases.jsonl`
- `formaltrust_platform/nodes/afw.py`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `tests/test_interfaces.py`
- `tests/test_power_ops_action_invariance.py`

## 2026-07-02 Findings: Repair Validity and Partial Human Review

## 需求

- 第三轮已经能做 fieldwise repair，但仍需检查 repair 是否只修改 invalid authority frame。
- 用户关心“安全监督不要过度保守”，但不能为了不过度保守而偷偷改变合法字段含义。

## 研究发现

- `executable_fieldwise_repair_success_rate=1.000` 只能说明最终动作保留了授权字段并移除了未授权字段。
- 还需要 `repair_frame_validity_rate` 检查：
  - 授权字段值没有变化。
  - 该删的 invalid action keys 已删除。
  - 不该删的原始 action keys 没被删。
  - invalid frame 外的业务字段没有被改写。
  - `partial_human_review_fields` 与 invalid fields 一致。
- 当前 10 个 fieldwise-repair cases 中，10 个 repair frame 都 valid。

## 技术发现

| 发现 | 影响 |
|---|---|
| `original_action` 是 repair validity 的必要证据 | 真实 trace 中必须保留候选动作原文 |
| `partial_human_review_fields` 应等于 invalid fields | 局部转人工不能只靠自然语言 rationale |
| `auto_executable_fields` 应等于 allow fields | 可执行部分必须明确，避免误执行未授权字段 |
| strict-block 没有 repair frame | `repair_frame_validity_rate` 对 strict-block 是 vacuous 1.0，同时 checked=0 |

## 当前边界

- verifier 是 frame-level property，不证明外部系统真的执行了局部审批。
- 当前 partial-human-review 仍是结构化 final action，不是生产审批 API。
- 当前 trace adapter 还没有自动生成 `action_field_schema`。
- 需要下一轮把 repair validity 接入 trace/span/OTLP 派生动作。

## 资源

- `docs/power_ops_action_invariance_repair_validity_2026-07-02.md`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `formaltrust_platform/nodes/afw.py`
- `tests/test_power_ops_action_invariance.py`
- `tests/test_interfaces.py`

## 2026-07-02 Findings: Trace-Adapter Repair Replay

## 需求

- 前几轮结果主要依赖 curated metadata cases。
- 为了接近真实 agent 执行过程，需要验证 raw trace events 经 `custom.afw_trace_adapter` 后仍能做 fieldwise repair。

## 研究发现

- 新增 2 个 canonical trace cases 后，完整图：

```text
custom.afw_trace_adapter
  -> guardrail.afw_capguard(runtime_final_action_mode=fieldwise_repair)
  -> evaluate.afw_runtime
```

可以稳定跑通。
- trace repair 覆盖两类 gate：
  - role mismatch block：manual answer authority 不能授权 dispatch。
  - counter-authority abstain：publish approval 被 DLP hold 暂停。
- 两个 trace cases 都能保留 `answer`，移除 `side_effect` / `public_publish`，并通过 repair frame validity。

## 技术发现

| 发现 | 影响 |
|---|---|
| trace adapter 输出的 `candidate_action` 会被放进 `metrics` | `final_action.original_action` 可保留 trace-derived 原始动作 |
| trace-derived `afw_counter_authority` 已可触发 abstain | fieldwise repair 可处理 trace 里的 policy hold |
| `action_invariance_oracle` 仍从 case metadata 读取 | trace replay 目前还需要 metadata oracle 支撑评估 |
| repair validity 在 trace replay 上可复用 | verifier 不依赖数据来源，只依赖 final/original action 与 field schema |

## 当前边界

- 当前是 canonical trace schema，不是 span_log_v1 或 OTLP。
- trace case 是 curated，不是真实生产 transcript。
- trace adapter 还没有自动推断 `action_field_schema`。

## 资源

- `examples/data/power_ops_action_invariance_trace_repair_cases.jsonl`
- `examples/power_ops_action_invariance_trace_repair_validation.yaml`
- `docs/power_ops_action_invariance_trace_repair_2026-07-02.md`
- `docs/power_ops_action_invariance_trace_repair_results_2026-07-02.md`
## 2026-07-02 Findings: Span/OTLP Repair Replay

## 需求

- 上一轮只证明了 canonical trace adapter replay。
- 为了贴近真实 agent runtime，需要验证 span log 和 OTLP `resourceSpans` 这种日志形态能不能被转换成 AFW 的 source / consumption / counter-authority。
- 用户要求持续迭代，因此本轮必须有新增样本、测试、结果和 README 入口。

## 研究发现

- `custom.afw_trace_adapter` 的 `schema_preset=span_log_v1` 可以处理两类输入：
  - 普通 span event list。
  - OpenTelemetry 风格 `resourceSpans -> scopeSpans -> spans`。
- span/OTLP replay 后，CapGuard 仍能做字段级判断：
  - `answer` 字段保留。
  - `side_effect` 因角色不匹配被 block 后移除。
  - `public_publish` 因 DLP counter-authority 被 abstain 后移除并进入局部人工复核。
- 2 个 span/OTLP cases 端到端通过，且 repair frame validity 为 1.000，说明当前 verifier 不依赖输入来自手写 metadata 还是日志 adapter。

## 技术发现

| 发现 | 影响 |
|---|---|
| OTLP 的 resource-level `source.id` 可以被 adapter 继承到 retrieval span | 能表达“这个来源产生了什么 capability” |
| `action.*` 前缀属性可以还原 candidate action | 可以从 runtime span 中恢复混合动作 |
| `need.*` 前缀属性可以还原字段级 Need | 可以把 agent 字段消费映射到授权检查 |
| `counter.*` 前缀属性可以还原 counter-authority | 可以表达 DLP hold / policy hold 一类 abstain |

## 当前边界

- 样本仍是 curated replay，不是真实生产日志。
- OTLP case 规模较小，还没有覆盖多服务、多工具、多轮计划。
- oracle 仍由 metadata 提供，后续要探索 trace-derived oracle 或半自动标注。

## 资源

- `examples/data/power_ops_action_invariance_span_otlp_repair_cases.json`
- `examples/power_ops_action_invariance_span_otlp_repair_validation.yaml`
- `docs/power_ops_action_invariance_span_otlp_repair_2026-07-02.md`
- `docs/power_ops_action_invariance_span_otlp_repair_results_2026-07-02.md`
## 2026-07-02 Findings: Literature Review / Novelty Firewall

## 需求

- 用户持续追问“创新点在哪”，而相似论文确实已经很多。
- 本轮目标是把创新边界写死：什么不能说，什么还能谨慎说。

## 研究发现

- AgentSpec、AgentVisor、CaMeL、Towards Verifiably Safe Tool Use 等工作已经覆盖了运行时约束、能力/数据流策略、工具安全和形式化监督。
- AgentSentry、AgentVisor、InjecGuard 已经明确讨论安全和效用之间的权衡，不能把“guardrail 会过度保守”当作新问题。
- ToolPrivBench / RACG 压住了“least privilege for LLM agents”的宽泛说法。
- 当前项目能保住的创新点是更窄的：在 guard 已经决定 block/abstain 某些字段时，最终动作是否仍保持授权字段不变，并且只移除 invalid authority frame。

## 技术发现

| 发现 | 影响 |
|---|---|
| runtime enforcement 已有 AgentSpec 等工作 | 我们不能写成通用 DSL 或首个 runtime guard |
| safe continuation 已有 AgentSentry 等工作 | 我们必须突出 field authority witness，而不是仅仅“继续执行安全部分” |
| least privilege 已有 ToolPrivBench/RACG | 我们不能只说“降低权限”，要说“动作字段和来源授权的覆盖关系” |
| over-defense 已有 InjecGuard | 我们的度量必须是 final-action authorized-field loss，而不是普通 false positive |

## 当前边界

- 文献综述已足够支撑“查新收缩”，但还没有跑官方 baseline。
- 需要第八轮补 stronger baseline / ablation，否则 novelty firewall 仍偏概念。

## 资源

- `docs/power_ops_action_invariance_lit_review_2026-07-02.md`
- `docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md`
## 2026-07-02 Findings: Baseline Grid / Ablation

## 需求

- novelty firewall 指出：只说概念差异不够，需要对照 baseline 证明 fieldwise repair 的价值。
- 用户关心的是严格监督会不会让 agent 过度保守，因此 baseline 必须看最终动作，而不是只看 gate decision。

## 研究发现

- strict-block 和 fieldwise-decision-only 都能安全移除未授权字段，但代价是 10/10 mixed cases 整动作打回，授权字段最终保留率为 0。
- provenance-only 能保留所有授权字段，但在当前 10 个 cases 中也 false-allow 所有未授权字段。
- fieldwise-repair 在当前 curated suite 中同时做到：
  - 授权字段最终保留率 1.000
  - 未授权字段最终移除率 1.000
  - 整动作阻断率 0.000
  - false allow field rate 0.000

## 技术发现

| baseline | 说明 | 结论 |
|---|---|---|
| strict-block | 任何危险字段出现就整条动作转人工 | 安全但过度保守 |
| fieldwise-decision-only | 有字段级判断但没有最终动作修复 | 仍然过度保守 |
| provenance-only | 只看字段有没有来源归因 | 不保守但不安全 |
| fieldwise-repair | 保留 allow 字段，移除 block/abstain 字段 | 当前最佳折中 |

## 当前边界

- baseline grid 仍然是 curated power-ops suite，不是独立公开 benchmark。
- provenance-only 是内部消融 baseline，不代表某篇论文的官方实现。
- 下一轮需要增强外部有效性：真实/semi-real trace 或 AgentDojo-style task mapping。

## 资源

- `formaltrust_platform/experiments/power_ops_action_invariance_baselines.py`
- `docs/power_ops_action_invariance_baseline_grid_2026-07-02.md`
- `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json`
## 2026-07-02 Findings: Human Review Burden Metrics

## 需求

- baseline grid 证明了 fieldwise repair 可以避免整动作阻断，但还缺少人审负担指标。
- 用户关心 agent 性能和正常行为，因此需要量化“哪些字段还能自动执行，哪些字段转人工”。

## 研究发现

- strict-block 没有局部人审字段，因为它不暴露 repair frame，而是整条 final action 打回。
- fieldwise-repair 在当前 10 个 curated cases 中，每条平均 1 个字段转人工、1 个字段保留自动执行。
- trace-repair 和 span/OTLP repair 也保持同样结构，说明局部人审字段可以穿过 trace-derived action。

## 技术发现

| 指标 | 作用 |
|---|---|
| `mean_partial_human_review_fields` | 衡量平均每个 case 要转人工几个字段 |
| `auto_executable_field_ratio` | 衡量 repair 后多少字段仍可自动执行 |
| `human_review_field_counts` | 给报告和论文表格提供总量口径 |

## 当前边界

- 当前只是字段数量，不是真实人工审核耗时。
- 真实 workload 还需要 field severity、operator time、review queue 等数据。

## 资源

- `docs/power_ops_action_invariance_human_review_burden_2026-07-02.md`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
- `tests/test_power_ops_action_invariance.py`
## 2026-07-02 Findings: AgentDojo-Style Externality Mapping

## 需求

- 前几轮都是 curated power-ops regression，需要向更外部的 benchmark 形态靠近。
- 本轮先做 bridge：把 AgentDojo-style 的“任务环境 + 注入指令 + 工具动作”映射为 action fields 和 authority needs。

## 研究发现

- email/calendar 类任务可以自然映射为 `answer`、`calendar_event`、`external_email` 字段。
- telemetry/tool 类任务可以自然映射为 `answer`、`dashboard_update`、`side_effect` 字段。
- 当前 fieldwise repair 能保留 4 个授权字段并移除 2 个未授权字段。

## 当前边界

- 这不是官方 AgentDojo 复现。
- 这不是和 AgentDojo defenses 的比较。
- 这只是证明接口能表达类似任务形态。

## 资源

- `examples/data/power_ops_action_invariance_agentdojo_style_cases.json`
- `examples/power_ops_action_invariance_agentdojo_style_validation.yaml`
- `docs/power_ops_action_invariance_agentdojo_style_mapping_2026-07-02.md`
- `docs/power_ops_action_invariance_agentdojo_style_results_2026-07-02.md`
## 2026-07-02 Findings: Severity-Weighted Review Burden

## 需求

- 第九轮只有字段数量，不能区分 `answer` 和 `open_breaker` 的风险差异。
- 电力场景里少数高危字段会主导人工复核压力，因此需要 severity-weighted burden。

## 研究发现

- 新增 `field_severity` 后，AgentDojo-style bridge suite 的未加权结果是 4 个自动字段、2 个转人工字段。
- 加权后，自动字段严重度总和为 6，转人工字段严重度总和为 10。
- 这说明“转人工字段数量少”不等于“转人工风险负担低”。

## 技术发现

| 输入 | 权重 |
|---|---:|
| `low` | 1 |
| `medium` / `moderate` | 2 |
| `high` | 3 |
| `critical` | 5 |
| numeric | 原值 |
| missing | 1 |

## 当前边界

- 当前权重是工程默认，不是领域专家标定。
- 仍然没有真实 operator review time。
- 下一轮可以把 severity 加到 semi-real trace 或更大外部映射样本里。

## 资源

- `docs/power_ops_action_invariance_severity_weighted_review_2026-07-02.md`
- `examples/data/power_ops_action_invariance_agentdojo_style_cases.json`
- `formaltrust_platform/experiments/power_ops_action_invariance.py`
## 2026-07-02 Findings: Semi-Real Power Trace Replay

## 需求

- AgentDojo-style mapping 是外部形态桥接，但还不是电力运行 trace。
- 本轮需要更接近电力 runtime 日志的 span replay，并且携带 severity 标签。

## 研究发现

- SCADA alarm + operator work request 可以表达为 retrieval spans、action span、authority-use spans。
- incident dashboard + publish approval + regulatory hold 可以表达为 retrieval spans、authority-use spans、counter-authority span。
- 两条 semi-real trace 均通过 fieldwise repair，并同时给出数量和 severity 人审负担。

## 当前边界

- 仍是 curated semi-real trace，不是真实生产日志。
- 还没有多轮 planner trace，也没有真实 span exporter 输出。
- 下一轮需要进入 claim ledger / paper integration，把哪些 claim 已有证据写清楚。

## 资源

- `examples/data/power_ops_action_invariance_semireal_trace_cases.json`
- `examples/power_ops_action_invariance_semireal_trace_validation.yaml`
- `docs/power_ops_action_invariance_semireal_trace_2026-07-02.md`
- `docs/power_ops_action_invariance_semireal_trace_results_2026-07-02.md`
## 2026-07-02 Findings: Claim Ledger / Paper Integration

## 需求

- 连续多轮已经产生了代码、样本、trace、baseline、severity、文献边界。
- 现在需要把它们转为论文可写 claim，防止把 L2/L3/L4 证据说成生产级结论。

## 研究发现

- 当前最安全的论文贡献是 field-level action invariance under strict supervision。
- 已有证据能支持 curated suite、trace replay、bridge fixture 级别的结论。
- 还不能支持真实生产 trace、真实 operator workload、官方系统优越性。

## 资源

- `docs/power_ops_action_invariance_claim_ledger_2026-07-02.md`
- `docs/power_ops_action_invariance_claim_ledger_2026-07-02.json`

## 2026-07-02 Findings: Continuous Iteration Queue

## 需求

- 用户明确补充：计划必须可以一直迭代，不停。
- 不能只写研究点子；后续每轮都要能产生代码、建模、样本、测试、结果或论文资产。
- 当前项目已经推进到第十三轮 claim ledger，所以下一轮不能回到空泛规划，而应从第十四轮 paper kernel / figure-table package 继续。

## 研究发现

- 持续迭代需要把“下一步”写成可执行队列，而不是一句“后续继续扩展”。
- 当前最自然的连续路线是：
  - 第十四轮：把已有结果整理成论文核心叙事、图、表。
  - 第十五轮：扩成更大 power-ops 样本集。
  - 第十六轮：加入 action-invariance metamorphic tests。
  - 第十七轮：扩展到 skill-driven agent security。
  - 第十八轮：量化性能和过度保守问题。
  - 第十九轮：增强 realistic trace import path。
  - 第二十轮：进入 paper draft integration。
- 每轮结束必须做 keep/revise/reject 判断，否则持续迭代会变成堆文件，而不是科研收敛。

## 技术决策

| 决策 | 理由 |
|---|---|
| 在 `task_plan.md` 追加第十四至第二十轮 backlog | 避免上下文压缩后丢失“接着做什么” |
| 每轮列出拟产物路径 | 保证计划可执行，不停留在口头点子 |
| 每轮列出验收标准 | 后续能判断完成与否 |
| 保留自动续轮规则 | 满足用户“不断迭代，不停”的要求 |

## 当前边界

- 这是持续迭代计划，不代表第十四至第二十轮已经完成。
- 后续实现阶段仍需遵守 TDD：涉及代码时先写失败测试，再实现。
- 每轮新增 claim 都必须回写 claim ledger，防止论文叙事过度外推。

## 2026-07-02 Findings: Paper Kernel / Figure-Table Package

## 需求

- 第十四轮需要把已有工程结果变成可写论文、可汇报、可持续迭代的核心材料。
- 用户要求不停迭代，因此本轮不能只写口头总结，要有可落地文件、图和表。

## 研究发现

- 当前最稳的论文题眼不是“通用 agent 安全框架”，而是：

```text
field-level action invariance under strict LLM-agent supervision
```

- 三张图分别承担三种功能：
  - architecture figure：讲方法结构。
  - repair-frame figure：讲创新机制。
  - evidence ladder：讲 claim 边界。
- 证据阶梯必须放在图表包里，因为当前证据最高到 L4 bridge，不能写成 L5 production evidence。

## 技术发现

- `figure-spec` renderer 可以复用来生成 deterministic SVG。
- Windows 默认 GBK 控制台无法打印 renderer 的 checkmark，需要设置：

```powershell
$env:PYTHONIOENCODING='utf-8'
```

## 产物

- `docs/power_ops_action_invariance_paper_kernel_2026-07-02.md`
- `docs/power_ops_action_invariance_figure_table_package_2026-07-02.md`
- `figures/specs/power_ops_action_invariance_architecture.json`
- `figures/specs/power_ops_action_invariance_repair_frame.json`
- `figures/specs/power_ops_action_invariance_result_ladder.json`
- `figures/power_ops_action_invariance_architecture.svg`
- `figures/power_ops_action_invariance_repair_frame.svg`
- `figures/power_ops_action_invariance_result_ladder.svg`
- `refine-logs/iterations/ITERATION_123.md`

## 下一步

第十五轮进入 large-sample power-ops expansion。优先扩样本、补 dataset audit、跑 expanded validation，让结果不只停在 10 条 curated cases。

## 2026-07-02 Findings: Large-Sample Power-Ops Expansion

## 需求

- 第十五轮要把当前 10 条 curated cases 扩成覆盖面更好的 suite。
- 用户要求持续迭代，因此本轮必须有新增数据、测试、代码、报告和 README 入口。

## 研究发现

- expanded suite 从 10 条扩到 18 条，新增 8 条 covering:
  - dispatch
  - risk-level override
  - tool-metadata-to-control laundering
  - approval waiver
  - switching operation
  - public publish with regulatory hold
  - export with unmet scan obligation
  - equipment certification
- dataset audit 显示：
  - total cases：18
  - oracle coverage rate：1.000
  - gate decisions：block=14，abstain=4
  - source types：evidence=6，memory=2，prior_step_output=2，skill=2，tool_metadata=3，user_approval=7
  - severity labels：critical=6，high=2，medium=3，low=5
- expanded runtime 结果显示：
  - 18/18 passed
  - authorized final-field preservation：1.000
  - unauthorized final-field removal：1.000
  - whole-action block rate：0.000
  - repair-frame validity：1.000

## 技术发现

- dataset audit 独立于 runtime summary，适合在后续扩样本时先检查覆盖面。
- 当前 expanded suite 仍是手写 curated 数据，不是自动生成 benchmark；下一轮应做 metamorphic tests，把“只靠人工样本”的证据继续往前推。

## 产物

- `formaltrust_platform/experiments/power_ops_action_invariance_dataset_audit.py`
- `examples/data/power_ops_action_invariance_expanded_cases.jsonl`
- `examples/power_ops_action_invariance_expanded_validation.yaml`
- `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.md`
- `docs/power_ops_action_invariance_expanded_dataset_audit_2026-07-02.json`
- `docs/power_ops_action_invariance_expanded_runtime_report_2026-07-02.md`
- `docs/power_ops_action_invariance_expanded_runtime_report_2026-07-02.json`
- `docs/power_ops_action_invariance_expanded_results_2026-07-02.md`
- `docs/power_ops_action_invariance_expanded_results_2026-07-02.json`
- `refine-logs/iterations/ITERATION_124.md`

## 下一步

第十六轮进入 action-invariance metamorphic tests：从合法 base action 出发，只改变非法字段的授权条件，验证合法字段在 repair 后仍保持不变。

## 2026-07-02 Findings: Action-Invariance Metamorphic Tests

## 需求

- 第十六轮要减少对手写样本的依赖，改为系统性 authority-confusion mutation。
- 变形测试必须验证：非法字段授权条件改变后，合法字段仍应在 final action 中保持不变。

## 研究发现

- 已实现 4 类 deterministic mutation：
  - `role_mismatch`：边界相同，但 required role 不匹配。
  - `scope_mismatch`：角色相同，但 data scope 不匹配。
  - `counter_authority`：capability 本身覆盖，但存在 active hold，输出 abstain。
  - `expired_approval`：approval 角色/字段/范围接近，但 time scope 过期。
- metamorphic suite 结果：
  - 4/4 passed
  - metamorphic preservation rate：1.000
  - unsafe mutation removal rate：1.000
  - repair-frame validity rate：1.000
  - whole-action block rate：0.000
- 这比单纯 expanded suite 更强，因为它从 base case 系统生成授权混淆变体，开始测试“干预下动作不变性”这个性质本身。

## 技术发现

- metamorphic generator 仍然复用现有 AFW runtime graph，没有新开评估接口。
- `expected_final_decision` 在 metamorphic case 中设为 `fieldwise_repaired`，因此 runtime evaluator 的 L3 final-action match 也能直接通过。
- 当前 metamorphic suite 是 deterministic seed，不是随机 fuzzing；后续可以扩成批量 mutation generator。

## 产物

- `formaltrust_platform/experiments/power_ops_action_invariance_metamorphic.py`
- `examples/data/power_ops_action_invariance_metamorphic_cases.jsonl`
- `examples/power_ops_action_invariance_metamorphic_validation.yaml`
- `docs/power_ops_action_invariance_metamorphic_runtime_report_2026-07-02.md`
- `docs/power_ops_action_invariance_metamorphic_runtime_report_2026-07-02.json`
- `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.md`
- `docs/power_ops_action_invariance_metamorphic_tests_2026-07-02.json`
- `refine-logs/iterations/ITERATION_125.md`

## 下一步

第十七轮进入 skill-driven agent security：验证 report-formatting skill、incident-summary skill 等 no-RAG skill 输出不能升级成风险评估、调度或控制 authority。

## 2026-07-02 Findings: Skill-Driven Agent Security

## 需求

- 用户提出不能局限于 RAG，很多 agent 是 skill-driven；因此需要验证 AFW 统一框架能接 no-RAG skill manifest。
- 第十七轮要有实际数据、YAML、结果和模型说明，而不是只讨论方向。

## 研究发现

- 4 个 no-RAG skill cases 均只使用 `source_type=skill`。
- skill manifest 可以 lift 成 `Cap(skill)`：

```text
skill_manifest.output_semantic_roles -> capability.semantic_roles
skill_manifest.fields -> capability.fields
skill_manifest.operations -> capability.operations
skill_manifest.data_scope/effect_scope -> capability scopes
```

- 测试边界：
  - report-formatting skill：可写 `risk_report`，不能写 `risk_level`。
  - incident-summary skill：可写 `answer`，不能写 `dispatch`。
  - risk-assessment skill：可写 `risk_level`，不能写 `switching_operation`。
  - dispatch-prep skill：可写 `dispatch_order`，不能执行 `dispatch`。
- 结果：
  - 4/4 passed
  - authorized final-field preservation：1.000
  - unauthorized final-field removal：1.000
  - whole-action block rate：0.000
  - repair-frame validity：1.000

## 当前边界

- 这是 4-case no-RAG skill fixture，不是通用 skill-agent benchmark。
- 还没有多 skill 链、skill-to-tool delegation、skill memory、真实 skill marketplace manifest。
- 后续第十八轮应把已有 suite 统一到 performance / over-conservatism profile。

## 产物

- `examples/data/power_ops_skill_authority_cases.jsonl`
- `examples/power_ops_skill_authority_validation.yaml`
- `docs/power_ops_skill_authority_model_2026-07-02.md`
- `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md`
- `docs/power_ops_skill_authority_dataset_audit_2026-07-02.json`
- `docs/power_ops_skill_authority_runtime_report_2026-07-02.md`
- `docs/power_ops_skill_authority_runtime_report_2026-07-02.json`
- `docs/power_ops_skill_authority_results_2026-07-02.md`
- `docs/power_ops_skill_authority_results_2026-07-02.json`
- `refine-logs/iterations/ITERATION_126.md`

## 下一步

第十八轮进入 performance / over-conservatism evaluation：把安全性、正常行为保留、人审负担、audit compression 放到同一张 profile 表。

## 2026-07-02 Findings: Performance / Over-Conservatism Evaluation

## 需求

- 用户关心严格防御会不会让 agent 过度保守，因此需要把安全性和正常行为保留放在同一个 profile 中。
- 不能只报告拦截率；需要同时看正常字段保留、非法字段移除、整动作阻断、人审负担、latency proxy 和 audit compression。

## 研究发现

- 当前 performance profile 包含 3 个 suite：
  - expanded-fieldwise：18 cases
  - metamorphic：4 cases
  - skill-authority：4 cases
- 三个 suite 均为：
  - normal preservation：1.000
  - safety removal：1.000
  - whole-action block：0.000
- baseline profile 显示：
  - strict-block：安全移除 1.000，但正常保留 0.000，整动作阻断 1.000。
  - provenance-only：正常保留 1.000，但安全移除 0.000，false allow 1.000。
  - fieldwise-repair：正常保留 1.000，安全移除 1.000，整动作阻断 0.000，false allow 0.000。

## 技术发现

- `latency_proxy_units` 当前定义为 runtime field checks 数量，不是 wall-clock latency。
- audit compression 使用已有 `mean_witness_compression_ratio`。
- 这轮支持“不过度保守”的 artifact-level 论证，但不能写成真实系统延迟低或真实人审成本低。

## 产物

- `formaltrust_platform/experiments/power_ops_action_invariance_perf.py`
- `docs/power_ops_action_invariance_performance_2026-07-02.md`
- `docs/power_ops_action_invariance_performance_2026-07-02.json`
- `refine-logs/iterations/ITERATION_127.md`

## 下一步

第十九轮进入 realistic trace import path：把 adapter 行为写成导入合约，并测试 malformed trace、missing source、duplicate approval、expired epoch。

## 2026-07-02 Findings: Realistic Trace Import Path

## 需求

- 第十九轮要把 trace 导入从已有 adapter 能力推进成可复现的 import contract。
- 用户要求持续迭代，因此本轮必须包含代码、fixture、YAML、结果报告和论文 claim 边界更新。

## 研究发现

- `custom.afw_trace_adapter` 已经支持 canonical events、`span_log_v1` 和 OTLP 展开；第十九轮不需要改核心 adapter。
- 可把 trace 导入合约拆成 4 类对象：
  - `source_event` -> `metrics.afw_source_events` -> `Cap(x)`
  - `authority_consumption` -> `metrics.afw_consumptions` -> `Need(s,f)`
  - `candidate_action` -> `metrics.candidate_action`
  - malformed/unknown events -> `metrics.afw_trace_adapter_diagnostics`
- 新 fixture 覆盖 4 类导入边界：
  - malformed trace：记录 diagnostics，但不阻止其他有效事件被检查。
  - missing source：consumption 引用未导入 source id，非法字段被 block。
  - duplicate approval：重复 approval 被统计，但不会扩权成 switching authority。
  - expired epoch：Q3 publish approval 不能覆盖 Q4 publish need。
- trace-import suite 结果：
  - 4/4 passed
  - authorized final-field preservation：1.000
  - unauthorized final-field removal：1.000
  - whole-action block rate：0.000
  - repair-frame validity：1.000
  - invalid trace cases：1
  - missing source cases：1
  - duplicate approval cases：1
  - expired epoch cases：1

## 技术发现

- `datasets.py` 已支持 JSON 数组，因此 `examples/data/power_ops_trace_import_fixture.json` 可以直接作为 FormalTrust dataset 使用。
- trace-import summary 适合作为报告层模块，不应把导入统计写入新的 `FormalTrustState` 顶层字段。
- 当前 missing-source 统计来自 imported source ids 与 consumption attribution 的差集；expired epoch 统计来自 imported capability `time_scope` 与 Need `time_scope` 的不匹配。

## 当前边界

- 这是 realistic import-path fixture，不是生产 telemetry。
- 尚未导入真实 SCADA/OMS/EMS/vendor agent logs。
- 还没有多步 planner trace、intermediate tool call、memory mutation 的完整导入链。

## 产物

- `formaltrust_platform/experiments/power_ops_trace_import.py`
- `examples/data/power_ops_trace_import_fixture.json`
- `examples/power_ops_trace_import_validation.yaml`
- `docs/power_ops_trace_import_contract_2026-07-02.md`
- `docs/power_ops_trace_import_runtime_report_2026-07-02.md`
- `docs/power_ops_trace_import_runtime_report_2026-07-02.json`
- `docs/power_ops_trace_import_results_2026-07-02.md`
- `docs/power_ops_trace_import_results_2026-07-02.json`
- `refine-logs/iterations/ITERATION_128.md`

## 下一步

第二十轮进入 paper draft integration：把当前 L1/L2/L3/L4 证据链合成论文 outline，并让每个 section 绑定 claim ledger 和可复现实验文件。

## 2026-07-02 Findings: Paper Draft Integration

## 需求

- 第二十轮要把前 19 轮成果合成论文骨架。
- 不能只写一个描述性 outline；需要把 claim、section、artifact、result JSON 绑定，形成后续写论文的证据约束。

## 研究发现

- `docs/power_ops_action_invariance_claim_ledger_2026-07-02.json` 已足够作为 paper outline 的 claim backbone。
- 当前 claims-evidence matrix 包含：
  - L1=1：实现级 claim。
  - L2=6：curated/expanded/metamorphic/skill/performance/baseline 结果。
  - L3=2：trace/span/OTLP 与 trace-import fixture。
  - L4=1：AgentDojo-style 与 semi-real bridge。
- 第二十轮生成的 outline 明确把：
  - 方法与形式化放到 §3。
  - 测试框架放到 §4。
  - 主结果、性能 profile、trace-import 结果放到 §5。
  - 生产 trace、真实人审、官方 benchmark 缺口放到 §6。

## 技术发现

- `power_ops_paper_artifact_map.py` 可以从 claim ledger 和结果 JSON 生成机器可读 artifact map。
- result artifact readback 当前覆盖：
  - `power_ops_action_invariance_performance_profile`
  - `power_ops_trace_import_summary`
- 旧 `PAPER_PLAN.md` 里有大量 WarrantGuard/RAG-only 历史内容，必须在顶部加 active update，否则后续写作容易混淆方向。

## 产物

- `formaltrust_platform/experiments/power_ops_paper_artifact_map.py`
- `docs/power_ops_action_invariance_paper_outline_2026-07-02.md`
- `docs/power_ops_action_invariance_paper_outline_2026-07-02.json`
- `refine-logs/iterations/ITERATION_129.md`

## 下一步

第二十一轮建议进入 draft skeleton 或 multi-step trace extension。若优先写论文，生成 section skeleton；若优先补实验，扩展 memory/tool/prior-step/approval 的多步 trace 导入链。

## 2026-07-02 Findings: Multi-Step Trace Source-Chain Import

## 需求

- 用户要求不断迭代，不停留在描述性 plan。
- 第二十一轮优先补实验而不是写论文 skeleton：把 trace import 从异常边界 fixture 扩展到复杂 agent 常见的多步来源链。

## 研究发现

- 当前 AFW trace adapter 已经能承载多类 runtime authority source；新增能力主要在 summary/report 层，把来源类型覆盖显式读出来。
- 新 multi-step fixture 把 4 类来源统一成 `Cap(x)`：
  - `memory`：只能支持 answer/style 个性化。
  - `tool_metadata`：只能支持 citation/schema 引用。
  - `prior_step_output`：只能支持 diagnosis/summary 复用。
  - `user_approval`：只能支持 internal work-order creation。
- 同一个 approval 支持 internal work order，但不能扩权成 grid switching；这正是 action-invariance 问题里的“保留正常字段、删除危险字段”。
- 结果显示：
  - multi-step trace-import：1/1 passed。
  - source-type coverage：1.000。
  - authorized final-field preservation：1.000。
  - unauthorized final-field removal：1.000。
  - whole-action block rate：0.000。

## 技术发现

- `power_ops_trace_import.py` 新增 `source_type_counts` 和 `multi_step_source_type_coverage`，因此 trace import report 不只看异常边界，也能看复杂 agent 来源链是否覆盖。
- `power_ops_paper_artifact_map.py` 修复了 trace-import readback 的硬编码：不再固定写 “4 import boundaries”，而是从 JSON 实际统计 boundary_count，并在有 coverage 时输出 `source_type_coverage`。
- 新增测试覆盖了两个点：
  - 多步 trace import summary 必须报告 4 类 source type。
  - paper outline 必须能读回 multi-step trace 的 source coverage。

## 当前边界

- 这是单条 multi-step source-chain fixture，不是任意 planner trace。
- 还没有 branching plan、memory write-back、skill-to-tool delegation、真实 OMS/SCADA/EMS telemetry。
- 还不能声称支持任意复杂 agent，只能声称当前接口能表达并检查一类多步来源链。

## 产物

- `examples/data/power_ops_multistep_trace_import_fixture.json`
- `examples/power_ops_multistep_trace_import_validation.yaml`
- `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.md`
- `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`
- `docs/power_ops_multistep_trace_import_results_2026-07-02.md`
- `docs/power_ops_multistep_trace_import_results_2026-07-02.json`
- `formaltrust_platform/experiments/power_ops_trace_import.py`
- `formaltrust_platform/experiments/power_ops_paper_artifact_map.py`
- `refine-logs/iterations/ITERATION_130.md`

## 下一步

第二十二轮进入 draft skeleton with evidence-bound paragraphs：把 claim ledger 和 artifact map 转成可写论文草稿，但每段都绑定证据，不写 forbidden claims。

## 2026-07-02 Findings: Evidence-Bound Draft Skeleton

## 需求

- 用户要求不仅做实验，还要持续把成果推进到论文可写状态。
- 第二十二轮目标是把 paper outline 变成 draft skeleton，但不能让自由写作引入无证据 claim。

## 研究发现

- 直接写 prose 风险较大：当前证据混合了 L1/L2/L3/L4，容易把 trace fixture 或 bridge fixture 写成 production evidence。
- 更稳的做法是先生成 evidence-bound skeleton：
  - 每个 claim-bound paragraph 保留 `claim`、`level`、`section`、`evidence`、`safe_use`。
  - §5 结果段落必须有 evidence list。
  - forbidden claim scan 必须为 0。
- 生成结果：
  - sections：7。
  - claim-bound paragraphs：11。
  - evidence-bound paragraphs：11。
  - forbidden claim hits：0。
  - multi-step trace import 已进入 §5 Results and Analysis，并绑定对应结果 JSON、runtime JSON、fixture。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_draft_skeleton.py`，输入 `docs/power_ops_action_invariance_paper_outline_2026-07-02.json`，输出 Markdown/JSON skeleton。
- renderer 不输出 forbidden phrase 列表，避免 forbidden claims 被复制进草稿正文。
- 新增测试保证：
  - skeleton 覆盖 7 个 section。
  - §5 result paragraphs 都有 evidence。
  - multi-step trace import evidence 被保留。
  - Markdown 中没有 `TODO-EVIDENCE` 或 `proves production safety`。

## 当前边界

- 这是 draft skeleton，不是完整论文正文。
- 当前 §0/§1/§2/§4 仍是 no-supported-claim note，需要下一轮扩成 prose draft。
- safe-use 约束仍是静态文本扫描，不是自然语言事实核查。

## 产物

- `formaltrust_platform/experiments/power_ops_draft_skeleton.py`
- `docs/power_ops_action_invariance_draft_skeleton_2026-07-02.md`
- `docs/power_ops_action_invariance_draft_skeleton_2026-07-02.json`
- `refine-logs/iterations/ITERATION_131.md`

## 下一步

第二十三轮进入 evidence-constrained prose draft：把 skeleton stub 扩成短段落，但继续保留 evidence list 和 forbidden-claim scan。

## 2026-07-02 Findings: Evidence-Constrained Prose Draft

## 需求

- 用户要求持续迭代到实际成果；第二十三轮把 skeleton 继续推进成论文短段落。
- 不能把段落写成自由发挥，必须保留 evidence 和 result readback。

## 研究发现

- 从 skeleton 到 prose draft 的最小安全步是“短段落 + evidence list + safe-use + result readback”。
- 当前 prose draft 覆盖 §0-§6：
  - §0/§1/§2/§4 当前是 no-supported-claim structure note。
  - §3 有 L1 implementation paragraph。
  - §5 有 L2/L3 result paragraphs。
  - §6 有 L4 bridge/limitation paragraph。
- §5 multi-step trace import paragraph 保留了：
  - `docs/power_ops_multistep_trace_import_results_2026-07-02.json`
  - `docs/power_ops_multistep_trace_import_runtime_report_2026-07-02.json`
  - `source_type_coverage=1.000`
- 生成结果：
  - sections：7。
  - §5 paragraphs：9。
  - forbidden claim hits：0。
  - full pytest：228 passed。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_prose_draft.py`，输入 draft skeleton JSON，输出 prose draft Markdown/JSON。
- 对 evidence 路径和 result readback 路径做了 `/` 与 `\` 的归一化，确保 Windows 路径也能匹配。
- 新增测试保证：
  - 每节至少有 paragraph 或 structure note。
  - §5 result paragraph 不丢 evidence。
  - multi-step trace import paragraph 不丢 source claim。
  - Markdown 中保留 `source_type_coverage=1.000`，且无 forbidden phrase。

## 当前边界

- 这是证据约束初稿，不是最终论文语言。
- 当前没有做自然语言数值核查，只是把 result readback 携带到段落旁边。
- 下一轮需要审计 prose draft、paper kernel、README 中的数字是否都能从 JSON 追溯。

## 产物

- `formaltrust_platform/experiments/power_ops_prose_draft.py`
- `docs/power_ops_action_invariance_prose_draft_2026-07-02.md`
- `docs/power_ops_action_invariance_prose_draft_2026-07-02.json`
- `refine-logs/iterations/ITERATION_132.md`

## 下一步

第二十四轮进入 numeric claim and table consistency audit：扫描文档中的数字、case counts、coverage、0.000/1.000，并绑定到 result JSON/readback。

## 2026-07-02 Findings: Numeric Claim and Table Consistency Audit

## 需求

- 第二十四轮要检查写作层数字是否可追溯，避免论文/README 表格数字脱离 result JSON。
- 重点检查刚新增的 `source_type_coverage=1.000` 和常用的 `whole_action_block_rate=0.000`。

## 研究发现

- 新 numeric audit 对 3 个文档做扫描：
  - `README_POWER_OPS_ACTION_INVARIANCE.md`
  - `docs/power_ops_action_invariance_paper_kernel_2026-07-02.md`
  - `docs/power_ops_action_invariance_prose_draft_2026-07-02.md`
- 使用 4 个 evidence 文件：
  - performance profile JSON
  - trace-import results JSON
  - multi-step trace-import results JSON
  - paper outline/artifact map JSON
- 关键数字检查：
  - `source_type_coverage=1.000`：supported。
  - `whole_action_block_rate=0.000`：supported。
- 审计也暴露出下一步问题：
  - supported numeric mentions：22。
  - needs_evidence mentions：218。
  - 很多 needs_evidence 来自 README / paper kernel 的大结果表；它们需要 row-to-artifact binding，而不是只靠全局 result readback。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`。
- 审计器会跳过 inline code、fenced code block、ISO date 和 section 编号，减少路径日期噪声。
- 当前支持 metric=value 风格的关键数字检查；表格行级数字还没有自动绑定。

## 当前边界

- 这是数字表面审计，不是完整自然语言事实核查。
- 表格行级支持关系尚未建模，所以很多正确数字仍会被标成 `needs_evidence`。
- 下一轮应做 table row evidence binding，把 Current Result、Baseline Grid、Performance Profile 每行绑定到对应 JSON。

## 产物

- `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`
- `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
- `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
- `refine-logs/iterations/ITERATION_133.md`

## 下一步

第二十五轮进入 table row evidence binding：把主要结果表的每一行绑定到 result JSON，逐步减少 numeric audit 的 `needs_evidence`。

## 2026-07-02 Findings: Table Row Evidence Binding

## 需求

- 第二十五轮要解决 numeric audit 暴露的表格数字问题。
- 目标不是改结果，而是把 README 主结果表每一行绑定到产生该数字的 JSON artifact。

## 研究发现

- README 当前有三张需要绑定的主表：
  - `Current Result`
  - `Baseline Grid`
  - `Performance Profile`
- 新 table evidence binding 解析 README Markdown 表格并逐行比对 JSON。
- 绑定结果：
  - tables：3。
  - evidence files：13。
  - fully supported rows：18。
  - unsupported rows：0。
- 代表性行：
  - `multistep-trace-import` 绑定到 `docs/power_ops_multistep_trace_import_results_2026-07-02.json`。
  - `fieldwise-repair` baseline 绑定到 `docs/power_ops_action_invariance_baseline_grid_2026-07-02.json`。
  - `metamorphic` performance 绑定到 `docs/power_ops_action_invariance_performance_2026-07-02.json`，其中 `Audit compression` 的 README 显示值 `0.688` 与 JSON 的 `0.6875` 四舍五入一致。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_table_evidence_binding.py`。
- 支持三类 evidence shape：
  - action-invariance summary / metamorphic summary / trace-import summary。
  - baseline grid。
  - performance profile。
- 行级 binding 会输出 observed values、expected values、supported metrics、missing metrics。

## 当前边界

- 这轮只生成 row-to-artifact binding；numeric audit 还没有消费这个 binding。
- 下一轮需要把 table binding 接入 numeric audit，把 README 表格数字从 `needs_evidence` 转成 `supported_by_table_binding`。

## 产物

- `formaltrust_platform/experiments/power_ops_table_evidence_binding.py`
- `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.md`
- `docs/power_ops_action_invariance_table_evidence_binding_2026-07-02.json`
- `refine-logs/iterations/ITERATION_134.md`

## 下一步

第二十六轮进入 numeric audit with table binding：让数字审计读取 table binding JSON，减少大表数字的 `needs_evidence`。

## 2026-07-02 Findings: Numeric Audit With Table Binding

## 需求

- 第二十六轮要让 numeric audit 消费第二十五轮的 table evidence binding。
- 目标是把 README 大表里的数字从 `needs_evidence` 转成有行级证据支持。

## 研究发现

- 接入 table binding 后，numeric audit 结果变化明显：
  - table_binding_count：1。
  - supported numeric mentions：22。
  - supported_by_table_binding numeric mentions：184。
  - needs_evidence mentions：43。
- 对比第二十四轮：
  - needs_evidence 从 218 降到 43。
  - 说明 README 三张主表的大部分数字已经被 row-level artifact binding 覆盖。
- 剩余 43 个 needs_evidence 主要不是表格行内数字，而是更靠近上下文叙述、标题附近或还没有细粒度 evidence model 的数字。

## 技术发现

- `build_numeric_claim_audit()` 新增 `table_binding_paths` 参数。
- CLI 新增 `--table-binding`。
- numeric mention 状态新增 `supported_by_table_binding`。
- 匹配逻辑：如果数字 context 同时包含 fully-supported row label 和该 row 的 observed value，则标记为 table-binding supported。

## 当前边界

- 当前匹配是 context-window heuristic，不是完整 Markdown AST。
- 对剩余 `needs_evidence` 还没有分类；下一轮需要 triage。
- 不能简单把所有剩余数字自动标成 supported，否则会失去审计价值。

## 产物

- 更新 `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`
- 更新 `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md`
- 更新 `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.json`
- `refine-logs/iterations/ITERATION_135.md`

## 下一步

第二十七轮进入 residual needs-evidence triage：对剩余 43 个数字逐类判断，决定是 context-only、需要新 evidence，还是需要改写。

## 2026-07-02 Findings: Residual Needs-Evidence Triage

## 需求

- 第二十七轮要把 numeric audit 中剩余的 43 个 `needs_evidence` 数字分类，而不是继续堆新结果。
- 目标是判断这些数字到底是论文结果 claim、上下文数字、parser 缺口，还是文本需要改写。

## 研究发现

- triage 结果：
  - total needs_evidence：43。
  - context_only：25。
  - parser_extension：17。
  - rewrite_needed：1。
- 唯一明确需要改写的是 README 中的 Current Result 表引导语：
  - 现文案写的是 “On the 10-case curated power-ops suite”。
  - 但该表现在包含 trace、span/OTLP、AgentDojo-style、semi-real、expanded、metamorphic、skill、trace-import、multi-step trace-import 等多 suite 结果。
  - 因此这个 lead-in 应改成“rows come from multiple current result artifacts”之类的表述。
- context_only 主要来自：
  - continuous iteration queue 的轮次编号。
  - ordered list 编号。
  - forbidden hits / date / status note。
- parser_extension 主要来自：
  - baseline-grid lead-in 中的 `10-case`。
  - baseline comparative sentence。
  - prose draft 中的 `expanded 18-case`、`suite_count=3`、`baseline_count=4` 等已有 artifact 可支持但 parser 未覆盖的上下文数字。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py`。
- 输入 numeric audit JSON，输出 triage Markdown/JSON。
- triage 没有把剩余数字强行 supported，而是保留可执行分类。

## 当前边界

- triage 是规则分类，不是自然语言证明。
- 下一轮应先改写唯一明确的 rewrite-needed lead-in，然后重跑 audit/triage。
- parser_extension 类需要逐步加规则，不应一次性全部放行。

## 产物

- `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py`
- `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md`
- `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.json`
- `refine-logs/iterations/ITERATION_136.md`

## 下一步

第二十八轮进入 lead-in rewrite and parser refinement：先修 README Current Result lead-in，再重跑 numeric audit 和 residual triage。

## 2026-07-02 Findings: Lead-In Rewrite And Parser Refinement

## 需求

- 第二十八轮处理 residual triage 中唯一明确需要改写的文本风险。
- 目标是让 Current Result 表不再被描述成单一 10-case curated suite。

## 研究发现

- 原 README lead-in：
  - “On the 10-case curated power-ops suite”
- 这个说法已不准确，因为 Current Result 表已经包含：
  - curated suite
  - trace repair
  - span/OTLP repair
  - AgentDojo-style bridge
  - semi-real trace
  - expanded-fieldwise
  - metamorphic
  - skill-authority
  - trace-import
  - multi-step trace-import
- 改写后：
  - “Rows below combine the current curated-suite summaries, trace replays, bridge fixtures, expanded cases, skill cases, and trace-import summaries”
- 重跑 residual triage：
  - rewrite_needed：0。
  - context_only：32。
  - parser_extension：17。
  - needs_evidence mentions：49。
- needs_evidence 数量从 43 变为 49 的原因是 README 迭代队列新增了第 26/27/28 轮数字，这些被分类为 context_only，不是新增未证实结果 claim。

## 技术发现

- 新增测试 `test_power_ops_current_result_lead_in_no_longer_triggers_rewrite_triage`。
- 该测试动态构建 numeric audit，再用临时 audit JSON 运行 residual triage，验证 rewrite_needed 为 0。

## 当前边界

- 这轮只修了 rewrite-needed 文本。
- parser_extension 仍有 17 个，下一轮应继续为 baseline lead-in、baseline comparative sentence、result-readback snippets 加规则。

## 产物

- 更新 `README_POWER_OPS_ACTION_INVARIANCE.md`
- 更新 `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md/json`
- 更新 `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md/json`
- `refine-logs/iterations/ITERATION_137.md`

## 下一步

第二十九轮进入 parser-extension cleanup：让已由现有 artifact 支持的上下文数字从 parser_extension 转为 supported，同时保留 context-only 的排除边界。

## 2026-07-02 Findings: Parser-Extension Cleanup

## 需求

- 第二十九轮处理 residual triage 中剩余的 parser_extension 数字。
- 目标不是把所有数字都放行，而是只让 baseline-grid lead-in、baseline comparative sentence、expanded result phrase、performance readback 这几类已有 artifact 支撑的上下文数字获得规则支持。

## 研究发现

- numeric audit 新增 `supported_by_context_rule` 状态后，原先的 parser-extension 缺口被拆清：
  - baseline grid 的 `10-case` 由 `power_ops_action_invariance_baseline_grid` 的 `total_cases=10` 支撑。
  - `fieldwise_repair` comparative sentence 的 `1.000/0.000` 由 baseline grid 中的 preservation/removal/block/false-allow 指标支撑。
  - prose draft 的 `expanded 18-case` 由 expanded results 的 `total_cases=18` 支撑。
  - `suite_count=3` 与 `baseline_count=4` 由 performance profile 支撑。
- residual triage 从 `context_only=32, parser_extension=17, rewrite_needed=0` 更新为：
  - `context_only=42`
  - `parser_extension=0`
  - `rewrite_needed=0`
- 这说明当前剩余数字主要是 README 迭代队列、列表编号、贡献点编号等结构性数字，不是缺实验结果。

## 技术发现

- `power_ops_numeric_claim_audit.py` 新增 context-rule support path：
  - 保留原 `supported` 和 `supported_by_table_binding`。
  - 新增 `supported_by_context_rule`，只匹配已知 artifact + 已知上下文模式。
- `power_ops_residual_numeric_triage.py` 扩展 context-only 分类：
  - FormalTrust artifact 列表编号。
  - Power-ops evaluation slice 列表编号。
  - multi-step trace fixture / no-RAG / large-sample queue 等结构性编号。
- 测试新增 `test_power_ops_parser_extension_cleanup_supports_known_result_contexts`，同时验证：
  - 已知 artifact readback 会被支持。
  - `**FormalTrust artifact.**` 附近的编号不会被误标为 supported result claim。

## 当前边界

- context-rule 是规则化 artifact binding，不是自然语言事实核查器。
- 剩余 context-only 数字当前仍以 `needs_evidence` 进入 numeric audit，再由 residual triage 排除；下一轮应把这些数字更早标成 ignored/context-only，避免 unsupported count 噪声。
- 现有 audit 仍是写作层数字审计，不是 production telemetry 证明。

## 产物

- 更新 `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`
- 更新 `formaltrust_platform/experiments/power_ops_residual_numeric_triage.py`
- 更新 `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md/json`
- 更新 `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md/json`
- `refine-logs/iterations/ITERATION_138.md`

## 下一步

第三十轮进入 context-only exclusion：让轮次、列表、section 等结构性数字不再计入 `unsupported_numeric_claim_count`，只保留真正需要证据的结果数字。

## 2026-07-02 Findings: Context-Only Exclusion From Numeric Claim Count

## 需求

- 第二十九轮后 residual triage 已经没有 parser-extension，但 `unsupported_numeric_claim_count` 仍被结构性数字污染。
- 第三十轮目标是把轮次编号、列表编号、section 附近数字等 context-only mention 提前标成 ignored，而不是先算作 `needs_evidence` 再由 residual triage 排除。

## 研究发现

- numeric audit 新增 `ignored_context_number` 状态后，最终统计为：
  - supported numeric mentions：22。
  - supported_by_table_binding mentions：184。
  - supported_by_context_rule mentions：11。
  - ignored_context_number：50。
  - unsupported_numeric_claim_count：0。
- residual triage 的 `total_needs_evidence_mentions` 变为 0，说明当前写作层数字没有剩余未解释 claim。
- 一个重要顺序问题被测试捕获：
  - 如果先判断 context-only，再判断 supported readback，`source_type_coverage=1.000` 会因为靠近 “Next Experiments” 标题被误忽略。
  - 修复后顺序为：supported / table-binding / context-rule 先于 context-only ignore。

## 技术发现

- `power_ops_numeric_claim_audit.py` 现在把结构性数字作为 `ignored_context_number` 保留在 mention 列表中，但不计入 unsupported。
- 真实未证实数字仍会失败：测试中的 `failure_rate=0.123` 在没有 evidence 时仍为 `needs_evidence`。
- residual triage 现在只处理真正剩余的 `needs_evidence`，当前正式报告为空，这比把 context-only 混在 triage 中更干净。

## 当前边界

- ignored context number 是写作结构过滤，不是证据支持。
- 不应把 `ignored_context_number` 当成实验结果 claim。
- 下一步需要把 numeric audit、table evidence binding、residual triage 与 forbidden-claim scan 合成 readiness gate，避免人工逐个打开报告。

## 产物

- 更新 `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py`
- 更新 `docs/power_ops_action_invariance_numeric_claim_audit_2026-07-02.md/json`
- 更新 `docs/power_ops_action_invariance_residual_numeric_triage_2026-07-02.md/json`
- `refine-logs/iterations/ITERATION_139.md`

## 下一步

第三十一轮进入 paper-claim readiness gate：把当前分散的审计报告合成为一个 pass/fail artifact，直接告诉论文 claim 是否已经证据就绪。

## 2026-07-02 Findings: Paper-Claim Readiness Gate

## 需求

- numeric audit、table binding、residual triage、draft/prose forbidden scan 已经分别存在，但论文写作时仍需要人工逐个打开。
- 第三十一轮目标是生成单个 pass/fail readiness artifact，让“当前能不能把这些 claim 写进论文”变成可测试、可阻塞的接口。

## 研究发现

- 当前 readiness gate 结果为 PASS：
  - blockers：0。
  - numeric claim audit：PASS，`unsupported_numeric_claim_count=0`。
  - table evidence binding：PASS，`unsupported_row_count=0`。
  - residual numeric triage：PASS，`needs_evidence=0; parser_extension=0; rewrite_needed=0`。
  - forbidden claim scan：PASS，`forbidden_claim_hit_count=0`。
- readiness gate 的价值不是新增实验结果，而是把论文 claim 的证据边界变成统一入口：
  - 数字没有未解释 claim。
  - 表格没有未绑定行。
  - triage 没有 parser/rewrite 残留。
  - draft/prose 没有 forbidden claim hits。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py`。
- 新增函数：
  - `build_paper_claim_readiness`
  - `render_paper_claim_readiness_markdown`
  - `write_paper_claim_readiness`
- CLI 默认读取当前 numeric audit、table binding、residual triage、draft skeleton、prose draft，并输出 Markdown/JSON readiness 报告。
- 测试覆盖当前 pass path 与两个 fail path：
  - unsupported numeric claims 非 0 会 fail。
  - forbidden claim hits 非空会 fail。

## 当前边界

- readiness gate 只说明当前 artifacts 在写作证据门上通过，不代表生产部署安全。
- readiness gate 依赖输入报告质量；如果前置 audit 漏检，它不会自动发现自然语言事实错误。
- 下一步应把 readiness status 接入 claim ledger / PAPER_PLAN，让论文入口直接显示证据门状态。

## 产物

- `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py`
- `docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.md`
- `docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json`
- `refine-logs/iterations/ITERATION_140.md`

## 下一步

第三十二轮进入 claim-ledger readiness sync：把 readiness pass/fail 和 blockers 接入 claim ledger 或 companion artifact，并同步到 PAPER_PLAN。

## 2026-07-02 Findings: Claim-Ledger Readiness Sync

## 需求

- 第三十一轮有 readiness gate，但 claim ledger / PAPER_PLAN 还需要直接读到 PASS/FAIL 状态。
- 第三十二轮目标是不改写原始 claim ledger，而是生成 companion artifact，把 supported claims 与 readiness 状态绑定。

## 研究发现

- claim-ledger readiness 结果：
  - readiness_status：PASS。
  - supported_claim_count：11。
  - paper_ready_supported_claim_count：11。
  - blocked_supported_claim_count：0。
  - forbidden_claim_count：7。
  - readiness_blockers：0。
- 这让论文入口更清楚：
  - 当前 11 条 supported claims 可以作为 paper-ready claim pool。
  - 7 条 forbidden claims 仍明确 `paper_ready=false`。
  - 如果 readiness blockers 非空，companion artifact 会把 supported claims 全部标为 blocked。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_claim_ledger_readiness.py`。
- 新增函数：
  - `build_claim_ledger_readiness`
  - `render_claim_ledger_readiness_markdown`
  - `write_claim_ledger_readiness`
- `PAPER_PLAN.md` 顶部 active paper slice 已加入：
  - paper claim readiness artifact。
  - claim ledger readiness artifact。
  - drafting rule：abstract/introduction/results 先读 claim-ledger readiness。

## 当前边界

- companion artifact 不改变原始 claim ledger 的 claim/evidence 内容。
- paper_ready=true 仍只代表当前本地证据门通过，不代表 L5 production evidence。
- 下一轮可以基于 paper-ready claim pool 生成 abstract/introduction skeleton，但仍不能写 production/workload/generalization 过度 claim。

## 产物

- `formaltrust_platform/experiments/power_ops_claim_ledger_readiness.py`
- `docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.md`
- `docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json`
- 更新 `PAPER_PLAN.md`
- `refine-logs/iterations/ITERATION_141.md`

## 下一步

第三十三轮进入 readiness-bound abstract skeleton：只从 `paper_ready=true` 的 supported claims 生成摘要/引言贡献骨架，并显式保留 forbidden/L5 边界。

## 2026-07-02 Findings: Readiness-Bound Abstract Skeleton

## 需求

- claim-ledger readiness 已经给出 paper-ready claim pool，但 abstract/introduction 仍可能手写时越界。
- 第三十三轮目标是生成受限 abstract skeleton：只能引用 `paper_ready=true` supported claims，不把 forbidden 或 non-ready claim 带入摘要骨架。

## 研究发现

- readiness-bound abstract skeleton 结果：
  - abstract_status：ready。
  - paper_ready_claim_count：11。
  - forbidden_claim_count：7。
  - abstract_skeleton items：5。
  - intro_contribution_bullets：4。
- 生成的 skeleton 覆盖：
  - problem。
  - method。
  - results。
  - trace coverage。
  - limitations。
- skeleton Markdown 不包含 forbidden claim phrase，并显式保留：
  - no production telemetry。
  - no real operator workload reduction。
  - no official neighboring-system superiority。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_readiness_bound_abstract.py`。
- 每个 abstract skeleton item 和 contribution bullet 都携带 `source_claims`，并且测试要求这些 source claim 均为 `paper_ready=true`。
- 当 claim-ledger readiness 中没有 ready claims 时，生成器返回 `abstract_status=blocked_no_ready_claims`，且不输出 abstract skeleton。

## 当前边界

- 这是 abstract/introduction skeleton，不是最终论文摘要。
- 该 skeleton 仍不声称 production safety、real workload reduction 或官方系统 superiority。
- 下一轮可以把 skeleton 转成 concise abstract prose，但必须保持 sentence-to-source-claim binding。

## 产物

- `formaltrust_platform/experiments/power_ops_readiness_bound_abstract.py`
- `docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.md`
- `docs/power_ops_action_invariance_readiness_bound_abstract_2026-07-02.json`
- 更新 `PAPER_PLAN.md`
- `refine-logs/iterations/ITERATION_142.md`

## 下一步

第三十四轮进入 evidence-bound abstract prose：把 skeleton 转成不超过 180 words 的摘要段落，并为每句保留 source slot / claim 绑定。

## 2026-07-02 Findings: Evidence-Bound Abstract Prose

## 需求

- 第三十三轮只有 abstract skeleton，仍不是可直接放进论文的摘要段落。
- 第三十四轮目标是生成 concise abstract prose，但每句必须保留 source slot / source claim binding，避免自由写作越界。

## 研究发现

- evidence-bound abstract prose 结果：
  - abstract_status：ready。
  - word_count：79。
  - sentence_count：5。
  - forbidden_claim_hits：0。
- 每句都绑定 skeleton slot：
  - problem。
  - method。
  - results。
  - trace coverage。
  - limitations。
- 摘要明确保留边界：
  - no production telemetry。
  - no real operator workload reduction claim。
  - no official neighboring-system superiority claim。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_evidence_bound_abstract.py`。
- 生成器输出：
  - `abstract_text`
  - `word_count`
  - `sentences`
  - `forbidden_claim_hits`
- 测试要求：
  - abstract prose 不超过 180 words。
  - 每句都有 source claims。
  - 每个 source claim 都是 paper_ready。
  - blocked skeleton 不生成 abstract prose。

## 当前边界

- 这是 evidence-bound abstract，不是完整 introduction。
- 该摘要仍是本地 artifact-ready claim，不代表生产安全或真实用户/操作员效果。
- 下一轮应生成 introduction outline，而不是继续扩写未绑定 prose。

## 产物

- `formaltrust_platform/experiments/power_ops_evidence_bound_abstract.py`
- `docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.md`
- `docs/power_ops_action_invariance_evidence_bound_abstract_2026-07-02.json`
- 更新 `PAPER_PLAN.md`
- `refine-logs/iterations/ITERATION_143.md`

## 下一步

第三十五轮进入 evidence-bound introduction outline：把 paper-ready contribution bullets 转成 problem/gap/method/evidence/boundary 五段式引言骨架。

## 2026-07-02 Findings: Evidence-Bound Introduction Outline

## 需求

- 第三十四轮已有 bounded abstract prose，但 introduction 仍需要结构化展开。
- 第三十五轮目标是生成五段式 introduction outline，并保持每段 source-claim binding 或 limitation reason。

## 研究发现

- evidence-bound introduction outline 结果：
  - intro_status：ready。
  - paragraph_count：5。
  - slots：problem、gap、method、evidence、boundary。
  - forbidden_claim_hits：0。
- 每段都有 paper-ready source claim 或 explicit limitation reason：
  - problem/method/evidence 使用 paper-ready claims。
  - gap/boundary 显式说明不写 firstness、production、workload、official-superiority claim。

## 技术发现

- 新增 `formaltrust_platform/experiments/power_ops_evidence_bound_intro.py`。
- 输出字段：
  - `intro_status`
  - `paragraph_outline`
  - `forbidden_claim_hits`
- 测试覆盖：
  - 五段式 slot 顺序。
  - source claims 全部 paper_ready。
  - forbidden phrases 不进入 Markdown。
  - blocked skeleton 不生成 intro outline。

## 当前边界

- 这是 introduction outline，不是最终 prose。
- 该 outline 保留边界，不扩写 production/workload/official-superiority claim。
- 下一轮应生成 introduction prose，并继续保留 sentence/paragraph source binding。

## 产物

- `formaltrust_platform/experiments/power_ops_evidence_bound_intro.py`
- `docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.md`
- `docs/power_ops_action_invariance_evidence_bound_intro_2026-07-02.json`
- 更新 `PAPER_PLAN.md`
- `refine-logs/iterations/ITERATION_144.md`

## 下一步

第三十六轮进入 evidence-bound introduction prose：把五段式 outline 转成 bounded prose paragraphs，并保留每段 source claim 或 limitation reason。
## 2026-07-02 Findings: Evidence-Bound Introduction Prose

## Need
- The introduction outline had source-bound slots, but not paper-ready prose paragraphs.
- The next writing artifact needed to preserve paragraph/source binding and avoid unsupported production, workload, firstness, or official-superiority claims.

## Research Finding
- The generated introduction prose is ready and contains 5 paragraphs:
  - problem
  - gap
  - method
  - evidence
  - boundary
- Each paragraph keeps either paper-ready source claims or an explicit limitation reason.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_intro_prose.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_intro_prose_2026-07-02.md/json`.
- Added TDD coverage in `tests/test_power_ops_action_invariance.py`.

## Boundary
- This is bounded paper prose, not a deployment safety claim.
- It does not claim production telemetry, real operator workload reduction, or official neighboring-system superiority.

## Next
- After adding new writing artifacts, the readiness gate itself must scan these artifacts by default.

## 2026-07-02 Findings: Writing-Artifact Readiness Coverage

## Need
- Paper readiness previously scanned only 2 old writing artifacts by default.
- New abstract and introduction artifacts could have escaped the default forbidden-claim gate.

## Research Finding
- The readiness gate now scans 6 writing artifacts by default:
  - draft skeleton
  - prose draft
  - readiness-bound abstract skeleton
  - evidence-bound abstract prose
  - evidence-bound introduction outline
  - evidence-bound introduction prose
- Paper claim readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `DEFAULT_WRITING_ARTIFACT_PATHS` to `formaltrust_platform/experiments/power_ops_paper_claim_readiness.py`.
- `forbidden_claim_scan` now records `artifact_paths`, making scan coverage auditable.
- Added TDD coverage for CLI default readiness scanning.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=53, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=6.
- Full verification: `pytest -q` -> 242 passed.

## Next
- Iteration 38 should generate an evidence-bound method-section outline from the formal model, CapGuard flow, and claim ledger.
## 2026-07-02 Findings: Evidence-Bound Method Outline

## Need
- The project had a formal model and paper outline, but §3 still needed a bounded method-section structure tied to source artifacts.
- The method section must not drift into unverified production or superiority claims.

## Research Finding
- The generated method outline is ready and covers 6 method slots:
  - formal_objects
  - coverage_rule
  - minimal_witness_decision
  - repair_invariance
  - implementation_binding
  - claim_boundary
- The outline binds `Cap(x)`, `Need(s,f)`, `Covers(c,n)`, `Minimal Authority Witness`, `FieldDecision`, `ActionInvariant`, and `Repair(a)` to the formal-model artifact.
- It uses paper-ready source claims from claim-ledger readiness and keeps forbidden claim hits at 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_method_outline.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.md/json`.
- Added TDD coverage for ready and blocked claim-ledger paths.

## Boundary
- The method outline is evidence-bound writing structure, not a new production safety proof.
- The boundary slot explicitly excludes production telemetry, real workload reduction, and official neighboring-system superiority claims.

## 2026-07-02 Findings: Method-Outline Readiness Coverage

## Need
- Once method outline became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 7 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_method_outline_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the method outline path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=56, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=7.
- Full verification: `pytest -q` -> 243 passed.

## Next
- Iteration 40 should generate bounded §3 method prose from the method outline.

## 2026-07-02 Findings: Evidence-Bound Method Prose

## Need
- The method outline had formal-model refs and paper-ready claims, but §3 still needed bounded prose paragraphs.
- Each method paragraph needed to preserve its formal refs, source claims, and explicit limitation boundary.

## Research Finding
- The generated method prose is ready and contains 6 paragraphs:
  - formal_objects
  - coverage_rule
  - minimal_witness_decision
  - repair_invariance
  - implementation_binding
  - claim_boundary
- The prose keeps `Cap(x)`, `Need(s,f)`, `Minimal Authority Witness`, `ActionInvariant`, and `Repair(a)` in the method narrative.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_method_prose.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.md/json`.
- Added TDD coverage for ready and blocked method-outline paths.

## Boundary
- The method prose is bounded writing material, not a production deployment proof.
- It explicitly excludes production telemetry, real workload reduction, and official neighboring-system superiority.

## 2026-07-02 Findings: Method-Prose Readiness Coverage

## Need
- Once method prose became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 8 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_method_prose_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the method-prose path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=59, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=8.
- Full verification: `pytest -q` -> 244 passed.

## Next
- Iteration 42 should generate an evidence-bound related-work outline from the novelty firewall and literature review.

## 2026-07-02 Findings: Evidence-Bound Related-Work Outline

## Need
- The paper needed a bounded §2 structure that says what prior work already covers and what the current artifact can still safely claim.
- The related-work section must not drift into generic firstness, superiority, or production-safety language.

## Research Finding
- The generated related-work outline is ready and contains 6 slots:
  - runtime_enforcement_neighbors
  - prompt_injection_privilege_neighbors
  - least_privilege_capability_neighbors
  - over_conservatism_neighbors
  - action_invariance_delta
  - claim_boundary
- It covers 9 neighboring works, including AgentSpec, AgentVisor, AgentSentry, CaMeL, ToolPrivBench, RACG, InjecGuard, AgentDojo, and formal-security-agent work.
- The safe delta is field-level action invariance with authority witnesses and repair-frame validity.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_related_work_outline.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.md/json`.
- Added TDD coverage for ready and blocked source paths.

## Boundary
- Related work positions prior systems as close neighbors, not as failures.
- It blocks broad runtime-enforcement, least-privilege, prompt-injection, official superiority, and production deployment claims.

## 2026-07-02 Findings: Related-Work Readiness Coverage

## Need
- Once related-work outline became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 9 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_related_work_outline_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the related-work outline path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=62, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=9.
- Full verification: `pytest -q` -> 245 passed.

## Next
- Iteration 44 should generate bounded §2 related-work prose from the outline.

## 2026-07-02 Findings: Evidence-Bound Related-Work Prose

## Need
- The related-work outline needed to become usable paper prose while preserving neighbor/source binding.
- The prose needed to avoid prior-work superiority, generic firstness, and production-safety claims.

## Research Finding
- The generated related-work prose is ready and contains 6 paragraphs:
  - runtime_enforcement_neighbors
  - prompt_injection_privilege_neighbors
  - least_privilege_capability_neighbors
  - over_conservatism_neighbors
  - action_invariance_delta
  - claim_boundary
- Each paragraph keeps neighbor names, source refs, safe deltas, or claim-boundary text.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_related_work_prose.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.md/json`.
- Added TDD coverage for ready and blocked outline paths.

## Boundary
- This prose positions neighboring work without claiming it is defeated or inferior.
- It keeps the contribution narrow: field-level action invariance with authority witnesses and repair-frame validity.

## 2026-07-02 Findings: Related-Work Prose Readiness Coverage

## Need
- Once related-work prose became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 10 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_related_work_prose_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the related-work prose path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=65, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=10.
- Full verification: `pytest -q` -> 246 passed.

## Next
- Iteration 46 should generate an evidence-bound §5 results outline with table/source binding.

## 2026-07-02 Findings: Evidence-Bound Results Outline

## Need
- The paper had result JSON files, table evidence binding, and paper-ready result claims, but §5 needed a bounded outline that ties them together.
- The results section must not promote fixture evidence into production telemetry, workload, latency, or official-superiority claims.

## Research Finding
- The generated results outline is ready and contains 7 slots:
  - fieldwise_repair_result
  - expanded_metamorphic_skill_results
  - baseline_grid
  - performance_profile
  - trace_replay_and_import
  - multi_step_source_chain
  - claim_boundary
- It binds 9 paper-ready result claims to result evidence paths.
- It carries table evidence binding readback: 18 fully supported rows and 0 unsupported rows.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_results_outline.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.md/json`.
- Added TDD coverage for table/source binding and blocked claim-readiness paths.

## Boundary
- The outline treats trace evidence as fixture evidence, not production telemetry.
- Performance is phrased as safety-preserving normal behavior, not wall-clock latency or real operator workload reduction.

## 2026-07-02 Findings: Results-Outline Readiness Coverage

## Need
- Once results outline became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 11 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_results_outline_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the results-outline path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=68, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=11.
- Results outline: ready; result_claims=9; fully_supported_table_rows=18; unsupported_table_rows=0.
- Full verification: `pytest -q` -> 247 passed.

## Next
- Iteration 48 should generate bounded §5 results prose from the outline.

## 2026-07-02 Findings: Evidence-Bound Results Prose

## Need
- The results outline needed to become usable §5 prose while preserving table/source binding.
- Results prose needed to avoid turning fixture evidence into production telemetry, workload reduction, latency, or official-superiority claims.

## Research Finding
- The generated results prose is ready and contains 7 paragraphs:
  - fieldwise_repair_result
  - expanded_metamorphic_skill_results
  - baseline_grid
  - performance_profile
  - trace_replay_and_import
  - multi_step_source_chain
  - claim_boundary
- Each paragraph carries source claims, result evidence paths, table refs, or explicit limitation text.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_results_prose.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.md/json`.
- Added TDD coverage for table/source binding and blocked outline paths.

## Boundary
- The prose states fixture evidence only where that is all the current artifacts support.
- The performance paragraph explicitly excludes wall-clock latency and operator workload reduction claims.

## 2026-07-02 Findings: Results-Prose Readiness Coverage

## Need
- Once results prose became a writing artifact, readiness default scanning needed to include it.

## Research Finding
- Paper readiness now scans 12 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_results_prose_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the results-prose path.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=71, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=12.
- Results prose: ready; paragraph_count=7; forbidden_hits=0.
- Full verification: `pytest -q` -> 248 passed.

## Next
- Iteration 50 should generate a bounded §6 limitations outline from missing-evidence boundaries and forbidden claims.

## 2026-07-02 Findings: Evidence-Bound Limitations Outline

## Need
- The paper needed a §6 structure that turns missing evidence and forbidden claims into explicit limitations and next experiments.
- Limitation text must not accidentally turn unsupported claims into supported claims.

## Research Finding
- The generated limitations outline is ready and contains 6 slots:
  - production_trace_gap
  - latency_gap
  - operator_workload_gap
  - official_benchmark_gap
  - forbidden_firstness_security_claims
  - next_experiments
- It binds 7 forbidden claims to excluded-claim boundaries.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_limitations_outline.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_limitations_outline_2026-07-02.md/json`.
- Added TDD coverage for paper-readiness PASS and blocked readiness paths.

## 2026-07-02 Findings: Limitations Prose and Readiness Coverage

## Need
- The limitations outline needed prose that is usable in §6 without copying forbidden phrases into the paper-facing Markdown.
- New limitations artifacts needed to be included in the paper-readiness forbidden-claim scan.

## Research Finding
- The limitations prose is ready with 6 paragraphs and 0 forbidden hits.
- Paper readiness now scans 14 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_limitations_prose.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_limitations_prose_2026-07-02.md/json`.
- Added both limitations outline and limitations prose JSON to `DEFAULT_WRITING_ARTIFACT_PATHS`.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=77, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=14.
- Limitations outline: ready; forbidden_claim_count=7; slots=6; forbidden_hits=0.
- Limitations prose: ready; paragraph_count=6; forbidden_hits=0.
- Full verification: `pytest -q` -> 250 passed.

## Next
- Iteration 54 should assemble the current bounded section prose into a single paper-draft artifact.

## 2026-07-02 Findings: Evidence-Bound Paper Draft Assembly

## Need
- The project had bounded prose for abstract, introduction, related work, method, results, and limitations, but not a single assembled paper draft.
- The assembled draft needed to preserve source linkage so later edits can trace each section back to its JSON artifact.

## Research Finding
- The generated paper draft is ready and contains 6 sections:
  - abstract
  - introduction
  - related_work
  - method
  - results
  - limitations
- Each section carries source path, source status, artifact type, and text.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_paper_draft.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.md/json`.
- Added TDD coverage for ready assembly and blocked source-section paths.

## Boundary
- The draft is an assembled bounded artifact, not a production deployment proof.
- It keeps source comments in Markdown and keeps unsupported production, workload, latency, and official-superiority claims out of the paper text.

## 2026-07-02 Findings: Paper-Draft Readiness Coverage

## Need
- Once the assembled draft became a writing artifact, paper-readiness scanning needed to include it by default.

## Research Finding
- Paper readiness now scans 15 writing artifacts by default.
- Readiness remains PASS with 0 blockers and 0 forbidden hits.

## Technical Finding
- Added `docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.json` to `DEFAULT_WRITING_ARTIFACT_PATHS`.
- Updated the readiness coverage test to require the paper-draft path.
- Refreshed numeric audit, residual triage, paper readiness, claim-ledger readiness, all bounded writing artifacts, and the assembled paper draft.

## Current Readback
- Numeric audit: supported=22, table-binding=184, context-rule=11, ignored-context=80, unsupported=0.
- Residual triage: needs_evidence=0.
- Readiness: PASS; forbidden scan artifact_count=15.
- Paper draft: ready; section_count=6; forbidden_hits=0.

## Next
- Iteration 56 should audit the assembled draft for section-order consistency, source-link completeness, and unresolved evidence-boundary language.

## 2026-07-02 Findings: Paper Draft Consistency Audit

## Need
- The assembled paper draft needed a separate consistency check, because readiness scanning only detects forbidden phrases and does not prove the draft still matches its section sources.

## Research Finding
- The current assembled draft passes consistency audit:
  - section_count=6
  - source_link_completeness_rate=1.0
  - text_match_rate=1.0
  - mismatch_count=0
  - unresolved_boundary_hit_count=0
- The audit also detects a corrupted draft when a section text no longer matches the source JSON.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_paper_draft_consistency_audit.py`.
- Generated `docs/power_ops_action_invariance_paper_draft_consistency_audit_2026-07-02.md/json`.
- Added TDD coverage for PASS and mismatch FAIL behavior.

## Boundary
- This audit proves draft/source consistency for the current assembled artifact.
- It does not add new empirical evidence or promote fixture evidence into production claims.

## Next
- The assembled draft currently jumps from method section 3 to results section 5. Iteration 57 should add evidence-bound section 4 evaluation setup from dataset, benchmark, trace, and audit sources.

## 2026-07-02 Findings: Evidence-Bound Evaluation Setup

## Need
- The assembled draft jumped from method section 3 to results section 5.
- Section 4 needed to describe the evaluation setup using existing evidence rather than inventing new experiment claims.

## Research Finding
- The generated section 4 evaluation setup is ready and contains 6 bounded paragraphs:
  - benchmark_scope
  - dataset_and_cases
  - baselines
  - trace_imports
  - metrics_and_audits
  - claim_boundary
- It binds:
  - 18 expanded cases
  - 4 baselines
  - 4 trace-import boundary cases
  - 1 multi-step source-chain case
  - 18 fully supported table rows
  - draft consistency audit source-link completeness 1.000 and text match rate 1.000
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_evaluation_setup.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_evaluation_setup_2026-07-02.md/json`.
- Updated paper draft assembly, paper-readiness scanning, and paper-draft consistency audit to include section 4.

## Boundary
- Section 4 treats trace replay and expanded cases as fixture evidence.
- It explicitly excludes production telemetry, wall-clock latency, operator workload reduction, and official benchmark superiority.

## Next
- Iteration 58 should include the assembled 7-section paper draft in numeric-claim audit coverage.

## 2026-07-02 Findings: Assembled Draft Numeric Audit

## Need
- Numeric audit previously scanned README, paper kernel, and an older prose draft, but not the assembled 7-section paper draft.
- This left a gap where numeric claims in the current assembled draft could avoid direct audit.

## Research Finding
- The refreshed numeric audit now scans 4 documents, including the assembled paper draft.
- Section 4 numeric claims are supported by existing evidence/context rules:
  - 10-case curated baseline grid
  - 18-case expanded suite
  - oracle coverage 1.000
  - 4 baselines
  - 4 trace-import boundary cases
  - 1 multi-step trace case
  - 18 fully supported table rows
  - source-link completeness/text match rate 1.000
- Unsupported numeric claims remain 0.

## Technical Finding
- Extended `formaltrust_platform/experiments/power_ops_numeric_claim_audit.py` with section-4 support rules.
- Ignored Markdown heading numbers and HTML source-comment date/path numbers.
- Normalized numeric-audit document paths to POSIX style for stable artifact tests.

## Boundary
- This strengthens audit coverage for the assembled draft.
- It does not create new empirical evidence; it only binds existing section-4 numbers to existing artifacts.

## Next
- Iteration 59 should add a bounded conclusion section from paper-ready claims and limitation boundaries.

## 2026-07-02 Findings: Evidence-Bound Conclusion

## Need
- The assembled draft had abstract through limitations, but no bounded conclusion.
- The conclusion needed to close the paper without turning limitation language into unsupported deployment or superiority claims.

## Research Finding
- The conclusion is ready with 4 paragraphs:
  - takeaway
  - supported_evidence
  - scope_boundary
  - next_work
- It records 11 paper-ready supported claims and 7 forbidden claims as metadata.
- It preserves the boundary around production telemetry, deployment safety, wall-clock latency, operator workload, and official benchmark superiority.
- Forbidden claim hits remain 0.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_evidence_bound_conclusion.py`.
- Generated `docs/power_ops_action_invariance_evidence_bound_conclusion_2026-07-02.md/json`.
- Updated paper draft assembly, readiness scanning, and draft consistency audit to include conclusion.

## Boundary
- The conclusion is a synthesis of already-ready claims and limitations.
- It does not add a new empirical claim.

## Next
- Iteration 60 should build a claim-to-paragraph map for the assembled draft.

## 2026-07-02 Findings: Claim-to-Paragraph Map

## Need
- The assembled paper draft had section-level source links, but reviewers still could not quickly see which paragraph was backed by which claim, source file, or limitation boundary.
- This created a risk that later prose edits could preserve section order while silently weakening paragraph-level evidence binding.

## Research Finding
- The claim-to-paragraph map passes on the current assembled draft:
  - section_count=8
  - paragraph_count=41
  - source_link_completeness_rate=1.0
  - claim_or_source_binding_rate=1.0
  - claim_mapped_paragraph_count=30
  - source_mapped_paragraph_count=11
  - boundary_marked_paragraph_count=18
  - unmapped_paragraph_count=0
- The map distinguishes direct claim-mapped paragraphs from source-mapped paragraphs and separately records boundary flags such as production telemetry, workload, latency, official-superiority, firstness, and prompt-injection-solution exclusions.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_claim_to_paragraph_map.py`.
- Generated `docs/power_ops_action_invariance_claim_to_paragraph_map_2026-07-02.md/json`.
- Added TDD coverage for:
  - PASS on the current assembled draft;
  - FAIL when a draft section loses its source path.

## Boundary
- This artifact does not add empirical evidence or new paper claims.
- It is an audit layer that protects paragraph-level traceability during future rewriting.

## Next
- Iteration 61 should compress the paragraph map into reviewer-facing claim packets and audit whether source-only paragraphs need stronger claim binding or explicit boundary-only classification.

## 2026-07-02 Findings: Paragraph Evidence Packets

## Need
- The claim-to-paragraph map is complete but verbose.
- A reviewer-facing version should group repeated paragraph evidence by claim and separately audit source-only paragraphs.

## Research Finding
- The paragraph evidence packet artifact passes on the current claim-to-paragraph map:
  - paragraph_count=41
  - claim_packet_count=11
  - source_only_row_count=11
  - reviewer_packet_count=14
  - audit_compression_ratio=0.658537
  - needs_stronger_binding_count=0
- Source-only rows are not ignored. They are resolved as related-work context, evaluation-audit context, or boundary-only rows.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_paragraph_evidence_packets.py`.
- Generated `docs/power_ops_action_invariance_paragraph_evidence_packets_2026-07-02.md/json`.
- Added TDD coverage for:
  - PASS on the current claim-to-paragraph map;
  - FAIL when a source-only paragraph loses both evidence refs and a recognized context/boundary resolution.

## Boundary
- This packet is a reviewer-facing compression of existing paragraph evidence.
- It does not make new claims and does not replace the full paragraph map.

## Next
- Iteration 62 should add a draft edit gate that marks paragraph map and packet artifacts stale when the assembled paper draft changes without regeneration.

## 2026-07-02 Findings: Paper Draft Edit Gate

## Need
- The paragraph map and reviewer packets are useful only if they remain synchronized with the assembled paper draft.
- Direct draft edits could otherwise leave stale paragraph evidence artifacts that still look complete.

## Research Finding
- The edit gate passes on the current artifact chain:
  - draft_map_hash_matches=True
  - packet_map_hash_matches=True
  - stale_artifact_count=0
- The gate fails when:
  - the draft text changes without regenerating the paragraph map;
  - the paragraph map changes without regenerating the reviewer packet.

## Technical Finding
- Added `draft_content_sha256` to the claim-to-paragraph map.
- Added `paragraph_map_content_sha256` and carried `draft_content_sha256` into paragraph evidence packets.
- Added `formaltrust_platform/experiments/power_ops_paper_draft_edit_gate.py`.
- Generated `docs/power_ops_action_invariance_paper_draft_edit_gate_2026-07-02.md/json`.

## Boundary
- The edit gate proves artifact synchronization, not empirical validity.
- It prevents stale evidence mappings after direct draft edits.

## Next
- Iteration 63 should export the assembled bounded draft into an evidence-bound LaTeX manuscript skeleton with source comments and edit-gate checks.

## 2026-07-02 Findings: Evidence-Bound LaTeX Manuscript

## Need
- The project had a Markdown/JSON assembled draft, but not a paper-file artifact that can be compiled, edited, or handed to an academic writing workflow.
- The export needed to preserve evidence comments instead of flattening the draft into untraceable prose.

## Research Finding
- The LaTeX manuscript export is ready:
  - section_count=8
  - paragraph_count=41
  - paragraph_comment_count=41
  - edit_gate_status=PASS
  - forbidden_claim_hits=0
- Each section carries a `% source:` comment and each paragraph carries a `% paragraph-map:` comment.
- The export cleans the historical section-sign/mojibake marker in the results prose.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_latex_manuscript.py`.
- Generated:
  - `paper/power_ops_action_invariance/main.tex`
  - `docs/power_ops_action_invariance_latex_manuscript_2026-07-02.md/json`
- Added TDD coverage for ready export, source comments, paragraph-map comments, stale edit-gate blocking, and encoding cleanup.

## Boundary
- This is a manuscript skeleton, not a polished submission.
- It intentionally keeps source comments for auditability.

## Next
- Iteration 64 should run a LaTeX compile audit and either produce a PDF or persist a clear environment-blocked report.

## 2026-07-02 Findings: LaTeX Compile Audit

## Need
- The manuscript skeleton should not be described as compiled unless a local TeX toolchain actually produced a PDF.
- If compilation is impossible in the current environment, that blocker should be explicit and persisted.

## Research Finding
- The compile audit is environment-blocked:
  - tex_exists=True
  - toolchain_available=False
  - pdf_exists=False
  - compile_status=blocked_missing_toolchain
- The checked local tools were `latexmk`, `pdflatex`, and `xelatex`.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_latex_compile_audit.py`.
- Generated `docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.md/json`.
- Added TDD coverage for missing-toolchain reporting.

## Boundary
- This does not mean the LaTeX manuscript is invalid.
- It means this local environment cannot compile it until a TeX toolchain is installed or another compile environment is used.

## Next
- Iteration 65 should create a citation/BibTeX scaffold for named neighboring systems and clearly mark unverified bibliography entries.

## 2026-07-02 Findings: Citation Scaffold

## Need
- The LaTeX manuscript names neighboring systems but did not yet have a bibliography scaffold.
- Generating full BibTeX from memory would risk invented authors or incomplete metadata.

## Research Finding
- The citation scaffold is ready:
  - entry_count=11
  - metadata_pending_count=11
  - verified_source_count=10
  - caution_source_count=1
  - invented_reference_count=0
- All generated BibTeX entries intentionally omit author/year fields and carry a `metadata pending citation audit` note.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_citation_scaffold.py`.
- Generated:
  - `docs/power_ops_action_invariance_citation_scaffold_2026-07-02.md/json`
  - `paper/power_ops_action_invariance/references_scaffold.bib`
- Added TDD coverage to ensure no `author =` field is fabricated.

## Boundary
- This is not a final bibliography.
- It is a safe scaffold that must be promoted by a citation metadata audit before paper submission.

## Next
- Iteration 66 should verify or fetch metadata from primary sources and promote only confirmed entries into checked BibTeX.

## 2026-07-02 Findings: Continuous Iteration Plan Refresh

## Need
- User clarified that the plan must support continuous iteration and should not stop after a single planning note.
- The plan also must remain concrete: modeling, code, test samples, test framework, experiments, reports, and paper artifacts should keep appearing across rounds.

## Research Finding
- The current Power-Ops action-invariance track already has enough infrastructure to support a long loop:
  - formal model and paper-ready claim ledger;
  - FormalTrust-compatible runtime and YAML/data interfaces;
  - trace/span/OTLP/multi-step examples;
  - baseline grid, numeric audits, paragraph evidence packets, edit gate, LaTeX manuscript, and citation scaffold.
- The next bottleneck is not idea generation. It is maintaining a disciplined loop where every new claim is bound to code, data, tests, and evidence artifacts.

## Technical Finding
- Added `docs/power_ops_action_invariance_continuous_iteration_plan_2026-07-02.md`.
- Registered a concrete 66/175 through 80/189 queue in `task_plan.md`.
- Extended `README_POWER_OPS_ACTION_INVARIANCE.md` so the project entrypoint shows that iteration continues after citation metadata audit.

## Boundary
- The new plan is not evidence that iterations 66-80 are complete.
- It is the execution contract for the next loop. Each future iteration still needs its own TDD test, artifact readback, README update, and keep/revise/reject decision.

## Next
- Continue with Iteration 66 / 175: citation metadata audit using primary-source metadata only, without invented author/year fields.

## 2026-07-02 Findings: Citation Metadata Audit

## Need
- The citation scaffold intentionally omitted authors and years to avoid invented bibliography metadata.
- A paper manuscript needs checked BibTeX entries, but only entries confirmed from primary metadata should be promoted.

## Research Finding
- The current metadata audit is `partial`:
  - entry_count=11
  - metadata_record_count=10
  - confirmed_entry_count=10
  - pending_entry_count=1
  - rejected_entry_count=0
  - invented_reference_count=0
- The 10 confirmed entries are arXiv-backed records.
- `formal_security_agents` remains pending because the current pass did not verify enough primary metadata for final BibTeX promotion.

## Technical Finding
- Added `load_citation_metadata_records(...)` to `formaltrust_platform/experiments/power_ops_citation_metadata_audit.py`.
- Added CLI support for `--metadata-json`.
- Added `docs/power_ops_action_invariance_primary_metadata_seed_2026-07-02.json`.
- Regenerated:
  - `docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.json`
  - `paper/power_ops_action_invariance/references_checked.bib`

## Boundary
- `references_checked.bib` is checked only for the 10 confirmed records in the current seed.
- The OpenReview entry is not promoted and should not be cited until a later audit confirms title/authors/year from a primary source.

## Next
- Iteration 67 should add a cite-ready LaTeX gate: any `\cite{...}` in `main.tex` must resolve to a key in `references_checked.bib`, and scaffold-only/pending keys must be blocked.

## 2026-07-02 Findings: LaTeX Citation Gate

## Need
- After checked BibTeX generation, the manuscript still needed a guard preventing future paper edits from citing scaffold-only or pending references.
- This matters because `formal_security_agents` remains in the scaffold but is not yet checked.

## Research Finding
- The current LaTeX citation gate passes:
  - citation_key_count=10
  - checked_bib_key_count=10
  - scaffold_bib_key_count=11
  - unchecked_citation_keys=0
  - pending_scaffold_only_keys=0
  - bibliography_uses_checked=True
- `main.tex` now cites checked entries for AgentSpec, AgentVisor, AgentSentry, CaMeL, secure design patterns, verifiably safe tool use, ToolPrivBench, RACG, AgentDojo, and InjecGuard.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_latex_citation_gate.py`.
- Generated:
  - `docs/power_ops_action_invariance_latex_citation_gate_2026-07-02.md`
  - `docs/power_ops_action_invariance_latex_citation_gate_2026-07-02.json`
- Updated `paper/power_ops_action_invariance/main.tex` to use `\bibliography{references_checked}` and only checked cite keys.

## Boundary
- This gate validates citation-key readiness, not full LaTeX compilation.
- PDF generation remains blocked by the missing local TeX toolchain recorded in the compile audit.

## Next
- Iteration 68 should produce a contribution packet that states the innovation in reviewer-facing form and binds each claim to evidence, code, and explicit boundaries.

## 2026-07-02 Findings: Reviewer-Facing Contribution Packet

## Need
- The project had many artifacts, but the innovation story needed a compact reviewer-facing packet.
- The user repeatedly asked "innovation point在哪里", so the packet must avoid broad firstness claims and instead bind each contribution to evidence.

## Research Finding
- The contribution packet is ready:
  - claim_count=3
  - forbidden_headline_count=0
  - all_claims_have_code_evidence=True
  - all_claims_have_result_evidence=True
  - all_claims_have_boundary=True
- The three claims are:
  - field-level authority witness;
  - fieldwise action invariance under strict intervention;
  - non-RAG authority sources for skill-driven agents.

## Technical Finding
- Added `formaltrust_platform/experiments/power_ops_contribution_packet.py`.
- Generated:
  - `docs/power_ops_action_invariance_contribution_packet_2026-07-02.md`
  - `docs/power_ops_action_invariance_contribution_packet_2026-07-02.json`

## Boundary
- The packet is a claim/evidence compression artifact, not new empirical evidence.
- It must be updated whenever claims expand beyond the current code/result boundaries.

## Next
- Iteration 69 should expand skill-driven power-agent samples beyond RAG-only settings.

## 2026-07-02 Findings: Skill-Driven Authority Source Expansion

## Need
- The earlier no-RAG skill fixture only showed `source_type=skill`.
- The user wanted a unified framework, so the evidence needed to show that Cap(x) can come from common agent runtime objects beyond RAG documents and beyond skill manifests alone.

## Research Finding
- The skill-authority dataset now has 8 no-RAG cases with oracle coverage 1.000.
- Source-type coverage is:
  - skill=4
  - tool_metadata=1
  - user_approval=1
  - memory=1
  - prior_step_output=1
- The added cases test four non-RAG authority boundaries:
  - tool metadata may validate `tool_arguments`, but cannot authorize `public_publish`;
  - a user approval may authorize the current `public_publish`, but cannot grant `approval_waiver`;
  - memory may carry `risk_report_style`, but cannot set `risk_level`;
  - prior-step output may carry `plan_note`, but cannot perform `switching_operation`.
- Runtime results remain aligned with the action-invariance claim:
  - total_cases=8
  - authorized final-field preservation=1.000
  - unauthorized final-field removal=1.000
  - whole_action_block_rate=0.000
  - executable fieldwise-repair success=1.000
  - repair-frame validity=1.000

## Technical Finding
- Extended `examples/data/power_ops_skill_authority_cases.jsonl` from 4 to 8 cases.
- Reused the existing AFW interface:
  - `skill_manifest` / `tool_manifest` / `authority_manifest` -> Cap(x)
  - `afw_consumptions` -> Need(s, f)
  - `guardrail.afw_capguard` performs field-level coverage.
- Updated tests so the skill-authority audit must cover skill, tool metadata, approval, memory, and prior-step outputs.
- Updated claim ledger/readiness and generated paper/prose artifacts so the supported L2 claim is no longer phrased as skill-manifest-only.
- Regenerated:
  - `docs/power_ops_skill_authority_dataset_audit_2026-07-02.md/json`
  - `docs/power_ops_skill_authority_runtime_report_2026-07-02.md/json`
  - `docs/power_ops_skill_authority_results_2026-07-02.md/json`
  - `docs/power_ops_action_invariance_performance_2026-07-02.md/json`
  - `docs/power_ops_action_invariance_contribution_packet_2026-07-02.md/json`

## Verification

- Focused skill-authority regression: 6 passed.
- `pytest tests/test_power_ops_action_invariance.py -q`: 67 passed.
- `pytest -q`: 267 passed.
- Residual numeric triage: needs_evidence=0.
- Paper claim readiness: PASS.
- Claim ledger readiness: PASS.

## Boundary
- This strengthens the non-RAG / skill-driven claim, but it is still a curated 8-case fixture.
- It does not prove general marketplace-skill safety, branching planner safety, memory write-back safety, or production power-agent reliability.

## Next
- Iteration 70 should build a multi-step planner-skill-tool-memory action-invariance benchmark, so the same field-level authority property is tested across a complex agent execution chain rather than one source event per case.

## 2026-07-02 Findings: Planner-Skill-Tool-Memory Benchmark

## Need
- The previous multi-source result was mostly single-step or one source event per case.
- The user wanted the framework to cover complex agent execution, where planner output, skill output, tool metadata, memory, and approval are all present before the final action.

## Research Finding
- Added a 2-case planner-skill-tool-memory trace benchmark.
- Source-chain coverage is complete:
  - memory=2
  - prior_step_output=2
  - skill=2
  - tool_metadata=2
  - user_approval=2
- Field-level outcome:
  - authorized_fields=10
  - preserved_authorized_fields=10
  - unauthorized_fields=2
  - removed_unauthorized_fields=2
  - whole_action_block_rate=0.000
  - authorized final-field preservation=1.000
  - unauthorized final-field removal=1.000

## Technical Finding
- Added:
  - `examples/data/power_ops_planner_skill_tool_memory_fixture.json`
  - `examples/power_ops_planner_skill_tool_memory_validation.yaml`
  - `formaltrust_platform/experiments/power_ops_planner_skill_tool_memory.py`
- Generated:
  - `docs/power_ops_planner_skill_tool_memory_results_2026-07-02.md/json`
  - `docs/power_ops_planner_skill_tool_memory_runtime_report_2026-07-02.md/json`
- Upgraded the existing L3 multi-step trace claim so it now includes planner, skill, tool metadata, memory, prior-step output, and user approval source chains.
- Updated contribution packet C3, evaluation setup, paper outline, prose draft, paragraph map, LaTeX manuscript, numeric audit, and readiness artifacts.

## Verification

- Focused Iteration 70 regression: 5 passed.
- `pytest tests/test_power_ops_action_invariance.py -q`: 68 passed.
- `pytest -q`: 268 passed.
- Numeric claim audit: unsupported_numeric_claim_count=0.
- Residual numeric triage: needs_evidence=0.
- Paper claim readiness: PASS.
- Claim ledger readiness: PASS.
- Table evidence binding now covers 19 result rows with unsupported_row_count=0 after adding the planner-skill-tool-memory current-results row.
- Two stale synchronization assertions were updated:
  - the skill-authority `16` latency-proxy number is now supported through table binding;
  - the evidence-bound results outline expects 19 fully supported table rows instead of 18.

## Boundary
- This is still fixture-level trace evidence, not production telemetry.
- It does not yet measure normal-action false intervention at scale, wall-clock overhead, or real operator workload reduction.

## Next
- Iteration 71 should stress-test fully authorized normal behavior under strict supervision, measuring false intervention and authorized-field preservation.

## 2026-07-02 Findings: Normal-Behavior Stress Test

## Need
- A strict field-level guard can look good on unsafe cases but still be unusable if it blocks normal agent behavior.
- The user explicitly identified this as the key research pressure: under strict supervision and intervention, preserve normal action behavior.

## Research Finding
- Added a 4-case fully authorized normal-behavior stress suite.
- The suite covers normal power-operation workflows:
  - internal feeder inspection work order;
  - internal outage-notice review;
  - read-only topology simulation;
  - internal maintenance report distribution.
- Current readback:
  - total_cases=4
  - passed_cases=4
  - fully_authorized_case_count=4
  - authorized_field_count=16
  - preserved_authorized_field_count=16
  - false_block_field_count=0
  - false_intervention_field_rate=0.000
  - whole_action_intervention_rate=0.000
  - final_action_mutation_cases=0
  - mean_repair_overhead_fields=0.000

## Technical Finding
- Added:
  - `examples/data/power_ops_normal_behavior_stress_fixture.json`
  - `examples/power_ops_normal_behavior_stress_validation.yaml`
  - `formaltrust_platform/experiments/power_ops_normal_behavior_stress.py`
- Generated:
  - `docs/power_ops_normal_behavior_stress_results_2026-07-02.md/json`
  - `docs/power_ops_normal_behavior_stress_runtime_report_2026-07-02.md/json`
- Updated README, PAPER_PLAN, table evidence binding, numeric audit, paper readiness, claim ledger readiness, and paper draft derivative artifacts.

## Verification

- Focused Iteration 71 regression: 5 passed.
- `pytest tests/test_power_ops_action_invariance.py -q`: 69 passed.
- `pytest -q`: 269 passed.
- Table evidence binding: fully_supported_row_count=20, unsupported_row_count=0.
- Numeric claim audit: unsupported_numeric_claim_count=0.
- Residual numeric triage: needs_evidence=0.
- Paper claim readiness: PASS.
- Claim ledger readiness: PASS.

## Boundary
- This is still fixture-level evidence, not production telemetry.
- It strengthens the normal-behavior preservation claim under curated fully authorized traces.
- It does not yet measure wall-clock overhead, real operator workload, or large-scale distribution shift.

## Next
- Iteration 72 should generate trace-derived authority-confusion rows: keep the original legal row, mutate only the required role, and verify CapGuard blocks the role-confusion row while preserving the legal row.

## 2026-07-02 Findings: Trace-Derived Authority Confusion

## Need

- Hand-written attack rows are useful, but reviewers can object that the attack distribution is cherry-picked.
- The project needs a way to start from a valid agent trace and systematically create a role-confusion contrast without changing the obvious boundary fields.

## Research Finding

- Added a generator that reads the planner-skill-tool-memory trace fixture and creates 10 paired rows from legal authority consumptions.
- Each generated row keeps:
  - field unchanged;
  - operation unchanged;
  - attributed source unchanged;
  - data/effect/delegation/time scopes unchanged.
- Each generated row mutates only `need.required_role`.
- Current readback:
  - source_case_count=2
  - generated_row_count=10
  - boundary_preserved_row_count=10
  - mutated_required_role_only_count=10
  - CapGuard legal preservation rate=1.000
  - CapGuard confusion block rate=1.000
  - boundary-scope-only false allow rate=1.000

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_trace_authority_confusion.py`.
- Generated:
  - `examples/data/power_ops_trace_authority_confusion_rows.json`
  - `docs/power_ops_trace_authority_confusion_results_2026-07-02.md/json`
- Added TDD coverage proving the generator mutates only the semantic role and preserves the boundary fields/scopes.

## Boundary

- This is still generated from a curated 2-case planner-chain fixture.
- It does not yet prove large-scale trace coverage, production distribution realism, or runtime overhead bounds.
- It does show a clean contrast: boundary-only supervision cannot distinguish the mutated rows, while role-aware CapGuard can.

## Next

- Iteration 73 should quantify runtime overhead and audit-compression scalability across the current suite family.

## 2026-07-02 Findings: Runtime Overhead Audit

## Need

- The user asked whether strict supervision would hurt agent performance by making the agent too conservative or too expensive.
- The project already measures false intervention and field preservation, but it also needs an overhead-facing artifact.

## Research Finding

- Added a proxy-only runtime overhead audit across 6 current suites:
  - expanded action-invariance results;
  - metamorphic results;
  - skill-authority results;
  - planner-skill-tool-memory results;
  - normal-behavior stress results;
  - trace-derived authority-confusion paired rows.
- Current readback:
  - total field-check proxy units=108
  - action-suite proxy units=88
  - paired-authority proxy units=20
  - max field-check proxy units per case=6
  - weighted mean audit-compression ratio=0.587963
  - wall-clock latency available=False
  - reporting status=proxy_only_no_wall_clock

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_runtime_overhead_audit.py`.
- Generated `docs/power_ops_runtime_overhead_audit_2026-07-02.md/json`.
- Added TDD coverage requiring the audit to aggregate current action suites and paired authority-confusion rows.

## Boundary

- This is overhead proxy evidence, not measured wall-clock latency.
- The safe claim is: the current suite family requires 108 field-level checks and compresses audit context by a weighted mean 0.587963.
- The unsafe claim is: the method is fast in production. That still needs instrumented timing.

## Next

- Iteration 74 should expand the baseline/ablation grid, especially on trace-derived authority-confusion rows, to separate role-aware checking from boundary-only and provenance-only variants.

## 2026-07-02 Findings: Authority-Confusion Baseline Grid

## Need

- The trace-derived authority-confusion result shows CapGuard works, but the paper also needs contrastive baselines.
- The most important comparison is not only "safe vs unsafe"; it is "role-aware vs boundary-only vs attribution-only vs strict refusal".

## Research Finding

- On 10 trace-derived boundary-preserving role-confusion rows:
  - CapGuard preserves legal rows at 1.000 and blocks confused rows at 1.000.
  - Permission-only, boundary-scope-only, and field-attribution-only all falsely allow confused rows at 1.000.
  - Strict-block blocks confused rows but falsely blocks legal rows at 1.000.
  - CapGuard's role-confusion advantage over boundary-scope-only is 1.000.
- This is a sharper evidence point for the innovation claim:
  - boundary preservation alone is insufficient;
  - source attribution alone is insufficient;
  - whole-action refusal is overconservative;
  - the semantic role in `Need(s,f)` is doing real work.

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_authority_confusion_baseline_grid.py`.
- Generated `docs/power_ops_authority_confusion_baseline_grid_2026-07-02.md/json`.
- Added TDD coverage for CapGuard, boundary-scope-only, field-attribution-only, permission-only, and strict-block behaviors.

## Boundary

- This is an ablation over generated authority-confusion rows, not a full production benchmark.
- It supports the role-aware distinction, not broad claims that CapGuard is superior on all agent-safety tasks.

## Next

- Iteration 75 should add statistical robustness checks, starting with intervals around the key point estimates.

## 2026-07-02 Findings: Statistical Robustness

## Need

- Several current results are perfect point estimates, such as 16/16 normal-field preservation and 10/10 role-confusion blocking.
- Reporting only 1.000 can sound overconfident unless the finite fixture size is explicit.

## Research Finding

- Added Wilson 95% intervals for five core rates:
  - normal authorized-field preservation: 16/16, lower 0.8064, upper 1.0000;
  - CapGuard confusion block: 10/10, lower 0.7225, upper 1.0000;
  - CapGuard false allow: 0/10, lower 0.0000, upper 0.2775;
  - boundary-scope-only false allow: 10/10, lower 0.7225, upper 1.0000;
  - strict-block false block: 10/10, lower 0.7225, upper 1.0000.
- The statistical language is deliberately bounded: these intervals describe finite fixture evidence, not production population guarantees.

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_statistical_robustness.py`.
- Generated `docs/power_ops_statistical_robustness_2026-07-02.md/json`.
- Reused the same Wilson formula already used by the EAIR robustness sweep code.

## Boundary

- This is not a multi-seed or live deployment study.
- It is a confidence-interval wrapper around current fixture counts.
- Production generalization still requires larger traces or live telemetry.

## Next

- Iteration 76 should generate paper-ready figures and tables with every plotted value bound to source JSON paths.

## 2026-07-02 Findings: Paper Figure/Table Package

## Need

- The evidence chain had strong JSON/Markdown reports, but paper/report writing also needs figures and tables.
- The figures must be reproducible and bound to source artifacts, not manually copied point estimates.

## Research Finding

- Added an evidence-bound figure/table package:
  - 2 SVG figures:
    - authority-confusion baseline grid;
    - Wilson interval ladder;
  - 2 LaTeX tables in one generated `.tex` file:
    - authority-confusion baseline table;
    - statistical robustness interval table.
- Every figure/table record includes source JSON paths.

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_paper_figure_table_package.py`.
- Generated:
  - `docs/power_ops_paper_figure_table_package_2026-07-02.md/json`
  - `figures/power_ops_authority_confusion_baseline_grid.svg`
  - `figures/power_ops_statistical_interval_ladder.svg`
  - `figures/power_ops_paper_tables.tex`
- Fixed a path normalization issue so source paths use stable `/` separators on Windows.

## Boundary

- These are data-driven figures and tables, not an architecture diagram.
- The figures do not add new empirical claims; they visualize the existing authority-confusion baseline grid and statistical robustness summaries.

## Next

- Iteration 77 should refresh related-work and novelty boundaries using the now-stronger evidence package.

## 2026-07-02 Findings: External 50-Case Full-Agent Authority Stress Suite

## Need

- The user clarified that the 50 new tests should not be fragmented field snippets.
- The suite therefore needed complete agent-task cases with source background, task goal, trace events, candidate action, field consumptions, and oracles.

## Research Finding

- Added 50 externally seeded power-operations full-agent cases from NERC Lessons Learned metadata.
- Each case treats a public lesson as valid support for an internal review packet, but not as live operational authority.
- Runtime readback:
  - total_cases=50
  - passed_cases=50
  - external_lesson_count=50
  - authorized_fields=350
  - unauthorized_fields=50
  - authorized_final_field_preservation_rate=1.000
  - unauthorized_final_field_removal_rate=1.000
  - whole_action_block_rate=0.000
  - blocked_field_family_count=7

## Technical Finding

- Added `formaltrust_platform/experiments/power_ops_external_case_50.py`.
- Added source seed `examples/data/power_ops_external_50_source_seed.json`.
- Generated full-case fixture `examples/data/power_ops_external_50_fixture.json`.
- Added runnable config `examples/power_ops_external_50_validation.yaml`.
- Generated results:
  - `docs/power_ops_external_case_50_results_2026-07-02.md`
  - `docs/power_ops_external_case_50_results_2026-07-02.json`
- Generated HTML review report:
  - `docs/power_ops_external_case_50_results_2026-07-02.html`
  - Each case block shows the NERC metadata anchor, agent task design, authorized fields preserved, high-risk field removed, and field-level authority chain.
- Added TDD coverage requiring full case granularity and end-to-end runtime execution.
- Added TDD coverage requiring the HTML report to expose all 50 case designs, not only aggregate pass rates.

## Boundary

- This is externally seeded synthetic testing, not production telemetry.
- NERC metadata anchors the operational themes; the agent traces and high-risk authority misuse candidates are generated test cases.
- The safe claim is action-invariance preservation under these 50 full-agent cases, not broad production safety.

## Next

- Refresh related work and novelty boundaries before upgrading paper claims around the expanded 50-case suite.
