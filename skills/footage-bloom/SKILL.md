---
name: footage-bloom
description: >-
  Put a cinematic bloom on a stretch of the user's own footage in Tella: the
  bright parts swell into a soft glow with a warm red halation around the
  lights and thin tinted anamorphic streaks running sideways through them, then
  settle back to the clean shot, so the entry and exit never show as a cut.
  Built as a live Tella Motion overlay that replays the clip under a glow, a
  halation layer and a streak shader, keyed to one envelope. Best on footage
  with real highlights (night streets, lamps, neon, screens, sun through
  windows). Use when asked for a bloom, glow, halation, dreamy or cinematic
  glow, lens flare streaks, anamorphic streaks or flares, a sci-fi flare
  look, glowing lights or a romantic lift on a moment of footage.
metadata:
  title: Bloom
  author: Tella
  category: Editing
  image: og.jpg
  poster: gallery/anamorphic-bloom.webp
  preview: gallery/anamorphic-bloom.mp4
  prompt: When I say "that's when the city lit up", make the street lights bloom with blue anamorphic streaks and let it settle after the sentence.
---

# Bloom

A treatment of the user's **own footage over a short range**. Outside it the clip plays as shot; inside, the highlights swell into a soft glow, a red-orange halation bleeds around them, and thin blue streaks stretch sideways through every hot light, held for the phrase, then everything settles back. It is one Tella Motion overlay laid over the clip that plays the clip's footage again with the effects on it; the clip's sound is untouched. It suits night streets, neon, headlights, screens, stage lights and backlit hair: a romantic, dreamy or cinematic lift on one moment.

Builds on `tella-motion-design` (timing, checking) and pairs with `tella-camera-moves` (a slow push-in under the swell). Not for retro looks (`retro-footage-looks`) or cut stingers (`glitch-transitions`).

## Ask once

Work these out yourself and never ask: the clip and its source (`list_clips`, `list_sources`), the stressed word or beat (`get_transcript` word timings; over music `get_music_beats`), whether the footage has highlights (look at a frame at the planned peak with `get_clip_frame`), the canvas size and the clip's layout.

Then one `ask_form`, every field prefilled, so the user can just submit:

| Field | Type | Required | Default / prefill | Limits |
|---|---|---|---|---|
| **Where** | text | yes | the selected clip or range ("0:08–0:13"); with nothing selected, the phrase around the stressed word (`peak on "lit up" at 0:11`) | one range, 1.5–8 s; a whole clip is fine |
| **Strength** | slider, % | yes | 100 (the values below) | 20–120 |
| **Streaks** | switch | no | on | |
| **Streak colour** | pick | no | Blue | Blue, Warm, White |
| **Halation** (red glow round the lights) | switch | no | on | |
| **How it moves** | pick | no | Swell and settle | Swell and settle, Steady |

If the frame at the peak has no real highlights (flat daylight, a lit talking head against a wall), say so in the form's intro: the bloom will mostly fog the shot, and lights in frame help. Don't ask for other media: the footage is the user's clip. If the range is a screen recording or a graphic, say bloom needs camera footage and stop, or offer a night clip from Tella's vintage catalogue (`list_library` scope `vintage`) as b-roll under it.

Skipped or dismissed form: build with the prefilled values. One bloom per range, at most a few per video; it is an accent.

## Timing

Times are on the overlay's clock (word time − overlay start). Start the overlay 0.9 s before the ramp begins, or at the clip's start.

