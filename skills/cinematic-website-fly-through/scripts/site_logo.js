#!/usr/bin/env node
const HELP = `Take the site's own logo from its header (or its SVG favicon) and render it to a transparent PNG.

  node site_logo.js <url> --out logo.png [--min-width 1500] [--fill '#111111'] [--timeout 30]

Looks for an <svg> or <img> in the page header (top 150 px, left half) inside a link home
("/", "/home", "/homepage") or labelled as the logo; falls back to link[rel=icon][type=image/svg+xml]
and link[rel=mask-icon]. The SVG is redrawn with its computed colours at --min-width px across,
trimmed to its pixels. --fill paints every pixel of it one colour (keeps the edges' alpha), for a
logo that would vanish on the end card (a white logo on a light card).

Prints JSON: out, width, height, kind (wordmark when wider than 2:1, else symbol), source,
meanColor and meanLuminance (0-1) of the logo's pixels, and notes.
Exit codes: 0 ok, 3 no SVG logo on the page (go to Brandfetch, then list_library), 1 error, 2 timeout.
Needs playwright (npm i playwright; npx playwright install chromium).`;

const args = process.argv.slice(2);
if (!args.length || args.includes('--help') || args.includes('-h')) { console.log(HELP); process.exit(0); }
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const url = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const out = opt('--out', 'logo.png');
const minWidth = Number(opt('--min-width', 1500));
const fill = opt('--fill', null);
const timeoutS = Number(opt('--timeout', 30));
const fs = require('fs');
const { chromium } = require('playwright');

let browser, timedOut = false;
const timer = setTimeout(async () => {
  timedOut = true;
  console.error(`timed out after ${timeoutS} s`);
  try { await browser?.close(); } catch {}
  process.exit(2);
}, timeoutS * 1000);

