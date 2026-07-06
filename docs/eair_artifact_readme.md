# EAIR Artifact README

This document defines the reproducible artifact protocol for EAIR-Bench model-output experiments.

## Evidence Boundary

The evidence object for model-facing experiments is:

```text
Transcript JSONL
+ artifact_manifest.json
+ structured_action_transcript_replay_results.json
+ structured_action_transcript_replay_report.md
```

Replay evaluates saved transcripts; it does not sample a live model.

## Dry-Run Sampling

Use the dry-run sampler config when testing the pipeline without a provider key:

```powershell
formaltrust eair-sample --config examples/eair_sampler_dry_run.yaml
```

This writes:

```text
outputs/eair_sampler_cli_dry_run/sampled_transcripts.jsonl
outputs/eair_sampler_cli_dry_run/replay/
```

## Live Sampling

Use the live template as a starting point:

```text
examples/eair_sampler_live_template.yaml
```

Set the environment variable named by `api_key_env`, then run:

```powershell
formaltrust eair-sample --config examples/eair_sampler_live_template.yaml
```

The sampler writes transcript JSONL first, then replay evaluates the saved transcripts. Do not cite a live run unless the transcript JSONL and replay artifacts are archived together.

Before running a live provider, check the config:

```powershell
formaltrust eair-check-live-config --config examples/eair_sampler_live_template.yaml
```

This check validates secret handling, expected-condition coverage, replay output paths, and accidental dry-run settings. It does not call the provider.

To check the current shell/runtime before sampling:

```powershell
formaltrust eair-doctor-live-run --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/live_preflight
```

This writes `live_run_doctor.json` and `live_run_doctor.md`. It verifies that the environment variable named by `api_key_env` is set, but it never records the secret value.

To snapshot the whole live workflow status:

```powershell
formaltrust eair-live-workflow-status --config examples/eair_sampler_live_template.yaml --output-dir outputs/eair_live_model_run/workflow_status
```

This writes `live_workflow_status.json` and `live_workflow_status.md`, including the first blocked stage and expected downstream artifacts.

Generate a live-run command bundle before collecting provider transcripts:

```powershell
formaltrust eair-write-live-runbook --config examples/eair_sampler_live_template.yaml --output outputs/eair_live_model_run/RUN_LIVE_MODEL.md
```

The runbook records the readiness check, provider sampling command, replay manifest verification, and coverage-gated summary command. Treat the runbook as protocol documentation, not as model-behavior evidence.

## Replay Existing Transcripts

Replay externally collected transcripts with:

```powershell
formaltrust eair-replay --transcripts examples/data/eair_structured_action_transcripts.jsonl --output-dir outputs/eair_replay_cli_pilot
```

The replay command writes:

```text
structured_action_transcript_replay_results.json
structured_action_transcript_replay_report.md
artifact_manifest.json
```

## Verify Artifacts

Verify that the manifest still matches the transcript and replay outputs:

```powershell
formaltrust eair-verify-artifact --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json
```

Verification checks:

- `artifact_type` is `eair_transcript_replay`;
- transcript file exists;
- transcript SHA256 matches `artifact_manifest.json`;
- result and report artifacts exist;
- manifest summary matches replay result JSON.

## Summarize Artifacts

Build paper-facing tables from one or more verified manifests:

```powershell
formaltrust eair-summarize-artifacts --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json --output-dir outputs/eair_artifact_summary
```

For planned model-condition coverage, pass expected condition keys:

```powershell
formaltrust eair-summarize-artifacts --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json --expected-condition approval_bypass::risk_report_downgrade_no_tool --output-dir outputs/eair_artifact_summary
```

For formal runs, require complete coverage:

```powershell
formaltrust eair-summarize-artifacts --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json --expected-condition approval_bypass::risk_report_downgrade_no_tool --require-complete-coverage --output-dir outputs/eair_artifact_summary
```

If coverage is incomplete, the command exits with an error after writing the coverage audit files.

For a complete dry-run fixture, use:

