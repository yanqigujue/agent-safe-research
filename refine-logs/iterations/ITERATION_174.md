# Iteration 174: Citation Scaffold

## Status

complete

## Goal

Create a BibTeX/citation scaffold for named neighboring systems without inventing unverified bibliographic metadata.

## TDD

Added `test_power_ops_citation_scaffold_uses_lit_review_without_inventing_bibtex` to require:

- artifact type `power_ops_citation_scaffold`;
- ready scaffold from the local literature review;
- keys for AgentSpec, AgentVisor, AgentSentry, CaMeL, ToolPrivBench, RACG, AgentDojo, and InjecGuard;
- all entries marked metadata-pending;
- invented reference count `0`;
- no fabricated `author =` field in the scaffold BibTeX;
- blocked output when no literature entries can be parsed.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_citation_scaffold'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_citation_scaffold.py`.
- Parsed the closest-work table in `docs/power_ops_action_invariance_lit_review_2026-07-02.md`.
- Generated:
  - `docs/power_ops_action_invariance_citation_scaffold_2026-07-02.md`
  - `docs/power_ops_action_invariance_citation_scaffold_2026-07-02.json`
  - `paper/power_ops_action_invariance/references_scaffold.bib`
- BibTeX entries include title, URL, and a metadata-pending note, but no invented author/year fields.
- Updated README, PAPER_PLAN, task_plan, findings, and progress.

## Readback

```text
citation_scaffold: ready
entry_count=11
metadata_pending_count=11
verified_source_count=10
caution_source_count=1
invented_reference_count=0
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_citation_scaffold_uses_lit_review_without_inventing_bibtex -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_citation_scaffold_uses_lit_review_without_inventing_bibtex tests/test_power_ops_action_invariance.py::test_power_ops_latex_compile_audit_records_missing_toolchain tests/test_power_ops_action_invariance.py::test_power_ops_current_numeric_audit_includes_assembled_paper_draft -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
62 passed

pytest -q
262 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 175 should verify or fetch citation metadata from primary sources and promote only confirmed entries into checked BibTeX.
