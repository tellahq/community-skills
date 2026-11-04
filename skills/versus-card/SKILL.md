---
name: versus-card
description: >-
  Make a split-screen "this vs that" comparison card in Tella Motion: two halves
  in contrasting colours slam in from the sides (or from top and bottom in 9:16)
  along a slanted divider, a VS badge punches in where they meet, then rows of
  comparison points tick in side by side with drawn-on check and cross icons,
  timed to the speaker's words, ending with the losing side dimming and a
  WINNER pill popping in on the winning side. Works as a full-frame overlay that
  slams in over the footage, as b-roll, or as its own clip. Use when asked for a
  versus card, a VS screen, this vs that, X vs Y, old way vs new way, before vs
  after, us vs them, a side-by-side comparison or a pros and cons split.
metadata:
  title: Versus card
  author: Tella
  category: Diagrams
  image: og.jpg
  poster: gallery/paper-and-ink.webp
  preview: gallery/paper-and-ink.mp4
  prompt: When I compare status meetings with async updates, slam in a versus card with the four differences I list, and make async updates the winner.
---

# Versus card

One graphic, one comparison: the left half is the old way, the rival or "before", the right half is the new way, your product or "after". The two halves crash together along a slanted seam, a VS badge stamps onto it, and each point the speaker makes lands as a pair of rows, one per side, with a cross or a check drawing itself on. Then the loser dims and the winner gets a pill. It reads in a glance, and the motion has impact without bounce.

Also load `tella-explainer-graphics` (a comparison that builds as it is said). If a side is just a number ("3 days vs 4 hours"), use `tella-data-callouts` instead.

## Ask once

From the transcript, find the two things and each point made about them, then ask in one `ask_form`, every field prefilled:
- **The two sides**: a small label and a name each, e.g. `THE OLD WAY / Status meetings` vs `THE NEW WAY / Async updates`. Names up to about 18 characters.
- **The rows**, `left | right` per line: 3 to 5 pairs in 16:9, 3 to 4 in 9:16, each side up to about 28 characters. The speaker's words, shortened; never invent a point.
- **Ticks**: winner all checks and loser all crosses (default), or marked per row for a fair comparison.
- **Winner**: right (default), left, or none (no dim, no pill; checks on both sides suits "before vs after").
- **Look**: one of the themes below, or matched to the video.
- **Where**: over the footage (default: a transparent overlay that slams in and slides away), b-roll that hard-cuts in, or its own clip.

## Timing to the speech

- Start the card about 0.4 s before the first word of the comparison ("versus", "compared to", the first name), so the halves land on it.
- Each row starts 0.1 s before the word that names its point; the right item follows the left by about 0.25 s, or gets its own time when the speaker says the two sides far apart. Keep rows at least 0.6 s apart, even when they're said in one breath.
- The verdict lands on the word that gives it ("so…", "that's why…"), else 1 s after the last row.
- Hold the finished card at least 2 s, then exit on the speaker's next thought.

## The look

Two tones and one accent. Each half is a panel and its ink; the only saturated colour is the VS stamp and the WINNER pill. The halves contrast by value (light against dark, or two clearly different darks), never two loud hues: primary red against blue reads as a sports graphic and drowns the words.

| Look | Left: bg / text / label | Right: bg / text / label | Stamp (badge + pill) | Loser dim |
|---|---|---|---|---|
| Bone and forest | `#EFEBE3` / `#1C1B18` / `#7D776C` | `#1F3A2F` / `#F3EFE6` / `#9DB5A7` | ochre `#E2A93B`, ink text, ring `#F3EFE6` | `#EFEBE3` 0.6 |
| Stone and oxblood | `#E6E3DD` / `#1A1A1A` / `#77736C` | `#4A1D26` / `#F6EFE6` / `#C69DA5` | `#141414`, ivory text, ring `#F6EFE6` | `#E6E3DD` 0.6 |
| Blackout (dark footage) | `#4A4D55` / `#FFFFFF` / `#B9BCC3` | `#0E0F11` / `#FFFFFF` / `#8E9196` | lime `#D4F24A`, ink text, ring `#0E0F11` | black 0.55 |
| Paper and ink | `#EDE7DC` / `#1B1B1F` / `#7A746A` | `#16161A` / `#F5F1EA` / `#A39E95` | `#FF5B35`, white text, ring `#F7F3EC` | `#F7F3EC` 0.6 |
| Graphite vs indigo | `#262A33` / `#FFFFFF` / `#9AA1AE` | `#4F46E5` / `#FFFFFF` / `#C7C4FF` | `#FFD43B`, ink text, ring `#0B0C10` | black 0.5 |

