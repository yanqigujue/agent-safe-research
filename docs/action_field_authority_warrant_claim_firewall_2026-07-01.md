# Claim Firewall: Action-Field Authority Warrants

Date: 2026-07-01

## Purpose

This file protects the paper from overclaiming. The field is crowded: provenance, authorization, proof-carrying actions, skill security, MCP invariants, tool privilege, consent integrity, memory authority, and protocol composition all overlap with parts of the vocabulary.

The paper should claim a narrow object:

> semantic-role authority for non-parameter protected action fields.

## Claim We Can Make

Safe main claim:

> We identify semantic-role laundering in agent actions: the same source may be valid for one action field but invalid for another. We propose action-field authority warrants, which check whether each protected non-parameter field consumed sources that cover the field's required semantic roles and scopes.

Safe algorithm claim:

> CapGuard implements a field-authority type check over source capabilities and field needs, including same-source contrast, multi-source required roles without role amplification, trace-derived role-confusion generation, minimal authority witness extraction and compression, manifest-lifted capability inference, and obligation discharge.

Safe runtime-adapter claim:

> A FormalTrust graph can now parse curated raw agent trace events through `custom.afw_trace_adapter`, lift manifest-declared source authority into `Cap(x)`, derive field-level `Need(s,f)` consumptions, and run runtime CapGuard before the AFW evaluator.

Safe malformed-trace claim:

> The same trace-adapter path now records schema diagnostics for curated malformed raw trace events and fails closed: malformed or unknown events are not trusted as runtime authority inputs, and CapGuard abstains when no valid capability/consumption pair can be derived.

Safe span-log claim:

> The trace adapter also supports one semi-real span-log preset, `span_log_v1`, which maps retrieval, agent-action, and authority-use spans into the same AFW runtime inputs before CapGuard runs.

Safe benchmark claim:

> Same-source paired rows expose a failure mode missed by binary permission, binary attribution, and pure strict-blocking baselines.

Safe action-invariance claim:

> CapGuard can also be described as a fieldwise supervisor: under explicit source-to-field consumptions and independent field effects, it preserves protected fields with valid authority witnesses while suppressing or routing fields without valid authority. This is a local fieldwise permissiveness claim, not a global optimal-control claim for arbitrary LLM agents.

Safe production-chain claim:

> The current AFW implementation includes a machine-checkable production-chain manifest for the planned electric-power RAG system. It validates that embedding, rerank, and generation roles are declared, the AFW guardrail is placed after generation, and the stated memory/API constraints are internally consistent.

## Claims To Avoid

Do not claim:

- first agent authorization framework;
- first proof-carrying agent action system;
- first provenance-aware agent defense;
- first content-to-authority flow model;
- first skill security system;
- first MCP runtime invariant framework;
- first tool-privilege benchmark;
- first study of guardrail utility loss, over-refusal, or benign-task preservation;
- first runtime monitor, probabilistic safety monitor, action shield, or runtime-assurance architecture for LLM agents;
- first symbolic guardrail, policy DSL, or customizable runtime enforcement framework for LLM agents;
- first multi-valued access-control decision model, deontic security-policy logic, policy-composition semantics, or obligation-carrying authorization system;
- first policy-adherence verifier, dialogue-level policy remediation system, or guardrail availability / denial-of-service analysis;
- first information-flow, noninterference, declassification, abstract-interpretation, static-analysis, capability-security, confused-deputy, protocol-verification, attack-tree, attack-graph, or game-theoretic security model for agents;
- first trust-management logic, credential-chain authorization model, assurance-case/GSN model, evidence-fusion trust model, subjective-logic model, Bayesian attack graph, argumentation-based security policy, causal-attribution defense, robust-optimization guard policy, model-based diagnosis, or formal-concept-analysis access-control method;
- first STPA/STAMP method, STPA-Sec security analysis, FMEA/FMECA method, fault-tree analysis, bow-tie risk model, HAZOP method, or risk-prioritized security benchmark for AI/LLM agents;
- first RBAC, ABAC, ReBAC, UCON/usage-control, NGAC/policy-machine, zero-trust, policy-as-code, separation-of-duty, or least-privilege model for AI/LLM agents;
- first Byzantine/quorum, threshold-signature, multi-approval, non-repudiation, tamper-evident log, Merkle log, transparency-log, secure-provenance, provenance-semiring, verifiable-credential, in-toto, SLSA, Sigstore/Rekor, or software-supply-chain provenance model for AI/LLM agents;
- first assume-guarantee, contract-based design, interface-automata, I/O automata, TLA+, LTL, Alloy, HyperLTL, trace-refinement, rely-guarantee, separation-logic, or formal model-checking framework for AI/LLM agents;
- globally maximally permissive supervision for arbitrary LLM agents; current theory only supports a local fieldwise claim under explicit consumption edges and independent-field assumptions;
- official failure of AuthGraph, SkillGuard, PCAA, Cordon, or any named system unless we actually run their implementations.
- fully automatic production-log parsing or live-agent trace coverage; the current raw-trace adapter evidence covers curated smoke cases, one semi-real span-log preset, and curated malformed negative cases, not a production deployment.
- fully automatic OTLP production observability coverage; the current OTLP result covers one curated OpenTelemetry-style attribute-list case under the `span_log_v1` preset.
- fully automatic OTLP resourceSpans production coverage; the current envelope result covers one curated `resourceSpans -> scopeSpans -> spans` export case.
- fully general obligation lifecycle enforcement; the current runtime evidence covers two curated span-log cases with one `must_discharge` static-scan obligation.
- fully general temporal policy reasoning; the current runtime temporal evidence covers two curated span-log cases with a single explicit policy epoch.
- live production deployment, real GPU saturation, or measured concurrent-user service behavior; the current production-chain evidence is a manifest validation report, not a launched service.

