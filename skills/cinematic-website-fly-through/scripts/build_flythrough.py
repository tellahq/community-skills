#!/usr/bin/env python3
"""Build the cinematic fly-through as one Tella Motion command batch.

  python3 build_flythrough.py spec.json --out /workspace/fly_cmds.json

Apply the file with apply_motion_editor_commands (commandsFile) on an EMPTY 1920x1080
Tella Motion document. One script builds every input and look:

spec.json
{
  "duration": 12,                    # seconds
  "cuts": [2.23, 5.5, 9.2],          # one per word: the moment its card covers the frame (the word settles ~0.3 s more)
  "endAt": 10.2,                     # optional: when the end card starts, 0.5-1.3 s after the last cut (default last cut + 1.0)
  "words": ["All-in-one", "Agentic", "Video"],
  "font": "inter", "weight": 500,    # catalog slug or library font id (mi_...)
  "fontFile": "/workspace/font.ttf", # optional, same font, to measure the end card's name
  "ending": "logo",                  # logo | name | hold
  "logo": {"sourceId": "su_...", "width": 1500, "height": 375},   # ending logo (transparent PNG). On screen a wordmark (wider
                                     # than 2:1) is at least 960 px wide, a symbol at least 378 px tall; a note says when that
                                     # blows the source up past 1.3x (it is shown soft: find a bigger logo)
  "end": ["northwind", "notes.com"], # the name in two parts (ending name, and hold; the fallback without a logo)
  "cardSheen": false,                # true puts the moving glass sheen on the word cards too
  "look": { ... },                   # optional: the object brand_look.py prints, or "light" / "dark"

  # The set: a full-page screenshot ...
  "page": {"sourceId": "su_...", "width": 2560, "height": 5867,
           "targets": [450, [1050, 2250], [2200, 3600]],   # optional y per shot: one y for the hero, then [from, to]
           "targetsIn": "image"},            # image (default): y in the screenshot's own pixels; page: y on the 1920-wide page

  # ... or a screen recording (an Auto Capture take or a Tella recording)
  "recording": {
    "sourceId": "su_...", "width": 3840, "height": 2160,
    "durationMs": 24800,                                         # the take's length (list_sources): a shot that plays past it is noted
    "scale": 1.3,                                                # drawn this much larger than the frame, centred, so no edge shows
    "clipCuts": [{"startTimeMs": 3050, "durationMs": 1616}],   # the clip's raw cuts (get_timeline include cuts)
    "mouseEvents": "/workspace/mouse.json",                      # get_mouse_events result (playback times), or a list
    "avoid": [{"startTimeMs": 9074, "durationMs": 15615}],       # optional source ranges to warn about (a take's suggestedCuts)
    "cursor": {"os": "mac", "size": 72},                         # mac (Tella's macOS Golden Gate arrow) | windows | none;
                                                                 # size 56-96: 72 draws an arrow about 83 px tall on the page
                                                                 # (none is forced when the mouse barely moves: < 8 samples
                                                                 # or < 8 % of the width travelled; aim those shots with focus)
    "shots": [                                                   # one per word
      {"startMs": 0},                                            # clip playback time on screen when the shot opens
      {"startMs": 5400, "speed": 1},
      {"startMs": 11000, "focus": [50, 44]}                      # optional focus in % of the screen
    ]
  }
}
"""
import json, sys, os, math

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help') or '--out' not in sys.argv:
    print(__doc__)
    sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help') else 2)

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = json.load(open(os.path.join(HERE, '..', 'references', 'template.json')))
TPS = TPL['ticksPerSecond']
W, H = 1920, 1080
FULL = (0, 0, W, H)

DRIFT = (0.22, 0, 0, 1)
WHIP = (0.6, 0, 0.9, 0.5)
GLIDE = (0.05, 0.535, 0, 1)
GLIDE_X = (0.03, 0.71, 0, 1)
SKIM = (0.05, 0.59, 0.5, 0.8)
BLAST = (0.5, 0.12, 0.9, 0.5)
IN = (0.1, 0.5, 0.4, 1)
OUT = (0.5, 0, 0.86, 0.5)
LOOKS = {
    'light': {'plane': '#FFFFFF', 'shadow': '#1A1450', 'shadowOpacity': 0.6, 'cards': ['#FFFFFF'], 'inks': ['#111111'],
              'endBg': '#FFFFFF', 'endInk': '#111111', 'ripple': '#111111', 'glow': 0.3},
    'dark': {'plane': '#0E0E10', 'shadow': '#000000', 'shadowOpacity': 0.7, 'cards': ['#0E0E10'], 'inks': ['#FFFFFF'],
             'endBg': '#0E0E10', 'endInk': '#FFFFFF', 'ripple': '#FFFFFF', 'glow': 0.2},
}


def tk(s):
    return int(round(s * TPS))


def ease(e):
    if e in ('hold', 'linear'):
        return {'type': e}
    if isinstance(e, str):
        return {'type': 'function', 'name': e}
    return {'type': 'cubicBezier', 'x1': e[0], 'y1': e[1], 'x2': e[2], 'y2': e[3]}


def kf(keys, t0=0.0):
    """keys: [(seconds, value, easing)] -> keyframes on the node's local clock (node starts at t0)."""
    out, last = [], None
    for t, v, e in keys:
        t = tk(max(0.0, t - t0))
        if last is not None and t <= last:
            t = last + 1
        last = t
        out.append({'time': t, 'value': v, 'easing': ease(e)})
    return {'type': 'keyframes', 'timeDomain': 'local', 'keyframes': out}


def deg(keys, t0=0.0):
    return {'unit': 'degrees', 'value': kf(keys, t0)}


def rgba(hexs, a=None):
    h = hexs.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    if a is None:
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
    return {'r': r, 'g': g, 'b': b, 'a': a}


def rrect(x, y, w, h, r=0):
    c = {'x': r, 'y': r}
    return {'type': 'roundedRect', 'rect': {'rect': {'x': x, 'y': y, 'width': w, 'height': h},
                                             'topLeft': c, 'topRight': c, 'bottomRight': c, 'bottomLeft': c}}


