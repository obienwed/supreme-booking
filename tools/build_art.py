#!/usr/bin/env python3
"""Draws the site's original illustrations as SVG into assets/art/.

Run from the repo root:  python3 tools/build_art.py
Every scene is 1200x520, flat neon style in the site palette.
"""
import pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "art"
OUT.mkdir(parents=True, exist_ok=True)

PLUM, PLUM2, PLUM3 = "#1E1234", "#2C1B4A", "#3D2862"
HOT, GOLD, ORANGE, BLUE, TEAL, LILAC = "#FF2E93", "#FFC83D", "#FF8A00", "#2E7BFF", "#2EC4B6", "#F3EEFF"
W, H = 1200, 520


def svg(body, defs="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
            f'<title>{title}</title><defs>{defs}</defs>{body}</svg>\n')


def night_sky(id_="sky", top=PLUM, bottom=PLUM3):
    d = (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>'
         '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
         '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>')
    return d, f'<rect width="{W}" height="{H}" fill="url(#{id_})"/>'


def stars(seed, n=60, ymax=260):
    r = random.Random(seed)
    return "".join(
        f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, ymax):.0f}" r="{r.choice([1, 1, 1.5, 2])}" '
        f'fill="{LILAC}" opacity="{r.uniform(.25, .8):.2f}"/>' for _ in range(n))


def skyline(seed, base, color=PLUM2, win=GOLD, hmin=60, hmax=210, tower=True):
    r = random.Random(seed)
    out, x = [], -10
    while x < W + 10:
        w = r.randint(40, 95)
        h = r.randint(hmin, hmax)
        out.append(f'<rect x="{x}" y="{base - h}" width="{w}" height="{h + 2}" fill="{color}"/>')
        for wy in range(base - h + 12, base - 10, 16):
            for wx in range(x + 8, x + w - 8, 14):
                if r.random() < .28:
                    out.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="{win}" opacity="{r.uniform(.35, .9):.2f}"/>')
        x += w + r.randint(0, 6)
    if tower:
        tx = 930
        out.append(f'<rect x="{tx}" y="{base - 300}" width="14" height="300" fill="{color}"/>'
                   f'<ellipse cx="{tx + 7}" cy="{base - 300}" rx="34" ry="14" fill="{color}"/>'
                   f'<rect x="{tx + 5}" y="{base - 360}" width="4" height="60" fill="{color}"/>'
                   f'<circle cx="{tx + 7}" cy="{base - 362}" r="4" fill="{HOT}"/>')
    return "".join(out)


def person(x, y, s=1.0, color=PLUM, arms="up", r=None):
    """Simple silhouette: head + rounded torso + optional raised arms."""
    r = r or random.Random(int(x * 7 + y))
    hr = 14 * s
    body = (f'<circle cx="{x}" cy="{y}" r="{hr:.1f}" fill="{color}"/>'
            f'<rect x="{x - 20 * s:.1f}" y="{y + hr + 3 * s:.1f}" width="{40 * s:.1f}" height="{70 * s:.1f}" rx="{16 * s:.1f}" fill="{color}"/>')
    if arms == "up":
        lx = x - 16 * s - r.uniform(4, 14) * s
        rx = x + 16 * s + r.uniform(4, 14) * s
        top = y - r.uniform(28, 46) * s
        body += (f'<path d="M{x - 14 * s:.1f} {y + 26 * s:.1f} L{lx:.1f} {top:.1f}" stroke="{color}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>'
                 f'<path d="M{x + 14 * s:.1f} {y + 26 * s:.1f} L{rx:.1f} {top + r.uniform(-8, 8) * s:.1f}" stroke="{color}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>')
    return body


def confetti(seed, n, colors=(HOT, GOLD, TEAL, ORANGE, LILAC), area=(0, 0, W, H)):
    r = random.Random(seed)
    x0, y0, x1, y1 = area
    out = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        c = r.choice(colors)
        if r.random() < .5:
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="10" height="4" rx="1" fill="{c}" transform="rotate({r.randint(0, 180)} {x:.0f} {y:.0f})"/>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([3, 4, 5])}" fill="{c}"/>')
    return "".join(out)


