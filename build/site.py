"""Builds the ForeCheck feature pages. Run from the repo root: python3 build/site.py

Every visible string goes through t(key, english). Translations live in build/i18n_pages.json
as {key: {"de": ..., "fr": ..., "it": ...}}; anything missing falls back to English.
All numbers and players on these pages are invented demo data.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import charts as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR_PATH = os.path.join(ROOT, "build", "i18n_pages.json")
TR = json.load(open(TR_PATH, encoding="utf-8")) if os.path.exists(TR_PATH) else {}

PAGES = [
    ("load", "load.html", "Load"),
    ("conditioning", "conditioning.html", "Conditioning"),
    ("calendar", "calendar.html", "Calendar"),
    ("strength", "strength.html", "Strength & testing"),
    ("rehab", "rehab.html", "Rehab"),
    ("players", "players.html", "Players"),
]

_dict = {}


def t(key, en, tag="span", cls=None):
    _dict[key] = dict({"en": en}, **TR.get(key, {}))
    c = ' class="%s"' % cls if cls else ""
    return '<%s%s data-i18n="%s">%s</%s>' % (tag, c, key, en, tag)


def tt(key, en):
    """Register a string and return it bare, for elements that carry data-i18n themselves."""
    _dict[key] = dict({"en": en}, **TR.get(key, {}))
    return en


LOGO = '<svg viewBox="6 12 104 90" fill="currentColor" aria-hidden="true"><polygon points="44,98 57,98 104,16"/><polygon points="62,98 68,98 104,16"/><polygon points="73,98 76,98 104,16"/><polygon points="12,56 32,56 58,98 38,98"/><polygon points="10,52 100,52 100,55.5 10,55.5"/><polygon points="104,16 19,52 11,52"/></svg>'


def header(active):
    links = "".join('<a href="%s"%s data-i18n="nav_%s">%s</a>' % (href, ' aria-current="page"' if pid == active else "", pid, tt("nav_" + pid, label)) for pid, href, label in PAGES)
    return """<header class="top">
  <div class="wrap">
    <a class="mark" href="index.html" aria-label="ForeCheck home">%s<span>Fore<b>Check</b></span></a>
    <nav class="links pages" aria-label="Product">%s</nav>
    <div class="actions">
      <label class="lang" title="Language"><span class="sr">Language</span><select id="lang-select" aria-label="Language"><option value="en">EN</option><option value="de">DE</option><option value="fr">FR</option><option value="it">IT</option></select></label>
      <a class="btn" href="index.html#contact" data-i18n="cta_talk">%s</a>
    </div>
  </div>
  <details class="menu"><summary data-i18n="menu">%s</summary><nav aria-label="Product">%s</nav></details>
</header>""" % (LOGO, links, tt("cta_talk", "Talk to us"), tt("menu", "Product"), links)


def footer(active):
    nxt = PAGES[(next(i for i, p in enumerate(PAGES) if p[0] == active) + 1) % len(PAGES)]
    return """<section class="next">
  <div class="wrap next-row">
    <div><p class="eyebrow">%s</p><a class="next-link" href="%s" data-i18n="nav_%s">%s</a></div>
    <div class="contact"><span class="eyebrow">%s</span><a href="mailto:info@fore-check.ch">info@fore-check.ch</a></div>
  </div>
</section>
<footer><div class="wrap"><span>© 2026 ForeCheck · info@fore-check.ch</span>%s</div></footer>""" % (
        t("next", "Next"), nxt[1], nxt[0], tt("nav_" + nxt[0], nxt[2]), t("email_eyebrow", "Email us"), t("footer_demo", "All player examples on this site use invented demo data."))


def appbar(active_room):
    rooms = ["Locker Room", "Coach's Office", "Conditioning", "Heart Rate", "Testing Lab", "Strength Room", "Rehab Clinic", "Calendar"]
    tabs = "".join('<span class="tab%s">%s</span>' % (" on" if r == active_room else "", r) for r in rooms)
    return '<div class="appbar"><span class="appmark">%s FORECHECK</span><div class="tabs">%s</div><span class="tag demo">%s</span></div>' % (LOGO, tabs, t("tag_demo", "Demo data"))


def kpis(items):
    return '<div class="kpis">%s</div>' % "".join('<div class="kpi%s"><span>%s</span><b>%s</b></div>' % (" acc" if acc else "", lab, val) for lab, val, acc in items)


def screen(room, title, sub, body):
    return '<figure class="screen">%s<div class="app"><div class="apphead"><p class="eyebrow">%s</p><h4>%s</h4><span class="sub">%s</span></div>%s</div></figure>' % (
        appbar(room), t("perf", "Performance"), title, sub, body)


def panel(title, body, cls=""):
    return '<div class="pnl %s"><p class="ptitle">%s</p>%s</div>' % (cls, title, body)


def hero(pid, room, h1, lead, art):
    return """<section class="phero" data-bg="%s">
  <canvas class="bgfx" aria-hidden="true"></canvas>
  <div class="wrap phero-in">
    <p class="eyebrow">%s</p>
    <h1>%s</h1>
    <p class="lead">%s</p>
  </div>
  <div class="wrap shot">%s</div>
