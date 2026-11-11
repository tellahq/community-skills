---
name: ascii-waveform
description: >-
  Make an audio waveform out of small text characters on a dark screen in
  Tella Motion. The sound is drawn as ASCII art printed outward from the
  centre line like a log scrolling both ways, with each character picked from
  the ramp " .:-=+*#%@" by how loud the sound is there, so the band is tall,
  dense and bright where the audio is loud, thins through + = - to dots at its
  edges and goes blank in silence. One live SkSL shader fed by level curves
  read from a clip's voice (get_audio_levels) or built from the background
  music's beats (get_music_beats). Works as its own clip, as b-roll over a
  stretch of speech, or as a strip across footage, with an optional title kept
  clear of the characters. Use when asked for an ASCII or text-character
  waveform, a terminal or hacker-style audio visualizer, a code-style sound
  wave, a waveform made of letters or symbols, a retro computer audiogram
  look, or a dark techy visual that moves with a voice or a song.
metadata:
  title: ASCII waveform
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/ascii-ice-blue.webp
  preview: gallery/ascii-ice-blue.mp4
  tags: audio, waveform, ascii, terminal, visualizer, audio-reactive, music, voice, shader, characters, dark, retro
  prompt: Turn the last 10 seconds of my voice into an ASCII waveform in ice blue, with the title "Northwind Notes" over it.
---

# ASCII waveform

The sound becomes a band of text characters across a near-black screen. The newest sound prints at the centre column and scrolls out to both edges, so the frame always shows the last few seconds; each column's height follows the level at that moment, and inside the band the characters step down a brightness ramp, `@ % #` in the loud core, `* + = -` toward the edge, `: .` at the fringe, with a sparse field of faint dots behind. Use it as its own clip (a voice memo, a teaser, a track), as b-roll over a stretch of speech so the voice keeps playing under it, or as a strip across footage. It is not an audiogram with a player, cover art or captions; for that, use `audiogram`. Builds on `tella-motion-design` (one look, every graphic has an exit) and, for an optional title, `tella-title-cards`.

## Ask once

Work out yourself, never ask: the sound (the video's background music if `get_video` shows one, else the speaking clip's voice), the loudest 8 s stretch of speech or music from the transcript and `get_audio_levels`, a title from the video's name, and brand colours from earlier graphics. Then one `ask_form`, every field prefilled:

| Field | Required | Prefill | Limits |
|---|---|---|---|
| **Sound** (pick) | yes | the video's audio: its voice, or its music when it has background music | `This video's voice`, `This video's music`, `A curated track`, `A track I attach` |
| **Colour** (pick) | yes | Ice blue | `Ice blue`, `Green terminal`, `Amber`, `White`, `Brand` (brand hexes from the video or the message) |
| **Start** (number, s) | yes | start of the chosen stretch | within the video, or 0 for a track |
| **Length** (slider, s) | yes | 8 | 4–33 (one curve covers 33 s; past that, split it) |
| **Where** (pick) | yes | voice: `B-roll over the speech`; music or a track: `Own clip` | `Own clip`, `B-roll over the speech`, `Strip across the footage` |
| **Title** (text) | no | empty | at most 7 words, about 32 characters |
| **Kicker** (text) | no | empty; shown only with a title | about 28 characters, e.g. `EP 12 · VOICE MEMO` |

- **Media.** A curated track comes from `list_library` scope `default`, type `music` (pick one by mood; it is placed with `set_background_music`, see **Sound in the result**). For an attached song look first at the message's attachments (an attachment is already an upload with a `sourceId`); if missing, `ask_question` "Attach the song (an audio file, at least as long as the visualizer)", suggested answers `Use a curated track instead` / `Use this video's audio`. Never use a teammate's video or recording that wasn't offered, and never invent a real artist.
- **Skipped form:** build with the prefilled values.
- Put the title in only when the user gives one or asks for it; the example has none.

## Timing to the sound

- The visualizer must open on sound, not silence. With music, fold the track's 2 s fade-in into the curve (below); with a voice, start the range on the first syllable of a phrase, about 0.2 s before it.
- Peaks on screen land on the audio exactly, at the centre column; they reach the frame's edge `15 × histStep` = 2.55 s later. End the range at the end of a phrase or a bar, not mid-word.
- A title fades in 0.6–0.85 s after the start, after the band has grown, and everything fades out over the last 0.5 s.

## The look (1920×1080, from the example)

| Uniform | Ice blue (example) | Green terminal | Amber (untested) | White (untested) |
|---|---|---|---|---|
| `bg` | `#070A12` | `#080B09` | `#0C0905` | `#09090B` |
| `ink` (loud core) | `#EAF4FF` | `#F1FFE8` | `#FFF1D6` | `#FFFFFF` |
| `dim` (edges, dots) | `#4F86D9` | `#4CC873` | `#C98A2E` | `#8A8F99` |
| `accent` (rare glyph) | `#7CF0D2` | `#FFB547` | `#FFD27A` | `#BFC6D4` |

