---
name: full-frame-titles
description: >-
  Make a film-title moment in Tella Motion: one word set in a very tall,
  condensed, leaning display serif (Playfair Display stretched 2.8 times
  tall and skewed into an italic) in warm yellow, so large it fills the
  whole frame edge to edge over the footage, with a tiny rotated subtitle
  tucked beside one of its letters. It cuts in, holds for a few seconds
  while it pushes in very slowly, and fades away. Works as a transparent
  full-frame overlay on any clip, in front of the footage or behind the
  person in it. Use when asked for a full frame title, a giant title over
  footage, a film or movie title card, a cinematic title, an opening title
  word, a one-word title that fills the screen, a big yellow title, or a
  documentary or trailer style title over b-roll.
metadata:
  title: Full frame titles
  author: Tella
  category: Images
  image: og.jpg
  poster: gallery/dream.webp
  preview: gallery/dream.mp4
  prompt: Two seconds in, put a giant full-frame title over the footage that says DRIFT, with a small subtitle "a film about slowing down" beside it.
---

# Full frame titles

One word, as big as the frame allows: a classic serif pulled 2.8 times taller and leaned into an italic, so the letters run from the top edge to the bottom edge and nearly side to side, in one warm yellow over the footage. A small line of the same serif, turned almost upright, sits in a gap beside one letter like a credit. It cuts in, holds about six seconds with a barely visible push-in, and fades out in its last 0.7 s. It is a transparent overlay on top of a clip, typically an opening shot, a chapter's first shot or a moody b-roll moment. Builds on `tella-motion-design` (timing, one look) and `tella-title-cards` (it is an opening or chapter title).

## Ask once

Work out yourself, never ask: the word (from the user's message, else the video's title or the transcript's key word), when it appears (the transcript's word timings), the footage's orientation and whether a person is in the shot (`get_clip_frame`), and the brand colour (the video's text presets, existing overlays, or the message).

Then one `ask_form`, every field prefilled, so the user can just press submit:

