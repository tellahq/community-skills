# iMessage 16:9 layout in points

Every value is in iPhone points on the 393 × 852 pt screen, from its top-left corner. On the 1920 × 1080 canvas the screen's top-left is at (739.9, 62.9) px and k = 1.12: x px = 739.9 + x × 1.12, y px = 62.9 + y × 1.12, sizes × 1.12. Read from the example document (Grant's edit of the iOS Messages look, light mode, iPhone 15/16 Pro proportions). `addTitle` boxes take the top of the first line's box, so text below is given as box tops.

Bubble y values are for the first bubble at 226 pt with nothing scrolled; the thread scrolls as one group (`thread.scroll`).

## Status bar and island

| Part | Position and size |
|---|---|
| Time "9:41" | Inter 16.5, 650 (the semibold file), −0.01 em, box 71.5 wide centred on x 71.1, box top 19.5 |
| Signal | 4 bars 3.2 wide, 4.9 apart from x 283.2, heights 4.6 / 6.8 / 9.2 / 11.6, bottoms on y 35, radius 1 |
| Wi-Fi | 3 filled wedges ±40° about (317.25, 35.6): radius 0–4.1, 6.2–8.2, 10.2–12.3 |
| Battery | outline 22.6 × 11.8 at (334.6, 23.6), radius 3.6, 1 pt stroke `#A3A3A6`; fill 18.6 × 7.8 at (336.6, 25.6), radius 1.9, black; nub 1.4 pt stroke x 358.6, y 27.6–31.4, `#9C9CA0` |
| Dynamic Island | 122 × 36.6 at (135.5, 12.6), radius 18.3, black; lens circle 10.4 at centre (239.4, 30.9) `#0E0F16`, inner 4.8 `#1C2238` |
| Home indicator | 134 × 5, centred, top 839, radius 2.5, black |

## Header

| Part | Position and size |
|---|---|
| Back button | white circle 44, centre (38, 80.5), `dropShadow` black 9 %, blur 15, dy 3; chevron stroke 2.35 round, (39.2, 72.3) → (31.3, 80.4) → (39.2, 88.4) |
| FaceTime button | white circle 44, centre (357, 80.5), same shadow; body rounded rect 16.6 × 15.2 at (345.6, 72.9), radius 3.6, stroke 1.85; lens (362.2, 78.2) → (368.8, 74.4) → (368.8, 86.6) → (362.2, 82.8), stroke 1.85 round join |
| Avatar | circle 59.2, centre (196.5, 87.3). Photo or illustration: ring `#FCC6D3` behind, image destination 121.2 × 68.2 (its own 16:9) centred on the circle, `fit: "fill"`, ellipse mask on the circle. Initials: linear gradient `#A8ADBA` → `#868B99` top to bottom, the initial in Inter 26, 600, white, centred |
| Name pill | white, 32.5 tall, top 112.5, radius 16.25, centred; 13 padding, name, 4.2 gap, chevron, 13 padding; shadow black 8 %, blur 14, dy 3 |
| Name | Inter 16.5, 700, −0.02 em, box top 118.2 |
| Name chevron | stroke 1.9 `#BDBDC1`, 3.2 wide, 8 tall, top 124.4 |

## Thread

