#!/usr/bin/env python3
"""Generate the SVG figures used by the profile README.

    python3 tools/build_assets.py

Writes into ../assets, one light and one dark file each (the README picks
one with <picture>):
  banner-{light,dark}.svg         name + a slowly rotating coloured point cloud
  sketch-<project>-{light,dark}.svg   small schematic for each project

Standard library only. The point cloud is procedural (a seeded random scene),
so re-running gives the same picture.
"""

import math
import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SERIF = "'Iowan Old Style', 'Charter', 'Palatino Linotype', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Background matches GitHub's page colour so the banner sits on the page
# instead of floating in a box.
THEMES = {
    "light": {"bg": "#ffffff", "ink": "#1f2328", "gray": "#59636e", "faint": "#d1d9e0",
              "hair": "#e6e9ec", "red": "#cf3a1f", "blue": "#2f6fb3", "green": "#3f8f3a",
              "shade": 0.9},
    "dark": {"bg": "#0d1117", "ink": "#e6edf3", "gray": "#9198a1", "faint": "#3d444d",
             "hair": "#21262d", "red": "#f0643f", "blue": "#5d9ce6", "green": "#6cbf62",
             "shade": 1.0},
}

# Natural colours for the scanned scene, a few shades per material.
MATERIALS = {
    "ground": ["#8b9a6c", "#a4aa86", "#7c8a5e", "#b1ad98", "#969c7c"],
    "wall": ["#dccfb8", "#c9bba1", "#b3a58b"],
    "roof": ["#ad573b", "#97482f", "#813d29"],
    "door": ["#5f4130"],
    "glass": ["#6f8597"],
    "trunk": ["#6f5038"],
    "leaf": ["#5e7f3f", "#4b6b33", "#789650", "#3f5c2b"],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f1(v):
    s = f"{v:.1f}"
    return "0" if s in ("0.0", "-0.0") else s.rstrip("0").rstrip(".")


def shade(hex_color, k):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{min(255, round(c * k)):02x}" for c in (r, g, b))


# ---------------------------------------------------------------- point cloud

def scene_points(rnd):
    """Sample a small house, a tree and a bush in horizontal rings, like a
    stationary LiDAR sweep. Returns (layer height step, {layer: [(x, z, colour)]})."""
    DY = 0.032
    layers = {}

    def add(y, x, z, material, tone=None):
        pal = MATERIALS[material]
        c = pal[tone if tone is not None else rnd.randrange(len(pal))]
        j = 0.006
        layers.setdefault(max(0, round(y / DY)), []).append(
            (x + rnd.uniform(-j, j), z + rnd.uniform(-j, j), c))

    hx, hz, ox, oz = 0.33, 0.25, -0.12, -0.06
    wall, ridge, eave, step = 0.42, 0.74, 0.05, 0.04
    i = 0
    while i * DY <= ridge + 1e-9:
        y = i * DY
        if y <= wall:
            n = int(2 * hx / step)
            for k in range(n + 1):
                x = -hx + k * 2 * hx / n
                door = -0.06 < x < 0.06 and y < 0.26
                window = (0.13 < x < 0.26 or -0.26 < x < -0.13) and 0.17 < y < 0.31
                mat = "door" if door else "glass" if window else "wall"
                add(y, ox + x, oz + hz, mat, 0 if mat == "wall" else None)
                add(y, ox + x, oz - hz, "glass" if window else "wall", 2 if not window else None)
        top_z = hz if y <= wall else hz * max(0.0, (ridge - y) / (ridge - wall))
        if top_z > 0.004:
            n = max(1, int(2 * top_z / step))
            for k in range(n + 1):
                z = -top_z + k * 2 * top_z / n
                add(y, ox - hx, oz + z, "wall", 1)
                add(y, ox + hx, oz + z, "wall", 1)
        if y >= wall - DY:
            zr = (hz + eave) * max(0.0, (ridge - y) / (ridge - (wall - DY)))
            n = int(2 * (hx + eave) / step)
            for k in range(n + 1):
                x = -(hx + eave) + k * 2 * (hx + eave) / n
                add(y, ox + x, oz + zr, "roof", 0)
                add(y, ox + x, oz - zr, "roof", 2)
        i += 1

    tx, tz = 0.6, 0.42
    for i in range(0, int(0.34 / DY) + 1):
        for k in range(6):
            a = k / 6 * math.tau
            add(i * DY, tx + 0.035 * math.cos(a), tz + 0.035 * math.sin(a), "trunk")
    for cx, cz, cy, r in ((tx, tz, 0.6, 0.25), (-0.68, 0.46, 0.12, 0.13)):
        for i in range(max(0, int((cy - r) / DY)), int((cy + r) / DY) + 1):
            y = i * DY
            rr = math.sqrt(max(0.0, r * r - (y - cy) ** 2))
            n = max(3, int(math.tau * rr / 0.048))
            off = rnd.random()
            for k in range(n):
                a = (k + off) / n * math.tau
                add(y, cx + rr * math.cos(a), cz + rr * math.sin(a), "leaf")

    for _ in range(760):
        r = math.sqrt(rnd.random())
        if rnd.random() < r * 0.6:
            continue
        a = rnd.random() * math.tau
        x, z = r * math.cos(a), r * math.sin(a)
        if abs(x - ox) < hx and abs(z - oz) < hz:
            continue
        add(0, x, z, "ground")
    return DY, layers


def banner_svg(theme):
    t = THEMES[theme]
    DY, layers = scene_points(random.Random(11))
    n_points = sum(len(v) for v in layers.values())
    n_cams = 10

    W, H = 1200, 290
    S = 150                       # px per scene unit
    elev = math.radians(21)
    sq, cy_scale = math.sin(elev), math.cos(elev)
    CX, GY = 905, 190
    SPIN = 64                     # seconds per turn

    # Each height layer is a flat group: rotate in the ground plane, then squash
    # by sin(elevation). That is an exact orthographic turntable for every point
    # in the layer, so one animateTransform per layer is enough. Without
    # animation support the picture is simply the first frame.
    spin = (f'<animateTransform attributeName="transform" type="rotate" from="0" to="-360" '
            f'dur="{SPIN}s" repeatCount="indefinite"/>')

    def layer(y, inner):
        return (f'<g transform="translate({CX} {f1(GY - y * S * cy_scale)}) scale(1 {sq:.4f})">'
                f'<g>{spin}{inner}</g></g>')

    # start at a three-quarter view, so the still frame already reads as 3D
    a0 = math.radians(-32)
    ca, sa = math.cos(a0), math.sin(a0)
    groups = []
    for idx in sorted(layers):
        by_colour = {}
        for x, z, c in layers[idx]:
            by_colour.setdefault(c, []).append((x * ca - z * sa, x * sa + z * ca))
        parts = []
        for c, pts in by_colour.items():
            d = "".join(f"M{f1(x * S)} {f1(z * S)}h0" for x, z in pts)
            parts.append(f'<path d="{d}" stroke="{shade(c, t["shade"])}"/>')
        groups.append(layer(idx * DY, "".join(parts)))

    # COLMAP-style red camera frustums on the capture orbit
    ring_y, ring_r = 0.38, 1.25
    cams = []
    for k in range(n_cams):
        a = k / n_cams * math.tau
        x, z = ring_r * math.cos(a) * S, ring_r * math.sin(a) * S
        cams.append(f'<g transform="translate({f1(x)} {f1(z)}) rotate({math.degrees(a) + 180:.0f})">'
                    f'<path d="M-3 0L9 -6.5L9 6.5Z M-3 0L9 0" fill="none"/></g>')
    orbit = layer(ring_y,
                  f'<circle r="{ring_r * S:.0f}" fill="none" stroke="{t["gray"]}" stroke-opacity=".5" '
                  f'stroke-dasharray="1 5"/><g stroke="{t["red"]}" stroke-width="1.2" stroke-linejoin="round">'
                  f'{"".join(cams)}</g>')

    # world axes, drawn like a viewer gizmo
    ax, ay = CX - 240, 262
    gizmo = (f'<g stroke-width="1.4" stroke-linecap="round" font-family="{MONO}" font-size="10">'
             f'<path d="M{ax} {ay}h22" stroke="{t["red"]}"/><path d="M{ax} {ay}v-22" stroke="{t["green"]}"/>'
             f'<path d="M{ax} {ay}l-12 9" stroke="{t["blue"]}"/>'
             f'<text x="{ax + 26}" y="{ay + 3.5}" fill="{t["gray"]}" stroke="none">x</text>'
             f'<text x="{ax - 3}" y="{ay - 26}" fill="{t["gray"]}" stroke="none">y</text>'
             f'<text x="{ax - 22}" y="{ay + 14}" fill="{t["gray"]}" stroke="none">z</text></g>')

    caption = f"fig. 1   turntable scan, {n_points:,} points, {n_cams} views"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Feng-Yuan Kuo</title>
  <desc id="desc">Bringing real-world scenes into 3D: capture, reconstruct, train, explore. A coloured point cloud of a small house and a tree is scanned from the ground up and turns slowly, with red camera frustums on the capture orbit.</desc>
  <style>.pc path {{ vector-effect: non-scaling-stroke }} .pc circle {{ vector-effect: non-scaling-stroke }}</style>
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <text x="56" y="122" font-family="{SERIF}" font-size="54" letter-spacing="-.5" fill="{t["ink"]}">Feng-Yuan Kuo</text>
  <text x="58" y="164" font-family="{SANS}" font-size="20" fill="{t["gray"]}">Bringing real-world scenes into 3D.</text>
  <text x="58" y="214" font-family="{MONO}" font-size="13" fill="{t["gray"]}">capture <tspan fill="{t["red"]}">→</tspan> reconstruct <tspan fill="{t["red"]}">→</tspan> train <tspan fill="{t["red"]}">→</tspan> explore</text>
  <g class="pc" fill="none" stroke-linecap="round" stroke-width="2.2">{"".join(groups)}</g>
  <g class="pc">{orbit}</g>
  {gizmo}
  <text x="{CX}" y="{H - 12}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["gray"]}">{esc(caption)}</text>
</svg>
'''


# ---------------------------------------------------------------- sketches
# 360 x 160, transparent background so they sit on the table cell.

def sketch_align_capture(t, rnd):
    out = []
    # survey grid
    for x in range(10, 231, 20):
        out.append(f'<path d="M{x} 12V148" stroke="{t["hair"]}"/>')
    for y in range(12, 149, 17):
        out.append(f'<path d="M10 {y}H230" stroke="{t["hair"]}"/>')
    # lawnmower flight path
    rows = [34, 64, 94, 124]
    pts = []
    for i, y in enumerate(rows):
        xs = (34, 206) if i % 2 == 0 else (206, 34)
        pts += [(xs[0], y), (xs[1], y)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{t["gray"]}" stroke-dasharray="3 3"/>')
    # capture points along each pass
    shots = []
    for i, y in enumerate(rows):
        for k in range(7):
            x = 40 + k * 27.5
            shots.append((x, y))
            out.append(f'<rect x="{x - 2.5:.1f}" y="{y - 2.5}" width="5" height="5" fill="{t["ink"]}"/>')
    hx, hy = shots[11]
    out.append(f'<rect x="{hx - 5:.1f}" y="{hy - 5}" width="10" height="10" fill="none" stroke="{t["red"]}" stroke-width="1.4"/>')
    # drone at the end of the path
    dx, dy = pts[-1]
    out.append(f'<g transform="translate({dx} {dy})" fill="none" stroke="{t["ink"]}" stroke-width="1.2">'
               f'<path d="M-6 -6L6 6M6 -6L-6 6"/><circle cx="-7" cy="-7" r="3.2"/><circle cx="7" cy="-7" r="3.2"/>'
               f'<circle cx="-7" cy="7" r="3.2"/><circle cx="7" cy="7" r="3.2"/></g>')
    # EXIF callout
    out.append(f'<path d="M{hx + 5:.1f} {hy}C{hx + 40:.0f} {hy} 230 40 250 40" fill="none" stroke="{t["red"]}" stroke-width="1"/>')
    lines = ["IMG_0142.jpg", "GPSLatitude  ✓", "GPSLongitude ✓", "GPSAltitude  ✓"]
    out.append(f'<rect x="250" y="26" width="104" height="70" rx="3" fill="{t["bg"]}" stroke="{t["faint"]}"/>')
    for i, s in enumerate(lines):
        col = t["ink"] if i == 0 else t["gray"]
        out.append(f'<text x="258" y="{42 + i * 15}" font-family="{MONO}" font-size="9.5" fill="{col}">{esc(s)}</text>')
    out.append(f'<text x="250" y="122" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">RTSP frame +</text>')
    out.append(f'<text x="250" y="136" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">MAVLink fix</text>')
    return "".join(out)


def sketch_reconstudio(t, rnd):
    out = []
    # frames
    for i in range(3):
        x, y = 14 + i * 7, 40 + i * 7
        out.append(f'<rect x="{x}" y="{y}" width="62" height="42" rx="2" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.1"/>')
    out.append(f'<path d="M34 76l12 -12l10 8l8 -6l12 10" fill="none" stroke="{t["gray"]}"/>')
    out.append(f'<circle cx="64" cy="64" r="3" fill="none" stroke="{t["gray"]}"/>')
    # sparse cloud + cameras
    cx, cy = 178, 70
    for _ in range(90):
        a = rnd.random() * math.tau
        r = abs(rnd.gauss(0, 1)) * 18
        x, y = cx + r * math.cos(a) * 1.4, cy + r * math.sin(a) * 0.8
        c = shade(rnd.choice(MATERIALS["wall"] + MATERIALS["leaf"] + MATERIALS["roof"]), t["shade"])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.25" fill="{c}"/>')
    for k, (x, y, rot) in enumerate(((140, 30, 35), (178, 22, 90), (216, 30, 145))):
        out.append(f'<g transform="translate({x} {y}) rotate({rot})"><path d="M-3 0L8 -5L8 5Z" fill="none" '
                   f'stroke="{t["red"]}" stroke-width="1.1" stroke-linejoin="round"/></g>')
    # mesh
    mx, my = 300, 70
    ring = [(mx + 38 * math.cos(a), my + 30 * math.sin(a)) for a in (k / 7 * math.tau for k in range(7))]
    inner = [(mx + 15 * math.cos(a + .4), my + 12 * math.sin(a + .4)) for a in (k / 4 * math.tau for k in range(4))]
    edges = []
    for i in range(7):
        edges.append((ring[i], ring[(i + 1) % 7]))
        edges.append((ring[i], inner[(i * 4 // 7) % 4]))
        edges.append((ring[i], inner[((i + 1) * 4 // 7) % 4]))
    for i in range(4):
        edges.append((inner[i], inner[(i + 1) % 4]))
    edges.append((inner[0], inner[2]))
    d = "".join(f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" for a, b in edges)
    out.append(f'<path d="{d}" fill="none" stroke="{t["ink"]}" stroke-width=".9"/>')
    # arrows + labels
    for x0, x1 in ((100, 132), (232, 254)):
        out.append(f'<path d="M{x0} 70H{x1}m-5 -4l5 4l-5 4" fill="none" stroke="{t["gray"]}"/>')
    for x, s in ((44, "frames"), (178, "COLMAP"), (300, "3DGS → mesh")):
        out.append(f'<text x="{x}" y="128" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">{esc(s)}</text>')
    return "".join(out)


def sketch_cesium(t, rnd):
    out = []
    gx, gy, r = 92, 80, 62
    out.append(f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="{t["ink"]}" stroke-width="1.1"/>')
    for k in (0.35, 0.7):
        out.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{r * k:.1f}" ry="{r}" fill="none" stroke="{t["faint"]}"/>')
    for lat in (-0.5, 0, 0.5):
        yy = gy - r * math.sin(lat)
        rx = r * math.cos(lat)
        out.append(f'<ellipse cx="{gx}" cy="{yy:.1f}" rx="{rx:.1f}" ry="{rx * .18:.1f}" fill="none" stroke="{t["faint"]}"/>')
    px, py = gx + 24, gy - 26
    out.append(f'<circle cx="{px}" cy="{py}" r="3" fill="{t["red"]}"/>')
    # inset with gaussian splats
    bx, by, bw, bh = 214, 18, 132, 112
    out.append(f'<path d="M{px + 3} {py}L{bx} {by}M{px + 3} {py}L{bx} {by + bh}" stroke="{t["faint"]}"/>')
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="{t["bg"]}" stroke="{t["faint"]}"/>')
    pal = MATERIALS["roof"] + MATERIALS["wall"] + MATERIALS["leaf"] + MATERIALS["ground"]
    for _ in range(46):
        x = bx + 18 + rnd.random() * (bw - 36)
        y = by + 22 + rnd.random() * (bh - 44)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rnd.uniform(4, 11):.1f}" ry="{rnd.uniform(2, 5):.1f}" '
                   f'transform="rotate({rnd.uniform(-60, 60):.0f} {x:.1f} {y:.1f})" '
                   f'fill="{shade(rnd.choice(pal), t["shade"])}" fill-opacity=".55"/>')
    out.append(f'<text x="{bx}" y="{by + bh + 18}" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">PLY → 3D Tiles</text>')
    out.append(f'<text x="{gx}" y="{gy + r + 18}" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">geo-aligned</text>')
    return "".join(out)


def sketch_ragglass(t, rnd):
    out = []
    # source page
    out.append(f'<path d="M20 12H96L114 30V148H20Z" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.1"/>')
    out.append(f'<path d="M96 12V30H114" fill="none" stroke="{t["ink"]}" stroke-width="1.1"/>')
    y = 42
    for i in range(9):
        w = 70 if i % 3 else 52
        if i in (4, 5):
            out.append(f'<rect x="29" y="{y - 5}" width="{w + 4}" height="9" fill="{t["red"]}" fill-opacity=".18"/>')
        out.append(f'<path d="M31 {y}h{w}" stroke="{t["gray"]}" stroke-width="2"/>')
        y += 11
    out.append(f'<text x="20" y="160" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">p. 2</text>')
    # answer
    ax, ay = 200, 34
    out.append(f'<rect x="{ax}" y="{ay}" width="146" height="78" rx="4" fill="{t["bg"]}" stroke="{t["faint"]}"/>')
    for i, w in enumerate((118, 126, 96, 70)):
        out.append(f'<path d="M{ax + 12} {ay + 18 + i * 13}h{w}" stroke="{t["ink"]}" stroke-width="2" stroke-opacity=".75"/>')
    cx, cy = ax + 92, ay + 57
    out.append(f'<rect x="{cx - 1}" y="{cy - 7}" width="22" height="13" rx="2" fill="{t["bg"]}" stroke="{t["red"]}"/>')
    out.append(f'<text x="{cx + 10}" y="{cy + 3}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["red"]}">[2]</text>')
    out.append(f'<path d="M{cx + 10} {cy + 6}C{cx + 10} 140 140 110 106 92" fill="none" stroke="{t["red"]}" '
               f'stroke-dasharray="3 3"/><path d="M110 88l-5 4l6 2" fill="none" stroke="{t["red"]}"/>')
    out.append(f'<text x="{ax}" y="{ay - 10}" font-family="{MONO}" font-size="9.5" fill="{t["gray"]}">answer + citation</text>')
    return "".join(out)


SKETCHES = {
    "align-capture": sketch_align_capture,
    "reconstudio": sketch_reconstudio,
    "cesium-viewer": sketch_cesium,
    "ragglass": sketch_ragglass,
}


def sketch_svg(name, theme):
    t = THEMES[theme]
    body = SKETCHES[name](t, random.Random(name))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="166" viewBox="0 0 360 166" '
            f'role="img" aria-label="Sketch of {esc(name)}">{body}</svg>\n')


def main():
    ASSETS.mkdir(exist_ok=True)
    out = {}
    for theme in THEMES:
        out[f"banner-{theme}.svg"] = banner_svg(theme)
        for name in SKETCHES:
            out[f"sketch-{name}-{theme}.svg"] = sketch_svg(name, theme)
    for name, svg in out.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(f"{name:34s} {len(svg.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
