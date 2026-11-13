---
name: glitch-title-reveal
description: >-
  Crash a title onto the footage through digital damage, in Tella Motion: a
  short white title on a black box stutters in through slice offsets, RGB
  split and pixelated blocks, settles clean in the lower left, crashes once
  while it holds, then glitches out. A transparent overlay, so the footage
  plays on underneath, finished with a light film look (scanlines, vignette
  and a colour fringe). Timed to the word that names the topic. Use when
  asked for a glitch title, glitch text reveal, glitchy chapter or topic
  title, RGB split text, a datamosh or broken-signal title, a techy or VHS
  style title over footage, or a lower-left title box that glitches in.
metadata:
  title: Glitch title reveal
  author: Tella
  category: Titles & text
  image: og.jpg
  poster: gallery/slab-title-over-footage.webp
  preview: gallery/slab-title-over-footage.mp4
  prompt: When I start talking about the paper trail, glitch a chapter title onto the footage in a black box, lower left.
---

# Glitch title reveal

A chapter or topic title that crashes onto the footage. A white title on a near-black box arrives broken (torn into slices, split into red, green and blue, chunks pixelated, flickering), resolves in under 0.75 s, holds clean in the lower left, glitches once mid-hold and glitches out. It is a full-frame transparent overlay over the user's own footage; the footage gets a light film look (scanlines, vignette, a colour fringe) so the damage feels part of the picture. Builds on `tella-title-cards` (titles and their placement) and `tella-motion-design` (timing, overlays, checks); load them first. For a glitch on a cut between shots, use a transition skill instead.

## Ask once

Work out yourself, never ask: the title and the word it lands on (from the transcript: the chapter or topic the speaker names), where the footage is busy (keep the box off faces), and the brand colour (from the workspace or the message). Then ask one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Default / prefill | Limits |
|---|---|---|---|---|
| **Title** | text | yes | the topic, 2–4 words, uppercase (e.g. `THE PAPER TRAIL`) | up to 22 characters; one line |
| **Lands on** | text | yes | the transcript word that names the topic, with its time (e.g. `"paper" at 0:42.1`) | one word from the transcript |
| **On screen for** | slider, s | yes | 4.6 | 3–8 (no mid-hold crash under 3.8; capped at what is left of the clip) |
| **Position** | pick | yes | Lower left | Lower left, Lower right, Centre |
| **Glitch strength** | slider, % | yes | 55 | 20–100 |
| **Colours** | pick | yes | White on black | White on black, Black on white, Brand box (brand colour box, white or black text, whichever contrasts) |
| **Film look on the footage** | switch | no | on | scanlines + vignette (+ fringe) over the clip |

No media is needed: the title goes over the video's own footage. If the user wants it over other footage, look for it in the message's attachments, then the media library; else ask with `ask_question` ("Which clip should the title sit over?") and fall back to the video's own footage. A title longer than 22 characters: shorten it to the speaker's key words, never wrap it to two lines. If the user skips the form, build with the prefilled values.

## Timing

- The overlay starts 0.1 s before the word it lands on; the entrance glitch lasts 0.73 s, so the box is clean by the end of the word. Never land it over a second name or a number.
- Every time below is a formula of the length L (the **On screen for** slider), in seconds from the overlay's start; the example is L = 4.6:
  - Entrance: 0 to 0.733 (fixed).
  - Crash: starts C = L/2 − 0.167, ends C + 0.4 (example 2.133–2.533). Only when L ≥ 3.8; below that drop the crash, or it would sit within 1 s of the entrance and the exit.
  - Exit: starts E = L − 0.667, title gone at E + 0.267 = L − 0.4, envelope 0 at E + 0.4 = L − 0.267 (example 3.933, 4.2, 4.333).
  - Canvas duration L; overlay `durationMs` L × 1000.
- Worked: L = 3: entrance to 0.733, no crash, exit 2.333, gone 2.6, clean 2.733. L = 8: crash 3.833–4.233, exit 7.333, gone 7.6, clean 7.733. Only L = 4.6 has been built; other lengths are untested.
- The overlay belongs to one clip and can't span a cut between clips: if the clip ends before landing time + L, shorten L to fit (not below 3 s), or land it earlier.
- Every key is a hold key on a 1/15 s step, and `seed` steps 15 times a second. Smooth easing turns the damage into a blur.
- No two crashes within 1 s and no white flash frames, for viewers sensitive to flashing.

## The look (values from the example, 1920 × 1080)

