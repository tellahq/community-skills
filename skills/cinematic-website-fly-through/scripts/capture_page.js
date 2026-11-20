#!/usr/bin/env node
const HELP = `Capture the full-page screenshot for the fly-through: 1280 px wide at 2x (2560 px image).

  node capture_page.js <url> --out page.png [--max-image-px 6000] [--container '<css>'] [--timeout 90]

Before capturing it:
- clicks the accept button of a cookie / consent banner, then hides whatever banner stays up (display: none);
- scrolls to the bottom in 600 px steps (250 ms apart) and back to the top, so lazy-loaded sections are in;
- when the document is one screen tall and an inner element scrolls instead (e.g. .app-scroll-viewport), finds
  that element (or takes --container) and sets the viewport height to its scrollHeight.
Always 2x; the image is cropped to the top --max-image-px IMAGE pixels (default 6000), never shrunk to 1x.

Prints JSON: out, imageWidth, imageHeight (pass these to create_source and the spec's page), cssHeight,
container (the selector used, or null), cropped (true when the page was taller), cookie (clicked / hidden).
Exit codes: 0 ok, 1 error, 2 timeout. Needs playwright.`;

const args = process.argv.slice(2);
if (!args.length || args.includes('--help') || args.includes('-h')) { console.log(HELP); process.exit(0); }
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const url = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const out = opt('--out', 'page.png');
const maxImage = Number(opt('--max-image-px', 6000));
const forced = opt('--container', null);
const timeoutS = Number(opt('--timeout', 90));
const WIDTH = 1280, DPR = 2, VIEW_H = 800;
const { chromium } = require('playwright');

let browser, timedOut = false;
const timer = setTimeout(async () => {
  timedOut = true;
  console.error(`timed out after ${timeoutS} s`);
  try { await browser?.close(); } catch {}
  process.exit(2);
}, timeoutS * 1000);

const HIDE_CSS = `[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=consent i],[aria-label*=cookie i],[aria-label*=consent i],
#onetrust-consent-sdk,#CybotCookiebotDialog,.cky-consent-container,#usercentrics-root,.osano-cm-window,#hs-eu-cookie-confirmation
{display:none !important}`;

async function dismissCookies(page) {
  const clicked = await page.evaluate(() => {
    const words = /^(accept( all)?( cookies)?|allow( all)?( cookies)?|agree|i agree|got it|ok(ay)?|accept & close|alle akzeptieren|tout accepter)$/i;
    const inBanner = (el) => !!el.closest('[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=consent i],[aria-label*=cookie i],[role=dialog],[aria-modal=true]')
      || /cookie|consent|privacy/i.test((el.closest('div,section,aside,footer') || {}).innerText || '');
    for (const b of document.querySelectorAll('button, a, [role=button]')) {
      const t = (b.innerText || b.getAttribute('aria-label') || '').trim();
      const r = b.getBoundingClientRect();
      if (t.length < 40 && words.test(t) && r.width && r.height && inBanner(b)) { b.click(); return t; }
    }
    return null;
  });
  if (clicked) await page.waitForTimeout(600);
  return clicked;
}

async function hideCookies(page) {
  await page.addStyleTag({ content: HIDE_CSS });
  return page.evaluate(() => {
    let n = 0;
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
      const r = el.getBoundingClientRect();
      if (r.height > innerHeight * 0.6 || r.top < 100 && r.height < 120 && !/cookie|consent/i.test(el.innerText)) continue;
      if (/cookie|consent|we use|privacy/i.test(el.innerText || '') && (el.innerText || '').length < 1500) { el.style.setProperty('display', 'none', 'important'); n++; }
    }
    return n;
  });
}

(async () => {
  browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: WIDTH, height: VIEW_H }, deviceScaleFactor: DPR });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: Math.min(45, timeoutS / 2) * 1000 });
  await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1200);
  const clicked = await dismissCookies(page);
  let hidden = await hideCookies(page);

  // Which element scrolls: the document, or a container inside it.
  const container = await page.evaluate((forced) => {
    const doc = document.scrollingElement || document.documentElement;
    if (!forced && doc.scrollHeight > innerHeight + 50) return null;
    let best = forced ? document.querySelector(forced) : null;
    if (!best) {
      let max = 0;
      for (const el of document.querySelectorAll('body *')) {
        const oy = getComputedStyle(el).overflowY;
        if ((oy === 'auto' || oy === 'scroll' || oy === 'overlay') && el.scrollHeight > el.clientHeight + 50 && el.clientWidth > innerWidth * 0.6 && el.scrollHeight > max) { max = el.scrollHeight; best = el; }
      }
    }
    if (!best) return null;
    best.setAttribute('data-fly-scroll', '1');
    return forced || (best.id ? '#' + best.id : best.tagName.toLowerCase() + (best.className && typeof best.className === 'string' ? '.' + best.className.trim().split(/\s+/).join('.') : ''));
  }, forced);
  const scroller = container ? '[data-fly-scroll]' : null;

  // Scroll through for lazy loading, then back to the top.
  await page.evaluate(async (sel) => {
    const el = sel ? document.querySelector(sel) : (document.scrollingElement || document.documentElement);
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    for (let i = 0; i < 80 && el.scrollTop + el.clientHeight < el.scrollHeight - 4; i++) { el.scrollBy(0, 600); await wait(250); }
    await wait(1500);
    el.scrollTo(0, 0);
    await wait(1000);
  }, scroller);
  if (!clicked) await dismissCookies(page);
  hidden += await hideCookies(page);

  const maxCss = Math.floor(maxImage / DPR);
  const full = await page.evaluate((sel) => {
    const el = sel ? document.querySelector(sel) : (document.scrollingElement || document.documentElement);
    return el.scrollHeight;
  }, scroller);
  const cssHeight = Math.min(full, maxCss);
  if (scroller) {
    const chrome = await page.evaluate((sel) => innerHeight - document.querySelector(sel).clientHeight, scroller);
    await page.setViewportSize({ width: WIDTH, height: Math.min(full + Math.max(0, chrome), maxCss) });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: WIDTH, height: Math.min(full + Math.max(0, chrome), maxCss) } });
  } else {
    await page.screenshot({ path: out, fullPage: true, clip: { x: 0, y: 0, width: WIDTH, height: cssHeight } });
  }
  const png = require('fs').readFileSync(out);
  const imageWidth = png.readUInt32BE(16), imageHeight = png.readUInt32BE(20);
  console.log(JSON.stringify({ out, imageWidth, imageHeight, cssHeight: imageHeight / DPR, container, cropped: full > maxCss,
    cookie: { clicked, hidden } }, null, 1));
  clearTimeout(timer);
  await browser.close();
})().catch(async (e) => {
  if (timedOut) return;
  console.error(String(e).split('\n')[0]);
  try { await browser?.close(); } catch {}
  process.exit(1);
});
