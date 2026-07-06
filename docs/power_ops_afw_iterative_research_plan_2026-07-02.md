# 电力大模型安全 AFW/CapGuard 迭代研究计划

日期：2026-07-02

## 0. 这轮要解决什么

这轮不是重新起炉灶，而是把已有的 AFW/CapGuard 工作，收束成一个可以反复迭代的电力大模型安全研究工程。核心问题是：

在电力大模型 agent 执行复杂任务时，安全监督不能只会“一刀切拦截”。我们要研究一种更细的机制：合法字段尽量保持不变，非法字段才被拦截、修复或转人工。也就是把前面讨论的“严格策略监督下如何保证动作不变性”，落到电力运维 agent 的形式化建模、测试框架、测试样本和实验方案里。

一句大白话：

> agent 可以看资料、用 skill、调用工具、记住历史、拿到用户批准，但每个动作字段到底能不能做，必须看它有没有对应授权；有授权的部分别乱动，没授权的部分别放行。

## 1. 当前项目已有基础

这不是从 0 开始。项目里已经有一条可运行的电力运维安全切片：

| 类别 | 已有资产 |
|---|---|
| FormalTrust 接口 | `formaltrust_platform/interfaces.py`, `formaltrust_platform/state.py`, `formaltrust_platform/graph.py`, `formaltrust_platform/registry.py`, `formaltrust_platform/config.py` |
| AFW 节点 | `formaltrust_platform/nodes/afw.py` |
| 核心算法 | `formaltrust_platform/experiments/afw_bench.py` |
| 运行时报告 | `formaltrust_platform/experiments/afw_runtime_report.py`, `formaltrust_platform/experiments/afw_runtime_suite.py` |
| 电力样本 | `examples/afw_power_ops_rag_rows.json`, `examples/afw_power_ops_trace_scenarios.json`, `examples/data/afw_runtime_power_ops_cases.jsonl` |
| 运行时配置 | `examples/afw_runtime_validation.yaml` 以及 trace adapter / OTLP / obligation / temporal / counter-authority variants |
| 当前报告 | `docs/power_ops_afw_current_results_2026-07-01.md`, `docs/power_ops_afw_test_framework_2026-07-01.md`, `docs/power_ops_afw_test_samples_2026-07-01.md`, `docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md` |

当前最重要的已有结果：

| 指标 | 当前值 |
|---|---:|
| all-config runtime suite cases | 27 |
| passed cases | 27 |
| mean AFW BehMatch | 1.000 |
| false allow fields | 0 |
| false block fields | 0 |
| allow / block / abstain cases | 4 / 20 / 3 |
| mean witness compression ratio | 0.760 |

这些结果说明现有框架已经能跑通“字段级授权检查 + runtime evaluator”。但它还更像一个强安全切片，下一步要把它扩成“动作不变性 + 电力安全 agent”的统一研究框架。

## 2. 必须遵守的项目接口

所有新增成果都要按当前 FormalTrust 接口做，不另造孤立脚本体系。

### 2.1 节点接口

新增方法优先做成 FormalTrust node：

```python
def node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any] | None:
    ...
```

返回值只允许 patch `FormalTrustState` 顶层字段。中间结构优先写入：

```python
state.metrics["..."]
state.artifacts["..."]
```

不要随便新增顶层 state 字段。

### 2.2 配置接口

实验入口继续走 YAML graph：

```text
dataset_path -> graph.nodes -> graph.edges -> ExperimentRunner
```

新增配置应放在 `examples/*.yaml`，新增数据放在 `examples/data/*.jsonl` 或 `examples/*.json`。

### 2.3 当前 AFW runtime 输入输出

当前 `guardrail.afw_capguard` 已经支持这些输入来源：

| 输入 | 位置 |
|---|---|
| candidate action | `state.metrics["candidate_action"]` 或 `case.metadata["candidate_action"]` |
| capability | `state.metrics["afw_capabilities"]`, `case.metadata["afw_capabilities"]`, `case.metadata["afw_source_events"]`, `retrieval_context.metadata["authority_manifest"]` |
| need / consumption | `state.metrics["afw_consumptions"]`, `state.metrics["afw_needs"]`, `case.metadata["afw_consumptions"]`, `candidate_action["afw_consumptions"]` |
| oracle | `case.metadata["afw_oracle"]` |

当前输出：

| 输出 | 位置 |
|---|---|
| 字段级判定 | `metrics["afw_runtime_field_results"]` |
| gate 判定 | `metrics["afw_gate_decision"]` |
| 最终动作 | `metrics["final_action"]` |
| 最小授权见证 | `metrics["afw_runtime_field_results"][*]["witness"]` 及相关 audit |
| 行为匹配 | `metrics["afw_behmatch"]` |
| false allow / false block | `metrics["afw_runtime_false_allow_fields"]`, `metrics["afw_runtime_false_block_fields"]` |