```powershell
formaltrust eair-sample --config examples/eair_sampler_complete_dry_run.yaml
```

Then summarize the generated manifest with the expected conditions and `--require-complete-coverage`. This fixture is deterministic and is only a protocol check, not live-model evidence.

The command verifies every manifest before aggregation and writes:

```text
artifact_summary.json
artifact_summary.csv
artifact_summary.md
artifact_summary_by_model.csv
artifact_summary_by_model.md
artifact_summary_by_prompt_variant.csv
artifact_summary_by_prompt_variant.md
artifact_summary_by_condition.csv
artifact_summary_by_condition.md
artifact_summary_by_model_condition.csv
artifact_summary_by_model_condition.md
artifact_summary_by_model_prompt_condition.csv
artifact_summary_by_model_prompt_condition.md
artifact_summary_warrant_leaderboard.json
artifact_summary_warrant_leaderboard.csv
artifact_summary_warrant_leaderboard.md
artifact_summary_coverage.csv
artifact_summary_coverage.md
```

The summary is an aggregation of replay manifests. It does not sample a model or rerun replay.

## Audit Reportable Live Runs

After a live provider run has been sampled, replayed, verified, and summarized with complete coverage, run:

```powershell
formaltrust eair-audit-reportable-run --manifest outputs/eair_live_model_run/replay/artifact_manifest.json --summary outputs/eair_live_model_run/summary/artifact_summary.json
```

This is the final reportability gate before citing model-behavior results. It requires verified manifests, complete coverage, matching summary rows, and transcript provenance with `sampling_mode: live`.

Dry-run artifacts are intentionally rejected even if they pass complete coverage.

To archive the audit:

```powershell
formaltrust eair-audit-reportable-run --manifest outputs/eair_live_model_run/replay/artifact_manifest.json --summary outputs/eair_live_model_run/summary/artifact_summary.json --output-dir outputs/eair_live_model_run/reportability
```

This writes `reportable_run_audit.json` and `reportable_run_audit.md`. Failure cases still write the audit files before exiting with an error.

## Export Reportable Results

Only after reportability passes, export paper-facing model-condition tables:

```powershell
formaltrust eair-export-reportable-results --summary outputs/eair_live_model_run/summary/artifact_summary.json --audit outputs/eair_live_model_run/reportability/reportable_run_audit.json --output-dir outputs/eair_live_model_run/paper_tables
```

This writes:

```text
reportable_results_export.json
reportable_model_condition_table.csv
reportable_model_condition_table.md
reportable_warrant_leaderboard.json
reportable_warrant_leaderboard.csv
reportable_warrant_leaderboard.md
```

If the audit did not pass, the command blocks export and writes `reportable_results_export_blocked.json` and `.md`.

## Multi-Prompt Dry-Run Smoke Test

Before spending live-provider budget, run the deterministic prompt-protocol fixture:

```powershell
formaltrust eair-sample --config examples/eair_multi_prompt_sampler_dry_run.yaml
```

This writes:

```text
outputs/eair_multi_prompt_sampler_dry_run/sampled_transcripts.jsonl
outputs/eair_multi_prompt_sampler_dry_run/replay
outputs/eair_multi_prompt_sampler_dry_run/summary
```

Expected control pattern:

- `legacy_action_only` has no valid warrant.
- `proof_carrying` and `proof_carrying_strict` have valid warrants.
- the WarrantGuard leaderboard preserves `prompt_variant`.

## Prompt-Protocol Matrix

For a fuller deterministic matrix, run:

```powershell
formaltrust eair-sample --config examples/eair_prompt_protocol_matrix_dry_run.yaml
```

This single command writes transcripts, replay outputs, coverage-gated artifact summaries, prompt-condition tables, and WarrantGuard leaderboard files under:

```text
outputs/eair_prompt_protocol_matrix_dry_run/
```

The control pattern is intentionally stricter than the single-condition smoke test: proof-carrying prompts pass clean and legitimate-evidence cases, but still fail parameter hijack when the warrant is backed by bad evidence or violates hard gates.

