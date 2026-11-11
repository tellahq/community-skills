# Generated deck or your own photo

For Deck = `Generated` or `My own photo`. The timing and look are the same as Tella's deck; only the layers differ.

## Generated deck

`generate_image` (default model), prompt as used in the test build. It gave a clean, unbranded, square-on deck on black in one try:

> Studio product photo, exact top-down orthographic view looking straight down at a generic unbranded direct-drive record turntable, centred in frame. A black 12-inch vinyl record with fine concentric grooves and a soft radial light sheen sits on a dark metal platter whose outer rim has a ring of small strobe dots. Plain pure white paper centre label with a small chrome spindle. The tonearm rests on its post at the right side of the deck, swung out away from the record, with a slim silver S-shaped arm and a black headshell. Matte black plinth, no logos, no text, no brand marks, no buttons with lettering. Single soft overhead spotlight, everything else falls off to pure black background. Photorealistic, sharp, high detail.

Then `decompose_image` on its `sourceId` (seedream-5.0-pro, about a minute):

> Split out only two elements: the whole tonearm assembly (the pivot base with its counterweight, the curved silver arm and the black headshell with its cartridge) as one layer, and the white centre label with the chrome spindle as another layer. Leave the plinth, platter, strobe-dot rim and black vinyl record in the plate, with the plinth filled in where the tonearm was.

What came back (2048×1152 source): the plate with the label area filled in dark; a 472×1601 tonearm layer with `box` {left 0.67, top 0.068, width 0.128, height 0.775}; and a label layer that was slightly oval (not used). In that plate the spindle was at (925, 549), the record's radius 450 px and the platter's outer edge 497 px. The pivot was the round chrome boss at (250, 320) in the arm layer and the stylus tip at (85, 1560). With the plate scaled 0.9375 and centred, the arm layer goes at x 1379, y 98, 246×833, pivot (1509, 265). Rest −8° and play 19° put the stylus 400 px from the spindle (record radius 422). Your own numbers will differ: read them off a gridded copy of the plate and the arm layer.

Your own photo: upload it (`create_source` `kind: 'image'`, PUT), then run the same `decompose_image` prompt on it.

## Building from the plate

1. `addMedia` the plate, then `node.patch` its `destination` so the spindle lands on (960, 540). For a 2048×1152 plate: x = 960 − spindleX × 0.9375, y = 540 − spindleY × 0.9375, 1920×1080.
2. Rim: `addMedia` the plate again with the same destination, `setMasks` to an annulus: first an `add` ellipse at the platter's outer edge, then a `subtract` ellipse 2 px outside the record (test build: r 470 minus r 424, both centred on (960, 540)). Anchor it at (960, 540) and give it the label's rotation keys for the whole clip (there is no separate blurred ring; its motion blur does the smear). Don't spin the plate itself: its sheen would turn with it.
3. Label: draw it, since the decomposed label comes out oval. A disc r 142 `#F1EEE6` and the two titles as in SKILL.md, grouped as `label`, anchor (960, 540); a 24 px `#BDBDC2` spindle on top.
4. Arm: `addMedia` the arm layer, patch its `destination` to where the decompose `box` put it (scaled like the plate), anchor at the pivot. Find the play angle by rotating the stylus point about the pivot (positive = clockwise) until it is the record's radius − 20 px from the centre; rest about 27° outside it. For the shadow use the node's own: shadowX/Y/Blur/Opacity lifted (22, 30, 18, 0.45) → resting (7, 10, 6, 0.75) over the touch.