## Reviewer Objection Map

| Objection | Why it is dangerous | Safe answer | Required evidence |
|---|---|---|---|
| "This is just access control." | Access control is a broad old concept. | AFW is a field-level authority-consumption check: the same source is allowed in one field and blocked in another. | Same-source legal-vs-laundered table. |
| "AuthGraph already aligns authorization and provenance." | AuthGraph is close on tool and parameter-source provenance. | AFW focuses on semantic-role validity for non-parameter fields such as approval, risk/report, side-effect release, delegation, and data scope. | AuthGraph-discriminator row where parameter provenance is valid but approval/risk authority is not. |
| "PCAA already carries action proofs." | PCAA blocks generic proof-carrying action novelty. | AFW can be framed as field-level payload semantics for a certificate, not as the first certificate system. | Show AFW fields can fit inside proof-carrying action envelopes. |
| "SkillGuard/proof-carrying skills already protect skills." | Skill-security work covers skill artifacts and permissions. | Our skill rows make the skill benign/allowed; the failure is later laundering of skill authority into a protected action field. | Skill rows with legal formatting/data-cleaning and illegal delegation/data-scope/risk uses. |
| "Tool privilege already covers this." | Tool-privilege benchmarks cover overpowered tool choices. | AFW handles allowed tools whose side-effect, approval, or risk fields are justified by the wrong source role. | Tool metadata rows where schema use is legal but approval/side-effect use is invalid. |
| "Consent or scope-boundary checks already cover this." | Consent-lattice and boundary guards are stronger than permission-only baselines. | Boundary checks can verify field, operation, data, effect, delegation, and time scopes while still missing semantic-role validity. | Role-only discriminator: report-formatting skill has correct boundary scope but is not risk-assessment authority. |
| "Attribution already tells us where the answer came from." | Attribution is a common RAG defense. | Attribution says which source influenced a field; AFW asks whether the source may govern that field. | Attribution-only baseline false-allows laundered rows. |
| "Strict blocking would be safer." | A blocker can match laundering block rate. | Strict blocking destroys legal same-source utility. | Strict-block baseline has false-block rate 1.0. |
| "SafeHarbor/TRIAD already handle agent over-refusal." | They directly pressure a broad over-refusal framing. | AFW should not claim first over-refusal mitigation. The safe delta is exact authorized-field preservation through minimal authority witnesses, not only benign-task success. | Fieldwise transparency / witness-backed transparency metrics. |
| "PolicyGuard already verifies policy adherence and remediates dialogue." | It pressures any broad policy-adherence or remediation claim. | AFW should not claim first policy verifier. The delta is source-to-field capability coverage and invariance for authorized action fields. | `ValidAuthority(s,f)`, minimal witness, and authorized-field preservation. |
| "Guardrail DoS already shows guardrails can hurt availability." | It directly pressures the claim that strict guardrails can damage normal operation. | AFW should cite this as motivation, not novelty. The delta is measuring and bounding conservative collapse at the field level. | Guard cost bound violation, conservative collapse rate, partial task salvage. |
| "ShieldAgent/ProbGuard already do agent shielding or runtime monitoring." | They pressure any broad "runtime guard" framing. | AFW does not decide only when to intervene; it decides which concrete fields have authority witnesses and therefore must be preserved or repaired. | Field-level source-to-Need witness and local maximal-permissiveness table. |
| "AgentSpec/symbolic guardrails already provide runtime policy enforcement." | They pressure any broad policy-DSL or trigger-check-enforce claim. | AFW is not a general guardrail DSL. The safe claim is a field-authority witness relation and the corresponding fieldwise transparency/maximal-permissiveness property. | `Cap(x)` / `Need(s,f)` coverage, witness-backed transparency metric. |
| "Supervisory control already has maximal permissiveness." | The theory is old and strong. | We borrow the lens and instantiate a local fieldwise analogue for LLM agent actions. Do not claim first maximal-permissiveness theory. | Theorem assumptions: explicit consumption, decidable authority, independent fields. |
| "XACML/Belnap/deontic logic already model permit/deny/conflict/obligation." | They pressure any claim about multi-valued policy decisions or obligations. | AFW borrows the decision vocabulary, but its object is source-to-field authority consumption and witness-backed field preservation. | Policy-logic appendix plus AFW witness/evaluator evidence. |
| "Information-flow control already models unauthorized influence." | Noninterference and declassification are mature theories. | AFW should not claim first information-flow model. The safe delta is authority flow from heterogeneous agent sources to structured action fields. | Authority noninterference property plus source-to-field rows. |
| "Abstract interpretation already explains soundness and precision." | Static analysis has a deep soundness/precision vocabulary. | AFW should use this as a lens: conservative collapse is precision loss in the authority abstraction. | Authority abstraction ablation and `authority_abstraction_precision`. |
| "Capability security already solves confused deputy." | Capability theory directly overlaps with wrong-authority misuse. | AFW instantiates capability discipline at the source-to-action-field boundary, including skill outputs, memory, approval, and prior-step outputs. | Boundary-preserving semantic-role mismatch and downstream skill-consumption rows. |
| "Protocol verification can already prove correspondence properties." | ProVerif/Tamarin/Dolev-Yao tools are mature. | Keep protocol verification as appendix/future-work support unless we actually encode AFW traces. | Trace correspondence statement: `Exec(s,f) => ValidAuthority(s,f)`. |
| "Attack trees / attack graphs already model attacks." | They are standard threat-modeling tools. | Use them to generate benchmark coverage, not as the core AFW contribution. | ADTree-derived laundering rows if implemented. |
| "Trust-management logics already model credential chains and delegation." | SPKI/SDSI, RT, and SecPAL overlap with capability manifests and delegation. | AFW should not claim new trust-management logic. The safe delta is applying credential-chain reasoning to heterogeneous agent source-to-field witnesses. | Manifest-lifted capability rows and no-role-amplification delegation cases. |
| "Assurance cases already connect claims to evidence." | GSN and safety/security cases already formalize claim-evidence arguments. | AFW should frame minimal authority witness as a field-level assurance subcase, not invent assurance cases. | Witness compression, assumptions, defeaters, and missing-fact outputs. |
| "Argumentation / defeasible logic already handles counterarguments." | Mature theory for accepted/attacked/undecided claims. | Use it to clarify counter-authority and `abstain`, not as a new argumentation framework. | Counter-authority rows with exposed defeaters. |
| "Evidence fusion already models uncertainty and trust confidence." | Dempster-Shafer, subjective logic, and Bayesian attack graphs are old. | Keep authority validity separate from confidence; confidence can guide review priority but cannot grant missing authority. | Confidence-carrying witness ablation if implemented. |
| "Causal attribution defenses already find malicious influence." | AttriGuard/CausalArmor-style work pressures any causal-provenance claim. | AFW checks whether the causal or declared source is allowed to govern the field; it does not claim first causal attribution. | Authority-causal alignment metric. |
| "Model-based diagnosis already produces minimal explanations." | Diagnosis and hitting-set repair are old. | AFW's safe delta is diagnosing missing authority facts for protected action fields. | Minimal diagnosis / blame localization oracle. |
| "STPA/STPA-Sec already analyze unsafe control and security flaws." | Safety engineering has mature hazard-analysis methods. | AFW should use STPA to derive agent authority scenarios, not claim a new STPA method. | STPA-derived unsafe control action table and legal/laundered/repair traces. |
| "FMEA/FMECA already prioritize failure modes." | Field failure scoring is an old reliability method. | AFW can use FMEA to prioritize false allow/block/abstain/repair failures for protected fields. | High-RPN failure coverage metric. |
| "Fault trees, bow-tie, and HAZOP already generate risk scenarios." | These are standard risk-engineering tools. | AFW's safe delta is applying them to source-to-field authority laundering and guard ablations. | Cut-set coverage and HAZOP-derived authority deviation rows. |
| "RBAC/ABAC already model roles and attributes." | Traditional access control is mature and broad. | AFW's boundary is source-to-field consumption, not user/tool permission. | Source-role separation and attribute coverage ablations. |
| "UCON already models ongoing authorization and obligations." | UCON strongly overlaps with temporal decay and obligation-carrying warrants. | AFW should cite UCON as the formal lens for continuous field authority. | Revocation response and obligation mutation cases. |
| "ReBAC/NGAC/policy graphs already model relationship paths." | Relationship and graph policy systems are mature. | AFW uses relationship paths to bound delegation from user/skill/memory/source to action fields. | Skill-driven relationship-bounded delegation rows. |
| "Zero Trust / policy-as-code already does dynamic contextual enforcement." | ZTA and OPA/Rego are widely used deployment patterns. | AFW's safe delta is zero-trust over source authority, not a new enterprise policy engine. | Source zero-trust rule and policy-export appendix if implemented. |
| "BFT/quorum systems already handle faulty participants." | Byzantine quorum theory is mature and much stronger than our use. | AFW should not claim consensus. The safe delta is threshold authority at the action-field witness boundary. | k-of-n issuer rows and source-independence violations. |
| "Threshold signatures and multisig already implement multi-party approval." | Threshold approval is old cryptographic and workflow machinery. | AFW uses threshold logic to decide whether a field has enough independent authority; it does not propose a new signature scheme. | `quorum_authority_coverage` and fake-quorum attack rows. |
| "Certificate Transparency and Merkle logs already give tamper-evident audit." | Append-only transparency logs are established. | AFW can log field-witness events for inclusion, consistency, and replay-epoch checks; the log design is not the novelty. | witness-log completeness and tamper-detection tests. |
| "Provenance semirings already model why-provenance." | Database provenance has a precise formal foundation. | AFW uses provenance expressions to compress source-to-field authority witnesses, not to claim new provenance theory. | provenance witness minimality and alternative witness path reports. |
| "Verifiable Credentials already encode signed claims." | VC issuer-holder-verifier models are standard. | AFW uses signed capability claims as inputs to `Cap(x)`; signature validity does not imply the capability covers the field. | wrong-role signed manifest discriminator rows. |
| "SLSA, in-toto, and Sigstore already solve supply-chain provenance." | Software supply-chain integrity is a mature deployment area. | AFW binds skill/tool outputs to artifact provenance before they may authorize protected fields. | skill provenance verification and unreviewed-skill rejection rows. |
| "Assume-guarantee and contracts already handle compositional systems." | Compositional verification is a mature formal-methods area. | AFW uses these as authority contracts: components may attenuate or explicitly combine capabilities, but composition must not create undeclared semantic roles. | contract refinement and no-role-amplification rows. |
| "Interface automata and I/O automata already model component compatibility." | Automata-based interface compatibility is old. | AFW's compatibility object is source-to-component authority consumption, not arbitrary protocol interaction. | interface compatibility and illegal-authority-consumption rows. |
| "TLA+, LTL, Alloy, and model checking already verify workflows." | Formal modeling tools are established and recent agent work already uses them. | AFW should use them to specify/generate action-field authority lifecycle cases, not claim first workflow verification. | temporal-property coverage and relational counterexample rows. |
| "Hyperproperties already model noninterference." | Hyperproperties and HyperLTL are mature. | AFW uses them to express same-source legal-vs-laundered contrast: unauthorized source perturbations must not affect guarded fields. | paired trace authority-noninterference metric. |
| "Trace refinement/process algebra already handles behavioral preservation." | Refinement checking is a standard verification technique. | AFW defines selective authority refinement: preserve authorized fields while suppressing or repairing unauthorized fields. | authority refinement pass rate. |
| "Rely-guarantee or separation logic already handles interference and frames." | Concurrency and frame reasoning are old. | AFW borrows frame conditions for fieldwise repair and source-mutation reasoning, not as a new logic. | frame preservation and interference violation detection. |
| "Unified source schema is hand-written." | The framework may look like examples only. | Use the same `Cap(x)` / `Need(s,f)` relation across evidence, skill, tool metadata, memory, approval, prior output, and composite authority rows. | Source-family generalization table and composite rows. |
| "This is just intent-governed authorization." | IGAC-style systems narrow tool authorization by user intent and payload consistency. | AFW is not an intent certificate; it checks whether each protected field consumed a source with the required semantic role and exposes a minimal field witness. | Boundary-preserving role-mismatch rows and witness output. |