def shape(nid, box, color, start, end, r=0, **common):
    c = {'start': tk(start), 'duration': tk(end - start)}
    c.update(common)
    return {'type': 'shape', 'id': nid, 'paint': {'style': 'fill', 'source': {'type': 'solid', 'color': rgba(color)}},
            'geometry': rrect(*box, r), 'common': c}


def sheen(nid, box, grad_end, tx_keys, start, end, opacity=None):
    g = {'type': 'linear', 'start': {'x': 0, 'y': 0}, 'end': {'x': grad_end[0], 'y': grad_end[1]}, 'tileMode': 'clamp',
         'transform': {'translateX': kf(tx_keys, start)}, 'stops': TPL['sheenStops']}
    c = {'start': tk(start), 'duration': tk(end - start), 'blendMode': 'screen'}
    if opacity:
        c['opacity'] = kf(opacity, start)
    return {'type': 'shape', 'id': nid, 'paint': {'style': 'fill', 'source': {'type': 'gradient', 'gradient': g}},
            'geometry': rrect(*box), 'common': c}


def ins(node, parent='', name=None):
    out = [{'type': 'node.insert', 'parent': parent, 'node': node}]
    if name:
        out.append({'type': 'meta.set', 'node': node['id'], 'meta': {'name': name}})
    return out


class Measure:
    def __init__(self, path, weight):
        self.path, self.weight, self.cache = path, weight, {}

    def width(self, text, size, ls_em):
        if not self.path:
            return len(text) * size * (0.56 + ls_em)
        from PIL import ImageFont
        if size not in self.cache:
            f = ImageFont.truetype(self.path, int(round(size)))
            try:
                axes = f.get_variation_axes()
                f.set_variation_by_axes([self.weight if a.get('name', b'') in (b'Weight', 'Weight') else a['default'] for a in axes])
            except Exception:
                pass
            self.cache[size] = f
        return self.cache[size].getlength(text) + len(text) * ls_em * size


# ---------------------------------------------------------------- camera

def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def camera_rows(spec, n, cuts, D, ph, targets, E):
    """Rows (t, anchorX, anchorY, screenX, screenY, scale, rotateX, rotation, rotateY, ease, easeX, easeY)."""
    rows = []
    rec = 'recording' in spec

    def row(t, ax, ay, sx, sy, s, rx, rz, ry, e, ex=None, ey=None):
        rows.append((t, ax, ay, sx, sy, s, rx, rz, ry, e, ex or e, ey or e))

    for i in range(n):
        C = cuts[i]
        S = 0.0 if i == 0 else cuts[i - 1] + 0.82
        t = targets[i]
        last = i == n - 1
        if rec:
            fx, fy = t
            cx = lambda v: clamp(v, 0.28 * W, 0.72 * W)      # keep the screen filling the frame, not its corner
            cy = lambda v: clamp(v, 0.3 * ph, 0.7 * ph)
            if i == 0:
                row(S, 960, cy(ph / 2 - 40), 960, 540, 0.95, 36, -8, 0, DRIFT)
                row(C - 0.55, cx(fx), cy(fy), 960, 540, 1.35, 22, -4, 0, WHIP)
                row(C, cx(fx), cy(fy), 960, 240, 1.9, 6, -3, 0, 'hold')
            elif not last:
                row(S, cx(fx - 320), cy(fy - 120), 1260, 540, 1.2, 18, -6, -10, GLIDE, GLIDE_X, DRIFT)
                row(C - 0.55, cx(fx), cy(fy), 960, 540, 1.35, 16, 3, 10, WHIP)
                row(C, cx(fx), cy(fy), 900, 240, 1.4, 15, 4, 13, 'linear')
                row(C + 0.15, cx(fx), cy(fy), 860, 120, 1.47, 13.6, 5.4, 17.1, 'hold')
            else:
                row(S, cx(fx - 140), cy(fy - 200), 960, 540, 1.3, 58, -2, 0, SKIM)
                row(C - 0.35, cx(fx), cy(fy), 960, 540, 1.4, 40, -1, 0, BLAST)
                row(C, cx(fx), cy(fy), 960, 540, 0.4, 48, -1, 0, 'hold')
        else:
            if i == 0:
                y = t if not isinstance(t, (list, tuple)) else t[0]
                row(S, 760, y + 30, 960, 540, 0.95, 38, -9, 0, DRIFT)
                row(C - 0.55, 760, y, 960, 540, 1.35, 22, -4, 0, WHIP)
                row(C, 760, y, 960, 100, 1.9, 6, -3, 0, 'hold')
            elif not last:
                y0, y1 = t
                row(S, 960, y0, 1320, 540, 1.15, 18, -6, -10, GLIDE, GLIDE_X, DRIFT)
                row(C - 0.55, 960, y1, 960, 540, 1.25, 16, 3, 10, WHIP)
                row(C, 960, y1, 900, 40, 1.3, 15, 4, 13, 'linear')
                row(C + 0.15, 960, y1, 860, -160, 1.368, 13.6, 5.4, 17.1, 'hold')
            else:
                y0, y1 = t
                row(S, 760, y0, 960, 540, 1.25, 62, -2, 0, SKIM)
                row(C - 0.35, 900, y1, 960, 540, 1.3, 40, -1, 0, BLAST)
                row(C, 900, y1, 960, 540, 0.4, 48, -1, 0, 'hold')
    ey = rows[-1][2] if not rec else ph / 2
    ex = 960
    row(E, ex, ey - 70 if not rec else ey, 960, 540, 0.88, 22, -7, 0, DRIFT)
    row(D, ex, ey - 40 if not rec else ey, 960, 540, 0.8, 18, -5, 0, 'hold')
    return rows


