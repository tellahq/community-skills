---
name: light-leak-transitions
description: >-
  Add warm film light leaks and film burns at cuts in a Tella video: a soft,
  grainy flare of light sweeps across the frame for about a second, blooms to a
  bright wash right on the cut and fades out, screen-blended over the footage so
  the switch hides inside the flare. Built procedurally in Tella Motion (one
  SkSL shader on a full-frame shape with blend mode screen, no stock files), in
  amber, rose or teal colourways or a custom one. Use when asked for light leak
  transitions, film burns, light flares or lens flares between shots, a "light
  spot" or flash transition, or a warm, filmic way to hide cuts.
metadata:
  title: Light leak transitions
  author: Tella
  category: Transition screens
  image: og.jpg
  poster: gallery/amber-golden-hour.webp
  preview: gallery/amber-golden-hour.mp4
  prompt: Add amber light leak transitions at the cuts between my b-roll shots.
---

# Light leak transitions

A light leak is the flare you get when light reaches the film: big soft blobs of warm colour slide in from one side, burn almost to white for a moment, and drift off. Used as a transition, the brightest moment sits exactly on the cut, so the eye never sees the switch. The footage keeps playing under it; nothing is cut or crossfaded.

It builds on `tella-transitions` (when a transition is worth it, never on a word) and `tella-motion-design`. This skill only covers the leak itself.

`references/light-leak.sksl` is the shader, and it is the look. Pass its whole text as the effect's `source`; don't retype or "improve" it.

## The look

- **Shape.** Three large, soft, noise-warped blobs travel together across the frame in one direction, the lead one biggest. Fractal noise warps their edges so they billow and read as light, not shapes. Nothing has a hard edge.
- **Peak.** At the middle of the leak an extra wash (`coverage`) lifts the whole frame, so for 2–4 frames the picture is mostly light. That is where the cut goes.
- **Colour.** Three colours per colourway: `deep` at the faint edges, `mid` for the body, `hot` for the burnt core. Hot is always tinted, never pure white.
- **Grain.** Fine 2 px grain at 40 steps a second, only inside the light. The footage's own grain is untouched.
- **Blend.** `screen`. The shader returns opaque black where there is no light, which leaves the footage exactly as it was: no edges, no darkening.

| Colourway | deep | mid | hot | Suits |
|---|---|---|---|---|
| Amber | `[0.62,0.16,0.02,1]` | `[1.0,0.52,0.12,1]` | `[1.0,0.92,0.72,1]` | Golden hour, warm interiors, people; the default |
| Rose | `[0.54,0.08,0.19,1]` | `[1.0,0.36,0.42,1]` | `[1.0,0.94,0.88,1]` | Black-and-white and archive film, nostalgic, romantic |
| Teal | `[0.0,0.16,0.20,1]` | `[0.16,0.58,0.60,1]` | `[0.86,0.97,0.92,1]` | Blue hour, night, water, tech, cool grades |

Colours are linear 0–1 RGBA (`half4` uniforms). For a custom colourway use the user's colour as `mid`, a darker, more saturated version at about 55 % brightness as `deep`, and a pale tint of it as `hot`. One colourway per video unless asked.

## Settings that worked

| Uniform | Value | Notes |
|---|---|---|
| `progress` | 0 → 1, linear, over the leak | The shader eases itself: in over the first 35 %, out over the last 35 % |
| `seed` | different per cut (3.1, 7.4, 11, 5.3…) | The same seed twice in a row looks repeated |
| `angle` | one per video: -15 (left to right, rising) or 200 (right to left) | Keep the direction of travel |
| `strength` | 1.0; 0.85–0.95 on dark footage | Blob brightness |
| `coverage` | 0.55 on bright footage, 0.75 on dark or night (screen only brightens) | Lower and the cut shows at the peak; above 0.85 it turns into a white flash |
| `grain` | 0.05; 0.04 on dark footage | |

