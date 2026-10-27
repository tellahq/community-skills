"""Exploded-view / teardown animation builder for Tella Motion.

A *model* is a Python module with:
  build()   -> list[Part]    geometry at the current yaw (call set_yaw() first); parts in paint
                              order, back to front. Point counts must not depend on yaw.
  EXPLODE   -> {part: (dx, dy, dz)} explode offsets in mm (model axes, z up). (0,0,0) = stays.
  LABELS    -> [(text, part, (x, y, z) anchor in mm on the assembled part, 'L'|'R'), ...]
  DRAW      -> optional {part: (start_s, duration_s)} parts visible when assembled get a
               trim-path draw-on; parts not listed are hidden inside and only appear on explode.
Run:  python3 explode.py path/to/model.py [--out DIR] [--preview]
Writes batch_N.json (each <= ~38k chars, one command per item) ready to paste into
tella__apply_motion_editor_commands, plus optional preview PNGs at key times.
"""
import math, json, sys, os, importlib.util
import numpy as np
from shapely.geometry import Polygon, LineString, MultiPoint, Point

# ---------------------------------------------------------------- projection
CFG = dict(S=5.0, CX=960.0, CY=540.0, YAW=0.0)
C30, S30 = math.cos(math.radians(30)), 0.5

def set_view(scale=None, cx=None, cy=None):
    if scale is not None: CFG['S'] = scale
    if cx is not None: CFG['CX'] = cx
    if cy is not None: CFG['CY'] = cy

def set_yaw(deg): CFG['YAW'] = float(deg)

def P(pts):
    """(N,3) mm -> (N,2) px. Isometric, z up; +x goes right-down, +y left-down. Yaw about z first."""
    p = np.asarray(pts, float).reshape(-1, 3)
    c, s = math.cos(math.radians(CFG['YAW'])), math.sin(math.radians(CFG['YAW']))
    p = np.column_stack([p[:, 0]*c - p[:, 1]*s, p[:, 0]*s + p[:, 1]*c, p[:, 2]])
    S = CFG['S']
    return np.column_stack([CFG['CX'] + (p[:, 0]-p[:, 1])*C30*S,
                            CFG['CY'] + (p[:, 0]+p[:, 1])*S30*S - p[:, 2]*S])

def offset_px(d, yaw=None):
    """Screen offset (px) of a model-space offset d=(dx,dy,dz) mm at a yaw."""
    yaw = CFG['YAW'] if yaw is None else yaw
    dx, dy, dz = d; c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    x, y = dx*c - dy*s, dx*s + dy*c; S = CFG['S']
    return ((x - y)*C30*S, (x + y)*S30*S - dz*S)

# ---------------------------------------------------------------- 2D outlines (mm)
def rrect(w, h, r, n=6):
    r = min(r, w/2, h/2); pts = []
    for cx, cy, a0 in [(w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)]:
        for i in range(n+1):
            a = math.radians(a0 + 90*i/n); pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return np.array(pts)

def circle(r, n=32): return ellipse(r, r, n)
def ellipse(rx, ry, n=32):
    return np.array([(rx*math.cos(2*math.pi*i/n), ry*math.sin(2*math.pi*i/n)) for i in range(n)])

def resample_closed(pts, n=64):
    """Any closed outline (e.g. traced from SVG/PDF/raster) -> n points evenly by arc length,
    centred on its centroid. Use for custom profiles so point counts are fixed."""
    pts = np.asarray(pts, float); ring_ = LineString(np.vstack([pts, pts[:1]]))
    out = np.array([ring_.interpolate(ring_.length*i/n).coords[0] for i in range(n)])
    c = np.array(Polygon(out).centroid.coords[0]); return out - c

def lift(o2, plane, k, off=(0, 0)):
    """2D outline -> 3D. 'xy' at z=k (2D=(x,y)); 'yz' at x=k (2D=(y,z)); 'xz' at y=k (2D=(x,z))."""
    o = np.asarray(o2, float) + np.asarray(off, float); kk = np.full(len(o), float(k))
    return {'xy': lambda: np.column_stack([o[:, 0], o[:, 1], kk]),
            'yz': lambda: np.column_stack([kk, o[:, 0], o[:, 1]]),
            'xz': lambda: np.column_stack([o[:, 0], kk, o[:, 1]])}[plane]()

def ring(a): a = np.asarray(a); return np.vstack([a, a[:1]])

