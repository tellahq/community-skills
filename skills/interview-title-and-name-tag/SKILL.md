---
name: interview-title-and-name-tag
description: >-
  Open a documentary-style interview in Tella with a big two-line title over
  the speaker's footage, then a small name tag. The title is set large in Inter
  Bold at the left (or right) of the frame and drifts gently sideways; its first
  words fade in and the last word types on letter by letter, it holds, then
  each word flashes pink, blue and yellow and blinks out in turn. Then the
  speaker's name and role slide in on one line at the bottom-left over a soft
  black gradient and fade away. One transparent Tella Motion overlay, timed to
  the clip. Use when asked for an interview title, a documentary or mini-doc
  opening, a cold-open title over the speaker, a title then name tag, a
  speaker intro, a lower third with name and role, a "who is this" tag, a
  founder story or customer story opener, or a typed-on title over camera
  footage.
metadata:
  title: Interview title and name tag
  author: Tella
  category: Images
  image: og.jpg
  poster: gallery/back-to-building.webp
  preview: gallery/back-to-building.mp4
  tags: interview, documentary, title, name tag, lower third, typewriter, speaker intro, opening, overlay, kinetic type
  prompt: Open this interview with a big typed-on title, "Made by Hand", then put my name and role in the bottom-left corner.
---

# Interview title and name tag

The opening of a mini documentary: over the first seconds of the speaker's footage (walking in, sitting down, a quiet look before they talk) a two-line title fills the empty side of the frame, the last word typing itself on. It flashes out word by word, and the speaker's name and role settle small in the bottom corner, the way a doc introduces its subject. One transparent, full-frame Tella Motion overlay on the camera clip; nothing is cut or added to the timeline. Builds on `tella-title-cards` (opening title and name tag from one design) and `tella-kinetic-type` (the typed line); follow `tella-motion-design` for timing and checks.

## Ask once

Work these out yourself and never ask: where the speaker's face and body sit (a frame at 0.5 s and one at the name tag's time), when they first speak (`get_transcript` word timings), whether the footage is bright behind the text, the speaker's name if they say it ("I'm Maya…") or the video's title or account name otherwise, and what the video is about.

Then ask once with `ask_form`, every field prefilled so the user can just press submit:

| Field | Required | Prefill | Limits |
|---|---|---|---|
| **Title** | yes | 2–4 words from the video's title or what the speaker is about, e.g. `Made by Hand` | The last word types on alone on line 2; the rest is line 1. Each line at most 12 characters, the last word at most 10. |
| **Name** | yes | From the transcript, else the video's or account's name | Up to 28 characters |
| **Role and company** | no | From the transcript (`Founder, Ortiz Ceramics`); empty leaves the name alone | Up to 32 characters |
| **Title starts at** | yes | 0.1 s into the clip (slider, s) | 0 to 10 s; before the first word, over the walk-in |
| **Name tag at** | yes | 0.1 s after the title has gone (T + 2.6 s + 0.12 s per title word: T + 2.96 s for three words), or the first word of the speaker's first full sentence if that is later (slider, s) | Never before the title has gone |
| **Side** | yes | Away from the face: left (default) or right | Pick of two |

Only the speaker's footage is needed, and it is the clip the overlay goes on. If the video has no camera footage, ask with `ask_question` for "one clip of the person facing the camera, at least 6 s, with room on one side", and offer `generate_video` of a fictional interviewee as the fallback (see Variations). If the user skips the form, build with the prefilled values and report them.

## Timing

T (the "Title starts at" field) and N (the "Name tag at" field) are on the clip's playback timeline, cuts applied, the same clock as the clip's transcript words. The table counts from them; the build converts them to the document's clock.

