from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


def build_claim_ledger_readiness(
    *,
    claim_ledger_path: str | Path,
    readiness_path: str | Path,
) -> dict[str, Any]:
    claim_ledger = _load_json(claim_ledger_path)
    readiness = _load_json(readiness_path)
    readiness_passed = bool(readiness.get("passed", False))
    readiness_status = str(readiness.get("status", "PASS" if readiness_passed else "FAIL"))
    readiness_blockers = [
        str(item)
        for item in _list_value(readiness.get("blockers"))
        if str(item)
    ]

    supported_claims = [
        _supported_claim_row(
            claim,
            readiness_passed=readiness_passed,
            readiness_status=readiness_status,
            readiness_blockers=readiness_blockers,
        )
        for claim in _list_value(claim_ledger.get("supported_claims"))
        if isinstance(claim, Mapping)
    ]
    forbidden_claims = [
        {
            "claim": str(claim),
            "paper_ready": False,
            "reason": "forbidden_claim",
        }
        for claim in _list_value(claim_ledger.get("forbidden_claims"))
        if str(claim)
    ]
    paper_ready_supported = sum(1 for claim in supported_claims if claim["paper_ready"])

    return {
        "artifact_type": "power_ops_claim_ledger_readiness",
        "claim_ledger": str(claim_ledger_path),
        "readiness": str(readiness_path),
        "readiness_status": readiness_status,
        "readiness_passed": readiness_passed,
        "readiness_blockers": readiness_blockers,
        "supported_claim_count": len(supported_claims),
        "paper_ready_supported_claim_count": paper_ready_supported,
        "blocked_supported_claim_count": len(supported_claims) - paper_ready_supported,
        "forbidden_claim_count": len(forbidden_claims),
        "supported_claims": supported_claims,
        "forbidden_claims": forbidden_claims,
    }


def render_claim_ledger_readiness_markdown(sync: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Claim Ledger Readiness",
        "",
        f"**Readiness status:** {sync.get('readiness_status', 'FAIL')}",
        f"**Supported claims:** {int(sync.get('supported_claim_count', 0))}",
        f"**Paper-ready supported claims:** {int(sync.get('paper_ready_supported_claim_count', 0))}",
        f"**Blocked supported claims:** {int(sync.get('blocked_supported_claim_count', 0))}",
        "",
        "## Readiness Blockers",
        "",
    ]
    blockers = _list_value(sync.get("readiness_blockers"))
    if blockers:
        for blocker in blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Supported Claims",
            "",
            "| Claim | Level | Paper ready | Evidence |",
            "|---|---|---:|---|",
        ]
    )
    for claim in _list_value(sync.get("supported_claims")):
        if not isinstance(claim, Mapping):
            continue
        evidence = "; ".join(f"`{item}`" for item in _list_value(claim.get("evidence")))
        lines.append(
            "| {claim} | {level} | {ready} | {evidence} |".format(
                claim=_escape_table_text(str(claim.get("claim", ""))),
                level=_escape_table_text(str(claim.get("level", ""))),
                ready="yes" if claim.get("paper_ready") else "no",
                evidence=_escape_table_text(evidence),
            )
        )

    lines.extend(
        [
            "",
            "## Forbidden Claims",
            "",
            "| Claim | Paper ready | Reason |",
            "|---|---:|---|",
        ]
    )
    for claim in _list_value(sync.get("forbidden_claims")):
        if not isinstance(claim, Mapping):
            continue
        lines.append(
            "| {claim} | {ready} | {reason} |".format(
                claim=_escape_table_text(str(claim.get("claim", ""))),
                ready="yes" if claim.get("paper_ready") else "no",
                reason=_escape_table_text(str(claim.get("reason", ""))),
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_claim_ledger_readiness(
    sync: Mapping[str, Any],
    *,
    markdown_path: str | Path,
    json_path: str | Path | None = None,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_claim_ledger_readiness_markdown(sync), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(sync, ensure_ascii=False, indent=2), encoding="utf-8")


def _supported_claim_row(
    claim: Mapping[str, Any],
    *,
    readiness_passed: bool,
    readiness_status: str,
    readiness_blockers: list[str],
) -> dict[str, Any]:
    return {
        "claim": str(claim.get("claim", "")),
        "level": str(claim.get("level", "")),
        "evidence": [str(item) for item in _list_value(claim.get("evidence")) if str(item)],
        "paper_ready": readiness_passed,
        "readiness_status": readiness_status,
        "blocking_reasons": [] if readiness_passed else readiness_blockers,
    }


def _load_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Attach paper-claim readiness status to the power-ops claim ledger."
    )
    parser.add_argument(
        "--claim-ledger",
        default="docs/power_ops_action_invariance_claim_ledger_2026-07-02.json",
    )
    parser.add_argument(
        "--readiness",
        default="docs/power_ops_action_invariance_paper_claim_readiness_2026-07-02.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.md",
    )
    parser.add_argument(
        "--out-json",
        default="docs/power_ops_action_invariance_claim_ledger_readiness_2026-07-02.json",
    )
    args = parser.parse_args(argv)

    sync = build_claim_ledger_readiness(
        claim_ledger_path=args.claim_ledger,
        readiness_path=args.readiness,
    )
    write_claim_ledger_readiness(sync, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
