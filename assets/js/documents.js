/* =====================================================================
 * PORTAL PROTOTYPE — documents controller (demo, UI-only)
 * Searchable document catalogue with role-based listing.
 * ===================================================================== */
(function () {
  'use strict';

  var role = PortalApp.getRole();
  if (!PortalApp.isAuthenticated()) { PortalApp.goTo('index.html'); return; }
  if (!PortalApp.can(role, 'view_documents')) {
    PortalApp.showAccessDenied('Доступ до документів заборонено.');
    return;
  }

  var app = document.getElementById('app');
  var pageTitle = document.getElementById('page-title');

  if (PortalApp.can(role, 'manage_documents')) {
    app.innerHTML =
      '<div class="card" style="margin-bottom:16px;">' +
        '<h3>Додати документ</h3>' +
        '<div class="form-grid" style="grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div class="field"><label>Назва</label><input class="input" id="new-doc-title" placeholder="Назва документу" /></div>' +
          '<div class="field"><label>Категорія</label><select class="select" id="new-doc-category">' +
            '<optgroup label="Всього">' + PortalDemoData.getCategories().map(function (c) { return '<option value="' + c + '">' + c + '</option>'; }).join('') + '</optgroup>' +
          '</select></div>' +
          '<div class="field"><label>Віддділ</label><select class="select" id="new-doc-dept">' +
            '<optgroup label="Віддділи">' + PortalDemoData.getDepartments().map(function (d) { return '<option value="' + d + '">' + d + '</option>'; }).join('') + '</optgroup>' +
          '</select></div>' +
          '<div class="field"><label>Власник</label><select class="select" id="new-doc-owner"><option value="emp-1">Олександр Коваль (HR)</option><option value="emp-3">Дмитро Петров (IT)</option><option value="emp-4">Олена Іваненко (HR)</option></select></div>' +
          '<div class="field"><label>Розмір</label><input class="input" id="new-doc-size" value="120 КБ" /></div>' +
          '<div class="field"><label>Тип</label><input class="input" id="new-doc-type" value="pdf" /></div>' +
        '</div>' +
        '<div class="row" style="margin-top:10px;"><button id="save-doc" class="btn">Додати демо-документ</button></div>' +
      '</div>';
  }

  // filters
  app.innerHTML +=
    '<div class="grid grid-3" style="gap:10px;margin-bottom:16px;">' +
      '<div class="card" style="padding:12px;">' +
        '<input class="input" id="search-q" placeholder="Пошук за назвою, тегом, віддділом..." style="width:100%;" />' +
      '</div>' +
      '<div class="card" style="padding:12px;">' +
        '<select class="select" id="filter-cat"><option value="">Всі категорії</option>' + PortalDemoData.getCategories().map(function (c) { return '<option value="' + c + '">' + c + '</option>'; }).join('') + '</select>' +
      '</div>' +
      '<div class="card" style="padding:12px;">' +
        '<select class="select" id="filter-dept"><option value="">Всі віддділи</option>' + PortalDemoData.getDepartments().map(function (d) { return '<option value="' + d + '">' + d + '</option>'; }).join('') + '</select>' +
      '</div>' +
    '</div>';

  var table = document.createElement('table');
  app.appendChild(table);

  function render() {
    var q = document.getElementById('search-q').value.trim();
    var cat = document.getElementById('filter-cat').value;
    var dept = document.getElementById('filter-dept').value;
    var items = PortalDemoData.searchDocuments(q, cat, dept);
    if (!items.length) {
      table.innerHTML = '<tr><td colspan="6" class="empty" style="padding:24px;">Немає документів, що відповідають фільтру.</td></tr>';
      return;
    }
    table.innerHTML =
      '<tr>' +
        '<th>Назва</th><th>Категорія</th><th>Віддділ</th><th>Власник</th><th>Дата</th><th>Опис</th>' +
      '</tr>' +
      items.map(function (d) {
        var owner = PortalDemoData.findEmployeeById(d.owner);
        return '<tr>' +
          '<td><b>' + d.title + '</b><div style="font-size:12px;color:var(--text-muted);">#' + d.id + ' · ' + d.type + ' · ' + d.size + '</div></td>' +
          '<td>' + d.category + '</td>' +
          '<td>' + d.department + '</td>' +
          '<td>' + (owner ? owner.name : '—') + '</td>' +
          '<td>' + d.date + '</td>' +
          '<td style="font-size:13px;">' + d.tags.join(', ') + '</td>' +
        '</tr>';
      }).join('');
  }

  document.getElementById('search-q').addEventListener('input', render);
  document.getElementById('filter-cat').addEventListener('change', render);
  document.getElementById('filter-dept').addEventListener('change', render);

  render();
  pageTitle.textContent = 'Документи';
})();