function findLogo() {
  const homePaths = ['/', '', '/home', '/homepage', '/index.html'];
  const isHome = (a) => {
    if (!a) return false;
    const label = (a.getAttribute('aria-label') || '').toLowerCase();
    if (label.includes('home')) return true;
    try { const u = new URL(a.getAttribute('href') || 'x:', location.href); return u.origin === location.origin && homePaths.includes(u.pathname) && !u.hash; } catch { return false; }
  };
  const brand = location.hostname.replace(/^www\./, '').split('.')[0].toLowerCase();
  const cands = [];
  for (const el of document.querySelectorAll('svg, img')) {
    if (el.tagName.toLowerCase() === 'svg' && el.parentElement && el.parentElement.closest('svg')) continue;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (r.width < 16 || r.height < 8 || r.top < 0 || r.top > 150 || r.left > innerWidth / 2) continue;
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const a = el.closest('a');
    const text = [el.getAttribute('aria-label'), el.getAttribute('alt'), el.getAttribute('class'), el.id,
      el.querySelector && el.querySelector('title')?.textContent, a && a.getAttribute('aria-label')].join(' ').toLowerCase();
    let score = 0;
    if (isHome(a)) score += 3;
    if (text.includes('logo')) score += 2;
    if (brand && text.includes(brand)) score += 2;
    if (!score) continue;
    score += r.width / r.height > 2 ? 1 : 0;
    score -= r.left / innerWidth;
    cands.push({ el, score, r });
  }
  cands.sort((x, y) => y.score - x.score);
  const pick = cands[0];
  if (!pick) {
    const link = document.querySelector('link[rel~=icon][type="image/svg+xml"], link[rel=mask-icon]');
    return link ? { kind: 'url', src: link.href, source: 'favicon-svg', w: 512, h: 512 } : null;
  }
  const { el, r } = pick;
  if (el.tagName.toLowerCase() === 'img') {
    const src = el.currentSrc || el.src;
    const svg = /\.svg(\?|#|$)/i.test(src) || src.startsWith('data:image/svg');
    return { kind: 'url', src, source: svg ? 'header-img-svg' : 'header-img-raster', w: r.width, h: r.height, natural: el.naturalWidth };
  }
  // Redraw the svg with its computed paint inlined, and copy any defs it refers to from elsewhere in the page.
  const props = ['fill', 'fill-opacity', 'fill-rule', 'clip-rule', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-linecap',
    'stroke-linejoin', 'opacity', 'display', 'visibility', 'stop-color', 'stop-opacity', 'color'];
  const clone = el.cloneNode(true);
  const src = [el, ...el.querySelectorAll('*')], dst = [clone, ...clone.querySelectorAll('*')];
  src.forEach((s, i) => {
    const cs = getComputedStyle(s);
    dst[i].setAttribute('style', props.map((p) => `${p}:${cs.getPropertyValue(p)}`).join(';'));
  });
  const ids = new Set();
  clone.querySelectorAll('*').forEach((n) => {
    for (const at of n.attributes) {
      const m = at.value.match(/url\(["']?#([^"')]+)/) || (/(^|:)href$/.test(at.name) && at.value.startsWith('#') && [0, at.value.slice(1)]);
      if (m) ids.add(m[1]);
    }
    const st = n.getAttribute('style') || '';
    for (const m of st.matchAll(/url\(["']?#([^"')]+)/g)) ids.add(m[1]);
  });
  const defs = [...ids].filter((id) => !clone.querySelector('#' + CSS.escape(id))).map((id) => document.getElementById(id)).filter(Boolean);
  if (defs.length) {
    const d = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.forEach((n) => d.appendChild(n.cloneNode(true)));
    clone.insertBefore(d, clone.firstChild);
  }
  if (!clone.getAttribute('viewBox')) clone.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.removeAttribute('class');
  clone.removeAttribute('width');
  clone.removeAttribute('height');
  return { kind: 'svg', svg: clone.outerHTML, source: 'header-svg', w: r.width, h: r.height };
}

function analyse([dataUrl, fill]) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const g = c.getContext('2d');
      g.drawImage(img, 0, 0);
      const d = g.getImageData(0, 0, c.width, c.height).data;
      let x0 = c.width, y0 = c.height, x1 = -1, y1 = -1, n = 0, R = 0, G = 0, B = 0;
      for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) {
        const i = (y * c.width + x) * 4;
        if (d[i + 3] < 24) continue;
        x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
        const a = d[i + 3] / 255; n += a; R += d[i] * a; G += d[i + 1] * a; B += d[i + 2] * a;
      }
      if (x1 < 0) return resolve(null);
      const w = x1 - x0 + 1, h = y1 - y0 + 1;
      const t = document.createElement('canvas');
      t.width = w; t.height = h;
      const tg = t.getContext('2d');
      tg.drawImage(c, x0, y0, w, h, 0, 0, w, h);
      if (fill) { tg.globalCompositeOperation = 'source-in'; tg.fillStyle = fill; tg.fillRect(0, 0, w, h); }
      const mean = fill ? [1, 3, 5].map((k) => parseInt(fill.slice(k, k + 2), 16)) : [R / n, G / n, B / n];
      const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      const lum = 0.2126 * lin(mean[0]) + 0.7152 * lin(mean[1]) + 0.0722 * lin(mean[2]);
      resolve({ png: t.toDataURL('image/png'), width: w, height: h,
        meanColor: '#' + mean.map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), meanLuminance: +lum.toFixed(3) });
    };
    img.src = dataUrl;
  });
}

(async () => {
  if (!url) throw new Error('give the site URL');
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: timeoutS * 700 });
  await page.waitForTimeout(1500);
  const found = await page.evaluate(findLogo);
  const notes = [];
  if (!found || found.source === 'header-img-raster' && (found.natural || 0) < 600) {
    console.log(JSON.stringify({ error: 'no SVG logo on the page', found: found && found.source }));
    await browser.close();
    process.exit(3);
  }
  if (found.source === 'header-img-raster') notes.push(`raster logo ${found.natural} px wide: it is shown soft above ${Math.round(found.natural * 1.3)} px`);
  const ar = found.w / found.h;
  const w = ar >= 1 ? minWidth : Math.round(minWidth * ar);
  const h = Math.round(w / ar);
  const r = await browser.newPage({ viewport: { width: w + 40, height: h + 40 } });
  const body = found.kind === 'svg'
    ? found.svg.replace('<svg', `<svg width="${w}" height="${h}"`)
    : `<img src="${found.src}" width="${w}" height="${h}" style="object-fit:contain">`;
  await r.setContent(`<html><body style="margin:20px;background:transparent">${body}</body></html>`);
  await r.waitForLoadState('networkidle').catch(() => {});
  const shot = await r.locator('body > *').first().screenshot({ omitBackground: true });
  const a = await r.evaluate(analyse, ['data:image/png;base64,' + shot.toString('base64'), fill]);
  if (!a) throw new Error('the logo rendered empty');
  fs.writeFileSync(out, Buffer.from(a.png.split(',')[1], 'base64'));
  const kind = a.width / a.height > 2 ? 'wordmark' : 'symbol';
  if (found.source === 'favicon-svg') notes.push('no logo in the header: this is the SVG favicon (a symbol)');
  console.log(JSON.stringify({ out, width: a.width, height: a.height, kind, source: found.source, meanColor: a.meanColor,
    meanLuminance: a.meanLuminance, fill: fill || undefined, notes }, null, 1));
  clearTimeout(timer);
  await browser.close();
})().catch(async (e) => {
  if (timedOut) return;
  console.error(String(e).split('\n')[0]);
  try { await browser?.close(); } catch {}
  process.exit(1);
});
