---
name: minimal-statements
description: >-
  Louise's "minimal statements": full-frame light-grey cards with thin
  curly-brace text. Statement: a short line builds word by word inside the
  braces, { networking is more impactful }, braces and four tiny corner dots
  spreading as each word lands, with an optional small grey letter-spaced label
  (REBUTTAL 02). Image inset: one word splits open, { build [image] er }, the
  halves turn pink and the slot cycles through one photo per item the speaker
  lists, then the word closes again. Hard cut in and out. Use for topic intros,
  numbered points, rebuttals, one-line claims, or a key word plus a quick list
  of examples, or when asked for minimal statements, bracket cards, brace text
  or a word with an image inside. Part of Louise's minimal motion set with
  photo-stacks, minimal-steps and pink-blur-gradient. Needs Tella's freeform
  tools.
metadata:
  title: Minimal statements
  author: Louise de Sadeleer
  category: Transition screens
  tags: minimal, statement, brackets, braces, kinetic type, word by word, title card, rebuttal, section intro, image inset, b-roll
  image: og.jpg
  poster: gallery/rebuttal-02.webp
  preview: gallery/rebuttal-02.mp4
  video: multiple-cool-motion-graphics-arhofrqp
  video-aspect: landscape
  video-start: "169.3"
  prompt: Add a minimal statement card for each rebuttal in this video, and an image inset where I list examples.
---
# Minimal statements

Two variants of one card, both 1920×1080 full-frame b-roll on light grey (#ECECEC) in thin Inter (64 px, weight 300, ink #141414) between `{` and `}`, with four 9 px black corner dots that ride on the braces. No exit animation: the card hard-cuts back to the speaker. See `references/reference.md` for the source, the prompt that produced each and the approved outcomes.

- **Statement** (2.5–5 s): 2–6 of the speaker's words build one by one. Each word fades and de-blurs in on its spoken word while the braces and dots glide outward (0.3 s easeOutCubic) to make room. Optional label (26 px grey letter-spaced caps, e.g. "REBUTTAL 03") 120 px above.
- **Image inset** (5–9 s): starts as one key word, `{ builder }`. On the first listed item the word splits at a natural break (build|er): the halves slide apart 0.4 s and turn accent pink (#D6336C), grey ← → arrows slide in at the sides, and a 170×110 rounded image slot opens between them. The slot swaps to a new photo on each spoken item, with the item's word as a small grey caption underneath. When the speaker lands the point ("that makes you a builder") the slot shrinks away and the word closes back to ink `{ builder }`.

`gallery/` has a short clip and a poster of each approved card from the example video: the `{ build[image]er }` image inset and the four rebuttal statements. Watch them to see the timing.

## The set
This is one of four skills that share one look: **minimal-statements**, **photo-stacks**, **minimal-steps**, **pink-blur-gradient**. Use them together freely; don't mix in other text styles. Shared tokens: Inter only; ink #141414, grey #8C8C8C, light grey #ECECEC, card #F4F4F2, accent #D6336C; word reveal = opacity 0→1 in 0.3 s + blur 10→0 in 0.35 s starting ~0.05 s before the word; easeOutCubic in, easeInCubic out, never bouncy; full-frame pieces cut in and out hard.

## When to use which
- Statement: every instance of the same kind of beat (each rebuttal, each numbered point) gets one card, same label style, numbered consistently.
- Image inset: one key word (a role, an idea) followed by a quick list of 3–6 examples in one breath ("whether you do that by making videos, by writing, by making websites… that makes you a builder"). The word must be one the speaker says.
- Words are the speaker's own, shortened only if the meaning holds ("all of my work is in private repos" → "my work is private"). Never add a claim. At most 6 words.
- Skip a beat if a screen demo the viewer needs is on screen at that moment.

## Steps
1. `get_transcript` (words view) for each beat, in this turn. Card start = the first word that introduces the beat, card end = just before the next sentence (trim lead-in dead air). Spec times are seconds from the card start.
2. Copy the scripts: `mkdir -p /workspace/mg && cp $HOME/.agents/skills/minimal-statements/scripts/*.py /workspace/mg/` (fallback `/workspace/skills/minimal-statements/scripts`).
3. Write a spec and run it in `/workspace/mg`:
   - Statement: `{"label": "REBUTTAL 02", "label_t": 0.06, "words": ["networking","is","more","impactful"], "times": [1.27,1.87,2.19,2.33], "dur": 4.1}` → `python3 statement.py spec.json card.json` (label may be null). Each word's time = its spoken word's start (the nearest spoken word when you paraphrase).
   - Image inset: `{"left": "build", "right": "er", "dur": 8.3, "open_t": 0.45, "close_t": 7.1, "images": [{"uri": "…", "w": 400, "h": 300, "caption": "videos", "t": 0.45}, …]}` → `python3 inset.py spec.json card.json`. `open_t` = first item's word, each image's `t` = its item's word, `close_t` = the word that lands the point.
4. Inset images: search the user's own saves first (`list_library` scope `mymind` and `pinterest`, 1–3 word queries per item; Are.na may not be connected). Look at Pinterest candidates in one `montage` contact sheet. One literal, readable image per item (a real photo beats a diagram at 170×110). Import each pick with `add_library_item {from, sourceId: item id, scope: "video", videoId}` and use the item's `url` and `dimensions`.
5. `create_freeform_document` (1920×1080, a descriptive name), `read_file` card.json and pass its commands unchanged to `apply_freeform_editor_commands`.
6. Place it: `add_layout` on the clip, `startTimeMs`/`durationMs` = card start/length (clip playback ms), `media: {type: "freeform", documentId}`, `transitionStyle: "hardCut"`. One call per card (apply_video_edits rejects freeform media). Then `list_layouts` and make sure the section right after the card is `hardCut` too.
7. Check with `get_filmstrip`: for a statement, the start, two word landings and just before the end (the last word must not touch the closing brace); for an inset, every image swap and the close (each photo readable, captions under the slot, the word fully closed before the cut).
8. Make the remaining cards from new specs (same label style, same size). Report each card's time and words.

Read `references/freeform-notes.md` before editing freeform documents by hand.
