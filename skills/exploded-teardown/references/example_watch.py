"""Example model: Apple Watch Ultra 3 teardown (dimensions in mm from Apple's case-design PDF:
case 49.14 x 41.0, 12 mm thick, crown dia 9.42). Copy this file and replace build()/EXPLODE/LABELS.
Run: python3 ../scripts/explode.py example_watch.py --out out --preview"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from explode import *
from shapely.geometry import Polygon

VIEW = dict(scale=5.0, cx=960, cy=540)        # px per mm; pick so the EXPLODED stack fits ~80% of height

def build():
    parts = []
    # painter's order: back to front (bottom of stack first, side parts on the far side early)
    bk = Part('back')
    prism(bk, rrect(36.8, 44.07, 10.5), 'xy', -1.4, 0.0)
    for r in (27.3/2, 10.6): bk.stroke(ring(P(lift(circle(r), 'xy', 0.0))))
    for sx in (-4.4, 4.4):
        for sy in (-4.4, 4.4):
            c = P(lift(circle(2.6, 28), 'xy', 0.0, (sx, sy))); bk.fill(Polygon(c), '#cfcfcf'); bk.stroke(ring(c))
    for sx in (-13.6, 13.6):
        for sy in (-16.8, 16.8):
            bk.stroke(ring(P(lift(circle(1.3, 16), 'xy', 0.0, (sx, sy)))))
            bk.stroke(P(np.array([[sx-0.9, sy, 0], [sx+0.9, sy, 0]])))
    parts.append(bk)

    bt = Part('battery')
    prism(bt, rrect(29, 35, 5.5), 'xy', 2.5, 7.0)
    bt.stroke(ring(P(lift(rrect(25, 31, 4), 'xy', 7.0))))
    prism(bt, rrect(7, 4, 1), 'xy', 7.0, 7.8, off=(0, -15))
    parts.append(bt)

    ab = Part('action')       # orange accent part on the far (-x) side
    prism(ab, rrect(12, 4.2, 2.1), 'yz', -22.0, -20.5, top_fill='#ff6a2b', side_fill='#ff6a2b', off=(-8, 6.2))
    parts.append(ab)

    cs = Part('case')
    body = rrect(41.0, 49.14, 10.5)
    hull, top = prism(cs, body, 'xy', 0.0, 10.4)
    clipped(cs, P(lift(body, 'xy', 4.2)), hull.difference(top), K=24)            # antenna split line
    slot = P(lift(rrect(18, 3.4, 1.7), 'xz', 24.57, (0, 5.2))); cs.fill(Polygon(slot), '#e2e2e2'); cs.stroke(ring(slot))
    prism(cs, rrect(39.2, 47.4, 9.6), 'xy', 10.4, 12.0)                           # raised rim
    op = rrect(36.2, 43.4, 8.6); opening = Polygon(P(lift(op, 'xy', 12.0)))
    cs.fill(opening, '#ececec'); cs.stroke(ring(P(lift(op, 'xy', 12.0))))
    clipped(cs, ring(P(lift(op, 'xy', 10.6))), opening, K=24)                     # inner ledge
    prism(cs, rrect(15, 7.4, 3.0), 'yz', 20.4, 22.4, off=(-4, 6.0))                # crown guard
    parts.append(cs)

    sb = Part('sidebtn'); prism(sb, rrect(10, 3.6, 1.8), 'yz', 20.4, 21.9, off=(12, 5.6)); parts.append(sb)

    cr = Part('crown')
    cylinder(cr, 9.42/2, 'yz', 22.4, 26.4, center=(-4.0, 6.0), knurl=24)
    cr.stroke(ring(P(lift(circle(3.0, 32), 'yz', 26.4, (-4.0, 6.0)))))
    parts.append(cr)

    dp = Part('display'); prism(dp, rrect(34.6, 41.8, 8.0), 'xy', 11.2, 11.8, top_fill='#c9c9c9'); parts.append(dp)

    gl = Part('glass')
    prism(gl, rrect(36.0, 43.2, 8.4), 'xy', 12.0, 13.1, top_fill='#f1f1f1')
    for yy, x0, x1 in ((-12.5, -9, 6), (-9.5, -9, 2)):                            # glare marks
        gl.stroke(P(np.array([[x0, yy, 13.1], [x1, yy, 13.1]])))
    parts.append(gl)
    return parts

# explode order = stagger order (top of stack first reads best)
EXPLODE = {'glass': (0, 0, 52), 'crown': (20, 0, 0), 'sidebtn': (13, 0, 0), 'display': (0, 0, 30),
           'action': (-26, 0, 0), 'battery': (0, 0, -32), 'back': (0, 0, -58), 'case': (0, 0, 0)}

# parts visible when assembled draw on; hidden inner parts only appear as the stack opens
DRAW = {'case': (0.15, 0.95), 'glass': (0.35, 0.9), 'crown': (0.55, 0.6), 'sidebtn': (0.6, 0.45)}

LABELS = [
    ('COVER GLASS', 'glass', (16.5, -19.5, 13.1), 'R'),
    ('DISPLAY', 'display', (-15.5, 18.5, 11.8), 'L'),
    ('DIGITAL CROWN', 'crown', (26.4, -4, 6), 'R'),
    ('SIDE BUTTON', 'sidebtn', (21.9, 12, 5.6), 'R'),
    ('TITANIUM CASE', 'case', (-19.5, 22.5, 6), 'L'),
    ('BAND SLOT', 'case', (-6, 24.57, 5.2), 'L'),
    ('ACTION BUTTON', 'action', (-21.2, -8, 8.3), 'L'),
    ('BATTERY', 'battery', (-14, 17, 7.0), 'L'),
    ('BACK CRYSTAL', 'back', (18.0, -21.5, 0), 'R'),
    ('OPTICAL SENSORS', 'back', (-4.4, 4.4, 0), 'L'),
]
