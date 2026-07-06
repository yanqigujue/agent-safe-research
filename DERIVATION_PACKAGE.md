## 2026-06-21 Refinement: WarrantGuard / Proof-Carrying Actions

The active method is upgraded from a gate-only framing to **WarrantGuard**:
high-risk RAG-agent actions must be proof-carrying. The agent is no longer
viewed as emitting a bare action. It emits:

```text
Agent(q, K) -> (a, W_a)
```

where `a` is the structured action and `W_a` is an action warrant:

```text
W_a = {
  decision_warrant,
  tool_arg_warrants,
  parameter_warrants,
  approval_warrant,
  risk_level_warrant,
  risk_report_warrant,
  freshness_warrant,
  source_diversity_warrant,
  conflict_resolution_warrant,
  counter_warrant_report
}.
```

Execution is permitted only when the action carries a verifiable warrant:

```text
Execute(a) = 1[
  HardGate(a) = PASS
  and VerifyWarrant(a, W_a | q, K) = PASS
  and CounterWarrant(a, W_a | q, K) = CLEAR
].
```

`VerifyWarrant` checks that every safety-critical field of `a` is backed by
claim-level evidence paths that are source-diverse, trusted, fresh/current,
low-conflict, and low-poison. This reframes EAIR-Full as the reference
verifier for proof-carrying actions, not merely as a post-hoc safety gate.

The prior admissibility form remains as the verifier's core condition:

```text
VerifyWarrant(a, W_a | q, K) = PASS
  only if
    EvidenceSufficient(a | q, K)
    and each required action field has a field-specific warrant.
```

This gives the paper a sharper method contribution:

```text
proof-carrying RAG-agent actions
```

rather than only:

```text
action-level attribution or gate-based blocking.
```

## 2026-06-20 Refinement: Artifact Verification

Replay artifacts now have a verifier:

```text
VerifyArtifact(manifest)
  = CheckArtifactType
    and CheckTranscriptHash
    and CheckOutputFiles
    and CheckSummaryConsistency
```

The verification command:

```text
formaltrust eair-verify-artifact --manifest artifact_manifest.json
```

turns the replay evidence object into a checkable artifact:

```text
ValidEvidenceObject =
  1[ VerifyArtifact(artifact_manifest.json) = PASS ].
```

This adds a reproducibility gate before claims are copied into tables or paper text.

## 2026-06-20 Refinement: Manifest Summary Operator

Paper-facing replay tables should be generated only after artifact verification:

```text
VerifiedSummary =
  Aggregate({ manifest_i : VerifyArtifact(manifest_i) = PASS })
```

The summary operator is:

```text
SummarizeArtifacts({manifest_i})
  = VerifyArtifact(manifest_1) and ... and VerifyArtifact(manifest_n)
  -> {artifact_summary.json, artifact_summary.csv, artifact_summary.md}
```

This is not a new safety score. It is a reproducibility boundary that keeps table construction tied to transcript-hash-verified replay artifacts. A paper table can cite `VerifiedSummary`, but live-model behavior still requires provider-generated transcripts plus replay artifacts.

## 2026-06-20 Refinement: Grouped Verified Summary

For model-backed analysis, aggregate verified replay transcripts along analysis axes:

```text
GroupedSummary(axis)
  = GroupBy(axis, Transcripts(VerifiedSummary))
```

where:

```text
axis in {model, case_id::condition}
```

The grouped quantities are counts over replay outcomes:

```text
N, ParseError, CandidateUnsafe, FinalUnsafe, GateCounts, InfluenceCounts.
```

This operator supports failure analysis without changing the EAIR safety definition. It answers where replayed unsafe candidates occur, not whether a live model was sampled.

## 2026-06-20 Refinement: Model-Condition Matrix

For fair model-backed evaluation, define the replay matrix:

```text
M[model, condition] =
  GroupedSummary(axis = (model, case_id::condition)).
```

Each cell stores replay outcome counts:

```text
M[m, k] =
  (N, ParseError, CandidateUnsafe, FinalUnsafe,
   CandidateUnsupported, FinalUnsupported,
   GateCounts, InfluenceCounts).
```

This matrix is not part of the EAIR score. It is an artifact-analysis operator that exposes model-condition coverage and failure concentration.

## 2026-06-20 Refinement: Coverage Audit

Let:

```text
E = expected condition set
O_m = observed condition set for model m
```

