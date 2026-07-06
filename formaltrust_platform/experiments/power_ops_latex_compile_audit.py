from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_TEX_PATH = "paper/power_ops_action_invariance/main.tex"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_latex_compile_audit_2026-07-02.json"
DEFAULT_TOOLS = ("latexmk", "pdflatex", "xelatex")


def build_latex_compile_audit(
    *,
    tex_path: str | Path = DEFAULT_TEX_PATH,
    tool_candidates: Sequence[str] = DEFAULT_TOOLS,
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    tex_target = Path(tex_path)
    tex_exists = tex_target.exists()
    pdf_path = tex_target.with_suffix(".pdf")
    selected_tool = _first_available_tool(tool_candidates)

    if not tex_exists:
        return _blocked_audit(
            tex_path=tex_target,
            pdf_path=pdf_path,
            status="blocked_missing_tex",
            blocker=f"TeX file does not exist: {tex_target}",
            tool_candidates=tool_candidates,
            selected_tool=selected_tool,
        )

    if not selected_tool:
        return _blocked_audit(
            tex_path=tex_target,
            pdf_path=pdf_path,
            status="blocked_missing_toolchain",
            blocker="No LaTeX toolchain found; checked " + ", ".join(tool_candidates),
            tool_candidates=tool_candidates,
            selected_tool="",
        )

    command = _compile_command(selected_tool, tex_target.name)
    completed = subprocess.run(
        command,
        cwd=tex_target.parent,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    pdf_exists = pdf_path.exists()
    blockers = []
    if completed.returncode != 0:
        blockers.append(f"LaTeX command exited with return code {completed.returncode}")
    if not pdf_exists:
        blockers.append(f"Expected PDF was not produced: {pdf_path}")

    return {
        "artifact_type": "power_ops_latex_compile_audit",
        "compile_status": "PASS" if not blockers else "FAIL",
        "passed": not blockers,
        "tex_path": str(tex_target),
        "tex_exists": tex_exists,
        "pdf_path": str(pdf_path),
        "pdf_exists": pdf_exists,
        "toolchain_available": True,
        "tool_candidates": list(tool_candidates),
        "selected_tool": selected_tool,
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": _tail(completed.stdout),
        "stderr_tail": _tail(completed.stderr),
        "blockers": blockers,
    }


def render_latex_compile_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops LaTeX Compile Audit",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Compile status | {audit.get('compile_status', 'FAIL')} |",
        f"| TeX exists | {bool(audit.get('tex_exists', False))} |",
        f"| Toolchain available | {bool(audit.get('toolchain_available', False))} |",
        f"| Selected tool | {audit.get('selected_tool', '')} |",
        f"| PDF exists | {bool(audit.get('pdf_exists', False))} |",
        "",
        "## Blockers",
        "",
    ]
    blockers = _list_value(audit.get("blockers"))
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    if audit.get("stdout_tail") or audit.get("stderr_tail"):
        lines.extend(
            [
                "",
                "## Command Output",
                "",
                "```text",
                str(audit.get("stdout_tail", "")),
                str(audit.get("stderr_tail", "")),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def write_latex_compile_audit(
    audit: Mapping[str, Any],
    *,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_latex_compile_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _blocked_audit(
    *,
    tex_path: Path,
    pdf_path: Path,
    status: str,
    blocker: str,
    tool_candidates: Sequence[str],
    selected_tool: str,
) -> dict[str, Any]:
    return {
        "artifact_type": "power_ops_latex_compile_audit",
        "compile_status": status,
        "passed": False,
        "tex_path": str(tex_path),
        "tex_exists": tex_path.exists(),
        "pdf_path": str(pdf_path),
        "pdf_exists": pdf_path.exists(),
        "toolchain_available": bool(selected_tool),
        "tool_candidates": list(tool_candidates),
        "selected_tool": selected_tool,
        "command": [],
        "returncode": None,
        "stdout_tail": "",
        "stderr_tail": "",
        "blockers": [blocker],
    }


def _first_available_tool(tool_candidates: Sequence[str]) -> str:
    for tool in tool_candidates:
        resolved = shutil.which(tool)
        if resolved:
            return tool
    return ""


def _compile_command(tool: str, tex_name: str) -> list[str]:
    if tool == "latexmk":
        return ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_name]
    return [tool, "-interaction=nonstopmode", "-halt-on-error", tex_name]


def _tail(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[-max_chars:]


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile or audit the power-ops LaTeX manuscript.")
    parser.add_argument("--tex-path", default=DEFAULT_TEX_PATH)
    parser.add_argument("--tool", action="append", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    audit = build_latex_compile_audit(
        tex_path=args.tex_path,
        tool_candidates=tuple(args.tool) if args.tool else DEFAULT_TOOLS,
        timeout_seconds=args.timeout_seconds,
    )
    write_latex_compile_audit(audit, markdown_path=args.out_md, json_path=args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
