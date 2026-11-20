---
name: cinematic-website-fly-through
description: >-
  Make a cinematic trailer from a website in Tella Motion. The site lies tilted
  in 3D on a plane under a tilt-shift lens with grain, glow and a glass sheen;
  the camera drifts, whips in, glides and blasts back out, cutting each time to
  one big word on a flat-colour card, and ends on the brand's logo. About 12 s,
  silent: music can be added to the video afterwards. The set can be a full-page
  screenshot, an Auto Capture take, or a screen recording made in Tella: a
  recording plays under the camera with no zooms added and a large animated
  cursor drawn for the user's OS (macOS or Windows). Looks: Light, Dark, or
  Brand matched (colours and font taken from the site). Use when asked for a
  website fly-through or flythrough, a cinematic trailer or teaser of a site,
  product or landing page, a 3D camera flight over a homepage or a screen
  recording, a tilt-shift look on a web page, or a brand-matched launch trailer
  from a website or an Auto Capture take.
metadata:
  title: Cinematic website fly-through
  author: Tella
  category: UI & apps
  image: og.jpg
  poster: gallery/tella-launch.webp
  preview: gallery/tella-launch.mp4
  prompt: Make a 12-second cinematic fly-through of northwindnotes.com that cuts to "Capture", "Organize" and "Share" and ends on the site's logo.
---
# Cinematic website fly-through

A trailer where the website is the set. The site lies on a plane, tilted away in 3D with a soft shadow under it, filmed through a tilt-shift lens so only a band across the middle is sharp. The camera drifts in, dives, and cuts to a full-frame card with one big word; glides on, cuts to the next word; skims low, then pulls back hard into a zoom-blurred last word and the brand's logo. 10–15 s, as its own video or the first clip of one.

The set can also be a **screen recording** that plays while the camera flies over it (an Auto Capture take, or a recording made in Tella) with a large animated cursor drawn for the user's OS, and the scene can be **brand matched** to the site instead of white or black.