def camera_common(rows, cuts, extra_z=None):
    t = {'perspective': 1700,
         'translateX': kf([(r[0], r[3] - r[1], r[10]) for r in rows]),
         'translateY': kf([(r[0], r[4] - r[2], r[11]) for r in rows]),
         'scaleX': kf([(r[0], r[5], r[9]) for r in rows]),
         'scaleY': kf([(r[0], r[5], r[9]) for r in rows]),
         'rotateX': deg([(r[0], r[6], r[9]) for r in rows]),
         'rotate': deg([(r[0], r[7], r[9]) for r in rows]),
         'rotateY': deg([(r[0], r[8], r[9]) for r in rows])}
    if extra_z is not None:
        t['translateZ'] = extra_z
    blur = []
    for C in cuts[:-1]:
        blur += [(C - 0.5, 0, 'easeInCubic'), (C, 28, 'hold'), (C + 0.82, 0, 'hold')]
    return {'transform': t,
            'origin': {'x': kf([(r[0], r[1], r[9]) for r in rows]), 'y': kf([(r[0], r[2], r[9]) for r in rows])},
            'effects': [{'id': 'speed', 'order': 'a0', 'effect': {'type': 'blur', 'kind': 'image', 'radiusX': 0,
                                                                   'radiusY': kf(blur), 'tileMode': 'decal'}}]}


# ---------------------------------------------------------------- recording + cursor

# macOS 27 Golden Gate arrow, the artwork Tella draws for Mac recordings (tella_render_adapter mac-goldengate/pointer.svg),
# in points with the hotspot at 0,0: black tail and body, then their white outlines, each its own path.
MAC_FILL = ["M 6.192 14.662 L 6.19 14.663 C 5.651 14.889 5.031 14.636 4.805 14.097 L 2.34 8.233 C 2.113 7.694 2.366 7.074 2.905 6.847 C 3.444 6.62 4.064 6.873 4.291 7.412 L 6.758 13.275 C 6.985 13.815 6.731 14.436 6.192 14.662",
            "M -0.012 0.011 L -0.012 10.908 C -0.012 11.498 0.685 11.812 1.127 11.421 L 3.862 9 L 7.662 9.001 C 8.272 9.001 8.578 8.264 8.147 7.832 L 0.239 -0.093 C 0.147 -0.186 -0.012 -0.12 -0.012 0.011"]
MAC_EDGE = ["M 6.044 9 L 4.959 9 L 6.758 13.275 C 6.985 13.814 6.731 14.435 6.192 14.662 L 6.19 14.663 C 5.651 14.889 5.031 14.635 4.805 14.097 L 2.99 9.779 L 2.199 10.479 L 3.883 14.484 C 4.204 15.25 4.95 15.745 5.781 15.745 C 6.055 15.745 6.323 15.691 6.579 15.584 C 7.086 15.371 7.48 14.973 7.688 14.463 C 7.896 13.954 7.893 13.394 7.68 12.888 Z",
            "M 8.873 7.143 L 0.49 -1.258 C -0.064 -1.813 -1.012 -1.421 -1.012 -0.637 L -1.012 10.93 C -1.012 12.374 0.692 13.141 1.773 12.185 L 3.396 10.748 L 2.987 9.775 L 1.127 11.421 C 0.685 11.812 -0.012 11.498 -0.012 10.908 L -0.012 0.011 C -0.012 -0.12 0.147 -0.186 0.24 -0.093 L 8.148 7.832 C 8.578 8.264 8.273 9.001 7.663 9.001 L 4.959 9.001 L 5.379 10 L 7.687 10.001 C 9.179 10.001 9.926 8.199 8.873 7.143"]
WIN = 'M0 0 L0 17 L4 13.2 L6.6 19.4 L9 18.4 L6.5 12.3 L12 12.3 Z'


def scale_path(d, k):
    out = []
    for tok in d.split():
        if tok[0].isalpha():
            out.append(tok[0] + (('%g' % round(float(tok[1:]) * k, 2)) if len(tok) > 1 else ''))
        else:
            out.append('%g' % round(float(tok) * k, 2))
    return ' '.join(out)


def to_source(p_ms, cuts):
    """Clip playback ms -> source ms, through the clip's raw cuts."""
    s = p_ms
    for c in sorted(cuts, key=lambda c: c['startTimeMs']):
        if c['startTimeMs'] <= s:
            s += c['durationMs']
    return s


