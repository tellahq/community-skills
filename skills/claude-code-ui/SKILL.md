---
name: claude-code-ui
description: >-
  Recreate the Claude Code terminal as live Tella Motion in a Tella video. A
  dark macOS window on a light backdrop shows the app's header with its pixel
  mascot, a request types itself at the prompt behind a block cursor, then the
  agent works through one turn with an orange spinner thinking, Read and
  Update tool lines, a diff with red and green rows, a Bash test run that
  turns into a green PASS, and a closing summary that streams in word by
  word, all timed to the narration. The brand marks sit in their own groups,
  so one switch turns it into a generic coding agent. Use when asked for a
  Claude Code animation or demo, a Claude Code UI, an animated coding-agent
  session, an AI agent fixing a bug in the terminal, a fake terminal
  recording of an agent editing code and running tests, or b-roll for "I
  asked Claude Code to fix it".
metadata:
  title: Claude Code UI
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/claude-code-session.webp
  preview: gallery/claude-code-session.mp4
  tags: claude code, coding agent, terminal, cli, ai agent, diff, tests, typing, ui, macos, developer, b-roll
  prompt: When I say "so I asked Claude Code to fix it", show a Claude Code session that fixes the rounding bug in convert.ts and runs the tests.
---

# Claude Code UI

The Claude Code app recreated in Tella Motion: a dark macOS terminal window, the app's header with its coral pixel mascot, the bordered prompt with its permission-mode line, and one agent turn. The request types in at the caret, the spinner thinks, tool calls print with a red and green diff and a passing test run, and the answer streams in. Every glyph is live type or a drawn path on an exact Roboto Mono grid, so it stays sharp, editable and on the speaker's words. Use it as its own Tella Motion clip (the example) or as b-roll over the stretch where the speaker talks about the agent. It builds on `tella-motion-design`, `tella-ui-redraw` and the typing recipe in `tella-ui-interactions`.

## Ask once

Work these out yourself and never ask: where the speaker introduces the request and what the agent did (the transcript with word timings), the spoken range, the model and version line (invented but plausible, e.g. `Sonnet 5 with medium effort · Claude Pro` and `v2.4.12`), the welcome lines, the placeholder, the spinner word (`Simmering…`, `Pondering…`, `Noodling…`), and real-looking file names and line numbers that fit the story. Read anything the user pasted or attached: a diff, a test log, a screenshot of their session. Take the steps and numbers from it exactly, but never copy their real paths, account or plan names from a screenshot.

**The session.** A form can't hold several lines, so before the form write out the session you'll show, as rows, in the chat message: the tool calls (`Read(src/fx/convert.ts)` → `Read 48 lines`; `Update(…)` with 3–6 diff lines; `Bash(npm test)` → `PASS`, `Tests: 12 passed, 12 total`). Take it from a diff or log in the message first, else from the transcript, else draft a plausible short session for a fictional project and say it's invented. The user corrects it in the form's one-line field or by replying.

Then one `ask_form`, every field prefilled so the user can just submit:

| Field | Kind | Required | Prefill and limits |
|---|---|---|---|
| Request typed at the prompt | text | yes | The speaker's words for what they asked, from the transcript, as a lowercase command (`round converted totals to cents and run the tests`). One line, at most 70 characters. |
| What the agent does | text | yes | A one-line summary of the drafted rows (`reads convert.ts, rounds to cents, runs npm test: 12 pass`), or `use the session I pasted`. At most 3 tool calls, at most 160 characters. |
| Closing answer | text | yes | One or two sentences the agent ends with, drafted from what the speaker says it did. At most 150 characters (two rows). |
| Project folder | text | no | `~/code/<project>`, invented to fit the story (`~/code/harborline`). At most 30 characters. |
| Permission mode | pick | no | `accept edits on` (default), `plan mode on`, `bypass permissions on`. |
| Real Claude Code marks | switch | no | On when the user names Claude Code; off draws a generic coding agent (see Brand marks). |
| Length | slider, seconds | no | 13 s (8–20). As b-roll, the spoken range instead. |
| Where | pick | no | Its own Tella Motion clip (default), or b-roll over the spoken range. |

