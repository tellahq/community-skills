---
name: stop-motion-intro
description: >-
  Make a hand-animated stop-motion opener in Tella Motion at 12 fps: a
  top-down cutting-mat surface whose grid lines draw on one per frame, then
  cut-out photos of the user's products or objects slide in, hop between
  arrangements, lift and flip like pieces moved by hand between frames (held
  poses that boil a pixel or two, small rotations, shadows that grow when an
  object is picked up), then a fade to black and the brand's logo and
  wordmark as the end card. Its own clip at the start of the video. Use when
  asked for a stop-motion intro, a stop motion opener, a hand-animated or
  claymation-style product intro, objects moving on a cutting mat or desk,
  a flat-lay product animation, a frame-by-frame logo reveal, or a crafty
  tactile intro for a product, shop or show.
metadata:
  title: Stop motion intro
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/cassette-tapes.webp
  preview: gallery/cassette-tapes.mp4
  tags: stop motion, intro, opener, product, flat lay, cutting mat, 12 fps, logo reveal, end card, handmade
  prompt: Make a stop-motion intro with my two notebooks hopping around on a green cutting mat, ending on the Northwind Notes logo.
---

# Stop motion intro

A 13.5 s opener that looks shot frame by frame on a craft table: a cutting mat seen from straight above, its grid drawing itself on, then the user's objects (two cassette tapes in the example) sliding in, swapping places, flipping over and swapping back, and a cut to black with the logo. Everything moves on twos at 12 fps and nothing is ever perfectly still, which is the whole look. It is its own Tella Motion clip, put first in the video. Builds on `tella-motion-design`; `tella-title-cards` covers the end card's type rules.

## Ask once

