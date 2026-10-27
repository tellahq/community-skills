---
name: kaleidoscope-tile-glitch
description: >-
  Turn a photo into a looping kaleidoscope animation that breaks the image into
  2×2, 4×4 and 8×8 tiles that glitch around, then settles a quarter turn
  further. Rendered as a video with a script and placed as b-roll. Use when the
  user wants the kaleidoscope or tile-glitch effect on an image.
metadata:
  based-on: >-
    tellahq/community-skills/kaleidoscope@1d02577b8e12b2986111498cd79f61aad5db89d5
  author: Michiel Westerbeek
---
# Kaleidoscope (rendered version)

Copy the effect in `references/reference.mp4` onto the user's image.

## The effect

- The photo fills a square frame.
- It splits into a 2×2 grid, then 4×4, then 8×8. At each step the tiles glitch: they jump, swap, zoom and flicker for a few frames.
- The tiles come back together as the whole photo, turned a quarter turn further than before.
- Then it repeats from that angle. Two turns take about 8.6 s.

## Steps

1. Look at the reference first (`ffmpeg -i references/reference.mp4 -vf fps=3,scale=200:-1,tile=8x6 sheet.png`, then `view_image`) so pacing and tile steps match.
2. Use the image the user names or attaches. If there is none, ask; never pick one.
3. Render it as a video rather than building 64 animated tiles in freeform: copy `references/kaleidoscope.py`, set `SRC` to the image, make a `fr/` folder, and run it (`pip install --break-system-packages numpy pillow` first; about 50 s for 258 frames at 720x720, so run it in the background). Then `ffmpeg -framerate 30 -i fr/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4`.
4. Check a contact sheet of the output against the reference: grid steps, glitch length, the quarter turn.
5. Upload with `create_source` (kind video, 720x720, duration 8.6), `curl -T` to the uploadUrl, `wait_for_jobs` on the source, then place it: `add_layout` with `media: {type: 'video', sourceId, muted: true}` over the clip's range (b-roll, keeps the video length), or `upload_clip` if the user wants it as its own clip. Say that the animation is 8.6 s and is cut off if the clip is shorter.

## Timing of one turn (4.3 s)

0-0.4 s whole photo; 0.4-1.2 2×2 glitch; 1.2-2.0 4×4; 2.0-2.8 8×8; 2.8-3.9 the 8×8 tiles settle back (fewer scrambled tiles over time) while the whole image rotates 90° with smooth easing; 3.9-4.3 hold at the new angle. The glitch state changes every 2 frames at 30 fps. Each scrambled tile takes a random tile from the image, may zoom in on half of it, and turns by a random multiple of 90°.

## Making it your own

- Fewer or more turns change the length (the frame count `N`).
- Shorter stage times are more frantic; longer ones calmer.
- Stopping at 4×4 gives a chunkier look.
