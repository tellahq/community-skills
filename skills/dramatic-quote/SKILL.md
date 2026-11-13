---
name: dramatic-quote
description: >-
  Set a short press quote over slow cinematic footage like a film trailer: a
  few words in an old-style serif (IM Fell English), small and centred as a
  justified block with hanging quote marks, landing one line at a time on hard
  cuts, then the attribution in two beats (the name, then the publication) on
  one row underneath, and everything fading out together. Built from plain text
  overlays, so it works in every workspace and stays editable. Use when asked
  for a dramatic quote, a press quote, a review quote, a critic's quote, a
  trailer quote, a pull quote over footage, "as seen in" praise, a quote card
  with attribution, or a cinematic quote moment.
metadata:
  title: Dramatic quote
  author: Tella
  category: Titles & text
  image: og.jpg
  poster: gallery/jutland-courier.webp
  preview: gallery/jutland-courier.mp4
  prompt: Put "a quiet, aching film that stays with you long after it ends" from Maya Ortiz at The Northwind Review over slow misty footage, like a trailer.
---

# Dramatic quote

One quote, about ten seconds, in the voice of a film trailer: slow, quiet footage, and a few words of praise set small in an old-style serif in the middle of the frame. Each line cuts in on its own beat, the name follows, then the publication, and the whole block fades away before the shot ends. It is a moment on its own (a trailer card, an opener, social proof between scenes) or an overlay on a stretch of footage the video already has. Five text overlays, no Tella Motion document: they stay editable in the editor's text panel. Builds on `tella-motion-design` (placement, checks) and `tella-kinetic-type` (text overlay animation).

## Ask once

Work out yourself, never ask: the quote when the message or its attachments give one, or when the speaker reads it out (`get_timeline` with `words`); the name and publication when they are said or written next to it; the clip to put it on (the one the user is looking at, else the first clip); whether the clip has picture worth using (`get_filmstrip`: slow, uncluttered, mid-to-dark in the middle of the frame); the canvas size.

Then one `ask_form`, every field prefilled so the user can just submit:

1. **Quote** (required, one line): the words without quote marks, at most about 12 words / 70 characters. Prefill from the message or the transcript, shortened only by cutting words, never by rewording. The user may put ` / ` where lines should break; otherwise you break it (see the look).
2. **Name** (required): who said it, up to about 24 characters. Prefill from the message, else `Name Surname` as a visible placeholder.
3. **Publication or role** (optional): up to about 28 characters, e.g. `The Northwind Review` or `Film critic`. Empty: the name stands alone, without its comma.
4. **Footage** (pick): `This clip` (default when the clip has usable picture), `From my library`, `Generate new footage` (default when the clip is a talking head, a screen recording or blank).
5. **What the footage shows** (one line, used only for generation): prefill from the quote's mood, e.g. `misty lake at dawn, slow push-in`.
6. **Start** (slider, seconds on the clip, 0 to the clip length): prefill with 0.3 s before the first quoted word when the speaker reads it, else 0.
7. **Lines land on the spoken words** (switch): on when the quote is in the transcript, else off and hidden in the prefill note.
8. **Length** (slider, 6–15 s, default 10).

Skipped or submitted untouched: build with the prefilled values. Media can't go in the form: for `From my library`, look at the message's attachments, then the video's own library (`list_library` scope `video`), then `list_library` type `video` in private; if nothing fits, `ask_question` for "one slow, quiet shot of at least the chosen length: a landscape, a street at night, water, an empty room; no faces looking at the camera, no text". Fall back to `generate_video` (seedance-2.5, the chosen length rounded up) with the field-5 subject plus `slow cinematic dolly forward, low mist, muted desaturated palette, soft overcast light, 35mm film look, gentle grain, no people, no text, calm and quiet`. Tella's vintage film catalogue (`list_library` scope `vintage`) suits a black-and-white take.

## Timing

