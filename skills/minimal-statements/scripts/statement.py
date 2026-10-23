"""Minimal statement card: '{ word word word }' built word by word, braces and corner dots spreading as words land.
Usage: python3 statement.py spec.json out.json
spec = {"label": "REBUTTAL 02", "label_t": 0.06, "words": ["networking","is","more","impactful"],
        "times": [1.27,1.87,2.19,2.33], "dur": 4.1}
times = seconds on the card's own clock (spoken word start - card start)."""
import json, sys
from common import *

def statement(label, label_t, words, times, dur, size=64, cy=545, move=0.3):
    times = list(times)
    for i in range(1, len(times)):          # moves must not overlap
        times[i] = max(times[i], times[i - 1] + move)
    sp, bw, n = width(' ', size), width('{', size), len(words)
    def layout(k):
        ws = [bw] + [width(w, size) for w in words[:k]] + [bw]
        gap = sp * 1.15 if k else sp * 2.2
        x = 960 - (sum(ws) + gap * (len(ws) - 1)) / 2; xs = []
        for wv in ws: xs.append(x); x += wv + gap
        d = {'L': xs[0], 'R': xs[-1]}
        for i in range(k): d['w%d' % i] = xs[i + 1]
        return d
    st = [layout(k) for k in range(n + 1)]; fin = st[n]; ts = [0] + times
    c = [{"type": "canvas.set", "canvas": {"duration": {"seconds": dur}}},
         {"type": "addShape", "nodeId": "bg", "start": 0, "duration": dur, "shape": "fill", "color": BG}]
    if label:
        lw = width(label, 26, 400) + 40
        c += title('label', label, 960 - lw / 2, cy - 120, 26, GREY, w=lw, align='center', dur=dur, wght=400, ls=0.08)
        c.append(keys('label', 'opacity', [(0, 0, None), (label_t, 0, 'easeOutCubic'), (label_t + 0.4, 1, None)]))
    c += title('L', '{', fin['L'], cy, size, dur=dur) + title('R', '}', fin['R'], cy, size, dur=dur)
    for i, w in enumerate(words): c += title('w%d' % i, w, fin['w%d' % i], cy, size, dur=dur)
    def offs(nid, first):
        ks, prev = [], None
        for k in range(first, n + 1):
            v = round(st[k][nid] - fin[nid], 1)
            if prev is None: ks.append((ts[k], v, None))
            else: ks += [(ts[k], prev, 'easeOutCubic'), (ts[k] + move, v, None)]
            prev = v
        if all(abs(k[1]) < 0.05 for k in ks): return []
        return [keys(nid, 'x', ks)]
    c += offs('L', 0) + offs('R', 0)
    for i in range(n):
        c += offs('w%d' % i, i + 1) + word_in('w%d' % i, times[i] + 0.03)
    for b in ('L', 'R'): c.append(keys(b, 'opacity', [(0, 0, 'easeOutCubic'), (0.25, 1, None)]))
    pad, ds = 70, 9
    lx, rx = fin['L'] - pad, fin['R'] + bw + pad - ds
    for nid, x, y, side in [('dTL', lx, cy - 95, 'L'), ('dBL', lx, cy + 95 - ds, 'L'), ('dTR', rx, cy - 95, 'R'), ('dBR', rx, cy + 95 - ds, 'R')]:
        c.append({"type": "addShape", "nodeId": nid, "start": 0, "duration": dur, "shape": "rect", "box": {"x": round(x, 1), "y": round(y, 1), "width": ds, "height": ds}, "color": INK})
        c.append({"type": "node.patch", "node": nid, "patch": {"common": {"transformParent": side}}})   # dots ride with the braces
        c.append(keys(nid, 'opacity', [(0, 0, 'easeOutCubic'), (0.25, 1, None)]))
    return c

if __name__ == '__main__':
    s = json.load(open(sys.argv[1]))
    dump(statement(s.get('label'), s.get('label_t', 0), s['words'], s['times'], s['dur']), sys.argv[2])
