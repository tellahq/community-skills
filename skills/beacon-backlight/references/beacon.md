# Beacon shader (SkSL)

Paste everything inside the fence, unchanged, as the `source` of `addEffect {kind: "shader"}` on the full-frame `bg` fill. It loops seamlessly every `loopSeconds`; `resolution` is bound to the shape for you.

```glsl
// Beacon: volumetric light. Shafts of a brand colour fan out from a hot core,
// shimmering as they turn, through a faint haze, graded over a dark field with
// film grain and a soft vignette.
// Written for the liquid-backgrounds skill. Seamless every loopSeconds.
uniform shader image;
uniform float2 resolution;
uniform float time;
uniform float loopSeconds;
uniform half4 ground;       // the dark field
uniform half4 ray;          // the light: the brand colour
uniform half4 core;         // the hottest light, near white with a hint of the brand
uniform float2 origin;      // where the core sits, 0-1 of the frame (it can sit off frame, e.g. 0.5, -0.1)
uniform float spread;       // how many shafts: 1.5 a few broad beams, 4 many fine ones
uniform float reach;        // how far the shafts carry: 0.6 short, 1.6 across the frame
uniform float haze;         // 0-1: dust and smoke breaking up the shafts
uniform float drift;        // how far it moves per loop: 0.5 calm, 1 default, 2 lively (the loop stays seamless)
uniform float4 scrim;       // a soft ellipse for the type: centre x, y and radius x, y (0-1 of the frame)
uniform half4 scrimColor;   // the scrim's colour; its alpha is the strength
uniform float grain;        // film grain, 0.03-0.08

float hash21(float2 c) {
  float3 p3 = fract(float3(c.x, c.y, c.x) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

float gnoise(float2 p) {
  float2 i = floor(p);
  float2 f = fract(p);
  float2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
  float a0 = 6.2831853 * hash21(i);
  float a1 = 6.2831853 * hash21(i + float2(1.0, 0.0));
  float a2 = 6.2831853 * hash21(i + float2(0.0, 1.0));
  float a3 = 6.2831853 * hash21(i + float2(1.0, 1.0));
  float va = dot(float2(cos(a0), sin(a0)), f);
  float vb = dot(float2(cos(a1), sin(a1)), f - float2(1.0, 0.0));
  float vc = dot(float2(cos(a2), sin(a2)), f - float2(0.0, 1.0));
  float vd = dot(float2(cos(a3), sin(a3)), f - float2(1.0, 1.0));
  return 0.5 + 0.75 * mix(mix(va, vb, u.x), mix(vc, vd, u.x), u.y);
}

float fbm(float2 p) {
  float v = 0.0;
  float a = 0.55;
  for (int i = 0; i < 3; i++) {
    v += a * gnoise(p);
    p = float2(1.6 * p.x - 1.2 * p.y, 1.2 * p.x + 1.6 * p.y) + float2(2.3, 7.1);
    a *= 0.45;
  }
  return v;
}

half4 main(float2 p) {
  float2 res = resolution;
  half alpha = image.eval(p).a;
  float ph = 6.2831853 * time / loopSeconds;
  float2 q = (p - origin * res) / res.y;
  float r = length(q);
  float2 dir = q / max(r, 0.0001);

  // shafts: noise read around a circle of directions (no seam at any angle),
  // drifting around a circle in noise space once per loop
  float2 o = 0.22 * drift * float2(cos(ph), sin(ph));
  float broad = fbm(dir * spread + o);
  float fine = gnoise(dir * spread * 3.1 + float2(3.3, 1.1) - 1.3 * float2(o.y, o.x));
  float shafts = pow(clamp(broad * 1.1 + 0.4 * fine - 0.45, 0.0, 1.0), 1.6);
  shafts *= smoothstep(0.0, 0.09, r);  // the shafts melt into the core instead of meeting in a point
  float fall = exp(-r / (0.42 * reach));
  float glow = 1.3 * exp(-r * r / 0.006) + 0.5 * exp(-r / 0.11);
  float hz = fbm(q * 2.2 + 0.15 * drift * float2(sin(ph), cos(ph)) + float2(7.0, 3.0));
  float I = shafts * fall * 2.2 * mix(1.0, 0.35 + 1.3 * hz, haze) + glow;
  I += 0.06 * haze * hz * exp(-r / (0.8 * reach));

  float3 col = float3(ground.rgb);
  col = mix(col, float3(ray.rgb), clamp(I, 0.0, 1.0));
  col = mix(col, float3(core.rgb), smoothstep(0.85, 2.2, I));
  float2 v = p / res - 0.5;
  col *= 1.0 - 0.55 * dot(v, v);

  float2 uv = p / res;
  float2 sd = (uv - scrim.xy) / max(scrim.zw, float2(0.001));
  float m = 1.0 - smoothstep(0.0, 1.0, length(sd));
  col = mix(col, float3(scrimColor.rgb), float(scrimColor.a) * m);
  float g = hash21(p + floor(time * 24.0) * float2(7.0, 13.0)) - 0.5;
  col += g * grain * (0.6 + 0.8 * clamp(I, 0.0, 1.0));

  return half4(half3(col) * alpha, alpha);
}
```
