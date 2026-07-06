# Iteration 068: Reportable Export Integrity Audit

## Goal

Turn the protocol source hash from static metadata into a post-export audit gate.

## Implemented

- Added `audit_reportable_eair_export`.
- Added CLI command `eair-audit-reportable-export`.
- The audit recomputes the current SHA256 of `protocol_legitimacy_path`.
- The audit checks reportable protocol child artifacts for the same recorded hash.
- Failure writes `reportable_export_integrity_audit.json` and `.md` before returning a blocking CLI exit.
- The live prompt-protocol runbook now includes a final `reportable_export_integrity_audit` command.

## Red-Green

Red checks:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_protocol_source_hash_mismatch -q
failed because the CLI command did not exist

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
failed because the runbook did not include reportable_export_integrity_audit
```

Green checks:

```text
pytest tests/test_mvp.py::test_eair_audit_reportable_export_detects_protocol_source_hash_mismatch -q
1 passed

pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
1 passed
```

## Readback

The current reportable fixture audit passes with:

```text
expected_protocol_legitimacy_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
actual_protocol_legitimacy_sha256=317d7ef211ab083cf91b85a12c9ba537f99d753a4ea29ad0eee850b0939fb6f4
child artifacts passed=true
```

## Boundary

This supports artifact-chain integrity for reportable tables. It does not claim live-provider safety behavior.
