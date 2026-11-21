#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news summary image (entry.png, 1024x1024).

Flat broadsheet style, drawn entirely with Pillow primitives so every word
stays crisp: a masthead naming the day, one lead story, four panels and a
ticker strip. The stories are the day's most consequential, as reported on
20 November 2026 by Open Chronicle's Global News Brief, Informed Clearly's
daily summary, the Virginia Times daily recap and KLZ's Daily Brief:

- the joint peace declaration after the Trump-Xi-Putin summit in Shenzhen
- Russia's barrage of 400+ drones and 110 missiles on Ukraine, with two
  missiles falling inside Poland
- the ICJ ruling that Myanmar committed genocide against the Rohingya
- Anthropic's record-breaking IPO ($81 billion raised, shares up 33%)
- the nine-hour worldwide Microsoft 365 outage
- ticker: GTA VI's launch, the EU-UK Brussels summit, the Haiti raid that
  killed 34 gang suspects, and a tanker struck in the Strait of Hormuz

This script needs Pillow and is only the artwork source; the entered program
is main.py, which copies the rendered entry.png into the output directory.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
PANEL = (255, 253, 247)
INK = (20, 24, 31)
RED = (179, 35, 42)
NAVY = (29, 58, 110)
GOLD = (176, 141, 32)
GREY = (92, 96, 104)

FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
# DejaVu ships with most Linux desktops and CI images; the entered program
# (main.py) does not need it — only this artwork source does.


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        trial = (cur + ' ' + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.12, align='left'):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    lh = int(fnt.size * leading)
    for ln in lines:
        w_ = draw.textlength(ln, font=fnt)
        dx = x if align == 'left' else x + (max_w - w_) / 2
        draw.text((dx, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, box, tag, tag_color):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=PANEL, outline=INK, width=3)
    draw.rounded_rectangle([x0, y0, x0 + 118, y0 + 40], radius=10, fill=tag_color)
    draw.rectangle([x0, y0 + 22, x0 + 118, y0 + 40], fill=tag_color)
    draw.text((x0 + 12, y0 + 9), tag, font=font(FB, 21), fill=(255, 255, 255))


