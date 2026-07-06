# Reportable Claim Review Declaration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an auditable command that turns a claim-template manifest plus a passing citation audit into a hash-locked reviewed claim manifest.

**Architecture:** Implement a focused `record_reportable_claim_review` function in `formaltrust_platform/experiments/eair_bench.py`, expose it through Typer, and wire it into the generated live runbook before the strict paper-ready claim audit. The command writes a new reviewed manifest and never silently mutates the source template manifest.

**Tech Stack:** Python, Typer CLI, pytest, existing EAIR reportable claim artifacts.

---

### Task 1: Red CLI Test

**Files:**
- Modify: `tests/test_mvp.py`

- [x] **Step 1: Add a failing review declaration test**

Add a test near the existing reportable-claim tests:

```python
def test_eair_record_reportable_claim_review_requires_passing_audit(tmp_path: Path) -> None:
    artifact_path = tmp_path / "reportable_results_export.json"
    claims_path = tmp_path / "reportable_claims.json"
    audit_dir = tmp_path / "claim_audit"
    reviewed_path = tmp_path / "paper_ready_claims.json"
    artifact_path.write_text(
        json.dumps({"artifact_type": "eair_reportable_results_export", "warrant_leaderboard": [{"warrant_quality_score": 0.4444}]}) + "\n",
        encoding="utf-8",
    )
    artifact_sha256 = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    claims_payload = {
        "artifact_type": "eair_reportable_claims",
        "claim_generation": "template",
        "claims": [
            {
                "claim_id": "warrant_quality_rank_1",
                "text": "Template claim: WarrantGuard quality score is 0.4444.",
                "artifact_path": str(artifact_path),
                "artifact_sha256": artifact_sha256,
                "json_path": "warrant_leaderboard.0.warrant_quality_score",
                "expected": 0.4444,
            }
        ],
    }
    claims_path.write_text(json.dumps(claims_payload) + "\n", encoding="utf-8")

    audit = CliRunner().invoke(
        app,
        [
            "eair-audit-reportable-claims",
            "--claims",
            str(claims_path),
            "--output-dir",
            str(audit_dir),
        ],
    )
    assert audit.exit_code == 0, audit.output

    audit_path = audit_dir / "reportable_claim_citation_audit.json"
    failed_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    failed_audit["passed"] = False
    failed_audit["errors"] = ["forced failure"]
    audit_path.write_text(json.dumps(failed_audit) + "\n", encoding="utf-8")

    blocked = CliRunner().invoke(
        app,
        [
            "eair-record-reportable-claim-review",
            "--claims",
            str(claims_path),
            "--claim-audit",
            str(audit_path),
            "--reviewer",
            "paper-author",
            "--review-note",
            "Reviewed claim text and cited values.",
            "--reviewed-at-utc",
            "2026-06-21T00:00:00Z",
            "--output",
            str(reviewed_path),
        ],
    )
    assert blocked.exit_code == 2
    assert "claim citation audit did not pass" in blocked.output
    assert not reviewed_path.exists()

    fresh_audit = CliRunner().invoke(
        app,
        [
            "eair-audit-reportable-claims",
            "--claims",
            str(claims_path),
            "--output-dir",
            str(audit_dir),
        ],
    )
    assert fresh_audit.exit_code == 0, fresh_audit.output

    reviewed = CliRunner().invoke(
        app,
        [
            "eair-record-reportable-claim-review",
            "--claims",
            str(claims_path),
            "--claim-audit",
            str(audit_path),
            "--reviewer",
            "paper-author",
            "--review-note",
            "Reviewed claim text and cited values.",
            "--reviewed-at-utc",
            "2026-06-21T00:00:00Z",
            "--output",
            str(reviewed_path),
        ],
    )
    assert reviewed.exit_code == 0, reviewed.output
    reviewed_payload = json.loads(reviewed_path.read_text(encoding="utf-8"))
    assert reviewed_payload["claim_generation"] == "human_reviewed"
    assert reviewed_payload["human_reviewed"] is True
    assert reviewed_payload["review_status"] == "reviewed"
    assert reviewed_payload["reviewer"] == "paper-author"
    assert reviewed_payload["review_note"] == "Reviewed claim text and cited values."
    assert reviewed_payload["reviewed_at_utc"] == "2026-06-21T00:00:00Z"
    assert reviewed_payload["source_claims_sha256"] == hashlib.sha256(claims_path.read_bytes()).hexdigest()
    assert reviewed_payload["source_claim_audit_sha256"] == hashlib.sha256(audit_path.read_bytes()).hexdigest()

    strict = CliRunner().invoke(
        app,
        [
            "eair-audit-reportable-claims",
            "--claims",
            str(reviewed_path),
            "--output-dir",
            str(tmp_path / "paper_ready_claim_audit"),
            "--require-reviewed",
        ],
    )
    assert strict.exit_code == 0, strict.output
```

