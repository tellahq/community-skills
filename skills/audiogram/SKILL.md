---
name: audiogram
description: >-
  Turn a podcast or voice clip into a social audiogram in Tella, made in
  Tella Motion and timed to the transcript word by word. Three looks: a
  Spotify-style "now playing" screen (gradient taken from the cover art, big
  cover, scrubber with times, play controls, and a transcript card that lights
  up as it is said), a Substack-style post page (publication bar, serif
  headline, byline, podcast player, and the transcript as the post's text),
  and a cream 1:1 card with a waveform that fills as it plays. Use when asked
  for an audiogram, a podcast clip for Instagram, TikTok, Reels or LinkedIn, a
  "now playing" or newsletter-style share of an episode, a waveform video, or
  a quote from an episode as a vertical or square video.
metadata:
  title: Audiogram
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/now-playing-9-16.webp
  preview: gallery/now-playing-9-16.mp4
  prompt: Make a 9:16 audiogram of the best 15 seconds of this episode, styled like a podcast app's now-playing screen, with my cover art and word-by-word transcript.
---

# Audiogram

A short card that makes a voice worth watching with the sound off. It shows the cover art, who and what is talking, something that moves while it plays, and the words as they are said. The two 9:16 looks copy screens people already know from their podcast and newsletter apps, so the clip reads as "an episode you can listen to" before anyone reads a word.

Use `tella-short` to pick the moment and for the phone's safe zones. The captions here are Tella Motion titles and part of the design, so turn the video's own captions off.

## Ask first

Read the transcript with word timings and propose a moment: one self-contained thought of 8–30 s that opens strong and ends on a full sentence. Then ask in one form:
- **Moment**: prefilled with the start and end words you found, and their times.
- **Look**: Now playing or Post (9:16, for Reels, TikTok, Shorts, Stories), or Cream square (1:1, for feeds and LinkedIn).
- **Cover art**: an attached or library image, or a generated square motif with no text or letters. Never invent a logo.
- **Text**: show name and episode title (Now playing, Cream square); publication, headline, subtitle, author and date (Post). Prefill them from the video and the transcript.

Use the user's own show, publication and author. The gallery's names ("The Green Archive", "The Loamwright Letter", "Tamsin Quillfeather") are invented; never invent a person who might be real. Never put a real app's logo or wordmark on screen: the look comes from layout, colour and type. Draw every icon as a plain path (chevron, dots, tick, 15 s skip arrows, moon, heart, bubble, restack, share).

## The three looks

**Now playing** (1080×1920). Everything sits in one column from x 160 to 920, between the phone's top bar (190 px) and its bottom UI (below y 1536). From the top: a header (⌄, show name centred, •••); a 760 px square cover, radius 16, with a soft dark shadow below; the episode title (Inter 48/700) with the show under it (32/500, 70 %) and a green saved tick on the right; a 6 px white scrubber (track at 28 % white, a round knob, elapsed time left and remaining time right, 26 px at 70 %); centred controls: 1x · back 15 · big white round pause (about 116 px) · forward 15 · sleep timer; then a "Transcript" card, radius 24, about 250 px tall, with the phrase at 48/800 and the next phrase below it.
- Background: a vertical gradient from the cover's dominant colour, darkened, to `#121212` (gallery: `#4F7D5D` → `#1F3528` → `#121212`). The card is a mid tone of that colour (`#4B7A5A`), unspoken words a dark tone of it (`#18291E`), spoken words white.
- The episode title must fit one line of about 660 px at 48 px. Shorten it rather than let it wrap into the show line.
- These parts don't all fit above y 1536. A layout that works: header centred on y 232 (a 19 px "PLAYING FROM PODCAST" at 70 % over the show at 27/700), cover 284–1044, title at 1072, show at 1134, scrubber track at 1266 with clocks at 1286, controls centred on 1380, card 1466–1716 with a 22/700 "Transcript" label at 1486 and the lit phrase at 1528. The card runs past 1536, so keep the lit phrase at its top.
- The look has nothing driven by the audio. When the user asks for a waveform or levels, put the Cream square's 64-bar waveform (52 px tall, white over 28 % white) just above the scrubber as a seek bar, and pulse the cover with the voice.

**Post** (1080×1920). A white newsletter page with margins at x 60 and 1020: a bar with the publication's square logo (the cover, 64 px), its serif name and an orange **Subscribe** pill, then a rule; a Lora 64/700 headline and a grey Lora 36 subtitle; an initials avatar with author (28/600) and date (26); a light grey player card (cover art, title, publication, orange round pause, orange progress line with knob, remaining time); then like 214 · comment 38 · restack 12 · share between two rules. The quote is the body text below, Lora 400 48 px, line height 1.5, starting near y 984.
- Platform colours, not the show's: paper `#FFFFFF`, ink `#1A1A1A`, grey `#6E6E6E`, rules `#E6E6E6`, player `#F4F4F2`, accent `#FF6719`, unspoken body text `#C4C4C4`. Only the logo and the player art come from the show.
- Keep the quote to about 40 words so it ends above y 1500. For a longer moment, use Now playing.

**Cream square** (1080×1080). Cream `#F2E8D5`, dark green text `#1F3B2D`, accent `#E8772A`. A 400 px cover (radius 30) top left that pulses gently with the voice; beside it an uppercase show label (22 px, 0.16 em tracking), a two-line Inter 76/800 title with line height 1.0, and a meta line at 60 %. Across the middle a whole-clip waveform of 64 round-capped bars; under it captions at 64 px across the width.

Inter for interface text (700 titles, 500–600 meta). Lora for the Post's publication name, headline, subtitle and body.

## Motion and timing

Everything that shows progress runs linearly over the whole duration: the scrubber fill (a `trimPath` whose end is keyed 0 → 1), the knob (`x` keyed from 0 to the track's length), the clocks (one title per second, "0:00", "0:01"…, and the remaining time counting down from the rounded duration), and the Cream square's waveform fill.

Captions are titles with a word animator whose `delays` hold one entry per word: its `get_transcript` start minus the moment's start (its time on the document clock) minus the title's start, in ticks (seconds × 254016000000). Use the speaker's words exactly, fixing only the transcript's spelling of names (`update_transcript_words`).
- **Now playing (synced lyrics)**: one title per phrase. Each word's `fillColor` goes dim → white over 0.12 s (easeOutCubic) on its delay. Split at natural breaks, at most about 26 characters so each phrase fits one line of the card, never ending on "the / in / a / of / for". The first phrase is on screen, unlit, from frame 0 (a good poster). The next phrase waits dim 60 px below. On each change, over 0.3 s, the new phrase rises 60 px into place, the one after it rises 60 px (from 120 px below) and fades in, and the old one moves up 60 px and fades out within 0.16 s. A 40 px rise overlaps the 58 px line mid-move. Each phrase title runs from the previous phrase's start to 0.3 s after the next one's. Mask the captions group to the card, below its label.
- **Post (ink)**: one title for the whole quote from 0. Each word goes `#C4C4C4` → ink over 0.16 s on its time.
- **Cream square (reveal)**: phrases of up to about five words. Each word fades in over 0.10 s and rises 22 px over 0.22 s, lands in the accent, holds it to 0.32 s and settles to the text colour by 0.62 s (easeInOutSine).

A phrase runs from 0.06 s before its first word to 0.06 s before the next phrase's first word; the last one runs to the end.

## Building it in Tella Motion

- **Voice inside the document** (Now playing, Post): when the moment is one uncut stretch of one source, make a new 1080×1920 document without a `videoId`, add the source with `addMedia`, then `node.patch` its `sourceIn` to the moment's start and `common.hidden: true` (its sound still plays). Set the canvas duration to the moment and make a motion clip of it in a new video (captions off), so the user's original stays untouched.
- **Audio on a clip** (Cream square, or any moment with cuts): `duplicate_video` the range as a new 1080×1080 video, captions off, and place the document as a full-frame front overlay; its opaque background hides the footage.
- **Voice-driven parts**: read `get_audio_levels` over the range, normalise it (roughly 10th–97th percentile) and smooth it (fast attack, slow release) into a curve. Bind the cover's `scale` to about 0.98 + 0.035 × level. The waveform is 64 round-capped bars, the levels bucketed into peaks, height (0.18 + 0.82 × level) × 120 px, at least 6 px. Draw it twice, a 22 % base in the text colour and a played copy in the accent, and reveal the played group with a rect mask whose width is keyed across the duration. Don't use the live `audioSpectrum`/`audioWaveform` generators for this: they show only the current moment, look like a flat row of dots in stills, and a muted node can't drive them.
- Crop the cover to the image's centred square with `sourceRect` and a rounded rect mask. The Post reuses the same image for the logo and the player art.
- Name nodes by role and group each part (header, cover, scrubber, controls, card, captions) so the user can move or swap them. For several clips from one episode, `duplicate_motion_document` the finished one and swap the voice's `sourceIn`, the title and the caption titles.

## Gotchas

- `addShape` takes only a flat colour. For the gradient, patch the shape's `paint` source to a linear gradient.
- Keyframing `x` or `y` moves a node by that many pixels from where it was drawn, not to that position.
- A word animator holds its first key before each word's delay, so a dim → white `fillColor` pair shows the whole phrase dim until each word is said. That is the lyrics look.
- A `node.patch` of a title's `content` must repeat the full paragraph (text, position, width, align, style, animators).
- A hyphenated word ("real-world") counts as two animator words: give each half its own delay. In a paragraph it may break after the hyphen, which is fine.
- `inspect_motion_node_properties` reports a bound property as 0; check it in rendered frames.
- A group scales about the canvas centre. Set `anchorX`/`anchorY` to the cover's centre before binding `scale`. Masks don't follow their own node's scale, so put the rounded mask on an inner group.
- Everything keyed over the whole duration has to be re-keyed if the duration changes.
- Vintage catalogue films never get a transcript (`get_transcript` stays empty, even with captions on). Get word times another way, such as speech recognition with word timestamps, and check the starts against `get_audio_levels` onsets (a step above −20 dB after a quieter one); recognisers often put the first word at 0. Never type captions from memory. Bring the film in with `add_library_item` (`from: vintage`, scope `private`; scope `video` is refused) and make a scratch video from its `sourceId` to read its levels.

## Check

- `get_motion_frame` full size at 0, mid-phrase, during a phrase change and on the last frame: the cover is crisp and inside its mask, no title wraps, card phrases are one line each and never overlap the next, and the lit word is the one being said.
- One `get_filmstrip` across the whole duration: the highlight or ink reaches each word on time and the scrubber runs to the end. Confirm with `get_audio_levels` that the result isn't silent (around −19 dB mean; old films run quieter, about −23).
- Look at it as someone who uses the app daily would: the order of the parts, the white scrubber and big round pause, or the orange Subscribe pill, serif headline and reactions row. If it doesn't read as that app at a glance, fix the layout, not the colours.
- Report each audiogram's link, its range in the source, the look and the phrase list. Say that you checked timing in preview renders, not by listening.
