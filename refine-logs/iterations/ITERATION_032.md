# ITERATION_032: Artifact Verifier and README

Date: 2026-06-20

## Hypothesis

An artifact manifest is useful only if it can be verified. EAIR-Bench should provide both machine verification and a human-readable artifact protocol.

## Design Change

Added verifier:

```text
verify_replay_artifact_manifest
```

Added CLI:

```text
formaltrust eair-verify-artifact --manifest artifact_manifest.json
python -m formaltrust_platform eair-verify-artifact --manifest artifact_manifest.json
```

The verifier checks:

- manifest artifact type;
- transcript file existence;
- transcript SHA256;
- result artifact existence;
- report artifact existence;
- manifest summary matches result JSON.

Added human-readable artifact protocol:

```text
docs/eair_artifact_readme.md
```

## Tests

Added TDD tests:

- `test_eair_artifact_verifier_checks_manifest_hash`
- `test_eair_artifact_readme_documents_sampling_replay_and_verification`

Observed failures before implementation:

- CLI reported `No such command 'eair-verify-artifact'`.
- `docs/eair_artifact_readme.md` did not exist.

## Verification

Ran:

```text
python -m formaltrust_platform eair-verify-artifact --manifest outputs/eair_replay_cli_pilot/artifact_manifest.json
```

Output:

```text
Artifact verified: outputs\eair_replay_cli_pilot\artifact_manifest.json
```

## Supported Claim

EAIR-Bench artifacts can now be independently verified from the command line: transcript hash, result/report presence, and summary consistency are checked.

## Claim Boundary

Verification proves artifact consistency, not model behavior. Live-model claims still require saved transcripts from real provider calls.

## Next Iteration

Add a small artifact summary table generator that collects manifest summaries across runs, so paper result tables can be assembled from manifests rather than manual copying.
