# Power-Ops Evidence-Bound Related Work Prose

**Status:** ready
**Paper section:** §2 Related Work and Novelty Boundary
**Paragraph count:** 6
**Forbidden claim hits:** 0

## Related Work Prose

AgentSpec and formal-security-agent work already establish broad runtime enforcement and formal monitoring as neighboring territory. We therefore frame this paper around a narrower object: field-level action invariance inside a structured candidate action.

AgentVisor, AgentSentry, and CaMeL cover semantic privilege separation, safe continuation, and capability-style prompt-injection defenses. Our positioning is that CapGuard repairs structured action fields after authority decisions and records why preserved fields remain allowed.

ToolPrivBench and RACG make least privilege and capability minimization close neighbors. The distinction here is below tool exposure: after a mixed action is formed, each field must still be justified by the authority of its source.

InjecGuard, AgentSentry, and AgentVisor already motivate over-defense and security utility tradeoffs. We use that motivation only to define a measurable failure mode: authorized final-field loss under strict intervention.

The safe contribution is field-level action invariance with authority witnesses and repair-frame validity: preserve authorized fields, remove invalid fields, and expose the evidence that supports every preserved field.

The related-work boundary is explicit. The current artifact does not use production telemetry, does not make an official neighboring-system superiority claim, does not claim generic agent-security firstness, and does not claim real workload reduction.

## Paragraph Evidence

| Slot | Paragraph | Neighbors | Source refs | Safe delta | Boundary |
|---|---|---|---|---|---|
| runtime_enforcement_neighbors | AgentSpec and formal-security-agent work already establish broad runtime enforcement and formal monitoring as neighboring territory. We therefore frame this paper around a narrower object: field-level action invariance inside a structured candidate action. | AgentSpec; AI Agents with Formal Security Guarantees | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Closest Work Table (AgentSpec,Formal Security); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Closest Prior Work Delta (AgentSpec) | Field-level action invariance studies source-to-field authority coverage inside a candidate action, not a general policy DSL. | Do not present the artifact as a generic agent runtime monitor. |
| prompt_injection_privilege_neighbors | AgentVisor, AgentSentry, and CaMeL cover semantic privilege separation, safe continuation, and capability-style prompt-injection defenses. Our positioning is that CapGuard repairs structured action fields after authority decisions and records why preserved fields remain allowed. | AgentVisor; AgentSentry; CaMeL | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Closest Work Table (AgentVisor,AgentSentry,CaMeL); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Closest Prior Work Delta (AgentVisor,AgentSentry,CaMeL) | The current artifact repairs structured action fields after authority decisions and records witnesses for preserved fields. | Use these systems as close neighbors, not as failure cases. |
| least_privilege_capability_neighbors | ToolPrivBench and RACG make least privilege and capability minimization close neighbors. The distinction here is below tool exposure: after a mixed action is formed, each field must still be justified by the authority of its source. | ToolPrivBench; RACG | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Closest Work Table (ToolPrivBench,RACG); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Closest Prior Work Delta (ToolPrivBench,RACG) | Those neighbors reason about tool choice or exposure; this slice checks whether each field in an already formed action is justified by its source authority. | Do not sell field repair as the first least-privilege agent method. |
| over_conservatism_neighbors | InjecGuard, AgentSentry, and AgentVisor already motivate over-defense and security utility tradeoffs. We use that motivation only to define a measurable failure mode: authorized final-field loss under strict intervention. | InjecGuard; AgentSentry; AgentVisor | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Landscape Summary (over-defense,conservative blocking); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Core Claims (C2,C5) | The measurable object here is authorized final-field loss under intervention, not benign-prompt false positives. | Use over-conservatism as motivation only. |
| action_invariance_delta | The safe contribution is field-level action invariance with authority witnesses and repair-frame validity: preserve authorized fields, remove invalid fields, and expose the evidence that supports every preserved field. | AgentSpec; AgentVisor; AgentSentry; CaMeL; ToolPrivBench; RACG | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Positioning Takeaway (field-level action invariance); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Defensible Contribution Statement (field-level,repair) | The safe claim is field-level action invariance: preserve authorized fields, remove invalid fields, and expose why each preserved field is allowed. | Limit empirical language to the current curated and trace-backed artifacts. |
| claim_boundary | The related-work boundary is explicit. The current artifact does not use production telemetry, does not make an official neighboring-system superiority claim, does not claim generic agent-security firstness, and does not claim real workload reduction. | AgentDojo; AgentSpec; AgentVisor; AgentSentry; CaMeL; ToolPrivBench; RACG | docs/power_ops_action_invariance_lit_review_2026-07-02.md#Unsafe Headlines (Unsafe headlines); docs/power_ops_action_invariance_novelty_firewall_2026-07-02.md#Claim Boundary For Paper Draft (Forbidden) |  | No production telemetry, no official neighboring-system superiority, no generic agent-security firstness, and no real workload-reduction claim. |
