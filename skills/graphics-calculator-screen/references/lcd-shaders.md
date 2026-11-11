# Graphics calculator screen: the five shaders

Add each with `addEffect` `kind: "shader"`, passing the source below and its uniforms. Tella adds its shader library (`tella_hash2d`, `tella_noise2d`, `tella_fbm2d`) to the source, so these bodies call it without defining it. `win` is always the screen window `[260, 165, 1400, 750]` (x, y, w, h) at 1920×1080. Bind any `time` uniform to `{time: "seconds"}` with `bindProperty` after adding the effect (`inspect_motion_node_properties` lists its field).

## 1. `lcdtex`: the LCD glass colour (on `lcdbg`, a full-frame fill)

Uniforms: `win`. The two `float3` lines are the tint: classic green-grey below; amber `(0.80, 0.58, 0.24)` / `(0.86, 0.64, 0.29)`; blue `(0.55, 0.65, 0.74)` / `(0.61, 0.71, 0.79)`.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float4 win;
half4 main(float2 p){
  float2 uv = (p - win.xy) / win.zw;
  float3 top = float3(0.66, 0.725, 0.545);
  float3 bot = float3(0.72, 0.775, 0.59);
  float3 col = mix(top, bot, clamp(uv.y, 0.0, 1.0));
  col *= 1.0 - 0.07 * length(uv - float2(0.42, 0.38));
  col += (tella_fbm2d(p / 240.0, 3) - 0.5) * 0.045;
  col += (tella_fbm2d(p / 35.0 + 11.0, 2) - 0.5) * 0.015;
  col += (tella_hash2d(floor(p / 1.5)) - 0.5) * 0.03;
  return half4(col, 1.0);
}
```

## 2. `lcdpix`: the dot matrix (on the `screen` group)

Resamples everything dark drawn in the group onto a 5 px grid of rounded square dots, with each dot's shadow cast on the glass behind it. Light pixels (the text inside an inverse menu tab) stay unlit, so inverse video works.

Uniforms: `win`, `cell` 5, `dotSize` 0.8, `shadowOff` [4.5, 5.5], `ink` [0.08, 0.12, 0.17, 0.95] (amber [0.17, 0.09, 0.03, 0.95], blue [0.04, 0.09, 0.22, 0.95]), `shadowAlpha` 0.22, `matrixAlpha` 0.03 (the faint unlit dot grid).

```glsl
uniform shader image;
uniform float2 resolution;
uniform float4 win;
uniform float cell;
uniform float dotSize;
uniform float2 shadowOff;
uniform half4 ink;
uniform float shadowAlpha;
uniform float matrixAlpha;
float dk(float2 q){
  half4 c = image.eval(q);
  float a = c.a;
  if (a < 0.002) { return 0.0; }
  float l = dot(c.rgb / a, half3(0.3, 0.59, 0.11));
  return a * (1.0 - smoothstep(0.35, 0.55, l));
}
float cov(float2 c){
  float2 b = win.xy + (c + 0.5) * cell;
  float o = cell * 0.22;
  float a = dk(b) * 0.4;
  a += dk(b + float2(o, o)) * 0.15;
  a += dk(b + float2(-o, o)) * 0.15;
  a += dk(b + float2(o, -o)) * 0.15;
  a += dk(b + float2(-o, -o)) * 0.15;
  return smoothstep(0.3, 0.6, a);
}
float dmask(float2 f, float soft){
  float h = dotSize * 0.5; float r = 0.16;
  float2 q = abs(f - 0.5) - (h - r);
  float d = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
  return 1.0 - smoothstep(-soft, soft, d);
}
float inside(float2 l, float2 g){ return (l.x >= 0.0 && l.y >= 0.0 && l.x < g.x && l.y < g.y) ? 1.0 : 0.0; }
half4 main(float2 p){
  float2 g = win.zw / cell;
  float2 l = (p - win.xy) / cell;
  float a = 0.0;
  if (inside(l, g) > 0.5) {
    float2 c = floor(l); float2 f = l - c;
    float lit = cov(c);
    float m = dmask(f, 0.7 / cell);
    float var = 0.88 + 0.12 * tella_hash2d(c + 17.0);
    float yv = mix(1.0, 0.84, l.y / g.y) * mix(0.96, 1.0, l.x / g.x);
    a = (lit * ink.a * var * yv + matrixAlpha * (1.0 - lit)) * m;
  }
  float2 ls = (p - shadowOff - win.xy) / cell;
  float sh = 0.0;
  if (inside(ls, g) > 0.5) {
    float2 cs = floor(ls); float2 fs = ls - cs;
    sh = cov(cs) * dmask(fs, 0.22) * shadowAlpha * mix(1.0, 0.8, ls.y / g.y);
  }
  float outA = a + sh * (1.0 - a);
  return half4(ink.rgb * outA, outA);
}
```

## 3. `glassfx`: inner shadow, reflection, light sweep, a smudge and dust (on `glass`, a transparent full-frame fill above the screen)

Uniforms: `win`, `time` (bound to seconds). The sweep crosses once about every 4.4 s; the smudge sits at (1395, 330) and the smear at (430, 770), away from the stack values.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float4 win;
uniform float time;
float sdRB(float2 p, float2 b, float r){ float2 q=abs(p)-b+r; return length(max(q,0.0))+min(max(q.x,q.y),0.0)-r; }
half4 main(float2 p){
  float2 c = win.xy + win.zw * 0.5;
  float d = sdRB(p - c, win.zw * 0.5, 10.0);
  if (d > 1.0) { return half4(0.0); }
  float ins = 1.0 - smoothstep(-0.5, 0.5, d);
  float top = p.y - win.y; float left = p.x - win.x;
  float right = win.x + win.z - p.x; float bot = win.y + win.w - p.y;
  float sh = 0.42 * exp(-top / 26.0) + 0.26 * exp(-left / 20.0) + 0.08 * exp(-right / 26.0) + 0.05 * exp(-bot / 30.0);
  sh += 0.3 * (1.0 - smoothstep(0.0, 3.0, -d));
  float2 uv = (p - win.xy) / win.zw;
  float diag = uv.x * 0.75 + uv.y * 0.55;
  float refl = 0.055 * smoothstep(0.05, 0.4, diag) * (1.0 - smoothstep(0.4, 0.9, diag));
  float s = diag - (time / 7.5) * 1.7 + 0.25;
  float sweep = 0.075 * exp(-(s * s) / 0.004) + 0.035 * exp(-((s - 0.1) * (s - 0.1)) / 0.0008);
  float2 fp = p - float2(1395.0, 330.0);
  float ca = cos(0.5); float sa = sin(0.5);
  fp = float2(fp.x * ca + fp.y * sa, -fp.x * sa + fp.y * ca) / float2(140.0, 185.0);
  float r = length(fp + (tella_noise2d(p / 70.0) - 0.5) * 0.12);
  float ridges = 0.5 + 0.5 * sin(r * 100.0 + tella_noise2d(p / 22.0) * 2.5);
  float fall = 1.0 - smoothstep(0.5, 1.0, r);
  float smudge = fall * (0.018 + 0.05 * ridges * ridges) * (0.55 + 0.45 * tella_noise2d(p / 45.0));
  float2 sp = (p - float2(430.0, 770.0)) / float2(280.0, 95.0);
  float smear = 0.05 * (1.0 - smoothstep(0.2, 1.0, length(sp))) * tella_fbm2d(p / 55.0, 3);
  float2 gc = floor(p / 34.0); float h = tella_hash2d(gc);
  float dust = 0.0;
  if (h > 0.972) {
    float2 off = float2(tella_hash2d(gc + 7.0), tella_hash2d(gc + 13.0)) * 28.0 + 3.0;
    float rad = 0.9 + 2.4 * tella_hash2d(gc + 21.0);
    float dd = length(p - (gc * 34.0 + off));
    dust = 0.55 * (1.0 - smoothstep(rad * 0.35, rad, dd));
  }
  float white = clamp(refl + sweep + smudge + smear + dust, 0.0, 1.0);
  float black = clamp(sh, 0.0, 0.9);
  float a = white + black * (1.0 - white);
  return half4(half3(white), a) * ins;
}
```

