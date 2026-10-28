#!/usr/bin/env python3
"""Logo mask reveal: build Tella Motion command batches from any SVG logo.

One shape of the logo (the "window") becomes a hole onto the video below.
The logo can play an intro animation, then scales up toward the window until
the window covers the frame; the window's own fill fades so the video shows
through it, and the rest of the logo flies off the edges.

  pip install --break-system-packages -q svgelements svgpathtools numpy pillow
  python3 build_reveal.py logo.svg --list --preview /workspace/lr/parts.png
  python3 build_reveal.py logo.svg --window 3 --width 1920 --height 1080 \
      --intro spin --out /workspace/lr

Writes commands.json (one apply_motion_editor_commands batch, on a blank
document) and prints the overlay duration and the chosen zoom target.
"""
import argparse, json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from svgelements import SVG, Shape, Path, Color
from svgpathtools import parse_path

TPS = 254016000000  # Tella Motion ticks per second (motion blur shutter is in ticks)


def load_parts(svg_file):
    svg = SVG.parse(svg_file, reify=True)
    parts = []
    for el in svg.elements():
        if not isinstance(el, Shape):
            continue
        if el.values.get('visibility') == 'hidden' or el.values.get('display') == 'none':
            continue
        p = Path(el)
        p.reify()
        d = p.d()
        if not d.strip():
            continue
        fill, stroke = el.fill, el.stroke
        sw = el.stroke_width or 0
        has_fill = fill is not None and fill.value is not None and fill.alpha > 0
        has_stroke = stroke is not None and stroke.value is not None and stroke.alpha > 0 and sw > 0
        raw_fill = str(el.values.get('fill', ''))
        warn = 'url(' in raw_fill
        if warn:  # gradient/pattern fill: placeholder colour, rebuild by hand
            has_fill, fill = True, Color('#888888')
        if not has_fill and not has_stroke:
            continue
        bb = p.bbox()
        if bb is None:
            continue
        op = float(el.values.get('opacity', 1) or 1)
        parts.append(dict(
            idx=len(parts), id=el.id, d=d, bbox=bb,
            fill=fill.hex[:7] if has_fill else None,
            fill_alpha=(fill.alpha / 255 if has_fill else 1) * op,
            stroke=stroke.hex[:7] if has_stroke else None,
            stroke_alpha=(stroke.alpha / 255 if has_stroke else 1) * op,
            stroke_width=sw, gradient=warn))
    if not parts:
        sys.exit('No visible shapes found in the SVG.')
    return parts


def tf(d, s, tx, ty):
    return parse_path(d).scaled(s).translated(complex(tx, ty)).d()


def polys(d, n=400):
    out = []
    for sp in parse_path(d).continuous_subpaths():
        L = max(sp.length(error=1e-3), 1e-6)
        k = max(24, int(n * L / 400))
        pts = [sp.point(i / k) for i in range(k)]
        out.append([(p.real, p.imag) for p in pts])
    return out


def raster(d, W, H, scale=1.0):
    img = Image.new('1', (int(W * scale), int(H * scale)), 0)
    acc = np.zeros((img.height, img.width), bool)
    for poly in polys(d):  # even-odd composition of subpaths
        m = Image.new('1', img.size, 0)
        ImageDraw.Draw(m).polygon([(x * scale, y * scale) for x, y in poly], fill=1)
        acc ^= np.array(m, bool)
    return acc


def best_window_rect(mask, aspect):
    """Largest centred rect of the frame's aspect inside the mask.
    Returns (cx, cy, half_height) in mask pixels."""
    H, W = mask.shape
    I = np.zeros((H + 1, W + 1), np.int64)
    I[1:, 1:] = mask.astype(np.int64).cumsum(0).cumsum(1)
    ys, xs = np.mgrid[0:H, 0:W]
    lo, hi, best = 0.5, max(H, W) / 2, None
    for _ in range(26):
        h = (lo + hi) / 2
        w = h * aspect
        y0 = np.floor(ys - h).astype(int); y1 = np.ceil(ys + h).astype(int)
        x0 = np.floor(xs - w).astype(int); x1 = np.ceil(xs + w).astype(int)
        ok = (y0 >= 0) & (x0 >= 0) & (y1 < H) & (x1 < W)
        y0c, y1c, x0c, x1c = [np.clip(a, 0, n) for a, n in ((y0, H - 1), (y1, H - 1), (x0, W - 1), (x1, W - 1))]
        area = (y1c - y0c + 1) * (x1c - x0c + 1)
        s = I[y1c + 1, x1c + 1] - I[y0c, x1c + 1] - I[y1c + 1, x0c] + I[y0c, x0c]
        valid = ok & (s == area)
        if valid.any():
            lo = h
            vy, vx = np.nonzero(valid)
            cy, cx = np.nonzero(mask)
            my, mx = cy.mean(), cx.mean()
            j = np.argmin((vy - my) ** 2 + (vx - mx) ** 2)
            best = (vx[j], vy[j], h)
        else:
            hi = h
    return best


