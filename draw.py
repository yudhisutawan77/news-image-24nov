#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024).

Five stories, all events that happened or were first reported on
Tuesday 24 November 2026:
  1. Indonesia factory fire - at least 24 killed, dozens missing
  2. Russian cargo ship Sparta II hit by drone, ablaze off Finland
  3. COP31 climate talks end with no fossil-fuel phase-out deal
  4. Carlos Alcaraz wins his first ATP Finals title in Turin
  5. Nvidia rallies ~$1 trillion as Jensen Huang returns

Run:  python3 draw.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (193, 39, 45)
NAVY = (20, 33, 61)
ORANGE = (232, 90, 12)
GOLD = (245, 176, 0)
GREEN = (34, 139, 34)
DARKGREEN = (11, 94, 46)
TEAL = (14, 116, 144)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
FSERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def flame(draw, cx, base, s, colors=(GOLD, ORANGE, RED)):
    """Layered flame teardrops centred on cx, sitting on base."""
    for i, col in enumerate(colors):
        k = 1.0 - i * 0.28
        w = 62 * s * k
        h = 150 * s * k
        top = base - h
        pts = [
            (cx, top - 22 * s * k),
            (cx + w * 0.55, top + h * 0.45),
            (cx + w * 0.28, base - 6),
            (cx, base - 26 * s * k),
            (cx - w * 0.28, base - 6),
            (cx - w * 0.55, top + h * 0.45),
        ]
        draw.polygon(pts, fill=col)


def smoke(draw, x, y, r, color=(120, 120, 120)):
    for dx, dy, rr in [(0, 0, r), (r * 0.7, -r * 0.8, r * 0.75), (-r * 0.6, -r * 1.5, r * 0.6)]:
        draw.ellipse([x + dx - rr, y + dy - rr, x + dx + rr, y + dy + rr], fill=color)


def factory(draw, x0, y0, x1, y1, color=(40, 40, 48)):
    """Simple factory silhouette: hall + sawtooth roof + chimney."""
    draw.rectangle([x0, y1 - 90, x1, y1], fill=color)
    draw.polygon([(x0, y1 - 90), (x0 + 45, y1 - 130), (x0 + 90, y1 - 90),
                  (x0 + 135, y1 - 130), (x0 + 180, y1 - 90)], fill=color)
    draw.rectangle([x1 - 30, y1 - 170, x1 - 8, y1 - 60], fill=color)


def waves(draw, x0, x1, y, color, amp=7):
    pts = [(x0, y)]
    x = x0
    up = True
    while x < x1:
        pts.append((x + 26, y - amp if up else y + amp))
        x += 26
        up = not up
    pts += [(x1, y + 26), (x0, y + 26)]
    draw.polygon(pts, fill=color)


def globe(draw, cx, cy, r, sea=(38, 132, 190), land=(46, 160, 90)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=sea)
    draw.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05], fill=land)
    draw.ellipse([cx + r * 0.15, cy + r * 0.25, cx + r * 0.7, cy + r * 0.72], fill=land)
    draw.ellipse([cx - r * 0.2, cy - r * 0.95, cx + r * 0.35, cy - r * 0.45], fill=land)
    for dy in (-r * 0.5, 0, r * 0.5):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)


