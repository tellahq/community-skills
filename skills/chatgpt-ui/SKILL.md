---
name: chatgpt-ui
description: >-
  Recreate the ChatGPT desktop app in Tella Motion as a floating window on a soft grey backdrop and play out
  one exchange in it, timed to the narration. The icon rail, the sidebar with New chat, Projects and Recents, the
  Chat/Work toggle and the empty home screen with its rounded composer are live shapes and type. A prompt types
  into the composer with a caret, the send button presses, the composer docks, the user's grey bubble lands, then
  the answer streams in word by word as markdown (heading, bullets with bold lead-ins, a tip) under a stop button,
  the copy and thumbs row appears and the chat's title types into Recents. The ChatGPT name sits in brand groups
  so it swaps for a generic assistant. Use when asked for a ChatGPT animation, an AI chat UI as b-roll, "show me
  asking ChatGPT", a prompt being typed and answered, or a streaming AI answer as a motion graphic.
metadata:
  title: ChatGPT UI
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/chatgpt-launch-plan.webp
  preview: gallery/chatgpt-launch-plan.mp4
  prompt: When I say "so I asked ChatGPT", show me typing the question into ChatGPT and the answer streaming in.
---

# ChatGPT UI

The ChatGPT app redrawn as Tella Motion shapes and live type, a window at 86 % on a pale grey backdrop: a prompt
types itself, sends, and the answer streams in. Full-frame b-roll over the line where the speaker talks about
asking, or its own clip. Builds on `tella-ui-redraw` (rebuild the screen) and
`tella-ui-interactions` (typing, press, list fills); load `tella-motion-design` first.

## Ask once

