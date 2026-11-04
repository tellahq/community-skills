---
name: hype-reel
description: >-
  Cut a fast, beat-synced hype reel (8–30 s) in Tella from the user's footage.
  It picks the most visual moments from storyboards and filmstrips, sets a
  curated Tella music track and reads its beats with get_music_beats. It then
  builds the reel as one Tella Motion clip: hard cuts on the beat, one or two
  speed ramps, white flash frames on a couple of downbeats, a motion-blurred
  whip in the direction of the action, one grade over everything, and a closing
  title on the last bar. Restrained but punchy. Use when asked for a hype reel,
  sizzle reel, highlight reel, montage, teaser or promo cut to music, a "sick
  edit" of their clips, or to cut footage on the beat.
metadata:
  title: Hype reel
  author: Tella
  category: Editing
  image: og.jpg
  poster: gallery/machine-age.webp
  preview: gallery/machine-age.mp4
  prompt: Make a 12-second hype reel from the clips in this video, cut to the beat, ending on "Built to move".
---

# Hype reel

A short music-driven cut: the strongest moving shots from the user's footage, one per beat or two, and a closing title. The music decides every cut, so the edit feels tight even though nothing on screen is fancy. The craft is restraint: one look, one typeface, at most two flashes, one or two whips, one or two speed ramps.

Everything except background music lives in **one Tella Motion document**: footage, grade, flashes and titles. Placed as a clip, it plays as its own short video or as the opener of an existing one. Builds on `tella-transitions` (flash and whip timing), `tella-title-cards` (the closing title) and, for vertical delivery, `tella-short` (phone safe zones).

## Ask first

Read the video and its clips, then ask once with `ask_form`, guesses filled in:

- **Footage**: default all clips in this video. With none, offer Tella's public-domain vintage library (`list_library` scope `vintage`, a search word like "rocket" or "steam train"), or up to four AI clips (`generate_video`, which costs AI credits; say so).
- **Length**: 8, 12 (default), 15 or 30 s. At 105–120 BPM, 12 s is about 6 bars and 11–13 shots.
- **Music**: energetic curated tracks with their BPM (see Tracks), or the user's own upload.
- **Closing title**: the line plus an optional small sub line, prefilled from the video's title or what the user said. Never invent a claim, date or name.
- **Shape**: 16:9 (default), 9:16 or 1:1.
- **Look**: Archival B&W, Warm tint, Teal duotone or Natural. Natural for sharp modern footage, Archival for old footage.

## Pick the moments

Scan every source with storyboards, then a denser filmstrip (250 ms apart) over a promising stretch. Rank by strong motion inside the frame (spray, sparks, smoke, wheels, a launch, a crowd surging, hands at work), then one clear subject that reads at a glance, then contrast and light (fire, flares, backlight). Skip title cards, burnt-in captions and logos, talking heads, static shots, burnt-in black borders, trademarks and brand signage. Use each clip once; only the title bed may repeat one. Vintage items become sources with `add_library_item` scope `private` (scope `video` is refused for vintage).

Note for each pick its source in-point, how long it stays good, the direction of motion and, for vertical, where the subject sits across the frame. Order them as a rise: a calm or wide opener, a run of fast close details, a hero shot with a speed ramp, then a slow, textured shot as the title bed.

## Music and the beat grid

`get_music_beats` gives `bpm`, `beatsMs` and `downbeatsMs`; below about 0.5 confidence pick another track. Two routes:

- **Background music (simplest).** `set_background_music` at about 0.8. It starts at 0, fades in over 2 s and plays under the whole video, so it only suits a track whose first hit comes early and a reel that is its own video; use the rise as a cold open (one slow shot fading up from black, first hard cut on the hit).
- **Start on the drop (stronger).** Most tracks build for 10–20 s. Read the track's beats as a source and pick an in-point on the drop's downbeat (or one beat before a re-entry, so the hit lands after a short breath). Play it as an audio node inside the document with a 1.2 s fade out. Reel time = beat time − in-point. Don't also set background music.

**Tracks** (tested; the others are too calm):

| Track | BPM | Shape |
|---|---|---|
| Modern Tech Pulse | 120 | Quiet until the drop on the 17.032 s downbeat. Start there. |
| Bright Startup Energy | 110 | Riser 0.4–2.2 s, first hit at 2.229 s. Works as background music. |
| Chill House Screenbeat | 105 | Break 17.15–18.25 s, re-enters at 18.285 s. Start one beat early, at 17.713 s. |
| Old School Hip Hop | 95 | Loose pulse (0.6 confidence). Cut on downbeats only. |

## Plan the cut

Show a table before building, one row per shot: beats, reel times, shot, in-point, speed, move. Rules that kept the examples tight:

- Cut only on beats. Most shots last 1 or 2 beats, never less than 1. Hero shots and the shot after a flash get 2.
- Downbeats carry the accents: a punch-in (scale 1.12 → 1.0 over 0.3 s, ease out) on the shot starting there; a flash on at most two (one mid-reel, one into the title); the closing title. Other shots get a slow linear push, 1.0 → 1.06.
- At most two speed ramps, one per 4 bars: slow-mo (0.45×) kicking to 4× just before a cut, or 2× landing in 0.4× after one.
- One or two whips, centred on a beat and moving with the action: horizontal for trains, boats and cars, upward for launches.
- Title on the last full bar's downbeat, sub line one beat later, held at least 2 s, then 0.5 s to black. The music fades over the last 1.2 s.

