---
name: projector-quote
description: >-
  Show one short quote like a slide from an old projector: a near-black frame
  with the words in bold condensed type (Oswald) on the left, slightly soft and
  glowing as if thrown on a wall, the speaker's name small underneath, and on
  the right a small 4:3 window of footage playing as old film, with grain,
  flicker, scratches, dust, a warm light leak and a hair in the gate. The
  picture is there from the first frame, the quote fades in after it and out
  before the end, and the whole slide trembles and slips like a worn print. A
  live, editable Tella Motion document, used as b-roll or as a clip of its own.
  Use when asked for a projector quote, an old film quote, a Super 8 or
  home-movie quote card, a vintage or archive-footage quote, a founder's or
  historical quote beside film, a quote slide with a film look, or a nostalgic
  quote moment. For a press quote set over full-frame footage like a trailer,
  use dramatic-quote.
metadata:
  title: Projector quote
  author: Tella
  category: Titles & text
  image: og.jpg
  poster: gallery/everest.webp
  preview: gallery/everest.mp4
  prompt: Show "We just kept fixing the next thing" from our founder Ana Ruiz as an old projector slide, beside grainy film of a workshop.
---

# Projector quote

One line from a person, about eight seconds, shown like a slide from an old projector. The frame is near black. A short quote sits on the left in bold condensed type with the name under it; on the right a small 4:3 window of footage plays as old film. Nothing slides or bounces: the picture is simply there, the words fade up beside it, and the slide trembles as a worn print does. It suits a line from someone the footage is about (a founder, an explorer, a customer on camera) and works as an opener, a chapter break or a closing thought.

One Tella Motion document: every word stays editable and the film look is live effects on ordinary footage, not a baked video. Builds on `tella-motion-design`. For a press quote over full-frame footage, use `dramatic-quote`.

## Ask once

Work out yourself, never ask: the quote and the name when the message gives them or the speaker reads the line (`get_timeline` with `words`); the canvas size; whether it is b-roll over a stretch of the video or a clip of its own (b-roll when the speaker says the line, a clip when the video is empty or the user asks for an opener or an ending).

Then one `ask_form`, every field prefilled so the user can just submit:

1. **Quote** (required): the words without quote marks, at most about 60 characters. Shorten only by cutting words, never by rewording, and only with the user's OK.
2. **Name** (required): who said it, up to about 30 characters. A role can follow after a comma ("Ana Ruiz, founder").
3. **Footage** (pick): `A moment of this video`, `From my library`, `Old film from Tella's vintage catalogue`, `Generate new footage`.
4. **What the footage shows** (one line): used to search the vintage catalogue or to generate.
5. **Length** (slider, 6–12 s, default 8).

**Never invent a quote or put words in a real person's mouth.** With nothing real to show, use a clearly fictional line and name and say so in the report.

## Footage

Anything slow with one clear subject: a landscape, a building, hands at work, a street. The window is small, so wide shots with fine detail turn to mush and a single shape reads best. It needs to last the whole length.

- **Vintage catalogue**: `list_library` scope `vintage` with a `query`. Items are real old film, mostly 4:3, which is what the window wants. An item has a `url`, not a `sourceId`: download it, `create_source` kind `video`, upload it to the `uploadUrl`, and use that source.
- **Library or attachment**: its `sourceId`.
- **Generated**: `generate_video` with the subject plus `slow, static or gently drifting camera, natural light, no people looking at the camera, no text`. Don't ask the generator for a film look: the treatment below adds it, and doing it twice turns to noise.
- Colour footage is right; the treatment cools and fades it. Black-and-white works too.

## The look (1920 × 1080; scale every size and position by the canvas width / 1920)

Nodes in paint order: `ground`, then a `slide` group holding the `film` group (`halo`, `footage`, `gate`, `hair`) and the `quote` group.