| When | What |
|---|---|
| T → T+0.6 s | The title group fades in (easeOutCubic) while drifting from 100 px off its resting place toward it (the slide runs to T+2.4 s, easeOutCubic, so it is still easing when the title leaves). |
| T+0.4 s | The last word starts typing, one character every 0.1 s ("Building" is done at T+1.1 s). |
| T+2.5 s | Exit: the first word flips to pink for 0.12 s and vanishes, then the next word blue for 0.12 s, the last word yellow for 0.12 s. Hard cuts, no fades. Gone at T+2.5 + 0.12 × words. |
| Name tag time N | The name slides 60 px into place over 0.5 s (easeOutCubic) and fades in over 0.3 s; the role does the same 0.12 s later. |
| N+2.2 s or the end of the thought | Name and role fade out together over 0.25 s (easeInOutSine). Keep the tag at least 2 s. |

The title belongs over the seconds before the speaker gets going (a walk-in, a settle, the first breath); if they talk straight away, start it at 0.1 s anyway and let the name tag land on their first full sentence. Never stretch the hold past 4 s. A second speaker later in the video gets the name tag alone, from a `duplicate_motion_document` with the title words removed.

## The look

1920 × 1080 canvas, transparent; everything is Inter Bold (700), white `#FFFFFF`, no shadow or outline: the gradient carries the tag and the title is large enough to read on its own.

- **Title**: 174 px, line height 1, letter spacing −0.03 em (−5.22 px). Line 1's box at x 88, y 649; line 2 at x 88, y 820. Each word is its own title node so it can flash on its own; a word after the first sits at the previous word's x plus the width of that word and a space. Tella reports no text bounds, so add up Inter Bold advance widths (with the −0.03 em tracking) in em × 174: space 0.21, `i l j I` 0.24, `f r t` 0.36, `m w` 0.85, `M W` 0.95, other capitals 0.68, other lowercase 0.57. "Back " is 2.50 em (435 px, so "to" sits at x 522), "Made " 2.83 em (492 px). Check a frame and nudge to one normal word space.
- **Exit colours**: pink `#FF8FB5`, blue `#7FC6FF`, yellow `#FFDD66` (the last word is always yellow; with three words on line 1 the middle ones alternate pink and blue).
- **Name tag**: 52 px, line height 1.2, letter spacing −0.02 em (−1.04 px), box at x 96, y 934. The role is on the same line, the same size, weight and white, starting about 94 px (1.8 × the font size) after the end of the name; measure the name with the same em widths × 52 ("Maya Ortiz" is 266 px, so the role sits at x 456).
- **Bottom gradient**: a 1920 × 540 rect at y 540, linear top to bottom, black at alpha 0 (top), 0.07 at 35 %, 0.22 at 70 %, 0.40 at the bottom edge. In the example it covers the whole video; when the overlay starts or ends mid-clip, fade it in over 0.4 s and out with the tag so its edge never pops.
- **Right side** (untested): mirror it. Boxes right-aligned with their right edge at x 1832 (title) and 1824 (tag), the drift and slides come from the left (−100 px, −60 px), and in the tag the role sits right and the name to its left.
- A long title shrinks as one: drop the size until the longer line fits about 1000 px, never under 120 px. Over a bright background (white wall, window) add a black shadow (0 2 24 px, 0.25) to the title words rather than changing the colour.

## Building it

Two clocks. The overlay starts at T on the clip, and the document's clock starts with it: document time = clip time − T. So the title starts at 0, the tag starts at L = N − T, and the document runs D = L + 2.5 s (the tag's 2.2 s hold, its 0.25 s fade and 0.05 s spare). Worked example, T = 5 s and the three-word default N = 7.96 s: L = 2.96, D = 5.46, the name at 2.96, the role at 3.08, the overlay at `startTimeMs` 5000 with `durationMs` 5460. T to T + D must lie inside one clip, since an overlay belongs to one clip: if the clip ends sooner, pull N earlier (never before the title has gone), and on a clip under about 5.5 s drop the title or the tag.

