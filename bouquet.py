# -*- coding: utf-8 -*-
# Пышный цветной букет с корнями для консоли (cmd / Windows Terminal / Linux)
# Запуск: python bouquet.py      (окно консоли шириной от 112 символов)
import os, random, math, sys, time
os.system("")
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

R = "\033[0m"
def c(code): return f"\033[{code}m"
RED, PINK, MAG, YEL, ORG, BLUE, CYAN, WHITE, VIO = (c("1;91"), c("1;95"), c("35"), c("1;93"),
    c("33"), c("1;94"), c("1;96"), c("1;97"), c("34"))
GREEN, DGREEN = c("1;92"), c("32")
BROWN, LBROWN = c("38;5;130"), c("38;5;180")

W, H = 262, 76
cv = [[" "] * W for _ in range(H)]
col = [[""] * W for _ in range(H)]
def put(x, y, ch, cl):
    if 0 <= x < W and 0 <= y < H and ch != " ":
        cv[y][x] = ch; col[y][x] = cl

ROSE  = ["  .--.  ", " (@@@@) ", "(@(**)@)", " (@@@@) ", "  `--'  "]
PEONY = ["  ,@@@,  ", " @@@@@@@ ", "@@@(*)@@@", " @@@@@@@ ", "  '@@@'  "]
DAISY = [" \\ | / ", "-- * --", " / | \\ "]
TULIP = ["\\/\\/\\/", " |@@| ", "  \\/  "]
SMALL = [" .-. ", "( o )", " '-' "]
BELL  = [" ,*, ", "(***)", " v v "]
ASTER = [" .:*:. ", ":*(o)*:", " ':*:' "]
BIG   = ["   _.-._   ", " .(@@@@@). ", "(@@(***)@@)", " `(@@@@@)' ", "   `-.-'   "]
TPLS = [ROSE, ROSE, PEONY, PEONY, DAISY, TULIP, SMALL, BELL, ASTER, BIG]
PAL = [RED, PINK, MAG, YEL, ORG, BLUE, CYAN, WHITE, VIO, RED, PINK]