| Part | Position and size |
|---|---|
| "iMessage" | Inter 11, 400, −0.01 em, `#8A8A8E`, centred on x 196.5, box top 165.3 (group `brand:imessage-label`) |
| Lock + "Encrypted" | lock body 7.4 × 5.6, radius 1.2, top 183.1; shackle stroke 1.05, radius 2.1; 3.6 gap; "Encrypted" Inter 11, box top 178.0; centred as a unit |
| "Today 9:38 AM" | Inter 11, "Today" 600 and the time 400, `#8A8A8E`, centred as a unit, box top 204.7 |
| Bubble | one line 40 tall, + 22 per extra line, radius 20; width = the text's Inter width (16.5 pt, −0.02 em) + 2 × 14.6, at most 283 (72 % of the screen); text Inter 16.5, 400, −0.02 em, line height 1.3333, box at x + 14.6, top + 9.4, box width = bubble width + 30 |
| Sent | right edge x 378, `#44B5FA`, white text |
| Received | left edge x 15, `#E9E9EB`, black text |
| Gap | 10 between items |
| "Delivered" | Inter 11, 600, −0.01 em, `#7C7C80`, right-aligned to x 375, box top = bubble bottom + 6.6; the next item starts 31.4 below the bubble (10 + 21.4 for the label) |
| Delivered moving on | it shows only under the newest sent bubble: when the next sent bubble lands, the old one fades in 0.15 s and every item after it moves up 14 over 0.4 s (one `afterN` group) |
| Typing pill | 58 × 38, radius 19, received colour, in the slot of the message that replaces it; circles r 5.6 at (left + 3.2, top + 35.6) and r 2.6 at (left − 1.4, top + 42.6); dots r 4.25, `#8E8E93`, centres (left + 15.3 + 12.5 i, top + 19) |
| Photos | two tiles 118.2 × 160, 3.6 apart (240 wide; one photo is 240 × 160), left edge 15, 10 below the item above; one rounded-rect mask radius 17.9 over both; `fit: "cover"` with `align.x` on each photo's subject; no tail |
| Thread mask | rect from x −45 to 438, y 151 to 767, feather 10.7, on `thread.clip` |
| Scroll | when the newest item's bottom (its tail, 6.6 below the bubble, or its Delivered label) would pass 757, `thread.scroll` moves up so it sits at 757; example: −75 when the map card lands (0.45 s), −64 more on the send (0.42 s) |
| Tapback | white circles r 17.5 at C and r 3.9 at C + (12.8, 15.6); `#E9E9EB` circles r 16 and r 2.5 on top; C = (bubble left + 1, bubble top − 12); heart about 14 wide `#FF2D55` |

## Composer (field 774 to 812)

| Part | Position and size |
|---|---|
| "+" button | white circle 38, centre (35, 793), shadow as the header buttons; plus 14.8 wide, stroke 2 round |
| Field | white capsule 310 × 38 at (67.7, 774), radius 19, same shadow |
| Placeholder | "iMessage", Inter 16.5, 400, −0.02 em, `#C2C2C4`, x 83.6, box top 783.1 (group `brand:imessage-placeholder`) |
| Mic | `#A8ACB4`, stroke 1.5: capsule 6.2 × 10.6 at (354.4, 784.6); cup from (351.9, 791.6) to (363.1, 791.6) dipping to 796.7; stem to 801.2 |
| Typed text | as the placeholder, black, box width = its width + 30 |
| Caret | 1.9 × 21.2 at (83, 782.4), radius 1, `#007AFF`; `x` keyed (hold) to the typed width + 0.6, × 1.12 in px |
| Send button | `#0A84FF` circle 29, centre (359.9, 793); arrow stroke 2.4 round, white, 13 tall, head 5.6 each side |

## Tail path

For a sent bubble with body left L, right R, top T, bottom B and r = min(20, (B − T) / 2) (mirror x about the bubble for a received one):

```
M L+r,T  H R-r  (arc r to R,T+r)  V B-r
C R,B-r+9  R-2.6,B-4.2  R-8.3,B-1.4
C R-9.6,B+0.6  R-9.4,B+3.6  R-7.9,B+5.6
C R-7.3,B+6.4  R-8.4,B+6.6  R-9.4,B+6.1
C R-12.5,B+4.6  R-15.5,B+1.2  R-21,B
H L+r  (arc to L,B-r)  V T+r  (arc to L+r,T)  Z
```

Write the quarter arcs as cubics (handle 0.5523 × r) so the bubble is one `addPath` in canvas pixels. Only the last bubble of a run gets the tail; the others close with an ordinary arc.

## Phone body

Concentric rounded rects around the screen, each `offset` pt outside it with corner radius 55 + offset, drawn outside in: 15.5 `#C6C6C8`, 14.6 `#8B8B8D`, 13.4 `#B9B9BB`, 11.2 `#E2E2E3`, 9.0 `#F3F3F3`, 7.9 `#3B3B3C`, 6.6 `#000000`, then the screen (radius 55, white). Side buttons `#A9A9AC`, 3 wide, radius 1.4, under the rims: left at x −18.2 for y 166–208, 237–303 and 321–387; right at x 408.2 for y 259–363.

## Map card (a shared location)

At the received margin, 10 below the item above. Card 240 × 178.6, masked by the received bubble path for that size (tail at the bottom left). From the card's top-left:

