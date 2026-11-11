---
name: beacon-backlight
description: >-
  Make a keynote-style title card in Tella Motion where a single warm light
  burns in the dark, flares into slow rotating light rays with haze and film
  grain, and lights a title beneath it, with a small label above the title and a
  detail line below. The title blurs into focus and glows from behind as the
  light breathes, and the whole card dims back to a point at the end. The
  background is one looping SkSL shader, so it also works held steady as a
  living background. Use when asked for a keynote opener, an event or
  conference title, a chapter card or reveal on light rays, god rays, a glowing
  core, a beacon, a spotlight or sunburst title, or a dramatic dark opener.
metadata:
  title: Beacon backlight
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/beacon-keynote-opener.webp
  preview: gallery/beacon-keynote-opener.mp4
  tags: light rays, god rays, keynote, opener, title card, shader, glow, event, chapter card, loop, background
  prompt: Open the video with an 8-second keynote card for "Northwind Live", with KEYNOTE above it and "12 March · Online" below, in our blue.
---

# Beacon backlight

One look: a hot core near the top of a near-black frame switches on, its light rays reach out and turn slowly, and a centred title below it comes into focus with a glow that swells and fades with the light. A small mono label sits above the title, a detail line below. It is its own clip (an opener or a chapter card) or b-roll that hard-cuts in over the speech; held steady, it is a living background. Builds on `tella-motion-design` (load it first) and `tella-title-cards` when it opens a set of matching titles.

## Ask once

Work these out yourself and never ask: the title from the video's name, the chapter or the opening line of the transcript; a label and detail line only when the user or the speaker gave them (never invent a date, a place or "keynote"); the brand colour from the video's presets or the message; where it goes (the start of the video, or the topic change the user named).

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Prefill | Limits |
|---|---|---|---|---|
| Title | text | yes | video name or chapter title | up to ~24 characters on one line; 25–40 goes on two lines at 104 px |
| Small label above | text | no | e.g. `KEYNOTE`, `CHAPTER 2`, or empty | up to 24 characters, set in capitals |
| Detail line below | text | no | a date and place the user gave, else empty | up to 40 characters, set in capitals |
| Light colour | pick | yes | Amber | Amber, White, Blue, Magenta, Brand (prefill Brand when the video has a brand colour) |
| Length | slider, s | yes | 8 | 5–15 s |
| Use | pick | yes | Opener | Opener (flares up, dims out), Steady background (rays at full from frame 0, no dim) |
| Where | pick | yes | Own clip at the start | Own clip at the start, Own clip at a chapter, B-roll over the speech |

No media is needed: everything is the shader and live type. If the user submits the form unchanged, build with the prefilled values. An empty label or detail line removes that line; the rest stays where it is.

## Timing

- Own clip: the length from the form. Never cut into a sentence; a chapter card goes at the topic change.
- B-roll: start 0.3 s before the first word it introduces, so the title (in from 1.15 s) lands near the name being said. End it before the next thought. A b-roll layout belongs to one clip: keep the card inside the clip where its words are said, and if that clip ends sooner, shorten the card (move the exit earlier) or start it earlier so it ends by the clip's end. `add_layout` takes a `clipId`, and its `startTimeMs`/`durationMs` are on that clip's playback timeline (cuts applied). Only when the spoken range truly runs across a cut, split it there (untested): one document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document starting at the frame the first ended on, keys on each clip's own clock. Then `list_layouts` and make sure the layout after each b-roll is a hardCut too (it can come back with a spring).
- For other lengths keep the entrance times below as they are and move the exit: everything that starts at 6.4 s starts at `length − 1.6 s`. Set `loopSeconds` to the length.

## The look

1920×1080. For 9:16 (untested): 1080×1920, `origin` [0.5, 0.32], `scrim` [0.5, 0.52, 0.46, 0.16], and every text box re-centred on x 540: label box x 90 w 900 at y 860, title in Inter 600 96 px box x 60 w 960 at y 900 (about 16 characters a line, two lines at most), detail box x 90 w 900 at 52 px below the title's last line.

- **Shader** (`references/beacon.md`): `origin` [0.5, 0.3], `spread` 2.5, `haze` 0.5, `drift` 1, `grain` 0.06, `loopSeconds` 8, `scrim` [0.5, 0.7, 0.42, 0.24] with `scrimColor` = `ground` at alpha 0.7.
- **Colours** (`ground` / `ray` / `core`, then label / title / detail):

| Light | ground | ray | core | label | title | detail |
|---|---|---|---|---|---|---|
| Amber (the example) | `#0A0603` | `#FF8A2A` | `#FFF1DC` | `#FFC98F` | `#FFF6EA` | `#E6B98A` |
| White | `#060708` | `#C9D3E2` | `#FFFFFF` | `#DCE3EE` | `#FFFFFF` | `#AEB7C4` |
| Blue | `#02040B` | `#2F7BFF` | `#E8F0FF` | `#A9C6FF` | `#F2F6FF` | `#8FA8D6` |
| Magenta | `#0B0208` | `#FF3DA8` | `#FFE8F5` | `#FFADD9` | `#FFF2F9` | `#D98DB6` |
| Brand | the brand hue at under 6 % lightness | the brand colour, saturated | a near-white tint of it | a 55 % tint | near-white tint | a muted tint |

  Keep `ground` very dark or the rays lose depth. A dark or greyish brand colour makes weak rays: raise its saturation and lightness to about 55 % for `ray`.
