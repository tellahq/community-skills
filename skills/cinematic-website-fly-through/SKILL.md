---
name: cinematic-website-fly-through
description: >-
  Make a cinematic trailer from a website in Tella Motion. One full-page
  screenshot of the site lies tilted in 3D on a clean backdrop, seen through a
  tilt-shift lens (a sharp band across the middle, blurred top and bottom) with
  grain, a soft glow and a glass sheen. The camera drifts over the hero, whips
  in, glides down the sections, skims low across a heading and blasts back
  out, cutting each time to one big word from the site's own headlines on a
  clean card. It ends on the site's name. About 12 seconds, on the beat of a
  curated track, as a new video or the first clip of one. Use when asked for
  a website fly-through or flythrough, a cinematic trailer or teaser of a site
  or landing page, a 3D camera flight over a homepage, a tilt-shift or
  depth-of-field look on a web page, a launch trailer made from a website, or
  to make my homepage look like a movie trailer.
metadata:
  title: Cinematic website fly-through
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/tella-launch.webp
  preview: gallery/tella-launch.mp4
  tags: website, landing page, trailer, 3D, camera move, tilt-shift, depth of field, kinetic type, launch, teaser
  prompt: Make a 12-second cinematic fly-through of northwindnotes.com that cuts to "Capture", "Organize" and "Share" and ends on the site's name.
---

# Cinematic website fly-through

A trailer where the website is the set. The whole page is one tall screenshot lying on a white plane, tilted away in 3D with a soft shadow under it, and filmed through a tilt-shift lens so only a band across the middle is sharp. The camera drifts over the hero, dives in, and cuts to a white card with one big word. It glides down the page, cuts to the next word, skims low across a heading, then pulls back hard into a zoom-blurred third word and the site's name. It is 10–15 s and works as its own video, a launch teaser, or the first clip of a product video.

Builds on `tella-motion-design` (load it first) and `tella-camera-moves`. For many screenshots on a wall use `screenshot-wall`; for depth layers cut from one screen use `tella-ui-parallax`.

## Ask once

Work these out yourself and never ask: the site's headings and its name or domain (from the URL, the message or the video), its background colour (light or dark), whether music is already set on the video, and a full-page screenshot if one is attached. Then ask in one `ask_form`, every field prefilled, so the user can just press submit:

| Field | Required | Prefill | Limits |
|---|---|---|---|
| **Website URL** | yes | from the message, the transcript, or the workspace's site | one URL |
| **Words to feature** | yes | 3 one- or two-word picks from the site's headlines, comma-separated (the example: `All-in-one, Agentic, Video`) | 3 at 12 s, one more per extra 3 s, at most 5; each up to 12 characters |
| **End card** | yes | the domain split in two (`northwind` + `notes.com`); the user can type the name instead | up to 20 characters |
| **Ending** | yes | pick: Name on a white card (default), Logo on a white card, Hold on the last page | |
| **Music** | yes | pick up to 12 curated tracks with a clear beat (`list_library` scope `default`, type `music`; `get_music_beats` confidence above 0.3), plus None. Default: the clearest beat near 100–120 bpm, or the video's current track | |
| **Length** | yes | slider 8–20 s, default 12 | |
| **Look** | yes | pick: Light (white plane and cards, ink `#111111`), Dark (`#0E0E10` plane and cards, white words). Default: the site's own background | |
| **Where** | yes | pick: A new video (default), First clip of this video | |

If the user skips the form, build with the prefilled values. Use the site's own words only: never invent a claim.

**The page.** It needs one tall screenshot of the whole page, 1280–1440 px wide and captured at 2× (the example is 2560 × 5867), with the cookie banner closed. Look first in the message's attachments and the video's media library. If there is none, ask with `ask_question`: "Attach a full-page screenshot of the homepage (in Chrome: DevTools → ⌘⇧P → Capture full size screenshot), with any cookie banner closed", suggested answers "I'll attach one" and "Capture it for me". The fallback: `import_from_url` (`video: false`) of the URL plus 2–3 inner pages, each a 1920 × 1080 capture above the fold, stacked into one tall page (each next capture moved down so its content follows on, its repeated nav bar hidden with a rect mask from y 70). The flight then has less page to cover, so keep it to 12 s.

**The logo** (Ending: Logo): from the attachments or the media library; if missing, ask once for a transparent PNG or SVG, and fall back to the name.

## Timing

- Lay the clip out as: hero shot ~2.2 s, card 1, glide shot ~2.4 s, card 2, skim shot ~2.7 s, card 3, end card ≥ 1.8 s. Each card covers about 1 s, and the next shot starts under its exit. For other lengths, stretch or shorten the shots, never the cards.
- With music: put each cut (the moment the card is fully up and the camera holds) on a beat from `get_music_beats` (see step 8 for which id), the third cut on a downbeat, and the end card on a downbeat. Background music fades in over 2 s, so the first cut is at least 2.2 s in.
- Without music the example's cuts are at 2.23, 5.5 and 9.2 s and the end card at 10.2 s.

## The look

