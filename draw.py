#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (entry.png, 1024x1024).

Editorial-illustration style: a newspaper front page with a lead story, four
more stories and an ALSO strip. Every scene is drawn from scratch with PIL
primitives (gradients, silhouettes, flat shapes) -- no photos, no network,
no clock, no randomness except a fixed-seed speckle, so the output bytes are
fully deterministic: run it twice and the sha256 is identical.

Stories (all reported 17 November 2026, cross-checked across BBC / AP /
Reuters / Al Jazeera / NPR):
  LEAD  Ukraine strikes the Kerch Bridge; a road span collapses.
  2     Trump lands in Manila for the ASEAN summit; trade pact with Thailand.
  3     Two tankers hit mines in the Strait of Hormuz; third US carrier in.
  4     Estonia to shut its Russia border crossings from 1 December.
  5     Japan scrambles jets as Russian aircraft enter its airspace.
  ALSO  Depardieu pleads guilty in Paris; JPMorgan blames a software bug
        for its banking outage; UN counts 1,390 civilians killed in Sudan.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
GREY = (110, 106, 96)
RED = (176, 32, 32)
NAVY = (20, 33, 61)
RULE = (30, 30, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(img, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(top, bottom, (y - y0) / h))


def speckle(img, box, n, seed, color, alpha=60):
    """Deterministic grain: n dots of `color` inside box."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = rng.randint(x0, x1)
        y = rng.randint(y0, y1)
        r = rng.randint(1, 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (alpha,))
    img.alpha_composite(layer)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
# Each scene draws on its own RGB image of (w, h) and returns it.

def scene_bridge(w, h):
    im = Image.new("RGB", (w, h), (27, 42, 74))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, int(h * 0.62)), (24, 38, 70), (232, 134, 58))
    # low sun
    d.ellipse([int(w * 0.68), int(h * 0.30), int(w * 0.78), int(h * 0.44)],
              fill=(245, 214, 150))
    # sea
    d.rectangle([0, int(h * 0.62), w, h], fill=(16, 42, 66))
    for i in range(6):
        yy = int(h * 0.66) + i * int(h * 0.055)
        d.line([(0, yy), (w, yy)], fill=(52, 96, 128), width=2)
    # bridge deck (left + right spans, middle span broken and tilted down)
    deck_y = int(h * 0.52)
    d.rectangle([0, deck_y, int(w * 0.42), deck_y + 10], fill=(12, 14, 18))
    d.rectangle([int(w * 0.58), deck_y, w, deck_y + 10], fill=(12, 14, 18))
    # broken middle span, tilted into the gap
    d.polygon([(int(w * 0.42), deck_y), (int(w * 0.55), deck_y + 4),
               (int(w * 0.52), deck_y + 34), (int(w * 0.40), deck_y + 26)],
              fill=(12, 14, 18))
    # towers
    for tx in (int(w * 0.20), int(w * 0.80)):
        d.rectangle([tx - 6, int(h * 0.22), tx + 6, deck_y], fill=(12, 14, 18))
        d.rectangle([tx - 34, int(h * 0.30), tx + 34, int(h * 0.30) + 8],
                    fill=(12, 14, 18))
    # cables
    for tx in (int(w * 0.20), int(w * 0.80)):
        for fx in (0.02, 0.10, 0.30, 0.38, 0.62, 0.70, 0.90, 0.98):
            d.line([(tx, int(h * 0.24)), (int(w * fx), deck_y)],
                   fill=(40, 44, 52), width=2)
    # flame + smoke at the break
    bx, by = int(w * 0.50), deck_y + 6
    d.polygon([(bx - 16, by), (bx - 4, by - 34), (bx + 6, by - 12),
               (bx + 18, by - 30), (bx + 22, by)], fill=(240, 140, 40))
    d.polygon([(bx - 8, by), (bx, by - 18), (bx + 10, by)], fill=(250, 210, 90))
    for i, (sx, sy, sr) in enumerate([(0, -52, 20), (14, -78, 26), (-8, -102, 30),
                                      (10, -128, 34)]):
        d.ellipse([bx + sx - sr, by + sy - sr, bx + sx + sr, by + sy + sr],
                  fill=(70, 70, 74))
    # birds
    for bx2, by2 in [(90, 60), (130, 44), (420, 70)]:
        d.arc([bx2, by2, bx2 + 22, by2 + 12], 200, 340, fill=(20, 20, 26), width=2)
        d.arc([bx2 + 22, by2, bx2 + 44, by2 + 12], 200, 340, fill=(20, 20, 26), width=2)
    return im


def scene_summit(w, h):
    im = Image.new("RGB", (w, h), (214, 228, 238))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, h), (198, 220, 235), (240, 236, 222))
    d.ellipse([int(w * 0.74), int(h * 0.10), int(w * 0.88), int(h * 0.30)],
              fill=(248, 220, 140))
    # skyline silhouettes
    base = int(h * 0.98)
    for x0, bw, bh in [(0, 26, 52), (24, 34, 78), (56, 28, 60), (82, 40, 92),
                       (120, 30, 64), (148, 36, 84), (182, 26, 56)]:
        d.rectangle([x0, base - bh, x0 + bw, base], fill=(58, 70, 88))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x0 + 5, x0 + bw - 4, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 214, 120))
    # three flag poles with plain tricolour flags
    for i, cols in enumerate([((200, 40, 40), (255, 255, 255), (30, 60, 140)),
                              ((30, 90, 160), (255, 255, 255), (200, 40, 40)),
                              ((30, 120, 60), (255, 215, 0), (30, 60, 140))]):
        px = 30 + i * 62
        d.rectangle([px, int(h * 0.18), px + 3, base], fill=(40, 40, 44))
        fx0, fy0 = px + 3, int(h * 0.18)
        for j, c in enumerate(cols):
            d.rectangle([fx0, fy0 + j * 9, fx0 + 34, fy0 + (j + 1) * 9], fill=c)
    return im


def scene_tanker(w, h):
    im = Image.new("RGB", (w, h), (30, 70, 96))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, int(h * 0.55)), (250, 178, 110), (214, 110, 70))
    d.ellipse([int(w * 0.10), int(h * 0.12), int(w * 0.22), int(h * 0.30)],
              fill=(252, 226, 160))
    d.rectangle([0, int(h * 0.55), w, h], fill=(18, 58, 84))
    for i in range(5):
        yy = int(h * 0.60) + i * int(h * 0.08)
        d.line([(0, yy), (w, yy)], fill=(60, 110, 140), width=2)
    # tanker hull + containers
    hy = int(h * 0.62)
    d.polygon([(8, hy), (int(w * 0.92), hy), (int(w * 0.84), hy + 34),
               (16, hy + 34)], fill=(24, 26, 30))
    d.rectangle([int(w * 0.70), hy - 26, int(w * 0.86), hy], fill=(200, 60, 40))
    for i, c in enumerate([(210, 90, 40), (40, 120, 90), (220, 170, 60),
                           (70, 110, 180), (190, 70, 110)]):
        d.rectangle([14 + i * 26, hy - 22, 14 + (i + 1) * 26 - 3, hy - 2], fill=c)
    # mine: spiked circle floating ahead of the bow
    mx, my, mr = int(w * 0.94), int(h * 0.86), 9
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx, my), (mx + int(16 * math.cos(a)), my + int(16 * math.sin(a)))],
               fill=(14, 16, 18), width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(14, 16, 18))
    # flame + smoke at the stern
    fx, fy = 26, hy - 4
    d.polygon([(fx - 12, fy), (fx - 2, fy - 30), (fx + 8, fy - 10),
               (fx + 16, fy - 26), (fx + 18, fy)], fill=(240, 140, 40))
    for i, (sx, sy, sr) in enumerate([(0, -40, 14), (10, -60, 18), (-6, -80, 20)]):
        d.ellipse([fx + sx - sr, fy + sy - sr, fx + sx + sr, fy + sy + sr],
                  fill=(60, 60, 64))
    return im


def scene_border(w, h):
    im = Image.new("RGB", (w, h), (206, 224, 232))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, int(h * 0.55)), (196, 218, 232), (232, 236, 228))
    d.ellipse([int(w * 0.76), int(h * 0.08), int(w * 0.90), int(h * 0.28)],
              fill=(250, 224, 150))
    # distant hills + field
    d.polygon([(0, int(h * 0.55)), (int(w * 0.35), int(h * 0.40)),
               (int(w * 0.70), int(h * 0.55)), (w, int(h * 0.46)),
               (w, int(h * 0.58)), (0, int(h * 0.58))], fill=(120, 150, 110))
    d.rectangle([0, int(h * 0.58), w, h], fill=(96, 138, 82))
    # fence: posts + wires
    fy0, fy1 = int(h * 0.52), int(h * 0.92)
    for px in range(6, w, 34):
        d.rectangle([px, fy0, px + 5, fy1], fill=(52, 48, 44))
    for wy in (fy0 + 12, fy0 + 34, fy0 + 56):
        d.line([(0, wy), (w, wy)], fill=(90, 86, 80), width=3)
    # red-white barrier arm, lowered
    d.rectangle([int(w * 0.06), int(h * 0.66), int(w * 0.62), int(h * 0.66) + 10],
                fill=(200, 40, 40))
    for i in range(6):
        x0 = int(w * 0.06) + i * int(w * 0.093)
        d.rectangle([x0, int(h * 0.66), x0 + int(w * 0.046), int(h * 0.66) + 10],
                    fill=(245, 245, 240) if i % 2 else (200, 40, 40))
    # sign board
    sx0, sy0 = int(w * 0.66), int(h * 0.60)
    d.rectangle([sx0, sy0, sx0 + 56, sy0 + 40], fill=(245, 243, 236),
                outline=(176, 32, 32), width=3)
    d.line([(sx0 + 10, sy0 + 12), (sx0 + 46, sy0 + 12)], fill=(176, 32, 32), width=3)
    d.line([(sx0 + 10, sy0 + 22), (sx0 + 46, sy0 + 22)], fill=(176, 32, 32), width=3)
    d.line([(sx0 + 10, sy0 + 32), (sx0 + 34, sy0 + 32)], fill=(176, 32, 32), width=3)
    return im


def scene_jets(w, h):
    im = Image.new("RGB", (w, h), (240, 200, 150))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, h), (248, 214, 160), (196, 120, 90))
    # rising sun disc
    d.ellipse([int(w * 0.38), int(h * 0.42), int(w * 0.62), int(h * 0.78)],
              fill=(214, 52, 44))
    # clouds
    for cx, cy, cr in [(30, 30, 22), (120, 18, 18), (170, 110, 16)]:
        d.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2],
                  fill=(252, 240, 224))
    # two jets: simple delta silhouettes with contrails
    def jet(cx, cy, s):
        d.polygon([(cx - s, cy), (cx + s, cy - s // 3), (cx + s, cy + s // 3)],
                  fill=(28, 30, 34))
        d.polygon([(cx, cy - s // 2), (cx + s // 2, cy), (cx, cy + s // 2)],
                  fill=(28, 30, 34))
    jet(int(w * 0.30), int(h * 0.30), 30)
    jet(int(w * 0.62), int(h * 0.52), 24)
    for y0, x1 in [(int(h * 0.30), int(w * 0.30) - 30),
                   (int(h * 0.52), int(w * 0.62) - 24)]:
        d.line([(0, y0 + 26), (x1, y0)], fill=(255, 250, 240), width=3)
        d.line([(0, y0 + 44), (x1 - 10, y0 + 18)], fill=(255, 250, 240), width=2)
    return im


# ---------------------------------------------------------------- layout

LEAD = {
    "kicker": "WAR  ·  UKRAINE",
    "headline": "Ukraine strikes Kerch Bridge — span collapses",
    "summary": ("Kyiv says the road span to Crimea is down. Moscow vows to "
                "rebuild — and hits Kyiv's bridges in reply."),
    "scene": scene_bridge,
}

SECONDARIES = [
    {
        "kicker": "ASIA  ·  ASEAN",
        "headline": "Trump lands in Manila for ASEAN summit",
        "summary": ("Signs a trade statement with Thailand, then on to China "
                    "for talks with Xi and Putin."),
        "scene": scene_summit,
    },
    {
        "kicker": "GULF",
        "headline": "Two tankers hit mines in Strait of Hormuz",
        "summary": ("Iran's Guards say the tankers caught fire; a third U.S. "
                    "carrier steams into the region."),
        "scene": scene_tanker,
    },
    {
        "kicker": "EUROPE",
        "headline": "Estonia to shut Russia border crossings",
        "summary": ("Crossings close from 1 December after a foiled plot to "
                    "bomb a drone plant."),
        "scene": scene_border,
    },
    {
        "kicker": "ASIA  ·  JAPAN",
        "headline": "Japan scrambles jets as Russian planes enter its airspace",
        "summary": ("Tokyo protests after Russian aircraft enter its "
                    "airspace."),
        "scene": scene_jets,
    },
]

ALSO = ("ALSO:  Depardieu pleads guilty in Paris  ·  JPMorgan blames a bug "
        "for its outage  ·  UN: 1,390 killed in Sudan")


def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    mx = 36  # side margin

    # masthead
    d.text((mx, 22), "THE WORLD", font=SERIF_B(62), fill=INK)
    d.text((W - mx, 30), "TUESDAY, 17 NOVEMBER 2026", font=SANS_B(23),
           fill=INK, anchor="ra")
    d.text((W - mx, 62), "FIVE STORIES  ·  ONE DAY", font=SANS(15),
           fill=GREY, anchor="ra")
    d.rectangle([mx, 100, W - mx, 104], fill=RED)

    # ---- lead story
    ly = 122
    lead_img = LEAD["scene"](524, 330)
    im.paste(lead_img, (mx, ly))
    d.rectangle([mx, ly, mx + 524, ly + 330], outline=RULE, width=2)
    tx = mx + 548
    tw = W - mx - tx
    d.text((tx, ly + 2), LEAD["kicker"], font=SANS_B(21), fill=RED)
    y = text_block(d, tx, ly + 34,
                   wrap(d, LEAD["headline"], SERIF_B(44), tw),
                   SERIF_B(44), INK, 52)
    text_block(d, tx, y + 10,
               wrap(d, LEAD["summary"], SANS(22), tw), SANS(22),
               (58, 58, 58), 30)

    # ---- secondary grid (2 x 2)
    gy = 470
    d.rectangle([mx, gy - 6, W - mx, gy - 2], fill=RULE)
    cell_w = (W - 2 * mx - 28) // 2
    cell_h = 200
    for i, st in enumerate(SECONDARIES):
        cx = mx + (i % 2) * (cell_w + 28)
        cy = gy + 12 + (i // 2) * (cell_h + 12)
        img = st["scene"](196, 148)
        im.paste(img, (cx, cy))
        d.rectangle([cx, cy, cx + 196, cy + 148], outline=RULE, width=2)
        tx2 = cx + 212
        tw2 = cx + cell_w - tx2
        d.text((tx2, cy), st["kicker"], font=SANS_B(17), fill=RED)
        y2 = text_block(d, tx2, cy + 26,
                        wrap(d, st["headline"], SERIF_B(25), tw2),
                        SERIF_B(25), INK, 29)
        text_block(d, tx2, y2 + 6,
                   wrap(d, st["summary"], SANS(17), tw2), SANS(17),
                   (58, 58, 58), 21)

    # ---- ALSO strip + footer
    ay = 912
    d.rectangle([mx, ay - 8, W - mx, ay - 4], fill=RULE)
    fsize = 18
    while d.textlength(ALSO, font=SANS(fsize)) > W - 2 * mx and fsize > 12:
        fsize -= 1
    d.text((mx, ay + 6), ALSO, font=SANS(fsize), fill=(74, 74, 74))
    d.text((mx, H - 26),
           "All events reported Tuesday 17 November 2026  ·  Sources: BBC, "
           "AP, Reuters, Al Jazeera.",
           font=SANS(14), fill=GREY)
    d.text((W - mx, H - 26), "THE WORLD IN ONE DAY", font=SANS_B(14),
           fill=GREY, anchor="ra")
    return im


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    img = build()
    if out:
        os.makedirs(out, exist_ok=True)
        img.save(os.path.join(out, "entry.png"), optimize=True)
    else:
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
