---
name: vinyl-record-player
description: >-
  Make a needle-drop moment in Tella Motion: a top-down turntable in a dark
  spotlight, the tonearm swinging in from its rest and dropping onto the
  record with its shadow closing under it, the platter's strobe-dot rim
  spinning up into a blur and the centre label (plain white, the user's
  artwork, or a track title and artist) turning at 33 or 45 rpm, with the
  music starting the moment the needle lands. Built from the layered photo
  cut-outs that ship with the skill (or a generated deck, or the user's own
  top-down photo). Works as its own clip
  or as b-roll over a stretch of footage. Use when asked for a record player,
  a turntable, a vinyl or needle-drop intro, a spinning record, a music or
  podcast intro with a record, a "now playing" record, or an animated vinyl
  for an audio clip.
metadata:
  title: Vinyl record player
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/needle-drop.webp
  preview: gallery/needle-drop.mp4
  tags: vinyl, record, turntable, needle drop, music, podcast, intro, audio, spin, photo cut-out
  prompt: Open my podcast episode with a record player whose needle drops on our theme, with "Low Tide Hours" and "Maya Ortiz" on the label.
---

# Vinyl record player

One shot, looking straight down at a turntable in a pool of light on black. The tonearm swings in from off the frame, lowers onto the lead-in groove (its shadow tightens under it as it touches), then the platter spins up: the strobe dots on the rim smear into a blur and the label starts turning. The sound starts on the touch. It's an intro or a bridge for music, a podcast or an audio clip: its own clip, or b-roll over a few seconds of the video. Builds on `tella-motion-design`.

## Ask once

Work out without asking: the label's words (the video's title, the episode or song name, the speaker's name in the transcript), whether the video has speech or music to play (`get_transcript`, `get_timeline`), its beats if a track plays (`get_music_beats`), and attachments on the message. Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Prefill / limits |
|---|---|---|---|
| Label title | text | no | Song, episode or show name; empty = the plain white label. Up to 18 characters. |
| Label second line | text | no | Artist or host; empty if there is no title. Up to 22 characters, shown in caps. |
| Sound | pick | yes | `The clip's own audio`, `None`, or a Tella track: Vinyl Memories (default), Jazzy Relax, Midnight Velvet, Focus Lo-Fi Flow, Old School Hip-Hop, Chill Pathways. Prefill `The clip's own audio` when the graphic is b-roll or the clip has music. |
| Needle drop at | slider, s | yes | 3.1–8, default 3.6: the moment the stylus lands and the sound starts. The swing starts at D−3.1, so nothing earlier fits. |
| Length | slider, s | yes | 6–20, default 10. At least the drop + 4 s. |
| Speed | pick | yes | 33 rpm (default) or 45 rpm. |
| Where | pick | yes | `Its own clip` (default, added at the start or where the user said), `B-roll over the clip`. |
| Deck | pick | yes | `Tella's deck` (default, the photo layers in `assets/`), `My own photo`, `Generated`. |

Skipped form: use the prefilled values. Media can't go in a form:
- **Label artwork**: if the message has a square image attached (cover art, logo), use it as the label in place of `label.png`, masked to the label circle, and leave the text fields empty (untested). Don't ask for artwork that isn't there.
- **Your own photo** (Deck = `My own photo`): if none is attached, `ask_question` for "one photo taken straight down over the spindle, phone flat and level, the tonearm parked on its rest off the record, even light, no glare on the label; any turntable". Cover any brand marks before use. No photo: use Tella's deck.
- **The clip's own audio** on its own clip: the stretch to play, from the transcript or the user's message as `from <word/time> to <word/time>`; ask with `ask_question` only when the video has several candidates.

## Timing

D is the needle drop. Key everything from it, on the document's clock:

| Beat | When | What |
|---|---|---|
| Rest | 0 → D−3.1 | Arm parked off the frame, still (at D = 3.1 the swing starts on the first frame; D ≥ 3.6 gives a held rest). |
| Swing | D−3.1 → D−0.7 | Arm rotates −22° → 22° about its pivot onto the record, easeInOutCubic. |
| Touch | D−0.6 → D | Arm scale 1.006 → 1 (it lowers away from the camera); the lifted shadow fades out as the resting one, closer to the arm, fades in. easeInOutSine. |
| Spin-up | D+0.3 → D+1.0 | Label and strobe dots 0 → 70° (45 rpm: 95°), cubic-bezier (0.333, 0, 0.667, 0.333). |
| Blur | D+0.55 → D+1.35 | The blurred rim fades in over the dots, then the dots fade out. |
| Play | D+1.0 → end | Linear at 200 °/s (33⅓ rpm) or 270 °/s (45 rpm). |
| Tracking | from D+1.2, every 0.9 s | Arm drifts +0.08°, +0.02°, +0.10°, +0.03°, +0.11°, easeInOutSine: barely visible, but it stops the arm looking pasted on. |

