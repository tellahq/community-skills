---
name: logo-mask-reveal
description: >-
  Reveal the video through a brand's logo in Tella: the user's SVG logo sits
  over a solid plate, optionally plays an intro animation (spin, pop, fade,
  rise, drop or none), then scales up toward one of its shapes (the "window")
  until that shape fills the frame. The window turns into a hole, so the video
  and layers below show through it while the rest of the logo flies off the
  edges. Built as an editable Tella Motion overlay with motion blur. Use when
  asked for a logo mask reveal, a logo reveal / logo intro / logo transition
  into the footage, or to zoom through a logo into the video.
metadata:
  title: Logo mask reveal
  author: Grant Shaddick
  category: Transition screens
  image: og.jpg
  poster: gallery/logo-intro.webp
  preview: gallery/logo-intro.mp4
  video: logo-mask-reveal-intro-fvzpgp90
  video-aspect: landscape
  prompt: Open this video with a logo mask reveal of my logo (SVG attached), spinning in and then zooming through it into the footage.
---
# Logo mask reveal

The core of this effect: **one shape of the logo becomes a window onto what's below.** The logo sits on a solid plate that hides the video, scales up with an ease-out toward that shape until the shape covers the frame, and the shape turns from solid to a hole, revealing the clip (and any layers under the overlay). The rest of the logo flies off the edges. The real clip plays underneath, so audio and lip sync are untouched.

An intro animation before the reveal is optional. The logo keeps the colours in its SVG: there's no glow, gradient mesh or other brand treatment added.

## 1. Ask for the logo and the animation

1. Run `tella_sessions__list_sessions` (house rule), then `get_timeline` for the canvas size and clips.
2. **Get an SVG.** If the message doesn't carry an `.svg` (attachments are staged under `/workspace/.eve/attachments/…`; from a connected local folder use `local_folder` read), ask for one with an open `ask_question`: the logo as an SVG file, with each part as its own shape. A PNG/JPG won't work: the window has to be a real vector shape. Don't trace a raster logo unless the user asks.
3. **Find the shapes** in the sandbox:
   ```
   pip install --break-system-packages -q svgelements svgpathtools numpy pillow
   S=$HOME/.agents/skills/logo-mask-reveal/scripts/build_reveal.py
   python3 $S /path/logo.svg --list --preview /workspace/lr/parts.png
   ```
   It lists every visible shape (index, id, fill, bbox) and draws a preview with each shape numbered. `view_image` it. To show it in the form, upload it (`create_source` kind image with its size, `curl -T`, then `get_source_thumbnail` with that `sourceId` for an https URL).
4. **Ask in one `ask_form`:**
   - **Window shape** (choice): one option per sensible shape, labelled by index and what it is ("4 – square"), each with the preview as `imageUrl`. Pre-select the best candidate: a compact, chunky shape (square, circle, a solid letter) reveals well; thin strokes, small dots and outlines don't. A letter's counter (the hole in an "O") only works if it is its own shape in the SVG.
   - **Intro animation** (choice, `multiple`): None, Spin, Pop (scale in with overshoot), Fade in, Rise in, Drop in. Default Spin + nothing else. Say they can describe something else instead.
   - **Spin turns** (number 0.5–4, default 2), only meaningful with Spin.
   - **Plate colour** (text, default `#FFFFFF`): the solid colour behind the logo before the reveal.
   - **Where** (choice): start of the video (default), or the playhead / another moment (e.g. a transition into a section).

## 2. Build

1. `create_motion_document` with `videoId`, named "Logo mask reveal".
2. Generate the batch:
   ```
   python3 $S /path/logo.svg --window <index|id> --width <W> --height <H> \
     --intro spin[,fade|pop|rise|drop] --turns 2 --background '#FFFFFF' --out /workspace/lr
   ```
   Timing options: `--intro-end` (0.75 s; the intro's length), `--hold` (pause before the reveal; 0.3 s by default with no intro), `--reveal` (0.8 s zoom), `--window-fade` (0.35 s for the window's fill to clear; 0 opens it at once), `--rest-size` (logo size at rest as a fraction of the frame's shorter side, 0.18), `--cover` (1.12: how far past the frame the window ends), `--motion-blur` (1/45 s; 0 = off).
   The script picks the zoom target itself: the centre of the largest frame-shaped rectangle inside the window, and the end scale that makes it cover the frame, so circles, triangles and odd shapes still fill the screen.
3. `apply_motion_editor_commands` with `commandsFile: /workspace/lr/commands.json` and the document's `seq` as `baseRevision`.
4. For an intro the presets don't cover, edit the keys after the batch with `setKeyframes` / `editKeyframe` on the transformed groups (all of them identically, see below). Keep the reveal keys from the reveal start onward untouched.
5. `add_overlay` on the clip: `motionDocumentId`, `startTimeMs` (0 or the chosen moment, clip-local), `durationMs` = the duration the script prints, `point {0,0}`, `dimensions` = the full canvas, depth front.

## 3. Check

- One `get_filmstrip` over the overlay's range at about 70 ms, plus a full-size `get_video_frame` mid-reveal: the window should be clear with the footage visible inside it, the logo's other shapes intact (no clipped corners), and the frame fully footage at the end with no plate edge.
- Report where it lands and that the plate covers the footage (and the speaker's first words) until the reveal; offer to start the reveal earlier or place it over a pause.
- If the script warned about gradient fills, tell the user they were replaced by grey and rebuild them with `node.patch` `{paint: {source: {type: 'gradient', gradient: {type: 'linear', start, end, tileMode: 'clamp', stops}}}}` on those paths.

## Node structure (for tweaks)

- `plate` = `bg` (full-frame plate colour) + `logo.below` (logo shapes painted before the window in the SVG). It has an **alphaInverted matte** of `hole`, which holds `h.window` (a copy of the window shape), so only the window cuts through to the video.
- `window` = `w.fill`, the window drawn in its own colour; its opacity fades out at the reveal.
- `logo.above` = shapes painted after the window (sits outside the matte, so it's never cut).
- `logo.below`, `hole`, `window` and `logo.above` carry **identical** anchor (canvas centre), scale, x, y, rotation and motion blur. Edit them together or the hole slides off its shape. `hole` stays at opacity 0 until just before the reveal, then switches on while `w.fill` still covers it.

## Gotchas

- Scale and opacity are fractions (scale 2 doubles, opacity 0.5 is half).
- Motion blur `shutter` is in ticks (254016000000 per second): 1/45 s ≈ 5644800000. A value like 180 does nothing.
- A matted or grouped layer is clipped to the canvas rectangle in its own local coordinates. The script draws the logo at 100% fitting inside the canvas and shrinks it with the scale property, so nothing gets cut. Don't redraw paths outside the canvas.
- `x`/`y` are offsets from the anchor; changing the anchor doesn't move a node at rest.
- The zoom is sampled in log-zoom space (9 keys, `continuous` easing) with position linear in scale, so the target glides to the centre. A plain ease-out on linear scale feels like a jump cut.
- `setMasks` on a group didn't clip blurred children; use track mattes (`setMatte`) for any extra clipping.
- `addPath` colours are `#rrggbb` only; alpha goes on the node's opacity (the script does this).
