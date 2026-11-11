---
name: google-search-ui
description: >-
  Recreate a Google search in Chrome on macOS as live Tella Motion: the Chrome window, the Google
  homepage, a cursor that clicks the search box, a query that types itself while the autocomplete
  dropdown changes under it, Enter, the results page loading in a cascade with the user's own site as
  the first result (favicon, site name, URL, blue title, snippet, sitelinks), then a hover and click
  that lands on it. Every label is editable and timed to the narration. Full-frame b-roll or its own
  clip, with a generic search engine in place of Google's marks when wanted. Use when asked for a
  Google search animation, someone googling the product, "just search for us", a search results page
  as b-roll, a recreated Chrome window, or a search and click-through shot.
metadata:
  title: Google Search UI
  author: Tella
  category: Full animations
  image: og.jpg
  poster: gallery/google-search.webp
  preview: gallery/google-search.mp4
  tags: google, search, chrome, browser, ui, typing, autocomplete, results, cursor, product demo
  prompt: When I say "just search for us", show someone googling "tella ai video editor" in Chrome and clicking through to our page.
---

# Google Search UI

A Google search rebuilt the way a motion designer redraws UI for a product video: the real layout, colours and type, every label live, and the UI performing the search at a human pace. It is a whole-window shot, so it plays as full-frame b-roll over the line where the speaker talks about being found, or as its own clip; it doesn't fit in a corner. Builds on `tella-ui-redraw` (screens as shapes, paths and titles) and `tella-ui-interactions` (typing, press, loading); follow `tella-motion-design` for timing. Geometry, colours, icon and cursor paths and Inter advance widths are in `references/layout.md`: read it before building and take numbers from it.

## Ask once

