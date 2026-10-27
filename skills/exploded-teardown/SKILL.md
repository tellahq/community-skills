---
name: exploded-teardown
description: >-
  Build an animated exploded-view / teardown of a physical object as an editable
  Tella Motion clip (or overlay/b-roll): an isometric line drawing draws itself
  on, explodes into its parts along assembly axes, leader lines and typewriter
  labels name each part, the object turns slowly while holding, labels retract
  and the parts reassemble. Best from technical drawings (PDF or SVG, then
  raster images), but also works from plain text descriptions, product photos,
  renders or video frames of the object. Use when asked for a teardown, exploded
  view, "how it's made"/"what's inside" animation, or to explode a product into
  its components.
metadata:
  title: Exploded teardown
  author: Grant Shaddick
  category: Diagrams
  tags: exploded view, teardown, isometric, line art, product, hardware, technical drawing, labels, how it's made, what's inside
  image: og.jpg
  poster: gallery/teardown.webp
  preview: gallery/teardown.mp4
  video: untitled-video-hj0vh8im
  video-aspect: landscape
  prompt: Make an exploded-view teardown of the product in this video, with a label for each part.
---
# Exploded view / teardown animation (Tella Motion)

The result is a 10-second Tella Motion clip on near-white paper (`#fafafa`) with fine dark ink lines (`#1d1d1f`, 1.2 px):

1. **0.15–1.3 s:** the assembled object draws itself on in isometric view (trim-path lines, pale fills fade in).
2. **1.8–2.9 s:** parts slide apart along their assembly axes, staggered by 0.04 s. Top-of-stack parts go up, bottom parts go down, side parts move out sideways.
3. **2.95–4.6 s:** thin leader lines (anchor → 24 px knee → column) draw out, and Roboto Mono 13 px uppercase labels type in. Left and right columns sit clear of the drawing.
4. **4.6–10 s:** the whole exploded object turns slowly about its vertical axis (0° → 15°). Leaders follow their parts.
5. **7.75–8.15 s:** labels fade and leaders retract.
6. **8.2–9.1 s:** parts slide back together. The assembled object holds to the end, still turning.

`references/example_exploded.jpg` is a frame of the finished look (Apple Watch Ultra 3).

Everything is built by `scripts/explode.py` from a small Python **model file** you write per object. `references/example_watch.py` is a complete, working model; copy it as your starting point. The script writes paste-ready command batches for `tella__apply_motion_editor_commands`, plus a PIL preview so you can check the geometry before sending anything.

## 1. Understand the object from what you were given

Work out the parts, their real dimensions (mm) and how they stack. Use the best source available:

- **PDF or SVG technical drawing (best).** Copy the skill scripts into the sandbox. Then:
  - Read the vectors: `profiles.pdf_polylines(path, page)` / `profiles.svg_polylines(path)`, then `profiles.closed_outlines(...)`.
  - Run `profiles.overview(polys, 'ov.png')` and `view_image` it. Each outline is numbered, so you can see which one is the top, front or side view of which part.
  - Get the scale from a dimensioned length. Read dimension text with `pymupdf` `page.get_text('words')` and compare it with that feature's length in PDF units.
  - Convert outlines with `profiles.to_mm(poly, units_per_mm)` and `resample_closed(..., n)`. Use top-view profiles as extrusion outlines and side views for thicknesses and heights.
  - Also read the drawing's callouts and notes: they give you label names and hidden internal parts.
- **Raster drawing, photo or render.** Trace with `profiles.raster_outlines(path)`, then `view_image` the source and `overview(...)` to pick outlines. Set the scale from a stated dimension or the product's known real size (search the spec sheet if needed). Simplify photo outlines to clean primitives (`rrect`, `circle`, `ellipse`) wherever the shape allows; traced noise looks bad as line art.
- **Video or footage of the object.** Pull frames (`get_filmstrip` / `get_source_thumbnail` / `get_clip_frame`) and treat them like raster images.
- **Text description only.** Look up real dimensions and internal layout if it's a real product (spec sheets, teardown reports). Otherwise use plausible proportions. Decompose into canonical layers: for example glass / display / frame / board / battery / back for a device, or cap / body / mechanism / base for a pen or bottle. Build everything from primitives.

If the parts or how they split is genuinely unclear, give the user a short part list (names, order, which one gets the accent colour) and ask before building. Otherwise proceed.

## 2. Plan the explode

- Use **4–10 parts** and one main stacking axis (z, vertical). Layers stack along z; buttons, crowns and ports move out along x or y.
- **Explode offsets (mm):**
  - Visible gaps between layers should come out roughly even on screen; roughly 3–5× the part thickness reads well.
  - The core part (case, body, frame) stays at `(0,0,0)`.
  - The example uses glass `+52`, display `+30`, case `0`, battery `−32`, back `−58` (z), crown `+20` (x), action button `−26` (x).
