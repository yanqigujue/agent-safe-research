from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_SCAFFOLD = "docs/power_ops_action_invariance_citation_scaffold_2026-07-02.json"
DEFAULT_BIB_PATH = "paper/power_ops_action_invariance/references_checked.bib"
DEFAULT_OUT_MD = "docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.md"
DEFAULT_OUT_JSON = "docs/power_ops_action_invariance_citation_metadata_audit_2026-07-02.json"
ATOM = "{http://www.w3.org/2005/Atom}"


def build_citation_metadata_audit(
    *,
    scaffold_path: str | Path = DEFAULT_SCAFFOLD,
    metadata_records: Sequence[Mapping[str, Any]] = (),
    fetch_arxiv: bool = False,
) -> dict[str, Any]:
    scaffold = _load_json(scaffold_path)
    entries = [
        entry
        for entry in _list_value(scaffold.get("entries"))
        if isinstance(entry, Mapping)
    ]
    records = {str(record.get("key", "")): dict(record) for record in metadata_records if record.get("key")}
    fetch_errors: list[str] = []
    if fetch_arxiv:
        fetched, fetch_errors = _fetch_arxiv_records(entries)
        for key, record in fetched.items():
            records.setdefault(key, record)

    audit_rows = [_audit_entry(entry, records.get(str(entry.get("key", "")))) for entry in entries]
    confirmed_rows = [row for row in audit_rows if row["metadata_status"] == "confirmed"]
    rejected_rows = [row for row in audit_rows if row["metadata_status"].startswith("rejected")]
    pending_rows = [row for row in audit_rows if row["metadata_status"].startswith("pending")]
    checked_bibtex_text = _render_checked_bibtex(confirmed_rows)
    if len(confirmed_rows) == len(entries) and entries:
        status = "PASS"
    elif confirmed_rows:
        status = "partial"
    else:
        status = "blocked_no_confirmed_entries"

    return {
        "artifact_type": "power_ops_citation_metadata_audit",
        "scaffold_path": str(scaffold_path),
        "audit_status": status,
        "entry_count": len(entries),
        "metadata_record_count": len(records),
        "confirmed_entry_count": len(confirmed_rows),
        "pending_entry_count": len(pending_rows),
        "rejected_entry_count": len(rejected_rows),
        "invented_reference_count": 0,
        "fetch_arxiv": fetch_arxiv,
        "fetch_errors": fetch_errors,
        "audit_rows": audit_rows,
        "checked_bibtex_text": checked_bibtex_text,
    }


def render_citation_metadata_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Power-Ops Citation Metadata Audit",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | {audit.get('audit_status', '')} |",
        f"| Entries | {int(audit.get('entry_count', 0) or 0)} |",
        f"| Confirmed | {int(audit.get('confirmed_entry_count', 0) or 0)} |",
        f"| Pending | {int(audit.get('pending_entry_count', 0) or 0)} |",
        f"| Rejected | {int(audit.get('rejected_entry_count', 0) or 0)} |",
        f"| Invented references | {int(audit.get('invented_reference_count', 0) or 0)} |",
        "",
        "## Rows",
        "",
        "| Key | Status | Title match | Authors | Year |",
        "|---|---|---:|---:|---|",
    ]
    for row in _list_value(audit.get("audit_rows")):
        if not isinstance(row, Mapping):
            continue
        lines.append(
            "| {key} | {status} | {title} | {authors} | {year} |".format(
                key=_escape_table_text(str(row.get("key", ""))),
                status=_escape_table_text(str(row.get("metadata_status", ""))),
                title=bool(row.get("title_matches", False)),
                authors=len(_list_value(row.get("authors"))),
                year=_escape_table_text(str(row.get("year", ""))),
            )
        )
    fetch_errors = _list_value(audit.get("fetch_errors"))
    if fetch_errors:
        lines.extend(["", "## Fetch Errors", ""])
        lines.extend(f"- {error}" for error in fetch_errors)
    lines.append("")
    return "\n".join(lines)


