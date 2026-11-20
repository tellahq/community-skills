# Camera path and card keys (as `scripts/build_flythrough.py` writes them)

Times are seconds on the document clock. `C` is a word's cut (its card fully up); a shot opens at `S` = the previous cut + 0.82 (0 for the first); `D` is the length. The 12 s example: cuts 2.23, 5.5, 9.2.

## The camera

The same keys go on two sibling groups inside `drift`: `stage` (plane and shadow, `translateZ` −160) and `page` (the screenshot or the recording, the sheen, the cursor). Both have `perspective` 1700. The anchor is the point the camera looks at (page pixels on the 1920-wide page); `x`/`y` put that point on screen (960, 540 centres it). Scale is keyed on both axes.

| Shot | t | anchor | screen x, y | scale | rotateX | rotation | rotateY | Easing into the next key |
|---|---|---|---|---|---|---|---|---|
| First (drift, whip in) | S | hero | 960, 540 | 0.95 | 38 | −9 | 0 | drift `{0.22, 0, 0, 1}` |
| | C − 0.55 | target | 960, 540 | 1.35 | 22 | −4 | 0 | whip `{0.6, 0, 0.9, 0.5}` |
| | C | target | 960, 100 (recording: 240) | 1.9 | 6 | −3 | 0 | hold |
| Middle (glide) | S | from | 1320, 540 | 1.15 | 18 | −6 | −10 | glide `{0.05, 0.535, 0, 1}`; x `{0.03, 0.71, 0, 1}`, y drift |
| | C − 0.55 | to | 960, 540 | 1.25 | 16 | 3 | 10 | whip |
| | C | to | 900, 40 | 1.3 | 15 | 4 | 13 | linear |
| | C + 0.15 | to | 860, −160 | 1.368 | 13.6 | 5.4 | 17.1 | hold |
| Last (skim, blast out) | S | from | 960, 540 | 1.25 | 62 | −2 | 0 | skim `{0.05, 0.59, 0.5, 0.8}` |
| | C − 0.35 | to | 960, 540 | 1.3 | 40 | −1 | 0 | blast `{0.5, 0.12, 0.9, 0.5}` |
| | C | to | 960, 540 | 0.4 | 48 | −1 | 0 | hold |
| Under the end card | E | last | 960, 540 | 0.88 | 22 | −7 | 0 | drift |
| | D | last | 960, 540 | 0.8 | 18 | −5 | 0 | hold |

On a page the anchors are `targets`: the hero's y, then `[from, to]` per shot; keep a glide to about 400 page pixels a second. On a recording the screen is one frame high, so the camera aims at the shot's focus (its clicks, the cursor, or `focus`), starts each glide about 320 px left and 120 px above it, and the anchor is kept within ±22 % of the recording box's width and ±20 % of its height around its centre so the screen keeps filling the frame; scales run a little higher (1.2 → 1.35 → 1.47, skim 1.3 → 1.4).

Speed blur on `stage` and `page` (a `blur` effect, radiusX 0, decal): `radiusY` 0 at C − 0.5 (`easeInCubic`) → 28 at C (`hold`) → 0 at C + 0.82, for every cut but the last.

`drift` (origin 960, 540) moves linearly over the whole clip: scale 1 → 1.15, `x` 70 → −70, `y` 35 → −35, rotation −1.8 → 1.8.

## The recording and the cursor

