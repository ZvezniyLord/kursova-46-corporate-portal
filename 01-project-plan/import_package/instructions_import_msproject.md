# Інструкція імпорту та збереження: Project XML → Microsoft Project

Цей пакет є **блокуванням (BLOCKED)** для створення справжнього `.mpp`.
Причина: на цій машині **немає ліцензованої версії Microsoft Project** (Project.exe /
деплоймент Office з компонентом Project не встановлено). Без ліцензії неможливо
створити перевірений нативний `.mpp`; замість `corporate-portal.mpp` тут надано
**сумісний проміжний Project XML** та інструкцію, якою можна скористатися одразу після
одержання ліцензії.

## Що у пакеті
- `project_schedule.xml` — вивід Project XML у форматі MS Project (2010+), створений із узгоджених CSV.
- `tasks.csv`, `resources.csv`, `wbs.csv`, `baseline.csv`, `calendar.csv` — оригінальні джерела (уже у `01-project-plan/`).
- `gantt.png` — узгоджений діаграма Ганта (навчальний екземпляр).
- `formulas.md`, `reconciliation.csv`, `evm-snapshot.csv` — формули, реконціляція та EVM-знімок 2026-11-06.

## Як імпортувати у MS Project після отримання ліцензії
1. У MS Project: **File > Open** → вибрати `01-project-plan/import_package/project_schedule.xml`.
2. **File > Options > Calendar** → переконатися, що календар "Standard" (пн–пт, 09:00–17:00, початок 2026-09-07).
3. **Project > Properties** → перевірити базові параметри (дати початку/закінчення, валюту USD).
4. **Project > Baseline > Set Baseline** → зберегти Baseline 0 з готової колонки `baseline_cost_usd`.
5. **Project > Gantt Chart > Format > Bar Styles** → увімкнути колонки факту/EV/AC (PV, EV, AC, CV, SV, SPI, CPI).
6. Указати фактичні значення (PV/EV/AC, CPI/SPI) тільки як умовні **симуляційні** (див. `evm-snapshot.csv`, дата стану 2026-11-06).
7. Зберегти як `01-project-plan/corporate-portal.mpp` лише після отримання ліцензії.

## Термінологія
- `PV` — Planned Value; `EV` — Earned Value; `AC` — Actual Cost;
  `CPI = EV/AC`; `SPI = EV/PV`; `BAC = 32 264 USD`; `EAC = 32 636.88 USD`;
  `VAC = −372.88 USD`; `ETC = 6 518.88 USD`.
- Усі цифри — умовні навчальні припущення (EDUCATIONAL_SIMULATION), не факти підприємства.

## Блокер (honest BLOCKED)
Нативний `corporate-portal.mpp` (справжній) **не створено** — немає ліцензованого
Microsoft Project на машині. Ніяк не називайте цей XML/.csv `corporate-portal.mpp`;
цей файл — лише імпортний пакет для майбутнього відкриття у MS Project.
