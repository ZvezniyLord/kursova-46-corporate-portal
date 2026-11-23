/* =====================================================================
 * PORTAL PROTOTYPE — dashboard controller (demo, UI-only)
 * ===================================================================== */
(function () {
  'use strict';

  var role = PortalApp.getRole();
  if (!PortalApp.isAuthenticated()) { PortalApp.goTo('index.html'); return; }
  if (!PortalApp.can(role, 'view_dashboard')) {
    PortalApp.showAccessDenied('Ви не маєте доступу до панелі.');
    return;
  }

  var roleMeta = null;
  if (PortalApp.ROLE_META) {
    for (var i = 0; i < PortalApp.ROLE_META.length; i++) {
      if (PortalApp.ROLE_META[i].id === role) { roleMeta = PortalApp.ROLE_META[i]; break; }
    }
  }

  var avatar = document.getElementById('user-avatar');
  var nameEl = document.getElementById('user-chip-name');
  if (avatar) avatar.textContent = roleMeta ? roleMeta.name.charAt(0) : 'П';
  if (nameEl) nameEl.textContent = roleMeta ? roleMeta.name : role;

  var app = document.getElementById('app');
  var today = new Date();
  var greeting = today.getHours() < 12 ? 'Доброго ранку' : (today.getHours() < 18 ? 'Доброго дня' : 'Доброго вечора');

  var html = '<div class="grid grid-2">' +
    '<div class="card">' +
      '<h3>' + greeting + ', ' + (roleMeta ? roleMeta.name : role) + '!</h3>' +
      '<p>Ви увійшли у демо-сервіс. Дані синтетичні.</p>' +
      '<p>Роль: <span class="role-badge" style="background:' + (role === 'superadmin' ? '#e4e0f0' : role === 'admin' ? '#e3edf7' : '#e4f4e9') + ';color:' + (role === 'superadmin' ? '#443a7a' : role === 'admin' ? '#1f5fbf' : '#1c7c45') + ';">' + roleMeta ? roleMeta.name : role + '</span></p>' +
      '<a class="btn btn-secondary" style="margin-top:10px;" href="index.html">Вийти</a>' +
    '</div>' +

    '<div class="card">' +
      '<h3>Швидкі посилання</h3>' +
      '<div class="grid grid-2" style="gap:10px;">' +
        '<a href="announcements.html" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--border);border-radius:8px;background:var(--surface);text-decoration:none;">📢 Оголошення</a>' +
        '<a href="documents.html" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--border);border-radius:8px;background:var(--surface);text-decoration:none;">📄 Документи</a>' +
        '<a href="directory.html" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--border);border-radius:8px;background:var(--surface);text-decoration:none;">👥 Довідник</a>' +
        '<a href="roles.html" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--border);border-radius:8px;background:var(--surface);text-decoration:none;">🔐 Ролі</a>' +
      '</div>' +
    '</div>' +

    '<div class="card">' +
      '<h3>Останні оголошення</h3>' +
      '<div id="recent-notes"></div>' +
    '</div>' +

    '<div class="card">' +
      '<h3>Активні сповіщення</h3>' +
      '<ul style="margin:0;padding-left:20px;">' +
        '<li>Оновлено внутрішній портал — перший вхід свободний.</li>' +
        '<li>Поточна дата (демо): ' + today.getFullYear() + '-' + String(today.getMonth()+1).padStart(2,'0') + '-' + String(today.getDate()).padStart(2,'0') + '</li>' +
      '</ul>' +
    '</div>' +
  '</div>';

  app.innerHTML = html;

  // render recent announcements
  var notes = PortalDemoData.announcements.slice(0, 3);
  var box = document.getElementById('recent-notes');
  if (!box) return;
  box.innerHTML = notes.map(function (a) {
    return '<div class="card" style="margin-bottom:8px;padding:10px;">' +
      '<div style="font-weight:700;">' + a.title + '</div>' +
      '<div style="font-size:12px;color:var(--text-muted);">' + a.date + ' · ' + a.category + '</div>' +
      '<div style="margin-top:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">' + a.text + '</div>' +
    '</div>';
  }).join('');
})();
