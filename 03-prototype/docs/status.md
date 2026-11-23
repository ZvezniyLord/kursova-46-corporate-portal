# 03-prototype — статус артефактів та smoke-check

Статус **фактичний** після запуску:
- Smoke-check `docs/smoke-check.js` → `passed: 15/15`, `EXIT=0` (Node 24).
- Браузерна перевірка потоків (user/admin/guest) → **УРІШЕНО** (див. `docs/screenshots/`).
- Помилка `PortalApp.setRole` (інтерфейс не експортував `setRole`) — виправлено в `assets/js/app.js`.
- Немає `subagent`, live Jira, зовнішніх сервісів та платних бібліотек.
- Condition: `REAL` (підтверджено виконанням), `PLANNED` (немає доступу/юзер-приймання).

## 1. Артефакти прототипу (`03-prototype/`)

| Шлях | Статус | Примітка |
|---|---|---|
| `index.html` (макет входу) | `REAL` | UI-only mock login; demo-аккаунт `demo@firm.ua`; роль — селект |
| `dashboard.html` (панель) | `REAL` | Показує роль, привітання, оголошення, посилання |
| `announcements.html` (оголошення) | `REAL` | Фільтр категорій; адмін-форма додавання |
| `documents.html` (документи) | `REAL` | Пошук/фільтри/таблиця; адмін-форма додавання |
| `directory.html` (довідник) | `REAL` | Пошук/фільтр; адмін-форма додавання |
| `roles.html` (ролі/матриця) | `REAL` | RBAC-матриця + статус сеансу |
| `assets/js/demo-data.js` | `REAL` | Синтетичні дані: 10 співробітників, 10 оголошень, 14 документів, 4 ролі |
| `assets/js/app.js` | `REAL` | Мок-сесія + RBAC `can(role, perm)`; додано `setRole` |
| `assets/js/nav.js` | `REAL` | Навігація за `data-perm` |
| `assets/js/*.js` (сторінки) | `REAL` | Логіка кожного екрану з `requireAuth`/`requirePermission` |
| `assets/css/styles.css` | `REAL` | CSS (без build) |
| `README.md` | `REAL` | Точний запуск + обмеження + smoke check |
| `docs/smoke-check.js` | `REAL` | Node-скрипт (15/15) |
| `docs/traceability.csv` | `REAL` | Ідентифікатори REQ-001…008 + US-001…008 |
| `docs/proto-spec.md` | `REAL` | Скріншоти/потіки |
| `docs/access-matrix.md` | `REAL` | Суворіше описання для UAT |
| `docs/security-notes.md` | `REAL` | Чітке заборонення production auth/security (екран/README) |

## 2. Smoke-check (`docs/smoke-check.js`, Node 24.22.1)

`node docs/smoke-check.js` → `passed: 15/15`, `EXIT=0`.

- файли наявні;
- синтаксис JS OK (node --check);
- HTML посилається на CSS/JS;
- RBAC: guest 3 дозвілa, user 5, admin 11, superadmin 13;
- `searchDocuments('безпека',…)` → 3 docs; `searchEmployees` — без помилок.
- Браузерні потоки (user/admin/guest): інтерфейс, редирект, форма адміна — успішно.

## 3. Екрани успішно пройдені у браузері

- `login-page.png` — сторінка входу з підказкою про mock
- `dashboard-user.png` — панель привітання (роль `user`)
- `documents-user.png` — пошук `безпека` → 3 доки
- `roles-user.png` — матриця ролей (роль `user`)

## 4. Обмеження (honest, необхідно прочитати)

1. **Login/роль — мок.** `sessionStorage` + селект ролі; немає JWT/OAuth, серверної авторизації, списку облікових.
2. **Немає бекенду.** Усі стани — UI-імітація; дані синтетичні, зайві для прикладу.
3. **Немає production security.** Шифрування, CSRF, rate limiting, логування — відсутні.
4. **Екрани не зберігають стани на сервері** (окрім `sessionStorage` в браузері).
5. **UAT** може перевірити вигляд/навігацію/екрани, але **не** продуктивність, доступність, безпеку, масштабування.
6. UAT-прийняття (User Acceptance) потребує реального замовника та **НЕ зроблено**.
