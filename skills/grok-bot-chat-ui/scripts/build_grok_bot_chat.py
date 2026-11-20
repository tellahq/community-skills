#!/usr/bin/env python3
"""Build the Grok Bot chat UI as a batch of Tella Motion commands.

  python3 build_grok_bot_chat.py config.json out.json            # writes the batch, prints timings
  python3 build_grok_bot_chat.py config.json --plan              # prints timings + clip duration only

The batch goes to apply_motion_editor_commands as commandsFile, on an EMPTY 1920x1080 document
whose duration is the printed "duration". Everything is live text and shapes in Inter.
"""
import json, os, re, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, '_inter')
FONTS = {400: 'Inter-Regular.ttf', 500: 'Inter-Medium.ttf', 600: 'Inter-SemiBold.ttf'}

def ensure_fonts():
    if all(os.path.exists(os.path.join(FONT_DIR, f)) for f in FONTS.values()):
        return
    os.makedirs(FONT_DIR, exist_ok=True)
    z = os.path.join(FONT_DIR, 'inter.zip')
    urllib.request.urlretrieve('https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip', z)
    with zipfile.ZipFile(z) as zf:
        for f in FONTS.values():
            with zf.open('extras/ttf/' + f) as src, open(os.path.join(FONT_DIR, f), 'wb') as dst:
                dst.write(src.read())

ensure_fonts()
from PIL import ImageFont
_fc = {}
def tw(s, size, weight=400):
    k = (size, weight)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[weight]), size)
    return _fc[k].getlength(s)

def wrap(s, size, maxw, weight=400):
    lines, cur = [], ''
    for w in s.split(' '):
        t = (cur + ' ' + w).strip()
        if tw(t, size, weight) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

# ---------------- config ----------------
cfg = json.load(open(sys.argv[1]))
BOT = cfg['botName']
BOTC = cfg.get('botColor', '#54B9A6')
UC = cfg.get('userBubbleColor', '#111110')
ACCOUNT = cfg['accountName']
OPENER = cfg['opener']
PROMPT = cfg['prompt']
REPLY = cfg['reply']                       # @mentions are drawn blue
CHECKS = cfg.get('checks', [])             # [[bold label, rest], ...] 0-3 lines
CARD = cfg['card']                         # {label,title,sub,primary,secondary,done}
TIMESTAMP = cfg.get('timestamp', 'Friday 7:48 AM')
TILES = cfg.get('tiles', [['Inbox Manager', '#6464EF'], ['Mktg Data', '#885CF5']])
ROWS = cfg.get('rows', [['New Hires', '3 intros drafted in your voice', '#3C82F6'],
                        ['Expense Manager', 'Report filed. 9 receipts, not yet approved', '#ED712E'],
                        ['Chief of Staff', 'Rescheduled your flight to Thursday', '#5BC67A']])
STATUS = cfg.get('status', ['Thinking', 'Exploring'])
MENTION = '#2F6FEB'

# ---------------- timing ----------------
TYPE0, CPS = 0.8, 15.0
r2 = lambda v: round(v, 2)
SEND = r2(TYPE0 + len(PROMPT) / CPS + 0.25)
UB = r2(SEND + 0.06)
TH0 = r2(UB + 0.35); TH1 = r2(TH0 + 1.1); EX1 = r2(TH1 + 0.9)
R1 = EX1; R2 = r2(R1 + 0.45); R3 = r2(R2 + 0.45) if CHECKS else R2
CUR0 = r2(R3 + 0.45); CUR1 = r2(CUR0 + 1.0); CLICK = r2(CUR1 + 0.15); SCHED = r2(CLICK + 0.2)
END = float(cfg.get('duration') or max(10.0, r2(SCHED + 1.7)))
plan = dict(duration=END, typing=[TYPE0, SEND], userBubble=UB, thinking=[TH0, TH1], exploring=[TH1, EX1],
            reply=R1, checks=R2 if CHECKS else None, card=R3, cursor=[CUR0, CUR1], click=CLICK, done=SCHED)
if '--plan' in sys.argv:
    print(json.dumps(plan)); sys.exit(0)

