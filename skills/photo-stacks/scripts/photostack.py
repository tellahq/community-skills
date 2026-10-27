"""Photo stacks in Louise's minimal set. Two variants, selectable speeds.
Usage: python3 photostack.py spec.json out.json
fan      = cards slide out of one pile into a 3D fan (rotateY 32) beside the presenter: a transparent OVERLAY.
cascade  = cards land one by one, small to large, on light grey with a word either side: full-frame B-ROLL.
spec (fan):     {"variant":"fan","speed":"medium","dur":5.1,"t_in":0.1,"side":"right","label":"fashion & wardrobe",
                 "images":[{"uri":"https://ucarecdn.com/.../","w":1200,"h":1800}, ...]}
spec (cascade): {"variant":"cascade","speed":"word","dur":7.7,
                 "images":[{"uri":...,"w":1200,"h":1053,"t":0.42,"name":"reading"}, ...],
                 "left_word":{"text":"you","t":4.78},"right_word":{"text":"build","t":6.24}}
speed: slow | medium (the reference fan) | fast | word (cascade: each card on its own spoken word, the reference)."""
import json, sys
from common import *

SPEEDS = {  # entrance length, gap between cards, drift over the whole stack
    'slow':   dict(ent=0.9, stag=0.32, drift=30),
    'medium': dict(ent=0.6, stag=0.14, drift=24),
    'fast':   dict(ent=0.35, stag=0.06, drift=12),
}

def fan(s):
    sp = SPEEDS[s.get('speed', 'medium') if s.get('speed') in SPEEDS else 'medium']
    dur, t_in = s['dur'], s.get('t_in', 0.1); t_out = dur
    imgs = s['images']; n = len(imgs)
    cxs = 1540 if s.get('side', 'right') == 'right' else 380
    cw, ch, cy, step = 210, 315, 500, 85
    centers = [cxs + (i - (n - 1) / 2) * step for i in range(n)]
    c = [{"type": "canvas.set", "canvas": {"duration": {"seconds": dur}}}]
    for i, im in enumerate(imgs):
        nid, aid = 'f%d' % i, 'img.f%d' % i
        c.append(image_asset(aid, im['uri'], im['w'], im['h']))
        c.append(raster(nid, aid, centers[i] - cw / 2, cy - ch / 2, cw, ch, t_in, t_out - t_in, im.get('name')))
        for p, v in (('perspective', 1100), ('cornerRadius', 6), ('shadowOpacity', 0.3), ('shadowBlur', 30), ('shadowX', -12)):
            c.append({"type": "setProperty", "node": nid, "property": p, "value": v})
        ts = t_in + i * sp['stag']; dx = round(cxs - centers[i], 1)
        c.append(keys(nid, 'x', [(t_in, dx, None), (ts, dx, 'easeOutCubic'), (ts + sp['ent'], 0, 'linear'), (t_out, -sp['drift'], None)]))
        c.append(keys(nid, 'rotateY', [(ts, 0, 'easeOutCubic'), (ts + sp['ent'], 32, None)]))
        c.append(keys(nid, 'opacity', [(t_in, 0, None), (ts, 0, 'easeOutCubic'), (ts + sp['ent'] / 2, 1, None), (t_out - 0.3, 1, 'easeInCubic'), (t_out, 0, None)]))
        c.append(keys(nid, 'scale', [(ts, 0.7, 'easeOutCubic'), (ts + sp['ent'], 1, None)]))
    if s.get('label'):
        lw = width(s['label'], 24, 500) + 48
        c.append({"type": "addShape", "nodeId": "fpill", "start": t_in, "duration": round(t_out - t_in, 3), "shape": "rect", "box": {"x": round(cxs - lw / 2, 1), "y": 700, "width": round(lw, 1), "height": 48}, "color": CARD, "radius": 24})
        c += title('flab', s['label'], cxs - lw / 2, 724, 24, INK, w=lw, align='center', start=t_in, dur=round(t_out - t_in, 3), wght=500)
        c.append({"type": "group", "nodes": ["fpill", "flab"], "nodeId": "fl", "name": "stack label"})
        tl = t_in + sp['ent'] * 0.8
        c.append(keys('fl', 'opacity', [(tl, 0, 'easeOutCubic'), (tl + 0.4, 1, None), (t_out - 0.3, 1, 'easeInCubic'), (t_out, 0, None)]))
        c.append(keys('fl', 'y', [(tl, 20, 'easeOutCubic'), (tl + 0.4, 0, None)]))
    return c

