/* Diamond search: client-side filter and sort over /diamonds.json. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const root = $('[data-ds]'); if (!root) return;
  const form = $('#ds-form'), rows = $('[data-ds-rows]'), count = $('[data-ds-count]'), empty = $('[data-ds-empty]'), more = $('[data-ds-more]');
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const COLORS = 'DEFGHIJK', CLAR = ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2'];
  let all = [], view = [], limit = 40;

  function read() {
    const fd = new FormData(form);
    const g = k => fd.get(k);
    return {
      shapes: fd.getAll('shape'), origin: g('origin'),
      cmin: +g('cmin') || 0, cmax: +g('cmax') || 99,
      colmin: COLORS.indexOf(g('colmin')), colmax: COLORS.indexOf(g('colmax')),
      clmin: CLAR.indexOf(g('clmin')), clmax: CLAR.indexOf(g('clmax')),
      pmin: +g('pmin') || 0, pmax: +g('pmax') || Infinity, cut: g('cut'), sort: g('sort'),
    };
  }
  function apply() {
    const f = read();
    view = all.filter(d =>
      (!f.shapes.length || f.shapes.includes(d.shape)) &&
      (f.origin === 'all' || (f.origin === 'lab') === d.lab) &&
      d.carat >= f.cmin && d.carat <= f.cmax &&
      COLORS.indexOf(d.color) >= Math.min(f.colmin, f.colmax) && COLORS.indexOf(d.color) <= Math.max(f.colmin, f.colmax) &&
      CLAR.indexOf(d.clarity) >= Math.min(f.clmin, f.clmax) && CLAR.indexOf(d.clarity) <= Math.max(f.clmin, f.clmax) &&
      d.price >= f.pmin && d.price <= f.pmax && (!f.cut || d.cut === f.cut));
    view.sort((a, b) => f.sort === 'price-desc' ? b.price - a.price : f.sort === 'carat-desc' ? b.carat - a.carat : f.sort === 'carat-asc' ? a.carat - b.carat : a.price - b.price);
    limit = 40; render();
  }
  function render() {
    count.textContent = view.length;
    empty.hidden = view.length > 0;
    rows.innerHTML = view.slice(0, limit).map(d =>
      '<tr><td>' + d.shape + '</td><td>' + d.carat.toFixed(2) + '</td><td>' + d.color + '</td><td>' + d.clarity + '</td><td>' + d.cut + '</td><td>' + d.origin + '</td><td>' + d.cert + ' ' + d.cert_no + '</td><td>' + d.measurements + '</td><td class="price">' + money(d.price) + '</td><td><button type="button" class="btn btn-ghost btn-sm" data-inquire="' + d.id + '">Ask</button></td></tr>').join('');
    more.hidden = view.length <= limit;
  }
  form.addEventListener('change', apply);
  form.addEventListener('input', e => { if (e.target.type === 'number') apply(); });
  form.addEventListener('reset', () => setTimeout(apply, 0));
  form.addEventListener('submit', e => e.preventDefault());
  more.addEventListener('click', () => { limit += 40; render(); });
  rows.addEventListener('click', e => {
    const b = e.target.closest('[data-inquire]'); if (!b) return;
    const d = all.find(x => x.id === b.dataset.inquire);
    const text = d.carat.toFixed(2) + ' ct ' + d.shape + ', ' + d.color + ' ' + d.clarity + ', ' + d.cut + ' cut, ' + d.origin.toLowerCase() + ', ' + d.cert + ' ' + d.cert_no + ', ' + money(d.price) + ' (ID ' + d.id + ')';
    $('[data-inquire-summary]').textContent = text;
    $('[data-inquire-field]').value = text;
    $('#inquire').showModal();
  });
  fetch((document.body.dataset.base || '') + '/diamonds.json').then(r => r.json()).then(d => { all = d; apply(); });
})();
