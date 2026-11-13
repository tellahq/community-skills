---
name: zoom-blur
description: >-
  Hit a moment of the user's own footage in Tella with a punch of radial zoom
  blur: the picture streaks outward from a point on the subject, red and blue
  fanning apart at the streak ends, while the point itself stays sharp. It
  ramps up in 0.3 s so its peak lands on a hit, a stressed word or a beat,
  holds a moment, and decays back to the clean clip, so the entry and exit
  never show as a cut. Built as a live Tella Motion overlay (a backdrop shader
  on a clear fill) over the clip, with the blur's centre keyed to follow the
  subject. One hit, or one on every bar of the music. Use when asked for a
  zoom blur, radial blur, speed blur, punch blur, impact blur, a blur hit or
  whoosh on a jump, trick, reveal or "and then…" moment, or a zoom blur on the
  beat.
metadata:
  title: Zoom blur
  author: Tella
  category: Editing & effects
  image: og.jpg
  poster: gallery/zoom-blur-ollie.webp
  preview: gallery/zoom-blur-ollie.mp4
  prompt: When the board pops at 0:04, hit the footage with a zoom blur pulling from the board and let it settle.
---

# Zoom blur

One treatment for a short stretch of the user's **own footage**: on the hit, the frame bursts into streaks that radiate from a point on the subject, the colour splitting red-outside, blue-inside at their ends, and under a second and a half later the clip is clean again. It sits over the clip as a full-frame Tella Motion overlay that filters whatever is beneath it, so it works on camera footage, b-roll or a screen recording in any layout. Audio is untouched. It is an accent: one or two per video.

Builds on `tella-motion-design` (timing to words, checking) and `tella-camera-moves` (pair it with a punch-in layout for more impact; it is not a camera move itself). For a rainbow edge split without the blur, a glow, or a ripple, this is the wrong skill.

## Ask once

Work these out yourself and never ask:
- **The hit**: from `get_transcript` word timings, the stressed word of the line (an impact word, "and then…", a reveal, a number); with music, `get_music_beats` on the background music (or the clip's source); with no speech, the loudest transient in `get_audio_levels` (10 ms steps) or, from frames, the moment of action (a pop, a landing, a cut-in). Pick the strongest one in the clip the user means, or in the current selection.
- **The subject's position** at each key, from `get_clip_frame` at hit − 0.25 s, hit + 0.2 s and hit + 0.5 s.
- The canvas size, the clip and overlay times, and the video's flashes already there.

Then one `ask_form`, every field prefilled so submit alone builds it:

| Field | Type | Required | Prefill / default | Limits |
|---|---|---|---|---|
| **The moment** | text | yes | the hit you found, as `0:04.3 – "pop"` (or `0:04.3 – board pops`) | a time on the video, or a range `0:12–0:20` for beat mode; ≤ 40 characters |
| **Strength** | slider, % | yes | 100 % (the example) | 20–100 %; peak `amount` = 0.7 × value. 60 % is a subtle accent |
| **Pulls from** | pick | yes | The subject, tracked | The subject, tracked · The face · Frame centre |
| **Colour fringes** | switch | no | on | on = `fringe 0.4`, off = `fringe 0` |
| **Length of the punch** | slider, s | yes | 1.3 s (the example) | 0.6–2.0 s, rise to the end of the decay |
| **Hits** | pick | yes | One hit | One hit · Every bar (downbeats) · Every other beat |
| **Whoosh** | switch | no | off | on adds a quiet whoosh sound effect under each hit |

- Show the pick options as words only; no pictures are needed.
- No media to ask for: the effect uses the clip's own footage. If the stretch has no footage (a blank clip, a pure Tella Motion clip), say so with `ask_question` and offer "lay it over the next clip", "add a vintage library clip from `list_library` scope `vintage` as b-roll first", or "skip".
- Beat mode without background music or a range: ask with `ask_question` "Which stretch should hit on the beat?" with up to three suggested ranges from the transcript.
- Skipped form: build with the prefilled values.

## Timing

Times are on the overlay's own clock (`hit` = the moment − the overlay's start; the overlay starts at least 0.9 s before the first hit and ends about 0.45 s after the last decay).

| Key on `amount` | Time | Value | Easing into the next key |
|---|---|---|---|
| hold | 0 | 0 | `hold` |
| rise starts | hit − 0.3 s | 0 | `easeOutCubic` |
| peak | hit | peak | `linear` |
| shoulder | hit + 0.2 s | 0.9 × peak (0.62 in the example) | `easeInOutSine` |
| clean | hit + length − 0.3 s (1.0 s in the example) | 0 | `linear` |

