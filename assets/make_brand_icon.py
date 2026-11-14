#!/usr/bin/env python3
"""Generate Asad Bukhari / Asad Digital Labs brand icon.
Navy rounded square (#0b1b33 -> #14315e gradient), gold 'AB' monogram.
Outputs: brand-icon-512.png, favicon-192.png, favicon-32.png,
apple-touch-icon.png (180), favicon.ico (16/32/48).
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

OUT = pathlib.Path(__file__).parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NAVY_TOP = (11, 27, 51)
NAVY_BOT = (20, 49, 94)
GOLD = (232, 193, 90)

def make(size, radius_frac=0.22, supersample=2):
    S = size * supersample
    img = Image.new("RGB", (S, S))
    d = ImageDraw.Draw(img)
    # diagonal gradient
    for y in range(S):
        t = y / S
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (S, y)], fill=c)
    # subtle gold ring inset
    ring = max(2, S // 128)
    d.rounded_rectangle([S*0.045, S*0.045, S*0.955, S*0.955],
                        radius=int(S*radius_frac), outline=(232, 193, 90, 90), width=ring)
    # AB monogram
    font_size = int(S * 0.42)
    font = ImageFont.truetype(FONT, font_size)
    text = "AB"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((S-tw)/2 - bbox[0], (S-th)/2 - bbox[1] - S*0.02),
           text, font=font, fill=GOLD)
    # gold underline bar under AB
    bar_w = int(S * 0.34)
    bar_h = max(4, int(S * 0.018))
    bar_y = int(S * 0.74)
    d.rounded_rectangle([(S-bar_w)/2, bar_y, (S+bar_w)/2, bar_y+bar_h],
                        radius=bar_h//2, fill=GOLD)
    img = img.resize((size, size), Image.LANCZOS)
    # rounded corners mask (transparent outside)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, size, size], radius=int(size*radius_frac), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out

def make_square(size):
    """Apple touch / WP site icon: solid square, no transparent corners."""
    S = size * 2
    img = Image.new("RGB", (S, S))
    d = ImageDraw.Draw(img)
    for y in range(S):
        t = y / S
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (S, y)], fill=c)
    font = ImageFont.truetype(FONT, int(S * 0.42))
    bbox = d.textbbox((0, 0), "AB", font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((S-tw)/2 - bbox[0], (S-th)/2 - bbox[1] - S*0.02), "AB", font=font, fill=GOLD)
    bar_w, bar_h = int(S*0.34), max(4, int(S*0.018))
    bar_y = int(S*0.74)
    d.rounded_rectangle([(S-bar_w)/2, bar_y, (S+bar_w)/2, bar_y+bar_h], radius=bar_h//2, fill=GOLD)
    return img.resize((size, size), Image.LANCZOS)

icon512 = make(512)
icon512.save(OUT / "brand-icon-512.png")
make(192).save(OUT / "favicon-192.png")
make(32).save(OUT / "favicon-32.png")
make_square(180).save(OUT / "apple-touch-icon.png")
make_square(512).save(OUT / "brand-icon-512-square.png")
# favicon.ico with 16/32/48
ico = make_square(48)
ico.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("done", sorted(p.name for p in OUT.glob("*icon*")) + ["favicon.ico"])
