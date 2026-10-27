---
name: text-bubble-stack
description: >-
  Add a stack of skeuomorphic (iOS 6 style, glossy) text-message bubbles behind
  a talking-head speaker in Tella, timed to the words they say: each bubble pops
  in at the bottom with a soft overshoot while the ones above are knocked up out
  of its way with a jaunty wobble, over a full-frame white gradient wash (100%
  white at the top to 10% at the bottom) that fades in with the first bubble.
  The bubbles sit behind the speaker but in front of the wash. Asks the user for
  bubble colour, how many bubbles and what they say. Use when asked for chat
  bubbles, iMessage/text message bubbles, speech bubbles stacking behind a
  speaker, or this bubble effect.
metadata:
  title: Text bubble stack
  author: Grant Shaddick
  category: Full animations
  tags: text message, chat bubbles, imessage, sms, speech bubble, skeuomorphic, talking head, behind speaker, kinetic, overlay
  image: og.jpg
  poster: gallery/no-nope-nooooope.webp
  preview: gallery/no-nope-nooooope.mp4
  video: animate-sms-bubbles-73iy6tz0
  video-aspect: portrait
  prompt: Add a stack of text bubbles behind me for what I say at the start, in a colour that matches my shirt.
---
# Text bubble stack

A stack of glossy chat bubbles behind the speaker, one per spoken phrase, over a white gradient wash. `references/reference.jpg` shows the finished look (violet theme, "No / Nope / Nooooope!") on a 9:16 talking-head clip. `scripts/make_bubbles.py` renders the bubble images and the wash.

## 1. Ask first

Read the transcript (`get_transcript` on the clip, word timings) to find the phrases that could be bubbles, then ask with one `ask_form`:
- **Bubble colour**: a choice such as Match the speaker / captions (look at a frame and the video's `captionStyle`), Classic iMessage blue, Grey (received), Green (SMS), or a custom colour. Fill in your pick.
- **How many bubbles**: a number (usually 2–4). Fill in the number of phrases you found.
- **What they say**: one text field, one bubble per line, separated by ` / `. Prefill it with the spoken words, written expressively when it suits the delivery (e.g. "No / Nope / Nooooope!").
Also confirm, in the same form, which spoken moment each bubble lands on when it isn't obvious.

## 2. Colour themes

Each theme is a vertical gradient (top light, mid, bottom) plus an outline, shadow and text colour:
- Classic iMessage blue: top #E3F0FD, mid #B4D5F8, bottom #8DBCF1, outline #55779F, shadow #1D3557, text #000000.
- Violet (matched to a lavender shirt and indigo-outlined captions): top #F3ECFF, mid #CDB8F4, bottom #A98AE8, outline #4A45A0, shadow #312E81, text #312E81.
- Any other colour: derive a pale top, mid and saturated bottom from it, a darker outline (slightly lighter than the darkest shade, not near-black), and dark text in the same hue.
Match a speaker or caption colour by sampling a frame and reading `get_video` `settings.captionStyle`.

## 3. Render the images

Write a spec JSON (`texts`, `fontSize` 88, `theme`, canvas size from `get_timeline`, `wash` `{top: 1.0, bottom: 0.1}`) and run `python3 scripts/make_bubbles.py spec.json out/`. It prints each bubble's 1x width `W` (170 px tall, tail at the bottom right, width fitted to its text) and writes `wash.png`. View one bubble on a grey background before uploading.

Upload each PNG: `create_source` (kind image, the printed pixel size), `curl -T`, `wait_for_jobs`, then `add_library_item` (private) to get a hosted `url`. Image assets in a Tella Motion document need that URL.

## 4. Build the Tella Motion document

`create_motion_document` with the videoId, width ~600 (wide enough for the widest bubble + 30), height = 3 slots for 3 bubbles (slot step 188 px: 170 bubble + 18 gap; bottom slot y = height − 20 − 170). One batch:
- `canvas.set` duration = from the first bubble's word to where the stack should end (often the clip end).
- `asset.set` kind `images` per bubble: `{id: "bubble.N", source: {type: "uri", uri: <library url>}, dimensions}`.
- Per bubble a `node.insert` group `bN` on the canvas, starting at its appear time and lasting to the end, `common.origin` at the tail tip (x = rightEdge − 6, y = 164), motion blur `{shutter: 180, samples: 12}`, child `raster` (`fit: fill`, destination `{x: rightEdge − W, y: 0, width: W, height: 170}`). The bubbles are right-aligned with the tails on the right, like sent messages.
- `addTitle` in each group: the text, font `inter`, size 88, weight 400, the theme's text colour, `align: center`, box `{x: rightEdge − W, y: 26, width: W − 16}`. Keep the text as live text.
- Keys (easing on a key is the segment leaving it). Soft overshoot easing `{x1: 0.3, y1: 1.18, x2: 0.45, y2: 1}`, never the spring presets (they land hard):
  - opacity 0 → 1 over 0.12 s from the appear time.
  - scale 0.4 → 1 over 0.45 s (shorter if the document ends sooner), soft overshoot.
  - y: starts at the bottom slot. For every later bubble, start moving up one slot **0.1 s before** that bubble appears (so the new one never overlaps it), over 0.45 s, soft overshoot.
  - rotation (jaunty knock): the new bubble swings in from about ±8–10° (easeOutCubic) to the opposite side (easeInOutSine) and settles at a small rest tilt, alternating left and right between bubbles (−3°, +2.5°, −1.5°). When knocked up, each existing bubble rocks about 4–5° the other way and wobbles back to its rest tilt over ~0.4 s. Hold the rest tilt between knocks.
Appear times are the spoken word's start in clip time minus the overlay's start, so the first bubble is at 0.

## 5. Place in the video

One `apply_video_edits` batch on the clip:
- The wash: `add_media_overlay` with `wash.png`, full frame (point 0,0, canvas dimensions), starting at the first bubble's word and lasting as long as the stack, `depth: behind_presenter`, animation intro `{preset: fade, durationMs: 300, easing: {curve: smooth}}`, outro null.
- The stack: `add_media_overlay` with the document id as `sourceId`, dimensions = the document's canvas size, `depth: behind_presenter`, positioned above or beside the speaker's head (look at a frame; the bottom bubble may tuck slightly behind the hair).
- Restack so the wash is under the stack. `list_overlays` and compare their `zIndex`. Setting a `zIndex` moves the overlay to that position and the others keep their order, so only when the wash's `zIndex` is **higher** than the stack's, `update_media_overlay` on the wash with `zIndex` equal to the stack's (the wash moves under it). When the wash's is already lower, leave it: setting it to the stack's index would move the wash on top.
If you later change the document's canvas size, remove and re-add the overlay: an existing overlay keeps the old aspect and renders stretched.

## 6. Check

`get_filmstrip` at each appear time, 0.1 s before each, mid-push and the last frame. Check that no bubble overlaps another, that the text is readable and centred in its bubble, that the wash sits behind the speaker and the bubbles in front of the wash (`list_overlays`: the stack's `zIndex` is higher than the wash's; pale, washed-out bubbles, palest at the top, mean the wash is on top), and that nothing important is hidden behind the head. Fix and re-check. Report each bubble's time and the colour used, and say the motion wasn't watched in playback unless you listened/watched a preview.