# ---------------- helpers ----------------
C = []
def rect(i, x, y, w, h, col, r=0, s=0, d=None):
    C.append({'type': 'addShape', 'nodeId': i, 'start': s, 'duration': d if d else END - s, 'shape': 'rect',
              'box': {'x': x, 'y': y, 'width': w, 'height': h}, 'color': col, 'radius': r}); return i
def circ(i, cx, cy, dd, col, s=0, d=None):
    C.append({'type': 'addShape', 'nodeId': i, 'start': s, 'duration': d if d else END - s, 'shape': 'circle',
              'box': {'x': cx - dd / 2, 'y': cy - dd / 2, 'width': dd, 'height': dd}, 'color': col}); return i
def text(i, s_, x, y, w, size, col, weight=400, align='left', lh=1.42, s=0, d=None, nudge=0.0):
    # nudge: fraction of the font size the text is lifted so it looks vertically centred in its container
    C.append({'type': 'addTitle', 'nodeId': i, 'start': s, 'duration': d if d else END - s, 'text': s_,
              'box': {'x': round(x, 2), 'y': round(y - round(size * nudge, 1), 2), 'width': round(w, 2)},
              'font': 'inter', 'fontSize': size, 'color': col, 'align': align, 'weight': weight, 'lineHeight': lh}); return i
def path(i, d_, col, paint='stroke', sw=2.4, s=0, d=None, parent=None):
    c = {'type': 'addPath', 'nodeId': i, 'start': s, 'duration': d if d else END - s, 'path': d_, 'color': col,
         'paint': paint, 'strokeWidth': sw, 'cap': 'round', 'join': 'round'}
    C.append(c); return i
def group(i, nodes, name):
    C.append({'type': 'group', 'nodes': nodes, 'nodeId': i, 'name': name}); return i
def keys(node, prop, ks):
    out = []
    for a, v, e in sorted(ks, key=lambda z: z[0]):
        a = round(a, 3)
        if out and abs(out[-1]['at'] - a) < 0.002: continue
        k = {'at': a, 'value': v}
        if e: k['easing'] = e
        out.append(k)
    C.append({'type': 'setKeyframes', 'node': node, 'property': prop, 'keys': out})
def setp(node, prop, val):
    C.append({'type': 'setProperty', 'node': node, 'property': prop, 'value': val})
def enter(node, t, dy=14, dur=0.32):
    keys(node, 'opacity', [(t, 0, 'easeOutCubic'), (t + dur, 1, None)])
    keys(node, 'y', [(t, dy, 'easeOutCubic'), (t + dur, 0, None)])
def bordered(i, x, y, w, h, r, o, border, fill, s=0):
    """A filled rounded rect with a hairline stroke: a slightly larger rect behind it."""
    return [rect(i + '.border', x - o, y - o, w + 2 * o, h + 2 * o, border, r + o, s=s), rect(i + '.bg', x, y, w, h, fill, r, s=s)]

# ---------------- geometry (1920x1080) ----------------
X0, Y0, W, H = 110, 56, 1700, 968
SB = 430
CX0 = X0 + SB; CX1 = X0 + W - 24; CXC = (CX0 + CX1) / 2
MX0 = CX0 + 44; MX1 = CX1 - 40
FS, LH = 27, 1.42; LN = FS * LH; PX, PY, BR = 24, 15, 24
BOTBG, INK, GREY = '#F2F2F0', '#111110', '#9E9E9C'
HAIR, HAIR2 = 0.75, 0.6            # stroke widths
MSG, UI = 0.13, 0.09               # text nudges: message bubbles / buttons, pills, inputs

C.append({'type': 'addShape', 'nodeId': 'bg', 'start': 0, 'duration': END, 'shape': 'fill', 'color': '#EBEBE9'})
win = []
win.append(rect('win.border', X0 - HAIR, Y0 - HAIR, W + 2 * HAIR, H + 2 * HAIR, '#DADAD8', 28 + HAIR))
win.append(rect('win.fill', X0, Y0, W, H, '#FCFCFB', 28))
win.append(rect('sidebar.border', X0 + SB - HAIR / 2, Y0, HAIR, H, '#E7E7E5'))
for k, col in enumerate(['#FF5F57', '#FEBC2E', '#28C840']):
    win.append(circ(f'tl.{k}', X0 + 36 + k * 26, Y0 + 38, 17, col))

