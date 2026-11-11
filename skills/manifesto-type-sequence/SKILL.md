---
name: manifesto-type-sequence
description: >-
  Make a manifesto type sequence in Tella Motion: a short statement set in
  heavy Archivo capitals on a near-black field, three to five lines of two or
  three words, each line's words pushed to the left and right edges of one
  justified column. The words land one after another, then a strip of moving
  black-and-white footage opens in the gap of every line, top to bottom, and
  the last word sits in a red-orange accent. Timed to the spoken words or to
  even beats, as its own clip or as b-roll over the stretch where it is said.
  Use when asked for a manifesto, a mission statement or values sequence, a
  bold typographic statement, words with video in the gaps, a justified type
  opener, a brand statement or a slogan reveal.
metadata:
  title: Manifesto type sequence
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/manifesto.webp
  preview: gallery/manifesto.mp4
  prompt: Open the video with a manifesto of "Ship small / Ship often / Let it run / For years", with archive film in the gaps and YEARS in orange.
---

# Manifesto type sequence

A statement as a poster that builds itself: heavy capitals in one justified column, the first word of each line flush left and the last flush right, and in the space between them a strip of moving footage, cut exactly to the height of the capitals. The words arrive one at a time, then the strips open line by line and the sequence holds. It works as a 7–10 s Tella Motion clip (an opener, a closing statement) or as full-frame b-roll over the stretch where the speaker says the line. Load `tella-motion-design` first. For spoken words over the footage itself use `tella-kinetic-type`; for a plain title card, `tella-title-cards`.

## Ask once

