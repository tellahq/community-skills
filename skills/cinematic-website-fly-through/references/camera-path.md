# Camera path and card keys from the example (12 s)

All times are seconds on the document clock. The example has no music; its cuts sit at 2.23, 5.5 and 9.2 s. With music, move each cut time (C) onto a beat and shift that shot's keys with it.

## The camera

The same keys go on two sibling groups inside `drift`: `stage` (the backdrop plane and the page's shadow, plus `translateZ` −160) and `page` (the screenshot and its sheen). Both have `perspective` 1700. `anchorX`/`anchorY` is the page point the camera looks at (page pixels, 1920 wide, top-left 0, 0); `x`/`y` place that point on screen (`x` = 960 − anchorX and `y` = 540 − anchorY centre it; the example pushes it off-centre on purpose during the whips). `scale` is keyed on both axes.

| t | anchorX | anchorY | x | y | scale | rotateX | rotation | rotateY | Easing into the next key |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 760 | 330 | 200 | 210 | 0.95 | 38 | −9 | 0 | drift `{0.22, 0, 0, 1}` |
| 1.68 | 760 | 300 | 200 | 240 | 1.35 | 22 | −4 | 0 | whip `{0.6, 0, 0.9, 0.5}` |
| 2.23 | 760 | 300 | 200 | −200 | 1.9 | 6 | −3 | 0 | hold (card 1) |
| 3.05 | 960 | 700 | 360 | −160 | 1.15 | 18 | −6 | −10 | glide `{0.05, 0.535, 0, 1}` |
| 4.95 | 960 | 1500 | 0 | −960 | 1.25 | 16 | 3 | 10 | whip |
| 5.5 | 960 | 1500 | −60 | −1460 | 1.3 | 15 | 4 | 13 | linear |
| 5.65 | 960 | 1500 | −100 | −1660 | 1.368 | 13.6 | 5.4 | 17.1 | hold (card 2) |
| 6.32 | 760 | 1450 | 200 | −910 | 1.25 | 62 | −2 | 0 | skim `{0.05, 0.59, 0.5, 0.8}` |
| 8.85 | 900 | 2420 | 60 | −1880 | 1.3 | 40 | −1 | 0 | blast `{0.5, 0.12, 0.9, 0.5}` |
| 9.2 | 900 | 2420 | 60 | −1880 | 0.4 | 48 | −1 | 0 | hold (card 3) |
| 10.2 | 960 | 2350 | 0 | −1810 | 0.88 | 22 | −7 | 0 | drift |
| 12 | 960 | 2380 | 0 | −1840 | 0.8 | 18 | −5 | 0 | hold |

In the glide row `x` uses `{0.03, 0.71, 0, 1}` and `y` uses `{0.22, 0, 0, 1}`. The whip rows speed up into the cut: the camera dives (scale up, rotateX down) as the card fades in over it. The blast row pulls the camera back hard (scale 1.3 → 0.4) under the zoom blur.

Speed blur on `stage` and `page` (a `blur` effect, radiusX 0, decal): `radiusY` 0 at 1.73 (`easeInCubic`) → 28 at 2.23 (`hold`) → 0 at 3.05; the same at 5.0 → 5.5 → 6.32. Not on the third cut.

Under all of it, `drift` (origin 960, 540) moves linearly over the whole clip: scale 1 → 1.15, `x` 70 → −70, `y` 35 → −35, rotation −1.8 → 1.8.

Fit to your page: aim anchorY at a section you want seen (the hero at 300, the middle of the page for the glide, a strong heading near the bottom for the skim), and keep the glide to about 400 page pixels per second.

## The cards

Each card is a white full-frame rect (`cardN.bg`) and a group holding the word, with a screen-blended sheen rect above it. The group's origin is the canvas centre, `perspective` 1400. Every word has motion blur (shutter 0.0167 s, 16 samples).

**Card 1, rise and swing off (C = 2.23).** bg 2.07–3.45: opacity 0 → 1 over 0.16 s (`easeInOutSine`), hold, 1 → 0 from 3.05 to 3.33. The word's `y` 1125 at 2.07 → 405 at 2.23 (linear) → 0 at 2.68 `{0.1, 0.5, 0.4, 1}`. The group: rotateX 16 → 12 → 0, rotation −4 → −3 → 0, scale 0.8 → 0.9 → 1 on the same three times; opacity like the bg. Exit from 2.73, curve `{0.5, 0, 0.86, 0.5}`: at 3.05 rotateY 36, `x` −620, `y` −110, rotation −4, rotateX 9, scale 1.02; then linear to 3.45: rotateY 68, `x` −2500, `y` −460, rotation −9, rotateX 19.

**Card 2, rise and drop away (C = 5.5).** bg 5.38–6.5. The word: `y` 855 → 405 → 0 at 5.4, 5.5, 5.95 with `x` 100 → 50 → 0; then `y` 0 at 6.0 → −60 at 6.32 → −120 at 6.5. The group: rotateY 13 → 10 → 0 and rotateX 32 → 26 → 0 (5.4, 5.5, 5.95); exit scale 1 at 6.0 → 0.72 at 6.32 → 0.48 at 6.5 and rotateX 0 → 10 → 16; opacity in 5.38–5.54, out 6.32–6.5.

**Card 3, blast in (C = 9.2).** bg 9.04–10.2. The group's scale 6 at 9.04 → 3.5 at 9.2 → 1 at 9.65 (settle), rotateX 10 → 8 → 0, opacity in 9.04–9.2. Exit from 9.88: at 10.2 rotateY 10, `x` −290, scale 0.97; at 10.36 rotateY 15, `x` −1010, opacity 0.

**End card (from 10.2).** Opaque white bg to the end. The name's first part slides in: `x` 360 → 0 over 0.4 s `{0.1, 0.5, 0.4, 1}`, opacity 0.25 → 1 in 0.1 s, then drifts `x` 0 → −60 from 0.47 to 0.97 s. The second part (".com") starts 0.3 s later: `x` 300 → 0 in 0.17 s, then 0 → −56 by 0.57 s, opacity 0.25 → 1 in 0.17 s. The group drifts for the rest of the clip: rotateY −12 → 6, rotateX 3 → −1.5, `x` 30 → −15, first key `{0.1, 0.5, 0.3, 1}`, opacity in over 0.16 s.

**Sheen.** A 1920×1080 rect, blend `screen`, a linear gradient from (0, 0) to (1920, 1200), white with alpha 0 → 0 at 0.38 → 0.1 at 0.47 → 0.22 at 0.5 → 0.08 at 0.55 → 0 at 0.66. Key the gradient's `translateX` −700 → −44 across the card's hold, opacity as the card's bg. The page's own sheen is the same band on a 1920×4400 rect (gradient end 2400, 1500), `translateX` −1600 → 1600 over the whole clip.
