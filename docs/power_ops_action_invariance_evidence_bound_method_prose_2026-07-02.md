# Power-Ops Evidence-Bound Method Prose

**Status:** ready
**Paper section:** §3 Formal Model and CapGuard
**Paragraph count:** 6
**Forbidden claim hits:** 0

## Method Prose

We model each agent source as a capability object Cap(x) and each action field as an authority need Need(s,f), so authorization is checked at field granularity rather than at the whole-action level.

A capability covers a field only when role, field, operation, data scope, effect scope, delegation scope, time scope, and required obligations all match.

For each field, CapGuard records a Minimal Authority Witness when coverage exists; otherwise the field decision becomes abstain or block depending on counter-authority and evidence completeness.

The repair target is ActionInvariant(a,a'): preserve allowed fields, prevent unauthorized fields, and implement Repair(a) as keep allowed fields plus remove, block, or route the rest.

The implementation binds these objects to existing FormalTrust metadata and metrics, including afw_source_events, afw_consumptions, candidate_action, afw_runtime_field_results, witness_audit, and final_action.

This method section is bounded to the local artifact and benchmark slice: no production telemetry, no real workload-reduction claim, and no official neighboring-system superiority claim.

## Paragraph Evidence

| Slot | Paragraph | Formal refs | Source claims | Limitation reason |
|---|---|---|---|---|
| formal_objects | We model each agent source as a capability object Cap(x) and each action field as an authority need Need(s,f), so authorization is checked at field granularity rather than at the whole-action level. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#1. Objects (Cap(x), Need(s, f)); docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§3 Formal Model and CapGuard | L1:fieldwise repair final-action mode exists |  |
| coverage_rule | A capability covers a field only when role, field, operation, data scope, effect scope, delegation scope, time scope, and required obligations all match. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#2. Coverage (Covers(c, n), obligations_satisfied) | L1:fieldwise repair final-action mode exists |  |
| minimal_witness_decision | For each field, CapGuard records a Minimal Authority Witness when coverage exists; otherwise the field decision becomes abstain or block depending on counter-authority and evidence completeness. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#3. Minimal Authority Witness (MinimalWitness); docs/power_ops_action_invariance_formal_model_2026-07-02.md#4. Decision Rule (FieldDecision) | L1:fieldwise repair final-action mode exists |  |
| repair_invariance | The repair target is ActionInvariant(a,a'): preserve allowed fields, prevent unauthorized fields, and implement Repair(a) as keep allowed fields plus remove, block, or route the rest. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#5. Action Invariance (ActionInvariant); docs/power_ops_action_invariance_formal_model_2026-07-02.md#6. Conservative Collapse (strict_block_collapse_rate); docs/power_ops_action_invariance_formal_model_2026-07-02.md#9. Claim Boundary (Repair(a)) | L1:fieldwise repair final-action mode exists; L2:curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields; L2:expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields |  |
| implementation_binding | The implementation binds these objects to existing FormalTrust metadata and metrics, including afw_source_events, afw_consumptions, candidate_action, afw_runtime_field_results, witness_audit, and final_action. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#8. Current Implementation Binding (metrics[, afw_runtime_field_results) | L1:fieldwise repair final-action mode exists |  |
| claim_boundary | This method section is bounded to the local artifact and benchmark slice: no production telemetry, no real workload-reduction claim, and no official neighboring-system superiority claim. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#9. Claim Boundary (live deployment safety, human-label agreement) | L1:fieldwise repair final-action mode exists | No production telemetry; no real workload reduction; no official neighboring-system superiority. |