def preview(parts, out):
    x0 = min(p['bbox'][0] for p in parts); y0 = min(p['bbox'][1] for p in parts)
    x1 = max(p['bbox'][2] for p in parts); y1 = max(p['bbox'][3] for p in parts)
    S = 900 / max(x1 - x0, y1 - y0)
    W, H = int((x1 - x0) * S) + 80, int((y1 - y0) * S) + 80
    img = Image.new('RGB', (W, H), (235, 235, 235))
    dr = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
    except Exception:
        font = ImageFont.load_default()
    for p in parts:
        d = tf(p['d'], S, 40 - x0 * S, 40 - y0 * S)
        col = p['fill'] or p['stroke']
        m = raster(d, W, H)
        rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
        img.paste(Image.new('RGB', (W, H), rgb), mask=Image.fromarray((m * 255).astype('uint8')))
    for p in parts:
        bx0, by0, bx1, by1 = p['bbox']
        cx, cy = 40 + ((bx0 + bx1) / 2 - x0) * S, 40 + ((by0 + by1) / 2 - y0) * S
        t = str(p['idx'])
        dr.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 40, 90), outline='white', width=3)
        tw = dr.textlength(t, font=font)
        dr.text((cx - tw / 2, cy - 20), t, fill='white', font=font)
    img.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('svg')
    ap.add_argument('--list', action='store_true', help='list the shapes and exit')
    ap.add_argument('--preview', help='with --list: write a PNG with each shape numbered')
    ap.add_argument('--window', help='shape index or id that becomes the reveal window')
    ap.add_argument('--width', type=float); ap.add_argument('--height', type=float)
    ap.add_argument('--background', default='#FFFFFF', help="plate colour behind the logo, or 'none'")
    ap.add_argument('--intro', default='spin', help='comma list: none, spin, pop, fade, rise, drop')
    ap.add_argument('--turns', type=float, default=2)
    ap.add_argument('--intro-end', type=float, default=None, help='s (default 0.75, or 0 with intro none)')
    ap.add_argument('--hold', type=float, default=None, help='s of stillness before the reveal (default 0, or 0.3 with intro none)')
    ap.add_argument('--reveal', type=float, default=0.8, help='s the zoom takes')
    ap.add_argument('--window-fade', type=float, default=0.35, help='s for the window fill to fade (0 = opens at once)')
    ap.add_argument('--rest-size', type=float, default=0.18, help="logo's longer side at rest, as a fraction of the frame's shorter side")
    ap.add_argument('--cover', type=float, default=1.12, help='how far past the frame the window ends (1 = just covers)')
    ap.add_argument('--motion-blur', type=float, default=45, help='shutter as 1/N s; 0 = off')
    ap.add_argument('--out', default='.')
    a = ap.parse_args()

    parts = load_parts(a.svg)
    if a.list:
        for p in parts:
            bx0, by0, bx1, by1 = p['bbox']
            print(f"{p['idx']:>3}  id={p['id']!s:<18} fill={p['fill']} stroke={p['stroke']} "
                  f"bbox=({bx0:.1f},{by0:.1f})-({bx1:.1f},{by1:.1f}){'  GRADIENT FILL (placeholder)' if p['gradient'] else ''}")
        if a.preview:
            os.makedirs(os.path.dirname(a.preview) or '.', exist_ok=True)
            preview(parts, a.preview); print('preview:', a.preview)
        return
    if a.window is None or not a.width or not a.height:
        sys.exit('--window, --width and --height are required (run --list first).')
    win = next((p for p in parts if str(p['idx']) == a.window or p['id'] == a.window), None)
    if win is None:
        sys.exit(f'No shape {a.window!r}; run --list.')

    W, H = a.width, a.height
    C = (W / 2, H / 2)
    intro = [s.strip() for s in a.intro.split(',') if s.strip() and s.strip() != 'none']
    t_in = a.intro_end if a.intro_end is not None else (0.75 if intro else 0.0)
    hold = a.hold if a.hold is not None else (0.0 if intro else 0.3)
    tr = t_in + hold
    te = tr + a.reveal
    D = round(te + 0.05, 3)

    # Draw the logo centred on the canvas, fitting inside it at 100% (keeps every
    # grouped/matted layer inside canvas-local coordinates, so nothing is clipped).
    x0 = min(p['bbox'][0] for p in parts); y0 = min(p['bbox'][1] for p in parts)
    x1 = max(p['bbox'][2] for p in parts); y1 = max(p['bbox'][3] for p in parts)
    lw, lh = x1 - x0, y1 - y0
    u = 0.9 * min(W / lw, H / lh)
    ox, oy = C[0] - (x0 + lw / 2) * u, C[1] - (y0 + lh / 2) * u
    for p in parts:
        p['cd'] = tf(p['d'], u, ox, oy)

    # Zoom target: centre of the largest frame-shaped rect inside the window.
    rs = min(1.0, 1400 / max(W, H))
    mask = raster(win['cd'], W, H, rs)
    if not mask.any():
        sys.exit('Window shape has no area (is it a stroke-only line?).')
    bx, by, bh = best_window_rect(mask, W / H)
    T = (bx / rs, by / rs)
    h_canvas = bh / rs
    s0 = a.rest_size * min(W, H) / (max(lw, lh) * u)
    s1 = a.cover * (H / 2) / h_canvas
    if s1 <= s0:
        sys.exit('Window already covers the frame at rest; lower --rest-size.')

    wi = win['idx']
    below = [p for p in parts if p['idx'] < wi]
    above = [p for p in parts if p['idx'] > wi]
    c = [{'type': 'canvas.set', 'canvas': {'duration': {'seconds': D}}}]

    def add_part(nid, p, alpha_override=None):
        out = []
        if p['fill']:
            out.append({'type': 'addPath', 'nodeId': nid, 'start': 0, 'duration': D, 'path': p['cd'],
                        'color': p['fill'], 'paint': 'fill'})
            if p['fill_alpha'] < 0.999:
                out.append({'type': 'setProperty', 'node': nid, 'property': 'opacity', 'value': round(p['fill_alpha'], 3)})
        if p['stroke']:
            sid = nid + '.stroke' if p['fill'] else nid
            out.append({'type': 'addPath', 'nodeId': sid, 'start': 0, 'duration': D, 'path': p['cd'],
                        'color': p['stroke'], 'paint': 'stroke', 'strokeWidth': round(p['stroke_width'] * u, 2),
                        'join': 'round', 'cap': 'round'})
            if p['stroke_alpha'] < 0.999:
                out.append({'type': 'setProperty', 'node': sid, 'property': 'opacity', 'value': round(p['stroke_alpha'], 3)})
        return out, [nid] + ([nid + '.stroke'] if p['fill'] and p['stroke'] else [])

    plate_kids = []
    if a.background.lower() != 'none':
        c.append({'type': 'addShape', 'nodeId': 'bg', 'start': 0, 'duration': D, 'shape': 'fill', 'color': a.background})
        plate_kids.append('bg')
    groups = []  # transformed groups
    if below:
        ids = []
        for p in below:
            cmds, n = add_part(f"b.{p['idx']}", p); c += cmds; ids += n
        c.append({'type': 'group', 'nodes': ids, 'nodeId': 'logo.below', 'name': 'Logo under the window'})
        plate_kids.append('logo.below'); groups.append('logo.below')
    if not plate_kids:  # need something to matte
        c.append({'type': 'addShape', 'nodeId': 'bg', 'start': 0, 'duration': D, 'shape': 'fill', 'color': '#000000'})
        c.append({'type': 'setProperty', 'node': 'bg', 'property': 'opacity', 'value': 0})
        plate_kids.append('bg')
    c.append({'type': 'group', 'nodes': plate_kids, 'nodeId': 'plate', 'name': 'Plate (cut by the window)'})
    c.append({'type': 'addPath', 'nodeId': 'h.window', 'start': 0, 'duration': D, 'path': win['cd'], 'color': '#000000', 'paint': 'fill'})
    c.append({'type': 'group', 'nodes': ['h.window'], 'nodeId': 'hole', 'name': 'Window hole (matte)'})
    c.append({'type': 'setMatte', 'node': 'plate', 'matte': 'hole', 'mode': 'alphaInverted'})
    groups.append('hole')
    cmds, n = add_part('w.fill', win); c += cmds
    c.append({'type': 'group', 'nodes': n, 'nodeId': 'window', 'name': 'Window fill'})
    groups.append('window')
    if above:
        ids = []
        for p in above:
            cmds, n = add_part(f"a.{p['idx']}", p); c += cmds; ids += n
        c.append({'type': 'group', 'nodes': ids, 'nodeId': 'logo.above', 'name': 'Logo over the window'})
        groups.append('logo.above')

    # ---- animation ----
    def key(t, v, e='linear'):
        return {'at': round(t, 3), 'value': round(v, 4), 'easing': e}

    N = 9
    rest = 'hold' if tr > 0 else 'continuous'  # with no intro or hold the zoom starts at 0: don't hold its first key
    popin = 'pop' in intro and t_in > 0
    vert = ('rise' in intro or 'drop' in intro) and t_in > 0
    # scale: optional pop-in, rest, then the ease-out zoom (log-zoom space)
    scale = [key(0, 0, 'easeOutBack'), key(t_in, s0, 'hold' if tr > t_in else 'continuous')] if popin else [key(0, s0, rest)]
    if tr > (t_in if popin else 0):
        scale.append(key(tr, s0, 'continuous'))
    rev = []
    for i in range(1, N):
        tau = i / (N - 1)
        e = 1 - (1 - tau) ** 3
        s = s0 * (s1 / s0) ** e
        rev.append((tr + tau * (te - tr), s, (s - s0) / (s1 - s0)))  # offset linear in scale
    scale += [key(t, s, 'continuous') for t, s, _ in rev]
    dx, dy = -s1 * (T[0] - C[0]), -s1 * (T[1] - C[1])
    xk = [key(0, 0, rest)] + ([key(tr, 0, 'continuous')] if tr > 0 else []) + [key(t, f * dx, 'continuous') for t, _, f in rev]
    if vert:
        sgn = 1 if 'rise' in intro else -1
        yk = [key(0, sgn * 0.12 * H, 'easeOutCubic'), key(t_in, 0, 'hold' if tr > t_in else 'continuous')]
        if tr > t_in:
            yk.append(key(tr, 0, 'continuous'))
    else:
        yk = [key(0, 0, rest)] + ([key(tr, 0, 'continuous')] if tr > 0 else [])
    yk += [key(t, f * dy, 'continuous') for t, _, f in rev]

    b = []
    for g in groups:
        b += [{'type': 'setProperty', 'node': g, 'property': 'anchorX', 'value': C[0]},
              {'type': 'setProperty', 'node': g, 'property': 'anchorY', 'value': C[1]},
              {'type': 'setKeyframes', 'node': g, 'property': 'scale', 'keys': scale},
              {'type': 'setKeyframes', 'node': g, 'property': 'x', 'keys': xk},
              {'type': 'setKeyframes', 'node': g, 'property': 'y', 'keys': yk}]
        if 'spin' in intro and t_in > 0:
            b.append({'type': 'setKeyframes', 'node': g, 'property': 'rotation',
                      'keys': [key(0, -360 * a.turns, 'easeOutCubic'), key(t_in, 0)]})
        if a.motion_blur > 0:
            b.append({'type': 'node.patch', 'node': g, 'patch': {'common': {'motionBlur': {'shutter': int(TPS / a.motion_blur), 'samples': 32}}}})
        if 'fade' in intro and t_in > 0 and g != 'hole':
            b.append({'type': 'setKeyframes', 'node': g, 'property': 'opacity',
                      'keys': [key(0, 0, 'easeOutCubic'), key(min(t_in, 0.4), 1)]})
    # hole switches on at the reveal while the opaque window fill still covers it
    b.append({'type': 'setKeyframes', 'node': 'hole', 'property': 'opacity',
              'keys': [key(0, 0, 'hold'), key(max(tr - 0.01, 0), 1)]})
    if a.window_fade > 0:
        b.append({'type': 'setKeyframes', 'node': 'w.fill', 'property': 'opacity',
                  'keys': [key(0, win['fill_alpha'], 'hold'), key(tr + 0.01, win['fill_alpha'], 'easeOutCubic'),
                           key(tr + a.window_fade, 0)]})
    else:
        b.append({'type': 'setKeyframes', 'node': 'window', 'property': 'opacity',
                  'keys': [key(0, 1, 'hold'), key(tr + 0.01, 0)]})
    if win['stroke'] and win['fill']:
        b.append({'type': 'setKeyframes', 'node': 'w.fill.stroke', 'property': 'opacity',
                  'keys': [key(0, 1, 'hold'), key(tr + 0.01, 1, 'easeOutCubic'), key(tr + max(a.window_fade, 0.01), 0)]})

    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, 'commands.json')
    with open(path, 'w') as f:
        json.dump(c + b, f, separators=(',', ':'))
    print(f'{path}: {len(c + b)} commands, {os.path.getsize(path)} bytes')
    print(f'overlay duration: {int(round(D * 1000))} ms; reveal starts {tr:.2f}s, ends {te:.2f}s')
    print(f'rest scale {s0:.3f}, end scale {s1:.2f}, zoom target ({T[0]:.0f},{T[1]:.0f}) on the 100% drawing')
    if any(p['gradient'] for p in parts):
        print('WARNING: gradient fills were replaced by #888888; rebuild them with node.patch paint.source gradient.')
    if win['fill'] is None:
        print('NOTE: the window is stroke-only, so only its line fades; the hole still uses its outline area.')


if __name__ == '__main__':
    main()
