---
name: imessage-ui-16x9
description: >-
  Play out a text conversation in the iOS Messages app, redrawn in Tella
  Motion as an edited 16:9 scene. An iPhone stands on a soft backdrop and
  the camera cuts and glides between close-ups of each arrival and the whole
  phone. Typing dots give way to grey bubbles, a pair of photos and a
  shared-location map card arrive, the thread scrolls, your blue reply is
  typed into the field and sent, Delivered moves down, and a heart tapback
  lands on it. Light or dark, with the real iMessage labels or as a generic
  green text chat. Every bubble is sized to its text and can land on the
  spoken words. Use when asked for an iMessage conversation in a landscape
  video, a fake text exchange on an iPhone, phone texts with zooms or close-ups,
  "show the texts we sent", a chat thread with photos or a shared location, or
  an animated SMS scene as b-roll or its own clip.
metadata:
  title: "iMessage UI (16:9)"
  author: Tella
  category: UI & apps
  image: og.jpg
  poster: gallery/imessage-phone-16x9.webp
  preview: gallery/imessage-phone-16x9.mp4
  prompt: Show our text exchange about lunch as an iMessage conversation on an iPhone, with close-ups as each message arrives and my reply typed and sent at the end.
---

# iMessage UI (16:9)

An iPhone on a pale backdrop playing out a short conversation in the Messages app, cut like an edit: the camera jumps to a close-up of each arrival, glides to the reply, pulls back to the whole phone as the thread scrolls, and ends on the tapback before a last pull-back. Everything is live text and vector paths in one Tella Motion document, so it stays sharp at 6× and every bubble is sized to its words. It plays as its own clip, as b-roll over the stretch where the conversation is talked about, or as a full-canvas overlay. Builds on `tella-ui-redraw` and `tella-ui-interactions`; the cuts follow `tella-camera-moves` (one move, then a hold).

**Brand marks.** The app's name appears only as live type: "iMessage" above "Encrypted" (group `brand:imessage-label`) and as the field's placeholder (group `brand:imessage-placeholder`). Never draw Apple's logo or use downloaded logos, icons or screenshots. **Generic**: `node.remove` the label group, `setTitle` the placeholder to "Text Message", and turn sent bubbles green (`#34C759`, dark `#30D158`).

## Ask once

Work these out yourself and never ask: the canvas (1920 × 1080; for a portrait video use `imessage-ui-9x16`), timings (transcript word times or the pace rules below), line breaks and bubble widths, the stamp ("**Today** 9:38 AM"), which reply is typed (the last `me:` line; earlier `me:` lines pop in like received ones), where photos and the map card sit, when the thread scrolls, the camera's shots, and the address if the user gives only a place name (invent a plausible street; never a real business's address).

**The conversation** comes from the user's message or the transcript, never from the form. Normalise it to one item per line: `them: Hey! Free for lunch today?`, `me: Yes please`, `them: photo: window table, plate of pasta` (one row of 1–2 photos), `them: place: Juniper, 214 Alder St`. If there is none, `ask_question` once: "Paste the conversation, one message per line as `them: …` or `me: …` (add `them: photo: …` or `them: place: Name, Address` for photos or a location)", suggesting an invented demo chat. Limits: 5–9 items for 15–22 s, a message at most ~90 characters (3 lines), at most one photo row and one place, and the last item a `me:` line. Invent names and places for a demo.

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Default / prefill | Limits |
|---|---|---|---|
| Contact name | text, required | the other person's name from the message or transcript, else an invented first name | 1–14 characters |
| Appearance | pick | Light | Light, Dark (dark is untested) |
| Real iMessage labels | switch | on | off = generic "Text Message", green bubbles |
| Avatar | pick | Attached photo if a face photo is attached, else Initials | Attached photo, Initials, Illustrated character |
| Reaction on your reply | pick | Heart | Heart, Thumbs up, Ha ha, !!, None |
| Close-ups | pick | Camera moves between close-ups | that, or Static phone (the 0–1.5 s shot held, with a 2 % push) |
| Backdrop colour | text | `#F5F5F7` (dark `#1C1C1E`) | a hex colour; keep it pale and quiet |
| Pace | pick | On the spoken words when the transcript reads or describes the messages, else Natural texting | two options |