def iconbtn(i, cx, cy, kind, ring=True, fill='#FFFFFF'):
    ns = []
    if ring: ns.append(circ(i + '.ring', cx, cy, 45 + 2 * HAIR, '#E4E4E2'))
    ns.append(circ(i + '.bg', cx, cy, 45, fill))
    if kind == 'search':
        ns.append(path(i + '.ic', f'M {cx-3} {cy-11} A 8 8 0 1 0 {cx-3} {cy+5} A 8 8 0 1 0 {cx-3} {cy-11} Z M {cx+3} {cy+3} L {cx+10} {cy+10}', '#2A2A28'))
    else:
        ns.append(path(i + '.ic', f'M {cx-9} {cy} L {cx+9} {cy} M {cx} {cy-9} L {cx} {cy+9}', '#2A2A28'))
    return group(i, ns, i)
win.append(iconbtn('btn.search', X0 + 330, Y0 + 42, 'search'))
win.append(iconbtn('btn.plus', X0 + 388, Y0 + 42, 'plus'))

def avatar(i, cx, cy, d, col, style='ticks', blob=False, extra=None):
    ns = []
    if blob: ns.append(rect(i + '.body', cx - d * 0.47, cy - d * 0.45, d * 0.94, d * 0.9, col, d * 0.36))
    else: ns.append(circ(i + '.body', cx, cy, d, col))
    if style == 'pills':
        ew, eh = d * 0.13, d * 0.29
        ns.append(rect(i + '.e1', cx - d * 0.15 - ew / 2, cy - eh / 2 + d * 0.01, ew, eh, '#FFFFFF', ew / 2))
        ns.append(rect(i + '.e2', cx + d * 0.15 - ew / 2, cy - eh / 2 + d * 0.01, ew, eh, '#FFFFFF', ew / 2))
    else:
        ew, eh = d * 0.11, d * 0.24
        for n, (ox, oy) in enumerate([(-0.04, -0.12), (0.15, -0.16)]):
            ns.append(rect(f'{i}.e{n+1}', cx + ox * d - ew / 2, cy + oy * d - eh / 2, ew, eh, '#FFFFFF', ew / 2))
    if extra: ns += extra()
    group(i, ns, i)
    if style != 'pills':
        setp(f'{i}.e1', 'rotation', -22); setp(f'{i}.e2', 'rotation', -22)
    if blob: setp(i + '.body', 'rotation', -12)
    setp(i, 'anchorX', cx); setp(i, 'anchorY', cy)
    return i

def two_lines(name):
    w = name.split(' ')
    return name if len(w) < 2 or tw(name, 20) <= 104 else ' '.join(w[:-1]) + '\n' + w[-1]

# --- sidebar: bot tiles (the chosen bot is the selected, animated one) ---
TY = Y0 + 92
AVD = 80; ACX = X0 + 22 + 59; ACY = TY + 52
win.append(rect('tile.sel', X0 + 22, TY, 118, 158, '#EFEFED', 20))
# happy-eye arcs for the chosen bot, shown after the click (made after the eyes so they draw on top of the body)
def happy_arcs():
    r = AVD * 0.094; arcs = []
    for k, (ax, ay) in enumerate([(ACX - AVD * 0.1625, ACY - AVD * 0.1125), (ACX + AVD * 0.1375, ACY - AVD * 0.1375)]):
        arcs.append(path(f'av.bot.h{k+1}', f'M {ax-r} {ay+4} A {r} {r} 0 0 1 {ax+r} {ay+4}', '#FFFFFF', 'stroke', AVD * 0.081, s=r2(SCHED + 0.07)))
    return arcs
