# Slack desktop on macOS: build sheet

Measured from a screenshot of the real app (light theme, purple window frame) and drawn at 1.5× its point size, so
the window is 1840 × 1032 at (40, 24) on a 1920 × 1080 canvas. Every value is canvas px. All text is Inter from the
catalog (`tella.font.inter.regular` / `.medium` / `.semibold`, weights 400 / 500 / 600; Slack's own bold reads as
Inter 600), emoji fall back to Apple Color Emoji (`fallbackFontIds: ["font.tella.emoji.regular"]`).

## Frame and backdrop

| Piece | Where and how |
|---|---|
| Backdrop | full frame, linear `#2A1F3D` → `#171728` → `#0F1A2A` (top left to bottom right) plus a radial `#6A3C86` glow at 45 % → 0 around (500, 200), r 900 |
| Window | rect 1840 × 1032, radius 18. Shadow: a separate rect behind it with `shadows [{blur 50, dy 24, #000 55 %}]`. Hairline: a 1.5 px stroke of white at 16 % |
| Frame gradient | linear on the window, along (0.534, 0.846) from window origin +130 to +1000 along that direction: `#7B3D87` → `#4A3C70` → `#293E5E`. Purple top left, navy top right and bottom left |
| Title bar | 60 tall. Traffic lights 20 px at x +28.5 / +63 / +97.5, y centre +30.5: `#EC6A5E #F4BF4F #61C554` with a 1 px 12 % black ring. Sidebar toggle 30 px at +135 |
| Search | rect x 560–1300, y 33–75, radius 9, white 20 %. Back / forward (50 %) / history icons 28–30 px, 130 / 81 / 33 px left of it. Search icon 24 px, placeholder "Search <workspace>" 21/400 white |
| AI tile (brand mark) | 40 px square 36 px right of the search: four quarters `#36C5F0 #2EB67D #E01E5A #ECB22E` (outer corners radius 9), white 4-point star (r 13 / 3.6), 1.5 px white 28 % ring. Group `brand:slack-ai-tile` |
| Help | 30 px circled ? at window right − 30 |
| Workspace rail | 90 wide on the frame gradient. Active tile 52 px radius 13 with a 62 px `#E5D4F1` 2.5 px ring at y +104; more tiles every 78–80 px; + at +340 |

## Container (light)

Container from (130, 84) to (1875.5, 1051.5), radius 15, `#EEECF2`. A 1.5 px `#D9D2DD` line at x 235 splits the
icon column (105 wide) from the sidebar (270 wide). The pane is white from x 505 with the right corners rounded 15 and
`shadows [{blur 14, dx −3, #000 7 %}]` so the sidebar's edge darkens slightly.

| Piece | Spec |
|---|---|
| Icon column | items every 102 px from y 127 (Home, DMs, Activity, Files, More): 30 px icons in `#340A38`, label 17/600 43 px below. Active Home on a 54 px `#D7CEDA` tile radius 12, 9 px `#7A3C86` dot top right. Badges: 30 × 24 `#7A3C86` pill, text 15/600 `#F7EDFE`; quiet ones `#E4DEE8` with dark text. Bottom: + and moon on 54 px `#DCD3E0` circles at container bottom −218 / −141, your avatar 54 px radius 12 at −62 with a 12 px `#2BAC76` presence dot ringed in `#EEECF2` |
| Workspace name | x 259, centre y 121: 27/600 `#340A38`, chevron 22 px right after it; gear 28 px at sidebar right −83, compose at −32 (`#58365C`) |
| Find field | x 247, y 160.5, 244.5 × 37.5, radius 9, `#FDFCFE` with a 6 % black hairline; search icon 20 px, "Find a conversation" 20/400 `#58365C` |
| Nav rows | centres y 236 + 42 n: Threads, Huddles, Drafts & sent, Saved, Directories. Icon 24 px at x 271, label at x 295, 22.5/400 `#58365C` |
| Rule | y 442, x 253–487, 1.5 px `#D5CCD9` |
| Sections | "Starred" header (star icon) at y 481.5, rows every 42 from y 523; a header row (chevron + "Channels", "Direct messages") takes 1.24 rows. Row: `#` icon 22 px at x 283 or a 27 px avatar radius 6 at x 270 with a presence dot, label at x 307 22.5/400 |
| Active row | x 247, 246 × 42, radius 9, `#245178`, text and icon `#E7F7FE` |
| Unread | label switches to 600 `#340A38`; badge 30 × 24 `#7A3C86` pill centred at sidebar right −42 |

## Pane

