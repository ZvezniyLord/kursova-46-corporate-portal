# spec 03-prototype (proto-spec)

## Screens & flows (shared IDs, mapped to `docs/traceability.csv`)

| ID | Screen | File | Entrance | Access rule (demo) |
|---|---|---|---|---|
| SCR-001 | Вхід | `index.html` | direct | demo login (role selector) |
| SCR-002 | Панель привітання | `dashboard.html` | login | `view_dashboard` |
| SCR-003 | Оголошення | `announcements.html` | login | `view_announcements` |
| SCR-004 | Документи | `documents.html` | login | `view_documents` |
| SCR-005 | Довідник | `directory.html` | login | `view_directory` |
| SCR-006 | Ролі та матриця | `roles.html` | login | `manage_roles` (живих елементів показ) |

## Flows (demo)

1. `SCR-001 → SCR-002`: впевнитися в демо-акаунті → вибрати роль → `sessionStorage`
   записується `portal_demo_role` → редірект.
2. `SCR-002 → SCR-003/004/005/006`: sidebar nav показує тільки розпізнавані елементи
   (на основі `PortalApp.can(role, perm)`).
3. `SCR-003 → (admin)`: форма "додати оголошення" збереження в локальному `window`
   (UI-only).
4. `SCR-004 → (admin)`: форма "додати документ", вибір категорії/відділу/власника.
5. `SCR-005 → (admin)`: форма "додати співробітника".
6. `SCR-006`: читання матриці, статус сеансу, інструменти керування залежно від ролі.

## UAT cases (prototype level)

- UAT-001: login mock (demo account + role) → `SCR-002` shows role; `sessionStorage` set.
- UAT-002: guest role → redirect to `SCR-001`; `SCR-002..006` not accessible.
- UAT-003: `user` role → `SCR-002..005` accessible; `SCR-006` matrix shown (no edit).
- UAT-004: `admin` role → edit forms on `SCR-003..005`; `SCR-006` manages.
- UAT-005: search documents (`documents.html`) returns matching docs.
- UAT-006: filter announcements by category (`announcements.html`).
- UAT-007: `role.js` matrix matches `PortalApp.can` semantics.
- UAT-008: `node docs/smoke-check.js` exits 0.

## Known limitations (reproducible)

- No browser automation is bundled; `smoke-check.js` verifies structure/JS only.
- Full UI walkthrough needs Playwright/Chromium (not installed in this env).
- All access checks are simulated (`sessionStorage` only); no real identity provider.
