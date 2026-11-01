#!/usr/bin/env python3
"""(Re)build the blank spreadsheet templates.

  templates/lead-sheet.xlsx                 - lead sheet (Leads + Re-engagement sheets, column guide)
  knowledge/past-sponsors.template.xlsx     - fill this in and save as knowledge/past-sponsors.xlsx
  knowledge/past-sponsors.template.csv      - same, as CSV

Usage: python3 scripts/build_templates.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from openpyxl import load_workbook  # noqa: E402
from xlsx_tools import (HISTORY_COLUMNS, LEAD_COLUMNS, PAST_SPONSOR_COLUMNS,  # noqa: E402
                        _add_validations, _write_sheet, write_lead_sheet, Workbook)

EXAMPLE_PAST = {
    "company": "Example Ltd (delete this row)", "website": "example.com",
    "events_sponsored": "WORKTECH London; WORKTECH New York", "year": 2026, "tier": "Gold",
    "contact_name": "Jane Example", "contact_title": "Head of Field Marketing",
    "contact_email": "jane@example.com", "notes": "Took a speaking slot; wanted more HR audience",
    "outcome": "Renewed / Lapsed / Upgraded / Downgraded",
}

# lead sheet: Leads sheet + Re-engagement sheet
out = ROOT / "templates" / "lead-sheet.xlsx"
write_lead_sheet([], out)
wb = load_workbook(out)
ws = wb.create_sheet("Re-engagement", 1)
cols = LEAD_COLUMNS + HISTORY_COLUMNS
_write_sheet(ws, cols, [], history_from=len(LEAD_COLUMNS) + 1)
_add_validations(ws, cols, 0)
wb.save(out)
print(out)

# past sponsors
out = ROOT / "knowledge" / "past-sponsors.template.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "Past sponsors"
_write_sheet(ws, PAST_SPONSOR_COLUMNS, [EXAMPLE_PAST])
wb.save(out)
print(out)

out = ROOT / "knowledge" / "past-sponsors.template.csv"
with out.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow([h for _, h, _ in PAST_SPONSOR_COLUMNS])
    w.writerow([EXAMPLE_PAST[k] for k, _, _ in PAST_SPONSOR_COLUMNS])
print(out)
