# Матриця контролю доступу (RBAC) — прототип

> Це демонстрація механізму на рівні UI. У реальній системі ця матриця лежить в бекенді
> індентичності та пристрої API, а не тільки в браузері.

| Дозвіл | guest | user | admin | superadmin | Слот |
|---|---|---|---|---|---|
| `login` | ✓ | ✓ | ✓ | ✓ | основа |
| `view_dashboard` | ✗ | ✓ | ✓ | ✓ | core |
| `view_announcements` | ✓ | ✓ | ✓ | ✓ | core |
| `view_documents` | ✓ | ✓ | ✓ | ✓ | core |
| `view_directory` | ✓ | ✓ | ✓ | ✓ | core |
| `manage_announcements` | ✗ | ✗ | ✓ | ✓ | administration |
| `manage_documents` | ✗ | ✗ | ✓ | ✓ | administration |
| `manage_directory` | ✗ | ✗ | ✓ | ✓ | administration |
| `manage_roles` | ✗ | ✗ | ✓ | ✓ | administration |
| `manage_users` | ✗ | ✗ | ✓ | ✓ | administration |
| `view_audit` | ✗ | ✗ | ✓ | ✓ | senior |
| `export_data` | ✗ | ✗ | ✗ | ✓ | senior |
| `reset_credentials` | ✗ | ✗ | ✗ | ✓ | senior |

## Flow signs

- `guest` — залишається на сторінці входу; публічний контент (оголошення/документи)
  демонструється формулювачем, інші екрани недоступні.
- `user` — панель, оголошення, документи, довідник. Без керування контентом.
- `admin` — додатково: додавання/редагування оголошень та документів, довідника,
  ролей, користувачів.
- `superadmin` — усі включно до `export_data` / `reset_credentials`.

## AV (access verification)

UAT може перевірити відображення елементів для кожної ролі в браузері
(UI-шар). Продакшн-перевірка `AV-001..` очікує реальну авторизацію на бекенді та немає
інтерпретації користувача без серверної перевірки.
