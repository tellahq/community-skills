# Retro footage looks: shader sources

Four SkSL runtime shaders, each tested on 1920x1080 footage in Tella Motion. Pass the source as one string to `addEffect` with `kind: "shader"` and give every uniform a starting value (e.g. `{time:[0], tracking:[0], bleed:[10], noise:[0.07]}`). Tella supplies `image` and `resolution`.

## VHS (`vhs`) on a group of footage plus OSD titles

| uniform | range | use |
|---|---|---|
| time | bind `{time:"seconds"}` | drives the per-frame noise (29.97 fps) and the band's roll |
| tracking | 0–1 | wavy horizontal shear plus a stronger band |
| bleed | 6–14 px | how far chroma smears to the right of luma |
| noise | 0.04–0.1 | tape grain |

```glsl
uniform shader image;
uniform float2 resolution;
uniform float time;
uniform float tracking;
uniform float bleed;
uniform float noise;

float hash(float2 p) {
  float3 p3 = fract(float3(p.x, p.y, p.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}
float luma(float3 c) { return dot(c, float3(0.299, 0.587, 0.114)); }
float2 chroma(float3 c) { return float2(dot(c, float3(0.596, -0.274, -0.322)), dot(c, float3(0.211, -0.523, 0.312))); }

half4 main(float2 p) {
  float2 uv = p / resolution;
  float tf = floor(time * 29.97);
  float jit = (hash(float2(floor(p.y / 2.0), tf)) - 0.5) * 1.8;
  float hs = smoothstep(0.935, 0.985, uv.y);
  jit += hs * (hash(float2(floor(p.y / 3.0), tf)) * 0.7 + 0.3) * 38.0;
  float bandY = 1.0 - fract(time * 0.09 + 0.35);
  float bd = (uv.y - bandY) * 38.0;
  float band = exp(-bd * bd) * (0.35 + tracking);
  jit += band * (hash(float2(floor(p.y / 2.0), tf + 5.0)) - 0.5) * 46.0;
  jit += tracking * sin(uv.y * 23.0 + time * 31.0) * 28.0 * (0.6 + 0.4 * hash(float2(floor(p.y / 4.0), tf)));
  float x = p.x + jit;
  float3 a = image.eval(float2(x, p.y)).rgb;
  float3 l1 = image.eval(float2(x - 2.0, p.y)).rgb;
  float3 l2 = image.eval(float2(x + 2.0, p.y)).rgb;
  float Y = luma(a * 0.5 + (l1 + l2) * 0.25);
  float Yb = luma(image.eval(float2(x - 5.0, p.y)).rgb);
  Y += (Y - Yb) * 0.22;
  float2 iq = float2(0.0);
  for (int i = 0; i < 8; i++) {
    float o = (float(i) - 3.5) * bleed * 0.4 - bleed * 0.7;
    iq += chroma(image.eval(float2(x + o, p.y)).rgb);
  }
  iq = iq / 8.0 * 0.9;
  float3 col = float3(Y + 0.956 * iq.x + 0.621 * iq.y, Y - 0.272 * iq.x - 0.647 * iq.y, Y - 1.106 * iq.x + 1.703 * iq.y);
  col = col * 0.88 + 0.055;
  col = pow(max(col, 0.0), float3(0.94, 0.98, 1.06));
  col += (hash(p * 0.5 + tf * 7.13) - 0.5) * noise;
  col += (hash(float2(floor(p.x / 3.0), floor(p.y / 2.0) + tf)) - 0.5) * noise * 0.6;
  float dl = hash(float2(floor(p.y / 2.0), tf * 1.7));
  float st = hash(float2(tf, floor(p.y / 2.0))) * resolution.x;
  col += step(0.9988, dl) * smoothstep(st, st + 6.0, p.x) * (1.0 - smoothstep(st + 40.0, st + 160.0, p.x)) * 0.7;
  col = mix(col, float3(hash(p + tf)), hs * 0.3);
  col += band * hash(float2(floor(p.x / 4.0), tf)) * 0.22;
  col *= 0.95 + 0.05 * mod(floor(p.y), 2.0);
  float2 v = uv - 0.5;
  col *= 1.0 - dot(v, v) * 0.35;
  return half4(half3(clamp(col, 0.0, 1.0)), 1.0);
}
```