- Colours are RGBA arrays 0–1: the example's are `bg [0.0275, 0.0392, 0.0706, 1]`, `ink [0.9176, 0.9569, 1, 1]`, `dim [0.3098, 0.5255, 0.851, 1]`, `accent [0.4863, 0.9412, 0.8235, 1]`. Brand: the darkest brand colour (darkened to under 8 % lightness) as `bg`, its brightest as `ink`, the main brand colour as `dim`, a second as `accent`.
- Shape: `cellW` 24, `cellH` 38 (a 80 × 28 grid, glyph pixels 4 px), `speed` 16 cells a second, `histStep` 0.17, `field` 0.08, `quiet` [0, 0, 0, 0]. The shader adds fine scanlines (a 4 px period) and a soft vignette; the colour shifts from `dim` to `ink` as a cell gets louder, and about 3 % of loud cells take `accent`.
- Title, when there is one: `quiet` = a box (x, y, w, h px) about 80 px larger than the type all round, so the ramp fades to blank 1–3.5 cells around it. Kicker Roboto Mono 500, 26 px, +0.3 em, in `accent`; title Space Grotesk 700, 140 px, −0.03 em, in `ink`, centred. They fade in and rise 20 px over 0.7 s on ease `0.22, 1, 0.36, 1`, the kicker 0.2 s first.

## The sound as numbers

Curves `lvl` (0–1, the level now) and `h0`…`h15`, where `hk(t) = lvl(t − k × 0.17)` (before the start, the floor). Key each with `setCurve` every 1/30 s, `easing: linear` (8 s = 241 keys; at most 1000 keys, so 33 s).

- **Voice** (a clip's own audio): `get_audio_levels` on the range, `stepMs` 20. Map dB to 0–1 between the range's 10th and 97th percentile, then a one-pole follower, attack 0.04 s, release 0.3 s, on a floor of 0.07.
- **Music** (background music or a curated track): `get_audio_levels` can't hear it. `get_music_beats {videoId}`; for each beat a pulse falling off over 0.12 s (downbeats 1.0, others 0.6) on a floor of 0.2, smoothed with attack 0.06 s, release 0.45 s, times `0.35 + 0.65 × fade` (fade 0 → 1 over the track's first 2 s). The example is this curve for a 113 BPM track: 0.07 rising to 0.2 by 2 s, beats peaking 0.47–0.5, downbeats 0.68. Below `confidence` 0.1, use a slow 0.3–0.6 drift and say so.
- `get_audio_levels` reads only a recorded clip's voice track: on a Tella Motion clip it fails with "This clip has no voice track", even when the document plays the voice. Read the levels from the user's original clip, never from the clip you made.
- **Attached song:** no Tella tool reads an audio-only source's levels. If your sandbox has ffmpeg, measure the file's RMS per 20 ms (`astats` with `asetnsamples` at 8 kHz) and treat it as a voice with release 0.4 s (this worked in testing). Otherwise use the music path on its beats: set it as the new video's background music at `volume` 0 just to call `get_music_beats`, and shift the beat times by the range start (untested).

## Building it in Tella Motion

