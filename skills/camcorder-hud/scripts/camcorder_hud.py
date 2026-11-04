#!/usr/bin/env python3
"""Build the Tella Motion commands for one clip's camcorder HUD.

Usage:
  camcorder_hud.py --width 1920 --height 1080 --clip-start-ms 0 --clip-duration-ms 2655 \
      --font-id mi_xxx --date "OCT. 31 2026" --clock "23:47:03" --out hud_clip1.json

--clip-start-ms is the clip's timelineStartMs (whole-video time), so the tape counter,
clock and REC blink continue across clips. Pass the JSON path as `commandsFile` to
tella__apply_motion_editor_commands on a blank document made with create_motion_document.
"""
import argparse, json, math

def build(W, H, S, D, font, date, clock):
    land = W >= H
    s = min(W, H) / 1080.0          # scale everything to the short side
    fs = round(72 * s) if land else round(64 * s)
    ins, arm, sw = round(70 * s if land else 60 * s), round(80 * s), max(3, round(5 * s))
    dur = D / 1000.0
    t0, t1 = S / 1000.0, (S + D) / 1000.0
    h0, m0, s0 = [int(x) for x in clock.split(":")]
    c = [{"type": "canvas.set", "canvas": {"width": W, "height": H, "duration": {"seconds": dur}}}]
    # viewfinder corner brackets
    p = (f"M{ins} {ins+arm} L{ins} {ins} L{ins+arm} {ins} "
         f"M{W-ins-arm} {ins} L{W-ins} {ins} L{W-ins} {ins+arm} "
         f"M{W-ins} {H-ins-arm} L{W-ins} {H-ins} L{W-ins-arm} {H-ins} "
         f"M{ins+arm} {H-ins} L{ins} {H-ins} L{ins} {H-ins-arm}")
    c.append({"type": "addPath", "start": 0, "duration": dur, "nodeId": "brackets", "path": p,
              "color": "#ffffff", "paint": "stroke", "strokeWidth": sw, "cap": "square", "join": "miter"})
    # REC: blinking red dot (on for the first half of every whole-video second) + label
    top = ins + round(28 * s)
    left = ins + round(52 * s)
    dot = round(fs * 0.47)
    c.append({"type": "addShape", "start": 0, "duration": dur, "nodeId": "rec.dot", "shape": "circle",
              "box": {"x": left, "y": top + round(fs * 0.4), "width": dot, "height": dot}, "color": "#ff2a1f"})
    keys = {}
    k = math.floor(t0 * 2) / 2
    while k < t1:
        at = round(max(0, k - t0), 3)
        keys[at] = {"at": at, "value": 1 if round(k * 2) % 2 == 0 else 0, "easing": "hold"}
        k += 0.5
    keys = sorted(keys.values(), key=lambda x: x["at"])
    if len(keys) > 1:
        c.append({"type": "setKeyframes", "node": "rec.dot", "property": "opacity", "keys": keys})
    elif keys and keys[0]["value"] == 0:
        c.append({"type": "setProperty", "node": "rec.dot", "property": "opacity", "value": 0})
    c.append({"type": "addTitle", "start": 0, "duration": dur, "nodeId": "rec.label", "text": "REC",
              "box": {"x": left + dot + round(14 * s), "y": top, "width": round(200 * s)},
              "font": font, "fontSize": fs, "color": "#ffffff", "align": "left"})
    # SP + battery, top right
    bw, bh = round((92 if land else 84) * s), round((40 if land else 36) * s)
    bx, by = W - ins - round(24 * s) - bw - round(10 * s), top + round(fs * 0.25)
    c.append({"type": "addTitle", "start": 0, "duration": dur, "nodeId": "sp", "text": "SP",
              "box": {"x": bx - round(144 * s), "y": top, "width": round(120 * s)},
              "font": font, "fontSize": fs, "color": "#ffffff", "align": "right"})
    c.append({"type": "addPath", "start": 0, "duration": dur, "nodeId": "batt.body",
              "path": f"M{bx} {by} H{bx+bw} V{by+bh} H{bx} Z", "color": "#ffffff",
              "paint": "stroke", "strokeWidth": max(2, round(4 * s)), "join": "miter"})
    c.append({"type": "addShape", "start": 0, "duration": dur, "nodeId": "batt.nub", "shape": "rect",
              "box": {"x": bx + bw + 2, "y": by + round(bh * 0.28), "width": round(8 * s), "height": round(bh * 0.45)},
              "color": "#ffffff"})
    gap = round(7 * s)
    barw = (bw - gap * 4) / 3
    for i in range(3):
        c.append({"type": "addShape", "start": 0, "duration": dur, "nodeId": f"batt.bar{i}", "shape": "rect",
                  "box": {"x": round(bx + gap + i * (barw + gap)), "y": by + gap, "width": round(barw), "height": bh - 2 * gap},
                  "color": "#ffffff"})
    # bottom: tape counter (left), clock over date (right); one title per whole-video second
    line = round(fs * 0.8)
    datey = H - ins - round(28 * s) - fs
    clocky = datey - line
    rbox_w = round(500 * s)
    rbox_x = W - ins - round(52 * s) - rbox_w
    n = math.floor(t0)
    while n < t1:
        a, b = max(0, n - t0), min(dur, (n + 1) - t0)
        if b - a > 0.0005:
            base = h0 * 3600 + m0 * 60 + s0 + n
            hh, mm, ss = (base // 3600) % 24, (base // 60) % 60, base % 60
            tm = f"{hh % 12 or 12}:{mm:02d}:{ss:02d} {'PM' if hh >= 12 else 'AM'}"
            c.append({"type": "addTitle", "start": round(a, 4), "duration": round(b - a, 4), "nodeId": f"counter.{n}",
                      "text": f"{n // 3600}:{(n // 60) % 60:02d}:{n % 60:02d}",
                      "box": {"x": left, "y": datey, "width": round(400 * s)},
                      "font": font, "fontSize": fs, "color": "#ffffff", "align": "left"})
            c.append({"type": "addTitle", "start": round(a, 4), "duration": round(b - a, 4), "nodeId": f"clock.{n}",
                      "text": tm, "box": {"x": rbox_x, "y": clocky, "width": rbox_w},
                      "font": font, "fontSize": fs, "color": "#ffffff", "align": "right"})
        n += 1
    c.append({"type": "addTitle", "start": 0, "duration": dur, "nodeId": "date", "text": date,
              "box": {"x": rbox_x, "y": datey, "width": rbox_w},
              "font": font, "fontSize": fs, "color": "#ffffff", "align": "right"})
    return c

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    ap.add_argument("--clip-start-ms", type=int, required=True)
    ap.add_argument("--clip-duration-ms", type=int, required=True)
    ap.add_argument("--font-id", required=True, help="library font id (mi_...) of VT323")
    ap.add_argument("--date", default="OCT. 31 2026")
    ap.add_argument("--clock", default="23:47:03", help="24h start time shown at 0:00 of the video")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cmds = build(a.width, a.height, a.clip_start_ms, a.clip_duration_ms, a.font_id, a.date, a.clock)
    json.dump(cmds, open(a.out, "w"))
    print(f"{len(cmds)} commands -> {a.out}")

