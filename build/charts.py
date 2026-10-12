"""Small SVG helpers for the demo app screens. All data is invented."""
import math
import random


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def polyline(pts, cls, extra=""):
    return '<polyline class="%s" %s points="%s"/>' % (cls, extra, " ".join("%.1f,%.1f" % p for p in pts))


def load_chart(seed=3, days=28, w=720, h=230):
    """Daily TRIMP bars, chronic load area and ACWR line (team average)."""
    rnd = random.Random(seed)
    padl, padr, padt, padb = 34, 34, 12, 26
    iw, ih = w - padl - padr, h - padt - padb
    trimp, chronic, acwr = [], [], []
    c = 112.0
    a = 112.0
    for d in range(days):
        rest = d % 7 == 6
        game = d % 7 in (2, 5)
        v = 0 if rest else rnd.uniform(150, 185) if game else rnd.uniform(95, 135)
        if d in (19, 20):
            v *= 1.25
        trimp.append(v)
        a = a + (v - a) * 2 / (7 + 1)
        c = c + (v - c) * 2 / (28 + 1)
        chronic.append(c)
        acwr.append(a / c)
    ymax = 220
    bw = iw / days
    x = lambda i: padl + i * bw + bw / 2
    y = lambda v: padt + ih - v / ymax * ih
    ya = lambda r: padt + ih - (r - 0.4) / (1.8 - 0.4) * ih
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for g in (0, 50, 100, 150, 200):
        out.append('<line class="grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%d</text>' % (padl, w - padr, y(g), y(g), padl - 6, y(g) + 4, g))
    for r in (0.8, 1.3):
        out.append('<line class="band" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f">%.1f</text>' % (padl, w - padr, ya(r), ya(r), w - padr + 6, ya(r) + 4, r))
    area = [(x(0), y(0))] + [(x(i), y(v)) for i, v in enumerate(chronic)] + [(x(days - 1), y(0))]
    out.append('<polygon class="area" points="%s"/>' % " ".join("%.1f,%.1f" % p for p in area))
    for i, v in enumerate(trimp):
        if v:
            out.append('<rect class="bar%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>' % (" hot" if v > 170 else "", x(i) - bw * 0.32, y(v), bw * 0.64, y(0) - y(v)))
    out.append(polyline([(x(i), ya(r)) for i, r in enumerate(acwr) if i > 3], "acwr"))
    for i in range(0, days, 7):
        out.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%02d/09</text>' % (x(i), h - 6, 1 + i))
    out.append("</svg>")
    return "".join(out), acwr[-1]


def player_acwr(seed=5, w=720, h=170):
    rnd = random.Random(seed)
    nums = [2, 5, 7, 9, 11, 14, 17, 19, 21, 23, 27, 33, 44, 55, 61, 71, 77, 88]
    vals = [round(rnd.uniform(0.85, 1.25), 2) for _ in nums]
    vals[2], vals[10], vals[15] = 1.42, 1.48, 1.36
    vals[5], vals[12] = 0.71, 0.76
    padl, padb, padt = 30, 24, 18
    iw, ih = w - padl - 10, h - padt - padb
    bw = iw / len(nums)
    y = lambda r: padt + ih - r / 1.8 * ih
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for r in (0.8, 1.3):
        out.append('<line class="band" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%.1f</text>' % (padl, w - 10, y(r), y(r), padl - 4, y(r) + 4, r))
    for i, (n, v) in enumerate(zip(nums, vals)):
        cls = "hi" if v > 1.3 else "lo" if v < 0.8 else "ok"
        xx = padl + i * bw
        out.append('<rect class="pb %s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>' % (cls, xx + bw * 0.18, y(v), bw * 0.64, y(0) - y(v)))
        if cls != "ok":
            out.append('<text class="flag %s" x="%.1f" y="%.1f" text-anchor="middle">%.2f</text>' % (cls, xx + bw / 2, y(v) - 5, v))
        out.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">#%d</text>' % (xx + bw / 2, h - 6, n))
    out.append("</svg>")
    return "".join(out)