- **Box** (`slab`): rect `#0E0E0F`, square corners, x 120, y 730, 933 × 170 for `THE PAPER TRAIL`. Width = the title's width + 43 px each side.
- **Title** (`title`): Inter 800, 104 px, line height 1, letter spacing −4.16 (−0.04 em), `#FFFFFF`, left-aligned at x 163, y 770 (43 px in, 40 px down from the box's corner).
- **Positions**: lower left as above; lower right, box's right edge at x 1800, same y; centre, box centred horizontally with its top at y 455.
- **Colour pairs**: white on black `#FFFFFF` on `#0E0E0F`; black on white `#0E0E0F` on `#F3F1EC`; brand, the brand colour on the box.
- **Glitch** (`references/type-glitch.sksl`) on the `card` group: `rgb 8`, `slice 40`, `mosaic 0.3`, `seed` = floor(composition seconds × 15) + 37. The `amt` envelope below is at full strength; multiply every value by the strength (0.55 in the example). Values every 1/15 s from each part's start:
  - Entrance at 0 s: 1, 0.85, 1, 0.9, 0.7, 1, 0.8, 0.55, 0.35, 0.18, 0.08, 0.
  - Crash at C (L ≥ 3.8 only): 0.35, 1, 1, 0.75, 0.4, 0.15, 0.
  - Exit at E: 0.3, 0.8, 1, 1, 0.6, 0.25, 0.
- **Flicker**: `card` opacity hold keys 1 at 0, 0.35 at 0.067, 1 at 0.133, 0.5 at 0.267, 1 at 0.333 (entrance, fixed), 0 at E + 0.267 = L − 0.4 (4.2 in the example).
- **Fringe on the type**: an adjustment group `aberration` above `card` with `fx.chromaticAberration` amount 4, unkeyed, 0 to L. The clean type keeps a faint red/blue edge, which is the look.
- **Film look** (one more overlay, from the clip's start for the clip's whole length, independent of L, above the title): a transparent full-frame rect with `references/alpha-vignette.sksl` (amount 0.5, size 0.42, softness 0.5), and a black full-frame rect at opacity 0.22 with `fx.venetianBlinds` (completion 0.5, angle 0, width 4, feather 0) for scanlines.
- **Footage fringe** (example only, see gotchas): the clip's footage re-placed in a full-frame overlay under the title, scale 1.015 about the centre, `fx.chromaticAberration` amount 6.

## Building it

1. `create_motion_document` with the video's id, name `Chapter title: <title> (block glitch)`, then `canvas.set` duration to L. Add `slab` (`addShape` rect) and `title` (`addTitle`), `group` them as `card`.
2. `addEffect` kind `shader` on `card` with the full text of `references/type-glitch.sksl` as `source`, unchanged (no backdrop). Set `rgb`, `slice`, `mosaic`; `bindProperty` `seed` to the expression; write the `amt` keys with `setKeyframes` by the `field:` path `inspect_motion_node_properties` lists, easing `hold`.
3. Key `card` opacity as above. Add the `aberration` adjustment group (`addAdjustment`, then `addEffect` `fx.chromaticAberration`).
4. `get_motion_frame` at 0.033, 1.0 and 2.2 s (`startTimeMs`) to check the box, then `add_overlay` with `motionDocumentId`, at the landing time, 1920 × 1080 at 0, 0.
5. Film look on: a second document `Look: scanlines + vignette`, the clip's length, the two rects above; `add_overlay` it above the title (higher zIndex), from the clip's start.

## Checking it

`get_filmstrip` on the video at every 1/15 s through the entrance, crash and exit, plus 0.1 s either side: the first frame is already broken (no clean frame before the glitch), the last step leaves the box exactly in place, nothing tears outside the box, and no frame is blank or flashes. Then one `get_video_frame` at 1920 on a clean hold: the title's right edge sits 43 px inside the box, the box is clear of faces, and the scanlines don't make the title shimmer. Report the time, the word it lands on, and the title.

## Gotchas

- **The shader goes on the group, never a backdrop.** A backdrop shader in an overlay sees the video beneath it and tears the whole frame.
- A shader on a group gets `resolution` = the whole canvas and canvas-pixel coordinates; slices still only move what the group drew, so tears stay inside the box's rows.
- Inter 800 at 104 px is wide: size the box from a rendered frame, not by eye, and check the right edge at full size.
- `bindProperty` on a wrong path says "numeric properties only", which really means the path doesn't exist. The `amt` storage index changes after `removeEffect`/`addEffect`: read the path again.
- The footage fringe re-plays the clip's footage inside an overlay. It only stays in sync on an uncut clip with the overlay starting at the clip's start; on a cut or talking-head clip skip it (the film look and the type's fringe are enough).
- The scanline rect is opaque black with a venetian-blinds mask; at opacity above 0.3 it dims the footage noticeably.

## Variations

- Calmer: strength 30%, `mosaic` 0, drop the mid-hold crash.
- A second line (untested): a kicker above the title in Inter 600, 28 px, tracked 0.18, uppercase, inside the box, box 50 px taller.
- No film look: switch it off for clean, modern footage; the type's own fringe still carries the glitch.
