# Reference

## Source of the look
A product promo (the attached reference "multiple.mp4", ~0:19-0:25): on flat light grey, fashion portraits appear one at a time, then several cards stand in perspective and cascade from small to large left to right, and the words "you" and "create" frame the stack on either side.

## Prompt that produced them
Louise, with the promo attached: "implement all of the different motion graphics featured in this video, but apply to the content of my video. if you need images, find relevant ones in my mind, pinterest or ar.ena connection". Of everything built she kept the two photo stacks and asked for "various versions of speed of the photo stack at 08:54 and 09:04", which became the `slow`, `medium`, `fast` and `word` speeds.

Example asks once the skill is loaded:
- "Add a photo stack where I list my hobbies, with images from my Pinterest and mymind."
- "Put a photo fan next to me when I talk about outfits, fast."
- "Turn 'reading, family, sports, relationships' into a cascade framed by 'you … build'."

## Approved examples (Louise liked these; she wants speed versions)
Video "multiple cool motion graphics" (https://www.tella.tv/video/vid_cmvi625kg00r902nyarhofrqp/view), a talking-head explainer on GitHub for marketers.

Times below are on the editor's clip. In the published video, after earlier cuts, the fan plays at 8:53.6 and the cascade at 9:01.9 (`gallery/fan.mp4`, `gallery/cascade.mp4`).

**Fan, 8:55.6-9:00.7** (overlay on the right, over the door, presenter centre-left), on "I also like to dabble with anything fashion-related, wardrobe-related, to help me with my outfit stress." Five Pinterest outfit photos (street-style women, full-length), pill label "fashion & wardrobe". Medium speed: cards leave the pile 0.14 s apart, 0.6 s each, rotateY 0->32, scale 0.7->1, then drift 24 px left and fade out in the last 0.3 s.

**Cascade, 9:03.9-9:11.6** (full-frame b-roll), on "whether it's reading, your family life, sports, relationships. Anything that interests you beyond work, just build stuff around that". Pinterest images: woman reading (reading), family portrait at home (family life), Nike basketball poster (sports), couple on a bicycle (relationships). Each lands on its word (0.42, 1.42, 2.12, 2.68 s), then "you" on "you" (4.78 s) and "build" on "build" (6.24 s).
Spec: `{"variant":"cascade","speed":"word","dur":7.7,"images":[{"uri":"https://ucarecdn.com/4b399997-edf9-4e90-8ae3-41e226ac3769/","w":1200,"h":1053,"t":0.42,"name":"reading"},{"uri":"https://ucarecdn.com/b5b6a449-e81c-47f9-92e2-1196df87c773/","w":1024,"h":1280,"t":1.42,"name":"family"},{"uri":"https://ucarecdn.com/ef657137-374d-4b72-ac22-8252c761eda4/","w":1200,"h":1661,"t":2.12,"name":"sports"},{"uri":"https://ucarecdn.com/dd0a71bf-268b-41aa-a733-e43796a7a0cf/","w":474,"h":585,"t":2.68,"name":"relationships"}],"left_word":{"text":"you","t":4.78},"right_word":{"text":"build","t":6.24}}`