## Current Evidence Status

Implemented:

- same-source deterministic rows: `examples/afw_same_source_paired_rows.json`;
- composite authority rows: `examples/afw_composite_authority_rows.json`;
- counter-authority rows: `examples/afw_counter_authority_rows.json`;
- attenuation rows: `examples/afw_attenuation_rows.json`;
- boundary-role rows: `examples/afw_boundary_role_rows.json`;
- trace scenario seed: `examples/afw_trace_scenarios.json`;
- obligation rows: `examples/afw_obligation_rows.json`;
- temporal rows: `examples/afw_temporal_rows.json`;
- power-ops RAG rows: `examples/afw_power_ops_rag_rows.json`;
- power-ops trace scenarios: `examples/afw_power_ops_trace_scenarios.json`;
- evaluator: `formaltrust_platform/experiments/afw_bench.py`;
- FormalTrust node wrapper: `formaltrust_platform/nodes/afw.py`;
- power-ops report helper: `formaltrust_platform/experiments/afw_power_ops_report.py`;
- tests: `tests/test_afw_bench.py`;
- deterministic results: `docs/action_field_authority_warrant_deterministic_results_2026-07-01.md`.
- manifest-lifted authority type inference: `infer_capability_from_trace_scenario` supports skill manifests and generic source authority manifests.
- time-scope authority decay: explicit `time_scope` blocks expired approval and stale memory reuse.
- power-ops trace scenario scale: 20 semi-real domain trace scenarios across 6 source types.
- power-ops paired-row scale: 32 rows across 6 source types and 4 sample origins; source-type and laundered field-family gaps are closed in the coverage matrix.
- power-ops trace-derived authority-confusion rows: 40 generated rows preserve boundary dimensions while mutating only the required semantic role across 19 target authority roles.
- power-ops plausibility audit sheet: 40 generated rows are structurally prechecked and ready for human review; do not claim human plausibility until the sheet is filled.
- runtime CapGuard path: `evaluate_authority_consumptions` and `guardrail.afw_capguard` can check explicit or manifest-lifted `Cap(x)` against runtime `Need(s,f)` consumptions and replace unauthorized candidate actions with `final_action=require_human_approval`.
- runtime evaluator path: `evaluate.afw_runtime` scores field decisions, gate decision, and final action against `case.metadata["afw_oracle"]`, producing `afw_behmatch`, false-allow fields, false-block fields, and prevented fields.
- executable runtime graph example: `examples/afw_runtime_validation.yaml` with `examples/data/afw_runtime_power_ops_cases.jsonl` runs `guardrail.afw_capguard -> evaluate.afw_runtime` over eight cases, preserving one legal answer action and blocking seven unsafe field consumptions across evidence, memory, skill, tool metadata, user approval, and prior-step output with mean `afw_behmatch=1.0`; all runtime cases use `afw_source_events` manifests.
- runtime K/BehMatch report: `formaltrust_platform/experiments/afw_runtime_report.py` aggregates FormalTrust case artifacts into AFW-subset K1-K4 proxy metrics; do not claim full project K1-K4 until live traces and a broader dataset are added.
- runtime witness audit report: `docs/power_ops_afw_runtime_k_report_2026-07-01.md` now aggregates minimal-witness audit fields across the eight-case runtime smoke run, reporting `mean_compression_ratio=0.875`, `covers_need_fields=1`, and `missing_role_fields=7`.
- raw trace adapter runtime graph: `examples/afw_trace_adapter_runtime_validation.yaml` with `examples/data/afw_trace_adapter_runtime_cases.jsonl` runs `custom.afw_trace_adapter -> guardrail.afw_capguard -> evaluate.afw_runtime` over one curated raw-trace case. The adapter parses 3 raw events into 1 source event, 1 candidate action, and 1 field consumption; CapGuard blocks `side_effect=dispatch_work_order` because `manual_answer_authority` does not cover `dispatch_operation_authority`, producing `afw_behmatch=1.0`, `prevented_fields=1`, and zero false allow/block fields.
- multisource raw trace adapter runtime graph: `examples/afw_trace_adapter_multisource_runtime_validation.yaml` with `examples/data/afw_trace_adapter_multisource_runtime_cases.jsonl` extends the same graph to six curated raw-trace source families: evidence, skill, tool metadata, memory, user approval, and prior-step output. The latest run `runs/20260701-071845-945921-afw-trace-adapter-multisource-runtime-validation` passes 6/6 cases with `mean_afw_behmatch=1.0`, `prevented_fields=6`, and zero false allow/block fields.
- malformed raw trace adapter contract: `examples/afw_trace_adapter_malformed_runtime_validation.yaml` with `examples/data/afw_trace_adapter_malformed_runtime_cases.jsonl` checks that malformed raw trace events are diagnosed and ignored rather than trusted. The latest run `runs/20260701-072826-635894-afw-trace-adapter-malformed-runtime-validation` passes 2/2 cases, records `cases_with_invalid_trace_schema=2`, `invalid_events=5`, `unknown_events=2`, and returns `afw_gate_decision=abstain` with no trusted runtime authority inputs.
- span-log raw trace adapter preset: `examples/afw_trace_adapter_span_log_runtime_validation.yaml` with `examples/data/afw_trace_adapter_span_log_runtime_cases.jsonl` runs `custom.afw_trace_adapter` with `schema_preset=span_log_v1` over two semi-real span-log cases. The latest run `runs/20260701-074652-664045-afw-trace-adapter-span-log-runtime-validation` passes 2/2 cases, covers evidence and skill span sources, blocks two laundered fields, and reports zero invalid/unknown trace events.
- OTLP attribute-list trace adapter preset: `examples/afw_trace_adapter_otlp_runtime_validation.yaml` with `examples/data/afw_trace_adapter_otlp_runtime_cases.jsonl` runs the same `schema_preset=span_log_v1` over an OpenTelemetry-style key/value span export. The latest run `runs/20260701-080027-503760-afw-trace-adapter-otlp-runtime-validation` passes 1/1 case, unwraps `stringValue`, `boolValue`, `arrayValue`, and `resource.attributes`, blocks one laundered dispatch field, and reports zero invalid/unknown trace events.
- OTLP resourceSpans envelope trace adapter preset: `examples/afw_trace_adapter_otlp_envelope_runtime_validation.yaml` with `examples/data/afw_trace_adapter_otlp_envelope_runtime_cases.jsonl` runs the same graph over a nested `resourceSpans -> scopeSpans -> spans` export. The latest run `runs/20260701-081053-922886-afw-trace-adapter-otlp-envelope-runtime-validation` passes 1/1 case, preserves resource-level source attribution, blocks one laundered dispatch field, and reports zero invalid/unknown trace events.
- runtime obligation-carrying warrant path: `examples/afw_trace_adapter_obligation_runtime_validation.yaml` with `examples/data/afw_trace_adapter_obligation_runtime_cases.jsonl` runs `custom.afw_trace_adapter -> guardrail.afw_capguard(runtime_enforce_obligations=true) -> evaluate.afw_runtime` over two curated span-log cases. The latest run `runs/20260701-082043-882765-afw-trace-adapter-obligation-runtime-validation` passes 2/2 cases: the discharged static-scan case is allowed, and the missing-discharge case is blocked with `undischarged_obligations=["requires_static_scan"]`.
- runtime temporal authority decay path: `examples/afw_trace_adapter_temporal_runtime_validation.yaml` with `examples/data/afw_trace_adapter_temporal_runtime_cases.jsonl` runs the same trace-adapter graph over two curated span-log cases. The latest run `runs/20260701-082951-007400-afw-trace-adapter-temporal-runtime-validation` passes 2/2 cases: Q3 approval authorizes Q3 public publish, while Q3 approval reused for Q4 is blocked.
- runtime counter-authority abstain path: `examples/afw_trace_adapter_counter_authority_runtime_validation.yaml` with `examples/data/afw_trace_adapter_counter_authority_runtime_cases.jsonl` runs the same trace-adapter graph over two curated span-log cases. The latest run `runs/20260701-084348-705454-afw-trace-adapter-counter-authority-runtime-validation` passes 2/2 cases: clean publish approval is allowed, while the same approval with `policy_hold` counter-authority abstains and routes to human approval.
- runtime suite report: `docs/power_ops_afw_runtime_suite_report_2026-07-01.md` aggregates 3 validation runs / 12 cases and reports false allow/block, abstain, malformed-trace diagnostics, counter-authority counts, and witness compression.
- all-config runtime suite report: `docs/power_ops_afw_runtime_all_configs_suite_report_2026-07-01.md` aggregates all 10 current runtime validation configs / 27 cases with zero false allow/block fields.
- requirement coverage matrix: `docs/power_ops_afw_requirement_coverage_2026-07-01.md` maps screenshot/PDF requirements to AFW artifacts and marks 4 supported, 6 partial, and 0 missing.
- dataset annotation audit: `docs/power_ops_afw_dataset_annotation_audit_2026-07-01.md` audits 32 paired rows and 8 runtime cases for the four required label elements; it keeps Kappa and full-scale dataset construction explicitly pending.
- annotation packet and Kappa workflow: `docs/power_ops_afw_annotation_packet_2026-07-01.jsonl` prepares 40 items for double annotation, and `docs/power_ops_afw_annotation_agreement_smoke_2026-07-01.md` verifies the Cohen's Kappa calculation path with machine-prefilled labels only.
- defense-loop proxy report: `docs/power_ops_afw_defense_loop_report_2026-07-01.md` runs measure-locate-defend-retest on 32 power-ops paired rows and reports `k2_min_risk_discovery_lift=0.125`, `k3_min_safety_issue_reduction=1.0`, `k4_utility_preservation=1.0`, and zero general ability drop.
- production-chain manifest report: `docs/power_ops_afw_production_chain_report_2026-07-01.md` validates the declared embedding/rerank/generation chain, memory budget, API compatibility, concurrency target, and AFW guardrail placement. Its status is `manifest_validated_not_live_deployment`.