def palm(x, base, h, color, lean=0):
    tx, ty = x + lean, base - h
    trunk = f'<path d="M{x} {base} Q{x + lean * .3} {base - h * .5} {tx} {ty}" stroke="{color}" stroke-width="14" fill="none" stroke-linecap="round"/>'
    fronds = ""
    for ang, ln in [(-160, 120), (-130, 135), (-95, 90), (-60, 135), (-25, 120), (10, 95), (-190, 95)]:
        import math
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * ln, ty + math.sin(a) * ln * .55 + 40
        mx, my = tx + math.cos(a) * ln * .5, ty + math.sin(a) * ln * .5 - 22
        fronds += f'<path d="M{tx} {ty} Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}" stroke="{color}" stroke-width="16" fill="none" stroke-linecap="round"/>'
    return trunk + fronds


def note(x, y, c, s=1):
    return (f'<g fill="{c}" transform="translate({x} {y}) scale({s})">'
            '<ellipse cx="0" cy="22" rx="9" ry="7"/><rect x="7" y="-14" width="3.5" height="36"/>'
            '<path d="M10.5 -14 q14 4 14 18 q-4 -8 -14 -8z"/></g>')


# ---------------------------------------------------------------- scenes
def party_bus():
    d, bg = night_sky()
    base = 400
    body = bg + stars(1) + f'<circle cx="160" cy="95" r="38" fill="{LILAC}" opacity=".9"/><circle cx="176" cy="85" r="34" fill="{PLUM}"/>'
    body += skyline(2, base, PLUM2) + skyline(3, base, PLUM3, hmin=30, hmax=110, tower=False)
    body += f'<rect y="{base}" width="{W}" height="{H - base}" fill="{PLUM}"/>'
    body += "".join(f'<rect x="{x}" y="{base + 62}" width="60" height="6" rx="3" fill="{GOLD}" opacity=".7"/>' for x in range(-20, W, 120))
    # glow under bus
    body += f'<ellipse cx="600" cy="{base + 40}" rx="330" ry="26" fill="{HOT}" opacity=".55" filter="url(#glow)"/>'
    bx, by, bw, bh = 300, 230, 600, 170
    body += (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="34" fill="{HOT}"/>'
             f'<rect x="{bx}" y="{by + bh - 34}" width="{bw}" height="34" rx="12" fill="#D81B78"/>'
             f'<rect x="{bx + bw - 70}" y="{by + 26}" width="58" height="76" rx="14" fill="{PLUM2}"/>')
    # windows with partiers
    r = random.Random(9)
    for i, wx in enumerate(range(bx + 26, bx + bw - 90, 104)):
        body += f'<rect x="{wx}" y="{by + 26}" width="88" height="76" rx="14" fill="{PLUM2}"/>'
        body += f'<rect x="{wx}" y="{by + 26}" width="88" height="76" rx="14" fill="{GOLD}" opacity=".12"/>'
        body += f'<clipPath id="w{i}"><rect x="{wx}" y="{by + 26}" width="88" height="76" rx="14"/></clipPath>'
        body += f'<g clip-path="url(#w{i})">' + person(wx + 30, by + 62, .62, PLUM, r=r) + person(wx + 62, by + 70, .55, PLUM3, r=r) + '</g>'
    # stripe + roof lights
    body += f'<rect x="{bx + 20}" y="{by + 116}" width="{bw - 110}" height="8" rx="4" fill="{GOLD}"/>'
    body += "".join(f'<circle cx="{x}" cy="{by - 2}" r="5" fill="{c}"/>' for x, c in zip(range(bx + 40, bx + bw - 30, 46), [GOLD, TEAL, HOT, LILAC] * 4))
    # wheels
    for wx in (bx + 110, bx + bw - 120):
        body += f'<circle cx="{wx}" cy="{by + bh}" r="40" fill="{PLUM}"/><circle cx="{wx}" cy="{by + bh}" r="18" fill="{LILAC}" opacity=".85"/>'
    body += f'<rect x="{bx + bw - 14}" y="{by + 130}" width="18" height="12" rx="4" fill="{GOLD}"/>'
    body += note(240, 200, GOLD) + note(960, 170, TEAL, 1.2) + note(1010, 260, HOT, .9) + note(200, 300, LILAC, .8)
    return svg(body, d, "Party bus on the Las Vegas Strip at night")