- The peak lands **on** the word's first syllable or the beat, not before it.
- Beat mode (untested): the same five-key envelope per hit, one overlay per clip the range covers (see "Across clips" below); each envelope must reach 0 before the next one's rise. Keep hits at least 1.5 s apart (at most two in any 3 s, for viewers sensitive to flashing); drop beats to get there, and shorten the length to fit.
- Never let a peak sit over a name, number or on-screen text the viewer has to read.

## The look (from the example, 1920 × 1080)

- `amount` peak 0.7, shoulder 0.62, `fringe` 0.4, `clear` 0.04: a tight sharp spot and streaks that reach almost to the centre.
- `center` x 0.52 fixed; y keyed with `easeInOutSine` 0.47 at hit − 0.25 s → 0.36 at hit + 0.2 s → 0.30 at hit + 0.5 s, so the sharp spot rides up with the board as it rises. Follow whatever the subject does the same way: one key per position, about 0.3 s apart, only while the blur is visible.
- "The face": centre on the bridge of the nose. "Frame centre": 0.5, 0.5, no keys.
- At full strength the frame is mostly streaks for about 0.4 s; the subject must stay readable in the sharp spot, which is why the centre tracks it.

## Building it

1. `create_motion_document` with the `videoId`, named `Zoom blur: <what it hits>`; `canvas.set` its duration to the overlay's. Show it with `add_overlay` `motionDocumentId` on the clip: `point` 0,0, `dimensions` the video size, `depth: "front"`, `transition: "hard_cut"`, no `animation`.
2. One node `fx`: `addShape` `shape: "fill"`, `color: "#00000000"`.
3. `addEffect` on `fx`: `kind: "shader"`, `backdrop: true`, the source from `references/shader.md` as written, uniforms `amount 0`, `center [0.52, 0.47]` (or your point), `fringe 0.4`, `clear 0.04`.
4. Key with `setKeyframes` on the paths `inspect_motion_node_properties` lists (a backdrop has a doubled `effect`): `field:common/effects/0/effect/effect/uniforms/amount/values/0` and `…/center/values/1` (and `/values/0` for x). Times in seconds on the document's clock.
5. Whoosh: `list_library` scope `default` sound effects, a short whoosh, `add_sound_effect` starting about 0.15 s before the hit, volume 0.3–0.5.

### Across clips

An overlay belongs to one clip and can't span a cut, and a document plays in one place only. The moment and the range are on whole-video time; overlay times are on each clip's playback timeline (cuts applied). So:
- **Beat mode** (untested): split the range at clip boundaries from `list_clips` (each clip's start = the sum of the earlier clips' cut durations). Build one document and one overlay per clip, each covering only its part of the range, and convert every key to that document's own clock (video time − clip start − overlay start).
- **A punch that straddles a cut** (a beat or the one hit within a punch-length of a clip's end): part 1 on the outgoing clip, ending on its last frame, with the keys before the cut; part 2 on the incoming clip from 0, with the rest of the keys shifted back and a first key holding the envelope value (and `center`) in force at the cut, so the blur carries on without a step. If the hit is in the last clip, shorten the decay to end on its last frame instead.
- **A hit less than 0.9 s into a clip**: start the overlay at the clip's 0 and keep the keys on its clock; the rise may be shortened, never moved off the hit.

A second hit elsewhere: `duplicate_motion_document` (a document plays in one place only), then move the keys. Name them in order ("Zoom blur 02: landing").

## Checking it

- `get_filmstrip` of the clip at the overlay start, hit − 0.3 s, the hit, hit + 0.2 s, the end of the decay and the overlay end: clean before and after, the peak on the moment, no pop at the overlay's edges.
- One `get_clip_frame` at the hit, 1920 wide: the subject sharp in the clear spot, streaks even all round, red outside and blue inside at the ends. A blur pulling from empty floor or sky means the centre keys are off.
- A 10 fps `get_video_preview` across the range: the ramp moves smoothly, no snap where a key jumps.
- Report each hit's time, what it lands on, the peak and the centre.

## Gotchas

- The fill must stay clear and its blend mode `normal`: any other blend mode drops the backdrop and shows the footage unfiltered.
- `addAdjustment` inside an overlay only sees the overlay's own layers; the clear backdrop fill is what reaches the footage.
- A brand-new document refuses a raw shader insert through `node.patch`; use `addEffect`. A shader that fails to compile poisons the document's renders: rebuild in a fresh document.
- Changing the source means `removeEffect`, `addEffect` again, then re-keying.
- Keep `amount × (1 + fringe)` ≤ 1 (see `references/shader.md`), so with fringes on never push past 0.71.
- Built-in `blur` or `fx.chromaticAberration` can't make this: one is not radial, the other draws three ghosts and coloured edge bands.

## Variations

- Subtle accent under a talking head: 50–60 %, fringes off, length 0.8 s, centre on the face.
- Stack with a punch-in layout on the same word for a harder hit.