- **Icons.** In the first three looks, icons stay in the side's own tones: a check is a solid disc in the side's ink with the glyph in the panel colour, a cross a quiet tonal disc (`#D8D2C6` on bone, `#355246` on forest) with an ink glyph. Paper and ink and Graphite vs indigo use green check (`#34D399`, `#1F9D55` on a light half) and red cross (`#F0565A`, `#E5484D`) discs with white glyphs. The loser's row text is a softer tint of its ink; never grey out the winner.
- **Matching a video:** one light and one dark tone from its palette, its brand colour only on the stamp. When the dark half loses on a light theme, dim it with black at about 0.45 instead.
- **Type.** A display font (Archivo or DM Sans) 800 for the names and 900 for "VS"; Inter for the rest. At 1080p landscape: label 26 px, 700, tracked 0.18, in the muted colour; name 80 px just under it; row text 40 px, 500; pill text 28 px, 800, tracked 0.16.
- **16:9 layout.** The seam slants about 80 px, right of centre at the top to left at the bottom. Headers near the top, centred in each half, well short of the badge. The badge (170 px disc, 7 px contrasting ring, resting at −8°, soft drop shadow) sits on the seam level with the headers. Rows from a little above the middle, about 136 px apart (tighter for 5), a 54 px icon disc then the text; the right column starts about 120 px past the seam. The pill (about 250 × 62, fully round) under the winning column, clear of the last row.
- **9:16 layout.** The halves stack, the seam sloping about 120 px across the middle. Bigger type (label 30, name 96, rows 46, icons 60), the badge 200 px dead centre, at most 4 rows per half, everything between y 200 and 1720, clear of the platform's captions and buttons.

## The motion

| Beat | When | What moves |
|---|---|---|
| Slam | 0 → 0.38 s | Each half travels in from about 0.6 of the frame off its side (top/bottom in 9:16), bezier (0.12, 0.9, 0.25, 1): fast, hard stop. A blur along the axis goes 70 → 0 px as a streak. |
| Recoil | → 0.62 s | Each half bounces ~14 px back out and settles: the crash. |
| VS punch | 0.42 → 0.78 s | Badge scale 2.4 → 0.92 → 1, rotation −24° → −8°, opacity in 0.06 s. A ring in the stamp colour scales 1 → 1.9 and fades out behind it. |
| Row tick | each row | The row fades in (0.16 s) while sliding 28 px inward (0.4 s, ease out). The icon pops 0.3 → 1 with one small overshoot; its glyph draws on just after. |
| Verdict | on the word | The loser dims over 0.5 s. The winner's name pops to 1.05 and back, the pill pops in, the winner's icons pulse once, top to bottom. |
| Exit | next thought | Halves slide back out the way they came (0.4 s, ease in) with the streak; the badge shrinks and fades in 0.2 s. |

The only overshoots are the badge stamp and the icon pop.

## Building it in Tella Motion

- An overlay is transparent and full frame; b-roll has an opaque background and hard-cuts in through `add_layout`; its own clip goes through `create_clip`.
- Panels and icon discs are paths, glyphs are stroked paths with round caps and a `trimPath` draw-on, every word a live title. The left panel reaches about 60 px past the seam, under the right one, so the recoil never opens a gap.
- Group it: disc + glyph as the icon, icon + text as the row, then each half (panel, header, rows, its dim or pill) as `A` and `B`; the badge (ring, disc, "VS") on top, its expanding ring separate. Key the slam on `A` and `B`, never on the children.
- Sound, if wanted, from `list_library` sound effects through `add_sound_effect`: a woosh on the slam, an impact on the badge, a soft success on the verdict, a woosh on the exit, all low and never under important words.

## Gotchas

- `setMotionBlur` on the half groups smeared them into ghost copies that hung on ~0.3 s after they stopped. Use a keyed `blur` effect as the streak and leave motion blur off.
- `setKeyframes` refuses an effect parameter by index ("is a keyed list: write its members by id"). Give the effect an `effectId` and key it with `node.patch` on `common.effects.<id>.effect.<param>` as `{type: "keyframes", timeDomain: "local", keyframes: [{id, time, value, easing}]}`, times in ticks. The trim draw-on and the streak blur both need this.
- Paths and groups scale and rotate about the canvas centre until you set `anchorX`/`anchorY` to their own centre (x/y are offsets, so this doesn't move them). Do it for every icon, the badge, its ring, the winner's name and the pill.
- A document plays in one place only: a second card is `duplicate_motion_document` with new titles.
- A transparent overlay renders black where it's empty in `get_motion_frame`; judge its edges in the video.

## Check

One `get_filmstrip` of the document at 0.1 s (streaked halves), 0.5 s (badge mid-stamp), each row + 0.2 s (glyph half drawn), the verdict + 0.6 s and the last held frame, then the same moments in the video. Look for a name touching the badge, row text crossing the seam, a seam opening in the recoil, the pill crowding the last row, and every word against the transcript; shorten the words before shrinking the type. Report each row with its time, the winner, and any wording you shortened.

## Making it your own

- Three rows feel punchy; five is the most that reads. Past that, split it into two cards.
- Flip the winner to the left for "the classic still wins"; the dim and pill follow.
- "OR" works in place of "VS" (two or three letters fit the disc), and `OUR PICK` or `NEW` in place of WINNER with a slightly wider pill.
