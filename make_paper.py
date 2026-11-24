#!/usr/bin/env python3
"""The Daily Compass — Monday 23 November 2026.

Renders the front page for the make.fun news-image-20261123 entry: the day
COP31 collapsed in Antalya without a deal, Ukraine's strike on a Russian
warship at a Libyan port, the weekend toll around Kyiv, and BepiColombo's
arrival at Mercury. Drawn with PIL only; writes entry.png next to itself.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 960, 1024
PAPER = (247, 243, 233)
INK = (26, 23, 18)
ACCENT = (140, 43, 29)
FAINT = (110, 102, 88)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, leading, fill=INK):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, y, text, fnt, fill=INK):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)
    return y


def rule(draw, y, weight=2):
    draw.line([(36, y), (W - 36, y)], fill=INK, width=weight)
    return y


def cracked_globe(draw, cx, cy, r):
    """A wireframe globe split by a jagged crack — the COP31 talks in one mark."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    for k in (0.35, 0.7):
        w = r * k
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=INK, width=1)
    for frac in (-0.55, 0.0, 0.55):
        yy = cy + int(r * frac)
        half = int(r * (1 - frac * frac) ** 0.5)
        draw.line([(cx - half, yy), (cx + half, yy)], fill=INK, width=1)
    crack = [(cx - 6, cy - r), (cx + 14, cy - r // 2), (cx - 10, cy - r // 6),
             (cx + 16, cy + r // 3), (cx - 4, cy + 2 * r // 3), (cx + 8, cy + r)]
    draw.line(crack, fill=ACCENT, width=5, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top strip -------------------------------------------------------
    d.text((36, 14), "Vol. V — No. 327", font=font(SANS, 17), fill=FAINT)
    right = "ANTALYA • KYIV • DARMSTADT"
    d.text((W - 36 - d.textlength(right, font=font(SANS, 17)), 14), right,
           font=font(SANS, 17), fill=FAINT)
    rule(d, 42, 1)

    # --- masthead --------------------------------------------------------
    size = 84
    while d.textlength("THE DAILY COMPASS", font=font(SERIF_B, size)) > W - 72:
        size -= 2
    centred(d, 52, "THE DAILY COMPASS", font(SERIF_B, size))
    rule(d, 146, 4)
    rule(d, 154, 1)
    centred(d, 162, "MONDAY, 23 NOVEMBER 2026", font(SANS_B, 25))
    centred(d, 192, "The day's news, on one page", font(SERIF_I, 19), fill=FAINT)
    rule(d, 222, 2)

    # --- lead ------------------------------------------------------------
    d.text((36, 236), "COP31  •  ANTALYA, TURKEY", font=font(SANS_B, 19), fill=ACCENT)
    y = para(d, (36, 262), "CLIMATE SUMMIT COLLAPSES WITHOUT A DEAL",
             font(SERIF_B, 49), W - 72, 52)
    y = para(d, (36, y + 4),
             "The longest COP in history ends in deadlock over two words — fossil fuels — "
             "as the EU and island states reject the Pact",
             font(SERIF_I, 21), W - 72, 26, fill=(60, 54, 44))

    cracked_globe(d, 140, y + 100, 76)
    lead = ("ANTALYA — The UN climate conference closed on Sunday without an agreement "
            "for the first time since Copenhagen in 2009, after two weeks of overtime "
            "talks that became the longest COP ever held. The meeting called to adopt the "
            "Antalya Pact broke up without consensus among 190-plus countries, as Saudi "
            "Arabia, Russia and other petrostates blocked any mention of moving away from "
            "fossil fuels, and the EU and island states rejected the text. The United "
            "States, which has quit international climate action under President Trump, "
            "took no part. “This has been the worst ever COP,” said Mohamed Adow of "
            "Power Shift Africa.")
    y = para(d, (248, y + 22), lead, font(SERIF, 17), W - 248 - 36, 22)
    rule(d, y + 14, 1)

    # --- three panels ------------------------------------------------------
    top = y + 28
    colw = (W - 72 - 2 * 24) // 3
    panels = [
        ("WAR WIDENS TO THE MEDITERRANEAN",
         "KYIV — President Zelenskyy announced that Ukrainian naval drones had destroyed "
         "a Russian warship at the Libyan port of Benghazi — the war's first strike in "
         "the Mediterranean."),
        ("AT LEAST 15 DEAD AROUND KYIV",
         "KYIV REGION — Russian bombardment killed at least 15 people around Kyiv over "
         "the weekend. In Dymer a drone partly destroyed an apartment block; a boy was "
         "pulled alive from the rubble, 14 still missing."),
        ("MERCURY, AFTER EIGHT YEARS",
         "DARMSTADT — The European–Japanese BepiColombo pair slipped into orbit around "
         "Mercury on Saturday, ending an eight-year cruise, controllers in Germany "
         "confirmed."),
    ]
    bottom = top
    for idx, (head, body) in enumerate(panels):
        x = 36 + idx * (colw + 24)
        hy = para(d, (x, top), head, font(SERIF_B, 18), colw, 22, fill=ACCENT)
        by = para(d, (x, hy + 6), body, font(SERIF, 14), colw, 19)
        bottom = max(bottom, by)
        if idx:
            d.line([(x - 12, top), (x - 12, bottom)], fill=FAINT, width=1)

    # --- briefs ------------------------------------------------------------
    by = bottom + 14
    rule(d, by, 2)
    d.text((36, by + 10), "THE DAY IN BRIEF", font=font(SANS_B, 19), fill=ACCENT)
    briefs = ("Asian tech shares fall further as the AI sell-off deepens  •  Euro-area "
              "inflation rises to 4.0%  •  Israel's Eisenkot brands West Bank settler "
              "arson “Jewish terrorism”  •  Bahrain says an Iranian attack on a civilian "
              "industrial facility injured two")
    by = para(d, (36, by + 36), briefs, font(SERIF, 15), W - 72, 20)
    rule(d, by + 10, 1)
    centred(d, by + 18, "The Daily Compass — Monday 23 November 2026 — Page 1 of 1",
            font(SANS, 15), fill=FAINT)
    print("final y:", by + 44)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
