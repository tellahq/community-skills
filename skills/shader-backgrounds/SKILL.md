---
name: shader-backgrounds
description: >-
  Designed cards on live, looping shader backgrounds in Tella Motion, in the
  user's brand colours: a chapter card on a drifting topographic map
  ("Survey"), a quote card with archive footage on moving cotton paper
  ("Rag"), a stat slide with two screen-printed ink discs ("Overprint"), and a
  speaker lower third on a small map panel. Each background is hand-written
  SkSL that loops seamlessly, and each card is an editorial layout (folio,
  rules, grid, index) built in Tella Motion. Use when
  asked for shader or animated backgrounds, moving or looping branded
  backgrounds behind titles, topographic or contour-line backgrounds, a paper
  or grain texture card, riso, halftone or print-dot backgrounds, or a chapter
  card, quote card, stat slide or lower third with a moving background.
metadata:
  title: Shader backgrounds
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/survey-chapter-card.webp
  preview: gallery/survey-chapter-card.mp4
  prompt: Make a chapter card for each section of this video on the topographic Survey background in our brand green (#0f2a24, accent #e4f5b8), with the chapter number, title and a one-line dek.
---

# Shader backgrounds

A shader background here is the sheet a layout is printed on, never the subject. Every card is an editorial layout on a 120 px margin grid: a tracked mono folio over a hairline at the top, a left-aligned content block, and a rule with an index, source line or folio at the foot. The shader moves from the first frame to the last and stays quiet wherever type sits.

Three looks, each a hand-written SkSL file in `shaders/` (use the file as it is; the look is in the code):

| Look | What it is | Suits | Card |
|---|---|---|---|
| **Survey** (`survey.sksl`) | Contour lines of a warped relief drifting on a small circle, every fifth line heavier in the accent, faint survey crosses, a quiet zone behind the type | Roadmaps, strategy, chapters | Chapter card (7 s); lower third panel (7 s) |
| **Rag** (`rag.sksl`) | Cotton paper: mottling, embossing lit by a circling light, fibres, specks, two pale brand washes drifting in opposite corners, grain | Stories, customer quotes, archive footage | Quote card (8 s) |
| **Overprint** (`overprint.sksl`) | Two discs of brand ink screened into ordered dots, the second a few px out of register; the ramps turn and the small disc circles the big one | Release notes, numbers, claims | Stat slide (7 s) |

For a plain preset gradient behind a screen recording, use `update_clip` `background: {type: "shaderGradient"}` instead; this skill is for designed cards in the user's own colours. Load `tella-title-cards` too when this is one family of titles across a video.

## Ask first

Find the moments that want a card: each topic change (chapter), a number the speaker stresses (stat), a line worth quoting (quote), the first time a person appears (lower third). Then ask in one `ask_form`: which cards; which look (one look per video for chapters and lower thirds; a stat or quote card may use its own); 2–4 brand hex colours, prefilled from the video's presets; the words, one card per line, prefilled from the transcript and chapters; footage for a quote card (a clip, a library item, or Tella's vintage film via `list_library {scope: "vintage"}`); and where each goes (a separate clip, b-roll over the speaker, or an overlay for the lower third). A stat card needs the before and after values the speaker actually gives; the chapter index lists only chapters the video has.

## Colour by role

Map the brand colours by role, not by their order. One accent per card.

- **Survey:** a dark ground (lightness under 20 %) in the brand's darkest hue, contour lines a mid tint of it, the one bright brand colour as accent (every fifth contour, the numeral, the current chapter, the marker); type near-white with two or three dimmer tints for dek, labels and rules. Example: `#0f2a24` ground, `#8fc4a6` lines, `#e4f5b8` accent, `#f1f7ea` ink.
- **Rag:** light paper (lightness over 90 %), the wash a pale tint of a brand colour, a deep brand tone as accent for the quote mark and short rule, warm near-black ink, an off-white mount. Example: `#f2ebe0` paper, `#e2b39a` wash, `#a3472f` accent, `#2a211c` ink.
- **Overprint:** paper, `inkA` the main brand colour (saturated, mid-dark), `inkB` a contrasting second ink; the kicker and the "after" bar use `inkA`; type one near-black. Example: `#efe9df`, `#3b5bdb`, `#f0506e`, `#1b1d3a`.

