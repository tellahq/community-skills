---
name: glitch-transitions
description: >-
  Add short digital glitch stingers (0.4–0.8 s) to a Tella video at cuts,
  layout changes, b-roll entries, punch-ins or clip boundaries: the frame tears
  into displaced horizontal slices, splits into red/green/blue, breaks into
  pixelated blocks and fills with static, peaking on the switch so the change
  happens inside the glitch, then settles on the new shot. Built as live,
  editable Tella Motion overlays (a transparent full-frame layer running a
  glitch shader on the footage beneath), in three intensities: Chroma blip,
  Signal tear and Hard crash. Use when asked for glitch transitions, glitch
  cuts, RGB split / chromatic aberration transitions, datamosh or digital
  distortion stingers, VHS/signal-error transitions, or a techy, edgy cut
  between shots.
metadata:
  title: Glitch transitions
  author: Tella
  category: Transition screens
  image: og.jpg
  poster: gallery/signal-tear.webp
  preview: gallery/signal-tear.mp4
  prompt: Add a glitch transition at every b-roll cut in this video, medium intensity, with a glitch sound.
---

# Glitch transitions

A glitch stinger hides a switch inside a burst of broken signal. For a fraction of a second the
picture tears: horizontal slices jump sideways, the colour channels split (red one way, blue the
other), rectangles break off and pixelate, and static washes over it. The burst peaks on the switch
itself, so neither shot is readable on the frames around the cut, then falls away and leaves the
new shot clean.

Load `tella-transitions` too, for when a transition is worth having. `references/glitch.sksl` is
the shader; it is the look, so use its full text as is.

## The presets

| Preset | Length | Switch at | rgb | slice | blocks | noise | Use it for |
|---|---|---|---|---|---|---|---|
| **Chroma blip** | 0.4 s | 0.2 s | 18 | 40 | 0 | 0.06 | punch-ins, small layout changes, a title's entrance |
| **Signal tear** | 0.6 s | 0.3 s | 30 | 160 | 0.5 | 0.18 | b-roll in and out, screen ↔ camera changes |
| **Hard crash** | 0.8 s | 0.4 s | 48 | 320 | 1 | 0.4 | a new chapter, a title card, the opening hit |

Hard crash also keys `flash` to 0.55 for one frame on the switch (a single pale frame). Between
presets, scale the four numbers together; longer than 0.8 s or `slice` above 320 reads as a broken
file, not a transition. Keep one preset per kind of switch across a video, and Hard crash for one or
two moments at most.

`amt` is the envelope, keyed on 1/15 s steps with `hold` easing: a stutter in (up, back down, up),
1 on the frames either side of the switch, then a falling tail to 0. The tested Signal tear keys:
0.25, 0.55, 0.3, 0.8, 1, 0.9, 0.6, 0.35, 0.15, 0. Chroma blip is shorter (0.35, 0.8, 1, 0.85, 0.4,
0.15, 0); Hard crash holds 1 for two steps and has a longer tail. Smooth easing makes it a fade.

## Ask first

From the timeline and transcript, list the candidate switches (b-roll starts and ends, layout
changes, punch-ins, clip boundaries), then ask in one question, prefilled with what you found:

- **Where**: every b-roll change, every layout change, every clip boundary, or named moments.
- **Intensity**: one preset or a mix (Chroma blip on punch-ins, Signal tear on b-roll, Hard crash
  on the one chapter change). Default Signal tear.
- **Sound**: a glitch sound on each (default yes).

Skip the question if they have said all three.

## The switches and the words

- A glitch covers an instant change. Set every layout change it covers to `transitionStyle:
  "hardCut"`; a spring move under a glitch reads as mush. Adding a time-ranged b-roll layout also
  creates the layout after it with `spring`, so set that one to `hardCut` too.
- Skip switches less than about 1 s after another (let it hard-cut and say so), and any in the
  first or last 0.3 s of the video.
- The audio is untouched, so a stinger can sit over speech, but its peak should land between words
  or on the first word of the new thought, never inside a name or number. If a switch is mid-word,
  offer to nudge it to the nearest gap within 0.2 s.

## Building it in Tella Motion

Each stinger is its own overlay document, full frame, `depth: "front"`, no overlay `animation`,
starting at the switch minus the preset's switch point. Inside is one node: a full-frame `fill`
shape coloured `#00000000` with the shader added as a `backdrop` effect, so it filters the footage,
b-roll, layout and lower overlays beneath. Set the preset uniforms, key `amt` (and `flash`), and
bind `seed` to `floor(time × 15) + offset` so the pattern changes 15 times a second. No built-in
effect does the slice tear (`fx.chromaticAberration` only splits outward from the centre), which is
why it is a shader.

Build and check the first one, then `duplicate_motion_document` it for each further switch and
re-bind `seed` with a new offset (0, 37, 74, …) so no two tear the same way. Name them in order
("Glitch 02: Signal tear").

A switch **between two clips** takes two documents, since an overlay belongs to one clip: part 1 on
the outgoing clip, ending on its last frame, with the keys before the switch; part 2 on the incoming
clip from 0, with the rest of the keys shifted back and a first key holding the value in force at
the switch. Give part 2 a seed offset of part 1's plus the steps already played, so the pattern
carries on. Overlays work on Tella Motion clips too, so a glitch can tear into a title card clip.

What was hit:

- `addAdjustment` in an **overlay** only sees the overlay's own layers, so the footage is untouched
  (faint static and nothing else). An adjustment layer does work inside a Tella Motion clip or b-roll
  that contains both shots.
- `kind: "shader"` is refused inside `addAdjustment`'s `effects`; add the shape, then `addEffect`.
- Uniform paths on the backdrop shape have a doubled `effect`
  (`…/effects/0/effect/effect/uniforms/<name>/…`); take them from `inspect_motion_node_properties`.
- `duplicate_motion_document` with commands can return a null `result` although they applied;
  confirm with `inspect_motion_node` that the seed expression has the new offset.
- `setEffect` on a uniform keeps the keys. Changing the shader text means `removeEffect` and
  `addEffect`, then re-keying `amt` and re-binding `seed`.
- The shader scales by canvas height / 1080, so the presets hold at 4K and in portrait, but on 9:16
  use Chroma blip or Signal tear; Hard crash's slabs read as a blank frame on a phone.
- Very dark footage shows the slices less: go one preset up or raise `noise` by 0.1.

## Sound

Tella's curated `cyber-glitch` (912 ms) fits all three. Add it at each stinger's start, volume 0.5,
0.6 and 0.7 for the three presets, trimmed so it ends inside the clip. One sound for every stinger.

## Check

One `get_filmstrip` per stinger, every 1/15 s (the seed step) from 0.2 s before it to 0.2 s after,
plus the frame either side of the switch: clean picture
100 ms either side (no leftover static, colour shift or offset); it stutters in, peaks across the
switch with both shots torn and neither readable, no black or empty frame (Hard crash: exactly one
pale frame), no frame of the new shot before the peak, and the tail settles rather than snaps.

Keep flashes to a single frame at 0.55 or less and no more than two stingers in any 3 s, for viewers
sensitive to flashing. Report each stinger's time, preset and what it covers.

## Making it your own

- A brand-coloured split: mix the separated red and blue channels toward the brand's two colours.
- A clean "UI glitch": `blocks` 0, `noise` 0, `slice` 80. A dirtier VHS look: `noise` 0.3, `rgb` 40,
  `slice` 60.
- A glitch title: a Chroma blip on a title's entrance, so the words tear into place.
