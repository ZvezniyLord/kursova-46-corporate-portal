/* =====================================================================
 * PORTAL PROTOTYPE — shared engine: authentication + RBAC access control
 * =====================================================================
 * This file is the UI-only demonstration of RBAC for the corporate
 * portal prototype. DECISION: the prototype is a static front-end
 * simulation. Permissions are enforced in the browser only and are NOT
 * production authorization logic. No real login, no session tokens,
 * no secure storage. A real deployment must put the same role/permission
 * matrix behind a real identity provider and API layer.
 * ===================================================================== */

window.PortalApp = (function () {
  'use strict';

  /* ---- Role metadata (mirrors PortalDemoData.roles) ---- */
  var ROLE_META = PortalDemoData ? PortalDemoData.roles : null;

  /* ---- Permission matrix: role -> allowed permissions ---- */
  var PERMISSIONS = {};
  if (ROLE_META) {
    ROLE_META.forEach(function (r) { PERMISSIONS[r.id] = r.permissions; });
  }

  /* ---- Stored session (MOCK) ---- */
  var ROLE_KEY = 'portal_demo_role';
  var AUTH_KEY = 'portal_demo_auth';

  function getRole() {
    try { return sessionStorage.getItem(ROLE_KEY); } catch (e) { return null; }
  }
  function setRole(role) {
    try { sessionStorage.setItem(ROLE_KEY, role); } catch (e) { /* ignore */ }
  }
  function isAuthenticated() {
    var r = getRole();
    return r !== null && r !== 'guest';
  }

  /* ---- RBAC engine ---- */
  function can(role, permission) {
    if (!PERMISSIONS[role]) return false;
    return PERMISSIONS[role].indexOf(permission) !== -1;
  }

  /* ---- Helpers for the demo: require role / permission ---- */
  function requireAuth(redirectTo) {
    if (!isAuthenticated()) {
      goTo('index.html' + (redirectTo ? '?' + encodeURIComponent(redirectTo) : ''));
      return false;
    }
    return true;
  }

  function requirePermission(permission, fallbackUrl) {
    var role = getRole();
    if (!role) { goTo('index.html'); return false; }
    if (!can(role, permission)) {
      if (fallbackUrl) { goTo(fallbackUrl); } else { showAccessDenied('Потрібен розширений доступ.'); }
      return false;
    }
    return true;
  }

  function goTo(url) {
    window.location.href = url;
  }

  function showAccessDenied(message) {
    var root = document.getElementById('app');
    if (!root) return;
    root.innerHTML =
      '<div class="alert alert-danger" role="alert"><strong>Доступ заборонено.</strong> ' +
      (message || 'Ця функція доступна лише для обраного користувача з розширеним доступом.') +
      '</div>';
  }

  /* ---- Stateless helpers ---- */
  function byId(list, id) {
    if (!list) return null;
    for (var i = 0; i < list.length; i++) { if (list[i].id === id) return list[i]; }
    return null;
  }

  return {
    getRole: getRole,
    isAuthenticated: isAuthenticated,
    can: can,
    requireAuth: requireAuth,
    requirePermission: requirePermission,
    goTo: goTo,
    showAccessDenied: showAccessDenied,
    byId: byId,
    setRole: setRole,
    ROLE_META: ROLE_META,
    PERMISSIONS: PERMISSIONS
  };
})();
