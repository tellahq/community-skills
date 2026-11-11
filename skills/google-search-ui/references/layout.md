# Google Search UI: layout, icons and type metrics

Everything here is in canvas pixels on a 1920 × 1080 document, measured from a macOS Chrome window with
the Google homepage and a results page (2× screenshots scaled by 0.72, so 1 CSS px ≈ 1.44 canvas px).
Colours are sampled from those screenshots. Use it as the default geometry, then check your frame
against the user's own screenshot if they give one.

## Window and Chrome

| Piece | Geometry | Colour |
|---|---|---|
| Backdrop | full frame | `#e4e8ee` |
| Window frame | x 40, y 20, 1840 × 1040, radius 20, vertical gradient `#c9d5ef` → `#d6dbe6` (5.6 %) → `#d9dce2` → `#cfd2d9`; shadows: blur 64 dy 28 `#1b2a44` 28 % and blur 10 dy 4 black 18 % | |
| Window edge / body / bevel | edge: 1 px stroke black 22 % at radius 20.5 just outside the frame; body: x 41, y 21, 1838 × 1038, radius 19; bevel: 1 px white stroke inset 1.5 px, 95 % at the top fading to 12 % | body `#ffffff` |
| Tab strip | y 21 → 78, top corners follow the window, vertical gradient | `#e0e9fd` → `#d2dffa` |
| Traffic lights | centres x 68.8 / 101.9 / 135.8, y 49.5; r 9.6 disc with a radial gradient (centre 5 px low, light core, darker ring) and a 0.75 px black 25 % drop shadow, under an r 9.1 1 px stroke that is light at the top and saturated at the bottom | red `#e0746a`/`#e25c4f`, then amber and green in the same pattern (`#f4c855`, `#91d06c` family) |
| Tab search button | x 174, y 29, 38.5 × 39, radius 9, chevron 19 px | `#edf3fd` |
| Active tab | x 222.9 → 554, top y 28.6, top radius 10, bottom flares of radius 9 into the toolbar | `#ffffff` |
| Favicon | centre (243.8, 49.5), arcs r 7.4, stroke 3.6 | see Brand marks |
| Tab title | x 267.5, centre y 49.5, Inter 18.5 | `#1f1f1f` |
| Tab close ✕ / new tab + | (532.5, 49.5) 17 px / (583.6, 49.5) 20 px | `#1f1f1f` |
| Toolbar | y 78 → 144.5, hairline at 143.5 (1.5 px) | `#ffffff`, line `#e1e3e1` |
| Back / forward / reload | x 73 / 124 / 176.8, centre y 110.7, 23 px, stroke 2.3 | `#474747`, forward disabled `#a8a8a8` |
| Omnibox | x 214, y 86.2, 1387 × 49, radius 24.5 | `#eef2f9` |
| Site-info disc + tune icon | centre (238.7, 110.7), r 17.3 | disc `#ffffff`, icon `#474747` |
| URL | x 269, Inter 21; host `#1f1f1f`, path and query `#5f6368`; long URLs masked by a rect x 150 → 1539 with feather 26 | |
| Star | centre x 1570, 23 px | `#474747` |
| Extensions | the puzzle piece only, centre x 1636; divider x 1678, y 99.7, 1.5 × 22 | puzzle `#474747`, divider `#c7d3ee` |
| Profile pill | x 1699, y 86.2, 112 × 49, radius 24.5; avatar r 14.5 at x 1722 with an Inter 700 15 initial; label Inter 20 at x 1745 | `#d6e2fb`, avatar `#7c5cc4`, label `#0b1d46` |
| Menu ⋮ | x 1847.6, dots r 2.1, 6.5 apart | `#474747` |

The page area is y 144.5 → 1060. Clip it with one rect mask (x 40, y 144.5, 1840 × 915.5, radius 20).

## Google homepage

| Piece | Geometry | Style |
|---|---|---|
| Gmail / Images | centres x 1544.5 / 1621.7, y 186.3 | Inter 19.5 `#1f1f1f` |
| Apps grid | centre (1702.5, 186.3), 3 × 3 dots r 2.6, 8.6 apart | `#474747` |
| Sign in | x 1744.6, y 157.5, 121 × 57.5, full radius | `#2656c9`, Inter 500 20 white |
| Wordmark | centred on x 960, letters spanning about x 751 → 1170, baseline about y 382 (cap height ~98 px): set as Poppins 500 about 140 px (caps ≈ 0.7 em) | per-letter colours `#3186ff #fc413d #ffbe00 #3186ff #00af57 #fc413d` |
| Search box | x 465.5, y 454, 989 × 75, radius 37.5, 1 px `#dadce0` rim, shadow blur 8 dy 2 at 10 % | `#ffffff` |
| Box contents (centre y 491.5) | + at x 502 (28 px); text and caret from x 538 (Inter 23); ✕ x 1146 and divider x 1172 while there is text; mic x 1204.6 (30 px); lens x 1262.3 (30 px) | `#1f1f1f` |
| AI Mode pill | x 1304, y 467, 136.8 × 48, radius 24; icon at x 1327, label x 1345 Inter 21.5 | `#f2f4f7`, label `#16171a` |
| Chips (centre y 602.6, 60.5 tall) | x ranges 532.3–746.2, 759.1–975.8, 988.1–1171, 1183.2–1387.7; icon 31.7 in, label 58 in, Inter 22 | `#f2f4f7`, text `#16171a` |
| Footer | country at (82.5, 957.8); rule at y 993; links at y 1026 (About 90.4, Advertising 185.8, Business 328.7, How Search works 454; Privacy 1549.5, Terms 1659, Settings 1757.6) | Inter 20.5 `#1f1f1f`, rule `#d2d2d2` |