## CRT screen (`crt`, then a `glow`) on the media node

| uniform | range | use |
|---|---|---|
| time | bind seconds | rolling band, 60 Hz flicker, grain |
| power | 0–1 | power-on: a line opens into the full picture with a white flash |
| curvature | 0.04–0.08 | barrel bulge of the glass |
| scan | 0.3–0.5 | scanline depth (bright areas bloom over the lines) |
| lines | 160–220 | scanline count. Finer lines vanish or moiré in previews |
| snow | 0–1 | channel-change static with tearing |

```glsl
uniform shader image;
uniform float2 resolution;
uniform float time;
uniform float power;
uniform float curvature;
uniform float scan;
uniform float lines;
uniform float snow;

float hash(float2 p) {
  float3 p3 = fract(float3(p.x, p.y, p.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

half4 main(float2 p) {
  float2 c = (p / resolution) * 2.0 - 1.0;
  float sx = mix(0.03, 1.0, smoothstep(0.0, 0.4, power));
  float sy = mix(0.004, 1.0, smoothstep(0.4, 1.0, power));
  c = c / float2(sx, sy);
  float r2 = dot(c, c);
  float2 cc = c * (1.0 + curvature * r2) * 1.015;
  float2 suv = cc * 0.5 + 0.5;
  float2 sp = suv * resolution;
  float2 hb = resolution * 0.5;
  float R = 64.0;
  float2 q = abs(sp - hb) - (hb - R);
  float d = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - R;
  float inside = 1.0 - smoothstep(-2.5, 2.5, d);
  float tf = floor(time * 30.0);
  sp.x += snow * 90.0 * (hash(float2(floor(sp.y / 6.0), tf)) - 0.5);
  sp.y = mod(sp.y + snow * snow * resolution.y * 0.35 * hash(float2(tf, 3.0)), resolution.y);
  float ca = 1.5 + 3.0 * r2;
  float3 col;
  col.r = image.eval(sp + float2(ca, 0.0)).r;
  col.g = image.eval(sp).g;
  col.b = image.eval(sp - float2(ca, 0.0)).b;
  float3 soft = (image.eval(sp + float2(2.5, 0.0)).rgb + image.eval(sp - float2(2.5, 0.0)).rgb) * 0.5;
  col = mix(col, soft, 0.3);
  float luma = dot(col, float3(0.299, 0.587, 0.114));
  float s = 0.5 + 0.5 * cos(6.2831853 * suv.y * lines);
  float w = scan * mix(1.0, 0.45, luma);
  col *= 1.0 - w * (1.0 - s);
  float m = mod(floor(p.x), 3.0);
  float3 tri = m < 1.0 ? float3(1.0, 0.86, 0.86) : (m < 2.0 ? float3(0.86, 1.0, 0.86) : float3(0.86, 0.86, 1.0));
  col *= tri;
  float vig = pow(clamp(16.0 * suv.x * suv.y * (1.0 - suv.x) * (1.0 - suv.y), 0.0, 1.0), 0.22);
  col *= vig;
  float pos = fract(time * 0.11);
  float bd = (suv.y - pos) * 7.0;
  float band = exp(-bd * bd) * 0.05;
  col += band;
  col *= 1.0 + 0.012 * sin(time * 376.99);
  col += (hash(floor(p) + fract(time) * 97.0) - 0.5) * 0.035;
  col *= 1.12;
  float sn = hash(floor(p / 2.0) + tf * 13.0);
  col = mix(col, float3(sn) * 0.9, clamp(snow * 0.85, 0.0, 1.0));
  float flash = 1.0 - smoothstep(0.35, 1.0, power);
  col = mix(col, float3(0.92, 0.97, 1.0), flash * 0.9);
  float3 bezel = float3(0.018, 0.018, 0.02);
  float rim = (1.0 - smoothstep(0.0, 22.0, d)) * 0.05 * (1.0 - smoothstep(-0.0, 1.0, inside));
  float3 outc = mix(bezel + rim, col, inside);
  return half4(half3(clamp(outc, 0.0, 1.0)), 1.0);
}
```