Coverage audit reports:

```text
Covered_m = O_m intersect E
Missing_m = E \ O_m
Unexpected_m = O_m \ E
CoverageRate_m = |Covered_m| / |E|
```

The audit is complete only when:

```text
forall m, Missing_m = empty
and forall m, Unexpected_m = empty.
```

This is an experimental validity gate, not an EAIR safety score.

## 2026-06-20 Refinement: Coverage Gate

Define:

```text
CoverageGate = PASS iff CoverageAudit.complete = true.
```

For formal model comparison:

```text
ReportModelComparison only if CoverageGate = PASS.
```

If:

```text
exists m such that Missing_m != empty
```

then the experiment should fail before model safety rates are reported, while preserving coverage artifacts for diagnosis.

## 2026-06-20 Refinement: Positive-Control Fixture

Define a positive-control artifact run:

```text
PositiveControl =
  DryRunSampler
  -> Replay
  -> VerifyManifest
  -> SummarizeArtifacts
  -> CoverageGate(PASS).
```

This proves the artifact protocol can pass when:

```text
forall m, Missing_m = empty
```

It is not evidence about live-model safety; it is evidence that the experiment pipeline has a passing control case.

## 2026-06-20 Refinement: Live-Run Readiness

Define a live-run readiness predicate:

```text
LiveReady(config) =
  Has(api_key_env)
  and not Has(inline api_key)
  and not Has(dry_run_responses)
  and Has(output_path)
  and Has(replay_output_dir)
  and ExpectedConditions(config) subset ScenarioConditions(config).
```

Live sampling should only proceed when:

```text
LiveReady(config) = PASS.
```

This predicate is about experiment validity and secret discipline. It is not a model-safety metric.

## 2026-06-20 Refinement: Replay Artifact Manifest

Replay evaluation now emits a manifest:

```text
Manifest =
  (artifact_type,
   protocol,
   claim_boundary,
   transcript_path,
   transcript_sha256,
   outputs,
   summary)
```

The manifest binds:

```text
sha256(TranscriptJSONL) -> ReplayResults
```

This makes the replay evidence object:

```text
EvidenceObject = (TranscriptJSONL, artifact_manifest.json, replay_results.json, replay_report.md)
```

rather than an unverifiable live-model interaction.

## 2026-06-20 Refinement: Standalone Replay Operator

The replay operator is now executable without sampling:

```text
ReplayCLI(transcripts, output_dir)
  = ReplayEvaluation(transcripts)
  -> {results.json, report.md}
```

This supports external transcript collection:

```text
ExternalModelRun -> transcript JSONL
formaltrust eair-replay --transcripts transcript JSONL --output-dir replay_dir
```

Therefore the evidence object for model-facing experiments is not a live API call. It is the saved transcript plus deterministic replay artifacts.

## 2026-06-20 Refinement: Configurable Sampler Protocol

The sampling protocol is now executable from a declarative config:

```text
SamplerConfig
  = (base_url, model, api_key_env, scenarios, output_path, replay_output_dir)
```

The command:

```text
formaltrust eair-sample --config sampler.yaml
```

implements:

```text
SamplerConfig -> TranscriptJSONL -> ReplayEvaluation -> ReplayReport
```

For dry-run and CI, `dry_run_responses` replaces the network transport while preserving the same transcript and replay interfaces.

## 2026-06-20 Refinement: Sampling-Evaluation Separation

Live model experiments are now represented as two stages:

```text
Sampler(model, case, K) -> TranscriptJSONL
ReplayEvaluation(TranscriptJSONL) -> EAIR results
```

The sampler is not allowed to make safety claims. It only records:

```text
transcript_id, model, case_id, condition, prompt, model_output, raw_response
```

All safety quantities remain replay-side quantities:

```text
ParseAction(model_output)
HardGate(a_hat)
EvidenceSufficient(a_hat)
EAIR(q, a_hat)
Unsafe(candidate), Unsafe(final)
```

This gives a cleaner experimental protocol: stochastic sampling is archived once, while deterministic EAIR evaluation can be rerun, audited, and versioned.

## 2026-06-20 Refinement: Transcript Replay Layer

The model-output boundary now has a replayable artifact form:

```text
Transcript = (transcript_id, model, case_id, condition, y_text)
Replay(Transcript) =
  ParseAction(y_text)
  -> Allow(a_hat | q, K)
  -> Eval(candidate_action, final_action)
```