| Piece | Spec |
|---|---|
| Header | centre y 120. Star tile 40 px radius 9 `#FEFAE3` at x 534 with a `#ECB22E` star (r 11.5 / 5.2) and a faint `#B8892A` outline; `#` 27 px at x 598; name 28.5/600 `#1D1C1D` at x 617, chevron after. Right: member stack (27 px squares radius 7, 20 px apart, white 2 px border) + count 20/600 in a 116 × 42 hairline box; headphones+chevron, bell, search, kebab 30 px `#454447` at pane right −197 / −128 / −82 / −40 |
| Tabs | centre y 186. Filled message icon + "Messages" 21/600 `#1D1C1D` at x 553 / 572; "Files" and "Pins" 21/500 `#454447` with their icons; + after. Rule y 214, 1.5 px `#DDDDDD`; underline under the active tab 140 × 4 `#7A3C86` sitting on the rule |
| Feed | clipped to y 215.5–838.5 by a hidden rect matte (Slack clips, it does not fade). Avatar 54 px radius 12 at x 534; text at x 600. Name 22.5/600 `#1D1C1D` then two spaces and time 18/400 `#616061` in one rich paragraph; name centre +11, body centre +44, more lines +45 each. A group is 78.6 tall plus 45 per extra line plus 47 for a reaction row. Bottom of the last group at y 824.5 |
| Reaction pill | 66 × 34.5, radius 17.25, `#EFEFEF`, top 22 below the last line's centre; emoji 21 px at +10, count 18/600 at +39; next pill 6 px later. Yours: `#E3F1F8` fill, 1.5 px `#1D9BD1` outline |
| Composer | x 535–1842.5, y 838.5–1012.5, radius 12, 1.5 px `#B6B6B7` border. Toolbar 57 tall `#F8F8F8`: icons 27 px `#454447` at +26, 74.5, 123, 171, 216 (+chevron 240), 305, 353, 402, 461, 511, 559, 607, separators at +277 and +432. Placeholder "Message #channel" 22.5/400 `#696969` at x +26, centre y 924. Bottom row centre y 981: + on a 40 px `#EEEEEE` circle (+30), underlined "Aa" (+76), emoji (+124), @ (+172), video (+236), mic (+284), shortcuts (+352), separators at +203 and +316 |
| Send | empty: grey `#BBBBBB` arrow at right −76, a hairline and a chevron. With text: a 90 × 36 `#007A5A` split button radius 6, white arrow, 45 % white divider, white chevron |
| Typing | under the composer at y 1032: "**Name** is typing" 19/400 `#616061`, name 600 `#454447`, then `slice("...", 0, n)` with n stepping 0–3 every 0.25 s |

## Icons

24 × 24 SVG path data, stroke 1.6–1.9 (round caps and joins) unless marked filled. Put each path in a group with
`transform {translateX: cx − 12 s, translateY: cy − 12 s, scaleX: s, scaleY: s}`, `origin {x: 0, y: 0}` and
s = size / 24, so one path serves every size.