1. `create_motion_document` with the videoId, named "Interview title", 1920 × 1080; `canvas.set` its duration to D. Every time below is on the document's clock.
2. One batch:
   - `addShape` `rect`, box 0, 540, 1920, 540, nodeId `bottom-gradient`, the overlay's full duration; then `node.patch` its `paint` to `{style: "fill", source: {type: "gradient", gradient: {type: "linear", start: {x: 0, y: 540}, end: {x: 0, y: 1080}, tileMode: "clamp", stops: [...]}}}` with the four stops above as `{offset, color: {r: 0, g: 0, b: 0, a}}`, and `setKeyframes` `opacity` 0 (easeOutCubic) at 0, 1 (hold) at 0.4, 1 (easeInOutSine) at D − 0.3, 0 at D − 0.05, so it leaves with the tag.
   - `addTitle` per word: font `inter`, weight 700, fontSize 174, color `#FFFFFF`, align left, letterSpacing −0.03, lineHeight 1, box `{x, y, width: 1400}`. Line-1 words start at 0; the last word starts at 0.4. Each ends where its flash ends (2.62, 2.74, … for the words in order).
   - `setTextAnimation` on the last word: phase `in`, preset `typewriter`, unit `character`, duration 0.03, stagger 0.1.
   - `setKeyframes` `color` on each word: `#FFFFFF` (hold) at its start, its flash colour (hold) at its end − 0.12 s.
   - `group` the words as `title`, then `setKeyframes` on it: `opacity` 0 → 1 from 0 to 0.6 (easeOutCubic) and `x` 100 → 0 from 0 to 2.4 (easeOutCubic); `setMotionBlur` on the group, shutter angle 180.
   - `addTitle` `name` at start L and `role` at L + 0.12, each running to D, fontSize 52, letterSpacing −0.02, lineHeight 1.2, weight 700, box widths 800 / 900. On each, from its own start S (L or L + 0.12): `setKeyframes` `x` 60 (easeOutCubic) at S, 0 at S + 0.5; `opacity` 0 (easeOutCubic) at S, 1 (hold) at S + 0.3, 1 (easeInOutSine) at D − 0.3, 0 at D − 0.05. Never the clip-time N here: with T = 5 s it would start the tag after the document ends.
3. `add_overlay` with `motionDocumentId` on the camera clip, `startTimeMs` T × 1000 and `durationMs` D × 1000 (both on the clip's timeline), full frame (point 0,0, 1920 × 1080), depth front.

All of step 2 went through as one batch of about 25 commands in the test build; `setKeyframes` takes `x` on a group and hex values on `color`.

## Checking it

`get_filmstrip` with the clipId (so times are clip times; for the video's own timeline add the clip's start) at T+0.3, T+0.8 (half typed), T+1.4, T+2.55 (first word pink), T+2.68, T+2.8 (last word yellow alone), N+0.15 (tag sliding), N+1 and the end − 0.1 s. Look for: the title over the speaker's face (move it to the other side, or start it before they sit down), a word gap that reads as two spaces or none, the last word typing while line 1 is still faint (fine) or after the speaker is talking (move T earlier), the role colliding with the name, the tag under the video's captions (lift both by the caption's height), and a gradient edge visible at the overlay's start. Read every word against the transcript and the form.

## Gotchas

- The typewriter on a left- or right-aligned title doesn't reflow: letters appear in their final places, so the word never shifts as it types.
- `get_motion_frame` renders the transparent overlay over black; judge the gradient and contrast in the video.
- Group transforms scale about the canvas centre; the title only translates, so leave its anchor alone.
- Each line-1 word ends at its own time; a word that ends before its flash key never shows its colour, so set the flash at end − 0.12 s exactly.

## Variations

- No role: the name alone, same place.
- Portrait (1080 × 1920): title 132 px at x 72 with line 1 at about y 1180, tag 44 px at y 1560, clear of the platform's captions. Untested.
- No interview footage: `generate_video` "Documentary interview shot, static camera, a <person> sits framed on the right third, looking just off-camera to the left as they talk, the left half calm background, shallow depth of field, no text", 8 s.