Only dark Survey and light Rag/Overprint are proven; any other variant needs every frame checked.

## The design system

- **Grid:** 1920×1080, content from x 120 to 1800. Folio at y 100 over a 2 px rule at y 150; foot rule around y 884–920 with labels just under it (lowest text ends near y 975).
- **Type:** titles Inter 700 tracked in (−0.035 em at 136 px, −0.025 em at 64 px); numerals Inter 200 at 210 px or Space Grotesk 700 at 300 px; quotes Playfair Display 500 at 68 px, line height 1.12, with a 220 px accent quote mark; folio, labels, index, captions Roboto Mono 500/700 at 24–28 px, uppercase, +0.12–0.16 em. Nothing under 24 px.
- **Chapter card:** "CHAPTER 03 / 05" right in the folio row, the thin numeral in the accent, a two-line title below it, a 38 px dek, the chapter index along the foot (1680 px split evenly, the current one bold in the accent with a 6 px accent bar on the rule), and a pinging map marker with a date label on the right.
- **Quote card:** footage in an off-white mount on the left (about 760×610 at x 120, 20 px border, radius 3, soft drop shadow) with a mono figure caption under it; the quote, a 72 px accent rule, name (Inter 600, 36 px) and role on the right from x 980; a folio-style foot.
- **Stat slide:** content in the left 740 px: folio and rule, a mono kicker in the accent, the 300 px number, a two-line 50 px claim, before/after bars drawn to scale (before 440 px, after 440 × after / before) with mono labels and values, a source line on the foot rule. The discs own the right half.
- **Lower third:** an 860×188 Survey panel at x 120 near the bottom, an 8 px accent tab on its left edge, the name in Inter 700 64 px and the role in tracked mono, a pinging marker at the panel's right end.
- **Keep the shader off the type:** Survey's `calm` ellipse sits on the type block; Rag's washes stay in the corners; Overprint's discs stay right (`discA` x 0.76).
- **Never:** a centred title over a full-frame shader, a logo on the shader, a lone small card in empty space, a card without its folio/foot structure.

## Motion

- The background moves from frame 0 and loops every `loopSeconds`; keep that equal to the card length (or an exact divisor) so a held or repeated card has no seam.
- Type enters 0.3–2.1 s in, staggered by role (rules and folio first, then numeral, title, dek, then index and marker). Fade in 0.56 s (0.63 s for big lines) and rise 10–40 px over 0.8–0.9 s, on ease `0.22, 1, 0.36, 1`; big lines also go from a 10–14 px blur to sharp. Rules draw from their left end.
- Something stays alive through the hold: the marker pings every 1.5 s (a ring scaling 1 → 2.6 while fading out over 1.4 s), the number counts up (0.75–2.0 s), the contours flow, the discs drift. On the stat slide the disc radii grow in (`discA` 0.3 → 0.48 over 1.6 s, `discB` 0 → 0.18 from 0.5 s), so it opens on one disc.
- Everything leaves together 0.7 s before the end (0.45 s, ease `0.55, 0, 0.75, 0.2`), so the card opens and closes on the moving background. The lower third differs: its panel wipes on with `reveal` (0.75 s, ease `0.65, 0, 0.25, 1`), the type leaves first, then the panel wipes back into its tab.

## Time it to the speech

