---
name: subscribe-end-screen
description: >-
  Add the two creator calls to action to a Tella video, branded with the user's
  colours: a mid-video subscribe nudge (the channel's monogram tile drops into a
  corner and a brand-coloured slab wipes out of it with a big typographic call
  to action, "Subscribe for more →", or a paper tab whose line rolls to the
  upload schedule while a timer bar runs) as an editable Tella Motion overlay,
  and a 10–20 second end screen with two 16:9 video slots and a subscribe circle
  laid out where YouTube's end-screen elements go, either as a full-frame clip
  (brand panel and ink) or as a paper sheet rising over the last shot. Use when
  asked for a subscribe button, subscribe reminder or nudge, a follow prompt,
  "like and subscribe", an end screen, end card or outro with video
  placeholders, or YouTube end-screen slots.
metadata:
  title: Subscribe nudge and end screen
  author: Tella
  category: Publishing
  image: og.jpg
  poster: gallery/brand-slab-nudge.webp
  preview: gallery/brand-slab-nudge.mp4
  prompt: Add a subscribe nudge in the bottom-left when I say "subscribe", and a 12 second end screen with two video slots in my brand lime.
---

# Subscribe nudge and end screen

Two pieces that share one look: the channel's **mark** (a square monogram tile), one **brand colour**, and big, tight Inter type. Everything is live Tella Motion (shapes, paths and live text, no images), built on `tella-motion-design`. This is the end card that `tella-title-cards` mentions.

- **Subscribe nudge** (5 s, a full-frame overlay with the tag in a bottom corner). The tile drops in with a slight turn, then a slab wipes out of it sideways carrying a small tracked eyebrow (the channel name) over a big call-to-action line. Two styles:
  - **slab**: a brand-coloured slab, "Subscribe for more" and a stroked arrow that nudges forward every ~1.1 s.
  - **tab**: a paper slab; "Subscribe" rolls up like a drum to the schedule ("A new build every Friday") while the slab resizes to fit, and a brand timer bar runs along its foot until the slab folds back into the tile.
- **End screen** (10–20 s at the very end). An eyebrow, a large headline, two 16:9 **video slots** and a **subscribe circle**, placed where the user will drop YouTube's video and subscribe elements in YouTube Studio. The slots are placeholders that read as ours: a flat fill, a slowly drifting diagonal hatch, a thin edge, an outlined play glyph, brand crop marks that close in on the corners, and a numbered mono label ("01 — LATEST VIDEO"). The circle holds the initials, with a dotted ring turning slowly around it, an arrow nudging toward it, and "Subscribe" plus the schedule beside it. Two layouts:
  - **panel** (a clip of its own): a brand panel on the left 840 px rises from the bottom with a two-line headline and the subscribe block; the slots stack on near-black ink on the right.
  - **sheet** (over the last shot): an opaque paper sheet with a thin brand band on its leading edge rises over the footage; the headline runs full width, the slots sit side by side, and the subscribe block sits bottom-right with its label to the circle's left.

It is not a platform button. No pill "Subscribe" button, bell, "Subscribed" toggle, clicking cursor, or any platform's red, logo or play-button shape. The call to action is typography on the channel's own mark and colour.

## Ask first

Ask in one `ask_form`, prefilled with your best guesses:

- **Which pieces**: the nudge, the end screen or both (default both).
- **Channel name** (the eyebrow, in capitals), **initials** (two letters) and a **schedule** line. Never invent a schedule: without one, use the slab style and leave the circle's second line out.
- **Brand colour** (one accent) and a **paper or ink** pairing; offer what the video already uses. A bright brand (lime, yellow, orange) works as the slab or panel with ink text; a deep brand (cobalt, violet, green) works as text, tile and band on paper.
- **Words**: "Subscribe for more" / "Subscribe" for YouTube, "Follow for more" / "Follow" elsewhere.
- **Nudge style and corner**: slab or tab; bottom-left (default) or bottom-right, whichever is clear of the speaker, the cursor and the content.
- **When**: prefill the moment the speaker says "subscribe" or "follow"; otherwise just after the first payoff, 30–90 s in. One nudge per video, two at most.
- **End screen**: length (default 12 s; YouTube allows 5–20 s on videos at least 25 s long), headline ("Keep watching", "Thanks for watching"), the two slot labels ("Latest video", "Best for you", "Watch next", "Most popular"), and panel (a new clip at the end) or sheet (over the last shot).

## Look

Colours: ink `#121212` (panel background `#121316`), paper `#F3EEE4`, text on paper `#17161B`, muted on paper `#6A655C`. On a bright brand panel, muted is a dark shade of the brand (`#434D0C` for lime `#D4F53C`). The examples use lime `#D4F53C` and cobalt `#2B50E8`.

Nudge at 1080p. Don't shrink these; they are what keeps it legible over footage.
- Tile 152 px square, radius 14, initials Inter 800 62 px centred. The slab is the same height, starts under the tile's inner edge, has 40 px padding, and is as wide as the longer of eyebrow and line.
- Eyebrow Inter 700 28 px, tracking 0.14; line Inter 800 58 px, tracking −0.02. Both left-aligned at the same x.
- The tag sits 88 px from the side and 104 px from the bottom.
- slab: brand slab, ink tile with brand initials, ink text. tab: paper slab; tile, eyebrow and an 8 px timer bar in the brand; ink line.

