---
name: retro-footage-looks
description: >-
  Give a stretch of the user's own footage a retro look in Tella: VHS home
  video (chroma bleed, tracking wobble, tape noise, camcorder PLAY/date OSD),
  CRT screen (curved glass, scanlines, vignette, glow, power-on and static),
  halftone print (CMYK dot screens on paper), or photocopier (toner threshold,
  grain, misfeed jitter, 8 fps stepping, scan-bar entry). Built as an
  editable Tella Motion document that re-plays the clip's own source with a
  custom shader stack, placed as b-roll over just the chosen time range. Use
  when asked for a VHS look, camcorder or tape effect, old TV / CRT / retro
  monitor look, scanlines, halftone or comic-dot print look, photocopy /
  xerox / zine look, or to make part of a video look vintage or lo-fi.
metadata:
  title: Retro footage looks
  author: Tella
  category: Editing & effects
  image: og.jpg
  poster: gallery/vhs-home-video.webp
  preview: gallery/vhs-home-video.mp4
  prompt: Make 0:04 to 0:12 of my clip look like it's playing on an old CRT TV, switching on at the start and cutting to static at the end.
---
# Retro footage looks

Four treatments for the user's **own footage over a time range**. Outside the range the clip plays clean. Inside it, the same frames come back through a shader stack. The clip keeps playing underneath, so audio and lip sync never change; only the picture is swapped.

| Look | What's in it | Entry / exit | Good on |
|---|---|---|---|
| **VHS** | luma softening, chroma bleed, tracking band, head-switch noise along the bottom, tape grain, camcorder OSD | tracking wobble settles over 0.8 s, a short tracking pop later | handheld, lifestyle, "home movie" moments |
| **CRT screen** | barrel-curved glass in a dark bezel, scanlines that bloom in highlights, RGB triad, vignette, rolling band, flicker, glow | a line opens into the picture with a flash; channel-change static, then a hard cut | archive footage, "as seen on TV", flashbacks |
| **Halftone print** | CMYK dot screens at 15/75/0/45° on warm paper, misregistration, fibre, ink specks | big dots resolve into the photo, and grow back out at the end | product shots, objects, bold shapes |
| **Photocopier** | toner threshold with grainy edges, speckle, drum streaks, misfeed jitter with black edge wedges, 8 fps stepping, pasted-on labels copied too | a green-white scanner bar sweeps down, copying the footage | talking heads, people, zine/punk titles |

The shader sources and uniform ranges are in `references/shaders.md`. They are the look (`list_motion_effects` has nothing like them): use them as written, and read the file before building.

## Ask

If the request doesn't say, ask in one go: which look; which range (default a 4–9 s stretch starting on a cut or a pause); subtle or strong (VHS `noise`, CRT `scan`, halftone `cell`, copier `level`); for VHS the OSD date (default a plausible 90s date); for the photocopier an optional label (a zine title plus a name). Keep a range to about 10 s at most. Retro looks tire quickly, and clean footage either side makes the effect read as a choice. Don't stack two looks on one range; to go from VHS into CRT, use two back-to-back ranges with a hard cut.

## Build

An effect on an overlay doesn't reach the video (overlays render in isolation), so replay the clip's own source (`list_sources`) in a Tella Motion document as long as the range, and lay it over the range as b-roll with a hard cut.