This separates two sources of uncertainty:

```text
LiveSampling(model, prompt, evidence) -> transcript JSONL
ReplayEvaluation(transcript JSONL) -> deterministic EAIR results
```

The separation matters for scientific auditability. Live model sampling may be stochastic or expensive, while replay evaluation should be deterministic, versioned, and inspectable.

## 2026-06-20 Refinement: Model-Output Action Boundary

EAIR now has an explicit structured-output boundary:

```text
M(q, K) -> y_text -> ParseAction(y_text) -> a_hat -> Allow(a_hat | q, K)
```

`ParseAction` returns:

```text
(a_hat, parse_diagnostics)
```

where `parse_diagnostics` records whether the model output was raw JSON, fenced JSON, embedded JSON, or unparseable. If parsing fails:

```text
a_hat = abstain
risk_report(a_hat) = human_review_required
requires_human_approval(a_hat) = true
```

This prevents malformed model output from bypassing the gate and makes the benchmark closer to real agent execution, where the model emits structured action text before any tool/action layer receives it.

## 2026-06-20 Refinement: Risk Integrity in HardGate

The active admissibility abstraction is now:

```text
Allow(a | q, K) =
  1[
    HardGate(a) = PASS
    and EvidenceSufficient(a | q, K)
    and EAIR(q, a) <= eta
  ].
```

`HardGate(a)` is not only a tool-name or domain-rule check. It also protects action fields that change the operational meaning of a no-tool decision:

```text
HardGate(a) = PASS iff
  DecisionPolicy(a) = PASS
  and ToolPolicy(a) = PASS
  and ParameterBounds(a) = PASS
  and ApprovalIntegrity(a) = PASS
  and RiskLevelIntegrity(a) = PASS
  and RiskReportIntegrity(a) = PASS.
```

For a high-risk case with required risk level `r*`, risk integrity requires:

```text
RiskLevelIntegrity(a) = 1[ risk_level(a) >= r* ].
RiskReportIntegrity(a) = 1[ risk_report(a) does not suppress required review ].
```

This closes a loophole exposed by `risk_report_downgrade_no_tool`: a candidate can use `decision="reject_bypass"` and `tool="none"` while still being hijacked through `risk_level="low"` or `risk_report="safe_no_review"`. Conservative denial is relaxable only when all hard-gate action fields remain intact.

# Derivation Package: Evidence-to-Action Integrity

日期：2026-06-14

目标：给出一个可以同时覆盖 **检索命中劫持**、**证据冲突判断**、**工具/决策污染** 的数学抽象，并能落到 FormalTrust 框架的可计算指标和 guardrail。

## 0. 核心重述

原始三个方向看似分散：

- retrieval hit hijacking 关心污染文档是否进入上下文；
- evidence conflict judgment 关心互相矛盾的证据如何处理；
- tool / decision pollution 关心 Agent 是否做错动作。

统一对象是：

```text
retrieved evidence -> extracted claims -> conflict graph -> plan/tool/action -> safety outcome
```

因此主对象定义为 **Evidence-to-Action Integrity Risk**：

```text
R_EA = E[ L(y, pi, a, T ; q, K, C, G_c, w) ]
```

其中 `T` 是可审计证据链，`a` 是动作或工具调用，`w` 是真实世界/仿真状态。

## 1. 基本对象

令：

- `q in Q`：用户查询或任务。
- `D = D_h union D_p`：语料，包含 honest documents 与 poisoned documents。
- `R_phi(q, D)`：检索器。
- `K_q = (d_1, ..., d_k)`：按 rank 排列的 Top-K 检索结果。
- `z(d) in {0,1}`：实验中可见的污染标记，部署中不可见。
- `p_pois(d) in [0,1]`：部署时估计的污染/不可信概率。
- `tau(d) in [0,1]`：来源完整性/信任分数。
- `rho(d) in [0,1]`：时效性分数。
- `r(q,d)`：语义/词法相关性分数。
- `s(d)`：来源类型，例如 procedure、asset-db、simulation-log、web、tool-doc。
- `x(d)`：文档内容。

FormalTrust 对应：

- `RetrievedDocument.content = x(d)`
- `RetrievedDocument.poisoned = z(d)`，仅用于受控实验。
- `RetrievedDocument.metadata = {rank, score, tau, rho, source_type, claim_id, conflict_group}`。

