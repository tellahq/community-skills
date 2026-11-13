---
name: screenshot-wall
description: >-
  Make a screenshot wall in Tella: a tilted 3D grid of product screenshots or
  images that drifts slowly across the frame with real perspective and depth of
  field (sharp in the middle, soft toward the far and near edges, fading into the
  background). Options: rows sliding in alternate directions, a headline over it,
  and one screenshot that lifts off the wall and flies forward to fill the frame
  or land as a framed card. Built as an editable Tella Motion clip, b-roll or
  overlay from the user's uploads, pages captured with import_from_url or
  generated screens. 16:9 or 9:16. Use when asked for a screenshot wall, an image
  or photo wall, a 3D wall or grid of screens, a tilted grid, a "look at
  everything we shipped" shot, a recap or launch montage of screenshots, or a
  social grid loop.
metadata:
  title: Screenshot wall
  author: Tella
  category: UI & apps
  image: og.jpg
  poster: gallery/recap-headline.webp
  preview: gallery/recap-headline.mp4
  prompt: Open my launch video with a screenshot wall of these six screens, then have the dashboard fly forward to fill the frame as I say "meet the new dashboard".
---

# Screenshot wall

Many screens at once, on a wall leaning away from the camera. The wall slides slowly sideways, the middle row is sharp, the rows above and below go soft, and the far edge fades into the background, so it reads like a camera move rather than a template. It says "there's a lot here". Optionally one screenshot lifts off the wall, turns flat and flies forward. Use it for the hook or closing beat of a launch, or a "this year we shipped" recap.

Builds on `tella-motion-design` (load it first). For a carousel that lands on one card after another use `tella-carousels`; to lift pieces out of one screenshot use `tella-ui-parallax`.

## Ask first

After reading the video, ask once, with your guesses filled in:
- **Images** (4–12): uploads, public pages to capture, or generated product screens (say generated text is invented).
- **Hero**: none, or which image flies forward, and whether it fills the frame (cut into the real product next) or lands as a framed card with a caption.
- **Words** (optional): a headline over the wall or a caption under the landed card, at most seven words, from the user or the speaker. Never invent a name or claim.
- **Look**: Dark (`#0A0C16`, indigo glow), Light (`#F3F0EA`, soft tile shadows), or the brand's colour.
- **Where**: its own clip, b-roll over a stretch of speech, or a background behind a title.

## Images

- Uploads: `create_source`. Pages: `import_from_url` with `video: false`; look at each capture and drop ones showing other companies' logos, cookie banners, real people or an empty page.
- Generated screens: one `generate_image` per screen (flat front-on UI, no device frame, no real logos, legible text). Name any people in the prompt with invented names, and read the result for real brand names to crop out.
- Under 6 images, add 16:9 crops of them (`sourceRect` on the tile) so the wall doesn't look repeated.
- Screens 16:9 and 1600 px wide or more. The hero is shown full frame, so it must be sharp.

## The look

- **Wall pose**: perspective 1500–1800, screen tilt `rotation` ±12–20°, lean-back `rotateX` 30–38°. No `rotateY`, so every row stays at one depth.
- **Tiles**: 16:9, about 520–540 px wide in 16:9 (480 in 9:16), 30–40 px gap, radius 12–14, odd rows offset by half a tile like brickwork. The plane is much wider and taller than the frame.
- **Depth of field**: blur per row by distance from the focal row, about 0, 1.5, 4, 7, 10 px.
- **Fog**: gradients of the background colour over the far top (380–520 px) and near bottom (220–420 px, 55–75% opaque), so the wall fades out instead of ending.
- **Background**: a solid fill plus, on dark looks, a soft radial glow in the accent at 0.2–0.45. Tile shadows only on light looks.
- **Titles**: Inter 800 headline (about 136 px in 16:9, 84 in 9:16) and a 500–600 subline. Over a light wall, put a soft pool of the background colour under them and move the sharp row below the text.

## Motion

- The plane drifts 360–620 px sideways, linear, over the whole clip; for a social-grid feel, odd rows slide the other way. The whole wall pushes in from scale 1 to 1.06.
- Needs at least 4 s of drift to read as motion; 6–8 s total.
- **Hero fly**: the hero is a separate image that starts exactly where its tile is at take-off (drifted and pushed). Over 1.3 s with easing `{x1: 0.7, y1: 0, x2: 0.2, y2: 1}` it untilts (rotation and rotateX to 0), grows to its end box (full frame, or a card with 60 px margins and radius 28) and loses its corner radius if full frame. Its tile hides at take-off, and the wall dims to brightness 0.3–0.35. After landing it grows slowly to about 1.02–1.04.
- Titles fade in and rise about 28 px over 0.7–0.9 s. A caption under a landed card starts 0.2 s before the landing, so they read as one move.

## Build

One Tella Motion document (`create_motion_document`, with `videoId` for b-roll or an overlay). Paint order, back to front: background and glow, the tiles grouped per row (`row0`, `row1`…), the rows grouped as the `plane` (drift), the plane inside a `wall` group that carries the 3D pose and the push, then the fog, the hero and the titles. Keep tiles as `addMedia` with `fit: "fill"` so the user can swap a screenshot later. A 16:9 wall is about 37 tiles.

## Time and place

- Take off 0.3 s before the word that names the hero, so it lands as the sentence finishes. Leave 2 s of drift before take-off and 1.5 s of hold after landing.
- Its own clip: `create_clip` `{type: "motion", documentId}`, then move it. B-roll: `add_layout` with Tella Motion `media` across the range, hard cuts; the wall starts already drifting, so it needs no intro. Behind a title: a full-canvas overlay with the title on top.
- After a full-frame hero, cut to the real product on the next beat: the last frame is that screenshot, flat and full screen, so the cut is invisible.

## Check

One `get_filmstrip` of the document at 0 s, mid-drift, just before take-off, mid-flight, landing and the last frame, then a `get_motion_preview`. Look for: no background past the wall's edges (the far edge fades, never a hard line); the middle row sharp; no pop or swapped image at take-off; clean edges on the hero in flight; titles clear of the sharp row.

## Gotchas (found building the examples)

- **Shadows jag a projected image.** A drop shadow on the flying hero gave it stair-stepped edges. Leave it off; tile shadows inside row groups are fine.
- **Put the hero's 3D on the image itself, not a group.** A group whose only child was the hero rendered its projection unfiltered. Set `perspective`, `rotation` and `rotateX` on the image, with its anchor at the canvas centre.
- **Group `blur` can't be keyed** ("is a keyed list"). Dim the wall with `brightness` keys instead.
- **Keying `brightness` on a group of one image made the image disappear.** Key it on the wall group.
- Groups aren't clipped to the canvas, so tiles can sit far outside the frame.
- Don't fade the whole wall in from 0 on a clip that opens a video: frame 0 must not be blank.
- Wall tiles are minified, so tiny UI text goes soft. That's fine; only the hero has to be readable.
