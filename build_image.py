#!/usr/bin/env python3
"""THE WEDNESDAY EDITION - news-image-20261125 entry generator.
Deterministic PIL broadsheet: one image, the world news of Wednesday 25 Nov 2026.
No randomness, no network. Run: python3 build_image.py  -> writes entry.png (1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
MX = 26                      # side margin
PAPER   = (246, 239, 221)
PANEL_BG= (251, 247, 236)
INK     = (28, 30, 38)
MUTED   = (96, 90, 78)
RED     = (168, 44, 34)
NAVY    = (30, 58, 92)
GOLD    = (178, 138, 44)
BORDER  = (203, 190, 158)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size): return ImageFont.truetype(FD + name, int(size))
SERIF_B  = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF    = lambda s: F("DejaVuSerif.ttf", s)
SANS_B   = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS     = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(draw, s, font):
    b = draw.textbbox((0, 0), s, font=font); return b[2] - b[0]

def tracked(draw, x, y, s, font, fill, track=2):
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += tw(draw, ch, font) + track
    return cx - track

def tracked_w(draw, s, font, track=2):
    return sum(tw(draw, ch, font) + track for ch in s) - track

def wrap(draw, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(draw, t, font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def grad(size, top, bot):
    w, h = size
    g = Image.new("RGB", size)
    gd = ImageDraw.Draw(g)
    for i in range(h):
        t = i / max(1, h - 1)
        gd.line([(0, i), (w, i)], fill=tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3)))
    return g

# ---------------------------------------------------------------- vignettes
def vig_rocket(w, h):
    v = grad((w, h), (16, 26, 54), (70, 110, 160)); dv = ImageDraw.Draw(v)
    for sx, sy in [(30, 18), (90, 40), (150, 14), (200, 50), (60, 60), (170, 70), (120, 26)]:
        dv.ellipse([sx, sy, sx + 2, sy + 2], fill=(235, 235, 220))
    # station module top right
    dv.rectangle([w - 66, 12, w - 40, 24], fill=(210, 205, 190), outline=(120, 115, 100))
    dv.rectangle([w - 92, 16, w - 68, 20], fill=(90, 120, 180))
    dv.rectangle([w - 38, 16, w - 14, 20], fill=(90, 120, 180))
    # rocket, ascending
    cx, cy = w // 2 - 10, h // 2 + 2
    dv.polygon([(cx - 11, cy + 14), (cx - 11, cy - 8), (cx, cy - 26), (cx + 11, cy - 8), (cx + 11, cy + 14)], fill=(240, 238, 230), outline=(90, 90, 90))
    dv.polygon([(cx - 11, cy - 8), (cx, cy - 26), (cx + 11, cy - 8)], fill=RED)
    dv.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY)
    dv.rectangle([cx - 11, cy + 8, cx + 11, cy + 11], fill=RED)
    dv.polygon([(cx - 11, cy + 6), (cx - 20, cy + 18), (cx - 11, cy + 18)], fill=RED)
    dv.polygon([(cx + 11, cy + 6), (cx + 20, cy + 18), (cx + 11, cy + 18)], fill=RED)
    dv.polygon([(cx - 5, cy + 18), (cx, cy + 31), (cx + 5, cy + 18)], fill=(255, 190, 60))
    dv.polygon([(cx - 2, cy + 18), (cx, cy + 26), (cx + 2, cy + 18)], fill=(255, 240, 190))
    # ground clouds
    for ex, ey, r in [(30, h - 8, 26), (80, h - 4, 32), (150, h - 8, 28), (205, h - 4, 30)]:
        dv.ellipse([ex - r, ey - r // 2, ex + r, ey + r // 2], fill=(225, 220, 205))
    return v

def vig_markets(w, h):
    v = Image.new("RGB", (w, h), (18, 24, 44)); dv = ImageDraw.Draw(v)
    for gx in range(0, w, 24): dv.line([(gx, 0), (gx, h)], fill=(34, 44, 70))
    for gy in range(0, h, 16): dv.line([(0, gy), (w, gy)], fill=(34, 44, 70))
    raw = [(6, 12), (40, 20), (74, 16), (108, 34), (142, 30), (176, 52), (210, 62), (w - 6, 66)]
    pts = [(x, int(y * h / 76)) for x, y in raw]
    dv.line(pts, fill=(235, 90, 70), width=3)
    for px, py in pts: dv.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 160, 120))
    ay = int(66 * h / 76)
    dv.polygon([(w - 22, ay - 10), (w - 6, ay + 4), (w - 4, ay - 14)], fill=(235, 90, 70))
    for bx, bh, col in [(16, 26, (90, 190, 120)), (44, 18, (235, 90, 70)), (72, 30, (235, 90, 70)), (100, 14, (90, 190, 120)), (128, 34, (235, 90, 70)), (156, 24, (235, 90, 70))]:
        bh = max(5, int(bh * h / 76))
        dv.rectangle([bx, h - 4 - bh, bx + 16, h - 4], fill=col)
    return v

def vig_tariffs(w, h):
    v = grad((w, h), (150, 180, 205), (215, 205, 180)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, h - 12, w, h], fill=(105, 100, 90))
    cols = [(200, 90, 60), (60, 110, 160), (90, 150, 90), (220, 170, 60)]
    rows = 2 if h >= 50 else 1
    spots = [(10, 0), (62, 0), (114, 0), (10, 1), (62, 1)]
    for i, (bx, rw) in enumerate(spots):
        if rw >= rows: continue
        by = h - 12 - (rw + 1) * 15
        c = cols[i % 4]
        dv.rectangle([bx, by, bx + 46, by + 14], fill=c, outline=(70, 65, 55))
        dv.line([(bx + 4, by), (bx + 4, by + 14)], fill=(70, 65, 55))
        dv.line([(bx + 42, by), (bx + 42, by + 14)], fill=(70, 65, 55))
    # crane
    dv.rectangle([w - 40, 4, w - 35, h - 12], fill=(70, 70, 75))
    dv.rectangle([w - 116, 4, w - 35, 9], fill=(70, 70, 75))
    dv.line([(w - 96, 9), (w - 96, 20)], fill=(70, 70, 75), width=2)
    dv.rectangle([w - 108, 20, w - 84, 33], fill=cols[1], outline=(70, 65, 55))
    # tariff tag
    dv.polygon([(150, 8), (192, 8), (201, 21), (192, 34), (150, 34)], fill=(250, 246, 235), outline=RED)
    dv.text((157, 13), "%", font=SANS_B(18), fill=RED)
    return v

def vig_hormuz(w, h):
    v = grad((w, h), (120, 150, 180), (60, 95, 135)); dv = ImageDraw.Draw(v)
    dv.polygon([(0, 0), (52, 0), (30, 44), (0, 60)], fill=(150, 125, 90))
    dv.polygon([(w, 0), (w - 56, 0), (w - 30, 40), (w, 58)], fill=(150, 125, 90))
    dv.rectangle([0, h - 22, w, h], fill=(45, 80, 115))
    for wy in (h - 16, h - 9):
        for wx in range(6, w, 26): dv.arc([wx, wy, wx + 16, wy + 6], 0, 180, fill=(140, 180, 210))
    # tanker
    tx, ty = w // 2 - 62, h - 28
    dv.polygon([(tx, ty), (tx + 124, ty), (tx + 112, ty + 12), (tx + 10, ty + 12)], fill=(40, 42, 48))
    dv.rectangle([tx + 8, ty - 6, tx + 104, ty], fill=(120, 60, 50))
    dv.rectangle([tx + 96, ty - 16, tx + 112, ty - 6], fill=(225, 222, 210), outline=(90, 90, 90))
    # mine with warning ring
    mx, my = w - 44, h - 24
    dv.ellipse([mx - 16, my - 16, mx + 16, my + 16], outline=(255, 120, 90), width=2)
    dv.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(35, 35, 40))
    for a in range(0, 360, 45):
        r = math.radians(a)
        dv.line([(mx + 8 * math.cos(r), my + 8 * math.sin(r)), (mx + 13 * math.cos(r), my + 13 * math.sin(r))], fill=(35, 35, 40), width=2)
    return v

def vig_gaza(w, h):
    v = grad((w, h), (205, 150, 110), (120, 110, 105)); dv = ImageDraw.Draw(v)
    dv.ellipse([w - 46, 4, w - 20, 30], fill=(245, 215, 160))
    # damaged block
    dv.rectangle([24, 5, 112, h - 5], fill=(105, 98, 92), outline=(70, 64, 58))
    for r in range(2):
        for c in range(3):
            x0, y0 = 33 + c * 26, 10 + r * max(11, (h - 22) // 2)
            if (r, c) == (0, 2):
                dv.polygon([(x0, y0), (x0 + 15, y0 + 3), (x0 + 6, y0 + 10), (x0, y0 + 9)], fill=(40, 38, 36))
            else:
                dv.rectangle([x0, y0, x0 + 15, y0 + 9], fill=(60, 62, 66) if (r + c) % 2 else (235, 200, 130))
    dv.line([(94, 5), (84, h // 2), (98, h - 5)], fill=(45, 42, 40), width=2)
    # second block + rubble + smoke
    dv.rectangle([138, h - 24, 198, h - 5], fill=(130, 122, 112), outline=(80, 74, 66))
    for px, py in [(146, h - 20), (168, h - 20), (146, h - 12), (168, h - 12)]:
        dv.rectangle([px, py, px + 12, py + 6], fill=(70, 72, 76))
    dv.polygon([(118, h - 5), (146, h - 16), (182, h - 5)], fill=(90, 84, 78))
    for sx, sy, r in [(158, 14, 8), (168, 8, 11), (180, 3, 13)]:
        dv.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2], fill=(150, 145, 140))
    return v

def vig_toll(w, h):
    v = grad((w, h), (170, 175, 180), (120, 125, 120)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, h - 26, w, h], fill=(105, 120, 95))
    # rows of grave markers receding
    for row, (yy, s) in enumerate([(h - 8, 4), (h - 16, 5), (h - 24, 6), (h - 31, 7)]):
        for i in range(7):
            x = 16 + i * 30 + (row % 2) * 12
            dv.rectangle([x, yy - s, x + s // 2 + 2, yy], fill=(235, 232, 222), outline=(120, 118, 110))
    for px, py in [(36, h - 5), (90, h - 3), (150, h - 6), (196, h - 4)]:
        dv.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        dv.line([(px, py + 3), (px, py + 8)], fill=(80, 110, 70), width=1)
    dv.rectangle([0, 0, w, 10], fill=(90, 95, 105))
    return v

def vig_chen(w, h):
    v = Image.new("RGB", (w, h), (120, 26, 26)); dv = ImageDraw.Draw(v)
    for cx in (14, 52, 168, 206):
        dv.rectangle([cx, 10, cx + 16, h - 10], fill=(150, 40, 36), outline=GOLD)
        dv.rectangle([cx - 3, 6, cx + 19, 12], fill=GOLD)
        dv.rectangle([cx - 3, h - 14, cx + 19, h - 8], fill=GOLD)
    dv.rectangle([88, 0, 132, 8], fill=GOLD)
    # falling document with seal + crack
    dv.polygon([(86, 10), (138, 5), (143, h - 5), (91, h - 1)], fill=(245, 240, 228), outline=(120, 110, 95))
    dv.ellipse([103, 12, 123, 32], outline=RED, width=2)
    dv.text((109, 15), "*", font=SANS_B(12), fill=RED)
    dv.line([(95, h - 13), (133, h - 16)], fill=(150, 145, 130))
    dv.line([(97, h - 8), (128, h - 10)], fill=(150, 145, 130))
    dv.line([(86, 10), (108, 23), (99, 31), (116, h - 5)], fill=(60, 55, 50), width=2)
    return v

def vig_puigdemont(w, h):
    v = grad((w, h), (165, 188, 214), (228, 216, 196)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, h - 8, w, h], fill=(120, 112, 100))
    # senyera (Catalan) flag, left
    dv.line([(26, h - 8), (26, 6)], fill=(70, 62, 50), width=2)
    dv.rectangle([26, 6, 56, 24], fill=(240, 195, 60))
    for i in range(4):
        dv.rectangle([26, 8 + i * 4 + (2 if i else 0), 56, 10 + i * 4 + (2 if i else 0)], fill=(200, 45, 50))
    # Spanish flag, right
    dv.line([(w - 26, h - 8), (w - 26, 6)], fill=(70, 62, 50), width=2)
    dv.rectangle([w - 56, 6, w - 26, 24], fill=(200, 45, 50))
    dv.rectangle([w - 56, 11, w - 26, 19], fill=(245, 200, 70))
    # podium with microphones, centre
    px = w // 2
    dv.polygon([(px - 17, h - 8), (px - 13, h - 26), (px + 13, h - 26), (px + 17, h - 8)], fill=(52, 58, 74), outline=(30, 34, 44))
    dv.rectangle([px - 15, h - 29, px + 15, h - 26], fill=(40, 46, 60))
    for sgn in (-1, 1):
        dv.line([(px + sgn * 6, h - 27), (px + sgn * 13, h - 38)], fill=(35, 35, 38), width=2)
        dv.ellipse([px + sgn * 13 - 3, h - 42, px + sgn * 13 + 3, h - 36], fill=(35, 35, 38))
    # homecoming plane, top centre
    ax, ay = px + 34, 12
    dv.polygon([(ax - 12, ay + 2), (ax + 10, ay - 3), (ax + 13, ay), (ax + 10, ay + 3), (ax - 8, ay + 4)], fill=(60, 66, 80))
    dv.polygon([(ax - 2, ay - 3), (ax + 3, ay - 8), (ax + 6, ay - 8), (ax + 5, ay - 2)], fill=(60, 66, 80))
    for t in range(4):
        dv.ellipse([ax - 26 + t * 5, ay + 8 + t * 2, ax - 24 + t * 5, ay + 10 + t * 2], fill=(240, 240, 235))
    return v

def vig_solomons(w, h):
    v = grad((w, h), (120, 175, 205), (70, 130, 165)); dv = ImageDraw.Draw(v)
    dv.ellipse([w - 48, 8, w - 22, 34], fill=(250, 220, 130))
    dv.rectangle([0, h - 26, w, h], fill=(60, 120, 155))
    for wx in range(4, w, 24): dv.arc([wx, h - 18, wx + 15, h - 12], 0, 180, fill=(150, 200, 225))
    # two islands
    dv.ellipse([16, h - 44, 104, h - 18], fill=(90, 150, 90))
    dv.ellipse([126, h - 40, 214, h - 18], fill=(90, 150, 90))
    # flag poles + flags
    t1 = max(3, h - 70); t2 = max(3, h - 66)
    dv.line([(58, h - 36), (58, t1)], fill=(60, 55, 45), width=2)
    dv.polygon([(58, t1), (82, t1 + 6), (58, t1 + 13)], fill=(40, 90, 170))
    dv.line([(168, h - 32), (168, t2)], fill=(60, 55, 45), width=2)
    dv.polygon([(168, t2), (192, t2 + 6), (168, t2 + 13)], fill=(30, 130, 70))
    # palm
    ptop = max(5, h - 58)
    dv.line([(120, h - 20), (120, ptop)], fill=(110, 85, 55), width=3)
    for dx, dy in [(-17, 2), (-10, -5), (0, -8), (10, -5), (17, 2)]:
        dv.line([(120, ptop), (120 + dx, ptop + dy + 5)], fill=(50, 110, 60), width=2)
    return v

def vig_iowa(w, h):
    v = grad((w, h), (175, 180, 185), (130, 135, 140)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, h - 16, w, h], fill=(120, 115, 105))
    # plant buildings behind
    dv.rectangle([150, 26, 210, 62], fill=(150, 148, 142), outline=(90, 88, 84))
    dv.rectangle([186, 14, 196, 26], fill=(120, 118, 112))
    dv.rectangle([20, 38, 74, 62], fill=(155, 152, 146), outline=(90, 88, 84))
    # barrels
    btop = max(6, h - 50)
    for i, bx in enumerate((34, 76, 118)):
        dv.rectangle([bx, btop, bx + 34, h - 16], fill=(105, 110, 118), outline=(60, 62, 68))
        dv.ellipse([bx, btop - 4, bx + 34, btop + 6], fill=(140, 145, 152), outline=(60, 62, 68))
        sy = min(btop + 13, h - 23)
        dv.rectangle([bx, sy, bx + 34, sy + 5], fill=(200, 160, 40))
    # warning sign
    scy = max(13, h - 48)
    dv.line([(196, h - 16), (196, scy + 10)], fill=(70, 70, 70), width=2)
    dv.polygon([(196, scy - 12), (213, scy + 11), (179, scy + 11)], fill=(245, 200, 60), outline=(60, 60, 60))
    dv.text((192, scy - 3), "!", font=SANS_B(13), fill=(40, 40, 40))
    # striped barrier
    for i in range(6):
        dv.rectangle([8 + i * 36, h - 14, 8 + (i + 1) * 36, h - 6], fill=(215, 60, 45) if i % 2 == 0 else (240, 238, 230), outline=(90, 90, 90))
    return v

def vig_hera(w, h):
    v = Image.new("RGB", (w, h), (12, 16, 34)); dv = ImageDraw.Draw(v)
    for fx, fy in [(0.07, 0.3), (0.27, 0.6), (0.53, 0.2), (0.8, 0.5), (0.89, 0.15), (0.18, 0.85), (0.4, 0.12), (0.66, 0.85), (0.11, 0.1), (0.87, 0.9)]:
        sx, sy = int(fx * w), int(fy * h)
        dv.ellipse([sx, sy, sx + 2, sy + 2], fill=(230, 230, 215))
    # dashed trajectory
    for t in range(0, 101, 8):
        x = w * 0.06 + t * w * 0.0048; y = h * 0.78 - (h * 0.34) * math.sin(t / 100 * math.pi * 0.8)
        dv.ellipse([x, y, x + 3, y + 3], fill=(150, 170, 210))
    # Dimorphos (small, dented) + Didymos (big)
    ay, ah = h * 0.52, max(14, h * 0.52)
    dv.ellipse([w * 0.57, ay - ah / 2, w * 0.57 + ah * 1.14, ay + ah / 2], fill=(150, 145, 138), outline=(90, 88, 84))
    dv.ellipse([w * 0.62, ay - ah * 0.22, w * 0.62 + ah * 0.27, ay + ah * 0.05], fill=(120, 116, 110))
    dv.polygon([(w * 0.57, ay - ah * 0.1), (w * 0.62, ay + ah * 0.08), (w * 0.575, ay + ah * 0.24)], fill=(100, 97, 92))
    by2, bh2 = h * 0.66, max(11, h * 0.4)
    dv.ellipse([w * 0.78, by2 - bh2 / 2, w * 0.78 + bh2 * 1.18, by2 + bh2 / 2], fill=(140, 135, 128), outline=(90, 88, 84))
    dv.ellipse([w * 0.83, by2 - bh2 * 0.14, w * 0.83 + bh2 * 0.3, by2 + bh2 * 0.14], fill=(112, 108, 102))
    # probe
    px, py = int(w * 0.2), int(h * 0.16)
    dv.rectangle([px, py, px + 15, py + 11], fill=(220, 215, 200), outline=(110, 108, 100))
    dv.rectangle([px - 19, py + 2, px - 2, py + 9], fill=(70, 100, 170))
    dv.rectangle([px + 17, py + 2, px + 34, py + 9], fill=(70, 100, 170))
    dv.line([(px + 7, py + 11), (px + 7, py + 17)], fill=(200, 195, 180), width=2)
    return v

def vig_cartagena(w, h):
    v = grad((w, h), (150, 185, 210), (215, 200, 165)); dv = ImageDraw.Draw(v)
    dv.rectangle([0, h - 10, w, h], fill=(150, 140, 125))
    # storefront
    dv.rectangle([36, 13, 196, h - 10], fill=(238, 232, 218), outline=(100, 95, 85))
    dv.polygon([(30, 13), (202, 13), (189, 3), (43, 3)], fill=RED)
    wy1 = max(22, h - 17)
    dv.rectangle([48, 19, 108, wy1], fill=(90, 120, 150), outline=(80, 78, 72))
    dv.rectangle([124, 19, 184, wy1], fill=(90, 120, 150), outline=(80, 78, 72))
    my = (19 + wy1) // 2
    dv.line([(48, my), (108, my)], fill=(200, 210, 220))
    dv.line([(124, my), (184, my)], fill=(200, 210, 220))
    dv.rectangle([94, max(24, h - 24), 128, h - 10], fill=(110, 85, 60), outline=(70, 60, 45))
    # cordon tape
    for i in range(7):
        dv.polygon([(10 + i * 30, h - 16), (10 + (i + 1) * 30, h - 16), (10 + (i + 1) * 30, h - 10), (10 + i * 30, h - 10)], fill=(215, 60, 45) if i % 2 == 0 else (245, 242, 235))
    # palm right
    ptop = max(6, h - 50)
    dv.line([(w - 16, h - 10), (w - 22, ptop)], fill=(110, 85, 55), width=3)
    for dx, dy in [(-15, 2), (-9, -4), (0, -7), (9, -4), (15, 2)]:
        dv.line([(w - 22, ptop), (w - 22 + dx, ptop + dy + 4)], fill=(50, 110, 60), width=2)
    return v

def vig_sudan(w, h):
    v = grad((w, h), (215, 180, 130), (170, 140, 105)); dv = ImageDraw.Draw(v)
    dv.ellipse([16, 8, 44, 36], fill=(250, 225, 160))
    dv.rectangle([0, h - 22, w, h], fill=(160, 130, 95))
    # town: flat roofs + minaret
    for bx, bw, bh in [(14, 40, 26), (60, 34, 20), (150, 44, 24), (196, 30, 18)]:
        dv.rectangle([bx, h - 22 - bh, bx + bw, h - 22], fill=(190, 165, 130), outline=(120, 100, 75))
        dv.rectangle([bx + 6, h - 22 - bh + 6, bx + 14, h - 22 - bh + 14], fill=(90, 80, 70))
    dv.rectangle([112, h - 56, 120, h - 22], fill=(200, 175, 140), outline=(120, 100, 75))
    dv.polygon([(108, h - 56), (124, h - 56), (116, max(2, h - 66))], fill=(200, 175, 140), outline=(120, 100, 75))
    # smoke column
    for sx, sy, r in [(80, 44, 10), (88, 30, 14), (98, 16, 18)]:
        dv.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2], fill=(110, 105, 100))
    # drone silhouette
    dx, dy = 168, 26
    dv.rectangle([dx - 8, dy - 3, dx + 8, dy + 3], fill=(45, 45, 48))
    for ox, oy in [(-16, -8), (16, -8), (-16, 8), (16, 8)]:
        dv.line([(dx, dy), (dx + ox, dy + oy)], fill=(45, 45, 48), width=2)
        dv.ellipse([dx + ox - 5, dy + oy - 2, dx + ox + 5, dy + oy + 2], outline=(45, 45, 48), width=2)
    return v

def vig_chess(w, h):
    v = Image.new("RGB", (w, h), (52, 44, 40)); dv = ImageDraw.Draw(v)
    # board sized to the box
    sq = max(7, min((h - 6) // 4, (w - 20) // 8))
    bx, by = (w - 8 * sq) // 2, (h - 4 * sq) // 2
    for r in range(4):
        for c in range(8):
            col = (232, 220, 195) if (r + c) % 2 == 0 else (120, 84, 58)
            dv.rectangle([bx + c * sq, by + r * sq, bx + (c + 1) * sq, by + (r + 1) * sq], fill=col)
    # two kings facing off, scaled to the squares
    def king(cx, base, col):
        s = sq / 24
        pts = [(-11, 0), (-7, -30), (-3, -22), (0, -32), (3, -22), (7, -30), (11, 0)]
        dv.polygon([(cx + int(px * s), base + int(py * s)) for px, py in pts], fill=col)
        dv.rectangle([cx - int(12 * s), base, cx + int(12 * s), base + max(2, int(5 * s))], fill=col)
        dv.line([(cx, base - int(44 * s)), (cx, base - int(34 * s))], fill=col, width=max(1, int(3 * s)))
        dv.line([(cx - int(4 * s), base - int(40 * s)), (cx + int(4 * s), base - int(40 * s))], fill=col, width=max(1, int(3 * s)))
    base = by + 4 * sq - max(3, int(5 * sq / 24))
    king(bx + 3 * sq + sq // 2, base, (30, 30, 34))
    king(bx + 4 * sq + sq // 2, base, (240, 236, 224))
    return v

VIGS = {1: vig_rocket, 2: vig_markets, 3: vig_tariffs, 4: vig_hormuz, 5: vig_gaza,
        6: vig_toll, 7: vig_chen, 8: vig_puigdemont, 9: vig_solomons, 10: vig_iowa,
        11: vig_hera, 12: vig_cartagena, 13: vig_sudan, 14: vig_chess}

# ---------------------------------------------------------------- panels
def panel(x, y, w, h, num, tag, head, sub, vig, head_size=13, sub_size=8.5,
          vig_h=40, head_lines=2, sub_lines=3):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=BORDER)
    v = vig(w - 12, vig_h)
    img.paste(v, (x + 6, y + 6))
    ty = y + 6 + vig_h + 4
    d.text((x + 7, ty), tag, font=SANS_B(7.5), fill=RED); ty += 11
    hf = SANS_B(head_size)
    for ln in wrap(d, head, hf, w - 14)[:head_lines]:
        d.text((x + 7, ty), ln, font=hf, fill=INK); ty += head_size + 3
    ty += 1
    sf = SANS(sub_size)
    for ln in wrap(d, sub, sf, w - 14)[:sub_lines]:
        d.text((x + 7, ty), ln, font=sf, fill=(52, 54, 60)); ty += sub_size + 3.5
    d.text((x + w - 22, y + h - 20), str(num), font=SERIF_B(13), fill=GOLD)

# ---------------------------------------------------------------- masthead
d.line([(MX, 12), (W - MX, 12)], fill=INK, width=2)
d.text((MX, 20), "ONE IMAGE · THE WHOLE WORLD · ONE DAY", font=SANS_B(10), fill=MUTED)
r = "WED 25 NOV 2026 · ALL TIMES UTC"
d.text((W - MX - tw(d, r, SANS_B(10)), 20), r, font=SANS_B(10), fill=MUTED)
d.line([(MX, 39), (W - MX, 39)], fill=INK, width=1)

name = "THE WEDNESDAY EDITION"
nf = SANS_B(19)
tracked(d, (W - tracked_w(d, name, nf, 6)) // 2, 48, name, nf, INK, 6)
date = "Wednesday 25 November 2026"
df = SERIF_B(50)
d.text(((W - tw(d, date, df)) // 2, 72), date, font=df, fill=INK)
d.line([(MX, 124), (W - MX, 124)], fill=BORDER, width=1)

strap = "50 STORIES · 8 REGIONS · EVERY ONE FROM WEDNESDAY 25 NOVEMBER 2026"
d.rectangle([MX, 128, W - MX, 152], fill=NAVY)
sf = SANS_B(13.5)
d.text(((W - tw(d, strap, sf)) // 2, 134), strap, font=sf, fill=(245, 242, 232))

# timeline strip
TY, TH = 158, 32
d.rectangle([MX, TY, W - MX, TY + TH], fill=PANEL_BG, outline=BORDER)
d.rectangle([MX, TY, MX + 96, TY + TH], fill=RED)
tl = "WEDNESDAY"
d.text((MX + (96 - tw(d, tl, SANS_B(10.5))) // 2, TY + 10), tl, font=SANS_B(10.5), fill=(250, 246, 238))
tl_items = ["00:18 Shenzhou-24 lifts off in China",
            "14:00 Chess game two opens in Geneva",
            "15:00 Iowa's blast hour, 9am local",
            "18:45 Hera's asteroid images, Berlin"]
for i, t in enumerate(tl_items):
    d.text((MX + 108 + i * 218, TY + 10), t, font=SANS(9), fill=INK)

# lead row
panel(MX, 196, 576, 144, 1, "1 · ASIA · SPACE — CONFIRMED · REUTERS",
      "Pakistan's first astronaut rides a Chinese rocket",
      "Shenzhou-24 lifts off at 00:18 UTC carrying Muhammad Zeeshan Ali, who docks at Tiangong: the first foreigner aboard China's station, and the first Pakistani in orbit.",
      vig_rocket, head_size=19, sub_size=11, vig_h=54, head_lines=2, sub_lines=3)
panel(610, 196, 388, 144, 2, "2 · ASIA · MARKETS — REPORTED · REUTERS",
      "AI rebound stumbles: Asia's chip shares slide",
      "Seoul sinks 5.3% and Taipei 5.1% at the worst; Tokyo sheds 2.9% as tariff threats return and the tech rally fizzles.",
      vig_markets, head_size=15.5, sub_size=10, vig_h=54, head_lines=2, sub_lines=3)

# 12 small panels, 4 x 3
COLX = [26, 271, 516, 761]; COLW = 237; ROWY = [348, 476, 604]; ROWH = 120
SMALL = [
    (3,  "3 · AMERICAS · TRADE — REPORTED · AP", "US readies tariffs on China, EU, 14 more",
     "A probe into subsidised output clears the path; sources say an announcement is near."),
    (4,  "4 · MIDEAST · SECURITY — REPORTED · REUTERS", "Iran: two tankers hit mines in Hormuz",
     "The Guards say both ships exploded and caught fire, and warn vessels to check in first."),
    (5,  "5 · GAZA · WAR — REPORTED · REUTERS", "Israel kills 2nd Hamas security chief",
     "Colonel Abuelouf, his wife and two children die in a dawn strike on their camp flat."),
    (6,  "6 · EUROPE · WAR — REPORTED · BBC", "Russia's toll: near 500,000 war dead",
     "Moscow's own published figures imply the count, BBC analysis of the data finds."),
    (7,  "7 · ASIA · POLITICS — REPORTED · REUTERS", "Xi purge takes a Politburo star",
     "Shanghai chief Chen Jining is the fourth Politburo member probed since 2025."),
    (8,  "8 · EUROPE · POLITICS — REPORTED · REUTERS", "Puigdemont to end exile, go home",
     "Nine years after fleeing to Brussels, the Catalan leader says he returns on 12 December."),
    (9,  "9 · OCEANIA · DIPLOMACY — CONFIRMED · REUTERS", "Solomons sign with Australia",
     "Canberra becomes partner of choice; no foreign military base, ever, Honiara vows."),
    (10, "10 · AMERICAS · SOCIETY — REPORTED · REUTERS", "Iowa empties for the big blast",
     "Near 5 tons of rotting lead azide are set to blow at 9am; Middletown is evacuated."),
    (11, "11 · SPACE · SCIENCE — REPORTED · BBC", "First look at the moved asteroid",
     "ESA's Hera shares its close-ups of Dimorphos in Berlin, four years after DART's hit."),
    (12, "12 · AMERICAS · SECURITY — REPORTED · AFP", "Cartagena hostages freed",
     "Troops storm the store; the siege begun Tuesday ends with one gunman dead."),
    (13, "13 · AFRICA · CONFLICT — REPORTED · REUTERS", "Sudan drones kill 19 civilians",
     "Tuesday's RSF strikes on two Blue Nile towns, reported Wednesday by lawyers."),
    (14, "14 · EUROPE · SPORT — REPORTED · FIDE", "Chess: Gukesh White in game 2",
     "After Tuesday's 38-move Berlin draw, the youngest title match resumes in Geneva."),
]
for i, (num, tag, head, sub) in enumerate(SMALL):
    panel(COLX[i % 4], ROWY[i // 4], COLW, ROWH, num, tag, head, sub, VIGS[num])

# ---------------------------------------------------------------- map + ALSO
BY = 732
d.rectangle([MX, BY, MX + 216, BY + 198], fill=PANEL_BG, outline=BORDER)
mt = "WHERE WEDNESDAY HAPPENED"
d.text((MX + 8, BY + 6), mt, font=SANS_B(8.5), fill=NAVY)
MAPX, MAPY, MAPW, MAPH = MX + 8, BY + 24, 200, 140
def lonlat(lon, lat):
    return (MAPX + (lon + 170) / 360 * MAPW, MAPY + (75 - lat) / 135 * MAPH)
CONT = [
    [(-168, 66), (-140, 70), (-125, 49), (-117, 33), (-97, 26), (-90, 21), (-86, 13), (-79, 9), (-81, 13), (-90, 14), (-105, 20), (-114, 29), (-125, 40), (-152, 60), (-168, 66)],
    [(-79, 9), (-77, -4), (-80, -9), (-75, -15), (-70, -19), (-70, -30), (-72, -40), (-74, -50), (-71, -54), (-66, -55), (-68, -45), (-65, -35), (-58, -28), (-49, -20), (-41, -10), (-35, -8), (-44, -3), (-50, 0), (-60, 5), (-68, 8), (-75, 10), (-79, 9)],
    [(-10, 36), (0, 39), (3, 43), (8, 44), (10, 46), (5, 50), (0, 51), (-2, 49), (-5, 44), (-9, 43), (-9, 37), (-10, 36)],
    [(20, 54), (30, 55), (45, 52), (60, 50), (75, 50), (90, 48), (105, 50), (120, 52), (135, 48), (142, 50), (150, 55), (160, 60), (170, 66), (178, 66), (178, 62), (160, 55), (140, 45), (130, 42), (122, 38), (121, 30), (110, 22), (108, 15), (105, 9), (100, 8), (98, 12), (92, 16), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25), (57, 26), (51, 28), (48, 30), (50, 25), (55, 25), (58, 23), (52, 17), (45, 12), (43, 12), (40, 15), (35, 28), (30, 31), (22, 37), (20, 40), (12, 44), (20, 54)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (44, 12), (40, -5), (40, -12), (37, -18), (35, -24), (32, -29), (27, -34), (20, -35), (17, -32), (15, -27), (12, -18), (13, -10), (9, -1), (9, 4), (-8, 5), (-13, 8), (-16, 12), (-17, 15), (-16, 21), (-13, 28), (-6, 35)],
    [(113, -22), (114, -34), (118, -35), (124, -33), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -30), (153, -25), (150, -22), (146, -19), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17), (117, -20), (113, -22)],
    [(95, 5), (100, 0), (105, -3), (110, -4), (115, -2), (120, 0), (125, 2), (130, 1), (135, 0), (140, -2), (145, -5), (150, -8), (155, -6), (160, -10), (165, -12), (170, -14), (175, -16), (178, -18), (172, -14), (165, -10), (155, -4), (145, 2), (135, 5), (125, 5), (115, 4), (105, 6), (95, 5)],
]
for poly in CONT:
    d.polygon([lonlat(lon, lat) for lon, lat in poly], fill=(216, 205, 175), outline=(170, 158, 125))
PINS = {1: (100.3, 40.9), 2: (126.9, 37.5), 3: (-77, 39), 4: (56.3, 26.5), 5: (34.3, 31.4),
        6: (37.6, 55.7), 7: (121.5, 31.2), 8: (4.35, 50.85), 9: (159.9, -9.4), 10: (-93.5, 42),
        11: (13.4, 52.5), 12: (-75.5, 10.4), 13: (34, 12), 14: (6.1, 46.2)}
OFF = {8: (-9, -6), 14: (6, 7), 5: (-6, 4)}
for n, (lon, lat) in PINS.items():
    px, py = lonlat(lon, lat)
    ox, oy = OFF.get(n, (0, 0)); px += ox; py += oy
    d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=RED, outline=(250, 246, 238))
    s = str(n); f7 = SANS_B(7)
    d.text((px - tw(d, s, f7) / 2, py - 4), s, font=f7, fill=(255, 255, 255))
d.text((MX + 8, BY + 170), "Pins: panel numbers. 11 = Berlin,", font=SANS(7.5), fill=MUTED)
d.text((MX + 8, BY + 181), "where Hera's pictures are shared.", font=SANS(7.5), fill=MUTED)

ALSO = [
    "Riyadh: Houthis claim refinery strike", "Dhaka: garment wage up 36% after protests",
    "London: energy cap jumps 26% to £2,166", "Murmansk: governor held in graft probe",
    "Athens: nationwide strike over wages", "Nairobi: Germany's president hosted by Ruto",
    "Berlin: Merz says Russia is escalating", "Moscow: Kremlin rejects Johnson call",
    "Rome: Italy rebukes Kyiv over Libya", "Amman: death sentence over killing",
    "Sydney: ex-policeman guilty of murders", "Kinshasa: army plane missing, rebels",
    "Dhaka: Hasina to return 16 December", "Harare: warrant for Mugabe's son",
    "Johannesburg: Ramaphosa wins in court", "Aden: Houthis advance, residents flee",
    "Kyiv: Hungarian PM's first visit in 15y", "Canberra: inflation jumps to 4.9%",
    "Sydney: platforms face 5% fines", "Tasmania: bushfire threatens homes",
    "Canberra: 14 hospitals change hands", "London: Compass lists in New York",
    "Washington: Pentagon audits base schools", "Washington: AG dodges Nvidia questions",
    "New York: parade balloons, wind watch", "Vatican: Pope Francis diary published",
    "Indonesia: mine flood traps 23, kills 3", "London: Afghan students lose visas",
    "Washington: Omar search files unsealed", "South Africa: Ukraine plot conviction",
    "Tennis: Sinner has minor knee surgery", "Delhi: food prices squeeze families",
    "Massachusetts: turkeys chase woman", "Norfolk: two charged over royal break-in",
    "Pyongyang: Swiss envoy expelled", "Oil: crude slips 1% on Wednesday",
]
AX = 258
d.text((AX, BY + 2), "ALSO ON WEDNESDAY 25 NOVEMBER", font=SANS_B(12.5), fill=NAVY)
d.line([(AX, BY + 20), (W - MX, BY + 20)], fill=BORDER)
colw = (W - MX - AX - 28) // 3
for i, item in enumerate(ALSO):
    cx = AX + (i // 12) * (colw + 14); cy = BY + 28 + (i % 12) * 13.2
    num = str(15 + i)
    d.text((cx, cy), num, font=SANS_B(9), fill=RED)
    d.text((cx + 16, cy), item, font=SANS(9), fill=INK)

# DATE CHECK band
DY = 946
d.rectangle([MX, DY, W - MX, DY + 34], fill=PANEL_BG, outline=BORDER)
d.rectangle([MX, DY, MX + 118, DY + 34], fill=RED)
dcl = "DATE CHECK"
d.text((MX + (118 - tw(d, dcl, SANS_B(10.5))) // 2, DY + 11), dcl, font=SANS_B(10.5), fill=(250, 246, 238))
dc = ("Tempting, everywhere today, but NOT this day: Senegal's Cup title came back Tuesday - the chess opener was "
      "Tuesday - Huawei's verdict was Tuesday - Sarkozy's trial order was Tuesday - Abrego Garcia flew out Tuesday - "
      "the turkey pardon was Tuesday - Villavicencio's car bomb was Monday - the landmine report landed Tuesday - "
      "Miley Cyrus married Saturday.")
for j, ln in enumerate(wrap(d, dc, SANS(9.5), 836)):
    d.text((MX + 130, DY + 4 + j * 13), ln, font=SANS(9.5), fill=INK)

foot1 = "Sources: Reuters, AP, AFP, BBC, The Guardian, ESA, Ofgem, FIDE and official statements, all dated Wednesday 25 November 2026. Claims by parties to a conflict are labelled as claims."
foot2 = "Built with Python + Pillow. One image, one day: Wednesday 25 November 2026."
d.text(((W - tw(d, foot1, SANS(8))) // 2, 986), foot1, font=SANS(8), fill=MUTED)
d.text(((W - tw(d, foot2, SANS(8))) // 2, 998), foot2, font=SANS(8), fill=MUTED)

# ---------------------------------------------------------------- fit audit
def check(label, text, font, width, lines_allowed):
    n = len(wrap(d, text, font, width))
    if n > lines_allowed:
        print(f"TRUNC-RISK {label}: wraps to {n} lines, only {lines_allowed} drawn")
check("lead head", "Pakistan's first astronaut rides a Chinese rocket", SANS_B(19), 562, 2)
check("lead sub", "Shenzhou-24 lifts off at 00:18 UTC carrying Muhammad Zeeshan Ali, who docks at Tiangong: the first foreigner aboard China's station, and the first Pakistani in orbit.", SANS(11), 562, 3)
check("p2 head", "AI rebound stumbles: Asia's chip shares slide", SANS_B(15.5), 374, 2)
check("p2 sub", "Seoul sinks 5.3% and Taipei 5.1% at the worst; Tokyo sheds 2.9% as tariff threats return and the tech rally fizzles.", SANS(10), 374, 3)
for num, tag, head, sub in SMALL:
    check(f"p{num} head", head, SANS_B(13), COLW - 14, 2)
    check(f"p{num} sub", sub, SANS(8.5), COLW - 14, 3)
for i, t in enumerate(tl_items):
    if tw(d, t, SANS(9)) > 210: print(f"TIMELINE-WIDE {i}: {t}")
for i, item in enumerate(ALSO):
    if tw(d, item, SANS(9)) > colw - 16: print(f"ALSO-WIDE {15 + i}: {item}")
if len(wrap(d, dc, SANS(9.5), 836)) > 2: print("DATECHECK wraps past 2 lines")
if tw(d, strap, SANS_B(13.5)) > W - 2 * MX: print("STRAP too wide")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
