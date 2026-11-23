/* =====================================================================
 * PORTAL PROTOTYPE — directory controller (demo, UI-only)
 * ===================================================================== */
(function () {
  'use strict';

  var role = PortalApp.getRole();
  if (!PortalApp.isAuthenticated()) { PortalApp.goTo('index.html'); return; }
  if (!PortalApp.can(role, 'view_directory')) {
    PortalApp.showAccessDenied('Доступ до довідника заборонено.');
    return;
  }

  var app = document.getElementById('app');
  var pageTitle = document.getElementById('page-title');

  if (PortalApp.can(role, 'manage_directory')) {
    app.innerHTML =
      '<div class="card" style="margin-bottom:16px;">' +
        '<h3>Додати співробітника (демо)</h3>' +
        '<div class="form-grid" style="grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div class="field"><label>Ім\'я</label><input class="input" id="new-emp-name" placeholder="Прізвище та ім\'я" /></div>' +
          '<div class="field"><label>Роль</label><select class="select" id="new-emp-role">' +
            '<option value="Працівник">Працівник</option><option value="Адміністратор">Адміністратор</option>' +
            '<option value="Головний лікар">Головний лікар</option><option value="Руководитель">Руководитель</option>' +
          '</select></div>' +
          '<div class="field"><label>Віддділ</label><input class="input" id="new-emp-dept" placeholder="Віддділ" /></div>' +
          '<div class="field"><label>Ел. пошта</label><input class="input" id="new-emp-email" placeholder="email@firm.ua" /></div>' +
        '</div>' +
        '<div class="row" style="margin-top:10px;"><button id="save-emp" class="btn">Додати демо-співробітника</button></div>' +
      '</div>';
  }

  app.innerHTML +=
    '<div class="grid grid-2" style="gap:10px;">' +
      '<div class="card" style="padding:12px;">' +
        '<input class="input" id="search-q" placeholder="Пошук за іменем, роллю, віддділом..." style="width:100%;" />' +
      '</div>' +
      '<div class="card" style="padding:12px;">' +
        '<select class="select" id="filter-dept"><option value="">Всі віддділи</option>' + PortalDemoData.getDepartments().map(function (d) { return '<option value="' + d + '">' + d + '</option>'; }).join('') + '</select>' +
      '</div>' +
    '</div>';

  var list = document.createElement('div');
  list.id = 'emp-list';
  app.appendChild(list);

  function render() {
    var q = document.getElementById('search-q').value.trim();
    var dept = document.getElementById('filter-dept').value;
    var items = PortalDemoData.searchEmployees(q, dept);
    if (!items.length) {
      list.innerHTML = '<div class="empty">Співробітники не знайдено.</div>';
      return;
    }
    list.innerHTML = items.map(function (e) {
      var roleClass = e.role === 'Адміністратор' || e.role === 'Суперадміністратор' ? 'admin' : ('user');
      return '<div class="card" style="padding:12px;margin-bottom:8px;">' +
        '<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">' +
          '<span class="role-badge" style="background:var(--accent-soft);color:var(--accent);">' + e.role + '</span>' +
          '<span style="font-size:12px;color:var(--text-muted);">#' + e.id + '</span>' +
        '</div>' +
        '<div style="font-weight:700;">' + e.name + '</div>' +
        '<div style="font-size:13px;color:var(--text-muted);">' + e.department + '</div>' +
        '<div style="font-size:12px;color:var(--text-muted);"><a href="mailto:' + e.email + '">' + e.email + '</a> · ' + e.phone + '</div>' +
      '</div>';
    }).join('');
  }

  document.getElementById('search-q').addEventListener('input', render);
  document.getElementById('filter-dept').addEventListener('change', render);
  render();

  var saveBtn = document.getElementById('save-emp');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      var name = document.getElementById('new-emp-name').value.trim();
      if (!name) { alert('Введіть ім\'я.'); return; }
      PortalDemoData.employees.unshift({
        id: 'emp-' + Date.now(),
        name: name,
        role: document.getElementById('new-emp-role').value,
        department: document.getElementById('new-emp-dept').value,
        email: document.getElementById('new-emp-email').value,
        phone: '+380 50 000 00 00',
        avatar: 'Співробітник',
        note: 'Демо-додаток.'
      });
      render();
      alert('Демо: співробітник додано (в пам\'яті сторінки).');
    });
  }

  pageTitle.textContent = 'Довідник співробітників';
})();
