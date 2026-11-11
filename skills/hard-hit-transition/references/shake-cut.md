The shake-cut shader. Pass the text inside the fence, whole and unchanged, as the `source` of `addEffect` (`kind: "shader"`). It is the exact shader in the example video.

```glsl
// Shake cut: shot A hops, pushes in and bends into the cut; shot B lands with
// the move mirrored (opposite bend and roll) and settles with a decaying shake.
// Edges are mirror-tiled, so a shake or push never shows an empty border.
// Put it on a full-frame fill shape above both shots; bind shotA and shotB
// through `inputs`. Key progress 0 -> 1 linearly over the shape's length.
uniform shader image;      // the shape itself (unused)
uniform shader shotA;      // outgoing shot
uniform shader shotB;      // incoming shot
uniform float2 resolution;
uniform float progress;    // 0 -> 1, linear, across the transition
uniform float dur;         // the transition's length in seconds
uniform float cut;         // where the switch sits, 0-1 (0.5 = the middle)
uniform float amp;         // shake in px at 1080p
uniform float hz;          // shake speed, jolts a second (10-16)
uniform float push;        // extra zoom at the cut (0.15-0.4)
uniform float bend;        // sideways bow of the frame at the cut (0-0.35)
uniform float warp;        // lens bulge at the cut (0-0.6)
uniform float roll;        // degrees of roll at the cut
uniform float blur;        // motion blur shutter, 0-1
uniform float split;       // colour fringe at the cut, px at 1080p
uniform float flash;       // exposure kick on the switch frame, 0-0.6
uniform float seed;

float h1(float n) { return fract(sin(n * 12.9898 + seed * 78.233) * 43758.5453); }
float vnoise(float t) {
  float i = floor(t);
  float f = fract(t);
  f = f * f * (3.0 - 2.0 * f);
  return mix(h1(i), h1(i + 1.0), f) * 2.0 - 1.0;
}

float2 mirrorWrap(float2 s) {
  float2 m = mod(s, 2.0 * resolution);
  return resolution - abs(m - resolution);
}

// x: 0 before the switch (shot A), 1 after (shot B); y: the move's envelope
float2 phaseAt(float t) {
  float tc = cut * dur;
  if (t < tc) {
    float a = clamp(t / max(tc, 0.001), 0.0, 1.0);
    return float2(0.0, a * a);               // accelerates into the cut
  }
  float b = clamp((t - tc) / max(dur - tc, 0.001), 0.0, 1.0);
  return float2(1.0, (1.0 - b) * (1.0 - b)); // lands hard, settles
}

// where screen point p samples its shot at time t (seconds)
float2 mapAt(float2 p, float t) {
  float tc = cut * dur;
  float2 ph = phaseAt(t);
  float env = ph.y;
  float sgn = ph.x < 0.5 ? 1.0 : -1.0;       // after the switch the move is mirrored
  float sc = resolution.y / 1080.0;
  float2 c = resolution * 0.5;
  float2 d = (p - c) / resolution.y;
  // lens bulge and a sideways bow, strongest at the cut
  float r2 = dot(d, d);
  d *= 1.0 - warp * env * r2;
  d.x += sgn * bend * env * (d.y * d.y - 0.08);
  // push in and roll
  float z = 1.0 + push * env;
  float ang = radians(roll) * env * sgn * (0.6 + 0.4 * vnoise(t * hz * 0.5 + 9.0));
  float2 rd = float2(d.x * cos(ang) - d.y * sin(ang), d.x * sin(ang) + d.y * cos(ang)) / z;
  // hops: a fast noise shake that grows into the cut and decays after it
  float shakeEnv = ph.x < 0.5 ? (0.25 + 0.75 * env) * smoothstep(0.0, 0.25, t / max(tc, 0.001)) : env;
  float2 off = float2(vnoise(t * hz), vnoise(t * hz + 31.7)) * amp * sc * shakeEnv;
  return c + rd * resolution.y + off;
}

half4 main(float2 p) {
  float t = progress * dur;
  half3 acc = half3(0.0);
  float tc = cut * dur;
  // 8-tap motion blur over the last part of the frame, never across the switch
  for (int i = 0; i < 8; i++) {
    float ti = t - blur * (1.0 / 30.0) * (float(i) / 7.0);
    if (t >= tc && ti < tc) { ti = tc; }
    float2 ph = phaseAt(ti);
    float2 s = mapAt(p, ti);
    float2 fr = (s - resolution * 0.5) / resolution.y;
    float2 ca = fr * split * ph.y * (resolution.y / 1080.0);
    half3 col;
    if (ph.x < 0.5) {
      col = half3(shotA.eval(mirrorWrap(s + ca)).r, shotA.eval(mirrorWrap(s)).g, shotA.eval(mirrorWrap(s - ca)).b);
    } else {
      col = half3(shotB.eval(mirrorWrap(s + ca)).r, shotB.eval(mirrorWrap(s)).g, shotB.eval(mirrorWrap(s - ca)).b);
    }
    acc += col;
  }
  half3 rgb = acc / 8.0;
  float k = (t - tc) * 30.0;               // frames from the switch
  rgb *= half(1.0 + flash * exp(-k * k * 0.5));
  return half4(rgb, 1.0);
}
```
