"""Minimal statement, image-inset variant: '{ builder }' splits into '{ build [image] er }', the halves turn accent pink,
grey arrows slide in at the sides, and the image slot cycles through one photo per spoken item (with a small grey caption),
then the word closes back to '{ builder }'. Full-frame B-ROLL, hard cut in and out.
Usage: python3 inset.py spec.json out.json
spec = {"left": "build", "right": "er", "dur": 8.3, "open_t": 0.45, "close_t": 7.1,
        "images": [{"uri": "https://ucarecdn.com/.../", "w": 400, "h": 300, "caption": "videos", "t": 0.45}, ...]}
times = seconds on the card's clock; image i shows from its t until the next image's t. Split the word where it reads
naturally (build|er, intro|ducing, port|folio)."""
import json, sys
from common import *

def inset(s, S=64, cy=545, slot_w=170, slot_h=110, g=22, mv=0.4):
    dur, t_open, t_close = s['dur'], s.get('open_t', 0.45), s['close_t']
    wl, wr = s['left'], s['right']
    sp = width(' ', S) * 1.15; bw = width('{', S); a, b = width(wl, S), width(wr, S)
    tj = bw + sp + a + b + sp + bw; xj = 960 - tj / 2
    J = dict(L=xj, B=xj + bw + sp, E=xj + bw + sp + a, R=xj + bw + sp + a + b + sp)
    tp = bw + sp + a + g + slot_w + g + b + sp + bw; xp = 960 - tp / 2
    P = dict(L=xp, B=xp + bw + sp, SL=xp + bw + sp + a + g); P['E'] = P['SL'] + slot_w + g; P['R'] = P['E'] + b + sp
    c = [{"type": "canvas.set", "canvas": {"duration": {"seconds": dur}}},
         {"type": "addShape", "nodeId": "bg", "start": 0, "duration": dur, "shape": "fill", "color": BG}]
    for nid, txt in (('L', '{'), ('R', '}'), ('B', wl), ('E', wr)):
        c += title(nid, txt, P[nid], cy, S, dur=dur)
    for nid in 'LRBE':
        d = round(J[nid] - P[nid], 1)
        c.append(keys(nid, 'x', [(0, d, None), (t_open, d, 'easeOutCubic'), (t_open + mv, 0, None), (t_close, 0, 'easeInOutCubic'), (t_close + mv, d, None)]))
        c.append(keys(nid, 'opacity', [(0, 0, 'easeOutCubic'), (0.25, 1, None)]))
    for nid in 'BE':
        c.append(keys(nid, 'color', [(0, INK, None), (t_open, INK, 'easeOutCubic'), (t_open + mv, ACCENT, None), (t_close, ACCENT, 'easeOutCubic'), (t_close + mv, INK, None)]))
    c += title('aL', '\u2190', P['L'] - 120, cy, 40, GREY, w=80, dur=dur, wght=400)
    c += title('aR', '\u2192', P['R'] + bw + 50, cy, 40, GREY, w=80, dur=dur, wght=400)
    for nid, dx in (('aL', 30), ('aR', -30)):
        c.append(keys(nid, 'opacity', [(0, 0, None), (t_open, 0, 'easeOutCubic'), (t_open + 0.5, 1, None), (t_close, 1, 'easeOutCubic'), (t_close + 0.3, 0, None)]))
        c.append(keys(nid, 'x', [(0, dx, None), (t_open, dx, 'easeOutCubic'), (t_open + 0.6, 0, None)]))
    imgs = s['images']; sx, sy = P['SL'], cy - slot_h / 2 - 4
    for i, im in enumerate(imgs):
        t0 = im['t']; t1 = imgs[i + 1]['t'] if i + 1 < len(imgs) else t_close + mv
        nid, aid = 'im%d' % i, 'img.in%d' % i
        c.append(image_asset(aid, im['uri'], im['w'], im['h']))
        c.append(raster(nid, aid, sx, sy, slot_w, slot_h, t0, t1 - t0, im.get('caption')))
        c.append({"type": "setProperty", "node": nid, "property": "cornerRadius", "value": 10})
        if i == 0: c.append(keys(nid, 'scale', [(t0, 0, 'easeOutCubic'), (t0 + mv, 1, None)]))
        if i == len(imgs) - 1: c.append(keys(nid, 'scale', [(t_close, 1, 'easeInOutCubic'), (t_close + mv, 0, None)]))
        if im.get('caption'):
            cw = width(im['caption'], 24, 400) + 40
            cd = t1 - t0 - (mv if i == len(imgs) - 1 else 0)
            c += title('cap%d' % i, im['caption'], 960 - cw / 2, cy + 110, 24, GREY, w=cw, align='center', start=t0, dur=round(cd, 3), wght=400, ls=0.04)
    pad, ds = 70, 9
    lx, rx = P['L'] - pad, P['R'] + bw + pad - ds
    for nid, x, y, side in [('dTL', lx, cy - 110, 'L'), ('dBL', lx, cy + 110 - ds, 'L'), ('dTR', rx, cy - 110, 'R'), ('dBR', rx, cy + 110 - ds, 'R')]:
        c.append({"type": "addShape", "nodeId": nid, "start": 0, "duration": dur, "shape": "rect", "box": {"x": round(x, 1), "y": round(y, 1), "width": ds, "height": ds}, "color": INK})
        c.append({"type": "node.patch", "node": nid, "patch": {"common": {"transformParent": side}}})
        c.append(keys(nid, 'opacity', [(0, 0, 'easeOutCubic'), (0.25, 1, None)]))
    return c

if __name__ == '__main__':
    dump(inset(json.load(open(sys.argv[1]))), sys.argv[2])
