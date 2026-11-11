# Claude Code in a macOS terminal: exact spec

Measured from a 2× screenshot of Claude Code in a dark macOS terminal and scaled by 1.13 so Roboto Mono 30 px matches its type; the window chrome is as the example video draws it now. Every coordinate is in canvas px at 1920×1080, relative to the window's top-left (`WX, WY`); the example puts the window at `WX 140, WY 70`, `WW 1640 × WH 940`. Bottom-pinned parts are measured up from the window's bottom edge so a taller or shorter window keeps them right.

## Grid

- Roboto Mono (`roboto-mono`), 30 px, `lineHeight: 1`. Advance 18 px, row pitch 38 px. A title's box `y` is the row top + 4; its cap top lands at box y + 3 and its baseline at box y + 29.5.
- Column `c` is at `WX + 43 + 18c`. Never wrap: the window holds about 86 columns.
- Weights: 400 body, 700 for tool names, the app name in the header and anything the app prints bold.

## Colours

| Role | Hex |
|---|---|
| Window body | `#292C33` flat, or the example's vertical gradient `#2A2D34` → `#25282E` |
| Window border (1 px) | `#3E4147` flat, or the example's gradient `#7C818C` 0 → `#545861` 0.03 → `#40434A` 0.5 → `#2E3036` 1 |
| Title bar | gradient `#3D414A` → `#30343C`, top to bottom |
| Window title text and ✳ | `#7C7C7C` |
| Traffic lights | `#E26657`, `#F4C11A`, `#5CBD1E` |
| Folder icon | `#457EE6` back, `#4F88EE` front, a white 1.6 px line across the top |
| Body text | `#FFFFFF` |
| Dim (version, model line, path, hints) | `#666666` |
| Secondary (⎿, tool results, elapsed time) | `#999999` |
| Placeholder in the prompt | `#949699` |
| Prompt rules | `#999999`, 2 px |
| Mascot | `#CA7C5E`, eyes `#000000` |
| Claude orange (spinner glyph and word) | `#D77757`, pulsing to `#EBA58B` |
| Success (tool dot, passing tests) | `#4EBA65` |
| Running tool dot | `#B8B8B8` |
| Accept-edits mode | `#AF87FF` |
| Plan mode | `#48968C` (teal; from the app's theme, not measured from a screenshot) |
| Bypass-permissions mode | `#9D3642` |
| Diff added / removed row | `#225C2B` / `#7A2936`, text `#FFFFFF` |
| Submitted prompt band | `#373A41`, its text `#E8E8E8`, its ❯ `#999999` |
| Link (`/model` style) | `#5B68EE` |

## Chrome (window coordinates)

- Window, bottom to top:
  - `winBorder`: rounded rect (0, 0, WW, WH), 26 px corners, filled with the border gradient. Two `dropShadow`s on it: black 0.38, dy 36, radius 90 (the soft one) and black 0.33, dy 6, radius 14 (contact).
  - `winEdge`: a 1 px stroke, black at 0.55, on a rect 0.5 px outside the window (26.5 px corners), so the window has a crisp dark outline on the light backdrop.
  - `winBody`: inset 1 px (25 px corners), the body colour or gradient.
  - `winTitleBar`: (1, 1, WW − 2, 69), top corners 25, bottom 0, the title-bar gradient. Under it a 1 px black 0.5 line at y 69 (`winTitleSep`) and a 1 px white 0.05 line at y 70 (`winTitleSepHi`).
  - `winBevel`: a 1 px stroke inset 1.5 px (24.5 px corners) with a white gradient top to bottom: 0.26 at 0, 0.12 at 0.02, 0.06 at 0.08, 0.04 at 0.9, 0.02 at 1. It catches light on the top edge like glass.
- Traffic lights: circles radius 13 centred at (35, 35), (79, 35), (123, 35). Each is filled with a radial gradient centred 7 px below its centre, radius 20: red `#E0746A` 0–0.2, `#E25C4F` 0.5–0.62, `#E87264` 1; yellow `#F6D054`, `#F0B500`, `#F1BC38`; green `#71C150`, `#4FB900`, `#6FC343`; plus a `dropShadow` black 0.25, dy 1, radius 1.5. On each a 1 px rim (radius 12.5) stroked with a vertical gradient from its light tint to its bright tint: red `#F7C7BD` 0.9 → 0.3 at 0.3, `#FF9E94` 0.35 at 0.6 → 1; yellow `#F7F682` / `#FFF272`; green `#BFF79B` / `#96E976`.
- Folder icon: tab 12×6 at (189, 21) r 2; back 31×23 at (188, 24) r 3.5; white line 25×1.6 at (191, 27); front 31×18 at (188, 29) r 3.
- Title (group `brand:title`): an eight-spoke asterisk centred at (242, 36), radius 10, four 2.4 px round-capped strokes at 0°, 45°, 90°, 135°; then `Claude Code` in Inter 600 27 px at box (261, 24).
- No toolbar, no tabs. The screenshot's terminal-app update badge is left out: it belongs to the terminal app, not Claude Code.

## Header (scrolls with the transcript)

- Mascot (group `brand:mascot`), origin (14, 115), unit 1.13 px (1.13 × the units below, so the body is 117.5 × 76.8 px); rects in units: body (16, 0, 104, 68); arms (0, 34, 136, 17); legs 8×17 at x 16, 32, 96, 112, y 68; eyes 8×17 at (32, 17) and (96, 17) in black.
- Text at x 206, box y 122, 160, 197: `Claude Code` bold white (group `brand:name`) with ` v<version>` dim at column 12 of that line; `<model> with <effort> effort · <plan>` dim; the project path dim.
- Body rows start with row 0's top at y 269 (two welcome lines in the example: bold white, then dim).

## Transcript rows

| Row | Build |
|---|---|
| Submitted prompt | a band (x 4, row top + 1, width WW − 8, 36 tall); ❯ at column 0 in secondary; text from column 2 |
| Tool call | ⏺ at column 0; tool name bold from column 2 (`Read`, `Update`, `Write`, `Bash`, `Search`); its argument in parentheses right after, regular |
| Tool result | ⎿ in columns 2–3; text from column 5 in secondary (`Read 48 lines`, `Updated <file> with 2 additions and 1 removal`, `Running…`) |
| Diff row | from column 5: the line number right-aligned in 4 columns, then the sign at column 10 and the code; `+` and `-` rows get a band from column 5 to 20 px before the window's right text edge, full row height |
| Bash output | as the tool prints it: a Jest-style ` PASS ` is a `#4EBA65` block 6 columns wide (row top + 3, 32 tall) with `PASS` bold black from the next column |
| Answer | a white ⏺ at column 0, text from column 2, continuation lines also from column 2 |

Leave a blank row between turns and between tool calls. Rows print instantly; only the answer streams (typewriter by word, 0.045 s apart).

## Pinned bottom (from the window's bottom edge, `B = WY + WH`)

- Spinner and effort row: top `B − 227`. Spinner at column 0, the word at column 2 (`Simmering…`), `(Ns · esc to interrupt)` at column 13 in secondary. At the right, ending 58 px inside the window, `● <effort> · /effort` in dim with a 12 px dot one column before the text.
- Rule 1 at `B − 168`, rule 2 at `B − 92`: x 4 to WW − 4, 2 px.
- Prompt row: top `B − 148`. ❯ at x 7, white; the input from column 0; placeholder `Try "<something>"` in the placeholder colour while empty.
- Cursor: a white block 18×36 at the row top + 1; the character under it drawn in the window colour, blinking with it.
- Status row: top `B − 74`. Two right-pointing filled triangles in columns 0–1, the mode name from column 3 (`accept edits on`), then `(shift+tab to cycle)` dim one column after it. Plan mode: a pause sign (two 4×16 rects in column 0) and `plan mode on` in teal. Bypass: the two triangles and `bypass permissions on` in `#9D3642`. The app's default mode prints no mode at all: `? for shortcuts` dim from column 0.
- The transcript viewport is masked from `WY + 80` to `B − 265`, so a blank row always separates the last line from the spinner row.

## Glyphs drawn as paths (Roboto Mono has none of them)

Coordinates relative to the cell's top-left (`x` = column x, `y` = row top).

| Glyph | Path |
|---|---|
| ❯ (prompt) | `M x+3 y+11 L x+10 y+20 L x+3 y+29`, stroke 4.2 white (2.4 in secondary for a submitted prompt), butt caps, miter join |
| ⏺ | circle 16 px centred at (x + 9, y + 21) |
| ⎿ | `M x+6 y+5 L x+6 y+22 L x+19 y+22` with x at column 2, stroke 2, secondary |
| Spinner ✻ | three 22 px strokes crossing at (x + 9, y + 20) at 90°, 150°, 210°, stroke 3.4, round caps; anchor at that centre; scale 0.55 ↔ 1 every 0.42 s (`easeInOutSine`) and rotation 30°/s |
| ⏵⏵ | two filled triangles `M x+1 y+12 L x+16 y+20 L x+1 y+28 Z` in columns 0 and 1 |
| ● (effort) | circle 12 px |
| ✳ (window title) | see Chrome |

`·` and `…` exist in Roboto Mono; use them as text.