End screen:
- Eyebrow Inter 700 26 px, tracking 0.16, near the top (~104 px). Headline Inter 800, tracking −0.035: ~132 px on two lines (line height 1.0) in the panel, ~108 px on one line on the sheet.
- Slots exactly 16:9: 640×360 stacked in the panel, 720×405 side by side on the sheet, radius 6. Labels Roboto Mono 500 26 px above each slot. Fill, edge and hatch are close tints of the background (on ink `#1A1C20`, `#2C2F35`, `#272A30`; on paper `#E8E2D6`, `#D6CEBF`, `#DCD4C5`). Crop marks and play glyph in the brand, crop marks just outside each corner.
- Subscribe circle ~160–184 px, initials at ~0.36 of its diameter, dashed ring ~20 px outside it. "Subscribe" Inter 800 46–52 px, the schedule 28 px muted below it. Panel: ink circle with brand initials and a hairline that draws on above the block. Sheet: brand circle with paper initials.

## Motion

One ease-out for every entrance (about cubic-bezier 0.22, 1, 0.36, 1), an ease-in for exits, easeInOutSine for the arrow, easeInOutCubic for the roll.

Nudge (5 s): the tile fades in over 0.2 s while it rises ~44 px and turns 7° to 0 over 0.5 s, its initials scaling 0.55 → 1. From 0.22 s the slab wipes out to full width over 0.6 s. At 0.5 s the eyebrow rises, and 0.08 s later the line rises ~84 px out of a masked band. The arrow starts nudging ~12 px at 0.95 s. Tab: at 2.3 s the line rolls up and the schedule rolls in over 0.55 s while the slab resizes with it; the timer runs from 0.8 to 4.3 s. At 4.3 s the copy fades and drops, the slab folds back into the tile 0.1–0.45 s later, and the tile leaves last.

End screen: the panel or sheet rises over 0.7–0.8 s, the eyebrow at ~0.4–0.55 s, the headline line by line from ~0.5–0.65 s (`setTextAnimation` rise by line), the slots from ~0.6–0.8 s, 0.16 s apart (fade, rise 40 px, 0.97 → 1), each slot's crop marks closing in (1.08 → 1) 0.55 s after it, the circle at ~1.0–1.2 s (0.6 → 1), then ring, arrow and labels. Keep something alive while YouTube's elements wait: the hatch drifts ~14 px a second, the ring turns ~9° a second, the arrow nudges every ~2.4 s. Everything fades over the last 0.6 s.

## Timing to speech

Start the nudge overlay 0.3 s before the word "subscribe", so the slab lands on it. Add the library sound `gentle-reveal` (volume 0.5) 0.1 s after the overlay starts and, for the tab, a quiet `toggle` on the roll. The end screen gets `light-reveal` at its start; duck or end the music under it, never under speech.

## Building it in Tella Motion

- Nudge: a document the video's size (`create_motion_document` with the `videoId`), placed full frame, `depth: front`, no overlay transition or motion blur (it animates itself). Groups: a **mark** (tile and initials), the line, the eyebrow, and one **nudge** group around everything. For another nudge, `duplicate_motion_document` it and keep the corner.
- Panel end screen: a Tella Motion clip (`create_clip`, type motion). Sheet: a full-frame overlay on the last seconds of the last clip; the sheet is opaque, so the footage needs no blur.
- End screen groups: one per slot (fill, mask, hatch, edge, play), the subscribe circle, and a **content** group around everything but the panel or sheet, for the exit fade. Name the groups so the user can find them.

Gotchas found while building the examples:
- **Wipes are a rect's keyed width** (with `x` to grow leftwards) for the slab, masks, timer bar, panel and hairline. For a right-corner slab, key `x` with the width so the right edge stays under the tile, and move the eyebrow and line with the slab's left edge when it resizes.
- **Clip text with track mattes** (alpha): the line (grouped with the arrow) to a rect band that moves with the slab, so it rises out of and rolls within the band instead of floating up from below; the eyebrow and timer to a copy of the slab; each hatch to a copy of its slot.
- **Roll both lines with one easing and one duration**, 84 px apart. With an ease-in on the outgoing line and an ease-out on the incoming one, they overlapped mid-roll.
- **No shadow on the tile**: it smudged across the slab. Only the slab carries one (y 14, blur 44, opacity 0.35–0.4); the sheet gets a soft upward one.
- **A trimPath key can't be set in the batch that adds the effect.** Draw lines that draw on as thin rects with a keyed width instead.
- **Fading a group fades each child separately** unless it is isolated (`node.patch` `common.isolate: true`): set it on the nudge, the mark, each slot, the circle and the content group.
- **An Inter cap top sits about 0.236 em below `box.y`** at line height 1.2; allow for it when aligning text to the tile and slab.
- The ring is a stroked circle path with a `dashPath` effect; put any alpha on the node's opacity.
- Size the slab from the copy and check a long channel name, headline or schedule still fits the slab, the panel or the space beside the circle.

## Check

- One `get_filmstrip` of each document: nudge at 0.6 s (wipe), 1.4 s (settled), for the tab 2.6 and 3.2 s, then 4.6 s (folding); end screen at 0.3, 1.0 and 3.0 s and just before its end. Then `get_clip_frame` over the real footage and a preview of the whole piece.
- Look for: the line fully inside its band (no glyph tops or descenders showing while it rolls), the arrow clear of the slab's end, eyebrow and line aligned, initials centred in the tile and circle, slots exactly 16:9 with crop marks square to their corners, the circle round, and the label beside the circle clear of the slots.
- Report the nudge's time and corner, the end screen's range, and that the user places YouTube's elements over the slots and circle in YouTube Studio → End screen.

## Variations

- **Follow prompt**: "Follow for more", "New posts every Monday"; nothing else changes.
- **Portrait (9:16)**: the nudge centred above the captions (~420 px from the bottom); stack 960×540 slots with the circle below.
