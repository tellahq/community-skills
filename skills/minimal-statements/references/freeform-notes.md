# Freeform notes (learned building this set)

- Canvas: `create_freeform_document` with width 1920, height 1080, a descriptive name. One document per graphic.
- Paste the script's commands literally into `apply_freeform_editor_commands` (read the output file with read_file; one command per line keeps lines under 2000 chars). Tool arguments are never run through a shell.
- `addTitle` only takes weight 400-700: the scripts add `setProperty field:content/style/fontWeight` for 300/500.
- A title's line box is fontSize x 1.2 tall; `box.y = centreY - fontSize x 0.6` centres it. The `x`/`y` properties are offsets from the box, so key moves as offsets from the final layout.
- Text widths: variable Inter measured with PIL at opsz 14 matches Tella's renderer within a few px (common.py downloads the font).
- Never put two keys at the same time on one property (keys() in common.py merges them).
- `group` puts the group at its topmost member's paint position: create nodes in back-to-front order, or fix with `node.move {node, index}` (index counts from the back).
- `node.patch {common:{transformParent:"L"}}` makes a node follow another's moves (the corner dots ride on the braces).
- Text colour animates with setKeyframes on `color` using #rrggbb values.
- Images: `asset.set {kind:"images", asset:{id, source:{type:"uri", uri}, dimensions}}` then `node.insert` a raster node. The uri is a library item's `url`: import mymind/Pinterest saves with `add_library_item {from, sourceId: item id, scope:"video", videoId}`; for an uploaded source, `add_library_item {sourceId}` returns its url. A mymind copy can fail with a retryable error: retry once, then pick another image.
- `duplicate_freeform_document` with commands once returned an error but had applied: re-read with get_freeform_document before retrying.
- Freeform b-roll must be placed with `add_layout`, one call each (`apply_video_edits` rejects freeform media).