def recording_cmds(spec, n, cuts, D, ph, look, notes):
    rec = spec['recording']
    clip_cuts = rec.get('clipCuts', [])
    ev = rec.get('mouseEvents') or []
    if isinstance(ev, str):
        ev = json.load(open(ev))
    if isinstance(ev, dict):
        ev = ev.get('events', [])
    ev = [dict(e, src=to_source(e['timestampMs'], clip_cuts)) for e in ev]
    travel = sum(math.hypot((b['xPct'] - a['xPct']) / 100 * W, (b['yPct'] - a['yPct']) / 100 * ph) for a, b in zip(ev, ev[1:]))
    sparse = bool(ev) and (len(ev) < 8 or travel < 0.08 * W)
    s = float(rec.get('scale', 1.3))
    x0, y0 = -(s - 1) * W / 2, -(s - 1) * ph / 2
    sx = lambda x: x0 + x * s                     # screen px -> page px, with the recording drawn s times larger, centred
    sy = lambda y: y0 + y * s
    cmds, windows, targets = [], [], []
    if not rec.get('durationMs'):
        notes.append('recording.durationMs missing: give the take\'s length (list_sources durationMs) so a shot that plays past its end is caught')
    cmds += ins({'type': 'group', 'id': 'screen', 'children': [], 'common': {'clip': rrect(x0, y0, W * s, ph * s, 28)}}, 'page', 'Recording')
    for i, sh in enumerate(rec['shots']):
        speed = float(sh.get('speed', 1))
        vis = 0.0 if i == 0 else cuts[i - 1] + 0.82          # when the shot opens on screen
        a = 0.0 if i == 0 else cuts[i - 1] + 0.3              # the node starts under the card
        b = D if i == n - 1 else cuts[i] + 0.5
        src_vis = to_source(sh['startMs'], clip_cuts)
        src_in = max(0.0, src_vis - (vis - a) * 1000 * speed)
        src_out = src_in + (b - a) * 1000 * speed
        seen_out = src_vis + ((cuts[i] if i < n else D) + 0.16 - vis) * 1000 * speed
        inside = [c for c in clip_cuts if src_vis < c['startTimeMs'] < seen_out]
        take = rec.get('durationMs')
        if take and seen_out > take:
            notes.append('shot %d runs past the end of the take: it is on screen until %d ms of the take and the take is %d ms, so '
                         'the picture stops for its last %.1f s: move its startMs %d ms earlier, or lower its speed' % (
                             i + 1, seen_out, take, (seen_out - take) / 1000 / speed, math.ceil((seen_out - take) / 100) * 100))
        if take and src_out > take:      # the part under the card: end the node with the take instead
            b = max(a + 0.1, a + (take - src_in) / 1000 / speed)
            src_out = take
        waits = [c for c in rec.get('avoid', []) if c['startTimeMs'] < seen_out and c['startTimeMs'] + c['durationMs'] > src_vis]
        if waits:
            notes.append('shot %d shows a wait (%s): start after it, or raise the shot\'s speed' % (
                i + 1, ', '.join('%d-%d ms' % (c['startTimeMs'], c['startTimeMs'] + c['durationMs']) for c in waits)))
        if inside:
            notes.append('shot %d plays through %d cut(s) of the clip (%s): the cut footage shows; move startMs to avoid it' % (
                i + 1, len(inside), ', '.join('%d-%d ms' % (c['startTimeMs'], c['startTimeMs'] + c['durationMs']) for c in inside)))
        nid = 'rec%d' % (i + 1)
        cmds.append({'type': 'addMedia', 'parent': 'screen', 'nodeId': nid, 'start': round(a, 4), 'sourceId': rec['sourceId'],
                     'duration': round(b - a, 4)})
        patch = {'destination': {'x': round(x0, 1), 'y': round(y0, 1), 'width': round(W * s, 1), 'height': round(ph * s, 1)}, 'fit': 'fill', 'sourceIn': tk(src_in / 1000), 'audio': {'mute': True}}
        if speed != 1:
            patch['playbackRate'] = {'numerator': int(round(speed * 100)), 'denominator': 100}
        cmds.append({'type': 'node.patch', 'node': nid, 'patch': patch})
        cmds.append({'type': 'meta.set', 'node': nid, 'meta': {'name': 'Recording, shot %d' % (i + 1), 'muted': True}})
        evs = [e for e in ev if src_in <= e['src'] <= src_out]
        to_t = lambda s, a=a, src_in=src_in, speed=speed: a + (s - src_in) / 1000 / speed
        before = [e for e in ev if e['src'] < src_in]
        seed = before[-1] if before else (evs[0] if evs else None)
        cur_end = b if i == n - 1 else cuts[i] + 0.3        # the next shot's node starts here, under the card
        pts = [(to_t(e['src']), sx(e['xPct'] / 100 * W), sy(e['yPct'] / 100 * ph), e.get('clicked', False)) for e in evs]
        pts = [q for q in pts if q[0] < cur_end]
        if seed:
            pts = [(a, sx(seed['xPct'] / 100 * W), sy(seed['yPct'] / 100 * ph), False)] + pts
        windows.append((a, cur_end, pts, vis))
        seen = [e for e in evs if vis <= to_t(e['src']) <= (cuts[i] if i < len(cuts) else D)]
        if ev and not sparse and not any(e.get('clicked') for e in seen):
            notes.append('shot %d has no click on screen: pick a moment with one, or aim it with focus' % (i + 1))
        if sh.get('focus'):
            f = sh['focus']
        elif sparse or not ev:
            f = [50, 45]
            notes.append('shot %d: no focus and no cursor to follow, aimed at the middle of the screen: give it focus [x%%, y%%] '
                         'on a heading or feature block you can see in the take' % (i + 1))
        else:
            pick = [e for e in seen if e.get('clicked')] or seen or evs
            f = [sum(e['xPct'] for e in pick) / len(pick), sum(e['yPct'] for e in pick) / len(pick)] if pick else [50, 50]
        targets.append((sx(f[0] / 100 * W), sy(f[1] / 100 * ph)))

    cur = rec.get('cursor', {})
    osn = cur.get('os', 'mac')
    if osn != 'none' and not ev:
        osn = 'none'
        notes.append('no mouse events: no cursor drawn (a web or uploaded recording has its own cursor in the picture)')
    if osn != 'none' and sparse:
        osn = 'none'
        notes.append('the cursor barely moves (%d samples, %d px travelled): no cursor drawn' % (len(ev), travel))
    if osn != 'none':
        size = clamp(float(cur.get('size', 72)), 56, 96)
        k = size / (15.3 if osn == 'mac' else 19.0)
        xs, ys, op, pulses = [], [], [], []
        for a, b, pts, vis in windows:
            if not pts:
                op += [(a, 0, 'hold')]
                continue
            pts = sorted(pts)
            for j, (t, x, y, clicked) in enumerate(pts):
                nxt = pts[j + 1] if j + 1 < len(pts) else None
                gap = (nxt[0] - t) if nxt else 0
                moves = nxt and (abs(nxt[1] - x) > 2 or abs(nxt[2] - y) > 2)
                e = 'hold' if not nxt else ('hold' if not moves else ('linear' if gap <= 0.16 else 'easeInOutCubic'))
                xs.append((t, x, e))
                ys.append((t, y, e))
                if clicked:
                    pulses.append(t)
            op += [(a, 1, 'hold')]
        body_scale, rip_scale, rip_op = [(0, 1, 'hold')], [(0, 0.2, 'hold')], [(0, 0, 'hold')]
        for t in pulses:
            body_scale += [(t - 0.02, 1, 'easeOutCubic'), (t + 0.07, 0.8, 'easeOutBack'), (t + 0.3, 1, 'hold')]
            rip_scale += [(t, 0.2, 'easeOutCubic'), (t + 0.5, 1, 'hold')]
            rip_op += [(t, 0.55, 'easeOutCubic'), (t + 0.5, 0, 'hold')]
        cmds += ins({'type': 'group', 'id': 'cursor', 'children': [], 'common': {
            'transform': {'translateX': kf(xs or [(0, W / 2, 'hold')]), 'translateY': kf(ys or [(0, ph / 2, 'hold')])},
            'opacity': kf(op or [(0, 0, 'hold')]),
            'motionBlur': {'shutter': tk(1 / 60), 'samples': 16}}}, 'page', 'Cursor (%s)' % ('macOS' if osn == 'mac' else 'Windows'))
        R = round(size * 0.95, 1)
        cmds.append({'type': 'addShape', 'parent': 'cursor', 'nodeId': 'cursor.ripple', 'start': 0, 'duration': D, 'shape': 'circle',
                     'box': {'x': -R, 'y': -R, 'width': 2 * R, 'height': 2 * R}, 'color': look['ripple']})
        cmds.append({'type': 'node.patch', 'node': 'cursor.ripple', 'patch': {'common': {
            'origin': {'x': 0, 'y': 0}, 'transform': {'scaleX': kf(rip_scale), 'scaleY': kf(rip_scale)}, 'opacity': kf(rip_op)}}})
        cmds.append({'type': 'meta.set', 'node': 'cursor.ripple', 'meta': {'name': 'Click ripple'}})
        # Golden Gate's shadow: black 45 %, 2 pt blur, 1 pt down; the Windows arrow keeps its softer one
        sha, sdy, sr = (0.45, 0.065, 0.13) if osn == 'mac' else (0.35, 0.09, 0.12)
        cmds += ins({'type': 'group', 'id': 'cursor.body', 'children': [], 'common': {
            'origin': {'x': 0, 'y': 0}, 'transform': {'scaleX': kf(body_scale), 'scaleY': kf(body_scale)},
            'effects': [{'id': 'shadow', 'order': 'a0', 'effect': {'type': 'dropShadow', 'color': {'r': 0, 'g': 0, 'b': 0, 'a': sha},
                                                                    'dx': 0, 'dy': round(sdy * size, 1), 'radiusX': round(sr * size, 1),
                                                                    'radiusY': round(sr * size, 1)}}]}}, 'cursor', 'Arrow')
        if osn == 'mac':
            parts = [('cursor.tail', MAC_FILL[0], '#000000', 'Arrow tail'), ('cursor.fill', MAC_FILL[1], '#000000', 'Arrow fill'),
                     ('cursor.tailedge', MAC_EDGE[0], '#FFFFFF', 'Arrow tail outline'), ('cursor.edge', MAC_EDGE[1], '#FFFFFF', 'Arrow outline')]
            for nid, d, color, name in parts:
                cmds.append({'type': 'addPath', 'parent': 'cursor.body', 'nodeId': nid, 'start': 0, 'duration': D,
                             'path': scale_path(d, k), 'color': color, 'paint': 'fill'})
                cmds.append({'type': 'meta.set', 'node': nid, 'meta': {'name': name}})
        else:
            d = scale_path(WIN, k)
            cmds.append({'type': 'addPath', 'parent': 'cursor.body', 'nodeId': 'cursor.edge', 'start': 0, 'duration': D, 'path': d,
                         'color': '#000000', 'paint': 'stroke', 'strokeWidth': round(1.9 * k, 2), 'join': 'miter', 'cap': 'round'})
            cmds.append({'type': 'addPath', 'parent': 'cursor.body', 'nodeId': 'cursor.fill', 'start': 0, 'duration': D, 'path': d,
                         'color': '#FFFFFF', 'paint': 'fill'})
            cmds.append({'type': 'meta.set', 'node': 'cursor.edge', 'meta': {'name': 'Arrow outline'}})
            cmds.append({'type': 'meta.set', 'node': 'cursor.fill', 'meta': {'name': 'Arrow fill'}})
        notes.append('cursor: %s, %d click(s), %d position keys' % (osn, len(pulses), len(xs)))
    return cmds, targets, (x0, y0, W * s, ph * s)