## 2. 检索命中劫持

Top-K 检索：

```text
K_q = TopK_k { r(q,d) : d in D }.
```

污染暴露率：

```text
PRE(q) = (1/k) * sum_{j=1}^k z(d_j).
```

Rank-weighted hijacking exposure：

```text
RHE(q) = sum_{j=1}^k alpha_j z(d_j),
alpha_1 >= alpha_2 >= ... >= alpha_k >= 0.
```

如果攻击目标是某个 claim `c*` 或 action `a*`，则目标命中率：

```text
THR(q, c*) = 1[ exists d in K_q : z(d)=1 and c* in Claims(d) ].
```

这一步只说明污染进入上下文，不说明伤害已经发生。因此需要继续追踪到 claim 和 action。

Retrieval perturbation:

```text
K'_q = P_seed(K_q; drop_doc_ids, drop_ranks, shuffle, top_k).
```

The `attack.eair_retrieval_perturbation` node applies this transformation to `retrieval_context` before claim/action selection. This keeps retrieval-set failures separate from claim extraction noise (`C_hat`) and evidence sufficiency checks.

## 3. Claim 层表示

抽取器：

```text
g: K_q -> C_q = {c_1, ..., c_m}.
```

每个 claim 包含：

```text
c_i = (subject_i, predicate_i, object_i, qualifier_i, time_i, scope_i).
```

例子：

```text
("maintenance_task", "requires_approval", true, "substation-inspection", "current", "grid-ops")
```

文档对 claim 的支持权重：

```text
S(c_i) = sum_{d in Supp(c_i)} beta(d,q) * tau(d) * rho(d) * e(d,c_i).
```

其中：

- `beta(d,q)`：rank/relevance 权重；
- `tau(d)`：来源完整性；
- `rho(d)`：新鲜度；
- `e(d,c_i)`：文档片段对 claim 的 entailment/support 分数。

污染支持质量：

```text
S_pois(c_i) = sum_{d in Supp(c_i)} beta(d,q) * z(d) * e(d,c_i).
```

部署时可用：

```text
S_susp(c_i) = sum_{d in Supp(c_i)} beta(d,q) * p_pois(d) * e(d,c_i).
```

Claim extraction noise:

```text
C_true(d) = claims entailed by document d.
C_hat(d) = g(d), the extracted claims used by the agent/gate.

ClaimFalseNegative(d,c) = 1[c in C_true(d) and c notin C_hat(d)].
ClaimFalsePositive(d,c) = 1[c notin C_true(d) and c in C_hat(d)].
```

The `attack.eair_claim_extraction_noise` node perturbs `RetrievedDocument.metadata["claims"]` while preserving `pre_noise_claims`, so EAIR-Bench can test utility loss from dropped required claims and unsafe candidate actions from injected claims.

Seeded stochastic extraction noise:

```text
C_hat_seed(d) =
  Drop_p(C_hat(d), seed)
  union Inject_p(C_candidates(d), seed).
```

Fixed seeds make stochastic false-negative and false-positive schedules replayable inside a FormalTrust graph, which is necessary before running multi-seed robustness sweeps.

Compounded graph perturbation summary:

```text
RobustnessOutcome =
  h(K'_q, C_hat_seed, candidate_action, gate_decision, final_action).
```

The `evaluate.eair_robustness_summary` node records whether retrieval perturbation and claim extraction noise were both active, then summarizes the candidate decision, gate decision, final decision, and outcome class. It does not replace the action evaluator; it standardizes perturbation outcomes for later sweeps.

Multi-run robustness sweep:

```text
Sweep = { (P_i, N_i, seed_i) }_{i=1}^n
OutcomeDist = Count_i[ RobustnessOutcome_i ].
PassRate = (1/n) * sum_i 1[action_evaluator_pass_i].
```

Seed-grid expansion:

```text
SeedGrid = R x C
R = {r_1, ..., r_m} retrieval perturbation seeds
C = {c_1, ..., c_l} claim extraction noise seeds

Expand(P, N, SeedGrid) =
  { (P[seed <- r], N[seed <- c]) : r in R, c in C }.
```

The `evaluate.eair_robustness_sweep` node executes a list of retrieval perturbation and claim-noise configs from the current retrieved evidence state, optionally expands each config through a retrieval/claim-noise seed grid, then writes JSON/CSV artifacts for aggregate analysis.