def load_citation_metadata_records(paths: Sequence[str | Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        payload = _load_json(path)
        raw_records = payload.get("records", [])
        for record in _list_value(raw_records):
            if isinstance(record, Mapping):
                records.append(dict(record))
    return records


def write_citation_metadata_audit(
    audit: Mapping[str, Any],
    *,
    bib_path: str | Path = DEFAULT_BIB_PATH,
    markdown_path: str | Path = DEFAULT_OUT_MD,
    json_path: str | Path | None = DEFAULT_OUT_JSON,
) -> None:
    bib_target = Path(bib_path)
    bib_target.parent.mkdir(parents=True, exist_ok=True)
    bib_target.write_text(str(audit.get("checked_bibtex_text", "")), encoding="utf-8")

    markdown_target = Path(markdown_path)
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_citation_metadata_audit_markdown(audit), encoding="utf-8")
    if json_path is not None:
        json_target = Path(json_path)
        json_target.parent.mkdir(parents=True, exist_ok=True)
        json_target.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")


def _audit_entry(entry: Mapping[str, Any], record: Mapping[str, Any] | None) -> dict[str, Any]:
    key = str(entry.get("key", ""))
    if not record:
        return {
            "key": key,
            "scaffold_title": str(entry.get("title", "")),
            "metadata_status": "pending_no_metadata",
            "title_matches": False,
            "authors": [],
            "year": "",
            "source": "",
            "url": str(entry.get("url", "")),
            "eprint": "",
        }

    authors = _string_values(record.get("authors"))
    year = str(record.get("year", ""))
    title_matches = _title_matches(str(entry.get("title", "")), str(record.get("title", "")))
    if not title_matches:
        status = "rejected_title_mismatch"
    elif not authors or not year:
        status = "rejected_incomplete_metadata"
    else:
        status = "confirmed"
    return {
        "key": key,
        "scaffold_title": str(entry.get("title", "")),
        "metadata_title": str(record.get("title", "")),
        "metadata_status": status,
        "title_matches": title_matches,
        "authors": authors,
        "year": year,
        "source": str(record.get("source", "")),
        "url": str(record.get("url", entry.get("url", ""))),
        "eprint": str(record.get("eprint", "")),
        "source_refs": _string_values(record.get("source_refs")),
    }


def _fetch_arxiv_records(entries: Sequence[Mapping[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    records: dict[str, dict[str, Any]] = {}
    errors = []
    for entry in entries:
        key = str(entry.get("key", ""))
        arxiv_id = _arxiv_id_from_url(str(entry.get("url", "")))
        if not arxiv_id:
            continue
        try:
            records[key] = _fetch_one_arxiv_record(key, arxiv_id, str(entry.get("url", "")))
        except Exception as exc:  # pragma: no cover - network/environment dependent
            errors.append(f"{key}: {exc}")
    return records, errors


def _fetch_one_arxiv_record(key: str, arxiv_id: str, source_url: str) -> dict[str, Any]:
    try:
        return _fetch_one_arxiv_atom_record(key, arxiv_id, source_url)
    except Exception:
        return _fetch_one_arxiv_bibtex_record(key, arxiv_id, source_url)


def _fetch_one_arxiv_atom_record(key: str, arxiv_id: str, source_url: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"id_list": arxiv_id})
    url = f"https://export.arxiv.org/api/query?{query}"
    with urllib.request.urlopen(url, timeout=20) as response:  # nosec - fixed metadata endpoint
        payload = response.read()
    root = ET.fromstring(payload)
    entry = root.find(f"{ATOM}entry")
    if entry is None:
        raise ValueError(f"arXiv metadata not found for {arxiv_id}")
    title = " ".join((entry.findtext(f"{ATOM}title") or "").split())
    authors = [
        " ".join((author.findtext(f"{ATOM}name") or "").split())
        for author in entry.findall(f"{ATOM}author")
        if author.findtext(f"{ATOM}name")
    ]
    published = entry.findtext(f"{ATOM}published") or ""
    return {
        "key": key,
        "title": title,
        "authors": authors,
        "year": published[:4],
        "source": "arxiv",
        "url": source_url,
        "eprint": arxiv_id,
    }


def _fetch_one_arxiv_bibtex_record(key: str, arxiv_id: str, source_url: str) -> dict[str, Any]:
    url = f"https://arxiv.org/bibtex/{arxiv_id}"
    with urllib.request.urlopen(url, timeout=20) as response:  # nosec - fixed metadata endpoint
        bibtex_text = response.read().decode("utf-8", errors="replace")
    fields = _parse_bibtex_fields(bibtex_text)
    authors = [
        author.strip()
        for author in str(fields.get("author", "")).split(" and ")
        if author.strip()
    ]
    return {
        "key": key,
        "title": str(fields.get("title", "")),
        "authors": authors,
        "year": str(fields.get("year", "")),
        "source": "arxiv_bibtex",
        "url": source_url,
        "eprint": str(fields.get("eprint", arxiv_id)),
    }


def _parse_bibtex_fields(bibtex_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in re.finditer(r"(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", bibtex_text):
        key = match.group(1).strip()
        value = match.group(2).strip()
        fields[key] = value
    return fields


def _arxiv_id_from_url(url: str) -> str:
    match = re.search(r"arxiv\.org/(?:abs|html)/([^?#]+)", url)
    if not match:
        return ""
    arxiv_id = match.group(1).strip("/")
    return re.sub(r"v\d+$", "", arxiv_id)


def _title_matches(scaffold_title: str, metadata_title: str) -> bool:
    scaffold_norm = _normalize_title(scaffold_title)
    metadata_norm = _normalize_title(metadata_title)
    if not scaffold_norm or not metadata_norm:
        return False
    aliases = [_normalize_title(part) for part in re.split(r"\s*/\s*", scaffold_title) if part.strip()]
    candidates = [scaffold_norm, *aliases]
    return any(candidate == metadata_norm or candidate in metadata_norm or metadata_norm in candidate for candidate in candidates)


def _normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def _render_checked_bibtex(rows: Sequence[Mapping[str, Any]]) -> str:
    blocks = []
    for row in rows:
        lines = [
            f"@misc{{{row['key']},",
            f"  title = {{{{{_bibtex_escape(str(row.get('metadata_title') or row.get('scaffold_title', '')))}}}}},",
            f"  author = {{{' and '.join(_bibtex_escape(author) for author in _string_values(row.get('authors')))}}},",
            f"  year = {{{_bibtex_escape(str(row.get('year', '')))}}},",
        ]
        if row.get("eprint"):
            lines.extend(
                [
                    f"  eprint = {{{_bibtex_escape(str(row.get('eprint', '')))}}},",
                    "  archivePrefix = {arXiv},",
                ]
            )
        lines.append(f"  url = {{{_bibtex_escape(str(row.get('url', '')))}}}")
        lines.append("}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def _bibtex_escape(value: str) -> str:
    return value.replace("\\", "\\textbackslash{}").replace("{", "\\{").replace("}", "\\}")


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


def _string_values(value: Any) -> list[str]:
    return [item for item in _list_value(value) if isinstance(item, str) and item]


def _escape_table_text(value: str) -> str:
    return value.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit citation scaffold metadata and emit checked BibTeX for confirmed entries."
    )
    parser.add_argument("--scaffold", default=DEFAULT_SCAFFOLD)
    parser.add_argument("--fetch-arxiv", action="store_true")
    parser.add_argument("--metadata-json", action="append", default=[])
    parser.add_argument("--bib-path", default=DEFAULT_BIB_PATH)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    parser.add_argument("--out-json", default=DEFAULT_OUT_JSON)
    args = parser.parse_args(argv)

    metadata_records = load_citation_metadata_records(args.metadata_json)
    audit = build_citation_metadata_audit(
        scaffold_path=args.scaffold,
        metadata_records=metadata_records,
        fetch_arxiv=args.fetch_arxiv,
    )
    write_citation_metadata_audit(
        audit,
        bib_path=args.bib_path,
        markdown_path=args.out_md,
        json_path=args.out_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