| Part | Position and size |
|---|---|
| Card | the bubble path filled `#E9E9EB` (this is the footer) |
| Map area | 240 × 134 from the top, land `#F3F0E9` |
| Park | `#CBE8C1` quad in the top-right corner, about 112 × 35 |
| Water | `#A9D4F6` patch at the bottom-left, about 30 × 25 |
| Blocks | six or seven `#E9E4DA` quads about 30–43 × 20 between the streets, tilted with them |
| Streets | two across, rising about 6° to the right (28.5 over 259), and four down, leaning about 6° the other way; casing `#DCD6CA` 6.4 wide under white 5 wide, butt caps; draw them 5 past the map's edges |
| Main road | one across-street through the middle (y about 84 at the left), `#FCE38F` 7.1 wide over casing `#E9CB6C` 8.6 wide |
| Pin | head r 11.6 `#FF3B30` with a white dot r 4.1, centre (127, 46.5); stem 2 wide `#9A9AA0` dropping 14.7; shadow oval 14.3 × 4.9, black 22 %, at the stem's foot |
| Pin label | the place's name, Inter 9.3, 700, `#C7332B`, x pin + 16, centred on the head |
| Title | the place's name, Inter 14.5, 600, −0.016 em, black, x 14.2, box top 141.2 |
| Address | Inter 11, 400, `#7C7C80`, x 14.2, box top 159.1 |

## Camera

`camera` is a group around `phone` with `anchorX` 960 and `anchorY` 540, keyed on `scale`, `x` and `y`, plus one `blur` effect (`effectId` `camblur`). To centre point (cx, cy) px at scale s: x = (960 − cx) · s, y = (540 − cy) · s.

| Time (s) | Shot | Centre (pt, scrolled) | Scale |
|---|---|---|---|
| 0–1.5 | whole phone, rising 20.5 px | — | 0.93 → 0.975 → 1 |
| 1.5 | first message, framed low so the reply's slot shows | (136.6, 270.6) | 5.933 → 6.4 → 6.5 |
| 2.3–2.95 | glide to the sent reply | (196.5, 298) | → 4.45 → 4.52 |
| 3.5 | dots and the answer | (196.5, 344) | 3.764 → 3.9 → 3.96 |
| 6.0 | photos | (181, 501) | 4.69 → 4.9 → 5 |
| 7.35–8.0 | glide to the sent reply | (196.5, 537) | → 4.4 → 4.5 |
| 8.7 | whole phone (dots, then the map card lands and scrolls) | — | 0.953 → 1 → 1.05 |
| 11.3 | map card | (186, 664) | 4.467 → 4.7 → 4.85 |
| 13.0 | composer (typing) | (196.5, 734) | 3.377 → 3.5 → 3.56 |
| 14.8–15.45 | glide up with the send | (196.5, 717) | → 3.7 → 3.75 |
| 16.0 | the reply and its tapback | (249.5, 695) | 5.664 → 6 → 6.2 |
| 17.6–18.1 | glide back to the whole phone | — | → 0.985 → 1.02 at 19.5 |

Each cut: a hold key 2 ms before, the jump value (93–96.5 % of the settle) with cubic-bezier (0.1, 0.6, 0.4, 0.9) for 0.35 s to the settle, then linear drift (1.5–3 %) to the next key. Glides use cubic-bezier (0.4, 0, 0.2, 1) over 0.65 s; the last pull-back uses (0.3, 0, 0.1, 1) over 0.5 s. Blur on each cut: 2.0–3.6 px into a close-up, 10.5–10.75 px into a wide shot (and at 0 s), easeOutCubic to 0 in 0.23 s.

For other content, frame each close-up on a box: the item (and what lands next to it), with about 1.2× margin on the side that binds: s = min(1920 / (1.12 × 1.2 × box width), 1080 / (1.12 × 1.2 × box height), 6.4). A tapback shot's box runs from the tapback's left edge (C − 17.5) to the bubble's right edge.

## Colours

| Part | Light (from the example) | Dark (not measured) |
|---|---|---|
| Backdrop / screen | `#F5F5F7` / `#FFFFFF` | `#1C1C1E` / `#000000` |
| Sent bubble / text | `#44B5FA` / white | `#0A84FF` / white |
| Received bubble / text | `#E9E9EB` / black | `#262628` / white |
| Labels, stamp / Delivered | `#8A8A8E` / `#7C7C80` | `#8D8D93` |
| Glass controls / icons | white + soft shadow / black | `#1C1C1E` / white |
| Placeholder / mic | `#C2C2C4` / `#A8ACB4` | `#6A6A70` |
| Send button, caret | `#0A84FF`, `#007AFF` | `#0A84FF` |
| Generic green | `#34C759` | `#30D158` |
| Avatar ring / heart | `#FCC6D3` / `#FF2D55` | same |
| Map land / footer / streets | `#F3F0E9` / `#E9E9EB` / white | try `#2C2C2E` / `#262628` / `#3A3A3C` |