## Halftone print (`halftone`) on the media node

| uniform | range | use |
|---|---|---|
| cell | 10–16 px (48 for the entry and exit) | screen pitch |
| amount | 0–1 | mix with the clean footage |
| misreg | 1.5–3 px | plate misregistration |

Before separation the shader lifts the input (levels, then gamma 0.8, then saturation ×1.35). Without that, dim archive footage turns into solid black dots. The dot radius is `sqrt(ink) × cell × 0.6`, so dot area tracks ink amount.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float cell;
uniform float amount;
uniform float misreg;

float hash(float2 p) {
  float3 p3 = fract(float3(p.x, p.y, p.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

float4 cmyk(float3 c) {
  c = clamp((c - 0.06) / 0.72, 0.0, 1.0);
  c = pow(c, float3(0.8));
  c = clamp(mix(float3(dot(c, float3(0.299, 0.587, 0.114))), c, 1.35), 0.0, 1.0);
  float k0 = 1.0 - max(c.r, max(c.g, c.b));
  float k = smoothstep(0.3, 1.0, k0) * 0.95;
  float3 cmy = clamp((1.0 - c - k) / max(1.0 - k, 0.001), 0.0, 1.0) * 0.85;
  return float4(cmy, k);
}

float dotCover(float2 p, float ang, float s, int ch, float2 off) {
  float cs = cos(ang);
  float sn = sin(ang);
  float2 q = float2(cs * p.x + sn * p.y, -sn * p.x + cs * p.y);
  float2 cq = (floor(q / s) + 0.5) * s;
  float2 cp = float2(cs * cq.x - sn * cq.y, sn * cq.x + cs * cq.y);
  float4 ink = cmyk(clamp(image.eval(clamp(cp + off, float2(0.5), resolution - 0.5)).rgb, 0.0, 1.0));
  float v = ch == 0 ? ink.x : (ch == 1 ? ink.y : (ch == 2 ? ink.z : ink.w));
  float r = sqrt(clamp(v, 0.0, 1.0)) * s * 0.6;
  float dist = length(q - cq);
  return 1.0 - smoothstep(r - 0.9, r + 0.9, dist);
}

half4 main(float2 p) {
  float3 src = image.eval(p).rgb;
  float s = max(cell, 1.5);
  float3 paper = float3(0.965, 0.945, 0.9);
  float fib = hash(floor(p / 2.0)) - 0.5;
  paper += fib * 0.035;
  float cC = dotCover(p, 0.2618, s, 0, float2(misreg, 0.0));
  float cM = dotCover(p, 1.309, s, 1, float2(-misreg * 0.6, misreg * 0.5));
  float cY = dotCover(p, 0.0, s, 2, float2(0.0, -misreg * 0.4));
  float cK = dotCover(p, 0.7854, s, 3, float2(0.0));
  float3 col = paper;
  col *= mix(float3(1.0), float3(0.05, 0.62, 0.88), cC * 0.92);
  col *= mix(float3(1.0), float3(0.93, 0.16, 0.52), cM * 0.92);
  col *= mix(float3(1.0), float3(1.0, 0.88, 0.06), cY * 0.9);
  col *= mix(float3(1.0), float3(0.11, 0.1, 0.12), cK);
  float spot = hash(floor(p / 3.0) + 17.0);
  col *= 1.0 - step(0.9993, spot) * 0.5;
  col = mix(src, col, amount);
  return half4(half3(clamp(col, 0.0, 1.0)), 1.0);
}
```

## Photocopier (`copier`) on a group of footage plus pasted-on labels

| uniform | range | use |
|---|---|---|
| time | bind seconds | per-copy jitter, grain and speckle at 8 fps |
| level | 0.3–0.4 | toner threshold. Start at 0.33 for people in a normally lit room. 0.5 floods a mid-tone scene with black |
| jitter | 0–1.5 | misfeed: ±11 px shift and ±0.35° rotation per copy, which shows a black wedge at the edges |
| scan | 0–1 | the scanner bar sweeps down and turns footage into copy above it. At 1 the whole frame is copy and the bar is hidden |

Pair it with `sampleGrid: {numerator: 8, denominator: 1}` on the media node. `tf = floor(time*8 + 0.5)` matches that grid, which snaps to the nearest frame.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float time;
uniform float level;
uniform float jitter;
uniform float scan;

float hash(float2 p) {
  float3 p3 = fract(float3(p.x, p.y, p.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}
float luma(float3 c) { return dot(c, float3(0.299, 0.587, 0.114)); }
float Ls(float2 q) { return luma(image.eval(clamp(q, float2(0.5), resolution - 0.5)).rgb); }

half4 main(float2 p) {
  float3 src = image.eval(p).rgb;
  float tf = floor(time * 8.0 + 0.5);
  float2 c = resolution * 0.5;
  float ang = (hash(float2(tf, 3.1)) - 0.5) * 0.012 * jitter;
  float2 sh = (float2(hash(float2(tf, 7.7)), hash(float2(tf, 9.3))) - 0.5) * 22.0 * jitter;
  float2 d = p - c - sh;
  float2 q = c + float2(cos(ang) * d.x - sin(ang) * d.y, sin(ang) * d.x + cos(ang) * d.y) * 0.985;
  float Y = Ls(q);
  float blur = (Ls(q + float2(9.0, 0.0)) + Ls(q - float2(9.0, 0.0)) + Ls(q + float2(0.0, 9.0)) + Ls(q - float2(0.0, 9.0))) * 0.25;
  float Yc = Y + (Y - blur) * 1.25;
  float g = hash(floor(p / 2.0) + tf * 13.0);
  float g2 = hash(floor(p / 5.0) + tf * 3.0 + 41.0);
  float t = level + (g - 0.5) * 0.16 + (g2 - 0.5) * 0.08;
  float ink = 1.0 - smoothstep(t - 0.03, t + 0.03, Yc);
  float spk = step(0.9975, hash(floor(p / 3.0) + tf * 5.0));
  float drop = step(0.997, hash(floor(p / 4.0) + tf * 2.0 + 7.0));
  ink = clamp(ink + spk - drop * ink, 0.0, 1.0);
  float st = hash(float2(floor(p.x / 3.0), 1.0));
  ink = max(ink, step(0.994, st) * 0.55 * (0.6 + 0.4 * hash(float2(floor(p.y / 40.0), floor(p.x / 3.0)))));
  float outside = 1.0 - step(0.0, q.x) * step(q.x, resolution.x) * step(0.0, q.y) * step(q.y, resolution.y);
  ink = max(ink, outside * (0.85 + g * 0.15));
  float2 uv = p / resolution;
  float edge = smoothstep(0.035, 0.0, min(uv.x, 1.0 - uv.x)) * 0.6;
  float3 paper = float3(0.95, 0.94, 0.905) + (hash(floor(p / 3.0) + 91.0) - 0.5) * 0.03;
  float3 toner = float3(0.075, 0.072, 0.08) + g * 0.05;
  float3 col = mix(paper, toner, max(ink, edge * g));
  float sy = scan * resolution.y * 1.25 - resolution.y * 0.12;
  float done = step(p.y, sy);
  float bar = exp(-abs(p.y - sy) / 26.0);
  col = mix(src, col, done);
  col += float3(0.55, 1.0, 0.75) * bar * step(scan, 0.999) * 0.9;
  return half4(half3(clamp(col, 0.0, 1.0)), 1.0);
}
```
