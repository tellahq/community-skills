---
name: imessage-ui-9x16
description: >-
  Recreate the iPhone Messages app (iMessage) in Tella Motion on a phone
  filling a 9:16 frame and play out a short conversation in it: the current
  iOS look with the Dynamic Island, round glass back and FaceTime buttons,
  the avatar over the contact name pill, grey received and blue sent bubbles
  with hooked tails, typing dots, a reply typed into the field and sent,
  Delivered, and a tapback. Light or dark, with the real iMessage labels or
  as a generic text chat. Every bubble is sized to its text and can land on
  the spoken words. Use when asked for an iMessage or iPhone text
  conversation in a vertical video, a fake text exchange for a short or reel,
  a chat thread on a phone, "show the texts we sent", or an SMS-style chat
  animation.
metadata:
  title: "iMessage UI (9:16)"
  author: Tella
  category: UI & apps
  image: og.jpg
  poster: gallery/imessage-portrait.webp
  preview: gallery/imessage-portrait.mp4
  prompt: Show this text exchange as an iMessage conversation on an iPhone filling the frame, with my reply typed and sent at the end.
---

# iMessage UI (9:16)

The Messages app redrawn natively in Tella Motion (live text and vector paths) on an iPhone that fills a 1080 × 1920 frame, close enough to the real app to read as iMessage at a glance. A conversation plays out the way people see it on their own phone: a couple of messages already there, their typing dots, their grey bubble, your blue reply typed into the field and sent, a quiet "Delivered", a heart on it. It's a clip of a conversation, with no camera moves: its own clip in a vertical video, b-roll over the stretch where the conversation is talked about, or a full-canvas overlay. Builds on `tella-ui-redraw` and `tella-ui-interactions`.

**Brand marks.** The app's visible name appears only as live type: "iMessage" above "Encrypted" (group `brand:imessage-label`) and as the field's placeholder (group `brand:imessage-placeholder`). Never draw Apple's logo or use downloaded logo or icon files. **Generic**: one `node.remove` per group, the placeholder becomes a new title "Text Message", and sent bubbles turn green (`#34C759`, dark `#30D158`).

## Ask once

Work these out yourself and never ask: the canvas (1080 × 1920), message timings (from transcript word times, or the pace rules below), line breaks and bubble sizes, the day stamp ("**Today** 9:38 AM"), and which reply is typed (the last `me:` line; earlier `me:` lines pop in like received ones).

**The conversation** comes from the user's message or the transcript, never from a form (it is multi-line). Normalise it to one message per line: `them: Hey! Free for lunch today?`, `me: Yes please, I'm starving`. If there is none, `ask_question` once for it in that format. Limits: 3–8 messages for 8–15 s, under about 90 characters a message. Invent names and places for a demo chat.

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Default / prefill | Limits |
|---|---|---|---|
| Contact name | text, required | the other person's name from the message or transcript, else an invented first name ("Maya") | 1–14 characters, shown in the pill |
| Appearance | pick | Light | Light, Dark |
| Real iMessage labels | switch | on | off = generic "Text Message", green bubbles |
| Avatar | pick | the attached face photo if there is one, else Initials | Attached photo, Initials on a grey gradient, Illustrated character |
| Reaction on your reply | pick | Heart | Heart, Thumbs up, Ha ha, !!, None |
| Already on screen at the start | number slider, messages | 2 | 0–3 (the first messages of the list) |
| Pace | pick | On the spoken words when the transcript reads or describes the messages, else Natural texting | two options |

Skipped or closed form: build with the prefilled values.

**Media.** The only image is the avatar. Take it from the message's attachments first, then the video's own clips, then the media library. A face photo must be of someone who agreed to appear; never a real person's picture otherwise. If the user picks Attached photo and none is there, `ask_question` "Attach a square photo of the contact's face", suggesting "Use initials" and "Generate an illustrated one". Illustrated: one `generate_image` of a friendly 3D cartoon character, head and shoulders, of a fictional person, centred, on a flat pastel background the colour of the ring `#FCC6D3` (the example's avatar is a generated image like this). Initials: two letters, Inter 600 white, on a `#A5A9B4` → `#868A96` vertical gradient circle.

## Timing

**On the spoken words**: each message lands at the start of its first spoken word (or of the line that introduces it), on the document's clock (word time minus where the clip, b-roll or overlay starts). Leave 1.5 s before a message that shows dots or typing; where lines come faster, drop the dots and shorten typing to 0.5–0.7 s. **Natural texting**: about 1 s + 0.13 s a word after the previous message, plus the dots (1.2 s) or the typing (16 characters a second). Start the first new message 1.2–1.8 s in so the screen reads first, hold about 2 s after the last arrival.

The example, 10 s at natural pace with 2 messages on screen at the start: phone in 0–0.85 s; dots 1.25; their message 2.55; field tapped (caret) 2.95; typing 3.3–4.5; send 4.86; Delivered 5.31; tapback 6.75; hold to 10.

## The look

Work in iPhone points on the 393 × 852 pt screen at **k 2.05** (px per pt): the screen is 806 × 1747 px at x 137.2, y 86.7, so message text is 34 px. The phone is centred on the backdrop with about 55 px above and below. Every measurement is in `references/imessage-layout.md` (status bar, header, thread, composer, tail path, phone body, colours); build from it.

- **Type.** Inter for SF Pro: bubble text 16.5 pt, 400, −0.02 em on a 22 pt line; name 700; status-bar time 650; labels, stamp and Delivered 11 pt.
- **Bubbles.** One line is a 40 pt pill (+22 pt a line), 14.6 pt side padding, 15 pt side margin, at most ~72 % of the screen wide, 10 pt apart. Sent `#44B5FA` white text, received `#E9E9EB` black text. The hooked tail is part of the same path, only on the last bubble of a run.
- **Phone.** iPhone 15/16 Pro proportions: 55 pt screen corners, black bezel, brushed-steel rim rings, side buttons, Dynamic Island. Backdrop `#F5F5F7` (dark `#1C1C1E`).

