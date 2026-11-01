#!/usr/bin/env python3
"""Convert a Markdown document to Word (.docx) and export every table to its own .xlsx.

House rule (CLAUDE.md): documents are always .docx, and every table in a document
also gets a separate Excel file containing that table.

Usage
-----
python3 scripts/md_to_docx.py output/2026-11-01/research-acme.md
  -> output/2026-11-01/research-acme.docx
  -> output/2026-11-01/research-acme-table-1-<heading>.xlsx  (one per table)

Options
-------
--reference templates/reference.docx   Word styles to use (optional; used automatically if present)
--no-tables                            skip the .xlsx table export
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_tools import write_table  # noqa: E402

SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def _cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)]
    # strip simple markdown emphasis / links for the spreadsheet
    clean = []
    for c in cells:
        c = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", c)
        c = re.sub(r"(\*\*|__)(.*?)\1", r"\2", c)
        c = c.replace("\\|", "|")
        clean.append(c)
    return clean


def extract_tables(md_text):
    lines = md_text.splitlines()
    tables, heading, i = [], "Table", 0
    while i < len(lines):
        line = lines[i]
        h = re.match(r"^#{1,6}\s+(.*)", line)
        if h:
            heading = h.group(1).strip()
        if "|" in line and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]):
            headers = _cells(line)
            rows = []
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                rows.append(_cells(lines[j]))
                j += 1
            tables.append({"title": heading, "headers": headers, "rows": rows})
            i = j
            continue
        i += 1
    return tables


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "table"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown")
    ap.add_argument("--out", help="output .docx path (default: alongside the .md)")
    ap.add_argument("--reference", help="reference .docx for styles")
    ap.add_argument("--no-tables", action="store_true")
    a = ap.parse_args(argv)

    src = Path(a.markdown)
    out = Path(a.out) if a.out else src.with_suffix(".docx")
    ref = a.reference or (Path(__file__).resolve().parent.parent / "templates" / "reference.docx")
    cmd = ["pandoc", str(src), "-f", "gfm", "-t", "docx", "-o", str(out)]
    if ref and Path(ref).exists():
        cmd += ["--reference-doc", str(ref)]
    subprocess.run(cmd, check=True)
    print(out)

    if not a.no_tables:
        for n, t in enumerate(extract_tables(src.read_text(encoding="utf-8")), start=1):
            x = out.with_name(f"{out.stem}-table-{n}-{slug(t['title'])}.xlsx")
            write_table(t["headers"], t["rows"], x, t["title"])
            print(x)


if __name__ == "__main__":
    main()
