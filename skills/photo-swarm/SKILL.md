---
name: photo-swarm
description: >-
  Throw a pile of printed photos onto the frame in Tella Motion. White-bordered
  prints fly in from every side, spinning and motion-blurred, and land
  overlapped across the whole frame like snapshots tossed on a table, each with
  a shadow that settles as it lands. A paper label with a handwritten-style
  title (a place and a year, a name, an event) is then thrown on top, the pile
  drifts slowly while it holds, and at the end every print and the label burst
  back out of frame. Built from the user's own photos as its own clip, an
  opener or a recap. Use when asked for a photo pile, photos thrown on a table,
  a collage of snapshots, a photo burst, photos flying in, a trip or holiday
  recap, a memories or year-in-review opener, a team offsite or event recap, or
  a title over a pile of pictures.
metadata:
  title: Photo swarm
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/amalfi-coast-2026.webp
  preview: gallery/amalfi-coast-2026.mp4
  prompt: Open my trip video with these photos thrown onto a table and a label that says Lisbon 2026.
---

# Photo swarm

A pile of printed photos: white-bordered prints fly in from all four sides, spin into place and land overlapped until they cover the frame, like snapshots thrown on a table. A paper label with a handwritten title lands on top, the pile breathes for a few seconds, then everything bursts back out and leaves the empty table. It is its own 8 s clip, usually the opener or the closing recap of a trip, event or year. Builds on `tella-motion-design` (load it first). For cards riding a path use `tella-carousels`; for a plain title card use `tella-title-cards`.

## Ask once

