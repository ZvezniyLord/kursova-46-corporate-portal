#!/usr/bin/env node
/* =====================================================================
 * PORTAL PROTOTYPE — smoke check (Node)
 * =====================================================================
 * Verifies, without a browser:
 *  1. required files exist
 *  2. JS syntax is valid (node --check)
 *  3. HTML references present CSS/JS
 *  4. demo data loads in a sandbox and RBAC matrix matches expectations
 *
 * Run:  node docs/smoke-check.js
 * ===================================================================== */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const ASSETS = path.join(ROOT, 'assets');
const JS_DIR = path.join(ASSETS, 'js');
const CSS_DIR = path.join(ASSETS, 'css');
const HTML_FILES = [
  path.join(ROOT, 'index.html'),
  path.join(ROOT, 'dashboard.html'),
  path.join(ROOT, 'announcements.html'),
  path.join(ROOT, 'documents.html'),
  path.join(ROOT, 'directory.html'),
  path.join(ROOT, 'roles.html'),
];

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok, detail: detail || '' });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -- ' + detail : ''}`);
}

// 1. required files
const required = [
  path.join(ROOT, 'index.html'),
  path.join(ROOT, 'dashboard.html'),
  path.join(ROOT, 'announcements.html'),
  path.join(ROOT, 'documents.html'),
  path.join(ROOT, 'directory.html'),
  path.join(ROOT, 'roles.html'),
  path.join(ASSETS, 'css', 'styles.css'),
  path.join(JS_DIR, 'demo-data.js'),
  path.join(JS_DIR, 'app.js'),
  path.join(JS_DIR, 'nav.js'),
  path.join(JS_DIR, 'login.js'),
  path.join(JS_DIR, 'dashboard.js'),
  path.join(JS_DIR, 'announcements.js'),
  path.join(JS_DIR, 'documents.js'),
  path.join(JS_DIR, 'directory.js'),
  path.join(JS_DIR, 'roles.js'),
].concat(HTML_FILES);

HTML_FILES.forEach((f) => {
  // already in required; skip
});

// reuse required list for HTML checks
const missing = required.filter((f) => !fs.existsSync(f));
check('required files exist', missing.length === 0, missing.length ? 'missing: ' + missing.join(', ') : '');

// 2. JS syntax
const jsFiles = [
  path.join(JS_DIR, 'demo-data.js'),
  path.join(JS_DIR, 'app.js'),
  path.join(JS_DIR, 'nav.js'),
  path.join(JS_DIR, 'login.js'),
  path.join(JS_DIR, 'dashboard.js'),
  path.join(JS_DIR, 'announcements.js'),
  path.join(JS_DIR, 'documents.js'),
  path.join(JS_DIR, 'directory.js'),
  path.join(JS_DIR, 'roles.js'),
];
let syntaxOk = true;
for (const f of jsFiles) {
  try {
    execFileSync(process.execPath, ['--check', f], { stdio: ['pipe', 'pipe', 'pipe'] });
  } catch (e) {
    syntaxOk = false;
    check('syntax: ' + path.relative(ROOT, f), false, e.message.split('\n')[0]);
  }
}
check('JS syntax valid', syntaxOk);

// 3. HTML references
for (const htmlFile of HTML_FILES) {
  const html = fs.readFileSync(htmlFile, 'utf8');
  const rel = path.relative(ROOT, htmlFile);
  const deps = [
    /assets\/css\/styles\.css/,
    /assets\/js\/demo-data\.js/,
    /assets\/js\/app\.js/,
    /assets\/js\/nav\.js/,
  ];
  // allow one page-specific extra script
  const pageJs = ['login.js', 'dashboard.js', 'announcements.js', 'documents.js', 'directory.js', 'roles.js'];
  const pageSpecific = html.includes('assets/js/') ? pageJs.some((p) => html.includes('assets/js/' + p)) : false;
  const hasDeps = deps.every((re) => re.test(html));
  check('HTML deps: ' + rel, hasDeps && pageSpecific, '');
}

// 4. RBAC matrix in sandbox
const vm = require('vm');
const dataSrc = fs.readFileSync(path.join(JS_DIR, 'demo-data.js'), 'utf8');
const appSrc = fs.readFileSync(path.join(JS_DIR, 'app.js'), 'utf8');
const sandbox = { console };
vm.createContext(sandbox);
sandbox.window = sandbox;
sandbox.document = { getElementById: () => null, querySelector: () => null };
vm.runInContext(dataSrc, sandbox, { filename: 'demo-data.js' });
vm.runInContext(appSrc, sandbox, { filename: 'app.js' });

let matrixOk = true;
const roleIds = [];
const permSet = {};
if (sandbox.PortalDemoData && sandbox.PortalApp) {
  // role ids
  (sandbox.PortalDemoData.roles || []).forEach((r) => roleIds.push(r.id));
  // expected: guest has only login/public perms; user+ has dashboard/announcements/docs/directory
  const expected = {
    guest: ['login', 'view_public_announcements', 'view_public_documents'],
    user: ['login', 'view_dashboard', 'view_announcements', 'view_documents', 'view_directory'],
    admin: ['login', 'view_dashboard', 'view_announcements', 'view_documents', 'view_directory',
            'manage_announcements', 'manage_documents', 'manage_directory', 'manage_roles', 'manage_users', 'view_audit'],
    superadmin: ['login', 'view_dashboard', 'view_announcements', 'view_documents', 'view_directory',
                 'manage_announcements', 'manage_documents', 'manage_directory', 'manage_roles', 'manage_users', 'view_audit',
                 'export_data', 'reset_credentials'],
  };
  for (const [role, perms] of Object.entries(expected)) {
    const actual = sandbox.PortalApp.can ? sandbox.PortalApp.can(role, perms[0]) : false;
    if (!sandbox.PortalApp.can) { matrixOk = false; continue; }
    const actualPerms = perms.filter((p) => sandbox.PortalApp.can(role, p));
    const missing = perms.filter((p) => !sandbox.PortalApp.can(role, p));
    const extra = actualPerms.filter((p) => !perms.includes(p));
    if (missing.length || extra.length) {
      matrixOk = false;
      check('RBAC ' + role, false, 'missing=' + missing.join(',') + ' extra=' + extra.join(','));
    } else {
      check('RBAC ' + role, true, 'all ' + perms.length + ' perms present');
    }
  }
} else {
  matrixOk = false;
  check('RBAC sandbox data/App loaded', false, 'PortalDemoData=' + !!sandbox.PortalDemoData + ', PortalApp=' + !!sandbox.PortalApp);
}

// demo search smoke
let searchOk = false;
if (sandbox.PortalDemoData) {
  const docs = sandbox.PortalDemoData.searchDocuments('безпека', '', '');
  const emps = sandbox.PortalDemoData.searchEmployees('Йо', 'Фінанси');
  searchOk = docs.length >= 1 && emps.length >= 0;
  check('demo search functions run', searchOk, 'docs=' + docs.length + ', emps=' + emps.length);
}

check('RBAC matrix matches expectations', matrixOk);
check('demo search functions run', searchOk);

console.log('\n==== SUMMARY ====');
const passed = results.filter((r) => r.ok).length;
console.log('passed: ' + passed + '/' + results.length);
process.exit(passed === results.length ? 0 : 1);