def flower(t, cx, cy, petal):
    h, w = len(t), len(t[0])
    for j, row in enumerate(t):
        for i, ch in enumerate(row):
            if ch == " ": continue
            cl = YEL if ch in "*o" else petal
            if t is DAISY and ch in "\\/|-": cl = WHITE if petal != WHITE else PINK
            if t is ASTER and ch in ".:'": cl = WHITE
            put(cx - w // 2 + i, cy - h // 2 + j, ch, cl)
            # фон под цветком стираем, чтобы цветы не «просвечивали»
        for i, ch in enumerate(row):
            if ch == " " and 0 < i < w - 1 and row[:i].strip() and row[i:].strip():
                x, y = cx - w // 2 + i, cy - h // 2 + j
                if 0 <= x < W and 0 <= y < H: cv[y][x] = " "; col[y][x] = ""

random.seed(2026)
GX, GY = W // 2, 45          # точка сбора стеблей
CX, CY, RX, RY = GX, 25, 84, 21

# позиции цветов: плотная сетка внутри купола
spots = []
for y in range(CY - RY, CY + 13, 3):
    for x in range(CX - RX, CX + RX + 1, 6):
        x2 = x + random.randint(-2, 2) + (3 if (y // 4) % 2 else 0)
        y2 = y + random.randint(-1, 1)
        dx, dy = (x2 - CX) / RX, (y2 - CY) / RY
        if dx * dx + dy * dy <= 1.0 and y2 < GY - 6:
            spots.append((x2, y2))


# ---------- извилистые ветки во все стороны ----------
def stemch(dx, dy):
    if abs(dx) < 0.45 * abs(dy): return "|" if random.random() < .8 else "("
    if abs(dy) < 0.45 * abs(dx): return "~" if random.random() < .6 else "-"
    return "/" if (dx > 0) == (dy < 0) else "\\"
def curve(x0, y0, x1, y1, bend, waves, amp):
    pts, n = [], int(math.hypot(x1 - x0, (y1 - y0) * 2) * 3) + 2
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
    cx, cy = mx + nx * bend, my + ny * bend * 0.5
    for k in range(n + 1):
        t = k / n
        x = (1-t)**2*x0 + 2*(1-t)*t*cx + t*t*x1
        y = (1-t)**2*y0 + 2*(1-t)*t*cy + t*t*y1
        w = math.sin(t * math.pi * waves) * amp * math.sin(t * math.pi)
        pts.append((x + nx * w, y + ny * w * 0.5))
    return pts
def draw_path(pts, leaves=True):
    prev = None
    for k, (x, y) in enumerate(pts):
        p = (round(x), round(y))
        if p == prev: continue
        if k > 0:
            dx, dy = x - pts[k-1][0], y - pts[k-1][1]
            put(p[0], p[1], stemch(dx, dy), GREEN if k % 4 else DGREEN)
        if leaves and k % 11 == 5 and random.random() < .85:
            side = random.choice([-1, 1])
            leaf = random.choice(["(\\)", "(/)", "<>", "{}", "~"])
            for i, ch in enumerate(leaf):
                put(p[0] + side * (2 + i) if side > 0 else p[0] - 2 - len(leaf) + 1 + i, p[1], ch, random.choice([GREEN, DGREEN]))
        if leaves and k % 23 == 17 and random.random() < .5:
            put(p[0] + random.choice([-2, 2]), p[1] - 1, "@", DGREEN)   # завиток-усик
        prev = p

sprays = []
for k in range(32):
    a = math.radians(-16 + k * (212 / 31) + random.uniform(-3, 3))
    rx, ry = random.uniform(100, 128), random.uniform(20, 24)
    ex, ey = GX + rx * math.cos(a), 23 - ry * math.sin(a)
    ey = max(2, ey)
    pts = curve(GX + random.randint(-3, 3), GY, ex, ey,
                random.uniform(-18, 18), random.choice([2, 3, 4]), random.uniform(2, 4))
    draw_path(pts)
    sprays.append((round(ex), round(ey)))
    # боковые веточки с бутонами
    for _ in range(2):
        i0 = random.randint(len(pts) // 2, len(pts) - 5)
        bx, by = pts[i0]
        tx, ty = bx + random.uniform(-14, 14), by - random.uniform(3, 8)
        draw_path(curve(bx, by, tx, ty, random.uniform(-4, 4), 2, 1), leaves=False)
        sprays.append((round(tx), round(ty), "bud"))

# стебли
for (x, y) in spots:
    steps = max(abs(GX - x), abs(GY - y)) * 2
    for s in range(steps + 1):
        t = s / steps
        px, py = round(x + (GX - x) * t), round(y + (GY - y) * t)
        dx = GX - x
        ch = "|" if abs(dx) < (GY - y) * 0.4 else ("\\" if dx > 0 else "/")
        put(px, py, ch, DGREEN if s % 3 else GREEN)

# листья и зелень по краю купола
for k in range(150):
    a = math.pi * random.random()
    rr = random.uniform(1.0, 1.12)
    x = int(CX + RX * rr * math.cos(a)); y = int(CY + 4 - RY * rr * math.sin(a))
    leaf = random.choice(["(\\)", "(/)", "~~", "}{", ")(", "//", "\\\\", "*"])
    for i, ch in enumerate(leaf):
        put(x + i, y, ch, random.choice([GREEN, DGREEN]))
for _ in range(130):  # мелкие цветочки-гипсофила
    a = math.pi * random.random(); rr = random.uniform(0.95, 1.15)
    put(int(CX + RX * rr * math.cos(a)), int(CY + 2 - RY * rr * math.sin(a)), random.choice("*.o"), WHITE)

# цветы: сзади вперёд (сверху вниз)
spots.sort(key=lambda p: p[1])
for i, (x, y) in enumerate(spots):
    flower(random.choice(TPLS), x, y, random.choice(PAL))

BUD = ["(@)"]
for sp in sprays:
    if len(sp) == 3:
        flower(random.choice([BUD, SMALL, BELL]), sp[0], sp[1], random.choice(PAL))
    else:
        flower(random.choice(TPLS), sp[0], sp[1], random.choice(PAL))

# обёртка
top = GY - 1
for x in range(GX - 50, GX + 51):
    put(x, top - 1, "^" if x % 2 else "~", PINK)
for j in range(17):
    y = top + j
    half = 49 - j * 2.8
    l, r = round(GX - half), round(GX + half)
    for x in range(l, r + 1):
        if x == l: ch, cl = "\\", MAG
        elif x == r: ch, cl = "/", MAG
        else:
            ch = ":" if (x + j) % 4 == 0 else ("." if (x - j) % 4 == 0 else "░")
            cl = PINK if (x // 4 + j) % 2 else MAG
        put(x, y, ch, cl)
wrap_bottom = top + 17

# бант
bow = ["  ___        ___  ", " /   \\__()__/   \\ ", " \\___/  ||  \\___/ ",
       "       / || \\      ", "      /  ||  \\     ", "     ~   ~~   ~    "]
for j, row in enumerate(bow):
    for i, ch in enumerate(row):
        put(GX - 9 + i, top + 2 + j, ch, YEL if ch in "()" else RED)

# стебли снизу из обёртки
for j in range(4):
    y = wrap_bottom + j
    for x in range(GX - 2 - j // 2, GX + 3 + j // 2):
        put(x, y, "|" if (x + j) % 2 == 0 else "!", GREEN if x % 2 else DGREEN)
soil = wrap_bottom + 4

# корни
for x in range(GX - 45, GX + 46):
    put(x, soil, random.choice("~_.,"), LBROWN)
def root(x, y, dirx, life):
    while life > 0 and y < H - 1:
        y += 1
        if random.random() < 0.6: x += dirx
        if random.random() < 0.15: dirx = random.choice([-1, 0, 1])
        ch = "|" if dirx == 0 else ("/" if dirx < 0 else "\\")
        put(x, y, ch, BROWN if life > 3 else LBROWN)
        if random.random() < 0.18 and life > 4:
            root(x, y, random.choice([-1, 1]), life // 2)
        life -= 1
for k, d in enumerate([-2, -2, -1, -1, 0, 0, 1, 1, 2, 2]):
    root(GX - 5 + k, soil, d, random.randint(10, 15))

# вывод
first = next(y for y in range(H) if any(ch != " " for ch in cv[y]))
last = max(y for y in range(H) if any(ch != " " for ch in cv[y]))
title = "✿ ❀ ✿   Б У К Е Т   Д Л Я   Т Е Б Я   ✿ ❀ ✿"
print("\n" + " " * ((W - len(title)) // 2) + PINK + title + R + "\n")
for y in range(first, last + 1):
    line, lastc = "", None
    for x in range(W):
        cl = col[y][x]
        if cl != lastc: line += R + cl; lastc = cl
        line += cv[y][x]
    print(line.rstrip() + R)
    time.sleep(0.02)
print()