Work out yourself and never ask: the brand or show name (from the video's title, the message, the workspace's brand), the logo (attachments on the message, then the media library: use it as the end card's mark; without one, draw a simple shape of the product, as the example's cassette, or set the name alone if the objects don't draw simply), the objects' colours (to pick a mat they stand out on), and whether the video already has music.

If photos of the objects are attached to the message, use them and leave out the two object fields below. Otherwise the user chooses between their own photos and generated ones in the form, before anything is built.

One `ask_form`, every field prefilled so the user can just submit:
- **Objects** (pick, required): "I'll upload my own photos" or "Generate them for me". Prefill Upload when the message mentions their product photos or the media library holds product photos; otherwise Generate.
- **What to generate** (text, up to 60 characters): the objects in a few words, prefilled from the video's topic or the brand's product, e.g. "two spiral notebooks". Used only with Generate; 2 objects read best, 4 at most.
- **Name on the end card** (required): the brand or show name, prefilled as found. Up to 12 characters at full size; longer names step the size down (150 px fits about 9 wide letters).
- **Line under the name** (optional, empty by default): a tagline or `NOTES`-style descriptor, up to 30 characters.
- **Surface** (pick): Blue cutting mat (default), Green cutting mat, Kraft paper, Light wood desk, Grey concrete. Prefill a surface the objects contrast with: dark-green or teal objects vanish on a green mat.
- **The turn move** (pick): Flip over (needs a photo of each object's back), Quarter turn (default: the objects lift and turn 90°), No turn.
- **Length** (slider, seconds): 13.5 default, 9 to 18. Under 11 s drop the second swap; over 15 s add one more swap.
- **Sound** (pick): None (default, as the example), A click on every landing, A music bed.

After the form:
- **Upload**: one `ask_question` saying exactly what to send, and wait for the attachments: "Attach 2 to 4 photos of your objects, shot straight down on a plain background, one object per photo (or several well apart). PNG cut-outs are ideal." With Flip over, add: "and a photo of each object's back, framed the same way." If the backs don't arrive, use the quarter turn.
- **Generate**: one `generate_image` of the objects together ("Top-down flat-lay product photo, shot straight down from directly above: <What to generate> side by side with clear space between them, no text, no logos. Plain seamless light grey background, soft even studio light, sharp focus, photorealistic."), then `decompose_image` on it to cut each object out. Backs aren't generated (a second generation never matches the fronts), so Flip over becomes the quarter turn; say so in the plan.
- **Logo**: never asked for separately; if the user wants theirs and none was found, they can attach it with the photos.

If the user skips the form, build with the prefilled values: with Generate prefilled, that means generating from the prefilled description. Never ship or reuse a product photo, logo or mat photo from another video.

## Timing

There is usually no speech under it. Start the next clip on a hard cut after the end card. With **A music bed** (`set_background_music` with a track from `list_library`, scope `default`), land each move's last frame on a beat (`tella-audio-sync`). With **clicks**, one short click or tap sound effect (`list_library` sound effects, then `add_sound_effect` at the video time) on each landing and each line burst, low in the mix. Because it is its own clip, nothing has to span a clip boundary.

## The look (values from the example, 1920×1080)

- **Canvas**: `canvas.set` frameRate 12/1, duration 13.5 s, clip background black.
- **Mat**: a texture image filling 2200×1400 at (-140, -160), in a group rotated -2.5° about the centre, so the grid never lines up with the frame. The example's texture is a photographed green mat recoloured blue with a `colorMatrix` (`[0.9,0,0,0,0, 0,0.25,0.75,0,0, 0,0,1.35,0,0, 0,0,0,1,0]`). For another surface, generate the texture without lines (see Building it).
- **Grid lines**: stroked paths, colour `#DBEBFA` (on green, `#EEF6EF`), butt caps: 10 horizontal at y = -63 + 134·i and 16 vertical at x = -45 + 134·i, 4.4 px; three 45° diagonals at 3.8 px (from (1064,-160) to (2060,836), and two short ones in the right corners); one dashed diagonal (dash 14/9, 3.3 px) from (1401,-160) to (602,1240).
- **Objects**: each photo 593×380 (keep the photo's aspect; about 30% of the frame wide), one group per object, resting about 215 px above and below the centre (or 230 px left and right for portrait objects), tilted -2° to +3°. A soft shadow on each group: dx 8, dy 14, blur 18, black at 0.5.
- **End card**: black, the mark centred about 100 px above the middle (the example's drawn cassette is a 320×204 white rounded rect, radius 26, with a `#2F7FE0` label stripe, black window and two white 7 px reels), the name below in Archivo 900, 150 px, tracking 12 px (0.08 em), white, caps, centred, top at y 600.

## The motion

Every key uses `hold` easing and sits on a 1/12 s grid, so each frame is a new held pose.

| Beat | Video time | What happens |
|---|---|---|
| Lines | 0.08 → 3.83 s | The long diagonal draws first (0.08–0.58), the dashed one wipes on (0.67–1.17), the corner diagonals (1.33–1.67), then the grid: one horizontal and one vertical start each frame from 2.08 s. Each line takes 6 frames with `trimPath` end 0, .42, .70, .88, .96, .99, 1 (ease-out cubic). |
| In | 3.67 → 4.83 s | Each object slides in from about 918 px off its edge (top and bottom), ease-out over 14 frames, its tilt settling from ±9° to ±2°; the second starts 3 frames later. |
| Swap | 5.5 → 6.75 s | The two trade places along arcs that bow about 525 px out to opposite sides, tilts swinging ±5°, ease in-out. |
| Flip / turn | 7.08 → 8.0 s | Each object (the second 2 frames later) lifts: scale 1 → 1.1 → 1 and shadow to dx 18, dy 32, blur 34, opacity 0.35 and back over 9 frames. A flip keys `rotateX` 0, 26, 56, 82 then -78, -50, -22, 0 with perspective 1800 and swaps the front photo for the back at the edge-on frame (opacity hold keys). A quarter turn keys rotation +90° (the other object -90°). |
| Swap back | 8.5 → 9.75 s | The same arc move to a new arrangement. |
| Black | 10.33 → 10.83 s | A full-frame black rect fades in over 7 frames (steps of 1/7). |
| End card | 11.08 → 13.5 s | The mark and name fade in over 6 frames; the mark keeps moving (the example's reels turn 360° over 3 s; a still mark rocks ±1.2° every 2 frames). |

**The boil.** Between moves, every object's x and y jump by up to ±1.2 px and its rotation by ±0.15° on every frame, as if nudged between shots. Without it the holds look like a frozen render. Add the same noise during moves too.

## Building it

1. `create_clip` (type `motion`, duration 13.5) on the video, then `update_clip` order 0. Then `canvas.set` frameRate {numerator 12, denominator 1}.
2. **Mat**: `addMedia` the texture by `sourceId`, then `node.patch` `destination` and `fit: "fill"` (it lands as `contain`). Without a mat photo, `generate_image`: "Seamless top-down texture of a plain self-healing cutting mat surface, matte <colour> vinyl, completely flat and evenly lit, shot straight down, fills the whole frame edge to edge. Fine light hairline knife scratches scattered sparsely, faint mottling and subtle grain. No grid lines, no rulers, no numbers, no text, no objects, no border, no shadow." (This gave a clean green mat. Use the same prompt for kraft paper, wood or concrete.) Draw the lines yourself, since generated grids are never straight.
3. **Lines**: per line, `addPath` (stroke), `addEffect` kind `trimPath` with an `effectId` (`trim_h0`, `trim_v3`…) and params {start 0, end 0}, then `setKeyframes` with `property: "field:@e.trim_h0/effect/end"` and the 7 hold keys. The dashed line: `addEffect` kind `dashPath` {dash 14, gap 9}, then kind `fx.linearWipe` with `effectId` `wipe_dash` and {completion 1, angle 0}, and key `field:@e.wipe_dash/effect/uniforms/completion/values/0` from 1 down to 0 on the same eased steps. Add every effect before you key it. Group the texture and lines as `mat` and set its rotation to -2.5°. One batch of about 90 commands is enough.
4. **Objects**: `addMedia` each photo, `node.patch` its destination centred on the canvas, then `group` it alone, and key only the group (anchors default to the canvas centre, which is the object's centre). Generate the keys in code: per frame, the pose eased between arrangements plus the boil noise, written as `setKeyframes` x, y and rotation with `hold` easing (at most 200 keys per call, so up to about 16 s). Key the lift with `scale`, `shadowX`, `shadowY`, `shadowBlur` and `shadowOpacity` on the same group.
5. **Black and end card**: `addShape` fill `#000000` with stepped opacity, then the mark (the logo with `addMedia`, or `addShape`/`addPath` drawings), and `addTitle` for the name, grouped as `logo` above the black.

## Checking it

`get_filmstrip` of the document at 1.0, 3.0, 4.3, 6.1, 7.5, 9.1, 10.6 and 12.5 s: lines half drawn, objects arriving, mid-swap, mid-lift, the last arrangement, the fade, the end card. Then a full-size `get_motion_frame` at a hold, to check each cut-out's edges against the mat. Last, play the clip in the video to check that two holds in a row differ by a pixel (the boil) and that nothing glides between frames.

## Gotchas

- `decompose_image` cut-outs can keep a grey haze of the old background around one object and be partly see-through at an edge. Clip the haze with a `setMasks` rect on the image (in canvas pixels, `expansion` -2, small radius) and `duplicate` the image inside its group so the edge turns solid.
- Key effect parameters by effect id (`field:@e.<effectId>/effect/…`), never by the effect's place in the list (`field:common/effects/0/…`), which other skills found refused as a keyed list. A shader's uniform is `…/effect/uniforms/<name>/values/0`.
- Masks don't follow transforms: put them on the image inside the group and move the group.
- `shadowColor` isn't a keyable property of a group; the style shadow is black by default, which is what you want.
- Linear keys look like a smooth render at a low frame rate, not stop motion. Use hold keys, the boil and slightly uneven spacing.
- A dark object on a dark mat disappears in the thumbnail: pick the surface for contrast.

## Variations

- Three or four objects: arrange them in a row, then a fan, then a stack, one move each.
- No mat: kraft paper or a wood desk with no grid, skipping the line draw (start the objects at 0.5 s).