def club():
    d, bg = night_sky(top="#120A20", bottom=PLUM2)
    body = bg
    # light beams
    for x0, x1, c, o in [(150, -120, HOT, .22), (300, 520, GOLD, .18), (600, 360, TEAL, .16), (600, 860, HOT, .18), (900, 700, GOLD, .18), (1050, 1340, TEAL, .2)]:
        body += f'<polygon points="{x0},0 {x1 - 90},{H} {x1 + 90},{H}" fill="{c}" opacity="{o}"/>'
    # disco ball
    body += f'<line x1="600" y1="0" x2="600" y2="60" stroke="{LILAC}" stroke-width="3"/><circle cx="600" cy="100" r="44" fill="{LILAC}"/>'
    for gy in range(62, 140, 12):
        body += f'<line x1="556" y1="{gy}" x2="644" y2="{gy}" stroke="{PLUM3}" stroke-width="2"/>'
    for gx in range(560, 644, 12):
        body += f'<line x1="{gx}" y1="56" x2="{gx}" y2="144" stroke="{PLUM3}" stroke-width="2"/>'
    body += f'<circle cx="600" cy="100" r="44" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    body += f'<circle cx="600" cy="100" r="70" fill="{LILAC}" opacity=".25" filter="url(#glow)"/>'
    # DJ booth
    body += (f'<rect x="470" y="250" width="260" height="70" rx="10" fill="{PLUM3}"/>'
             f'<rect x="470" y="250" width="260" height="10" rx="4" fill="{HOT}"/>'
             f'<circle cx="530" cy="285" r="20" fill="{PLUM}"/><circle cx="670" cy="285" r="20" fill="{PLUM}"/>'
             f'<circle cx="530" cy="285" r="5" fill="{GOLD}"/><circle cx="670" cy="285" r="5" fill="{GOLD}"/>')
    body += person(600, 205, .8, PLUM, r=random.Random(4))
    # crowd rows
    r = random.Random(11)
    for row, (y, s, c) in enumerate([(380, .95, PLUM3), (430, 1.15, PLUM), ]):
        x = -20 + row * 30
        while x < W + 40:
            body += person(x, y, s, c, arms="up" if r.random() < .6 else "down", r=r)
            x += r.randint(58, 84) * s
    body += f'<rect y="{H - 30}" width="{W}" height="30" fill="{PLUM}"/>'
    body += confetti(5, 45, area=(0, 140, W, 360))
    return svg(body, d, "Crowd dancing under lights at a nightclub")