def cascade(s):
    speed = s.get('speed', 'word')
    sp = SPEEDS.get(speed, SPEEDS['medium']); ent = {'word': 0.5}.get(speed, sp['ent'] * 0.85)
    dur, imgs = s['dur'], s['images']; n = len(imgs)
    t0 = s.get('t_in', 0.3)
    ws = [190 + (280 - 190) * i / max(n - 1, 1) for i in range(n)]
    hs = [min(max(w * im['h'] / im['w'], 0.7 * w), 1.5 * w) for w, im in zip(ws, imgs)]
    cx = [0.0]
    for i in range(1, n): cx.append(cx[-1] + (ws[i - 1] / 2 + ws[i] / 2) * 0.55)
    shift = 940 - (cx[0] - ws[0] / 2 + cx[-1] + ws[-1] / 2) / 2; cx = [x + shift for x in cx]
    cys = [560 - 10 * i * 3 / max(n - 1, 1) for i in range(n)]
    c = [{"type": "canvas.set", "canvas": {"duration": {"seconds": dur}}},
         {"type": "addShape", "nodeId": "bg", "start": 0, "duration": dur, "shape": "fill", "color": BG}]
    ids = []
    for i, im in enumerate(imgs):
        nid = im.get('name', 'p%d' % i).replace(' ', '_'); aid = 'img.%s' % nid; ids.append(nid)
        c.append(image_asset(aid, im['uri'], im['w'], im['h']))
        c.append(raster(nid, aid, cx[i] - ws[i] / 2, cys[i] - hs[i] / 2, ws[i], hs[i], 0, dur, nid))
        for p, v in (('perspective', 1200), ('cornerRadius', 4), ('shadowOpacity', 0.25), ('shadowBlur', 30), ('shadowX', -10), ('rotateY', 16)):
            c.append({"type": "setProperty", "node": nid, "property": p, "value": v})
        t = im['t'] if speed == 'word' and 't' in im else t0 + i * sp['stag'] * 2.2
        ts = max(t - 0.1, 0)
        c.append(keys(nid, 'opacity', [(0, 0, None), (ts, 0, 'easeOutCubic'), (ts + ent * 0.6, 1, None)]))
        c.append(keys(nid, 'y', [(ts, 70, 'easeOutCubic'), (ts + ent, 0, None)]))
        c.append(keys(nid, 'scale', [(ts, 0.85, 'easeOutCubic'), (ts + ent, 1, None)]))
    c.append({"type": "group", "nodes": ids, "nodeId": "stack", "name": "photo stack"})
    d = sp['drift'] if speed in SPEEDS else 20
    c.append(keys('stack', 'x', [(0, d, 'linear'), (dur, -d, None)]))
    left = cx[0] - ws[0] / 2 - 40; right = cx[-1] + ws[-1] / 2 + 40
    for key, al in (('left_word', 'right'), ('right_word', 'left')):
        w = s.get(key)
        if not w: continue
        nid = 'lw' if al == 'right' else 'rw'
        tw = width(w['text'], 64) + 60
        x = left - tw if al == 'right' else right
        c += title(nid, w['text'], x, 545, 64, INK, w=tw, align=al, dur=dur)
        c += word_in(nid, w['t'], dx=(-30 if al == 'right' else 30))
    return c

if __name__ == '__main__':
    s = json.load(open(sys.argv[1]))
    dump(fan(s) if s.get('variant', 'fan') == 'fan' else cascade(s), sys.argv[2])
