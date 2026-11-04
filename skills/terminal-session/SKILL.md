---
name: terminal-session
description: >-
  Recreate a terminal session as live Tella Motion in a Tella video: a window
  (or a full-frame console) where a command types itself character by character
  behind a blinking block cursor, then its output streams in line by line, with
  progress bars that fill in uneven jumps, vector check marks and crosses,
  spinners that resolve, PASS/FAIL badges, coloured log levels, diff rows and
  scrolling, built from a real log or command the user pastes and timed to the
  narration. Three themes: dark (slate window on a drifting grid), paper (an
  off-white page in an ink frame with a hard block shadow) and a retro CRT
  console in amber, green or blue phosphor. Also does an AI coding agent's
  session as a step log (verb tags, a timeline spine, diffs, a running check,
  done). Use when asked for a terminal animation, an animated CLI or command
  line, a "typing in the terminal" shot, a deploy/test/build log as b-roll, a
  retro amber, green-screen or blue CRT console, or an animated coding-agent
  session.
metadata:
  title: Terminal session
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/dark-deploy.webp
  preview: gallery/dark-deploy.mp4
  prompt: When I say "just run npm run deploy", show the deploy happening in a dark terminal. Here's the real output I got (pasted below).
---

# Terminal session

A terminal recreated in Tella Motion with live text in Roboto Mono on an exact character grid, so it stays sharp, editable and timed to the speaker. The command types itself behind a block cursor, then the output prints the way a real terminal prints it: rows pop in, bars jump unevenly, spinners turn into check marks, the view scrolls when it fills, and the window's status lamp pulses while the command runs. Every line of output comes from the user's real log; the look is this skill's own and isn't copied from any OS or terminal app.

## Ask

Find where the speaker runs or talks about the command in the transcript. Then one `ask_form`:

- **The session** (required): the command and its real output, or the agent session. Prefill from the chat or a screen-recording frame. If they have nothing, offer to write a plausible session for a fictional project, and say so in the report.
- **Theme**: Dark (default), Paper, Retro CRT in amber, green or blue, or "match my terminal" (sample the colours from their screenshot but keep this chrome).
- **Where**: b-roll over the spoken range (default), a standalone Tella Motion clip, or an overlay beside a small speaker.
- **Length**: the spoken range, usually 6–14 s.

Trim the log to what reads: at most 15 visible rows and about 20 in total, the important result last. Drop timestamps, hashes and long paths, but keep every number, name and status exactly. Secrets, emails, internal hosts and IPs become obvious placeholders (`sk-••••`, `notes.example.test`); third-party company names become fictional ones (say which). No real product names, logos or prompts in the chrome.

## The look

**Type.** Roboto Mono (`roboto-mono`) 30–34 px at 1080p in a window (never under 28), 40 px on the CRT. Rows are 1.6× the size; the advance is exactly 0.6× the size, so a column is `x0 + col × 0.6 × size` and spaces line things up as in the real log. Size the window to the log, not the frame: longest line + 4–8 columns, rows to fit, so there's no empty right half. Never wrap; lower the size instead.

**Window chrome** (dark and paper): a 66 px header band a shade off the window colour, no window buttons. A rounded tab in the window colour rises out of it at the left (16 px in, 12 px down, 10 px top corners) holding the title in Inter 500 24 px, with a 12 px rounded-square status lamp at its left. At the right of the band, muted 24 px: what runs it (`zsh`, `3 files attached`) and a clock counting the clip's seconds (`0:00`, `0:01`…), which keeps a held frame alive. 56 px side padding, 34 px above the first row. Behind it, a flat backdrop with a 64 px hairline grid (built-in `fx.grid`, 1 px) drifting 60 px right and 30 px down over the clip, under a soft `fx.vignette`.