- [x] **Step 2: Run the red test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit -q
```

Expected: FAIL because the CLI command does not exist.

### Task 2: Minimal Implementation

**Files:**
- Modify: `formaltrust_platform/experiments/eair_bench.py`
- Modify: `formaltrust_platform/cli.py`

- [x] **Step 1: Implement `record_reportable_claim_review`**

Add the function after `write_reportable_claim_template`. It should:

- read claims and claim audit JSON;
- reject non-`eair_reportable_claims`;
- reject non-`eair_reportable_claim_citation_audit`;
- require `passed=true`, `failed_claim_count=0`, and no audit errors;
- require the audit `claims_path` to match the supplied `--claims`;
- reject overwriting an existing output unless `force=True`;
- reject writing to the same path as the source claims file;
- write the reviewed manifest fields listed in the design.

- [x] **Step 2: Expose the CLI command**

Add `record_reportable_claim_review` to the import list in `formaltrust_platform/cli.py` and expose:

```text
eair-record-reportable-claim-review
```

Options:

```text
--claims
--claim-audit
--reviewer
--review-note
--reviewed-at-utc
--output
--force
```

- [x] **Step 3: Run the green test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_record_reportable_claim_review_requires_passing_audit -q
```

Expected: PASS.

### Task 3: Runbook Integration

**Files:**
- Modify: `tests/test_mvp.py`
- Modify: `formaltrust_platform/experiments/eair_bench.py`

- [x] **Step 1: Update the live-runbook test**

Require command name:

```text
paper_ready_claim_review_declaration
```

Require that the paper-ready strict audit and seal commands use:

```text
paper_ready_claims.json
```

- [x] **Step 2: Run the red runbook test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
```

Expected: FAIL because the review declaration command is missing.

- [x] **Step 3: Update `_live_runbook_payload`**

Add a command between diagnostic claim audit and paper-ready strict audit:

```text
formaltrust eair-record-reportable-claim-review --claims .../reportable_claims.json --claim-audit .../claim_audit/reportable_claim_citation_audit.json --reviewer REVIEWER_ID --review-note "Reviewed claim text and cited artifact values." --output .../paper_ready_claims.json
```

Update strict paper-ready audit and seal commands to use `paper_ready_claims.json`.

- [x] **Step 4: Run the green runbook test**

Run:

```powershell
pytest tests/test_mvp.py::test_eair_live_runbook_command_writes_prompt_matrix_json_sidecar -q
```

Expected: PASS.

### Task 4: Artifacts, Docs, Verification

**Files:**
- Modify generated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md`
- Modify generated `outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.json`
- Modify docs and logs.

- [x] **Step 1: Regenerate the live runbook**

Run:

```powershell
python -m formaltrust_platform eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
```

- [x] **Step 2: Update docs/logs**

Document that the paper-ready chain now starts from a review declaration artifact.

- [x] **Step 3: Run focused tests**

Run:

```powershell
pytest tests/test_mvp.py -k "live_runbook or claim_template or reportable_claims or claim_bundle or claim_bundle_seal or reportable_export or reportable_results or reportable_run_audit or protocol_legitimacy or prompt_adherence" -q
```

- [x] **Step 4: Run full tests**

Run:

```powershell
pytest -q
```