Autocomplete card (open while there is text): white, same x and top as the box, height
75 + 8 + 5 × 52 + 14 = 357, radius 30, shadow blur 14 dy 4 at 28 %; a divider at y 528 inset 22 px
(`#e8eaed`); five 52 px rows, magnifier 20 px `#5f6368` at x 503, text at x 538 Inter 23 `#1f1f1f`
with the typed prefix at 400 and the rest of the suggestion at 700.

## Results page

| Piece | Geometry | Style |
|---|---|---|
| Wordmark | from x 191, letters spanning about y 197 → 238 (cap height ~31 px): Poppins 500 about 44 px | same colours |
| Search box | x 385.6, y 182.7, 1044 × 75, centre y 220.2 | as on the homepage |
| Box contents | query x 415.8 Inter 24.5; ✕ x 1261.8 (28 px, stroke 2.8); divider x 1293.5; mic x 1328.8; lens x 1386.4 | `#1f1f1f` |
| Right icons (y 220.2) | gear 1566.8, share 1625, apps 1688.6, Sign in x 1729.5 (121 × 57.5) | `#474747` |
| Tabs (centre y 314.5) | lefts: AI Mode 190, All 302.8, Images 361, Videos 463, News 562.6, Short videos 648, Web 802, More 879, Tools 987; ▾ 10 px after More and Tools | Inter 500 21; active `#16171a`, rest `#717579` |
| Active underline | x 302.3, y 339.5, 26.3 × 4.5, radius 2 | `#1f1f1f` |
| Tab rule | y 344, full width, 1.4 px | `#e1e3e1` |
| Refinement chips (centre y 381.4, 49 tall) | start x 190, width = label × 1.1 + 46, gap 9.7, 1.4 px rim | rim `#d2d2d2`, fill white, Inter 22 `#1f1f1f` |
| Favicon | centre (209.9, 485), r 20.5 rim `#dadce0` around an r 19.4 `#f8f9fa` disc | |
| Site name / URL | x 247.4; name centre y 470 Inter 21 `#16171a`; URL centre y 497 Inter 17.3 `#4e5156`; ⋮ after the URL | |
| Title | x 189.8, centre y 537, Inter 30 | `#180ea4` (visited `#681da8`) |
| Snippet | x 189.8, first line centre y 576, Inter 21, line height 1.476, box 935 wide | `#4f4f4f` |
| Sitelinks | rules at y 652, 755.5, 858.6, 961.7 (x 189.8, 928.8 wide, `#dadce0`); title +38 Inter 28.5 `#1f1f1f`; snippet +71.5 Inter 21 `#4f4f4f`; chevron at x 1093.4, +51 | |

## Icon paths

All are drawn in a 24-unit box centred on (12, 12): scale by size / 24 and translate to the icon's
centre (every command below is absolute, so map each point). Stroke widths are in the same units.

