#!/usr/bin/env python3
"""Generatore di card tipografiche Yattayo AI (1080x1350, JPEG, 4:5 per Instagram/Facebook).

Uso:
  python3 yattayo_card.py --fonts DIR --out card.jpg --title "..." [--kicker "..."] \
      [--subtitle "..."] [--cta "..."] [--theme violet|light|orange]

Font richiesti in DIR: Sora.ttf e DMSans.ttf (variabili, da github.com/google/fonts:
  ofl/sora/Sora[wght].ttf  e  ofl/dmsans/DMSans[opsz,wght].ttf)
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

VIOLET = (108, 60, 224)      # #6C3CE0
VIOLET_DK = (74, 36, 168)
ORANGE = (255, 107, 53)      # #FF6B35
WHITE = (255, 255, 255)
INK = (26, 18, 51)
LIGHT_BG = (246, 243, 255)

W, H = 1080, 1350
M = 90  # margine

THEMES = {
    "violet": dict(bg=VIOLET, bg2=VIOLET_DK, title=WHITE, text=(232, 225, 255), accent=ORANGE, cta_bg=ORANGE, cta_fg=WHITE, logo=WHITE),
    "light":  dict(bg=LIGHT_BG, bg2=(233, 226, 255), title=INK, text=(70, 60, 110), accent=VIOLET, cta_bg=VIOLET, cta_fg=WHITE, logo=VIOLET),
    "orange": dict(bg=ORANGE, bg2=(232, 84, 30), title=WHITE, text=(255, 236, 228), accent=VIOLET, cta_bg=VIOLET, cta_fg=WHITE, logo=WHITE),
}


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            name = a.get("name", b"")
            name = name.decode() if isinstance(name, bytes) else str(name)
            if name.lower().startswith("weight"):
                vals.append(weight)
            elif "optical" in name.lower():
                vals.append(min(max(size / 2, a["minimum"]), a["maximum"]))
            else:
                vals.append(a.get("default", a["minimum"]))
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def wrap(draw, text, f, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=f) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_title(draw, text, path, max_w, max_h, start=112, min_size=56):
    size = start
    while size >= min_size:
        f = font(path, size, 700)
        lines = wrap(draw, text, f, max_w)
        lh = int(size * 1.12)
        if len(lines) * lh <= max_h and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines, lh
        size -= 4
    f = font(path, min_size, 700)
    return f, wrap(draw, text, f, max_w), int(min_size * 1.12)


def render(args):
    th = THEMES[args.theme]
    sora = os.path.join(args.fonts, "Sora.ttf")
    dm = os.path.join(args.fonts, "DMSans.ttf")

    img = Image.new("RGB", (W, H), th["bg"])
    d = ImageDraw.Draw(img)

    # forme decorative
    d.ellipse([W - 420, -260, W + 260, 420], fill=th["bg2"])
    d.ellipse([-220, H - 360, 260, H + 120], fill=th["bg2"])
    d.rounded_rectangle([M, 250, M + 120, 262], radius=6, fill=th["accent"])

    # logo testuale
    lf = font(sora, 44, 800)
    d.text((M, 110), "yattayo", font=lf, fill=th["logo"])
    lw = d.textlength("yattayo", font=lf)
    d.text((M + lw, 110), ".ai", font=lf, fill=th["accent"] if args.theme != "orange" else VIOLET)

    y = 300
    if args.kicker:
        kf = font(dm, 34, 700)
        d.text((M, y), args.kicker.upper(), font=kf, fill=th["accent"] if args.theme == "light" else th["text"])
        y += 70

    # titolo
    cta_h = 120 if args.cta else 0
    sub_f = font(dm, 40, 450)
    sub_lines = wrap(d, args.subtitle, sub_f, W - 2 * M) if args.subtitle else []
    sub_h = len(sub_lines) * 56 + (40 if sub_lines else 0)
    avail = H - y - 120 - cta_h - sub_h - 60
    tf, tlines, tlh = fit_title(d, args.title, sora, W - 2 * M, avail)
    for l in tlines:
        d.text((M, y), l, font=tf, fill=th["title"])
        y += tlh
    y += 40

    for l in sub_lines:
        d.text((M, y), l, font=sub_f, fill=th["text"])
        y += 56

    # CTA in basso
    if args.cta:
        cf = font(dm, 38, 700)
        cw = d.textlength(args.cta, font=cf)
        bx, by = M, H - 120 - 96
        d.rounded_rectangle([bx, by, bx + cw + 80, by + 96], radius=48, fill=th["cta_bg"])
        d.text((bx + 40, by + 24), args.cta, font=cf, fill=th["cta_fg"])

    img.save(args.out, "JPEG", quality=90, optimize=True, progressive=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--fonts", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--kicker", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--cta", default="")
    p.add_argument("--theme", default="violet", choices=list(THEMES))
    render(p.parse_args())
