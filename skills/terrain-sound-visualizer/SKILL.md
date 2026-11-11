---
name: terrain-sound-visualizer
description: >-
  Make a synthwave sound visualizer in Tella Motion. A wireframe landscape
  rolls toward the camera under a starry violet sky, its hills rising and
  falling with the audio (the video's own voice or music, a curated Tella
  track, or an attached song), with a glowing horizon and a big title that
  drifts in above it. It is a live SkSL shader fed by level curves read from
  get_audio_levels or built from get_music_beats. Use it as its own clip, an
  intro card or b-roll over a stretch of the video. Use when asked for a
  terrain or landscape visualizer, a synthwave, retrowave or outrun
  background, a wireframe grid landscape, an audio-reactive or beat-reactive
  title card, visuals that move to the music, or a music visualizer with a
  title.
metadata:
  title: Terrain sound visualizer
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/terrain-night-shift.webp
  preview: gallery/terrain-night-shift.mp4
  prompt: Make a 10 second synthwave terrain visualizer for our background music with the title "Orbit Hours" glowing above the horizon.
---

# Terrain sound visualizer

A hidden-line wireframe landscape flies toward the camera. Each row of hills is raised by the sound at the moment it appears on the horizon and keeps that height as it rolls closer, so the track's shape passes underneath; the horizon glow brightens with the level, stars twinkle above it, and one big title floats in the sky. It is a full-frame, opaque picture: its own clip, an intro card, or b-roll over a stretch of the video. Builds on `tella-motion-design` (timing, one look, every graphic has an exit) and `tella-title-cards` for the type; `tella-audio-sync` for beat placement.

## Ask once

Work out yourself, never ask: whether the video has speech (`get_transcript`) or background music (`get_video` `backgroundMusic`), the song attached to the message if there is one, brand colours from the user's message or the video's existing graphics, and a title suggestion from the video's name or the user's message. Then one `ask_form`, every field prefilled, so the user can just submit:

1. **Sound** (required, pick): "The video's own audio" (default when it has speech or music), "A Tella track", "The song I attached" (default when a song is attached).
2. **Tella track** (pick, used only with "A Tella track"): up to 12 from `list_library` scope `default`, type `music`, beat-driven ones first. Prefill `Modern Tech Pulse` (tested: 120 bpm, beat confidence 0.92, quiet until its drop on the 17.032 s downbeat).
3. **Title** (optional, text): at most 16 characters, one line, 1–3 words; prefilled from the video's name. Empty means no type, just the landscape.
4. **Colours** (required, pick, each option with a small swatch picture): Violet and cyan (default), Sunset, Emerald, Ice, Brand colours (from the message or the video).
5. **Start** (number, seconds): where the sound range begins. For the video's audio, on its timeline: 0 or the stretch the user named. For a Tella track or a song, the offset into the track: prefill a downbeat where it gets loud (17.032 for Modern Tech Pulse), else 0.
6. **Length** (slider 4–30 s, default 10).
7. **Where** (required, pick): "Its own clip" (default; a new video, nothing of theirs changes), "Intro card at the start of this video", "B-roll over this stretch" (only with the video's own audio: the clip's sound keeps playing under it, so a track or song would drive hills nobody hears). If the user picks b-roll with a track or a song, build it with the video's own audio and say so in the plan.

Media: the only media is the sound. A song comes from the message's attachments first, then the video's own library (`list_library` scope `video`); if they picked "The song I attached" and there is none, `ask_question` "Attach the song (MP3, WAV or M4A) to the chat", suggested answers "Use a Tella track instead" / "Use the video's own audio". Never use a teammate's video or recording that wasn't offered, and never invent a real artist. If the user skips the form, build with the prefilled values.

## Where the sound in the result comes from