def hr_zones(seed=9, w=520, h=200):
    """Firstbeat-style stacked minutes in HR zones for a few players."""
    rnd = random.Random(seed)
    players = ["#7", "#11", "#14", "#21", "#27", "#44"]
    zones = ["z1", "z2", "z3", "z4", "z5"]
    padl, padt = 36, 8
    rowh = (h - padt - 22) / len(players)
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for i, p in enumerate(players):
        mins = [rnd.uniform(8, 16), rnd.uniform(10, 18), rnd.uniform(8, 14), rnd.uniform(5, 11), rnd.uniform(2, 7)]
        tot = 75
        xx = padl
        yy = padt + i * rowh
        out.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (padl - 6, yy + rowh * 0.62, p))
        for z, m in zip(zones, mins):
            ww = m / tot * (w - padl - 10)
            out.append('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (z, xx, yy + 3, ww, rowh - 8))
            xx += ww
    out.append('<text class="ax" x="%d" y="%d">0</text><text class="ax" x="%d" y="%d" text-anchor="end">75 min</text>' % (padl, h - 4, w - 10, h - 4))
    out.append("</svg>")
    return "".join(out)


def power_trace(seed=11, w=720, h=240):
    """56-minute bike session: warm-up, 3x6 s sprints, 3 sets of 10x10 s, with HR."""
    rnd = random.Random(seed)
    padl, padr, padt, padb = 34, 34, 10, 24
    iw, ih = w - padl - padr, h - padt - padb
    secs = 56 * 60
    pw = []
    for t in range(0, secs, 5):
        m = t / 60
        if m < 12:
            v = 130 + m * 6 + rnd.uniform(-12, 12)
        elif m < 18:
            v = 160 + rnd.uniform(-10, 10)
            if int(m * 60) % 120 < 6:
                v = rnd.uniform(560, 640)
        else:
            k = (t - 18 * 60) % 220
            setno = (t - 18 * 60) // 900
            v = 170 + rnd.uniform(-10, 10)
            if (t - 18 * 60) % 900 < 600 and k % 60 < 10:
                v = 600 + setno * 40 + rnd.uniform(-40, 40)
        pw.append(max(60, v))
    hr = []
    hv = 105.0
    for i, v in enumerate(pw):
        target = 100 + v * 0.11
        hv += (target - hv) * 0.06
        hr.append(hv)
    ymax = 800
    x = lambda i: padl + i / len(pw) * iw
    y = lambda v: padt + ih - v / ymax * ih
    yh = lambda v: padt + ih - (v - 90) / (190 - 90) * ih
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for g in (0, 200, 400, 600, 800):
        out.append('<line class="grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%d</text>' % (padl, w - padr, y(g), y(g), padl - 6, y(g) + 4, g))
    for i, v in enumerate(pw):
        cls = "z7" if v > 500 else "z2" if v > 150 else "z1"
        out.append('<rect class="%s" x="%.1f" y="%.1f" width="%.2f" height="%.1f"/>' % (cls, x(i), y(v), iw / len(pw) + 0.3, y(0) - y(v)))
    out.append(polyline([(x(i), yh(v)) for i, v in enumerate(hr)], "hr"))
    for m in (0, 10, 20, 30, 40, 50):
        out.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%d:00</text>' % (padl + m * 60 / secs * iw, h - 6, m))
    for v in (100, 140, 180):
        out.append('<text class="ax hrax" x="%d" y="%.1f">%d</text>' % (w - padr + 6, yh(v) + 4, v))
    out.append("</svg>")
    return "".join(out)


def rep_bars(seed=13, w=720, h=200):
    rnd = random.Random(seed)
    vals = []
    for s, base in enumerate((600, 650, 690)):
        for r in range(10):
            vals.append(base - 120 + r * 14 + rnd.uniform(-25, 25) if s == 0 else base + rnd.uniform(-40, 40))
    padl, padb, padt = 34, 22, 10
    iw, ih = w - padl - 10, h - padt - padb
    bw = iw / len(vals)
    y = lambda v: padt + ih - v / 900 * ih
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for g in (0, 300, 600, 900):
        out.append('<line class="grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%d</text>' % (padl, w - 10, y(g), y(g), padl - 6, y(g) + 4, g))
    for i, v in enumerate(vals):
        cls = ("s1", "s2", "s3")[i // 10]
        out.append('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>' % (cls, padl + i * bw + bw * 0.14, y(v), bw * 0.72, y(0) - y(v)))
    for s in range(3):
        out.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">S%d</text>' % (padl + (s * 10 + 5) * bw, h - 5, s + 1))
    out.append("</svg>")
    return "".join(out)


def season_plan(w=720, h=230):
    """Planned vs done weekly load across the season, with game counts."""
    rnd = random.Random(21)
    weeks = 30
    padl, padb, padt = 34, 36, 10
    iw, ih = w - padl - 10, h - padt - padb
    bw = iw / weeks
    y = lambda v: padt + ih - v / 1000 * ih
    out = ['<svg viewBox="0 0 %d %d" class="chart" role="img">' % (w, h)]
    for g in (0, 500, 1000):
        out.append('<line class="grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%d</text>' % (padl, w - 10, y(g), y(g), padl - 6, y(g) + 4, g))
    for i in range(weeks):
        phase = 880 if i < 6 else 700 - 120 * (i % 4 == 3)
        games = 0 if i < 5 else 3 if i % 3 == 0 else 2
        planned = phase
        done = planned + rnd.uniform(-70, 60) if i < 9 else None
        xx = padl + i * bw
        out.append('<rect class="plan" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>' % (xx + bw * 0.15, y(planned), bw * 0.7, y(0) - y(planned)))
        if done:
            out.append('<rect class="done" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>' % (xx + bw * 0.15, y(done), bw * 0.7, y(0) - y(done)))
        for g in range(games):
            out.append('<circle class="gm" cx="%.1f" cy="%.1f" r="2.6"/>' % (xx + bw / 2, h - 28 + g * 0 - g * 7 + 7))
        if i == 9:
            out.append('<line class="now" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (xx, xx, padt, h - padb))
    months = ["AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR"]
    for k, m in enumerate(months):
        out.append('<text class="ax" x="%.1f" y="%d">%s</text>' % (padl + k * 4.2 * bw, h - 2, m))
    out.append("</svg>")
    return "".join(out)
