---
name: kaleidoscope
description: Turn a photo into a looping kaleidoscope animation that breaks the image into 2×2, 4×4 and 8×8 tiles that glitch around, then settles a quarter turn further. Use when the user wants this kaleidoscope or tile-glitch effect on an image.
metadata:
  title: Kaleidoscope
  author: Tella
  category: Full animations
  image: og.jpg
---

# Kaleidoscope

Copy the effect in `references/reference.mp4` onto the user's image.

## The effect

- The photo fills a square frame.
- It splits into a 2×2 grid, then 4×4, then 8×8. At each step the tiles glitch: they jump, swap and flicker for a few frames.
- The tiles come back together as the whole photo, turned a quarter turn further than before.
- Then it repeats, so the end of one turn matches the start of the next and it loops cleanly. Two turns take about 8.6 s.

## Steps

1. Watch the reference before building anything. Pull frames with ffmpeg (`ffmpeg -i references/reference.mp4 -vf fps=4,scale=320:-1 frame_%03d.png`, or a contact sheet with `tile`) and look at them with `view_image`, so the pacing and tile steps match.
2. Use the image the user names or attaches. If there isn't one, ask which image to use. Don't pick one yourself.
3. Build it as a freeform motion graphic. Load `tella-motion-design` first for the shared rules.
4. Preview the result and compare it with the reference: grid steps, glitch length, the quarter turn, and a seamless loop.

## Making it your own

- Fewer or more turns change the length.
- Faster tile steps make it more frantic; slower ones make it calmer.
- A different final grid (for example stopping at 4×4) gives a chunkier look.
