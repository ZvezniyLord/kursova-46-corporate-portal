/* =====================================================================
 * PORTAL PROTOTYPE — shared navigation + user chip (UI-only demo)
 * Decides what is visible per role using PortalApp.can(role, perm).
 * NOT production authorization. Add to each page after app.js.
 * ===================================================================== */
window.PortalNav = (function () {
  'use strict';

  function roleLabel(role) {
    var meta = PortalApp.ROLE_META;
    if (!meta) return role || 'Гість';
    for (var i = 0; i < meta.length; i++) {
      if (meta[i].id === role) return meta[i].name;
    }
    return role || 'Гість';
  }

  function init(sidebarNavSelector, userChipSelector, avatarSelector, nameSelector) {
    var nav = document.querySelector(sidebarNavSelector);
    if (!nav) return;
    var role = PortalApp.getRole() || 'guest';

    var items = nav.querySelectorAll('li');
    for (var i = 0; i < items.length; i++) {
      var a = items[i].querySelector('a');
      if (!a) continue;
      var perm = a.getAttribute('data-perm');
      var allowed = perm ? PortalApp.can(role, perm) : true;
      items[i].style.display = allowed ? '' : 'none';
    }

    // user chip (optional)
    var chip = document.querySelector(userChipSelector);
    var avatar = document.querySelector(avatarSelector);
    var nameEl = document.querySelector(nameSelector);
    if (chip) {
      chip.innerHTML =
        '<span class="avatar">' + (avatar ? avatar.textContent : 'П') + '</span>' +
        '<span id="user-chip-name">' + roleLabel(role) + '</span>';
    }
    if (nameEl) nameEl.textContent = roleLabel(role);
  }

  return { init: init };
})();
