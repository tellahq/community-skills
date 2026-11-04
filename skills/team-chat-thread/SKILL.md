---
name: team-chat-thread
description: >-
  Animate a chat that reads instantly as a real platform, timed to the narration: a Slack-style workspace
  channel (sidebar, #channel header, reaction pills, thread replies, composer), a WhatsApp-style group chat
  (chat list, doodle wallpaper, green and white bubbles with tails, reaction pill, quoted replies, ticks), an
  X-style post with replies landing under it and its likes, reposts and views ticking up, or a YouTube-style
  live stream with your footage in the player, live chat with roles and Super Chat cards, and reactions floating
  up. Messages arrive on the words they illustrate, reactions pop and counts climb, someone is typing; all live
  Tella Motion shapes and text, with generic marks instead of any real logo. Use when asked for a Slack, WhatsApp,
  X / Twitter or YouTube style chat animation, a team channel reacting to a launch, a group chat, a reply thread
  or a live chat as a motion graphic.
metadata:
  title: Team chat thread
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/slack-channel.webp
  preview: gallery/slack-channel.mp4
  prompt: When I talk about the launch, show our Slack channel lighting up with messages and reactions.
---

# Team chat thread

A chat that plays out the story the speaker tells: a message lands, reactions pop onto it, counts tick up, the
thread fills, the next person is already typing. Four looks, each drawn to read as the app people use every day,
so the viewer gets "the team reacted" (or "the internet reacted") without reading a word:

| Platform | Reads as | Good for |
|---|---|---|
| Slack-style | workspace channel: dark rail, purple sidebar, `# channel`, rounded-square avatars, reaction pills, thread rows, composer | a team reacting to a launch, an incident, a win |
| WhatsApp-style | desktop group chat: chat list, doodle wallpaper, white and green bubbles with tails, one reaction pill per bubble, quoted replies, ticks | a small crew, friends, a customer group |
| X-style | dark post page: the post with ticking views / replies / reposts / likes, "Post your reply", replies landing under it | public reaction to an announcement |
| YouTube-style | dark live stream page: footage in the player with a LIVE bar, live chat with roles and Super Chats, reactions floating up | an audience watching something happen live |

Everything is live Tella Motion shapes, paths and titles, so every name, message and count stays editable.
**Never draw a real logo, wordmark or the platform's name.** Use a generic workspace tile (initials), a generic
mark (a spark, a ring), your own simple line icons, and fictional channels, groups, handles and people unless the
user or the transcript gives real ones. Pair with `tella-ui-redraw` and `tella-ui-interactions`.

Emoji are text in Apple Color Emoji, which the renderer ships: register the font once (`asset.set`, kind `fonts`,
`{id: "font.tella.emoji.regular", source: {type: "host", hostId: "tella.font.emoji.regular"}, family: "Apple Color
Emoji", weight: 400, style: "normal"}`), then set emoji as `richParagraph` runs whose style has that `fontId`. A plain
title in Inter draws them as empty boxes.

## Ask first

From the transcript, find the stretch where the speaker describes people reacting and draft the chat: 3 to 6 new
messages, each a short line someone would plausibly write, plus the earlier ones already there. Then one `ask_form`:
platform (prefilled with the best fit); full-frame b-roll over the stretch (default) or its own clip (these are
full-screen app views, not small panels); theme (Slack and WhatsApp light, X and YouTube dark by default); names
(workspace and channel, group, handles, or channel and stream title, as placeholders); messages as `Name: text`
(emoji welcome); reactions per message (X: the counts; YouTube: floating bursts); for YouTube, the player footage (a library
video, or one from `list_library` scope `vintage`).

## Time it to the speech

The document's clock starts where the graphic starts in the video.
- A message arrives 0.1–0.2 s before the first word of the sentence it illustrates, 2–3 s apart (at least 1.8 s).
  YouTube chat runs faster, 0.6–1 s apart.
- The first reaction pops 0.7–0.8 s after its message, the next ones 0.4–0.5 s apart. Counts step up every
  0.4–0.8 s, faster on "everyone" or "the whole team", and keep stepping to the very end so the last frame breathes.
  On X and YouTube, views, watching and likes tick all the way through.
- A Slack thread row appears on "thread", "replies", "everyone chimed in", its count climbing every ~0.5 s.
- Typing starts 0.8–1 s before a message and ends on its arrival (Slack under the composer, WhatsApp in the header).
- Seed the feed so the app looks lived-in on frame one: Slack and WhatsApp 4–5 messages, X 3 replies, YouTube 12+.
- Hold the finished state ≥ 1.5 s, then cut. Keep a graphic under 30 s; split longer chats in two.

## The look

1920 × 1080, laid out as the app at about 1.7× its desktop size so body text is 24–31 px. Inter for Slack, WhatsApp
and X; Roboto for YouTube. Names, counts and channels are fictional; avatars are coloured discs (rounded squares on
Slack, radius 12) with white initials on a mid-dark colour.

- **Slack** (light): top bar 76 and rail 112 in `#3B0B3C`, sidebar 460 in `#4E1D50` (text `#D9C9DA`, active channel
  on a `#F2E6F3` pill, unread bold, DMs with green `#2BAC76` presence dots), white channel pane in one rounded
  container: `# channel` 31/800, stacked member avatars and count, tabs, a sticky "Today" pill. Messages: 64 px
  avatars, name 27/800 `#1D1C1D`, time 20 grey `#616061`, body 27/400 at 1.45 line height; a run from one person
  drops avatar and name. Reaction pills 44 tall (`#EFEFEF`, 28 px emoji, count 21/700); yours is `#E3F1F8` with a
  `#1D9BD1` outline. Thread row: small avatars, "12 replies" 23/700 `#1264A3`, "Last reply today at …" grey. App
  messages get an APP tag and a coloured bar with a bold label. Composer: formatting bar, "Message #channel", tools.
  Dark: frame `#19171D`, sidebar `#211F26`, pane `#1A1D21`, text `#D1D2D3`.
- **WhatsApp** (light): rail 100 and header `#F0F2F5`, chat list 540 white ("Chats" 38/700, search, All / Unread /
  Favourites / Groups chips, 80 px avatars, green `#25D366` unread badges; the open chat's row updates its last
  message and time, at most six rows). Wallpaper `#EFEAE2` with a sparse field of tiny line doodles (dots, plus
  signs, rings, hearts, stars) in `#E3DBCF`, one path. Bubbles radius 12, tail on the first of a run: incoming white,
  yours `#D9FDD3` on the right with blue ticks `#53BDEB`; sender names in colours (`#1F7AEC #E542A3 #FA6533 #06A77D
  #A62C71`), body 26/400 `#111B21`, time tucked bottom right in `#667781`. One white reaction pill hangs off each
  bubble with the emoji so far and the total, widening as new emoji join. A quote is a tinted box with a coloured
  bar, name and one line at the top of the bubble. "Name is typing…" replaces the members line in green `#00A884`.
  Dark: panel `#111B21`, wall `#0B141A`, incoming `#202C33`, yours `#005C4B`.
- **X** (dark): black, rules `#2F3336`, text `#E7E9EA`, grey `#71767B`, blue `#1D9BF0`, like pink `#F91880`. Icon
  rail with a generic spark mark and a round compose button; a 1050 px centre column with the post (70 px avatar,
  name 27/700 with a blue tick, @handle, text 31/400, time and live views, the action bar with live counts), the
  "Post your reply" row with a greyed Reply button, then replies newest first. Right column: search, "Relevant
  people" with Follow, three fictional trends. Keep the post to two or three lines.
- **YouTube** (dark): `#0F0F0F`, text `#F1F1F1`, grey `#AAAAAA`, red `#FF0000`. Masthead with a generic ring mark and
  search; the player 1200 × 675 at the top left, rounded 18, footage cropped to cover with a dark bottom gradient,
  full red live bar, controls and a red dot + LIVE; title 31/700; channel row with a white Subscribe pill and a
  like pill with a live count; a description box with a live "watching now" (keep under 1,000). Live chat 616 wide
  on the right: "Top chat", a ticker of Super Chat chips (seed one so it's there from frame one), lines with a
  40 px avatar and the name inline before the 24/400 text; owner on a yellow `#FFD600` chip, moderators blue
  `#5E84F1` with a wrench, members green `#2BA640` with a badge. Super Chat cards take their tier's two colours
  (header / body): blue `#1565C0/#1E88E5`, yellow `#FFB300/#FFCA28`, orange `#E65100/#F57C00`, magenta
  `#C2185B/#E91E63`, red `#D00000/#E62117`.

## The motion

One soft ease-out `{x1: 0.22, y1: 1, x2: 0.36, y2: 1}` for everything that travels; a small overshoot
`{x1: 0.34, y1: 1.45, x2: 0.6, y2: 1}` only for things that pop (pills, emoji, the like heart, ticker chips).
- **In**: no blank frame. The app is there from frame one and settles from 103.5 % to 100 % over 0.9 s.
- **Arrival**: the feed slides by the new height in 0.45 s (YouTube 0.3 s); the new message fades in and rises
  22 px (YouTube 12). Old messages leave under the header through a soft fade.
- **Reaction**: the pill scales 0.3 → 1 in 0.4 s with the overshoot; each later count step bumps it 1 → 1.12 → 1
  and the number rises 6 px into place while fading up from 0.3.
- **Thread row** slides 16 px in from the left. **Like** (X): a pink heart pops over the outline, the count turns
  pink. **Floating reactions** (YouTube): each emoji pops in by the chat box, rises ~340 px over ~1.9 s with a
  sideways wobble and fades out in its last 40 %.

## Building it in Tella Motion

A 1920 × 1080 document (b-roll via `add_layout` with hard cuts, or its own clip). Draw the chrome once, then each
message as its own group (`m1`, `m2` …) drawn with its top at y = 0, its `y` keys holding its screen position over
time, with what fades in on arrival, its reactions and thread row as animated children. All messages sit in a `feed`
group alpha-matted under the header by a vertical-gradient shape (gradient paint via `node.patch` `paint.source`), so
old messages fade out rather than clip. Everything goes in one top group `ui` for the intro settle.
- Chat apps pin the feed to the bottom: every arrival, first reaction row (+54 Slack, +36 WhatsApp) or thread row
  grows a message and slides all older ones up by that much. X pins to the top: the post stays and replies land under
  the reply box.
- Keep height changes ≥ 0.45 s apart (0.3 s on YouTube). If one starts while the last slide is still running, start
  the new slide from where the message is at that moment, not where it was going.
- Counts are titles bound to a hold-keyed curve (`setCurve` + `bindProperty` on `text`). Show 1,000+ on X and YouTube
  (10,000+ elsewhere) as `1.2K` (curve in thousands, 1 decimal, suffix `K`), and keep one count's steps on one side of
  that line. On X a zero count shows no number.
- Emoji: a run in the emoji font at the pill's emoji size (28 px in a Slack pill); emoji in a message are runs in
  the same title. Keep spaces in the text font's runs: in the emoji font they're wide.
- YouTube footage: a media node with `destination` the player box and `fit: "cover"`, sound off, in a group matted
  by a rounded rect.
- Optional sound (`add_sound_effect`, curated catalog): `notification-chime` at 0.2 on each arrival (not YouTube),
  `tick` at 0.45 on first reactions.

## Gotchas

- Emoji left in an Inter run render as empty boxes, and ❤️ as Inter's black ♥: always give them the emoji font. Inter does render ✓ ★ ♥ ↳ → • ● @ #;
  ✔ ⚡ ☺ ✉ and all pictographic emoji don't.
- Group anchors start at the canvas centre: set `anchorX`/`anchorY` on a pill's centre before keying `scale`, or it
  scales toward the middle of the frame.
- A node that starts later than 0 takes keys only at or after its start. Keys on an effect field carry no `easing`.
- There's no text measuring: size pills, bubbles and the WhatsApp reaction pill from an estimate (Inter is about
  0.55 em per character at 400), then check frames. Slack and WhatsApp names over ~24 characters crowd the time;
  keep YouTube handles under ~20 and lines to about 40 characters after a name.
- Rebuilding into the same document: remove the old `ui` group first, or node ids collide.

## Check

- `get_motion_frame` at full width on the first and final state: reads as the app at a glance, looks lived-in,
  nothing cut by its box, no logo or platform name; crop a reaction and zoom to see every emoji reads.
- One `get_filmstrip` of the document across its length: each message lands on its word, the feed slides rather than
  jumps, pills pop one at a time, counts only go up, something moves every second, YouTube footage fills the player.
  Report each message's time, the platform, the theme and where it sits.
