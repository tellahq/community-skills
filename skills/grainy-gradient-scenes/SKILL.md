---
name: grainy-gradient-scenes
description: Make 8-second scenes on slowly drifting, grainy gradients, either big title cards (an italic serif line with a huge sans-serif word) or thin outline diagrams whose dots, lines and labels draw in one by one. Use when the user asks for grainy gradient scenes, gradient title cards, or this soft, filmic gradient look for titles or simple diagrams.
metadata:
  title: Grainy gradient scenes
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/opening.webp
  preview: gallery/opening.mp4
  made-with: Remotion
  prompt: Make an opening scene in the grainy gradient style that says "Marketers need GitHub", and a closing one with "Build things people want."
---

# Grainy gradient scenes

Short scenes, about 8 s each, on a soft gradient that drifts slowly under a layer of film grain. Each scene is one of two kinds:

- **A title card:** a big headline, sometimes with one hand-drawn curve.
- **A diagram:** a short headline top left, and a simple outline drawing (documents, bubbles, a folder, a grid, a path) that draws in piece by piece.

`gallery/` has twelve examples, each an `.mp4` with a `.webp` poster. Watch the one closest to what the user wants before you build anything.

## The look

**Gradient.** Two or three large, very soft colour fields blend across the frame, with no hard edges and no visible centre. They drift a little over the whole scene (a few percent of the frame, slow and steady, never pulsing). A darker band low in the frame gives the text above it contrast. Use one palette per scene, and keep each palette for its kind of scene across a video. The palettes in the examples, sampled from the clips:

| Palette | Colours | Used for |
|---|---|---|
| Lilac to amber | `#3e4144` charcoal, `#94746e` lilac-brown, `#d9c3ad` cream, `#bea065` amber | Opening |
| Blue to butter | `#5b8ab4` blue, `#86a2bb` haze, `#bec8b4` pale butter, `#56889e` teal | Most diagrams, README |
| Green to lime | `#294d37` forest, `#5a7d5e` sage, `#ccd675` lime | Activity, contributions, repository, profile |
| Lilac to cream | `#b398d8` lilac, `#dac1bc` blush, `#b7b293` olive cream | Big-word typography |
| Warm orange | `#b6642d` rust, `#efbc8d` peach, `#565137` olive dark | Closing |

**Grain.** Fine monochrome noise over the whole frame, new every frame, faint (around 4–6 % strength) so it reads as film, not static. Grain sits above the gradient and under the text.

**Type.** Everything is a warm off-white (about `#f4ead2`), never pure white.

- The small headline is an italic serif in sentence case, one or two short lines, set top left with a generous margin (about 5 % of the frame). It is roughly 4 % of the frame height.
- The big word is a heavy grotesk sans in capitals, filling most of the frame width, with an italic serif line under or over it ("README / about you", "NETWORKING / matters").
- Two typefaces only: one italic serif and one heavy sans.

**Diagrams.** Thin outline strokes (about 1.5 px at 1080p) in the same off-white at about 70 % opacity, with no fills.

- Labels are a small sans, about 1.5 % of the frame height.
- Paths between things are dotted or hairline curves. A small glowing dot can travel along a path.
- Diagrams sit on the right half of the frame, or in the lower middle, clear of the headline.

## Motion

On an 8 s scene:

1. **0–0.8 s:** the headline comes in from a blur: it starts soft, at about 20 px of blur and 0 % opacity, and sharpens to crisp. The big word does the same, a beat after the serif line.
2. **0.8–5 s:** the diagram's pieces draw in one at a time, about 0.4–0.6 s apart. Strokes trace along their length, labels fade and blur in after their shape, and a travelling dot moves along its path at a steady speed.
3. **5–8 s:** everything holds while the gradient keeps drifting. There is no exit animation inside the scene; scenes cut or cross-fade to the next.

Use one calm ease-out throughout. Nothing bounces, overshoots or scales up from zero.

## Steps

1. Pick the example closest to the request, and look at it before building. Pull frames with ffmpeg, for example `ffmpeg -i gallery/network.mp4 -vf fps=2,scale=480:-1,tile=4x4 sheet.png`, and look at them with `view_image`. Note the palette, where the headline sits, and the order things draw in.
2. Get the words. Use the user's words, or the speaker's words from the transcript; never invent a claim, name or number. A headline is at most about seven words. If there are no words to use, ask.
3. Load `tella-motion-design` for the shared rules. Also load `tella-title-cards` for a title card, or `tella-explainer-graphics` for a diagram.
4. Build each scene in Tella Motion, as an 8 s clip, a b-roll or a full-frame overlay, whichever the user asked for:
   - **Background:** a full-frame shape with a `shader` effect (custom SkSL). It mixes the palette's colours through a few large, soft radial falloffs whose centres move slowly with time, then adds per-frame hash noise for the grain. Bind the drift and grain to time, and keep both subtle.
   - **Text:** live text nodes, never drawn in the shader. Animate the blur-in with a blur effect keyed from soft to sharp, and opacity from 0 to 1.
   - **Diagram:** path shapes for the outlines, with their stroke traced in (trim or stroke-end keyed from 0 to 1). Use small text nodes for labels, and a small circle with a soft glow for the travelling dot.
5. Check frames at about 0.4 s, 2 s, 4 s and 7 s with `get_clip_frame` against the example: palette, grain strength, type sizes, stroke weight, and the draw-in order. Fix what is off before going on.
6. For more scenes, `duplicate_motion_document` the finished one and change its words, palette and drawing, instead of rebuilding the shader and text each time.

## Making it your own

- Change the palette per section of a video, but keep the same palette for the same kind of scene.
- For a quieter look, drop the travelling dot and slow the drift. For more energy, shorten the gaps between pieces drawing in to about 0.3 s.
- Portrait or square videos keep the same layout rules: headline top left, drawing below it, with the big word sized to the frame width.
