---
name: flower-transitions
description: >-
  Add Louise's "flower transitions" to a Tella video: grainy, retro kaleidoscope
  motion-graphic stingers (wavy mint/purple stripes, blue flower blooms, flower
  grids, plus pink, orange, violet and wavy-ring remixes) that wipe across the
  full frame at every layout change (camera ↔ split, etc.), fully covering the
  switch, as transparent video overlays 2.4s long. Use when asked for flower
  transitions, kaleidoscope/stripes/bloom transitions, or motion-graphic
  transitions between layouts.
metadata:
  title: Flower transitions
  author: Louise de Sadeleer
  category: Transition screens
  image: og.jpg
  poster: gallery/bloom-wave.webp
  preview: gallery/bloom-wave.mp4
  video: wavy-flower-motion-graphics-2tkkbmzz
  video-aspect: landscape
  prompt: Add flower transitions at every layout change in this video.
---
# Flower transitions

Full-frame motion-graphic transitions that cover each layout change. Each one is a transparent ProRes 4444 overlay (1920×1080, 30 fps): the graphic wipes in with a shaped mask, covers the whole frame, and wipes out again. The layout switch happens underneath while the frame is covered. The camera footage itself is never touched. Grain and retro texture stay on the graphics only.

## The set (8 designs, rotated)

They are saved in the user's private media library. Find them with `list_library` (`scope: 'private'`, `type: 'video'`) by name, all starting with "Flower transition –". Use each item's `sourceId`, and never guess IDs.

1. Stripes iris: wavy mint/purple stripes in a flower-shaped (8-petal) circle that opens and closes.
2. Bloom wave: blue flower bloom in a wavy left-to-right wipe.
3. Grid tiles: the 3×3 flower grid, built tile by tile on a diagonal.
4. Pink stripes blinds: stripes in pink and orange, as staggered horizontal blinds.
5. Warm bloom iris: orange and pink bloom in a 6-petal iris.
6. Stripes+bloom diagonal: the bloom keyed over the stripes, in a diagonal wipe.
7. Rings wave: new wavy concentric rings in the stripes palette, in a right-to-left wavy wipe.
8. Violet grid tiles: violet flower grid, with tiles popping in randomly.

`gallery/` has a short clip and a poster of each design as it looks over a real layout change. Watch them to see which design is which.

Each design comes as a 2.4s version (the default). Pink stripes blinds and Warm bloom iris also have 1.6s versions for tight spots.

## Steps

1. `get_timeline` with `layouts` (and `overlays`). List the moments where the layout really changes: camera-only ↔ side-by-side/split, fullscreen ↔ framed camera, and so on. Sort the layouts by start time first, because the list is not in order.
   - Skip punch-ins (a camera-only section with `punchIn: true` is emphasis, not a layout change). Treat the change out of a punch-in into a different layout as a change.
   - Skip b-roll boundaries by default. B-roll must end with a hard cut back to the speaker, so never put a transition on a b-roll exit. Offer b-roll entries as an option.
   - Skip changes in the last second of the video.
2. Placement. Each 2.4s transition fully covers the frame from about 1.0s to 1.3s into it. Start it at `switch − 1133 ms` so the switch falls in the middle of the full cover. For a 1.6s version, start it at `switch − 750 ms`.
3. Overlap check. When two neighbouring 2.4s transitions would overlap (layout changes less than about 2.4s apart), use the 1.6s versions there. If even those overlap (changes under about 1.6s apart), keep one transition and let the other change hard-cut, and say so.
4. Rotate the 8 designs in order (1→8, then repeat) so no two in a row look alike.
5. Add them all in one `apply_video_edits` batch: `add_media_overlay` with `point {xPct: 0, yPct: 0}` and `dimensions {width: 1920, height: 1080}` (the canvas size). Name each one "Transition – <design>". Leave `transition`/`animation` unset, because the alpha channel does the wipe.
6. Verify with one `get_filmstrip` around the first 3–5 switches (before, mid-in, at the switch, mid-out, after). Check that the frame is fully covered at the switch and transparent before and after.
7. To change the length later, render new files (below) and swap them in one batch: remove the old overlays, then add the new ones. `update_overlay` can't change the source.

Offer as follow-ups: a whoosh on each transition, b-roll entries, and leaving very quick sections as hard cuts.

## Rendering new versions (other length, canvas size or colours)

Use `scripts/gen.py`. It needs numpy (`pip install --break-system-packages numpy`) and ffmpeg.

1. Download the three source graphics into `$WORKDIR` (default `/workspace/flower-transitions`) as `stripes.mp4`, `bloom.mp4` and `grid.mp4`. Use `get_source_thumbnail` with `format: 'mp4'`, the full `durationMs` and `width: 1072`, then curl the URL. The original sources are "wavy stripes kaleidoscope" (`su_cmvi5vnx3009i08jk1ip831cn`, 11.4s), "flower bloom pulse" (`su_cmvi5vpt500kx02rm5nd9hl11`, 7.7s) and "flower grid" (`su_cmvi5vqzt001j02rvbjsw2pvl`, 4.1s). All are 1072×1080. If these sources aren't reachable, ask the user to attach the three clips again. Never use the bloom clip's first 0.5s: it shows player UI.
2. Run `NF=<frames> W=<width> H=<height> python3 gen.py [variant…]`. 72 frames gives 2.4s, 48 gives 1.6s, 24 gives 0.8s. Files land in `$WORKDIR/out<NF>/`. The full cover runs from frame round(NF·10/24) to round(NF·13/24)−1. Start the overlay at the middle of that window, converted to ms, before the switch.
3. Before uploading, look at a contact sheet. Composite a few frames over a solid colour with ffmpeg and `view_image` it.
4. Upload with `create_source` (`kind: 'video'`, width, height, duration) and `curl -T file.mov "<uploadUrl>"`. Upload several in parallel, then `wait_for_jobs` on the sources.
5. Save the new files to the library with `add_library_item`, using the same "Flower transition – <design> (<length>)" naming.

Keep the look: grainy, slightly pixel-stepped kaleidoscope patterns in mint/teal/lavender/blue, with remixes made by hue-shifting (pink/orange about +150°, warm about +170°, violet about +60°), mirroring, or keying one graphic over another. Mask shapes are petal irises, wavy wipes, tiles, blinds and diagonals. Masks animate in with an ease-in and out with an ease-out (cubic).
