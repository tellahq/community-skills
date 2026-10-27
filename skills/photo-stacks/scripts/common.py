"""Shared helpers for Louise's minimal motion set (Tella freeform batches).
Measures Inter like Tella's renderer (variable Inter, opsz 14) so word layouts line up."""
import json, os, urllib.request
from PIL import ImageFont
FONT = '/workspace/Inter.ttf'
FONT_URL = 'https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf'
INK, GREY, BG, CARD, ACCENT = '#141414', '#8C8C8C', '#ECECEC', '#F4F4F2', '#D6336C'
_f = {}
def width(text, size, wght=300):
    if not os.path.exists(FONT):
        urllib.request.urlretrieve(FONT_URL, FONT)
    k = (size, wght)
    if k not in _f:
        f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([14, wght]); _f[k] = f
    return _f[k].getlength(text)

def title(nid, text, x, ycenter, size, color=INK, w=None, align='left', start=0, dur=10, wght=300, ls=0):
    """addTitle whose line box is centred on ycenter. weight >400 or <400 set afterwards (addTitle only takes 400-700)."""
    if w is None: w = width(text, size, wght) + 40
    c = [{"type": "addTitle", "nodeId": nid, "start": start, "duration": dur, "text": text,
          "box": {"x": round(x, 1), "y": round(ycenter - size * 0.6, 1), "width": round(w, 1)},
          "font": "inter", "fontSize": size, "color": color, "align": align, "weight": 400}]
    if ls: c[0]["letterSpacing"] = ls
    if wght != 400:
        c.append({"type": "setProperty", "node": nid, "property": "field:content/style/fontWeight", "value": wght})
    return c

def keys(node, prop, ks):
    """ks = [(at, value, easing-or-None)]; never two keys at the same time."""
    out = []
    for a, v, e in ks:
        a = round(a, 3)
        if out and abs(out[-1]["at"] - a) < 1e-6:
            out[-1] = {"at": a, "value": v, **({"easing": e} if e else {})}; continue
        out.append({"at": a, "value": v, **({"easing": e} if e else {})})
    return {"type": "setKeyframes", "node": node, "property": prop, "keys": out}

def word_in(nid, t, blur=10, dy=0, dx=0):
    """Standard word reveal: fade + de-blur (+ optional slide) starting just before the spoken word."""
    c = [keys(nid, 'opacity', [(0, 0, None), (max(t - 0.05, 0), 0, 'easeOutCubic'), (t + 0.3, 1, None)]),
         keys(nid, 'blur', [(0, blur, None), (max(t - 0.05, 0), blur, 'easeOutCubic'), (t + 0.35, 0, None)])]
    if dy: c.append(keys(nid, 'y', [(0, dy, None), (max(t - 0.05, 0), dy, 'easeOutCubic'), (t + 0.45, 0, None)]))
    if dx: c.append(keys(nid, 'x', [(0, dx, None), (max(t - 0.05, 0), dx, 'easeOutCubic'), (t + 0.45, 0, None)]))
    return c

def image_asset(aid, uri, w, h):
    return {"type": "asset.set", "kind": "images", "asset": {"id": aid, "source": {"type": "uri", "uri": uri}, "dimensions": {"width": w, "height": h}}}

def raster(nid, aid, x, y, w, h, start, dur, name=None):
    n = {"type": "node.insert", "parent": "", "node": {"type": "raster", "id": nid, "source": {"type": "asset", "assetId": aid},
         "destination": {"x": round(x, 1), "y": round(y, 1), "width": round(w, 1), "height": round(h, 1)}, "fit": "cover",
         "sampling": {"filter": "linear", "mipmap": "linear"},
         "common": {"start": {"seconds": start}, "duration": {"seconds": round(dur, 3)}}}}
    if name: n["meta"] = {"name": name}
    return n

def dump(c, path):
    with open(path, 'w') as f:
        f.write('[\n' + ',\n'.join(json.dumps(x, separators=(',', ':'), ensure_ascii=False) for x in c) + '\n]\n')
    print(f'{len(c)} commands -> {path}')
