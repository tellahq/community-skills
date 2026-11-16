---
name: word-tunnel
description: >-
  Make a word tunnel in Tella Motion: a word or short phrase repeated in lanes
  on the four walls of a 3D tunnel that rushes toward the viewer, with a dark
  (or light) core at the vanishing point. Speed, colours and typeface are the
  controls. Works as its own clip or as b-roll. Use when asked for a word
  tunnel, a text tunnel, words flying past / rushing at the camera, a 3D type
  tunnel, or a kinetic-type manifesto or hype beat.
metadata:
  title: Word tunnel
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/launch-week.webp
  preview: gallery/launch-week.mp4
  prompt: Open the video with a fast word tunnel of "LAUNCH WEEK", dark with an orange accent.
---

# Word tunnel

A short phrase repeats in three lanes on each wall of a square tunnel. The lanes stream toward the camera and the far end disappears into a soft core. That is the whole graphic: no title card, no landing. It is a 3–6 s beat for openers, manifesto lines, hype moments and section breaks. Load `tella-kinetic-type` too for choosing the phrase.

## Ask first

Read the transcript and find the phrase for the walls: the title, the hook, a manifesto line or the launch name. Then ask once:

- **Phrase:** 1–3 words, at most about 16 characters, usually in capitals. Prefill it with the speaker's words. Never invent a claim.
- **Look:** Midnight, Paper, Acid, or their brand's two colours.
- **Speed:** Cruise 1400, Rush 2400 (default) or Warp 3400 px per second along the tunnel.
- **Type:** Heavy grotesk (Archivo 800), Condensed (Oswald 700) or Editorial serif (Playfair Display 800).
- **Where:** a new opening clip (default), a clip between sections, or b-roll over a stretch of the video.

## The look

| Look | bg | ink | accent |
|---|---|---|---|
| Midnight | `#0A0A0F` | `#F4F1EA` | `#FF4B2B` |
| Paper | `#EFE8DA` | `#1A1814` | `#2D3FE0` |
| Acid | `#0B0D0A` | `#F2F2EE` | `#D7FF3A` |

- Lane colours cycle accent, ink, ink, offset by lane and wall so the accent scatters. The core is the bg colour: dark reads as depth, light as light at the end of the tunnel. With brand colours, make the bg the darkest or lightest one.
- **Walls:** font size 190–210, line height 1.0, three lanes at −300 / 0 / +300 px across each 900 px wall.
- **Pitch** (spacing along a lane) must exceed the phrase's rendered width, or the phrase wraps inside its box. Use about 1.25 × the width: 1800 for "LAUNCH WEEK" in Archivo, 1400 for "THE BIG CITY" in Oswald, 1200 for "SAY LESS" in Playfair. Give each title a box as wide as the pitch, text centred.

## Motion

- **In (0–0.8 s):** the walls slide in from depth (−1800 → −450) with an expo-out curve `{0.16, 1, 0.3, 1}` and fade up over 0.45 s.
- **Rush:** the lanes stream toward the camera at the chosen speed, looping seamlessly, for the rest of the clip. At least 2.5 s of it.
- **Out:** cut straight to the next clip, or fade the walls to the bg colour over the last 0.3 s when the next clip starts on the same colour.

## Timing to speech

- Start the tunnel on the phrase's spoken word, or just before it, so the walls are full when it is said.
- As an opener, put a whoosh or riser under the slide-in (`list_library` sound effects). Over music, start it and cut out on downbeats from `get_music_beats`.
- Don't run it over a sentence the viewer needs to follow. It is a beat, not a backdrop.

## Building it in Tella Motion

Top-level nodes: `bg` (a fill), four wall groups and `fog` (the core). Name them so the tunnel can be rebuilt: to change words, colours or speed, delete those nodes and rebuild in one batch rather than patching 120 titles.

- **One recipe, four rotations.** Each wall is a group with its origin at the canvas centre and a transform of `perspective` 1000, `rotateX` 90°, `translateZ` −450 (set with `node.patch` on `common.transform`). That lays a plane down as the floor; `rotate` 0 / 90 / 180 / −90 spins it round to floor / left / ceiling / right.
- **Scroll group inside each wall.** A plain 2D group rotated −90° (floor, left) or +90° (ceiling, right) about the centre, so text runs along the tunnel and reads upright on both side walls. It holds the titles: per lane, enough copies spaced one pitch apart to fill about 9000 px of depth plus one loop (10–12), each lane staggered by a third of the pitch. Negative depth is far away.
- **Speed** is the scroll group's `y` keyed linearly from 0 to 3 × pitch over 3 × pitch / speed seconds, with a loop expression (`direction: "out"`, `mode: "cycle"`). The loop distance must be a whole colour cycle (pattern length × pitch), or colours jump at the seam. Animate `y` on the inner scroll group: a wall group's own x and y move it in screen space, not along the tunnel.
- **Core:** a circle of about 520 px at the centre with a radial gradient in the bg colour, opaque to 30 % of the radius and transparent at the edge (`paint.source` gradient via `node.patch`). It hides the far end, where the text turns to mush.

## Check

- One `get_filmstrip` of the document at 0.3 s (walls closing in), 2 s (full rush) and 0.2 s before the end. In the rush: one line of text per lane (two stacked lines mean the pitch is too small), side walls upright, the core hides the far mush, the four corners meet cleanly.
- A second `get_filmstrip` a frame apart (1/30 s) either side of 3 × pitch / speed: the loop seam must not jump.
- Report the phrase, look, speed, where it sits and how long it runs.

## Gotchas

- **No motion blur.** `setMotionBlur` on a 3D wall clips the render to a small centre square, and on the scroll group it blanks the frame. At 30 fps the rush reads fine without it.
- **`translateZ` keys only as `field:common/transform/translateZ`.** It isn't an editor property. `rotateX`, `rotateY` and `perspective` are ordinary properties.
- **Batch size.** The tunnel is up to about 200 commands, close to a batch's limit: keep three lanes and at most 12 titles per lane, or build two walls per batch, then the core.
- **Long phrases.** Above about 16 characters, drop the wall size to 150 and raise the pitch, or the walls turn into texture. Keep the walls to the line's key words.
- **Square tunnel.** On 16:9 the side walls take more of the frame than floor and ceiling. That is intended.
- **Portrait is untested.** Only 16:9 has been checked. For 9:16, start from a tunnel half-width of 300 and wall size 150, and check every frame.

## Variations

- **Calmer manifesto:** Paper, Cruise, serif.
- **Hype:** Warp, condensed type, the Acid accent.
- **One accent lane:** all-ink walls, with the accent kept for one lane on one wall.
