import numpy as np, random, math
from PIL import Image
# Renders PNG frames to fr/ (create it first). Set SRC to the user's image.
SRC = 'image.png'
S = 720; FPS = 30; T = 4.3; N = int(T * 2 * FPS)
src = Image.open(SRC).convert('RGB').resize((S, S), Image.LANCZOS)

def rot(img, deg):
    # rotate with a cover scale so no empty corners show
    r = math.radians(deg % 90); s = math.cos(r) + math.sin(r)
    big = img.resize((int(S * s) + 1, int(S * s) + 1), Image.BICUBIC).rotate(-deg, resample=Image.BICUBIC)
    w = big.size[0]; o = (w - S) // 2
    return big.crop((o, o, o + S, o + S))

def grid(base, n, rng, p):
    a = np.asarray(base); out = a.copy(); t = S // n
    for i in range(n):
        for j in range(n):
            if rng.random() > p: continue
            si, sj = rng.randrange(n), rng.randrange(n)
            tile = a[si*t:(si+1)*t, sj*t:(sj+1)*t]
            if rng.random() < .5:
                z = t // 2; y = rng.randrange(t - z + 1); x = rng.randrange(t - z + 1)
                tile = np.asarray(Image.fromarray(tile[y:y+z, x:x+z]).resize((t, t), Image.BICUBIC))
            tile = np.rot90(tile, rng.randrange(4))
            out[i*t:(i+1)*t, j*t:(j+1)*t] = tile
    return out

def ease(x): return x * x * (3 - 2 * x)

for f in range(N):
    c, tt = divmod(f / FPS, T)
    base = 90 * int(c)
    rng = random.Random(int(c) * 1000 + f // 2)
    if tt < .4: arr = np.asarray(rot(src, base))
    elif tt < 1.2: arr = grid(rot(src, base), 2, rng, 1)
    elif tt < 2.0: arr = grid(rot(src, base), 4, rng, 1)
    elif tt < 2.8: arr = grid(rot(src, base), 8, rng, 1)
    elif tt < 3.9:
        u = (tt - 2.8) / 1.1
        arr = grid(rot(src, base + 90 * ease(u)), 8, rng, max(0, 1 - u * 1.1))
    else: arr = np.asarray(rot(src, base + 90))
    Image.fromarray(arr).save(f'fr/{f:04d}.png')
