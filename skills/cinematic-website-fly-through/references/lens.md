# The lens: tilt-shift adjustment and zoom blur

## Depth map (`tsdepth`)

A hidden 1920×1080 rect with a vertical linear gradient from (960, 0) to (960, 1080). White is blurred, black is sharp. Stops (grey value at offset): 1.0 at 0, 0.68 at 0.1, 0.4 at 0.2, 0.17 at 0.3, 0.04 at 0.38, 0 at 0.44, 0 at 0.56, 0.04 at 0.62, 0.17 at 0.7, 0.4 at 0.8, 0.68 at 0.9, 1.0 at 1. That leaves a sharp band across the middle 12 % of the frame that fades to full blur at the top and bottom edges.

## Adjustment group (`tiltshift`, topmost node, whole clip)

`addAdjustment`, then its effects in this order:

1. `glow`: radius 36, threshold 0.8, intensity 0.3, softness 0.3, screen on.
2. `lensBlur`: radius 16, blades 6, roundness 1, aspectRatio 1, highlightThreshold 1, highlightBrightness 0, `blurMap` = the depth map node's id, invertBlurMap false, focalDistance 0.
3. `colorMatrix` that forces alpha to 1: `[1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,0,1]`. Without it the lens blur leaves see-through edges.
4. Fringe (custom shader below), amount 2.
5. `fx.levels`: inputBlack 0, inputWhite 1, gamma 1, outputBlack 0.01, outputWhite 0.99.
6. `fx.vignette`: amount 0.08, size 0.7, softness 0.7, colour black.
7. `fx.addGrain`: intensity 0.025, size 1.4, monochrome 1, seed = floor(time × 24) (an expression: `floor(multiply(time seconds, 24))`).

The cards sit under it too, so their words get the same soft edges and grain.

## Fringe shader

```glsl
uniform shader image;
uniform float2 resolution;
uniform float amount;
half4 main(float2 p){
  float2 c = resolution * 0.5;
  float2 off = (p - c) / c.y * amount;
  float2 lo = float2(0.5);
  float2 hi = resolution - float2(0.5);
  half4 o = image.eval(p);
  o.r = image.eval(clamp(p + off, lo, hi)).r;
  o.b = image.eval(clamp(p - off, lo, hi)).b;
  return o;
}
```

## Zoom blur shader (the blast into the third card)

An empty adjustment group from 0.3 s before the cut to the cut (8.9–9.2 s in the example), opacity 0 → 1 with `{0.6, 0, 0.9, 0.5}`, holding this shader with amount 0.16. 24 samples toward the centre, inside SkSL's 128-iteration limit.

```glsl
uniform shader image;
uniform float2 resolution;
uniform float amount;
half4 main(float2 p){
  float2 c = resolution * 0.5;
  half4 acc = half4(0.0);
  for (int i = 0; i < 24; i++) {
    float t = float(i) / 23.0;
    acc += image.eval(c + (p - c) * (1.0 - amount * t));
  }
  return acc / 24.0;
}
```

A broken shader poisons a document's renders: check each one on a test frame before building on it, and rebuild in a fresh document if frames stop rendering.