# ---------------------------------------------------------------- cards

def word_cmds(nid, parent, text, spec, color, start, end, size=250, box=None, align='center'):
    box = box or {'x': 0, 'y': round(H / 2 - size * 0.6), 'width': W}
    return [{'type': 'addTitle', 'parent': parent, 'nodeId': nid, 'start': round(start, 4), 'duration': round(end - start, 4),
             'text': text, 'box': box, 'font': spec.get('font', 'inter'), 'weight': spec.get('weight', 500), 'fontSize': size,
             'color': color, 'align': align, 'letterSpacing': -0.02, 'lineHeight': 1.2},
            {'type': 'meta.set', 'node': nid, 'meta': {'name': text}}]


def fit_size(m, text, size, maxw):
    while m.width(text, size, -0.02) > maxw and size > 110:
        size -= 10
    return size


def card_cmds(i, n, C, D, text, spec, look, m, hold_end, E_end):
    cid = 'card%d' % (i + 1)
    bgc = look['cards'][i % len(look['cards'])]
    ink = look['inks'][i % len(look['inks'])]
    kind = 'swing' if i == 0 else ('blast' if i == n - 1 else 'drop')
    cmds = []
    grp = {'type': 'group', 'id': cid, 'children': [], 'common': {'origin': {'x': W / 2, 'y': H / 2}}}
    size = fit_size(m, text, 250, 1640)
    if kind == 'swing':
        a, b = C - 0.16, C + 1.22
        bg_op = [(a, 0, 'easeInOutSine'), (C, 1, 'hold'), (C + 0.82, 1, 'linear'), (C + 1.10, 0, 'hold')]
        grp['common']['transform'] = {
            'perspective': 1400,
            'rotateX': deg([(a, 16, 'linear'), (C, 12, IN), (C + 0.45, 0, 'hold'), (C + 0.5, 0, OUT), (C + 0.82, 9, 'linear'), (b, 19, 'hold')]),
            'rotate': deg([(a, -4, 'linear'), (C, -3, IN), (C + 0.45, 0, 'hold'), (C + 0.5, 0, OUT), (C + 0.82, -4, 'linear'), (b, -9, 'hold')]),
            'scaleX': kf([(a, 0.8, 'linear'), (C, 0.9, IN), (C + 0.45, 1, 'hold'), (C + 0.5, 1, OUT), (C + 0.82, 1.02, 'hold')]),
            'scaleY': kf([(a, 0.8, 'linear'), (C, 0.9, IN), (C + 0.45, 1, 'hold'), (C + 0.5, 1, OUT), (C + 0.82, 1.02, 'hold')]),
            'rotateY': deg([(C + 0.5, 0, OUT), (C + 0.82, 36, 'linear'), (b, 68, 'hold')]),
            'translateX': kf([(C + 0.5, 0, OUT), (C + 0.82, -620, 'linear'), (b, -2500, 'hold')]),
            'translateY': kf([(C + 0.5, 0, OUT), (C + 0.82, -110, 'linear'), (b, -460, 'hold')])}
        grp['common']['opacity'] = kf(bg_op)
        wt = {'translateY': kf([(a, 1125, 'linear'), (C, 405, IN), (C + 0.45, 0, 'hold')], a)}
        sh_tx = [(C, -700, 'linear'), (C + 0.82, -44, 'linear')]
        wb = b
    elif kind == 'drop':
        a, b = C - 0.12, C + 1.0
        bg_op = [(a, 0, 'easeInOutSine'), (C + 0.04, 1, 'hold'), (C + 0.82, 1, 'linear'), (b, 0, 'hold')]
        grp['common']['transform'] = {
            'perspective': 1400,
            'rotateY': deg([(C - 0.1, 13, 'linear'), (C, 10, IN), (C + 0.45, 0, 'hold')]),
            'rotateX': deg([(C - 0.1, 32, 'linear'), (C, 26, IN), (C + 0.45, 0, 'hold'), (C + 0.5, 0, OUT), (C + 0.82, 10, 'linear'), (b, 16, 'hold')]),
            'scaleX': kf([(C + 0.5, 1, OUT), (C + 0.82, 0.72, 'linear'), (b, 0.48, 'hold')]),
            'scaleY': kf([(C + 0.5, 1, OUT), (C + 0.82, 0.72, 'linear'), (b, 0.48, 'hold')])}
        grp['common']['opacity'] = kf(bg_op)
        wt = {'translateY': kf([(C - 0.1, 855, 'linear'), (C, 405, IN), (C + 0.45, 0, 'hold'), (C + 0.5, 0, OUT),
                                (C + 0.82, -60, 'linear'), (b, -120, 'hold')], a),
              'translateX': kf([(C - 0.1, 100, 'linear'), (C, 50, IN), (C + 0.45, 0, 'hold')], a)}
        sh_tx = [(C, -700, 'linear'), (C + 0.82, -44, 'linear')]
        wb = b
    else:
        a = C - 0.16
        E = E_end
        b = E + 0.2 if not hold_end else E + 0.3
        wb = E + 0.16
        bg_op = [(a, 0, 'easeInOutSine'), (C, 1, 'hold'), (E, 1, 'linear'), (b, 0 if hold_end else 1, 'hold')]
        grp['common']['transform'] = {
            'perspective': 1400,
            'scaleX': kf([(a, 6, 'linear'), (C, 3.5, IN), (C + 0.45, 1, 'hold'), (C + 0.68, 1, OUT), (E, 0.97, 'hold')]),
            'scaleY': kf([(a, 6, 'linear'), (C, 3.5, IN), (C + 0.45, 1, 'hold'), (C + 0.68, 1, OUT), (E, 0.97, 'hold')]),
            'rotateX': deg([(a, 10, 'linear'), (C, 8, IN), (C + 0.45, 0, 'hold')]),
            'rotateY': deg([(C + 0.68, 0, OUT), (E, 10, 'linear'), (wb, 15, 'hold')]),
            'translateX': kf([(C + 0.68, 0, OUT), (E, -290, 'linear'), (wb, -1010, 'hold')])}
        grp['common']['opacity'] = kf([(a, 0, 'easeInOutSine'), (C, 1, 'hold'), (E, 1, 'linear'), (wb, 0, 'hold')])
        wt = None
        sh_tx = [(C, -700, 'linear'), (E, -44, 'linear')]
    cmds += ins(shape(cid + '.bg', FULL, bgc, a, b, opacity=kf(bg_op, a)), '', 'Card %d background' % (i + 1))
    cmds += ins(grp, '', 'Card %d word' % (i + 1))
    cmds += word_cmds(cid + '.word', cid, text, spec, ink, a, wb, size)
    common = {'motionBlur': {'shutter': tk(1 / 60), 'samples': 16}, 'origin': {'x': W / 2, 'y': H / 2}}
    if wt:
        common['transform'] = wt
    cmds.append({'type': 'node.patch', 'node': cid + '.word', 'patch': {'common': common}})
    if spec.get('cardSheen'):   # off by default: the cards are flat colour
        sh_op = [(a, 0, 'easeInOutSine'), (a + 0.16, 1, 'hold'), (wb - 0.18, 1, 'linear'), (wb, 0, 'hold')]
        cmds += ins(sheen(cid + '.sheen', FULL, (1920, 1200), sh_tx, a, wb, sh_op), '', 'Card %d sheen' % (i + 1))
    return cmds