| Icon | Path |
|---|---|
| sidebar toggle (outline; fill `toggleFill` too) | `M5 4.5h14a2.5 2.5 0 0 1 2.5 2.5v10a2.5 2.5 0 0 1-2.5 2.5H5A2.5 2.5 0 0 1 2.5 17V7A2.5 2.5 0 0 1 5 4.5Z M10 4.5v15` |
| sidebar toggle, filled left panel | `M5.2 6.3h3.3v11.4H5.2a.9.9 0 0 1-.9-.9V7.2a.9.9 0 0 1 .9-.9Z` |
| back | `M19.5 12H4.5M10.5 6l-6 6 6 6` |
| forward | `M4.5 12h15M13.5 6l6 6-6 6` |
| history | `M3.4000000000000004 12a8.6 8.6 0 1 0 17.2 0a8.6 8.6 0 1 0 -17.2 0Z M12 7.2v5.2l3.2 2` |
| search | `M3.9000000000000004 10.5a6.6 6.6 0 1 0 13.2 0a6.6 6.6 0 1 0 -13.2 0Z M15.4 15.4L20.5 20.5` |
| help (add a filled dot: `M10.8 17.4a1.2 1.2 0 1 0 2.4 0a1.2 1.2 0 1 0 -2.4 0Z`) | `M2.8000000000000007 12a9.2 9.2 0 1 0 18.4 0a9.2 9.2 0 1 0 -18.4 0Z M9.4 9.6a2.7 2.7 0 1 1 3.9 2.4c-.8.4-1.3 1-1.3 1.9v.6` |
| Home (filled) | `M12 3.6 3.8 10.1c-.3.2-.4.5-.4.8v8.6c0 .6.4 1 1 1H9.6v-5.6c0-.6.4-1 1-1h2.8c.6 0 1 .4 1 1v5.6h5.2c.6 0 1-.4 1-1v-8.6c0-.3-.1-.6-.4-.8Z` |
| DMs | `M9.6 9.2a5.6 5.6 0 0 1 0 11.2H4v-5.6a5.6 5.6 0 0 1 5.6-5.6Z M9.2 7.8a5.6 5.6 0 0 1 11 1.6v5.4h-4.1` |
| Activity / notifications | `M6.2 16.6v-5.4a5.8 5.8 0 0 1 11.6 0v5.4l1.6 1.9H4.6Z M10 20.6a2.1 2.1 0 0 0 4 0` |
| Files | `M8.2 7.6V6.1a2 2 0 0 1 2-2h7.7a2 2 0 0 1 2 2v7.7a2 2 0 0 1-2 2h-1.4 M6.1 8h7.7a2 2 0 0 1 2 2v7.8a2 2 0 0 1-2 2H6.1a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2Z` |
| new / add | `M12 4.5v15M4.5 12h15` |
| new message | `M11.2 4.6H6.6a2 2 0 0 0-2 2v10.8a2 2 0 0 0 2 2h10.8a2 2 0 0 0 2-2v-4.6 M17.4 3.6l3 3-8.6 8.6-3.8.8.8-3.8Z` |
| Threads | `M12 3.6a8.4 8.4 0 1 1-3.9 15.8L3.8 20.4l1.1-4A8.4 8.4 0 0 1 12 3.6Z M8.6 10.6h6.8 M8.6 14h4.6` |
| Huddles | `M4.2 15.4V12a7.8 7.8 0 0 1 15.6 0v3.4 M4.2 14.2h2.6a1 1 0 0 1 1 1v4.4a1 1 0 0 1-1 1H5.6a1.4 1.4 0 0 1-1.4-1.4Z M19.8 14.2h-2.6a1 1 0 0 0-1 1v4.4a1 1 0 0 0 1 1h1.2a1.4 1.4 0 0 0 1.4-1.4Z` |
| Drafts & sent | `M4.4 4.6 20.2 12 4.4 19.4 6.8 12Z M6.8 12h5.6` |
| Saved | `M7.2 3.6h9.6a1.1 1.1 0 0 1 1.1 1.1v15.8l-5.9-4.3-5.9 4.3V4.7a1.1 1.1 0 0 1 1.1-1.1Z` |
| Directories | `M6.6 3.6h11a1.4 1.4 0 0 1 1.4 1.4v14a1.4 1.4 0 0 1-1.4 1.4h-11A1.4 1.4 0 0 1 5.2 19V5a1.4 1.4 0 0 1 1.4-1.4Z M3.4 8h3.4 M3.4 12h3.4 M3.4 16h3.4 M10.1 10.2a2.1 2.1 0 1 0 4.2 0a2.1 2.1 0 1 0 -4.2 0Z M8.8 16.4a3.6 3.6 0 0 1 6.8 0` |
| channel # | `M9.8 4.2 7.6 19.8 M16.4 4.2l-2.2 15.6 M4.6 9.2h15.4 M3.8 14.8h15.4` |
| chevron down | `M7 9.8l5 5 5-5` |
| Messages tab (filled) | `M12 3.4a8.6 8.6 0 1 1-4.1 16.2L3.6 20.6l1.2-4.1A8.6 8.6 0 0 1 12 3.4Z` |
| Pins tab | `M14.6 3.8 20.2 9.4 M17.4 6.6l-4.1 4.1-3.9-.6-2 2 6.5 6.5 2-2-.6-3.9 4.1-4.1 M10.2 15.8l-5.6 5.6` |
| B | `M7.2 4.6h5.6a3.7 3.7 0 0 1 0 7.4H7.2Z M7.2 12h6.6a3.8 3.8 0 0 1 0 7.6H7.2Z` |
| I | `M10.2 4.6h7.2 M6.6 19.4h7.2 M14.4 4.6l-4.8 14.8` |
| U | `M7.2 4.2v7.2a4.8 4.8 0 0 0 9.6 0V4.2 M5.8 20h12.4` |
| S | `M16.4 7.6c-.6-1.9-2.3-3.2-4.5-3.2-2.6 0-4.5 1.5-4.5 3.6 0 1.6.9 2.6 2.4 3.2 M4.2 12h15.6 M14.2 13.4c1.4.6 2.4 1.6 2.4 3.2 0 2.2-2 3.6-4.8 3.6-2.4 0-4.3-1.2-4.9-3.1` |
| paragraph | `M18 4.6h-7.4a4 4 0 0 0 0 8h1.2 M11.8 4.6v14.8 M15.6 4.6v14.8` |
| link | `M10.2 13.8a3.9 3.9 0 0 0 5.6 0l3-3a3.9 3.9 0 0 0-5.6-5.6l-1.1 1.1 M13.8 10.2a3.9 3.9 0 0 0-5.6 0l-3 3a3.9 3.9 0 0 0 5.6 5.6l1.1-1.1` |
| numbered list | `M10.4 6.4h9.8 M10.4 12h9.8 M10.4 17.6h9.8 M4.4 4.9l1.3-.7v4.4 M4 14.6c.2-.9 2.7-1.2 2.7.3 0 1-2.7 2-2.7 3.3h2.9` |
| bullet list | `M10.4 6.4h9.8 M10.4 12h9.8 M10.4 17.6h9.8 M5.2 6.4h.01 M5.2 12h.01 M5.2 17.6h.01` |
| quote | `M5 4.6v14.8 M10 6.4h10 M10 12h10 M10 17.6h7` |
| code | `M8.4 7.4 3.8 12l4.6 4.6 M15.6 7.4l4.6 4.6-4.6 4.6 M13.4 5.4l-2.8 13.2` |
| code block | `M4.4 8.8v9.4a1.6 1.6 0 0 0 1.6 1.6h12a1.6 1.6 0 0 0 1.6-1.6V8.8 M8.6 4.4 6 7l2.6 2.6 M15.4 4.4 18 7l-2.6 2.6 M12.9 3.6l-1.8 7` |
| more formatting | `M5 5.2h14 M5 18.8h14 M3.6 12h16.8 M7.4 8.6h9.2 M7.4 15.4h9.2` |
| emoji | `M3.4000000000000004 12a8.6 8.6 0 1 0 17.2 0a8.6 8.6 0 1 0 -17.2 0Z M8.4 14.2a4.4 4.4 0 0 0 7.2 0 M9.3 9.8v.6 M14.7 9.8v.6` |
| mention | `M8.6 12a3.4 3.4 0 1 0 6.8 0a3.4 3.4 0 1 0 -6.8 0Z M15.4 8.8v4.4a2.4 2.4 0 0 0 4.8 0V12a8.2 8.2 0 1 0-3.4 6.6` |
| video clip | `M4 6.8h9.6a1.4 1.4 0 0 1 1.4 1.4v7.6a1.4 1.4 0 0 1-1.4 1.4H4a1.4 1.4 0 0 1-1.4-1.4V8.2A1.4 1.4 0 0 1 4 6.8Z M15 10.6l5.6-3.2v9.2L15 13.4` |
| audio clip | `M12 3.6a2.6 2.6 0 0 1 2.6 2.6v5.2a2.6 2.6 0 0 1-5.2 0V6.2A2.6 2.6 0 0 1 12 3.6Z M6.4 11.2a5.6 5.6 0 0 0 11.2 0 M12 16.8v3.6` |
| shortcuts | `M6.4 4.2h11.2a2.2 2.2 0 0 1 2.2 2.2v11.2a2.2 2.2 0 0 1-2.2 2.2H6.4a2.2 2.2 0 0 1-2.2-2.2V6.4a2.2 2.2 0 0 1 2.2-2.2Z M14.2 7.6l-4.4 8.8` |
| send (filled) | `M3.6 4.2 21 12 3.6 19.8 5.9 12Z` |
| kebab (filled) | `M10.5 5.4a1.5 1.5 0 1 0 3.0 0a1.5 1.5 0 1 0 -3.0 0Z M10.5 12a1.5 1.5 0 1 0 3.0 0a1.5 1.5 0 1 0 -3.0 0Z M10.5 18.6a1.5 1.5 0 1 0 3.0 0a1.5 1.5 0 1 0 -3.0 0Z` |
| More (filled) | `M3.5 12a1.7 1.7 0 1 0 3.4 0a1.7 1.7 0 1 0 -3.4 0Z M10.3 12a1.7 1.7 0 1 0 3.4 0a1.7 1.7 0 1 0 -3.4 0Z M17.1 12a1.7 1.7 0 1 0 3.4 0a1.7 1.7 0 1 0 -3.4 0Z` |
| star (outline) | `M12.00 3.40 L14.41 9.08 L20.56 9.62 L15.90 13.67 L17.29 19.68 L12.00 16.50 L6.71 19.68 L8.10 13.67 L3.44 9.62 L9.59 9.08 Z` |
| settings gear (stroke both) | `M18.84 10.50 L21.13 10.85 L21.13 13.15 L18.84 13.50 L17.90 15.77 L19.27 17.64 L17.64 19.27 L15.77 17.90 L13.50 18.84 L13.15 21.13 L10.85 21.13 L10.50 18.84 L8.23 17.90 L6.36 19.27 L4.73 17.64 L6.10 15.77 L5.16 13.50 L2.87 13.15 L2.87 10.85 L5.16 10.50 L6.10 8.23 L4.73 6.36 L6.36 4.73 L8.23 6.10 L10.50 5.16 L10.85 2.87 L13.15 2.87 L13.50 5.16 L15.77 6.10 L17.64 4.73 L19.27 6.36 L17.90 8.23 Z` and `M8.9 12a3.1 3.1 0 1 0 6.2 0a3.1 3.1 0 1 0 -6.2 0Z` |
