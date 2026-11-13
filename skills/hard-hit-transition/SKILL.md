---
name: hard-hit-transition
description: >-
  Make a cut land like a hit. For a few frames the outgoing shot shakes, pushes
  in, rolls and bows sideways, faster and faster, with motion blur and a colour
  fringe. The switch happens inside the blur on one bright frame, and the
  incoming shot lands with the move mirrored, then settles under a decaying
  shake. Edges are mirror-tiled, so no border ever shows. One SkSL shader in
  Tella Motion, placed across a cut between two clips, a jump cut inside one,
  or between shots in a Tella Motion montage, with an optional impact boom and
  woosh on the switch and the cut moved onto the music's downbeat. Use when
  asked for a hard hit, shake, punch, impact or camera-shake transition, a cut
  that hits, a slam cut, a hype cut for a reel or montage, or to make the cuts
  hit harder.
metadata:
  title: Hard hit transition
  author: Tella
  category: Transitions
  image: og.jpg
  poster: gallery/hard-hit.webp
  preview: gallery/hard-hit.mp4
  prompt: Make the cut into the launch shot hit hard, with a boom on it, on the beat of the music.
---

# Hard hit transition

A one-second hit on a cut. Shot A starts to judder, the judder grows, and the frame pushes in, rolls and bends into the switch. Shot B arrives at full push, bent and rolled the other way, and shakes itself still. It is a treatment of the footage on both sides of a cut, not an overlay drawn over it: both shots go into one Tella Motion document so the shader can read either at any pixel. Use it for one big moment (a launch, a drop, the start of a sequence) or a few cuts of a montage, never on every cut of a talking video: three or four a minute at most. Builds on `tella-transitions` (when a transition is worth it, never over a word) and `tella-motion-design`; `tella-audio-sync` for beats.

## Ask once

Work out yourself, never ask: the candidate cuts (every clip boundary and every jump cut in the selection or the video, from `get_timeline` with `cuts` and `words`), which one is strongest (a change of place or energy, a pause, the first word of a new section; never mid-word), whether the video has background music, and its beats (`get_music_beats`). The footage is the video's own: nothing to upload.

Then one `ask_form`, every field prefilled:

| Field | Type | Required | Default and limits |
|---|---|---|---|
| **Which cuts** | pick, multiple | yes | Up to 12 cuts, each labelled with its time and the words either side ("0:41, …ready? / Liftoff…"), a frame of shot B as its picture. Prefilled with the cut the user selected or named, else the strongest one. |
| **Strength** | slider, % | yes | 30–100, step 10, default 100 (the example). Scales the move, see The look. |
| **Sound effect** | switch | no | On. |
| **Which sound** | pick | no | Boom + woosh (default), Boom only, Woosh only. From Tella's curated catalogue. |
| **On the beat** | switch | no | Only when the video has music. On: each cut moves to the nearest downbeat within 0.3 s. Off: cuts stay where they are. |

