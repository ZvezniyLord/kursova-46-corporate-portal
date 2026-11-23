/* =====================================================================
 * PORTAL PROTOTYPE — roles & access-control matrix controller (demo)
 * ===================================================================== */
(function () {
  'use strict';

  var role = PortalApp.getRole();
  if (!PortalApp.isAuthenticated()) { PortalApp.goTo('index.html'); return; }
  // Matrix is read-only for everyone; manage_roles only toggles who may see the "edit" controls.
  if (!PortalApp.can(role, 'view_audit') && !PortalApp.can(role, 'manage_roles')) {
    // Show the matrix but grey out management controls.
    var canManage = PortalApp.can(role, 'manage_roles') || PortalApp.can(role, 'manage_users');
    renderMatrix(canManage);
    return;
  }

  function renderMatrix(canManage) {
    var app = document.getElementById('app');
    app.innerHTML = '<div class="card" style="max-width:1100px;">' +
      '<h3>Матриця контролю доступу (RBAC, демо)</h3>' +
      '<p style="color:var(--text-muted);font-size:14px;">Симуляція політики. У продакшені цей файл підтримується більш ніж UI: він має бути покладений на ідентичні послуги ідентифікації та послуги API.</p>' +

      '<div class="grid grid-2" style="gap:16px;">' +
        '<div class="card">' +
          '<h4>Ролі та дозволи</h4>' +
          '<div class="roles-grid">' + PortalDemoData.roles.map(function (r) {
            return '<div class="card" style="padding:12px;">' +
              '<div style="font-weight:700;">' + r.name + ' <span style="font-weight:400;font-size:12px;color:var(--text-muted);">(' + r.id + ')</span></div>' +
              '<div style="font-size:13px;color:var(--text-muted);">' + r.description + '</div>' +
              '<div style="margin-top:8px;line-height:1.6;">' + r.permissions.map(function (p) { return '• ' + p + '<br/>'; }).join('') + '</div>' +
            '</div>';
          }).join('') + '</div>' +
        '</div>' +

        '<div class="card">' +
          '<h4>Матриця роль x дозвіл</h4>' +
          '<table class="matrix">' +
            '<tr><th>Дозвіл \\ Роль</th>' + PortalDemoData.roles.map(function (r) { return '<th>' + r.name + '</th>'; }).join('') + '</tr>' +
            PortalDemoData.roles[0].permissions.map(function (perm) {
              var row =
                '<tr><th>' + perm + '</th>' +
                PortalDemoData.roles.map(function (r) {
                  var ok = PortalApp.can(r.id, perm);
                  return '<td class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '✗') + '</td>';
                }).join('') + '</tr>';
              return row;
            }).join('') +
          '</table>' +
        '</div>' +
      '</div>' +

      '<div class="card" style="margin-top:16px;">' +
        '<h4>Статус доступу поточного сеансу</h4>' +
        '<div style="display:flex;flex-direction:column;gap:8px;">' +
          PortalDemoData.roles.map(function (r) {
            var ok = PortalApp.can(r.id, 'view_dashboard');
            return '<div><b>' + r.name + '</b> — <span class="role-badge" style="background:' + (ok ? 'var(--good-soft)' : 'var(--warn-soft)') + ';color:' + (ok ? 'var(--good)' : 'var(--warn)') + ';">' + (ok ? 'працює' : 'заборонено') + '</span></div>';
          }).join('') +
        '</div>' +
      '</div>' +

      '<div class="card" style="margin-top:16px;">' +
        '<h4>Керуючі елементи (демо)</h4>' +
        '<p style="color:var(--text-muted);font-size:13px;">' +
          (canManage
            ? 'Ви можете керувати ролями та користувачами. У продакшені це вимагає пристрою сесії, контролю доступу до API та аудиту.'
            : 'Цей екран читається лише для перегляду. Редагування доступне лише для адміністраторів та суперадміністраторів.')
        + '</p>' +
      '</div>' +
    '</div>';
  }

  renderMatrix(PortalApp.can(role, 'manage_roles') || PortalApp.can(role, 'manage_users'));
})();