Work out without asking: where the speaker talks about asking (transcript words), the length (9–15 s), the avatar
initials (the user's, else invented) and 10 older Recents titles (invented, everyday, 3–4 words, never real ones).

**The answer** is multi-line, so it never goes in the form: take it from the user's message or script, else draft
it from the speaker's words and post it as text right above the form. Format: a heading (≤ 40 characters), one
sentence, 2–4 bullets as `Lead: rest` (≤ 60 characters), an optional `Tip: …`; 60–80 words. Never invent facts
about the user's product: keep what the transcript doesn't say general ("open on the problem") or leave it out.

Then one `ask_form`, every field prefilled so submit works as is:
1. **Prompt** (required): what types into the composer, prefilled from the transcript as a request. ≤ 55 characters.
2. **Answer** (pick, required): "Use the draft above" (default) or "I'll paste my own". On the second, one
   `ask_question` for it in the format above. Skip this field when the user already supplied the answer.
3. **Chat title** (required): what types into Recents. Prefill 3–4 words from the prompt. ≤ 28 characters.
4. **Start from** (pick): "Empty home screen" (default) or "Mid-conversation" (see Variations).
5. **Real ChatGPT marks** (switch, on): off swaps the brand groups for a generic assistant (see Brand marks).
6. **Appearance** (pick): Light (default, the example) or Dark.
7. **Where** (pick): "B-roll over the spoken range" (default) or "Its own clip".

No media is needed: every icon is drawn (`references/icons.md`). Skipped form: build with the prefilled values.

## Timing

One ease-out `{x1: 0.22, y1: 1, x2: 0.36, y2: 1}` for everything that travels; no bounce. The example's clock:

| Time (s) | Beat |
|---|---|
| 0–0.9 | the window is there on frame one and settles from 88.15 % to 86 %; the caret blinks at the placeholder (0.45 s on/off) |
| 0.9–3.2 | typing: the placeholder hides on the first key, the voice button swaps to the send arrow (0.13 s fade), 0.055 s a key |
| 3.2–4.2 | the caret blinks; the send button presses at 3.95: scale 1 → 0.9 (0.1 s, ease in-out) → 1 (0.15 s) |
| 4.15–4.75 | send: `composer` and `es.traygroup` slide down 435 px in 0.6 s; `empty` fades out in 0.17 s; send becomes the stop square; the user bubble fades in (0.3 s) and rises 24 px (0.5 s); the placeholder returns (4.35–4.6); the disclaimer fades in (4.55–4.85) |
| 4.65–5.25 | an 18 px `#0D0D0D` thinking dot pulses where the answer starts (scale 0.6 → 1 → 0.75 → 1, ease in-out sine) |
| 4.75–5.2 | Recents slides down one row (55.2 px); the selected pill fades in (4.85–5.15); the title types from 5.0 at 0.035 s a character |
| 5.25–9.8 | the answer streams: `fade` by word, 0.3 s each, 0.07 s apart |
| 9.9–10.4 | stop becomes the voice button (0.15 s); the action row fades in (0.3 s) and rises 8 px (0.4 s) |
| 10.4–12 | hold, then cut |

**To the speaker's words**: the first key on the word that introduces the question ("so I asked it…"), key interval
= seconds to say it ÷ characters (0.045–0.08 s), send on the pause after. Start the stream on the word that
introduces the answer, stagger so the last word lands as they finish it; hold the finished answer ≥ 1.5 s.

## The look (1920 × 1080)

**Stage**: canvas `#E4E5E9`; a soft glow, circle at (960, 470) r 750 `#F5F6F8` with an image `blur` 260 (tile mode
decal). The app is drawn at full 1920 × 1080 inside group `ui` (origin 960, 540, clip a rounded rect radius 30),
scaled 0.86. Behind it `window.plate`: rect (−1.5, −1.5, 1923 × 1083) radius 31.5 `#D5D6DB` (a 1.5 px rim),
`transformParent: "ui"`, with `dropShadow` 0/40 radius 100 at 22 % black and 0/6 radius 16 at 14 %.

The app is a 1280 × 720 pt ChatGPT window at 1.5×. Inter everywhere (closest to SF Pro), titles at letter-spacing
about −0.01 em. A title's box `y` = baseline − 0.964 × size at line height 1.2.

| Part | Geometry | Colour, type |
|---|---|---|
| Main pane `bg` | full frame | `#FCFCFC` |
| Icon rail | x 0–78 | `#F9F9F9`; active tile 54 px at (12,12), radius 12, `#ECECEC`, filled home icon `#0D0D0D`; icons 24 px at x 39, y 117 / 195 / 273, dots at 351, a 35 px `#E3E3E3` rule at 395, apps grid at 442, all `#8F8F8F`; avatar 36 px circle at (39,1041) `#D8833B`, white initials 12/600 |
| Sidebar | x 78–510, 1 px `#EBEBEB` edge; `#E2E2E2` rule at x 510 | "ChatGPT" 25/600 `#2F2F2F` at x 103, baseline 47; search and collapse 22 px at (402,39), (467,39) `#8F8F8F`; New chat 21/400 `#2F2F2F` baseline 111; "Projects" 184 and "Recents" 329 `#8F8F8F`; "No projects" 244 `#C5C5C5`; Recents rows 21/400 `#2F2F2F` at x 104 from baseline 389, every 55.2; selected pill x 90–498, 44 tall, radius 12, `#ECECEC` |
| Chat/Work toggle | track x 1048–1384, y 13–65, full radius, `#F4F4F4`; "Work" selected: pill x 1202–1383, white, 1 px `#E5E5E5` | 21/500, selected `#0D0D0D`, other `#5D5D5D` |
| Heading | box x 815, width 800, centred, y 318.4 | "What should we work on?" 33/400 `#0D0D0D` |
| Composer | x 638–1793, y 411–604.5, radius 39, white, 1 px `#EBEBEB`; shadows 28 blur 6 down 6 % + 4 blur 1 down 3 % | placeholder and typed text 23/400 at (668, 424.8), placeholder `#8F8F8F`; caret 2 × 29 at (668, 421.5) `#0D0D0D`; plus 21 px at (679,563); "GPT-6.1" `#0D0D0D` + "Light" `#8F8F8F` 21/400 ending at 1640 with a chevron; mic 24 px at (1686,564); round button 54 px at (1753,564) `#3C66BF` |
| Tools tray | x 659–1769, from under the composer to y 673, radius 24, `#F1F1F1` | 21/400 `#5C5C5C`, baseline 645: folder + Choose project, Files, Plugins left; monitor + Open desktop app right-aligned to 1744 |
| User bubble | right-aligned to 1791, top 108, 66 tall, radius 26, `#F0F0F0` | 24/400 `#0D0D0D`, 24 px side padding |
| Answer | at (639, 222), width 1152 | richParagraph 24/400 `#0D0D0D`, line height 1.75, letter-spacing −0.003; heading 30/600 line 1.4 spaceAfter 14; sentence spaceAfter 12; bullets `"•  "` + 600 lead-in, startIndent 6, spaceAfter 4 (14 after the last) |
| Docked composer | same box +435 px | "ChatGPT can make mistakes. Check important info." 17/400 `#8F8F8F` centred at baseline 1066 |
| Action row | 19 px icons from x 654 every 44, ~40 px under the answer | copy, thumbs up, thumbs down, share, regenerate `#5D5D5D`, stroke 1.8 |

No suggestion cards under the tray. **Dark** (untested): stage `#16171A`, glow `#24262B`, plate `#3A3B40`; main
`#212121`, rail and sidebar `#181818`, pills and track `#2F2F2F`, composer and bubble `#303030` with a 1 px
`#FFFFFF1A` edge, tray `#2A2A2A`; text `#ECECEC`, secondary `#AFAFAF`, faint `#6B6B6B`; the button stays blue.

**Brand marks**: the wordmark, the placeholder ("Work with ChatGPT"), the model name and the disclaimer each sit in
a group, `brand.wordmark`, `brand.placeholder`, `brand.model`, `brand.disclaimer` (editor names `brand:…`). For a
generic assistant `setTitle` them ("Assistant", "Ask anything", "Model 2", "AI can make mistakes."). They are
live type, never a downloaded logo; draw no OpenAI logo. Icons are our own line drawings.

## Building it in Tella Motion

Top level in paint order: `backdrop`, `backdrop.glow`, `window.plate`, then `ui` holding `bg`, rail, sidebar,
`recents` (one group, so one `translateY` key shifts it), the toggle, `empty` (heading and `es.traygroup`),
`composer` (border, box, `brand.placeholder`, caret, plus, model, chevron, mic, and the `cmp.voice`, `cmp.send`,
`cmp.stop` groups on one centre, plus `cmp.typed`), `brand.disclaimer`, `conv.user`, `sb.new` (pill + title),
`conv.thinking`, `conv.answer`, `conv.actions`. Insert with `addShape` / `addPath` / `addTitle`, then `group`;
about 60 commands a batch. `node.patch` `window.plate`'s `common.transformParent` to `ui` (scales, unclipped).
- **Typing**: `cmp.typed` starts on the first key, `typewriter` by character (duration 0.01, stagger = key interval);
  the caret's `translateX` steps on hold keys to each prefix's measured width (Inter 23/400, PIL `getlength`).
- **The answer** is one `node.insert` text node with `content.type: "richParagraph"` (runs as in the table, bold
  runs `fontId: font.freeform.inter.600`, which exists once any title uses weight 600), then `setTextAnimation`
  `fade` by word, duration 0.3, stagger 0.07.
- **Buttons** swap with hold keys on group opacity; set `cmp.send`'s origin to (1752.75, 564) before its press.
- **Docking**: identical `translateY` keys on `composer` and `es.traygroup`; `ui` settles 0.8815 → 0.86 over 0.9 s.
- Name the document "ChatGPT UI · <topic>". B-roll is one `add_layout` with the clip's `clipId`, times on that clip's
  playback clock: keep the shot inside the clip where the words are said (shorten it or start earlier). Only if the
  range truly crosses a cut (untested): one document and one `hardCut` layout per clip, the second starting on the
  frame the first ended on, keys on each clip's clock; then `list_layouts` and make the layout after it `hardCut` too.

## Checking it

`get_motion_frame` (with `startTimeMs`) at 0.5 s, 4.5 s and the last frame, full width: window corners and shadow
clean, nothing clipped, no real chat titles. Then a 30 fps preview: the caret stays glued to the last letter,
the press comes before the slide, the tray never crosses the composer, stop turns back into voice as the row appears.

## Gotchas

- `typewriter` skips spaces in its stagger: key the caret on the n-th non-space character; keyframe times must rise.
- Inter is wider than SF Pro: keep the limits above. An answer over ~620 px tall runs under the docked composer.

## Variations

- **Mid-conversation** (untested): no empty state; composer docked and the chat selected in Recents from frame one,
  one earlier exchange (user bubble, two-line answer from the transcript) at the top that slides up out of the
  pane as the new bubble lands; the title doesn't type.
