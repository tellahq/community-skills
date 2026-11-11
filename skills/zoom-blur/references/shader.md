# Zoom blur: shader source

One SkSL runtime shader, the one playing in the example video ("Zoom blur: ollie"). Pass the source as one string to `addEffect` with `kind: "shader"`, `backdrop: true`, on a clear full-frame fill, and give every uniform a starting value. Tella supplies `image` and `resolution`. Distances scale with the canvas height, so the same numbers hold at 4K and in portrait.

| uniform | range | use | example value |
|---|---|---|---|
| amount | 0–0.7 | how far toward `center` each pixel's streak reaches; **the intensity to key** | 0 → 0.7 → 0.62 → 0 |
| center | 0–1, 0–1 | the point it pulls from, as a fraction of the frame (x, y); key it to follow the subject | x 0.52; y 0.47 → 0.36 → 0.30 |
| fringe | 0–0.5 | red streaks further than blue: the colour fan at the streak ends (0 = no fringe) | 0.4 |
| clear | 0–0.3 | radius, as a fraction of the height, that stays sharp around `center` | 0.04 |

Keep `amount × (1 + fringe)` at or below 1. Past it the red tap crosses `center` and samples the picture mirrored through it, a red ghost of the wrong part of the frame. With `fringe 0.4` that caps `amount` at about 0.71; with fringes off, 0.8 is still clean but reads as a smear.

The `hash` jitter offsets each pixel's 32 taps by a random fraction, so long streaks come out as fine grain instead of 32 stepped copies. Keep it. The loop must stay in the static form `for (int i = 0; i < N; i++)` with N ≤ 128.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float amount;
uniform float2 center;
uniform float fringe;
uniform float clear;

float hash(float2 p) {
  float3 p3 = fract(float3(p.x, p.y, p.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

half4 main(float2 p) {
  float2 c = center * resolution;
  float2 d = p - c;
  float r = length(d) / resolution.y;
  float w = smoothstep(clear, clear + 0.45, r);
  float a = amount * w;
  float j = hash(p);
  float3 acc = float3(0.0);
  for (int i = 0; i < 32; i++) {
    float t = (float(i) + j) / 32.0;
    float k = a * t;
    acc.r += image.eval(c + d * (1.0 - k * (1.0 + fringe))).r;
    acc.g += image.eval(c + d * (1.0 - k)).g;
    acc.b += image.eval(c + d * (1.0 - k * (1.0 - fringe))).b;
  }
  return half4(half3(acc / 32.0), 1.0);
}
```
