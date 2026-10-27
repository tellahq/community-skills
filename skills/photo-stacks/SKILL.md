---
name: photo-stacks
description: >-
  Louise's "photo stacks": the user's own saved images (mymind, Pinterest) as 3D
  photo stacks timed to the words, in two variants and selectable speeds (slow,
  medium, fast, or one card per spoken word). Fan = a pile of cards that slides
  out into a perspective fan beside the presenter with a small pill label
  (transparent overlay). Cascade = cards landing one by one, small to large, on
  light grey with one word either side, "you [photos] build" (full-frame
  b-roll). Use when the speaker lists things (hobbies, examples, outfits,
  projects, interests), or when asked for photo stacks, image fans, card stacks
  or collage moments. Part of Louise's minimal motion set with
  minimal-statements, minimal-steps and pink-blur-gradient. Needs Tella's
  freeform tools.
metadata:
  title: Photo stacks
  author: Louise de Sadeleer
  category: Images
  tags: photo stack, image fan, card stack, collage, 3D, perspective, pinterest, mymind, list, overlay, b-roll, minimal
  image: og.jpg
  poster: gallery/fan.webp
  preview: gallery/fan.mp4
  video: multiple-cool-motion-graphics-arhofrqp
  video-aspect: landscape
  video-start: "533.6"
  prompt: Add a photo stack where I list my hobbies, with images from my Pinterest and mymind. Show me a slow, medium and fast version.
---
# Photo stacks

Images the speaker's words point to, shown as a stack of real photos in perspective, never as a flat grid. See `references/reference.md` for the source of the look, the prompt that produced it and the approved examples.

`gallery/` has a clip and a poster of each approved example from the example video: the medium-speed fan ("fashion & wardrobe") and the per-word cascade ("you [photos] build"). Watch them to see the timing.

## The set
This is one of four skills that share one look: **minimal-statements**, **photo-stacks**, **minimal-steps**, **pink-blur-gradient**. Shared tokens: Inter only; ink #141414, grey #8C8C8C, light grey #ECECEC, card #F4F4F2, accent #D6336C; word reveal = opacity 0→1 in 0.3 s + blur 10→0 in 0.35 s starting ~0.05 s before the word; easeOutCubic in, easeInCubic out, never bouncy; full-frame pieces cut in and out hard (no outro on b-roll).

## Pick the variant
- **Fan** (overlay, speaker stays on screen): one topic with several examples ("fashion-related, wardrobe-related" → 3–5 outfit photos). Cards 210×315 start piled at the side's centre (x 1540 right, 380 left), slide out 85 px apart while turning to rotateY 32° (perspective 1100), drift 24 px over the hold, then fade out. A light pill label (24 px, weight 500) under the fan names the topic in the speaker's words. Put it on the side away from the presenter: check a frame first.
- **Cascade** (full-frame b-roll): a list said in one breath ("reading, your family life, sports, relationships") that ends in a point you can frame with two words ("you … build"). 3–5 cards, widths 190→280 px, rising 30 px, each overlapping the last by 45 %, rotateY 16°, each landing on its own spoken word (y +70 → 0, scale 0.85 → 1); then the left word and the right word (64 px, weight 300) appear on their spoken words.

## Pick the speed
`"speed"` in the spec:
- `slow` – 0.9 s entrance, 0.32 s between cards, 30 px drift. Calm, for a reflective line.
- `medium` – 0.6 s entrance, 0.14 s between cards, 24 px drift (the approved fan).
- `fast` – 0.35 s entrance, 0.06 s between cards, 12 px drift. A snap, for a quick aside.
- `word` (cascade only, the approved cascade) – every card on its own spoken word, 0.5 s entrance.
If the user hasn't said, use medium for a fan and word for a cascade; offer the other speeds after.

## Images
Search the user's own saves first: `list_library` scope `mymind` and `pinterest` with 1–3 word queries per item (Are.na may not be connected). Pinterest items carry a preview `url`: download candidates and look at them in one `montage` contact sheet before choosing. Prefer real photos of people and places that match the word literally; skip memes, UI screenshots and text-heavy images unless the line is about them. Import each pick with `add_library_item {from, sourceId: item id, scope: "video", videoId}`; the item's `url` and `dimensions` go into the spec. Never add an image of a specific person or brand the video doesn't mention.

## Steps
1. `get_transcript` (words) for the stretch, this turn. Times in the spec are seconds from the graphic's start.
2. `mkdir -p /workspace/mg && cp $HOME/.agents/skills/photo-stacks/scripts/*.py /workspace/mg/` (fallback `/workspace/skills/photo-stacks/scripts`).
3. Spec and run (`python3 photostack.py spec.json stack.json`):
   - fan: `{"variant":"fan","speed":"medium","dur":5.1,"t_in":0.1,"side":"right","label":"fashion & wardrobe","images":[{"uri":"…","w":1200,"h":1800}, …]}`. Start the overlay just before the first item is said; end it when the topic ends.
   - cascade: `{"variant":"cascade","speed":"word","dur":7.7,"images":[{"uri":"…","w":1200,"h":1053,"t":0.42,"name":"reading"}, …],"left_word":{"text":"you","t":4.78},"right_word":{"text":"build","t":6.24}}`.
4. `create_freeform_document` (1920×1080, a descriptive name), `read_file` the output and pass its commands unchanged to `apply_freeform_editor_commands`.
5. Place: fan → `add_overlay` with `freeformDocumentId`, `point {0,0}`, `dimensions 1920×1080`. Cascade → `add_layout` with `media: {type:"freeform", documentId}`, `transitionStyle: "hardCut"` (one call; `apply_video_edits` rejects freeform media), then confirm in `list_layouts` that the following section is `hardCut`.
6. `get_filmstrip` across the entrance (every 0.2 s) and the hold: cards never cover the presenter's face or body, the label is readable, each card lands on its word.

Read `references/freeform-notes.md` before editing freeform documents by hand.
