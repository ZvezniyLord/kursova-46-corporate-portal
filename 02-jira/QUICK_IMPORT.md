# Quick Import Instructions — 02-jira (course46-jira)

**Status: PLANNED / EDUCATIONAL_SIMULATION / BLOCKED**  
Авторизований безкоштовний Jira Cloud **відсутній** (ACTIVE + SANCTIONED). Цей пакет — імпортуваний запропонований backlog, а не експорт наживого. Ніякі `jira_key`, URL, скриншоти, issue keys, дозволи облікового запису чи статуси доставки не створюються, не вигадуються та не твердити як виконане.

## 1. What this package contains

| Artifact | Content |
|---|---|
| `backlog-import-proposal.csv` | 29 rows: 4 Epics, 10 Stories, 10 Tasks, 5 Sub-tasks. Fixes за REQ/US/WBS + UAT + evidence + AC. |
| `agile-proposal.md` | Гібридний Sparсман (2-тижневі спринти S1–S8), MoSCoW, status workflow, quick snapshot. |
| `QUICK_IMPORT.md` (цей файл) | Послідовність імпорту для правильного Jira. |
| `BLOCKED_NO_AUTH.md` | Чесний блокер: немає доступу до Jira Cloud. |

## 2. Правильний склад CSV-стовпців на імпорт

`backlog-import-proposal.csv` має 17 колонок (`id`, `issue_type`, `summary`, `description`, `moscow`, `priority`, `story_points`, `status`, `requirement_id`, `story_id`, `wbs_id`, `epic`, `uat_case`, `prototype_screen`, `evidence_path`, `acceptance_criteria`, `assignee`).

При імпорті Jira має відповідати колонки і відображатися як:
- `id` → internal row key (local import id, not Jira key)
- `issue_type` → Epic / Story / Task / Sub-task
- `summary`, `description`, `acceptance_criteria`
- `priority` (High/Medium), `story_points` (optional), `status` (Proposed)
- `requirement_id`, `story_id`, `wbs_id`
- `epic` → Epic links (EPC-001..004)
- `uat_case`, `prototype_screen`, `evidence_path`
- `assignee` → `_` (unassigned until roles confirmed)

## 3. Import steps (if real free Jira access is later authorized)

1. Create a **Jira Cloud project (Software)**; note the project key (e.g., `PROJ`).
2. In Jira: **Projects → Import** → **CSV** → select `02-jira/backlog-import-proposal.csv`.
3. Map CSV columns to Jira: Epic / Story / Task / Sub-task, Summary, Description, Priority, Story Points, Status, Requirements, WBS, Epic links, UAT/evidence.
4. Map Epic links: `epic` (EPC-001..004) → Epic issue links.
5. Verify: each story row traces to `REQ-001..010` + `US-001..010` + `WBS-1.1..4.2`; no fabricated keys.
6. Run smoke checks: no PII, no claims about live access, status `PLANNED`.

## 4. What this package is NOT

- Не реальний Jira проєкт.
- Не дерево скриншотів.
- Не активні issue keys.
- Не фіксований графік/бюджет/витрати.

## 5. Readiness

Отже статус: `PLANNED / BLOCKED` — чесний блокер без доступу до Jira Cloud. Під час реального імпорту (обов'язково після авторизації користувача) суворо дотримуватися цього транспорту.

---

*Generation: O2 (course46-jira), 02-jira/. Status: PLANNED / EDUCATIONAL_SIMULATION / BLOCKED (no authorized free Jira Cloud).*
