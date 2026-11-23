# BLOCKED — why there is no corporate-portal.mpp

## Контент
Цей каталог — імпортний пакет для Microsoft Project. Він створено з узгоджених CSV
(`01-project-plan/`) і готовий до відкриття у MS Project:

- `import_package/project_schedule.xml` — Project XML (MS Project 2010+ format, namespace
  `http://schemas.microsoft.com/project`), 24 задач, 8 ресурсів, Baseline, EVM.
- `import_package/instructions_import_msproject.md` — інструкція імпорту/збереження.
- `gantt.png` — узгоджений діаграма Ганта (навчальний екземпляр).

## Чому нативного .mpp немає
1. На цій машині не встановлено ліцензованої **Microsoft Project** (Project.exe/Office-Component
   з Project відсутній); перевірка `command -v proj / devenv` та перегляд каталогу
   `Program Files\Microsoft Office\Office16` виявили відсутність.
2. Без ліцензії неможливо створити **перевірений справжній** `.mpp` (календар, ресурси,
   Baseline, моніторинг з фактами).
3. Тому `.mpp` позначено **BLOCKED**, і цей XML/.csv **НІКОЛІ НЕ перейменовано в `.mpp`**.
   Викладаний XML/JSON — це імпортний пакет, а не підміна нативного файлу.

## Що потрібно зробити, щоб отримати справжній .mpp
- Отримати/встановити ліцензований Microsoft Project (послуга, ліцензійний ключ, робочий
  оточення). Після встановлення: File > Open > Import > XML → налаштувати календар,
  Baseline, PV/EV/AC та зберегти як `01-project-plan/corporate-portal.mpp`.
- Після встановлення — перевірка відкриття, скріншоти ключових подань та звіт перевірки
  надсилаються як виправлення цього блоку. Ніякого платного шляху, ніяких фальшивих файлів.

## Перевірка цього пакета
- `python3 build/make_project_xml.py` → `import_package/project_schedule.xml`
- `python3 -c "import xml.etree.ElementTree as ET; t=ET.parse('import_package/project_schedule.xml'); root=t.getroot(); print(len(root.find('{http://schemas.microsoft.com/project}Tasks').findall('Task')))` → 24
- `python3 -c "import csv; print(len(list(csv.DictReader(open('01-project-plan/tasks.csv')))))"` → 24