Work these out yourself and never ask: the title (from the video's name, the message or the first sentence: a place and year, an event, a name), the photo order (strongest photo, ideally faces, thrown last so it lands on top), which photos are portrait, landscape or wide (from their dimensions), brand colours (only if the user picks the brand background).

**Photos first.** They can't go in a form. Look in this order: attachments on the message, then a media-library folder the user names, then the video's own clips. If there are none, ask once with `ask_question`: "Send 10–30 photos for the pile (phone photos are fine, a mix of portrait and landscape; people and places both work). Or should I use frames from this video's clips?" Suggested answers: "I'll attach them", "Use frames from my clips", "Generate some". Fallbacks, in order: stills cut from the video's own clips (sharp frames, no burnt-in captions, faces not mid-blink), then `generate_image` (a few "candid 35 mm snapshot of …" images of invented people and places, never of the user). Fewer than 8 photos: crop extra prints from them with `sourceRect` (a portrait crop and a detail crop of a landscape) so the frame still fills. Use at most 30.

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Default / prefill | Limits |
|---|---|---|---|---|
| Title on the label | text | yes | worked out as above, e.g. `Amalfi Coast 2026` | 1–24 characters, one line |
| Background | pick | yes | Off-white | Off-white `#ECE7DE`, Kraft `#C8A97E`, Dark `#1E1C1A`, Brand (the brand's lightest neutral) |
| Label | pick | yes | White card, red marker | White card (red marker), Tape strip, No label |
| Title colour | pick | no | Marker red `#D62828` | Marker red, Ink `#1D1B19`, Brand colour |
| Length | slider, s | yes | 8 | 6–12 |
| Ending | pick | yes | Burst away | Burst away (prints fly out, ends on the empty background), Hold (ends on the full pile) |

If the user skips the form, build with the prefilled values. Show the photo count you used in your reply, not in the form.

## Timing

All times for the default 8 s; for another length, keep the throw and burst durations and stretch only the hold.

| Beat | When | What |
|---|---|---|
| Throw | 0 → ~2.05 s | One print every 0.08–0.17 s (alternate short and long gaps), each flight 0.6 s. Frame 0 is the empty background with the first print entering. 12 prints: last lands 2.05 s. 24–30 prints: the gaps shrink to 0.06–0.1 s, so the throw still ends by about 2.4 s. |
| Label | 2.3 → 2.95 s | Thrown up from below, lands on the pile. |
| Hold | 2.95 → 6.5 s | Nothing new lands. The pile drifts (scale 1 → 1.06, rotation 0 → −1.5°, linear 0 → 7 s); the label grows 1 → 1.025. |
| Burst | 6.5 → 7.2 s | Every print leaves along its own line out, starts staggered over 0.28 s in random order, each 0.42 s. The label goes at 6.56 s. |
| Empty | 7.2 → 8 s | The bare background; cut to the next clip on it. |

With music, land the label on a downbeat (`get_music_beats`) and start the burst a beat before the next section. The title should land while it is said if a voice says it.

## The look (1920×1080, from the example)

- **Background**: one full-frame rect, `#ECE7DE`.
- **Prints**: a white `#FFFFFF` rounded rect (radius 3) with the photo inside a 12 px border, `fit: "fill"` and a `sourceRect` cropped to the print's shape. Three shapes: landscape 4:3 card 544×414 (photo 520×390), portrait 3:4 384×504 (photo 360×480), wide 16:9 584×339 (photo 560×315). Pick the shape nearest each photo's own ratio; a tall phone shot becomes 3:4 by cropping from about 11% down from the top, so heads stay in.
- **Scale and tilt** at rest: 0.88–1.12 per print, rotation ±6–19° (never near 0, alternate signs).
- **Landing spots** for 12 prints (offsets from the centre): (−630, −290) (−260, 310) (630, −365) (−785, 60) (210, 290) (−120, −375) (−600, 320) (295, −240) (650, 365) (−430, −100) (490, 70) (830, −70). That is a jittered 4×3 grid reaching ±830 by ±375, so prints run off every edge and no background shows by 2 s. For more prints, add a jittered 6×4 grid over the same area and land extras between the first ones.
- **Shadow**: `dropShadow` black at 0.32 opacity (0.5 on Dark), dx 0, keyed with the throw: dy 36 → 6 and radius 56 → 16.
- **Label**: a 1000×300 rect, `#FFFDF8`, radius 4, centred, shadow at 0.4. The title is centred live text across the card's 1000 px width, top at y 470, 190 px, line height 1, `#D62828`, in a handwritten font: the workspace's own handwriting brand font if it has one, else Caveat 700. The example's font is an uploaded custom font, so expect Caveat to read a little rounder. Over 18 characters, shrink the size (to 150 px at 24 characters) before widening the card (at most 1300).
- **Tape strip** label (not in the example, untested): no card; a 360×70 strip of `#F3E9CF` at 0.85 opacity, rotated −4°, across the top of the title, the title in Ink with a soft white shadow. **No label**: skip the label beat and start the hold at 2.05 s.
- **Motion blur**: `setMotionBlur` `shutterAngle` 180 on every print group and on the label.

## Building it

1. `create_motion_document` (1920×1080, `canvas.set` duration = Length), then `create_clip` `{type: "motion", documentId}` where it plays. Upload photos that are files with `create_source` `kind: "image"`.
2. Background rect `bg`, then a group `pile`, then a group `label`, in that paint order. Prints are painted in throw order, so the last one thrown lies on top.
3. Each print: build it centred on the canvas (rect, then image, then `group` as `p<i>`, origin 960, 540), and move it only with the group's transform. `addMedia` lands with `fit: "contain"`: patch `fit: "fill"`, `destination` and `sourceRect` with `node.patch`.
4. Throw keys on the group, all 0.6 s with curve `{x1: 0.1, y1: 0.75, x2: 0.25, y2: 1}`: translate from a start point on the line from the centre through the landing spot, 2000–2400 px out (so prints come from every side, not only the nearest edge); rotation from rest ± 120–170°; scale from rest × 1.18. Key the shadow's dy and radius on the same times (an effect parameter is keyed with `node.patch` on `common.effects.<effectId>.effect.<param>`; `setKeyframes` refuses it by index).
5. Burst keys, 0.42 s each with the ease-in curve `{x1: 0.55, y1: 0, x2: 0.85, y2: 0.35}`: hold the rest values, then translate to about 3.5× the landing offset (keep its direction), rotate a further ±45–95°, scale × 1.12. The label goes up and left: translate (−420, −1350), rotation −3° → −70°, scale → 1.15.
6. Label: rect, then title (`addTitle` font `caveat` 700, or the brand font), `group` as `label`; key it translate y 1000 → 0, rotation 4° → −3°, scale 1.06 → 1 from 2.3 to 2.95 s with the throw curve.
7. Key `pile` last (scale and rotation drift). Batches take at most 256 commands: build nodes in one, keys in the next.

## Checking it

- `get_filmstrip` of the document at 0.3, 1.0, 2.0, 2.6, 4.2, 6.8 and 7.5 s. At 2.0 s the background shows only in slivers; at 2.6 s the label is mid-flight and blurred; at 4.2 s the title is sharp, unclipped and over no face; at 6.8 s the prints are leaving in every direction; at 7.5 s the frame is empty (Burst away) or full (Hold).
- One full-size `get_motion_frame` at 4.2 s: border widths equal, no photo stretched (`sourceRect` ratio = destination ratio), faces not cut by the label. Move a face print's landing spot rather than the label.
- A 10 fps `get_video_preview` for rhythm, then the 30 fps one. Previews are cached on the video's `updatedAt`: touch the video before fetching again after a Motion-only edit.

## Gotchas

- Rotate and scale the print group, not the rect and image separately, or the border and photo drift apart in flight. Group anchors default to the canvas centre, which is right here because every print is built centred.
- Motion blur fades a node out at the end of its window. Keep every print's window the whole canvas.
- `sourceRect` is in the source image's own pixels (a phone photo is often 4000 px wide), not the print's.

## Variations

- Portrait 9:16: half the spread horizontally, landing grid 3×5 over ±400 by ±800, label 860×280, title 150 px. Untested.
- Recap over a song: one print per beat for the throw, title on the drop.