win.append(avatar('av.bot', ACX, ACY, AVD, BOTC, 'pills', extra=happy_arcs))
win.append(text('lab.bot', two_lines(BOT), X0 + 22 - 6, TY + 102, 130, 20, '#2A2A28', 400, 'center', 1.25))
for k, (nm, col) in enumerate(TILES[:2]):
    tx = X0 + 22 + (k + 1) * 126
    win.append(avatar(f'av.tile{k}', tx + 59, TY + 52, 80, col, 'ticks', blob=(k == 0)))
    win.append(text(f'lab.tile{k}', two_lines(nm), tx - 6, TY + 102, 130, 20, '#2A2A28', 400, 'center', 1.25))
RY = Y0 + 292
for k, (nm, pv, col) in enumerate(ROWS[:5]):
    y = RY + k * 82
    win.append(avatar(f'av.row{k}', X0 + 52, y + 26, 50, col, 'ticks'))
    win.append(text(f'nm.row{k}', nm, X0 + 92, y - 2, 320, 23, INK, 400, 'left', 1.3))
    s = pv
    while tw(s, 19) > 300: s = s[:-2].rstrip() + '…'
    win.append(text(f'pv.row{k}', s, X0 + 92, y + 28, 320, 19, '#8C8C8A', 400, 'left', 1.3))
# --- account ---
ini = ''.join(p[0] for p in ACCOUNT.split()[:2]).upper()
win.append(circ('acct.av', X0 + 46, Y0 + H - 48, 40, '#EFEFED'))
win.append(text('acct.ini', ini, X0 + 26, Y0 + H - 48 - 10, 40, 14, '#7A7A78', 500, 'center', 1.4, nudge=UI))
win.append(text('acct.nm', ACCOUNT, X0 + 80, Y0 + H - 48 - 15, 330, 21, INK, 400, 'left', 1.4, nudge=UI))

# --- header ---
hs = 22; hw = 16 + 30 + 10 + tw(BOT, hs) + 20; hh = 50; hx = CXC - hw / 2; hy = Y0 + 16
win += bordered('hdr', hx, hy, hw, hh, hh / 2, HAIR2, '#E6E6E4', '#FFFFFF')
win.append(avatar('hdr.av', hx + 16 + 15, hy + hh / 2, 30, BOTC, 'pills'))
win.append(text('hdr.nm', BOT, hx + 16 + 30 + 10, hy + hh / 2 - hs * 1.3 / 2, 500, hs, INK, 400, 'left', 1.3, nudge=UI))
sw_ = tw('Share', 20) + 40
win += bordered('share', CX1 - sw_, hy + 2, sw_, 46, 23, HAIR2, '#E6E6E4', '#FFFFFF')
win.append(text('share.t', 'Share', CX1 - sw_, hy + 2 + 23 - 13, sw_, 20, INK, 400, 'center', 1.3, nudge=UI))
win.append(text('ts', TIMESTAMP, CXC - 200, Y0 + 92, 400, 19, GREY, 400, 'center', 1.3))

# --- messages ---
BMAX = 780
y = Y0 + 136
def bot_bubble(i, lines, top, s):
    """lines: list of lines, each a list of (text, colour|None, weight) runs."""
    width = max(sum(tw(t, FS, wt) for t, _, wt in l) for l in lines) + 2 * PX
    h = len(lines) * LN + 2 * PY
    ns = [rect(i + '.bg', MX0, top, width, h, BOTBG, BR, s=s)]
    for li, segs in enumerate(lines):
        x = MX0 + PX
        for si, (t, col, wt) in enumerate(segs):
            if t.strip():
                ns.append(text(f'{i}.l{li}s{si}', t, x, top + PY + li * LN, tw(t, FS, wt) + 40, FS, col or INK, wt, 'left', LH, s=s, nudge=MSG))
            x += tw(t, FS, wt)
    return ns, h
def rich_lines(s):
    """Wrap text at BMAX; words starting with @ become blue runs."""
    lines, cur, curw = [], [], 0.0
    for w in s.split(' '):
        piece = (' ' if cur else '') + w
        if cur and curw + tw(piece, FS) > BMAX:
            lines.append(cur); cur, curw, piece = [], 0.0, w
        m = re.match(r'^(\s?)(@[\w-]+)(.*)$', piece)
        runs = [(m.group(1), None), (m.group(2), MENTION), (m.group(3), None)] if m else [(piece, None)]
        for t, col in runs:
            if not t: continue
            if cur and cur[-1][1] == col: cur[-1] = (cur[-1][0] + t, col, 400)
            else: cur.append((t, col, 400))
            curw += tw(t, FS)
    lines.append(cur)
    return lines

