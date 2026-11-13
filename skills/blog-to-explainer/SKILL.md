---
name: blog-to-explainer
description: >-
  Turn a blog post URL into a 15–90 second explainer video in Tella: read the
  post, write a short script, then build a title card, one Tella Motion scene
  per key point (count-up numbers, proportional bars, step lines, branch
  diagrams, rings, kinetic statements, splits, lists, footage), the post's page
  captured scrolling, optional public-domain film b-roll, background music with
  every cut on the beat, and an end card. Every scene is one editorial layout
  on a 12-column grid with a solid colour field that changes shape across each
  cut, so the video plays as one continuous piece. Narration is optional:
  music-only scenes, or the user's voiceover with the scenes cut in as b-roll
  and captions on. Use when asked to turn a blog post, article, changelog page
  or URL into an explainer, summary or social video.
metadata:
  title: Blog post to explainer
  author: Tella
  category: Editing & effects
  image: og.jpg
  poster: gallery/paper-story.webp
  preview: gallery/paper-story.mp4
  prompt: Turn this blog post into a 60-second explainer video with music and no voiceover https://www.tella.com/blog/self-updating-help-docs-with-videos
---

# Blog post to explainer

A post becomes a short explainer: one Tella Motion scene per idea, cut together on the beat of the music (or on the speaker's words). The viewer should get the post's point with the sound off. Builds on `tella-plan-video` (the script), `tella-title-cards` and `tella-explainer-graphics`.

## The look: field and column

Every scene is a printed page on a 12-column grid plus one solid colour field: a full-bleed rectangle whose inner edges sit in the grid's gutters, so each layout is a deliberate split of the frame (right five columns, left half, top band, full frame, bottom band), never a card floating in space. The field frames the scene's main idea: the big number sits in it, the footage fills it, the page capture hangs in it.

At every cut the field changes shape from this scene's layout to the next one's. Each scene starts with the field halfway between the last layout and its own and ends halfway to the next, so the cut lands mid-move and the video plays as one piece. A running header (series title left, e.g. "Tella blog · Self-updating help docs"; section label and `NN/NN` right) and a thin progress line never move, and invert where the field covers them.

## 1. Read the post, ask once

Fetch the URL and read all of it. Note the title, the one-line point, and every number, step, before/after, rule or list in the post's own words. Never add a fact, number or name it doesn't give. If you can't reach the page, ask for the text.

Then one `ask_form`, each with your guess filled in:
- **Voice**: music only (default) / I'll record a voiceover (write the script, `get_recording_link`) / I have a recording.
- **Length**: 15 s / 30 s / 60 s (default) / 90 s. Under 30 s, keep the title card and two or three scenes.
- **Look**: Paper / Midnight / my brand (background, ink, one field colour, a font from `list_motion_fonts`).
- **Music**: four tracks from `list_library` `scope: "default"`, `type: "music"`.
- **Footage**: the page capture (always), public-domain vintage film, generated images (costs AI Credits).

## 2. Script and scene plan

About 150 words a minute, short sentences, the post's words, open on the hook, never "In this post". A title scene (4–5 s, the page capture in its field), one scene per key point (3–6, 4–6.5 s each), an end card with the takeaway and link (4.5–5 s). Give each point the shape it has, and the field a resting place that suits it:

| Shape | Scene | Field at rest |
|---|---|---|
| Hook | title beside the scrolling page | right five columns |
| The source itself, a before/after, a checklist | page capture with url; bars on one scale; rows with rules | left three columns |
| One big number; growth to a share | count-up up to 560 px; ring with a count | left half |
| This vs that | two columns at one size | right half |
| Part of a whole; a process; a rule with a condition | proportional bar with big legend figures; steps on a line with a travelling playhead; pills, a diamond, yes/no | top band, y ≤ 440 |
| A claim | kinetic statement, word by word | full frame |
| A physical idea | footage filling the field | left seven columns |
| Takeaway and link | takeaway on the page, link set large on the field | bottom band, y ≥ 600 |

At most seven headline words per scene plus a short note. Never the same layout twice in a row: the field would have nowhere to move. Show the plan (scene, layout, words, source sentence) and wait for a go.

## 3. Visuals

- Page capture: `import_from_url` with `scroll: true` (a 12 s scroll of the page). Crop it to the article column and hang it as a white sheet bleeding off the frame edge. One `get_filmstrip` of the source shows where to start: on headings and text, not the site's navigation or screenshots with people; play it at 0.6–0.8× speed.
- Vintage film: `list_library` `scope: "vintage"` with a topic word, look at frames of the clips, then `add_library_item` `from: "vintage"`, `scope: "private"` (scope `video` is refused). Credit the film in 22 px mono.
- Generated images only if the user agreed; they fail with "out of credits" in workspaces without AI Credits. The capture plus vintage film covered every example.

## Design system

- **Grid** 1920×1080: 12 columns of 112 px, 32 px gutters, 112 px margins. Field edges in the middle of a gutter or on the frame edge; content keeps one empty column from the field's edge. Header cap top at y 50, progress line at y 1014 (2 px track, 4 px fill), content between y 140 and 960.
- **Paper**: page `#F2EEE6`, ink `#161513`, muted `#6E6A62`, cobalt field `#2B44FF` with white type, field muted `#B8C1FF`, field track `#5468FF`, hairlines `#D9D3C7`, coral `#F0532D` only for the bad part of a bar. Archivo 800 at −0.03 em.
- **Midnight**: page `#0F1012`, ink `#F1EDE4`, muted `#8E918F`, amber field `#F2B33D` with `#141312` type, field muted `#6E5216`, field track `#D89A26`, hairlines `#2A2C30`. Space Grotesk 700 (its maximum).
- **Brand**: background, ink, one field colour, and two tints of the field colour that read on it (secondary text, tracks). The serif example: `#ECE8DD` / `#1B211D` / field `#1F5640` with `#F3EFE3` type, Playfair Display 800 at −0.01 em, line height 1.06. The vermilion one: `#F7F5F0` / `#141414` / `#E4472B`, DM Sans 800.
- **Type**: one display face, line height about 1.04; Inter 500 for notes at 32–38 px; Roboto Mono 500 uppercase at +0.12 em, 26 px, for the header, kickers and labels. Fit display copy to its column in balanced lines: titles 84–150 px, statements up to 260 px, split columns up to 150 px, legend figures up to 128 px, steps 34–64 px, end link up to 220 px. Same role, same size within a scene (all steps, both split columns). Nothing under 26 px except the credit.

## Motion

- Field hand-off: each half of the move takes 0.45 s, `easeInCubic` into the cut and `easeOutCubic` out of it, so the speed matches across the cut. The first scene's field grows in from its frame edge over 0.9 s; the last one holds.
- Entrances in reading order: parts rise 40 px over 0.7 s on bezier `{x1: 0.16, y1: 1, x2: 0.3, y2: 1}` and fade in over 0.35 s. Headlines rise word by word (`setTextAnimation` `rise`, `unit: "word"`, 0.7 s, 0.06 s stagger). A statement's words are separate titles rising 70 px over 0.8 s, 0.09 s apart.
- Lines, bars and rings draw on with `trimPath`; numbers count up (about 1.35 s); the steps playhead travels its line to each step as it lands.
- Never still: the page side drifts up 32 px over the scene and the field's content 64 px; footage scales 1.08 → 1.14; the progress line draws on across the whole video. In the last 0.3 s content rises 60 px and fades as the field moves on, so all motion runs upward. Nothing ever cuts to a blank frame.

## Timing

- **Music only**: each scene is a Tella Motion clip (`create_clip`), with the video's `defaultClipTransition: "hard_cut"`. Music at volume 0.45; from `get_music_beats`, end the first scene on a beat and make every other scene a whole number of beats; land counts, draws and steps on beats too.
- **Narrated**: no hand-off between scenes; each grows its field in from its frame edge and holds to its last frame, and there's no progress line. Time scenes to the words (tella-motion-design). Add each as b-roll with `add_layout` (Tella Motion `media`, hard cut), the speaker on screen between. Captions on, one line, in the display face; music at 0.12.

## Building it in Tella Motion

One document per scene, in this structure so it stays editable: a background fill; a "Paper side" group; the header and progress line; then a "Field" group holding a full-frame fill in the field colour, any media, a "Field content" group and an inverted copy of the header and line, alpha-matted (`setMatte`) to a hidden rect named `field`. Keyframe that rect's geometry for the hand-off, and everything on the field clips to it and moves with it. Build the first scene of a kind, check it, then `duplicate_motion_document` it for the next.

Gotchas found building the examples:
- Eased `setKeyframes` on an effect field (the `trimPath` end) fails with "is a keyed list": drive it with `setCurve` and `bindProperty` instead. A curve can drive the steps playhead's `x` too, so it stays on the line's end.
- Effect ids are document-wide: name them `trim_<node>`.
- `addMedia` fits to the whole canvas and scales about the canvas centre: to fill the field, set its destination to the field rect with `fit: "cover"` and anchor it at the rect's centre.
- Media `volume` is dB: mute with −60, not 0.
- Playfair's old-style figures make "01" read as "o1": set step numbers in Inter.
- `addTitle`'s `box.y` is not the cap top: the first baseline sits at `y + lineHeight × fontSize × ascent/(ascent+descent)`. Measured ratio / cap height: Inter 0.801/0.728, Archivo 0.807/0.686, Space Grotesk 0.771/0.700, Playfair 0.812/0.708, DM Sans 0.762/0.700, Roboto Mono 0.795/0.711. `align` defaults to centre; always pass it.
- When a layout changes, rebuild its neighbours too: their hand-offs point at it.

## Check

- Each scene: one `get_filmstrip` of its document at 0.4 s, mid-build and 0.5 s before the end. Look for orphan words, text touching the field's edge, overlaps, a column with an empty half.
- The video: `get_filmstrip` across it and around every cut: every part arrives, the field sits in the same place on both sides of a cut, nothing flashes or holds still.
- Every on-screen number and name against the post. Say you can't judge the music level by ear.
- Report the link, length, one line per scene (time, layout, words) and anything you guessed.

Vertical: the grid is 16:9 only. For a Short, hand the explainer to `tella-short` or rebuild the strongest two or three scenes at 1080×1920. For a series, keep the theme and header line so every explainer shares one look.
