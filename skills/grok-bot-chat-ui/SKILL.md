---
name: grok-bot-chat-ui
description: >-
  Build an animated re-creation of the Grok Bot desktop chat window as one editable 10-second Tella Motion clip:
  a light app window with a sidebar of bots, a bot pill header, chat bubbles, a typed prompt with a caret,
  Thinking and Exploring indicators, a reply with blue @mentions and a checklist, a "Needs your OK" approval
  card, and a cursor that clicks its button. The chosen bot's avatar has animated eyes that react to the chat
  (blink, dart on send, roll while working, happy arcs when done). Asks which bot to use, what the conversation
  is about and whose account name to show, then writes the conversation and builds it with a script. Live text
  and shapes in Inter. Use when asked for a Grok Bot chat UI, Grok Bot mockup or demo animation, an AI teammate
  chat animation in this look, or to redo this clip with another bot, topic or account.
metadata:
  title: Grok Bot chat UI
  author: Grant Shaddick
  category: UI & apps
  image: og.jpg
  poster: gallery/launch-bot.webp
  preview: gallery/launch-bot.mp4
  prompt: Make a Grok Bot chat clip where a Launch Bot catches an outdated spec and I approve the fix.
---

# Grok Bot chat UI

One Tella Motion clip (1920x1080, about 10 s) that re-creates the Grok Bot desktop app and plays one short exchange: the user types a request, the bot thinks, replies, asks for approval, and the user clicks approve. Built by `scripts/build_grok_bot_chat.py` from a small JSON config. Everything is live text and shapes, so it stays editable.

Files:
- `scripts/build_grok_bot_chat.py`: writes the batch of Tella Motion commands from a config.
- `scripts/cursor.json`: the cursor's traced vector outline (black arrow, rounded tail, white border). The script reads it; keep it next to the script.
- `example.json`: a complete config (the original Launch Bot conversation). Copy its shape.
- `references/reference.mp4`: the finished original, 10 s. Pull frames from it with ffmpeg to see what the result should look like.

## 1. Ask

Ask with one `ask_form` (skip any field the request already answers):

1. **Which bot** (it is the selected, animated one): a text field for the bot's name (e.g. "Launch Bot"), and a choice for its colour from the Grok Bot palette: Teal `#54B9A6`, Pink `#E8247A`, Blue `#3C82F6`, Purple `#885CF5`, Indigo `#6464EF`, Orange `#ED712E`, Yellow `#F19D38`, Green `#5BC67A`, Red `#EA4045`, Brown `#97683D`.
2. **Topic of the conversation**: a text field, e.g. "fixing an outdated spec before a product launch".
3. **Account name**: a text field for whose account the app is signed in to (shown bottom-left with their initials).

## 2. Write the conversation

From the topic, write the config. Keep it short, lowercase and casual for the user, plain and specific for the bot, as in `example.json`. Never use real company or customer names the user didn't give.

| Field | What it is | Limit |
| --- | --- | --- |
| `botName`, `botColor`, `accountName` | from the answers | bot name at most ~18 characters |
| `opener` | the bot's message already on screen: it noticed something | at most ~95 characters (2 lines) |
| `prompt` | what the user types | at most 34 characters, or the clip runs past 10 s |
| `reply` | the bot's answer; `@Name` words are drawn blue | 1 line, at most ~55 characters |
| `checks` | 0 to 2 lines of `["Bold label", "what was done"]`, drawn as `✓ Label → what was done` | each under ~45 characters |
| `card` | approval card: `label` ("Needs your OK"), `title`, `sub`, `primary` button, `secondary` button, `done` (what replaces the buttons after the click, e.g. "Scheduled") | title under ~45 characters |
| `timestamp` | e.g. "Friday 7:48 AM" | |
| `tiles` | the two other bots beside the chosen one: `[name, colour]` | names of one or two words |
| `rows` | three sidebar chats: `[bot name, preview line, colour]` | fit the topic; previews are truncated to fit |
| `userBubbleColor` | optional; black `#111110` by default. The real app tints the user's bubbles with the bot's colour: use `botColor` here if the user asks for that | |

