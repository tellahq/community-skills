# Graphics calculator screen: dot paths

Everything on the plot screen is drawn on the 5 px dot grid of the window `[260, 165, 1400, 750]`, as filled `addPath` shapes (`fillType` winding) in the ink colour, one `M x y h5 v5 h-5 z` square per dot (merge a horizontal run into one `hN`). Snap every x and y to a multiple of 5 so each square lands on exactly one dot of the `lcdpix` shader; a square that straddles two dots lights both, or neither.

## Axes (`plotaxes`)

The video's axes, for x from about −0.56 to 8.2 and y from −0.29 to +0.29:

- origin (352.5, 487.5): y axis is the dot column x 350, x axis the dot row y 485, each one dot thick, the x axis spanning the whole window width (x 260–1660);
- x scale 160 px (32 dots) per unit, a tick every unit: three dots tall (y 475–495) at x 510, 670, 830 … 1630;
- y scale 1100 px per unit, a tick every 0.1: five dots wide (x 340–360) at y 265, 375, 595, 705.

Pick the scales for the user's function so 2–3 periods (or the interesting part) fill the width, the peaks sit about 30 px inside the window top and bottom, and ticks land on round values. Keep the origin about 90 px in from the left edge so the y axis and its ticks read.

## The curve (`plotcurve`)

Sample the function once per dot column and join neighbours so a steep part stays unbroken:

```python
def curve_path(f, x0px, y0px, sx, sy, left=260, right=1655, top=165, bottom=905):
    snap = lambda v: int(round(v / 5.0)) * 5
    dots, prev = set(), None
    for px in range(left, right + 1, 5):
        x = (px + 2.5 - x0px) / sx                      # canvas → function units
        py = snap(y0px - f(x) * sy - 2.5)
        if top <= py <= bottom:
            if prev is None or abs(py - prev) <= 5:
                dots.add((px, py))
            else:                                       # steep: fill from just past the last dot
                step = 5 if py > prev else -5
                for y in range(prev + step, py + step, step):
                    dots.add((px, y))
            prev = py
        else:
            prev = None                                 # off screen: lift the pen
    return "".join(f"M{x} {y}h5v5h-5z" for x, y in sorted(dots))
```

In the video `f(x) = 0.25*cos(1.98057*x)` (the pendulum's swing for its period of 3.172 s), with `x0px = 352.5`, `y0px = 487.5`, `sx = 160`, `sy = 1100`. That gives 615 dots, about 10 KB of path text, well inside one command.

Draw it on with `fx.linearWipe` on the curve: `completion` keyed 1 → 0 (linear) over 1.5 s, `angle` −90, `feather` 0, so it reveals left to right.

## Trace cross (`tcross`)

A 5-dot plus centred on the origin: `M350 475h5v5h-5zM350 480h5v5h-5zM340 485h25v5h-25zM350 490h5v5h-5zM350 495h5v5h-5z`. Move it with `x`/`y` hold keys, one key every 0.04 s, 20 px (0.125 units) right per key and `y = −f(x) × sy` (snapped to 5) down. Key the same steps into a named curve (`setCurve` `trT`, hold keys, value = x in function units) and bind the readouts to it:

- `rdx`: `bindProperty` `text` to `{curve: "trT"}`, `text: {prefix: "(", suffix: ",", decimals: 3}`;
- `rdy`: `bindProperty` `text` to the function of the curve, e.g. `{op: "multiply", args: [0.25, {op: "cos", args: [{op: "multiply", args: [{curve: "trT"}, 1.98057]}]}]}`, `text: {suffix: ")", decimals: 4}`.

Write the function with the `bindProperty` ops (`add`, `multiply`, `sin`, `cos`, `pow`, `sqrt`, `abs`, …). A function those ops can't express can still be plotted; key `rdy`'s values into a second curve instead.

## Busy annunciator (`hg*`)

A 7 × 9 dot hourglass in the status line, top-left dot at (1180, 190), shown for 0.15–0.25 s while each step "computes". Rows, top to bottom (`#` is a dot):

```
#######
#.....#
.#...#.
..#.#..
...#...
..#.#..
.#.#.#.
#.###.#
#######
```

Draw it as one path (`M1180 190h35v5h-35z…`) and give each showing its own start and end, or duplicate the path per showing.
