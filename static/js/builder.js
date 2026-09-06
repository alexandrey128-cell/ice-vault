/* Engagement ring builder: live preview + price estimate. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const root = $('[data-builder]'); if (!root) return;
  const months = +document.body.dataset.months || 12;
  const BASE = document.body.dataset.base || '';
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const COLOR_NAMES = { Y: 'Yellow Gold', W: 'White Gold', R: 'Rose Gold' };
  const SETTING_NAMES = { solitaire: 'Solitaire', 'hidden-halo': 'Hidden halo', halo: 'Halo', 'three-stone': 'Three stone', pave: 'Pave band', cathedral: 'Cathedral' };
  const SHAPE_FACTOR = { round: 1, oval: .88, emerald: .82, cushion: .85, radiant: .84, pear: .86, marquise: .84, princess: .85 };

  function state() {
    const setting = $('input[name=setting]:checked'), metal = $('input[name=metal]:checked'), shape = $('input[name=shape]:checked');
    return {
      setting: setting.value, base: +setting.dataset.base,
      purity: metal.dataset.purity, color: metal.dataset.color, mult: +metal.dataset.mult,
      shape: shape.value, carat: +$('[data-carat]').value, origin: $('input[name=origin]:checked').value,
      colorF: +$('[data-dcolor]').value, colorG: $('[data-dcolor]').selectedOptions[0].text.split(' ')[0],
      clarF: +$('[data-dclarity]').value, clarG: $('[data-dclarity]').selectedOptions[0].text,
    };
  }
  function diamondPrice(s) {
    const ct = s.carat;
    const perCt = s.origin === 'lab' ? 980 * Math.pow(ct, .45) : 4100 * Math.pow(ct, .95);
    return Math.round(perCt * ct * s.colorF * s.clarF * SHAPE_FACTOR[s.shape] / 50) * 50;
  }
  function update() {
    const s = state();
    const settingPrice = Math.round(s.base * s.mult / 10) * 10;
    const dPrice = diamondPrice(s);
    const total = settingPrice + dPrice;
    const size = s.carat < 1.1 ? 's' : s.carat < 2.2 ? 'm' : 'l';
    const chosen = $('input[name=setting]:checked').closest('.opt').querySelector('img'); if (chosen) $('[data-preview]').src = chosen.dataset.photo || chosen.src;
    $('[data-carat-out]').textContent = s.carat.toFixed(2);
    $('[data-sum-setting]').textContent = SETTING_NAMES[s.setting];
    $('[data-sum-metal]').textContent = s.purity === 'Platinum' ? 'Platinum' : s.purity + ' ' + COLOR_NAMES[s.color];
    const dia = s.carat.toFixed(2) + ' ct ' + s.shape + ', ' + (s.origin === 'lab' ? 'lab grown' : 'natural') + ', ' + s.colorG + ' ' + s.clarG;
    $('[data-sum-diamond]').textContent = dia;
    const totalEl = $('[data-total]'); const from = +(totalEl.dataset.value || 0); totalEl.dataset.value = total;
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && from) {
      const t0 = performance.now(); const step = now => { const k = Math.min(1, (now - t0) / 300); const e = 1 - Math.pow(1 - k, 3); totalEl.textContent = money(from + (total - from) * e); if (k < 1) requestAnimationFrame(step); }; requestAnimationFrame(step);
    } else totalEl.textContent = money(total);
    $('[data-setting-price]').textContent = money(settingPrice);
    $('[data-diamond-price]').textContent = money(dPrice);
    $('[data-monthly]').textContent = money(total / months);
    const summary = SETTING_NAMES[s.setting] + ' in ' + $('[data-sum-metal]').textContent + ' with a ' + dia + '. Estimate ' + money(total) + '.';
    $('[data-request-summary]').textContent = summary;
    $('[data-request-field]').value = summary;
  }
  root.addEventListener('change', update);
  root.addEventListener('input', update);
  $$('[data-request-open]').forEach(b => b.addEventListener('click', () => $('#request').showModal()));
  update();
})();