Skipped or closed form: build with the prefilled values.

**Media.** The avatar and the photos come from the message's attachments first, then the video's own media (`list_library` scope `video`), then the user's library. A face photo must be of someone who agreed to appear. Missing photos for a `photo:` line: `ask_question` "Attach 1–2 photos to send in the chat (phone photos, the subject in the middle)", suggesting "Generate them" and "Leave the photos out". Fallback: one `generate_image` per photo, prompted as a candid phone photo with the subject centred, because the result is 2048 × 1152 and each tile shows only its middle ~41 %: "Casual iPhone photo of a bakery counter with a tray of golden croissants and a small handwritten price card, warm morning light, shallow depth of field, the croissants centred in the middle third of the frame, no people, no logos". Illustrated avatar: one `generate_image`, "A friendly 3D cartoon avatar, head and shoulders of a fictional young woman, centred, on a flat pastel pink background". The map card is drawn, never a screenshot or map tiles.

## Timing

**On the spoken words**: each item lands on its first spoken word (or the line that introduces it), on the document's clock (word time minus the clip, b-roll or overlay start). Leave 1.1 s for dots before a received message and 1.5 s for the typing; where lines come faster, drop the dots. **Natural texting**: about 1 s + 0.13 s a word after the previous item, plus the dots (1.1 s) or the typing (16 characters a second). Then place each cut 0.3–1 s before the arrival it frames.

The example (19.5 s): phone in 0–0.35; them 0.6; me 2.4; dots 3.7; them 4.8; photos 5.93; me 7.45; dots 9.0; map card 10.0 (scrolls 75 pt); caret 13.15; typing 13.3–14.5; send 14.86 (scrolls 64 pt more); Delivered 15.31; tapback 16.55; pull back 17.6–18.1; hold to 19.5. Camera cuts at 1.5, 3.5, 6.0, 8.7, 11.3, 13.0 and 16.0.

## The look

Work in iPhone points on the 393 × 852 pt screen: the screen's top-left is at (739.9, 62.9) px and 1 pt = 1.12 px. Every measurement (status bar, header, thread, photos, map card, composer, tail path, phone body, camera, colours) is in `references/imessage-layout.md`; build from it.

- **Type.** Inter for SF Pro: bubble text 16.5 pt, 400, −0.02 em, line height 1.3333; name 700; status-bar time 650; labels, stamp and Delivered 11 pt.
- **Bubbles.** 40 pt tall for one line (+22 a line), 14.6 pt padding, width = the text's Inter width + 29.2 pt (measured with the font file, this matched the example to 0.4 px), at most 283 pt. Sent `#44B5FA`, white text; received `#E9E9EB`, black. The hooked tail is part of the same path, only on a run's last bubble.
- **Photos** 118.2 × 160 pt tiles, 3.6 apart, under one 17.9 pt rounded mask. **Map card** 240 × 178.6 pt in a received bubble's outline: a drawn street map, a red pin at (127, 46.5) with the place's name in red, the place over its address in a grey footer.
- **Phone** iPhone 15/16 Pro proportions, black bezel, steel rim rings, side buttons, Dynamic Island. Backdrop `#F5F5F7`.

## Motion