Current test:

```text
pytest tests\test_afw_bench.py -q
57 passed
```

Interface registration test:

```text
pytest tests\test_interfaces.py tests\test_afw_bench.py -q
81 passed
```

Platform regression test:

```text
pytest tests\test_interfaces.py tests\test_afw_bench.py tests\test_mvp.py -q
146 passed
```

Do not overclaim:

- The runtime counter-authority path currently proves curated field/effect-scoped `counter_authority` span handling, not a complete policy-conflict lifecycle, automatic revocation discovery, or universal production-log parsing.
- Runtime witness compression is currently an artifact-level proxy over curated smoke cases, not a measured reduction in human reviewer time.
- The runtime suite reports currently aggregate curated validation runs, not the full benchmark and not a live deployment.
- The requirement coverage matrix is a slice-level AFW coverage audit, not a claim that the full project contract or final acceptance package is complete.
- The dataset annotation audit checks label completeness on the current AFW subset, not the full 1050/800/700-scale dataset and not human double-annotation Kappa.
- The annotation agreement smoke report is not human double annotation; do not cite its `min_kappa=1.0` as satisfying the project Kappa target.
- The defense-loop report is an AFW power-ops subset proxy; do not cite it as full project-level K2/K3/K4 until the broader dataset and live/semi-real traces are evaluated.
- The production-chain report is a manifest-level readiness check; do not cite it as evidence of live deployment, GPU-load performance, service availability, or measured 32/64-user concurrency.

