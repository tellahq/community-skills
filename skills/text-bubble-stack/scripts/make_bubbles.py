#!/usr/bin/env python3
"""Render skeuomorphic (iOS 6 style) chat bubbles and the white gradient wash.

Usage: python3 make_bubbles.py spec.json OUTDIR
spec.json:
{
  "texts": ["No", "Nope", "Nooooope!"],
  "fontSize": 88,
  "theme": {"top": "#F3ECFF", "mid": "#CDB8F4", "bottom": "#A98AE8",
            "outline": "#4A45A0", "shadow": "#312E81"},
  "canvas": {"width": 1080, "height": 1920},
  "wash": {"top": 1.0, "bottom": 0.1}
}
Writes bubble_<i>.png (3x scale, 170 px tall at 1x, tail bottom-right) and wash.png,
and prints JSON with each bubble's 1x width W and pixel size, for the motion document.
"""
import json, sys, os, subprocess
from playwright.sync_api import sync_playwright

spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
t = spec["theme"]; FS = spec.get("fontSize", 88); PAD = 48; TAIL = 16

def svg(W):
    R = W - TAIL
    return f'''<svg width="{W*3}" height="510" viewBox="0 0 {W} 170" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['top']}"/><stop offset="0.5" stop-color="{t['mid']}"/><stop offset="1" stop-color="{t['bottom']}"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.2"/></linearGradient>
<filter id="s" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2.5" stdDeviation="2" flood-color="{t.get('shadow', t['outline'])}" flood-opacity="0.35"/></filter></defs>
<path filter="url(#s)" d="M60 6 H{R-54} A54 54 0 0 1 {R} 60 V122 C{R} 140 {R+4} 152 {R+12} 160 C{R-2} 162 {R-16} 156 {R-24} 150 C{R-32} 154 {R-44} 156 {R-54} 156 H60 A54 54 0 0 1 6 102 V60 A54 54 0 0 1 60 6 Z" fill="url(#g)" stroke="{t['outline']}" stroke-width="2.2"/>
<path d="M58 11 H{R-52} A44 44 0 0 1 {R-8} 55 V58 C{R-8} 66 {R-14} 70 {R-22} 70 H28 C18 70 12 64 12 56 A44 44 0 0 1 58 11 Z" fill="url(#gl)"/></svg>'''

res = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.set_content('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=block" rel="stylesheet"><span id=t style="font-family:Inter;font-size:%dpx">x</span>' % FS)
    pg.wait_for_timeout(1500)
    for i, txt in enumerate(spec["texts"]):
        tw = pg.evaluate("w=>{const t=document.getElementById('t');t.textContent=w;return t.getBoundingClientRect().width}", txt)
        W = max(int(tw + 2*PAD + TAIL), 200)
        q = b.new_page(viewport={'width': W*3, 'height': 510})
        q.set_content('<html><body style="margin:0;background:transparent">' + svg(W) + '</body></html>')
        f = os.path.join(out, f"bubble_{i+1}.png"); q.screenshot(path=f, omit_background=True); q.close()
        res.append({"text": txt, "W": W, "file": f, "px": [W*3, 510]})
    b.close()
c = spec.get("canvas", {"width": 1080, "height": 1920}); w = spec.get("wash", {"top": 1.0, "bottom": 0.1})
wf = os.path.join(out, "wash.png")
subprocess.run(["convert", "-size", f"{c['width']}x{c['height']}",
                f"gradient:rgba(255,255,255,{w['top']})-rgba(255,255,255,{w['bottom']})", f"PNG32:{wf}"], check=True)
print(json.dumps({"bubbles": res, "wash": wf}))