- **Order `EXPLODE` top of stack first:** the order is the stagger order.
- **`DRAW`** lists only the parts visible when assembled, with a start time and duration for each. Inner parts get no draw-on: they're hidden behind white fills and are revealed as the stack opens.
- **One accent colour on one meaningful part** (the example's action button is `#ff6a2b`). Other fills are pale greys: `#fafafa`, `#f1f1f1`, `#ececec`, `#e2e2e2`, `#cfcfcf`, `#c9c9c9`.
- **`LABELS`:** 6–10 entries, uppercase. Each anchor is a 3D point on the assembled part (mm). Use side `L`/`R` by which side of the drawing the anchor is on; the script stacks each column 30 px apart.

## 3. Write the model file (copy `references/example_watch.py`)

Units are mm, z is up. `P()` projects isometrically and applies the current yaw. `prism(part, outline2d, plane, k0, k1, ...)` extrudes an outline:

- plane `xy` gives a horizontal slab from z=k0 to z=k1.
- plane `yz` gives something sticking out along x (the visible cap is at the larger x).
- plane `xz` gives something along y.

`cylinder(...)` is for crowns, knobs and lenses, and `clipped(...)` draws detail lines that stay inside a face.

Rules (the script asserts some of them):

- **Painter's order.** In `build()`, append parts back to front: the bottom of the stack and far-side parts first, top layers and near-side parts last. Inside a part, draw the silhouette fill, then its outline, then the near cap. White fills hide what's behind them, which is how hidden lines disappear.
- **Point counts must not change with yaw.** Every outline needs a fixed vertex count: `rrect(n)`, `circle(n)`, `resample_closed(n)`, silhouettes through `radial(M)`, detail lines through `clipped(K)`. Decide anything visibility-dependent (which knurl lines show, which face is visible) at yaw 0 and keep it fixed.
- **Rotate only about z, and keep the total turn ≤ ~20°.** Faces that are hidden at yaw 0 are never drawn.
- **`VIEW`:** set `scale` (px per mm) so the fully exploded stack fills about 75–80% of the 1080 px height, centred at 960×540.
  - Labels sit in columns: left labels end at x = `lcol` (640), right labels start at `rcol` (1500). Override both in `TIMELINE` if the drawing is wider.
  - Keep total stack height × scale + label rows on screen.
- **Overrides.** An optional `TIMELINE = {...}` overrides any key of `TL` in `explode.py`: timings, `yaws` / `yaw_t`, `ink`, `paper`, `stroke`, `font_size`, columns. For a blueprint variant, set `paper` `#1b4f8f` and `ink` `#eaf3ff` and give parts darker blue fills. Set `yaws: (0,0,0)` for no turn.

## 4. Generate and preview

```
mkdir -p /workspace/teardown && cp -r $HOME/.agents/skills/exploded-teardown/scripts $HOME/.agents/skills/exploded-teardown/references /workspace/teardown/
cd /workspace/teardown/references && python3 ../scripts/explode.py my_model.py --out ../out --preview
```

The script prints the batch files and `out/preview_sheet.png`, which shows frames at 0.5 / 3.5 / 7.5 / 9.8 s. `view_image` the sheet. Fix overlaps, wrong stacking order, uneven gaps or parts running off frame, and re-run until it's clean. To check the turn, temporarily call `render(model, t, path)` at a few times.

## 5. Put it in the video

1. Make the target:
   - Its own scene: `tella__create_clip` with `type: 'motion'`.
   - Over existing footage: `tella__create_motion_document`, then place it with `add_overlay` (`motionDocumentId`) or `add_layout` (`media: {type:'motion', documentId}`).
2. Apply each `out/batch_N.json` in order with `tella__apply_motion_editor_commands`.
   - Pass `baseRevision` = the `seq` returned by the previous call (start with 0 on a new document).
   - `cat` each file and pass its JSON array as `commands` unchanged.
   - Batches are about 38k characters; send them one by one.
3. To change the timing or motion later, edit the model or `TIMELINE`, regenerate, rebuild into a **fresh** clip or document, then delete the old clip and reorder. Never retime an existing document in place (moving nodes and re-keying): it has broken view-page and export playback before.

## 6. Verify

- `get_filmstrip` on the clip at 800, 2400, 4500, 6000, 7500, 8100, 8700 and 9900 ms. Check: drawn → exploded → labelled → turned → labels gone → reassembled.
- `get_clip_frame` at ~6000 ms at 1280 px wide. Check that leaders touch their parts and labels don't collide.
- `get_clip_preview` (10 s, 640 px) and `show_media` it to the user. Ask them to confirm playback on the view page or in an export.

## Gotchas (learned the hard way)

- **10 s limit.** Tella Motion clips are 10 s; `canvas.set` doesn't lengthen the clip. Build the timeline to fit.
- **Easing names are a fixed list.** `setPath` (and most keyframe) easings accept only `linear`, `hold`, `easyEase`, `easyEaseIn`, `easyEaseOut`, `easeInOutSine`, `easeInOutCubic`, `easeInOutExpo`, `easeOutCubic`, `easeInCubic`, `easeOutBack`, `easeInOutBack`, `springGentle` and `springBouncy`. `easeInSine` is rejected.
- **No dots in effect ids.** The script uses `tr_<node id with dots → _>`.
- **≤ 200 nodes per group.** The script asserts it; split a huge part.
- **Morph keys need identical point counts.** The script asserts it across yaws.
- **Use ≥ 3 yaw keys.** Points morph linearly between keys; two keys far apart make the turn shrink slightly mid-way. The default 0 / 7.5 / 15° is fine.
- **Lateral offsets turn with the yaw.** The script re-keys group x/y over the turn; z offsets don't need it.
- **`setSpeed` doesn't work on groups.** Never try to speed or retime a finished build; rebuild instead.
- **Clip Style.** If the user sees rounded corners or a "Glass" border around Tella Motion clips, they must set Style → Shape: square and Border style: None in the editor. The API refuses clip style edits on Tella Motion clips.

## Files

- `scripts/explode.py`: geometry primitives (`P`, `rrect`, `circle`, `ellipse`, `resample_closed`, `lift`, `prism`, `cylinder`, `clipped`, `radial`), the timeline (`TL`), the command builder, batch writer and PIL preview. CLI: `explode.py model.py --out DIR [--preview]`.
- `scripts/profiles.py`: reads outlines from PDF, SVG and raster references and converts them to mm.
- `references/example_watch.py`: a complete model (Apple Watch Ultra 3, from Apple's case-design PDF dimensions). Copy and adapt it.
- `references/example_exploded.jpg`: the target look, mid-turn with labels.
