#!/usr/bin/env python3
"""Lay out a dramatic quote as Tella text overlays.

Reads a spec JSON, measures each line in the real font file, and prints the
`operations` array for one `apply_video_edits` call: one text overlay per quote
line, then the name and the publication. The quote is a justified block centred
on the canvas: every line is stretched with letterSpacing to the widest line's
width, the opening and closing quote marks hang outside it, and the attribution
spans the same measure (name on the left edge, publication on the right edge).

Spec (times in seconds on the clip's playback timeline):
{
  "clipId": "cl_...",
  "canvas": [1920, 1080],
  "fontFile": "/workspace/IMFeENrm28P.ttf",
  "fontId": "mi_...",            # or "fontFamily": "Lora" for the fallback
  "lines": ["a bizarre experience", "and unexpected end", "to a regular weekend"],
  "name": "Astrid Vestergaard",
  "source": "The Jutland Courier",
  "times": [0.8, 1.75, 2.7],       # one per line
  "nameTime": 4.2, "sourceTime": 4.9,
  "end": 9.7                       # all overlays end together, fading out over 0.7 s
}
Usage: python3 dramatic_quote.py spec.json > ops.json
"""
import json
import sys

from PIL import ImageFont

INK = "#F5F0E6"
OPEN, CLOSE = "“", "”"


def main():
    spec = json.load(open(sys.argv[1]))
    w, h = spec["canvas"]
    k = min(w, h) / 1080
    qs, asz = 63 * k, 32.7 * k          # quote and attribution font sizes
    pitch, gap = 78 * k, 92 * k         # line to line, last line to attribution
    qbox, abox = 80 * k, 56 * k         # box heights
    qf = ImageFont.truetype(spec["fontFile"], round(qs))
    af = ImageFont.truetype(spec["fontFile"], round(asz))

    lines = [l.strip().strip(OPEN + CLOSE + '"') for l in spec["lines"]]
    texts = list(lines)
    texts[0] = OPEN + texts[0]
    texts[-1] = texts[-1] + CLOSE
    measure = max(qf.getlength(l) for l in lines)
    left = (w - measure) / 2
    name = spec["name"].rstrip(",") + ","
    source = spec["source"]
    row = af.getlength(name + " " + source)
    one_row = row <= measure * 1.06    # a hair wider than the block still reads as one justified row
    span = max(measure, row)
    top = (h - ((len(lines) - 1) * pitch + gap + abox * (1 if one_row else 2))) / 2

    font = {"fontId": spec["fontId"]} if spec.get("fontId") else {"fontFamily": spec.get("fontFamily", "Lora")}
    end = spec["end"]
    style = dict(font, color=INK, fontWeight=400, shadow="subtle", transition="hard_cut", depth="front",
                 animation={"intro": None, "outro": {"preset": "fade", "durationMs": 700,
                                                     "easing": {"curve": "accelerate", "intensity": 0.5}},
                            "textIntro": None, "textOutro": None, "motionBlur": False})

    def overlay(op, text, size, x, y, bw, bh, align, ls, start):
        return dict(style, type="add_text_overlay", operationId=op, clipId=spec["clipId"], text=text,
                    fontSize=round(size, 1), textAlign=align, letterSpacing=round(ls, 4),
                    point={"xPct": round(100 * x / w, 3), "yPct": round(100 * y / h, 3)},
                    dimensions={"width": round(bw), "height": round(bh)},
                    startTimeMs=round(start * 1000), durationMs=round((end - start) * 1000))

    ops, warnings = [], []
    for i, (core, text) in enumerate(zip(lines, texts)):
        ls = (measure - qf.getlength(core)) / (qs * max(len(core) - 1, 1))
        if ls > 0.06:
            warnings.append(f"line {i + 1} needs letterSpacing {ls:.3f}: rebalance the line breaks")
        x = left
        if text.startswith(OPEN):
            x -= qf.getlength(OPEN) + ls * qs
        ops.append(overlay(f"line{i + 1}", text, qs, x, top + i * pitch, measure + 360 * k, qbox, "left",
                           ls, spec["times"][i]))
    ay = top + (len(lines) - 1) * pitch + gap
    bw = measure + 60 * k
    ops.append(overlay("name", name, asz, left, ay, bw, abox, "left", 0.002, spec["nameTime"]))
    if one_row:
        ops.append(overlay("source", source, asz, left + span - bw, ay, bw, abox, "right", 0.002,
                           spec["sourceTime"]))
    else:
        warnings.append("name and publication don't fit one row: publication set on its own row")
        ops.append(overlay("source", source, asz, left, ay + abox * 0.8, bw, abox, "left", 0.002,
                           spec["sourceTime"]))
    for msg in warnings:
        print("warning:", msg, file=sys.stderr)
    print(json.dumps(ops, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