- **Type**, all centred: label in Roboto Mono 500, 26 px, letter spacing 7.8 (0.3 em), box x 360 w 1200 at y 600. Title in Inter 600, 128 px, letter spacing −4.48 (−0.035 em), line height 1.1, box x 160 w 1600 at y 640. Detail in Roboto Mono 500, 28 px, spacing 5.6 (0.2 em), box x 360 w 1200 at y 812. Separate parts of the detail with a middle dot and two spaces each side.
- **Backlight on the title**: two `dropShadow`s (not shadow-only) in the light's colours. Wide: `ray` colour, alpha `0.06 + 0.88 × light`, radius `70 + 80 × light`, dy −6, dx `lean`. Rim: the label colour (amber `#FFC27A`), alpha `0.12 + 0.6 × light`, radius `22 + 14 × light`, dy −3, dx `0.4 × lean`.
- **Curves**: `light` 0 at 1.0 s → 1 at 2.7 → 0.12 at 4.0 → 1 at 5.3 → 0.15 at 7.0 → 0.1 at 8.0, all `easeInOutCubic`. `lean` (the glow drifting with the rays) −7 at 1 s → −12 at 2.3 → 0 at 4.4 → +3.3 at 5.8 → −4.9 at 8.0, smooth.

## Motion (8 s opener)

| What | When | How |
|---|---|---|
| Light switches on | 0 → 1.8 s | `reach` 0.15 → 1, bezier (0.3, 0, 0.2, 1) |
| Title | 1.15 → 2.1 s | opacity 0 → 1 by 1.95, y +30 → 0 by 2.0, blur 30 → 0 by 2.1 (`easeOutCubic`) |
| Label | 1.85 → 2.7 s | opacity by 2.4, y +14 → 0 by 2.7 |
| Detail | 2.2 → 3.05 s | opacity by 2.75, y +14 → 0 by 3.05 |
| Hold | → 6.4 s | the rays turn, the glow breathes |
| Type out | 6.4 → 7.4 s | opacity → 0, y → −10, title blur 0 → 26 (`easeInCubic`) |
| Light dims | 6.4 → 8.0 s | `reach` 1 → 0.2 and brightness 1 → 0.35, `easeInOutSine` |

Type eases in on (0.22, 1, 0.36, 1) and out on (0.55, 0, 0.75, 0.2). **Steady background**: `reach` 1 from frame 0, no dim, no type exit; the shader loops so the clip can be any length (keep `loopSeconds` = length or a divisor of it).

## Building it in Tella Motion

1. `create_motion_document` (with `videoId`), `canvas.set` the duration, then `create_clip` with the `documentId` for its own clip, or `add_layout` with `media: {type: "motion", documentId}` for b-roll.
2. `addShape {shape: "fill", nodeId: "bg"}`, then `addEffect {node: "bg", kind: "shader", effectId: "shader", source: <the fence in references/beacon.md>, uniforms}`, declaring every uniform (`time` as `[0]`, colours as 0–1 RGBA). `bindProperty` `field:common/effects/0/effect/uniforms/time/values/0` to `{time: "seconds"}`. Key `reach` with `setKeyframes` on `…/uniforms/reach/values/0`.
3. The end dim is a `colorMatrix` effect on `bg` with its three diagonal entries keyed 1 → 0.35.
4. `addTitle` for `kicker`, `title`, `foot` with the values above. Key opacity and `translateY`. The title's blur: `setCurve` `blur_title`, then `bindProperty` the blur's radiusX and radiusY to it. The glows: `setCurve` `light` and `lean`, then two `dropShadow` effects whose alpha, radius and dx are expressions on those curves.
5. Check the first frame right after adding the shader (see Gotchas).

## Checking it

`get_filmstrip` of the document at 0.3 s (a small core), 1.6 s (rays nearly out, title blurred), 2.7 s (glow at its brightest), 4.0 s (glow low), 6.9 s (type leaving) and the last frame (a dim point). Then a 1 s `get_motion_preview` at 10 fps around 3 s: the rays should turn smoothly, never boil. Read every word against what the user gave, and check the detail line against the busiest rays behind it.

## Gotchas

- `addEffect` accepts SkSL that doesn't compile and reports success, then every frame fails with `thumbnail_fetch_failed`, even after removing the node, because the bad `shader.custom.*` asset stays. Rebuild in a fresh document, or `asset.remove` it.
- `setKeyframes` on a title's `blur` is refused: go through a named curve as above.
- Changing the shader text means `removeEffect`, `addEffect` again, then re-binding `time` and re-keying `reach`.
- Faster or slower rays: change `drift` (0.5 calm, 2 lively), never a `time` term outside the loop phase, or the loop seams.
- A title over ~24 characters crowds the scrim's edges; go to two lines at 104 px and move the detail line down by the second line's height.

## Variations

- Chapter card: label `CHAPTER 03`, no detail line, 6 s.
- Light from above: `origin` [0.5, −0.1] and `reach` 1.4, with the type block moved up by 120 px.