Current result:

| Baseline | Legal preservation | Laundering block | False allow | False block |
|---|---:|---:|---:|---:|
| AFW / CapGuard | 1.0 | 1.0 | 0.0 | 0.0 |
| Permission-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Attribution-only | 1.0 | 0.0 | 1.0 | 0.0 |
| Strict-block | 0.0 | 1.0 | 0.0 | 1.0 |

Additional stronger-neighbor discriminator:

| Baseline | What it checks | What it misses |
|---|---|---|
| Boundary-scope-only | field, operation, data scope, effect scope, delegation scope, time scope | semantic-role mismatch, e.g. formatting authority reused as risk-assessment authority |
| Field-attribution-only | requires a named source for each field | whether the named source has authority for that field |
| AuthGraph-style parameter provenance | checks authorized parameter-source edges | non-parameter semantic roles such as approval, risk, side-effect, delegation |
| Skill-permission-style | checks direct skill effects against a manifest | downstream action-field consumption of skill outputs |

## Cited Pressure Points

- AuthGraph: https://arxiv.org/abs/2605.26497
- Proof-Carrying Agent Actions: https://arxiv.org/abs/2606.04104
- Toward Secure LLM Agents survey: https://arxiv.org/abs/2606.10749
- SkillGuard: https://arxiv.org/abs/2606.03024
- ToolPrivBench: https://arxiv.org/abs/2606.20023
- Intent-Governed Tool Authorization: https://arxiv.org/abs/2606.22916
- SafeHarbor: https://arxiv.org/abs/2605.05704
- TRIAD / Tri-Guard: https://arxiv.org/abs/2606.05805
- PolicyGuard: https://arxiv.org/abs/2606.29225
- Guardrail DoS: https://arxiv.org/abs/2606.14517
- ShieldAgent: https://arxiv.org/abs/2503.22738
- ProbGuard: https://arxiv.org/abs/2508.00500
- AgentSpec: https://arxiv.org/abs/2503.18666
- Symbolic Guardrails for Domain-Specific Agents: https://arxiv.org/abs/2604.15579
- MCP Security Best Practices: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- Language-Based Information-Flow Security: https://www.cs.cornell.edu/andru/papers/jsac/sm-jsac03.pdf
- Robust Declassification: https://www.cis.upenn.edu/~stevez/papers/Zda03.pdf
- Abstract Interpretation: https://cs.nyu.edu/~pcousot/publications.www/Cousot-FSP-2024.pdf
- Capability Myths Demolished: https://classpages.cselabs.umn.edu/Fall-2021/csci5271/papers/SRL2003-02.pdf
- ProVerif applied pi calculus: https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.pdf
- Tamarin Prover: https://tamarin-prover.com/manual/master/book/001_introduction.html
- Attack-defense trees: https://arxiv.org/abs/1210.8092
- SPKI Certificate Theory: https://www.rfc-editor.org/rfc/rfc2693
- SecPAL: https://www.microsoft.com/en-us/research/publication/secpal-design-semantics-decentralized-authorization-language/
- Goal Structuring Notation: https://scsc.uk/scsc-141B
- Subjective Logic: https://link.springer.com/book/10.1007/978-3-319-42337-1
- Dung argumentation frameworks: https://doi.org/10.1016/0004-3702(94)00041-X
- CausalArmor: https://arxiv.org/abs/2602.07918
- AttriGuard: https://arxiv.org/abs/2603.10749
- STPA Handbook: https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf
- STPA-Sec: https://sunnyday.mit.edu/papers/2014-03-19-STPA-Sec.pdf
- IEC 60812 FMEA/FMECA overview: https://webstore.iec.ch/publication/26359
- NASA Fault Tree Handbook: https://ntrs.nasa.gov/api/citations/20020062164/downloads/20020062164.pdf
- IEC 61882 HAZOP overview: https://webstore.iec.ch/publication/24321
- NIST RBAC: https://csrc.nist.gov/projects/role-based-access-control
- NIST SP 800-162 ABAC: https://csrc.nist.gov/pubs/sp/800/162/upd2/final
- UCONABC Usage Control: https://doi.org/10.1145/775412.775414
- NIST Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- Open Policy Agent: https://www.openpolicyagent.org/docs/latest/
- Practical Byzantine Fault Tolerance: https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance
- Shamir secret sharing: https://dl.acm.org/doi/10.1145/359168.359176
- NIST Multi-Party Threshold Cryptography: https://csrc.nist.gov/projects/threshold-cryptography
- Certificate Transparency RFC 6962: https://datatracker.ietf.org/doc/html/rfc6962
- Certificate Transparency RFC 9162: https://www.rfc-editor.org/info/rfc9162/
- Provenance Semirings: https://dl.acm.org/doi/10.1145/1265530.1265535
- W3C Verifiable Credentials Data Model 2.0: https://www.w3.org/TR/vc-data-model-2.0/
- in-toto: https://in-toto.io/
- SLSA specification: https://slsa.dev/spec/v1.2/
- Sigstore Rekor: https://docs.sigstore.dev/logging/overview/
- Interface Automata: https://dl.acm.org/doi/10.1145/503209.503226
- Contracts for Systems Design: https://www.nowpublishers.com/article/Details/EDA-016
- TLA+ book: https://lamport.azurewebsites.net/tla/book.html
- Temporal Logic of Actions: https://dl.acm.org/doi/10.1145/177492.177726
- Alloy Analyzer: https://alloytools.org/
- Hyperproperties: https://doi.org/10.3233/JCS-2009-0393
- Temporal Logics for Hyperproperties: https://link.springer.com/chapter/10.1007/978-3-642-54792-8_15
- Rely-guarantee reasoning: https://dl.acm.org/doi/10.1145/357980.358001
- Separation Logic: https://dl.acm.org/doi/10.1109/LICS.2002.1029817

## Final Positioning Sentence

Use:

> AFW is a field-authority validity layer for agent actions: it checks whether the source consumed by each protected action field has the semantic role required by that field.

Avoid:

> AFW is a universal agent authorization framework.