Give the other bots colours different from the chosen bot's. Show the user the conversation in a few lines before building only if they asked to approve it; otherwise build.

## 3. Build

```bash
cd $HOME/.agents/skills/grok-bot-chat-ui
python3 scripts/build_grok_bot_chat.py /workspace/grok/config.json --plan     # prints timings and "duration"
```

The script needs Pillow and downloads Inter once to measure text. If it exits with "Conversation is too tall", shorten the opener or reply or drop a checklist line.

1. `create_clip` with `type: "motion"`, a name, and `duration` = the printed `duration` (10 unless the prompt is long). To use it as an overlay or b-roll instead, `create_motion_document` and place it with `add_overlay` or `add_layout`.
2. `python3 scripts/build_grok_bot_chat.py config.json /workspace/grok/cmds.json`, then `apply_motion_editor_commands` with `commandsFile` = that path on the new, empty document. It is one batch (about 230 commands).

To rebuild an existing one with new content, put `delete` commands for the nodes `window`, `cursor` and `bg` in front of the batch and apply it to the same document.

## 4. What the clip does

Times for a 32-character prompt; the script prints the real ones.

- 0:00 the window fades and scales in with the opener already there. The chosen bot blinks at 1.5 s.
- 0:00.8 the prompt types at 15 characters a second with a caret; the mic button becomes a send arrow. On send the button presses, the field clears and the user bubble rises in.
- The bot's eyes dart up and right, the avatar hops, then three pulsing dots with "Thinking" (eyes roll up into flat dashes) and a pulsing ring with "Exploring" (eyes grow and roll around).
- The reply, the checklist and the approval card rise in 0.45 s apart; the eyes blink back to neutral and glance toward the card.
- The cursor comes in from the bottom right, hovers the primary button (it lightens), clicks (button and cursor press), the buttons fade to a check and the `done` label, and the bot's eyes turn into happy arcs with a small bounce. It holds about 1.7 s.

## 5. Rules learned building it

- **Caret and typing**: the typewriter text animation reveals one visible glyph per step and skips spaces. Key the caret per visible glyph with the same stagger, or the text runs ahead of the caret. The script does this.
- **Vertical centring**: Inter sits low in its line box. Text in message bubbles is lifted 13% of its font size, and text in buttons, pills and the input 9%, so it looks centred. Keep these nudges when adding text.
- **Strokes are hairlines**: 0.75 px (window, sidebar divider, card, input, secondary button, icon buttons) and 0.6 px (header pill, Share). A stroke is a slightly larger rounded rectangle behind the fill. Don't thicken them.
- **Shadows are light**: the approval card's is barely there (y 3, blur 14, 2.5%); the window's is y 28, blur 70, 12%; the cursor's y 4, blur 10, 30%.
- **Cursor**: use the traced outline in `cursor.json` as is (tip at 0,0, about 58 px tall). Don't redraw it by eye.
- **Eyes**: only the chosen bot's sidebar avatar animates. A blink is the eye pills turning edge-on (`rotateX` to 86 and back in 0.18 s). Poses are x, y, rotation and scale per eye; keep the eyes inside the body.
- **Scaling a group about a point** (send button, avatar, cursor): set the group's `anchorX`/`anchorY` to that point first, or it scales about the canvas centre and jumps.
- The app's own typeface isn't available; Inter is the stand-in. Say so once in the report.

## 6. Check and report

`get_filmstrip` on the document at about 0.3 s, mid-typing, just after send, Thinking, Exploring, after the card lands, the click, and the end. Check: the caret sits right after the last typed letter, nothing overlaps the input bar, the user bubble fits, the cursor tip is on the primary button at the click, and the eyes are inside the avatar. Then report in a few lines what happens when, and offer to change wording, colours or pace.