## Live Prompt-Protocol Matrix

The live-provider template mirrors the deterministic matrix:

```powershell
formaltrust eair-check-live-config --config examples/eair_prompt_protocol_matrix_live_template.yaml
formaltrust eair-doctor-live-run --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir outputs/eair_prompt_protocol_matrix_live/live_preflight
formaltrust eair-live-workflow-status --config examples/eair_prompt_protocol_matrix_live_template.yaml --output-dir outputs/eair_prompt_protocol_matrix_live/workflow_status
```

The checker reports the planned scale before any provider call:

```text
scenario_count: 3
prompt_variants: 3
planned_transcripts: 9
```

If `OPENAI_API_KEY` is not set, the doctor and workflow status should block at live preflight while still recording the planned matrix and `secret_value_recorded=false`.

Generate the reportable handoff runbook:

```powershell
formaltrust eair-write-live-runbook --config examples/eair_prompt_protocol_matrix_live_template.yaml --output outputs/eair_prompt_protocol_matrix_live/RUN_LIVE_PROMPT_MATRIX.md
```

This writes both:

```text
RUN_LIVE_PROMPT_MATRIX.md
RUN_LIVE_PROMPT_MATRIX.json
```

Use the JSON sidecar for automation and the Markdown file for human execution review. Neither file is live-model evidence by itself.

The prompt-protocol live runbook now includes the full paper-claim evidence chain after reportable table export:

```text
reportable_export_integrity_audit
reportable_claim_template
reportable_claim_citation_audit
reportable_claim_bundle_seal
reportable_claim_bundle_seal_verification
```

The `reportable_claims.json` file can be started with `eair-write-reportable-claim-template`, then reviewed and edited after paper-facing claims are drafted from the reportable tables.

## Prompt Adherence Audit

After transcripts exist, check whether each prompt variant followed its requested output protocol:

```powershell
formaltrust eair-audit-prompt-adherence --transcripts outputs/eair_prompt_protocol_matrix_dry_run/sampled_transcripts.jsonl --output-dir outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence
```

This writes:

```text
prompt_adherence_audit.json
prompt_adherence_audit.csv
prompt_adherence_audit.md
```

Use this audit to diagnose protocol-following failures. Do not use it as evidence that a warrant is legitimate or an action is safe.

## Protocol-Legitimacy Table

Join prompt adherence with WarrantGuard metrics:

```powershell
formaltrust eair-export-protocol-legitimacy-table --adherence outputs/eair_prompt_protocol_matrix_dry_run/prompt_adherence/prompt_adherence_audit.json --summary outputs/eair_prompt_protocol_matrix_dry_run/summary/artifact_summary.json --output-dir outputs/eair_prompt_protocol_matrix_dry_run/protocol_legitimacy
```

This writes:

```text
protocol_legitimacy_table.json
protocol_legitimacy_table.csv
protocol_legitimacy_table.md
protocol_legitimacy_by_prompt_variant.json
protocol_legitimacy_by_prompt_variant.csv
protocol_legitimacy_by_prompt_variant.md
```

The `adherence_legitimacy_gap` column is useful when a model follows the requested protocol but WarrantGuard rejects the warrant/action.

Use the prompt-variant aggregate for paper-level prompt ablations. Use the condition-level table to diagnose the specific scenario that caused the gap.

## Reportable Protocol-Legitimacy Export

After reportability audit passes, include protocol-legitimacy artifacts in the paper export:

```powershell
formaltrust eair-export-reportable-results --summary outputs/eair_warrant_live_fixture_summary/artifact_summary.json --audit outputs/eair_warrant_live_fixture_audit/reportable_run_audit.json --protocol-legitimacy outputs/eair_warrant_live_fixture_protocol_legitimacy/protocol_legitimacy_table.json --output-dir outputs/eair_warrant_reportable_export
```

This writes:

