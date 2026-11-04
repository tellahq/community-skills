---
name: notification-pop
description: >-
  Pop phone or desktop notifications over a Tella video, timed to the words:
  "Payment received $49", "New signup", "Deploy succeeded". Pick the platform
  and they read as it at a glance: iOS lock-screen banners (top centre, drop in,
  older ones tuck behind into a pile), macOS notification-centre banners (top
  right, slide in from the edge, older ones pushed down) or Android heads-up
  cards (round icon, "App • now" header, expand chevron, slide down from the
  top). Light and dark themes, fictional app names with simple icons of their
  own, a transparent Tella Motion overlay with spring motion, plus a chime per
  banner. Use when asked for notification pop-ups, push notifications, toasts
  or alert banners, iOS / iPhone, Mac or Android notifications, "payment
  received" / "new signup" / "new order" pings, or notifications stacking up
  over the footage.
metadata:
  title: Notification pop
  author: Tella
  category: Images
  image: og.jpg
  poster: gallery/ios-lock-screen.webp
  preview: gallery/ios-lock-screen.mp4
  prompt: When I say the first payment came in, then the signup, then the deploy, pop up a Mac notification for each in the top right, stacking.
---

# Notification pop

A burst of notifications over the footage, one per spoken event, drawn as the platform the viewer knows: an iPhone's lock-screen banners, a Mac's notification-centre banners or an Android phone's heads-up cards. Someone who uses that device every day should recognise it before reading a word. What stays fictional is the app: its name and icon are invented for the video (or are the user's own product), never a real app's name, icon, colours or logo.

It is the full version of the "Notifications" row in `tella-ui-interactions`. The banners move on springs, unlike the calm easing `tella-motion-design` asks for, because the systems they copy do; keep every other graphic in the video calm.

## Ask

Find the events the speaker names (a payment, a signup, an order, a deploy, a message, a milestone) and check where there is room: three Mac banners take about the top-right 760 × 460 px at 1080p, the iOS pile the top 350 px of a portrait frame, three Android cards about 780 px (560 px top right on 16:9). If the speaker's head is there, use another corner or platform, or ask. Then ask in one `ask_form`, prefilled:

- **Notifications**, one per line: `time · app · title · body`. Use the speaker's numbers and names exactly; invent nothing but "now". The app is the user's product or a made-up one.
- **Platform**: iPhone (default for portrait) · Mac (default for landscape) · Android.
- **Theme**: Light · Dark, preselected from the footage. Light reads best on Apple over dark or mid-tone footage; dark suits night footage and is Android's common look.
- **Position** (Mac and landscape only): top right (default) · top left · top centre.
- **Sound**: a chime on each (default) · cha-ching on money · none.

## The platforms

Sizes are for a 1080-wide portrait frame (iOS, Android) or a 1080-high landscape frame (Mac); scale with the frame. On a landscape frame the phone cards shrink to 78 % (a 780-wide card at 1080p). Margins are 40 px.

| | iOS | macOS | Android |
|---|---|---|---|
| Where | top centre, 120 px down | top right | top centre, 110 px down |
| Card | 1000 × 184, radius 58, opaque | 720 × 132, radius 30, 94 % opaque, gap 14 | 1000 × 212, radius 56, gap 16 |
| Icon | squircle 96 (radius 22.5 %), gradient | squircle 68, gradient | flat circle 96 |
| Text | Inter: title 37/600, body 35/400, grey "now" 29 top right | Inter: title 28/650, body 27/400, "now" 23 | Roboto: "App • now" 30, title 38/500, body 35, chevron pill 68 × 44 top right |
| Arrives | drops from above the frame, one soft overshoot | slides in from the right edge | slides down, no overshoot |
| Stacking | newest in front; older tuck behind at scale 0.94 / 0.88, peeking 24 / 44 px below, brightness 0.93 / 0.86, words faded | newest on top, older pushed down one slot | newest on top, older pushed down like the shade |
| Leaves | the pile lifts off the top | slides back out right, top first, ~0.07 s apart | slides up off the frame |

Themes, light / dark:
- **iOS**: card `#F4F4F7` / `#252528`; title `#000000` / `#FFFFFF`, body `#1C1C1E` / `#EBEBF0`, "now" `#6E6E73` / `#98989F`; hairline black 5 % / white 7 %; faint shadow (dy 8, blur 24).
- **macOS**: card `#F2F2F4` / `#2A2A2D` at 94 %, hairline black 10 % / white 14 %; title `#1D1D1F` / `#F5F5F7`, body `#2C2C2E` / `#DCDCE0`, "now" `#86868B` / `#98989D`; soft shadow (dy 12, blur 30).
- **Android**: tonal surface `#EEE8F4` / `#2B2930`, title `#1D1B20` / `#E6E0E9`, header and body `#49454F` / `#CAC4D0`, chevron pill `#DDD6E6` / `#3B3842`; light shadow (dy 4, blur 14), no hairline.

