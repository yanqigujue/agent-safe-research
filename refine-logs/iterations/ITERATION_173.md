# Iteration 173: LaTeX Compile Audit

## Status

complete

## Goal

Attempt to compile the source-commented LaTeX manuscript when a local TeX toolchain is available, and otherwise persist an explicit environment-blocked compile audit.

## TDD

Added `test_power_ops_latex_compile_audit_records_missing_toolchain` to require:

- artifact type `power_ops_latex_compile_audit`;
- `blocked_missing_toolchain` status when no configured tool is found;
- TeX file existence recorded;
- PDF absence recorded;
- explicit blocker naming the missing toolchain.

Observed red:

```text
ModuleNotFoundError: No module named 'formaltrust_platform.experiments.power_ops_latex_compile_audit'
```

## Implementation

- Added `formaltrust_platform/experiments/power_ops_latex_compile_audit.py`.
- The audit checks for `latexmk`, `pdflatex`, and `xelatex`.
- If a tool exists, it runs the compiler and records return code, output tails, and PDF existence.
- If no tool exists, it writes a blocked audit instead of pretending compilation succeeded.
- Generated:
  - `docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.md`
  - `docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.json`
- Updated README, PAPER_PLAN, task_plan, findings, and progress.

## Readback

```text
latex_compile_audit: blocked_missing_toolchain
tex_exists=True
toolchain_available=False
pdf_exists=False
blocker=No LaTeX toolchain found; checked latexmk, pdflatex, xelatex
```

## Verification

```text
pytest tests/test_power_ops_action_invariance.py::test_power_ops_latex_compile_audit_records_missing_toolchain -q
1 passed

pytest tests/test_power_ops_action_invariance.py::test_power_ops_latex_compile_audit_records_missing_toolchain tests/test_power_ops_action_invariance.py::test_power_ops_latex_manuscript_exports_bound_draft_with_source_comments tests/test_power_ops_action_invariance.py::test_power_ops_current_numeric_audit_includes_assembled_paper_draft -q
3 passed

pytest tests/test_power_ops_action_invariance.py -q
61 passed

pytest -q
261 passed
```

## Keep / Revise / Reject

keep

## Next

Iteration 174 should create a citation/BibTeX scaffold for named neighboring systems and source artifacts without inventing unverified references.