def pool():
    d = (f'<linearGradient id="day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ORANGE}"/>'
         f'<stop offset=".7" stop-color="{HOT}"/></linearGradient>'
         f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
         '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>')
    body = f'<rect width="{W}" height="{H}" fill="url(#day)"/>'
    body += f'<circle cx="880" cy="150" r="120" fill="{GOLD}" opacity=".45" filter="url(#glow)"/><circle cx="880" cy="150" r="80" fill="{GOLD}"/>'
    body += skyline(21, 300, "#C7225F", win=GOLD, hmin=40, hmax=140, tower=False)
    body += f'<rect y="290" width="{W}" height="40" fill="{LILAC}"/>'
    body += f'<rect y="320" width="{W}" height="{H - 320}" fill="url(#water)"/>'
    for i, y in enumerate(range(350, H, 34)):
        body += f'<path d="M0 {y} ' + "".join(f"q30 -10 60 0 t60 0 " for _ in range(11)) + f'" transform="translate({-(i % 2) * 30} 0)" stroke="{LILAC}" stroke-width="4" fill="none" opacity=".45"/>'
    body += palm(120, 300, 220, PLUM, lean=30) + palm(1100, 300, 250, PLUM, lean=-40)
    # umbrella + loungers
    body += (f'<line x1="330" y1="300" x2="330" y2="180" stroke="{PLUM}" stroke-width="6"/>'
             f'<path d="M230 190 Q330 110 430 190 Z" fill="{GOLD}"/><path d="M280 190 Q330 140 380 190 Z" fill="{HOT}"/>')
    body += f'<rect x="420" y="276" width="110" height="14" rx="6" fill="{PLUM}"/><rect x="560" y="276" width="110" height="14" rx="6" fill="{PLUM}"/>'
    # floats
    for cx, cy, c in [(520, 420, HOT), (790, 460, GOLD), (300, 470, LILAC)]:
        body += f'<ellipse cx="{cx}" cy="{cy}" rx="58" ry="24" fill="{c}"/><ellipse cx="{cx}" cy="{cy - 2}" rx="26" ry="10" fill="{TEAL}"/>'
    body += person(520, 380, .7, PLUM, r=random.Random(3)) + person(790, 422, .62, PLUM, r=random.Random(8))
    body += f'<g transform="translate(980 430)"><circle r="34" fill="{LILAC}"/><path d="M-34 0 A34 34 0 0 1 34 0" fill="{HOT}"/><path d="M-12 -32 L12 32" stroke="{GOLD}" stroke-width="10"/></g>'
    return svg(body, d, "Pool party with palm trees and floats")


def yacht():
    d, bg = night_sky(top="#0E1440", bottom=PLUM2)
    d += (f'<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/>'
          f'<stop offset="1" stop-color="{PLUM}"/></linearGradient>')
    body = bg + stars(31, 70)
    body += f'<circle cx="1040" cy="90" r="40" fill="{LILAC}"/><circle cx="1040" cy="90" r="70" fill="{LILAC}" opacity=".2" filter="url(#glow)"/>'
    body += skyline(33, 300, "#241A55", win=TEAL, hmin=70, hmax=200, tower=False)
    body += f'<rect y="300" width="{W}" height="{H - 300}" fill="url(#sea)"/>'
    r = random.Random(5)
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(310, H)
        body += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(20, 70):.0f}" height="3" rx="1.5" fill="{r.choice([GOLD, TEAL, HOT])}" opacity="{r.uniform(.2, .55):.2f}"/>'
    # yacht
    body += f'<ellipse cx="600" cy="390" rx="320" ry="20" fill="{BLUE}" opacity=".5" filter="url(#glow)"/>'
    body += (f'<path d="M280 330 L960 330 L900 395 L330 395 Z" fill="{LILAC}"/>'
             f'<path d="M330 380 L905 380 L900 395 L330 395 Z" fill="{BLUE}"/>'
             f'<path d="M380 330 L420 270 L820 270 L870 330 Z" fill="{LILAC}"/>'
             f'<path d="M460 270 L500 225 L740 225 L770 270 Z" fill="{LILAC}"/>'
             f'<rect x="430" y="284" width="380" height="26" rx="8" fill="{PLUM2}"/>'
             f'<rect x="515" y="236" width="220" height="22" rx="7" fill="{PLUM2}"/>')
    for x in range(440, 800, 34):
        body += f'<rect x="{x}" y="288" width="22" height="18" rx="4" fill="{GOLD}" opacity=".75"/>'
    # string lights
    body += f'<path d="M300 330 Q450 290 600 300 Q750 290 940 330" stroke="{LILAC}" stroke-width="1.5" fill="none" opacity=".7"/>'
    for i, x in enumerate(range(310, 940, 30)):
        y = 330 - 34 * (1 - ((x - 620) / 320) ** 2)
        body += f'<circle cx="{x}" cy="{y:.0f}" r="4" fill="{[GOLD, HOT, TEAL][i % 3]}"/>'
    # partiers on deck
    rr = random.Random(77)
    for x in range(330, 900, 62):
        body += person(x, 300 - 30, .5, PLUM, r=rr)
    body += note(250, 220, GOLD) + note(940, 200, HOT, 1.1)
    return svg(body, d, "Party yacht on the water at night")


