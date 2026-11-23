from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "final-report.md"
OUT = ROOT / "Курсова_робота_46.docx"
text = SRC.read_text(encoding="utf-8")
doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2)
sec.bottom_margin = Cm(2)
sec.left_margin = Cm(3)
sec.right_margin = Cm(1.5)
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(14)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.first_line_indent = Cm(1.25)
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(0)
for name, size in [("Title", 16), ("Heading 1", 14), ("Heading 2", 14), ("Heading 3", 14)]:
    style = doc.styles[name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.paragraph_format.first_line_indent = Cm(0)
    style.paragraph_format.space_before = Pt(12)
    style.paragraph_format.space_after = Pt(6)
header = sec.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.CENTER
header.add_run("Курсова робота №46 · Управління ІТ-проєктами").font.size = Pt(9)
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
footer._p.append(fld)

def inline(paragraph, value):
    for part in re.split(r"(\*\*.*?\*\*|`[^`]+`)", value):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(10)
        else:
            paragraph.add_run(part)

def parse_table(table_lines):
    rows = []
    for line in table_lines:
        if re.match(r"^\s*\|?\s*:?-{3,}", line):
            continue
        rows.append([value.strip() for value in line.strip().strip("|").split("|")])
    if not rows:
        return
    count = max(map(len, rows))
    table = doc.add_table(rows=0, cols=count)
    table.style = "Table Grid"
    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for column, cell in enumerate(cells):
            cell.text = ""
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_after = Pt(0)
            inline(paragraph, row[column] if column < len(row) else "")
            for run in paragraph.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9)
                run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Times New Roman")
            if row_index == 0:
                shading = OxmlElement("w:shd")
                shading.set(qn("w:fill"), "D9EAF7")
                cell._tc.get_or_add_tcPr().append(shading)
                for run in paragraph.runs:
                    run.bold = True
    doc.add_paragraph()

lines = text.splitlines()
index = 0
first_title = True
while index < len(lines):
    value = lines[index].strip()
    if not value:
        index += 1
        continue
    if value.startswith("|"):
        block = []
        while index < len(lines) and lines[index].strip().startswith("|"):
            block.append(lines[index])
            index += 1
        parse_table(block)
        continue
    if value.startswith("```"):
        index += 1
        code = []
        while index < len(lines) and not lines[index].strip().startswith("```"):
            code.append(lines[index])
            index += 1
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.first_line_indent = Cm(0)
        run = paragraph.add_run("\n".join(code))
        run.font.name = "Consolas"
        run.font.size = Pt(9)
        index += 1
        continue
    if value.startswith("# "):
        title = value[2:].strip()
        if first_title:
            paragraph = doc.add_paragraph(style="Title")
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            inline(paragraph, title)
            first_title = False
        else:
            doc.add_page_break()
            paragraph = doc.add_paragraph(style="Heading 1")
            inline(paragraph, title)
        index += 1
        continue
    if value.startswith("## "):
        paragraph = doc.add_paragraph(style="Heading 2")
        inline(paragraph, value[3:])
        index += 1
        continue
    if value.startswith("### "):
        paragraph = doc.add_paragraph(style="Heading 3")
        inline(paragraph, value[4:])
        index += 1
        continue
    if value.startswith("> "):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.left_indent = Cm(0.6)
        paragraph.paragraph_format.first_line_indent = Cm(0)
        inline(paragraph, value[2:])
        index += 1
        continue
    if re.match(r"^[-*]\s", value):
        paragraph = doc.add_paragraph(style="List Bullet")
        paragraph.paragraph_format.left_indent = Cm(1.25)
        paragraph.paragraph_format.first_line_indent = Cm(-0.6)
        inline(paragraph, re.sub(r"^[-*]\s+", "", value))
        index += 1
        continue
    if re.match(r"^\d+\.\s", value):
        paragraph = doc.add_paragraph(style="List Number")
        paragraph.paragraph_format.left_indent = Cm(1.25)
        paragraph.paragraph_format.first_line_indent = Cm(-0.6)
        inline(paragraph, re.sub(r"^\d+\.\s+", "", value))
        index += 1
        continue
    paragraph = doc.add_paragraph()
    inline(paragraph, value)
    index += 1

doc.core_properties.title = "Курсова робота №46 — Управління ІТ-проєктом корпоративного порталу"
doc.core_properties.subject = "Навчальний робочий проєкт; моделювання явно позначено"
doc.core_properties.author = "Галенко Віталій Олександрович"
doc.save(str(OUT))
print(OUT)