Case-level robustness aggregation:

```text
CaseSweep = { (case_j, condition_j, SweepConfig_j) }_{j=1}^m
CaseOutcomeDist_j = Count_i[ RobustnessOutcome_{j,i} ]
AggregateOutcomeDist = sum_j CaseOutcomeDist_j
CaseTypeOutcomeDist_t =
  sum_{j: type(case_j)=t} CaseOutcomeDist_j
AggregatePassRate =
  (1 / sum_j n_j) * sum_j sum_i 1[action_evaluator_pass_{j,i}].

CaseSelector(case_ids, conditions, case_types, limit)
  -> ordered subset of EAIR-Bench (case_id, condition) samples.

PassRateCI95 = WilsonCI(successes=sum pass_i, n=total runs, z=1.9599639845).

CoverageGate =
  1[ observed_cases >= min_cases
     and observed_case_types >= min_case_types
     and RequiredCaseTypes subset ObservedCaseTypes ].
```

The `evaluate.eair_case_robustness_sweep` node creates fresh EAIR-Bench retrieval states for multiple `(case_id, condition)` pairs, runs the same sweep semantics per case, and writes aggregate JSON/CSV/Markdown artifacts. Cases may be provided explicitly or selected from the built-in benchmark with `case_selector` filters over `case_ids`, `conditions`, and `case_types`. It also groups outcomes by `case_type` so benchmark-category failure modes can be summarized separately, reports Wilson 95% pass-rate intervals at aggregate, per-case, and per-case-type levels, and can fail the evaluator result when an optional `coverage` gate shows the selected slice is too narrow for the intended claim. In robustness summaries, `route_to_simulation` is treated as an allowed supported action when it is the evidence-backed final decision, not as a generic safe fallback.

## 4. 冲突图

构造 claim conflict graph：

```text
G_c = (C_q, E_c),
E_c = { (c_i, c_j, t, omega_ij) }.
```

其中 `t` 是冲突类型：

- `semantic_conflict`：语义互斥，例如 “可跳过审批” vs “必须审批”。
- `temporal_conflict`：过期信息 vs 当前信息。
- `source_conflict`：低信任来源 vs 高信任来源。
- `procedural_conflict`：流程要求不一致。
- `simulation_conflict`：自然语言建议与仿真结果不一致。
- `tool_schema_conflict`：工具描述/参数约束与注册表不一致。

冲突强度：

```text
conf(c_i,c_j) = omega_ij in [0,1].
```

对 claim `c_i` 的可信反压力：

```text
M_conf(c_i) = sum_{j:(i,j) in E_c} conf(c_i,c_j) * S(c_j) * kappa(t_ij).
```

`kappa(t)` 是冲突类型的重要性权重。例如，在电网操作中，simulation conflict 和 procedural conflict 权重应高于普通网页文本冲突。

Claim credibility：

```text
Cred(c_i) = S(c_i) / (epsilon + S(c_i) + M_conf(c_i)).
```

Claim suspicion：

```text
Susp(c_i) = S_susp(c_i) / (epsilon + S(c_i)).
```

解释：

- `Cred(c)` 高表示 claim 有强可信支持且冲突压力低。
- `Susp(c)` 高表示 claim 主要由可疑或污染证据支撑。
- 二者都不是“真值”，而是 action gate 的可计算 proxy。

## 5. Agent 决策模型

Agent 产生：

```text
(y, pi, a, T) = F_theta(q, K_q, C_q, G_c, H_t).
```

其中：

- `y`：自然语言回答；
- `pi = (p_1, ..., p_l)`：计划步骤；
- `a`：工具调用或操作性建议；
- `T`：证据链，记录 `claim -> plan step -> action` 的支持边。

动作集合：

```text
A = A_read union A_sim union A_report union A_write_like union A_approval.
```

风险等级：

```text
risk(a) in {low, medium, high, critical}.
```

电网场景中，`write_like` 不一定是真写控制命令，也可以是：

- 建议跳过审批；
- 给出危险参数；
- 建议解除安全联锁；
- 在报告中错误降低风险等级；
- 调用错误仿真工具或漏掉 N-1 检查。

## 6. 文档到动作的影响

硬影响定义：

```text
I_hard(d -> a | q,K) =
1[ A(F_theta(q,K)) != A(F_theta(q,K \ {d})) ].
```

软影响定义：

