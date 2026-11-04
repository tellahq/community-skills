---
name: route-map
description: >-
  Animate a stylised route map in Tella: a vector map drawn from Tella's
  get_map_data (land, borders, lakes, in the canvas's pixels), a route that
  draws itself between cities, pins that drop with
  name cards, a plane or glowing dot that travels the route, and a camera
  that gently follows it and pulls back to the whole journey at the end.
  Each city lands on the word that names it. Four looks (night, paper atlas,
  light, dot matrix), chains (A → B → C) or spokes from one HQ, as
  full-screen b-roll, a Tella Motion clip or a map card over footage. Use
  when asked for a route map, a travel or flight map, a shipping or delivery
  route, a "we expanded to X" or new-offices map, an animated map with pins,
  or a plane flying between cities.
metadata:
  title: Route map
  author: Tella
  category: Diagrams
  image: og.jpg
  poster: gallery/expansion-spokes.webp
  preview: gallery/expansion-spokes.mp4
  prompt: When I list the cities on our tour, show a route map that flies between them with a pin and label for each one.
---
# Route map

A flat, designed map, not a satellite view. Land is one or two quiet tones. One route colour carries the story. Pins drop as each city is named, and a small card gives the city and one short fact. A plane or dot flies each leg along a curved arc while the line draws behind it. The camera leans in on the current leg and pulls back at the end to show the whole route. Builds on `tella-motion-design`. Borrow `tella-camera-moves`' rule: one move at a time, then a hold.

## Ask

Find the stretch where the places are named and note when each city's word starts. Then ask everything at once, prefilled from the transcript:

- **Stops** in travel order, as `City — short fact` ("Austin — HQ since 2019"). The fact is optional, at most three words, and only from the speaker. If a name is ambiguous (Portland, Cambridge, San José), ask which one. Look up the lat/lon yourself.
- **Shape**: a chain (A → B → C, a trip or delivery) or spokes from the first stop (HQ to new markets).
- **Look** (below), **traveller** (plane, dot or none), and **where**: full screen over the speaker (b-roll, the default), a map card beside the speaker, or its own clip.
- An optional small-caps **kicker** ("Pebblewren Studio · Opening tour"). Leave it out if nothing the speaker says fits.

Four to six stops is the most that reads. With more, the route becomes the point instead of the cities.

## The map data

One static `get_map_data` call gives the whole map in canvas pixels; never download or project map data yourself.

- **Area**: `points` with the stops, and `padding` of about the widest card plus 100 px, since cards keep their screen size (a 30% pad on the stops alone pushes an edge city's side card off the frame). `canvas` is the document's size, or the card's.
- **Projection**: `equirectangular` or `naturalEarth` for world and continent views, `mercator` for a country or a few hundred km.
- **Layers**: `land`, `boundaries` (`kinds` country only, matted to the land), `water` with only `lake` so the Great Lakes are water (drawn in the sea colour over the land), and `graticule` for the night and atlas looks.
- **Markers**: one per stop. Pins, cards and the legs' end points all come from their x, y.
- `detail: 'medium'` holds up to the 1.5× lean-in; `high` only for a view of a few hundred km, and drop back to `medium` if an item's path is over `addPath`'s 100 k characters.
- Keep path data out of your own context: call `get_map_data` and `apply_motion_editor_commands` from one script and never print a result. Send batches under ~900 KB and 240 commands; a `group` must come after the nodes it gathers.

## Looks

| Look | Sea | Land | Route / pin | Card (bg / name / sub) | Extras |
|---|---|---|---|---|---|
| Night | `#0B1322` | `#1C2B44`, borders `#2C3E5C` | `#FFB547`, glow | `#FFFFFF` / `#0B1322` / `#6A7890` | white plane, 15° graticule (white at 5%), vignette 0.35 |
| Paper atlas | `#D5E2E4` | `#F4EEE1`, coast `#B7AB91` 1.2 px, borders `#CDBFA4` | `#D2452B`, dashed 16/11 | `#1F2A30` / `#FFFFFF` / `#C9B79A` | teardrop pins, 5° graticule `#7F99A1` at 22%, grain 0.06 |
| Light | `#F3F4F7` | `#DEE2E9`, borders in the sea colour | `#4F46E5` | `#FFFFFF` / `#111827` / `#4F46E5` | indigo dot traveller |
| Dot matrix | `#0A0E13` | dots `#2A3846` (r 3.1 on a 13 px grid) | `#3EE6C1`, glow | `#212E3A` / `#FFFFFF` / `#3EE6C1` | white dot, vignette 0.4 |

The kickers are `#8C9AB3`, `#5E6F74`, `#6B7280` and `#6F8091`, in table order. To brand the map, use the brand accent for the route and pins only and keep the land neutral. Delivery and field-team stories suit the atlas look with a dot. Global launches suit night with a plane, or light with spokes.

The atlas coastline is the land paths again as strokes. Dot-matrix land is one path of circles at the grid points inside `land` (whole dots read better at the coast than a dot grid matted to the land).

These sizes are for 1080p. The route is 4 px (3.5 px for dot matrix) with round caps. The glow is a `dropShadow` in the route colour at about 45%, radius 9, no offset. A dot pin is a white disc of radius 11 with an accent dot of radius 7. A teardrop pin is 34 px tall, with a head of radius 13 and a white eye. The dot traveller is an accent dot of radius 9 in a white ring of radius 13, with a soft shadow and a faint accent halo (radius 22, about 16%), so it reads as the moving thing and not as another pin.

Each card has the name in Inter 600 at 28 px and the sub-label in Inter 600 at 17 px, in caps with 0.08 em tracking, 18/12 px padding, a 10 px radius and a soft shadow, sized to its text, never a fixed width: one left-aligned title with the two lines as runs and a `lineBackground` with `coverBlock` hugs them, so there is nothing to measure. Put it 22 px from the pin, on the side no route leaves from.

The kicker is Inter 600, 22 px caps with 0.14 em tracking, 72/64 px from the top left, outside the camera group. In a chain a border or coast can slide right through it mid-zoom: check frames there, and leave it out if that happens.

## Motion

- **Routes**: one cubic Bézier per leg between the stops' markers, control points at ⅓ and ⅔ of the straight line pushed north by about 22% of its length (bend it the other way to keep it off a label). It draws with a `trimPath` `end` 0 → 1 from departure to arrival, eased `cubicBezier(0.45, 0, 0.25, 1)`. Night, light and dot matrix also show a faint dotted ghost of the leg ahead (dashes 2/9, 20–30% opacity), fading in 0.6 s before departure.
- **Traveller**: one node per leg, drawn around 0,0, on a two-key `setMotionPath` whose tangents are that Bézier's handles, with the trim's ease so it rides the tip of the line. The plane is a ~48 px silhouette pointing +x with `autoOrient` and a soft shadow. Fade it in over the leg's first 0.22 s and out over its last 0.22 s, so it comes out of one pin and sinks into the next.
- **Pins**: each falls 46 px over 0.42 s with an ease-in, fading in over the first 0.2 s, and lands exactly on its word. On landing it squashes 1 → 1.12 → 1 over 0.32 s, and a ring pulses out to 3.4× while fading over 1 s. The card fades in and slides 12 px out from the pin side, from 0.05 to 0.45 s after landing.
- **Camera**: everything on the map in one `cam` group, keyed on `x`, `y` and `scale`; pins and travellers get the inverse scale on the same keys so they keep their screen size.
  - Chain: start on the overview, frame each leg (up to 1.5×) leaning about 45% toward the traveller, and pull back to 1× 0.6 s after the last arrival.
  - Spokes and cards: one slow push to about 1.07× across the whole graphic.
  - Never show the map edge, and keep every landed card at least 28 px inside the frame, zooming out if you must (a cross-continent chain ends up about 1.5× on the first leg, 1.3× on the last).
  - What works: frame keys at each departure and arrival (each already including the card that lands at the end of that leg), a hold at 0.35 s and 0.6 s after the last arrival, and the pull-back done about 1.2 s later. Interpolate with a monotone spline that has zero slope at the holds and write the samples every 0.1 s with linear easing, clamping the centre at every sample, not only at the keys, because cards drift out of frame between keys. `continuous` easing through two equal hold keys overshoots.

## Timing to speech

- A pin lands on the first syllable of its city. A leg takes up to 2.4 s and leaves at least 0.45 s after the previous pin lands. A flight shorter than about 0.9 s doesn't read, so cities named less than about 1.4 s apart share a stop ("Lisbon & Porto"), or use spokes with overlapping legs.
- Start the graphic 0.6 s before the first city and hold the finished route for at least 2 s; it leaves when the thought ends. B-roll cuts in and out with no transition.
- Times inside the document are the word's time minus the time the document starts.

## Where it plays

- **B-roll**: a document at the video's size, made with `videoId`.
- **Own clip**: a 1920×1080 document without `videoId`, then `create_clip` `type: 'motion'` with its `documentId`; the new video is named after the document, so rename it with `update_video`.
- **Card**: about 880×580 on 1080p, every size scaled by about 0.95 (labels about 27 px tall). A radius-22 rect inset from the canvas edge so its shadow has room, with the `cam` group matted to a same-size rect, placed as an overlay in the empty side of the frame. It slides up 8% on a soft ease-out and fades out. It failed the full-size preview (`preview_render_failed` at 1280 px / 30 fps, fine at 640 px / 10 fps), so preview it at full size and fall back to b-roll if it fails.
- Name the nodes and groups (`Pin London`, `Camera`). Group each pin as its pulse ring, its drop group (head and eye) and its card, with every group's anchor on the pin's point.

## Gotchas found building this

- **`addTitle`, `addShape` and `addPath` default to 3 s.** Set the canvas duration and pass `duration` on every node, or the map vanishes at 3 s.
- **Set `anchorX`/`anchorY` on every group you scale.** A group of paths anchors on the canvas centre, so a traveller with the inverse scale drifts off its line.
- **Only the first path effect on a node applies**, so `trimPath` and `dashPath` don't combine. For the atlas dashed route, draw the dashes into the geometry (one subpath per dash) so `trimPath` alone reveals them, or matte the dashed path with a trimmed solid one.
- **Keying the trim**: if `setKeyframes` on `field:common/effects/0/effect/end` refuses with "keyed list", write the keys (and opacity keys) with `node.patch` on the effect, keyed by its `effectId`, in ticks. Commands that rewrite the effect stack fail after that patch, so add every effect first and patch the keys last.
- To change the map, rebuild it: remove every node in one call and add the new ones, instead of patching nodes.
- If the canvas size changes, remove the overlay and add it again; it keeps the old aspect.

## Check

- One `get_filmstrip` of the document at `timesMs` as the first pin lands, mid-leg, just after each arrival and on the final overview, plus two of those as 1920-wide `get_motion_frame`s. Every card is fully inside the frame and clear of other cards, the kicker and routes leaving its pin; each route meets its pin and the traveller stays on the line's tip; text is at least 26 px tall; no map edge or empty band of sea shows at any zoom.
- Filmstrips at `intervalMs` 100–200 over each camera move: the camera is smooth with no jump between legs, the pins land on time and nothing pops.
- Once placed, `get_video_frame` at the poster moment, 960 or 1280 wide (a full 1920 frame right after an edit sometimes times out).
- Usual fixes: move a label to the other side, bend a leg the other way, widen the view, lower the maximum zoom, or use a single push for small cards.
- Portrait: a view taller than wide, labels left or right of north–south routes, and check those frames closely (the examples are all landscape).
- Report each stop's time, the look and where it plays.