def end_cmds(spec, look, cuts, D, m, hold_end, E, notes):
    cmds = []
    ending = spec.get('ending', 'logo')
    if hold_end:   # the last page stays up behind a tinted scrim, so the name reads over it
        cmds += ins(shape('end.bg', FULL, look['endBg'], E, D, opacity=kf([(E, 0, 'easeInOutSine'), (E + 0.5, 0.78, 'hold')], E)), '', 'End scrim')
    else:
        cmds += ins(shape('end.bg', FULL, look['endBg'], E, D, opacity=kf([(E, 0, 'linear'), (E + 0.16, 1, 'hold')], E)), '', 'End card background')
    # The card's slow turn eases out to flat and centred by the last frame: the trailer ends square-on, on the middle.
    grp = {'type': 'group', 'id': 'endcard', 'children': [], 'common': {
        'origin': {'x': W / 2, 'y': H / 2},
        'transform': {'perspective': 1400, 'rotateY': deg([(E, -12, (0.1, 0.5, 0.3, 1)), (D, 0, 'hold')]),
                      'rotateX': deg([(E, 3, (0.1, 0.5, 0.3, 1)), (D, 0, 'hold')]),
                      'translateX': kf([(E, 30, (0.1, 0.5, 0.3, 1)), (D, 0, 'hold')])},
        'opacity': kf([(E, 0, 'linear'), (E + 0.16, 1, 'hold')])}}
    cmds += ins(grp, '', 'End card')
    mb = {'shutter': tk(1 / 60), 'samples': 16}
    # A part slides in from x0 px to the right, holds, then takes its little bump (`bump` px, negative = left) and comes to
    # REST at `rest`: 0 is where it is laid out, the middle of the frame. Nothing on the end card drifts past its resting place.
    slide = lambda x0, t1, bump, t2, t3, t0, rest=0: {
        'transform': {'translateX': kf([(t0, rest + x0 - bump, IN), (t0 + t1, rest - bump, 'hold'), (t0 + t2, rest - bump, 'easeOutCubic'),
                                        (t0 + t3, rest, 'hold')], t0)},
        'opacity': kf([(t0, 0.25, 'linear'), (t0 + min(t1, 0.17), 1, 'hold')], t0), 'motionBlur': mb, 'origin': {'x': W / 2, 'y': H / 2}}
    logo = spec.get('logo') or ({'sourceId': spec['logoSourceId']} if spec.get('logoSourceId') else None)
    if ending == 'logo' and logo:
        cmds.append({'type': 'addMedia', 'parent': 'endcard', 'nodeId': 'logo', 'start': round(E, 4), 'sourceId': logo['sourceId'],
                     'duration': round(D - E, 4)})
        ar = logo.get('width', 1) / max(1, logo.get('height', 1))
        if ar > 2:                                                  # a wordmark: at least half the frame's width
            lw = clamp(380.0 * ar, 0.5 * W, 1400.0)
            lh = lw / ar
        else:                                                       # a symbol: at least 35 % of the frame's height
            lh = 420.0 if ar <= 1.3 else 400.0
            lw = lh * ar
        if logo.get('width') and lw > 1.3 * logo['width']:
            notes.append('the logo is %d px wide and is shown %d px wide (%.1fx): it will look soft; use a bigger logo '
                         '(site_logo.js renders 1500 px)' % (logo['width'], lw, lw / logo['width']))
        patch = {'destination': {'x': round((W - lw) / 2, 1), 'y': round((H - lh) / 2, 1), 'width': round(lw, 1), 'height': round(lh, 1)},
                 'fit': 'contain'}
        patch['common'] = slide(360, 0.4, -60, 0.47, 0.97, E)
        cmds.append({'type': 'node.patch', 'node': 'logo', 'patch': patch})
        cmds.append({'type': 'meta.set', 'node': 'logo', 'meta': {'name': 'Logo'}})
    else:
        p1, p2 = (spec.get('end') or ['', ''])[:2]
        size = fit_size(m, p1 + p2, 220, 1500)
        w1, w2 = m.width(p1, size, -0.02), m.width(p2, size, -0.02)
        split = round(W / 2 + (w1 - w2) / 2, 1)          # the joined name rests centred on the frame
        y = round(H / 2 - size * 0.6)
        ink = look['endInk']
        cmds += word_cmds('end.a', 'endcard', p1, spec, ink, E, D, size, {'x': split - 1600, 'y': y, 'width': 1600}, 'right')
        cmds.append({'type': 'node.patch', 'node': 'end.a', 'patch': {'common': slide(360, 0.4, -60, 0.47, 0.97, E, -2 if p2 else 0)}})
        if p2:
            cmds += word_cmds('end.b', 'endcard', p2, spec, ink, E + 0.3, D, size, {'x': split, 'y': y, 'width': 1600}, 'left')
            cmds.append({'type': 'node.patch', 'node': 'end.b', 'patch': {'common': slide(300, 0.17, -56, 0.17, 0.57, E + 0.3, 2)}})
    return cmds


