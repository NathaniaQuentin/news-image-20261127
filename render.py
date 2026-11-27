#!/usr/bin/env python3
"""Render the Friday 27 November 2026 world-news front page as news.png.

Build-time only: draws a 1024x1024 newspaper front page with PIL and the
local DejaVu fonts. No network, no downloaded assets.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
INK = (18, 18, 18)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
ACCENT = (140, 20, 20)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
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


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, spacing=3, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def section_head(draw, x, y, label, width):
    f = font(SANS_B, 12)
    draw.text((x, y), label.upper(), font=f, fill=ACCENT)
    rule(draw, x, y + 17, x + width, 2)
    return y + 24


# ---------------------------------------------------------------- stories
LEADS = [
    (
        "Drone strike in Kuwait kills two Italians; Iran denies role",
        "Kuwait says an Iranian drone attack killed two Italian workers "
        "and wounded others. Tehran denies responsibility as Gulf states "
        "condemn the strike and flights are diverted.",
    ),
    (
        "Storm wrecks Thanksgiving: Macy's parade postponed for first time",
        "A huge storm battered the US north-east on Thanksgiving. New York "
        "postponed the 100th Macy's parade for the first time ever, more "
        "than 500,000 homes lost power and hundreds of flights were cut.",
    ),
    (
        "Trump's new tariffs hit 14 partners; China and allies hit back",
        "Washington proposed sweeping tariffs of up to 40% on 14 trading "
        "partners after a probe into excess industrial capacity. China, "
        "Japan and the EU protested; markets fell and Brent crude jumped.",
    ),
]

PANELS = [
    (
        "Gaza: Hamas weighs reply after Israel kills 10",
        "Hamas was weighing its response after Israeli strikes killed ten "
        "people in Gaza. Sixteen schoolchildren have been killed in Gaza "
        "this month, the territory's health ministry said.",
    ),
    (
        "UK migration falls to lowest since 1997",
        "Net migration to Britain fell to its lowest level since 1997, "
        "excluding the pandemic years, official figures showed.",
    ),
    (
        "Depardieu to stand trial over alleged rape",
        "A French court ruled Gerard Depardieu will stand trial over the "
        "alleged rape of an actress in 2018. He denies the allegations.",
    ),
    (
        "Tanker capsizes off Ibiza; one dead",
        "A diesel tanker carrying up to 7,000 tonnes capsized near Ibiza, "
        "killing one person. A clean-up and salvage operation began.",
    ),
    (
        "Musk: every US child to get two SpaceX shares",
        "Elon Musk said every child in the United States would receive "
        "two shares in SpaceX, in a surprise announcement.",
    ),
    (
        "Chess: Gukesh and Sindarov draw marathon Game 3",
        "Gukesh and Sindarov played out a marathon draw in Game 3 of the "
        "World Championship match. Nothing separates them after three games.",
    ),
    (
        "New Zealand awaits final election count",
        "Final results, including about 400,000 special votes, were due in "
        "the afternoon. The coalition holds a slim 67 of 131 seats so far.",
    ),
    (
        "Russia hits Kyiv with ballistic missiles",
        "Russian forces struck Kyiv with ballistic missiles overnight, the "
        "city's mayor said, as air defences worked across the capital.",
    ),
    (
        "Houthis strike Saudi refinery; Brent jumps",
        "Yemen's Houthis said they attacked Saudi Arabia's Jazan refinery. "
        "A Nepali worker was killed. Brent crude settled 3.5% higher.",
    ),
    (
        "S&P 500 in correction as AI rally fades",
        "Wall Street fell into correction, down about 10% from October "
        "highs. Nvidia slid 3.9% as AI shares lost steam for a second day.",
    ),
    (
        "Bank of Korea lifts rates on AI boom",
        "South Korea's central bank raised its key rate to fight inflation "
        "as the AI chip boom fuels growth and price pressures.",
    ),
    (
        "SpaceX cleared for orbital data centres",
        "The US regulator said SpaceX may deploy satellites for space "
        "data centres, clearing a new frontier for computing in orbit.",
    ),
]

BRIEFS = [
    "Ebola in Congo passes 12,000 cases; responders flee unrest.",
    "Nepal to declare 4,000 missing landslide victims dead.",
    "Belgium opens Europe's biggest satellite factory.",
    "India top court: judge must sit to confirm PMLA seizures.",
    "India court quashes early release of ex-MP Anand Mohan.",
    "India clears Rs 11,000 crore manufacturing scheme.",
    "GST cancellations go automatic in India from 1 Dec.",
    "US grounds flights to Washington Reagan airport in storm.",
    "300+ Russians killed backing Mali's junta, reports say.",
    "France's mainstream faces presidential vote debacle.",
    "Kim Jong Un vows permanent nuclear armament.",
    "US approves $621.9m F-16 support package for Ukraine.",
    "Ukrainian drones hit a key Russian fertiliser plant.",
    "French navy seizes suspected drug-smuggling vessel.",
    "EU urged to act over Turkey-Libya maritime deal.",
    "2,000 march in Paris for more education funding.",
    "Estonia to shut rail border with Russia over sabotage.",
    "Spain sends troops to El Hierro in migrant emergency.",
    "Barrett to captain All Blacks for first time, vs England.",
    "Australian PGA: Kibori tied second after round one.",
    "India-NZ second Test starts in Christchurch.",
    "Ferrari boss sets Hamilton, Leclerc a clear target.",
    "Anthropic's Claude now turns artifacts into apps.",
    "New evidence hints at a giant planet beyond Neptune.",
    "China's drones are reshaping Asia's militaries.",
    "US judge: FCC violated ABC's free speech, reports say.",
    "Black Friday: basics join gifts in shoppers' carts.",
    "Consumer NZ: half of sale items were no cheaper.",
    "US markets shut for Thanksgiving; short Friday session.",
    "Nvidia halts chip shipments to four SE Asian states.",
]

REGIONS = [
    ("AMERICAS", "Storm halts parade; tariffs roil markets"),
    ("EUROPE", "UK migration low; Depardieu trial ordered"),
    ("MIDDLE EAST", "Kuwait drone strike; Gaza toll rises"),
    ("ASIA-PACIFIC", "NZ count due; Korea raises rates"),
    ("AFRICA", "Ebola passes 12,000 in Congo; Mali toll"),
]

TIMELINE = [
    ("00:03", "EU gives little on US drug-pricing pressure"),
    ("01:03", "Two Italians killed in Kuwait drone strike"),
    ("02:05", "BBC confirms Kuwait strike; Iran denies role"),
    ("02:26", "Hamas weighs reply after 10 killed in Gaza"),
    ("03:31", "Tanker capsizes off Ibiza; one dead"),
    ("14:00", "NZ final election count due (2pm local)"),
]


def main():
    img = Image.new("RGB", (W, H), (252, 250, 244))
    d = ImageDraw.Draw(img)
    mx = 26
    right = W - mx

    # ---- masthead
    f_title = font(SERIF_B, 52)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 21)
    date = "FRIDAY 27 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 76), date, font=f_date, fill=ACCENT)
    f_tag = font(SANS, 11)
    tag = "One day's world news  \u00b7  Friday edition  \u00b7  All times UTC unless stated"
    tgw = d.textlength(tag, font=f_tag)
    d.text(((W - tgw) / 2, 106), tag, font=f_tag, fill=GREY)
    rule(d, mx, 126, right, 3)

    # ---- lead stories: three columns
    col_w = (right - mx - 2 * 18) // 3
    y = 138
    lead_bottom = y
    for i, (head, deck) in enumerate(LEADS):
        x = mx + i * (col_w + 18)
        yy = draw_wrapped(d, x, y, head, font(SERIF_B, 19), col_w,
                          spacing=2, max_lines=4)
        yy += 2
        yy = draw_wrapped(d, x, yy, deck, font(SERIF, 12), col_w,
                          spacing=2, max_lines=5)
        lead_bottom = max(lead_bottom, yy)
    rule(d, mx, lead_bottom + 10, right, 2)

    # ---- middle: panels left, briefs right
    mid_y = lead_bottom + 22
    split_x = 700
    y = section_head(d, mx, mid_y, "The day's big stories", split_x - mx - 14)
    panel_col_w = (split_x - mx - 14 - 16) // 2
    per_col = 6
    panel_h = 78
    for i, (head, body) in enumerate(PANELS):
        col = i // per_col
        row = i % per_col
        x = mx + col * (panel_col_w + 16)
        yy = y + row * panel_h
        yy = draw_wrapped(d, x, yy, head, font(SANS_B, 12), panel_col_w,
                          spacing=1, max_lines=2)
        draw_wrapped(d, x, yy, body, font(SANS, 10), panel_col_w,
                     spacing=1, max_lines=3)
    panels_bottom = y + per_col * panel_h

    by = section_head(d, split_x, mid_y, "In brief", right - split_x)
    bf = font(SANS, 10)
    for b in BRIEFS:
        lines = wrap(d, "\u2022  " + b, bf, right - split_x)
        for ln in lines:
            d.text((split_x, by), ln, font=bf, fill=INK)
            by += 13
        by += 1
    briefs_bottom = by

    bottom = max(panels_bottom, briefs_bottom)
    rule(d, mx, bottom + 8, right, 2)

    # ---- regions strip
    y = bottom + 18
    y = section_head(d, mx, y, "Around the regions", right - mx)
    reg_w = (right - mx - 4 * 12) // 5
    for i, (reg, txt) in enumerate(REGIONS):
        x = mx + i * (reg_w + 12)
        d.text((x, y), reg, font=font(SANS_B, 11), fill=ACCENT)
        draw_wrapped(d, x, y + 15, txt, font(SANS, 10), reg_w,
                     spacing=1, max_lines=3)
    y += 62
    rule(d, mx, y, right, 1)

    # ---- UTC timeline
    y += 10
    y = section_head(d, mx, y, "The day in UTC", right - mx)
    tl_w = (right - mx - 5 * 10) // 6
    for i, (t, txt) in enumerate(TIMELINE):
        x = mx + i * (tl_w + 10)
        d.text((x, y), t, font=font(SANS_B, 12), fill=ACCENT)
        draw_wrapped(d, x, y + 16, txt, font(SANS, 10), tl_w,
                     spacing=1, max_lines=3)
    y += 58

    # ---- footer
    rule(d, mx, H - 34, right, 2)
    f_foot = font(SANS, 10)
    foot = ("Friday 27 November 2026  \u00b7  Sources: BBC, Reuters, AP, NYT, "
            "Newstalk ZB  \u00b7  One image, one day.")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 26), foot, font=f_foot, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