def icon_flags(draw, cx, cy):
    """Three simplified flags: USA, China, Russia."""
    w_, h_ = 62, 44
    x = cx - (3 * w_ + 16) // 2
    for i in range(3):
        fx = x + i * (w_ + 8)
        draw.rounded_rectangle([fx, cy - h_ // 2, fx + w_, cy + h_ // 2], radius=5, outline=INK, width=2)
        if i == 0:
            for s in range(4):
                col = RED if s % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx + 2, cy - h_ // 2 + 2 + s * 10, fx + w_ - 2, cy - h_ // 2 + 12 + s * 10], fill=col)
            draw.rectangle([fx + 2, cy - h_ // 2 + 2, fx + 28, cy - 2], fill=NAVY)
        elif i == 1:
            draw.rectangle([fx + 2, cy - h_ // 2 + 2, fx + w_ - 2, cy + h_ // 2 - 2], fill=RED)
            draw.ellipse([fx + 8, cy - 14, fx + 18, cy - 4], fill=GOLD)
            for dx, dy in [(22, -16), (26, -8), (26, 2), (21, 10)]:
                draw.ellipse([fx + dx, cy + dy, fx + dx + 5, cy + dy + 5], fill=GOLD)
        else:
            draw.rectangle([fx + 2, cy - h_ // 2 + 2, fx + w_ - 2, cy - 8], fill=(255, 255, 255))
            draw.rectangle([fx + 2, cy - 8, fx + w_ - 2, cy + 6], fill=NAVY)
            draw.rectangle([fx + 2, cy + 6, fx + w_ - 2, cy + h_ // 2 - 2], fill=RED)


def icon_drone(draw, cx, cy):
    draw.line([cx - 34, cy - 22, cx + 34, cy + 22], fill=INK, width=7)
    draw.line([cx - 34, cy + 22, cx + 34, cy - 22], fill=INK, width=7)
    for dx, dy in [(-38, -26), (38, -26), (-38, 26), (38, 26)]:
        draw.ellipse([cx + dx - 13, cy + dy - 6, cx + dx + 13, cy + dy + 6], outline=INK, width=4)
    draw.rounded_rectangle([cx - 14, cy - 11, cx + 14, cy + 11], radius=6, fill=INK)


def icon_scales(draw, cx, cy):
    draw.line([cx, cy - 40, cx, cy + 34], fill=INK, width=6)
    draw.line([cx - 44, cy - 28, cx + 44, cy - 28], fill=INK, width=6)
    draw.ellipse([cx - 8, cy - 50, cx + 8, cy - 34], fill=GOLD, outline=INK, width=2)
    for sx in (-44, 44):
        draw.line([cx + sx, cy - 28, cx + sx - 15, cy + 8], fill=INK, width=3)
        draw.line([cx + sx, cy - 28, cx + sx + 15, cy + 8], fill=INK, width=3)
        draw.arc([cx + sx - 17, cy - 2, cx + sx + 17, cy + 22], start=0, end=180, fill=INK, width=4)
    draw.rectangle([cx - 26, cy + 34, cx + 26, cy + 42], fill=INK)


def icon_chip(draw, cx, cy):
    for i in range(-2, 3):
        draw.line([cx + i * 16, cy - 52, cx + i * 16, cy - 36], fill=INK, width=5)
        draw.line([cx + i * 16, cy + 36, cx + i * 16, cy + 52], fill=INK, width=5)
        draw.line([cx - 52, cy + i * 16, cx - 36, cy + i * 16], fill=INK, width=5)
        draw.line([cx + 36, cy + i * 16, cx + 52, cy + i * 16], fill=INK, width=5)
    draw.rounded_rectangle([cx - 36, cy - 36, cx + 36, cy + 36], radius=10, fill=NAVY, outline=INK, width=3)
    t = 'AI'
    f = font(FB, 34)
    draw.text((cx - draw.textlength(t, font=f) / 2, cy - 20), t, font=f, fill=(255, 255, 255))


def icon_cloud(draw, cx, cy):
    draw.ellipse([cx - 48, cy - 14, cx - 4, cy + 30], fill=(198, 214, 235), outline=INK, width=3)
    draw.ellipse([cx - 26, cy - 34, cx + 24, cy + 30], fill=(198, 214, 235), outline=INK, width=3)
    draw.ellipse([cx + 2, cy - 16, cx + 50, cy + 30], fill=(198, 214, 235), outline=INK, width=3)
    draw.rectangle([cx - 44, cy + 8, cx + 46, cy + 30], fill=(198, 214, 235))
    draw.line([cx - 44, cy + 30, cx + 46, cy + 30], fill=INK, width=3)
    draw.polygon([(cx + 8, cy - 2), (cx - 8, cy + 26), (cx + 2, cy + 26), (cx - 6, cy + 50),
                  (cx + 22, cy + 16), (cx + 10, cy + 16)], fill=RED, outline=INK)


def main():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    t = 'THE WORLD IN ONE DAY'
    f = font(FR, 47)
    d.text(((W - d.textlength(t, font=f)) / 2, 24), t, font=f, fill=INK)
    t = 'FRIDAY, 20 NOVEMBER 2026'
    f = font(FB, 55)
    d.text(((W - d.textlength(t, font=f)) / 2, 84), t, font=f, fill=RED)
    d.line([36, 158, W - 36, 158], fill=INK, width=5)
    d.line([36, 166, W - 36, 166], fill=INK, width=2)

    # Lead story: Shenzhen summit
    panel(d, [36, 182, W - 36, 428], 'SUMMIT', NAVY)
    icon_flags(d, 512, 232)
    text_block(d, (70, 262), 'TRUMP, XI & PUTIN ISSUE A JOINT PEACE DECLARATION',
               font(FB, 39), INK, 884, align='center')
    text_block(d, (70, 352), 'Historic three-power summit in Shenzhen pledges talks on cutting nuclear risk',
               font(FS, 25), GREY, 884, align='center')

    # Row 1: Ukraine / World Court
    panel(d, [36, 444, 504, 692], 'UKRAINE', RED)
    icon_drone(d, 130, 520)
    text_block(d, (196, 466), 'RUSSIA FIRES 400+ DRONES, 110 MISSILES',
               font(FB, 27), INK, 288)
    text_block(d, (60, 618), 'Kyiv power plants hit, eight killed; two missiles land in Poland.',
               font(FS, 23), GREY, 420)

    panel(d, [520, 444, 988, 692], 'JUSTICE', GOLD)
    icon_scales(d, 614, 526)
    text_block(d, (712, 466), 'WORLD COURT: MYANMAR COMMITTED GENOCIDE',
               font(FB, 27), INK, 252)
    text_block(d, (544, 618), 'Landmark ICJ ruling on the genocide of the Rohingya.',
               font(FS, 23), GREY, 420)

    # Row 2: Anthropic IPO / Microsoft outage
    panel(d, [36, 708, 504, 916], 'MARKETS', NAVY)
    icon_chip(d, 130, 790)
    text_block(d, (196, 730), "ANTHROPIC'S IPO IS THE BIGGEST EVER",
               font(FB, 27), INK, 288)
    text_block(d, (60, 842), '$81 billion raised; shares leap 33% on debut.',
               font(FS, 23), GREY, 420)

    panel(d, [520, 708, 988, 916], 'TECH', RED)
    icon_cloud(d, 614, 790)
    text_block(d, (712, 730), 'MICROSOFT 365 OUTAGE HITS WORLD',
               font(FB, 27), INK, 252)
    text_block(d, (544, 842), 'Outlook and Teams down for nine hours across the globe.',
               font(FS, 23), GREY, 420)

    # Ticker
    d.line([36, 936, W - 36, 936], fill=INK, width=3)
    text_block(d, (36, 948),
               'ALSO TODAY:  GTA VI launches after 13 years, breaking pre-order records  •  '
               'EU–UK summit in Brussels  •  Haiti raid kills 34 gang suspects  •  '
               'Tanker struck by projectile in the Strait of Hormuz',
               font(FS, 22), INK, 952)

    out = Path(__file__).with_name('entry.png')
    img.save(out, optimize=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
