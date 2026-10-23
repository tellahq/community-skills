#!/usr/bin/env python3
"""Render the flower-transition stingers as transparent ProRes 4444 .mov files.

Usage: NF=72 W=1920 H=1080 WORKDIR=/workspace/flower-transitions python3 gen.py [variant ...]
Needs stripes.mp4, bloom.mp4, grid.mp4 (the three source graphics) in WORKDIR.
Output: WORKDIR/out<NF>/<variant>.mov. Full cover from frame round(NF*10/24) to round(NF*13/24)-1.
"""
import numpy as np, subprocess, sys, os
W = int(os.environ.get("W", "1920")); H = int(os.environ.get("H", "1080")); FPS = 30
N = int(os.environ.get("NF", "72"))
NIN = round(N*10/24); NHE = round(N*13/24)
D = os.environ.get("WORKDIR", "/workspace/flower-transitions")

def read(src, ss, vf):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss), "-i", f"{D}/{src}.mp4", "-frames:v", str(N),
           "-filter_complex", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    assert len(a) == N, (src, len(a), "source too short for this in-point/length")
    return a

# mirror-tile (kaleidoscope continues sideways, native scale) or scale-to-cover
MIRROR = "[0:v]split=3[a][b][c];[a]hflip[a2];[c]hflip[c2];[a2][b][c2]hstack=3,scale=-2:%d,crop=%d:%d{x}" % (H, W, H)
COVER = "[0:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d{x}" % (W, H, W, H)
def mirror(src, ss, extra=""): return read(src, ss, MIRROR.format(x=extra))
def cover(src, ss, extra=""): return read(src, ss, COVER.format(x=extra))

def rings(seed=3):
    """New graphic: wavy concentric rings in the stripes palette, pixel-stepped, with grain."""
    rng = np.random.default_rng(seed)
    pal = np.array([(34,110,135),(52,190,136),(98,118,214),(148,162,230),(180,200,234),(45,161,135)], np.float32)
    s = 12
    yy, xx = np.mgrid[0:H//s+1, 0:W//s+1].astype(np.float32)
    cx, cy = W/s/2, H/s/2
    r = np.hypot(xx-cx, yy-cy); th = np.arctan2(yy-cy, xx-cx)
    out = []
    for f in range(N):
        v = r/5.5 - f*0.35 + 1.4*np.sin(th*6 + f*0.08) + 0.6*np.sin(r/7 + f*0.2)
        img = pal[np.floor(v).astype(int) % len(pal)]
        img = np.repeat(np.repeat(img, s, 0), s, 1)[:H, :W]
        img = img + rng.normal(0, 14, (H, W, 1)).astype(np.float32)
        out.append(np.clip(img, 0, 255).astype(np.uint8))
    return out

def combo():
    """Bloom flower keyed (by its light-green petals) over the stripes."""
    bg = mirror("stripes", 7.5); fl = cover("bloom", 2.6)
    out = []
    for f in range(N):
        b, l = bg[f].astype(np.float32), fl[f].astype(np.float32)
        a = np.clip((l[..., 1:2] - 160) / 30, 0, 1)
        out.append((b*(1-a) + l*a).astype(np.uint8))
    return out

# ---- masks: alpha (H,W) in 0..1 for frame f ----
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W/2, H/2
R = np.hypot(xx-cx, yy-cy); TH = np.arctan2(yy-cy, xx-cx)

def phase(f):
    if f < NIN: return "in", ((f+1)/NIN) ** 1.5
    if f < NHE: return "hold", 1.0
    q = (f-NHE+1)/(N-NHE); return "out", 1-(1-q)**3

def aa(d): return np.clip(d/1.5 + 0.5, 0, 1)
FULL = lambda: np.ones((H, W), np.float32)

def m_iris(f, petals=8, amp=0.08):
    ph, p = phase(f)
    if ph == "hold": return FULL()
    rmax = np.hypot(cx, cy) * 1.05 / (1-amp)
    edge = (1 + amp*np.sin(petals*TH + f*0.15)) * p * rmax
    return aa(edge - R) if ph == "in" else aa(R - edge)

def m_wave(f, rev=False):
    ph, p = phase(f)
    if ph == "hold": return FULL()
    A = 70; x = (W - xx) if rev else xx
    e = p*(W + 2*A) - A + A*np.sin(yy/80 + f*0.5)
    return aa(e - x) if ph == "in" else aa(x - e)

def m_diag(f):
    ph, p = phase(f)
    if ph == "hold": return FULL()
    u = xx + yy*0.7; e = p*(W + H*0.7 + 40) - 20
    return aa(e - u) if ph == "in" else aa(u - e)

def m_blinds(f, n=12):
    ph, p = phase(f)
    if ph == "hold": return FULL()
    bh = H/n; i = np.floor(yy/bh); c = (i+0.5)*bh
    pi = np.clip((p - i/n*0.4)/0.6, 0, 1)
    if ph == "in": return aa(pi*bh/2*1.02 - np.abs(yy-c))
    return aa(np.abs(yy-c) - pi*bh/2*1.02)

def m_tiles(f, order="diag", cols=8, rows=5):
    ph, p = phase(f)
    if ph == "hold": return FULL()
    cw, ch = W/cols, H/rows
    ci, cj = np.minimum(np.floor(xx/cw), cols-1), np.minimum(np.floor(yy/ch), rows-1)
    if order == "diag": d = (ci+cj)/(cols+rows-2)*0.45
    else: d = np.random.default_rng(7).random((rows, cols))[cj.astype(int), ci.astype(int)]*0.45
    pi = np.clip((p - d)/0.55, 0, 1)
    k = np.maximum(np.abs(xx-(ci+0.5)*cw)/(cw/2), np.abs(yy-(cj+0.5)*ch)/(ch/2))
    sz = pi*1.12 if ph == "in" else (1-pi)*1.12   # grow in, shrink out
    return np.where(sz >= 0.92, 1.0, aa((sz - k)*cw/2) * (sz > 0.02))

VARIANTS = {
    "t1_stripes_iris":        (lambda: mirror("stripes", 0.0), m_iris),
    "t2_bloom_wave":          (lambda: cover("bloom", 1.4), lambda f: m_wave(f)),
    "t3_grid_tiles":          (lambda: mirror("grid", 0.4), lambda f: m_tiles(f, "diag")),
    "t4_stripes_pink_blinds": (lambda: mirror("stripes", 5.0, ",hue=h=150:s=1.15"), m_blinds),
    "t5_bloom_warm_iris":     (lambda: cover("bloom", 4.2, ",hue=h=170:s=1.1"), lambda f: m_iris(f, 6, 0.1)),
    "t6_combo_diag":          (combo, m_diag),
    "t7_rings_wave":          (rings, lambda f: m_wave(f, rev=True)),
    "t8_grid_violet_tiles":   (lambda: mirror("grid", 1.5, ",hue=h=60"), lambda f: m_tiles(f, "rand")),
}

def build(name):
    content, mask = VARIANTS[name]
    fr = content()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-qscale:v", "11",
                          "-pix_fmt", "yuva444p10le", f"{D}/out{N}/{name}.mov"], stdin=subprocess.PIPE)
    for f in range(N):
        p.stdin.write(np.dstack([fr[f], (mask(f)*255).astype(np.uint8)]).tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    os.makedirs(f"{D}/out{N}", exist_ok=True)
    for n in (sys.argv[1:] or VARIANTS):   # run a few at a time: long renders use a lot of memory
        build(n); print("built", n, flush=True)