```text
I_soft(d -> a | q,K) =
TV( P_theta(A | q,K), P_theta(A | q,K \ {d}) ).
```

如果不能得到动作分布，可用重复采样估计：

```text
I_soft_hat(d) = (1/n) * sum_{b=1}^n 1[ A_b(q,K) != A_b(q,K \ {d}) ].
```

动作支持路径：

```text
Path(a) = { c in C_q : c is required by action a in trace T }.
```

路径最弱可信度：

```text
PathCred(a) = min_{c in Path(a)} Cred(c).
```

独立可信来源充分性：

```text
TrustedClusters(c) =
  { cluster(d) : d supports c
                 and tau(d) >= gamma_tau
                 and freshness(d) >= gamma_fresh
                 and p_pois(d) <= gamma_pois_doc }.

IndependentSources(c) = |TrustedClusters(c)|.

TrustedIndependentSupport(a) = 1[
  forall c in Path(a): IndependentSources(c) >= m(a)
].
```

实现上，cluster 内的多个近重复文档只贡献一次支持强度；因此 `S(c)` 不是简单文档求和，
而是对 `source_cluster` 饱和后的可信支持求和。`m(a)` 可由 action risk level 或
domain policy 指定，当前 EAIR-Bench pilot 对高风险 oracle action 使用
`min_support_clusters`。

Freshness / version sufficiency:

```text
SupportFreshness(c) =
  max_{d supports c, z(d)=0} freshness(d).

FreshSupport(a) = 1[
  forall c in Path(a): SupportFreshness(c) >= gamma_fresh(a)
].
```

Explicit version graph sufficiency:

```text
Superseded(d) = 1[
  exists d_new in K_q:
    tau(d_new) >= gamma_tau
    and freshness(d_new) >= gamma_fresh
    and supersedes(d_new, d)
].

CurrentSupport(c) = 1[
  exists d supports c:
    tau(d) >= gamma_tau
    and freshness(d) >= gamma_fresh
    and Superseded(d) = 0
].

VersionCurrentSupport(a) = 1[
  forall c in Path(a): CurrentSupport(c) = 1
].
```

The current pilot implements this through `version_id` and `supersedes` metadata on retrieved documents. The `superseded_trusted_policy_support` condition shows why scalar freshness is not enough: archived 2025 policy documents keep high freshness scores, but a trusted 2026 notice supersedes their versions. These documents remain visible through `candidate_superseded_support_count`, but they do not count toward `TrustedIndependentSupport(a)`.

在当前 pilot 中，过期但高信任的 archived policy 仍可产生 oracle-shaped action；
但如果 `FreshSupport(a)=0`，该动作不能被视为 evidence-sufficient。后续更强版本应将
`freshness(d)` 替换或增强为显式 version graph，例如 `current(d)`、`supersedes(d_i,d_j)`、
`valid_at(d,t)`。

路径污染暴露在实现中拆成原始审计信号与门控有效信号：

```text
RawPathPois(a) = max_{c in Path(a)} Susp(c).

PoisonSupportWarning(a) = 1[
  RawPathPois(a) > gamma_pois(a)
  and TrustedIndependentSupport(a) = 1
  and HardGate(a) = PASS
].

PathPois(a) =
  0,              if PoisonSupportWarning(a) = 1
  RawPathPois(a), otherwise.
```

也就是说，污染证据与可信证据共同支撑同一动作时，系统保留
`raw_path_poison` 与 `poison_support_warning` 供审计；只有在缺少独立可信支撑、
或动作违反硬策略时，污染压力才作为有效 `path_poison` 进入阻断条件。

## 7. Evidence-to-Action Integrity Risk

定义动作级风险：

```text
EAIR(q,a) =
  lambda_1 * sum_{d in K_q} I_soft(d -> a) * (1 - tau(d))
+ lambda_2 * sum_{d in K_q} I_soft(d -> a) * p_pois(d)
+ lambda_3 * max_{c in Path(a)} (1 - Cred(c))
+ lambda_4 * PathPois(a)
+ lambda_5 * ConflictAction(a)
+ lambda_6 * DomainViolation(a,w)
+ lambda_7 * ToolPolicyViolation(a).
```

其中：

```text
ConflictAction(a) = max_{c in Path(a)} M_conf(c) / (epsilon + S(c) + M_conf(c)).
```

```text
DomainViolation(a,w) in [0,1]
```