| Icon | Path (stroke unless noted) |
|---|---|
| Back | `M19.5 12 L4.8 12 M11 5.8 L4.8 12 L11 18.2` |
| Forward | `M4.5 12 L19.2 12 M13 5.8 L19.2 12 L13 18.2` |
| Reload | arc `M18.6 12.6 A6.7 6.7 0 1 1 16.3 7` + filled head `M13.2 7.6 L18.4 7.6 L18.4 2.4 Z` |
| Stop / close | `M6 6 L18 18 M18 6 L6 18` |
| Tune | `M11 8 L20 8 M4 16 L13 16` + circles r 2.7 at (7, 8) and (17, 16) |
| Puzzle | `M5 8 L9 8 A2.2 2.2 0 0 1 13.4 8 L17 8 L17 11.6 A2.2 2.2 0 0 1 17 16 L17 20 L5 20 Z` |
| Chevron down / right | `M6.5 9.5 L12 15 L17.5 9.5` / `M9 5.5 L15.5 12 L9 18.5` |
| Plus | `M12 4.5 L12 19.5 M4.5 12 L19.5 12` |
| Magnifier | `M10 4 A6 6 0 1 0 10 16 A6 6 0 1 0 10 4 Z M14.5 14.5 L20 20` |
| Mic | filled `M12 2.5 A3.2 3.2 0 0 1 15.2 5.7 L15.2 11.3 A3.2 3.2 0 0 1 8.8 11.3 L8.8 5.7 A3.2 3.2 0 0 1 12 2.5 Z` + stroke `M5.6 10.8 A6.4 6.4 0 0 0 18.4 10.8 M12 17.4 L12 21.2` |
| Lens | `M3.8 9 L3.8 7.8 A3.6 3.6 0 0 1 7.4 4.2 L8.6 4.2 L10 2.8 L14 2.8 L15.4 4.2 L16.6 4.2 A3.6 3.6 0 0 1 20.2 7.8 L20.2 9 M3.8 15 L3.8 16.2 A3.6 3.6 0 0 0 7.4 19.8 L9.5 19.8` + filled dots r 3.2 at (12, 12.5) and r 1.8 at (18.5, 18.5) |
| Sparkle (AI Mode, filled) | `M12 2 Q12.8 7.2 18 8 Q12.8 8.8 12 14 Q11.2 8.8 6 8 Q11.2 7.2 12 2 Z` |
| Share | `M8.5 9 L6 9 L6 20.5 L18 20.5 L18 9 L15.5 9 M12 2.8 L12 14 M8.3 6.3 L12 2.8 L15.7 6.3` |
| Paperclip | `M16.5 8.5 L9.6 15.4 A1.9 1.9 0 0 1 6.9 12.7 L14.4 5.2 A3.4 3.4 0 0 1 19.2 10 L11.6 17.6 A5 5 0 0 1 4.5 10.5 L11 4` |
| Light bulb | `M9.2 17 L14.8 17 M9.8 20.2 L14.2 20.2 M9 14.4 A6 6 0 1 1 15 14.4 L15 17 L9 17 Z` |
| Gear | a 32-point polygon alternating radius 9.2 (two points) and 7.2 (two points), plus a circle r 4 |

Cursors, hotspot at (0, 0), drawn at 1.55×, each with a drop shadow (black 30 %, dy 2, blur 3). The
example places macOS-style cursor PNGs at these sizes instead (arrow 77 × 111 from (-12.5, -11.2), I-beam
56 × 53 centred, hand 87 × 87 from (-32.6, -20.4)); draw these paths unless the user attaches their own:
- Arrow: `M0 0 L0 24.5 L5.8 19 L9.9 28.6 L13.7 27 L9.7 17.7 L17.4 17.7 Z`, black fill over a white 3.6 stroke.
- I-beam: `M-5 -13 Q-1 -13 0 -10.5 Q1 -13 5 -13 M0 -10.5 L0 10.5 M-5 13 Q-1 13 0 10.5 Q1 13 5 13 M-3 0 L3 0`, black 1.9 stroke over white 5.
- Pointing hand: `M-2.2 1.4 Q0 -1.2 2.2 1.4 L2.2 12.4 Q3 10 5.2 10.4 Q7.2 10.9 7.2 13.2 Q8 11.3 10.2 11.8 Q12.1 12.3 12.1 14.6 Q13 13 15 13.8 Q16.6 14.6 16.6 17 L16.6 23.5 Q16.6 29.5 12.4 32.6 L3.3 32.6 Q0.6 31 -1.6 27.2 L-7.6 18.6 Q-8.8 16 -6.6 15.2 Q-4.6 14.7 -2.2 17.6 Z`, white fill, black 1.7 stroke, finger lines `M7.2 13.2 L7.2 19 M12.1 14.6 L12.1 19.5`.

## Inter advance widths (per 1000 em)

Tella Motion has no text measuring, so place a caret, an underline or a pill from these. Width of a
string at size s = sum of advances × s / 1000 (Inter's kerning changes it by well under 1 %).

Inter 400:
a 562 b 612 c 571 d 612 e 583 f 370 g 613 h 591 i 242 j 242 k 549 l 242 m 876 n 591 o 600 p 612 q 612 r 376 s 528 t 327 u 591 v 562 w 818 x 546 y 562 z 552;
space 281, 0 631 1 407 2 610 3 618 4 646 5 608 6 620 7 566 8 619 9 620, `.` 288 `,` 288 `-` 460 `?` 511 `&` 644 `+` 662 `/` 360 `:` 288 `|` 333;
A 690 B 654 C 730 D 722 E 601 F 590 G 746 H 743 I 269 J 571 K 672 L 565 M 903 N 753 O 765 P 639 Q 765 R 644 S 642 T 646 U 744 V 690 W 985 X 682 Y 679 Z 629.

Inter 700:
a 581 b 630 c 588 d 630 e 596 f 398 g 632 h 623 i 271 j 271 k 580 l 271 m 913 n 623 o 613 p 630 q 630 r 407 s 560 t 366 u 623 v 600 w 850 x 580 y 602 z 573; space 237.

Example: "tella ai video editor" at 23 px is 205 px wide, so after the last key the caret sits at
538 + 205 = 743.