def radial(poly, M=64):
    """Convex/star-shaped polygon -> exactly M boundary points by rays from the centroid.
    Needed for silhouettes (convex hulls) whose vertex count would change with yaw."""
    c = np.array(poly.centroid.coords[0]); ext = LineString(poly.exterior.coords); out = []
    for k in range(M):
        a = 2*math.pi*k/M; ray = LineString([c, c + 5000*np.array([math.cos(a), math.sin(a)])])
        q = ray.intersection(ext)
        if q.geom_type != 'Point': q = min(getattr(q, 'geoms', [q]), key=lambda g: g.distance(Point(c)))
        out.append(q.coords[0])
    return np.array(out)

def resample(line, K=16):
    L = LineString(line); return np.array([L.interpolate(L.length*i/(K-1)).coords[0] for i in range(K)])

# ---------------------------------------------------------------- parts
WHITE = '#fafafa'; INK = '#1d1d1f'

class Part:
    def __init__(self, name):
        self.name = name; self.fills = []; self.strokes = []; self.order = []
    def fill(self, poly, color=WHITE): self.fills.append((poly, color)); self.order.append(('f', len(self.fills)-1))
    def stroke(self, line): self.strokes.append(np.asarray(line, float)); self.order.append(('s', len(self.strokes)-1))

def prism(part, o2, plane, k0, k1, top_fill=WHITE, side_fill=WHITE, off=(0, 0), M=64):
    """Extrude a 2D outline between k0 and k1 along the plane normal. Draws the silhouette
    (filled, outlined) then the near cap (k1 = the cap facing the viewer: +z for 'xy', +x for
    'yz', +y... note: for 'xz' the visible cap is the one with SMALLER y; pass k0>k1 then).
    Returns (silhouette Polygon, cap Polygon) in px for clipping detail lines."""
    a = P(lift(o2, plane, k0, off)); b = P(lift(o2, plane, k1, off))
    hr = radial(MultiPoint(np.vstack([a, b])).convex_hull, M)
    part.fill(Polygon(hr), side_fill); part.stroke(ring(hr))
    cap = Polygon(b); part.fill(cap, top_fill); part.stroke(ring(b))
    return Polygon(hr), cap

def cylinder(part, r, axis_plane, k0, k1, center=(0, 0), cap_fill='#f2f2f2', knurl=0, n=40):
    """Cylinder along the plane normal (e.g. a crown along +x: plane 'yz'). Optional knurl lines."""
    c0 = P(lift(circle(r, n), axis_plane, k0, center)); c1 = P(lift(circle(r, n), axis_plane, k1, center))
    h = Polygon(radial(MultiPoint(np.vstack([c0, c1])).convex_hull, 56))
    part.fill(h); part.stroke(ring(np.array(h.exterior.coords)[:-1]))
    band = h.difference(Polygon(c1))
    for i in range(knurl):
        th = 2*math.pi*i/knurl
        if math.cos(th) + math.sin(th) <= 0.15: continue   # decide visibility at yaw 0, keep fixed
        u, v = center[0] + r*math.cos(th), center[1] + r*math.sin(th)
        seg = np.array([lift([(u, v)], axis_plane, k0 + 0.05*(k1-k0))[0], lift([(u, v)], axis_plane, k1 - 0.05*(k1-k0))[0]])
        clipped(part, P(seg), band, K=2)
    part.fill(Polygon(c1), cap_fill); part.stroke(ring(c1))
    return h, Polygon(c1)

def clipped(part, line_px, region, K=16):
    """Stroke only the longest piece of line_px inside region, resampled to K points (fixed count)."""
    g = LineString(line_px).intersection(region)
    segs = [s for s in getattr(g, 'geoms', [g]) if not s.is_empty and s.geom_type == 'LineString']
    part.stroke(resample(max(segs, key=lambda q: q.length).coords, K) if segs else resample(np.asarray(line_px)[:2], K))

# ---------------------------------------------------------------- timeline
TL = dict(
    T=10.0,                      # Tella Motion clips are 10 s; build to fit, never retime later
    explode=(1.8, 0.95, 0.04),   # start, duration, stagger per part (in EXPLODE order)
    labels=(2.95, 0.13),         # first leader start, stagger
    yaws=(0.0, 7.5, 15.0), yaw_t=(4.6, 7.3, 10.0),   # slow turn while holding; >=3 keys avoid chord shrink
    labels_out=(7.75, 8.15),
    collapse=(8.2, 0.9, 0.02),   # start, duration, stagger -> parts return to assembled
    ink=INK, paper=WHITE, stroke=1.2, font='roboto-mono', font_size=13,
    lcol=640, rcol=1500,         # label column edges (px): left labels end at lcol, right start at rcol
)