No media is needed: everything is drawn. If the user skips the form, build with the prefilled values and say which rows were invented.

**Trim the session** to what reads in 10 rows: the important result last, timestamps, hashes and long paths dropped, every number, name and status kept exactly. Secrets, emails, internal hosts and IPs become obvious placeholders (`sk-••••`, `api.example.test`); real third-party company names become fictional ones (say which).

**Brand marks.** This skill draws Claude Code's marks only because it recreates that app on request: the title `✳ Claude Code`, the pixel mascot and the bold `Claude Code` in the header, each as live type or plain rects (never a downloaded logo file), each in its own group: `brand:title`, `brand:mascot`, `brand:name`. With the switch off, `node.remove` those three groups, start the header text where the mascot was, drop the plan from the model line, and title the window `agent — zsh` (Inter 600 27 px, same box).

## Timing

The example's 13.43 s, document clock: window enters 0–0.7 s; idle prompt with blinking cursor until 1.25 s; typing 1.25–4.6 s (49 characters); Enter at 4.83 s; spinner from 4.98 s; `Read` at 6.13 s, its result +0.35 s; `Update` at 7.23 s, result +0.35 s, then the four diff rows 0.12 s apart; `Bash` at 8.73 s, `Running…` +0.15 s, `PASS` at 9.83 s and `Tests:` +0.15 s; the answer at 10.63 s (spinner ends) and its second line at 11.23 s; 2.2 s hold on the blinking cursor.

For another length, keep the typing speed (14–18 keys a second) and the gaps inside a tool call, and stretch or squeeze the gaps between tool calls (1–1.5 s). As b-roll, start 0.3 s before the speaker says the request so the window has entered, put the first key on the word that introduces it ("asked it to", "typed"), the `PASS` on "tests pass", and the answer where the speaker says what it did; hard-cut back after the hold. Offer Tella's `keyboard-typing` sound from first to last key + 0.1 s at volume 0.5.

## The look

Every measurement, colour and glyph path is in `references/claude-code.md`; read it before building. In short, at 1920×1080:

- **Backdrop**: flat `#E4E5E9`, a `#F5F6F8` circle (centre 960, 470, radius 750) with a 260 px blur behind the window, like a product shot.
- **Window**: 1640×940 at (140, 70), 26 px corners, a gradient border and body (`#2A2D34` → `#25282E`), a 69 px title bar (`#3D414A` → `#30343C`) with a hairline under it, a glassy 1 px bevel, a crisp black 0.55 outline, a soft shadow (dy 36, 90 px) and a contact shadow (dy 6, 14 px). Glossy traffic lights (radius 13, 44 px apart), a blue folder icon, then `✳ Claude Code` in Inter 600 27 px `#7C7C7C`.
- **Type**: Roboto Mono 30 px, advance 18 px, rows 38 px, column `c` at `183 + 18c`; 700 for tool names and the app's bold. White text, dim `#666666`, secondary `#999999`.
- **Header** (scrolls away with the transcript): the coral `#CA7C5E` mascot, `Claude Code` bold + ` v2.4.12` dim, the model line and project folder dim, a bold welcome line and a dim one.
- **Prompt box** (pinned): two 2 px `#999999` rules at y 842 and 918, the white `❯`, the input, a white 18×36 block cursor; status line `⏵⏵ accept edits on (shift+tab to cycle)` in `#AF87FF` and dim; `● medium · /effort` right-aligned above the box, sharing its row with the spinner.
- **The turn**: the submitted prompt on a `#373A41` band; the spinner (three strokes in `#D77757`) with its word pulsing lighter and `(Ns · esc to interrupt)` counting up each second; `⏺ Read(…)` with a grey dot that blinks while it runs and turns green `#4EBA65`; `⎿` results in secondary; diff rows on `#7A2936` and `#225C2B`; a green ` PASS ` block with black bold text; the answer after a white `⏺`.

## Building it