1. **Document.** Own clip: `create_motion_document` without `videoId` (1920×1080), then `create_clip` `type: motion` with its `documentId` once it is built: without `videoId` that makes a new video (rename it with `update_video`), with the user's `videoId` it adds the clip to the end of their video. B-roll: make it with the `videoId` and place it with `add_layout` (`media: {type: 'motion', documentId}`) over the range. `add_layout` takes a `clipId` and its `startTimeMs`/`durationMs` are on that clip's playback timeline (cuts applied), so one layout can't run into the next clip: keep the range inside the clip where it is said (start earlier or shorten it). Only when the range truly runs across a cut, split it there: one document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document's curves continuing from where the first ended, on its own clip's clock; then `list_layouts` and make the layout after each b-roll `hardCut` too (it can come back as a spring). The split is untested. Strip: an overlay document with the shape below.
2. **Sound in the result** (below), before the curves.
3. **Curves.** One batch of 17 `setCurve`s.
4. **Shader node.** `addShape` fill covering the canvas (node `viz`, full length), `addEffect kind: shader` with the source from `references/shader.md` and every uniform declared (`time` [0], `level` [0], `hA`…`hD` [0,0,0,0], plus the values above). This worked directly in a brand-new document.
5. **Bind.** `bindProperty` `field:common/effects/0/effect/uniforms/time/values/0` to `{time: seconds}`, `…/level/values/0` to `{curve: lvl}`, and `…/hA/values/0` … `…/hD/values/3` to `h0` … `h15` in order.
6. **Title** last, so it sits above `viz`; set `quiet` to its box.

### Sound in the result

Levels and curves only move the picture; the sound has to be placed too.

| Sound | Own clip | B-roll or strip |
|---|---|---|
| This video's voice | Put the voice in the document (tested): `addMedia {sourceId}` with the clip's source (`list_sources`), then `node.patch` it with `sourceIn` = the range start in ticks (seconds × 254016000000), `common.duration` = the length in ticks and `common.hidden: true` (it stops drawing, its sound still plays), `node.move` it to index 0. This needs one uncut stretch of one source; with cuts or several sources in the range, `duplicate_video` the range instead and place the document over it as a full-frame front overlay (its opaque `bg` hides the footage; untested here). | Nothing to add: the clip's own voice keeps playing under it. |
| A track I attach | The same `addMedia` with the song's `sourceId` (from the attachment, or `create_source` `kind: audio` with `duration` in seconds, then PUT the file). An audio-only source lands as an `audio` node, nothing to hide; patch `sourceIn` and `common.duration` the same way (tested). | Same audio node in the document, so the song plays only while the visualizer is on screen, over the speaker (untested; lower its `gain` if the voice must stay clear). |
| This video's music / a curated track | A new video has no music: `set_background_music` on it with the same `presetId` (the video's own track: `get_video` `backgroundMusic`), then `get_music_beats` on that video, so the beats match where the track starts. Added to the end of the user's video, the music is already there; shift its beat times by the clip's start in the video. (Untested.) | The video's music already plays; a curated track is `set_background_music` on the user's video, which loops under the whole video at volume 0.2, so tell the user. (Untested.) |

`addMedia` stretches the canvas to the whole source (30 s for a 30 s file): run `canvas.set` to the length after it, not before.

## Check

- `get_motion_frame` at 1920 wide: on the loudest beat or word (the centre is `@ % #`, white with the odd accent), in a quiet gap (only a short run of `- . :` near the middle, or just the faint dots), and at the first frame (faint dots on `bg`, not black). Every glyph is whole and crisp; none touches the title.
- A 2 fps `get_motion_preview`: loud and quiet stretches must look clearly different. If not, lower the floor or shorten the release.
- The result isn't silent: download a `get_video_preview` of the clip and run ffmpeg `volumedetect` (or compare its loudness per 0.25 s with the source's range). In testing, the voice played exactly from the chosen start (correlation 1.0 with the source) and the centre column's brightness followed it about 0.1 s late, the follower's lag.
- In the video (`get_video_preview` 30 fps), loud frames land on loud audio at the centre column.

## Gotchas

- The shader scales its cells with the node's height (`resolution.y / 1080`). In a 360 px strip, multiply `cellW`/`cellH` by 3 (72/114) to keep 24×38 px cells. The strip is opaque `bg`; untested, so check the speaker stays clear.
- Don't use the built-in `audioSpectrum` or `audioWaveform` generators: in preview renders they drew nothing.
- A broken shader asset poisons the document's renders: rebuild in a fresh document.
- `get_motion_frame` needs `startTimeMs`; `timeMs` silently gives frame 0, which is nearly empty here.

## Variations

- **Portrait** (1080×1920): the cells scale with the height, so the grid is 25 × 28; use `speed` 5 so 15 × 0.17 s still spans centre to edge. Untested, check every frame.
- **Calmer voice:** release 0.5 s and `speed` 12 with `histStep` 0.22.