ns, oh = bot_bubble('msg.opener', rich_lines(OPENER), y, 0)
win.append(group('msg.opener', ns, 'Opener message')); y += oh + 22
uw = tw(PROMPT, FS) + 2 * PX + 4; uh = LN + 2 * PY
win.append(group('msg.user', [rect('msg.user.bg', MX1 - uw, y, uw, uh, UC, uh / 2, s=UB),
                              text('msg.user.t', PROMPT, MX1 - uw + PX, y + PY, uw, FS, '#FFFFFF', 400, 'left', LH, s=UB, nudge=MSG)], 'User message'))
y += uh + 22
IY = y + 8
dots = [circ(f'think.d{k}', MX0 + 12 + k * 22, IY + 16, 14, BOTC, s=TH0, d=TH1 - TH0) for k in range(3)]
win.append(group('think', dots + [text('think.t', STATUS[0], MX0 + 86, IY + 16 - 22 * 1.3 / 2, 400, 22, '#A3A3A1', 400, 'left', 1.3, s=TH0, d=TH1 - TH0)], 'Thinking'))
win.append(group('explore', [circ('expl.ring', MX0 + 30, IY + 16, 40, BOTC, s=TH1, d=EX1 - TH1), circ('expl.inner', MX0 + 30, IY + 16, 38.5, '#FCFCFB', s=TH1, d=EX1 - TH1),
                             circ('expl.pulse', MX0 + 30, IY + 16, 26, BOTC, s=TH1, d=EX1 - TH1), circ('expl.dot', MX0 + 30, IY + 16, 14, BOTC, s=TH1, d=EX1 - TH1),
                             text('expl.t', STATUS[1], MX0 + 86, IY + 16 - 22 * 1.3 / 2, 400, 22, '#A3A3A1', 400, 'left', 1.3, s=TH1, d=EX1 - TH1)], 'Exploring'))
setp('expl.ring', 'opacity', 0.22)
ns, rh = bot_bubble('msg.reply', rich_lines(REPLY), y, R1)
win.append(group('msg.reply', ns, 'Reply')); y += rh + 12
if CHECKS:
    ns, chh = bot_bubble('msg.checks', [[('✓ ', None, 400), (a, None, 600), (' → ' + b, None, 400)] for a, b in CHECKS[:3]], y, R2)
    win.append(group('msg.checks', ns, 'Checklist')); y += chh + 16
else:
    y += 4
# --- approval card ---
CW = 720; CY = y; BH = 54
b1w = tw(CARD['primary'], 23, 500) + 48; b2w = tw(CARD['secondary'], 23) + 48
CH = 24 + 30 + 40 + 38 + 22 + BH + 26
BY = CY + CH - 26 - BH
IH = 74; IYB = Y0 + H - IH - 26
if CY + CH > IYB - 24:
    sys.exit(f'Conversation is too tall by {CY + CH - (IYB - 24):.0f}px: shorten the opener or reply, or drop a checklist line.')
card = bordered('card', MX0, CY, CW, CH, 24, HAIR, '#E2E2E0', '#FFFFFF', s=R3) + [
    text('card.label', CARD.get('label', 'Needs your OK'), MX0 + 26, CY + 22, 500, 20, '#A6A6A4', 400, 'left', 1.3, s=R3),
    text('card.title', CARD['title'], MX0 + 26, CY + 56, 660, 26, INK, 500, 'left', 1.3, s=R3),
    text('card.sub', CARD.get('sub', ''), MX0 + 26, CY + 98, 660, 21, '#A6A6A4', 400, 'left', 1.3, s=R3)]