Reading levels or beats drives the picture only; it does not put sound in a new clip. For each choice:
- **Its own clip, the video's voice:** in a document without `videoId`, `addMedia` the clip's source, `node.patch` its `sourceIn` to the range start (ticks, 254016000000 a second) and `common.hidden: true`; its sound still plays. `create_clip` `type: motion` with the `documentId` makes the new video.
- **Its own clip or intro card, music (a Tella track, a song, or the video's background music):** play it as an audio node inside the document, so Start is honoured. It needs a `sourceId`: a song attachment has one; for a Tella track or the video's background music, download its `url` (`list_library` scope `default`, or `get_video` `backgroundMusic`), `create_source` `kind: audio` with its duration and PUT the file. Then `addMedia {nodeId: music, start: 0, sourceId, duration: length}` and `node.patch {node: music, patch: {sourceIn: Start in ticks}}` (a top-level field on the audio node). Don't also set background music: `set_background_music` always starts at 0 with a 2 s fade-in and has no offset. Tested with Modern Tech Pulse from 17.032 s: the clip's audio matched the track from the drop.
- **Intro card in their video:** `create_clip` `type: motion` with their `videoId` (it lands last), then `reorder_clip` `order: 0`; untested. A voice range or music plays from the document as above. If their video has background music, it keeps playing under the card too: tell the user, and never replace it without asking.
- **B-roll (the video's own audio only):** a motion document with the video's `videoId`, placed with `add_layout` `media: {type: motion, documentId}`. The clip's own audio plays under it; the curves are on that clip's clock. A layout belongs to one clip: `add_layout` takes a `clipId`, and `startTimeMs`/`durationMs` are on that clip's playback timeline (cuts applied), so keep the shot inside the one clip (shorten it or start it earlier). Only when the range truly runs across a cut, split it there: one document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document starting at the frame the first ended on, keys on each clip's own clock (untested). Then `list_layouts` and make sure the layout after each time-ranged b-roll is hardCut too (it can come back with a spring).

## The sound as numbers

Curves: `lvl` (0–1, the level now) and `h0`…`h15`, the same level delayed by k × 0.4 s. Key each with `setCurve` every 1/30 s, `easing: linear` (at most 1000 keys, so 33 s a document).
- **A clip's voice:** `get_audio_levels` over the range, `stepMs` 20. Map dB to 0–1 between the 10th and 97th percentile, then a one-pole follower, attack 0.04 s, release 0.3 s.
- **Music, a track or a song:** `get_audio_levels` can't hear it. `get_music_beats {sourceId}` of the same source the audio node plays; times are source time, so document time = beat time − Start (keep beats from Start to Start + length). Each beat is a pulse falling off over 0.12 s (downbeats 1.0, others 0.6) on a floor of 0.18; smooth with attack 0.06 s, release 0.45 s. When Start is 0 and the track opens quietly, multiply by a 0 → 1 ramp over its intro. Below `confidence` 0.1 use a slow 0.3–0.6 drift and say so.
- Grant's example peaks at 0.62 on downbeats, about 0.42 on other beats and rests near 0.23 between them; aim for that range.

## The look (1920×1080, from the example)

- **Terrain** (`references/terrain.sksl`, node `viz`, a full fill): `speed` 3, `histStep` 0.4, `height` 3.2, `cell` 0.5, `horizon` 0.5 (the horizon at y 540). Colours as RGBA 0–1:

| Palette | sky | haze | ground | lineColor | peakColor | title ramp end |
|---|---|---|---|---|---|---|
| Violet and cyan | `#04050C` | `#4B2C8F` | `#070612` | `#32AAB1` | `#FFFFFF` | `#B598FF` |
| Sunset | `#0B0410` | `#9C2A5C` | `#10050C` | `#FF8A3D` | `#FFE7C2` | `#FF9E6B` |
| Emerald | `#020806` | `#0F5A3C` | `#03100A` | `#3BE58A` | `#EFFFF4` | `#7CF0B0` |
| Ice | `#03060C` | `#1F4F8F` | `#050A14` | `#7FD3FF` | `#FFFFFF` | `#9CCBFF` |

  Brand colours: the darkest brand colour (darkened to under 8 % lightness) as sky and ground, a mid tone as haze, the brightest saturated one as lineColor, white peaks. Keep the ground dark; light grounds are untested.
- **Stars** (`references/stars.sksl`, node `stars`, a `#00000000` fill above `viz`): `horizon` 0.5, `density` 0.3, `brightness` 1. They fade out before the horizon glow.
- **Title** (node `title`, above both): Oxanium 700, 150 px, letter spacing −0.035 em, line height 1, centred in a 1600 px box at x 160, y 282, colour `#F6F3FF`. Oxanium is the user's uploaded font in the example: use it when `list_motion_fonts` lists it in `libraryFonts`, else Space Grotesk 700 at the same size (tested, reads the same). Effects, innermost first: a `blur` (`styleBlur`), an `fx.gradientRamp` (`skyReflection`) from (960, 282) to (960, 432), colours title, title, ramp end, `colorCount` 3, and a `dropShadow` glow (`whiteGlow`) `#FFFFFFB3`, dx/dy 0, radius 36. Transform: `perspective` 1000, `rotateX` 30°, `origin` (960, 357), so the type leans back over the land.
- **Motion** (on a 10 s canvas; for other lengths keep the entrance and move the exit with the end): opacity 0 → 1 from 0.85 to 1.5 s, ease `0.22, 1, 0.36, 1`; translateY 30 → 0 from 0.85 to 1.8 s, same ease; blur 28 → 0 from 0.85 to 1.7 s, easeOutCubic. Scale 1.2 → 1 linear from 0.85 s to end − 0.2 s, a slow push back. Exit: blur 0 → 28 from end − 0.8 s and opacity 1 → 0 from end − 0.7 s, both easeInCubic, gone at end − 0.2 s. The landscape runs the whole time.

## Timing

The title starts at 0.85 s. With beats, move the title's first key to 0.1 s before the first downbeat after 0.8 s; with a voice, to the first word. Never open on silence: the first second has to move.

## Building it in Tella Motion

1. Document: own clip, `create_motion_document` without `videoId`, `canvas.set` the duration, add the sound (above), then `create_clip`; b-roll, with the video's `videoId`. Name test or new videos after the title.
2. One batch: 17 `setCurve`s; `addShape` `fill` `viz` (`#000000`); `addEffect` `kind: shader`, `effectId: shader`, the file's full text as `source`, every uniform given (`time` [0], `level` [0], `hA`…`hD` [0,0,0,0] plus the look); `bindProperty` `field:common/effects/0/effect/uniforms/time/values/0` to `{time: seconds}`, `…/level/values/0` to `{curve: lvl}`, `…/hA/values/0` … `…/hD/values/3` to `h0` … `h15` in order; then `stars` the same way with its `time` bound. 42 ops in all.
3. Title: `addTitle` (font slug or `mi_…` id, `letterSpacing` −0.035), `addEffect` `dropShadow`, `fx.gradientRamp` and `blur` with `effectId`s, then `moveEffect` `styleBlur` to 0 and `skyReflection` to 1. Key opacity, translateY, scaleX/scaleY and the blur with one `node.patch` on `common` as `{type: keyframes, timeDomain: local, keyframes: [{id, time, value, easing}]}`, times in ticks; the blur's radii go in the nested form `{common: {effects: {styleBlur: {effect: {radiusX, radiusY}}}}}` (dotted keys are refused).
4. To recolour, `node.patch` `viz` `{common: {effects: {shader: {effect: {uniforms: {sky: {type: values, values: [r,g,b,1]}, …}}}}}}` and the ramp's `color1`–`color3` the same way.

## Check

- `get_motion_frame` at full size on a downbeat, in the quietest moment and mid-title-entrance: crisp lines near the camera melting into the haze, no hard band at the horizon, the title clear of the horizon by at least 50 px and not clipped by the lean.
- A 2 fps `get_motion_preview`: loud and quiet stretches must look different. If not, raise `height` or lower the curve's floor.
- The result isn't silent: download a 30 fps `get_video_preview` of the clip and check it has an audio stream with sound in the range, and that the tall hills arrive with the loud parts.
- Report the sound source and how the levels were read (measured or built from beats), the range, the palette and the font used.

## Gotchas

- Tella refuses a shader over 65,536 operations a pixel. Swapping the terrain's own `vnoise` for `tella_noise2d` pushes it over, so it keeps its `fract(sin)` hash; Tella warns that may draw faint grid lines on export GPUs (not seen in previews, export untested). The stars use `tella_hash2d` and are fine.
- A broken shader poisons the document's renders: fix it in a fresh document.
- `get_motion_frame` takes `startTimeMs`; `timeMs` silently gives frame 0.
- Behind a talking head (a cut-out presenter over the landscape) is untested; check the person stays sharp and the title clears their head.

## Variations

- No title: drop the `title` node; raise `horizon` to 0.42 for more land (untested).
- Lower energy (a calm voice): `height` 2.2, release 0.5 s (untested).
