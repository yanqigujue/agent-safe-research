from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from formaltrust_platform.config import load_config
from formaltrust_platform.experiments.eair_bench import (
    audit_prompt_protocol_adherence,
    audit_reportable_claim_citations,
    audit_reportable_eair_run,
    audit_reportable_eair_export,
    check_live_sampling_config,
    export_protocol_legitimacy_table,
    doctor_live_run_config,
    export_reportable_eair_results,
    live_workflow_status,
    record_reportable_claim_review,
    run_openai_compatible_sampling_config,
    run_structured_action_transcript_replay,
    seal_reportable_claim_bundle,
    summarize_replay_artifact_manifests,
    verify_replay_artifact_manifest,
    verify_reportable_claim_review_declaration,
    verify_reportable_claim_bundle_seal,
    write_live_runbook,
    write_reportable_claim_template,
)
from formaltrust_platform.interfaces import NodeConfigError
from formaltrust_platform.runner import ExperimentRunner

app = typer.Typer(help="FormalTrust modular validation platform CLI.")


@app.callback()
def main() -> None:
    """Run modular LLM trustworthiness validation experiments."""


@app.command("run")
def run_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to experiment YAML config."),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Override output run directory."),
) -> None:
    experiment_config = load_config(config)
    if output_dir is not None:
        experiment_config = experiment_config.with_output_dir(output_dir)

    try:
        result = ExperimentRunner().run(experiment_config)
    except NodeConfigError as exc:
        # A node's config violates its declared interface — surface it cleanly
        # instead of as a traceback.
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Run directory: {result.run_dir}")
    typer.echo(f"Report: {result.report_path}")


@app.command("eair-sample")
def eair_sample_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to EAIR sampler YAML config."),
) -> None:
    try:
        result = run_openai_compatible_sampling_config(config)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise configuration/runtime errors
        typer.echo(f"EAIR sampler error: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Transcripts: {result['output_path']}")
    replay_report = result.get("replay_report_path")
    if replay_report:
        typer.echo(f"Replay report: {replay_report}")
    summary_report = result.get("summary_report_path")
    if summary_report:
        typer.echo(f"Summary report: {summary_report}")


