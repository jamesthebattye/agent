#!/usr/bin/env python3
"""Spreadsheet helpers for the WORKTECH sales agent.

Subcommands
-----------
lead-sheet  JSON rows -> formatted lead sheet .xlsx (optionally with history columns)
outbox      Folder of draft .md files -> outbox.xlsx summary
table       JSON {"headers": [...], "rows": [[...], ...]} -> .xlsx
read        .xlsx or .csv -> JSON rows on stdout (so Claude can read spreadsheets)

Examples
--------
python3 scripts/xlsx_tools.py lead-sheet --in output/2026-11-01/leads.json \
    --out output/2026-11-01/lead-sheet-new-york-2027.xlsx
python3 scripts/xlsx_tools.py lead-sheet --history --in rows.json --out reengage.xlsx
python3 scripts/xlsx_tools.py outbox --dir output/2026-11-01/outbox
python3 scripts/xlsx_tools.py read --in knowledge/past-sponsors.xlsx
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# ---------------------------------------------------------------- columns
# (JSON key, column header, width)
LEAD_COLUMNS = [
    ("company", "Company", 26),
    ("website", "Website", 26),
    ("hq_region", "HQ / Region", 20),
    ("employees", "Size (employees)", 12),
    ("segment", "Segment", 22),
    ("fit_score", "Fit score (1-5)", 10),
    ("fit_reason", "Fit reason", 44),
    ("contact_score", "Contact score (1-5)", 10),
    ("priority", "Priority (A/B/C)", 10),
    ("contact_name", "Contact name", 22),
    ("title", "Title", 30),
    ("function", "Function (BD/Marketing)", 14),
    ("email", "Email", 30),
    ("email_status", "Email status", 12),
    ("linkedin", "LinkedIn", 34),
    ("source", "Source", 22),
    ("suggested_event", "Suggested event", 22),
    ("suggested_tier", "Suggested tier", 14),
    ("suggested_angle", "Suggested angle", 44),
    ("apollo_org_id", "Apollo org ID", 16),
    ("apollo_person_id", "Apollo person ID", 16),
    ("apollo_owner", "Apollo owner (⚑ = colleague)", 22),
    ("status", "Status", 14),
    ("notes", "Notes", 34),
]

HISTORY_COLUMNS = [
    ("past_events", "Past events sponsored", 28),
    ("past_years", "Past years", 12),
    ("past_tier", "Past tier", 12),
    ("past_contact", "Past contact (from our records)", 24),
    ("past_contact_status", "Past contact still there? (Yes/Left/Unknown)", 16),
    ("past_outcome", "Past outcome", 18),
    ("history_notes", "History notes", 34),
]

PAST_SPONSOR_COLUMNS = [
    ("company", "Company", 26),
    ("website", "Website", 26),
    ("events_sponsored", "Events sponsored", 30),
    ("year", "Year", 8),
    ("tier", "Tier", 12),
    ("contact_name", "Contact name", 22),
    ("contact_title", "Contact title", 26),
    ("contact_email", "Contact email", 28),
    ("notes", "Notes", 40),
    ("outcome", "Outcome", 18),
]

OUTBOX_COLUMNS = [
    ("contact", "Contact", 22),
    ("title", "Title", 26),
    ("company", "Company", 22),
    ("function", "Function", 12),
    ("email", "Email", 28),
    ("event", "Event", 22),
    ("subject", "Subject", 30),
    ("body", "Body (first touch)", 70),
    ("follow_up_1", "Follow-up 1", 60),
    ("follow_up_2", "Follow-up 2", 60),
    ("owner_flag", "Owner flag", 18),
    ("critic_score", "Critic score", 10),
    ("status", "Status", 12),
    ("file", "Draft file", 30),
]

TIERS = ["Bronze", "Silver", "Gold", "Gold Plus", "Platinum"]

HEADER_FILL = PatternFill("solid", fgColor="1F2A44")
HEADER_FONT = Font(bold=True, color="FFFFFF")
HISTORY_FILL = PatternFill("solid", fgColor="5B3A7A")


# ---------------------------------------------------------------- helpers
def _write_sheet(ws, columns, rows, history_from=None):
    for i, (_, header, width) in enumerate(columns, start=1):
        c = ws.cell(row=1, column=i, value=header)
        c.font = HEADER_FONT
        c.fill = HISTORY_FILL if history_from and i >= history_from else HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 32
    for r, row in enumerate(rows, start=2):
        for i, (key, _, _) in enumerate(columns, start=1):
            val = row.get(key, "")
            if isinstance(val, (list, tuple)):
                val = "; ".join(str(v) for v in val)
            cell = ws.cell(row=r, column=i, value=val)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "B2"
    if columns:
        ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}{max(1, len(rows) + 1)}"


def _add_validations(ws, columns, n_rows):
    keys = [k for k, _, _ in columns]
    last = max(n_rows + 1, 500)

    def col(key):
        return get_column_letter(keys.index(key) + 1)

    if "suggested_tier" in keys:
        dv = DataValidation(type="list", formula1='"' + ",".join(TIERS) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col('suggested_tier')}2:{col('suggested_tier')}{last}")
    if "function" in keys:
        dv = DataValidation(type="list", formula1='"BD,Marketing"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col('function')}2:{col('function')}{last}")
    if "fit_score" in keys:
        dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col('fit_score')}2:{col('fit_score')}{last}")
    if "past_contact_status" in keys:
        dv = DataValidation(type="list", formula1='"Yes,Left,Unknown"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col('past_contact_status')}2:{col('past_contact_status')}{last}")


def write_lead_sheet(rows, out, history=False):
    columns = LEAD_COLUMNS + (HISTORY_COLUMNS if history else [])
    wb = Workbook()
    ws = wb.active
    ws.title = "Leads"
    _write_sheet(ws, columns, rows, history_from=len(LEAD_COLUMNS) + 1 if history else None)
    _add_validations(ws, columns, len(rows))
    guide = wb.create_sheet("Column guide")
    guide.append(["Column", "JSON key", "What goes here"])
    for k, h, _ in columns:
        guide.append([h, k, COLUMN_HELP.get(k, "")])
    for c in guide[1]:
        c.font = HEADER_FONT
        c.fill = HEADER_FILL
    guide.column_dimensions["A"].width = 30
    guide.column_dimensions["B"].width = 20
    guide.column_dimensions["C"].width = 90
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


COLUMN_HELP = {
    "company": "Company name as in Apollo.",
    "website": "Primary domain.",
    "hq_region": "HQ city/country, plus the presence relevant to the event if different.",
    "employees": "Apollo estimated headcount.",
    "segment": "ICP segment (e.g. Workplace tech, AV & collaboration, Office furniture).",
    "fit_score": "1-5 event fit (see CLAUDE.md scoring rubric).",
    "fit_reason": "One line: why this company fits this event. Must be grounded in Apollo/web data.",
    "contact_score": "1-5 contact rating (see morning-brief SKILL.md rubric): function, seniority, regional match, reachability, ownership.",
    "priority": "A / B / C, from company fit x contact score. A = work today.",
    "contact_name": "Full name.",
    "title": "Current title per Apollo.",
    "function": "BD or Marketing.",
    "email": "Only filled after James approves enrichment. Blank = not yet revealed.",
    "email_status": "Apollo email status (verified / guessed / unavailable).",
    "linkedin": "LinkedIn URL from Apollo.",
    "source": "Where the row came from, e.g. 'Apollo company search 2026-11-01'.",
    "suggested_event": "WORKTECH event + year.",
    "suggested_tier": "Bronze / Silver / Gold / Gold Plus / Platinum - a starting suggestion only.",
    "suggested_angle": "One-line outreach angle for this contact (BD vs Marketing angle).",
    "apollo_org_id": "Apollo organisation ID (for later enrichment / sequences).",
    "apollo_person_id": "Apollo person ID.",
    "apollo_owner": "Apollo owner of the account/contact. '⚑ Kirsty Darlington' etc. = colleague-owned: included, but check with them before outreach. Blank = unowned or James.",
    "status": "shortlisted / approved / enriched / drafted / contacted / replied / not now.",
    "notes": "Free text.",
    "past_events": "WORKTECH events this company sponsored (from knowledge/past-sponsors).",
    "past_years": "Years sponsored.",
    "past_tier": "Tier(s) bought.",
    "past_contact": "Who we dealt with last time.",
    "past_contact_status": "Yes = still at company per Apollo; Left = no longer there; Unknown.",
    "past_outcome": "Outcome recorded in past-sponsors (renewed / lapsed / etc.).",
    "history_notes": "Anything relevant from the history file.",
}


def write_table(headers, rows, out, title="Table"):
    wb = Workbook()
    ws = wb.active
    ws.title = (re.sub(r"[\[\]\*\?/\\:]", "", title) or "Table")[:31]
    cols = [(f"c{i}", h, max(12, min(60, len(str(h)) + 6))) for i, h in enumerate(headers)]
    dict_rows = [{f"c{i}": v for i, v in enumerate(r)} for r in rows]
    _write_sheet(ws, cols, dict_rows)
    for i, _ in enumerate(headers, start=1):
        longest = max([len(str(r[i - 1])) for r in rows if len(r) >= i] + [len(str(headers[i - 1]))])
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(70, longest + 2))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


# ---------------------------------------------------------------- outbox
FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
SECTION_RE = re.compile(r"^##\s+(.+)$", re.M)


def parse_draft(text):
    meta = {}
    m = FRONT_RE.match(text)
    body = text
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        body = text[m.end():]
    sections = {}
    parts = SECTION_RE.split(body)
    # parts = [pre, title1, content1, title2, content2, ...]
    for i in range(1, len(parts) - 1, 2):
        sections[parts[i].strip()] = parts[i + 1].strip()
    emails = []
    for title, content in sections.items():
        t = title.lower()
        if t.startswith("email 1") or t.startswith("follow-up"):
            subj = ""
            sm = re.search(r"^\*\*Subject:\*\*\s*(.+)$", content, re.M)
            if sm:
                subj = sm.group(1).strip()
                content = content[sm.end():].strip()
            emails.append({"title": title, "subject": subj, "body": content})
    return meta, emails


def build_outbox(folder, out=None):
    folder = Path(folder)
    rows = []
    for f in sorted(folder.glob("*.md")):
        if f.name.lower() in ("readme.md",):
            continue
        meta, emails = parse_draft(f.read_text(encoding="utf-8"))
        first = next((e for e in emails if e["title"].lower().startswith("email 1")), {"subject": "", "body": ""})
        fups = [e for e in emails if e["title"].lower().startswith("follow-up")]
        rows.append({
            "contact": meta.get("contact", ""),
            "title": meta.get("title", ""),
            "company": meta.get("company", ""),
            "function": meta.get("function", ""),
            "email": meta.get("email", ""),
            "event": meta.get("event", ""),
            "subject": first["subject"],
            "body": first["body"],
            "follow_up_1": (fups[0]["body"] if len(fups) > 0 else ""),
            "follow_up_2": (fups[1]["body"] if len(fups) > 1 else ""),
            "owner_flag": meta.get("owner_flag", ""),
            "critic_score": meta.get("critic_score", ""),
            "status": meta.get("status", "draft"),
            "file": f.name,
        })
    out = out or str(folder / "outbox.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Outbox"
    _write_sheet(ws, OUTBOX_COLUMNS, rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out, len(rows)


# ---------------------------------------------------------------- read
def read_any(path):
    p = Path(path)
    if p.suffix.lower() == ".csv":
        with p.open(newline="", encoding="utf-8-sig") as fh:
            return list(csv.DictReader(fh))
    wb = load_workbook(p, data_only=True, read_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        headers = [str(h) if h is not None else f"col{i}" for i, h in enumerate(rows[0])]
        recs = []
        for r in rows[1:]:
            if all(v in (None, "") for v in r):
                continue
            recs.append({headers[i]: ("" if v is None else v) for i, v in enumerate(r) if i < len(headers)})
        out[ws.title] = recs
    return out


# ---------------------------------------------------------------- cli
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("lead-sheet")
    a.add_argument("--in", dest="inp", required=True, help="JSON file: list of row objects")
    a.add_argument("--out", required=True)
    a.add_argument("--history", action="store_true", help="add re-engagement history columns")

    b = sub.add_parser("outbox")
    b.add_argument("--dir", required=True)
    b.add_argument("--out")

    c = sub.add_parser("table")
    c.add_argument("--in", dest="inp", required=True, help='JSON {"title":..,"headers":[..],"rows":[[..]]}')
    c.add_argument("--out", required=True)

    d = sub.add_parser("read")
    d.add_argument("--in", dest="inp", required=True)

    args = ap.parse_args(argv)
    if args.cmd == "lead-sheet":
        rows = json.loads(Path(args.inp).read_text(encoding="utf-8"))
        print(write_lead_sheet(rows, args.out, history=args.history))
    elif args.cmd == "outbox":
        out, n = build_outbox(args.dir, args.out)
        print(f"{out} ({n} drafts)")
    elif args.cmd == "table":
        spec = json.loads(Path(args.inp).read_text(encoding="utf-8"))
        print(write_table(spec["headers"], spec["rows"], args.out, spec.get("title", "Table")))
    elif args.cmd == "read":
        json.dump(read_any(args.inp), sys.stdout, indent=2, default=str, ensure_ascii=False)
        print()


if __name__ == "__main__":
    main()
