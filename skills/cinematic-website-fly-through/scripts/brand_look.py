#!/usr/bin/env python3
"""Work out the Brand matched look from the site's own pixels.

  python3 brand_look.py frame.png [more.png ...] [--primary '#492FFB'] [--bg '#F4F3F0'] > look.json

Give it the full-page screenshot, or two or three frames of the recording. Pass --primary when you
know the brand colour (the site's button or link colour, its theme-color, the workspace brand kit):
it wins over the colour the script finds. Prints the `look` object build_flythrough.py takes.
"""
import sys, json, colorsys
from collections import Counter
from PIL import Image


def hx(c):
    return '#%02X%02X%02X' % tuple(int(round(v)) for v in c)


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def lum(c):
    f = lambda v: (v / 255 / 12.92) if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ink_on(bg, dark=(17, 17, 17), light=(255, 255, 255)):
    return light if contrast(light, bg) >= contrast(dark, bg) else dark


def main():
    import argparse
    ap = argparse.ArgumentParser(
        prog='brand_look.py',
        description='Work out the Brand matched look from the site\'s own pixels and print {"look": ..., "found": ...} as JSON.',
        epilog='Pass the full-page screenshot (one file), or 2-3 frames of the recording taken mid-shot at different shots '
               '(get_motion_frame / get_video_frame PNGs, or ffmpeg frames of the take), never the end card or a card frame. '
               'Put the printed "look" object in the spec.')
    ap.add_argument('images', nargs='+', help='screenshot, or 2-3 recording frames (PNG/JPEG)')
    ap.add_argument('--primary', metavar='#RRGGBB', help='the brand colour (site_brand.js "primary"[0], theme-color, brand kit); wins over the colour found in the pixels')
    ap.add_argument('--bg', metavar='#RRGGBB', help='the page background (site_brand.js "background"); wins over the most common pixel colour')
    ns = ap.parse_args()
    args = ns.images
    opt = {}
    if ns.primary:
        opt['--primary'] = rgb(ns.primary)
    if ns.bg:
        opt['--bg'] = rgb(ns.bg)
    counts = Counter()
    for p in args:
        im = Image.open(p).convert('RGB')
        im.thumbnail((400, 4000))
        for c in (im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata()):
            counts[(c[0] // 8 * 8 + 4, c[1] // 8 * 8 + 4, c[2] // 8 * 8 + 4)] += 1
    total = sum(counts.values()) or 1
    bg = opt.get('--bg') or (counts.most_common(1)[0][0] if counts else (255, 255, 255))
    accents = Counter()
    for c, n in counts.items():
        h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c))
        if s > 0.4 and 0.3 < v and n / total > 0.0005:
            accents[c] += n * s * s
    found = [c for c, _ in accents.most_common(5)]
    primary = opt.get('--primary') or (found[0] if found else ink_on(bg))
    dark = lum(bg) < 0.18
    plane = mix(bg, primary, 0.14 if dark else 0.10)
    deep = mix(primary, (0, 0, 0), 0.8) if not dark else mix(primary, (255, 255, 255), 0.88)
    accent_ink = primary if contrast(primary, plane) >= 3 else ink_on(plane)
    look = {
        'plane': hx(plane),
        'shadow': hx(mix(primary, (0, 0, 0), 0.55)) if not dark else '#000000',
        'shadowOpacity': 0.5 if not dark else 0.7,
        'cards': [hx(primary), hx(plane), hx(deep)],
        'inks': [hx(ink_on(primary)), hx(accent_ink), hx(ink_on(deep, dark=primary if contrast(primary, deep) >= 4.5 else (17, 17, 17)))],
        'endBg': hx(plane),
        'endInk': hx(ink_on(plane, dark=mix(primary, (0, 0, 0), 0.8))),
        'ripple': hx(primary),
        'glow': 0.2,
    }
    json.dump({'look': look, 'found': {'background': hx(bg), 'primary': hx(primary), 'otherAccents': [hx(c) for c in found[1:]],
                                       'dark': dark}}, sys.stdout, indent=1)
    print()


if __name__ == '__main__':
    main()
