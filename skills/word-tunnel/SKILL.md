---
name: word-tunnel
description: >-
  Make a word tunnel in Tella Motion: a word or short phrase repeated in lanes
  on the four walls of a 3D tunnel that rushes toward the viewer, with a dark
  (or light) core at the vanishing point, then the walls open, the core swells
  and the phrase flies out of the depth to land flat in the centre, with an
  optional small kicker line under it. Speed, colours and typeface are the
  controls. Works as its own opening clip, as b-roll, or as a full-frame overlay
  whose plate opens onto the footage. Use when asked for a word tunnel, a text
  tunnel, words flying past / rushing at the camera, a 3D type tunnel, a
  manifesto or hype opener, or a kinetic-type intro that lands on one phrase.
metadata:
  title: Word tunnel
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/launch-week.webp
  preview: gallery/launch-week.mp4
  prompt: Open the video with a word tunnel of "LAUNCH WEEK" that lands on the title, dark with an orange accent, fast.
---

# Word tunnel

A short phrase repeats in three lanes on each wall of a square tunnel. The lanes stream toward the camera, the far end disappears into a soft core, and after a few seconds the walls open outward and fade while the core swells over them. The phrase then flies out of the vanishing point and lands flat and still in the centre. It is a 7–8.5 s beat for intros, manifesto lines and hype openers. Load `tella-kinetic-type` too for choosing the line.

## Ask first

Read the transcript and find the line the tunnel should land on: the title, the hook, a manifesto sentence or the launch name. Then ask once:

- **Wall phrase:** 1–3 words, at most about 16 characters, usually in capitals. Prefill it with the speaker's words.
- **Landing phrase:** usually the same, but it can pay it off ("SAY LESS" on the walls, "Say less. / Show more." landing). Never invent a claim.
- **Kicker** (optional): one small line under it, such as a name, a date or "Episode 01". Leave it empty unless the video gives one.
- **Look:** Midnight, Paper, Acid, or their brand's two colours.
- **Speed:** Cruise 1400, Rush 2400 (default) or Warp 3400 px per second along the tunnel.
- **Type:** Heavy grotesk (Archivo 800), Condensed (Oswald 700) or Editorial serif (Playfair Display 800).
- **Where:** a new opening clip (default), a full-frame overlay over the first seconds that opens onto the footage, or b-roll.

## The look

| Look | bg | ink | accent |
|---|---|---|---|
| Midnight | `#0A0A0F` | `#F4F1EA` | `#FF4B2B` |
| Paper | `#EFE8DA` | `#1A1814` | `#2D3FE0` |
| Acid | `#0B0D0A` | `#F2F2EE` | `#D7FF3A` |

- Lane colours cycle accent, ink, ink, offset by lane and wall so the accent scatters. The core is the bg colour: dark reads as depth, light as light at the end of the tunnel. With brand colours, make the bg the darkest or lightest one.
- One typeface for walls and landing phrase. The kicker is Roboto Mono 500 at 32–34 px, tracked +0.24 em, in the accent, 30–40 px under the phrase.
- **Walls:** font size 190–210, line height 1.0, three lanes at −300 / 0 / +300 px across each 900 px wall.
- **Landing phrase:** 1300–1500 px wide on a 1920 frame, never over 85 %. Archivo 900 at 176 px fits "LAUNCH WEEK"; Playfair 800 at 196 px fits two short lines; Oswald 700 at 220 px fits "THE BIG CITY".
- **Pitch** (spacing along a lane) must exceed the phrase's rendered width, or the phrase wraps inside its box. Use about 1.25 × the width: 1800 for "LAUNCH WEEK" in Archivo, 1400 for "THE BIG CITY" in Oswald, 1200 for "SAY LESS" in Playfair. Give each title a box as wide as the pitch, text centred.

## Motion

- **In (0–0.8 s):** the walls slide in from depth (−1800 → −450) with an expo-out curve `{0.16, 1, 0.3, 1}` and fade up over 0.45 s.
- **Rush:** the lanes stream toward the camera at the chosen speed, looping seamlessly. At least 2.5 s of it.
- **Open (`openAt`, 1.0 s):** the walls push back to about −2600 with a slow-in curve `{0.55, 0, 0.9, 0.6}`, hold full opacity for 0.35 s then ease-in to 0. The core scales 1 → 9 ease-in over the same second, so it swallows the walls before the phrase arrives; without it the phrase flies through busy wall text.
- **Landing (`openAt` + 0.35 s):** the phrase flies from z −9000 to 0 over 1.0 s with the expo-out curve, fading in over the first 0.25 s, then drifts slowly to +60 until the end. It lands at `openAt` + 1.35 s. The kicker fades in over 0.45 s and rises 18 px, starting 0.25 s before the landing.
- **Overlay:** the bg and core fade out from `openAt` + 0.2 s to the end of the open, revealing the footage. Give the phrase and kicker a soft shadow (about 0.55 opacity, blur 40) and fade them out over the last 0.5 s.

