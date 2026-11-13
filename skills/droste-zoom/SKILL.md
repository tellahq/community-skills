---
name: droste-zoom
description: >-
  Make an endless recursive (Droste) zoom in Tella. A shot holds a smaller copy
  of the next shot, or of itself, inside a picture frame, a photo print, a
  screen or an app window. The camera zooms in without stopping until that
  inner frame fills the screen and becomes the next shot. It works as a
  transition between two clips, as a chain through several shots, or as a
  seamless hypnotic loop of one scene, optionally twisting into a spiral. Built
  as live Tella Motion levels whose scales read one shared depth value, so it
  stays sharp at every depth. Use when asked for a Droste zoom, an infinite or
  recursive zoom, picture-in-picture-in-picture, a zoom-through-the-screen or
  zoom-into-the-photo transition, a "frame within a frame" loop, or an endless
  zoom loop.
metadata:
  title: Droste zoom
  author: Tella
  category: Transitions
  image: og.jpg
  poster: gallery/app-to-chapter.webp
  preview: gallery/app-to-chapter.mp4
  prompt: Add a Droste zoom from the street shot into the lake shot. Drop in an old photo print of the lake, then zoom through it until it becomes the next clip.
---

# Droste zoom

One shot holds a smaller copy of the next shot inside a frame. The camera pushes in at one smooth exponential rate, and the frame grows until it **is** the screen. Then the next shot carries on, and it can hold its own frame, and so on. Every level is a full-canvas shot scaled down into the window of the level above, so the inner shot is the real next shot, never a stand-in.

It is the "zoom through" move from `tella-transitions`, done recursively.

## Three uses

| Use | What it is | Typical length |
|---|---|---|
| **Transition** | Shot A gets a frame holding shot B (a print slides in, or a screen or window is already there). It zooms through, and B continues as the next clip. | 3–3.5 s |
| **Chain** | A → B → C in one continuous push, for example app → recording → chapter card. | 4–5 s |
| **Loop** | One scene contains itself. The zoom never ends and repeats seamlessly every step, optionally turning a few degrees per copy so it spirals. | 2–3 steps of 3–4 s |

## Ask first

Look at a frame of each shot involved, then ask once with `ask_form`, every field prefilled with your pick:
- **Use**: transition (default when the request names two moments), chain or loop.
- **The frame**: a photo print dropping in (good over footage), a picture frame on a wall, a monitor or TV, a browser or app window (good for product videos), or their own idea. The opening must have the video's aspect ratio; a portrait phone in a landscape video doesn't work, so offer a landscape screen.
- **Inner shot**: the next clip (default), an attached image, or a title card (ask for the words). For a loop, the scene itself.
- **Where**: prefill the nearest pause before the new section's first word.
- **Caption on the frame** (optional, e.g. handwriting on the print), in their words only.
- Loop only: **twist** (none, or 6–10° per copy) and **steps** (2–3).

## Geometry

- The window `{x, y, w}` has ratio `r = w / canvasWidth`, and its height must be exactly `r × canvasHeight`. Use r = 0.36–0.5: smaller looks deeper but needs more levels.
- Its fixed point is `c = (x / (1 − r), y / (1 − r))`. Zooming about `c` by `1/r` maps the window exactly onto the canvas. A centred window gives a straight push; an off-centre one drifts toward its side, which also looks good.
- Level `k` has anchor `c` and scale `(1/r)^(depth − k)`. `depth` runs 0 → 1 for a transition, 0 → 2 for a three-shot chain, and `(time mod T) / T` for a loop.
- In a chain, put the window at the same place and size in every shot, so one fixed point serves every step. Otherwise the aim jumps at each hand-off.
- A loop needs levels until the innermost copy is under about 3 px: `1 + log(3/1920) / log(r)`, so 9–10 levels at r = 0.4–0.5.

## Build in Tella Motion

