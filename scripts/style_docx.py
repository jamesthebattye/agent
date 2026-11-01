#!/usr/bin/env python3
"""Polish a pandoc-generated .docx: bordered tables with a shaded header row, smaller code font.
Usage: python3 scripts/style_docx.py file.docx"""
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HEADER_FILL = "1F2A44"; BORDER = "C9D0D4"; ZEBRA = "F3F6F6"

def set_borders(tbl):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), BORDER)
        b.append(e)
    for old in tblPr.findall(qn("w:tblBorders")): tblPr.remove(old)
    tblPr.append(b)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
    tcPr.append(s)

def main(path):
    d = Document(path)
    for name in ("Verbatim Char", "Source Code"):
        try:
            st = d.styles[name]; st.font.size = Pt(9); st.font.color.rgb = RGBColor(0x1F, 0x6F, 0x6B)
        except KeyError:
            pass
    for t in d.tables:
        set_borders(t)
        for r_i, row in enumerate(t.rows):
            for cell in row.cells:
                if r_i == 0:
                    shade(cell, HEADER_FILL)
                elif r_i % 2 == 0:
                    shade(cell, ZEBRA)
                for para in cell.paragraphs:
                    para.paragraph_format.space_after = Pt(2)
                    for run in para.runs:
                        run.font.size = Pt(9.5)
                        if r_i == 0:
                            run.font.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    d.save(path)
    print(path)

if __name__ == "__main__":
    main(sys.argv[1])