Work out yourself, without asking: the statement (the speaker's own lines from `get_transcript`, or the user's message), the line breaks, where it goes, the brand colours from the video's presets, and which footage fits the strips (the video's own b-roll and screen recordings, attachments on the message). Then ask one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Prefill and limits |
|---|---|---|---|
| **Lines** | text | yes | The statement with ` / ` between lines: `DO WORK / THAT WILL / LIVE ON`. 3–5 lines, 2–3 words each, about 12 letters a line (see the look). The speaker's words, never an invented claim. |
| **Accent word** | text | no | The last word. One word from the lines. |
| **In the strips** | pick | yes | The video's own footage (default when it has b-roll, a screen recording or wide shots) · Attached photos or clips · Tella archive film (default when the video is only a talking head) · Generated clips. |
| **Strips in colour** | switch | no | Off: the strips are black and white. |
| **Colours** | pick, with swatches | yes | Warm black (default), Paper, Oxblood, Forest, or Brand (the video's dark, light and accent). |
| **Timing** | pick | yes | To the spoken words (default when the lines are in the transcript) · Even beats, 0.35 s a word · On the music's beat (only when the video has background music). |
| **Where** | pick | yes | B-roll over the words (default when timed to speech) · Its own clip at the start · Its own clip at the end. |

- If the lines are missing (no transcript, nothing in the message), ask with `ask_question`: "What should the manifesto say? 3–5 short lines, one line per row, e.g. `DO WORK` / `THAT WILL` / `LIVE ON`", suggesting up to three versions from the video's title.
- Strip media can't go in a form. One clip or photo per line. Look first at the message's attachments, then the video's own clips (a source placed with `addMedia` `sourceId`; `list_library` scope `video` lists its media), then the media library. If the user picked "Attached" and none are there, `ask_question`: "Attach 3–5 wide, calm clips or photos (a skyline, a landscape, hands at work, a screen scrolling). Each shows as a thin strip about 105 px tall, so texture matters more than detail."
- Fallbacks: Tella's archive film (`list_library` scope `vintage` with a word from the line: "city", "ocean", "train", "clouds"), then `generate_video` with a wide, slow, low-detail prompt.
- A talking head makes a poor strip (a slice of a face). Use it only if the user asks.
- If the user skips the form, build with the prefilled values.

## Timing

- **To the spoken words:** each word starts 0.1 s before the transcript's start time for it. Keep at least 0.25 s between words; if the speaker rushes, spread them evenly across the phrase.
- **Even beats:** the first word at 1.0 s, then one every 0.35 s (the example: six words from 1.0 to 2.75 s).
- **Music beat:** `get_music_beats`, one word a beat, starting on the first real beat (curated tracks can open with 1–2 s of intro).
- The strips open after the last word: the first strip 0.3 s after it, the next ones 0.12 s apart, top to bottom (example: 3.05, 3.17, 3.29 s). On speech, start them on the last word's end instead.
- Hold the finished poster at least 2.5 s after the last strip is fully open (the example holds 4.6 s, to 8.5 s).

## The look

Values from the example (1920 × 1080, 30 fps, 8.5 s):

| Colours | Field | Words | Accent |
|---|---|---|---|
| Warm black (default) | `#14120F` | `#EFE9DD` | `#FF6A3D` |
| Paper | `#EDE9E0` | `#1A1915` | `#E0482B` |
| Oxblood | `#2A0F12` | `#F4EDE4` | `#F2B84B` |
| Forest | `#0F1F1A` | `#ECEFE6` | `#D4F24A` |

- **Type:** Archivo 800, 150 px, capitals, line height 1, letter spacing 0. The accent colour goes on one word only, set in that colour from the start (no recolour).
- **Column:** x 210 to 1710 (1500 px wide). Every word is a title whose box is the whole column (x 210, width 1500): the first word aligned left, the last aligned right. In a three-word line the middle word joins the left side: its own left-aligned title, its x the first word's right edge plus about 30 px.
- **Lines:** box tops 170 px apart, centred on the frame: top = 455 + (i − (n − 1) / 2) × 170. Three lines are 285, 455, 625; four are 200, 370, 540, 710; five are 115 to 795.
- **Width:** at 150 px a capital is about 100 px wide (W and M about 125, I about 45). The words of a line need at most about 1240 px, which leaves a strip of at least 200 px. When a line is longer, shorten the words first; else drop the size for all lines and scale every number here with it (pitch 1.133 × size, strip offset 0.113 × size, strip height 0.70 × size).
- **Strip:** as tall as the capitals, from the box top + 17 px, 105 px tall. Left edge 30 px past the left word's ink, right edge 30 px before the right word's ink. Example strips: (469, 302, 723 × 105), (654, 472, 649 × 105), (591, 642, 855 × 105).
- **Footage:** `fit: "cover"`, desaturated with a luminance `colorMatrix` (`0.2126, 0.7152, 0.0722` on each colour row), no grade, playing from its start.

## Motion

- **Words:** opacity 0 → 1 over 0.18 s, easeOutCubic. Nothing slides or scales; the column stays still while it fills.
- **Strips:** a rect mask, x fixed at the strip's left edge, width keyed 1 → full over 0.6 s with the curve (0.16, 1, 0.3, 1), so each strip wipes open left to right from the left word.
- **No exit** in its own clip (the cut ends it). As b-roll, the cut back to the speaker is the exit.

## Building it

1. `create_motion_document` (or `create_clip` `type: "motion"` with the length), `canvas.set` duration. As b-roll, place the document through `add_layout` over the stretch. A b-roll layout belongs to one clip (`clipId`, times on that clip's timeline with cuts applied) and can't run into the next clip: keep the sequence inside the clip where the words are said, shortening it or starting it earlier so it ends by the clip's end. Only when the spoken lines truly run across a cut, split there (untested): one document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document starting on the frame the first ended on, keys on each clip's own clock. Then `list_layouts` and make the layout after each time-ranged b-roll a hard cut too.
2. One batch of `node.insert`: the field (a full-frame `roundedRect` shape with zero corners), then one `text` node per word (`content.type: "paragraph"`, `position`, `width: 1500`, `align`, style as above) with `common.start` on its time and `common.opacity` keyed `{time: 0, value: 0, easeOutCubic}` → `{time: 0.18 s, value: 1}` (times in ticks). The Archivo 800 font asset needs `asset.set` (`hostId: "tella.font.archivo.regular"`, weight 800) first.
3. **Measure the gaps; never guess.** `get_motion_frame` after the last word, `startTimeMs`, `width: 1920`, `format: "png"`; download it and in each line's band (box top + 17 to + 122) mark the columns where any pixel differs from the field colour by more than about 60 in any RGB channel (this finds dark words on Paper and the accent word as well as light words on the dark fields). Join runs less than 25 px apart into words; the gap is between the last left-side word's run and the right word's run, inset 30 px. Measure before adding the strips, or the footage counts as ink.
4. Per strip: `addMedia` with `sourceId`, `nodeId`, `start` and `duration` to the end, then one `node.patch` with `destination` {x, y, width, height: 105}, `fit: "cover"`, `audio: null`, `common.masks` (one rect, width keyed as above) and `common.effects` (the `colorMatrix`, skipped when the strips stay in colour).

## Check

`get_filmstrip` of the document at the first word + 0.1 s, the middle, the last word + 0.2 s, each strip's start + 0.3 s (half open) and the last frame. Look for a strip touching or overlapping a word, a three-word line whose middle word crowds the strip, a line wider than the column, the accent on the wrong word, and every word against the transcript. Then `get_video_preview` at 30 fps to check the timing. Report the lines, the accent word, the strip footage and the time of each word.

## Gotchas

- `get_motion_frame` takes `startTimeMs`; anything else silently returns frame 0.
- `get_video_preview` fails with `preview_render_failed` when a silent archive film keeps the `audio` block `addMedia` adds: patch `audio: null` on every strip.
- Masks are in canvas pixels and don't follow the node; key the mask's rect, not the node.
- An archive film first becomes a source with `add_library_item` (`from: "vintage"`, `scope: "private"`); most are 320 × 240, fine for a strip.
- A strip of fast or busy footage flickers; wide, slow shots read best.

## Variations

- **Portrait (untested):** 1080 × 1920, Archivo 800 at 110 px, column x 90 to 990, 5–6 lines of 2 short words.
- **Signature:** a muted Roboto Mono 24 px line (name, date) about 85 px under the column, 0.5 s after the last strip.