On b-roll, put D on the first downbeat of a song (`get_music_beats`) or on the word that introduces it, and start the graphic D−3.6 s before.

## The look

Grant's example: 1920×1080, 10 s, D = 3.6 s. Every layer's file, position, size, anchor and keys are in `references/tella-deck.md`; follow it exactly.
- Black fill, the static deck photo (record, platter, plinth) full frame, the spindle at (960, 536).
- The rim is two layers over it: strobe dots that spin for 1.2 s, then a ready-blurred ring that never rotates.
- The label (`label.png`, a plain white paper label with a small hand-drawn smiley) is a disc of radius 163 px on (960.5, 536.5); it and anything on it turn about that point. The spindle sits on top, still.
- The tonearm's pivot is off the top right at (1632, 230): it starts out of frame and only its headshell and the end of the arm swing in.
- Spotlight on top: `fx.vignette` amount 1, size 0.19, softness 0.475, black. It hides the plinth and the corners.
- Label text: the title in Inter 700 27 px `#16161A`, box (840.5, 568) 240 wide, centred; the second line in Inter 600 17 px, tracked 0.18, `#6B675E`, box (840.5, 608). Both below the spindle, clear of the smiley. Give them the label's anchor and rotation keys and paint them just above it.
- Motion blur (shutter 180°) on the label, its text, the dots and the arm. The record's light sheen is in the static photo and never turns.

## Building it

1. **Get the files.** Tella's deck: `$HOME/.agents/skills/vinyl-record-player/assets/`, else `/workspace/skills/vinyl-record-player/assets/`; outside the editor, `get_community_skill` `vinyl-record-player` gives a download url for each file. For each PNG: `create_source` `kind: 'image'` with its width and height, PUT the bytes (`Content-Type: image/png`) to `uploadUrl`. Eight uploads.
2. New 1920×1080 document (no `videoId` for its own clip; with `videoId` for b-roll), canvas = Length. `addMedia` each `sourceId` in the table's order, then `node.patch` each `destination` (`addMedia` lands with `fit: contain`), `setProperty` `anchorX`/`anchorY`, `setKeyframes`, `setMotionBlur`, and the spotlight last: a `#00000000` full-frame shape with `addEffect` `fx.vignette`, `backdrop: true`.
3. Label text: `addTitle` both lines, `node.move` them to just above `label` (`parent: ""`, `index`), then the label's anchor and rotation keys.
4. **Generated** or **My own photo**: `references/deck-prompts.md` (a `generate_image` prompt and a `decompose_image` split into a plate and a tonearm layer; the plate's rim is masked out and spun, the label drawn).
5. **Its own clip**: `create_clip` `type: 'motion'` with the `documentId` (a new video, or `videoId` to append). **B-roll**: `add_layout` with `media: {type: 'motion', documentId}` inside one clip. A layout can't span clips: split a range at clip boundaries, one document per clip.

## Sound in the result

A Tella Motion clip is silent until you give it sound:
- **Tella track** (tested): `list_library` `scope: 'default'`, `type: 'music'` gives the track's `url`. Download it, `create_source` `kind: 'audio'` with its duration, PUT the bytes, then `add_sound_effect` on the motion clip with that `sourceId`, starting at D minus the track's leading silence, until the clip's end. Vinyl Memories has 2.82 s of silence. Measure it (`ffmpeg -af silencedetect=n=-50dB`). `add_sound_effect` refuses a music `presetId`, and `set_background_music` loops the whole video from 0, so it can't start on the drop.
- **The clip's own audio** on its own clip (untested): `addMedia` the clip's source into the document at D, `node.patch` `sourceIn` to the range start and `common.hidden: true` (it keeps playing).
- **B-roll**: the clip's own audio plays on under it; nothing to add.
- A soft touch: curated `press` at D−0.55, volume 0.5.

## Check

`get_filmstrip` of the document at 0, D−1.9 (mid-swing), D−0.3 (shadow closing), D, D+0.7 (dots smearing), D+3 and the end. Look for: the stylus on the lead-in, not on the label; the arm turning about its pivot, not drifting; the label text readable at D+3 and turning with the label; no seam between the dots and the blurred rim. Then `get_video_preview` the result and confirm it isn't silent and the sound starts within 0.1 s of D (`ffmpeg volumedetect` in 0.25 s windows). The first preview right after an upload can be silent while the source processes: render it again a minute later.

## Gotchas

- `get_motion_frame` needs `startTimeMs`. `inspect_motion_node_properties` takes `path`, not `node`.
- A new title paints on top of everything, the spotlight included, until you `node.move` it.
- Anchors are canvas pixels, not the layer's own: without them every layer turns about (960, 540) and the arm flies off.
- Generated decks sometimes add a logo or lettering; regenerate (or mask it) rather than use one.

## Variations

- 45 rpm for an upbeat intro; a slower 0.9 s swing for a calm one.
- Behind an audiogram or captions: build it as b-roll and put the text on top.