**Length:** 1.2 s per leak, centred on the cut (starts 0.6 s before it). The light is visible for about 0.9 s. Use 1.0 s for fast edits and 1.6 s for a slow, dreamy piece; the peak always sits at the middle.

## Choosing the cuts and asking

A leak suits a change of place, time or mood: a montage, an intro into the story, a chapter change, a memory. Not every cut. Find candidates from the timeline (clip boundaries, b-roll in and out, layout changes) and the word timings, skip cuts less than about 1.5 s apart, and keep the peak off a word.

Ask once, in one form, prefilled with your picks:
- **Colourway:** Amber / Rose / Teal / Custom, picked from a frame of the footage (warm → amber, monochrome or archive → rose, cool or night → teal).
- **Which cuts:** a checklist of the cuts you found with their times, the suitable ones ticked.
- **Strength:** Subtle (`coverage` 0.45, `strength` 0.8) / Normal / Burn (see below).

## Building it in Tella Motion

Each leak is its own overlay document of the video at the canvas size: one full-frame black `fill` shape with the shader (`kind: shader`) as its only effect, `blendMode` `screen`, and `progress` keyed linearly across the document. Place it full-frame, depth `front`, no overlay animation. Build and check the first one, then copy it per cut with `duplicate_motion_document`, changing only `seed`. Name them "Light leak · <colourway> · <time>".

**A cut between two clips.** An overlay can't run past its clip's end (`add_overlay` silently shortens it), so split the leak: a 0.6 s document keyed 0 → 0.5 ending at the outgoing clip's end, and a 0.6 s document keyed 0.5 → 1 at the start of the incoming clip, with the same seed, angle and colours. The shader depends only on `progress`, so the halves meet without a seam. Set the incoming clip's transition to `hard_cut`; a smooth clip transition fights the leak. A cut inside one clip (b-roll, a layout change) takes one 1.2 s overlay.

## Gotchas

- **Blend mode works through overlays.** `screen` on the shape composites onto the video underneath, so the shader returns black where there is no light. Don't fake it with alpha.
- **Keying uniforms:** each uniform value is its own property (`inspect_motion_node_properties` lists the paths); a colour is four values, so set each channel.
- **To change the shader,** remove the effect, add it again and re-key `progress`; the keys go with the effect.
- **Keep the arithmetic hash.** A `sin`-based hash makes blocky square patches on the GPU at full-HD pixel coordinates.
- **The grain is in the shader,** only inside the light; don't stack a grain effect on the shape.
- An inset layout shows the leak over the padding too. That's fine, but fullscreen footage looks best.

## Check

- One `get_filmstrip` from about −450 to +400 ms around each cut, dense near it (−33, 0, +33 ms): clean footage at the ends, a blob entering from the travel side, the frame mostly light at the peak with both shots barely visible, the light leaving the far side. If either shot reads clearly at ±33 ms, raise `coverage` by 0.1; if the peak frames are flat white, lower it.
- One full-size frame about 250 ms before the cut: soft billowing edges, no banding, no square blocks, grain fine and only in the light.
- A video preview over each leak ±1 s: one smooth sweep in, a bloom, one sweep out, no pop where the overlay (or the two halves) start or end.
- Read the overlays back: one per cut (two at a clip boundary), named, none overlapping.

Report each leak's cut time, colourway and seed.

## Making it your own

- **Film burn:** `coverage` 0.85, `strength` 1.2, `hot` pushed to `[1.0,0.97,0.9,1]`. On bright footage the frame burns to warm white for about 4 frames, orange at the edges. For the start of a montage or a flashback, once per video.
- **Accent, not transition:** a 1.6 s leak at `coverage` 0.2 over a held shot on a key word (the title, the reveal). No cut needed.
- **Sound:** offer a soft whoosh or projector flutter from the curated sound effects (`list_library`, else `generate_sound_effect`), peaking on the cut, at low volume.
- **Portrait:** the shader works at any size; keep the document at the video's canvas size.
