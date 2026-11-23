# -*- coding: utf-8 -*-
"""make_gantt_png.py — static PNG Gantt for 01-project-plan (educational data)."""
import csv, os, datetime
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))          # build/
DIR = os.path.dirname(OUT)                                 # 01-project-plan
TASKS = os.path.join(DIR, "tasks.csv")
CAL   = os.path.join(DIR, "calendar.csv")
OUTPNG = os.path.join(DIR, "gantt.png")

rows = list(csv.DictReader(open(TASKS, encoding="utf-8")))
cal = list(csv.DictReader(open(CAL, encoding="utf-8")))
font = ImageFont.load_default(size=15)
small = ImageFont.load_default(size=12)

PHASE_COLOR = {
    "Initiation & governance": (154, 165, 177),     # #9aa5b1
    "UX & portal (design)": (79, 134, 198),         # #4f86c6
    "Planning & control": (112, 48, 160),           # #7030a0
    "UX & portal (build)": (47, 111, 176),          # #2f6fb0
    "Quality & acceptance": (232, 163, 61),         # #e8a33d
    "Manuscript & QA gate": (106, 168, 79),         # #6aa84f
}
PHASE_COLOR_L = {k: (max(c[0]-12,0), max(c[1]-12,0), max(c[2]-12,0)) for k, c in PHASE_COLOR.items()}

WEEKS = 16
COL_W = 150
NAME_W = 240
TOP = 70
ROW_H = 52
canvas_w = NAME_W + WEEKS * COL_W + 30
canvas_h = TOP + len(rows) * ROW_H + 60

def wk_date(i):
    # i = working day index 1..80
    d, cnt = datetime.date(2026, 9, 7), 0
    while True:
        if d.weekday() < 5:
            cnt += 1
            if cnt == i:
                return d
        d += datetime.timedelta(days=1)

import datetime
def wk_label(i):
    return "W" + str(i) + "\n" + wk_date((i-1)*5+1).strftime("%d %b")

img = Image.new("RGB", (canvas_w, canvas_h), "white")
d = ImageDraw.Draw(img, "RGBA")

# --- header ---
d.rectangle([0, 0, canvas_w, TOP-10], fill=(24, 38, 56))
d.text((14, 10), "Гант-діаграма — інтегрований навчальний цикл (16 тижнів)", fill="white", font=font)
d.text((14, 42), "Тема 46 · корпоративний портал підприємства · 16-тиждень симуляційний план (2026-09-07 .. 2026-12-25)", fill=(150,165,180), font=small)

# --- legend ---
lx = 14
for i, ph in enumerate(["Initiation & governance", "UX & portal (design)", "Planning & control",
                        "UX & portal (build)", "Quality & acceptance", "Manuscript & QA gate"]):
    yy = 78 + i * 18
    d.rectangle([lx, yy+2, lx+14, yy+16], fill=PHASE_COLOR[ph], outline="white")
    d.text((lx+20, yy), ph, fill="black", font=small)

# --- week axis ---
d.rectangle([NAME_W, TOP-6, NAME_W + WEEKS*COL_W, TOP+4], fill=(230,230,230), outline=(150,150,150))
d.text((NAME_W + 6, TOP-34), "Тижні →", fill=(90,90,90), font=small)
for i in range(1, WEEKS+1):
    x = NAME_W + (i-1)*COL_W
    d.line([(x, TOP-6), (x, TOP+4)], fill=(120,120,120), width=1)
    d.text((x-26, TOP-26), wk_label(i), fill=(80,80,80), font=small)

# --- rows ---
y = TOP + 10
for r in rows:
    name = r["task_id"] + " " + r["task_name"]
    dur = int(r["duration_workdays"]); s = int(r["start_workday"]); f = int(r["finish_workday"])
    d.rectangle([0, y, NAME_W, y+ROW_H], fill=(248,249,250), outline=(225,225,225))
    d.text((8, y+14), name, fill=(40,40,40), font=small)
    for wk in range(1, WEEKS+1):
        ws = (wk-1)*5 + 1; we = wk*5
        x = NAME_W + (wk-1)*COL_W
        if s <= we and f >= ws:
            ov = min(f, we) - max(s, ws) + 1
            pct = ov / dur
            col = PHASE_COLOR.get(r["phase"], (150,150,150))
            d.rectangle([x, y+3, x + int(pct*COL_W), y+ROW_H-3], fill=col, outline=(220,220,220))
    # status chips
    if r["task_id"] in ("T-19","T-20","T-21","T-22"):
        d.text((NAME_W + WEEKS*COL_W - 10, y+ROW_H//2 - 6), "inprog", fill=(180,60,60), font=small)
    elif r["task_id"] in ("T-23","T-24"):
        d.text((NAME_W + WEEKS*COL_W - 10, y+ROW_H//2 - 6), "pending", fill=(110,110,110), font=small)
    y += ROW_H

# --- milestone markers ---
for i, r in enumerate(rows):
    if r["task_id"] in ("T-19", "T-20", "T-21", "T-22", "T-23", "T-24"):
        pass
# draw milestones as extra diamonds at bottom row area (fake) -> skip, documented in milestones.csv/log

d.rectangle([0, canvas_h-140, canvas_w, canvas_h-40], fill=(240,240,240), outline=(180,180,180))
d.text((14, canvas_h-134), "БУГЕТ БАС = 32,264 USD · ПВ = 28,060 · ВИН = 25,819.6 · ВА = 26,118 · SPI = 0.92 · CPI = 0.99 · дата стану 2026-11-06 · відносна вартість -372.88 USD", fill=(60,60,60), font=small)

img.save(OUTPNG, "PNG")
print("saved", OUTPNG, img.size)
