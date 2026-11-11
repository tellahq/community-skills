# iMessage layout in points

Measured from a screenshot of the current iOS Messages app (light mode, iPhone 15/16 Pro, 393 × 852 pt screen). Every value is in iPhone points from the screen's top-left corner. In Tella Motion, x px = screen left + x × k and y px = screen top + y × k, with k = 2.05 for the phone filling 1080 × 1920 (screen at x 137.2, y 86.7 px, 806 × 1747 px). Sizes in px are the pt value × k.

Bubble y values below are for the first bubble at 226 pt with nothing scrolled; the thread scrolls as one group (`thread.scroll`).

## Status bar and island

| Part | Position and size |
|---|---|
| Time "9:41" | Inter 16.5, weight 650, −0.01 em, centred on x 71.1, cap top 23.4 |
| Signal | 4 bars 3.2 wide, 4.9 apart from x 283.2, heights 4.6 / 6.8 / 9.2 / 11.6, bottoms on y 35, radius 1 |
| Wi-Fi | 3 filled wedges ±40° about (317.25, 35.6): radius 0–4.1, 6.2–8.2, 10.2–12.3 |
| Battery | outline 22.6 × 11.8 at (334.6, 23.6), radius 3.6, 1 pt stroke `#A3A3A6`; fill 18.6 × 7.8 at (336.6, 25.6), radius 1.9, black; nub 1.4 pt stroke x 358.6, y 27.6–31.4, `#9C9CA0` |
| Dynamic Island | 122 × 36.6 at (135.5, 12.6), radius 18.3, black; lens circle 10.4 at centre (239.4, 30.9) `#0E0F16`, inner 4.8 `#1C2238` |
| Home indicator | 134 × 5, centred, bottom 8 above the screen's bottom, radius 2.5, black |

## Header

| Part | Position and size |
|---|---|
| Back button | white circle 44, centre (38, 80.5), shadow black 9 % blur 15 dy 3; chevron stroke 2.35 round, (39.2, 72.3) → (31.3, 80.4) → (39.2, 88.4) |
| FaceTime button | white circle 44, centre (357, 80.5), same shadow; body rounded rect 16.6 × 15.2 at (345.6, 72.9), radius 3.6, stroke 1.85; lens: (362.2, 78.2) → (368.8, 74.4) → down to (368.8, 86.6) → (362.2, 82.8), stroke 1.85 round join |
| Avatar | circle 59.2, centre (196.5, 87.3), ring colour `#FCC6D3` behind the image |
| Name pill | white, 32.5 tall, top 112.5, radius 16.25, centred; padding 13 left, name, 4.2 gap, chevron, 13 right; shadow black 8 % blur 14 dy 3 |
| Name | Inter 16.5, 700, −0.02 em, cap top 122.1 |
| Name chevron | stroke 1.9 `#BDBDC1`, 3.2 wide, 8 tall, from cap top 124.4 |

## Thread

| Part | Position and size |
|---|---|
| "iMessage" | Inter 11, 400, −0.01 em, `#8A8A8E`, centred on x 196.5, cap top 167.9 (group `brand:imessage-label`) |
| Lock + "Encrypted" | lock body 7.4 × 5.6 radius 1.2 at cap top + 5, shackle stroke 1.05 radius 2.1; 3.6 gap; "Encrypted" Inter 11, cap top 180.6; centred as a unit |
| "Today 9:41 AM" | Inter 11, "Today" 600, time 400, `#8A8A8E`, centred, cap top 207.3 |
| First bubble | top 226 |
| Bubble | one line 40 tall, + 22 per extra line, radius 20 (half the one-line height), padding 14.6 each side; text Inter 16.5, 400, −0.02 em, line height 22, cap top = bubble top + 14.4 |
| Sent | right edge x 378, `#44B5FA`, white text |
| Received | left edge x 15, `#E9E9EB`, black text |
| Gap | 10 between bubbles |
| "Delivered" | Inter 11, 600, −0.01 em, `#7C7C80`, right edge 3 in from the bubble's right, cap top = bubble bottom + 9.2 |
| Typing pill | 58 × 38, radius 19, received colour; circles r 5.6 at (left + 3.2, top + 35.6) and r 2.6 at (left − 1.4, top + 42.6); dots 8.5, `#8E8E93`, centres at left + 15.3 + 12.5 i, top + 19 |
| Thread mask | rect from y 151 to 767 (under the name pill to just above the field), full screen width plus 45 each side, feather 10.7; whenever the thread's bottom passes 766, scroll `thread.scroll` up by the overflow |
| Tapback | white circle r 17.5 and r 3.9 at (+12.8, +15.6); grey `#E9E9EB` circle r 16 and r 2.5 on top; centre (message left + 1, message top − 13); heart about 15 wide `#FF2D55` |