Work these out yourself and never ask: where the search happens (the transcript words that introduce it, "just search for…", "google us"); full-frame b-roll over that range, or its own clip when the video has no speech there or the message says so; the five autocomplete suggestions per key (an ordered pool of plausible phrases that start with the prefix, the user's product among them); the refinement chips (6–7 short follow-ups to the query: "Pricing", "Review", "For Mac"); the profile pill (`Work`), footer country, and the URL's `/search?q=` string. Fetch the user's site (`import_from_url` of their home page, or the URL in the message) to prefill the result.

Then one `ask_form`, every field prefilled so the user can just submit:
1. **Query** (required): what gets typed, lowercase as people type, 2–5 words, at most 32 characters so the box never overflows. Prefill from the speaker's words or `<product> <what it does>`.
2. **Result URL** (required): the page the click lands on, e.g. `tella.com/ai-video-editor`. Prefill with the home page or the page the speaker names.
3. **Site name**: the name above the URL, at most 24 characters. Prefill from the site's title or brand.
4. **Result title**: at most 55 characters (one line at 30 px). Prefill from the page's `<title>`.
5. **Snippet**: at most 150 characters (two lines). Prefill from the page's meta description; never invent claims.
6. **Sitelinks**: 3–4 page titles, comma-separated, each at most 24 characters. Prefill from the site's main navigation (Pricing, Features, …); each one's line under it comes from that page's description, cut to ~55 characters with " ...".
7. **Ending** (pick): click the result (default), hold on the results page, or stop at Enter. Stop at Enter skips the results page, so fields 2–6 go unused.
8. **Real Google look** (switch, on by default): off draws a generic search engine instead (see Brand marks).

Media: the result's favicon. Look first in the message's attachments, then the media library (the brand's logo), then the site's favicon or icon from `import_from_url`. Use a square image, masked to the 38.8 px disc. Only if none exists, `ask_question` once for "your site's favicon or a square logo (PNG)", with "Use a letter instead" as a suggested answer; that fallback is a disc in the brand colour with the site's initial in Inter 700 white. Cursors, icons and wordmarks are drawn, so nothing else is needed.

If the user skips the form, build with the prefilled values. Every other result or suggestion that names a business is fictional ("Northwind Notes"); never show another real company or copy a real results page.

## Time it to the speech

The document clock starts where the graphic starts. Put the first key 0.2 s after the word that introduces the search, keep about 90 ms a key so a 20-character query takes about 2 s, and press Enter on the beat after the query is said. Land the results on the next phrase and the hover on the word that names the result ("…and there we are"). If the speaker is quick, shorten the cursor's approach (0.6 s minimum) and start typing on the click; if slow, hold the finished query with the dropdown open rather than slowing the keys. Keep the whole graphic under 15 s; the example runs 9.7 s.

As b-roll, the shot belongs to one clip: `add_layout` takes a `clipId` and times on that clip's playback timeline, so it can't run into the next clip. Keep it inside the clip where the words are said (start it earlier or shorten the hold so it ends by the clip's end). Only when the spoken range truly crosses a cut, split it there (untested): one Tella Motion document and one `add_layout` per clip, each `transitionStyle: "hardCut"`, the second document starting on the frame the first ended on, with keys on each clip's own clock. Then `list_layouts` and make sure the layout after each b-roll is a hard cut too (it can come back with a spring).

| Time | What happens |
|---|---|
| 0–0.9 s | Window on screen from frame one, `ui` settling from 103 % to 100 % (ease `{0.22, 1, 0.36, 1}`) |
| 0.25–1.22 s | Arrow glides from (1560, 1000) to the box at (826, 494), ease `{0.45, 0, 0.2, 1}`; it becomes the I-beam at 1.0 s |
| 1.24–1.44 s | Click: cursor scale 1 → 0.88 → 1; the box's focus layer fades in over 0.15 s; the caret appears at 1.35 s |
| 1.75–4.05 s | 21 keys, 70–200 ms apart (~90 ms, +90 before a space, +50 after). Dropdown and the ✕ with its divider open on the first key; the suggestions change on every key |
| 4.47 s | Enter: dropdown and caret go, the tab favicon becomes the spinning blue arc, reload becomes ✕, the omnibox shows the `/search?q=…` URL |
| 4.79 s | Results page replaces the homepage, tab title changes. Chips, result head, title, snippet and each sitelink fade up 10 px, 60 ms apart (opacity 0.3 s, y 0.4 s, ease `{0.22, 1, 0.36, 1}`) |
| 5.07 s | I-beam back to the arrow |
| 5.22 s | Loaded: favicon back, reload back |
| 5.52–7.22 s | Camera `cam` pushes 100 % → 114 %, ease `{0.45, 0, 0.2, 1}`, anchored top-left so tab and omnibox stay in frame |
| 5.82–7.12 s | Arrow travels to the title, a third of the way in and 4 px below its centre (470, 541) |
| 7.04–7.12 s | Hover: the pointing hand, then the title's underline (1.7 px rect, the title's colour and width, 17 px below its centre) |
| 7.83–8.05 s | Click: hand scale 1 → 0.88 → 1; at 8.0 s the spinner starts and the omnibox shows the result URL. Hold ≥ 1.5 s |

Ending "hold on results" stops after 5.5 s with the camera push and no cursor move; "stop at Enter" holds on the Enter state with the spinner turning for ~1.5 s.

## The look

1920 × 1080, light theme. A pale grey-blue backdrop `#e4e8ee`; the window fills it (x 40, y 20, 1840 × 1040, radius 20) with a cool gradient frame, a 1 px dark edge at 22 %, a white inner bevel, and two shadows (blur 64 dy 28 `#1b2a44` 28 %, blur 10 dy 4 black 18 %). Everything is at 1.44× desktop size, so body text is 20–24 px and titles 28–30 px.
- **Chrome**: gradient tab strip `#e0e9fd` → `#d2dffa`, glossy traffic lights, the tab search chevron, one white tab whose bottom corners flare into the toolbar (favicon, title, ✕), then +. White toolbar: back, forward greyed, reload, the omnibox pill `#eef2f9` (1387 px wide) with the white site-info disc and the URL, the star, only the puzzle piece, a divider, the profile pill with a purple initial disc, and ⋮. Long URLs and tab titles fade out under feathered masks.
- **Homepage**: Gmail, Images, apps grid, blue Sign in pill `#2656c9`; the wordmark centred; the 75 px search box with +, mic, lens and the AI Mode pill; the footer.
- **Results page**: small wordmark, search box with the query and ✕; the tab row (AI Mode, **All** underlined, Images, Videos, News, Short videos, Web, More ▾, Tools ▾) over a hairline; outlined chips; the result: favicon disc, site name `#16171a`, URL with › in `#4e5156`, ⋮, title `#180ea4` Inter 30, snippet `#4f4f4f` Inter 21 over two lines, four sitelinks between hairlines with chevrons. The page runs off the bottom: that's correct.
- **Type**: Inter throughout (close to Chrome's and Google's faces at this size, and it has the advance table, so carets and underlines land): 400 for text, 500 for tabs and Sign in, 700 for the completed part of each suggestion.

## Building it in Tella Motion

One 1920 × 1080 document. Groups (`node.insert` type `group`, then `addShape` / `addTitle` / `addPath` with `parent`): `backdrop` · `cam` → `ui` → `win` → (`win.border`, `win.edge`, `win.body`, `chrome`, `page` → (`home` → `box` → `dd`, `res` → blocks)), and `cam` → `cursor` → (`cur.arrow`, `cur.ibeam`, `cur.hand`).
- **Typed text**: one title per prefix (`q1` … `q21`), each with its own `start` and `duration` so one shows at a time; the last lasts until the page swaps. More reliable than a typewriter animation and allows an uneven rhythm.
- **Caret**: a 2 × 29 rect whose `translateX` is hold-keyed to 537 + width(prefix) at each key, from the Inter table; `opacity` hold-keyed.
- **Suggestions**: per key a group `dd.sN` of five titles windowed to that key; `node.patch` each `content` to a `richParagraph` with the prefix in `font.freeform.inter.400` and the rest in a run with `fontId: font.freeform.inter.700`, `fontWeight: 700`.
- **State swaps** (favicon/spinner, reload/stop, three URLs, two tab titles, homepage/results, the three cursors): hold-keyed `opacity`. The spinner group rotates linearly (about 500°/s) about the favicon centre.
- **Loading cascade**: each results block is a group keyed `opacity` 0 → 1 and `translateY` 10 → 0.
- **Cursor**: shapes drawn with the hotspot at (0, 0), so the `cursor` group's `translateX/Y` is the screen position; set its anchor to (0, 0) before keying `scale`.
- **Masks**: `page` gets one rounded-rect mask for the window; the tab title (x 180 → 515) and the URLs (x 150 → 1539) get rect masks with `feather` 22–26. Masks don't follow the node's own transform: move the parent.
- **Shadows**: `effects` `dropShadow` on the window frame, search box, dropdown card and cursors.
- The example is about 560 commands; batches take at most 256, so send three. To rebuild, `node.remove` `cam` and `backdrop` first or ids collide.

## Brand marks

The real look draws three marks, each in its own group so they can be swapped: `brand:google-wordmark`, `brand:google-wordmark-small` and `brand:google-g-favicon` (four stroked arcs `#e85247 #f5c142 #4eac60 #4a84f7` and a bar). The result's favicon group is `brand:<site>-favicon`. Nothing is a downloaded logo: set the wordmark as Poppins 500 type with one colour per letter (`#3186ff #fc413d #ffbe00 #3186ff #00af57 #fc413d`). The example draws its wordmark as filled letter outlines; this skill doesn't ship those. With **Real Google look** off, leave out the three Google groups, set a neutral one-word wordmark in Inter 600 `#1f1f1f`, a grey globe favicon, the tab title "<query> - Search", no "Gmail", and `search.example` in the omnibox.

## Checking it

- `get_motion_frame` (with `startTimeMs`) at full width: 0.5 s (empty homepage), 3.0 s (mid-typing), 5.6 s (results loaded), 7.3 s (hover), the last frame.
- Every suggestion starts with the typed prefix and bolds only the rest; the caret sits just after the last letter on every key (check the longest prefix); the underline is exactly as wide as the title.
- One `get_motion_preview` at 10 fps: keys arrive unevenly but steadily, the dropdown changes on keys, the page loads in a cascade, the hand and underline arrive together, the last state holds ≥ 1.5 s.

## Gotchas

- Text sits in its box by font metrics: for Inter at line height 1.2 put the box top at centre − 0.62 × size.
- `addTitle` registers a font asset per weight; create one plain title in Inter 700 before a `richParagraph` refers to it.
- A title wider than its box wraps: give long URLs a 2400 px box and mask them.
- A title over 55 characters runs past the snippet's width; shorten it rather than shrinking the type.
