# ASCII waveform shader (SkSL)

The exact shader in the example video. Pass everything between the fences, unchanged, as the shader `source` of `addEffect kind: shader`. It draws its own 5×7 bitmap characters, so no font is needed. 128 lines, well under the per-pixel op limit.

```glsl
// Stream: the sound drawn as real ASCII art, printed outward from the centre
// line of the frame like a log scrolling both ways. Each cell's character is
// picked from a brightness ramp " .:-=+*#%@" by how strong the sound is there:
// the loud core of the band is dense (@ % #), its edges fade through + = - :
// to dots, and silence is blank. Newest sound at the centre, older sound
// scrolls out to the edges. 5x7 bitmap font drawn in the shader (no font needed).
// Written for the sound-visualizer skill.
uniform shader image;
uniform float2 resolution;   // bound to the node's size by the renderer
uniform float time;          // bind to the clock (seconds)
uniform float level;         // 0-1, the sound now (curve lvl)
uniform half4 hA;            // sound history, newest first: h0..h3
uniform half4 hB;            // h4..h7
uniform half4 hC;            // h8..h11
uniform half4 hD;            // h12..h15 (oldest, at the frame's edges)
uniform half4 bg;            // the screen
uniform half4 ink;           // characters in the loud core of the band
uniform half4 dim;           // characters at the band's edges and the faint field
uniform half4 accent;        // the odd highlighted character
uniform float cellW;         // character cell, px at 1080p (24)
uniform float cellH;         // (38)
uniform float speed;         // cells per second the stream moves outward (16)
uniform float histStep;      // seconds between history samples (must match the h curves)
uniform float field;         // 0-1 faint dots across the whole screen (0.08)
uniform float4 quiet;        // a box (x, y, w, h px) where characters thin out behind a title; 0s for none

float hist(float u) {
  u = clamp(u, 0.0, 15.0);
  float4 a = smoothstep(1.6, 0.0, abs(float4(0.0, 1.0, 2.0, 3.0) - u));
  float4 b = smoothstep(1.6, 0.0, abs(float4(4.0, 5.0, 6.0, 7.0) - u));
  float4 c = smoothstep(1.6, 0.0, abs(float4(8.0, 9.0, 10.0, 11.0) - u));
  float4 d = smoothstep(1.6, 0.0, abs(float4(12.0, 13.0, 14.0, 15.0) - u));
  float4 one = float4(1.0);
  return (dot(float4(hA), a) + dot(float4(hB), b) + dot(float4(hC), c) + dot(float4(hD), d))
       / max(1e-4, dot(a, one) + dot(b, one) + dot(c, one) + dot(d, one));
}
float hash(float3 p) { return fract(sin(dot(p, float3(12.9898, 78.233, 37.719))) * 43758.5453); }

// ASCII brightness ramp, darkest first: ' ' . : - = + * # % @
float2 glyphBits(float id) {
  if (id < 0.5) return float2(0.0, 0.0);  // ' '
  if (id < 1.5) return float2(0.0, 396.0);  // '.'
  if (id < 2.5) return float2(12672.0, 12672.0);  // ':'
  if (id < 3.5) return float2(31.0, 0.0);  // '-'
  if (id < 4.5) return float2(992.0, 31744.0);  // '='
  if (id < 5.5) return float2(4255.0, 4224.0);  // '+'
  if (id < 6.5) return float2(4782.0, 21632.0);  // '*'
  if (id < 7.5) return float2(338922.0, 32074.0);  // '#'
  if (id < 8.5) return float2(812100.0, 8803.0);  // '%'
  return float2(476917.0, 23055.0);  // '@'
}

// 1 inside the glyph's lit pixel at gp (column 0-4 from the left, row 0-6 from the top)
float glyphPixel(float id, float2 gp) {
  if (gp.x < 0.0 || gp.x > 4.0 || gp.y < 0.0 || gp.y > 6.0) return 0.0;
  float2 bits = glyphBits(id);
  float rowVal = gp.y < 3.5 ? floor(bits.x / exp2(5.0 * (3.0 - gp.y))) : floor(bits.y / exp2(5.0 * (6.0 - gp.y)));
  rowVal = mod(rowVal, 32.0);
  return mod(floor(rowVal / exp2(4.0 - gp.x)), 2.0);
}

half4 main(float2 p) {
  float2 res = resolution;
  float s = res.y / 1080.0;
  float2 cs = float2(cellW, cellH) * s;
  float cols = floor(res.x / cs.x), rows = floor(res.y / cs.y);
  float2 off = 0.5 * (res - float2(cols, rows) * cs);       // centre the grid
  float2 cell = floor((p - off) / cs);
  float2 local = p - off - cell * cs;

  float dc = cell.x + 0.5 - 0.5 * cols;
  float side = dc < 0.0 ? 1.0 : 0.0;
  float dist = floor(abs(dc));
  float tick = floor(time * speed);
  float sid = dist - tick;                                  // texture travels outward with the sound
  float env = hist(dist / speed / histStep);
  float dy = abs(cell.y + 0.5 - 0.5 * rows) / (0.5 * rows); // 0 at the centre row, 1 at top and bottom

  float3 key = float3(sid, cell.y, side);
  float h2 = hash(key + 17.3);
  float jit = hash(float3(sid, cell.y, side + floor(time * 6.0))) - 0.5;

  // brightness of this cell: strongest on the centre row, falling off to the band's edge
  float e = smoothstep(0.07, 0.68, env);                    // the sound, 0 quiet ... 1 loudest
  // wave shape: the sound's height, pushed to a wider range, then rippled by
  // waves that travel outward and a random height per column (like a spectrum)
  float colR = hash(float3(sid, 101.0, side));              // per column, travels with the stream
  float colR2 = hash(float3(floor(sid / 3.0), 202.0, side));// per group of 3 columns
  float w1 = sin(dist * 0.38 - time * 4.2 + side * 1.9);
  float w2 = sin(dist * 0.13 + time * 1.7 + side * 0.7);
  float shape = 0.62 + 0.30 * w1 + 0.22 * w2 + 0.42 * (colR2 - 0.5) + 0.36 * (colR - 0.5);
  float band = 0.035 + 1.05 * pow(e, 1.35) * clamp(shape, 0.12, 1.4);
  float edge = band * (0.85 + 0.15 * h2);                   // slightly ragged edge
  float t = clamp(1.0 - dy / max(edge, 1e-3), 0.0, 1.0);
  float v = pow(t, 0.7) * (0.22 + 0.85 * e) * (0.94 + 0.12 * level) + 0.07 * jit;
  v = clamp(v, 0.0, 1.0);

  float clear = 1.0;
  if (quiet.z > 0.0) {
    float2 cc = off + (cell + 0.5) * cs;
    float2 qd = max(abs(cc - (quiet.xy + 0.5 * quiet.zw)) - 0.5 * quiet.zw, 0.0) / cs;
    float m = length(qd);
    clear = smoothstep(1.0, 3.5, m);                        // fade the ramp down toward the title
  }
  v *= clear;

  float id = floor(v * 9.99);                               // 0 = blank ... 9 = @
  float on = step(0.5, id);
  float faint = (1.0 - on) * step(hash(key + 9.7), field) * step(0.999, clear);
  float gid = on > 0.5 ? id : 1.0;                          // the faint field is dots

  float gpx = floor(min(cs.x / 6.0, cs.y / 9.0));
  float2 gpos = floor((local - 0.5 * (cs - float2(5.0, 7.0) * gpx)) / gpx);
  float px = glyphPixel(gid, gpos);

  half3 c = mix(dim.rgb, ink.rgb, half(smoothstep(0.35, 0.9, v)));
  c = mix(c, accent.rgb, half(step(0.97, hash(key + 3.3)) * step(0.6, v)));
  float bright = on * (0.55 + 0.45 * v);
  float2 q = (p / res - 0.5);
  half3 col = bg.rgb;
  col += c * half(px * bright);
  col += dim.rgb * half(px * faint * 0.24);
  col += c * half(on * 0.025 * v);                          // a little phosphor bloom in lit cells
  col *= half(0.93 + 0.07 * sin(p.y * 3.14159 / (2.0 * s))); // scanlines
  col *= half(1.0 - 0.6 * dot(q, q));
  return half4(min(col, half3(1.0)), 1.0) * image.eval(p).a;
}

```
