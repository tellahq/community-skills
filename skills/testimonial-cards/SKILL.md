---
name: testimonial-cards
description: >-
  Put social proof on screen as live, editable Tella Motion typography: one
  customer quote set large across the frame (an editorial pull-quote spread
  with the reviewer's initials as a big serif monogram), a wall of three tall
  quote cards with the featured one larger and inverted, or a full-height quote
  panel that slides in over one side of the footage. Quotes rise in line by
  line, the key phrase gets a marker that sweeps across it word by word, stars
  pop in, and the layout refits when the words are edited. Portrait-free and
  unbranded: no platform post or comment chrome. Use when asked for testimonial
  cards, review cards, customer quotes, social proof, a quote from a tweet/post
  or a comment, a highlighted review, "show what people are saying" or a wall of
  reviews.
metadata:
  title: Testimonial cards
  author: Tella
  category: Images
  image: og.jpg
  poster: gallery/cobalt-spread.webp
  preview: gallery/cobalt-spread.mp4
  prompt: When I say "our customers love it", show three customer quotes as a wall of cards and highlight "scary good" in the middle one.
---

# Testimonial cards

A customer's own words, set like a magazine pull-quote rather than a screenshot of a feed. One design system, three layouts:

- **Spread** (b-roll or a standalone clip): one quote fills the frame. A solid band down the left 30 % carries the reviewer's initials as a huge serif monogram, one letter per line, with stars, a short accent rule, name and role at its foot. The quote is set large on the rest of the frame under a big accent `“`.
- **Trio** (b-roll or a standalone clip): three tall cards edge to edge across the frame. The featured card (the one the speaker reads) is larger and inverted; the two beside it are paper cards.
- **Panel** (an overlay over footage): a full-height panel, about 36 % of the width, on the side away from the speaker. It slides in from the edge with a source line, stars, the quote and the attribution, then slides back out.

Builds on `tella-motion-design`. For many quotes riding a path or a ring, `tella-carousels` is the better tool.

## What makes it this look

- **The quote is the hero**, in a serif. No avatar, @handle or time-ago, and no like, reply or repost icons or counts, even when the quote came from a social post or a comment. The only meta is a name, a role or company, an optional source line in words ("Review · Juniper & Bean") and stars.
- **No portraits.** People are their initials: a rounded-square tile, or the monogram on the spread.
- **It fills the frame.** Spread and trio use the whole canvas; the panel runs from the top edge to the bottom, never a small floating card.
- **One accent, a marker and an inverted plate.** The key phrase gets an opaque marker under the text.
- **It ends on a held frame that keeps breathing**: a slow push on the quote or the wall, the monogram drifting. The panel slides out to clean footage.
- **All text stays live**, and the layout refits when the words change.

## Ask

Find where the speaker talks about customers, reviews or feedback, or reads a quote, then send one `ask_form`, prefilled:

- **Testimonials**, one per line as `name · role or company · quote`: from the user's message, a pasted review, a screenshot (read the words off it) or the transcript. **Never invent a testimonial, a name or a rating.** With nothing real, offer a clearly fictional demo set and say so in the report.
- **Key phrase** per quote (optional): the 2–6 words that carry the claim, ideally the ones the speaker says aloud.
- **Layout**: spread, trio or panel; and **where**: over the footage (panel), b-roll, or a standalone clip.
- **Palette** and **tone** (light or dark), or the video's own brand colours. Pick the palette nearest the video's existing graphics.
- **Stars** (0–5), only if the source has a rating. **Source line** for a panel (optional).

## Words

A testimonial is a quote, not a paragraph: one or two sentences, under ~110 characters on a spread or featured card, ~90 on a trio side card, ~140 on a panel. Never reword a customer; shorten only with `…` and the user's OK. Avoid a one-word last line: trim with their OK, or change the size by a few px. Keep a trio side card's role short (under ~24 characters) so it doesn't wrap. Use no real companies besides the user's own.

## Colour

Each palette has a light (`paper`) and a dark (`ink`) tone, and sets every role: ground, cards, the inverted plate (featured card, a dark panel, the spread band) with its own type, the accent (quote mark, stars, source line, panel edge, monogram), a marker for light surfaces and one for the plate, and initials-tile colours.

| Palette | Light: ground · card · plate · accent · marker | Dark: ground · card · plate · accent · marker |
|---|---|---|
| Vermilion (default, warm editorial) | `#F1EBE1` · `#FBF8F3` · `#1E1C26` · `#E2552C` · `#FFD45C` | `#16151C` · `#211F29` · `#F6F1E8` · `#FF7A50` · `#E2552C` |
| Cobalt (cool, technical) | `#E7EDF3` · `#F8FAFC` · `#13233B` · `#2D5BD2` · `#BBD5FF` | `#0E1829` · `#172439` · `#EEF3F9` · `#7FA6FF` · `#2D5BD2` |
| Forest (natural) | `#E9ECE2` · `#F8F9F3` · `#18291F` · `#2F7A4D` · `#BFE08A` | `#0F1913` · `#17241B` · `#F1F3EA` · `#73C893` · `#2F7A4D` |
| Plum (premium) | `#EEE5EB` · `#FBF7FA` · `#2A1530` · `#93306F` · `#F4C9DF` | `#1A0E1E` · `#26162A` · `#F7EFF4` · `#E489C0` · `#93306F` |
| Mono (newsprint) | `#EFEFED` · `#FFFFFF` · `#111111` · `#111111` · `#D6D6D2` | `#0E0E0E` · `#1B1B1B` · `#F5F5F3` · `#F5F5F3` · `#4D4D4D` |
| Sunflower (sunny) | `#FFF7E3` · `#FFFFFF` · `#FFC629` · `#C98500` · `#FFD84A` | `#19160F` · `#242017` · `#FFC629` · `#FFC629` · `#8A6400` |

- On light tones the band is the plate colour; on dark tones it is the light ground (sunflower stays yellow), so the spread inverts either way.
- The accent changes on the plate so it still reads: a paler accent on a dark plate (cobalt `#8DB1FF`, forest `#8FD3A3`, plum `#E6A0CB`), the deep accent on a light plate, white stars in mono, and black type, stars and monogram with a white marker on sunflower's yellow plate.
- The marker on the plate is the other one: the accent colour on a dark plate, the pale marker on a light one.
- Muted type (roles, unfilled stars) is a grey of the ink, around `#6F6A72` on light and `#A39E99` on dark. Tiles are solid palette colours in card order with white initials (vermilion: `#E2552C`, `#2F6B5A`, `#3C4FA0`, `#B9862B`, `#8A3B6B`; blues and teals for cobalt, greys for mono).
- To brand it, swap the accent and marker for the brand's and keep the rest; the quote must still read through the marker.

## Type and proportions (1920 × 1080; scale with the width)

- Quotes in Playfair Display 500, letter-spacing −0.005 em. Names Inter 600, roles Inter 400, the source line Inter 600 caps tracked 0.12 em in the accent. Any font from `list_motion_fonts` works if the user has one; keep a serif quote over a sans attribution.
- **Spread**: quote 84 px, line height 1.16, from 125 px right of the band to 134 px from the right edge, no quote marks in the text (the ~286 px `“` above does that). Quote mark and quote are centred vertically together: at line height 1 the mark's ink sits ~20 px below its box top and is ~75 px tall; leave ~55 px from its ink to the first line. Monogram Playfair Display 700 at ~326 px, line height 0.9, in the accent on the band, its box ~100 px from the top. Band content sits at an 81 px left margin. Foot, ending ~90 px above the bottom: 30 px stars 36 px apart, a 63 × 4 rule ~38 px below their centres, name 39, role 28 about 56 px under the name's top. 2–4 lines read best.
- **Trio**: outer margins 81, gaps 40, side cards ~520 × 713, featured ~638 × 864, all centred vertically, radius 24, soft shadow. Inside: stars at the top, the quote with curly quotes (50 px, featured 62, line height 1.22), and at the foot a hairline at 25 % opacity, the initials tile (58–64 px, radius 22 %) with name 28 and role 24. Padding ~50.
- **Panel**: full height, an 8 px accent edge on its inner side, padding 81, paper or plate colour. A content block centred vertically: source line 22 px, stars 28, quote 55 px at line height 1.2, then tile 60 with name 30 and role 26 about 54 px under the last line.
- Stars are drawn five-point paths (inner radius ~0.48 of outer), not an icon font. The marker is ~1.08 × the font size tall with rounded ends only where a line of it starts or ends.

## Motion

One calm easing for entrances, `cubicBezier(0.16, 1, 0.3, 1)`; exits ease in with `cubicBezier(0.55, 0, 0.75, 0.2)`. Nothing bounces.

- **Lines** rise 0.6 × the font size and fade in over 0.75 s, each 0.09 s after the one above.
- **Stars** pop 0 → 1.18 → 1 over 0.42 s, 60 ms apart.
- **Marker** fills word by word, ~0.13 s a word, with `cubicBezier(0.45, 0, 0.25, 1)`, carrying on across line breaks.
- **Spread**: the band wipes in from the left (scaleX, 0.8 s); the monogram rises 70 px at +0.25 s and then drifts up slowly to the end; the quote mark scales 0.6 → 1 at +0.3; lines from +0.45; stars +0.7; rule, name and role +0.8; the quote pushes 1 → 1.025 to the end.
- **Trio**: each card rises ~140 px and scales 0.94 → 1 over 0.9 s; left, right, then featured last, 0.12–0.2 s apart. Its lines and stars follow ~0.3 s later. The whole wall pushes 1 → 1.035 over the clip.
- **Panel**: slides in from beyond its edge over 0.85 s; source +0.35, stars +0.45, lines +0.5, attribution +0.9. It slides back out over 0.55 s.
- B-roll normally has no exit: it hard-cuts on the held frame.

## Time it to the speech

Work on the document's clock. The card or panel starts entering ~0.3 s before the word that introduces the quote ("one customer wrote…"); over footage, keep the entrance off a hard cut in the footage. The marker starts on the first word of the key phrase as the speaker says it, or 1–1.5 s after the lines land if they don't read it. A panel leaves when the thought ends, at least 1.5 s after the marker finishes and fully gone before its range ends.

## Building it in Tella Motion

One document per graphic: an overlay over the full canvas for the panel (no overlay intro, outro or motion blur; the document animates itself), b-roll with `add_layout` for spread and trio, or a Tella Motion clip for standalone. One `isolate: true` group per card (or panel, or band) holding its plate, stars, marker, quote and attribution, so it fades as one layer without the plate showing through. Name nodes with `meta.set` (`{name}`), the quotes clearly, so `setTitle` changes the words later; unnamed ones list as their text or "Rectangle".

- **Marker**: use the quote's own rich-text runs, not drawn rects. Split the key phrase into one run per word with a run `background` (marker colour, padding ~0.12 × the font size, rounded, `connectLines`), and reveal it word by word with a text animator on words animating `backgroundScale`/`backgroundOpacity`, ~0.13 s a word or from the speaker's word times (`delays`). It then follows edits and line breaks on its own; rebuild it only if the key phrase changes.
- **Refit**: the quote mark above a quote and the attribution under a panel quote follow its line count (`measureText` count × font size × line height) as an expression in each node's `transform.translateY`. Measurements are refused in text content and layout, and a `ref` to another node's value is refused outside a composition, so repeat the expression on each following node.
- Scale origins: x 0 for the band's wipe and the rule, each star's centre for its pop, the quote block's centre for the push.

## Gotchas (all hit while building this)

- **Don't measure a text node before it starts**: every earlier frame fails (500 on frames, "Preview render failed" on previews). So a measured quote starts at 0, and its line rise is not `setTextAnimation` (which plays when the node starts) but a text animator on lines (opacity 0, translate y) whose `expressionSelector` amount is a `timeShift` of keyframes 1 → 0 from the card's time, shifted by `textSelector` rank × −0.09 s.
- `measureText` is refused unless its text node is in the same batch or an earlier one. `measure` with `box: "lines"` gave 0 on a text node; line count × line height works.
- The quote's `addTitle` must come before patching its content with a `fontId`: it registers the font asset.
- A later `node.patch` of `common.transform` replaces the whole transform: write each node's transform once.
- No motion blur on anything with live text measurements: it re-lays the text every sub-frame and renders very slowly.
- If a marker ever has to be drawn as rects from `measureText` word boxes: compare line numbers (`floor(top / lineHeight)`), not tops, or it breaks into pills at short words; word indices skip punctuation and curly quotes; overlap each piece 2 px into the next word or a seam shows.
- `create_clip` names the new video after the clip: rename it with `update_video`.

## Check

- `get_motion_frame` on the held frame, `get_filmstrip` of the document over the whole range (card landing, marker finishing, hold), and `get_video_frame` for a panel over the footage. The quote is large with no one-word last line; the marker sits exactly behind the key phrase and fills once; lines rise in order without a jump; the attribution is clear of the quote; nothing is clipped; the held frame keeps moving; the panel clears the speaker's whole head in every frame of its range (narrow it, or use a spread as b-roll, if not) and is gone before the range ends.
- Report each quote with its time, the key phrase, where it came from, and anything fictional.