b1 = group('card.btn1', [rect('card.btn1.bg', MX0 + 26, BY, b1w, BH, '#1A1A19', BH / 2, s=R3),
                         text('card.btn1.t', CARD['primary'], MX0 + 26, BY + BH / 2 - 23 * 1.3 / 2, b1w, 23, '#FFFFFF', 500, 'center', 1.3, s=R3, nudge=UI)], 'Primary button')
b2x = MX0 + 26 + b1w + 14
b2 = group('card.btn2', bordered('card.btn2', b2x, BY, b2w, BH, BH / 2, HAIR, '#DCDCDA', '#FFFFFF', s=R3) +
           [text('card.btn2.t', CARD['secondary'], b2x, BY + BH / 2 - 23 * 1.3 / 2, b2w, 23, INK, 400, 'center', 1.3, s=R3, nudge=UI)], 'Secondary button')
btns = group('card.btns', [b1, b2], 'Card buttons')
done = group('card.done', [circ('card.done.c', MX0 + 26 + 17, BY + BH / 2, 34, BOTC, s=SCHED),
                           path('card.done.ck', f'M {MX0+26+9.5} {BY+BH/2+0.5} L {MX0+26+15} {BY+BH/2+6} L {MX0+26+25} {BY+BH/2-5.5}', '#FFFFFF', 'stroke', 3, s=SCHED),
                           text('card.done.t', CARD.get('done', 'Done'), MX0 + 26 + 46, BY + BH / 2 - 23 * 1.3 / 2, 500, 23, INK, 500, 'left', 1.3, s=SCHED, nudge=UI)], 'Done state')
win.append(group('card', card + [btns, done], 'Approval card'))

# --- input bar ---
win += bordered('in', MX0, IYB, MX1 - MX0, IH, IH / 2, HAIR, '#E0E0DE', '#FFFFFF')
win.append(iconbtn('in.plus', MX0 + 38, IYB + IH / 2, 'plus', ring=False, fill='#F2F2F0'))
win.append(text('in.ph', 'Message ' + BOT, MX0 + 76, IYB + IH / 2 - 25 * 1.3 / 2, 800, 25, '#A8A8A6', 400, 'left', 1.3, nudge=UI))
win.append(text('in.typed', PROMPT, MX0 + 76, IYB + IH / 2 - 25 * 1.3 / 2, 950, 25, INK, 400, 'left', 1.3, s=TYPE0, d=SEND - TYPE0, nudge=UI))
win.append(rect('in.caret', MX0 + 76, IYB + IH / 2 - 16, 2.5, 32, INK, 1, s=TYPE0, d=SEND - TYPE0))
SBX = MX1 - 14 - 25; SBY = IYB + IH / 2
win.append(group('send', [circ('send.bg', SBX, SBY, 50, '#111110'),
                          rect('send.mic.body', SBX - 5, SBY - 12, 10, 16, '#FFFFFF', 5),
                          path('send.mic.arc', f'M {SBX-8.5} {SBY-1} A 8.5 8.5 0 0 0 {SBX+8.5} {SBY-1} M {SBX} {SBY+7.5} L {SBX} {SBY+12}', '#FFFFFF', 'stroke', 2.2),
                          path('send.arrow', f'M {SBX} {SBY+10} L {SBX} {SBY-10} M {SBX-8} {SBY-2} L {SBX} {SBY-10} L {SBX+8} {SBY-2}', '#FFFFFF', 'stroke', 2.8)], 'Send button'))
setp('send', 'anchorX', SBX); setp('send', 'anchorY', SBY)

# --- cursor (traced arrow with white outline, tip at 0,0) ---
cur = json.load(open(os.path.join(HERE, 'cursor.json')))
group('cursor', [path('cursor.outline', cur['outline'], '#FFFFFF', 'fill', 0, s=r2(CUR0 - 0.01)),
                 path('cursor.fill', cur['fill'], '#000000', 'fill', 0, s=r2(CUR0 - 0.01))], 'Cursor')
setp('cursor', 'anchorX', 12); setp('cursor', 'anchorY', 18)
group('window', win, 'Grok Bot window')

