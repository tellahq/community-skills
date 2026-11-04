---
name: phone-chat-thread
description: >-
  Animate a text-message conversation as an iMessage thread on an iPhone in
  Tella Motion, light or dark: the status bar, the contact header with avatar
  and name, blue sent and grey received bubbles with tails, typing dots before
  each incoming message, sent messages typed into the iMessage field first,
  "Delivered" under your last message, and the thread scrolling as it grows.
  Full-screen portrait for 9:16, or an iPhone centred on a backdrop or standing
  beside the footage in 16:9. Every bubble is sized to its text and lands on
  the spoken words. Use when asked for a text conversation, chat
  thread, phone messages, an iMessage/SMS-style chat animation, "show the texts
  we sent", or a fake text exchange in a video.
metadata:
  title: Phone chat thread
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/portrait-light.webp
  preview: gallery/portrait-light.mp4
  prompt: Show the text exchange I describe here as a phone chat thread, with each message landing as I read it out.
---

# Phone chat thread

A conversation that plays out the way people see it on their own phone: the other person's typing dots, their grey bubble, your blue reply typed into the field and sent, a quiet "Delivered", and the thread scrolling up as it grows. Anyone who texts on an iPhone recognises it at a glance. Draw it natively in Tella Motion (live text and vector paths, no images) so it stays sharp, editable and on the word.

Copy the app's interface, not its maker's branding: no logo on the phone or anywhere else, and no wordmark beyond "iMessage" as the field's placeholder ("Text Message" with the green accent). This is not `text-bubble-stack` (glossy bubbles stacked behind a speaker).

## Ask first

Ask everything in one `ask_form`:
- **The conversation**, one message per line, prefixed `Me:` or `Them:`, prefilled from what the speaker says. Under about 90 characters a message, 4–8 new messages for 8–15 s. A made-up chat for a demo uses fictional names.
- **Contact name** for the header (and initials if not obvious).
- **Format**: full-screen portrait chat (default for 9:16), iPhone on a backdrop as b-roll (default for 16:9), iPhone beside the speaker or over footage (overlay), or a separate clip.
- **Mode**: light (default) or dark. **Bubble colour**: iMessage blue (default), text-message green, or a brand hex.
- **Already on screen**: how many of the first messages are in the thread from the start (default: enough to fill most of the screen, about 4 in portrait and 3–4 in a phone).
- **Timing**: on the spoken words (default when they're said), or at a natural texting pace.

Emoji don't render (Tella Motion's fonts have none; they draw as empty boxes). Say so in the form and write the feeling in words.

## The look

Work in iPhone points on a 393 pt wide screen, at two scales: the phone's chrome (status bar, Dynamic Island, home indicator) at true size (screen width / 393), and the app (header, bubbles, field) larger so messages read on video. Message text comes out at about 58 px in a 1080×1920 portrait (3.4 px a point) and never under 28 px at 1080p (1.7 px a point in a 960 px tall phone).

- **Bubbles.** Inter 400, 17 pt on a 22 pt line, letter spacing −0.01 em, 12 × 7 pt padding, 18 pt corners, so a one-line message is a 36 pt pill. Widest 72 % of the screen, 15 pt side margin. 2.5 pt between bubbles from one sender, 9 pt when the sender changes. Break long messages into balanced lines (the narrowest bubble that keeps the line count), never a one-word last line; reword rather than tweak.
- **Tail.** Only the last bubble of each run has one, on the outer side, and it moves to each new bubble of the run as it lands. Its outer edge leaves the side 11 pt above the bottom and curls out to a point 5.6 pt out, level with the bottom; its inner edge is a quarter ellipse (about 11.5 × 7.2 pt) back up into the rounded corner, leaving the small notch the real one has.
- **Status bar** (54 pt): 9:41 in Inter 600 17 on the left; signal bars, Wi-Fi and a full battery on the right; in a phone, the Dynamic Island (126 × 37) between them.
- **Header.** A frosted bar over a 0.5 pt hairline: the back chevron on the left, a 46 pt round avatar (grey gradient, white Inter 600 initials) centred, the name in Inter 12 under it with a small grey chevron, and an outlined video camera on the right. Chevron and camera take the accent.
- **Thread.** "**Saturday** 8:12 AM" centred in Inter 11 grey (day 600, time 400), 12 pt below the header. "Delivered" in Inter 600 11, right-aligned 3 pt under your latest bubble until anything else arrives.
- **Typing bubble.** A 58 × 36 pill in the received colour with circles of 12 and 6 pt trailing off its lower outer corner, and three 8.5 pt dots 12.5 pt apart.
- **Field** (52 pt, opaque, above a 34 pt home area): a 34 pt grey "+" circle, then a 36 pt tall outlined round field with the placeholder in Inter 17 and a mic at its right end. While you type, the mic gives way to a 29 pt round send button in the accent with a white up arrow. Home indicator 134 × 5, 8 pt from the bottom.

| Part | Light | Dark |
|---|---|---|
| Screen | `#FFFFFF` | `#000000` |
| Received bubble / text | `#E9E9EB` / black | `#262628` / white |
| Sent bubble / text | `#1A84FF` / white | `#0A84FF` / white |
| Green accent | `#34C759` | `#30D158` |
| Header bar | `#F6F6F6` at 92 %, backdrop blur | `#161618` at 94 %, backdrop blur |
| Secondary text / typing dots | `#8A8A8E` / `#8E8E93` | `#8D8D93` |
| Field border / placeholder | `#C9C9CD` / `#A9A9AE` | `#3C3C3F` / `#6A6A70` |
| Avatar gradient | `#A7ACB8` → `#868B97` | `#7F8490` → `#5D616B` |
| Backdrop (radial, 16:9) | `#EEF0F4` → `#D6DAE2` | `#262830` → `#0C0D10` |

