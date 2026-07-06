# Iteration 167: Assembled Draft Numeric Audit

## Status

complete

## Goal

Include the assembled 7-section paper draft in numeric-claim audit coverage so the current paper-facing draft is audited directly.

## TDD

Added `test_power_ops_current_numeric_audit_includes_assembled_paper_draft` to require the generated numeric-audit JSON to list:

```text
docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.md
```

Observed red:

```text
assert 'docs/power_ops_action_invariance_evidence_bound_paper_draft_2026-07-02.md' in [...]
```

Added `test_power_ops_numeric_claim_audit_supports_assembled_draft_section4_numbers` to require section-4 draft numbers to resolve through evidence/context rules rather than `needs_evidence`.

Observed red:

```text
assert 22 == 0
```

## Implementation

- Extended numeric-audit context rules for section-4 draft numbers:
  - 10-case curated baseline grid;
  - 18-case expanded suite;
  - expanded dataset audit coverage `1.000`;
  - 4 baseline modes;
  - 4 trace-import boundary cases;
  - 1 multi-step source-chain case;
  - 18 fully supported table rows;
  - source-link completeness and text match rate `1.000`.
- Ignored Markdown heading numbers and HTML source-comment date/path numbers.
- Normalized document paths to POSIX style in audit JSON.
- Regenerated numeric audit with the assembled paper draft as document 4 and section-4 evidence files included.

## Readback

```text
numeric_audit: documents=4, evidence=9, supported=22, table=186, context=23, ignored=87, unsupported=0
residual_triage: needs_evidence=0, categories={}
paper_readiness: PASS, blockers=0, forbidden_scan_artifact_count=16, forbidden_hits=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_current_numeric_audit_includes_assembled_paper_draft tests/test_power_ops_action_invariance.py::test_power_ops_numeric_claim_audit_supports_assembled_draft_section4_numbers -q
2 passed

pytest tests/test_power_ops_action_invariance.py -q
55 passed

pytest -q
255 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 168 should add a bounded conclusion section from paper-ready claims and limitation boundaries.
