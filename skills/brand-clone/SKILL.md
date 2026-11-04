---
name: brand-clone
description: >-
  Clone a brand from its website into a working brand kit in Tella and dress the
  user's video in it. Captures the URL with import_from_url, reads the page's
  real design system (exact colours sampled from the capture, typefaces and
  weights from the CSS mapped to the nearest Tella font, the content column and
  margins, corner radii, hairlines, edge textures, icon glyphs, the voice of the
  headline copy) and writes it down as a kit file. Then builds, from that kit: a
  kit board (the capture is sampled with eyedropper markers and its tokens laid
  out as swatches, type specimen, shapes and icons), an opener in the site's
  hero layout whose media frame grows into the footage, a lower third, a quote
  card, an end card, and text and subtitle presets. Use when asked to
  brand-clone a website, match a video to a company's or product's site, make a
  brand kit, branded titles, lower thirds, intro or end card "in our brand", or
  to make a video look like it belongs on a given website.
metadata:
  title: Brand clone
  author: Tella
  category: Editing
  image: og.jpg
  poster: gallery/kit-board.webp
  preview: gallery/kit-board.mp4
  prompt: Brand-clone https://www.tella.com and apply it to this video. I want an opener, a lower third, a quote card and an end card in its look.
---

# Brand clone

A website already has a design system: two or three exact colours in strict roles, one or two typefaces at particular weights, a content column with fixed margins, a few corner radii, a hairline colour, a decorative motif and a way of writing headlines. Read that system off the live page, write it down as a short kit (values by role), and build every graphic from the kit only. If a value didn't come from the site, it doesn't go in. This builds on `tella-title-cards` for the opener, name tag and end-card family.

## Read the site