## Composer (field bottom 812, 40 above the screen's bottom)

| Part | Position and size |
|---|---|
| "+" button | white circle 38, centre (35, 793), shadow as the header buttons; plus 14.8 wide, stroke 2 round |
| Field | white capsule 310 × 38 at (67.7, 774), radius 19, same shadow |
| Placeholder | "iMessage", Inter 16.5, 400, −0.02 em, `#C2C2C4`, x 83.6, cap top 787 (group `brand:imessage-placeholder`) |
| Mic | `#A8ACB4`, stroke 1.5: capsule 6.2 × 10.6 at (354.4, 784.6); cup from (351.9, 791.6) to (363.1, 791.6) dipping to 796.7; stem to 801.2 |
| Typed text | as the placeholder in black |
| Caret | 1.9 × 21.2 at (83, 782.4), radius 1, `#007AFF`; x keyed to the typed width + 0.6 |
| Send button | `#0A84FF` circle 29, centre (359.9, 793); arrow stroke 2.4 round, white, 13 tall, head 5.6 each side |

## Tail path

For a sent bubble with body left L, right R, top T, bottom B and r = min(20, (B − T) / 2), in points (mirror x about the bubble for a received one):

```
M L+r,T  H R-r  (arc r to R,T+r)  V B-r
C R,B-r+9  R-2.6,B-4.2  R-8.3,B-1.4
C R-9.6,B+0.6  R-9.4,B+3.6  R-7.9,B+5.6
C R-7.3,B+6.4  R-8.4,B+6.6  R-9.4,B+6.1
C R-12.5,B+4.6  R-15.5,B+1.2  R-21,B
H L+r  (arc to L,B-r)  V T+r  (arc to L+r,T)  Z
```

Write the quarter arcs as cubics (handle 0.5523 × r) so the whole bubble is one `addPath` in canvas pixels. A bubble without a tail closes its bottom-right corner with an ordinary arc.

## Phone body

Concentric rounded rects around the screen, each `offset` pt outside it with corner radius 55 + offset, drawn outside in: 15.5 `#C6C6C8`, 14.6 `#8B8B8D`, 13.4 `#B9B9BB`, 11.2 `#E2E2E3`, 9.0 `#F3F3F3`, 7.9 `#3B3B3C`, 6.6 `#000000`, then the screen (radius 55, white). Side buttons `#A9A9AC`, 3 wide, radius 1.4, behind the rim: left at x −18.2 for y 166–208 (action), 237–303 and 321–387 (volume); right at x 408.2 for y 259–363 (side button).

## Colours

| Part | Light (measured) | Dark |
|---|---|---|
| Backdrop / screen | `#F5F5F7` / `#FFFFFF` | `#1C1C1E` / `#000000` |
| Sent bubble / text | `#44B5FA` / white | `#0A84FF` / white |
| Received bubble / text | `#E9E9EB` / black | `#262628` / white |
| Labels, stamp / Delivered | `#8A8A8E` / `#7C7C80` | `#8D8D93` |
| Glass controls / icons | white + soft shadow / black | `#1C1C1E` at 90 % / white |
| Placeholder / mic | `#C2C2C4` / `#A8ACB4` | `#6A6A70` |
| Send button, caret | `#0A84FF`, `#007AFF` | `#0A84FF` |
| Generic green accent | `#34C759` | `#30D158` |
| Avatar ring / heart | `#FCC6D3` / `#FF2D55` | same |

The dark column wasn't re-measured against the current app; check it against a dark-mode screenshot before relying on it. A light brand accent on sent bubbles takes black text.