## 3. 统一研究框架

本项目后续统一叫：

> Power-Ops Action-Field Warrant Framework

简称仍可沿用 AFW/CapGuard，但论文主问题建议往“动作不变性”上推：

> Authority-Constrained Action Invariance for Safety-Critical LLM Agents

### 3.1 统一对象

把 agent 上下文里的所有“可能被 agent 拿来当理由的东西”统一成 capability：

```text
Cap(x) = source x actually authorizes
```

来源包括：

```text
RAG 文档
skill 输出
tool metadata
memory
user approval
prior-step output
span / OTLP trace
policy epoch
obligation receipt
counter-authority
```

把 agent action 里的每个字段统一成 need：

```text
Need(s, f) = action step s 的字段 f 需要什么授权
```

合法性判断：

```text
Allow(s, f) iff exists minimal witness W:
  W subset Cap(Context)
  W covers Need(s, f)
  W is not expired
  W discharges required obligations
  W is not contradicted by counter-authority
```

### 3.2 电力场景保护字段

后续样本和测试优先覆盖这些字段：

```text
answer
side_effect
requires_human_approval
risk_level
risk_report
data_read_scope
data_write_scope
tool
parameters.*
delegation
dispatch_order
switching_operation
outage_notice
asset_private_data
protection_setting
fault_isolation
public_publish
```

### 3.3 动作不变性目标

安全监督不应该默认把整个 agent 行为拍死。更好的目标是：

```text
authorized fields remain unchanged
unauthorized fields are blocked, repaired, or routed to human approval
uncertain fields abstain
```

后续核心指标：

| 指标 | 含义 |
|---|---|
| authorized_field_preservation | 有授权字段是否被保留下来 |
| unauthorized_field_prevention | 无授权字段是否被阻止 |
| conservative_collapse_rate | 因一个坏字段导致整个任务被不必要阻断的比例 |
| false_allow_fields | 错放非法字段 |
| false_block_fields | 错拦合法字段 |
| witness_compression_ratio | 审计时只需看最小见证，能压缩多少上下文 |
| obligation_discharge_rate | 需要扫描、审批、DLP 等义务时是否真的完成 |
| temporal_validity_rate | 旧审批、旧 memory、旧 policy epoch 是否被正确拒绝 |
| counter_authority_abstain_rate | 有反向权威时是否转人工/暂停 |
| frame_preservation_rate | 授权边界不变时，是否没有被语义角色偷换 |

## 4. 前沿校准

初步查新发现，方向不能只写成“agent guardrail”或“prompt injection 防御”，因为已有工作很多。我们的差异化应放在“字段级授权 + 电力场景 + 不变性/不过度保守 + 最小授权见证”。