def fmt(v): return f'{v:.1f}'.rstrip('0').rstrip('.')
def dpoly(pts, close=False):
    s = 'M' + ' L'.join(f'{fmt(x)} {fmt(y)}' for x, y in np.asarray(pts)); return s + (' Z' if close else '')

def yaw_at(t):
    ys, ts = TL['yaws'], TL['yaw_t']
    if t <= ts[0]: return ys[0]
    for i in range(len(ys)-1):
        if t <= ts[i+1]: return ys[i] + (ys[i+1]-ys[i])*(t-ts[i])/(ts[i+1]-ts[i])
    return ys[-1]

def ease_for(i): return 'easyEaseIn' if i == 0 else 'linear'   # setPath easings are a fixed list: no easeInSine

def build_commands(model):
    T = TL['T']; ys, ts = TL['yaws'], TL['yaw_t']
    geo = {}
    for y in ys: set_yaw(y); geo[y] = model.build()
    set_yaw(0); base = geo[ys[0]]
    for y in ys:  # point-count sanity check
        for pa, pb in zip(base, geo[y]):
            assert [len(s) for s in pa.strokes] == [len(s) for s in pb.strokes], f'{pa.name}: stroke counts change with yaw'
            assert [len(f[0].exterior.coords) for f in pa.fills] == [len(f[0].exterior.coords) for f in pb.fills], f'{pa.name}: fill counts change with yaw'
    DRAW = getattr(model, 'DRAW', {})
    cmds = [{"type": "addShape", "nodeId": "paper", "start": 0, "duration": T, "shape": "fill", "color": TL['paper']}]
    def keys(fn): return [{"at": ts[i], "path": fn(y), "easing": ease_for(i)} for i, y in enumerate(ys)]
    for pi, p in enumerate(base):
        ids, run = [], []
        def flush():
            if not run: return
            idx = list(run); run.clear(); chunks = [[]]
            for i in idx:
                if chunks[-1] and len(' '.join(dpoly(p.strokes[j]) for j in chunks[-1]+[i])) > 1700: chunks.append([])
                chunks[-1].append(i)
            for ch in chunks:
                nid = f'{p.name}.s{len(ids)}'
                cmds.append({"type": "addPath", "nodeId": nid, "start": 0, "duration": T, "path": "M0 0 L1 0", "paint": "stroke",
                             "color": TL['ink'], "strokeWidth": TL['stroke'], "cap": "round", "join": "round"})
                cmds.append({"type": "setPath", "node": nid, "keys": keys(lambda y, ch=ch: ' '.join(dpoly(geo[y][pi].strokes[j]) for j in ch))})
                if p.name in DRAW:
                    st, du = DRAW[p.name]; eid = 'tr_' + nid.replace('.', '_')   # effect ids: no dots
                    cmds.append({"type": "addEffect", "node": nid, "kind": "trimPath", "effectId": eid, "params": {"end": 0}})
                    cmds.append({"type": "setKeyframes", "node": nid, "property": f"field:@e.{eid}/effect/end",
                                 "keys": [{"at": st, "value": 0, "easing": "easeInOutSine"}, {"at": round(st+du, 3), "value": 1}]})
                ids.append(nid)
        for kind, i in p.order:
            if kind == 's': run.append(i); continue
            flush(); col = p.fills[i][1]; nid = f'{p.name}.f{len(ids)}'
            cmds.append({"type": "addPath", "nodeId": nid, "start": 0, "duration": T, "path": "M0 0 L1 0 L1 1 Z", "paint": "fill", "color": col})
            cmds.append({"type": "setPath", "node": nid, "keys": keys(lambda y, i=i: dpoly(np.array(geo[y][pi].fills[i][0].exterior.coords)[:-1], True))})
            if col.lower() != TL['paper'].lower() and p.name in DRAW:
                st, du = DRAW[p.name]
                cmds.append({"type": "setKeyframes", "node": nid, "property": "opacity",
                             "keys": [{"at": round(st+du*0.5, 3), "value": 0, "easing": "easeInOutSine"}, {"at": round(st+du*1.2, 3), "value": 1}]})
            ids.append(nid)
        flush()
        assert len(ids) <= 200, f'{p.name}: >200 nodes in one group; split the part'
        cmds.append({"type": "group", "nodes": ids, "nodeId": f'g.{p.name}', "name": p.name.replace('_', ' ').title()})
    # explode -> hold/turn -> collapse, as group x/y keys
    e0, edur, est = TL['explode']; c0, cdur, cst = TL['collapse']
    for j, (name, d) in enumerate([(n, d) for n, d in model.EXPLODE.items() if any(d)]):
        t0 = round(e0 + j*est, 3); tc = round(c0 + j*cst, 3)
        lateral = abs(d[0]) > 1e-6 or abs(d[1]) > 1e-6
        for k, prop in enumerate(('x', 'y')):
            o0 = offset_px(d, ys[0])[k]
            if abs(o0) < 0.01 and not lateral: continue
            ks = [{"at": t0, "value": 0, "easing": "easeInOutCubic"}, {"at": round(t0+edur, 3), "value": round(o0, 1), "easing": "linear"}]
            if lateral:   # lateral offsets turn with the yaw
                ks[-1]["easing"] = "hold"
                ks.append({"at": ts[0], "value": round(o0, 1), "easing": "easyEaseIn"})
                for t in ts[1:-1]:
                    if t < tc: ks.append({"at": t, "value": round(offset_px(d, yaw_at(t))[k], 1), "easing": "linear"})
            ks.append({"at": tc, "value": round(offset_px(d, yaw_at(tc))[k], 1), "easing": "easeInOutCubic"})
            ks.append({"at": round(tc+cdur, 3), "value": 0})
            cmds.append({"type": "setKeyframes", "node": f'g.{name}', "property": prop, "keys": ks})
    cmds += label_commands(model)
    return cmds

