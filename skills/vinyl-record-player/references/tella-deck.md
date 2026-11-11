# Tella's deck: layers and keys

The default deck is eight PNG cut-outs in `assets/` (all but `deck.png` have alpha). Every value below is on a 1920×1080 canvas, as Grant's example has it. Paint order is top to bottom of this table, with a black full-frame shape under everything and the spotlight over everything. D is the needle drop (3.6 s in the example); times are on the document clock.

| Node | File (px) | Destination x, y, w × h | Anchor |
|---|---|---|---|
| `deck` (deck, platter, record, static) | `deck.png` 1920×1080 | 0, 0, 1920 × 1080 | none |
| `rimBlur` (platter rim, spinning blur) | `rim-blur.png` 1108² | 458.12, 38.33, 1003 × 1003 | 959.62, 539.83 |
| `rimDots` (platter rim, strobe dots) | `rim-dots.png` 1108² | 458.12, 38.33, 1003 × 1003 | 959.62, 539.83 |
| `label` (centre label) | `label.png` 994² | 510.64, 86.59, 899.80 × 899.80 | 960.54, 536.49 |
| `spindle` | `spindle.png` 68² | 929.75, 504.53, 61.56 × 61.56 | none |
| `armShadowLift` | `arm-shadow-lifted.png` 338×1656 | 1476.22, −532.03, 311.00 × 1523.71 | 1631.72, 229.82 |
| `armShadowRest` | `arm-shadow-resting.png` 338×1656 | 1476.22, −532.03, 311.00 × 1523.71 | 1631.72, 229.82 |
| `arm` (tonearm) | `arm.png` 548×3184 | 1505.66, −502.59, 252.11 × 1464.82 | 1631.72, 229.82 |

The arm's top edge is above the frame on purpose: the pivot (the anchor) is at (1632, 230), and the counterweight runs off the top.

## Keys

| Node | Property | Keys (time: value, easing into the next) |
|---|---|---|
| `arm`, both shadows | rotation | 0: −22 hold; D−3.1: −22 easeInOutCubic; D−0.7: 22, hold to D+1.2; then every 0.9 s 22.08, 22.02, 22.10, 22.03, 22.11 easeInOutSine |
| `arm` | scale | D−0.6: 1.006 easeInOutSine; D: 1 |
| both shadows | x, y (offsets) | D−0.6: 5, 7 easeInOutSine; D: 2, 3 |
| `armShadowLift` | opacity | D−0.6: 0.42 easeInOutSine; D: 0 |
| `armShadowRest` | opacity | D−0.6: 0 easeInOutSine; D: 0.5 |
| `label` | rotation | D+0.3: 0 cubic-bezier (0.333, 0, 0.667, 0.333); D+1.0: 70 linear; end: 70 + 200 °/s × (end − D − 1.0) (270 °/s for 45 rpm) |
| `rimDots` | start / duration | starts D+0.3, lasts 1.2 s |
| `rimDots` | rotation | D+0.3: 0 same bezier; D+1.0: 70 linear; D+1.5: 170 |
| `rimDots` | opacity | D+0.85: 1 easeInOutSine; D+1.35: 0 |
| `rimBlur` | opacity | 0: 0; D+0.55: 0 easeInOutSine; D+1.2: 1 (never rotates: the blur ring already looks spinning) |

Motion blur (shutter 180°) on `arm`, `label` and `rimDots`.

Spotlight: a full-frame `#00000000` shape on top with `addEffect` `fx.vignette`, `backdrop: true`, amount 1, size 0.19, softness 0.475 (colour black by default). Grant's document puts the same effect on an adjustment group; the result is the same.

## Commands that worked

1. `create_source` `kind: 'image'` with each file's width and height, PUT the bytes (`Content-Type: image/png`) to `uploadUrl`.
2. One batch: `canvas.set` duration, `addShape` `bg` fill `#000000`, then `addMedia` each `sourceId` in the order above with `start` 0 and `duration` = canvas length (`rimDots`: start D+0.3, duration 1.2).
3. A second batch: `node.patch` each node's `destination` (`addMedia` lands with `fit: contain` across the frame), `setProperty` `anchorX`/`anchorY`, `setKeyframes` as above, `setMotionBlur`, then the spotlight shape and its effect.
