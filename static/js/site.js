/* Ice Vault — shared behavior: nav, cart, filters, product page, forms, search. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const body = document.body;
  const BASE = body.dataset.base || '';
  const CFG = { phone: body.dataset.phone, tel: body.dataset.tel, email: body.dataset.email, endpoint: body.dataset.formEndpoint, wire: +body.dataset.wire || 3, months: +body.dataset.months || 12 };
  const money = n => '$' + Math.round(n).toLocaleString('en-US');

  /* ---------- toast ---------- */
  let toastTimer;
  function toast(html, ms) {
    const t = $('#toast'); if (!t) return;
    t.innerHTML = html; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, ms || 4000);
  }

  /* ---------- cart ---------- */
  const KEY = 'iv-cart';
  const cart = {
    get() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } },
    set(items) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {} cart.badge(); },
    add(item) {
      const items = cart.get();
      const key = item.slug + '|' + Object.values(item.options || {}).join('|');
      const found = items.find(i => i.key === key);
      if (found) found.qty += item.qty; else items.push(Object.assign({ key }, item));
      cart.set(items);
    },
    remove(key) { cart.set(cart.get().filter(i => i.key !== key)); },
    qty(key, q) { const items = cart.get(); const it = items.find(i => i.key === key); if (it) { it.qty = Math.max(1, Math.min(10, q | 0)); cart.set(items); } },
    count() { return cart.get().reduce((n, i) => n + i.qty, 0); },
    total() { return cart.get().reduce((n, i) => n + i.qty * i.price, 0); },
    badge() { const n = cart.count(); $$('[data-cart-count]').forEach(el => { el.textContent = n; if (n) delete el.dataset.zero; else el.dataset.zero = '1'; }); },
  };
  cart.badge();
  window.IVCart = cart;

  /* ---------- drawer ---------- */
  const drawer = $('#drawer'), scrim = $('.scrim');
  function openDrawer(open) {
    if (!drawer) return;
    drawer.hidden = !open; scrim.hidden = !open; body.style.overflow = open ? 'hidden' : '';
    $$('[data-drawer-open]').forEach(b => b.setAttribute('aria-expanded', String(open)));
    if (open) { const f = $('a, button, input', drawer); f && f.focus(); }
  }
  $$('[data-drawer-open]').forEach(b => b.addEventListener('click', () => openDrawer(true)));
  $$('[data-drawer-close]').forEach(b => b.addEventListener('click', () => openDrawer(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { openDrawer(false); closeFilters(); } });

  /* mega menus: hover opens on pointer devices; on touch the first tap opens and the second follows the link */
  const touchOnly = window.matchMedia('(hover: none)').matches;
  $$('.has-mega > a').forEach(a => a.addEventListener('click', e => {
    const li = a.parentElement;
    if (touchOnly && !li.classList.contains('is-open')) { e.preventDefault(); $$('.has-mega.is-open').forEach(o => o.classList.remove('is-open')); li.classList.add('is-open'); }
  }));
  document.addEventListener('click', e => { if (!e.target.closest('.has-mega')) $$('.has-mega.is-open').forEach(o => o.classList.remove('is-open')); });
  $$('.has-mega').forEach(li => li.addEventListener('mouseleave', () => li.classList.remove('is-open')));

  /* ---------- collection filters ---------- */
  const grid = $('[data-collection-grid]');
  const filtersPanel = $('#filters-panel');
  function closeFilters() { filtersPanel && filtersPanel.classList.remove('is-open'); }
  if (grid) {
    const form = $('#filters');
    const cards = $$('.card', grid);
    cards.forEach((c, i) => { c.dataset.index = i; });
    const params = new URLSearchParams(location.search);
    ['type', 'color', 'purity', 'stone', 'price'].forEach(k => {
      const v = params.get(k); if (!v) return;
      v.split(',').forEach(val => { const cb = form.querySelector('input[name="' + k + '"][value="' + val + '"]'); if (cb) cb.checked = true; });
    });
    function apply(push) {
      const active = {};
      $$('input:checked', form).forEach(cb => (active[cb.name] = active[cb.name] || []).push(cb.value));
      let shown = 0;
      cards.forEach(c => {
        let ok = true;
        for (const k in active) {
          const vals = active[k];
          if (k === 'price') { const p = +c.dataset.price; ok = vals.some(v => { const [lo, hi] = v.split('-').map(Number); return p >= lo && p < hi; }); }
          else ok = vals.includes(c.dataset[k]);
          if (!ok) break;
        }
        c.hidden = !ok; if (ok) shown++;
      });
      const s = $('[data-shown]'); if (s) s.textContent = shown;
      const e = $('[data-empty]'); if (e) e.hidden = shown > 0;
      if (push) {
        const q = new URLSearchParams();
        for (const k in active) q.set(k, active[k].join(','));
        history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : ''));
      }
    }
    form.addEventListener('change', () => apply(true));
    $$('[data-filters-clear]').forEach(b => b.addEventListener('click', () => { form.reset(); apply(true); }));
    $$('[data-filters-open]').forEach(b => b.addEventListener('click', () => filtersPanel.classList.add('is-open')));
    $$('[data-filters-close]').forEach(b => b.addEventListener('click', closeFilters));
    const sort = $('[data-sort]');
    sort && sort.addEventListener('change', () => {
      const v = sort.value;
      const sorted = cards.slice().sort((a, b) => {
        if (v === 'price-asc') return a.dataset.price - b.dataset.price;
        if (v === 'price-desc') return b.dataset.price - a.dataset.price;
        if (v === 'az') return a.dataset.title.localeCompare(b.dataset.title);
        if (v === 'new') return (b.dataset.new - a.dataset.new) || (a.dataset.index - b.dataset.index);
        return a.dataset.index - b.dataset.index;
      });
      sorted.forEach(c => grid.appendChild(c));
    });
    apply(false);
  }

  /* ---------- product page ---------- */
  const pdp = $('[data-product]');
  if (pdp) {
    const data = JSON.parse($('#product-data').textContent);
    const priceEl = $('[data-price]'), wireEl = $('[data-wire-price]'), monthEl = $('[data-monthly]'), compareEl = $('[data-compare]');
    const lengthSel = $('[data-option="Length"]');
    let price = data.price;
    function setPrice(p) {
      price = p; priceEl.textContent = money(p);
      wireEl && (wireEl.textContent = money(p * (100 - CFG.wire) / 100));
      monthEl && (monthEl.textContent = money(p / CFG.months));
      if (compareEl && data.compare_at) compareEl.textContent = money(data.compare_at * p / data.price);
    }
    if (lengthSel && data.length) {
      lengthSel.addEventListener('change', () => {
        const len = parseFloat(lengthSel.value);
        if (len) setPrice(Math.round(data.price * len / data.length / 10) * 10);
      });
    }
    $$('.thumb').forEach(t => t.addEventListener('click', () => {
      $$('.thumb').forEach(x => x.classList.remove('is-active')); t.classList.add('is-active');
      const img = $('[data-gallery-img]'); if (img && t.dataset.src) img.src = t.dataset.src;
    }));
    $('[data-options]').addEventListener('submit', e => {
      e.preventDefault();
      const options = {};
      $$('[data-option]').forEach(s => { options[s.dataset.option] = s.value; });
      cart.add({ slug: data.slug, title: data.title, price, image: data.image, url: data.url, sku: data.sku, options, qty: +($('[data-qty]').value || 1) });
      toast('Added to cart. <a href="' + BASE + '/cart/">View cart</a>');
    });
    const offer = $('#offer');
    $$('[data-offer-open]').forEach(b => b.addEventListener('click', () => offer.showModal()));
  }
  $$('dialog.modal').forEach(d => d.addEventListener('click', e => { if (e.target === d) d.close(); }));

  /* ---------- cart page + checkout summary ---------- */
  const linesEl = $('[data-cart-lines]');
  if (linesEl) {
    const compact = linesEl.classList.contains('compact');
    function render() {
      const items = cart.get();
      const empty = $('[data-cart-empty]'), summary = $('[data-cart-summary]');
      linesEl.innerHTML = items.map(i => {
        const opts = Object.entries(i.options || {}).map(([k, v]) => k + ': ' + v).join(', ');
        return '<div class="cart-line" data-key="' + i.key + '">' +
          '<a href="' + i.url + '"><img src="' + i.image + '" alt=""></a>' +
          '<div><a class="cart-line-title" href="' + i.url + '">' + i.title + '</a>' + (opts ? '<div class="cart-line-opts">' + opts + '</div>' : '') +
          (compact ? '<div class="cart-line-opts">Quantity ' + i.qty + '</div>' : '<div class="cart-line-ctl"><label>Qty <input type="number" min="1" max="10" value="' + i.qty + '" data-qty-input></label><button type="button" class="link" data-remove>Remove</button></div>') +
          '</div><div class="cart-line-price">' + money(i.price * i.qty) + '</div></div>';
      }).join('');
      const total = cart.total();
      $$('[data-cart-subtotal]').forEach(e => e.textContent = money(total));
      $$('[data-cart-wire]').forEach(e => e.textContent = money(total * (100 - CFG.wire) / 100));
      $$('[data-cart-monthly]').forEach(e => e.textContent = money(total / CFG.months));
      if (empty) empty.hidden = items.length > 0;
      if (summary) summary.hidden = items.length === 0;
      const submit = $('form[data-include-cart] button[type=submit]'); if (submit) submit.disabled = items.length === 0;
    }
    linesEl.addEventListener('change', e => { const inp = e.target.closest('[data-qty-input]'); if (inp) { cart.qty(inp.closest('.cart-line').dataset.key, +inp.value); render(); } });
    linesEl.addEventListener('click', e => { const b = e.target.closest('[data-remove]'); if (b) { cart.remove(b.closest('.cart-line').dataset.key); render(); } });
    render();
  }

  /* ---------- forms ---------- */
  function setStatus(form, msg, err) { const s = $('.form-status', form); if (s) { s.textContent = msg; s.classList.toggle('is-error', !!err); } }
  $$('form[data-form]').forEach(form => form.addEventListener('submit', async e => {
    e.preventDefault();
    const subject = 'Ice Vault: ' + form.dataset.form;
    const fd = new FormData(form);
    const lines = [];
    for (const [k, v] of fd.entries()) { if (typeof v === 'string' && v.trim()) lines.push(k.replace(/_/g, ' ') + ': ' + v.trim()); }
    if (form.dataset.includeCart) {
      lines.push('', 'Cart:');
      cart.get().forEach(i => lines.push('  ' + i.qty + ' x ' + i.title + (i.sku ? ' [' + i.sku + ']' : '') + ' ' + Object.values(i.options || {}).join(', ') + ' = ' + money(i.price * i.qty)));
      lines.push('Subtotal: ' + money(cart.total()));
    }
    const btn = $('button[type=submit]', form);
    if (CFG.endpoint) {
      btn.disabled = true; setStatus(form, 'Sending');
      try {
        fd.append('_subject', subject); fd.append('summary', lines.join('\n'));
        const r = await fetch(CFG.endpoint, { method: 'POST', body: fd, headers: { Accept: 'application/json' } });
        if (!r.ok) throw new Error(r.status);
        form.reset(); setStatus(form, 'Sent. We reply within one business day.');
        if (form.dataset.clearCart) cart.set([]);
      } catch (err) { setStatus(form, 'Could not send. Call or text ' + CFG.phone + '.', true); }
      btn.disabled = false;
    } else {
      location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      setStatus(form, 'Your email app opened with the details filled in. Send it and we reply within one business day. If nothing opened, text ' + CFG.phone + '.');
      if (form.dataset.clearCart) cart.set([]);
    }
  }));

  /* ---------- search page ---------- */
  const searchPage = $('[data-search-page]');
  if (searchPage) {
    const input = $('[data-search-input]'), results = $('[data-search-results]'), status = $('[data-search-status]');
    let index = null;
    const q0 = new URLSearchParams(location.search).get('q') || '';
    input.value = q0;
    function card(p) {
      const badge = p.compare_at ? '<span class="badge badge-sale">Sale</span>' : (p.badges || []).includes('Best seller') ? '<span class="badge">Best seller</span>' : (p.badges || []).includes('New') ? '<span class="badge">New</span>' : '';
      return '<a class="card" href="' + p.url + '"><span class="card-media"><img src="' + p.image + '" alt="" loading="lazy">' + badge + '</span><span class="card-metal">' + p.metal + '</span><span class="card-title">' + p.title + '</span><span class="card-price">' + money(p.price) + (p.compare_at ? ' <s>' + money(p.compare_at) + '</s>' : '') + '</span></a>';
    }
    function run() {
      const q = input.value.trim().toLowerCase();
      if (!index) return;
      if (!q) { results.innerHTML = ''; status.textContent = 'Type to search ' + index.length + ' pieces.'; return; }
      const terms = q.split(/\s+/);
      const hits = index.filter(p => { const hay = (p.title + ' ' + p.metal + ' ' + p.collection + ' ' + p.ptype + ' ' + (p.stone || '')).toLowerCase(); return terms.every(t => hay.includes(t)); });
      results.innerHTML = hits.slice(0, 60).map(card).join('');
      status.textContent = hits.length ? hits.length + ' pieces match "' + input.value.trim() + '"' : 'Nothing matches "' + input.value.trim() + '". Try a shorter word, or call ' + CFG.phone + '.';
      history.replaceState(null, '', BASE + '/search/?q=' + encodeURIComponent(input.value.trim()));
    }
    fetch(BASE + '/products.json').then(r => r.json()).then(d => { index = d; run(); });
    input.addEventListener('input', run);
    $('form', searchPage).addEventListener('submit', e => { e.preventDefault(); run(); });
  }
})();
