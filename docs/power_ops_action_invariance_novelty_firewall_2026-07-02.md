# Power-Ops Action Invariance Novelty Firewall

## Proposed Method

The current method, implemented in the FormalTrust AFW path, models each source as a capability carrier `Cap(x)` and each action field as a requirement `Need(s,f)`. CapGuard checks whether the capability covers the field need. In `fieldwise_repair` mode, the final action preserves fields with valid authority and removes or routes blocked/abstained fields to partial human review.

## Core Claims

| Claim | Novelty | Closest Work | Firewall Decision |
|---|---|---|---|
| C1. Runtime guardrails can enforce safe LLM-agent behavior. | LOW | AgentSpec, AgentVisor, CaMeL, verifiably safe tool use | Do not claim. This is established neighboring territory. |
| C2. Guardrails can be overly conservative and harm utility. | LOW | InjecGuard, AgentSentry, AgentVisor | Use as motivation only. |
| C3. Least privilege matters for LLM-agent tools and capabilities. | LOW | ToolPrivBench, RACG, CaMeL | Do not claim as main novelty. |
| C4. Authorization should be checked at action-field granularity, not only whole tool/action granularity. | MEDIUM | CaMeL capabilities, AgentSpec predicates, ToolPrivBench | Safe if phrased as field-to-source authority consumption with `Need(s,f)` and witness logs. |
| C5. Under a strict guard decision, authorized fields should remain invariant while invalid fields are repaired. | MEDIUM-HIGH | AgentSentry safe continuation, AgentVisor self-correction, runtime shielding | Strongest current claim, if backed by repair-frame validity and baseline comparison. |
| C6. This can be implemented over power-operation traces, span logs, and OTLP `resourceSpans`. | MEDIUM | Verifiably safe tool use, AgentBound/MCP security, AgentSpec domains | Safe as an artifact contribution, not a universal deployment claim. |

## Closest Prior Work Delta

| Neighbor | What They Already Cover | What We Must Not Say | Remaining Delta |
|---|---|---|---|
| AgentSpec | General runtime-enforcement DSL for agent constraints | "We are the first runtime policy enforcement system." | We define a specific field-authority coverage relation and measure final-action preservation. |
| AgentVisor | Semantic privilege separation, audit protocol, self-correction, low utility loss | "We solve security/utility tradeoff first." | We repair structured action fields after CapGuard decisions and output minimal authority witnesses. |
| AgentSentry | Temporal causal diagnosis, context purification, safe continuation | "We are the first safe-continuation defense." | We do not localize takeover; we enforce source-to-field authority and verify the repaired action frame. |
| CaMeL | Control/data-flow extraction and capability policies for prompt-injection resistance | "We invented capability-based agent security." | Our object is action-field authorization coverage and partial repair, not global program-flow isolation. |
| ToolPrivBench | Over-privileged tool selection and least-privilege tool choice | "We are the least-privilege tool paper." | We work inside a mixed action payload; tool privilege can be correct while a field's source authority is wrong. |
| RACG | Capability exposure gated by causal necessity and authorization provenance | "We introduced capability minimization." | RACG withholds tools before action selection; we preserve/repair fields after a candidate action is formed. |
| InjecGuard | Over-defense in prompt-injection guard models | "We discovered over-defense." | We measure over-conservatism as authorized final-field loss, not benign prompt false positives. |
| AgentDojo | Benchmark environment for prompt injection attacks/defenses | "Our curated cases prove general agent robustness." | Use AgentDojo as future external-validity target; current cases are regression artifacts. |

## Defensible Contribution Statement

Recommended:

> We introduce and implement a field-level action-invariance check for high-risk power-operation agents. The method gives each action field a required authority, derives capabilities from RAG/skill/tool/memory/trace sources, and verifies that guard intervention preserves authorized fields while removing only blocked or abstained fields. The current artifact demonstrates the property on curated power-operation cases and span/OTLP replay.

Avoid:

> We propose a new general guardrail for LLM agents.

Avoid:

> We solve prompt injection without utility loss.

Avoid:

> We are the first least-privilege framework for LLM agents.

## Current Evidence Ledger

| Evidence | Status | Supports |
|---|---|---|
| `formaltrust_platform/nodes/afw.py` fieldwise repair mode | implemented | CapGuard can produce repaired final actions. |
| `validate_fieldwise_repair_frame` | implemented | Repaired action preserves authorized fields and removes invalid keys. |
| 10-case power-ops metadata suite | implemented, curated | Fieldwise repair beats strict-block on whole-action collapse for current cases. |
| 2-case canonical trace repair suite | implemented, curated | Trace adapter can feed fieldwise repair. |
| 2-case span/OTLP repair suite | implemented, curated | `span_log_v1` and OTLP `resourceSpans` can feed fieldwise repair. |
| baseline grid | implemented, curated | strict-block is safe but over-conservative; provenance-only is useful but unsafe; fieldwise repair preserves and removes the right fields in current cases. |
| `pytest -q` | 210 passed | Current artifact is regression-stable. |
| Real production logs | missing | Needed for external validity. |
| Official baseline comparison | missing | Needed before claiming superiority. |
| Independent benchmark mapping | missing | Needed before claiming generality beyond power-ops. |

## Overall Novelty Assessment

- Score: 6.5/10 now.
- Recommendation: PROCEED WITH CAUTION.
- Key differentiator: action-field repair invariant with authority witnesses, not generic guardrails.
- Main risk: reviewers may collapse the idea into AgentSpec/CaMeL/RACG/ToolPrivBench unless the paper emphasizes final-action preservation and shows baselines where whole-action or tool-level controls are too coarse.

## Minimum Next Experiments

1. Metrics:
   - unauthorized field prevention
   - authorized final-field preservation
   - whole-action block rate
   - repair-frame validity
   - human-review field count
2. Externality:
   - add real/semi-real power span logs
   - or map a small AgentDojo-style task to fieldwise action fields

The baseline grid is now implemented for strict-block, fieldwise-decision-only, provenance-only, and fieldwise-repair on the curated power-ops suite. The next missing step is external validity, not the first baseline table.

## Claim Boundary For Paper Draft

Allowed:

- "On curated power-operation regression cases, fieldwise repair preserves authorized fields that strict-block would suppress."
- "The artifact supports span/OTLP trace replay through the existing FormalTrust interfaces."
- "The contribution is a field-level authority-witness and repair-validity formulation."

Forbidden:

- "Outperforms AgentSpec, AgentVisor, AgentSentry, CaMeL, ToolPrivBench, RACG, or AgentDojo defenses."
- "Solves prompt injection."
- "Proves production safety."
- "First runtime enforcement framework for LLM agents."
- "First least-privilege LLM-agent approach."