# ---------------- animation ----------------
keys('window', 'opacity', [(0, 0, 'easeOutCubic'), (0.5, 1, None)])
keys('window', 'scale', [(0, 0.965, 'easeOutCubic'), (0.55, 1, None)])
for n, sy, sb, so in (('win.border', 28, 70, 0.12), ('hdr.border', 2, 8, 0.05), ('card.border', 3, 14, 0.025), ('cursor', 4, 10, 0.3)):
    setp(n, 'shadowY', sy); setp(n, 'shadowBlur', sb); setp(n, 'shadowOpacity', so)
keys('in.ph', 'opacity', [(0, 1, 'hold'), (TYPE0, 0, 'hold'), (SEND, 1, None)])
# typing: the typewriter reveals one VISIBLE glyph per step (spaces take no step), so the caret is keyed per visible glyph
vis = [k for k, ch in enumerate(PROMPT) if ch != ' ']
ST = round((len(PROMPT) / CPS) / len(vis), 4)
C.append({'type': 'setTextAnimation', 'node': 'in.typed', 'phase': 'in', 'preset': 'typewriter', 'unit': 'character', 'duration': 0.01, 'stagger': ST})
keys('in.caret', 'x', [(TYPE0 + n * ST, round(tw(PROMPT[:k + 1], 25) * 1.003 + 2.5, 2), 'hold') for n, k in enumerate(vis)])
for n in ('send.mic.body', 'send.mic.arc'):
    keys(n, 'opacity', [(0, 1, 'hold'), (TYPE0, 0, 'hold'), (SEND + 0.1, 1, None)])
keys('send.arrow', 'opacity', [(0, 0, 'hold'), (TYPE0, 1, 'hold'), (SEND + 0.1, 0, None)])
keys('send', 'scale', [(SEND - 0.1, 1, 'easeOutCubic'), (SEND, 0.88, 'easeOutCubic'), (SEND + 0.16, 1, None)])
enter('msg.user', UB)
for k in range(3):
    ko, ks_ = [(TH0, 0.35, 'easyEase')], [(TH0, 0.85, 'easyEase')]
    t = TH0 + k * 0.15
    while t + 0.3 < TH1:
        a = t + 0.003 if t == TH0 else t
        ko += [(a, 0.35, 'easyEase'), (t + 0.18, 1, 'easyEase'), (t + 0.4, 0.35, 'easyEase')]
        ks_ += [(a, 0.85, 'easyEase'), (t + 0.18, 1.12, 'easyEase'), (t + 0.4, 0.85, 'easyEase')]
        t += 0.75
    keys(f'think.d{k}', 'opacity', ko); keys(f'think.d{k}', 'scale', ks_)
keys('think', 'opacity', [(TH0, 0, 'easeOutCubic'), (TH0 + 0.2, 1, None)])
pk, po, t = [], [], TH1
while t < EX1 - 0.05:
    e = min(t + 0.6, EX1) - 0.003
    pk += [(t, 0.7, 'linear'), (e, 1.55, 'hold')]; po += [(t, 0.4, 'linear'), (e, 0, 'hold')]
    t += 0.6
keys('expl.pulse', 'scale', pk); keys('expl.pulse', 'opacity', po)
enter('msg.reply', R1)
if CHECKS: enter('msg.checks', R2)
enter('card', R3, dy=18, dur=0.36)
tx = MX0 + 26 + b1w * 0.55; ty = BY + BH * 0.55
keys('cursor', 'x', [(CUR0, 1560, 'easeInOutCubic'), (CUR1, tx, 'hold'), (SCHED + 0.35, tx, 'easeInOutCubic'), (SCHED + 1.2, tx + 150, None)])
keys('cursor', 'y', [(CUR0, 1110, 'easeInOutCubic'), (CUR1, ty, 'hold'), (SCHED + 0.35, ty, 'easeInOutCubic'), (SCHED + 1.2, ty + 70, None)])
keys('cursor', 'scale', [(CLICK - 0.06, 1, 'easeOutCubic'), (CLICK, 0.86, 'easeOutCubic'), (CLICK + 0.14, 1, None)])
keys('card.btn1', 'scale', [(CLICK - 0.06, 1, 'easeOutCubic'), (CLICK, 0.95, 'easeOutCubic'), (CLICK + 0.14, 1, None)])
keys('card.btn1', 'brightness', [(CUR1 - 0.2, 1, 'easeOutCubic'), (CUR1, 1.9, None)])
keys('card.btns', 'opacity', [(SCHED - 0.02, 1, 'easeOutCubic'), (SCHED + 0.14, 0, None)])
enter('card.done', SCHED, dy=8, dur=0.28)