- `ground`: a full-frame fill, `#050505`.
- **Film window**: 640 × 480, centred on the right half at (1440, 540), so its top-left is (1120, 300).
- `gate`: the window's shape, a rounded rectangle (radius 22) whose edge is slightly uneven, as a film gate's is. Filled white, blurred 1.6 px, and used as the footage's alpha matte, which hides it. Get the path from `scripts/film_gate.py`.
- `halo`: the same path filled `#9DB2C6` at opacity 0.15 with a 42 px blur, under the footage. It is the projector's light spilling past the frame.
- `footage`: the media node, which fills the canvas when added. Scale 0.4577 (about the canvas centre, the default) so its height just covers the window, and x 480 to centre it in the window. Slide x either way to frame the subject, as far as the footage still covers the window (x 368 in the example).
- `hair`: a 2 px round-capped curved stroke in the ground colour rising about 60 px from the window's bottom edge, blurred 0.8 px: a hair caught in the gate. Also from the script.
- **Quote**: one text node on the left half. Box x 114, width 720, height 1080, centred vertically, left-aligned. Oswald 700 at 84 px, line height 1.16, `#F4F4F2`. Curly quote marks in the text, with hanging punctuation and a 100 px start indent, so the opening mark hangs to the left of the lines. 2–4 lines; for a longer quote drop to 72 px before letting it reach five.
- **Name**: a second run in the same node after a line break, Oswald 500 at 34 px, letter-spacing 0.68, line height 1.15, 34 px of space before it. Because it is the same paragraph, it follows the quote when the words change. No role line, stars, logo or portrait.
- The `quote` group is isolated, rotated −0.8° about (480, 540), and carries, in order: `fx.chromaticAberration` amount 2.5, a 1.1 px blur, and `glow` (radius 18, threshold 0.4, intensity 0.6, softness 0.3, screen). The type should look projected, not printed.

## Film treatment

On the footage, in this order (the order matters, each step works on the one before):

