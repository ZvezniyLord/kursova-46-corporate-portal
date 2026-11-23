from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "requirements_matrix.docx"
doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2)
sec.bottom_margin = Cm(2)
sec.left_margin = Cm(2)
sec.right_margin = Cm(2)
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(11)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.first_line_indent = Cm(0)
normal.paragraph_format.line_spacing = 1.15

title = doc.add_heading("Відповідність структури курсової вимогам Moodle", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("Перевірено за docs/structure-and-requirements.md та контрактом курсової в репозиторії. Матриця фіксує виконання структури документа, але не замінює відсутні практичні докази Microsoft Project, Jira або приймання.")

rows = [
("Вступ: актуальність, мета, завдання, результати й практична цінність", "Частково", "Є актуальність, мета, завдання, очікуваний результат. Додати окремі формулювання практичної цінності та методів."),
("1.1 Концепція, бізнес-потреба, SMART, Charter, обмеження й критерії успіху", "Частково", "Концепцію й межі описано як навчальне припущення. Немає повного SMART з числовими метриками, обумовленими замовником; статут не затверджено."),
("1.2 Stakeholder register / Power–Interest / вимоги / User Stories / AC", "Частково", "Є рольова stakeholder таблиця та приклади вимог/AC. Додати окремі User Stories і матрицю Power–Interest; усі дані лишаються гіпотетичними."),
("1.3 Waterfall/Scrum/Kanban/Hybrid, lifecycle, backlog, team, RACI, communications", "Частково", "Є порівняльне обґрунтування, RACI і канали. Треба імпортувати узгоджений backlog, чітко відрізняючи пропозицію від Jira."),
("2.1 Scope statement, WBS/packages, milestones, dependencies, durations, MS Project/Gantt", "Частково", "Є scope, WBS із 24 задачами, залежностями, календарем і Gantt у синтетичному наборі. Project XML — лише імпортна основа; справжнього перевіреного .mpp немає."),
("2.2 Ресурси, ставки, assignments, workload/overload, трудомісткість, бюджет, optimization, baseline", "Частково / BLOCKED", "Є ролі/ставки і навчальний BAC/Baseline. Нативний MS Project недоступний; перевантаження/вирівнювання ресурсів не перевірені. Дані не є підприємницькими фактами."),
("2.3 Реальний Jira project/board, Epic/Story/Task/Sub-task, priorities/statuses/Sprint/team", "BLOCKED_NO_AUTH", "Є готовий імпортний CSV/backlog і план Scrum; немає підтвердженого Jira Cloud проєкту, issue keys, board або фактичних Sprint-метрик."),
("3.1 Risk Register, probability-impact matrix, response owners, quality/DoD, Change Request impact", "Частково", "Є ризики й реакції, DoD/зміни. Треба додати явну Probability–Impact матрицю та повний приклад CR з таблицею впливу."),
("3.2 Модель виконання, план-факт, ресурсні відхилення, CPI/SPI, Jira reports/status report", "Частково / EDUCATIONAL_SIMULATION", "Є відтворювані навчальні PV/EV/AC, CPI/SPI і відхилення. Жодного реального факту підприємства немає; Jira reports відсутні."),
("3.3 Причини, коригувальні рішення, досягнення цілей, приймання, closure, lessons learned", "Частково", "Є рекомендації і Lessons Learned. Формальне приймання і closure не виконані, замовник/підпис відсутні."),
("Достовірні джерела й академічне цитування", "Частково", "Є вихідна бібліографія. Повні видання й точні цитати не верифіковано в цій записці; звірити і оформити за актуальними вимогами кафедри."),
("Обов’язкові нативний MPP, Jira evidence, повний UAT", "НЕ ВИКОНАНО", "MPP і live Jira не підтверджені; smoke 15/15 не є UAT; сценарії UAT-001…010 лишаються NOT_RUN/BLOCKED, формальне UAT — NOT_PERFORMED."),
]

table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
for i, label in enumerate(["Вимога Moodle", "Стан", "Фактична примітка / залишок"]):
    cell = table.rows[0].cells[i]
    cell.text = label
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "D9EAF7")
    tcpr.append(shd)
    for run in cell.paragraphs[0].runs:
        run.bold = True
for row in rows:
    cells = table.add_row().cells
    for j, value in enumerate(row):
        cells[j].text = value
        for p in cells[j].paragraphs:
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9)
                r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Times New Roman")

doc.add_heading("Критичні кроки перед поданням", level=1)
for item in [
    "Уточнити титульні дані та отримати погодження теми/структури у викладача.",
    "Якщо доступно, створити і перевідкрити нативний .mpp з календарем, ресурсами, бюджетом, Baseline і моніторингом; не називати XML імпортом завершений MPP.",
    "Авторизувати безкоштовний Jira Cloud лише за рішенням власника; якщо неможливо — лишити чесний BLOCKED_NO_AUTH і CSV як пропозицію.",
    "Звірити статуси UAT; провести тільки реально доступні тести, формальне приймання — лише з уповноваженим користувачем.",
    "Перевірити повний список джерел і вимоги до обсягу/оформлення у Moodle перед експортом фінальної редакції.",
]:
    doc.add_paragraph(item, style="List Number")

doc.core_properties.title = "Матриця перевірки вимог Moodle — курсова №46"
doc.core_properties.subject = "Внутрішня перевірка повноти за наявною структурою"
doc.core_properties.author = "Курсова робота №46"
doc.save(str(OUT))
print(OUT)
