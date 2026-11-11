---
name: slack-ui
description: >-
  Recreate the Slack desktop app on macOS in Tella Motion, live and editable: the purple window frame, workspace and
  icon rails, sidebar, a channel with square avatars and a lived-in feed, then your message typed into the formatting
  composer and sent, teammates "is typing" and replying, emoji reactions popping and counting up, and an unread badge
  ticking in the sidebar. Every name, message and count is live text, light or dark, with Slack's own marks in
  removable groups for a generic team chat. Use when asked for a Slack animation, a Slack message being sent, "show
  it landing in Slack", a team channel reacting to a launch or a win, a Slack thread with reactions, or a team chat
  app mock-up as b-roll or its own clip.
metadata:
  title: Slack UI
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/launch-channel.webp
  preview: gallery/launch-channel.mp4
  prompt: When I say I posted the launch in Slack, show me typing it into our #launches channel and the team reacting.
---

# Slack UI

The Slack desktop app, drawn natively at full frame: the window is there from the first frame, already lived-in, and
then the story plays out in it. The viewer's own account types a message into the composer and sends it, someone is
typing, replies land, reactions pop under the message and their counts climb, and another channel's unread badge pops
in the sidebar. It works as b-roll over the stretch where the speaker talks about posting or the team reacting, or as
its own clip. Builds on `tella-ui-redraw` (redraw a screen natively) and `tella-ui-interactions` (typing, press,
list fills, counts); a measured build sheet of the window is in `references/slack-desktop.md`.

**Brand marks.** The real look keeps Slack's visible marks only as shapes you draw, never a downloaded logo file: the
four-colour AI tile by the search bar, in its own group `brand:slack-ai-tile`. One `node.remove` of every `brand:`
group gives the generic team chat; nothing else changes. Workspace tiles are initials on a colour (or the user's own
logo if they attach it), never another company's logo. People, channels and messages are invented unless the user or
the transcript gives them.

## Ask once