## Timing to speech

- Land the phrase on its spoken word: `openAt` = word start − 1.35 s, in the document's own time (for an overlay, subtract the overlay's start).
- Hold the landed phrase at least 1.5 s.
- As an opener, put a riser into the open and a hit on the landing (`list_library` sound effects). Over music, move `openAt` so the landing falls on a downbeat from `get_music_beats`. The speaker can start on the landing.
- Don't run it over a sentence the viewer needs to follow. It is a beat, not a backdrop.

## Building it in Tella Motion

Top-level nodes: `bg` (a fill), four wall groups, `fog` (the core), `hero` and `kicker`. Name them so the tunnel can be rebuilt: to change words, colours or speed, delete those nodes and rebuild in one batch rather than patching 120 titles.

- **One recipe, four rotations.** Each wall is a group with its origin at the canvas centre and a transform of `perspective` 1000, `rotateX` 90°, `translateZ` −450 (set with `node.patch` on `common.transform`). That lays a plane down as the floor; `rotate` 0 / 90 / 180 / −90 spins it round to floor / left / ceiling / right.
- **Scroll group inside each wall.** A plain 2D group rotated −90° (floor, left) or +90° (ceiling, right) about the centre, so text runs along the tunnel and reads upright on both side walls. It holds the titles: per lane, enough copies spaced one pitch apart to fill about 9000 px of depth plus one loop (10–12), each lane staggered by a third of the pitch. Negative depth is far away.
- **Speed** is the scroll group's `y` keyed linearly from 0 to 3 × pitch over 3 × pitch / speed seconds, with a loop expression (`direction: "out"`, `mode: "cycle"`). The loop distance must be a whole colour cycle (pattern length × pitch), or colours jump at the seam. Animate `y` on the inner scroll group: a wall group's own x and y move it in screen space, not along the tunnel.
- **Core:** a circle of about 520 px at the centre with a radial gradient in the bg colour, opaque to 30 % of the radius and transparent at the edge (`paint.source` gradient via `node.patch`).
- **Phrase:** a group with `perspective` 1000 around the centre holding the landing title, so it can fly in on `translateZ`.

## Check

- One `get_filmstrip` of the document at 0.3 s (walls closing in), 2 s (full rush), `openAt` + 0.5 s (opening, phrase mid-flight) and landing + 0.5 s. In the rush: one line of text per lane (two stacked lines mean the pitch is too small), side walls upright, the core hides the far mush, the four corners meet cleanly. Landed: the phrase centred with comfortable margins, the kicker just under it, nothing else on screen.
- A second `get_filmstrip` a frame apart (1/30 s) either side of 3 × pitch / speed: the loop seam must not jump.
- For an overlay, a video frame just after the open: the footage shows and the phrase reads over it.
- Report the phrase, look, speed, where it sits and when the phrase lands.

## Gotchas

- **No motion blur.** `setMotionBlur` on a 3D wall clips the render to a small centre square, and on the scroll group it blanks the frame. At 30 fps the rush reads fine without it.
- **`translateZ` keys only as `field:common/transform/translateZ`.** It isn't an editor property. `rotateX`, `rotateY` and `perspective` are ordinary properties.
- **Batch size.** The tunnel is 165–200 commands, close to a batch's limit: keep three lanes and at most 12 titles per lane, or build walls first, then core and phrase.
- **Long phrases.** Above about 16 characters, drop the wall size to 150 and raise the pitch, or the walls turn into texture. Put a long line in the landing phrase and keep the walls to its key words.
- **Square tunnel.** On 16:9 the side walls take more of the frame than floor and ceiling. That is intended.
- **Portrait is untested.** Only 16:9 has been checked. For 9:16, start from a tunnel half-width of 300, wall size 150 and a landing phrase that fits 900 px, and check every frame.

## Variations

- **Calmer manifesto:** Paper, Cruise, serif, a two-line landing.
- **Hype:** Warp, condensed type, the Acid accent.
- **Accent as payoff:** all-ink walls with only the landing phrase in the accent.