def label_commands(model):
    """Leaders (anchor -> 24px knee -> column) and typewriter labels in left/right columns,
    de-overlapped 30px apart; they follow the turn and leave before the collapse."""
    T = TL['T']; f = TL['font_size']; ls = 0.08; out = []
    lo0, lo1 = TL['labels_out']; LT = [t for t in TL['yaw_t'] if t < lo1] + [lo1 + 0.05]
    set_yaw(0); labs = []
    for text, part, anc, side in model.LABELS:
        ax, ay = P(np.array(anc))[0]; ox, oy = offset_px(model.EXPLODE.get(part, (0, 0, 0)), 0)
        labs.append(dict(text=text, part=part, anc=np.array(anc, float), side=side, y=ay+oy))
    for side in 'LR':
        prev = -1e9
        for l in sorted([l for l in labs if l['side'] == side], key=lambda l: l['y']):
            l['row'] = max(l['y'], prev + 30); prev = l['row']
    labs.sort(key=lambda l: l['row'])
    t_first, t_step = TL['labels']
    for j, l in enumerate(labs):
        L = l['side'] == 'L'; colx = TL['lcol'] + 8 if L else TL['rcol'] - 8; ly = l['row']
        def lead(yaw, l=l, L=L, colx=colx, ly=ly):
            set_yaw(yaw); ax, ay = P(l['anc'])[0]; ox, oy = offset_px(model.EXPLODE.get(l['part'], (0, 0, 0)), yaw)
            ax += ox; ay += oy; kx = ax + (-24 if L else 24) if abs(ly-ay) > 1 else ax
            return dpoly([(ax, ay), (kx, ly), (colx, ly)])
        t0 = round(t_first + j*t_step, 3); nid = f'lead.{j}'; eid = f'tr_lead_{j}'
        out.append({"type": "addPath", "nodeId": nid, "start": 0, "duration": T, "path": lead(0), "paint": "stroke",
                    "color": TL['ink'], "strokeWidth": 1, "cap": "round", "join": "round"})
        out.append({"type": "setPath", "node": nid, "keys": [{"at": t, "path": lead(yaw_at(t)), "easing": ease_for(i)} for i, t in enumerate(LT)]})
        out.append({"type": "addEffect", "node": nid, "kind": "trimPath", "effectId": eid, "params": {"end": 0}})
        out.append({"type": "setKeyframes", "node": nid, "property": f"field:@e.{eid}/effect/end",
                    "keys": [{"at": t0, "value": 0, "easing": "easeOutCubic"}, {"at": round(t0+0.35, 3), "value": 1, "easing": "hold"},
                             {"at": lo0 + 0.1, "value": 1, "easing": "easeInCubic"}, {"at": lo1, "value": 0}]})
        w = len(l['text'])*(0.6+ls)*f + 40
        box = {"x": round(TL['lcol']-w, 1), "y": round(ly-0.43*f, 1), "width": round(w, 1)} if L else \
              {"x": round(TL['rcol']-0.06*f, 1), "y": round(ly-0.43*f, 1), "width": round(w, 1)}
        tid = f'label.{j}'; ts_ = round(t0+0.25, 3)
        out.append({"type": "addTitle", "nodeId": tid, "start": ts_, "duration": round(lo1+0.15-ts_, 3), "text": l['text'], "box": box,
                    "font": TL['font'], "fontSize": f, "color": TL['ink'], "align": "right" if L else "left", "lineHeight": 1, "letterSpacing": ls})
        out.append({"type": "setTextAnimation", "node": tid, "phase": "in", "preset": "typewriter", "unit": "character", "duration": 0.02, "stagger": 0.022})
        out.append({"type": "setKeyframes", "node": tid, "property": "opacity", "keys": [{"at": lo0, "value": 1, "easing": "easyEaseIn"}, {"at": lo1 - 0.1, "value": 0}]})
    return out