</section>""" % (pid, room, h1, lead, art)


def rows(items):
    out = []
    for i, (eyebrow, h, p, art) in enumerate(items):
        out.append('<div class="frow%s"><div class="ftext"><p class="eyebrow">%s</p><h3>%s</h3><p>%s</p></div><div class="fart">%s</div></div>' % (" flip" if i % 2 else "", eyebrow, h, p, art))
    return '<section class="features"><div class="wrap">%s</div></section>' % "".join(out)


def answers(qs):
    return '<section class="sheet answers"><div class="wrap"><div class="sec-head"><p class="eyebrow">%s</p><h2>%s</h2></div><ul class="qa">%s</ul></div></section>' % (
        t("qa_eyebrow", "Questions it answers"), t("qa_h2", "What you decide with it"), "".join("<li>%s</li>" % q for q in qs))


# ---------------------------------------------------------------- pages

def page_load():
    chart, acwr = C.load_chart()
    shot = screen("Locker Room", t("ld_screen_t", "Locker Room"), t("ld_screen_s", "Workload and readiness monitoring"),
                  kpis([(t("k_sessions", "Sessions"), "341", 0), (t("k_trimp", "TRIMP / session"), "125", 0), (t("k_acute", "Acute load"), "498", 0), (t("k_chronic", "Chronic load"), "450", 0), (t("k_hrmax", "HR avg % max"), "75", 0), ("ACWR", "%.2f" % acwr, 1)])
                  + panel(t("ld_p1", "Daily TRIMP, chronic load and ACWR · team average"), chart + '<div class="legend"><i class="lg bar"></i>%s<i class="lg area"></i>%s<i class="lg line"></i>ACWR</div>' % (t("lg_day", "Day TRIMP"), t("lg_chronic", "Chronic load")))
                  + panel(t("ld_p2", "Every player · ACWR today · red above 1.3, blue below 0.8"), C.player_acwr()))
    feats = [
        (t("ld_f1e", "Ice load"), t("ld_f1h", "Every shift, practice and game, already counted"),
         t("ld_f1p", "Catapult sessions sync on their own a couple of hours after the ice. ForeCheck turns them into volume, intensity and skating demand per player, so nobody exports or merges anything."),
         panel(t("ld_tbl", "Latest sessions · team average"), table_sessions())),
        (t("ld_f2e", "Heart rate"), t("ld_f2h", "Inside the effort, not only the distance"),
         t("ld_f2p", "Heart-rate zones per player and per session, in the style staff already know from Firstbeat. See who really worked in the red and who cruised."),
         panel(t("hr_p", "Minutes in heart-rate zones · last game"), C.hr_zones() + '<div class="legend"><i class="lg z1"></i>Z1<i class="lg z2"></i>Z2<i class="lg z3"></i>Z3<i class="lg z4"></i>Z4<i class="lg z5"></i>Z5</div>')),
        (t("ld_f3e", "Acute:chronic"), t("ld_f3h", "Spikes flagged before they hurt"),
         t("ld_f3p", "A rolling acute:chronic workload ratio (EWMA 5/20) for every player. Above 1.3 turns red, below 0.8 turns blue, so the conversation starts with the right two names."),
         flags_card()),
    ]
    qs = [t("ld_q1", "Who needs less ice today?"), t("ld_q2", "Who is under-loaded and needs extra work?"), t("ld_q3", "Was last night's game harder than usual?"), t("ld_q4", "Is the team load climbing too fast this week?")]
    return ("load", tt("ld_title", "Load monitoring"),
            hero("load", t("ld_eyebrow", "Locker Room · Heart Rate"), t("ld_h1", 'Less laptop.<br><span class="r">More coaching.</span>'),
                 t("ld_lead", "Ice load, intensity and heart rate for every player, every session. ForeCheck reads the Catapult data for you and shows only the players who need a different plan today."), shot)
            + rows(feats) + answers(qs))


def table_sessions():
    rows_ = [("10/10", "Ice practice", 14, 70, 112, 74), ("09/10", "Game · away", 19, 62, 168, 81), ("08/10", "Ice practice", 13, 75, 142, 77), ("07/10", "Ice practice", 14, 77, 136, 78), ("06/10", "Game · home", 19, 60, 171, 82)]
    head = "<tr><th>%s</th><th>%s</th><th>%s</th><th>min</th><th>TRIMP</th><th>%%HRmax</th></tr>" % (tt("th_date", "Date"), tt("th_session", "Session"), tt("th_players", "Players"))
    head = head.replace("<th>Date</th>", '<th data-i18n="th_date">Date</th>').replace("<th>Session</th>", '<th data-i18n="th_session">Session</th>').replace("<th>Players</th>", '<th data-i18n="th_players">Players</th>')
    body = ""
    for d, s, p, m, tr, hr in rows_:
        key = {"Ice practice": "s_ice", "Game · away": "s_away", "Game · home": "s_home"}[s]
        body += '<tr><td>%s</td><td data-i18n="%s">%s</td><td>%d</td><td>%d</td><td%s>%d</td><td>%d</td></tr>' % (d, key, tt(key, s), p, m, ' class="hot"' if tr > 160 else "", tr, hr)
    return '<div class="tblwrap"><table class="tbl">%s%s</table></div>' % (head, body)


def flags_card():
    items = [("hi", "#27 F", "1.48", t("fl1", "3 games in 4 days · cap ice time")), ("hi", "#7 D", "1.42", t("fl2", "Back from illness · build up gently")), ("lo", "#14 F", "0.71", t("fl3", "Scratched twice · add extra skate"))]
    li = "".join('<li class="%s"><b>%s</b><span class="v">%s</span>%s</li>' % (c, n, v, txt) for c, n, v, txt in items)
    return panel(t("fl_t", "Today's flags"), '<ul class="flags">%s</ul>' % li)


def page_conditioning():
    shot = screen("Conditioning", t("cd_screen_t", "Conditioning"), t("cd_screen_s", "Off-ice bike sessions · efforts, fatigue, next-time targets"),
                  kpis([(t("k_dur", "Duration"), "56:00", 0), (t("k_np", "Average / NP"), "222 / 255 W", 0), (t("k_work", "Work"), "745 kJ", 0), (t("k_hr", "HR avg / max"), "146 / 174", 0), (t("k_best", "Best 5 s"), "834 W", 0), (t("k_ftp", "FTP (est.)"), "223 W", 1)])
                  + panel(t("cd_p1", "Workout · power by zone and heart rate"), C.power_trace() + '<div class="legend"><i class="lg z1"></i>%s<i class="lg z2"></i>%s<i class="lg z7"></i>%s<i class="lg hrl"></i>%s</div>' % (t("lg_rec", "Recovery"), t("lg_end", "Endurance"), t("lg_spr", "Sprint"), t("lg_hr", "Heart rate"))))
    target = '<div class="raise"><b>%s</b><ul><li>%s</li><li>%s</li><li>%s</li></ul></div>' % (
        t("cd_raise", "Raise · next time aim for 695 W"), t("cd_r1", "First rep 433 W, last rep 722 W: the last third rose 16% over the first."), t("cd_r2", "Decrement score 12.3%: every rep stayed close to the best one."), t("cd_r3", "You finished stronger than you started, so open at the level of your last reps."))
    feats = [
        (t("cd_f1e", "Wattbike"), t("cd_f1h", "Every ride in, without typing a number"),
         t("cd_f1p", "Athletes export their Wattbike Hub session (TCX) and ForeCheck reads it: power, cadence, heart rate and the structure of the workout, block by block."),
         panel(t("cd_import", "Rides this week"), rides_list())),
        (t("cd_f2e", "Rep by rep"), t("cd_f2h", "See fatigue inside the set"),
         t("cd_f2p", "Sprints and intervals are split into reps automatically. First versus last rep, decrement score and power per heartbeat show whether the athlete held the quality."),
         panel(t("cd_reps", "30 × 10 s · 3 sets of 10"), C.rep_bars() + kpis([(t("k_first", "First → last rep"), "433 → 722 W", 0), (t("k_dec", "Decrement"), "12.3%", 0), (t("k_ftpp", "Mean % FTP"), "292%", 1)]))),
        (t("cd_f3e", "Next time"), t("cd_f3h", "A target for the next session, not just a report"),
         t("cd_f3p", "Each block ends with a plain recommendation: raise, hold or lower, with the watts to aim for. The same session name is compared over the weeks."),
         panel(t("cd_tgt", "Recommendation"), target)),
    ]
    qs = [t("cd_q1", "Did the athlete hold power to the last rep?"), t("cd_q2", "What should the next session's target be?"), t("cd_q3", "Is aerobic fitness improving between blocks?"), t("cd_q4", "Who skipped their off-ice work this week?")]
    return ("conditioning", tt("cd_title", "Conditioning"),
            hero("conditioning", t("cd_eyebrow", "Conditioning · Wattbike"), t("cd_h1", 'Off-ice work, <span class="r">analysed for you.</span>'),
                 t("cd_lead", "Bike sessions turned into efforts, fatigue and a clear target for next time. Your athletes ride, ForeCheck does the maths."), shot)
            + rows(feats) + answers(qs))


def rides_list():
    rows_ = [("#27 F", "3×6 s · 3×10×10 s", "56 min", "ok"), ("#5 D", "15-10-5-5 min", "55 min", "ok"), ("#14 F", "4×4 min VO2", "42 min", "ok"), ("#44 D", "—", "", "miss")]
    li = "".join('<li class="%s"><b>%s</b><span>%s</span><span class="v">%s</span></li>' % (c, n, w if c == "ok" else '<span data-i18n="cd_missing">%s</span>' % tt("cd_missing", "No ride yet"), d) for n, w, d, c in rows_)
    return '<ul class="rides">%s</ul>' % li


def month_grid():
    # October 2026 starts on a Thursday
    days = ["M", "T", "W", "T", "F", "S", "S"]
    keys = ["d_mo", "d_tu", "d_we", "d_th", "d_fr", "d_sa", "d_su"]
    ev = {2: ("home", ""), 4: ("away", ""), 9: ("home", ""), 11: ("away", "t"), 13: ("away", "t"), 16: ("home", ""), 18: ("away", ""), 23: ("home", ""), 25: ("away", "t"), 30: ("home", "")}
    head = "".join('<div class="dh" data-i18n="%s">%s</div>' % (k, tt(k, d)) for k, d in zip(keys, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
    cells = '<div class="dc mute"></div>' * 3
    for d in range(1, 32):
        e = ev.get(d)
        inner = '<span class="dn">%d</span>' % d
        if e:
            inner += '<i class="g %s"></i>' % e[0]
            if e[1]:
                inner += '<i class="bolt" title="travel"></i>'
        elif (d + 3) % 7 not in (6,):
            inner += '<i class="pr"></i>'
        cells += '<div class="dc">%s</div>' % inner
    legend = '<div class="legend"><i class="lg home"></i>%s<i class="lg away"></i>%s<i class="lg pr"></i>%s<i class="lg bolt"></i>%s</div>' % (t("lg_home", "Home game"), t("lg_away", "Away game"), t("lg_prac", "Practice"), t("lg_travel", "High travel strain"))
    return '<div class="month"><p class="mname" data-i18n="oct">%s 2026</p><div class="mgrid">%s%s</div>%s</div>' % (tt("oct", "October"), head, cells, legend)


def phone_calendar():
    items = [("17:30", t("pc1", "Ice practice"), ""), ("19:45", t("pc2", "Recovery bike · 20 min"), ""), ("Sat 19:45", t("pc3", "Away game · bus 15:00"), "away")]
    li = "".join('<li class="%s"><time>%s</time>%s</li>' % (c, a, b) for a, b, c in items)
    return '<div class="phone"><div class="notch"></div><p class="pt">%s</p><ul class="pcal">%s</ul><p class="sub-ok">%s</p></div>' % (t("pc_t", "Today"), li, t("pc_sub", "Subscribed · updates by itself"))


def page_calendar():
    shot = screen("Calendar", t("cl_screen_t", "Calendar"), t("cl_screen_s", "Team, groups and every player · games, practices, travel"),
                  '<div class="two">%s%s</div>' % (panel(t("cl_p1", "Team calendar"), month_grid()), panel(t("cl_p2", "Season load plan · planned vs done"), C.season_plan() + '<div class="legend"><i class="lg plan"></i>%s<i class="lg done"></i>%s<i class="lg gm"></i>%s</div>' % (t("lg_plan", "Planned"), t("lg_done", "Done"), t("lg_games", "Games")))))
    feats = [
        (t("cl_f1e", "On every phone"), t("cl_f1h", "One link per player, always up to date"),
         t("cl_f1p", "Each player and staff member gets a private calendar link for their phone. Games, practices, gym and rehab sessions appear on their own, and changes show up without a message in the group chat."),
         phone_calendar()),
        (t("cl_f2e", "Travel strain"), t("cl_f2h", "Heavy road weeks, flagged in advance"),
         t("cl_f2p", "The full league schedule is imported and kept current. Weeks with long bus trips and late arrivals are marked, so recovery is planned before the trip, not after."),
         panel(t("cl_trip", "Week 42 · travel"), trip_card())),
        (t("cl_f3e", "Season plan"), t("cl_f3h", "Plan the hard weeks and the easy ones"),
         t("cl_f3p", "Weekly load targets for the whole season sit next to the game schedule. As the weeks are played, the real load fills in, so you see straight away when the plan and reality drift apart."),
         panel(t("cl_groups", "Groups"), groups_card())),
    ]
    qs = [t("cl_q1", "Where does everyone need to be this week?"), t("cl_q2", "Which road trips need an extra recovery day?"), t("cl_q3", "Are we on track with the season plan?"), t("cl_q4", "Did every player get the schedule change?")]
    return ("calendar", tt("cl_title", "Calendar & planning"),
            hero("calendar", t("cl_eyebrow", "Calendar · Season plan"), t("cl_h1", 'Everyone in the <span class="r">right place.</span>'),
                 t("cl_lead", "Team, group and individual calendars on every phone, the full game schedule, travel strain and the season load plan in one place."), shot)
            + rows(feats) + answers(qs))


def trip_card():
    rows_ = [(t("tr1", "Thu"), t("tr1b", "Bus 780 km · arrive 02:10"), "hi"), (t("tr2", "Fri"), t("tr2b", "Away game"), ""), (t("tr3", "Sat"), t("tr3b", "Away game · home 03:40"), "hi"), (t("tr4", "Sun"), t("tr4b", "Recovery day planned"), "ok")]
    return '<ul class="trip">%s</ul>' % "".join('<li class="%s"><b>%s</b>%s</li>' % (c, a, b) for a, b, c in rows_)


def groups_card():
    gs = [(t("gp1", "Forwards"), "12"), (t("gp2", "Defence"), "8"), (t("gp3", "Goalies"), "3"), (t("gp4", "Rehab group"), "2"), (t("gp5", "Junior call-ups"), "4")]
    return '<ul class="chips">%s</ul>' % "".join('<li>%s<span>%s</span></li>' % g for g in gs)


def page_strength():
    rows_ = [("A1", "Back squat", "4 × 5", "80%"), ("A2", "Copenhagen plank", "3 × 20 s", "—"), ("B1", "Trap-bar jump", "4 × 3", "30%"), ("B2", "Single-leg RDL", "3 × 8", "RPE 7")]
    trs = "".join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td>%s</tr>' % (a, b, c, d, "".join('<td>%s</td>' % kg for kg in kgs(d, i))) for i, (a, b, c, d) in enumerate(rows_))
    table = '<div class="tblwrap"><table class="tbl"><tr><th></th><th data-i18n="th_ex">%s</th><th data-i18n="th_sets">%s</th><th data-i18n="th_load">%s</th><th>#5 D</th><th>#14 F</th><th>#27 F</th></tr>%s</table></div>' % (tt("th_ex", "Exercise"), tt("th_sets", "Sets × reps"), tt("th_load", "Load"), trs)
    shot = screen("Strength Room", t("st_screen_t", "Strength Room"), t("st_screen_s", "Week 42 · in-season · forwards"),
                  '<div class="two">%s%s</div>' % (panel(t("st_p1", "Workout · kilos per player from their latest maxes"), table), panel(t("st_p2", "Testing Lab · #27 F vs team"), test_profile())))
    feats = [
        (t("st_f1e", "Strength Room"), t("st_f1h", "Write the week once, every player gets their kilos"),
         t("st_f1p", "Build a session for the team, a position group or one player, with blocks and supersets. Percentages and RPE turn into kilos from each player's latest maxes."),
         panel(t("st_lib", "Exercise library"), '<ul class="chips">%s</ul>' % "".join("<li>%s</li>" % e for e in ["Back squat", "Bench press", "Trap-bar deadlift", "Hip thrust", "Nordic curl", "Copenhagen plank", "Pull-up", "Landmine press"]))),
        (t("st_f2e", "Testing Lab"), t("st_f2h", "Fitness tests that mean something"),
         t("st_f2p", "Jumps, sprints, strength and hip tests in one profile per player, scored against the team, against clear thresholds and against the player's own history."),
         panel(t("st_hip", "Hip strength · N/kg"), hip_card())),
        (t("st_f3e", "Linked"), t("st_f3h", "Tests feed the program"),
         t("st_f3p", "A new test result updates the maxes behind every workout, so the program follows the athlete instead of last summer's numbers."),
         panel(t("st_trend", "Countermovement jump · #27 F"), trend_card())),
    ]
    qs = [t("st_q1", "What does each player lift this week?"), t("st_q2", "Who is improving and who is slipping?"), t("st_q3", "Is the groin-to-hip balance where it should be?"), t("st_q4", "Which maxes are out of date?")]
    return ("strength", tt("st_title", "Strength & testing"),
            hero("strength", t("st_eyebrow", "Strength Room · Testing Lab"), t("st_h1", 'Programs that <span class="r">follow the athlete.</span>'),
                 t("st_lead", "A workout builder that turns percentages into kilos for every player, and a testing lab that shows who is improving and who is slipping."), shot)
            + rows(feats) + answers(qs))


def kgs(load, i):
    maxes = [(150, 132, 141), None, (150, 132, 141), None]
    if load.endswith("%") and maxes[i]:
        p = int(load[:-1]) / 100
        return ["%.1f kg" % (round(m * p / 2.5) * 2.5) for m in maxes[i]]
    return ["—", "—", "—"] if load == "—" else ["RPE 7"] * 3


def test_profile():
    tests = [("CMJ", 48.2, 46.0, "cm", "up"), ("10 m", 1.71, 1.74, "s", "down"), ("30 m", 4.12, 4.10, "s", "down"), ("Hip ADD", 6.4, 6.1, "N/kg", "up"), ("Hip ABD", 5.9, 5.6, "N/kg", "up"), ("ADD:ABD", 1.08, 1.09, "", "mid")]
    out = ""
    for name, v, team, unit, good in tests:
        better = (v > team) if good == "up" else (v < team) if good == "down" else True
        pct = 50 + (v - team) / team * 400 * (1 if good != "down" else -1)
        pct = max(8, min(96, pct))
        out += '<div class="tp"><span class="tn">%s</span><span class="tbar"><i class="team"></i><i class="me %s" style="left:%.0f%%"></i></span><span class="tv">%s %s</span></div>' % (name, "good" if better else "bad", pct, v, unit)
    return '<div class="tprof">%s<div class="legend"><i class="lg tmid"></i>%s<i class="lg me"></i>#27 F</div></div>' % (out, t("lg_team", "Team average"))


def hip_card():
    rows_ = [("#5 D", 6.9, 6.0, "1.15", "ok"), ("#14 F", 5.4, 5.2, "1.04", "warn"), ("#27 F", 6.4, 5.9, "1.08", "ok"), ("#44 D", 7.2, 5.8, "1.24", "warn")]
    head = '<tr><th></th><th>ADD</th><th>ABD</th><th>ADD:ABD</th></tr>'
    body = "".join('<tr><td><b>%s</b></td><td>%.1f</td><td>%.1f</td><td class="%s">%s</td></tr>' % r for r in rows_)
    return '<div class="tblwrap"><table class="tbl">%s%s</table></div>' % (head, body)


def trend_card():
    vals = [44.1, 45.0, 44.6, 46.2, 47.1, 48.2]
    w, h = 360, 120
    pts = [(20 + i * (w - 40) / 5, h - 20 - (v - 42) / 8 * (h - 40)) for i, v in enumerate(vals)]
    svg = '<svg viewBox="0 0 %d %d" class="chart">%s%s</svg>' % (w, h, C.polyline(pts, "trend"), "".join('<circle class="tdot" cx="%.1f" cy="%.1f" r="4"/><text class="ax" x="%.1f" y="%.1f" text-anchor="middle">%.1f</text>' % (x, y, x, y - 9, v) for (x, y), v in zip(pts, vals)))
    return svg


def page_rehab():
    stages = [("rh_s1", "Protect"), ("rh_s2", "Mobility"), ("rh_s3", "Strength"), ("rh_s4", "On-ice, no contact"), ("rh_s5", "Full contact")]
    st = "".join('<li class="%s"><i>%d</i><span data-i18n="%s">%s</span></li>' % ("done" if i < 3 else "now" if i == 3 else "", i + 1, k, tt(k, s)) for i, (k, s) in enumerate(stages))
    crit = [(t("rc1", "Single-leg hop · 94% of other side"), "ok"), (t("rc2", "Hip ADD:ABD · 1.06"), "ok"), (t("rc3", "Skating load · 82% of pre-injury"), "now"), (t("rc4", "Contact drills · physio sign-off Thu"), "")]
    cr = "".join('<li class="%s">%s</li>' % (c, x) for x, c in crit)
    shot = screen("Rehab Clinic", t("rh_screen_t", "Rehab Clinic"), t("rh_screen_s", "#5 D · lower-body injury · day 23"),
                  '<div class="two">%s%s</div>' % (panel(t("rh_p1", "Return-to-play stage"), '<ol class="stages">%s</ol>' % st + panel(t("rh_crit", "Criteria for the next stage"), '<ul class="crit">%s</ul>' % cr, "inner")),
                                                    panel(t("rh_p2", "Ice load during rehab vs pre-injury baseline"), rehab_chart())))
    feats = [
        (t("rh_f1e", "One view"), t("rh_f1h", "Physio, strength coach and head coach read the same page"),
         t("rh_f1p", "Stage, sessions and progress for every rehabbing player, in words the whole staff understands. Medical details stay with the people who need them."),
         panel(t("rh_list", "In rehab"), '<ul class="flags"><li class="lo"><b>#5 D</b><span class="v">4/5</span>%s</li><li class="hi"><b>#19 F</b><span class="v">2/5</span>%s</li></ul>' % (t("rh_l1", "On-ice, no contact · sign-off Thu"), t("rh_l2", "Mobility · gym only")))),
        (t("rh_f2e", "Back on the ice"), t("rh_f2h", "Load rebuilt against the player's own baseline"),
         t("rh_f2p", "Catapult data from rehab skates is compared with the player's own pre-injury load, so return-to-play is based on numbers, not on a feeling."),
         panel(t("rh_sess", "Rehab sessions this week"), '<ul class="trip"><li class="ok"><b>%s</b>%s</li><li class="ok"><b>%s</b>%s</li><li><b>%s</b>%s</li></ul>' % (t("tr_mo", "Mon"), t("rh_w1", "Gym · lower-body strength"), t("tr_tu", "Tue"), t("rh_w2", "Ice · 35 min, no contact"), t("tr_th", "Thu"), t("rh_w3", "Ice · physio test for contact")))),
        (t("rh_f3e", "In the calendar"), t("rh_f3h", "Rehab sessions where the player sees them"),
         t("rh_f3p", "Rehab sessions go into the player's own calendar, alongside the team schedule, without exposing health details to the rest of the group."),
         phone_calendar()),
    ]
    qs = [t("rh_q1", "When will the player be ready, and for what?"), t("rh_q2", "Is the rehab load close to the player's normal level?"), t("rh_q3", "Who signs off the next stage?"), t("rh_q4", "Does everyone on the staff have the same information?")]
    return ("rehab", tt("rh_title", "Rehab"),
            hero("rehab", t("rh_eyebrow", "Rehab Clinic"), t("rh_h1", 'Back on the ice <span class="r">on facts.</span>'),
                 t("rh_lead", "Every rehabbing player's stage, sessions and load in one view, so the physio, the strength coach and the head coach make the same call."), shot)
            + rows(feats) + answers(qs))


def rehab_chart():
    vals = [0, 0, 18, 32, 41, 55, 63, 71, 82]
    w, h = 360, 190
    padl, padb = 30, 22
    bw = (w - padl - 10) / len(vals)
    y = lambda v: 10 + (h - 10 - padb) * (1 - v / 120)
    out = '<svg viewBox="0 0 %d %d" class="chart">' % (w, h)
    out += '<line class="base" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">100%%</text>' % (padl, w - 10, y(100), y(100), w - 12, y(100) - 5)
    for i, v in enumerate(vals):
        if v:
            out += '<rect class="rb" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>' % (padl + i * bw + bw * .18, y(v), bw * .64, y(0) - y(v))
        out += '<text class="ax" x="%.1f" y="%d" text-anchor="middle">W%d</text>' % (padl + i * bw + bw / 2, h - 6, i + 1)
    return out + "</svg>"


def page_players():
    qs_ = [("pl_w1", "Sleep", 4), ("pl_w2", "Energy", 3), ("pl_w3", "Soreness", 2), ("pl_w4", "Stress", 4), ("pl_w5", "Mood", 4)]
    q = "".join('<li><span data-i18n="%s">%s</span><span class="dots">%s</span></li>' % (k, tt(k, s), "".join('<i class="%s"></i>' % ("on" if j < v else "") for j in range(5))) for k, s, v in qs_)
    phone = '<div class="phone"><div class="notch"></div><p class="pt">%s</p><ul class="well">%s</ul><p class="sub-ok">%s</p></div>' % (t("pl_how", "How do you feel today?"), q, t("pl_sent", "Sent · thank you"))
    team = panel(t("pl_team", "Team check-in · this morning"), kpis([(t("k_ans", "Answered"), "22 / 25", 0), (t("k_sleep", "Sleep"), "3.9", 0), (t("k_sore", "Soreness"), "2.4", 0), (t("k_flag", "Flagged"), "2", 1)]) + '<ul class="flags"><li class="hi"><b>#11 F</b><span class="v">↓</span>%s</li><li class="lo"><b>#33 G</b><span class="v">↓</span>%s</li></ul>' % (t("pl_f1", "Sleep 2/5 for three nights"), t("pl_f2", "Soreness high after travel")))
    shot = screen("Locker Room", t("pl_screen_t", "Players"), t("pl_screen_s", "Morning check-in, calendar and session RPE from the players' phones"), '<div class="two narrow">%s%s</div>' % (phone, team))
    feats = [
        (t("pl_f1e", "Wellness"), t("pl_f1h", "Twenty seconds in the morning"),
         t("pl_f1p", "Five quick questions on the phone: sleep, energy, soreness, stress and mood. Players see their own answers. Staff see who needs a conversation, not a spreadsheet."),
         phone),
        (t("pl_f2e", "Session RPE"), t("pl_f2h", "How hard it felt, next to how hard it was"),
         t("pl_f2p", "After each session players rate the effort. ForeCheck sets it next to the Catapult and heart-rate load, so mismatches stand out."),
         panel(t("pl_rpe", "Felt vs measured · last practice"), rpe_card())),
        (t("pl_f3e", "Calendar"), t("pl_f3h", "Their week, on their phone"),
         t("pl_f3p", "The same private calendar link carries team practices, games, gym and individual sessions. No app to install, no login to remember."),
         phone_calendar()),
    ]
    qs = [t("pl_q1", "Who slept badly before today's game?"), t("pl_q2", "Did the practice feel harder than it measured?"), t("pl_q3", "Who hasn't checked in this week?"), t("pl_q4", "Does every player know tomorrow's schedule?")]
    return ("players", tt("pl_title", "For players"),
            hero("players", t("pl_eyebrow", "Players · Phone"), t("pl_h1", 'Twenty seconds <span class="r">a day.</span>'),
                 t("pl_lead", "A morning check-in, session effort and a personal calendar on every player's phone. Quick for them, useful for you."), shot)
            + rows(feats) + answers(qs))


def rpe_card():
    rows_ = [("#7 D", 6, 7, ""), ("#11 F", 9, 6, "hi"), ("#21 F", 5, 5, ""), ("#27 F", 7, 7, "")]
    head = '<tr><th></th><th data-i18n="th_felt">%s</th><th data-i18n="th_meas">%s</th></tr>' % (tt("th_felt", "Felt (RPE)"), tt("th_meas", "Measured (0-10)"))
    body = "".join('<tr><td><b>%s</b></td><td class="%s">%d</td><td>%d</td></tr>' % (a, c, b, d) for a, b, d, c in rows_)
    return '<div class="tblwrap"><table class="tbl">%s%s</table></div>' % (head, body)


# ---------------------------------------------------------------- write

def write(builder):
    global _dict
    _dict = {}
    pid, title, body = builder()
    head = header(pid)
    foot = footer(pid)
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="ForeCheck · %s. Hockey performance data turned into the few things that change today's plan.">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<title>%s · ForeCheck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/pages.css">
</head>
<body class="page-%s">
%s
<main>
%s
</main>
%s
<script>window.FC_I18N=%s;</script>
<script src="assets/i18n.js"></script>
<script src="assets/bg.js"></script>
</body>
</html>
""" % (title, title, pid, head, body, foot, json.dumps(_dict, ensure_ascii=False))
    open(os.path.join(ROOT, pid + ".html"), "w", encoding="utf-8").write(html)
    return pid, len(_dict)


if __name__ == "__main__":
    allen = {}
    for b in (page_load, page_conditioning, page_calendar, page_strength, page_rehab, page_players):
        print(*write(b))
        allen.update({k: v["en"] for k, v in _dict.items()})
    missing = {k: v for k, v in allen.items() if not all(l in TR.get(k, {}) for l in ("de", "fr", "it"))}
    json.dump(missing, open(os.path.join(ROOT, "build", "untranslated.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("untranslated:", len(missing))