## 4. `bezelfx`: the dark plastic bezel with a bevelled window (on `bezel`, a full-frame fill `#2A2D30`, on top)

Uniforms: `win`. Transparent inside the window, so it frames everything beneath.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float4 win;
float sdRB(float2 p, float2 b, float r){ float2 q=abs(p)-b+r; return length(max(q,0.0))+min(max(q.x,q.y),0.0)-r; }
half4 main(float2 p){
  float2 wc = win.xy + win.zw * 0.5;
  float dw = sdRB(p - wc, win.zw * 0.5, 10.0);
  if (dw < -1.5) { return half4(0.0); }
  float tex = (tella_hash2d(floor(p * 0.8)) - 0.5) * 0.022 + (tella_noise2d(p / 3.0) - 0.5) * 0.025 + (tella_fbm2d(p / 300.0, 3) - 0.5) * 0.02;
  float3 col = float3(0.155, 0.162, 0.172) * (1.1 - 0.25 * p.y / resolution.y) + tex;
  float bw = 18.0;
  float bev = 1.0 - smoothstep(0.0, bw, dw);
  float side = clamp((p.y - wc.y) / (win.w * 0.5), -1.0, 1.0);
  float3 bevCol = float3(0.045, 0.048, 0.052) + 0.035 * max(side, 0.0) * (dw / bw);
  col = mix(col, bevCol, smoothstep(0.0, 1.0, bev) * 0.95);
  float ridge = smoothstep(bw - 2.5, bw, dw) * (1.0 - smoothstep(bw, bw + 2.5, dw));
  col += ridge * (0.025 + 0.03 * max(side, 0.0));
  col *= 1.0 - 0.25 * (1.0 - smoothstep(bw, bw + 30.0, dw)) * max(-side, 0.0);
  float alpha = smoothstep(-1.5, 0.5, dw);
  return half4(col * alpha, alpha);
}
```

## 5. `camera`: a slow push with handheld drift (first effect on the `device` group)

Uniforms: `yaw` 0, `pitch` 0, `zoom` 1.04, `focal` 1.6, `blurAmt` 0, `time` (bound to seconds), `drift` 0.02. It zooms 1.8 % per 7.5 s; a small `yaw`/`pitch` (±0.15 rad) tilts the calculator if wanted.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float yaw;
uniform float pitch;
uniform float zoom;
uniform float focal;
uniform float blurAmt;
uniform float time;
uniform float drift;
float3 rotX(float3 v, float a){ float c = cos(a); float s = sin(a); return float3(v.x, c * v.y - s * v.z, s * v.y + c * v.z); }
float3 rotY(float3 v, float a){ float c = cos(a); float s = sin(a); return float3(c * v.x + s * v.z, v.y, -s * v.x + c * v.z); }
half4 main(float2 p){
  float z = zoom * (1.0 + 0.018 * time / 7.5);
  float2 sh = float2(tella_noise2d(float2(time * 0.5, 21.3)) - 0.5, tella_noise2d(float2(time * 0.5, 31.9)) - 0.5) * drift * 0.25;
  float2 sc = (p - resolution * 0.5) / resolution.y;
  float3 r = float3(sc, focal);
  float3 n = rotY(rotX(float3(0.0, 0.0, 1.0), pitch), yaw);
  float3 P0 = float3(0.0, 0.0, focal);
  float t = dot(P0, n) / dot(r, n);
  float3 h = r * t - P0;
  float3 u = rotX(rotY(h, -yaw), -pitch);
  float2 s0 = (u.xy / z + sh) * resolution.y + resolution * 0.5;
  float rad = blurAmt * abs(t - 1.0) * resolution.y;
  half4 acc = image.eval(s0);
  float wsum = 1.0;
  if (rad > 0.35) {
    for (int i = 0; i < 12; i++) {
      float fi = float(i);
      float ang = fi * 2.39996;
      float rr = sqrt((fi + 0.5) / 12.0) * rad;
      acc += image.eval(s0 + float2(cos(ang), sin(ang)) * rr);
      wsum += 1.0;
    }
  }
  return acc / wsum;
}
```