- **Without speech** (Grant's rhythm, times from the start, for 10 s): line 1 at 0.8 s, line 2 at 1.75 s, line 3 at 2.7 s (0.95 s apart), name at 4.2 s (1.5 s after the last line), publication at 4.9 s (0.7 s after the name), everything ends at 9.7 s, fading out over the last 0.7 s, leaving 0.35 s of clean footage before the shot ends. Scale the gaps for other lengths, never below 0.7 s between lines, and keep the full block on screen at least 3 s.
- **With speech**: each line starts 0.1 s before the first spoken word of that line, at least 0.6 s after the previous line. The name lands 0.6 s after the last quoted word ends (or on the speaker saying it), the publication 0.7 s later. The fade ends before the speaker's next thought.
- Two lines: drop line 3 and keep the rest of the rhythm.

## The look

All values at 1920×1080; scale every size and offset by the canvas's shorter side / 1080 (a 9:16 canvas keeps the same sizes, with a narrower measure to spare).

- **Font**: IM Fell English, regular (400), a free Google font (OFL). Quote 63 px, attribution 32.7 px, both colour `#F5F0E6` (warm paper white), shadow `subtle`, no background, no outline.
- **Block**: a justified block centred on the canvas both ways. Measure = the widest quote line (about 545 px in Grant's). The other lines are stretched to it with `letterSpacing` (Grant's: 0.023, 0.024, 0.004; keep it under 0.06). The opening `“` hangs left of the block and the closing `”` hangs right of it, so the letters line up, not the marks.
- **Lines**: 2–3 lines of 2–4 words each, broken at phrase breaks with nearly equal widths ("a bizarre experience / and unexpected end / to a regular weekend"). Keep the quote's own case: a fragment starting lowercase reads like a real press clipping. Line tops 78 px apart; overlay boxes 80 px tall.
- **Attribution**: one row 92 px below the last line's top: `Name,` left-aligned at the block's left edge, the publication right-aligned to its right edge, so the row fills the measure (they meet with about one space between them). If the row is clearly wider than the block, the publication drops to its own row under the name.
- **Motion**: no intro animation, `hard_cut` in; outro `fade` 700 ms, easing `accelerate` 0.5, motion blur off; all overlays share one end time so they fade together.
- **Footage**: slow (a push-in or a drift), quiet, desaturated, mid-to-dark where the text sits. No zoom, grade or vignette added in Grant's.

## Building it

1. Font: `list_library` type `font` (private, then workspace) for a name containing "Fell". Missing: `curl -sfL -o /workspace/IMFeENrm28P.ttf https://github.com/google/fonts/raw/main/ofl/imfellenglish/IMFeENrm28P.ttf`, `create_source` kind `font`, `curl -sf -T /workspace/IMFeENrm28P.ttf "<uploadUrl>"`, `add_library_item` named `IM Fell English`; tell the user it is now in their library. Keep the `.ttf` locally either way, the script measures with it. If the download or upload fails, use `fontFamily: "Lora"` (the catalogue's closest old-style serif) and measure with `https://github.com/google/fonts/raw/main/ofl/lora/Lora%5Bwght%5D.ttf`; say so.
2. Footage: `This clip` needs nothing. Library or generated footage goes over the time range as full-frame b-roll (`add_layout`, `media: {type: 'video', sourceId}`, no `layout`), or becomes the video's first clip when the video is empty (`create_video` / `upload_clip` with the `sourceId`). Text overlays sit above b-roll.
3. Layout: copy `scripts/dramatic_quote.py` (`$HOME/.agents/skills/dramatic-quote/scripts/`, fallback `/workspace/skills/dramatic-quote/scripts/`), write a spec (format in the script's header: clipId, canvas, fontFile, fontId or fontFamily, lines, name, source, times, nameTime, sourceTime, end) and run `python3 dramatic_quote.py spec.json > ops.json`. It prints a warning when a line needs too much letter spacing (re-break the lines) or the attribution needs two rows.
4. Pass the printed array as `operations` to one `apply_video_edits` call. With no publication, drop the `source` operation and the name's trailing comma.

## Check

`get_video_frame` at 1920 wide just after each line lands, after the publication lands, mid-fade, and 0.1 s after the end. Look for: line ends forming a straight right edge (the closing mark outside it); the opening mark hanging left of the letters; the publication's last letter on the block's right edge; text readable against the footage (a bright sky behind the words fails); no caption or burnt-in text colliding. Report each line with its time, the attribution, the footage source and whether the font was added to the library.

## Gotchas

- Text overlays don't justify. The stretched look comes only from per-line `letterSpacing`, measured in the real font file; guessing from character counts leaves a ragged edge.
- `letterSpacing` is a fraction of the font size, not pixels (0.023 at 63 px is about 1.5 px per gap).
- A `fontFamily` from the catalogue and a `fontId` can't be combined; IM Fell English only works through `fontId`.
- With `textAlign: right` the box's right edge is the text's right edge: place the publication box by its right edge, not its left.
- Long words in a 2-word line stretch badly; move a word between lines before accepting spacing over 0.05.
- A text overlay belongs to one clip. If the quote's range crosses a clip boundary, move the start so the whole block fits in one clip (or put the footage in as b-roll over one clip); never split one quote across clips.
- Sound: Grant's has none. Keep the clip's own audio; for a trailer feel add soft music with `set_background_music` from Tella's curated tracks (`list_library` scope `default`, type `music`) only when asked. Generated footage is silent.

## Variations

- No publication: name only, left at the block edge.
- Black-and-white: vintage catalogue footage, same type.
- Several quotes in a row: one block per quote, each on its own shot, same rhythm, hard cut between shots.