- One group per level, `L0, L1, …`, each a full-canvas shot drawn at full size in canvas pixels, with a per-level id prefix (`L1_bg`, `L1_cap`) so it stays patchable. Its lowest node is a full-canvas background, so it exactly covers the window above. Draw the window in each level as a placeholder rect in the next level's average colour; it only shows on the innermost copy. For a loop, build L0 once and `duplicate` it.
- Paint order: L0 at the bottom, deeper levels above. Grouping can land a later group under an earlier one, so read the document back and fix with `node.move`.
- Set each level's `anchorX/Y` to `c` first (changing anchors later doesn't move a group at scale 1), then bind its `scale` to `pow(1/r, subtract(depth, k))`. For a loop, `depth` is `divide(mod({time: "seconds"}, T), T)`, constant speed with no easing: that is what makes it hypnotic. For a transition or chain, `depth` is a `setCurve "depth"` expression: one `smoothstep` of time per step, from one integer to the next, summed when steps overlap. Create the curve before the bindings that read it.
- Footage levels: `addMedia` with the clip's source, then patch it to `fit: "cover"` (it lands letterboxed with `contain`). When the b-roll replaces the end of clip A, start L0's copy where the b-roll starts (`sourceIn`).
- Rounded windows (app embeds, screens): the next level is square-cornered, so add a corner-cover path per level (four "square minus quarter circle" pieces in the surrounding colour) in a group `F<k>`, bound exactly like level k and painted above every `L` group. Bind its `opacity` to `clamp((k + 1 − depth) / 0.12, 0, 1)` so it fades as its window fills the screen, and the landed shot isn't left with rounded dark corners.
- Twist (loops): put the level's frame artwork in a subgroup anchored at `c`, and bind each level's `rotation` to `twist × (k − depth)`. Make L0's background a rect well past the canvas (about −600, −600, 3120 × 2280) so turned corners never show the void.
- `setMotionBlur` on each level with `shutterAngle: 30, local: true`. At 180° the peak of the zoom smears into mush.

## Looks that worked

**Transition over footage (photo print).** Centred window, r = 0.42. Paper border `#F3EEE3`, 22 px on the sides and top and 78 px at the bottom, radius 4, soft `dropShadow` (dy 20, radius 30). Optional caption in `caveat` 600 at 46 px, `#4A3F33`, centred in the bottom margin. Entry: the print and L1 share the same keys, `y` 780 → 0 and `rotation` 8° → 0 over 0.8 s with `easeOutCubic`, while the outer footage's `brightness` goes 1 → 0.78 so the print pops. Hold 0.2 s, zoom over 1.8 s (step from 1.0 to 2.8 s), land 0.4 s before the end of a 3.2 s document.

**Chain (product).** Window on the right (x 980, y 300, w 760), the same in A (an app window with a recording embed and a `▶ 4:12` pill under it) and B (a dark navy slide with the window as a glowing card). C is a full-bleed chapter card: `inter` 800 at 150 px, kicker 600 at 28 px with letter-spacing 0.24. Steps from 0.6 to 2.2 s and 1.9 to 3.5 s in a 5 s document: the overlap lets the push slow to a breath on B without stopping, then lands on C with 1.5 s to read. Both windows have radius 12, with a white cover on the app and a navy one on the slide. App and person names are invented or the user's own.

**Loop.** One scene (a framed picture on a wall, a screen in a room) copied into every level, period 3–4 s, twist 6–10° for a spiral.

Keep a frame's details (labels, captions, lamps) at least 15 px at level 0. They shrink with every copy, and that is the effect.

## Place it and time it to speech

- **Transition between clips A and B** (length D, usually 3.2 s): add a b-roll on clip A over its last D seconds with `transitionStyle: "hardCut"` and the Tella Motion document as `media`. Inside, L0 plays A's source from that moment and L1 plays B from 0. Then make clip B start D seconds in (cut its first D s, or upload it trimmed), so the hand-off is frame-exact instead of B jumping back to its start.
- Keep the zoom itself in a pause and land on the first word of the new section; the print's entry may start on the last words of the old one. Never hide a sentence under the push.
- **Chain or standalone loop**: a Tella Motion clip, new or appended. A loop also works as b-roll behind a voice-over; its length is steps × period so the end matches the start.
- Uploaded 4:3 footage needs the clip's base layout set to `fullscreen` to fill the frame.

## Check

- One `get_filmstrip` of the document with large tiles. Transition: start, mid-entry, settled, 25 / 50 / 75 % through the zoom, landed. Loop: 0, ¼, ½ and ¾ of a step, plus T − 40 ms against T, which must match apart from a 1 px edge or the loop jumps. A second strip at a 100–200 ms interval shows whether the speed is smooth, with no stall or lurch at a hand-off.
- Look for a window edge that doesn't meet the inner shot, a gap at a turned corner, soft text, and wrong paint order (the frame showing its placeholder instead of the inner shot).
- In the video, `get_filmstrip` around the b-roll's start and end: A identical across the start, B continuous across the cut.
- Report what you placed, where, how long, the inner shot, and the trim on clip B.

## Gotchas

- **Don't zoom a "camera" group that contains the levels.** Grouped content is rasterised at its own size and then scaled, so deeper copies turn soft once zoomed. Bind each level's own scale so every level renders at its final size.
- Zoom in log space (the exponent). Keyframed scale in linear space feels like it accelerates toward a jump; bound expressions are exact, so loops close perfectly.
- Shapes, titles and paths drawn into a group keep canvas coordinates: draw every level at full size and let the scale shrink it.
- `dropShadow` colours read back as `#rrggbb`: the alpha in `#rrggbbaa` is dropped. Control a glow's strength with the shadow-only node's `opacity`.
- Avoid footage with readable brand logos (old films show bottles and signs). Check the inner shot's frames first.
