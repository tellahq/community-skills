---
name: every-format-delivery
description: >-
  Deliver one finished 16:9 Tella video in every format: duplicate it into a
  9:16 vertical and a 1:1 square copy and re-compose each one for its frame.
  The footage is reframed to fill the frame and follow the subject (face
  tracking on camera clips, crop
  sections that pan with them, never a letterboxed band), titles are re-set in
  that format's safe zones at that format's type size, captions move above the
  phone UI, every overlay is checked with frames, the three are shown side by
  side on a sign-off board, and all are exported. The master is never touched.
  Use when asked to make a video vertical or square, for Reels, Shorts, TikTok,
  LinkedIn or Instagram versions of the same video, for "every format", "all
  aspect ratios", "make it 9:16 and fix what breaks", or to repurpose a
  landscape edit for social.
metadata:
  title: Every-format delivery
  author: Tella
  category: Publishing
  image: og.jpg
  poster: gallery/master-16-9.webp
  preview: gallery/master-16-9.mp4
  prompt: This video is done. Make 9:16 and 1:1 versions, fix anything that breaks, and export all three.
---

# Every-format delivery

One finished landscape edit becomes three deliverables: the **16:9 master**, a **9:16 vertical** and a **1:1 square** (4:5 on request). Same cut, words and graphics, each **composed for its own frame**: the picture fills the frame and follows the subject, titles sit where that frame has room, and type is sized for how that frame is watched. A small 16:9 picture floating in a band is the failure this skill exists to prevent: never letterbox, never fill the rest with a blur or gradient.

Changing a copy's canvas centre-crops the footage (whoever isn't in the middle is lost) and leaves every overlay at its old pixel size and percentage position, so most fall off the frame or render distorted. This skill is the pass that fixes that. It is not a Short: every copy keeps the whole video (use `tella-short` to pick the best 30 s).

## Read the master, then ask once

Read the master's timeline with layouts, overlays, text overlays, settings and words, a filmstrip of the whole thing with subtitles, and a full-width frame of each graphic. Find where the subject is over time: `get_camera_faces` for a camera clip; for uploaded footage it returns nothing, so read it off a filmstrip. Note the footage's own camera moves; the reframe should pan with them, not fight them.

Then one `ask_form`, prefilled: formats (9:16 1080×1920 and 1:1 1080×1080 checked, 4:5 1080×1350 offered), a sign-off board (yes), export when done (yes, captions burned in or not). **Never edit the master**: `duplicate_video` first, then set the copy's canvas with `update_video`. A filmstrip of each fresh copy is the breakage list; name each break ("speaker cut off at 2.5 s", "headline off the right edge").

## Frames and safe zones

| Format | Margin | Keep clear |
|---|---|---|
| 16:9 1920×1080 | 72 px | bottom ~140 px (captions) |
| 9:16 1080×1920 | 54 px | top 10 % (status bar, account); bottom 20 % (caption, account, buttons); the right 120 px from 50–80 % height (like/comment/share column) |
| 1:1 1080×1080 | 54 px | bottom ~150 px (captions) |
| 4:5 1080×1350 | 54 px | bottom ~12 % (feed UI) |

## Reframe the footage to fill and follow

- **Camera clips:** `update_clip` `keepCameraFaceCentered` on each clip of the copy keeps the face centred as it moves (`cameraFocusPoint` when the camera has no face detections).
- **Uploaded footage:** crop sections. Each is a `fullscreen` cover layout whose `crop` leaves a full-height window in the target aspect, centred on the subject and off film borders or black bars, with `transitionStyle: "spring"` so Tella animates the change as a pan: `update_layout` the base, then `add_layout` per section. Start a new section only when the subject drifts more than ~15 % of the window's width, about 0.3 s before they arrive; merge sections under ~0.9 s and tiny moves. Calm beats busy: in the example the 9:16 needed five sections over 11.6 s, the square one. Soft 4× archive footage on 9:16 is the footage, not a reason to letterbox.
- **Screen recordings:** don't crop UI to a sliver. Screen and camera on 9:16 goes `side-by-side` `style: even` (`position: bottom`) or `camera-bubble`; screen-only follows the action with crop sections and must stay readable at phone size.

## The look

When a graphic can't survive the new frame (a wide card, a corner callout that would land on the face), re-set it in this system rather than shrinking it. Masters made with this skill are built in it from the start.

- **Palette.** Paper `#F1E9DA`, ink `#15120F`, accent `#E2512C`, muted `#9C9184`.
- **Edge tabs.** A headline is one snug tab per line, flush to one margin, not a card: a paper rect with ink Archivo 800 at −0.01 em. Each tab is its words plus 0.3 × size each side, 1.14 × size tall, 0.06 × size apart. Above them a kicker tab in the accent with ink Roboto Mono 500 caps at +0.14 em: its words plus 0.55 × kicker size each side, 1.75 × kicker size tall, 0.18 × size above the first line. Ragged edges are the point: the shape is the sentence. A line that wraps in a narrow format just becomes another tab.
- **Series bug.** An accent square, the series name in Roboto Mono 600 and the issue number in Roboto Mono 400, on one line in a top corner, held the whole video, with a soft shadow (y 2, blur 10, opacity 0.6) because footage turns bright behind it. On 9:16 the head owns the top, so the bug turns 90° and runs down the right margin from about y 240.
- **Captions** (`update_video`): backdrop style, `#15120FE6` behind paper text, spoken word `#FF8A5B`, Archivo 700, one line per block.