Builds on `tella-motion-design` (load it first) and `tella-camera-moves`. One script builds every variant: `scripts/build_flythrough.py`. Helpers (each has `--help`; the Node ones need `playwright` and stop on their own timeout): `site_brand.js` (the site's colours and fonts), `site_logo.js` (its SVG logo as a PNG), `capture_page.js` (the screenshot), `brand_look.py` (the Brand matched look), `preview_frames.py` (the check frames).

Reference video: `gallery/tella-launch.mp4` is a full-page screenshot in the Light look. Pull frames from it with ffmpeg when you need to see a move.

## Ask once

Work these out yourself and never ask: whether this video is empty (`tella__list_clips` on it: no clips means build here), the site's headings, name and domain, whether its page is light or dark, the brand's logo for the end card (below), which OS the cursor is for (below), and anything attached (a screenshot, a recording, a take). Then ask in one `ask_form`, every field prefilled, so the user can just submit:

| Field | Prefill | Limits |
|---|---|---|
| **Set** | pick: Full-page screenshot, Auto Capture take, A Tella screen recording. Default: whatever the message carries (an attached or named recording or take, a screenshot); with only a URL, Full-page screenshot | |
| **Website URL** | from the message, the recording, or the workspace's site | one URL |
| **Words to feature** | 3 one- or two-word picks from the site's headlines, or from what the recording shows on screen, comma-separated | 3 at 12 s, one more per extra 3 s, at most 5; each up to 12 characters |
| **Ending** | pick: Brand logo on a card (default), Name on a card, Hold on the last shot | |
| **Length** | slider 8–20 s, default 12 | |
| **Look** | pick: Light (white plane and cards, ink `#111111`), Dark (`#0E0E10`, white words), Brand matched (the site's own colours and font). Default: Light or Dark by the site's background; Brand matched when the user asked for the brand | |
| **Where** | Not asked when this video is empty: build in it. When it already has content: pick A new video (default), First clip of this video | |

If the user skips the form, build with the prefilled values. **No music:** the skill never adds or changes music, and the trailer is silent (the recording's own sound is always muted). When you report, say the user can add music to the video afterwards. Use the site's own words only: never invent a claim. If Set is a Tella recording and it isn't clear which one, ask once which video or clip (a form pick with a frame of each).

## The set

### Full-page screenshot
One tall screenshot of the whole page, 1280 px wide at 2× (2560 px wide), at most 6000 IMAGE pixels tall, cookie banner gone. Look in the attachments and the video's media library first; if there is none, ask with `ask_question` ("Attach a full-page screenshot of the homepage, cookie banner closed", answers "I'll attach one" and "Capture it for me"). To capture it, run `node scripts/capture_page.js <url> --out page.png` (needs `playwright`; prints `imageWidth`, `imageHeight`, `container`, `cropped`). It:
- scrolls to the bottom in steps and back to the top before capturing, so lazy-loaded sections are in;
- when the page scrolls inside a container (e.g. `.app-scroll-viewport`: the document is one screen tall but an element has the content) finds it, or takes `--container '<css>'`, and sets the viewport height to that container's `scrollHeight`;
- clicks accept buttons in cookie banners, then hides what stays up in the DOM (`display: none`), also after the scroll;
- always captures at 2× and crops to the top 6000 image px (`--max-image-px`), never dropping to 1×. "About 6000 px" means image pixels.

Then `view_image` a downscaled copy (`convert page.png -resize 640x small.png`) for banners, modals and blank sections, and fix what you see. Upload with `tella__create_source` (`kind: "image"`, `width`, `height` = the script's `imageWidth`/`imageHeight`; the tool has no filename or contentType argument), then `curl -sf -T page.png "<uploadUrl>"` with the `uploadUrl` exactly as returned: copying its `x-amz-*` query values into headers gives a 403. Spec: `page: {sourceId, width, height, targets}`. `targets` (one y for the hero, then `[from, to]` per later shot) are **y values in the screenshot's own pixels** (what you read off the image; `targetsIn: "image"`, the default; the script scales them onto the 1920-wide page itself, so a 1280-wide screenshot needs no ×1.5 by hand). `"targetsIn": "page"` takes y on the 1920-wide page instead. Aim each shot at a section worth seeing (below).

### Auto Capture take
- A take the user already has (attached, or a clip): use it. Otherwise `create_auto_capture` with the URL and the user's own words plus what it is for. Keep the take short: **about 20–25 s**. Write the brief so the take acts, not just scrolls: "footage for a 12 s trailer, 20–25 s in all: three moments worth seeing. In each, move the cursor to a key section (the hero heading, a feature block, the product UI), hover it for a second, and click something real in it (a tab, a card, a button that opens something). Don't just scroll. No logins, no forms submitted, no waiting on slow loads." Follow the Auto Capture rules (logins, `wait_for_jobs`, read `handoff`, look at it with `get_filmstrip`).
- **No zooms.** The take plays inside the Tella Motion document from its `sourceId`; it is never left as a clip of its own and nothing zooms into the recording. The only camera is the fly-through.
- Cursor data comes from a clip: `upload_clip` the take onto the trailer's video, `get_mouse_events` (whole clip, `intervalMs: 100`), save the result to a file, then `delete_clip` (the recording stays; the clip arrives with an automatic tracking zoom, which goes with it). With no cuts on that clip its times are the source's, so `clipCuts` is `[]`.
- Pass the take's length as `recording.durationMs` (`list_sources` gives `durationMs`). The script ends each shot's recording with the take and **warns when a shot is still on screen after the take ends** (the picture would stop): move that shot's `startMs` earlier by what the note says. The last shot plays longest (about 2.5–3 s on screen at 12 s), so start it at least 3 s before the take ends.
- Pick the shots from `result.chapters` (source ms) and pass `result.suggestedCuts` as `avoid`, so the script warns when a shot sits on a wait.
- A take with no clicks, or a cursor that barely moves (`get_mouse_events` returns fewer than 8 samples, or the cursor travels less than 8 % of the screen width in all): the script draws **no cursor** (a large still arrow looks wrong) and prints a note per shot without clicks. Aim those shots at a page section (a heading or feature block you can see in the take's frames) with `focus: [x%, y%]`, not at the cursor.

### A Tella screen recording
- The clip can be in this video or any video the user can edit. `list_sources` gives the `Screen` source (`id`, `dimensions`, `recordedWith`); `durationMs` goes in `recording.durationMs`; `get_timeline` with `include: ['cuts']` gives the clip's cuts, passed as `clipCuts`; `get_mouse_events` on that clip gives the cursor in playback time. The script maps playback time to source time through the cuts and warns when a shot would play through one.
- Only the screen is used: no camera, no layout, and none of the clip's zooms. Its sound is muted. Never change the clip it comes from.
- A recording made in the browser or uploaded has its own cursor in the picture and no mouse data: the script then draws none. Say so.

### Shots from a recording
One shot per word, each `{startMs, speed?, focus?}`: `startMs` is the clip playback time on screen when the shot opens. Shot 1 shows about the first cut's time of recording (2.2 s); each later shot the gap between cuts minus 0.8 s. Choose moments where something happens (a click, a result arriving), in order, and end on the payoff. `speed` (1–3) fits a longer action into a shot. The camera aims at the clicks in the shot, or the cursor; `focus: [x%, y%]` overrides it (use it for a result that appears away from the cursor). Take the words from what those moments show.

**Aim at contrast.** Put each shot on a high-contrast part of the page: a heading, product UI, a colour block, a logo wall. On an all-dark or very pale page avoid the empty-looking stretches (large margins, a blank hero background, a gradient with nothing in it): pick the section with text and UI in it, and with `focus` or `targets` keep the sharp band on it. Check by looking at the mid-shot frame: if the sharp band shows mostly flat colour, move the target.

**The recording is drawn larger than the frame** (`recording.scale`, default 1.3, centred) so that the screen's edge, and the plane behind it, never shows at any camera position. A glide's start and the 3D turn expose edges otherwise (it showed at about 7.6 s). Raise it (1.5) when the edge check below finds one; the cursor and the aim points follow the scale.

## The cursor

Drawn in Tella Motion over the recording, because a take's or an app recording's picture has no cursor in it: a vector arrow about 83 px tall on the 1920-wide page at the default `size` 72 (large: about 9 % of the frame height once the camera is in), a soft shadow, motion blur, eased moves between samples, a squash to 0.8 on each click with an overshoot back, and a click ripple in the look's accent colour.

**Which OS** (`cursor.os`): `mac` is the macOS 27 Golden Gate arrow, the same artwork Tella's own cursor uses for Mac recordings (black with a white outline, its tail drawn as its own piece, Golden Gate's 45 % shadow); `windows` the white arrow with a black edge and sharp joins. Take it, in order, from: the recording's own `recordedWith` (`list_sources`: `mac` or `windows`); for a take or a web recording, the `recordedWith` of the user's most recent app recording (`list_videos`, then `list_sources` on a recent screen clip or two); the video's `settings.cursor.style` when it is `windows`; otherwise `mac`. Say which one you used. `cursor.size` takes 56–96.

## Brand matched look

The plane, the cards, the word colours, the shadow and the click ripple come from the site:

1. `node scripts/site_brand.js <url>` reads the page's CSS: background, text colour, the primary colour (its buttons and links), heading font and weight. If the site is the workspace's own, `get_brand_kit` wins where it has a colour or a font.
   `site_brand.js` prints 6-digit hex for every colour (oklch, oklab, lab and `color()` values are converted) and stops after 25 s (`--timeout`).
2. `python3 scripts/brand_look.py <frames> --primary '#RRGGBB' --bg '#RRGGBB' > look.json`, then put its `look` object in the spec (`--help` lists the options). Without `--primary` it picks the strongest saturated colour in the frames; check `found` against what you see. **Which frames:** for a screenshot, the one `page.png` (the script shrinks it). For a recording or an Auto Capture take, 2–3 frames of the source itself at about 25 %, 50 % and 75 % of the take (`get_source_thumbnail` with the `sourceId`, as PNG, or `ffmpeg -ss … -i take.mp4 -frames:v 1 f.png`), taken where the product's own UI fills the screen. Never a frame of a card, the end card or a motion-document frame with the lens on, and not a blank page or a loading screen. Pass `--primary` from `site_brand.js` (`primary[0]`) and `--bg` from its `background` when they look right.
3. It gives: a plane and end card in the page's background tinted 10 % with the brand colour; card 1 in the brand colour with white or dark words (whichever contrasts); card 2 in the tint with **brand-coloured words when they reach 3:1 contrast on the tint, otherwise `#111111` or white** (so card 2's words are often brand-coloured, and `#111111` on a pale or low-contrast brand colour); the last card in a deep shade of the brand colour (a pale tint of it on a dark site); a shadow in a dark shade of it; glow 0.2. More than three words cycle through the three cards.
4. Font: the site's heading font when `list_motion_fonts` has it (catalog slug, or a library font's id); otherwise the closest catalog family (a geometric sans → `inter` or `dm-sans`, a grotesque → `space-grotesk`, a serif → `playfair-display` or `lora`), at the site's heading weight. Say when it is a stand-in.

Check contrast on a frame of each card: if a word is hard to read, swap that card's `inks` entry for `#FFFFFF` or `#111111`.

## The cards and the ending

- **Cards are flat colour.** No shimmer or sheen crosses a word card: just the card, the word and its motion blur. Only the page keeps its glass sheen. (`cardSheen: true` in the spec puts the moving sheen back on the cards, if the user asks for it.)
- **The end card is the brand's logo**, not the website address. Find it in this order, and stop at the first that works:
  1. An attached logo; or, when the site is the workspace's own, `get_brand_kit` (`darkModeLogo` on a dark end card).
  2. **(a) The site's own SVG logo or wordmark**, from its header or its favicon links: `node scripts/site_logo.js <url> --out logo.png` renders it to a transparent PNG 1500 px wide (`--min-width` for more). It prints `kind` (wordmark or symbol), `meanColor` and `meanLuminance`. If the logo's luminance is close to the end card's (a white logo on a light card), re-run with `--fill '#111111'` (or `#FFFFFF`) for a single-colour logo. Exit code 3 means the page has no SVG logo.
  3. **(b) A Brandfetch wordmark** (the Logo Link CDN, `https://cdn.brandfetch.io/<domain>/theme/<dark|light>/type/logo?c=<client id>`; it needs a client id and must come back as an image: an HTML page or a 403 means no access, go to (c)). **The theme names are about the background, not the logo:** `theme/dark` is the dark-coloured logo, for LIGHT backgrounds; `theme/light` is the light-coloured logo, for DARK backgrounds. Take the one that contrasts with the end card's colour (`look.endBg`): `theme/dark` on a light card, `theme/light` on a dark one.
  4. **(c) `list_library`** (`scope: default`, `type: logo`, `query` = the domain) and `add_library_item` with its `presetId`. It returns only a square symbol or a 128 px icon, so use it last; the script says when it has to blow it up.
- **Minimum size on screen** (the script enforces it): a wordmark (wider than 2:1) at least 50 % of the frame width (960 px of 1920), a symbol at least 35 % of the frame height (378 px of 1080). A logo whose source is under 1/1.3 of that is shown soft: the script prints a note; go up the list above instead.
- Tella Motion refuses a company logo's own `sourceId` (its image lives on another host): download the item's `url` (or use your PNG), `tella__create_source` (`kind: "image"`, `width`, `height`), `curl -sf -T logo.png "<uploadUrl>"`, wait for the source (`wait_for_jobs`, `source`), and pass `logo: {sourceId, width, height}`. Contrast: check the logo against the end card in the frame check; swap the pick (`theme/dark` ↔ `theme/light`, or `--fill`) if it fades.
- The logo slides in from the right as the last word leaves, takes a little bump to the left, and **comes to rest in the exact middle of the frame**. The card's slow 3D turn settles with it: it eases out to flat and centred by the last frame, so the trailer ends on the logo square-on in the middle. Nothing on the end card drifts past its resting place. The script builds it this way (the Name ending rests centred the same way); if you retime or restyle the ending by hand, keep the logo's last `x` key at 0 and the card's last rotateY, rotateX and `x` keys at 0.
- No logo to be found: fall back to Name on a card (`ending: "name"`, `end: ["northwind", "notes.com"]`, the domain split in two) and say so. Name is also what the user gets when they pick it.

## Timing

- `cuts`: one time per word, the moment its card **covers the frame**. The word keeps settling for about 0.3 s after the cut (the card's rise and a slight scale-down run on): that is intended, don't "fix" it by moving the cut. The first cut needs 1.8 s before it, the others 2.4 s between them. The 12 s cuts are 2.23, 5.5, 9.2; four words at 15 s: 2.2, 5.4, 8.6, 11.9.
- The end card starts at `endAt` (default last cut + 1.0 s) and needs 1.8 s after it. `endAt` must be 0.5–1.3 s after the last cut.
- For other lengths, change the cuts, never the cards: each card covers about 1 s and the next shot starts under its exit.

## Build

1. Where the clip goes. **This video is empty** (`tella__list_clips` returns no clips): `tella__create_clip` `{videoId: storyId, type: "motion", name, duration}` on it, and rename the video after the site (`tella__update_video`). Make a new video only when this one already has content: `tella__create_video` (empty, `name` = the site), then `tella__create_clip` `{videoId, type: "motion", name, duration}`; or, when the user picks First clip of this video, `create_clip` on it and `tella__reorder_clip` to order 0. Always a clip, never an overlay.
2. **Start from a ready-made composition** in `compositions/`: the finished command batch for each set and look, with the spec that built it (`about`, `placeholders`, `spec`, `commands`): `screenshot-light`, `screenshot-dark`, `screenshot-brand`, `recording-mac-brand`, `recording-windows-light`. Don't write commands by hand.
   - **Use it as is** when the build matches: Light or Dark, a full-page screenshot exactly 2560×6000 (what `capture_page.js` gives a long page) whose sections suit its targets (450, then 1500–2700 and 3300–4800 in image px), 12 s, three words, the logo ending with a wordmark about 1500×375. Fill the placeholders and apply:
     ```
     python3 -c "import json,sys; f=json.load(open(sys.argv[1])); s=json.dumps(f['commands']); r=json.loads(sys.argv[2]); [s:=s.replace(k, json.dumps(v)[1:-1]) for k,v in r.items()]; open('/workspace/fly_cmds.json','w').write(s)" <skill>/compositions/screenshot-dark.json '{"{{WORD1}}":"Purpose","{{WORD2}}":"Agents","{{WORD3}}":"Speed","{{PAGE_SOURCE_ID}}":"su_...","{{LOGO_SOURCE_ID}}":"su_...","{{NAME}}":"Linear"}'
     ```
   - **Otherwise copy its `spec`, change what differs, and build with the script** (other targets, page size, length, word count, ending or logo shape, your brand's `look`, a real take's `mouseEvents`, `durationMs` and `shots`). The Brand matched and recording compositions always go this way: their colours are an example brand's and their cursor follows a sample take. They show what a correct build of that variant looks like.

   Build with the script (the header lists every field):
   ```
   pip install --break-system-packages -q pillow
   python3 <skill>/scripts/build_flythrough.py spec.json --out /workspace/fly_cmds.json
   ```
   It prints the command count, the camera targets and `notes`. Fix what the notes say (a shot on a cut or a wait, or past the end of the take: move its `startMs` or change its `speed`) and build again.
3. `tella__apply_motion_editor_commands` (`documentId`, `commandsFile`, `baseRevision`) on the clip's empty document with `commandsFile` and `baseRevision`. To rebuild after a change, remove the document's top-level nodes (`node.remove` each, from `get_motion_document`) in the same batch, ahead of the new commands.

What the script builds (`references/camera-path.md` has the keys, `references/lens.md` the lens): `bg`; `drift` holding `stage` (plane, shadow, 160 px behind) and `page` (the screenshot, or `screen` with one muted media node per shot, then the glass sheen, then the `cursor` group); per word `cardN.bg` and `cardN` with its title; `zoomblur` before the last card; `end.bg` and `endcard` (the logo); the hidden `tsdepth` and the `tiltshift` adjustment on top. Titles are live text and every node is named, so the user can edit it all.

## Check

Every check in the first block is **required** before you report done.

1. **Preview and cut frames (required).** `tella__get_motion_preview` (`documentId`, `startTimeMs: 0`, `durationMs` = the length, at most 30000, `fps: 30`, `width: 960`); when it says `rendering`, call it again with the same arguments. Download the MP4 from its URL (`curl -sf -o preview.mp4 "<url>"`), then `python3 scripts/preview_frames.py spec.json preview.mp4 --out /workspace/check` (ffmpeg; `--offset` if the preview didn't start at 0). It writes a frame at the middle and end of every shot, at each cut −0.3, 0 and +0.3, at the end card, +0.5 and the last frame, plus `check/sheet.png`, labelled. `view_image` the sheet (and single frames where something looks off). Confirm: the card covers the frame on each cut, the logo is on screen at least 1.8 s, and the file has no sound of its own. The script's `logo` result measures the last frame: fix any `warning` it gives (off centre by more than 10 px, small, or missing). Or by hand: `ffmpeg -ss <t> -i preview.mp4 -frames:v 1 f.png`.
2. **No plane edge (required).** In the middle frame and the end frame of **each shot** (the sheet's "shot N middle" and "shot N end"), confirm no edge of the page or screen and none of the plane's border is visible: only the far horizon of the tilted plane may show. An edge means: raise `recording.scale` (1.3 → 1.5) or move the shot's `focus`/`targets` toward the middle of the page, rebuild and check again.
3. **`tella__get_filmstrip`** (`documentId`, `timesMs`, `tileWidth`) at each cut ±0.3 s and mid-shot (at 12 s: 0, 0.7, 1.5, 2.1, 2.5, 3.3, 4.2, 5.0, 5.4, 5.8, 6.5, 7.6, 9.0, 9.4, 10.6, 11.8): the sharp band falls on what the shot is about (and on contrast, not flat colour), each shot opens on the moment you chose.
4. Recording: step through a click at 100 ms (`intervalMs: 100`, `tileWidth: 480`): the cursor tip is on what it clicks, the ripple fires on the click, and there is one cursor, not two. A second cursor means the recording has one in its picture: set `cursor.os` to `none`.
5. `tella__get_motion_frame` (`documentId`, **`startTimeMs`** (not `timeMs`), `width`, `format`): one at width 1280 mid-shot and one of each card: words crisp and readable against their card, no sheen on them, the cursor crisp. One at width 1920 of the end card: the logo is sharp, whole and readable against it, and at least the minimum size above. The logo's position and size come from `preview_frames.py` (check 1), measured from its pixels, not judged by eye.

## Gotchas

- `get_mouse_events` needs a clip; a bare source has none. That is the only reason a take is ever placed as a clip, and it is deleted again.
- `upload_clip` of a take adds a tracking zoom by itself. Never leave that clip in the video when the user asked for the fly-through.
- A media node plays the raw source: clip cuts, zooms, layouts and Tella's own animated cursor do not come along. That is why cuts are mapped and the cursor is drawn.
- The lens blur leaves see-through edges unless the alpha `colorMatrix` follows it in the adjustment (the template has it).
- `get_video_preview` is cached on the video's `updatedAt`, which Tella Motion edits don't move: check with `get_motion_preview`, or touch the video before rendering again.
- Don't put `motionBlur` on `drift`, `page` or `stage`; the speed blur is a keyed vertical blur on both groups.
- `get_motion_frame` takes `startTimeMs`; `timeMs` is ignored and gives frame 0.
- Upload bytes with `curl -sf -T <file> "<uploadUrl>"`, the URL exactly as returned and no extra headers.
- Dark pages: glow 0.2 so white text doesn't bloom. Hold on the last shot puts a 78 % scrim in the plane colour under the name so it reads.