def write_batches(cmds, outdir, limit=38000):
    """Split (only before an add/group command, so each node's follow-up edits stay with it) into batches <= limit chars. Each file has one command per
    line with long path keys on their own lines (lines < 2000 chars) so they can be read and pasted."""
    os.makedirs(outdir, exist_ok=True); batches = [[]]; sz = 0
    for c in cmds:
        s = len(json.dumps(c))
        if sz + s > limit and batches[-1] and c['type'] in ('addPath', 'addShape', 'addTitle', 'group'): batches.append([]); sz = 0
        batches[-1].append(c); sz += s
    files = []
    for i, b in enumerate(batches):
        txt = json.dumps(b, separators=(',', ':')).replace('{"at"', '\n{"at"').replace('{"type"', '\n{"type"')
        fn = os.path.join(outdir, f'batch_{i}.json'); open(fn, 'w').write(txt); files.append(fn)
        print(fn, len(b), 'cmds', len(txt), 'chars, longest line', max(len(x) for x in txt.split('\n')))
    return files

# ---------------------------------------------------------------- preview (sanity check before sending)
def render(model, t, path, size=(1920, 1080)):
    from PIL import Image, ImageDraw
    y = yaw_at(t); set_yaw(y); parts = model.build()
    e0, edur, est = TL['explode']; c0, cdur, cst = TL['collapse']
    names = [n for n, d in model.EXPLODE.items() if any(d)]
    def k_of(name):
        if name not in names: return 0
        j = names.index(name); a = (t - (e0 + j*est))/edur; b = (t - (c0 + j*cst))/cdur
        sm = lambda u: 0 if u <= 0 else 1 if u >= 1 else u*u*(3-2*u)
        return sm(a) * (1 - sm(b))
    ss = 2; im = Image.new('RGB', (size[0]*ss, size[1]*ss), TL['paper']); d = ImageDraw.Draw(im)
    for p in parts:
        k = k_of(p.name); ox, oy = offset_px(model.EXPLODE.get(p.name, (0, 0, 0)), y); ox *= k; oy *= k
        for kind, i in p.order:
            if kind == 'f':
                poly, col = p.fills[i]; d.polygon([((x+ox)*ss, (yy+oy)*ss) for x, yy in poly.exterior.coords], fill=col)
            else:
                d.line([((x+ox)*ss, (yy+oy)*ss) for x, yy in p.strokes[i]], fill=TL['ink'], width=int(TL['stroke']*ss), joint='curve')
    im.resize(size, Image.LANCZOS).save(path); return path

def load_model(path):
    spec = importlib.util.spec_from_file_location('model', path); m = importlib.util.module_from_spec(spec)
    sys.modules['model'] = m; spec.loader.exec_module(m); return m

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('model'); ap.add_argument('--out', default='out')
    ap.add_argument('--preview', action='store_true'); a = ap.parse_args()
    sys.modules['explode'] = sys.modules[__name__]   # models `from explode import *`: share this module's CFG/TL, not a second copy
    m = load_model(a.model)
    if hasattr(m, 'TIMELINE'): TL.update(m.TIMELINE)
    if hasattr(m, 'VIEW'): set_view(**m.VIEW)
    cmds = build_commands(m); print(len(cmds), 'commands')
    write_batches(cmds, a.out)
    if a.preview:
        from PIL import Image
        ims = [Image.open(render(m, t, os.path.join(a.out, f'p_{t}.png'))) for t in (0.5, 3.5, 7.5, 9.8)]
        sheet = Image.new('RGB', (1920, 1080)); [sheet.paste(im.resize((960, 540)), ((i % 2)*960, (i//2)*540)) for i, im in enumerate(ims)]
        sheet.save(os.path.join(a.out, 'preview_sheet.png')); print('preview', os.path.join(a.out, 'preview_sheet.png'))