**Icons** are the fictional app's own: a white monogram (one or two letters) or a simple white glyph (check, person, bag, star, play, bell, bolt, box) on a colour. Apple gets a top-to-bottom gradient, Android the darker colour flat. Pairs that work: indigo `#7D8BFF→#4338CA`, violet `#C39BFF→#7C3AED`, coral `#FF9A7A→#E5482E`, amber `#FFD36B→#E08A00`, teal `#5FE3D3→#0E8C84`, sky `#7CC8FF→#1D72D8`, rose `#FF8DB8→#D02A6B`, graphite `#7C8592→#3A404B`. Avoid pairings that copy a real app: a white `$` on green, a speech bubble on green or blue, a play button on red, a bird on sky. A monogram on a colour is always safe.

## Words

- Title: the event or the sender, 1–5 words ("Payment received", "New order", a person's name for a message). About 30 characters fit on Mac, 34 on the phones.
- Body: one line, facts joined with `·` ("$49.00 from … · Pro plan", "web · main · 42s"). About 40 characters on Mac, 44 on the phones. Shorten rather than shrink the type.
- Apple banners show no app name when there is a title, so the icon carries the app; Android shows it in the header ("Pebblequay Shop • now").
- The same event said again ("three more orders came in") can repeat the title with new bodies: it reads as a flood.

## Timing

- Each banner starts moving 0.2 s before its word and has landed about 0.3 s later, as the word is said. Start the overlay at least 0.3 s before the first one.
- Keep banners at least 0.8 s apart; things said in one breath can be 0.8–1.1 s apart because they stay on screen. Under 0.6 s, merge them.
- On a list (Mac, Android), older banners start moving down 0.1 s before the new one lands, so the slot is clearing. On the iOS pile they tuck back 0.1 s after the new one starts dropping, once it covers them.
- Keep three on screen. A fourth on Mac or Android fades the oldest out over 0.25 s as it arrives.
- Leave when the thought ends, at least 1.5 s after the last banner; the overlay runs at least 0.75 s past that so the last one finishes leaving.
- One overlay per burst; a later burst is a new document (`duplicate_motion_document` and change the words).
- Sound: from the curated catalog (`list_library`, scope default), `notification-chime` (volume 0.4) at each banner's start, `success` for a milestone, `cha-ching` for a money milestone, `error` (0.35) for a failure. No more than one sound per 0.8 s.

## Building it in Tella Motion

One full-frame overlay document, placed with `depth: "front"` and no intro, outro or motion blur (the document animates itself). Each banner is a group: the card (a rounded rect with a drop shadow), its hairline (the same rect, stroked) and an inner content group (icon, glyph or monogram, title, body, time; on Android the header and the chevron pill). Draw every banner in its landed first slot and move the outer group with springs on its transform, so later banners paint on top and changing words is just editing a title.

Springs (mass 1, stiffness/damping): arrival 170/20 on Apple (one ~10 px overshoot), 210/29 on Android (critically damped); pushes and tucks 160/23; exit 120/22. One spring curve per transform property with a target per move, so a push that starts while a banner is still settling stays smooth. Fade each group in over the first 0.12 s of its arrival. On iOS put the group's origin at the card's centre so the tuck scales around it.

## Gotchas (all hit while building this)

- **Turn motion blur off** on the document (`setMotionBlur`) and on the placed overlay (`animation.motionBlur: false`): both are on by default, and mid-push the text smeared into vertical streaks.
- **Patch the spring transform last.** `setKeyframes` on `brightness` (and other style properties) rewrites the node's transform, wiping springs patched before it. Set opacity, brightness and content keys first.
- **No frosted glass.** A backdrop `blur` on a translucent shape inside a moving group blurred a full-width band of the video, the speaker's face included. Use solid colours matched to the system material. Keep the iOS pile opaque: a translucent front card shows the cards behind as a ghost rectangle.
- **Fade a tucked iOS banner's words as the next one starts dropping** (over ~0.18 s), not once it has landed, or its text shows in the strip that peeks out below.
- Snap spring targets to whole frames, with `timeDomain: "local"` on groups that start at 0.
- `addShape` only fills: the hairline is a `node.patch` with `paint.style: "stroke"`, and icon gradients go on `paint.source` as a linear gradient in canvas coordinates.
- A document keeps the canvas it was made with: if the video is resized, make a new one (an old 1920 × 1164 one put every banner too low).

## Check

- `get_motion_frame` when the stack is fullest and 0.6 s after each arrival: every line inside its card and on one line, "now" clear of the title, equal gaps, shadows not cut, nothing over the speaker. Would someone who uses this device daily take it for theirs? Look at the corner radius, icon shape and size, and where the time sits.
- One `get_filmstrip` over the burst at about 0.1 s steps: each banner lands with at most one small overshoot (none on Android), older ones move just before it lands (lists) or as it covers them (the pile), no smeared text mid-move, no words left on a tucked iOS banner, and the last one gone before the overlay ends.
- Report each banner with its time and the line it comes from, the platform, theme and position, and the sounds.

## Variations

- **The user's own app**: its name, its brand colour as the gradient and a monogram.
- **One quiet ping**: a single banner, leaving 2.5 s later.
- **Flood**: 4–6 "New order" banners 0.8 s apart on Mac or Android; the oldest fall away as new ones arrive.
- **Failure**: rose, a bell or `!`, and the `error` sound.
- **Mac on a portrait video**: keep the 720-wide banner, top right.