def tennis_court(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(46, 125, 50))
    draw.rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 14], outline=WHITE, width=4)
    draw.line([x0 + 14, (y0 + y1) // 2, x1 - 14, (y0 + y1) // 2], fill=WHITE, width=4)
    draw.line([(x0 + x1) // 2, y0 + 14, (x0 + x1) // 2, y1 - 14], fill=WHITE, width=3)


def chart_arrow(draw, x0, y0, x1, y1, color=GOLD):
    w, h = x1 - x0, y1 - y0
    pts = [(x0, y1 - 8),
           (x0 + 0.28 * w, y1 - 0.55 * h),
           (x0 + 0.48 * w, y1 - 0.38 * h),
           (x0 + 0.72 * w, y1 - 0.82 * h),
           (x0 + 0.95 * w, y1 - 0.92 * h)]
    draw.line(pts, fill=color, width=10, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx - 4, hy + 22), (hx + 26, hy - 6), (hx - 26, hy - 14)], fill=color)


def panel(draw, x0, y0, x1, y1, fill, border=INK, bw=3):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=border, width=bw)


def kicker(draw, x, y, text, color=RED, size=26):
    draw.text((x, y), text, font=font(FB, size), fill=color)
    return y + size + 8


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top red strip -------------------------------------------------
    d.rectangle([0, 0, W, 34], fill=RED)
    d.text((20, 4), "WORLD NEWS  •  ONE DAY  •  ONE IMAGE",
           font=font(FB, 20), fill=WHITE)
    d.text((W - 20 - d.textlength("TUESDAY", font=font(FB, 20)), 4),
           "TUESDAY", font=font(FB, 20), fill=WHITE)

    # ---- masthead: the date, huge --------------------------------------
    d.text((20, 44), "24 NOVEMBER 2026", font=font(FBLACK, 96), fill=INK)
    d.text((20, 146), "THE WORLD IN ONE IMAGE  —  FIVE STORIES THAT DEFINED THE DAY",
           font=font(FB, 25), fill=RED)
    d.line([20, 186, W - 20, 186], fill=INK, width=4)

    # ---- HERO: Indonesia factory fire ----------------------------------
    hx0, hy0, hx1, hy1 = 20, 198, W - 20, 510
    panel(d, hx0, hy0, hx1, hy1, (255, 236, 214))
    # illustration: factory + flames on the left
    factory(d, 44, 0, 330, hy1 - 24)
    smoke(d, 300, 250, 22)
    smoke(d, 330, 235, 16, (150, 150, 150))
    flame(d, 130, hy1 - 24, 1.15)
    flame(d, 250, hy1 - 24, 0.85)
    flame(d, 195, hy1 - 24, 0.6)
    # headline + copy on the right
    tx = 372
    kicker(d, tx, hy0 + 18, "TRAGEDY  •  INDONESIA")
    y = text_block(d, tx, hy0 + 56, "FACTORY FIRE KILLS AT LEAST 24",
                   font(FB, 52), INK, hx1 - tx - 24, leading=58)
    y = text_block(d, tx, y + 10,
                   "Blaze rips through a candy factory; dozens still missing.",
                   font(FR, 29), (60, 60, 60), hx1 - tx - 24, leading=36)
    d.text((tx, hy1 - 50), "24 DEAD  •  ~30 MISSING",
           font=font(FB, 30), fill=RED)

    # ---- middle row ----------------------------------------------------
    my0, my1 = 524, 752
    mw = (W - 60) // 2

    # Russian ship, ablaze off Finland
    x0, x1 = 20, 20 + mw
    panel(d, x0, my0, x1, my1, (214, 231, 240))
    d.rectangle([x0, my0, x1, my0 + 108], fill=(30, 52, 74))
    # ship silhouette
    d.polygon([(x0 + 40, my0 + 66), (x0 + 300, my0 + 66), (x0 + 270, my0 + 92),
               (x0 + 70, my0 + 92)], fill=(20, 20, 26))
    for cx in (x0 + 90, x0 + 150, x0 + 210):
        d.rectangle([cx, my0 + 38, cx + 42, my0 + 66], fill=(200, 60, 40))
    flame(d, x0 + 255, my0 + 68, 0.45)
    smoke(d, x0 + 255, my0 + 16, 11)
    waves(d, x0, x1, my0 + 92, (38, 132, 190), amp=5)
    kicker(d, x0 + 18, my0 + 116, "WAR AT SEA", size=23)
    text_block(d, x0 + 18, my0 + 148, "Russian cargo ship ablaze after drone strike",
               font(FB, 30), INK, mw - 36, leading=35)

    # COP31 ends without a deal
    x0, x1 = 40 + mw, W - 20
    panel(d, x0, my0, x1, my1, (226, 240, 226))
    globe(d, x0 + 78, my0 + 54, 42)
    d.line([x0 + 150, my0 + 22, x0 + 250, my0 + 88], fill=RED, width=8)
    d.line([x0 + 250, my0 + 22, x0 + 150, my0 + 88], fill=RED, width=8)
    d.text((x0 + 272, my0 + 34), "NO\nDEAL", font=font(FB, 30), fill=RED)
    kicker(d, x0 + 18, my0 + 116, "CLIMATE  •  COP31", size=23)
    text_block(d, x0 + 18, my0 + 148, "COP31 ends with no fossil-fuel deal",
               font(FB, 30), INK, mw - 36, leading=35)

    # ---- bottom row ----------------------------------------------------
    by0, by1 = 766, 988

    # Alcaraz wins ATP Finals
    x0, x1 = 20, 20 + mw
    panel(d, x0, by0, x1, by1, (232, 242, 232))
    tennis_court(d, x0 + 16, by0 + 12, x0 + 210, by0 + 92)
    d.ellipse([x0 + 250, by0 + 24, x0 + 314, by0 + 88], fill=(210, 230, 40),
              outline=WHITE, width=4)
    d.arc([x0 + 250, by0 + 24, x0 + 314, by0 + 88], 300, 60, fill=WHITE, width=4)
    d.arc([x0 + 250, by0 + 24, x0 + 314, by0 + 88], 120, 240, fill=WHITE, width=4)
    d.text((x0 + 332, by0 + 36), "ACE!", font=font(FBLACK, 40), fill=GREEN)
    kicker(d, x0 + 18, by0 + 116, "SPORT  •  TURIN", size=23)
    text_block(d, x0 + 18, by0 + 148, "Alcaraz wins first ATP Finals title",
               font(FB, 30), INK, mw - 36, leading=35)

    # Nvidia rallies ~$1 trillion
    x0, x1 = 40 + mw, W - 20
    panel(d, x0, by0, x1, by1, (16, 60, 38))
    chart_arrow(d, x0 + 30, by0 + 16, x0 + 300, by0 + 92)
    d.text((x0 + 320, by0 + 28), "+$1tn", font=font(FBLACK, 42), fill=GOLD)
    kicker(d, x0 + 18, by0 + 116, "MARKETS", color=GOLD, size=23)
    text_block(d, x0 + 18, by0 + 148, "Nvidia soars ~$1tn as Huang returns",
               font(FB, 30), WHITE, mw - 36, leading=35)

    # ---- footer ---------------------------------------------------------
    d.rectangle([0, 1000, W, H], fill=NAVY)
    d.text((20, 1004), "TUESDAY 24 NOVEMBER 2026  •  FIVE STORIES, ONE IMAGE",
           font=font(FB, 19), fill=WHITE)

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