# ---------------------------------------------------------------- main

def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[sys.argv.index('--out') + 1]
    D = float(spec.get('duration', 12))
    words = spec['words']
    n = len(words)
    cuts = spec.get('cuts') or [2.23, 5.5, 9.2]
    assert len(cuts) == n, 'one cut per word'
    assert n >= 2 and cuts[0] >= 1.8 and all(y - x >= 2.4 for x, y in zip(cuts, cuts[1:])), 'the first cut needs 1.8 s before it and the others 2.4 s between them'
    E = float(spec.get('endAt', cuts[-1] + 1.0))
    assert 0.5 - 1e-6 <= E - cuts[-1] <= 1.3 + 1e-6, 'endAt must be 0.5-1.3 s after the last cut'
    assert E + 1.8 <= D + 1e-6, 'the end card needs 1.8 s: shorten the cuts or lengthen the duration'
    look = spec.get('look') or 'light'
    look = dict(LOOKS['light'], **(LOOKS[look] if isinstance(look, str) else look))
    ending = spec.get('ending', 'logo')
    hold_end = ending == 'hold'
    m = Measure(spec.get('fontFile'), spec.get('weight', 500))
    notes = []
    rec = 'recording' in spec
    if rec:
        r = spec['recording']
        assert len(r['shots']) == n, 'one recording shot per word'
        ph = round(W * r['height'] / r['width'])
    else:
        p = spec['page']
        ph = round(W * p['height'] / p['width'])

    cmds = [{'type': 'canvas.set', 'canvas': {'width': W, 'height': H, 'duration': {'seconds': D}}}]
    cmds += [{'type': 'asset.set', 'kind': 'shaders', 'asset': a} for a in TPL['shaders']]
    cmds += ins(shape('bg', FULL, look['plane'], 0, D), '', 'Background')
    cmds += ins({'type': 'group', 'id': 'drift', 'children': [], 'common': {
        'origin': {'x': W / 2, 'y': H / 2},
        'transform': {'scaleX': kf([(0, 1, 'linear'), (D, 1.15, 'linear')]), 'scaleY': kf([(0, 1, 'linear'), (D, 1.15, 'linear')]),
                      'translateX': kf([(0, 70, 'linear'), (D, -70, 'linear')]), 'translateY': kf([(0, 35, 'linear'), (D, -35, 'linear')]),
                      'rotate': deg([(0, -1.8, 'linear'), (D, 1.8, 'linear')])}}}, '', 'Drift')
    cmds += ins({'type': 'group', 'id': 'stage', 'children': [], 'common': {}}, 'drift', 'Stage')
    cmds += ins({'type': 'group', 'id': 'page', 'children': [], 'common': {}}, 'drift', 'Page')
    cmds += ins(shape('plane', (-3200, -3200, 8320, ph + 9000), look['plane'], 0, D), 'stage', 'Plane')
    ext = (0, 0, W, ph)
    if rec:
        rs = float(spec['recording'].get('scale', 1.3))
        ext = (-(rs - 1) * W / 2, -(rs - 1) * ph / 2, W * rs, ph * rs)
    sh = shape('shadow', (ext[0] - 20, ext[1] + 110, ext[2] + 40, ext[3]), look['shadow'], 0, D, 40)
    sh['paint']['source']['color'] = rgba(look['shadow'], look['shadowOpacity'])
    sh['common']['effects'] = [{'id': 'soft', 'order': 'a0', 'effect': {'type': 'blur', 'kind': 'image', 'radiusX': 140, 'radiusY': 140, 'tileMode': 'decal'}}]
    cmds += ins(sh, 'stage', 'Page shadow')

    psheen = ins(sheen('pagesheen', ext, (2400, 1500), [(0, -1600, 'linear'), (D, 1600, 'linear')], 0, D), 'page', 'Glass sheen')
    if rec:
        content, targets, _ = recording_cmds(spec, n, cuts, D, ph, look, notes)
        # the sheen goes over the recording and under the cursor
        k = next((i for i, c in enumerate(content) if c['type'] == 'node.insert' and c['node']['id'] == 'cursor'), len(content))
        content = content[:k] + psheen + content[k:]
    else:
        p = spec['page']
        scale = W / p['width']
        content = [{'type': 'addMedia', 'parent': 'page', 'nodeId': 'pageimg', 'start': 0, 'sourceId': p['sourceId'], 'duration': D},
                   {'type': 'node.patch', 'node': 'pageimg', 'patch': {
                       'destination': {'x': 0, 'y': 0, 'width': p['width'], 'height': p['height']}, 'fit': 'fill',
                       'common': {'origin': {'x': 0, 'y': 0}, 'transform': {'scaleX': scale, 'scaleY': scale}}}},
                   {'type': 'meta.set', 'node': 'pageimg', 'meta': {'name': 'Page screenshot'}}] + psheen
        targets = p.get('targets')
        if targets and p.get('targetsIn', 'image') == 'image':
            targets = [round(t * scale) if not isinstance(t, (list, tuple)) else [round(v * scale) for v in t] for t in targets]
        if targets:
            for i, t in enumerate(targets):
                for v in (t if isinstance(t, (list, tuple)) else [t]):
                    if not 0 <= v <= ph:
                        notes.append('target %s of shot %d is off the page (0-%d on the 1920-wide page): targetsIn is %s' % (
                            v, i + 1, ph, p.get('targetsIn', 'image')))
        if not targets:
            lo, hi = 700, max(900, ph - 700)
            step = (hi - lo) / max(1, n - 1)
            targets = [300] + [[round(lo + step * (i - 1)), round(lo + step * i)] for i in range(1, n)]
    cmds += content

    rows = camera_rows(spec, n, cuts, D, ph, targets, E)
    cmds.append({'type': 'node.patch', 'node': 'stage', 'patch': {'common': camera_common(rows, cuts, -160)}})
    cmds.append({'type': 'node.patch', 'node': 'page', 'patch': {'common': camera_common(rows, cuts)}})

    for i, w in enumerate(words):
        if i == n - 1:
            zb = json.loads(json.dumps(TPL['zoomblur']))
            zb['common'].update({'start': tk(cuts[i] - 0.3), 'duration': tk(0.3), 'opacity': kf([(0, 0, WHIP), (0.3, 1, 'hold')])})
            cmds += ins(zb, '', 'Zoom blur')
        cmds += card_cmds(i, n, cuts[i], D, w, spec, look, m, hold_end, E)
    cmds += end_cmds(spec, look, cuts, D, m, hold_end, E, notes)

    dep = json.loads(json.dumps(TPL['tsdepth']))
    dep['common'].update({'start': 0, 'duration': tk(D)})
    cmds += ins(dep, '', 'Tilt-shift depth map')
    ts = json.loads(json.dumps(TPL['tiltshift']))
    ts['common'].update({'start': 0, 'duration': tk(D)})
    for e in ts['common']['effects']:
        if e['id'] == 'glow':
            e['effect']['intensity'] = look['glow']
    cmds += ins(ts, '', 'Tilt-shift lens')
    cmds.append({'type': 'document.rename', 'name': spec.get('name', 'Website fly-through')})
    assert len(cmds) <= 256, 'more than 256 commands: split the file in two'
    json.dump(cmds, open(out, 'w'))
    print(json.dumps({'commands': len(cmds), 'out': out, 'pageHeight': ph, 'targets': targets, 'notes': notes}))


if __name__ == '__main__':
    main()