"Machine age" (Modern Tech Pulse from its drop, 0.5 s beats, 12.5 s): locomotive approaching with a push, press cylinder, sparks on the downbeat with a punch, molten pour, a drive wheel ramping 2× → 0.4× and whipping left at 4.0 s into a train under smoke, two 1-beat shots, a flash and punch on the 6.0 s downbeat, a ladle, a train at 0.45× kicking to 4× into the cut at 10.0 s, then a flash onto the title bed and "BUILT TO MOVE".

## Design

- **Grade**: one adjustment layer over all footage, never per shot. Values per look:
  - Archival B&W: desaturate fully; levels black 0.05, white 0.9, gamma 0.95; vignette 0.45 (size 0.45, softness 0.5); mono grain 0.12, size 1.6.
  - Warm tint (mixes colour and B&W sources): vibrance +0.15, saturation −0.1; tint black → `#06111d`, white → `#ffe6c4` at 0.45; levels 0.05 / 0.93 / 0.95; vignette 0.4; grain 0.08, size 1.4.
  - Teal duotone: desaturate; tint black → `#04202b`, white → `#effcff` at full; levels 0.05 / 0.92; vignette 0.35 (size 0.5); grain 0.1, size 1.8.
  - Natural: levels 0.03 / 0.97 and a 0.3 vignette, nothing else.
- **Flash**: a full-frame white fill (`#fff4e6` on a warm grade, or the brand colour) at 0.85 opacity fading out over 0.2 s.
- **Whip**: outgoing and incoming shots overlap 0.3 s centred on the beat; one slides a full frame out as the other slides in, `easeInOutCubic`, both with 360° motion blur.
- **Title bed**: the last shot at 0.35–0.6×, blurred (about 14) and darkened to about 0.42 brightness over 0.4 s from the flash. The darkened bed is the contrast: no outlines or shadows on the type.
- **Title**: one bold display face, centred a little above the middle, entering on scale 1.12 → 1.0 over 0.4 s with a 0.1 s fade, then drifting to 0.97. Sub line in Inter or Space Grotesk 500–600, letter-spaced 0.28–0.32 em, at least 32 px at 1080p, rising 18 px as it fades in over 0.3 s. White or warm off-white. Tested: Archivo 800 at 160 px over Inter 600 at 32 px; Oswald 600 at 220 px in `#fff4e6`; DM Sans 900 at 250 px stacked on two lines (line height 0.9) for 9:16. Budget about 0.68 em per capital for Archivo and DM Sans and 0.5 em for Oswald, so a line doesn't wrap by surprise.
- **Easing**: `easeOutCubic` for arrivals, `easeInOutCubic` for whips, linear pushes. No bounce or spring.

## Build in Tella Motion

Make the document at the delivery size, as long as the reel. For its own video, add it as a motion clip; to open an existing video, add it and reorder it to 0. Build everything in one batch, then tweak in small ones. Stack order: shots, the grade, flashes, titles, the fade to black. Give nodes readable ids (`s01`…, `grade`, `flash1`, `title`, `sub`) so the reel stays easy to retime.

Speed ramps are time-remap keys, all `linear`: eased keys stall the footage at each key, so build a smooth ramp from short linear steps (about 0.05 s). Keep the last key inside the clip's duration.

For 9:16, don't rely on `cover`, which crops the centre and often drops the subject: scale the media to fill the height and slide it so the subject is centred without exposing an edge. Keep the title between 10% and 80% of the frame height.

## Gotchas (all hit while building the examples)

- `addMedia` defaults to `fit: "contain"`, leaving bars: patch `fit: "cover"`.
- `addMedia` caps a node at the clip's own length even when slowed, so the shot goes black early. `trim` its end after the batch.
- `volume` is in dB, so `volume 0` is full volume. Mute footage by patching its whole `audio` object (`assetId: "media.<sourceId>"`, `mute: true`).
- Time remap refuses audio nodes. Set a music node's in-point by patching its `sourceIn`.
- Keyframing `blur` or a blur effect's radius fails ("keyed list: write its members by id"). Set blur static and let the flash hide the switch; animate brightness, scale, opacity and position instead.
- A deleted and re-added node goes to the top of the paint order, above the grade and titles. Move it back with `node.move`.
- Cuts land on the next 30 fps frame, up to 33 ms late. That's fine; don't nudge.
- Archive footage is 240–480 px tall. Grain and a vignette make the upscale read as film. Don't sharpen.

## Check

- **Cuts**: filmstrips of the document around each cut: within one frame of its beat, no black frame where a shot ran out, no bars, no half-built title. A whip shouldn't read as a cut.
- **Moves**: check whips and flashes in a 30 fps filmstrip, not single `get_motion_frame` renders, which once misreported a fast move.
- **Frames**: one mid-shot frame per shot for framing; full-size frames of the title and the last frame (black).
- **Audio**: music inside the document is in the motion preview; background music is only in the video preview. Hits line up with cuts, the level sits around −12 to −20 dBFS, no source audio leaks.
- **Video**: the clip length equals the reel's end.

Report the video link, length, track and BPM, the shot list with times, what to listen for, and anything guessed.

## Making it your own

- **30 s**: a middle section of 2-beat shots before a final 4-bar run of 1-beat cuts.
- **A spoken line**: land the title on its word from the transcript, keep cuts on beats, and duck the music about 8 dB under the words.
- **Brand colour**: for the flash and the sub line, not the grade.
