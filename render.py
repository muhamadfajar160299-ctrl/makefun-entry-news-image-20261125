#!/usr/bin/env python3
"""Render the one-day world news image for Wednesday 25 November 2026.

Draws a dense cream broadsheet (1024x1024) with PIL only. Every story
below was checked against news reported on 25 November 2026; claims that
are one side's assertion are marked with a hollow dot. The output is
deterministic: same input, same bytes.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 235)
INK = (26, 26, 26)
NAVY = (20, 38, 78)
NAVY_LT = (38, 64, 120)
RED = (166, 30, 34)
GOLD = (176, 132, 40)
TEAL = (14, 110, 110)
GREY = (96, 94, 88)
RULE = (60, 58, 52)
CARD_BG = (255, 252, 244)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_R = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, max_lines=None):
    """Draw wrapped lines; returns y after the last line drawn."""
    if leading is None:
        leading = fnt.size + 3
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
# Each icon draws a small flat scene inside a coloured panel (x, y, s).
# All shapes are original programmatic drawings, no photographs.

def _panel(draw, x, y, s, bg):
    draw.rectangle([x, y, x + s, y + s], fill=bg)


def icon_tanker(draw, x, y, s):
    _panel(draw, x, y, s, (24, 68, 110))
    u = s / 52.0
    draw.rectangle([x + 6 * u, y + 26 * u, x + 46 * u, y + 36 * u], fill=(200, 60, 40))
    draw.rectangle([x + 34 * u, y + 16 * u, x + 44 * u, y + 26 * u], fill=(240, 240, 230))
    draw.rectangle([x + 10 * u, y + 20 * u, x + 16 * u, y + 26 * u], fill=(250, 200, 60))
    draw.rectangle([x + 19 * u, y + 20 * u, x + 25 * u, y + 26 * u], fill=(250, 200, 60))
    draw.polygon([(x + 40 * u, y + 8 * u), (x + 44 * u, y + 14 * u),
                  (x + 36 * u, y + 14 * u)], fill=(255, 150, 40))
    draw.ellipse([x + 37 * u, y + 5 * u, x + 43 * u, y + 11 * u], fill=(255, 200, 60))
    for i, wx in enumerate((4, 20, 36)):
        draw.arc([x + wx * u, y + 40 * u, x + (wx + 12) * u, y + 48 * u],
                 0, 180, fill=(180, 220, 240), width=max(1, int(2 * u)))


def icon_chart(draw, x, y, s):
    _panel(draw, x, y, s, (30, 30, 34))
    u = s / 52.0
    draw.line([(x + 8 * u, y + 44 * u), (x + 8 * u, y + 8 * u)], fill=(240, 240, 230), width=2)
    draw.line([(x + 8 * u, y + 44 * u), (x + 46 * u, y + 44 * u)], fill=(240, 240, 230), width=2)
    pts = [(10, 14), (18, 20), (26, 18), (34, 30), (42, 38)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        draw.line([(x + ax * u, y + ay * u), (x + bx * u, y + by * u)],
                  fill=(230, 60, 50), width=3)
    draw.polygon([(x + 42 * u, y + 38 * u), (x + 46 * u, y + 38 * u),
                  (x + 44 * u, y + 44 * u)], fill=(230, 60, 50))


def icon_rocket(draw, x, y, s):
    _panel(draw, x, y, s, (16, 28, 66))
    u = s / 52.0
    for sx, sy in ((10, 10), (40, 8), (44, 30), (8, 34), (24, 6)):
        draw.ellipse([x + sx * u, y + sy * u, x + (sx + 2) * u, y + (sy + 2) * u],
                     fill=(255, 255, 255))
    draw.polygon([(x + 26 * u, y + 6 * u), (x + 32 * u, y + 18 * u),
                  (x + 20 * u, y + 18 * u)], fill=(240, 240, 230))
    draw.rectangle([x + 20 * u, y + 18 * u, x + 32 * u, y + 36 * u], fill=(240, 240, 230))
    draw.ellipse([x + 23 * u, y + 22 * u, x + 29 * u, y + 28 * u], fill=(90, 180, 230))
    draw.polygon([(x + 20 * u, y + 36 * u), (x + 14 * u, y + 42 * u),
                  (x + 20 * u, y + 40 * u)], fill=(230, 60, 50))
    draw.polygon([(x + 32 * u, y + 36 * u), (x + 38 * u, y + 42 * u),
                  (x + 32 * u, y + 40 * u)], fill=(230, 60, 50))
    draw.polygon([(x + 24 * u, y + 36 * u), (x + 28 * u, y + 36 * u),
                  (x + 26 * u, y + 46 * u)], fill=(255, 170, 40))


def icon_refinery(draw, x, y, s):
    _panel(draw, x, y, s, (120, 60, 20))
    u = s / 52.0
    draw.rectangle([x + 8 * u, y + 22 * u, x + 16 * u, y + 46 * u], fill=(60, 50, 44))
    draw.rectangle([x + 20 * u, y + 14 * u, x + 26 * u, y + 46 * u], fill=(60, 50, 44))
    draw.rectangle([x + 30 * u, y + 28 * u, x + 44 * u, y + 46 * u], fill=(60, 50, 44))
    draw.polygon([(x + 22 * u, y + 4 * u), (x + 26 * u, y + 10 * u),
                  (x + 18 * u, y + 10 * u)], fill=(255, 150, 40))
    draw.ellipse([x + 20 * u, y + 2 * u, x + 25 * u, y + 7 * u], fill=(255, 210, 80))
    draw.ellipse([x + 34 * u, y + 8 * u, x + 42 * u, y + 16 * u], fill=(220, 220, 210))
    draw.ellipse([x + 38 * u, y + 4 * u, x + 46 * u, y + 12 * u], fill=(200, 200, 190))


def icon_tower(draw, x, y, s):
    _panel(draw, x, y, s, (52, 66, 96))
    u = s / 52.0
    draw.rectangle([x + 20 * u, y + 10 * u, x + 32 * u, y + 46 * u], fill=(200, 205, 215))
    for wy in (14, 20, 26, 32, 38):
        draw.rectangle([x + 22 * u, y + wy * u, x + 25 * u, y + (wy + 3) * u], fill=(30, 40, 60))
        draw.rectangle([x + 27 * u, y + wy * u, x + 30 * u, y + (wy + 3) * u], fill=(30, 40, 60))
    draw.polygon([(x + 33 * u, y + 16 * u), (x + 40 * u, y + 20 * u),
                  (x + 33 * u, y + 24 * u)], fill=(255, 170, 40))
    draw.ellipse([x + 38 * u, y + 16 * u, x + 45 * u, y + 23 * u], fill=(255, 210, 80))
    draw.rectangle([x + 8 * u, y + 44 * u, x + 44 * u, y + 46 * u], fill=(30, 40, 60))


def icon_target(draw, x, y, s):
    _panel(draw, x, y, s, (90, 30, 30))
    u = s / 52.0
    draw.ellipse([x + 12 * u, y + 12 * u, x + 40 * u, y + 40 * u], outline=(255, 255, 255), width=3)
    draw.ellipse([x + 20 * u, y + 20 * u, x + 32 * u, y + 32 * u], fill=(255, 255, 255))
    draw.line([(x + 26 * u, y + 6 * u), (x + 26 * u, y + 46 * u)], fill=(255, 255, 255), width=2)
    draw.line([(x + 6 * u, y + 26 * u), (x + 46 * u, y + 26 * u)], fill=(255, 255, 255), width=2)


def icon_drone(draw, x, y, s):
    _panel(draw, x, y, s, (58, 58, 60))
    u = s / 52.0
    draw.ellipse([x + 22 * u, y + 20 * u, x + 30 * u, y + 28 * u], fill=(220, 220, 210))
    for cx, cy in ((12, 12), (40, 12), (12, 36), (40, 36)):
        draw.line([(x + 26 * u, y + 24 * u), (x + cx * u, y + cy * u)], fill=(220, 220, 210), width=2)
        draw.ellipse([x + (cx - 5) * u, y + (cy - 2) * u, x + (cx + 5) * u, y + (cy + 2) * u],
                     fill=(180, 180, 170))
    draw.ellipse([x + 24 * u, y + 30 * u, x + 28 * u, y + 34 * u], fill=(255, 170, 40))


def icon_treaty(draw, x, y, s):
    _panel(draw, x, y, s, (16, 90, 70))
    u = s / 52.0
    draw.rectangle([x + 12 * u, y + 10 * u, x + 40 * u, y + 42 * u], fill=(250, 248, 235))
    draw.line([(x + 16 * u, y + 16 * u), (x + 36 * u, y + 16 * u)], fill=(40, 40, 40), width=2)
    draw.line([(x + 16 * u, y + 22 * u), (x + 36 * u, y + 22 * u)], fill=(40, 40, 40), width=2)
    draw.line([(x + 16 * u, y + 28 * u), (x + 30 * u, y + 28 * u)], fill=(40, 40, 40), width=2)
    draw.ellipse([x + 30 * u, y + 32 * u, x + 42 * u, y + 44 * u], fill=(166, 30, 34))
    draw.ellipse([x + 33 * u, y + 35 * u, x + 39 * u, y + 41 * u], fill=(250, 248, 235))


def icon_gavel(draw, x, y, s):
    _panel(draw, x, y, s, (70, 54, 30))
    u = s / 52.0
    draw.line([(x + 14 * u, y + 38 * u), (x + 38 * u, y + 14 * u)], fill=(220, 180, 120), width=4)
    draw.rectangle([x + 30 * u, y + 8 * u, x + 44 * u, y + 16 * u], fill=(180, 140, 80))
    draw.rectangle([x + 10 * u, y + 40 * u, x + 38 * u, y + 46 * u], fill=(120, 90, 50))


def icon_cyber(draw, x, y, s):
    _panel(draw, x, y, s, (20, 40, 60))
    u = s / 52.0
    draw.rectangle([x + 10 * u, y + 12 * u, x + 42 * u, y + 36 * u], fill=(220, 225, 235))
    draw.rectangle([x + 8 * u, y + 38 * u, x + 44 * u, y + 42 * u], fill=(160, 165, 175))
    draw.polygon([(x + 26 * u, y + 16 * u), (x + 30 * u, y + 26 * u),
                  (x + 22 * u, y + 26 * u)], fill=(230, 60, 50))
    draw.rectangle([x + 25 * u, y + 28 * u, x + 27 * u, y + 32 * u], fill=(230, 60, 50))


def icon_fire(draw, x, y, s):
    _panel(draw, x, y, s, (140, 40, 20))
    u = s / 52.0
    draw.rectangle([x + 8 * u, y + 30 * u, x + 44 * u, y + 40 * u], fill=(60, 55, 50))
    draw.ellipse([x + 14 * u, y + 32 * u, x + 20 * u, y + 38 * u], fill=(30, 30, 30))
    draw.ellipse([x + 32 * u, y + 32 * u, x + 38 * u, y + 38 * u], fill=(30, 30, 30))
    draw.polygon([(x + 24 * u, y + 8 * u), (x + 32 * u, y + 22 * u),
                  (x + 28 * u, y + 30 * u), (x + 20 * u, y + 30 * u),
                  (x + 16 * u, y + 22 * u)], fill=(255, 150, 40))
    draw.polygon([(x + 25 * u, y + 18 * u), (x + 29 * u, y + 26 * u),
                  (x + 22 * u, y + 26 * u)], fill=(255, 220, 80))


def icon_wage(draw, x, y, s):
    _panel(draw, x, y, s, (30, 100, 60))
    u = s / 52.0
    draw.rectangle([x + 8 * u, y + 18 * u, x + 44 * u, y + 36 * u], fill=(230, 225, 190))
    draw.ellipse([x + 21 * u, y + 22 * u, x + 31 * u, y + 32 * u], outline=(30, 100, 60), width=2)
    draw.text((x + 24 * u, y + 23 * u), "$", font=SANSB(10), fill=(30, 100, 60))
    draw.line([(x + 12 * u, y + 12 * u), (x + 12 * u, y + 6 * u), (x + 18 * u, y + 6 * u)],
              fill=(255, 255, 255), width=3)
    draw.polygon([(x + 40 * u, y + 4 * u), (x + 44 * u, y + 10 * u),
                  (x + 36 * u, y + 10 * u)], fill=(255, 255, 255))


def icon_climate(draw, x, y, s):
    _panel(draw, x, y, s, (14, 110, 110))
    u = s / 52.0
    draw.ellipse([x + 10 * u, y + 10 * u, x + 42 * u, y + 42 * u], fill=(90, 180, 120))
    draw.ellipse([x + 16 * u, y + 16 * u, x + 26 * u, y + 24 * u], fill=(40, 120, 70))
    draw.ellipse([x + 28 * u, y + 28 * u, x + 38 * u, y + 36 * u], fill=(40, 120, 70))
    draw.line([(x + 46 * u, y + 8 * u), (x + 46 * u, y + 34 * u)], fill=(230, 60, 50), width=3)
    draw.ellipse([x + 43 * u, y + 34 * u, x + 49 * u, y + 40 * u], fill=(230, 60, 50))


def icon_ball(draw, x, y, s):
    _panel(draw, x, y, s, (20, 90, 40))
    u = s / 52.0
    draw.ellipse([x + 10 * u, y + 10 * u, x + 42 * u, y + 42 * u], fill=(250, 250, 245))
    draw.polygon([(x + 26 * u, y + 20 * u), (x + 31 * u, y + 24 * u),
                  (x + 29 * u, y + 30 * u), (x + 23 * u, y + 30 * u),
                  (x + 21 * u, y + 24 * u)], fill=(30, 30, 30))
    for (ax, ay) in ((26, 20), (31, 24), (29, 30), (23, 30), (21, 24)):
        draw.line([(x + ax * u, y + ay * u), (x + 26 * u, y + 26 * u)], fill=(30, 30, 30), width=1)
    draw.rectangle([x + 8 * u, y + 44 * u, x + 44 * u, y + 46 * u], fill=(255, 255, 255))


def icon_racket(draw, x, y, s):
    _panel(draw, x, y, s, (110, 40, 90))
    u = s / 52.0
    draw.ellipse([x + 14 * u, y + 8 * u, x + 36 * u, y + 30 * u], outline=(250, 250, 245), width=3)
    draw.line([(x + 20 * u, y + 8 * u), (x + 20 * u, y + 30 * u)], fill=(250, 250, 245), width=1)
    draw.line([(x + 25 * u, y + 8 * u), (x + 25 * u, y + 30 * u)], fill=(250, 250, 245), width=1)
    draw.line([(x + 30 * u, y + 8 * u), (x + 30 * u, y + 30 * u)], fill=(250, 250, 245), width=1)
    draw.line([(x + 14 * u, y + 15 * u), (x + 36 * u, y + 15 * u)], fill=(250, 250, 245), width=1)
    draw.line([(x + 14 * u, y + 22 * u), (x + 36 * u, y + 22 * u)], fill=(250, 250, 245), width=1)
    draw.line([(x + 25 * u, y + 30 * u), (x + 34 * u, y + 46 * u)], fill=(220, 180, 120), width=4)
    draw.ellipse([x + 38 * u, y + 36 * u, x + 46 * u, y + 44 * u], fill=(220, 230, 60))


def icon_sudan(draw, x, y, s):
    _panel(draw, x, y, s, (150, 110, 40))
    u = s / 52.0
    draw.rectangle([x + 10 * u, y + 34 * u, x + 42 * u, y + 44 * u], fill=(120, 90, 60))
    draw.rectangle([x + 14 * u, y + 24 * u, x + 24 * u, y + 34 * u], fill=(90, 70, 50))
    draw.rectangle([x + 30 * u, y + 28 * u, x + 38 * u, y + 34 * u], fill=(90, 70, 50))
    draw.polygon([(x + 26 * u, y + 6 * u), (x + 31 * u, y + 16 * u),
                  (x + 21 * u, y + 16 * u)], fill=(230, 60, 50))
    draw.ellipse([x + 36 * u, y + 8 * u, x + 44 * u, y + 16 * u], fill=(230, 230, 220))


ICONS = {
    "tanker": icon_tanker, "chart": icon_chart, "rocket": icon_rocket,
    "refinery": icon_refinery, "tower": icon_tower, "target": icon_target,
    "drone": icon_drone, "treaty": icon_treaty, "gavel": icon_gavel,
    "cyber": icon_cyber, "fire": icon_fire, "wage": icon_wage,
    "climate": icon_climate, "ball": icon_ball, "racket": icon_racket,
    "sudan": icon_sudan,
}

# ------------------------------------------------------------------ data
# 31 stories, all reported on Wednesday 25 November 2026 (UTC).
# "(Tue)" = happened on Tuesday 24 Nov, first reported on Wednesday.
# Claims asserted by one side only carry the hollow-dot marker in text.

LEADS = [
    {
        "kicker": "IRAN WAR  ·  STRAIT OF HORMUZ",
        "icon": "tanker",
        "headline": "Two tankers hit mines and burn in the Strait of Hormuz",
        "body": "Iran's Revolutionary Guard said two oil tankers struck naval "
                "mines and caught fire on an unauthorised route. Iran also "
                "claimed it downed two US drones. ◐",
    },
    {
        "kicker": "MARKETS  ·  WALL STREET",
        "icon": "chart",
        "headline": "Wall Street sinks as AI rout and new tariffs bite",
        "body": "Nvidia fell 8.7% and the Nasdaq lost 3.8% by midday. The "
                "White House proposed new tariffs on 14 partners, highest "
                "for China.",
    },
    {
        "kicker": "SPACE  ·  CHINA",
        "icon": "rocket",
        "headline": "Shenzhou-24 docks, carrying Pakistan's first astronaut",
        "body": "China's Shenzhou-24 docked at its space station carrying "
                "Muhammad Zeeshan Ali, the first Pakistani — and first "
                "foreign astronaut — on a Chinese mission.",
    },
]

CARDS = [
    ("HOUTHI WAR", "refinery",
     "Houthis say they hit Saudi Arabia's biggest refinery",
     "Houthis claimed a refinery attack caused fires. ◐"),
    ("SAUDI ARABIA  ·  Tue", "tower",
     "Houthi strike on Riyadh's tallest tower injures 11",
     "A skyscraper strike injured 11, two of them Indians."),
    ("GAZA", "target",
     "Israel kills Hamas security chief in Gaza strike",
     "Abuelouf was killed with his wife and two children."),
    ("UKRAINE", "drone",
     "Russian strikes kill at least five; power cut in five regions",
     "Two killed in Odesa; power cut in five regions."),
    ("SUDAN", "sudan",
     "RSF drone strikes kill 19 civilians in two cities",
     "19 killed, 20 wounded in Damazin and a second city."),
    ("PACIFIC", "treaty",
     "Solomon Islands signs pact barring foreign military bases",
     "Treaty bars any foreign military or security base."),
    ("USA  ·  TECH  ·  Tue", "gavel",
     "Huawei convicted of trade-secret theft and bank fraud",
     "Guilty of trade-secret theft and bank fraud."),
    ("USA  ·  CYBER", "cyber",
     "CIA and ODNI hit by cyber breach, sources say",
     "Some unclassified data was breached, a source said."),
    ("EGYPT", "fire",
     "Fuel tanker fire kills at least 30 on Cairo ring road",
     "Tanker overturned in Giza; 30+ killed, 25 injured."),
    ("BANGLADESH", "wage",
     "Garment wage rises 36% to $139 after protests",
     "Garment wage up 36% to $139 after protests in Dhaka."),
    ("CLIMATE", "climate",
     "Pope Leo XIV laments COP31 talks ending with no deal",
     "Pope: extreme weather is becoming more frequent."),
    ("FOOTBALL", "ball",
     "Barcelona hit Sabah 4–1; Gordon scores twice",
     "Gordon's double led Barça to a 4–1 win in Baku."),
    ("TENNIS", "racket",
     "Sinner out for an extended spell after knee surgery",
     "His team confirmed surgery on his knee."),
]

REST = [
    ("TRUMP", "War funding against Iran secured through January, he says."),
    ("USA", "Justice Dept charges 800+ defendants in 400 cases in a global "
     "anti-scam crackdown."),
    ("USA", "Army destroys 5 tons of degraded explosives in a controlled "
     "blast in Iowa."),
    ("USA  ·  Tue", "Trump awards the Medal of Freedom to Rudy Giuliani."),
    ("UKRAINE", "Zelenskyy and Hungary's Orbán hail a “new era” of "
     "cooperation after talks."),
    ("USA", "Kilmar Ábrego García lands in Spain after leaving the US."),
    ("SPAIN", "Puigdemont says he will return to Spain on 12 December, "
     "ending his exile."),
    ("GAZA", "UN tribunal: the UN sacked Palestinian staff on unproven "
     "Israeli allegations."),
    ("GAZA", "Palestinian journalist killed by Israel in Gaza wins the "
     "Rory Peck prize."),
    ("UK", "BBC asks an appeals court to throw out Trump's $10bn "
     "defamation lawsuit."),
    ("UK", "Bank of England: food inflation could hit 5% next year."),
    ("CHESS", "Gukesh holds Sindarov to a draw in Game 1 of the World "
     "Championship match."),
    ("USA", "Trump to meet Senator-elect El-Sayed on a health plan dubbed "
     "“Trumpcare”."),
    ("USA", "October inflation 3.8% a year; Q3 growth revised up to 4.3%."),
    ("INDIA", "India condemns the Houthi attack on the Riyadh tower that "
     "injured 11."),
]

NUMBERS = [
    ("−3.8%", "Nasdaq by midday"),
    ("−8.7%", "Nvidia shares"),
    ("3.8%", "US inflation, Oct (yr/yr)"),
    ("4.3%", "US Q3 growth, revised"),
    ("14", "partners in new tariff plan"),
    ("30+", "killed, Cairo tanker fire"),
    ("19", "civilians killed, Sudan strikes"),
    ("11", "injured, Riyadh tower strike"),
    ("800+", "charged in anti-scam sweep"),
]

TIMELINE = [
    ("OVERNIGHT", "Russian strikes hit Kyiv and Odesa"),
    ("MORNING", "Tankers hit mines in Hormuz; Houthis claim refinery hit"),
    ("MIDDAY", "Wall Street plunges; tariff plan for 14 partners"),
    ("AFTERNOON", "Huawei convicted; CIA and ODNI breach reported"),
    ("EVENING", "Cairo tanker fire kills 30+; Barça win 4–1"),
    ("LATE", "Shenzhou-24 docks with Pakistan's first astronaut"),
]

# (lon, lat) dots for the sketch map; places are named in the caption
# below the map, because the Middle East dots sit too close together
# for in-map labels.
MAP_DOTS = [
    (-77, 38.9), (-93, 42), (-0.1, 51.5), (30.5, 50.4), (34.5, 31.5),
    (46.7, 24.6), (56.5, 26.5), (31.2, 30.0), (32.5, 12), (90.4, 23.8),
    (116.4, 39.9), (160, -9.6), (49.9, 40.4),
]
MAP_PLACES = ("Washington · London · Kyiv · Gaza · Riyadh · Hormuz · "
              "Cairo · Sudan · Dhaka · Beijing · Baku · Solomons")

# Stylised continents as polygons in lon/lat space (rough sketch).
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 50), (-140, 60), (-168, 66)],
    # South America
    [(-78, 8), (-60, 10), (-50, 0), (-35, -8), (-40, -22), (-48, -28),
     (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20),
     (-80, -5), (-78, 8)],
    # Africa
    [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (48, -2), (40, -12), (33, -26), (26, -34), (18, -30),
     (12, -18), (9, 0), (-8, 5), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 49), (5, 58), (10, 60), (18, 70),
     (40, 68), (60, 70), (80, 73), (110, 77), (140, 72), (170, 66),
     (178, 65), (162, 60), (158, 52), (142, 45), (135, 35), (127, 40),
     (120, 32), (110, 20), (100, 8), (95, 16), (90, 22), (80, 13),
     (75, 8), (72, 22), (66, 25), (58, 26), (52, 28), (48, 30),
     (44, 39), (40, 36), (30, 36), (22, 37), (12, 44), (3, 43),
     (-2, 37), (-10, 36)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (130, -32),
     (124, -33), (115, -35), (114, -22)],
]


def draw_map(draw, x, y, w, h):
    """Sketch world map: continents as flat shapes, red dots for stories."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 242))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)

    def px(lon, lat):
        return (x + (lon + 180.0) / 360.0 * w,
                y + (72.0 - lat) / 132.0 * h)

    for poly in CONTINENTS:
        draw.polygon([px(lon, lat) for lon, lat in poly], fill=(168, 178, 158))
    for lon, lat in MAP_DOTS:
        cx, cy = px(lon, lat)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                     outline=(255, 255, 255), width=1)

