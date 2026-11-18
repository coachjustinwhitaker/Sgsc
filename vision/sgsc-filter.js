/* Owner and cadence filter for the SGSC task-list pages.
   Each page sets window.SGSC_FILTER before loading this file:
   { groups: [ { key, label, roles: [...], sections: [...] } ], shared: [ roles shown under every filter ] }
   An item is in a group when its owner is in roles, or its section id is in sections. */
(function () {
  var cfg = window.SGSC_FILTER; if (!cfg) return;
  var items = [].slice.call(document.querySelectorAll('ul.tasks > li')).map(function (li) {
    var w = li.querySelector('.who'), s = li.closest('section');
    return { li: li, role: w ? w.textContent.trim() : '', section: s ? s.id : '' };
  });
  function inGroup(i, g) {
    return (g.roles || []).indexOf(i.role) > -1 || (g.sections || []).indexOf(i.section) > -1;
  }
  var bar = document.createElement('div');
  bar.className = 'filter-bar no-print'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Filter items');
  bar.innerHTML = '<span class="filter-label">Show</span><div class="chips"></div>' +
    '<label class="filter-role">Role <select id="role-filter"></select></label>' +
    '<span id="filter-status" aria-live="polite"></span>';
  var chipBox = bar.querySelector('.chips'), sel = bar.querySelector('select'), status = bar.querySelector('#filter-status');
  var chips = [{ key: 'all', label: 'All' }].concat(cfg.groups).map(function (g) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = g.label; b.setAttribute('aria-pressed', g.key === 'all');
    b.addEventListener('click', function () { group = g.key; role = 'all'; chips.forEach(function (c) { c.setAttribute('aria-pressed', c === b); }); fillRoles(); apply(); });
    chipBox.appendChild(b); return b;
  });
  var nav = document.querySelector('.doc-nav');
  (nav ? nav : document.querySelector('.cover')).insertAdjacentElement('afterend', bar);
  var group = 'all', role = 'all';
  function groupDef() { return cfg.groups.filter(function (g) { return g.key === group; })[0]; }
  function inFilter(i) {
    if (group === 'all') return true;
    var g = groupDef(); return inGroup(i, g);
  }
  function fillRoles() {
    var counts = {};
    items.forEach(function (i) { if (inFilter(i)) counts[i.role] = (counts[i.role] || 0) + 1; });
    var names = Object.keys(counts).sort(), total = names.reduce(function (a, n) { return a + counts[n]; }, 0);
    sel.innerHTML = '<option value="all">All roles (' + total + ')</option>';
    names.forEach(function (n) { var o = document.createElement('option'); o.value = n; o.textContent = n + ' (' + counts[n] + ')'; sel.appendChild(o); });
    if (names.indexOf(role) < 0) role = 'all'; sel.value = role;
  }
  function apply() {
    var shown = 0, shared = cfg.shared || [];
    items.forEach(function (i) {
      var ok = inFilter(i) && (role === 'all' || i.role === role);
      if (!ok && role !== 'all' && shared.indexOf(i.role) > -1) ok = true; /* items for every role stay visible */
      i.li.hidden = !ok; if (ok) shown++;
    });
    [].forEach.call(document.querySelectorAll('section[id]'), function (s) {
      var has = s.querySelector('ul.tasks'); if (!has) return;
      var any = s.querySelector('ul.tasks > li:not([hidden])'); s.hidden = !any;
      var a = document.querySelector('.toc a[href="#' + s.id + '"]'); if (a && a.parentNode) a.parentNode.hidden = !any;
    });
    status.textContent = 'Showing ' + shown + ' of ' + items.length + ' items';
  }
  sel.addEventListener('change', function () { role = sel.value; apply(); });
  fillRoles(); apply();
})();
