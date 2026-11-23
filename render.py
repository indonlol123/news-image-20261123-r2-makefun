#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

One deterministic image: a newspaper front page with a lead story, three
section columns (war & security, politics & power, markets & tech) and a
sport / culture strip. No network, no randomness, no timestamps in the
output: the same input always renders the same bytes.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 84, 74)
NAVY = (18, 38, 66)
RED = (176, 30, 30)
BLUE = (28, 78, 138)
GOLD = (184, 134, 11)
RULE = (200, 192, 176)
SECTION_BG = (232, 226, 212)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
SERIF_B = FONT_DIR + "NotoSerif-Bold.ttf"
SANS_B = FONT_DIR + "NotoSans-Bold.ttf"
SANS = FONT_DIR + "NotoSans-Regular.ttf"
SANS_I = FONT_DIR + "NotoSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill, leading):
    """Draw wrapped text; return the y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels, a few land blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=NAVY, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    for dy in (-0.55, 0.55):
        y = cy + int(r * dy)
        half = int((r * r - (r * dy) ** 2) ** 0.5)
        draw.line([(cx - half, y), (cx + half, y)], fill=NAVY, width=2)
    # land masses, rough blobs
    draw.ellipse([cx - r * 0.75, cy - r * 0.6, cx - r * 0.15, cy - r * 0.1],
                 fill=RED)
    draw.ellipse([cx + r * 0.1, cy + r * 0.05, cx + r * 0.7, cy + r * 0.55],
                 fill=RED)
    draw.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.25, cy + r * 0.75],
                 fill=GOLD)


# ---------------------------------------------------------------- stories
LEAD_HEAD = "CLIMATE TALKS COLLAPSE IN ANTALYA"
LEAD_DECK = (
    "COP31 ends with no deal — the longest UN climate summit in history — "
    "after nearly 200 nations reject a draft that never names fossil fuels. "
    "The UN chief calls it \u201cdeeply disappointing\u201d; focus now shifts "
    "to COP32 in Addis Ababa."
)

# (headline, deck) per section
WAR = [
    ("Ukraine sinks Russian warship off Libya",
     "Seven sea drones hit the corvette Merkury in Benghazi; cargo ship MV Angara also struck."),
    ("Russian strike on Dymer kills 11",
     "A boy, 7, is pulled alive from the rubble of a Kyiv-region apartment block."),
    ("NATO in emergency session over missiles in Poland",
     "Three Russian Kh-101 cruise missiles fell in south-east Poland on Friday; Warsaw calls it a provocation."),
    ("Iran hits Bahrain and tankers in the Gulf",
     "Missiles and drones strike a Bahrain industrial site; three tankers attacked in the Strait of Hormuz."),
    ("Trump warns Iran\u2019s tankers: \u2018at the bottom of the sea\u2019",
     "US blockade pressure grows as fears of a Gulf clash rise."),
    ("Gaza \u2018a toxic wasteland\u2019, Oxfam warns",
     "Report finds contamination across 99% of Gaza; an Israeli strike on a truck kills three."),
    ("Russian cargo ship ablaze in the Baltic",
     "Sparta II drifts into Finnish waters after a suspected Ukrainian drone attack."),
]

POLITICS = [
    ("Democrats win 258 House seats \u2014 biggest since 1992",
     "A recount win over Rep. Virginia Foxx in North Carolina seals the majority; control from 3 January."),
    ("Trump moves to curb Congress oversight",
     "New order tells contractors to clear congressional requests with the White House first."),
    ("Trump signs law ending the penny",
     "The Common Cents Act closes the coin\u2019s 232-year run."),
    ("Netanyahu\u2013Eisenkot coalition talks fail",
     "Israel\u2019s government talks end with no deal; Eisenkot calls settler arson \u2018Jewish terrorism\u2019."),
    ("Armenia proposes new constitution for peace",
     "Step toward a deal with Azerbaijan; ground also breaks on the \u2018Trump Route\u2019 corridor."),
    ("Kenya and DR Congo restore ties",
     "Leaders agree to end tensions and respect each other\u2019s sovereignty."),
    ("China sets 2030 targets for care and children",
     "Beijing pledges more support for older people and young families."),
]

MARKETS = [
    ("AI rout: Nikkei -5.1%, Kospi -5.2%, Taiex -6.2%",
     "$12 trillion wiped from world stocks since October as AI-spending doubts spread."),
    ("Anthropic\u2019s Nasdaq debut fails to calm AI fears",
     "Shares jump 17% on debut, but the week\u2019s US rout still tops $4 trillion."),
    ("Nvidia scandal: aide \u2018in contact with Chinese spies\u2019",
     "Alice Huang kept in touch with a Chinese state-security official, US reports say; Trump backs Jensen Huang\u2019s return."),
    ("Delta outage delays 1,600 flights",
     "A weight-and-balance failure hits the Atlanta hub as Thanksgiving travel begins."),
    ("Belgian airports shut in austerity strike",
     "Air traffic control suspended as unions protest government cuts."),
    ("Catering giant to switch listing to US",
     "Another blow to London as a FTSE heavyweight eyes New York."),
    ("US Army to blow up explosives despite court order",
     "An unstable lead azide stockpile in Iowa is set to be detonated on Monday."),
]

LIFE = [
    ("Alcaraz beats Zverev to win first ATP Finals",
     "6\u20132, 7\u20136(7) in Turin; the Spaniard\u2019s sixth title of 2026."),
    ("Tyson Fury reveals schizophrenia diagnosis",
     "Boxer says he heard voices during a 2015 breakdown."),
    ("49ers rout Vikings 35\u201310 in Mexico City",
     "The NFL\u2019s first international Sunday Night Football game."),
    ("Candy factory fire in Banten kills 24",
     "About 30 still missing in Indonesia."),
    ("Record rain floods Belgrade",
     "Severe urban flooding in the Serbian capital."),
    ("New reports revisit Epstein\u2019s Russia links",
     "Fresh reporting challenges the official account."),
]

SECTIONS = [
    ("WAR & SECURITY", WAR, RED),
    ("POLITICS & POWER", POLITICS, NAVY),
    ("MARKETS, TECH & MONEY", MARKETS, BLUE),
]


def draw_story(draw, x, y, width, number, head, deck):
    """One numbered story block; returns the y below it."""
    num_f = font(SANS_B, 15)
    head_f = font(SANS_B, 15)
    deck_f = font(SANS, 12)
    draw.text((x, y), f"{number}.", font=num_f, fill=RED)
    num_w = draw.textlength(f"{number}. ", font=num_f)
    y = para(draw, (x + num_w, y), head, head_f, width - num_w, INK, 19)
    y = para(draw, (x + num_w, y + 1), deck, deck_f, width - num_w, MUTED, 15)
    return y + 8


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.text((mx, 10), "THE WORLD IN A DAY", font=font(SERIF_B, 52), fill=(255, 255, 255))
    d.text((mx, 68), "MONDAY  23  NOVEMBER  2026",
           font=font(SANS_B, 16), fill=(255, 214, 90))
    right = "ONE DAY \u00b7 THE WHOLE WORLD"
    d.text((W - mx - d.textlength(right, font=font(SANS_B, 14)), 72),
           right, font=font(SANS_B, 14), fill=(200, 210, 225))
    d.line([(0, 92), (W, 92)], fill=RED, width=4)

    # ---- lead story ----------------------------------------------------
    y = 108
    d.text((mx, y), "LEAD STORY \u2014 CLIMATE", font=font(SANS_B, 14), fill=RED)
    y += 22
    lead_w = W - 2 * mx - 150
    y = para(d, (mx, y), LEAD_HEAD, font(SERIF_B, 38), lead_w, INK, 44)
    y = para(d, (mx, y + 4), LEAD_DECK, font(SANS, 15), lead_w, MUTED, 20)
    draw_globe(d, W - mx - 62, 176, 58)
    rule(d, mx, 272, W - mx, width=2, fill=INK)

    # ---- three section columns -----------------------------------------
    col_gap = 16
    col_w = (W - 2 * mx - 2 * col_gap) // 3
    top = 286
    for i, (title, stories, color) in enumerate(SECTIONS):
        x = mx + i * (col_w + col_gap)
        d.rectangle([x, top, x + col_w, top + 30], fill=color)
        d.text((x + 10, top + 6), title, font=font(SANS_B, 15),
               fill=(255, 255, 255))
        sy = top + 42
        for n, (head, deck) in enumerate(stories, 1):
            sy = draw_story(d, x, sy, col_w, n, head, deck)
            if n < len(stories):
                rule(d, x, sy - 4, x + col_w)
        # column bottom rule
        rule(d, x, 838, x + col_w, width=2, fill=INK)

    # ---- sport / culture strip -----------------------------------------
    y = 852
    d.rectangle([mx, y, W - mx, y + 28], fill=GOLD)
    d.text((mx + 10, y + 5), "SPORT, CULTURE & LIFE", font=font(SANS_B, 15),
           fill=(255, 255, 255))
    y += 38
    cell_w = (W - 2 * mx - 2 * col_gap) // 3
    for idx, (head, deck) in enumerate(LIFE):
        row, col = divmod(idx, 3)
        x = mx + col * (cell_w + col_gap)
        cy = y + row * 56
        cy = para(d, (x, cy), head, font(SANS_B, 13), cell_w, INK, 16)
        para(d, (x, cy + 1), deck, font(SANS, 11), cell_w, MUTED, 14)

    # ---- footer ---------------------------------------------------------
    rule(d, mx, 980, W - mx, width=2, fill=INK)
    foot = ("Sources: Reuters, AP, BBC, CNN, UN News, ATP Tour  \u00b7  "
            "All events happened or were first reported on 23 November 2026  \u00b7  "
            "make.fun bounty news-image-20261123")
    d.text((mx, 990), foot, font=font(SANS_I, 11), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