# ------------------------------------------------------------------ build

def build(out_path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)

    # ---- masthead -------------------------------------------------
    d.text((W // 2, 12), "THE WORLD IN ONE DAY",
           font=SERIF(28), fill=NAVY, anchor="mt")
    d.text((W // 2, 44), "WEDNESDAY  25  NOVEMBER  2026",
           font=SERIF(40), fill=NAVY, anchor="mt")
    rule(d, 60, 92, W - 60, width=2)
    d.text((W // 2, 98), "31 STORIES  ·  9 REGIONS  ·  EVERYTHING REPORTED ON ONE DAY",
           font=SANSB(11), fill=GREY, anchor="mt")
    rule(d, 14, 118, W - 14, width=2)

    # ---- three leads ----------------------------------------------
    lead_y, lead_h = 124, 168
    col_w, gap = 322, 12
    for i, lead in enumerate(LEADS):
        x = 14 + i * (col_w + gap)
        d.rectangle([x, lead_y, x + col_w, lead_y + lead_h], fill=PAPER,
                    outline=RULE, width=1)
        ICONS[lead["icon"]](d, x + 1, lead_y + 1, 72)
        d.text((x + 80, lead_y + 8), lead["kicker"], font=SANSB(10), fill=RED)
        d.text((x + 80, lead_y + 24), "LEAD " + str(i + 1), font=SANSB(11), fill=NAVY)
        ty = lead_y + 80
        ty = text_block(d, x + 10, ty,
                        wrap(d, lead["headline"], SERIF(17), col_w - 20),
                        SERIF(17), fill=INK, leading=21, max_lines=2)
        text_block(d, x + 10, ty + 4,
                   wrap(d, lead["body"], SANS(11), col_w - 20),
                   SANS(11), fill=INK, leading=13, max_lines=3)
    rule(d, 14, 300, W - 14, width=2)

    # ---- section labels -------------------------------------------
    d.text((14, 308), "TODAY'S STORIES", font=SANSB(12), fill=NAVY)
    d.text((716, 308), "THE DAY IN NUMBERS", font=SANSB(12), fill=NAVY)
    rule(d, 14, 326, 700, width=1)
    rule(d, 716, 326, 1010, width=1)

    # ---- 13 illustrated cards --------------------------------------
    card_w, card_h, cg = 330, 60, 3
    for i, (kick, icon, head, body) in enumerate(CARDS):
        r, c = divmod(i, 2)
        x = 14 + c * (card_w + 24)
        y = 334 + r * (card_h + cg)
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD_BG,
                    outline=RULE, width=1)
        ICONS[icon](d, x + 1, y + 1, card_h - 2)
        tx = x + card_h + 6
        d.text((tx, y + 3), kick, font=SANSB(9), fill=RED)
        ty = text_block(d, tx, y + 15,
                        wrap(d, head, SERIF(12), card_w - card_h - 10),
                        SERIF(12), fill=INK, leading=15, max_lines=2)
        text_block(d, tx, ty + 1,
                   wrap(d, body, SANS(9), card_w - card_h - 10),
                   SANS(9), fill=GREY, leading=11, max_lines=1)

    # ---- the rest of the day ---------------------------------------
    rest_y = 334 + 7 * card_h + 6 * cg + 8
    d.text((14, rest_y), "THE REST OF THE DAY", font=SANSB(12), fill=NAVY)
    rule(d, 14, rest_y + 18, 700, width=1)
    ly = rest_y + 26
    col_w2 = 222
    for i, (kick, body) in enumerate(REST):
        r, c = divmod(i, 5)
        x = 14 + c * (col_w2 + 12)
        y = ly + r * 26
        full = kick + " — " + body
        lines = wrap(d, full, SANS(9), col_w2)[:2]
        if lines:
            first = lines[0]
            if first.startswith(kick):
                d.text((x, y), kick, font=SANSB(9), fill=NAVY)
                rest = first[len(kick):]
                kx = x + d.textlength(kick, font=SANSB(9))
                d.text((kx, y), rest, font=SANS(9), fill=INK)
            else:
                d.text((x, y), first, font=SANS(9), fill=INK)
            if len(lines) > 1:
                d.text((x, y + 11), lines[1], font=SANS(9), fill=INK)

    # ---- sidebar: numbers ------------------------------------------
    ny = 334
    for num, what in NUMBERS:
        d.text((716, ny), num, font=SANSB(15), fill=RED)
        d.text((800, ny + 2), what, font=SANS(11), fill=INK)
        ny += 24
    rule(d, 716, ny + 2, 1010, width=1)

    # ---- sidebar: timeline -----------------------------------------
    ty = ny + 10
    d.text((716, ty), "THE DAY IN ORDER  (UTC, REPORTS)", font=SANSB(11), fill=NAVY)
    ty += 20
    for when, what in TIMELINE:
        d.text((716, ty), when, font=SANSB(9), fill=TEAL)
        text_block(d, 716, ty + 11,
                   wrap(d, what, SANS(9), 294),
                   SANS(9), fill=INK, leading=11, max_lines=1)
        ty += 26
    rule(d, 716, ty + 2, 1010, width=1)

    # ---- sidebar: map ----------------------------------------------
    my = ty + 10
    d.text((716, my), "WHERE IT HAPPENED", font=SANSB(11), fill=NAVY)
    draw_map(d, 716, my + 20, 294, 118)
    cap = text_block(d, 716, my + 142,
                     wrap(d, "Each dot is a story on this page. Dots: "
                             + MAP_PLACES + ". Sketch map, not to scale.",
                          SANS(9), 294),
                     SANS(9), fill=GREY, leading=12, max_lines=3)

    # ---- bottom band: date check + how sure -------------------------
    by = 948
    rule(d, 14, by - 6, W - 14, width=2)
    d.rectangle([14, by, 500, by + 44], fill=PAPER, outline=RULE, width=1)
    d.text((24, by + 5), "DATE CHECK", font=SANSB(11), fill=NAVY)
    text_block(d, 24, by + 21,
               wrap(d, "Every dated event here was reported on Wed 25 Nov 2026. "
                       "“Tue” = happened Tue 24 Nov, reported today.",
                    SANS(10), 466),
               SANS(10), fill=INK, leading=12, max_lines=2)
    d.rectangle([512, by, 1010, by + 44], fill=PAPER, outline=RULE, width=1)
    d.text((522, by + 5), "HOW SURE  ·  ● confirmed  ·  ◐ one side's claim  ·  ○ still moving",
           font=SANSB(10), fill=NAVY)
    text_block(d, 522, by + 21,
               wrap(d, "Figures are as reported at the time; tolls may rise. "
                       "No photographs: every picture here is drawn.",
                    SANS(10), 478),
               SANS(10), fill=INK, leading=12, max_lines=2)
    d.text((W // 2, 1000), "Sources: Reuters · AP · The Guardian · BBC · Al Jazeera · Just Security — 25 Nov 2026",
           font=SANS(9), fill=GREY, anchor="mt")

    img.save(out_path, format="PNG", compress_level=6)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    build(target)
    print("wrote", target, os.path.getsize(target), "bytes")