| | Dark | Paper |
|---|---|---|
| Backdrop, grid | `#0B0D11`, white 3.5 % | `#E9E4D9`, `#1E1C19` 5 % |
| Window, border, header | `#10131A`, 1 px `#262B37`, `#191D27`; 18 px corners; soft shadow 80 px blur, 36 px down | `#FBF9F4`, 2 px ink `#1E1C19`, ink header; 12 px corners; hard ink block 12 px down-right, no blur |
| Title / muted header text | `#C9CFDB` / `#6B7287` | `#1E1C19` / `#A79F92` |
| Lamp idle / running | `#8FD694` / `#E8C468` | `#2F8F4E` / `#D9941A` |
| fg / dim / bright | `#D6DBE6` / `#666C82` / `#FFFFFF` | `#1E1C19` / `#8C857A` / `#000000` |
| ok / warn / err | `#8FD694` / `#E8C468` / `#F07A7A` | `#2F8F4E` / `#B26B00` / `#C8402E` |
| info (paths) / accent (branch) | `#6FD3E8` / `#C99BF0` | `#2364AA` / `#7A3FB0` |
| Bar track, diff add / del, spine | `#232734`, `#123A22` / `#3D1519`, `#353C4D` | `#E4DFD3`, `#DDF0E0` / `#F8E0DA`, `#D3CCBE` |

Keep `dim` about 45 % of the way from the window colour to fg so it stays readable; that's also the rule when matching a brand.

**Retro CRT.** No window: the whole frame is a tube. A bezel (60 px corners) inset 60/40 px, a screen inset 100/80 px (44 px corners) with a strong vignette, text from 166 px in. An inverse header bar on the first row (`VELLUMTARN SYSTEMS · OPS CONSOLE` left, `TTY3  22:58` right, both bold), an optional key legend on the bottom row above a thin rule (keys as badges, labels dim, `LINE 1  9600 BAUD` at the right). Write it in capitals; use dotted leaders to about column 34 so values form a column. Weight 500 (700 for bold) so the phosphor reads solid. The glow is a `dropShadow` with no offset, 10 px radius, in the glow colour, on the content group. Over everything: scanlines (`fx.grid`, cells 6000×4, 1.5 px lines, black at 44 %), grain (`fx.addGrain` backdrop at 7 %, size 1.4, mono), a blurred band 180 px tall at 5 % rolling down every 3.6 s, a backdrop vignette, and a tiny opacity flicker (0.9–0.94 for a frame or two). Each phosphor is one hue like a real tube; err is the one shift along its curve, for a FAIL, WARN or LOST badge:

| Phosphor | screen / bezel | fg / dim / bright | err | glow | header bar |
|---|---|---|---|---|---|
| Amber (ops console) | `#120A02` / `#17110A` | `#FFB13B` / `#9C6A20` / `#FFD58A` | `#FF7A3B` | `#FF9A1A` 60 % | `#FFB13B` |
| Green (mainframe, batch) | `#03110A` / `#0E1410` | `#52EB86` / `#2C9354` / `#BFF8D0` | `#CCF24A` | `#22F06A` 50 % | `#49D97C` |
| Blue (lab, telemetry) | `#020A16` / `#0D1219` | `#74CBFF` / `#3A7AAE` / `#D4EEFF` | `#B6A4FF` | `#2E9BFF` 68 % | `#66BDF2` |

Header text and badge text are the screen colour; the header bar is a touch calmer than fg so it doesn't flare.

**Output parts.** Icons sit in the first two columns: check (ok), cross (err), dot, arrow, and a spinner (a 70 % arc via trim path, turning 540°/s) that is swapped for its result icon and text on the word that resolves it. Badges (` PASS `, ` READY `) are a filled block with 4 px corners, 0.74 of a row tall, text bold in the window colour. Progress bars: a rounded track 0.36× the font size tall, a fill that reaches 100 % in about 6 uneven jumps (eased between, never backwards), a percentage after it that counts in step (dim until 100 %, then the bar colour), and a suffix (`1.9s`) when full. Diff rows get a tinted background with a 4 px edge bar in green or red.

**Agent session.** Our own step log, not any assistant's interface: lowercase bold verb tags right-aligned in the first 5 columns (`ask` accent, `plan` dim, `open` and `run` info, `patch` warn, `done` ok; `search`, `test`, `note` also fit; never a product's tool names), a 2 px spine in column 7 that grows down to each new step, a 12 px rounded-square marker per step on a window-coloured cut so the line breaks around it, text from column 9, and facts right-aligned to the last column (`142 lines`, `+3 -1`, `12 passed  1.3s`). A `run` step's marker is a spinner that becomes a check as its result fades in. End on `done` in bold bright and a fresh `ask` with a blinking cursor.

## Motion