`screen` (clipped to the recording's box, corner radius 28 × scale) holds one media node per shot. The box is the recording scaled by `recording.scale` (default 1.3) about the page's centre, so it extends past the 1920 × 1080 frame on every side and the plane's edge stays out of shot; the shadow and glass sheen use the same box, and the cursor and aim points are mapped into it (the cursor itself keeps its size). A node starts 0.3 s after the previous cut (under the card), ends 0.5 s after its own (or when the take ends, given `durationMs`), plays from `sourceIn` = the shot's source time minus what it plays before it shows, at `playbackRate` = the shot's speed, sound muted.

`cursor` is a group whose `x`/`y` are keyed from the mouse samples (page pixels): `hold` while it rests, `linear` between samples up to 0.16 s apart, `easeInOutCubic` across longer gaps. Each shot's keys start from the last sample before it and stop where the next shot's node starts. Motion blur shutter 1/60 s, 16 samples. Inside it: `cursor.ripple` (a circle 0.95 × the size in radius, scale 0.2 → 1 and opacity 0.55 → 0 over 0.5 s from each click, `easeOutCubic`) and `cursor.body` (the arrow; on `mac` the Golden Gate artwork as four fill paths, `cursor.tail` and `cursor.fill` in black under `cursor.tailedge` and `cursor.edge` in white, with a black 45 % drop shadow 0.065 × size down and 0.13 × size soft; on `windows` an outline path and a fill path with a 35 % shadow; scale 1 → 0.8 in 0.07 s on a click and back by 0.3 s with `easeOutBack`). The arrow's tip is the group's origin.

## The cards

Each card is a full-frame rect (`cardN.bg`) and a group holding the word: flat colour, no sheen (unless the spec sets `cardSheen`). Group origin 960, 540, `perspective` 1400. Words: 250 px (smaller when wider than 1640 px), weight 500, letter-spacing −0.02 em, line height 1.2, motion blur 1/60 s × 16.

**First card, rise and swing off.** bg from C − 0.16 to C + 1.22: opacity 0 → 1 by C (`easeInOutSine`), hold, 1 → 0 from C + 0.82 to C + 1.10. The word's `y` 1125 at C − 0.16 → 405 at C (linear) → 0 at C + 0.45 `{0.1, 0.5, 0.4, 1}`. The group: rotateX 16 → 12 → 0, rotation −4 → −3 → 0, scale 0.8 → 0.9 → 1 on the same times. Exit from C + 0.5, curve `{0.5, 0, 0.86, 0.5}`: at C + 0.82 rotateY 36, `x` −620, `y` −110, rotation −4, rotateX 9, scale 1.02; then linear to C + 1.22: rotateY 68, `x` −2500, `y` −460, rotation −9, rotateX 19.

**Middle cards, rise and drop away.** bg from C − 0.12 to C + 1.0. The word: `y` 855 → 405 → 0 at C − 0.1, C, C + 0.45 with `x` 100 → 50 → 0; then `y` 0 at C + 0.5 → −60 at C + 0.82 → −120 at C + 1.0. The group: rotateY 13 → 10 → 0 and rotateX 32 → 26 → 0; exit scale 1 → 0.72 → 0.48 and rotateX 0 → 10 → 16; opacity out from C + 0.82.

**Last card, blast in.** bg from C − 0.16 (it stays under the end card; with Hold it fades out by E + 0.3). The group's scale 6 at C − 0.16 → 3.5 at C → 1 at C + 0.45, rotateX 10 → 8 → 0. Exit from X = max(C + 0.45, E − 0.32) (C + 0.68 when E = C + 1.0): at E rotateY 10, `x` −290, scale 0.97; at E + 0.16 rotateY 15, `x` −1010, opacity 0. The zoom blur adjustment runs from C − 0.3 to C.

**End card (from E = `endAt`, default last C + 1.0; 0.5–1.3 s after the last cut).** A full-frame rect in the end colour, opacity in over 0.16 s (Hold on the last shot: a 78 % scrim over 0.5 s, the page drifting behind it). The logo is laid out in the exact middle of the frame (a wordmark wider than 2:1 at least 960 px and up to 980 px wide, a symbol at least 378 px tall and about 420 px square; the script notes when that means blowing a small source up past 1.3×) and that is where it comes to rest: `x` 420 → 60 over 0.4 s `{0.1, 0.5, 0.4, 1}`, opacity 0.25 → 1, a short hold, then the little bump left, 60 → 0 from 0.47 to 0.97 s (`easeOutCubic`). Its last key is 0: it never drifts past the middle. With the Name ending the split puts the joined name on the centre; the first part, right-aligned to the split, goes 418 → 58, then to −2, and the second part starts 0.3 s later: `x` 358 → 58 in 0.17 s, then to 2 by 0.57 s. The group's slow turn settles instead of carrying on: rotateY −12 → 0, rotateX 3 → 0, `x` 30 → 0 at the end of the clip `{0.1, 0.5, 0.3, 1}`, so the last frame is flat, square-on and centred.

**Sheen.** Only on the page: a rect over the whole page, blend `screen`, a linear gradient from (0, 0) to (2400, 1500), white with a smooth bell of alpha (`sheenStops` in template.json: 33 stops from 0.27 to 0.73, alpha 0.15 × sin³ so it peaks at 0.15 at 0.5 and eases to 0 with no kinks; a few hard stops band visibly), its `translateX` −1600 → 1600 over the clip, drawn under the cursor. With `cardSheen` the same band crosses each card (1920 × 1080, gradient end 1920, 1200, `translateX` −700 → −44 across the card's hold).