- Start the media node at the range start through `sourceIn`, in **source** time and in ticks (1 s = 254016000000; add the clip's trim), with `fit: "cover"`. If the clip's base layout is padded (`middle`), switch it to fullscreen first so clean and treated parts frame the same.
- Add the shader with `addEffect` `kind: "shader"`, bind `time` to seconds and key the animated uniforms linearly.
- When the look should treat extra layers too (VHS OSD, copier label), group them with the footage and put the shader on the group. Keep titles outside the halftone: halftoned text turns dotty.
- Speech stays as it is. No tape hiss or static unless asked, and then one short effect from `list_library` sound effects (or `generate_sound_effect`) on the power-on or static.
- Several ranges: build one, then `duplicate_motion_document` (a document plays in one place only) and re-point `sourceIn` and the duration.

### Per look

**VHS** (`vhs` on a group of footage plus OSD). Start at `bleed 10, noise 0.07`. Key `tracking` 1 → 0.15 at 0.5 s → 0 at 0.8 s, with a 0.6 pop around 3.2 s. OSD in `roboto-mono` 600, `#F4F4EE`, letter-spacing 0.06: "PLAY" (60 px) with a drawn triangle top left, "SP" top right, time and date (56 px) stacked bottom left, all about 120 px in from the edges at 1080p. PLAY and SP leave around 3.2 s; time and date stay on, like a real camcorder.

**CRT** (`crt` on the media node, then a built-in `glow`: radius 28, threshold 0.62, intensity 0.55, softness 0.45). Start at `curvature 0.06, scan 0.36, lines 180`. Key `power` 0 → 1 over the first 0.35 s; `snow` 0 at L−0.4 s, 0.9 at L−0.15 s, 0.7 at the end. The hard cut back from static reads as a channel change. Don't power off mid-video: clean footage straight after a dying tube looks wrong.

**Halftone** (`halftone` on the media node, no time binding). Start at `cell 12, amount 1, misreg 2`. Key `cell` 48 → 12 over the first 0.7 s and back to 48 over the last 0.7 s; `amount` 0 → 1 over the first 0.15 s and 1 → 0 over the last 0.15 s.

**Photocopier** (`copier` on a group of footage plus label). Set the media's `sampleGrid` to 8 fps. Start at `level 0.33, jitter 1`; key `scan` 0 → 1 over the first 0.6 s. The optional label is a white rect (about 580×132) with a 58 px `space-grotesk` 700 black title and a 28 px `roboto-mono` subtitle, near a dark corner away from the face. Start it at 0.75 s so it never shows clean while the bar sweeps.

**Vertical canvases** work, since every shader reads `resolution`: move the OSD and label into the safe area and lower CRT `lines` to about 160. For a variant (ink colours, paper tint, step rate), change one constant at a time and check each at full size.

## Gotchas

- Key a uniform by the `field:` path `inspect_motion_node_properties` lists after `addEffect`: the effect index in it is the storage index, not always the stack position.
- A shader's source can't be changed in place: remove the effect, add it again, then re-bind and re-key, since the paths can move.
- Adding the b-roll layout also creates a follow-on layout with a `spring` transition, which shows as a dark dip after the effect. Set it to `hardCut`.
- `sampleGrid` is a **rate** (numerator/denominator frames per second): 8 fps is `{8, 1}`. `{1, 8}` is one frame every 8 s, runs past the end of the source and makes every later frame fail (`thumbnail_fetch_failed` from that time on).
- Roboto Mono has no ▶ glyph and renders it as nothing; draw the triangle as a path.
- When editing a shader: square with `x*x`, not `pow(negative, 2.0)` (undefined on the GPU: streaks and 20 px jitter), and keep the sin-free hash; `fract(sin(…) * 43758.5)` breaks down at 1080p coordinates.
- Fine detail doesn't survive scaling: scanlines 160–220, halftone cells 10 px or more, grain blocks 2–3 px.
- Thresholds depend on the footage: try two copier `level` values side by side; a mid-tone scene floods black at 0.5. Dim archive footage relies on the halftone's built-in lift, or it prints solid black.

## Check, at full size

- `get_motion_frame` at 1920 wide on a calm moment, and look at a 480×270 crop at 2×: scanlines, dots and grain are judged at pixel level, not from a thumbnail.
- One `get_filmstrip` of the clip across the range edges (just before, the first 100 ms, the middle, the last 300 ms, just after) and through the entry and exit: the treated footage starts on the same frame as the clean shot, nothing fades dark after the range, tracking settles, the power-on and static land, the dots resolve, the copier steps.
- To debug a shader, disable it (`setEffect` `enabled: false`) and return intermediate colours from a throwaway copy.