@app.command("eair-check-live-config")
def eair_check_live_config_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to live EAIR sampler YAML config."),
) -> None:
    try:
        result = check_live_sampling_config(config)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise configuration errors
        typer.echo(f"EAIR live config check failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    if not result["ready"]:
        typer.echo("Live config readiness failed:", err=True)
        for error in result["errors"]:
            typer.echo(f"- {error}", err=True)
        raise typer.Exit(code=2)

    typer.echo(f"Live config ready: {result['config_path']}")
    typer.echo(f"model: {result['model']}")
    typer.echo(f"api_key_env: {result['api_key_env']}")
    typer.echo(f"expected_conditions: {len(result['expected_conditions'])}")
    typer.echo(f"scenario_count: {result['scenario_count']}")
    typer.echo(f"prompt_variants: {result['prompt_variant_count']}")
    typer.echo(f"planned_transcripts: {result['planned_transcript_count']}")
    if result["warnings"]:
        typer.echo(f"warnings: {result['warnings']}")
    typer.echo(f"coverage gate command: {result['coverage_gate_command']}")


@app.command("eair-doctor-live-run")
def eair_doctor_live_run_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to live EAIR sampler YAML config."),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for live-run doctor JSON/Markdown."),
) -> None:
    try:
        result = doctor_live_run_config(config, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise doctor failures
        typer.echo(f"EAIR live run doctor failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    if not result["ready"]:
        typer.echo("Live run doctor failed:", err=True)
        for error in result["errors"]:
            typer.echo(f"- {error}", err=True)
        typer.echo(f"Live run doctor report: {output_dir / 'live_run_doctor.md'}", err=True)
        raise typer.Exit(code=2)

    typer.echo(f"Live run doctor passed: {output_dir / 'live_run_doctor.md'}")


@app.command("eair-live-workflow-status")
def eair_live_workflow_status_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to live EAIR sampler YAML config."),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for live workflow status JSON/Markdown."),
) -> None:
    try:
        result = live_workflow_status(config, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise status failures
        typer.echo(f"EAIR live workflow status failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    if result["overall_status"] != "complete":
        typer.echo(f"Live workflow blocked: {result['blocked_stage']}", err=True)
        typer.echo(f"Live workflow status: {output_dir / 'live_workflow_status.md'}", err=True)
        raise typer.Exit(code=2)

    typer.echo(f"Live workflow complete: {output_dir / 'live_workflow_status.md'}")


@app.command("eair-write-live-runbook")
def eair_write_live_runbook_command(
    config: Path = typer.Option(..., "--config", "-c", help="Path to live EAIR sampler YAML config."),
    output: Path = typer.Option(..., "--output", "-o", help="Path for generated Markdown runbook."),
) -> None:
    try:
        result = write_live_runbook(config, output)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise configuration/write errors
        typer.echo(f"EAIR live runbook failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Live runbook: {result['runbook_path']}")
    typer.echo(f"Live runbook JSON: {result['runbook_json_path']}")


@app.command("eair-audit-reportable-run")
def eair_audit_reportable_run_command(
    manifest: list[Path] = typer.Option(
        ...,
        "--manifest",
        "-m",
        help="Repeatable path to a replay artifact_manifest.json.",
    ),
    summary: Path = typer.Option(..., "--summary", "-s", help="Path to artifact_summary.json."),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Optional directory for reportable_run_audit JSON/Markdown.",
    ),
) -> None:
    try:
        result = audit_reportable_eair_run(manifest, summary_path=summary, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise audit failures
        typer.echo(f"EAIR reportable run audit failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable run audit passed: {result['summary_path']}")
    typer.echo(f"models: {', '.join(result['models'])}")
    typer.echo(f"transcripts: {result['transcript_count']}")
    if output_dir is not None:
        typer.echo(f"Reportable run audit: {output_dir / 'reportable_run_audit.md'}")


@app.command("eair-export-reportable-results")
def eair_export_reportable_results_command(
    summary: Path = typer.Option(..., "--summary", "-s", help="Path to artifact_summary.json."),
    audit: Path = typer.Option(..., "--audit", "-a", help="Path to reportable_run_audit.json."),
    protocol_legitimacy: Optional[Path] = typer.Option(
        None,
        "--protocol-legitimacy",
        help="Optional protocol_legitimacy_table.json to include in reportable paper outputs.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for reportable paper-table outputs."),
) -> None:
    try:
        export_reportable_eair_results(
            summary_path=summary,
            audit_path=audit,
            protocol_legitimacy_path=protocol_legitimacy,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise export failures
        typer.echo(f"EAIR reportable results export failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable results export: {output_dir / 'reportable_model_condition_table.md'}")


@app.command("eair-audit-reportable-export")
def eair_audit_reportable_export_command(
    export: Path = typer.Option(..., "--export", "-e", help="Path to reportable_results_export.json."),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Optional directory for reportable export integrity audit JSON/Markdown.",
    ),
) -> None:
    try:
        result = audit_reportable_eair_export(export_path=export, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise integrity audit failures
        typer.echo(f"EAIR reportable export integrity audit failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable export integrity audit passed: {result['export_path']}")
    if output_dir is not None:
        typer.echo(f"Reportable export integrity audit: {output_dir / 'reportable_export_integrity_audit.md'}")


@app.command("eair-audit-reportable-claims")
def eair_audit_reportable_claims_command(
    claims: Path = typer.Option(..., "--claims", "-c", help="Path to reportable_claims.json."),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Optional directory for reportable claim citation audit JSON/Markdown.",
    ),
    require_reviewed: bool = typer.Option(
        False,
        "--require-reviewed",
        help="Require a human-reviewed claim manifest.",
    ),
) -> None:
    try:
        result = audit_reportable_claim_citations(
            claims_path=claims,
            output_dir=output_dir,
            require_reviewed=require_reviewed,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise claim-audit failures
        typer.echo(f"EAIR reportable claim citation audit failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable claim citation audit passed: {result['claims_path']}")
    typer.echo(f"claims: {result['passed_claim_count']}/{result['claim_count']}")
    if output_dir is not None:
        typer.echo(f"Reportable claim citation audit: {output_dir / 'reportable_claim_citation_audit.md'}")


@app.command("eair-write-reportable-claim-template")
def eair_write_reportable_claim_template_command(
    export: Path = typer.Option(..., "--export", "-e", help="Path to reportable_results_export.json."),
    integrity_audit: Path = typer.Option(
        ...,
        "--integrity-audit",
        "-i",
        help="Path to reportable_export_integrity_audit.json.",
    ),
    output: Path = typer.Option(..., "--output", "-o", help="Path to write reportable_claims.json."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing reportable_claims.json."),
) -> None:
    try:
        result = write_reportable_claim_template(
            export_path=export,
            integrity_audit_path=integrity_audit,
            output_path=output,
            force=force,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise template failures
        typer.echo(f"EAIR reportable claim template failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable claim template: {output}")
    typer.echo(f"claims: {len(result['claims'])}")


@app.command("eair-record-reportable-claim-review")
def eair_record_reportable_claim_review_command(
    claims: Path = typer.Option(..., "--claims", "-c", help="Path to source reportable_claims.json."),
    claim_audit: Path = typer.Option(
        ...,
        "--claim-audit",
        "-a",
        help="Path to a passing reportable_claim_citation_audit.json.",
    ),
    reviewer: str = typer.Option(..., "--reviewer", help="Reviewer identifier or role."),
    review_note: str = typer.Option(..., "--review-note", help="Short human review declaration."),
    reviewed_at_utc: Optional[str] = typer.Option(
        None,
        "--reviewed-at-utc",
        help="Optional UTC review timestamp. Defaults to current UTC time.",
    ),
    output: Path = typer.Option(..., "--output", "-o", help="Path to write paper_ready_claims.json."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing reviewed claims output."),
) -> None:
    try:
        result = record_reportable_claim_review(
            claims_path=claims,
            claim_audit_path=claim_audit,
            output_path=output,
            reviewer=reviewer,
            review_note=review_note,
            reviewed_at_utc=reviewed_at_utc,
            force=force,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise review declaration failures
        typer.echo(f"EAIR reportable claim review declaration failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reviewed reportable claims: {output}")
    typer.echo(f"review_status: {result['review_status']}")
    typer.echo(f"reviewer: {result['reviewer']}")


@app.command("eair-verify-reportable-claim-review")
def eair_verify_reportable_claim_review_command(
    claims: Path = typer.Option(..., "--claims", "-c", help="Path to paper_ready_claims.json."),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Optional directory for claim review verification JSON/Markdown.",
    ),
) -> None:
    try:
        result = verify_reportable_claim_review_declaration(
            claims_path=claims,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise review verification failures
        typer.echo(f"EAIR reportable claim review verification failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable claim review verified: {result['claims_path']}")
    if output_dir is not None:
        typer.echo(f"Reportable claim review verification: {output_dir / 'reportable_claim_review_verification.md'}")


@app.command("eair-seal-reportable-claim-bundle")
def eair_seal_reportable_claim_bundle_command(
    claims: Path = typer.Option(..., "--claims", "-c", help="Path to reportable_claims.json."),
    claim_audit: Path = typer.Option(
        ...,
        "--claim-audit",
        "-a",
        help="Path to reportable_claim_citation_audit.json.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for claim bundle seal JSON/Markdown."),
    require_reviewed: bool = typer.Option(
        False,
        "--require-reviewed",
        help="Require a reviewed claim audit before sealing.",
    ),
) -> None:
    try:
        result = seal_reportable_claim_bundle(
            claims_path=claims,
            claim_audit_path=claim_audit,
            output_dir=output_dir,
            require_reviewed=require_reviewed,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise seal failures
        typer.echo(f"EAIR reportable claim bundle seal failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable claim bundle sealed: {output_dir / 'reportable_claim_bundle_seal.json'}")
    typer.echo(f"seal_payload_sha256: {result['seal_payload_sha256']}")


@app.command("eair-verify-reportable-claim-bundle-seal")
def eair_verify_reportable_claim_bundle_seal_command(
    seal: Path = typer.Option(..., "--seal", "-s", help="Path to reportable_claim_bundle_seal.json."),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Optional directory for claim bundle seal verification JSON/Markdown.",
    ),
    require_reviewed: bool = typer.Option(
        False,
        "--require-reviewed",
        help="Require a paper-ready reviewed claim bundle seal.",
    ),
) -> None:
    try:
        result = verify_reportable_claim_bundle_seal(
            seal_path=seal,
            output_dir=output_dir,
            require_reviewed=require_reviewed,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise seal verification failures
        typer.echo(f"EAIR reportable claim bundle seal verification failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Reportable claim bundle seal verified: {result['seal_path']}")
    if output_dir is not None:
        typer.echo(f"Reportable claim bundle seal verification: {output_dir / 'reportable_claim_bundle_seal_verification.md'}")


@app.command("eair-replay")
def eair_replay_command(
    transcripts: Path = typer.Option(..., "--transcripts", "-t", help="Path to transcript JSONL/JSON."),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for replay artifacts."),
) -> None:
    try:
        summary = run_structured_action_transcript_replay(transcripts, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise configuration/runtime errors
        typer.echo(f"EAIR replay error: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Replay report: {output_dir / 'structured_action_transcript_replay_report.md'}")
    typer.echo(f"Transcripts evaluated: {summary['total_transcripts']}")


@app.command("eair-verify-artifact")
def eair_verify_artifact_command(
    manifest: Path = typer.Option(..., "--manifest", "-m", help="Path to replay artifact_manifest.json."),
) -> None:
    try:
        result = verify_replay_artifact_manifest(manifest)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise verification failures
        typer.echo(f"EAIR artifact verification failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Artifact verified: {result['manifest_path']}")


@app.command("eair-summarize-artifacts")
def eair_summarize_artifacts_command(
    manifest: list[Path] = typer.Option(
        ...,
        "--manifest",
        "-m",
        help="Repeatable path to a replay artifact_manifest.json.",
    ),
    expected_condition: Optional[list[str]] = typer.Option(
        None,
        "--expected-condition",
        help="Repeatable expected case_id::condition coverage key.",
    ),
    require_complete_coverage: bool = typer.Option(
        False,
        "--require-complete-coverage",
        help="Exit with an error if any model is missing expected conditions.",
    ),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for summary JSON/CSV/Markdown."),
) -> None:
    try:
        summarize_replay_artifact_manifests(
            manifest,
            output_dir=output_dir,
            expected_conditions=expected_condition,
            require_complete_coverage=require_complete_coverage,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise verification/aggregation failures
        typer.echo(f"EAIR artifact summary failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Artifact summary: {output_dir / 'artifact_summary.md'}")


@app.command("eair-audit-prompt-adherence")
def eair_audit_prompt_adherence_command(
    transcripts: Path = typer.Option(..., "--transcripts", "-t", help="Path to transcript JSONL/JSON."),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for prompt-adherence audit outputs."),
) -> None:
    try:
        result = audit_prompt_protocol_adherence(transcripts, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI should show concise audit failures
        typer.echo(f"EAIR prompt adherence audit failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Prompt adherence audit: {output_dir / 'prompt_adherence_audit.md'}")
    typer.echo(f"transcripts: {result['total_transcripts']}")
    typer.echo(f"compliance_rate: {result['compliance_rate']:.4f}")


@app.command("eair-export-protocol-legitimacy-table")
def eair_export_protocol_legitimacy_table_command(
    adherence: Path = typer.Option(..., "--adherence", "-a", help="Path to prompt_adherence_audit.json."),
    summary: Path = typer.Option(..., "--summary", "-s", help="Path to artifact_summary.json."),
    output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Directory for protocol-legitimacy outputs."),
) -> None:
    try:
        result = export_protocol_legitimacy_table(
            adherence_path=adherence,
            summary_path=summary,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should show concise export failures
        typer.echo(f"EAIR protocol legitimacy export failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Protocol legitimacy table: {output_dir / 'protocol_legitimacy_table.md'}")
    typer.echo(f"rows: {result['total_rows']}")
