# Power-Ops Evidence-Bound Method Outline

**Status:** ready
**Paper section:** §3 Formal Model and CapGuard
**Paper-ready claims:** 11
**Forbidden claim hits:** 0

## Method Outline

| Slot | Paragraph goal | Source refs | Source claims | Limitation reason |
|---|---|---|---|---|
| formal_objects | Define Cap(x) for source-derived capabilities and Need(s,f) for field-level authority needs in power-operation actions. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#1. Objects (Cap(x), Need(s, f)); docs/power_ops_action_invariance_paper_outline_2026-07-02.json#§3 Formal Model and CapGuard | L1:fieldwise repair final-action mode exists |  |
| coverage_rule | Specify Covers(c,n) across role, field, operation, data scope, effect scope, delegation scope, time scope, and obligations. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#2. Coverage (Covers(c, n), obligations_satisfied) | L1:fieldwise repair final-action mode exists |  |
| minimal_witness_decision | Explain Minimal Authority Witness and the field decision rule: allow, abstain, or block. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#3. Minimal Authority Witness (MinimalWitness); docs/power_ops_action_invariance_formal_model_2026-07-02.md#4. Decision Rule (FieldDecision) | L1:fieldwise repair final-action mode exists |  |
| repair_invariance | Define Preserve, Prevent, ActionInvariant, conservative collapse, and Repair(a) as the method's action-preservation target. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#5. Action Invariance (ActionInvariant); docs/power_ops_action_invariance_formal_model_2026-07-02.md#6. Conservative Collapse (strict_block_collapse_rate); docs/power_ops_action_invariance_formal_model_2026-07-02.md#9. Claim Boundary (Repair(a)) | L1:fieldwise repair final-action mode exists; L2:curated power-ops fieldwise repair preserves authorized fields and removes unauthorized fields; L2:expanded 18-case power-ops fieldwise repair preserves authorized fields and removes unauthorized fields |  |
| implementation_binding | Map formal objects to FormalTrust runtime locations without adding new state schema fields. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#8. Current Implementation Binding (metrics[, afw_runtime_field_results) | L1:fieldwise repair final-action mode exists |  |
| claim_boundary | State that the method section supports a local artifact and benchmark slice, not production telemetry or operator workload claims. | docs/power_ops_action_invariance_formal_model_2026-07-02.md#9. Claim Boundary (live deployment safety, human-label agreement) | L1:fieldwise repair final-action mode exists | No production telemetry; no real workload reduction; no official neighboring-system superiority. |