Name the document "Claude Code UI · <what it shows>". Top level: `bg`, `bgGlow`, then one `terminal` group (origin at the canvas centre) holding the window parts, traffic lights, folder, `brand:title`; a `viewport` group masked to (140, 150, 1640, 595) around a `scroll` group holding the header (`brand:mascot`, `brand:name`, the dim lines) and every transcript row; then the pinned spinner row, rules, prompt, cursor and status line. As its own clip, make a Tella Motion clip of the length; as b-roll, place the document with `add_layout` over the spoken range, hard cut in and out.

A b-roll layout belongs to one clip: `add_layout` takes a `clipId`, its `startTimeMs`/`durationMs` are on that clip's playback timeline (cuts applied), and it can't run into the next clip. Keep the shot inside the clip where the words are said (start it earlier or shorten the hold so it ends by the clip's end). Only when the spoken range truly crosses a cut, split it there: one document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document starting on the frame the first ended on, keys on each clip's own clock (untested). Then `list_layouts` and make sure the layout after each b-roll range is a hard cut too; it can come back with a spring.

- **Entrance**: `terminal` opacity 0 → 1 over 0.4 s, `translateY` 30 → 0 and scale 0.965 → 1 over 0.7 s, `easeOutCubic`, then scale on to 1.025 by the last frame.
- **Typing**: one title per typed word at its column, each with a `typewriter` text animation by character (stagger 0.055–0.077 s, unit duration 0.01 s) starting on its first key, a beat after each space. The cursor's `translateX` steps 18 px per key with hold keys on the same times. The placeholder ends on the first key; the inverse letter under the cursor (`#292C33`) shares the cursor's blink keys. Blink 0.53 s on/off while idle, solid while typing.
- **Enter**: the typed words end, the cursor jumps back to column 0, and the prompt band appears in the transcript on the same frame.
- **Rows** print instantly (each row's nodes start at its time and run to the end). A running tool dot blinks (opacity 1 ↔ 0.35 every 0.18 s) and its colour holds grey `#B8B8B8` then green on the frame its result prints. The answer is a `typewriter` by word, stagger 0.045 s.
- **Spinner**: anchored at its centre, scale 0.55 ↔ 1 every 0.42 s (`easeInOutSine`), rotating 30°/s; its word's colour pulses between `#D77757` and `#EBA58B` every 0.8 s. A new `(Ns …)` title replaces the last each second.
- **Scroll**: `scroll.translateY` moves up one row (38 px) in 0.12 s with `easeOutCubic` as each row arrives below the mask, holding between moves.

## Checking it

`get_filmstrip` of the document at 0.2 s, mid-typing, just after Enter, the first tool call, the diff, `PASS`, the answer and the last frame. Look for: the cursor right after the last typed character, nothing clipped at the right edge, no half-visible row under the title bar after a scroll, the dots green once their results print, the spinner gone when the answer starts. Then `get_motion_preview` for the typing rhythm and blink. Read every row back against the session and report the request, its key times and any line you shortened or invented.

## Gotchas

- A group is not a clock: give a row's children the row's start time, not 0, or they show early.
- Roboto Mono has none of `❯ ⏺ ⎿ ✻ ✳ ⏵ ● ⏸`: draw them as paths (`references/claude-code.md`). `·` and `…` are fine as text.
- Keyframe times must strictly increase: rows 0.12 s apart (the diff) merge into the scroll move already running.
- Masks don't follow their node's transform: mask the still `viewport` and key `scroll` inside it. Set `anchorX`/`anchorY` to the canvas centre before keying the window's scale.
- A shape's colour keys per channel (`r`, `g`, `b` with `hold`): that's how a dot turns green.
- Right-aligned text ignores trailing spaces: inset its box instead.
- A different request needs its word titles, staggers and cursor keys redone, not just `setTitle`.
- Insert big groups empty, then their children, in batches of about 30 KB.

## Variations

- Plan mode (`⏸ plan mode on` in teal) where the turn ends on a numbered plan instead of edits; bypass mode in `#9D3642`.
- A second turn typed after the answer; a red `FAIL` and the failing assertion, then a cut to the speaker explaining the fix.
- Portrait (1080×1920): a window about 1000 px wide with 26 px type (advance 15.6 px), the request under about 50 characters; untested, so check the frame.