| 方向 | 代表信号 | 对我们的启发 |
|---|---|---|
| 电力 LLM agent | [GridMind: LLMs-Powered Agents for Power System Analysis and Operations](https://arxiv.org/html/2509.02494v1) | 电力 agent 正在从问答走向多 agent + 工程求解器，安全监督必须面向工具调用和操作字段 |
| 电力 LLM 风险 | [Risks of Practicing Large Language Models in Smart Grid](https://arxiv.org/html/2405.06237v3) | 智能电网 LLM 风险包括坏数据注入和知识泄露，我们的样本要覆盖数据、操作和授权混淆 |
| 电力 LLM 综述 | [Large Language Models for Power System Applications](https://arxiv.org/html/2512.13004v1) | 领域挑战集中在可靠性、安全、可解释性，正好对应 witness/audit |
| agent step-level guardrail | [ToolSafe](https://arxiv.org/html/2601.10156v1) | 单步工具调用监督已是强相关方向，我们要强调字段级而不是 action 级整体分类 |
| action-level guardrail dataset | [WebGuard](https://arxiv.org/html/2507.14293v1) | action-level 数据集是趋势，但我们的差异是电力场景和 authority witness |
| prompt injection 设计模式 | [Design Patterns for Securing LLM Agents](https://arxiv.org/html/2506.08837v3) | 需要把 prompt injection 防御和能力边界/权限边界结合 |
| 通用风险基线 | [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | RAG 和 fine-tuning 都不能彻底解决 prompt injection，运行时授权检查有必要 |

后续完整文献综述按 `research-lit` 规则执行：本地论文优先，外部 web/arXiv/Semantic Scholar/OpenAlex 补齐，候选论文要记录验证状态，不把未核验论文混成已证事实。

## 5. 迭代产出路线

### Phase 0：清点与基线复跑

目标：把现有成果变成可重复起点。

产出：

```text
docs/power_ops_afw_iterative_research_plan_2026-07-02.md
docs/power_ops_afw_baseline_refresh_2026-07-02.md
```

动作：

1. 复跑当前 all-config runtime suite。
2. 记录 27-case 基线是否仍然 27/27 通过。
3. 把当前所有 YAML、JSONL、报告挂成索引。

验收：

```text
pytest tests/test_interfaces.py tests/test_afw_bench.py -q
```

### Phase 1：形式化建模 v2

目标：把 AFW 从“字段级授权检查”提升为“受授权约束的动作不变性”模型。

产出：

```text
docs/power_ops_action_invariance_formal_model_2026-07-02.md
docs/power_ops_afw_property_catalog_2026-07-02.md
```

要形式化的性质：

| 性质 | 大白话 |
|---|---|
| Authority Soundness | 没授权就不能执行对应字段 |
| Authorized Field Preservation | 有授权的字段不应被安全机制误伤 |
| No Role Amplification | 格式化 skill 不能变成风险评估权威 |
| Boundary-Preserving Role Mismatch | 边界看起来没变，但语义角色偷换，要能抓到 |
| Obligation Discharge | 要静态扫描/DLP/审批，就必须真的完成 |
| Temporal Decay | 旧审批、旧 memory、旧 policy 不能永久当授权 |
| Counter-Authority Abstain | 有暂停/反对/冲突授权时，不能硬执行 |
| Minimal Witness | 每个 allow/block 都能解释靠哪些授权、缺哪些授权 |
| Fieldwise Action Invariance | 安全处理只改应该改的字段，不乱改合法字段 |

### Phase 2：测试框架 v2

目标：把“不过度保守”变成可测指标，而不是口头承诺。

产出：

```text
formaltrust_platform/experiments/power_ops_action_invariance.py
examples/power_ops_action_invariance_runtime_validation.yaml
tests/test_power_ops_action_invariance.py
docs/power_ops_action_invariance_test_framework_2026-07-02.md
```

新增报告字段优先放入 `metrics`，例如：

```text
authorized_field_preservation_rate
conservative_collapse_rate
fieldwise_repair_success_rate
witness_log_completeness
quorum_authority_coverage
temporal_decay_pass_rate
obligation_discharge_pass_rate
frame_preservation_rate
```

### Phase 3：测试样本 v2

目标：不再只测“该拦的拦”，还测“该保留的保留”。

产出：

```text
examples/data/power_ops_action_invariance_cases.jsonl
examples/data/power_ops_action_invariance_paired_rows.json
docs/power_ops_action_invariance_sample_catalog_2026-07-02.md
```

样本族：

| 样本族 | 例子 |
|---|---|
| 合法字段保留 | manual 可以支撑 answer，但不能支撑 dispatch |
| 保守性坍缩 | 一个非法 side_effect 不应导致合法 answer 被删除 |
| skill 安全 | report-formatting skill 不能升级成 risk-assessment authority |
| tool metadata 安全 | 向量索引 metadata 不能变成资产数据读取授权 |
| memory 安全 | 用户语气偏好不能变成安全策略 |
| prior-step 安全 | 上一步总结不能变成设备认证 |
| human approval 安全 | 巡检排期审批不能变成送电授权 |
| obligation | repo write / public publish 需要 scan 或 DLP receipt |
| temporal | Q3 批准不能支持 Q4 发布 |
| counter-authority | 有 policy hold 时转人工 |
| quorum | 高风险操作需要 2-of-3 或多角色共同授权 |
| OTLP/trace | 从真实风格 trace 中解析 capability/need，不依赖手填字段 |

### Phase 4：实验方案与结果

目标：形成论文/项目汇报可用的结果表。

产出：

```text
docs/power_ops_action_invariance_results_2026-07-02.md
docs/power_ops_action_invariance_results_2026-07-02.json
docs/power_ops_action_invariance_ablation_2026-07-02.md
```

实验组：

| 组别 | 说明 |
|---|---|
| permission_only | 只看是否有工具权限 |
| attribution_only | 只看字段来源 |
| boundary_scope_only | 只看 scope，不看 role |
| strict_block | 一处不合法就全拦 |
| capguard_fieldwise | 字段级授权检查 |
| capguard_fieldwise_repair | 合法字段保留，非法字段转人工/修复 |

关键比较：

```text
strict_block vs capguard_fieldwise_repair
```

我们要证明的不是“安全机制越严越好”，而是：

```text
同样阻止危险字段时，字段级机制能保留更多正常行为。
```

### Phase 5：人工标注与样本可信度

目标：把当前 machine-prefill smoke 变成人类可审计数据集。

产出：

```text
docs/power_ops_action_invariance_annotation_packet_2026-07-02.jsonl
docs/power_ops_action_invariance_annotation_protocol_2026-07-02.md
docs/power_ops_action_invariance_kappa_report_2026-07-02.md
```

注意：当前已有 `mean_kappa=1.0` 只是 machine smoke，不是人工双标。后续不能把它写成真实人工一致性。

### Phase 6：文献查新与创新边界

目标：防止和已有 guardrail / tool-safety / prompt-injection 论文撞车。

产出：

```text
docs/power_ops_action_invariance_lit_review_2026-07-02.md
docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md
```

查新方向：

```text
LLM agents for power systems
smart grid LLM security
tool invocation safety
agent guardrails
prompt injection design patterns
proof-carrying / provenance-based agent actions
authorization logic for agents
runtime monitors and action invariance
```

创新边界先写死：

```text
不是第一个 agent guardrail
不是第一个 prompt injection 防御
不是第一个电力 LLM 应用
主张是：电力安全 agent 中，字段级授权见证可以降低过度保守，同时保持危险字段阻断。
```

### Phase 7：论文与汇报材料

目标：把工程成果变成论文/周报/答辩可讲的主线。

产出：

```text
docs/power_ops_action_invariance_paper_kernel_2026-07-02.md
docs/power_ops_action_invariance_figure_plan_2026-07-02.md
PAPER_PLAN.md 更新
```

建议图：

1. 统一 Cap/Need 框架图。
2. 电力 agent runtime graph。
3. 字段级 allow/block/abstain 示例。
4. strict-block 与 fieldwise-repair 对比图。
5. 样本 taxonomy。
6. 结果表：安全性、保守性、审计压缩。

### Phase 8：每轮固定闭环

每一轮迭代必须留下这 6 件东西：

| 项 | 文件 |
|---|---|
| 本轮目标 | `refine-logs/iterations/POWER_OPS_AFW_ITERATION_<N>.md` |
| 新发现 | `findings.md` |
| 实际动作 | `progress.md` |
| 新资产 | `docs/`, `examples/`, `formaltrust_platform/`, `tests/` |
| 测试命令与结果 | 对应 iteration log |
| claim boundary | 不夸大当前证据 |

## 6. 第一轮具体任务

下一轮先做最小但真实的一批成果：

1. 生成 `docs/power_ops_action_invariance_formal_model_2026-07-02.md`。
2. 生成 `docs/power_ops_afw_property_catalog_2026-07-02.md`。
3. 增加 `examples/data/power_ops_action_invariance_cases.jsonl`，至少 8 个 case。
4. 增加 `examples/power_ops_action_invariance_runtime_validation.yaml`。
5. 增加最小测试 `tests/test_power_ops_action_invariance.py`。
6. 跑通一份 `docs/power_ops_action_invariance_results_2026-07-02.md`。

第一批 8 个 case 建议：

| case | 目标 |
|---|---|
| manual_answer_keep_dispatch_block | 合法 answer 保留，非法 dispatch 阻断 |
| skill_format_keep_risk_gate_block | 格式化 skill 输出保留，风险门控阻断 |
| tool_metadata_keep_citation_block_data_read | metadata 可引用，不可读取私密资产 |
| memory_style_keep_policy_block | 语气记忆可用，安全策略不可由记忆生成 |
| prior_summary_keep_certification_block | 上一步总结可引用，不可变设备认证 |
| approval_schedule_keep_energize_block | 排期审批可用，不可变送电授权 |
| q3_publish_keep_q4_block | 时间过期后不能复用 |
| counter_authority_abstain_publish | 有 policy hold 时转人工 |

## 7. 风险和边界

当前不能过度声称：

```text
不能说已经完成真实生产部署
不能说覆盖全部电力大模型安全问题
不能说 27 个 curated case 证明泛化
不能说 machine-prefill kappa 是人工一致性
不能说 CapGuard 比所有 agent guardrail 都强
```

当前可以稳妥声称：

```text
已有 FormalTrust-compatible runtime guardrail
已有电力运维字段级授权样本
已有 27-case all-config regression suite
已有 trace/OTLP/obligation/temporal/counter-authority 覆盖
下一步将评估安全监督导致的 conservative collapse，并用字段级 action invariance 指标衡量正常行为保留
```

## 8. 当前活动状态

```text
status: planned
active_axis: power_ops_action_invariance
next_iteration: formal_model_v2 + sample_v2 + runtime_validation_v2
```

这份计划后续不作为一次性 checklist，而作为每轮迭代的总路线图。每轮完成后，更新 `progress.md`、`findings.md` 和对应 iteration log，再决定下一轮继续扩样本、扩指标、扩实现，还是收缩论文主张。