```text
reportable_protocol_legitimacy_table.json
reportable_protocol_legitimacy_table.csv
reportable_protocol_legitimacy_table.md
reportable_protocol_legitimacy_by_prompt_variant.json
reportable_protocol_legitimacy_by_prompt_variant.csv
reportable_protocol_legitimacy_by_prompt_variant.md
```

Use these `reportable_*` files for paper-facing protocol-legitimacy claims. Treat non-reportable protocol-legitimacy files as diagnostics.

The reportable export also checks row alignment. A supplied protocol row must match a row in the summary's `model x prompt_variant x condition` grouping, or the export is blocked.

It also checks selected metric consistency. Same-key protocol rows are blocked if their WarrantGuard rates, quality score, unsafe counts, or count-taxonomy JSON fields differ from the matching summary row.

Finally, it checks internal protocol-row arithmetic. Prompt adherence totals, compliant/noncompliant counts, prompt adherence rate, and adherence-legitimacy gap must agree inside each row.

Reportable protocol artifacts also record `protocol_legitimacy_sha256`, the SHA256 of the source `protocol_legitimacy_table.json`.

Audit the export after writing paper-facing files:

```powershell
formaltrust eair-audit-reportable-export --export outputs/eair_warrant_reportable_export/reportable_results_export.json --output-dir outputs/eair_warrant_reportable_export/integrity
```

This writes:

```text
reportable_export_integrity_audit.json
reportable_export_integrity_audit.md
```

The audit recomputes the SHA256 of `protocol_legitimacy_path` and checks that the reportable protocol child artifacts carry the same hash. It also checks that child artifact `rows` still match the rows embedded in `reportable_results_export.json`. If the source protocol file is replaced after export, or if a reportable child table is edited after export, the audit blocks while still writing its diagnostic files.

## Reportable Claim Citation Audit

For paper-facing claims, create a structured claim manifest:

```text
outputs/eair_warrant_reportable_export/reportable_claims.json
```

Generate a starter manifest with:

```powershell
formaltrust eair-write-reportable-claim-template --export outputs/eair_warrant_reportable_export/reportable_results_export.json --integrity-audit outputs/eair_warrant_reportable_export/integrity/reportable_export_integrity_audit.json --output outputs/eair_warrant_reportable_export/reportable_claims.json
```

Review the generated text before using the claims in paper prose.

The template command refuses to overwrite an existing `reportable_claims.json` by default. Use `--force` only when intentionally regenerating an unreviewed starter manifest or refreshing a deterministic fixture.

Each claim names an artifact, a dotted JSON path, and the expected value. Example paths:

```text
warrant_leaderboard.0.warrant_quality_score
protocol_legitimacy_by_prompt_variant.0.adherence_legitimacy_gap
checked_child_artifacts.0.rows_match_export
```

Audit the claims with:

```powershell
formaltrust eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/reportable_claims.json --output-dir outputs/eair_warrant_reportable_export/claim_audit
```

For paper-ready claims, require an explicit human-reviewed manifest:

```powershell
formaltrust eair-audit-reportable-claims --claims outputs/eair_warrant_reportable_export/reportable_claims.json --output-dir outputs/eair_warrant_reportable_export/claim_audit --require-reviewed
```

`--require-reviewed` rejects starter templates unless the manifest declares `claim_generation="human_reviewed"` or `human_reviewed=true`. Use the default audit for deterministic template-chain diagnostics; use the strict audit before treating claims as paper-ready.

This writes:

```text
reportable_claim_citation_audit.json
reportable_claim_citation_audit.md
```

The audit records each cited artifact SHA256, expected value, actual value, and pass/fail status. For paper-facing claims, include `artifact_sha256` in each claim entry so the audit also verifies that the cited artifact is the exact version used when the claim manifest was written.

Treat this as the paper-claim layer above reportable export integrity.

## Reportable Claim Bundle Seal

After the claim citation audit passes, seal the submission packet:

```powershell
formaltrust eair-seal-reportable-claim-bundle --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal
```

For paper-ready submission packets, require that the supplied claim audit was itself run in reviewed strict mode:

```powershell
formaltrust eair-seal-reportable-claim-bundle --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal --require-reviewed
```

