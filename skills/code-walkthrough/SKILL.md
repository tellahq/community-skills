---
name: code-walkthrough
description: >-
  Step through a code change in Tella on an editor-style code panel built in
  Tella Motion: a rounded panel with a filename tab, line numbers and syntax
  colours, where each beat of the narration is one step. Lines that move slide
  to their new place, new lines fade in on a green bar, removed lines flash red
  and collapse, changed lines roll from old text to new, and the lines being
  talked about stay lit while the rest dim. Input is a code snippet, several
  versions of it, or a diff. Works as full-frame b-roll, as a panel beside a
  speaker, or as a standalone clip, in a dark, light or warm theme. Use when
  asked for a code walkthrough, animated code, a code diff animation, code
  b-roll, highlighting lines of code as they're explained, or showing a
  refactor step by step.
metadata:
  title: Code walkthrough
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/midnight-diff.webp
  preview: gallery/midnight-diff.mp4
  prompt: Walk through this diff as b-roll while I explain it, one step per change, in a dark theme.
---

# Code walkthrough

A code panel that changes as the speaker talks, one step per beat. "Every call hits the network" lights line 2 and dims the rest; "so we cache notes by id" slides the function down, fades four green lines in and rolls `const note` into `const note: Note`; "one lookup instead of two" flashes the old `if` line red, collapses it and drops two new lines into the gap. Everything is live Tella Motion text and shapes, so any line, colour or time can be edited afterwards.

