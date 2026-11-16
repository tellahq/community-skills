#!/usr/bin/env python3
"""Paths for the projector-quote film window.

    python3 film_gate.py [x y width height] [--seed N]

x, y is the window's top-left corner in canvas pixels; the default is the
640 x 480 window centred at (1440, 540) on a 1920 x 1080 canvas. Prints JSON:

    {"gate": "<SVG path>", "hair": "<SVG path>"}

gate: a rounded rectangle with a slightly uneven edge (a point every ~14 px,
each nudged by up to 1 px, with a few 3-4 px nicks). Use it for the `gate`
matte and for the `halo`.
hair: a short curved stroke rising from the bottom edge.
Another seed gives another edge.
"""
import json
import math
import random
import sys


def gate(x0, y0, w, h, rng):
    k = w / 640.0
    r, step = 22.0 * k, 14.0 * k
    pts = []

    def edge(ax, ay, bx, by, nx, ny):
        n = max(1, round(math.hypot(bx - ax, by - ay) / step))
        for i in range(n + 1):
            t = i / n
            j = rng.uniform(-1.0, 1.0) * k
            if rng.random() < 0.03:
                j += rng.choice((-3.5, 3.5)) * k
            pts.append((ax + (bx - ax) * t + nx * j, ay + (by - ay) * t + ny * j))

    def corner(cx, cy, a0):
        for i in range(1, 8):
            a = a0 + (math.pi / 2) * (i / 8)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    edge(x0 + r, y0, x0 + w - r, y0, 0, 1)
    corner(x0 + w - r, y0 + r, -math.pi / 2)
    edge(x0 + w, y0 + r, x0 + w, y0 + h - r, 1, 0)
    corner(x0 + w - r, y0 + h - r, 0)
    edge(x0 + w - r, y0 + h, x0 + r, y0 + h, 0, 1)
    corner(x0 + r, y0 + h - r, math.pi / 2)
    edge(x0, y0 + h - r, x0, y0 + r, 1, 0)
    corner(x0 + r, y0 + r, math.pi)
    return "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"


def hair(x0, y0, w, h):
    k = w / 640.0
    bx, by = x0 + 177 * k, y0 + h + 1
    rel = [(4, -19), (16, -28), (12, -42), (9, -52), (0, -54), (-3, -64)]
    p = [(bx + dx * k, by + dy * k) for dx, dy in rel]
    c = lambda a: " ".join(f"{px:.0f} {py:.0f}" for px, py in a)
    return f"M{bx:.0f} {by:.0f} C{c(p[:3])} C{c(p[3:])}"


def main(argv):
    seed = 7
    if "--seed" in argv:
        i = argv.index("--seed")
        seed = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    x0, y0, w, h = (float(a) for a in argv) if len(argv) == 4 else (1120.0, 300.0, 640.0, 480.0)
    rng = random.Random(seed)
    print(json.dumps({"gate": gate(x0, y0, w, h, rng), "hair": hair(x0, y0, w, h)}))


if __name__ == "__main__":
    main(sys.argv[1:])