Default sealing is still useful for deterministic template-chain diagnostics. `--require-reviewed` is the stricter final-packet gate.

This writes:

```text
reportable_claim_bundle_seal.json
reportable_claim_bundle_seal.md
```

The seal records the SHA256 of the claim manifest, claim audit, every cited artifact, and the claim-review status. It also records `seal_payload_sha256`, a compact digest for the sealed packet.

Verify the sealed packet later with:

```powershell
formaltrust eair-verify-reportable-claim-bundle-seal --seal outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal/verification
```

For paper-ready packet verification, also require reviewed status:

```powershell
formaltrust eair-verify-reportable-claim-bundle-seal --seal outputs/eair_warrant_reportable_export/bundle_seal/reportable_claim_bundle_seal.json --output-dir outputs/eair_warrant_reportable_export/bundle_seal/verification --require-reviewed
```

Default verification checks hash integrity. `--require-reviewed` checks both integrity and the reviewed seal status.

This writes:

```text
reportable_claim_bundle_seal_verification.json
reportable_claim_bundle_seal_verification.md
```

The verifier recomputes the seal payload hash, claim manifest hash, claim audit hash, and cited artifact hashes.

## Live Runbook Paper-Ready Claim Handoff

The generated live prompt-protocol runbook includes two claim chains.

The default diagnostic chain initializes and checks generated claim scaffolding:

```text
reportable_claim_template
reportable_claim_citation_audit
reportable_claim_bundle_seal
reportable_claim_bundle_seal_verification
```

The paper-ready chain writes to separate `paper_ready_*` directories and requires reviewed status:

```text
paper_ready_claim_review_declaration
paper_ready_claim_citation_audit --require-reviewed
paper_ready_claim_bundle_seal --require-reviewed
paper_ready_claim_bundle_seal_verification --require-reviewed
```

Use the diagnostic chain immediately after template generation. Then edit the generated claim text into paper-facing claims and record the review declaration:

```powershell
formaltrust eair-record-reportable-claim-review --claims outputs/eair_warrant_reportable_export/reportable_claims.json --claim-audit outputs/eair_warrant_reportable_export/claim_audit/reportable_claim_citation_audit.json --reviewer paper-author --review-note "Reviewed claim text and cited artifact values." --output outputs/eair_warrant_reportable_export/paper_ready_claims.json
```

This writes `paper_ready_claims.json` with `claim_generation="human_reviewed"`, `human_reviewed=true`, source claim/audit hashes, and reviewer metadata. The strict paper-ready audit and seal should use `paper_ready_claims.json`, not the unreviewed template manifest.

The review declaration refuses to promote starter text that still begins with `Template claim:`. A passing diagnostic citation audit proves that artifact values match; it does not prove that the claim text is paper-ready.

Verify the declaration provenance before strict paper-ready audit:

```powershell
formaltrust eair-verify-reportable-claim-review --claims outputs/eair_warrant_reportable_export/paper_ready_claims.json --output-dir outputs/eair_warrant_reportable_export/paper_ready_claim_review_verification
```

This writes:

```text
reportable_claim_review_verification.json
reportable_claim_review_verification.md
```

The verifier recomputes the source claim and source audit hashes recorded in `paper_ready_claims.json`. It catches post-review drift in the declaration inputs; it does not judge the quality of the human review.

The reviewed manifest also carries `review_manifest_payload_sha256`. The same verifier recomputes this self-seal and catches edits to `paper_ready_claims.json` after declaration.

The strict claim audit also enforces this self-seal when `--require-reviewed` is used. A paper-ready claim audit fails if the reviewed manifest payload hash is missing or mismatched.

## Claim Discipline

Use replay artifacts for safety claims. Use sampler logs only to document how transcripts were collected.

Do not report dry-run results as live model behavior. Do not report replay-only artifacts as evidence that a model was queried.

Do not cite sampler logs as safety evidence. Cite saved transcript JSONL, replay artifacts, verified manifests, and coverage-gated summaries.