# --- the chosen bot's eyes react to the chat (poses are x, y, rotation, scale per eye, in px for an 80px avatar) ---
f = AVD / 80.0
N = ((0, 0, 0, 1), (0, 0, 0, 1))
P_SEND = ((16, -12, -32, 0.95), (16, -16, -32, 0.82))      # darts up-right as the message is sent
P_UP = ((0, -20, 80, 0.85), (-1, -21, 97, 0.85)); P_UP2 = ((3, -20, 84, 0.85), (2, -20, 100, 0.85))  # thinking: flat dashes at the top
P_W1 = ((-5, 6, 25, 1.22), (0, 9, 25, 1.22)); P_W2 = ((13, 13, -35, 1.25), (6, 1, -35, 1.25)); P_W3 = ((-4, 2, 30, 1.25), (-12, 14, 30, 1.25))  # exploring: big, rolling
P_TILT = ((2, -8, -14, 1), (2, -10, -14, 1)); P_LOOK = ((7, 5, -6, 1), (7, 5, -6, 1)); P_HAP = ((-1, -12, 0, 0.7), (-1, -13, 0, 0.7))
E = 'easeInOutCubic'
tl = [(0, N), (SEND + 0.02, N), (SEND + 0.24, P_SEND), (TH0, P_SEND), (TH0 + 0.25, P_UP), (TH0 + 0.65, P_UP2), (TH1 - 0.09, P_UP),
      (TH1 + 0.21, P_W1), (TH1 + 0.36, P_W1), (TH1 + 0.56, P_W2), (TH1 + 0.66, P_W2), (EX1 - 0.04, P_W3), (EX1 + 0.03, P_W3),
      (EX1 + 0.26, P_TILT), (EX1 + 0.36, P_TILT), (EX1 + 0.56, N), (R3 + 0.01, N), (R3 + 0.26, P_LOOK), (SCHED + 0.01, P_LOOK), (SCHED + 0.19, P_HAP), (END, P_HAP)]
blinks = (1.5, EX1 + 0.15, CUR0 + 0.36)
for ei, node in enumerate(['av.bot.e1', 'av.bot.e2']):
    for pi, prop in enumerate(['x', 'y', 'rotation', 'scale']):
        keys(node, prop, [(t, p[ei][pi] * (f if pi < 2 else 1), E) for t, p in tl])
    bl = [(0, 0, E)]
    for t in blinks: bl += [(t - 0.08, 0, E), (t, 86, E), (t + 0.1, 0, E)]   # a blink is the eye turning edge-on
    keys(node, 'rotateX', bl)
    keys(node, 'opacity', [(0, 1, 'hold'), (SCHED + 0.05, 1, E), (SCHED + 0.17, 0, None)])
for k in (1, 2):
    keys(f'av.bot.h{k}', 'opacity', [(SCHED + 0.07, 0, E), (SCHED + 0.21, 1, None)])
    keys(f'av.bot.h{k}', 'y', [(SCHED + 0.07, 9 * f, 'easeOutCubic'), (SCHED + 0.27, 0, None)])
keys('av.bot', 'y', [(UB, 0, 'easeOutCubic'), (UB + 0.12, -4, E), (UB + 0.3, 0, 'hold'), (SCHED + 0.07, 0, 'easeOutCubic'), (SCHED + 0.23, -5, E), (SCHED + 0.49, 0, None)])
keys('av.bot', 'scale', [(SCHED + 0.07, 1, 'easeOutCubic'), (SCHED + 0.23, 1.07, E), (SCHED + 0.49, 1, None)])

json.dump(C, open(sys.argv[2], 'w'), ensure_ascii=False)
plan['commands'] = len(C)
print(json.dumps(plan))