def miami():
    d, bg = night_sky(top="#14103A", bottom=PLUM3)
    body = bg + stars(41, 50, 200)
    # art deco buildings with neon outlines
    r = random.Random(44)
    x = 20
    for c in [HOT, TEAL, GOLD, HOT, TEAL, GOLD]:
        w, h = r.randint(150, 190), r.randint(170, 240)
        y = 400 - h
        body += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PLUM2}"/>'
                 f'<rect x="{x + w / 2 - 22}" y="{y - 40}" width="44" height="44" fill="{PLUM2}"/>'
                 f'<rect x="{x + w / 2 - 12}" y="{y - 70}" width="24" height="34" fill="{PLUM2}"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="4"/>'
                 f'<line x1="{x + 12}" y1="{y + 30}" x2="{x + w - 12}" y2="{y + 30}" stroke="{c}" stroke-width="3"/>'
                 f'<line x1="{x + 12}" y1="{y + 40}" x2="{x + w - 12}" y2="{y + 40}" stroke="{c}" stroke-width="3"/>')
        for wy in range(y + 60, 380, 34):
            for wx in range(x + 18, x + w - 26, 36):
                body += f'<rect x="{wx}" y="{wy}" width="20" height="18" rx="3" fill="{GOLD}" opacity="{r.uniform(.2, .75):.2f}"/>'
        x += w + 14
    body += f'<rect y="400" width="{W}" height="{H - 400}" fill="{PLUM}"/>'
    body += "".join(f'<rect x="{x}" y="455" width="60" height="6" rx="3" fill="{GOLD}" opacity=".6"/>' for x in range(-20, W, 120))
    body += palm(110, 410, 270, "#120A20", lean=25) + palm(640, 410, 300, "#120A20", lean=-30) + palm(1130, 410, 260, "#120A20", lean=-20)
    return svg(body, d, "South Beach street at night with palm trees")


def celebrate():
    d, bg = night_sky(top=PLUM, bottom="#4A1E5E")
    body = bg + confetti(61, 140)
    body += f'<circle cx="600" cy="230" r="190" fill="{HOT}" opacity=".25" filter="url(#glow)"/>'
    # champagne bottle (tilted)
    body += (f'<g transform="translate(470 300) rotate(28)">'
             f'<path d="M-40 160 L-40 10 Q-40 -30 -14 -50 L-14 -120 L14 -120 L14 -50 Q40 -30 40 10 L40 160 Z" fill="#14082A"/>'
             f'<rect x="-15" y="-130" width="30" height="34" rx="4" fill="{GOLD}"/>'
             f'<rect x="-40" y="40" width="80" height="60" fill="{GOLD}"/>'
             f'<rect x="-30" y="58" width="60" height="6" fill="{PLUM}"/><rect x="-22" y="74" width="44" height="6" fill="{PLUM}"/>'
             f'</g>')
    # spray
    r = random.Random(3)
    for _ in range(36):
        t = r.uniform(0, 1); x, y = 535 + t * 190 + r.uniform(-30, 30), 175 - t * 130 + r.uniform(-25, 25)
        body += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3, 9):.0f}" fill="{GOLD}" opacity="{r.uniform(.4, .95):.2f}"/>'
    # glasses clinking
    for gx, rot in [(760, 14), (860, -14)]:
        body += (f'<g transform="translate({gx} 330) rotate({rot})">'
                 f'<path d="M-36 -110 L36 -110 L22 -10 Q0 4 -22 -10 Z" fill="{LILAC}" opacity=".9"/>'
                 f'<path d="M-30 -70 L30 -70 L22 -10 Q0 4 -22 -10 Z" fill="{GOLD}"/>'
                 f'<rect x="-3" y="-4" width="6" height="74" fill="{LILAC}"/><rect x="-30" y="66" width="60" height="8" rx="4" fill="{LILAC}"/></g>')
    body += f'<g stroke="{GOLD}" stroke-width="5" stroke-linecap="round"><line x1="810" y1="180" x2="810" y2="150"/><line x1="780" y1="190" x2="764" y2="166"/><line x1="840" y1="190" x2="856" y2="166"/></g>'
    # balloons
    for bx, by, c in [(170, 160, HOT), (250, 120, GOLD), (1030, 150, TEAL), (1110, 110, HOT)]:
        body += (f'<path d="M{bx} {by + 64} Q{bx - 20} {by + 140} {bx + 6} {by + 220}" stroke="{LILAC}" stroke-width="2" fill="none" opacity=".7"/>'
                 f'<ellipse cx="{bx}" cy="{by}" rx="46" ry="58" fill="{c}"/><path d="M{bx - 7} {by + 58} L{bx + 7} {by + 58} L{bx} {by + 68} Z" fill="{c}"/>'
                 f'<ellipse cx="{bx - 16}" cy="{by - 22}" rx="10" ry="16" fill="{LILAC}" opacity=".35"/>')
    return svg(body, d, "Champagne, glasses and balloons for a celebration")