- **Swell and settle** (the example, 5 s): 0 until 0.9 s, ramp in to the peak by 1.6 s (`easeInOutSine`), hold to 3.8 s, ramp out to 0 by 4.5 s, overlay ends at 5.0 s. With a word: the peak lands on the word's start, the hold lasts the phrase, the ramp out starts at the phrase's end. Ramps stay 0.7 s.
- In Swell and settle, every keyed track starts with a `hold` key of 0 at 0 s (easing applies from a key to the next, so the value stays 0 until the ramp's own `easeInOutSine` key of 0 at 0.9 s), and the replay matches the clip at the overlay's edges.
- **Steady**: full strength for the whole range. Inside a clip: a key of 0 at 0 s with `easeInOutSine` easing, full strength at 0.3 s, held, then full strength with `easeInOutSine` at 0.3 s before the end and 0 at the end. Never a `hold` key of 0 first, or the effect snaps on at 0.3 s. On a cut (the overlay starts or ends with the clip): put a full-strength key there instead of the 0 key and its ramp.

## The look (from the example, 1920×1080)

Three media nodes playing the same source, full frame, painted in this order. All three envelopes share the key times above.

- **`footage`** (normal blend): `curves` "cool" (red 0.5→0.46, 1→0.97; blue 0→0.03, 0.5→0.55), `curves` "pink_tint" (red 0→0.04, 0.25→0.30; green 0.25→0.23; blue 0→0.03, 0.25→0.28), then `glow` radius 120, threshold 0.45, softness 0.5, `intensity` keyed 0 → **2.2**.
- **`streaks`** (blend `screen`): `erode` radiusX 0, radiusY 12 → `fx.levels` inputBlack 0.78 → `blur` radiusX 30, radiusY 1 (decal) → the `streak` shader (`references/streak-shader.md`): threshold 0, reach 800, tint Blue `0.4, 0.65, 1, 1`; `amount` keyed 0 → **1.8**.
- **`halation`** (blend `screen`): `fx.levels` inputBlack 0.6 → `blur` 24 × 24 (decal) → `fx.tint` black to `0,0,0`, white to `1, 0.235, 0.078` (`#FF3C14`), amount 1 → `fx.exposure` 1.2; node `opacity` keyed 0 → **1** with `easeInOutCubic` ramps.

Form mapping:
- **Strength** scales the three peaks linearly (100% = 2.2 / 1.8 / 1). Above about 120% the frame fogs; on bright daylight footage raise the glow threshold to 0.6 instead of the strength.
- **Streak colour**: Blue `0.4, 0.65, 1, 1`; Warm `1, 0.62, 0.3, 1`; White `1, 1, 1, 1`. Streaks off: leave out the `streaks` node.
- **Halation off**: leave out the `halation` node.
- The two `curves` are a static cool/pink grade. Keep them when the overlay covers whole clips (it starts and ends on cuts, as in the example). On a range inside a clip, leave them out, or the grade switches on at the overlay's edge.

## Building it

1. `add_overlay` of a new Tella Motion document on the clip: `point` 0,0, `dimensions` the video size, `depth: "front"`, `transition: "hard_cut"`, no `animation`. Canvas duration = the overlay's. Name it "Bloom: <word>". If the clip's layout is padded, switch it to fullscreen first: the replay is full frame.
2. `addMedia` the clip's source three times as `footage`, `streaks`, `halation` (that paint order). One `node.patch` each: `fit: "cover"` (`addMedia` lands with `contain`), `audio` `{assetId: "media.<sourceId>", mute: true}` so the sound isn't doubled, and `sourceIn` = range start in source time, in ticks (1 s = 254016000000; add the clip's trim). `streaks` and `halation` also get `common.blendMode: "screen"`.
3. `addEffect` the stacks above in order (`index` sets order; on a new document run one `addEffect` of each built-in shader kind before any raw insert). The streak shader is `kind: "shader"` with the source passed as written and every uniform given a value.
4. `setKeyframes` on the glow `intensity`, the shader's `amount` and `halation` opacity. Take each `field:` path from `inspect_motion_node_properties`: on a media node the index is the effect's storage index, not its place in the stack.

A range that crosses a cut: an overlay belongs to one clip and can't span clips, so split the range at each clip boundary and build one document and overlay per clip, each with its own source and `sourceIn` and its keys on that clip's own clock. The envelope carries over the cut: the side before the cut ends at the value the curve has at the cut, and the side after starts there (a full-strength key on each side for Steady; in Swell and settle, put the peak's hold across the cut where possible).

Several ranges: build one, check it, then `duplicate_motion_document` (a document plays in one place only) and change the keys and `sourceIn`. Sound is optional: a soft riser from `list_library` sound effects at 0.3–0.5 under the swell, only if asked.

## Checking it

- `get_filmstrip` of the clip at the overlay start, the ramp start, the peak, the ramp-out end and the overlay end: identical to the clip before and after, the peak on the word, nothing popping at the edges.
- One frame at the peak at 1920 wide: streaks thin and smooth (beads mean the `blur` before the shader is too small; flat grey bars mean the levels cut is too low), halation a red rim on the lights, not a red wash; faces still readable.
- A 5 fps `get_video_preview` across the range: the swell moves without a step.
- Report the range, peak strength, streak colour and what the peak lands on.

## Gotchas

- `glow` can't be a backdrop, and a backdrop shape with a non-normal blend drops its backdrop: that's why the footage is replayed instead of filtered from above.
- A shader that changes source needs `removeEffect`, `addEffect` again, then re-keying. A broken SkSL asset poisons the document's renders: rebuild in a fresh one.
- SkSL loops must be `for (int i = 0; i < N; i++)` with N ≤ 128; the streak shader uses 121 taps.
- Deleting the clip leaves its document marked as playing; `duplicate_motion_document` it to reuse it.

## Variations

- Halo only: streaks and halation off, glow peak 1.3, radius 80, threshold 0.55 (subtler, for faces).
- Warm streaks with the halation off, for sunset or candle light.