- **Chapter:** a separate 5–7 s clip at the topic change, never cutting into a sentence, or b-roll starting about 0.2 s before the chapter's first word. Under 5 s there is no time to read the dek after the index lands; cut words, not length.
- **Lower third:** starts 0.3 s before the speaker's first line after they appear, holds at least 4 s, placed where their body isn't.
- **Stat:** b-roll starting just before the number is said, so the count lands on the word.
- **Quote:** a separate card or b-roll over the line it quotes, in the speaker's or a named person's exact words.

## Building it in Tella Motion

One document per card. The background is a shape (`fill` for full frame, a `rect` for the lower-third panel) with a single `shader` effect whose `source` is the `.sksl` file. Type is live titles, rules and bars are rects, the marker is a dot plus two stroked circle paths (ring and ping). Give nodes role names (`bg`, `folio`, `title`, `chap3`, `pin`…) so the next card is a `duplicate_motion_document` and a few `setTitle`s; never change the shader per card.

The shaders share three uniforms you set: `frame`, the shape's box in canvas px (`[0, 0, 1920, 1080]` full frame, the panel's box for the lower third), since the renderer passes canvas coordinates; `time`, bound to the clock (every moving term in the code goes through `2π·time/loopSeconds`, so the last frame meets the first); `reveal` 0–1, which wipes the sheet on from the left (hold it at 1 on full-frame cards).

Uniforms that worked: **Survey** `lines` 22, `zoom` 3.2, `crosses` 0.3, `crossPx` 120, `calm` [0.26, 0.55, 0.62, 0.46] at strength 0.85 on the chapter card; on the panel `lines` 18, `zoom` 2.2, `crosses` 0, `calm` [0.36, 0.5, 1.7, 0.8] at 0.75. **Rag** `washAmount` 0.9, `grain` 0.03. **Overprint** `cell` 4 (whole numbers 3–6), `discA` [0.76, 0.62, 0.48], `discB` [0.87, 0.22, 0.18], `orbit` 0.05, `misregister` 3. Colours are RGBA arrays 0–1. Calmer: `loopSeconds` twice the card. Livelier: Survey `lines` 26, `zoom` 3.6; Overprint `cell` 3, `orbit` 0.07.

## Gotchas

- Declare every uniform the source has (`time` as `[0]`). Uniform paths are `field:common/effects/0/effect/uniforms/<name>/values/<i>`: bind `…/time/values/0` with `bindProperty {to: {time: "seconds"}}`, and key one component of a vector by index (`discA/values/2` is the radius).
- A rule draws on by keying `field:geometry/rect/rect/width` from 0.
- `setKeyframes` on a title's `blur` is refused ("keyed list"): `setCurve` a named curve and `bindProperty` the blur to it. The count-up is the title's `text` bound to a curve.
- Long mono labels wrap at their box width: shorten the words, not the size.
- Scale the marker's dot, ring and ping around their centre (`anchorX`/`anchorY` on the marker point), and key scale from 0.001 rather than 0.
- Footage in the mount: `addMedia`, then `node.patch` with `destination`, `fit: "cover"` and `sourceIn` in ticks of 1/254016000000 s, not seconds; `volume` 0 mutes.
- A lower third over a clip is a transparent document (no background shape) at the canvas size.

## Check

- One `get_filmstrip` of the document at 0.3 s, the landing (about 2.2 s), mid-hold, 0.5 s before the end, and 0 and one frame before `loopSeconds` for the seam on Survey and Rag (a difference means a term uses `time` outside the phase): contrast against the busiest background behind each line, nothing past the margins, no glyph clipped or wrapped, index labels clear of each other, type arriving in order and leaving together.
- Judge Survey and Overprint hairlines and dots only in a full-size `get_motion_frame`; small tiles and previews alias them into moiré that isn't there.
- The lower third stays clear of the speaker's face.

When you report, name the uniforms that set colour and speed (`ground`/`lineColor`/`accent`, `paper`/`wash`, `inkA`/`inkB`, `loopSeconds`) so the user can tweak them in the effect's settings.