def dress():
    d, bg = night_sky(top=PLUM, bottom=PLUM2)
    body = bg + stars(71, 30)
    body += f'<rect x="80" y="420" width="{W - 160}" height="10" rx="5" fill="{PLUM3}"/>'
    # button-up shirt on hanger
    body += (f'<g transform="translate(260 120)">'
             f'<path d="M0 -40 L0 -60 Q0 -76 14 -76" stroke="{LILAC}" stroke-width="5" fill="none"/>'
             f'<path d="M-120 20 L0 -40 L120 20" stroke="{LILAC}" stroke-width="6" fill="none" stroke-linecap="round"/>'
             f'<path d="M-90 0 L-40 -24 L0 6 L40 -24 L90 0 L130 120 L95 130 L80 70 L80 290 L-80 290 L-80 70 L-95 130 L-130 120 Z" fill="{HOT}"/>'
             f'<path d="M-40 -24 L0 30 L40 -24 L18 -26 L0 6 L-18 -26 Z" fill="{LILAC}"/>'
             f'<line x1="0" y1="30" x2="0" y2="290" stroke="#D81B78" stroke-width="4"/>'
             + "".join(f'<circle cx="8" cy="{y}" r="5" fill="{LILAC}"/>' for y in range(60, 280, 44)) +
             '</g>')
    # sneaker
    body += (f'<g transform="translate(600 370)">'
             f'<path d="M-140 40 L-140 -10 Q-136 -40 -100 -46 L-40 -60 Q-10 -96 30 -80 L60 -40 Q110 -30 140 -6 Q160 12 150 40 Z" fill="{LILAC}"/>'
             f'<rect x="-146" y="30" width="302" height="20" rx="10" fill="{GOLD}"/>'
             f'<path d="M-30 -58 L10 -30 M-12 -66 L26 -40 M8 -74 L42 -50" stroke="{PLUM}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M-120 0 Q-60 -14 20 4 Q80 14 130 6" stroke="{HOT}" stroke-width="8" fill="none" stroke-linecap="round"/>'
             f'</g>')
    # heel
    body += (f'<g transform="translate(940 340)">'
             f'<path d="M-120 70 Q-130 40 -96 30 L-30 22 Q20 18 60 -40 Q80 -70 110 -60 Q130 -50 120 -20 L104 70 L92 70 L96 0 Q60 30 0 60 Q-40 76 -120 70 Z" fill="{GOLD}"/>'
             f'<path d="M-96 30 Q-60 22 -30 22" stroke="{HOT}" stroke-width="6" fill="none"/>'
             f'<rect x="-130" y="68" width="70" height="12" rx="6" fill="{PLUM3}"/></g>')
    body += f'<circle cx="940" cy="200" r="90" fill="{GOLD}" opacity=".15" filter="url(#glow)"/>'
    return svg(body, d, "Button-up shirt, clean sneaker and heels")


SCENES = {"party-bus": party_bus, "club": club, "pool": pool, "yacht": yacht,
          "miami": miami, "celebrate": celebrate, "dress": dress}

if __name__ == "__main__":
    for name, fn in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn())
    print("drew", ", ".join(SCENES))