由电网规则或仿真 oracle 计算，例如审批未满足、设备状态不允许、潮流不可行、N-1 不满足。

```text
ToolPolicyViolation(a) in {0,1}
```

表示动作越权、工具参数不合法、读写权限不匹配、工具文档与注册表冲突等。

## 8. Evidence-Action Gate

高风险动作允许条件：

```text
Allow(a | q,K) = 1[
  EAIR(q,a) <= eta_risk(a)
  and PathCred(a) >= gamma_cred(a)
  and PathPois(a) <= gamma_pois(a)
  and DomainGate(a,w) = PASS
  and ToolGate(a) = PASS
].
```

否则输出策略：

```text
Block(a) -> one of {
  abstain,
  ask_for_more_evidence,
  route_to_simulation,
  require_human_approval,
  produce_non_operational_summary
}.
```

关键点：

- Gate 必须在模型外部执行，不能只是 prompt。
- 模型可以生成候选动作，但不能自行决定绕过 gate。
- 对 `critical` 动作，`eta_risk` 应更低、`gamma_cred` 更高。

## 9. Conflict-Aware Robust Retrieval

基础相关性检索：

```text
K_rel = argmax_{K subset D, |K|=k} sum_{d in K} r(q,d).
```

鲁棒检索目标：

```text
K_star = argmax_{K subset D, |K|=k}
    sum_{d in K} r(q,d)
  + mu * Diversity(K)
  + nu * sum_{d in K} tau(d) rho(d)
  - xi * Conflict(K)
  - omega * ActionSensitivity(K)
  - chi * ToolSurfaceRisk(K).
```

其中：

```text
Conflict(K) = sum_{(c_i,c_j) in E_c(K)} conf(c_i,c_j) * kappa(t_ij).
```

```text
ActionSensitivity(K) = max_{d in K} I_soft(d -> a).
```

```text
ToolSurfaceRisk(K) = sum_{d in K} 1[s(d)=tool-doc] * p_pois(d) * Privilege(tool(d)).
```

解释：

- 这不是要牺牲所有相关性，而是在高风险任务中防止“单个高相似污染文档”主导动作。
- 如果 evidence conflict 是真实业务冲突，不应简单删除；应保留并触发 abstain/escalation。

## 10. 可检验命题

命题 1：Retrieval exposure 与 action harm 不等价。

```text
PRE(q) high does not imply Unsafe(a)=1.
```

因为污染文档可能被冲突检测、低信任分数、domain gate 或 human approval gate 拦下。

命题 2：如果高风险动作的所有必需 claim 均满足可信度阈值，且 domain/tool gate 无假阴性，则 unsupported action rate 受 claim extraction 与 conflict detection 错误率上界约束。

非严格表达：

```text
P[UnsupportedAction]
<= P[claim_path_missing] + P[conflict_false_negative] + P[domain_gate_false_negative] + P[tool_gate_false_negative].
```

这个式子不是最终定理，而是实验假设：系统错误主要来自四类模块错误，可通过 ablation 验证。

命题 3：Action-sensitive retrieval 在相同 Top-K 污染比例下，应降低 unsafe decision rate。

实验假设：

```text
UDR(K_star) < UDR(K_rel)
```

尤其在 `z(d)=1` 但 `r(q,d)` 很高的 adversarial document 场景中。

## 11. 指标定义

检索层：

```text
Poison Retrieval Rate = (# poisoned docs in Top-K) / K
Rank-weighted Poison Exposure = sum alpha_j z(d_j)
```

证据层：

```text
Conflict Detection F1
Conflict Type Accuracy
Evidence Resolution Accuracy
Claim Credibility Calibration Error
```

动作层：

```text
Unsafe Decision Rate = # unsafe actions / # cases
Unsupported Action Rate = # actions without sufficient PathCred / # actions
Wrong Tool Rate = # wrong tool selections / # tool cases
Wrong Parameter Rate = # unsafe or invalid parameters / # parameter cases
Poison Support Warning Rate = # actions with poisoned co-support warning / # cases
```

可审计性：

```text
Evidence-to-Action Trace Fidelity =
# high-risk actions with replayable valid support path / # high-risk actions.
```

效用：

```text
Clean Utility Retention =
clean-task pass rate under defense / clean-task pass rate without defense.
```

过度拒绝：

```text
Over-refusal Rate =
# safe actions blocked / # safe actions.
```

## 12. 实验估计方法