Words follow `tella-motion-design`: one to four of the speaker's words per line, at most two lines plus a kicker.

## Sizes and placement per format

Type scales **up** as the frame narrows, because a phone shows the frame smaller. If a line won't fit, break it in two; never shrink the type.

| | 16:9 | 9:16 | 1:1 |
|---|---|---|---|
| Headline / kicker | 84 / 30 px (4.4 % of width) | 96 / 36 px (8.9 %) | 80 / 32 px (7.4 %) |
| Tabs | flush right on the empty side of the frame | flush **left** at the margin, just below the chin (the right edge is the button column), ending above ~62 % height | flush right, below the chin |
| Bug | top right, 28 px | rotated, right edge, 30 px | top right, 26 px |
| Captions (`captionPosition` y, `captionFontSize`) | 0.90, 54 px | 0.73, 60 px: the block ends above 0.80 and clear of the tabs | 0.90, 52 px |

Always choose the spot from frames of that copy: the empty part of the frame, clear of the whole person, inside the safe zones.

## Motion and timing

Each tab wipes open from its anchor edge in 0.5 s on one ease, bezier (0.16, 1, 0.3, 1): kicker first, each line 0.07 s after the last. Its words trail by a few frames and slide 0.4 × size into place behind the wipe. On exit the tabs collapse toward the far edge with `easeInCubic` over the last ~0.4 s, taking their words. No fades, no bounce, never an empty tab. The bug's square scales in, then its words slide off it (about 0.3 s each, 0.12 s apart) and hold to the end. A headline enters just before its first spoken word, and keeps the master's start and duration in every format.

## Building it in Tella Motion

Draw every graphic on a **full-frame** document (overlay at 0,0, dimensions = the canvas) with all its nodes in one group, `gfx`, so a new format is `canvas.set` to the new size, delete `gfx`, and rebuild at that format's sizes and positions. Each tab is a rect, its title, and a hidden copy of the rect the title is matted to. Check each rect hugs its words in a full-width `get_motion_frame`.

Other graphics: a Tella Motion one gets `canvas.set`, then its nodes moved and resized, side-by-side parts stacked top to bottom on 9:16; one whose shape is the frame's (a full-frame title card, a diagram) gets its own layout per format, never a scaled-down 16:9 one. Text overlays get a new `point` and a bigger `fontSize` on vertical. Image and video overlays can't reflow: re-place them keeping their aspect, or ask whether to drop one from a format.

## Gotchas

- The copy inherits the master's per-layout `crop`, which cover then crops again (a 16:9 headroom crop on 4:3 footage became a 196 px sliver in 9:16). Always replace it.
- `apply_video_edits` rejects `crop` on layouts: reframe sections go through single `add_layout` / `update_layout` calls, one at a time. After moving a section's time, `list_layouts` again; it can rewrite the base layout's crop.
- An overlay whose document canvas changed renders mirrored or stretched, even after resizing the overlay. Remove the overlay, `duplicate_motion_document`, and add the duplicate as a new overlay. A removed overlay keeps its document claimed, so remove and add in **separate** batches.
- Wipe a tab by keying its rect geometry (`field:geometry/rect/rect/x` and `…/width`), not `scale`, which is uniform and squashes the type.
- Matte the words to the hidden copy of their tab; matting them to the visible tab hides the tab. Deleting `gfx` on a document that doesn't have it fails the whole batch.
- Captions re-chunk per format width: read them in frames, don't assume the master's blocks.
- Library footage placed with `create_video` had no transcript after several minutes (so no captions); the same file through `create_source` + `upload_clip` was transcribed within a minute.

## Check every format with frames

For each copy, filmstrips with subtitles (tiles 300 wide for 9:16, 400 for 1:1) at each graphic's entry, middle and exit and at 250 ms steps through every pan: nothing clipped or in a safe zone, nothing over the face, the head in frame through each pan, type readable at phone size, the tabs opening and collapsing with their words, kicker first. Fix, then re-check that range.

## Sign-off board

A 1920×1080 Tella Motion clip on the ink ground: each format's preview (`get_video_preview` with subtitles, uploaded with `create_source`) plays side by side at equal height (512 px for 16:9 + 9:16 + 1:1, 64 px margins, 40 px gutters), with the format in Archivo 800 and its size in muted mono under each, a short title and series line above, and one accent playhead under all of them. The first panel keeps its sound; mute the rest. `addMedia` fits each video to the canvas height and centres it, so its scale is panel height ÷ 1080 and `x`/`y` are offsets from the centre. Name it "<master name> — all formats" and check a mid-way frame: the same moment in every panel.

## Export and report

When agreed, export each copy (and the master if it has no current export), with captions burned in if asked, and wait for every export. Report one row per format: link, reframe sections and their times, each graphic re-set (old → new placement and size), caption position, anything dropped. End with the board's link.