1. saturation 0.85, contrast 0.96, brightness 1.12 (the node's own properties);
2. a 2.6 px blur;
3. a cool `colorMatrix`: `[0.9, 0.04, 0.02, 0, 0, 0.02, 0.95, 0.03, 0, 0, 0.03, 0.06, 1.04, 0, 0.02, 0, 0, 0, 1, 0]`;
4. `fx.levels` gamma 1.18, outputBlack 0.03, outputWhite 0.98 (lifted blacks, dimmed whites);
5. `fx.addGrain` intensity 0.13, size 2, monochrome;
6. the `gate` matte;
7. the shader in `references/old-film.sksl`, with `t` keyed linearly from 0 to the length in seconds and `cx` set as its header says (960 for footage centred in the window, 1205 for x 368).

The shader is most of the look: a projector hot spot with dark corners, exposure flicker, a warm light leak that drifts in from the left now and then, scratches and dust, all stepping 18 times a second. Use it as written.

## Motion

- **Gate weave** on the footage, as wiggles: x by 1.3 px at 7 Hz, y by 1.8 px at 9 Hz, brightness by 0.045 at 12 Hz. Brightness is a multiplier, so 0.045 is 4.5 %; an amount of 4.5 blows the picture out.
- **The slide** (window and quote together): wiggle x 0.9 px at 11 Hz, y 2 px at 13 Hz, rotation 0.1° at 6 Hz. Give each wiggle its own seed.
- **Two frame slips** on the slide's y with `hold` keys: 0 at 0 s, +13 at 2.4 s, 0 at 2.467 s, −9 at 5.3 s, 0 at 5.333 s. For another length, put them at about 30 % and 66 % of it.
- **The quote** fades 0 → 1 from 0.5 s to 1.4 s and 1 → 0 from L − 1.4 s to L − 0.6 s (`easeInOutSine`). The window is there from the first frame to the last, so the picture leads and the words follow.
- **With speech**: start the document so the fade-in begins about 0.3 s before the speaker starts the line, and keep the quote fully up until they finish it.
- No motion blur, no intro or outro on the b-roll: it hard-cuts in and out.

## Building it

1. **The document.** B-roll: `create_motion_document` with the `videoId`. A clip of its own: `create_motion_document` without one (canvas the size of the video, or 1920 × 1080), shown later with `create_clip` (`type: 'motion'`, `documentId`). Everything below is `apply_motion_editor_commands` on it.
2. **Batch 1**: `canvas.set` `{duration: {seconds: L}}`; `addShape` `ground` (fill, `#050505`); `addPath` `halo`; `addMedia` `footage` (`sourceId`, start 0, duration L); `addPath` `gate` (white, fill); `addPath` `hair` (stroke, width 2, round cap). Every node starts at 0 and lasts L. Paths: `python3 film_gate.py` (`$HOME/.agents/skills/projector-quote/scripts/`, fallback `/workspace/skills/projector-quote/scripts/`) prints `{"gate", "hair"}` for the default window; pass `x y width height` for another.
3. **Batch 2, the film**: halo opacity and blur; gate and hair blurs; on the footage `setProperty` scale, x, saturation, contrast, brightness; then `addEffect` blur, `colorMatrix`, `fx.levels`, `fx.addGrain`; then `setMatte` (`matte: 'gate'`, `mode: 'alpha'`); then `addEffect` kind `shader` with the file as `source` and `uniforms: {t: [0], cx: [960]}`; the three `setExpression` wiggles; `group` the four nodes as `film`.
4. **Batch 3, the words**: `addTitle` the quote (`font: 'oswald'`, weight 700, size 84, box `{x: 114, y: 0, width: 720}`, left). Then `node.patch` its `content` into a `richParagraph`: `height: 1080`, `verticalAlign: 'center'`, `paragraphFormat: {hangingPunctuation: true, startIndent: 100}`, the same `defaultStyle`, and two `runs`: the quote ending in `\n`, and the name with `style: {fontId: 'font.freeform.oswald.500', fontSize: 34, fontWeight: 500, letterSpacing: {type: 'value', value: 0.68}, lineHeight: 1.15}` and `paragraph: {format: {spaceBefore: 34}}`.
5. **Batch 4, the slide**: `group` the text as `quote`; `node.patch` `{common: {isolate: true}}`; anchor (480, 540), rotation −0.8; its three effects; `setKeyframes` on opacity. `group` `film` and `quote` as `slide`; `setKeyframes` on its y with `easing: 'hold'`; its three wiggles.
6. **Key the shader's clock**: `inspect_motion_node_properties` on `footage`, find the property ending `uniforms/t/values/0`, and `setKeyframes` it `[{at: 0, value: 0}, {at: L, value: L}]` with `easing: 'linear'`.
7. **Place it**: b-roll with `add_layout` over the time range (`media: {type: 'motion', documentId}`, no `layout`), or `create_clip`.

## Gotchas (all hit while building this)

- A font weight exists in the document only once a title has used it. Patching a run to `font.freeform.oswald.500` fails with `asset.missing_or_wrong_kind` unless an `addTitle` in Oswald 500 came first: add a throwaway one-letter title at weight 500 in the same batch, before the patch, and `delete` it after. The weight stays registered.
- `setMatte` takes a place in the footage's effect stack, where it is called. Call it after the grain and before the shader, the order of the treatment list.
- `setKeyframes` keys are `{at, value}` in seconds, not `{time, value}`.
- The shader's uniforms appear as properties named by their position in the stack (`field:common/effects/8/effect/uniforms/t/values/0`), so look the name up instead of typing it.
- Leave `t` unkeyed and the film freezes: no flicker, one fixed set of scratches.
- Don't paste a noise or hash function into the shader. Tella adds its own, and `fract(sin(...))` hashes draw lines across the grain on export.
- `delete` takes one `node`, not a list.
- Footage narrower than 16:9 only covers the window near x 480. Slide it further and one side of the window goes empty.
- `create_clip` names a new video after the document: rename it with `update_video`.

## Check

- `get_motion_frame` at 1920 wide in the middle of the hold. The quote reads at a glance, its opening mark hangs outside the left edge of the lines, and the name is clear of the last line. The window's edge is soft and slightly uneven with a faint halo around it; the grain is visible but the subject still reads; nothing in the window is clipped to a straight edge.
- `get_filmstrip` of the document over the whole length. The window is there in the first and last tiles, the quote is absent from both, the leak comes and goes, and the brightness is steady from tile to tile (a white-out means the brightness wiggle is too large).
- Report the quote, the name, where the footage came from, the time range, and anything fictional.

## Variations

- **Mirrored**: window on the left at (480, 540) with the footage at x −480, quote box at x 1074, rotation +0.8° about (1440, 540). The light leak still comes from the window's left.
- **Black-and-white**: saturation 0 in place of 0.85, and drop the cool colour matrix.
- **No name**: an anonymous line, or a title rather than a quote. Leave out the second run and the quote marks.
- **Several quotes in a row**: one document each, on different footage, hard cut between them.
