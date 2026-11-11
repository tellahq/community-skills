# Icon paths

Every icon is our own line drawing on a 24-unit grid (the glyph spans about 2 to 22). Place one with `addPath`
after mapping it to the canvas: with `size` the glyph size in px and `(cx, cy)` its centre, `sc = size / 20`, then
every x becomes `cx + (x - 12) × sc` and every y `cy + (y - 12) × sc` (arc radii × `sc`). A mirrored icon (thumbs
down) uses `24 - y` and flips each arc's sweep flag. `circ(cx, cy, r)` below is
`M cx-r cy A r r 0 1 0 cx+r cy A r r 0 1 0 cx-r cy Z`.

Stroke icons: `paint: "stroke"`, `cap: "round"`, `join: "round"`, 1.8–1.9 px at the sizes given in SKILL.md.

| Icon | Where | Path (24 grid) |
|---|---|---|
| home (fill) | rail, active tile | `M3 10.4 L12 3 L21 10.4 V19.6 Q21 21 19.6 21 H15.2 V15.4 Q15.2 14 13.8 14 H10.2 Q8.8 14 8.8 15.4 V21 H4.4 Q3 21 3 19.6 Z` |
| library / files | rail, tools tray | `M9 3.4 H17.6 Q20.6 3.4 20.6 6.4 V14.6 M6.4 7.2 H14.6 Q17.2 7.2 17.2 9.8 V18.4 Q17.2 21 14.6 21 H6.4 Q3.8 21 3.8 18.4 V9.8 Q3.8 7.2 6.4 7.2 Z` |
| clock | rail | `circ(12,12,9)` + `M12 6.8 V12 L14.6 14.6` |
| agent / plugins | rail, tools tray | `circ(12,12,9)` + `circ(12,12,3.6)` + `M15.6 12 V13.2 Q15.6 15.6 18 15.6` |
| apps grid | rail | four rounded squares: `M5 3 H9 Q11 3 11 5 V9 Q11 11 9 11 H5 Q3 11 3 9 V5 Q3 3 5 3 Z` and the same at (13,3), (3,13), (13,13) |
| search | sidebar header | `circ(10.4,10.4,7.2)` + `M15.6 15.6 L21 21` |
| collapse sidebar | sidebar header | `M6 3.6 H18 Q21 3.6 21 6.6 V17.4 Q21 20.4 18 20.4 H6 Q3 20.4 3 17.4 V6.6 Q3 3.6 6 3.6 Z M9.4 3.6 V20.4` |
| new chat | sidebar | `M11 3.6 H6.6 Q3.4 3.6 3.4 6.8 V17.4 Q3.4 20.6 6.6 20.6 H17.2 Q20.4 20.6 20.4 17.4 V13 M17.6 2.8 Q18.6 1.8 19.6 2.8 L21.2 4.4 Q22.2 5.4 21.2 6.4 L13.4 14.2 L9.6 14.8 L10.2 11 Z` |
| chat bubble | top right | `M12 3 A9 9 0 1 1 4.6 17.2 L3.4 20.6 L7.2 19.6 M4.6 17.2 A9 9 0 0 1 12 3` |
| plus | composer | `M12 3 V21 M3 12 H21` (stroke 2) |
| chevron | model picker | `M6 9 L12 15 L18 9` |
| mic | composer | `M12 2.5 Q15.2 2.5 15.2 5.7 V11.3 Q15.2 14.5 12 14.5 Q8.8 14.5 8.8 11.3 V5.7 Q8.8 2.5 12 2.5 Z M4.8 10.8 A7.2 7.2 0 0 0 19.2 10.8 M12 18 V21.6` |
| folder | tools tray | `M2.8 6.4 Q2.8 4 5.2 4 H9.2 L11.6 6.4 H18.8 Q21.2 6.4 21.2 8.8 V17.6 Q21.2 20 18.8 20 H5.2 Q2.8 20 2.8 17.6 Z M2.8 9.6 H21.2` |
| monitor | tools tray | `M5 4 H19 Q21.4 4 21.4 6.4 V14 Q21.4 16.4 19 16.4 H5 Q2.6 16.4 2.6 14 V6.4 Q2.6 4 5 4 Z M8.4 20.6 H15.6 M12 16.4 V20.6` |
| copy | action row | `M15.6 8.4 V6 Q15.6 3.6 13.2 3.6 H6 Q3.6 3.6 3.6 6 V13.2 Q3.6 15.6 6 15.6 H8.4 M10.8 8.4 H18 Q20.4 8.4 20.4 10.8 V18 Q20.4 20.4 18 20.4 H10.8 Q8.4 20.4 8.4 18 V10.8 Q8.4 8.4 10.8 8.4 Z` |
| thumbs up (down = mirrored) | action row | `M7.6 10.4 V20.4 M7.6 10.4 L11.2 3.6 Q13.8 3.6 13.8 6.2 V9.4 H18.4 Q20.8 9.4 20.4 11.8 L19.2 18.4 Q18.8 20.4 16.8 20.4 H7.6 M7.6 10.4 H4.6 Q3.6 10.4 3.6 11.4 V19.4 Q3.6 20.4 4.6 20.4 H7.6` |
| share | action row | `M12 14.6 V3.6 M7.6 8 L12 3.6 L16.4 8 M4.8 12.4 V18 Q4.8 20.4 7.2 20.4 H16.8 Q19.2 20.4 19.2 18 V12.4` |
| regenerate | action row | `M19.8 12 A7.8 7.8 0 1 1 17.4 6.4 M19.8 3.2 V7.6 H15.4` |

Drawn directly in canvas px (no grid):
- **Voice button**: a 54 px circle `#3C66BF` with five white vertical strokes 2.4 px, round caps, at x offsets −8, −4, 0, 4, 8 from its centre and lengths 5, 11, 16, 9, 5.
- **Send button**: the same circle with a white arrow, stroke 2.6: `M c c+11 V c-12` and the head `M c-9.5 c-2.5 L c c-12 L c+9.5 c-2.5` (c = the centre).
- **Stop button**: the same circle with a white 15 px rounded square (radius 3) in the middle.
