---
name: tech-ey-explainer-diagrams
description: Make "tech-ey" explainer diagrams for the technical parts of a talk, one full-frame graphic per explanation that builds itself on white as the speaker names each part, with uppercase letter-spaced Roboto Mono labels, thin black outlines, dotted pipeline boxes, isometric cubes and slabs, and coloured wires. Use when the user asks for tech-ey, technical or flat isometric explainer graphics, diagrams of a workflow, pipeline or tool chain, or this clean black-on-white diagram look.
metadata:
  title: Tech-ey explainer diagrams
  author: Tella
  category: Diagrams
  image: og.jpg
  poster: gallery/agentic-editing.webp
  preview: gallery/agentic-editing.mp4
  video: claude-for-video-editing-motion-graphics-cufphmd9
  video-aspect: landscape
  video-start: "7.4"
  prompt: Make an explainer graphic in the tech-ey style for each of the technical parts of this video, at least 10.
---

# Tech-ey explainer diagrams

Full-frame diagrams on white that explain the technical parts of a talk: workflows, pipelines, tool chains, before and after, a chart of one moment. Each one is a small, flat, engineering-style drawing, like a figure in a well-made product doc: uppercase mono labels, thin black outlines, a few isometric cubes, and wires in a handful of bright colours. It builds up piece by piece as the speaker names each piece, then cuts back to them.

`gallery/` has twelve examples, each a `.webp` poster of the finished diagram and a short `.mp4` of it building. Look at the ones closest to what the user wants before you build anything.

## The look

**Canvas.** Plain white, full frame, with no texture and no gradient. A small centred mark of five dashes, `-----`, sits at the top (about 4 % down) on every graphic, so a set reads as one series.

**Type.** Roboto Mono only, in capitals, letter-spaced wide (about 0.15 em), in near-black `#111111`.

- The title, centred over the diagram or over the group it names, is medium weight at about 3 % of the frame height (`AGENTIC EDITING`, `ROUGH CUT`).
- Labels sit centred under their shape at about 2.2 % of the frame height. Headers over a group (`PDF`, `PIPELINE`, `TIMELINE`) are the same size.
- A note under a label is smaller (about 1.5 %) and coloured: red for a correction or a time (`AT EXACT TIMESTAMPS`, `PLACED 1:46`), purple for metadata (`TYPE: SOUND EFFECT`), amber for a result (`SAVED ONCE`), grey for something secondary or optional (`ASKED 1:50`, `+ MORE TOOLS`).
- Words only: no sentences. Text inside a shape is a short tag at most (`MP4`, `MEME`, `SILENCE`).

**Lines.** Every shape has a thin near-black outline (about 1.5 px at 1080p). Arrows are hairlines with a small solid head. A group of steps sits in a dashed rectangle (short dashes, same weight) with its title above. A loose, optional or "feeds into" link is a dotted line. A flow of different kinds of things is several parallel wires in different colours.

**Shapes.** Flat fills with outlines, from a small vocabulary:

- **Isometric cube** for an actor (the AI, a tool, an app): three faces of one hue, with the top light, the left mid and the right dark. A **slab** (a flat, wide cube) for a hub or service (a bot, an MCP server, a platform). A small cube can carry a symbol on its front face, like a play triangle for a video link.
- **Card**: an outlined square with a simple drawing inside, one per step in a row.
- **Picture**: a sky-blue rectangle with blue mountains and a yellow sun. Use it for any image, screenshot or photo.
- **Document**: an outlined page with grey text lines. A stack of offset pages for a PDF or many files.
- **Timeline**: a long bar or a row of segments, with tick marks under it. The highlighted segment is yellow.
- **Window**: an outlined rectangle with a title bar and three small circles, for an app or editor.
- **Person**: a circle head over a half-circle body, in blue or yellow.
- **Grid fill**: a yellow square with a fine darker grid, for "motion graphic" or "generated".

**Colour.** Black and white carry the drawing, and colour marks meaning, a few hues per graphic. Sampled from the examples:

