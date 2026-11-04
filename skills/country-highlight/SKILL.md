---
name: country-highlight
description: >-
  Build a clean map moment in Tella Motion: the camera flies from the whole
  globe down to one or more countries, fills them in the brand colour, and
  lands a label and a stat beside them ("Launching in Japan", "12,400 on the
  waitlist"). Two looks: flat (crisp vector, light or dark) and watercolour
  paper (pigment wash, soft edges, paper grain, handwritten labels). Country
  outlines, borders and the globe flight come from Tella's get_map_data.
  Use when asked for a country highlight, a map zoom, "zoom into <country>",
  a launch or expansion map, a "we're now in…" or "shipping to…" map, a
  where-our-customers-are map, or a watercolour map.
metadata:
  title: Country highlight
  author: Tella
  category: Diagrams
  image: og.jpg
  poster: gallery/flat-launch-japan.webp
  preview: gallery/flat-launch-japan.mp4
  prompt: When I say we're launching in Japan, zoom the world map into Japan, fill it in our brand colour and show "12,400 people on the waitlist".
---

# Country highlight

A full-frame map that starts on the whole globe, flies in to the countries the speaker names, washes them in a brand colour, then sets a short headline and one number beside them. One beat, 4–10 s, for the moment someone says "we're now in…". The zoom follows **tella-camera-moves**, the headline and stat **tella-data-callouts**, labels and leaders **tella-explainer-graphics**.

## Ask first

Read the transcript with word timings and find where the place and the number are said. Then ask once, prefilled from what you heard:

- **Countries**: one or more (get_map_data matches them by English `name`; its `id` is the ISO numeric code, so keep alpha-3 codes such as JPN for your node ids).
- **Brand colour**: one hex; offer the one from their logo or slides if you can see it.
- **Look**: flat light, flat dark or watercolour paper.
- **Headline** (2–5 words) and an optional **stat** (a number plus a short line). Never invent a number; with none, leave the stat out. If they want a stat but you can't ask, use a checkable public fact about the place ("13 provinces and territories") and say so.
- **City pin** (flat only, optional).
- **Where it plays**: its own full-frame clip (default) or b-roll over the speaker, and which words it lands on.

Use their brand name or none; never draw real logos.

## The map data

Get it from `get_map_data`; never download or project map data yourself. It returns Natural Earth countries (with names, bounds and label points), land, water and borders as SVG path data already in your canvas's pixels, plus your markers' x, y. Three calls make the whole shot:

- **The flight**: `camera` with `layers: ['countries']` and `detail: 'low'`. Stops: the whole globe at 0 (`radius` about 0.42 × the canvas height, `center` 35–45° from the target so the globe visibly turns), then the end view's `center` and `zoom` at the landing time. Don't hold the first stop: the flight eases in, so a held start reads as a frozen first second. End the stops at the landing. Every country and the globe's `outline` come back as keys: add each as a path and pass its keys to `setPath` unchanged. Skip items whose keys are all empty (the far side). `keysPerSecond` 6 is smooth enough and keeps the result near 2 MB.
- **The hold**: a static `area: {center, zoom}` map with `projection: 'orthographic'`, the same center and zoom + log2(1 / cos(center latitude)) (the camera's last `radius`), `layers: ['land', 'countries', 'boundaries']`, `kinds: {boundaries: ['country']}`, `detail: 'medium'` (`high` for small targets such as Singapore or Malta), and the pin as a `marker`. That lines up with the globe's last key to the pixel. The default mercator map at the same zoom does not: at country zoom it is ~10 % off at the frame's edges, a visible jump.
- **Finding the end view**: first call `area: {countries: [...]}` on a canvas the size of the space the map gets (about 1250×1080 when the text takes the other side), padding ~100, and read `projection.center` and `projection.zoom`. To put that centre at x = 0.33 of a 1920 frame instead of the middle, move the centre **east** by 0.17 × 1920 px: Δlon = 326 × 360 / (512 × 2^zoom) (west for a target on the right).
- Frame the target's main part only: `countries` frames main landmasses, so French Guiana and Svalbard stay out of the framing but drawn. It can also drop islands you need (for Japan it framed Honshu and Hokkaido and cut Kyushu off the bottom): check the bounds and set the zoom from the full extent if so.
- **Continental targets** (end zoom under ~4, e.g. Mexico to Brazil): the landing still shows the globe's edge. Use the outline's last key as the hold's sea instead of a full-frame fill. Keep the view centre on the targets and set the end stop's `position` (e.g. x 580) so the text sits in open space beside the globe. Static maps are always centred, so fetch the hold at 1920×1080 and move its map group by the same x offset.
- Path data never passes through your own context: call `get_map_data` and `apply_motion_editor_commands` from one script and send the commands in batches under ~900 KB and 240 commands. Never print a result.

Place every label from the static map's numbers: the target's `labelPoint` and `bounds`, the pin marker's x, y.

## Structure in Tella Motion

- `bg` fill a shade off the sea colour (it frames the globe), then the **globe**: its outline in the sea colour and every country in the land colour, each with its `setPath` keys, lasting 0.2 s past the landing (it holds its last key). For borders, `duplicate` each country and `setPath` the copy to a border-colour stroke (the keys stay). On watercolour, group those strokes and matte them with a duplicate of the land group, or the pencil traces coasts that the flat map doesn't have. The target stays in the land colour on the globe; it fills on the flat map, after the landing.
- The **flat hold** on top, starting at the landing and fading in over 0.2 s while both are still. Started before the landing, it ghosts against the still-moving globe. In order: land, then the borders path stroked 1–1.2 px in the background colour (OpenStreetMap borders run out over the sea, so give it the land as an alpha matte), then each target as `t_<code>` in the land colour with a brand-colour copy `h_<code>` at opacity 0 for the fill.
- There is no empty-group command: `group` a first path into `hold`, then give later `addPath`s `parent: 'hold'` (they stack in call order). Anchors and scale are the properties `anchorX`, `anchorY`, `scale`.
- Keep the hold alive with a slow push of `hold`, ~2 % scale, from the end of the hand-off fade, about a point that keeps the landing's direction of travel (off the side the camera came from); pushing about the target's centre makes the camera seem to back up after it lands.
- Text, pins, pills and paper grain sit outside the map, so they don't scale.
- End view: the targets fill 0.7–0.85 of the frame's tighter side, centred at x 0.32–0.35 or 0.65–0.68, away from the text. A target that is tall in Mercator (Canada: the Arctic islands are most of its height) is framed by its height, with ~100 px above it, and the text side gets clean open sea.

## Timing

- The flight **lands** on the word that names the place and starts 2.5–3 s earlier (the globe's first stop). Under 2 s feels like a jump cut; over 3.5 s drags.
- The fill starts at the landing and runs 0.5–1 s; stagger several countries 0.25 s apart in the order they're said.
- The headline follows 0.3–0.5 s after the fill. The stat lands on the spoken number, or 0.8 s after the headline.
- Hold the finished frame at least 2 s, longer while the speaker stays on the place.
- Times are on the document clock; for b-roll starting at clip time T, subtract T from word times.

## Flat look

- **Light**: background `#EEF1F5`, land `#D4DAE2`, borders in the background colour, ink `#0F172A`, secondary `#475569`.
- **Dark**: background `#0B1220`, land `#1B2434`, text `#F8FAFC` / `#94A3B8`; give brand fills a soft glow (`dropShadow`, brand at ~33 % alpha, no offset, radius 6).
- **Fill**: key `t_<code>` colour from land to brand (easeOutCubic, 0.6 s), or `h_<code>` opacity 0→1.
- **Type**: Inter or DM Sans (`font` takes the catalog slug: `inter`, `dm-sans`). Eyebrow 28 px 600 tracked 0.18 (no smaller: 28 px is the floor at 1080p); headline 68–84 px 700–800, box ~600 px wide; stat 88–132 px 800 in the brand colour; its line 30 px secondary. Each fades in and rises 16–22 px over 0.45–0.5 s, easeOutCubic, staggered ~0.15 s.
- **Pin**: a 24 px white circle with a 12 px ink dot, a white ring pulsing scale 1→3.4 and opacity 0.9→0 (three times), and a 2 px leader to the text drawn on.
- **Several countries**: a pill per country (54 px tall, fully rounded, dark `#0F1A2BF2` on the dark look) with a brand dot, the name (24 px 600) and its count right-aligned, staggered with the fills.

## Watercolour paper look

- Paper `#F2EBDD`, land `#DCD3C1`, borders `#C3B59C` at 0.9 px so they read as pencil.
- **Wash** on each `h_<code>`: blend mode multiply, `fx.turbulentDisplace` first in the stack (amount 40, size 40, complexity 3), then an inner `dropShadow` `#12395E66` radius 4.
- **Pooled edge**: duplicate `h_` to `e_<code>` before the inner shadow; make it a 6-unit stroke in a darker shade, multiply, `blur` 4.
- **Reveal**, ~1 s easeOutCubic, staggered 0.25 s: opacity 0→0.7 on `h_` and 0→0.28 on `e_`, while the turbulent amount settles 40→6 (`field:common/effects/0/effect/uniforms/amount/values/0`).
- **Paper grain**: two full-frame white `fill` layers above the map, multiply, each with `fx.fractalNoise` (complexity 6, contrast 1.4, brightness 0.1): scale 420 at opacity 0.1 and scale 5 at opacity 0.06.
- **Text area**: a paper-coloured rect off the text side, `blur` 90, opacity 0→0.9, quiets the map under the text.
- **Type**: Playfair Display 700 headline (~76 px, ink `#1E2A36`); Caveat 700 for country names (40 px, paper-white `#FBF7EE` on the wash, ink when out at sea) and the stat (~84 px, brand colour) with a hand-drawn curved underline drawn on; Lora 28 px for the supporting line.
- If a wash looks heavy or grey, lower its opacity before changing the colour; brand colours darken under multiply.

## Labels

Put a label inside its country only if the country is at least 1.4× the label's width; otherwise put it in open sea beside it. One headline, one number. Keep everything inside a 96 px margin and off busy coastlines.

## Gotchas

- A group's anchor defaults to the canvas centre: set `anchorX`/`anchorY` on `hold` before keying its scale.
- The globe's and the flat map's coordinates are already the canvas's: add them at x, y 0 and scale 1, never inside a moved or scaled group (except the exact `position` offset above), or the hand-off jumps.
- A `labelPoint` can land on a border in a long, thin country (Norway's sat on the Swedish border): move the label into the widest part.
- A title's `x`/`y` is an offset from its box: key a rise as 18→0, not as an absolute position.
- `trimPath` `end` can't be keyed. Patch `geometry.end` to 0, then key `field:geometry/end`.
- `addShape` takes `shape: fill | rect | circle` (not "rectangle").
- `duplicate` plus `node.patch` reuses a path's data for free: use it for highlights, borders and edges; never send a path twice.
- `get_motion_preview` renders 5 s unless you pass `durationMs`; pass the full length.

## Check with frames

- `get_filmstrip` with `documentId` at the globe, mid-flight, just before and just after the hand-off to the flat map, the landing and the hold: the target framed, fills in order, no label on a coastline, no jump at the hand-off.
- `get_motion_frame` (width 1920) at the hold, then a full-length low-fps `get_motion_preview` (pass `durationMs`): one smooth flight, borders thin, the wash settling.
- Once it's in the video, `get_video_frame` at the landing, the stat and the last second. The full hold is the poster moment.