- Window: fades in over 0.4 s, rises 30 px and scales 0.965 → 1 over 0.7 s with a calm ease-out, then pushes in to 1.03 across the clip. The CRT powers on instead: a bright glowing line opens from the centre in 0.16 s, then the picture unfolds vertically out of it by 0.5 s; push 1.02.
- Typing: the command is one title with the `typewriter` text animation by character (stagger = 1 ÷ speed, near-zero unit duration so keys pop); for a looser human rhythm (±35 % jitter, a beat longer after spaces) reveal it with an alpha matte whose width steps one advance per key instead. The cursor's x steps on the same times with hold keys. Cursor `0.92 × advance` wide and `1.2 × size` tall; it blinks 0.53 s on/off while idle, is solid while typing, and disappears on Enter, about 0.35 s after the last key.
- Rows: each fades in over 0.07 s. The status lamp pulses (1 ↔ 0.35 opacity every 0.4 s, in the running colour) from Enter until the next prompt.
- Scroll: when rows exceed the visible rows, the content moves up one row in 0.12 s with an ease-out as each new row arrives.

## Timing to speech

Work on the document's clock, with b-roll starting about 0.3 s before the speaker reaches the command so the window has entered. The first key lands on the word that introduces the command ("run", "type", "ask it to"), the last as they finish saying it: speed = characters ÷ seconds, kept between 10/s (deliberate, CRT) and 24/s (agent requests). Put each line the speaker names on its word ("214 modules", "one test fails", "it's live") and let the rest stream 0.1–0.25 s apart (agent steps 0.5–0.7 s, diff rows 0.12 s). A bar fills over the "it builds" pause; a spinner resolves on its word. End on a closing prompt with a blinking cursor held at least 1.5 s, then hard-cut back to the speaker. Offer Tella's `keyboard-typing` sound from first to last key + 0.1 s at volume 0.5, one per typed command; leave output silent or add `success` at 0.3 on the final "ready".

## Building it

Top level: `bg`, the grid and vignette layers, and one `terminal` group (or `crt` plus the full-frame scanlines, grain, band and vignette). Inside the window: the chrome, then a `viewport` group clipped to the text area holding a `scroll` group (the scroll keys) holding one group per row (`line03`) that owns its fade, so a changed value is one `setTitle`. Name the document "Terminal session · <what it shows>"; place b-roll with `add_layout` over the spoken range, hard cut in and out.

## Gotchas

- A group is not a clock: give a row's children the row's start time, not 0, or they vanish early.
- Insert big groups empty, then their children, so batches stay small (about 30 KB each).
- In a new document a built-in shader may fail with `asset.missing_or_wrong_kind`; add a throwaway 10×10 rect carrying `fx.vignette`, `fx.addGrain` and `fx.grid` first and remove it in the next batch.
- Roboto Mono has no box-drawing or symbol glyphs (`└ ├ │ ✓ ✗ ● ■ ◆ ❯`, block bars). Draw them as stroked paths in their cell; anything else outside ASCII and `› · … — %` must be replaced.
- Keyframe times must be strictly increasing: two rows arriving within 0.12 s become one longer scroll move.
- Start the scroll clip at the first row, not under the header band, or the row above shows as a sliver of descenders.
- Right-aligned text ignores trailing spaces: inset its box instead of padding with spaces.
- The title tab's width is estimated (about 13 px a character of Inter 24); keep titles under about 34 characters and check the frame.
- A typed command of a different length needs its stagger (or matte) and cursor keys redone, not just `setTitle`.

## Check

One `get_filmstrip` of the document at the entrance (0.2 s), mid-typing, just after Enter (lamp running), mid-bar, each named line and the last frame: even left padding, nothing clipped at the right, no empty right half, title inside its tab, badges centred, icons in their column, cursor right after the last character, no half-visible row after a scroll; for agents, tags flush against the spine and every marker on it. Then `get_motion_preview`: a human typing rhythm, the cursor blinking only when idle, the bar never going backwards, one row per scroll, the spine growing step by step. Read every value back against the pasted log, and report the theme, range, typed command with its start and end, and any line you shortened or renamed.

Variations: end on a red FAIL badge and the failing assertion, then cut to the speaker explaining the fix; drop the clock for long clips; turn off the push and entrance for a documentary feel; portrait is 1080×1920 with about 44 columns at 30 px.
