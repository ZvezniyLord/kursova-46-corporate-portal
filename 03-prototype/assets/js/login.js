/* =====================================================================
 * PORTAL PROTOTYPE — login screen controller (demo, UI-only)
 * ===================================================================== */
(function () {
  'use strict';

  var roleEl = document.getElementById('demo-role');
  var emailEl = document.getElementById('demo-email');
  var passwordEl = document.getElementById('demo-password');
  var rememberEl = document.getElementById('remember');
  var btn = document.getElementById('login-btn');

  function goHome() {
    var ref = document.referrer && document.referrer !== window.location.href
      ? document.referrer
      : 'dashboard.html';
    window.location.href = ref;
  }

  btn.addEventListener('click', function () {
    var role = roleEl.value;
    var email = emailEl.value.trim();
    var password = passwordEl.value;

    if (!email) {
      alert('Будь ласка, введіть електронну пошту.');
      return;
    }
    // Demo: single synthetic account; the role is what demonstrates RBAC.
    if (email !== 'demo@firm.ua') {
      alert('Демо-режим підтверджує лише синтетичний обліковий запис demo@firm.ua.');
      return;
    }
    if (portalRemember) { /* no-op: role stored in sessionStorage via PortalApp */ }
    PortalApp.setRole(role);
    goHome();
  });

  function portalRemember() { /* kept for readability */ }
})();
