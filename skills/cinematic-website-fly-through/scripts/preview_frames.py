#!/usr/bin/env python3
"""Pull the check frames out of a get_motion_preview MP4 with ffmpeg and tile them into one labelled sheet.

  python3 preview_frames.py spec.json preview.mp4 --out /workspace/check          # preview starts at 0 s
  python3 preview_frames.py spec.json preview.mp4 --out /workspace/check --offset 0   # --offset = the preview's startTimeMs / 1000

Frames: for every shot its middle and its end (just before the card starts), for every cut C-0.3, C and C+0.3, the end card
at E, E+0.5 and the last frame. Writes check/f_<time>.png, check/sheet.png (labelled, 4 per row, 1920 px wide: under the
2000 px view_image limit) and prints the times. It also measures the logo (or name) on the last frame: the bounding box of the
pixels that differ from the end card, in 1920x1080 pixels, its centre's offset from (960, 540) and its size, with a warning
when it is off centre by more than 10 px or small.
Use it for the REQUIRED checks: no plane edge in each shot's middle and end frame; the card fully up on each cut; the logo on screen.
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('spec')
ap.add_argument('mp4')
ap.add_argument('--out', default='check')
ap.add_argument('--offset', type=float, default=0.0, help='seconds of the document the MP4 starts at')
ap.add_argument('--width', type=int, default=480, help='frame width on the sheet (4 per row)')
ns = ap.parse_args()

spec = json.load(open(ns.spec))
D = float(spec.get('duration', 12))
cuts = spec['cuts']
E = float(spec.get('endAt', cuts[-1] + 1.0))
times = []
for i, C in enumerate(cuts):
    S = 0.0 if i == 0 else cuts[i - 1] + 0.82
    times += [(S + (C - 0.3 - S) / 2, 'shot %d middle' % (i + 1)), (C - 0.3, 'shot %d end' % (i + 1)),
              (C, 'cut %d' % (i + 1)), (C + 0.3, 'cut %d +0.3' % (i + 1))]
times += [(E, 'end card'), (E + 0.5, 'end card +0.5'), (D - 0.04, 'last frame')]
os.makedirs(ns.out, exist_ok=True)
files = []
for t, label in times:
    t = max(0.0, min(t, D - 0.04))
    f = os.path.join(ns.out, 'f_%06.2f.png' % t)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '%.3f' % (t - ns.offset), '-i', ns.mp4, '-frames:v', '1',
                    '-vf', 'scale=%d:-1' % ns.width, f], check=True)
    files.append((f, '%.2fs %s' % (t, label)))
try:
    from PIL import Image, ImageDraw
    ims = [Image.open(f) for f, _ in files]
    w, h = ims[0].size
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * (h + 22)), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for i, (im, (_, label)) in enumerate(zip(ims, files)):
        x, y = (i % cols) * w, (i // cols) * (h + 22)
        sheet.paste(im, (x, y + 22))
        d.text((x + 6, y + 5), label, fill=(255, 255, 255))
    sheet.save(os.path.join(ns.out, 'sheet.png'))
except ImportError:
    print('pillow missing: pip install --break-system-packages pillow for the sheet', file=sys.stderr)


def measure_logo():
    """Bounding box of what stands out from the end card on the last frame, in 1920x1080 pixels."""
    from PIL import Image
    f = os.path.join(ns.out, 'last_full.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '%.3f' % (D - 0.04 - ns.offset), '-i', ns.mp4, '-frames:v', '1', f],
                   check=True)
    im = Image.open(f).convert('RGB')
    w, h = im.size
    px = im.load()
    probes = [px[int(w * x), int(h * y)] for x, y in ((0.12, 0.5), (0.88, 0.5), (0.5, 0.17), (0.5, 0.83), (0.12, 0.2), (0.88, 0.8))]
    bg = tuple(sorted(p[c] for p in probes)[len(probes) // 2] for c in range(3))
    xs, ys = [], []
    for y in range(int(h * 0.1), int(h * 0.9)):       # the middle of the frame: the lens darkens the corners
        for x in range(int(w * 0.08), int(w * 0.92)):
            p = px[x, y]
            if max(abs(p[c] - bg[c]) for c in range(3)) > 48:
                xs.append(x)
                ys.append(y)
    if not xs:
        return {'found': False, 'warning': 'nothing stands out from the end card on the last frame: the logo is missing or too faint'}
    k = 1920 / w
    box = [round(min(xs) * k), round(min(ys) * k), round((max(xs) + 1) * k), round((max(ys) + 1) * k)]
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    r = {'found': True, 'background': '#%02x%02x%02x' % bg, 'box': box, 'size': [box[2] - box[0], box[3] - box[1]],
         'centre': [round(cx), round(cy)], 'offset': [round(cx - 960), round(cy - 540)]}
    warn = []
    if abs(cx - 960) > 10 or abs(cy - 540) > 10:
        warn.append('off centre by %d, %d px' % (cx - 960, cy - 540))
    bw, bh = r['size']
    if bw < 380 and bh < 300:
        warn.append('small: %dx%d px (a wordmark should be at least 960 px wide, a symbol about 400 px tall)' % (bw, bh))
    if warn:
        r['warning'] = '; '.join(warn)
    return r


out = {'frames': [{'file': f, 'what': l} for f, l in files], 'sheet': os.path.join(ns.out, 'sheet.png')}
try:
    out['logo'] = measure_logo()
except ImportError:
    pass
print(json.dumps(out, indent=1))