## Motion

One ease for everything that arrives: cubic-bezier (0.16, 1, 0.3, 1), no overshoot.
- **Phone in:** rises 34 pt (70 px) from 0.965 scale over 0.85 s (opacity in 0.35 s), then pushes in 2.2 % linearly to the end so the frame never freezes.
- **Received:** dots pop 0.6 → 1 about the tail corner in 0.3 s and pulse (each 0.38 → 0.95 → 0.38 over 0.6 s, 0.15 s apart); on the word they fade in 0.12 s while the bubble scales 0.62 → 1 about its tail corner in 0.34 s in the same slot. Without dots, the bubble alone.
- **Typed reply:** caret blinks (0.5 s on/off) from the tap, solid while typing; placeholder and mic hide and the send button pops (0.4 → 1, 0.22 s) on the first letter; `setTextAnimation` `typewriter` by character, stagger 0.0625 s; the button presses to 0.86 just before the send. On send the field clears and the bubble rises out of the field into its slot over 0.42 s from 0.84 scale, starting part-way toward the field's left edge.
- **Delivered:** the old one fades in 0.15 s and everything after it closes the 14 pt gap over 0.4 s; the new one fades in 0.45 s after the send.
- **Tapback:** scales 0.3 → 1 about its tail in 0.36 s, the heart beats 1 → 1.16 → 1 just after.
- **Scroll:** add up each message's height, the 10 pt gaps, the Delivered label (14 pt) and tapback room (36 pt) from y 226. When an arrival would end below 766 pt (8 pt above the field's top at 774), `thread.scroll` moves up over 0.45 s so the newest message sits ~8 pt above the field, and the mask fades older ones out under the header. Worked case: eight messages, five of them three lines (5 × 84) and three one line (3 × 40), with seven gaps, end at 226 + 610 = 836 pt, so the thread scrolls 70 pt in total, stepping up at each arrival that overflows. The typed reply in `thread.front` lands at its slot minus the scroll in force after the send, so it ends above the field. The example is short enough not to scroll, so scrolling is untested.

## Building it

Generate the commands from the point table with a small script in your workspace (x px = 137.2 + pt × 2.05, y px = 86.7 + pt × 2.05), so a retime is a rerun. Tree: `bg`, then `phone`: `phone.body` (buttons, rim rings, `screen.bg`), then `screen`: `thread` › `thread.clip` (a rect mask from 151 to 767 pt down, feather 11 pt) › `thread.scroll` (labels, one group per message `m1`, `m2`…, `typing`, and an `after1` group for what shifts when a Delivered goes); `header`; `composer`; `thread.front` (the typed reply, its Delivered and the tapback, outside the mask so the bubble can rise over the field); `statusbar`; `island`; `home.ind`. Messages already on screen start at 0 with no animation. Name groups by message.

- **Avatar:** `addMedia` by `sourceId` into `hdr.avatar`, `node.patch` its `destination` so the face's circle lands on the avatar circle, `fit: "fill"`, and an `ellipse` mask on the group.
- **Typewriter skips spaces:** the n-th visible letter lands at start + n × stagger. Key the caret's `translateX` with hold keys at those times to the width of the text so far.
- **Path colours take `#rrggbb` only**; pre-mix greys. Shapes accept `#rrggbbaa`.
- **Ids are global**: a group can't share an id with any node, including its own child.
- **No motion blur on `thread`**: its children then draw a little before their start.
- **Titles re-wrap at their box width**: write every line break in, balanced, and give 30–40 pt slack.
- **Retiming means rebuilding**: remove `bg` and `phone` and rerun the batches (≤256 commands each).
- **Emoji** in bubbles: register Apple Color Emoji (`asset.set` kind `fonts`, `{id: "font.tella.emoji.regular", source: {type: "host", hostId: "tella.font.emoji.regular"}, family: "Apple Color Emoji", weight: 400, style: "normal"}`) and set them as `richParagraph` runs with that `fontId`.

Place it with `create_clip` (a document made without `videoId`), as b-roll over the conversation's range (hard cuts), or as a full-canvas overlay, `depth: "front"`, no intro or outro. An overlay belongs to one clip: if the conversation's range crosses a clip boundary, use b-roll, or split it into one document and overlay per clip with the keys on each clip's own clock (as `glitch-transitions` does). The result's only sound is optional: `add_sound_effect` on the video, `"tick"` on received (0.65) and `"press"` on sends (0.55), 20 ms before each landing; the speaker's own audio plays underneath.

## Checking it

- `get_filmstrip` of the document just before and after every arrival: text inside its bubble with even padding, tails only on run ends, the tapback clear of the bubble above, the caret at the end of the typed text, nothing behind the field.
- `get_motion_preview`: dots give way to the bubble in the same slot, the send button replaces the mic, the reply rises out of the field, one smooth scroll per arrival when the thread is long.
- Compare one frame with a screenshot of the real app at the same scale: bubble heights, text size, tail shape and header spacing should be hard to tell apart.
- The dark column of the colour table was never re-measured against the current app; check it before relying on it.

## Variations

"Read 9:42 AM" instead of Delivered; a group chat with names over received bubbles; the keyboard sliding up when the field is tapped; with a talking head, the phone in the top half as b-roll (`tella-short`). For a phone on a backdrop in 16:9 with close-ups, photos and a map, use `imessage-ui-16x9`.
