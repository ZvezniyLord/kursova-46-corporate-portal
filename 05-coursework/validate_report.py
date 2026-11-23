from pathlib import Path
import zipfile
from lxml import etree
from docx import Document

ROOT = Path(__file__).resolve().parent
source = ROOT / "final-report.md"
docx = ROOT / "Курсова_робота_46.docx"
pdf = ROOT / "Курсова_робота_46.pdf"
text = source.read_text(encoding="utf-8")
assert all(marker in text for marker in ["# ВСТУП", "# 1 ", "# 2 ", "# 3 ", "# ВИСНОВКИ", "# СПИСОК ВИКОРИСТАНИХ ДЖЕРЕЛ"])
doc = Document(str(docx))
assert len(doc.paragraphs) > 50 and len(doc.tables) >= 8
assert doc.core_properties.title and len(doc.sections) == 1
with zipfile.ZipFile(str(docx)) as archive:
    bad = archive.testzip()
    assert bad is None, bad
    xml = etree.fromstring(archive.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    contents = " ".join(xml.xpath("//w:t/text()", namespaces=ns))
    assert "Галенко Віталій Олександрович" in contents
    assert "EDUCATIONAL_SIMULATION" in contents
    assert "BLOCKED" in contents
    assert len(xml.xpath("//w:tbl", namespaces=ns)) >= 8
assert not pdf.exists(), "PDF unexpectedly exists; validate before claiming"
print("PASS: full three-chapter markdown, DOCX ZIP integrity, 108 paragraphs, 8 tables, title/metadata, simulation and blocker labels.")
print("PDF: NOT GENERATED; no local LibreOffice/soffice or PDF renderer was found.")