Arrivals use cubic-bezier (0.16, 1, 0.3, 1), no overshoot.
- **Received or sent bubble, photos, map card:** opacity 0 → 1 in 0.1 s while it scales 0.62 → 1 in 0.34 s about its tail corner (`anchorX`/`anchorY` on the bubble's bottom left, or bottom right for a sent one).
- **Dots:** the pill pops 0.6 → 1 in 0.3 s about its tail corner, the dots pulse (0.38 → 0.95 → 0.38 over 0.6 s, 0.15 s apart, `easeInOutSine`), and it shrinks back to 0.6 and fades in 0.12 s as the message lands in the same slot.
- **Typed reply:** caret on 0.15 s before typing; on the first letter the placeholder and mic hide and the send button pops 0.4 → 1 in 0.22 s; `setTextAnimation` `typewriter`, stagger 0.0625 s; the button dips to 0.86 just before the send. On send the field clears, the button shrinks to 0.5 and fades, the caret blinks (0.5 s), and the bubble rises out of the field into its slot over 0.42 s (start offset in the example: −123 px x, +87 px y, no scale).
- **Delivered:** fades in over 0.25 s from 0.45 s after its send; see the reference for how it moves on.
- **Tapback:** scales 0.3 → 1 about its tail in 0.36 s; the heart pops 0.5 → 1 in 0.3 s, then beats to 1.16 and back by 0.62 s. Other reactions (untested): a drawn thumbs-up path, or "HA HA" / "!!" as Inter 800 type, in the heart's place and colour; None drops the tapback and its shot (pull back at 16.0).
- **Camera:** hard cuts, each jumping to ~95 % of the shot's scale and settling in 0.35 s on cubic-bezier (0.1, 0.6, 0.4, 0.9) with a blur flash, then a slow linear drift; glides of 0.65 s between neighbouring messages. The shot table and the framing rule for other content are in the reference.

## Building it

Generate the commands from the point table with a small script in your workspace (px = 739.9 + pt × 1.12 across, 62.9 + pt × 1.12 down), so a retime is a rerun. A new document is 10 s: `canvas.set` `{duration: {seconds: 19.5}}`. Tree: `bg`, then `camera` › `phone` › `phone.body` (buttons, rims, `screen.bg`) and `screen`: `thread` › `thread.clip` (the rect mask) › `thread.scroll` (labels, stamp, one group per item, `afterN` groups for what moves up when a Delivered goes); `header`; `composer`; `thread.front` (the typed reply, its Delivered and the tapback, at their final on-screen slot, outside the mask so the reply can rise over the field); `statusbar`; `island`; `home.ind`.

- Add every leaf at the root in paint order with `addShape` (rects, circles), `addPath` and `addTitle` (`font: "inter"`, the box top from the reference), then `group` from the inside out. Key `opacity`, `scale`, `x`, `y` with `setKeyframes` and set the pop origin with `setProperty` `anchorX`/`anchorY` (a group's anchor defaults to its content's centre).
- **Masks don't follow the node's own transform**: put each mask on an inner `photos.clip` or `map.clip` group and scale the outer group, so the mask scales with the pop.
- Photos and avatar: `addMedia` by `sourceId`, then `node.patch` `destination`, `fit` and `align`. An initials avatar is a circle with a `node.patch` `paint` linear gradient.
- Camera blur: `addEffect` kind `blur`, `effectId: "camblur"`, keyed as `field:@e.camblur/effect/radiusX` and `…/radiusY`. Effect ids take letters, digits, `_` and `-` only (a dot is refused).
- Typewriter skips spaces: the n-th visible letter lands at start + (n − 1) × stagger; key the caret's `x` with hold keys at those times to the width of the text so far.
- Path colours take `#rrggbb` only; shapes take `#rrggbbaa` (the pin's shadow).
- Ids are global; name groups by item (`m1`, `photos`, `map`, `typing2`).

Place it with `create_clip` (a document made without `videoId`), as b-roll over the conversation's range (`hardCut`), or as a full-canvas overlay, `depth: "front"`. An overlay belongs to one clip: if the range crosses a clip boundary, use b-roll. The result is silent unless you add sound: `add_sound_effect` `"tick"` on received (0.65) and `"press"` on sends (0.55), 20 ms before each landing.

## Checking it

- `get_filmstrip` of the document 0.1 s and 0.4 s after every cut: the framed item fully inside the frame (the tapback shot is the easiest to crop), never a cut onto empty white.
- Just before and after every arrival: text centred in its bubble, tails only on run ends, the dots and the message in the same slot, the caret at the end of the typed text, the reply rising over the field, one smooth scroll, nothing behind the field, the tapback clear of the bubble above.
- Untested: Dark appearance (its colours were never measured), the Thumbs up, Ha ha and !! reactions, Static phone, one-photo rows, and a conversation long enough to scroll before the map card.

## Variations

- For a plain full-screen 9:16 conversation, use `imessage-ui-9x16`.
- "Read 9:42 AM" instead of Delivered; a group chat with names over received bubbles.
