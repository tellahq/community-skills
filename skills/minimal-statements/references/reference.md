# Reference

## Source of the look
A product promo (the attached reference "multiple.mp4"):
- ~0:04-0:06 on flat light grey, `{ in }` -> `{ in one }` -> `{ in one place }` builds word by word in a thin grotesk, the braces pushing outward as words arrive, four tiny black square dots marking the corners of a box that grows with the text.
- ~0:06-0:07 `{ intro ducing }`: the word splits, the halves turn maroon/pink, faint arrows sit at the sides and a small image flickers in the gap before the word closes.

## Prompt that produced them
Louise, with the promo attached: "implement all of the different motion graphics featured in this video, but apply to the content of my video. if you need images, find relevant ones in my mind, pinterest or ar.ena connection". Of everything built she kept the statement cards and the builder image inset ("add the builder image one as an outcome + prompt to the minimal statements skill").

## Approved outcomes
Video "multiple cool motion graphics" (https://www.tella.tv/video/vid_cmvi625kg00r902nyarhofrqp/view), a talking-head explainer on GitHub for marketers. All full-frame b-roll with a hard cut in and out.

### Statement cards
| Time | Label | Statement | Spoken line |
|---|---|---|---|
| 5:12.3 (4.1 s) | REBUTTAL 02 | { networking is more impactful } | "The second rebuttal is that networking was way more impactful on hireability" |
| 6:31.6 (4.4 s) | REBUTTAL 03 | { engineers will think it's lame } | "Number three rebuttal. Engineers will think your GitHub profile is lame" |
| 7:50.4 (2.9 s) | REBUTTAL 04 | { my work is private } | "...is all of my work is in private repos" |
| 9:16.6 (3.4 s) | REBUTTAL 05 | { this feels intimidating } | "The last counter was, 'This feels intimidating.'" |

Spec for 5:12: `{"label":"REBUTTAL 02","label_t":0.06,"words":["networking","is","more","impactful"],"times":[1.27,1.87,2.19,2.33],"dur":4.1}`
Spec for 6:31: `{"label":"REBUTTAL 03","label_t":0.09,"words":["engineers","will","think","it's","lame"],"times":[1.39,2.01,2.17,2.51,3.49],"dur":4.4}`

### Image inset: { build[image]er }, 2:49.3-2:57.6 (8.3 s)
Spoken: "And whether you do that by making videos, by writing, by making websites, by making hardware, or by writing code using AI, that makes you a builder." Opens on "videos", one image per item, closes on "that makes you a builder". Images from her mymind and Pinterest: an animation studio being filmed (videos), Clarice Lispector writing at a desk (writing), a retro Windows paint window (websites), Alan Zenreich's hand reaching out of a computer (hardware), a terminal running a skills CLI (code).
Spec: `{"left":"build","right":"er","dur":8.3,"open_t":0.45,"close_t":7.1,"images":[{"uri":"https://ucarecdn.com/f9cfd70a-ce79-4302-a2b5-eb565ddd142e/","w":400,"h":300,"caption":"videos","t":0.45},{"uri":"https://ucarecdn.com/62ed146a-d516-4a1a-8f4c-f391f4a89fd5/","w":1370,"h":1404,"caption":"writing","t":1.54},{"uri":"https://ucarecdn.com/66dfb676-ac85-4608-98cc-a7925e36f016/","w":736,"h":883,"caption":"websites","t":2.72},{"uri":"https://ucarecdn.com/25e6b66f-e476-46df-9305-9ff43bbc5ac7/","w":1200,"h":1368,"caption":"hardware","t":3.84},{"uri":"https://ucarecdn.com/70bfa200-874e-4efc-816b-12e1a64b32b8/","w":2582,"h":1704,"caption":"code","t":5.56}]}`

Geometry: text 64 px centred on y 545; statement label on y 425; dots 70 px outside the text box, +-95 px (statement) or +-110 px (inset) vertically; word gap = one space x 1.15; inset slot 170x110 with 22 px gaps, captions 24 px on y 655, arrows 40 px grey 120/50 px outside the braces.
