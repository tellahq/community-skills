---
name: graphics-calculator-screen
description: >-
  Make a retro graphing-calculator screen in Tella Motion, a close-up of a
  green-grey dot-matrix LCD in a dark plastic bezel. The screen flickers on
  with a status line, a ticking clock and a stack of values, works a formula
  step by step (a busy hourglass, intermediate results, a constant typed in
  with a block cursor), settles on the result, then switches to a plot. The
  axes appear, the curve draws itself across the screen, and a trace cursor
  runs along it with its coordinates read out at the bottom. Every glyph and
  line is resampled onto a 5 px dot grid with dot shadows, glass reflections,
  a light sweep, ghosting and grain. Built as its own clip or as b-roll over
  the line that explains the maths. Use when asked for a calculator screen, a
  graphing calculator, a TI or HP style LCD, an RPN stack, a formula being
  worked out, showing a calculation step by step, plotting a function or a
  curve on a retro screen, a dot-matrix display, or a nerdy maths or physics
  explainer beat.
metadata:
  title: Graphics calculator screen
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/calculator-pendulum.webp
  preview: gallery/calculator-pendulum.mp4
  tags: calculator, lcd, dot matrix, retro, formula, maths, physics, plot, graph, rpn, explainer, shader
  prompt: Show the pendulum formula T=2π√(L/g) being worked out on an old graphing calculator for L = 2.5 m, then plot the swing.
---

# Graphics calculator screen

A 10 s close-up of a graphing calculator. The left half of the beat works a formula on an RPN stack and lands on the result. The right half plots a curve that follows from it and traces it with live coordinates. All of it reads as one real, slightly worn LCD: dark ink dots on green-grey glass, each dot casting a shadow. Use it as its own clip (an explainer beat or a cold open) or as b-roll over the sentence that gives the formula. It builds on `tella-motion-design` (timing, checks) and `tella-explainer-graphics` (a graphic that builds as it is said). Load those first. The calculator UI is invented, with no maker's name or logo.

## Ask once

Work these out yourself and never ask: the formula, its variable values and the result from the transcript or the message; every intermediate step (do the arithmetic); the six soft-key labels (unit menus such as `LENG AREA VOL TIME SPEED MASS` for physics, `STAT REGR PLOT` style for data); the clock and status line; the plot's scales.

Then one `ask_form`, every field prefilled, so the user can just submit:

1. **Formula** (text, required): as typed on a calculator, e.g. `T=2*π*√(L/g)`, at most 30 characters (π and √ count as two). Prefill from the transcript.
2. **Values** (text, optional): up to 3 as `name=value_unit`, comma-separated, e.g. `L=2.5_m, g=9.80665_m/s^2`. Empty shows the formula and the result alone.
3. **Result** (text, required): prefilled with your own answer, 12 significant digits plus the unit, e.g. `3.17241164155_s`, at most 20 characters. If you can't compute it (a symbolic formula), prefill from the transcript and say so.
4. **Function to plot** (text, required): `y=` an expression in `x`, at most 30 characters. Prefill with the curve the result implies (the pendulum's swing `0.25*cos(2π*x/3.172)`), else `sin(x)`.
5. **Screen tint** (pick): Classic green-grey (default), Amber, Blue.
6. **Length** (slider, 6–16 s, default 10).
7. **Where** (pick): Own clip (default) or B-roll over the speaker.

If the user skips the form, build with the prefilled values. Nothing needs media from the user. Sound is optional: soft key clicks and a beep from the curated library (`list_library` sound effects, `add_sound_effect` on the video), never in the document.

## Timing

The video's 10 s run, in seconds. For another length, stretch the holds (the result hold and the trace) and keep the typing (0.07 s a character) and busy blips fixed.

| When | What |
|---|---|
| 0–0.23 | Boot: the screen group's opacity hold-keys 0 → 0.3 (0.1) → 0.7 (0.17) → 1 (0.23). |
| 0.1–0.9 | Status line, clock, `{ HOME }`, rule, menu tabs. Stack: formula on 4, values on 2 and 1. |
| 0.9–1.1 | Stack empties to its labels, hourglass on (0.9–1.15). |
| 1.1–2.3 | First step (L/g) on 1, formula on 3; hourglass again at 1.8, then the next step (√) at 1.95. |
| 2.3–3.6 | The stack shifts up a row and a constant (`6.28318530718`, 2π) types into the command line, 0.07 s a character, the block cursor stepping with it, then blinking 0.15 s on/off. |
| 3.6–3.8 | Labels only, hourglass (3.6–3.85). |
| 3.8–5.0 | Result on 1, formula on 2. Hold it. |
| 5.0–5.15 | Blank screen. Axes at 5.15, curve wipes on 5.3 → 6.8. |
| 6.85 | Plot menu `ZOOM (X,Y) TRACE FCN EDIT CANCL`. At 7.3 `TRACE` becomes `TRAC` with a lit 25 px box, the trace cross appears at the origin. |
| 7.6–end | Menu gone, readout `(x, y)` bottom left. The cross steps along the curve every 0.04 s to x = 6.25 at 9.7 s, then holds. |

As b-roll, the result lands on the word that says it (or the end of the sentence), and the plot starts as the speaker moves to what it means. A b-roll layout lives in one clip (`add_layout` takes a `clipId`, its times on that clip's timeline), so keep the shot inside the clip where the words are said: shorten it or start it earlier. Only when the spoken range truly crosses a cut, split it there: one document per clip (`duplicate_motion_document`, the second starting on the frame the first ended on, keys on each clip's own clock), each `add_layout` `transitionStyle: "hardCut"`. Then check with `list_layouts` that the layout after each b-roll is a hard cut too. The split is untested.

## The look

- **Canvas** 1920×1080, 30 fps. Screen window `[260, 165, 1400, 750]`, 10 px corner radius: 280 × 150 dots of 5 px.
- **Colours**, by tint: content ink / LCD base / pixel `ink` uniform. Classic `#1A2630` / `#B4C394` / [0.08, 0.12, 0.17, 0.95]. Amber `#2B170A` / `#D9A04A` / [0.17, 0.09, 0.03, 0.95]. Blue `#0B1838` / `#9CB4C8` / [0.04, 0.09, 0.22, 0.95]. Bezel `#2A2D30`.
- **Type**: DotGothic16 (Google Fonts, OFL) 80.9 px, letter spacing −0.45, line height 1. That gives exactly 40 px (8 dots) a character and 35 characters a row. π and √ are full-width (80 px). Left text at x 277.28. Right-aligned values at x = 1642.28 − 40 × width-in-cells.
- **Rows** (text top y): status 178.37 (`RAD  XYZ  HEX  R= 'X'` left, clock `09:41:` + seconds + `A` at x 1282.28), path 253.37 (`{ HOME }`), a 5 px rule at y 335 (x 270–1650), stack levels 5:–1: at 353.37, 443.37, 533.37, 623.37, 713.37 (labels `5:` … `1:` at the left).
- **Menu tabs**: inverse, six 220 × 95 rects at y 815, x = 275 + 230 i, filled with ink. The label is drawn in the LCD base colour at x = tab + 7 + (5 − n) × 20, y 828.37. A 50 × 10 notch at y 800 sits over each tab that is a folder.
- **Cursor**: a 35 × 65 block at (280, 715), stepping 40 px a character.
- **Plot**: axes, curve, cross and hourglass are dot paths. Their numbers and the curve recipe are in `references/dot-paths.md`.

## Building it in Tella Motion

1. **Font.** `list_library` `type: 'font'` for DotGothic16. If it's missing, download `https://github.com/google/fonts/raw/main/ofl/dotgothic16/DotGothic16-Regular.ttf`, then `create_source` `kind: 'font'`, PUT the file to its `uploadUrl`, and `add_library_item`.
2. `create_motion_document` 1920×1080, the chosen length. Paint order, bottom to top, all inside a `device` group: `lcdbg` (full-frame fill + `lcdtex`), `screen` group (every text and dot path, with `lcdpix` then a `frameAverage` effect `backward` 3, `forward` 0, `interval` 1/30 s for the LCD's ghosting, then the boot opacity keys), `glass` (transparent full-frame fill + `glassfx`), `bezel` (full-frame fill + `bezelfx`). On `device`, in order: `camera`, `fx.chromaticAberration` 1.5, `fx.vignette` (amount 0.45, size 0.42, softness 0.55, black), `fx.addGrain` (intensity 0.05, size 1.3, monochrome 1, seed bound to floor(time × 30)). All shader sources and uniforms are in `references/lcd-shaders.md`.
3. **Stack states.** Each state is its own set of titles with a start and an end (labels and values), never edited text. Format numbers the calculator way: 12 significant digits, a leading `.` under 1, units after `_` (`.254929053244_s^2`). The formula stays in quotes one level above the working values and drops a level as they are used up.
4. **Typing**: `setTextAnimation` typewriter on the command-line title (0.07 s stagger, near-zero duration, from start) and hold keys on the cursor's x, 40 px per character.
5. **Clock**: `bindProperty` `text` to floor(time + 12) with prefix `09:41:` and suffix `A`.
6. **Plot**: the curve's `fx.linearWipe`, the cross's keys, the `trT` curve and the bound readouts are in `references/dot-paths.md`.
7. As its own clip, `create_clip` with the document. As b-roll, `add_layout` with Tella Motion media over the line.

## Checking it

`get_filmstrip` of the document at 0.15 (boot), 0.5, 1.0 (hourglass), 3.0 (typing), 4.5 (result), 6.0 (curve half drawn), 7.4 (TRACE selected) and 9.0. Then one full-size `get_motion_frame` at 4.5 and at 9.0. Look for: values not right-aligned to x 1642 (a π or √ counted as one cell), text overflowing 35 cells, a gap in the curve on its steep parts, the cross off the curve, a readout that disagrees with the cross, and light text inside a tab that doesn't read as unlit dots. Check every number against your own arithmetic and report the formula, the steps and the result.

## Gotchas

- Text must be dark on the screen: `lcdpix` lights only dark pixels and paints them in its own `ink`. A grey or anti-aliased colour comes out patchy.
- Off-grid shapes light two dots or none. Snap every rect and path to multiples of 5.
- The dot shader works on what's under the `screen` group only. Keep `glass` and `bezel` outside it or the bezel turns into dots.
- `glassfx` and `camera` need `time` bound, or the sweep and push freeze.
- 9:16 is untested. Keep the window inside the frame and re-lay the rows, not the dot size.

## Variations

- Skip the plot for a pure calculation (5–6 s), or skip the stack and open on the plot.
- A slight tilt: `camera` `yaw` 0.12 and `pitch` −0.08.