Builds on `tella-motion-design` and `tella-explainer-graphics` (b-roll over an explanation's range). This skill adds the panel, the line diffing and the step animation. Needs the Tella Motion tools.

## Get the code and ask

- The code is in the message or an attachment (a snippet, several versions, a diff or a PR patch), or on screen in the recording: read it from a full-size frame crop and type it out exactly. Never invent code, names or values; if a line is unreadable, ask.
- Find the stretch where the speaker explains it, and inside it the words that name each part or change ("the fetch here", "so we add a cache").
- Ask once with `ask_form`, prefilled: the **code** as you have it, so they can correct it; the **steps**, one per line as `time · lines or change · note`; the **theme** (Midnight, Paper, Ember, or a brand accent); **where** (full-frame b-roll by default, a panel beside the speaker, or a standalone clip); the **filename** for the tab.

## Plan the steps

- One step per beat, 1.5 s or more each, one idea per step: either a focus move or one change (add, remove or rewrite a few lines), never both.
- At most 12 lines (10 or fewer reads best), about 50 characters per line at b-roll size, 36 beside a speaker. Cut imports and boilerplate, keep the real indentation, and say what you trimmed.
- Step 1 shows the starting code whole. A focus step lights the lines being said. A change step lights its own new lines through their green bars.
- Footer notes use the speaker's words, two to five. Leave them out if the voice carries it.
- Match old and new lines with a line diff. A replaced line that is still clearly the same line (about 60 % alike or more) rolls in place; anything less alike is removed and re-added, since a diff pairs replaced lines by position and unrelated pairs morph oddly.

## The look

- **Panel**: radius 18, sized to the code, centred for b-roll. Shadow y 28, blur 70, opacity 0.55 (0.16 on Paper). Full-frame b-roll sits on a soft radial backdrop: a lighter glow a little above centre falling off to the dark edge colour.
- **Tab bar** (line step × 1.14 tall, a shade darker than the panel): the active tab in the panel colour with a 3 px accent line on top, a small mono badge (`TS`, `PY`, `JS`, `$_`) in the accent, the filename in Inter 500 at 0.78 × the code size, an optional dimmed second tab, and one small dot per step on the right, the current one lit.
- **Code**: Roboto Mono 400, 34 px on a 60 px line step for b-roll (line step ≈ 1.75 × size); 26–28 px beside a speaker, never under 26 at 1080p. Line numbers right-aligned in a gutter about 2.4 × the font size wide, dim until their line is focused.
- **Focus**: a rounded bar (radius 10) in the accent at about 12 % with a 4 px accent edge on the left; unfocused lines drop to about 32 % opacity.
- **Diff**: added lines get a full-width bar in green at about 14 % with a 4 px green edge and a `+` in the gutter; removed lines the same in red with `−`. Keep green and red even on a brand accent.
- **Footer** (line step × 0.93 tall, the tab-bar colour): the step's note on the left in Inter 500 at 0.66 × code size, the language name on the right, dim.

| Theme | Backdrop glow → edge | Panel | Text | Keyword | String | Number | Function | Type | Punct | Accent | Added | Removed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Midnight | `#1E2A55` → `#0B1020` | `#0F1521` | `#D6DEEB` | `#C792EA` | `#ECC48D` | `#F78C6C` | `#82AAFF` | `#7FDBCA` | `#8A99B8` | `#7AA2F7` | `#2FBF71` | `#F0506E` |
| Paper | `#FFFFFF` → `#EEF0F4` | `#FFFFFF` | `#24292F` | `#A626A4` | `#B4540A` | `#0550AE` | `#4F5BD5` | `#0E7C86` | `#6E7781` | `#2F6FEB` | `#1A7F37` | `#CF222E` |
| Ember | `#4A2416` → `#140D0B` | `#1A1210` | `#EDE0D4` | `#FF7A90` | `#E6C384` | `#FFB26B` | `#7FB4CA` | `#98BB6C` | `#A8948A` | `#FF9E64` | `#76C893` | `#FF5D6C` |

Comments are a muted grey of the theme; an identifier before `(` is a function, one starting with a capital is a type.

## The motion

One ease-out for arrivals (cubic-bezier 0.16, 1, 0.3, 1) and easeInOutCubic for moves; nothing bounces.

- **Entrance**: the panel rises 28 px and fades in over 0.6–0.8 s, then the lines build top to bottom from about 0.35 s, each rising 10 px and fading in over 0.45 s, spaced 35 ms apart with `stagger`. An overlay fades out and lifts 16 px over its last 0.45 s; b-roll just cuts.
- **Focus**: the bar slides and resizes to the new range over 0.55 s while lines and line numbers dim or brighten.
- **Removed**: its red bar and `−` fade in over 0.25 s, then from 0.45 s the line fades out while the lines below slide up.
- **Moved**: kept lines slide to their new slot over 0.55 s (after the removals, if any).
- **Added**: 0.4 s into the slide, it fades in and slides 18 px in from the left over 0.45 s, with its green bar.
- **Changed**: it rides to its new slot with the rest, then the old text rolls up and out (0.3 s) and the new text rolls up into place 0.18 s later (0.5 s), on a green bar.
- Green bars stay while the step is on screen and fade when the next step begins. The step dot and the note change on each step; the note slides 10 px in.

## Timing to speech

Times are on the document's clock: the word's time in the clip minus where the b-roll or overlay starts. Start a focus step on its word (the bar arrives about 0.5 s later). Start a change step about 0.3 s before the word that names the new code. Leave about 1.1 s after the panel starts before the first change, while the lines build in. The document runs from the explanation's first word to its last, plus about 1.5 s to hold the final state.

## Building it in Tella Motion

- One live text node per line version (a changed line has two: old and new), each a `richParagraph` with one run per token colour, so the code stays editable and copyable. Run colours are 0–1 channels, not hex. Leading spaces render, so indentation is real.
- Every line has the same box with line height = line step ÷ font size and moves by keying `y` to slot × line step; its diff bar and gutter mark copy those keys. Line numbers stay in fixed slots, like an editor. The focus bar is one rect with keyed `y` and height.
- Name nodes by role (`code.3`, `num.3`, `added.3`, `focus.bar`, `note.2`, `dot.2`) and group everything but the backdrop into one `panel` group that carries the entrance and exit.
- Keep each command batch to about 30 KB; a large panel takes several.

## Place

- **B-roll** (default): `add_layout` over the explanation's range with the document as motion media and `transitionStyle: "hardCut"` (it defaults to a spring move).
- **Beside the speaker**: a transparent canvas the size of the video, the panel in the empty side, placed with `add_overlay` (`motionDocumentId`) at the canvas size on `hard_cut` (the document animates itself). Keep the panel 40 px or more inside the frame. If the speaker sits in the middle, a custom layout can push the footage aside first.
- **Standalone clip**: `create_clip` of type motion, only when asked.

## Gotchas

- Cross-fading a changed line's old and new text on the same spot looks like a typo pile-up. Roll the old one out, then the new one in.
- A focus bar across a non-contiguous set covers lines that aren't focused. Hide it then and let the dimming and green bars show the focus, or split the step. Hide it too when the focus is just a change step's new lines: the green bars already mark them.
- Create backdrop and chrome, then bars, then text: bars created after the text paint over and tint it.
- Changing a document's canvas size after it is placed as an overlay stretches it: remove and re-add the overlay.
- To rebuild, remove the document's top-level nodes and build again; the document id, and so its placement, stays.

## Check

- One `get_filmstrip` of the document with `timesMs` at the built starting state, each step's settled state (step time + 1.2 s) and mid-change (+0.3 s for a removal, +0.6 s for an add or roll): every step reads in order, nothing jumps or overlaps. Read the code itself on a `get_motion_frame` at width 1920 (it defaults to 320).
- The code matches the source character for character, no line runs past the panel's right edge, line numbers match the lines, and the lit lines are the ones being said.
- Report each step's time and what it shows, any code you trimmed or retyped from a frame, and the theme.

## Making it your own

- Brand: change the accent (tab line, focus bar, badge, dots) and keep green and red for the diff.
- Quieter: focus steps only, no notes. Denser: a second tab and a note on every step.
- A terminal or config file works too: set the badge, language and filename to match.
- Portrait (1080×1920): code around 30 px and lines under 34 characters. Not tried in the examples: check the frames closely.
