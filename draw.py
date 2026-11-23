#!/usr/bin/env python3
"""news-22 b14 by-field: draws entry.png (1024x1024) for news-image-20261122.
Angle: BY FIELD (rank-19 pattern). 48 stories, 3 hero scenes, 12 small cards,
world map with numbered pins, DATE CHECK red box. All facts from the bedah
consensus (BEDAH-TOP20-20261122.md / NEWS-20261122.md).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 242, 231)
INK = (24, 24, 24)
RED = (178, 32, 44)
NAVY = (26, 58, 92)
GREY = (90, 90, 88)
LIGHT = (233, 226, 212)
MAPSEA = (184, 207, 224)
MAPLAND = (232, 220, 192)
MAPLINE = (150, 140, 110)

FD = "/usr/share/fonts/truetype/dejavu/"
_cache = {}


def F(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _cache:
        name = ("DejaVuSerif-Bold.ttf" if serif and bold else
                "DejaVuSerif.ttf" if serif else
                "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
        _cache[key] = ImageFont.truetype(FD + name, size)
    return _cache[key]


def wrap(text, font, maxw, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def txt(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def chip(d, x, y, label, right=None):
    """Certainty chip; returns width used. If right is given, right-align."""
    cols = {"CONFIRMED": (26, 110, 60), "REPORTED": (26, 58, 92),
            "CLAIM": (176, 110, 10), "OFFICIAL": (70, 60, 110),
            "ONGOING": (150, 40, 40), "PENDING": (110, 110, 110),
            "FORECAST": (90, 90, 130)}
    c = cols.get(label, (90, 90, 90))
    f = F(8, bold=True)
    w = int(d.textlength(label, font=f)) + 8
    if right is not None:
        x = right - w
    d.rounded_rectangle([x, y, x + w, y + 12], radius=3, fill=c)
    d.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return w


FIELD_COL = {"WAR": (150, 32, 40), "POLITICS": (26, 58, 92),
             "SPORT": (26, 110, 60), "MARKETS": (120, 80, 10),
             "SOCIETY": (110, 60, 120), "HEALTH": (10, 110, 130)}

# ---------------------------------------------------------------- stories
# n, field, kicker, title, body, chip, source, lon, lat
STORIES = [
 (1, "WAR", "KYIV · WAR", "186 drones fired, 161 shot down",
  "Russia fires 186 drones at Ukraine overnight; air defences down 161. A five-storey flat in Dymer collapses — 1 dead, 14 unaccounted for. Strikes hit 18 sites.",
  "REPORTED", "Ukrainian Air Force · AP", 30.5, 50.4),
 (2, "POLITICS", "HONG KONG · POLITICS", "Hong Kong votes: 98.79% turnout",
  "856 candidates, 723 seats; turnout 98.79%.",
  "CONFIRMED", "SCMP · Reuters", 114.2, 22.3),
 (3, "SPORT", "LAS VEGAS · SPORT", "Verstappen wins by 0.639s",
  "Beats Norris in Las Vegas; his 75th win.",
  "CONFIRMED", "F1 · Reuters", -115.1, 36.2),
 (4, "SPORT", "TURIN · SPORT", "Alcaraz takes ATP Finals",
  "Beats Zverev 6–2, 7–6(7); first title.",
  "CONFIRMED", "ATP · BBC", 7.7, 45.1),
 (5, "WAR", "TALLINN · WAR", "Estonia shuts 5 Russia crossings",
  "Five border crossings close from 1 Dec after sabotage attempts.",
  "REPORTED", "Reuters", 24.7, 59.4),
 (6, "WAR", "COPENHAGEN · WAR", "Denmark expels Russian attaché",
  "Expelled over an alleged plot to kill a US-Ukrainian rapper.",
  "REPORTED", "Reuters", 12.5, 55.7),
 (7, "SOCIETY", "BRUSSELS · SOCIETY", "Belgian air traffic joins strike",
  "Controllers join Monday's national strike; most Monday flights cancelled.",
  "REPORTED", "Reuters", 4.35, 50.85),
 (8, "WAR", "GULF OF FINLAND · WAR", "Sparta II still burning, towed home",
  "Russian cargo ship hit by a drone on Saturday; 16 crew safe. Finland blames Ukraine.",
  "REPORTED", "Reuters · AP", 24.0, 59.5),
 (9, "POLITICS", "ANTALYA · POLITICS", "COP31 collapses — NO DEAL",
  "Final text drops all fossil-fuel language; the EU and ~130 parties refuse it. Talks end after 44 hours overtime — the first summit to fail since 2009.",
  "CONFIRMED", "AP · Reuters · Guardian", 30.7, 36.9),
 (10, "WAR", "BAHRAIN · WAR", "Iran claims 2 Patriot radars hit",
  "Tehran says its missiles hit two US Patriot radars at al-Riffa and Awali. Bahrain denies any military strike — a civilian site at Sitra burns, 2 hurt, no deaths.",
  "CLAIM", "IRGC · Bahrain MoI · Reuters", 50.6, 26.2),
 (11, "WAR", "BENGHAZI · WAR", "Merkury corvette hit by sea drone",
  "Russian corvette hit off Benghazi; the ship lists, several dead. Who fired is disputed.",
  "CLAIM", "Reuters · AP", 20.1, 32.1),
 (12, "MARKETS", "TEHRAN · MARKETS", "Iran starts power rationing",
  "Rolling blackouts of about 2 hours a day as gas output is hit.",
  "REPORTED", "Reuters", 51.4, 35.7),
 (13, "WAR", "GAZA · WAR", "4 killed in Gaza; aid van hit",
  "Israeli fire kills 4; 3 die in a drone strike on a food-aid van in Tel al-Hawa. Hamas asks mediators to talk. WCK: the van was not ours.",
  "REPORTED", "Al Jazeera · AP", 34.5, 31.5),
 (14, "POLITICS", "JERUSALEM · POLITICS", "Eisenkot invites Likud to talks",
  "Ex-general's bloc, 48 seats and 13 short of a majority, opens coalition talks.",
  "REPORTED", "Reuters", 35.2, 31.8),
 (15, "WAR", "WEST BANK · WAR", "Settlers burn 12 cars",
  "Settlers torch cars near Ramallah and attack homes in Hebron.",
  "REPORTED", "AP", 35.2, 31.9),
 (16, "SOCIETY", "CIKANDE · SOCIETY", "Factory fire: 3 dead, 36 missing",
  "3 dead, 36 missing, 15 safe; fire began Sat.",
  "REPORTED", "Detiknews · Basarnas", 106.2, -6.3),
 (17, "SPORT", "NEW ZEALAND · SPORT", "India declare 720/9",
  "Rahul 136, Pant 128; record total in NZ.",
  "CONFIRMED", "ESPNcricinfo", 172.6, -43.5),
 (18, "HEALTH", "SEOUL · HEALTH", "Minister quits over AI-cheat scandal",
  "Education minister Choi Kyo-jin resigns; 111 cases of devices used in exams.",
  "CONFIRMED", "Yonhap · AP", 127.0, 37.5),
 (19, "POLITICS", "NEW DELHI · POLITICS", "Nepal PM lands in Delhi",
  "Balendra Shah's first foreign trip as PM; meets Modi on Monday.",
  "REPORTED", "Reuters", 77.2, 28.6),
 (20, "HEALTH", "MANIPUR · HEALTH", "Bootleg liquor toll rises",
  "Death toll climbs as hundreds are treated; 6 arrested.",
  "REPORTED", "Reuters", 93.9, 24.8),
 (21, "POLITICS", "JAKARTA · POLITICS", "EU–Indonesia trade deal signed",
  "Deal signed; the date is disputed — some wires date it Saturday, others Sunday.",
  "REPORTED", "Reuters", 106.8, -6.2),
 (22, "POLITICS", "CANBERRA · POLITICS", "Marles rejects AUKUS report",
  "Defence minister calls a US budget-office report on AUKUS submarines 'wrong'.",
  "REPORTED", "Reuters", 149.1, -35.3),
 (23, "POLITICS", "WASHINGTON · POLITICS", "Democrats take the House: 258",
  "Biggest majority since 1992; 4 races uncalled.",
  "CONFIRMED", "AP · Reuters", -77.0, 38.9),
 (24, "SOCIETY", "BRASILIA · SOCIETY", "Bolsonaro in intensive care",
  "Former president, 71, hospitalised with acute bowel obstruction; stable.",
  "REPORTED", "AP", -47.9, -15.8),
 (25, "SPORT", "SAN ANTONIO · SPORT", "Wembanyama scores 50",
  "50 pts, 19 reb, 5 blk; Spurs win 114–91.",
  "CONFIRMED", "NBA · AP", -98.5, 29.4),
 (26, "HEALTH", "FLORIDA · SCIENCE", "Falcon 9 lifts NROL-136",
  "Record 32-hour pad turnaround; booster lands.",
  "OFFICIAL", "SpaceX", -80.6, 28.4),
 (27, "HEALTH", "WASHINGTON ST. · SCIENCE", "FBI probes NCIC hack",
  "Crime database breached; Washington state pauses gun-dealer checks. Second breach in months.",
  "REPORTED", "AP · Reuters", -122.3, 47.6),
 (28, "WAR", "KHARTOUM · WAR", "Drones kill 4 near Khartoum",
  "Drone strike kills 4; a UN site is damaged.",
  "REPORTED", "Reuters", 32.5, 15.6),
 (29, "SOCIETY", "BAYELSA · SOCIETY", "Mourners' boat capsizes: 24 dead",
  "Boat carrying mourners overturns in Nigeria; 24 killed.",
  "REPORTED", "Reuters", 6.3, 4.8),
 (30, "HEALTH", "DR CONGO · HEALTH", "Ebola cases reach 11,613",
  "WHO counts 11,613 cases; medics trapped.",
  "OFFICIAL", "WHO · Reuters", 25.0, -2.0),
 (31, "SPORT", "MELBOURNE · SPORT", "70 years since the 1956 Games",
  "Melbourne marks 70 years since it opened the 1956 Olympics.",
  "REPORTED", "Reuters", 145.0, -37.8),
 (32, "SOCIETY", "SYDNEY · SOCIETY", "Fred Nile dies, 92",
  "Veteran NSW politician dies on 21 Nov; announced on Sunday.",
  "REPORTED", "AP", 151.2, -33.9),
 (33, "SPORT", "SYDNEY · SPORT", "Cummins stays Test captain",
  "Pat Cummins confirmed to keep the Australian Test captaincy.",
  "REPORTED", "Cricket Australia", 151.4, -33.7),
 (34, "MARKETS", "NEW YORK · MARKETS", "Bitcoin back above $60,000",
  "Bitcoin climbs back over $60,000, up 1.85% on the day.",
  "REPORTED", "Reuters", -74.0, 40.7),
 (35, "MARKETS", "SANTA CLARA · MARKETS", "Nvidia faces SEC probe",
  "Accounting probe reported; shares fell about 14% on Friday.",
  "REPORTED", "Reuters", -121.0, 37.4),
 (36, "SPORT", "LIVERPOOL · SPORT", "Liverpool rout Man Utd 4–0",
  "Rout on Pochettino's debut as United boss.",
  "CONFIRMED", "BBC Sport", -3.0, 53.4),
 (37, "WAR", "RIYADH · WAR", "Saudi shoots down Houthi attack",
  "Saudi defences intercept a Houthi drone and missile.",
  "CLAIM", "Saudi MoD · Reuters", 46.7, 24.6),
 (38, "WAR", "MANAMA · WAR", "Bahrain blames Iran for strike",
  "Bahrain blames Tehran for the attack on its territory.",
  "REPORTED", "Reuters", 50.8, 26.4),
 (39, "WAR", "ABU DHABI · WAR", "UAE condemns Bahrain strike",
  "The UAE condemns the attack on Bahrain.",
  "REPORTED", "Reuters", 54.4, 24.5),
 (40, "WAR", "MANILA · WAR", "Chinese bomber turns back",
  "Chinese bomber turns back 170 km from Manila after being tracked.",
  "REPORTED", "Reuters", 121.0, 14.6),
 (41, "WAR", "TAIPEI · WAR", "Taiwan holds live-fire drills",
  "Taiwan runs live-fire exercises amid regional tension.",
  "REPORTED", "Reuters", 121.6, 25.0),
 (42, "POLITICS", "OTTAWA · POLITICS", "US–Canada deal 'fairly close'",
  "Trade deal described as fairly close by negotiators.",
  "REPORTED", "Reuters", -75.7, 45.4),
 (43, "MARKETS", "LONDON · MARKETS", "Gold near $3,553",
  "Gold holds near $3,553 an ounce.",
  "REPORTED", "Reuters", -0.1, 51.5),
 (44, "SOCIETY", "ROME · SOCIETY", "Paolo Bulgari dies, 89",
  "Jewellery heir dies; empire spans a century.",
  "REPORTED", "AP", 12.5, 41.9),
 (45, "SOCIETY", "VATICAN · SOCIETY", "Pope Leo hosts 1,300 guests",
  "Pontiff welcomes 1,300 poor guests.",
  "REPORTED", "Vatican News", 12.45, 41.95),
 (46, "SOCIETY", "PARIS · SOCIETY", "Protests, day 3: 144 arrested",
  "Third day of protests across Europe; 144 arrested in France.",
  "REPORTED", "Reuters", 2.35, 48.85),
 (47, "WAR", "HELSINKI · WAR", "Finland: war spreading to Baltic",
  "Helsinki warns the war is spreading to the Baltic region.",
  "REPORTED", "Reuters", 24.9, 60.2),
 (48, "WAR", "KYIV · WAR", "Zelenskyy asks for more Patriots",
  "President asks allies for more Patriot air defences after the overnight barrage.",
  "REPORTED", "Reuters · AP", 30.7, 50.6),
]
BY_NUM = {s[0]: s for s in STORIES}
HEROES = [9, 1, 10]
CARDS = [2, 3, 4, 17, 25, 26, 16, 23, 30, 36, 44, 45]
LISTED = [n for n in range(1, 49) if n not in HEROES and n not in CARDS]
assert len(LISTED) == 33, len(LISTED)

FIELD_COUNTS = {"WAR & SECURITY": 16, "POLITICS": 8, "SPORT": 7,
                "MARKETS": 4, "SOCIETY": 8, "HEALTH & SCIENCE": 5}

NUMSTRIP = [("186", "drones fired"), ("161", "shot down"),
            ("720/9", "India declare"), ("98.79%", "HK turnout"),
            ("$120bn", "adaptation dropped"), ("50", "Wembanyama pts"),
            ("258", "Dems seats"), ("11,613", "Ebola cases")]

UTC = [("01:00", "HK polls open"), ("03:00", "COP31 objections"),
       ("06:00", "COP31 plenary"), ("~16:00", "COP31 ends"),
       ("18:13", "Dems 258"), ("20:43", "Alcaraz wins")]

# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    # sunset sky
    for i in range(h):
        t = i / h
        r = int(250 - 60 * t); g = int(150 - 60 * t); b = int(60 + 90 * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    d.ellipse([x + w - 78, y + 12, x + w - 28, y + 62], fill=(255, 214, 120))
    # conference hall silhouette
    d.rectangle([x + 8, y + h - 58, x + w - 8, y + h], fill=(40, 28, 34))
    for i in range(9):
        wx = x + 16 + i * 32
        d.rectangle([wx, y + h - 48, wx + 18, y + h - 22], fill=(255, 205, 90))
    # globe, cracked
    cx, cy, r = x + 62, y + 52, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 210),
              outline=(240, 240, 240), width=2)
    d.arc([cx - r + 6, cy - r + 4, cx + r - 4, cy + r - 10], 200, 340,
          fill=(240, 240, 240), width=2)
    d.line([(cx - 6, cy - r + 4), (cx + 4, cy - 8), (cx - 2, cy + 6),
            (cx + 8, cy + 16), (cx - 2, cy + r - 4)], fill=(60, 30, 30), width=3)
    # flags row
    for i, c in enumerate([(178, 32, 44), (26, 58, 92), (26, 110, 60),
                           (220, 180, 40), (120, 60, 140), (200, 90, 20)]):
        fx = x + w - 130 + i * 20
        d.line([(fx, y + h - 78), (fx, y + h - 58)], fill=(240, 240, 240), width=2)
        d.rectangle([fx, y + h - 78, fx + 14, y + h - 68], fill=c)


def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for (sx, sy, sr) in [(20, 14, 2), (70, 30, 1), (120, 10, 2), (180, 24, 1),
                         (240, 12, 2), (290, 34, 1), (40, 48, 1), (150, 44, 2)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(255, 255, 220))
    # searchlight beams
    for bx in (x + 40, x + w - 60):
        d.polygon([(bx, y + h), (bx - 26, y + 8), (bx + 6, y + 8)],
                  fill=(90, 110, 150))
    # drones with red trails
    for (dx, dy) in [(70, 26), (150, 18), (230, 30), (110, 44), (200, 48), (270, 20)]:
        d.line([(x + dx - 26, y + dy + 8), (x + dx, y + dy)], fill=(220, 60, 50), width=2)
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(220, 60, 50))
        d.line([(x + dx - 9, y + dy), (x + dx + 9, y + dy)], fill=(200, 200, 200), width=2)
        d.line([(x + dx, y + dy - 4), (x + dx, y + dy + 4)], fill=(200, 200, 200), width=2)
    # apartment block, one section collapsed
    d.rectangle([x + 14, y + h - 62, x + 150, y + h], fill=(120, 118, 112))
    for r in range(4):
        for c in range(6):
            wx = x + 22 + c * 21; wy = y + h - 56 + r * 13
            d.rectangle([wx, wy, wx + 12, wy + 8], fill=(255, 205, 90))
    d.polygon([(x + 150, y + h - 62), (x + 185, y + h - 30), (x + 150, y + h)],
              fill=(90, 88, 84))
    d.polygon([(x + 150, y + h - 8), (x + 210, y + h - 8), (x + 230, y + h),
               (x + 150, y + h)], fill=(100, 98, 94))
    # smoke
    for (sx, sy, sr) in [(185, 52, 12), (200, 40, 16), (218, 52, 10)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(140, 140, 145))
    # fire glow at rubble
    d.ellipse([x + 168, y + h - 26, x + 196, y + h - 6], fill=(255, 140, 40))
    d.polygon([(x + 172, y + h - 8), (x + 180, y + h - 26), (x + 188, y + h - 8)],
              fill=(255, 200, 60))


def scene_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 44))
    for (sx, sy, sr) in [(30, 12, 2), (90, 22, 1), (160, 10, 2), (230, 18, 1),
                         (280, 28, 2), (60, 34, 1), (200, 36, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(255, 255, 220))
    d.ellipse([x + w - 60, y + 8, x + w - 16, y + 52], fill=(235, 235, 220))
    # two radar dishes on masts
    for (rx, tilt) in [(70, -1), (170, 1)]:
        d.line([(x + rx, y + h - 34), (x + rx, y + 66)], fill=(180, 180, 180), width=4)
        d.pieslice([x + rx - 34, y + 30, x + rx + 34, y + 98], 200, 340,
                   fill=(200, 200, 205), outline=(240, 240, 240))
        d.line([(x + rx, y + 64), (x + rx + tilt * 30, y + 40)],
               fill=(255, 120, 60), width=2)
    # fire at base of first dish
    d.ellipse([x + 40, y + h - 44, x + 110, y + h - 6], fill=(255, 120, 30))
    d.polygon([(x + 56, y + h - 10), (x + 70, y + h - 44), (x + 84, y + h - 10)],
              fill=(255, 190, 60))
    d.polygon([(x + 78, y + h - 10), (x + 88, y + h - 34), (x + 100, y + h - 10)],
              fill=(255, 220, 100))
    # smoke column
    for (sx, sy, sr) in [(75, 58, 10), (88, 44, 13), (100, 30, 9)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(130, 130, 138))
    # fence + city lights
    d.line([(x, y + h - 6), (x + w, y + h - 6)], fill=(120, 120, 120), width=2)
    for lx in range(150, w - 10, 26):
        d.ellipse([x + lx, y + h - 12, x + lx + 4, y + h - 8], fill=(255, 205, 90))


def mini_icon(d, x, y, s, kind, col):
    """Tiny white pictogram on a coloured strip, s = strip height."""
    wht = (255, 255, 255)
    cx, cy = x + s // 2, y + s // 2
    if kind == "vote":
        d.rectangle([cx - 8, cy - 2, cx + 8, cy + 8], outline=wht, width=2)
        d.line([(cx - 8, cy - 2), (cx - 2, cy - 9), (cx + 8, cy - 9)], fill=wht, width=2)
        d.line([(cx - 3, cy - 6), (cx, cy - 3), (cx + 4, cy - 8)], fill=wht, width=2)
    elif kind == "car":
        d.rounded_rectangle([cx - 11, cy - 2, cx + 11, cy + 5], radius=3, outline=wht, width=2)
        d.ellipse([cx - 7, cy + 4, cx - 2, cy + 9], fill=wht)
        d.ellipse([cx + 2, cy + 4, cx + 7, cy + 9], fill=wht)
    elif kind == "ball":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=wht, width=2)
        d.arc([cx - 8, cy - 8, cx + 8, cy + 8], 300, 60, fill=wht, width=2)
        d.arc([cx - 8, cy - 8, cx + 8, cy + 8], 120, 240, fill=wht, width=2)
    elif kind == "bat":
        d.line([(cx - 8, cy + 8), (cx + 6, cy - 8)], fill=wht, width=3)
        d.ellipse([cx + 4, cy - 10, cx + 10, cy - 4], fill=wht)
    elif kind == "basket":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=wht, width=2)
        d.line([(cx - 8, cy), (cx + 8, cy)], fill=wht, width=1)
        d.line([(cx, cy - 8), (cx, cy + 8)], fill=wht, width=1)
    elif kind == "rocket":
        d.polygon([(cx, cy - 10), (cx - 5, cy + 2), (cx + 5, cy + 2)], fill=wht)
        d.polygon([(cx - 2, cy + 2), (cx, cy + 10), (cx + 2, cy + 2)], fill=(255, 180, 60))
    elif kind == "flame":
        d.polygon([(cx, cy - 9), (cx + 6, cy + 1), (cx + 3, cy + 8),
                   (cx - 3, cy + 8), (cx - 6, cy + 1)], fill=wht)
    elif kind == "dome":
        d.arc([cx - 9, cy - 6, cx + 9, cy + 8], 180, 360, fill=wht, width=2)
        d.line([(cx - 9, cy + 6), (cx + 9, cy + 6)], fill=wht, width=2)
        d.line([(cx, cy - 9), (cx, cy - 6)], fill=wht, width=2)
    elif kind == "virus":
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=wht, width=2)
        for a in range(0, 360, 45):
            ex = cx + int(9 * math.cos(math.radians(a)))
            ey = cy + int(9 * math.sin(math.radians(a)))
            d.line([(cx, cy), (ex, ey)], fill=wht, width=1)
    elif kind == "football":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=wht, width=2)
        d.polygon([(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)],
                  fill=wht)
    elif kind == "gem":
        d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)],
                  outline=wht, width=2)
    elif kind == "cross":
        d.line([(cx, cy - 9), (cx, cy + 9)], fill=wht, width=3)
        d.line([(cx - 6, cy - 4), (cx + 6, cy - 4)], fill=wht, width=3)
    else:
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=wht, width=2)

CARD_ICON = {2: "vote", 3: "car", 4: "ball", 17: "bat", 25: "basket",
             26: "rocket", 16: "flame", 23: "dome", 30: "virus",
             36: "football", 44: "gem", 45: "cross"}

# ---------------------------------------------------------------- map
CONTINENTS = [
 # North America
 [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
  (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
  (-80, 25), (-85, 20), (-90, 15), (-95, 16), (-100, 18), (-105, 20),
  (-110, 23), (-115, 30), (-125, 40), (-125, 48), (-135, 58), (-155, 58),
  (-165, 60)],
 # Greenland
 [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
  (-45, 78), (-58, 76), (-60, 70)],
 # South America
 [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-50, 5), (-50, 0),
  (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
  (-70, -50), (-73, -55), (-70, -45), (-73, -35), (-75, -20), (-80, -10),
  (-80, 0), (-80, 8)],
 # Europe
 [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
  (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (30, 70),
  (35, 66), (30, 60), (28, 55), (25, 55), (20, 54), (15, 55), (10, 54),
  (8, 55), (3, 58), (0, 57), (-5, 52), (-8, 48), (-10, 44)],
 # Africa
 [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37), (12, 33),
  (20, 32), (30, 31), (33, 27), (35, 23), (37, 18), (40, 15), (43, 11),
  (48, 10), (51, 11), (48, 5), (42, 0), (40, -5), (38, -10), (35, -15),
  (32, -25), (28, -32), (20, -35), (15, -30), (12, -18), (13, -10),
  (12, -5), (9, 4), (4, 6), (-5, 5), (-10, 6), (-15, 10), (-17, 14)],
 # Asia
 [(30, 36), (35, 36), (40, 38), (45, 40), (50, 42), (55, 45), (60, 50),
  (65, 55), (70, 60), (75, 65), (80, 70), (90, 72), (100, 75), (110, 75),
  (120, 73), (130, 72), (140, 72), (150, 70), (160, 68), (170, 66),
  (178, 65), (178, 60), (170, 60), (162, 58), (158, 52), (150, 60),
  (145, 60), (142, 55), (140, 50), (135, 45), (130, 42), (127, 40),
  (122, 38), (120, 32), (115, 25), (110, 20), (108, 15), (105, 10),
  (100, 8), (98, 12), (95, 15), (92, 20), (90, 22), (85, 20), (80, 15),
  (78, 10), (75, 8), (72, 20), (68, 25), (65, 25), (60, 25), (55, 26),
  (52, 28), (50, 30), (48, 30), (45, 30), (42, 32), (38, 35), (35, 36)],
 # Australia
 [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
  (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
  (153, -27), (150, -22), (146, -19), (142, -11), (140, -17), (136, -15),
  (132, -12), (128, -14), (122, -17), (118, -20)],
]
# pin offsets (dx, dy px) to de-clash dense clusters
PIN_OFF = {1: (-14, -8), 48: (12, 6), 5: (-4, -12), 6: (-12, 4), 7: (-16, 10),
           47: (10, -10), 36: (-8, -8), 46: (10, 8), 4: (12, 10),
           9: (-10, 12), 14: (8, 12), 15: (14, -2), 13: (-12, -6),
           10: (-14, 8), 38: (12, -8), 39: (14, 6), 37: (-6, 12),
           12: (10, -10), 32: (-10, -6), 33: (12, 8), 31: (-12, 8),
           16: (10, 8), 21: (-12, -8), 45: (10, -10), 44: (-12, 10)}


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = 14, W - 14

    # ---- masthead
    d.rectangle([0, 0, W, 6], fill=RED)
    txt(d, x0, 12, "THE WORLD IN ONE DAY", F(13, bold=True), fill=RED)
    txt(d, x1, 12, "48 STORIES  ·  7 REGIONS  ·  6 FIELDS", F(11, bold=True),
        fill=GREY, anchor="ra")
    txt(d, x0, 30, "Sunday 22 November 2026", F(40, bold=True, serif=True))
    d.line([(x0, 74), (x1, 74)], fill=INK, width=2)
    txt(d, x0, 80, "COP31 fails  ·  186 drones  ·  Bahrain radar claim — the day the world said no",
        F(13, bold=True), fill=RED)

    # ---- number strip
    y = 102
    cw = (x1 - x0) / len(NUMSTRIP)
    for i, (v, lab) in enumerate(NUMSTRIP):
        cx = x0 + cw * i + cw / 2
        txt(d, cx, y, v, F(20, bold=True, serif=True), anchor="ma")
        txt(d, cx, y + 23, lab, F(8, bold=True), fill=GREY, anchor="ma")
        if i:
            d.line([(x0 + cw * i, y + 2), (x0 + cw * i, y + 34)], fill=(200, 192, 175))
    d.line([(x0, y + 40), (x1, y + 40)], fill=(200, 192, 175))

    # ---- by-field bar
    y = 148
    parts = [(k, v) for k, v in FIELD_COUNTS.items()]
    tot_w = x1 - x0
    bx = x0
    for name, n in parts:
        seg = tot_w * n / 48
        col = {"WAR & SECURITY": FIELD_COL["WAR"], "POLITICS": FIELD_COL["POLITICS"],
               "SPORT": FIELD_COL["SPORT"], "MARKETS": FIELD_COL["MARKETS"],
               "SOCIETY": FIELD_COL["SOCIETY"],
               "HEALTH & SCIENCE": FIELD_COL["HEALTH"]}[name]
        d.rectangle([bx, y, bx + seg - 2, y + 20], fill=col)
        t = f"{name} {n}"
        f = F(9, bold=True)
        tw = d.textlength(t, font=f)
        if tw < seg - 6:
            d.text((bx + (seg - 2) / 2 - tw / 2, y + 5), t, font=f, fill=(255, 255, 255))
        bx += seg
    y += 26

    # ---- UTC strip
    d.rectangle([x0, y, x1, y + 20], fill=(26, 58, 92))
    txt(d, x0 + 6, y + 4, "THE DAY IN UTC", F(10, bold=True), fill=(255, 214, 120))
    ux = x0 + 118
    for t, lab in UTC:
        s = f"{t}  {lab}"
        f = F(10, bold=True)
        d.text((ux, y + 4), s, font=f, fill=(255, 255, 255))
        ux += d.textlength(s, font=f) + 12
    y += 26

    # ---- heroes
    hy, hh = y, 232
    hw = int((x1 - x0 - 12) / 3)
    scenes = {9: scene_cop31, 1: scene_drones, 10: scene_bahrain}
    for i, n in enumerate(HEROES):
        s = BY_NUM[n]
        hx = x0 + i * (hw + 6)
        d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=1, fill=(255, 255, 255))
        scenes[n](d, hx + 1, hy + 1, hw - 2, 108)
        ty = hy + 112
        chip(d, hx + 8, ty, s[5])
        txt(d, hx + 8, ty + 16, s[2], F(8, bold=True), fill=GREY)
        lines = wrap(s[3], F(17, bold=True, serif=True), hw - 16, d)
        ly = ty + 28
        for ln in lines[:2]:
            d.text((hx + 8, ly), ln, font=F(17, bold=True, serif=True), fill=INK)
            ly += 20
        blines = wrap(s[4], F(10), hw - 16, d)
        ly += 2
        for ln in blines[:3]:
            d.text((hx + 8, ly), ln, font=F(10), fill=INK)
            ly += 12
        txt(d, hx + 8, hy + hh - 14, "Source: " + s[6], F(8), fill=GREY)
    y = hy + hh + 8

    # ---- small cards: 4 cols x 3 rows
    ch, cgap = 74, 6
    cw2 = int((x1 - x0 - 3 * cgap) / 4)
    for i, n in enumerate(CARDS):
        s = BY_NUM[n]
        r, c = divmod(i, 4)
        cx = x0 + c * (cw2 + cgap)
        cy = y + r * (ch + cgap)
        col = FIELD_COL[s[1]]
        d.rectangle([cx, cy, cx + cw2, cy + ch], outline=(180, 172, 155), width=1,
                    fill=(255, 255, 255))
        d.rectangle([cx + 1, cy + 1, cx + cw2 - 1, cy + 23], fill=col)
        mini_icon(d, cx + 2, cy + 2, 20, CARD_ICON[n], col)
        txt(d, cx + 26, cy + 5, f"#{n}", F(11, bold=True), fill=(255, 255, 255))
        chip(d, cx + cw2 - 4, cy + 5, s[5], right=cx + cw2 - 4)
        txt(d, cx + 6, cy + 26, s[2], F(7, bold=True), fill=GREY)
        tlines = wrap(s[3], F(10, bold=True), cw2 - 12, d)
        ly = cy + 36
        for ln in tlines[:2]:
            d.text((cx + 6, ly), ln, font=F(10, bold=True), fill=INK)
            ly += 11
        blines = wrap(s[4], F(8.5), cw2 - 12, d)
        for ln in blines[:1]:
            d.text((cx + 6, ly), ln, font=F(8.5), fill=INK)
            ly += 10
        txt(d, cx + 6, cy + ch - 11, s[6], F(7), fill=GREY)
    y = y + 3 * ch + 2 * cgap + 8

    # ---- map + ALSO list
    my, mh = y, 222
    mx0, mx1 = x0, x0 + 486
    d.rectangle([mx0, my, mx1, my + mh], outline=INK, width=1, fill=MAPSEA)
    txt(d, mx0 + 6, my + 4, "WHERE IT HAPPENED — PIN = STORY NUMBER",
        F(9, bold=True), fill=NAVY)
    # graticule
    for gx in range(1, 6):
        gx0 = mx0 + 8 + gx * (mx1 - mx0 - 16) / 6
        d.line([(gx0, my + 18), (gx0, my + mh - 4)], fill=(200, 218, 232))
    for gy in range(1, 4):
        gy0 = my + 18 + gy * (mh - 22) / 4
        d.line([(mx0 + 8, gy0), (mx1 - 8, gy0)], fill=(200, 218, 232))

    def proj(lon, lat):
        px = mx0 + 8 + (lon + 170) / 360 * (mx1 - mx0 - 16)
        py = my + 18 + (72 - lat) / 130 * (mh - 22)
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND, outline=MAPLINE)
    # labels
    for lab, lon, lat in [("NORTH AMERICA", -100, 55), ("SOUTH AMERICA", -60, -15),
                          ("EUROPE", 15, 58), ("AFRICA", 18, 8),
                          ("ASIA", 95, 55), ("AUSTRALIA", 134, -25),
                          ("PACIFIC", -150, -20), ("ATLANTIC", -35, 25)]:
        px, py = proj(lon, lat)
        d.text((px, py), lab, font=F(8, bold=True), fill=(110, 125, 140),
               anchor="mm")
    # pins
    for n in range(1, 49):
        s = BY_NUM[n]
        px, py = proj(s[7], s[8])
        dx, dy = PIN_OFF.get(n, (0, 0))
        px, py = px + dx, py + dy
        r = 7
        col = RED if s[5] in ("CONFIRMED", "REPORTED") else (176, 110, 10)
        if s[5] == "CLAIM":
            col = (176, 110, 10)
        d.ellipse([px - r, py - r, px + r, py + r], fill=col,
                  outline=(255, 255, 255), width=1)
        f = F(7, bold=True)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))
    # ALSO list
    lx0 = mx1 + 10
    txt(d, lx0, my, "ALSO ON SUNDAY — 33 MORE STORIES", F(11, bold=True), fill=RED)
    txt(d, lx0, my + 15, "Red pin = reported  ·  Amber pin = claim",
        F(8), fill=GREY)
    colw = (x1 - lx0 - 8) / 2
    fitem = F(9.5)
    half = 17
    for i, n in enumerate(LISTED):
        s = BY_NUM[n]
        c, r = divmod(i, half)
        ix = lx0 + c * (colw + 8)
        iy = my + 30 + r * 11.5
        d.ellipse([ix, iy + 1, ix + 7, iy + 8], fill=RED if s[5] != "CLAIM"
                  else (176, 110, 10))
        d.text((ix + 3.5, iy - 1), str(n), font=F(6, bold=True),
               fill=(255, 255, 255), anchor="ma")
        d.text((ix + 10, iy), s[3], font=fitem, fill=INK)
    y = my + mh + 8

    # ---- DATE CHECK red box
    d.rectangle([x0, y, x1, y + 80], outline=RED, width=2, fill=(255, 244, 244))
    txt(d, x0 + 8, y + 5, "DATE CHECK — EVERY STORY HAPPENED OR WAS FIRST REPORTED "
        "ON SUNDAY 22 NOVEMBER 2026  ·  WIRES READ UP TO 23:00 UTC",
        F(10, bold=True), fill=RED)
    d.line([(x0 + 8, y + 21), (x1 - 8, y + 21)], fill=RED)
    fdc = F(9.5)
    lo = ("LEFT OUT (not 22 Nov): 400-drone barrage (19–20 Nov) · El Chapo Isidro "
          "captured (20 Nov) · BepiColombo Mercury orbit (21 Nov, burn 18:24 GMT) · "
          "Kryvyi Rih (20 Nov) · Peru quake (20 Nov) · Hormuz tankers hit (Sat 21 Nov "
          "05:00 GMT; reported Sun 17:13 UTC) · Sparta II hit Sat 21 Nov — shown only "
          "as still burning/towed.")
    for j, ln in enumerate(wrap(lo, fdc, x1 - x0 - 16, d)):
        d.text((x0 + 8, y + 24 + j * 12), ln, font=fdc, fill=INK)
    ny = ("NOT YET: 4 House races uncalled · Dymer final toll · COP32 venue · "
          "Gaza ceasefire talks — no deal announced.")
    d.text((x0 + 8, y + 62), ny, font=fdc, fill=INK)
    y = y + 80 + 6

    # ---- footer
    txt(d, x0, y, "SOURCES: AP · Reuters · BBC · Al Jazeera · Guardian · France 24 · "
        "Yonhap · Anadolu · SCMP · WHO · ATP · NBA · SpaceX · Detiknews", F(8.5), fill=GREY)
    txt(d, x0, y + 12, "CONFIRMED = 2+ outlets  ·  REPORTED = carried by the wires  ·  "
        "CLAIM = one side, unverified  ·  OFFICIAL = recorded result",
        F(8.5), fill=GREY)
    txt(d, x1, y + 12, "Scenes are drawn illustrations, not photographs.",
        F(8.5), fill=GREY, anchor="ra")
    assert y + 24 <= H, f"overflow: {y + 24}"

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    build()
