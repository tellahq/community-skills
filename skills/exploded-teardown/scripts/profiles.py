"""Get 2D part profiles (in mm) out of reference assets, for use as outlines in a teardown model.

  pdf_polylines(path, page)      vector paths of a PDF page (pymupdf), in PDF points
  svg_polylines(path)            vector paths of an SVG (installs svgelements on first use)
  raster_outlines(path)          closed contours of a drawing/photo/render (OpenCV), in image px
  closed_outlines(polys, min_area) keep closed shapes, largest first
  overview(polys, out_png)       numbered contact sheet so you can SEE which outline is which view/part
  to_mm(pts, units_per_mm, origin) convert + centre; get units_per_mm from a dimensioned length
Then: outline = resample_closed(to_mm(poly, k)) and use it in prism()/lift() (see explode.py).
"""
import math, numpy as np

def pdf_polylines(path, page=0, step=1.0):
    import pymupdf
    pg = pymupdf.open(path)[page]; out = []
    for d in pg.get_drawings():
        cur = []
        for it in d['items']:
            op = it[0]
            if op == 'l': seg = [it[1], it[2]]
            elif op == 'c':
                p0, p1, p2, p3 = it[1:5]; n = 12
                seg = [p0] + [pymupdf.Point(*(((1-t)**3)*np.array(p0) + 3*((1-t)**2)*t*np.array(p1) + 3*(1-t)*t*t*np.array(p2) + t**3*np.array(p3))) for t in np.linspace(0, 1, n)[1:]]
            elif op == 're': r = it[1]; seg = [r.tl, r.tr, r.br, r.bl, r.tl]
            elif op == 'qu': q = it[1]; seg = [q.ul, q.ur, q.lr, q.ll, q.ul]
            else: continue
            pts = [(p.x, p.y) for p in seg]
            if cur and np.hypot(cur[-1][0]-pts[0][0], cur[-1][1]-pts[0][1]) < 0.01: cur += pts[1:]
            else:
                if len(cur) > 1: out.append(np.array(cur))
                cur = pts
        if len(cur) > 1: out.append(np.array(cur))
    return out

def svg_polylines(path, n_per_seg=12):
    try: import svgelements
    except ImportError:
        import subprocess, sys; subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'svgelements']); import svgelements
    svg = svgelements.SVG.parse(path); out = []
    for el in svg.elements():
        if isinstance(el, svgelements.Shape):
            p = svgelements.Path(el)
            for sub in p.as_subpaths():
                sp = svgelements.Path(sub); L = sp.length() or 0
                if L <= 0: continue
                n = max(4, int(L/2))
                pts = [sp.point(t) for t in np.linspace(0, 1, n)]
                out.append(np.array([(q.x, q.y) for q in pts]))
    return out

def raster_outlines(path, thresh=None, min_area=400):
    import cv2
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if thresh is None: _, bw = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    else: _, bw = cv2.threshold(im, thresh, 255, cv2.THRESH_BINARY_INV)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    cs, hier = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    out = [c[:, 0, :].astype(float) for c in cs if cv2.contourArea(c) >= min_area]
    out = [cv2.approxPolyDP(c.astype(np.float32).reshape(-1, 1, 2), 1.0, True)[:, 0, :] for c in out]
    return sorted(out, key=lambda c: -abs(_area(c)))

def _area(p): p = np.asarray(p); return 0.5*np.sum(p[:, 0]*np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1)*p[:, 1])

def closed_outlines(polys, min_area=20, tol=0.5):
    out = [p for p in polys if len(p) > 3 and np.hypot(*(p[0]-p[-1])) <= tol and abs(_area(p)) >= min_area]
    return sorted(out, key=lambda p: -abs(_area(p)))

def overview(polys, out_png, width=1600):
    from PIL import Image, ImageDraw
    allp = np.vstack(polys); mn, mx = allp.min(0), allp.max(0); k = (width-40)/max(1e-9, (mx-mn)[0])
    H = int((mx-mn)[1]*k) + 40; im = Image.new('RGB', (width, H), 'white'); d = ImageDraw.Draw(im)
    for i, p in enumerate(polys):
        q = (p - mn)*k + 20; d.line([tuple(x) for x in q], fill=(0, 0, 0), width=1)
        c = q.mean(0); d.text(tuple(c), str(i), fill=(220, 0, 0))
    im.save(out_png); return out_png

def to_mm(pts, units_per_mm, origin=None, flip_y=True):
    p = np.asarray(pts, float).copy()
    if flip_y: p[:, 1] = -p[:, 1]          # drawing y goes down; model y/z go up
    o = p.mean(0) if origin is None else np.asarray(origin, float)
    return (p - o)/units_per_mm