| Colour | Hex (top / mid / dark face) | Used for |
|---|---|---|
| Orange | `#f7a659` / `#f0882d` / `#d96c14` | The AI, the main actor |
| Blue | `#5a81ff` / `#2256f2` / `#183dcf` | Tools, kept content, waveforms, timelines |
| Purple | `#6a3e9f` / `#4a1d7a` / `#30125c` | A bot or service in the middle |
| Yellow | `#ffdf79` / `#f6c946` / `#e8a91e` | Folders, highlights, the chosen moment |
| Red | `#d93a4a`, pale fill `#fad2d6` | Mistakes, things removed, corrections |
| Pink | `#d65ce0` | Filler words, memes, a third kind of thing |
| Green | `#4ecd87`, pale `#7ee1ab` | A fourth wire or tool |
| Sky | `#bee6f9`, lavender `#aebffe` | Pictures, screens, soft fills |
| Grey | `#c4c4c4` / `#8c8c8c` | Silences, placeholders, "more" |

For a scale (heat, intensity), ramp from dark brown `#3e130d` through maroon `#7c2024` and red to orange `#f08231` and yellow `#f5bf44`.

**Layout.** The diagram sits in the middle band of the frame (roughly 20 % to 75 % of the height) and reads left to right, or top to bottom for a short chain. Leave generous white space, and keep everything clear of the edges. Parts in a row share a size and a baseline, and their labels line up.

## Motion

Each graphic is b-roll for one explanation, timed to the transcript:

1. **Cut in** on the explanation's first word. The `-----` mark and the title (or the empty dashed box the steps will fill) fade in within the first 0.3 s, so the frame is never blank white.
2. **Each part arrives on the word that names it.** It fades in over about 0.35 s while rising about 10 px, with one calm ease-out, and its label comes with it. Parts appear where they stay: nothing moves once it has landed.
3. **Arrows and wires draw** from source to target (trim from 0 to 1 over about 0.4 s) just before the thing they lead to appears, so the eye follows the flow.
4. **Highlights come last**: segments light up in their colour, a crop rectangle tightens, a strike-through draws across a crossed-out name.
5. **Hold** the finished diagram for at least 1.5 s, then **cut out** straight back to the speaker, with no exit animation.

Nothing bounces, overshoots, spins or scales up from zero.

## Steps

1. Read the transcript and pick the explanations that have a shape: a sequence of steps, things flowing into a hub, a before and after, a moment on a timeline. Note each one's range and the words that name each part. If the user asked for a number ("at least 10"), find that many. Otherwise pick the clearest few, or ask.
2. Use the speaker's words for every label, cut to one to three words. Never invent a tool, name, number or claim. If the transcript is unclear (a mumbled product name), say which label you guessed.
3. Look at the gallery examples closest to each diagram. Pull frames with ffmpeg, for example `ffmpeg -i gallery/agentic-editing.mp4 -vf fps=2,scale=480:-1,tile=5x2 sheet.png`, and look at them and the posters with `view_image`.
4. Load `tella-motion-design` for the shared rules and `tella-explainer-graphics` for how to time and place a diagram.
5. Build the first graphic in Tella Motion at the video's size and frame rate:
   - A white full-frame rectangle at the back, the `-----` mark, then live text nodes in Roboto Mono for the title and labels. Never draw text into a shape or image.
   - Path shapes for outlines, cubes (three faces), slabs, arrows and wires, with dashed and dotted strokes for groups and loose links.
   - Key each part's opacity and position to the time of its word, and the trim of each arrow and wire.
6. Place it as b-roll over its explanation's range (`add_layout` with `media: {type: "motion", documentId}`), with hard cuts in and out.
7. Check frames with `get_clip_frame`: just after it cuts in, as two or three parts arrive, and the finished diagram. Compare with the gallery: type size and tracking, stroke weight, colours, alignment, and nothing clipped or overlapping. Fix what is off before going on.
8. For the next graphics, `duplicate_motion_document` the finished one and change its parts, keeping the mark, type styles and colours, instead of starting over. Name them in order ("Explainer 01 · Agentic editing").
9. Report each graphic with its start time and what it shows, and any label you guessed.

## Making it your own

- Attach a screenshot of a diagram style you like and name it in the prompt, the way the original prompt named "tech-ey". Attach a few more for colours and shapes to borrow.
- Swap the palette but keep each colour's job: one for the main actor, one for content, one for the thing in the middle, and red for what's removed.
- For a quieter set, use flat outlined boxes instead of cubes. For a denser one, add small coloured notes under labels.
- Portrait videos keep the same rules, with diagrams reading top to bottom.
