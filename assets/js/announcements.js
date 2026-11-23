/* =====================================================================
 * PORTAL PROTOTYPE — announcements controller (demo, UI-only)
 * ===================================================================== */
(function () {
  'use strict';

  var role = PortalApp.getRole();
  if (!PortalApp.isAuthenticated()) { PortalApp.goTo('index.html'); return; }
  if (!PortalApp.can(role, 'view_announcements')) {
    PortalApp.showAccessDenied('Доступ до оголошень заборонено.');
    return;
  }

  var app = document.getElementById('app');
  var pageTitle = document.getElementById('page-title');

  // admin / superadmin can also add a note (management representation)
  if (PortalApp.can(role, 'manage_announcements')) {
    app.innerHTML =
      '<div class="card" style="margin-bottom:16px;">' +
        '<h3>Додати оголошення</h3>' +
        '<div class="form-grid" style="grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div class="field"><label>Заголовок</label><input class="input" id="new-title" placeholder="Тема оголошення" /></div>' +
          '<div class="field"><label>Категорія</label><select class="select" id="new-category">' +
            '<option value="загальна">загальна</option><option value="графік">графік</option><option value="платні умови">платні умови</option>' +
            '<option value="навчання">навчання</option><option value="кампанія">кампанія</option><option value="методичка">методичка</option>' +
            '<option value="акуція">акуція</option><option value="зустріч">зустріч</option></select></div>' +
          '<div class="field"><label>Рівень</label><select class="select" id="new-importance">' +
            '<option value="норма">норма</option><option value="важливо">важливо</option></select></div>' +
          '<div class="field"><label>Дата (yyyy-mm-dd)</label><input class="input" id="new-date" value="' + new Date().toISOString().slice(0,10) + '" /></div>' +
        '</div>' +
        '<div class="row" style="margin-top:10px;"><button id="save-note" class="btn">Зберегти декларацію</button></div>' +
      '</div>';
  }

  // filter controls
  app.innerHTML +=
    '<div class="panel-strip">' +
      '<button data-filter="all" class="btn-active">Всі</button>' +
      '<button data-filter="загальна">загальна</button>' +
      '<button data-filter="графік">графік</button>' +
      '<button data-filter="платні умови">платні умови</button>' +
      '<button data-filter="навчання">навчання</button>' +
      '<button data-filter="акуція">акуція</button>' +
    '</div>';

  // list
  var list = document.createElement('div');
  list.id = 'note-list';
  app.appendChild(list);

  function render(filter) {
    var items = PortalDemoData.announcements.filter(function (a) {
      return !filter || a.category === filter || filter === 'all';
    });
    if (!items.length) {
      list.innerHTML = '<div class="empty">Немає оголошень за цим фільтром.</div>';
      return;
    }
    list.innerHTML = items.map(function (a) {
      var badge = a.importance === 'важливо'
        ? '<span class="badge badge-important">важливо</span>'
        : '<span class="badge badge-normal">' + a.importance + '</span>';
      return '<div class="card" style="margin-bottom:10px;padding:12px;">' +
        '<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">' +
          '<span class="badge" style="background:var(--accent-soft);color:var(--accent);">' + a.category + '</span>' +
          '<span style="font-size:12px;color:var(--text-muted);">' + a.date + '</span>' +
        '</div>' +
        '<div style="font-weight:700;margin-top:6px;">' + a.title + '</div>' +
        '<div style="font-size:13px;color:var(--text-muted);">' + badge + ' · ' + (PortalDemoData.findEmployeeById(a.author) || { name: '—' }).name + '</div>' +
        '<p style="margin:8px 0 0;font-size:14px;">' + a.text + '</p>' +
      '</div>';
    }).join('');
  }

  render();

  // filter buttons
  document.querySelectorAll('.panel-strip button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.panel-strip button').forEach(function (x) { x.classList.remove('btn-active'); });
      b.classList.add('btn-active');
      render(b.dataset.filter);
    });
  });

  // save new announcement (management demo)
  var saveBtn = document.getElementById('save-note');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      var title = document.getElementById('new-title').value.trim();
      if (!title) { alert('Введіть заголовок.'); return; }
      // In the real product this would call an API. Here it is UI-only:
      // append to the demo list and re-render.
      var newAnn = {
        id: 'ann-' + Date.now(),
        title: title,
        category: document.getElementById('new-category').value,
        importance: document.getElementById('new-importance').value,
        date: document.getElementById('new-date').value,
        author: role === 'superadmin' ? 'emp-super' : 'emp-admin',
        text: 'Записано через UI-форму (демо).'
      };
      PortalDemoData.announcements.unshift(newAnn);
      render();
      alert('Демо: оголошення додано (в пам\'яті сторінки). Реалізація API — на наступному етапі.');
    });
  }

  pageTitle.textContent = 'Оголошення';
})();