- **Canvas** 1920 × 1080, 30 fps. Background, plane and cards are white `#FFFFFF`; words `#111111` (Dark: `#0E0E10` and white).
- **Page.** The screenshot fills 1920 px wide (a 2560 px capture: `addMedia` sized 3840 wide at scale 0.5, top-left at 0, 0, so it stays sharp when the camera pushes in to 1.9×). A screen-blended diagonal glass sheen sweeps across it over the whole clip.
- **Stage.** A white plane far larger than the page (8320 × 12600 from −3200, −3200) and the page's shadow: a rounded rect 1960 wide and as tall as the page, from y 110, radius 40, `#1A1450` at 0.6, blurred 140 px (Dark: black at 0.7). It sits 160 px behind the page (`translateZ` −160).
- **Lens.** A tilt-shift adjustment over everything: lens blur radius 16 driven by a vertical gradient depth map (sharp band 44–56 % of the height), glow, chromatic fringe 2, levels 0.01–0.99, vignette 0.08, mono grain 0.025. Values and shaders in [references/lens.md](references/lens.md).
- **Cards.** Full-frame white, one word centred at 250 px, weight 500, letter-spacing −5 (−0.02 em), line height 1.2. The brand's own font if the workspace has it uploaded (the example uses Tella's), otherwise Inter 500. End card 220 px, letter-spacing −4.4. Every word has motion blur (shutter half a frame, 16 samples) and a sheen band crosses each card.

## Building it

1. `create_motion_document` 1920 × 1080, `canvas.set` duration; `addShape` the white background.
2. `group` → `drift` (origin 960, 540), holding two sibling groups with the same camera keys: `stage` (plane + shadow, `translateZ` −160 via `node.patch` on `common.transform`) and `page` (the screenshot + sheen). They are siblings because a child's own 3D doesn't nest inside a tilted group. Key `drift`'s slow linear drift.
3. Key the camera on `stage` and `page` from the rows in [references/camera-path.md](references/camera-path.md): one `setKeyframes` per property (`anchorX`, `anchorY`, `x`, `y`, `scaleX`, `scaleY`, `rotateX`, `rotation`, `rotateY`) in one batch. Refit `anchorY` to your page: the hero, mid-page, then a strong heading near the bottom. When the timing changes, rebuild from the rows rather than patching keys.
4. Add the speed blur on both groups (a `blur` effect with an `effectId`, keyed by `node.patch` on `common.effects.<id>.effect.radiusY`).
5. Cards in paint order above the page: each `cardN.bg`, its word group, and its sheen; the zoom-blur adjustment just before card 3; the end card. Animations per card are in the reference: rise and swing off, rise and drop away, blast in, slide in.
6. The tilt-shift adjustment last (topmost), with the hidden depth map node.
7. Place it as a clip, never as an overlay (an overlay belongs to one clip and can't span the clips of an opening). A new video: `create_motion_document` without a videoId, then `create_clip` `{type: "motion", documentId}` without a videoId. First clip of this video: `create_clip` with the videoId, then `reorder_clip` to order 0.
8. The sound in the result comes only from the chosen track; the example is silent. **A new video:** `set_background_music` with the track's `presetId`, volume about 0.4, and time the cuts from `get_music_beats` with that `videoId`. **First clip of this video:** background music would loop under the speaker, and `add_sound_effect` refuses a music `presetId`, so upload the track as a source: take its `url` from `list_library` (scope `default`, type `music`), download it, `create_source` `kind: "audio"` with its duration in seconds, PUT the bytes to the `uploadUrl`, then `add_sound_effect` on the trailer clip with that `sourceId` (startTimeMs 0, durationMs the clip's length, volume about 0.4). Curated tracks can open with seconds of silence: measure it (ffmpeg `silencedetect`) and cut it off (`ffmpeg -ss`) before uploading. Beats come from `get_music_beats` with the `sourceId`, in source time, which is then the clip's time. The first preview after the upload can be silent while the source processes; check again a minute later. If the video already has background music, ask before replacing it. Music: None leaves the clip silent.

For Ending: Logo, put the logo on the end card at about 520 px wide with the name's slide-in; for Hold on the last page, drop the end card's bg and fade the page to the drift's last key with the name over it.

## Check

- `get_filmstrip` of the document at 1.0, 2.1, 2.5, 4.0, 5.4, 5.8, 7.5, 9.0, 9.4 and 11 s (or your cut times ±0.1 s): the sharp band falls on readable content, no page edge or seam shows except the far horizon, no cookie banner or other company's logo is in frame.
- One `get_motion_frame` at width 1920 (`startTimeMs`, not `timeMs`) of each card and of a mid-glide frame: the words are crisp in the middle band and the page text isn't mush at 1.9×.
- `get_video_preview` at 1920, 30 fps, then frames from the MP4: each card cut lands on a beat, and the end card is on screen at least 1.8 s.

## Gotchas

- The lens blur leaves see-through edges unless a `colorMatrix` setting alpha to 1 follows it in the adjustment.
- `setProperty cornerRadius` on the page group adds a 1920 × 1080 clip that cuts off the page below the first screen. Don't round it; `node.patch` `{common: {clip: null}}` undoes it.
- `translateZ` isn't listed until it has been set once with `node.patch`.
- Keying brightness on a group inserts a colour matrix at effect index 0; read effect paths from `inspect_motion_node_properties`.
- `get_video_preview` is cached on the video's `updatedAt`, and Tella Motion edits don't move it: touch the video (an unchanged `update_clip` or music volume) before rendering again.
- A brand-new document refuses raw built-in shader inserts until one `addEffect` of that kind has run.

## Variations

- Four or five words for 15–20 s: repeat the glide and its rise-and-drop card.
- Dark sites: Dark look, and lower the glow to 0.2 so the white text doesn't bloom.