1. **The word** (required, text): one word, uppercase, 4 to 7 letters reads best; 3 and 8 still work (see Fitting the word). Prefill from the message, else the most title-like word in the video's title. If the user gives a phrase, keep its strongest word and offer the rest as the subtitle.
2. **Subtitle** (optional, text, up to about 30 characters): the small rotated line, e.g. "A visual exploration". Prefill from the rest of the video's title or leave empty; empty means no subtitle.
3. **Colour** (pick, default Warm yellow `#F2C24F`): Warm yellow, Cream `#F3E9D2`, Red `#E0453A`, White `#FFFFFF`, or Brand colour (prefilled with the brand hex when known; drop the option when there is none).
4. **Starts at** (number slider, seconds, 0 to the clip's length, default 2 s): prefill with 0.1 s before the spoken word when the word is said in the clip, else 2 s.
5. **Holds for** (number slider, seconds, 3 to 10, default 5.75 s, capped so it ends inside the clip it starts in).
6. **Depth** (pick, default In front): In front of everything, or Behind the person. Offer Behind only when `get_clip_frame` shows a person in the shot; it only shows where letters cross them.

No media is needed: the footage is the user's own clip. If the video has no footage yet, ask with `ask_question` for one clip of 5 to 15 s with a simple, dark-ish shot (a face, a landscape, a street), and offer Tella's vintage film catalogue (`list_library` scope `vintage`) or one `generate_video` as the fallback. If the user skips the form, build with the prefilled values.

## Timing

- Cut it in on the word that names it (0.1 s before its first syllable) or, with no matching word, 2 s into the clip, after the shot has settled.
- The subtitle appears 2.75 s after the word, with a hard cut, once the word has registered on its own. Never animate the letters themselves.
- Hold 5.75 s in all (the example), at least 3 s; it fades over its last 0.7 s. Keep it clear of the next cut or the next graphic.
- An overlay belongs to one clip and its times are on that clip's own clock (cuts applied). A title should not run across a cut, so if start + hold passes the clip's end, shorten the hold to end 0.2 s before it (never under 3 s; with less room, start earlier or put it on the next clip).

## The look (values from the example, 1920 × 1080)

- **Word:** Playfair Display 400, 500 px, colour `#F2C24F`, letter spacing -10 px (-0.02 em), line height 1, centred. Box x 0, y 311, width 1920 (widen it for longer words, below). On the node: origin (960, 540), scaleX 1 (for DREAM), **scaleY 2.8**, **skewX -27°**. The skew is what makes the upright font lean like an italic, and scaleY makes it tall and condensed.
- **Subtitle:** Playfair Display 400, 36 px, the same colour, letter spacing 1.08 px (0.03 em), centred in a box at x 1362, y 327, width 600; origin (1662, 345), **rotate -72.6°**, so it reads bottom to top, parallel to the letters' lean. In the example it sits inside the M, alongside its thin left stroke, in the upper half of the frame.
- **Group** both as `title`, origin (960, 540): scaleX and scaleY keyed 1 → 1.03, linear, over the whole document (a slow push); opacity keyed 1 at 5.05 s → 0 at 5.75 s with `easeInCubic`.
- Overlay: full frame, point (0, 0), 1920 × 1080, `transition: "hard_cut"`, `depth: "front"`. The colour is flat: no shadow, no outline, no glow. Dark or mid-toned footage makes it read; on very bright footage, use the Red or a darker brand colour rather than adding a shadow.

## Building it

1. `create_motion_document` with the `videoId`, named "<WORD> title"; `canvas.set` duration to the hold length.
2. One batch:
   - `addTitle` `word` (start 0, duration = hold, `font: "playfair-display"`, weight 400, fontSize 500, colour, `align: "center"`, letterSpacing -0.02, lineHeight 1, box as above);
   - `addTitle` `sub` (start 2.75, duration = hold − 2.75, fontSize 36, letterSpacing 0.03);
   - `group` [`word`, `sub`] as `title`;
   - `node.patch` on `word` with `common: {origin: {x: 960, y: 540}, transform: {scaleX, scaleY: 2.8, skewX: {unit: "degrees", value: -27}}}`;
   - `node.patch` on `sub` with its origin and `rotate: {unit: "degrees", value: -72.6}`;
   - `node.patch` on `title` with the origin, keyframed `transform.scaleX`/`scaleY` and `opacity` as `{type: "keyframes", timeDomain: "local", keyframes: [{id, time, value, easing}]}`, times in ticks (`canvas.ticksPerSecond`, 254,016,000,000 per second).
3. `add_overlay` with `motionDocumentId`, the start time and hold, full frame, `hard_cut`, the chosen depth.

### Fitting the word

The word should span about 90–95% of the width (inked edges about 80–120 px from each side at 1920) and touch the top and bottom edges. Height comes from scaleY 2.8 at 500 px and never changes. Width changes with the letters:
- Set scaleX to about 5 / letters (DREAM 1.0; ENCORE 0.82 in the test build), then render `get_motion_frame` at 1.5 s, 960 wide, find the leftmost and rightmost inked columns, and scale scaleX by target / measured. One correction is enough.
- For more than 5 letters, widen the box (x -1040, width 4000, still centred on 960): the text wraps at the box width **before** scaleX applies, so ENCORE at width 1920 broke onto two lines.
- 3 letters: scaleX up to about 1.6 still looks right; past 8 letters the strokes get hairline-thin, so ask for a shorter word.
- Move the subtitle into the widest gap between two letters in the upper half (look at the frame), keeping its -72.6° rotation; it must not touch a letter.

## Checking it

- `get_motion_frame` of the document at 1.5 s: one line, nothing cropped except the serifs grazing the top and bottom, side margins even.
- `get_filmstrip` of the video at the cut-in −0.1/+0.1 s, +2.85 s (subtitle on), mid-hold, and the last 0.7 s (fading); `get_video_frame` at mid-hold at 1280 wide to read the subtitle.
- Report the word, subtitle, colour, start and hold.

## Gotchas

- A transparent overlay renders black where it is empty in `get_motion_frame`; judge contrast in the video.
- `addTitle` takes letter spacing in em; the stored document shows px (-0.02 em = -10 px at 500 px).
- Behind the person: `depth: "behind_presenter"` mattes the person in the clip's camera or uploaded footage automatically; with no person it paints in front either way. Not tried in a build yet, so check a frame where letters cross the person.
- Portrait (9:16) was not built: keep fontSize 500, raise scaleY to about 5 to fill 1920 px, and expect scaleX near 0.55 for five letters; check the frame closely.

## Variations

- Two titles in one video: `duplicate_motion_document` and `setTitle` the word, then refit scaleX.
- A slow drift instead of a push: key the group's x by 20–30 px over the hold instead of its scale.
