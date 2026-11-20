#!/usr/bin/env node
const HELP = `Read a site's own brand from its CSS.

  node site_brand.js <url> [--timeout 25]

Prints JSON: title, background, text, headingColor, primary (up to 4 saturated, not near-black button / link
colours, most used first), headingFont, headingWeight, bodyFont, themeColor. Every colour is 6-digit hex
(#RRGGBB): oklch(), oklab(), lab(), lch(), color() and rgb() values are all converted through the
browser's own colour parser. A colour under 50 % alpha counts as none.
Stops after --timeout seconds (default 25) with exit code 2. Needs playwright.`;

const args = process.argv.slice(2);
if (!args.length || args.includes('--help') || args.includes('-h')) { console.log(HELP); process.exit(0); }
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const url = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const timeoutS = Number(opt('--timeout', 25));
const { chromium } = require('playwright');

let browser, timedOut = false;
const timer = setTimeout(async () => {
  timedOut = true;
  console.error(`timed out after ${timeoutS} s`);
  try { await browser?.close(); } catch {}
  process.exit(2);
}, timeoutS * 1000);

(async () => {
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: timeoutS * 700 });
  await page.waitForTimeout(1500);
  const out = await page.evaluate(() => {
    const g = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
    g.canvas.width = g.canvas.height = 1;
    const hex = (c) => {
      if (!c || c === 'transparent') return null;
      g.clearRect(0, 0, 1, 1);
      g.fillStyle = '#000';
      g.fillStyle = c;
      g.fillRect(0, 0, 1, 1);
      const [r, gg, b, a] = g.getImageData(0, 0, 1, 1).data;
      if (a < 128) return null;
      return '#' + [r, gg, b].map((v) => v.toString(16).padStart(2, '0')).join('').toUpperCase();
    };
    const sat = (h) => { const n = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255); const mx = Math.max(...n), mn = Math.min(...n); return mx ? (mx - mn) / mx : 0; };
    const cs = (el) => getComputedStyle(el);
    const tally = {};
    const val = (h) => Math.max(...[1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))) / 255;
    const add = (h, w) => { if (h && sat(h) > 0.35 && val(h) > 0.3) tally[h] = (tally[h] || 0) + w; };
    [...document.querySelectorAll('button, a, [role=button], input[type=submit]')].slice(0, 400).forEach((el) => {
      const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
      add(hex(cs(el).backgroundColor), 3 * Math.min(r.width * r.height, 20000)); add(hex(cs(el).color), 2000);
    });
    const h = document.querySelector('h1, h2') || document.body;
    const meta = document.querySelector('meta[name="theme-color"]');
    return { title: document.title, background: hex(cs(document.body).backgroundColor) || hex(cs(document.documentElement).backgroundColor) || '#FFFFFF',
      text: hex(cs(document.body).color), headingColor: hex(cs(h).color),
      primary: Object.entries(tally).sort((a, b) => b[1] - a[1]).slice(0, 4).map((e) => e[0]),
      headingFont: cs(h).fontFamily.split(',')[0].replace(/["']/g, '').trim(), headingWeight: cs(h).fontWeight,
      bodyFont: cs(document.body).fontFamily.split(',')[0].replace(/["']/g, '').trim(), themeColor: meta ? hex(meta.content) : null };
  });
  console.log(JSON.stringify(out, null, 1));
  clearTimeout(timer);
  await browser.close();
})().catch(async (e) => {
  if (timedOut) return;
  console.error(String(e).split('\n')[0]);
  try { await browser?.close(); } catch {}
  process.exit(1);
});
