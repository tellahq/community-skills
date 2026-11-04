---
name: camcorder-hud
description: >-
  Make a Tella video look like a home-video recording on an old camcorder by
  adding a viewfinder HUD over the whole video: white corner brackets, a
  blinking red REC, SP with a battery icon, a tape counter and a running
  clock above a date stamp, all in the VT323 pixel font. Built as editable
  Tella Motion overlays, one per clip, timed so the counter, clock and blink
  run on across cuts. Works in 16:9 and 9:16. Use when asked for a
  camcorder, camcorder HUD, home video, homevideo, found-footage, handycam
  or 'old cam' look, a REC overlay, or a viewfinder overlay. Needs the Tella
  Motion tools.
metadata:
  title: Camcorder HUD
  author: Louise de Sadeleer
  category: Editing
  image: og.jpg
  poster: references/reference-landscape.jpg
  prompt: Make this video look like it was filmed on an old camcorder, with a REC light, tape counter and date stamp.
---
# Camcorder HUD

Adds a camcorder viewfinder over every clip of a video, so it looks like a home video shot on an old camcorder. See `references/reference-landscape.jpg` for the finished look on a 16:9 video.

## The look

- **Corners:** thin white viewfinder brackets near each corner.
- **Top left:** a red dot that blinks (on for the first half of every second, off for the second half), followed by REC.
- **Top right:** SP, then a battery outline with three bars and a nub.
- **Bottom left:** a tape counter (0:00:00) that ticks up once a second.
- **Bottom right:** a running clock (11:47:03 PM) above a date stamp (OCT. 31 2026).
- **Type:** everything is white VT323, a free Google pixel font under the OFL licence. There's no shadow, outline, grain or scanlines.
- **The footage is not touched.** The HUD is graphics only: no VHS noise, colour bleed or film texture on the footage, unless the user asks for it explicitly.
- **Timing:** the counter, clock and blink are timed on whole-video time, so they carry on across cuts without a jump.

## Steps

1. **Read the video.** Call `get_timeline` (video dimensions, and each clip's `timelineStartMs` and `durationMs`). Look at a filmstrip so you know what's on screen. Read the timeline again right before building: the user may trim clips while you work.
2. **Ask only what matters.** Fill in the defaults: date `OCT. 31 2026`, start clock `23:47:03`, counter from 0:00:00. A spooky or late-night video suits the default. Otherwise offer today's date in the same `MMM. DD YYYY` uppercase format. Don't ask about the font or the layout.
3. **Font.** Check whether VT323 is already in the library: `list_library` with `type: 'font'` (look for a family or name of VT323). If it's not there:
   - `curl -sfL -o VT323-Regular.ttf https://github.com/google/fonts/raw/main/ofl/vt323/VT323-Regular.ttf`
   - `create_source` with `kind: 'font'`, then `curl -sf -T VT323-Regular.ttf "<uploadUrl>"`
   - `add_library_item` (named VT323). Its item `id` (`mi_...`) is the `--font-id`.
   - Tell the user the font was added to their library.
4. **Build one Tella Motion document per clip.** An overlay can't span clips, and a document plays in one place only. For each clip:
   - `create_motion_document` with the `videoId`, named `Camcorder HUD <n>`.
   - Run `scripts/camcorder_hud.py` with that clip's start and duration, for example:
     `python3 scripts/camcorder_hud.py --width 1920 --height 1080 --clip-start-ms <timelineStartMs> --clip-duration-ms <durationMs> --font-id <mi_...> --date "OCT. 31 2026" --clock 23:47:03 --out hud_<n>.json`
   - Apply it with `apply_motion_editor_commands` with `commandsFile` set to that JSON path. The script sets the canvas size and length, and lays out landscape and portrait automatically: everything is scaled to the short side, and the bottom elements sit above the bottom brackets.
5. **Place them.** Add every overlay in one `apply_video_edits` call, with one `add_media_overlay` per clip:
   - `sourceId`: the document's `ffd_...` id
   - `startTimeMs` 0, `durationMs` the clip's duration
   - `point` {xPct 0, yPct 0}, `dimensions` the full video width and height
   - `transition` `hard_cut`, `depth` `front`
   Overlays added after existing ones stack on top of them, so the HUD stays above picture-in-picture videos.
6. **Check.** Call `get_filmstrip` at about 0.1 s before and after several cuts, plus a few frames mid-clip:
   - the counter and clock don't jump at a cut
   - the dot is on in the first half of each second and off in the second half
   - nothing is clipped at the frame edges
   - the HUD sits above any other overlay
   Then look at one full-size frame (`get_clip_frame`, 1280 wide) to check the dot lines up with REC.
7. **Report.** Tell the user the date and clock you used, that there's one "Camcorder HUD" overlay per clip, and that if a clip's length changes later, the counter and clock after it drift until that clip's HUD is rebuilt.

## Changing it later

- **Date:** `setTitle` on node `date` in every HUD document.
- **Clock, counter or a trimmed clip:** run the script again for the clips from the change onwards. In each document, delete the old nodes (or make a fresh document and swap the overlay), apply the new commands, and set the overlay's `durationMs` to the clip's new length.
- **Changing to 9:16 (or any new size):** rebuild every document at the new `--width`/`--height` and replace the overlays. Don't stretch the landscape ones.
- **Text in the video:** keep subtitles and text overlays clear of the bottom corners where the counter and clock sit. Centre them, or place them between the two.

## Node ids in each document

`brackets`, `rec.dot`, `rec.label`, `sp`, `batt.body`, `batt.nub`, `batt.bar0`-`batt.bar2`, `date`, and one `counter.<s>` and one `clock.<s>` per whole-video second `<s>` that the clip covers.