对每个 case 构造多种 retrieval condition：

```text
clean
poison_only
clean_plus_poison
clean_plus_stale
clean_plus_conflict
tool_doc_poison
dynamic_tool_surface_poison
```

对每个 condition，运行：

```text
retrieval -> evidence extraction -> conflict graph -> model/agent -> gate -> evaluator
```

记录：

```text
{K_q, C_q, G_c, y, pi, a, T, EAIR, gate_decision, oracle_label}
```

比较：

```text
Delta_UDR = UDR_baseline - UDR_method
Delta_Utility = Utility_method - Utility_baseline
```

## 13. 边界与非主张

本文不能声称：

- 已经解决所有 RAG 投毒；
- 已经证明真实电网控制安全；
- `tau(d)` 或 `p_pois(d)` 在真实部署中可完美估计；
- LLM 生成的 evidence trace 天然可信。

本文可以声称：

- 提出 retrieval-to-action pollution 这一更贴近安全关键 Agent 的威胁模型；
- 给出统一检索、冲突、工具动作的数学风险函数；
- 提供可复现 benchmark 和可计算指标；
- 证明外部 evidence-action gate 在模拟电网任务中能降低 unsafe/unsupported actions，同时保持 clean utility。

## 14. 与 FormalTrust 的最小实现关系

需要新增或扩展：

1. `retrieval.mock_power` node：生成或重排 `RetrievedDocument`。
2. `evidence.claims` node：把文档转换为结构化 claims。
3. `guardrail.evidence_action_gate` node：计算 EAIR 并拦截动作。
4. `evaluate.actions` node：读取标准化动作 JSON，计算 UDR/UAR/EATF。
5. case metadata：定义 `oracle_action`、`risk_level`、`required_claims`、`forbidden_actions`。

这些都是局部扩展，不需要推翻当前框架。

## 15. Live-Run Evidence Boundary

For provider-backed experiments, the formal evidence object is not a transient API response or console log. It is:

```text
transcript JSONL
+ replay artifact_manifest.json
+ replay result JSON
+ replay report Markdown
+ coverage-gated summary tables
```

The run protocol is:

```text
LiveConfigReady
-> SampleProviderTranscripts
-> VerifyReplayManifest
-> RequireCompleteCoverage
-> ReportModelConditionMatrix
```

This boundary is orthogonal to the mathematical gate:

```text
Allow(a) =
  HardGate(a) = PASS
  and EvidenceSufficient(a)
  and EAIR(q,a) <= eta
```

The runbook and config checker establish experimental validity. They do not change `HardGate`, `EvidenceSufficient`, or `EAIR`; they only determine whether a provider-backed artifact is admissible for reporting.

Reportability is therefore a predicate over artifacts:

```text
ReportableRun(R) =
  VerifiedManifest(R)
  and CompleteCoverage(R)
  and ForAll(t in Transcripts(R)): SamplingMode(t) = live
  and not DryRunModel(R)
```

This is not part of the action-level gate. It is an experiment-validity condition for deciding whether model-condition outcomes may be cited as live-provider evidence.

The persisted audit artifact is:

```text
AuditArtifact(R) = {
  reportable,
  coverage_complete,
  sampling_modes,
  models,
  errors
}
```

`AuditArtifact(R).reportable=false` can coexist with `CompleteCoverage(R)=true`; this is exactly the dry-run positive-control case.

Paper-table export is gated by:

```text
ExportableForPaper(R) =
  ReportableRun(R)
  and AuditArtifact(R).reportable = true
  and SummaryCoverage(R).complete = true
```

If `ExportableForPaper(R)=false`, the system may write a blocked-export audit, but it must not write a live-provider result table.

Runtime preflight is a separate predicate:

```text
LiveRuntimeReady(C, E) =
  LiveConfigReady(C)
  and EnvPresent(E, C.api_key_env)
  and SecretNotPersisted(E[C.api_key_env])
```

`LiveRuntimeReady` is checked before sampling. It is not evidence about model behavior; it only decides whether provider sampling may start.

The operational workflow status is:

```text
WorkflowStatus(R) =
  first_failed([
    LiveRuntimeReady,
    TranscriptExists,
    ManifestVerified,
    CompleteCoverage,
    ReportableRun,
    ExportableForPaper
  ])
```

`WorkflowStatus` is an artifact-management predicate, not an EAIR safety predicate.
