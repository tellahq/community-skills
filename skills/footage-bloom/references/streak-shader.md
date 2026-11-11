# Bloom: the streak shader

SkSL runtime shader for the `streaks` node, used in the example video at 1920×1080. It is not a backdrop: it runs on a screened copy of the footage after `erode` (radiusX 0, radiusY 12), `fx.levels` (inputBlack 0.78) and `blur` (radiusX 30, radiusY 1), in that order, and outputs only the tinted streaks. Pass it as one string to `addEffect` with `kind: "shader"` and give every uniform a value. Tella supplies `image` and `resolution`.

| uniform | value | use |
|---|---|---|
| amount | key 0 → 1.8 | streak brightness, **the one to key** |
| threshold | 0 | leave at 0: `fx.levels` before it does the cut |
| reach | 800 px | half-length of a streak (500–1100 works; scale with height / 1080) |
| tint | `0.4, 0.65, 1, 1` | Blue; Warm `1, 0.62, 0.3, 1`; White `1, 1, 1, 1` |

```glsl
uniform shader image;
uniform float2 resolution;
uniform float amount;
uniform float threshold;
uniform float reach;
uniform half4 tint;

half4 main(float2 p) {
  float3 acc = float3(0.0);
  for (int i = 0; i < 121; i++) {
    float t = (float(i) - 60.0) / 60.0;
    float o = t * reach;
    float3 c = image.eval(p + float2(o, 0.0)).rgb;
    float l = max(max(c.r, c.g), c.b);
    float b = smoothstep(threshold, 1.0, l);
    acc += c * b * (exp(-abs(t) * 3.5) + 1.5 * exp(-abs(t) * 18.0));
  }
  float s = dot(acc, float3(0.3333)) / 3.0;
  float3 col = float3(tint.rgb) * s * amount;
  return half4(half3(col), 1.0);
}
```