Work these out yourself and never ask: the stretch to cover and each beat's word (from the transcript); the replies
and reactions people send, drafted from what the speaker says happened (2–3 replies, each a line a teammate would
write, 40–60 characters); 4–5 earlier messages that make the channel look lived-in (same topic, times 1–60 min
earlier); the sidebar's other channels and DMs; which row gets the unread badge (a channel the speaker mentions, else
an invented one); initials, avatar colours (`#D9572B #3B5BA5 #8E44AD #2E7D5B #C2416B`) and the tile colour.

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Kind | Required | Prefill and limits |
|---|---|---|---|
| Workspace / #channel | text | yes | Company or product from the transcript, else invented, e.g. `Northwind / #launches`. Workspace ≤ 20 chars, channel ≤ 20, lowercase-hyphen |
| You (who types) | text | yes | The speaker's name from the account or the intro, else `Maya Ortiz`. ≤ 22 chars (longer crowds the time) |
| Your message | text | yes | The line the speaker says they posted, then its reactions as `:emoji: n`, e.g. `Shipping Northwind Notes to everyone at noon 🚀 :tada: 5 :rocket: 2`. Message ≤ 60 chars (one line); 0–3 reactions, counts 1–99 |
| Replies | text | no | The drafted replies, `Name: message` separated by ` // `, reactions after a message as `:emoji: n`. 0–3 replies, each ≤ 60 chars |
| Appearance | pick | yes | Light (default) / Dark |
| Real Slack look | switch | yes | On when the video is about Slack or the speaker names it; off (generic team chat) otherwise |
| Pace | pick | yes | Timed to the speech (default when there's a transcript) / Natural (the fixed timing below) |
| Where | pick | yes | B-roll over the stretch (default) / Its own clip |

If the transcript or message already gives the whole thread (one line per message, `Name: message`, reactions as
`:emoji: n`), use it as written. No media needed: avatars are initials, emoji the renderer's font. A skipped form
builds with the prefilled values.

## Timing

The document's clock starts where the graphic starts. Natural pace (the example, 12 s):

| Beat | Time |
|---|---|
| Window settles 103.5 % → 100 %; caret blinks in the empty composer (0.45 s on / off) | 0 → 0.9 s |
| Your message types, ~14 chars/s with small random gaps (longer after some spaces, ~0.3 s before an emoji); send button turns green on the first character | 0.95 → 3.65 |
| Send press 1 → 0.9 → 1, field clears, message lands; "Name is typing..." then their reply lands | 4.05 → 4.25; 4.9 → 6.3 |
| First reaction on your message, counts step up | 7.05, then 7.6, 8.15 |
| Second reply typing → lands; unread badge pops on another channel (label turns bold) at 8.6 | 7.6 → 9.0 |
| Second reaction pops; counts keep stepping to the end | 9.5, then 9.9, 10.3 (badge), 10.6, 11.0 |

Timed to the speech: start typing on the first word of the sentence that introduces the message (or type in step if
the speaker reads it out), end the typing ~0.4 s before the send, and land the send on "posted" / "sent". A reply lands
0.1–0.2 s before the sentence it illustrates, at least 1.8 s apart, with "is typing" 1.2–1.4 s before it. The first
reaction pops 0.7–0.8 s after its message; the unread badge pops when the speaker mentions another channel or
"everyone else". Keep something moving every second, hold the last state ≥ 1.5 s, and keep it under 30 s.

## The look

1920 × 1080, the macOS window at 1.5× Slack's point size (body 22.5 px) on a dark backdrop, 40 / 24 px margins. Every
position, size, colour and icon path is in `references/slack-desktop.md`. The essentials:
- **Type**: Inter only. Body 22.5/400 `#1D1C1D`; names, workspace (27), channel (28.5) and tabs 600; times 18/400
  `#616061` after two spaces in the name's own rich paragraph; "is typing" 19/400 `#616061` with the name 600
  `#454447`. Every text has `fallbackFontIds: ["font.tella.emoji.regular"]`.
- **Frame**: diagonal gradient `#7B3D87` → `#4A3C70` → `#293E5E`; light container `#EEECF2`; active row `#245178`
  with `#E7F7FE` text; badges `#7A3C86` with 15/600 `#F7EDFE`; white pane; tab underline `#7A3C86`.
- **Feed**: avatars 54 px, radius 12, white 600 initials; a message is 78.6 tall, +45 per extra line, +47 for a
  reaction row; bottom of the last one at y 824.5, clipped to y 215.5–838.5. A run from one person drops avatar and name.
- **Reaction pill**: 66 × 34.5, radius 17.25, `#EFEFEF`; emoji 21 px at +10, count 18/600 at +39; next pill 6 px on.
- **Dark**: frame `#19171D`, sidebar `#211F26`, pane `#1A1D21`, text `#D1D2D3`; pills, rules and the composer border
  in greys a step lighter than the pane (check them against a frame).

Motion: one ease-out `{x1: 0.22, y1: 1, x2: 0.36, y2: 1}` for anything that travels or fades; overshoot
`{x1: 0.34, y1: 1.45, x2: 0.6, y2: 1}` only for pops. A new message fades in over 0.3 s while rising 14 px; older ones
slide up by its height over 0.45 s. A pill scales 0.3 → 1 in 0.4 s with the overshoot; each later count step bumps it
1 → 1.12 → 1 over 0.3 s. The unread badge pops 0.3 → 1 in 0.4 s and bumps 1.15 on its next step.

## Building it

One 1920 × 1080 document (b-roll through `add_layout` with hard cuts, or `create_clip`). B-roll belongs to one clip:
`add_layout` takes a `clipId` and times on that clip's playback, so keep the shot inside the clip where the words are
said (start earlier or shorten it). Only when the speech truly runs across a cut, split there (untested): one document
and one `hardCut` layout per clip, the second starting on the frame the first ended on, keys on each clip's own clock;
then `list_layouts` and make the layout after each b-roll `hardCut` too. Raw `node.insert` ops of whole
subtrees are fastest: `backdrop`, then a top group `ui` (keys the 1.035 → 1 settle; anchor at the canvas centre) holding
the window frame, `topbar` (with `brand:slack-ai-tile`), `wsrail`, `container` (icon column, `sidebar`) and `pane`
(header, tabs, `feed`, `composer`). Register Inter 400 / 500 / 600 and the emoji font once with `asset.set`.
- **Feed**: each message its own group (`s0`… seeded, `m1`… new) drawn with its top at y 0, its `translateY` keys
  holding its screen position over time, reactions as child groups `m1.r0`. The feed's matte is a hidden rect
  (`visible: false`) under the tabs, set as the group's `mask` effect. On each arrival or first reaction row, every
  older group's `translateY` slides up by the added height; keep height changes ≥ 0.45 s apart.
- **Typing**: `cp.typed` is a rich paragraph whose first run is `{type: "slice", start: 0, end: <hold keys, one per
  character>, text: "<message>"}` and whose last run is `{type: "inlineObject", node: "cp.caret", width: 2, height: 26,
  align: "baseline", baseline: 21}`, so the caret rides the typed text with no measuring. Step `end` to 0 on the send.
  The caret's hold-keyed opacity does the blink. `cp.send.off` / `cp.send.on` swap by hold-keyed opacity.
- **"is typing"**: one paragraph per typist: name run, " is typing", `slice("...", 0, n)` with n stepping 0 → 3
  every 0.25 s; fades in over 0.2 s, drops to 0 on the arrival. **Counts**: `curve.set` hold-keyed curves (`m1.r0.n`, `unread`) shown by a run `{type: "number", value: {type:
  "curve", name}, decimals: 0}`. The unread row swaps a 400 label for a 600 copy by opacity.

## Checking it

- `get_motion_frame` at 1920 on frame 0 and the last frame: reads as Slack, lived-in, nothing clipped, no mark but
  the `brand:` group you meant; crop a reaction row to check each emoji draws in colour. One `get_filmstrip` at mid-typing, the send + 0.1 s, each arrival + 0.2 s, each first pop + 0.2 s and the end: the
  caret rides the text, the feed slides rather than jumps, pills pop one at a time and counts only go up. Report each
  beat's time, the theme, the look (real or generic) and where it sits.

## Gotchas

- Emoji in a run without the emoji font render as empty boxes; keep spaces in Inter runs (wide in the emoji font).
  Group anchors start at the canvas centre: set `anchorX`/`anchorY` to a pill's or badge's centre before keying scale.
- Keys on one property must strictly increase: keep a pill's first count bump ≥ 0.1 s after its pop settles. No
  text measuring: Inter is ~0.55 em per character at 400. Rebuilding: remove the old `ui` group first, or ids collide.

## Variations

- A thread row ("12 replies" 23/600 `#1264A3`, small avatars) on "thread"; an app message (APP tag, coloured bar) for
  a bot. Sound (curated): `notification-chime` at 0.2 on each arrival, `tick` at 0.45 on first pops.