The shake runs on both axes, as in the example; there is no direction field (horizontal-only or vertical-only needs a shader change that hasn't been tested). If the user skips the form, use the prefilled values. If a chosen cut has footage under 640 px wide, say that the landing will look soft and suggest 60–70 % strength.

## Timing

- The switch is `cut × dur` after the effect starts: at strength 70 % and above, 0.45 s into a 1.0 s hit; below, 0.30 s into 0.6 s. Call `pre = cut × dur` and `post = (1 − cut) × dur`: 0.45 s and 0.55 s at full strength, 0.30 s and 0.30 s below 70 %. The hit starts `pre` before the cut and ends `post` after it; every length below uses them.
- On the beat: put the switch on a downbeat (`downbeatsMs`, else `beatsMs`) by cutting the end of clip A or the start of clip B so the boundary lands there. Move it at most 0.3 s, never into a word, and skip beats in the track's first 2 s (it fades in).
- Without music, the cut stays put. Never start a hit inside a word on either side; if the `pre` before the cut holds the end of a word, use the 0.6 s timing.
- At least 1.5 s between two hits; none in the first or last 0.3 s of the video.

## The look

Exactly the example (`Skill example: Impact transitions (shake: hard hit)`): canvas 1920×1080 at 30 fps, a 1.0 s shader on a full-frame black fill from 1.05 s to 2.05 s, switch at 1.50 s. Shader `references/shake-cut.md`, uniforms at 100 %:

`dur` 1, `cut` 0.45, `amp` 38, `hz` 14, `push` 0.25, `bend` 0.22, `warp` 0.35, `roll` 3, `blur` 1, `split` 6, `flash` 0.25, `seed` 4 (a new number for every hit: 4, 7, 9, …).

Strength `s` (0.3–1.0) multiplies `amp`, `push`, `bend`, `warp`, `roll`, `split` and `flash`; `hz` 14 and `blur` 1 stay. Below 0.7 use `dur` 0.6, `cut` 0.5, `hz` 12. Never go past 100 %: `push` above 0.3 or `warp` above 0.45 turns the landing to radial mush, and `amp` above 45 looks like a broken stabiliser.

`progress` is keyed 0 → 1 **linear** over the hit (the shader eases itself). The motion: A's envelope grows as `t²` into the switch, the shake starting at a quarter strength; B lands at full push mirrored (opposite bend and roll) and decays as `(1−t)²`. An 8-tap blur over one frame never crosses the switch, so every frame is all A or all B. Shots are `fit: "cover"` with `scale` 1.03 (A) and 1.02 (B) so old film's thin black edge never repeats in the mirror tiling.

## Building it

Pass the shader text from `references/shake-cut.md` whole as `source`; don't retype or "improve" it. Ticks are 254,016,000,000 a second.

**Across a clip boundary (tested).** A b-roll belongs to one clip, so the hit is two documents, one per clip, each on its own clip's clock:

1. Get each side's footage as a source: the clip's own upload if it is in `list_library` (`private`/`workspace`), else `get_clip_preview` (width 1920, fps 30) of the frames needed (clip A's last `pre`, clip B's first `post`), **before** adding any b-roll there, then `create_source` and PUT the file.
2. Per side, `create_motion_document` with `videoId`, then one batch: `canvas.set` duration = that part's length; `addMedia` `nodeId: "shot"` with the `sourceId`; `node.patch` `{fit: "cover", sourceIn, audio: {assetId: "media.<sourceId>", gain: 0, mute: true}}`; `addShape` `nodeId: "hit"`, `shape: "fill"`, `#000000`, full length; `addEffect` on `hit`, `kind: "shader"`, `inputs: {shotA: "shot", shotB: "shot"}`, every uniform; `setKeyframes` on `field:common/effects/0/effect/uniforms/progress/values/0` with `keys` `[{at: 0, value: p0}, {at: len, value: p1}]`, `easing: "linear"`. Clip A's part is `pre` long and runs `progress` 0 → `cut`; clip B's is `post` long and runs `cut` → 1. Binding one shot to both inputs works because the shader reads A only before the switch and B only after.
3. `add_layout` on clip A from its end − `pre` for `pre`, and on clip B from 0 for `post`, each `transitionStyle: "hardCut"`, `media: {type: "motion", documentId}`.
4. A time-ranged b-roll makes a follow-on layout for the rest of the clip, which can carry a `spring` transition: `list_layouts` on both clips and `update_layout` every layout touching the hit to `transitionStyle: "hardCut"`, or clean footage returns through a dip.

**A jump cut inside one clip.** One document, `pre + post` long, on that clip from `pre` before the cut to `post` after, the clip's rendered footage of that range as `shot`, `progress` 0 → 1; placed and hard-cut as in steps 3–4.

**Between shots in a Tella Motion montage (the example).** Add the shots **last first** so the earlier one draws on top. A runs to the hit's end, B starts at the hit's start; the shader shape spans the hit with `inputs: {shotA, shotB}`. Name each shape in order ("Hit 01").

**Sound.** `add_sound_effect` with `presetId`: `impact-boom` exactly on the switch (its hit is at 0 ms) at 1.0 × strength, on clip B at 0; `deep-woosh` at 0.4 starting 0.4 s before the switch, on clip A, 0.4 s long. Over music, halve both.

## Checking it

- `get_video_preview` at 1280+, 30 fps, from 1 s before the switch to 1 s after; tile its frames. Every frame before the switch is A, every one after is B; the push builds over the last third, not on one frame; B lands bent the other way and settles in about 0.4 s; no empty border; no jump where a b-roll starts or ends (A continuous into the hit, B continuous out of it).
- Read the preview's loudness in 50 ms bins: the boom's peak lands within one bin of the switch.

Gotchas:

- A shader on a media node sees the source's own pixels, not the canvas: always put it on the separate full-frame shape.
- In a montage, if shot A outlasts the hit it pops back on top for a frame. Trim it to end with the hit.
- A preview taken after the b-roll is placed includes the hit itself; take the footage first.
- Footage at 320–480 px goes to mush at the landing. Stock clips sometimes carry a stray frame at their head: start B's `sourceIn` a few frames in.
- To change a uniform, `setProperty` on its `field:` path; to change the shader, remove the effect, add it again and re-key `progress`.
- Flashes: keep `flash` at 0.25 or less and no more than three hits in 3 s.

## Variations

- **Beat run**: several hits at 50–60 % on consecutive downbeats of a montage, two bars apart.
- **Vertical (9:16)**: the shader scales with the canvas; keep the same values.