- `import_from_url` with the URL captures the page above the fold as a 1920×1080 still. Download it: colours are sampled from its pixels.
- Fetch the HTML and its stylesheets. Read the `@font-face` families, `--font-*` variables and the font and weight on `body`, `h1` and the hero; the most used radii and border colours; the hero headline and sub-line (the voice, and the CTA label); and the logo (an inline header `<svg>`, `mask-icon`, `/logo.svg`, then rasters).
- Take colours from the capture's pixels, not the CSS: CSS defines colours the page never shows, and the page is rarely pure white. Sample the headline, the sub-line, the main button, the page and any panel.
- Measure the content column (the logo's or headline's left edge to the nav's right edge) and scale it so the column becomes the video's margins.
- Logo: use the SVG path data as path nodes, with simple parts redrawn as real shapes (a plate as a rounded rect, a dot as a circle) so they can pop in separately. A raster-only wordmark can be placed as an image, or set in the display font when it is plain type.
- Fonts: use the site's family when `list_motion_fonts` has it, at the site's weights. For a licensed face pick the nearest catalogue family by shape (neo-grotesk → Inter, geometric → DM Sans or Figtree, humanist → Source Sans 3, transitional serif → Lora, high-contrast serif → Playfair Display) and say so. Never download a font from the site. The user can upload a font they own (`create_source` kind `font`, then `add_library_item`).

## Ask once

One `ask_form`, prefilled, with the capture and the swatches as images:
- **Brand found**: the hex values by role, the font plan ("Oracle isn't in Tella: Inter 450 for headlines, Lora for quotes"), the radii and the logo. Let them correct any value.
- **Build** (all on): kit board, opener, lower third, quote card, end card, text and subtitle presets.
- **Words**: the opener's two lines and pill label, the lower third's two lines (a name and role only as the video says them, or the topic in the speaker's words), the quote (the speaker's exact words, split at a natural break), and the end card's lines and two pill labels. Never invent a claim, name, number or link.

## The tella.com kit (the example clips)

- **Colour roles**: page `#FDFCFC`, never white. Panels `#F7F7F7` behind a 2 px `#EAEAEA` hairline, cards white. Ink `#0B0A0A`, grey `#747474`, inactive icons `#9A9896`. Indigo `#4B32F6` only where the site uses it: the main button, the active icon and play glyphs. Logo plate gradient `#8279FA` → `#5B4EF7`.
- **Type**: two-tone headlines, line 1 in ink and line 2 in grey at the same size. Inter 450 stands in for the licensed Oracle (−0.02 em, line height 1.12). UI text Inter 500, quotes Lora 400 (for Source Serif 4), mono labels Roboto Mono (for Inconsolata).
- **Grid**: the site's 1304 px column becomes a 1600 px column with 160 px margins at 1920, and everything aligns to them.
- **Shape**: pills fully round, panels 32 px radius, cards 24, media 20.
- **Motif and icons**: short grey and faint lilac/pink horizontal streaks hugging the inside of panel edges, and the site's tab glyphs (play, phone, cursor, bolt) redrawn as filled 24-unit paths.
- **Voice**: sentence case, plain words. Line 1 names the thing and line 2 says what you get. No exclamation marks.
- **Sizes at 1080p**: opener and end-card headline 84 px, board header 60, quote 96, lower third 44, pills 30, labels 28–32, mono captions 24 at the smallest.

A different site should come out clearly different. The fictional second brand in the gallery uses Playfair Display 500 headlines with line 2 in vermilion `#D4472A`, DM Sans for UI, warm paper `#F3EFE6` with a cream sheet, 4 px corners everywhere including pills, a bookmark glyph instead of play, ruled lines that draw in with a vermilion margin rule, and a split hero (headline column left, footage on the sheet right). The layout, motion and timing rules stay the same.

## The pieces

All are 1920×1080 Tella Motion documents on the page colour.
- **Kit board** (its own 7.5 s clip): the capture, cropped above the site's own media (never third-party logos, customer imagery or people), fills the frame between a mono "Source tella.com" line and a tray. Eyedropper markers (a ring with the sampled colour) pop on the headline, grey line, button and page, placed just past the end of a text line so they don't cover the words, and each adds a chip (dot, name, hex) to the tray. Then the capture moves into a 780 px top-left slot of a board: two-tone header with the logo at right, five swatches, a type card (the site's headline in the clone font, the serif, the font mapping), a shape card (CTA pill and the radii) and an icon card. An indigo focus ring steps across the swatches, and a white "active tab" tile slides between the icons while each glyph turns indigo.
- **Opener** (3.2 s overlay at the clip's start): the site's hero with the video's words: logo, two-tone headline, an indigo pill with the play glyph, and the hairline panel with streaks. The footage plays in the panel's media frame (1120×630, running off the bottom), then the frame grows to full screen and hands over to the clip with no visible cut.
- **Lower third** (overlay, bottom-left on the margin, about 144 px up, 260 with captions): a white card in the card radius with hairline and soft shadow. It opens sideways from a square to fit an indigo play glyph and two-tone text, with the text matted to the card.
- **Quote card** (overlay from the quote's first word): the footage shrinks from full frame into a 700×760 rounded frame on the left. The quote sets in the serif on the right, word by word as spoken, over a hairline rule and a grey citation.
- **End card** (its own 4.5 s clip): the hairline panel with live streaks, the brand icon with its parts popping in, a centred two-tone headline, an indigo pill beside a white outline pill. The site's cursor glyph glides in and presses the main pill.

## Motion and timing

One ease-out for every entrance (bezier 0.22, 1, 0.36, 1), one ease-in-out when a frame moves between slots (0.65, 0, 0.35, 1), `easeInCubic` for exits. Nothing springs or overshoots. Text rises by word (`setTextAnimation` rise by word, about 0.55 s, 0.06 s stagger); groups fade in over 0.3 s while lifting 16–24 px.
- Kit board: markers every 0.25 s from 0.3 s; markers and tray fade at 1.4 s; the capture moves 1.55–2.3 s; header, swatches (0.07 s apart) and the three cards follow by 2.5 s; the ring and tile step every 0.85 s from about 3.2 s.
- Opener: panel and frame rise 80 px over 0–0.8 s with the headline and pill; hold to 1.85 s; then the header lifts 70 px and fades while the frame grows to full screen by 2.65 s (corner radius keyed 20 → 0) and holds to the end, so it ends on the clip's own picture.
- Lower third: card opens 0.1–0.75 s, glyph pops at 0.12 s, lines rise at 0.2 and 0.32 s; it leaves over its last 0.35 s, fading and dropping 12 px. It enters 0.1–0.2 s before the first word it labels, or as the opener ends if the opener covers that word, and lasts at least 2 s.
- Quote: footage shrinks over 0–0.7 s, label at 0.45 s, each line rises when its first word is said, the rule draws from line 1 + 0.2 s, the citation fades in after line 2.
- End card: icon pops from 0.05 s, headline at 0.25 s, pills at 0.7 and 0.8 s, cursor glides in 1.6–2.5 s, the pill dips to 0.95 and back at 2.6–3.05 s.
- Streaks flicker on held keys (opacity and x) and jitter only inward, so they never leave their panel. Ruled lines draw in left to right 0.02 s apart.

## Building in Tella Motion

Overlays are full-canvas (`add_overlay` at 0,0, 1920×1080, depth front) with the layout already on the grid inside. The opener and quote play the clip's own footage inside the document: find the source time under the overlay's first frame (playback time plus everything cut before it), set the clip's layout to fullscreen so the full-frame footage matches the clip exactly at the hand-over, and split the overlay if a cut falls inside it. Group each piece by part (header, panel, footage, pill, card) so the words and timings stay easy to change; make further lower thirds with `duplicate_motion_document`.

Gotchas:
- `cornerRadius` on a media node clips it to its destination at the moment you set it and doesn't follow a keyed destination. Round footage with a matte rect instead (`setMatte` alpha), keying `field:geometry/rect/rect/{x,y,width,height}` together with the media's `field:destination/*`, and key the corners (`field:geometry/rect/topLeft/x` … `bottomLeft/y`) to 0 wherever the frame is full screen. A matte that overshoots the canvas shows square footage edges while it moves.
- `fit: "cover"` and `sourceIn` (ticks: seconds × 254016000000) go in one `node.patch` on the media. Set its `volume` to −60 so the clip's audio plays once.
- `sourceRect` crops an image (in source px) and `field:sourceRect/*` can be keyed.
- New nodes paint on top: add the footage last in the opener or it slides under the header. To push a node back, `node.move` with `parent: ""` and an `index`.
- Groups and paths anchor at the canvas centre. Set `anchorX`/`anchorY` before keying `scale`.
- Path colours key like numbers (`color` with hex values and `hold` easing): that is how the active icon turns indigo.
- A hairline card is the line colour at full size with the fill inset 2 px on top. A gradient plate is `fx.gradientRamp`. Shadows are `shadowY`, `shadowBlur` and a low `shadowOpacity` (about 0.1).
- Roboto Mono has no "→": write the font mapping with words ("Inter 450 for Oracle").
- If a document's canvas changes after `add_overlay`, remove and re-add the overlay.
- No `generate_image`: invented imagery defeats the point.

## Presets

Save the kit so it outlives the video, named after the brand: `save_text_preset` "<Brand> · Title" (display font and weight, ink, no background, left), "<Brand> · Label" (UI 500, ink on white) and "<Brand> · Pill" (UI 500, on-accent on the accent, squircle), and `save_subtitle_preset` "<Brand> captions" (backdrop in the page colour at `F2` alpha, ink text, accent word highlight, UI font 500 at 52, one chunked line near the bottom). Captions draw over overlays, so keep them off the opener and quote card, and cut false starts first.

## Check

Besides the usual checks: the kit board at 1.3 s (markers beside the words, not on them), the opener mid-hold (everything on the margin) and mid-grow (rounded corners, no square footage edge), the lower third (even padding, nothing outside the card), and a filmstrip across the opener's hand-over and the quote's start (no jump between the overlay's footage and the clip, no streak outside its panel). Report the kit (hex by role, font mapping, radii), each graphic with its time, and the preset names.