A light brand accent takes black text on sent bubbles.

**Formats.** Full-screen portrait: the canvas is the screen, with no island and no phone body. iPhone on a backdrop (16:9): screen about 89 % of the canvas height (960 px at 1080p), aspect 393:852, corners 14 % of its width, a near-black bezel (`#0B0B0C`, 1.6 % of the screen height) with a thin lighter rim (`#3A3A3D` light, `#46464A` dark), side buttons, and a long soft drop shadow on the quiet radial gradient. Over footage: the same phone with no backdrop, in the empty side of the shot. Light mode reads best on most footage; dark suits night shots.

## Motion

One ease-out for everything that arrives, cubic-bezier (0.16, 1, 0.3, 1): no overshoot.
- **Received:** typing dots appear about 1 s before the message (the pill scales 0.6 → 1 in 0.3 s; each dot pulses 0.38 → 0.95 → 0.38 opacity over 0.6 s, the three 0.15 s apart, every 0.9 s). On the word the dots shrink and fade in 0.12 s while the bubble scales 0.62 → 1 about its tail corner in 0.34 s, in the same slot.
- **Sent:** the text types into the field with `setTextAnimation`'s `typewriter` preset over 0.6–1.6 s (about 22 characters a second), ending 0.2 s before it lands, a long line sliding left so the caret stays in view. Placeholder and mic hide, the send button pops in (0.4 → 1 in 0.22 s) and presses to 0.86 just before the send. On the word the field clears and the bubble scales 0.84 → 1 about its tail corner while rising 30 pt over 0.38 s, so it comes out of the field.
- **Scroll:** at every arrival the thread moves up over about 0.42 s so the newest item sits 8 pt above the field. It stays top-anchored until it overflows.
- **Phone:** rises in 7 % of the screen height from 0.95 scale over 0.8 s (opacity in 0.4 s), then pushes in 3 % linearly over the rest so the frame never freezes. As an overlay it fades out over its last 0.4 s.

## Timing to speech

Each new message lands at the start of its first spoken word (or of the line that introduces it), on the document's clock (clip time minus where the overlay or b-roll starts). Leave at least 1.5 s between messages for the typing; where lines come faster, shorten the typing lead to 0.5–0.7 s or drop it. At texting pace, space them about 1 s plus 0.13 s a word after the previous one, plus the typing. Start the first new message 1.4–1.8 s in so the screen reads first, hold about 2 s after the last, and keep each bubble on screen at least 0.3 s a word + 0.5 s before a scroll pushes it far up.

## Building it in Tella Motion

Structure: an optional `backdrop`, then `phone` (rim with the shadow, buttons, frame, `screen`). `screen` holds the background, `thread`, `header`, `composer` and the island, with a rounded-rect mask on `screen` in phone mode. In `thread`, one group per message (an `addPath` bubble with its tail in the same path, so there is no seam, plus a title), anchored at its tail corner so it scales from there; one group per typing bubble; the stamp and "Delivered" titles. Key the scroll on `thread`'s y only, and move a bubble by keying its group, not by editing its path. Name groups by message (`m3`, `t3`) so later edits are easy.

Gotchas that were hit:
- **No motion blur on `thread`.** Tella Motion then draws its children a little before their start, so the next bubble ghosts in early.
- **Write every line break into the title** and give its box about 40 pt of slack: titles re-wrap at their box width. Size each bubble from Inter's widths (about 0.55 em a lowercase letter, so estimate generously) and confirm with a frame. Edit text with `setTitle` only if the breaks stay the same; otherwise redraw the bubble.
- **Handing on the tail:** a bubble that loses its tail gets a second, plain path that takes over at that moment.
- **A mask on a title moves with the title's x.** Clip the field's typing text with a mask on a still wrapper group and slide the title inside it.
- **Hiding scrolled bubbles:** the translucent header with a backdrop blur and the opaque field area do it the way the app does. Keep the blur on the header's background shape.
- **Retiming means rebuilding:** every scroll key depends on every arrival, so build a fresh document rather than nudging keys.
- Uploaded footage arrives in the `middle` layout (inset on a blurred copy); `update_layout` `layoutId: "base"`, `layout: {kind: "fullscreen"}` fills the frame.

Place it as a separate clip, as b-roll over the conversation's range (hard cuts in and out), or as a full-canvas overlay with `depth: "front"` and no overlay intro or outro (the document has its own). Optional sound: `add_sound_effect` `"press"` on sends (volume 0.55) and `"tick"` on received (0.65), 20 ms before each landing, 200 ms long.

## Check

- One `get_filmstrip` of the document just before and after every landing: lines inside their bubbles with even padding, each tail on the last bubble of its run and on the outer side, no overlaps, the newest message fully above the field, the status bar and header clear of the screen's corners.
- `get_motion_preview`: dots pulse and give way to the bubble in the same slot, the field types and the send button replaces the mic, the bubble rises out of the field, "Delivered" comes and goes, one smooth scroll per arrival, scrolled bubbles blur under the header.
- `get_filmstrip` of the video: each message on its words, nothing covering the speaker. Report each message with its landing time, the format, mode and colour.

## Making it your own

"Read 9:42 AM" instead of "Delivered"; an "iMessage" label above the stamp for the start of a conversation; an unread count beside the back chevron; a flat avatar colour. In portrait with a talking head, put the thread in the top half as b-roll and the speaker below, as `tella-short` describes.
