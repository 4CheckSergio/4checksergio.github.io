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
import seo
import langs

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
    ("security", "security.html", "Security"),
    ("science", "science.html", "Science"),
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


ABOUT = "ForeCheck (fore-check.ch) is science-backed sports performance and athlete monitoring software for coaches and medical staff in team and individual sports: training load and ACWR, heart rate, Wattbike conditioning, strength programming, fitness testing, return to play, wellness check-ins and team calendars. Built first for ice hockey, in Switzerland."


def footer(active):
    nxt = PAGES[(next(i for i, p in enumerate(PAGES) if p[0] == active) + 1) % len(PAGES)]
    return """<section class="next">
  <div class="wrap next-row">
    <div><p class="eyebrow">%s</p><a class="next-link" href="%s" data-i18n="nav_%s">%s</a></div>
    <div class="contact"><span class="eyebrow">%s</span><a href="mailto:info@fore-check.ch">info@fore-check.ch</a></div>
  </div>
</section>
<footer><div class="wrap"><span>© 2026 ForeCheck · info@fore-check.ch</span>%s</div><div class="wrap"><span class="about">%s</span></div></footer>""" % (
        t("next", "Next"), nxt[1], nxt[0], tt("nav_" + nxt[0], nxt[2]), t("email_eyebrow", "Email us"), t("footer_demo", "All player examples on this site use invented demo data."), t("footer_about", ABOUT))


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


def answers(qs, eyebrow=None, h2=None):
    return '<section class="sheet answers"><div class="wrap"><div class="sec-head"><p class="eyebrow">%s</p><h2>%s</h2></div><ul class="qa">%s</ul></div></section>' % (
        eyebrow or t("qa_eyebrow", "Questions it answers"), h2 or t("qa_h2", "What you decide with it"), "".join("<li>%s</li>" % q for q in qs))


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
    qs_ = [("pl_w1", "Sleep", .8), ("pl_w2", "Energy", .56), ("pl_w3", "Soreness", .34), ("pl_w4", "Stress", .72), ("pl_w5", "Mood", .76)]
    ends = '<li class="gends"><span>%s</span><span>%s</span></li>' % (t("pl_vbad", "Very badly"), t("pl_vwell", "Very well"))
    q = ends + "".join('<li class="g"><span data-i18n="%s">%s</span><span class="gscale"><i style="left:%d%%"></i></span></li>' % (k, tt(k, s), round(v * 100)) for k, s, v in qs_)
    phone = '<div class="phone"><div class="notch"></div><p class="pt">%s</p><ul class="well">%s</ul><p class="sub-ok">%s</p></div>' % (t("pl_how", "How do you feel today?"), q, t("pl_sent", "Sent · thank you"))
    team = panel(t("pl_team", "Team check-in · this morning"), kpis([(t("k_ans", "Answered"), "22 / 25", 0), (t("k_below", "Below own normal"), "3", 0), (t("k_flag", "Flagged"), "2", 1)]) + '<ul class="flags"><li class="hi"><b>#11 F</b><span class="v">↓</span>%s</li><li class="lo"><b>#33 G</b><span class="v">↓</span>%s</li></ul>' % (t("pl_f1b", "Sleep low for three nights"), t("pl_f2", "Soreness high after travel")))
    shot = screen("Locker Room", t("pl_screen_t", "Players"), t("pl_screen_s", "Morning check-in, calendar and session RPE from the players' phones"), '<div class="two narrow">%s%s</div>' % (phone, team))
    feats = [
        (t("pl_f1e", "Wellness"), t("pl_f1h", "Twenty seconds in the morning"),
         t("pl_f1p2", "Five quick questions on the phone: sleep, energy, soreness, stress and mood. Each answer is a slide on a grey scale from very badly to very well, with no numbers and no colours, so players answer how they feel, not what score they think the staff want. Staff see who is below their own normal and needs a conversation, not a spreadsheet."),
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


def page_security():
    path = '<ol class="dpath">%s</ol>' % "".join('<li class="%s"><b>%s</b><span>%s</span></li>' % (c, h, d) for c, h, d in [
        ("", t("sx_p1h", "Your staff"), t("sx_p1d", "Laptop, iPad, phone")),
        ("lock", t("sx_p2h", "HTTPS only"), t("sx_p2d", "Encrypted on the way")),
        ("ch", t("sx_p3h", "ForeCheck server"), t("sx_p3d", "Switzerland · Infomaniak")),
        ("ch", t("sx_p4h", "Nightly backup"), t("sx_p4d", "Encrypted · Swiss Backup"))])
    shot = '<figure class="screen secshot"><div class="app">%s%s</div></figure>' % (
        kpis([(t("sk_where", "Data stored in"), t("sk_where_v", "Switzerland"), 1), (t("sk_conn", "Connection"), "HTTPS", 0),
              (t("sk_backup", "Backups"), t("sk_backup_v", "Nightly, encrypted"), 0), (t("sk_ret", "Kept"), t("sk_ret_v", "14 d · 8 w · 12 m"), 0)]),
        panel(t("sx_path", "Where your data goes"), path))
    feats = [
        (t("sx_f1e", "Swiss hosting"), t("sx_f1h", "Your athletes' data stays in Switzerland"),
         t("sx_f1p", "ForeCheck runs on a server in Switzerland, with Infomaniak, a Swiss provider. Player data is stored and processed there, under Swiss law and the Swiss Federal Act on Data Protection (nFADP)."),
         panel(t("sx_loc", "Where it lives"), '<ul class="flags sec"><li class="lo"><b>%s</b><span class="v">CH</span>%s</li><li class="lo"><b>%s</b><span class="v">CH</span>%s</li></ul>' % (
             t("sx_app", "App"), t("sx_app_d", "Infomaniak server in Switzerland"), t("sx_bk", "Backup"), t("sx_bk_d", "Swiss Backup, Switzerland"))) ),
        (t("sx_f2e", "Backups"), t("sx_f2h", "Encrypted every night, kept for a year"),
         t("sx_f2p", "Every night the data is encrypted and copied to a separate backup in Switzerland. We keep 14 daily, 8 weekly and 12 monthly copies, so a mistake or a lost device never costs you a season."),
         panel(t("sx_ret", "Backup copies kept"), kpis([(t("sx_daily", "Daily"), "14", 0), (t("sx_weekly", "Weekly"), "8", 0), (t("sx_monthly", "Monthly"), "12", 1)]))),
        (t("sx_f3e", "Who sees what"), t("sx_f3h", "Health data only for the people who need it"),
         t("sx_f3p", "Every staff member gets a role. The head coach always sees each player's return-to-play stage, and the medical detail behind it can be limited to the physio and doctor whenever the club needs that. Health data such as rehab, heart rate and tests is a separate switch that the club turns on only when it is ready."),
         panel(t("sx_roles", "Roles"), '<ul class="trip"><li class="ok"><b>%s</b>%s</li><li class="ok"><b>%s</b>%s</li><li><b>%s</b>%s</li></ul>' % (
             t("sx_r1", "Head coach"), t("sx_r1d", "Availability, return-to-play stage, daily brief"), t("sx_r2", "Physio"), t("sx_r2d", "Rehab stages and medical notes"), t("sx_r3", "Player"), t("sx_r3d", "Own check-in and own calendar")))),
        (t("sx_f4e", "Your data"), t("sx_f4h", "Yours to keep, yours to take with you"),
         t("sx_f4p", "The club owns its data. It is never sold and never used for anyone else's purposes, including training AI. Ask and you get a full export in open formats, so you are never locked in."),
         panel(t("sx_exp", "Export"), '<ul class="chips"><li>CSV</li><li>JSON</li><li>%s</li></ul>' % t("sx_exp_all", "Everything, any time"))),
    ]
    qa = lambda q, a: q + '<span class="ans">%s</span>' % a
    qs = [qa(t("sx_q1", "In which country is our data stored?"), t("sx_a1", "In Switzerland, on Infomaniak servers, and the backups too.")),
          qa(t("sx_q2", "Who on the staff can see medical details?"), t("sx_a2", "You decide. Medical detail can be limited to the physio and team doctor, while the head coach still sees the return-to-play stage.")),
          qa(t("sx_q3", "What happens if a laptop is lost?"), t("sx_a3", "Nothing is lost. The data lives on the server, not on the laptop, and is backed up every night.")),
          qa(t("sx_q4", "Can we take our data with us if we leave?"), t("sx_a4", "Yes. You get a full export in open formats, CSV and JSON."))]
    return ("security", tt("sx_title", "Security"),
            hero("security", t("sx_eyebrow", "Security · Swiss hosting"), t("sx_h1", 'Swiss data. <span class="r">Swiss servers.</span>'),
                 t("sx_lead", "Player data is health data. ForeCheck keeps it in Switzerland, encrypted on the way and in the backups, and only in front of the people who need it."), shot)
            + rows(feats) + answers(qs, t("sx_qa_e", "Questions clubs ask"), t("sx_qa_h", "Answered before you ask")))


# ---------------------------------------------------------------- science

# Every method on science.html. Source text: the manual page "The science behind ForeCheck".
# To add a method, append a dict to METHODS (status "live", "dev" or "part") and its papers to REFS.
# Reference strings stay in English; every DOI was checked against PubMed before it went in.
# Papers without a resolving DOI get (text, None, url) and link to their repository record instead; books get (text, None).
REFS = {
    "nightingale2024": ("Nightingale S, Hughes J, De Ste Croix M, Pfeifer C. Practice and match load characteristics of elite men's ice hockey. Int J Strength Cond. 2024;4(1).", None, "https://eprints.glos.ac.uk/14636/"),
    "nightingale2026": ("Nightingale S, Hughes J, De Ste Croix M, Pfeifer C. A framework guide for the selection of external load metrics in ice hockey. Int J Strength Cond. 2026;6(1):1-9.", None, "https://eprints.glos.ac.uk/15875/"),
    "allard2022": ("Allard P, Martinez R, Deguire S, Tremblay J. In-season session training load relative to match load in professional ice hockey. J Strength Cond Res. 2022;36(2):486-492.", "10.1519/JSC.0000000000003490"),
    "bredt2020": ("Bredt SDGT, Chagas MH, Peixoto GH, Menzel HJ, de Andrade AGP. Understanding player load: meanings and limitations. J Hum Kinet. 2020;71:5-9.", "10.2478/hukin-2019-0072"),
    "williams2017": ("Williams S, West S, Cross MJ, Stokes KA. Better way to determine the acute:chronic workload ratio? Br J Sports Med. 2017;51(3):209-210.", "10.1136/bjsports-2016-096589"),
    "murray2017": ("Murray NB, Gabbett TJ, Townshend AD, Blanch P. Calculating acute:chronic workload ratios using exponentially weighted moving averages provides a more sensitive indicator of injury likelihood than rolling averages. Br J Sports Med. 2017;51(9):749-754.", "10.1136/bjsports-2016-097152"),
    "sampson2017": ("Sampson JA, Fullagar HHK, Murray A. Evidence is needed to determine if there is a better way to determine the acute:chronic workload. Br J Sports Med. 2017;51(7):621-622.", "10.1136/bjsports-2016-097085"),
    "impellizzeri2020": ("Impellizzeri FM, Tenan MS, Kempton T, Novak A, Coutts AJ. Acute:chronic workload ratio: conceptual issues and fundamental pitfalls. Int J Sports Physiol Perform. 2020;15(6):907-913.", "10.1123/ijspp.2019-0864"),
    "mclaren2018": ("McLaren SJ, Macpherson TW, Coutts AJ, et al. The relationships between internal and external measures of training load and intensity in team sports: a meta-analysis. Sports Med. 2018;48(3):641-658.", "10.1007/s40279-017-0830-z"),
    "jones2017": ("Jones AM, Vanhatalo A. The 'critical power' concept: applications to sports performance with a focus on intermittent high-intensity exercise. Sports Med. 2017;47(Suppl 1):65-78.", "10.1007/s40279-017-0688-0"),
    "skiba2012": ("Skiba PF, Chidnok W, Vanhatalo A, Jones AM. Modeling the expenditure and reconstitution of work capacity above critical power. Med Sci Sports Exerc. 2012;44(8):1526-1532.", "10.1249/MSS.0b013e3182517a80"),
    "skiba2021": ("Skiba PF, Clarke DC. The W' balance model: mathematical and methodological considerations. Int J Sports Physiol Perform. 2021;16(11):1561-1572.", "10.1123/ijspp.2021-0205"),
    "bartram2018": ("Bartram JC, Thewlis D, Martin DT, Norton KI. Accuracy of W' recovery kinetics in high performance cyclists: modeling intermittent work capacity. Int J Sports Physiol Perform. 2018;13(6):724-728.", "10.1123/ijspp.2017-0034"),
    "welburn2025": ("Welburn AJ, Pugh CF, Bailey SJ, Ferguson RA. W' reconstitution modelling during intermittent exercise performed to task failure. Eur J Appl Physiol. 2025.", "10.1007/s00421-025-05912-0"),
    "montgomery1988": ("Montgomery DL. Physiology of ice hockey. Sports Med. 1988;5(2):99-126.", "10.2165/00007256-198805020-00003"),
    "vighlarsen2020": ("Vigh-Larsen JF, Ermidis G, Rago V, et al. Muscle metabolism and fatigue during simulated ice hockey match-play in elite players. Med Sci Sports Exerc. 2020;52(10):2162-2171.", "10.1249/MSS.0000000000002370"),
    "vighlarsen2022": ("Vigh-Larsen JF, Mohr M. The physiology of ice hockey performance: an update. Scand J Med Sci Sports. 2024;34(1):e14284.", "10.1111/sms.14284"),
    "green1976": ("Green H, Bishop P, Houston M, et al. Time-motion and physiological assessments of ice hockey performance. J Appl Physiol. 1976;40(2):159-163.", "10.1152/jappl.1976.40.2.159"),
    "brocherie2018": ("Brocherie F, Girard O, Millet GP. Updated analysis of changes in locomotor activities across periods in an international ice hockey game. Biol Sport. 2018;35(3):261-267.", "10.5114/biolsport.2018.77826"),
    "weston2011": ("Weston M, Drust B, Gregson W. Intensities of exercise during match-play in FA Premier League referees and players. J Sports Sci. 2011;29(5):527-532.", "10.1080/02640414.2010.543914"),
    "collins2025": ("Collins JJ, Navarro JF, McRobert AP, et al. The physical demands of Major League Soccer match-play with specific reference to high-intensity activity by position, venue and opposition quality. PLoS One. 2025;20(10):e0334460.", "10.1371/journal.pone.0334460"),
    "gualtieri2023": ("Gualtieri A, Rampinini E, Dello Iacono A, Beato M. High-speed running and sprinting in professional adult soccer: current thresholds definition, match demands and training strategies. A systematic review. Front Sports Act Living. 2023;5:1116293.", "10.3389/fspor.2023.1116293"),
    "edwards1993": ("Edwards S. The Heart Rate Monitor Book. Polar Electro; 1993.", None),
    "spiering2003": ("Spiering BA, Wilson MH, Judelson DA, Rundell KW. Evaluation of cardiovascular demands of game play and practice in women's ice hockey. J Strength Cond Res. 2003;17(2):329-333.", "10.1519/1533-4287(2003)017<0329:eocdog>2.0.co;2"),
}

METHODS = [
    dict(id="volume", status="live", cat=("sc_m1c", "Session load"),
         h=("sc_m1h2", "Volume and density"),
         q=("sc_m1q2", "How much did the player do in this session, and how much skating was packed into each minute on the ice?"),
         how=[("sc_m1s1", "Measured by the player's sensor vest: on-ice load (accelerometer load), explosive efforts, high-intensity load, active time on ice, skating strides and skating load."),
              ("sc_v2s2", "Daily volume = Skating Load: the peak force of each skating stride multiplied by the player's body mass, summed over the day."),
              ("sc_v2s3c", "Density (SL/min) = Skating Load ÷ active minutes on ice: how much skating work is packed into each minute the player is actually skating. Active minutes, not the whole session, so players with little ice time are not made to look easier. Until 14 October 2026 ForeCheck used explosive efforts ÷ active minutes here."),
              ("sc_v2s4c", "Skating Load drives the daily load, the ACWR and the 7-day plan forecasts built on them. It is also the volume on the session tiles and charts, so every screen uses the same measure. The session volume and intensity scores below use their own three-metric models."),
              ("sc_m1s4", "Totals over periods or days are summed first and divided once. ForeCheck never averages ratios.")],
         why=[("sc_v2w1", "Skating Load counts only skating strides, and weighs each one by the player's body mass. A heavier player pushing the same stride does more work, and Skating Load reflects that, which is why an ice-hockey framework for choosing load metrics calls it the biologically valid volume measure."),
              ("sc_v2w2", "On-ice load, the alternative, appears in one paper on professional hockey. It is the vest's total accelerometer load with the very smallest movements removed: it adds up every movement in every direction (stride, upper body, shooting, contact) and ignores the player's weight. The framework's criticism is that it mostly repeats that accelerometer total, whose formula is reported inconsistently in the literature, and that it under-counts defencemen, who glide and skate backwards more."),
              ("sc_v2w4", "The earlier daily volume (0.4 × on-ice load + 0.4 × explosive efforts + 0.2 × high-intensity load) was a club choice with no published source. ForeCheck replaced it with Skating Load on 14 October 2026."),
              ("sc_v2w3", "On our own season data the earlier mixed volume and Skating Load agree closely (r = 0.95), so the switch is a refinement, not an upheaval.")],
         lim=("sc_v2l", "Skating Load sees only skating. Off-ice work, such as the bike, is counted through heart-rate load instead, never mixed into skating volume."),
         refs=["nightingale2026", "allard2022", "bredt2020"]),
    dict(id="density", status="live", cat=("sc_m7c", "Session load"),
         h=("sc_m7h", "Density (SL/min), and why there is no intensity ACWR"),
         q=("sc_m7q", "Is skating load per minute a measure of how hard a session was, and does it belong in a load ratio?"),
         how=[("sc_m7s1", "A value per minute describes how densely work is packed into the time, not how hard each movement was. So ForeCheck calls Skating Load per active minute density, SL/min for short, and keeps the word intensity for the session intensity score, which combines density with two true intensity measures: % high-force strides and % high-intensity skating load."),
              ("sc_m7s2", "On our own season data up to 14 October 2026, team daily Skating Load varies about 26 % from day to day. Team daily density varies only about 4 %, between 128 and 157 all season. For one player from session to session it varies about 11 %, against about 38 % for Skating Load."),
              ("sc_m7s3", "The true intensity measures move much more: % high-force strides about 36 % and % high-intensity skating load about 23 %. The session intensity score marks about 44 % of sessions as clearly harder or easier than the player's normal, as often as the volume score (45 %)."),
              ("sc_m7s4", "What ForeCheck shows: one load ratio in the Locker Room, the Skating Load ACWR, at full width. Density has no ACWR and raises no flags. \"Was this session harder than normal?\" is answered by the session intensity score, as a z-score and a T-score.")],
         why=[("sc_m7w1", "The framework behind ForeCheck's load model recommends the per-minute value of the chosen volume measure. Volume is Skating Load, so density is Skating Load per minute, not explosive efforts per minute. The same framework makes the point that time-relative measures describe density, not intensity."),
              ("sc_m7w2", "An acute:chronic ratio built on a rate that hardly changes, with zero on rest days, mostly follows how often players skate, not how hard. It would add to the general problems of load ratios described in the research, and the published ice-hockey 5-day against 20-day guide is used for practice volume, not for a rate.")],
         lim=("sc_m7l", "The reasoning against a density ACWR is ForeCheck's own, based on our season data, not a published finding. The figures are checked again as the season goes on."),
         refs=["nightingale2026", "impellizzeri2020"]),
    dict(id="dropoff", status="live", cat=("sc_m8c", "Games"),
         h=("sc_m8h", "Late-game drop-off"),
         q=("sc_m8q", "Do players keep their skating density and stride force through a game, or do they fade in the later periods?"),
         how=[("sc_m8s1", "Each period is shown as a percentage of the 1st period: 100 % means the same as the 1st period, 90 % means 10 % less."),
              ("sc_m8s2", "Two measures are compared: density (SL/min) and % high-force strides. Both are per minute or per stride, so a period with more or less ice time can still be compared fairly."),
              ("sc_m8s3", "The comparison is always with the same players' own 1st period, never with other players or with published values.")],
         why=[("sc_m8w", "A fall in density or in stride force late in a game shows which players keep their skating quality and which fade, in the units ForeCheck already uses for every session.")],
         lim=("sc_m8l", "A drop can also come from the game itself, such as penalties, the score or a changed role, not only from fatigue. ForeCheck shows the drop; it does not claim to know the cause."),
         refs=[]),
    dict(id="zscores", status="live", cat=("sc_m2c", "Every metric"),
         h=("sc_m2h", "Compared with the player's own normal"),
         q=("sc_m2q", "Was today hard or easy for this player, compared with what is normal for him?"),
         how=[("sc_m2s1", "The session is compared with the same player's earlier sessions of the same type: game days with game days, the day before a game with other days before a game."),
              ("sc_m2s2", "The session itself is never part of its own baseline."),
              ("sc_m2s3", "At least 3 earlier sessions are needed. Otherwise ForeCheck shows \"insufficient baseline\" instead of a weak comparison."),
              ("sc_m2s4", "z = (today − the player's mean) ÷ the player's standard deviation."),
              ("sc_m2s6", "Session volume score = 0.33 × z(Skating Load) + 0.33 × z(explosive efforts) + 0.33 × z(changes of direction)."),
              ("sc_m2s7b", "Session intensity score = 0.33 × z(density, Skating Load per active minute) + 0.33 × z(% high-force strides) + 0.33 × z(% high-intensity skating load)."),
              ("sc_m2s8", "Each score is also shown as a T-score (50 + 10 × z), which coaches find easier to read."),
              ("sc_m2s9", "Classes run from very easy (z ≤ −1.5, advise a top-up) through normal (−0.8 to 0.8) to very hard (z ≥ 1.5, plan recovery).")],
         why=[("sc_m2w", "A z-score scales each player against himself, so a heavy defenceman and a light forward can be read on the same page."),
              ("sc_m2w2", "Both scores, their equal weights, the T-scores and the class cut-offs with their actions follow the multi-modal models of a published framework for choosing load metrics in ice hockey. The three metrics in each score measure different movement qualities but are correlated."),
              ("sc_m2w3", "In one elite men's team over a full season, games carried more load than practices on every measure, and time on ice alone was not an accurate measure of load. Absolute values depend on the sensor's settings, so ForeCheck compares each player with himself rather than with published numbers.")],
         lim=("sc_m2l2", "Stated plainly: the weights and cut-offs come from the authors' professional practice and unpublished data. They have not been validated against injury or performance. Early in a season the history is short, so the comparison is less certain."),
         refs=["nightingale2026", "nightingale2024"]),
    dict(id="acwr", status="live", cat=("sc_m3c", "Load over time"),
         h=("sc_m3h", "Acute and chronic load (ACWR)"),
         q=("sc_m3q", "How does recent load compare with what the player is used to?"),
         how=[("sc_m3s1", "Acute load is a short exponentially weighted moving average (EWMA), chronic load a long one. ACWR = acute ÷ chronic."),
              ("sc_m3s2c", "It is shown for Skating Load and for heart-rate exertion. Density has no ACWR; the card on density explains why. Days without a session count as zero load."),
              ("sc_m3s3b", "Windows: 5-day acute and 20-day chronic, changeable in Settings. Ice-hockey practitioners report using a 5-day against a 20-day average to plan practice volume. That is professional practice, not a validated window, and they used plain rolling averages where ForeCheck uses EWMA. Team-sport EWMA studies more often use 7 and 28 days."),
              ("sc_m3s4", "The 0.8 to 1.3 band is a monitoring guide, never an injury threshold.")],
         why=[("sc_m3w1", "EWMA gives recent days more weight than older ones. A plain rolling average treats a session 27 days ago the same as yesterday's. EWMA was proposed for exactly this reason, and in a two-season study of 59 elite Australian football players it was more sensitive than the rolling average to the higher injury risk at very high ratios."),
              ("sc_m3w2", "Other researchers say the evidence for one averaging method is still thin, and that no study has shown that changing the ratio changes injury rates. So ForeCheck uses ACWR only to describe load, and never turns it into an injury prediction or a risk score.")],
         lim=("sc_m3l", "A ratio jumps when chronic load is low, for example after an injury or a break. Read it together with the absolute numbers."),
         refs=["williams2017", "murray2017", "sampson2017", "impellizzeri2020", "nightingale2026"]),
    dict(id="offfeet", status="live", cat=("sc_m4c", "Data quality"),
         h=("sc_m4h", "Vest on, but on the bike"),
         q=("sc_m4q", "Did the player ride the bike with his sensor vest on, and is that distorting his skating numbers?"),
         how=[("sc_m4s1", "Pedalling-sized movement: in at least half the seconds of each minute the vest's accelerometer load is at least 0.02, and 95 % of seconds stay at or below 0.10. Skating and running move the vest far more."),
              ("sc_m4s2", "Heart rate up: the stretch averages at least 55 % of the player's maximum heart rate."),
              ("sc_m4s3", "No skating: the sensor's own stride detector counts at most 8 strides a minute. Skating gives 20 to 120."),
              ("sc_m4s4", "Long enough: at least 15 minutes, with pauses of up to 5 minutes joined."),
              ("sc_m4s5", "Not mixed with skating: only recordings that are mostly off-feet are flagged. Short spins inside a practice, and spins during games, are left alone."),
              ("sc_m4s8", "Likely or unsure: each listed session is marked likely off-ice (at most 2.5 skating strides and 4 accelerations a minute) or unsure, some skating detected. The limits come from the coach's first 21 decisions: every confirmed bike session stayed under both, every denied on-ice rehab session was clearly above. Unsure sessions are still listed, never dropped, and the limits are checked again as more decisions come in."),
              ("sc_m4s9", "When the ride file is already there, nobody is asked. If the player's Wattbike ride is uploaded and overlaps the stretch by 10 minutes or more, the measured power is the proof: ForeCheck confirms the session itself and logs it as automatic. The coach can still undo it."),
              ("sc_m4s6", "Independent proof: when the player's Wattbike ride file is uploaded, ForeCheck shows the matching ride and its measured power."),
              ("sc_m4s7b", "Without a ride file, the coach decides. Confirm keeps the session's heart-rate load and removes its skating numbers from volume, intensity, skating ACWR, z-scores, team averages and alerts, with nothing put in their place. Deny changes nothing. Every decision is logged and can be undone.")],
         why=[("sc_m4w", "Players often wear the vest on the bike or rower so heart rate is recorded. Time on ice then stays tiny while pedalling can trigger explosive efforts, so intensity jumps. In one rehab case, bike days read 46 to 61 efforts a minute against 25 to 35 on the same player's full practices. Left in, that inflated number sits in his chronic average and makes his real return to the ice look easier than it is.")],
         lim=("sc_m4l", "A recording can only be split by time when the staff mark a period in the sensor's own software. If the player also skated briefly in the same recording, that skating leaves with the bike part. The list shows how many minutes are involved before you decide."),
         refs=[]),
    dict(id="bikeload", status="part", cat=("sc_m5c", "Conditioning"),
         h=("sc_m5h", "Bike load against the player's own threshold"),
         q=("sc_m5q", "How hard was this ride for this player, and how close did it come to what a game asks of him?"),
         how=[("sc_m5s1", "Heart-rate load is valid on the ice and on the bike, so it is the one load measure compared across both. Bike work is never converted into \"ice units\" and never merged with skating into one number."),
              ("sc_m5s2", "On the bike, power is measured and scored against the player's own critical power (CP), his aerobic ceiling, and W′, the fixed amount of work available above it, his sprint reserve."),
              ("sc_m5s3", "CP and W′ come from a test on the Wattbike: a 3-minute all-out test, or 3-, 7- and 12-minute maximal efforts. Until a player is tested, his rides show measured values only: kJ, average and peak watts."),
              ("sc_m5s4", "Rides can follow the player's own game: shift-length efforts sized as a share of his W′, a target of his measured game heart-rate exposure, and a comparison afterwards.")],
         why=[("sc_m5w1", "Internal load (heart rate, perceived exertion) tracks movement load across team-sport sessions, but how strongly depends on the type of session. There is no fixed exchange rate between bike and skating work."),
              ("sc_m5w2", "A single FTP number squeezes aerobic and anaerobic ability into one. For a power athlete, long blocks set from FTP end up above his real aerobic ceiling and sprints far below what he can produce. Setting long blocks from CP and sprints from W′ fixes both. How fast W′ comes back differs a lot between people, so each player is tested rather than given a population value."),
              ("sc_m5w3", "Ice hockey is played in shifts of about 30 to 80 seconds with long recoveries, about 40 seconds of it effective play. Heart rate climbs toward maximum each shift and averages about 85 % of maximum on the ice, and practices reach less time above 90 % than games.")],
         lim=("sc_m5l", "The W′ model is only as good as each player's own test. ForeCheck does not work out CP from ordinary rides."),
         refs=["mclaren2018", "jones2017", "skiba2012", "skiba2021", "bartram2018", "welburn2025", "montgomery1988", "green1976", "brocherie2018", "spiering2003", "vighlarsen2020", "vighlarsen2022"]),
    dict(id="running", status="live", cat=("sc_m6c", "Conditioning"),
         h=("sc_m6h", "Running and on-feet conditioning"),
         q=("sc_m6q", "How much running did the player do outdoors, how fast, and how hard was it on his heart?"),
         how=[("sc_m6s1", "An ice rink has no GPS signal, so every indoor recording shows 0 m of GPS distance. A recording with GPS distance is outdoor work. It goes to the same Confirm / Deny list as bike sessions: if confirmed, the skating numbers leave the hockey load and the heart-rate load stays."),
              ("sc_m6s7", "When the vest records no GPS: some vests are set up for indoor use and show 0 m outdoors too. ForeCheck then recognises a run from the vest's own stride counter, which also counts running steps. A run gives a steady 110 to 155 a minute; on the ice the best 10-minute average stays around 25 to 37 a minute (checked on four sessions, October 2026). So 80 or more a minute for at least 10 minutes is a run."),
              ("sc_m6s8", "Runs found this way are confirmed automatically, never asked, and the log says why. Without GPS, distance and speed are unknown and stay blank; heart rate, TRIMP and accelerometer load are still measured."),
              ("sc_m6s2", "Measured by the vest: total distance, maximum speed, accelerometer load and heart-rate exertion."),
              ("sc_m6s3", "Calculated from the vest's 10 samples per second: distance in high-speed running (19.8 to 25.2 km/h) and sprinting (above 25.2 km/h), and accelerations and decelerations of at least 3 m/s² held for at least 0.5 s."),
              ("sc_m6s4", "Heart rate: minutes at or above 85 % and 90 % of maximum, and Edwards TRIMP, which counts the minutes in each 10 % band from 50 % to 100 % of maximum heart rate and weights them 1 to 5."),
              ("sc_m6s5", "Distance, high-speed plus sprint distance and TRIMP each get their own EWMA ratio, with the same windows as the rest of the app. Only running sessions count, and ForeCheck says so while the history is still shorter than the chronic window."),
              ("sc_m6s6", "The same GPS metrics are the load model for field sports such as football and rugby: distance as volume, metres per minute as intensity, high-speed and sprint distance and accelerations as high-intensity load. Ice hockey keeps its skating model.")],
         why=[("sc_m6w", "The speed zones are the absolute thresholds most used in football research. A systematic review found no international agreement on the exact values, so in ForeCheck they are a club setting, as is the acceleration threshold.")],
         lim=("sc_m6l", "Absolute speed zones treat every player the same. A fast player reaches the sprint zone more easily than a slow one, so compare a player mainly with himself."),
         refs=["weston2011", "collins2025", "gualtieri2023", "edwards1993"]),
]


def ref_link(ref):
    if ref[1]:
        return ' <a href="https://doi.org/%s" rel="noopener" target="_blank">doi:%s</a>' % (ref[1], ref[1])
    if len(ref) > 2:
        return ' <a href="%s" rel="noopener" target="_blank">%s</a>' % (ref[2], ref[2].split("//")[1].rstrip("/"))
    return ""


def method_card(m, n):
    status = {"live": t("sc_live", "In ForeCheck", cls="tag live"), "dev": t("sc_dev", "In development", cls="tag dev"),
              "part": t("sc_part", "Measured load in ForeCheck · CP scoring in development", cls="tag dev")}[m["status"]]
    steps = "".join("<li>%s</li>" % t(k, v) for k, v in m["how"])
    why = "".join("<p>%s</p>" % t(k, v) for k, v in m["why"])
    refs = ""
    if m["refs"]:
        refs = '<div class="mrefs"><p class="eyebrow">%s</p><ol>%s</ol></div>' % (t("sc_refs", "Research"), "".join(
            '<li>%s%s</li>' % (REFS[r][0], ref_link(REFS[r])) for r in m["refs"]))
    return """<article class="method" id="%s">
  <header><p class="eyebrow">%02d · %s</p>%s</header>
  <h3>%s</h3>
  <p class="mq">%s</p>
  <div class="mgrid">
    <div><p class="eyebrow">%s</p><ol class="steps">%s</ol></div>
    <div class="mwhy"><p class="eyebrow">%s</p>%s<p class="eyebrow">%s</p><p>%s</p></div>
  </div>
  %s
</article>""" % (m["id"], n, t(*m["cat"]), status, t(*m["h"]), t(*m["q"]), t("sc_how", "How it is calculated"), steps,
                t("sc_why", "Why"), why, t("sc_lim", "Limits, stated openly"), t(*m["lim"]), refs)


def page_science():
    nref = len({r for m in METHODS for r in m["refs"]})
    toc = '<ul class="chips toc">%s</ul>' % "".join('<li><a href="#%s" data-i18n="%s">%s</a></li>' % (m["id"], m["h"][0], tt(m["h"][0], m["h"][1])) for m in METHODS)
    labels = '<ul class="flags lab"><li class="m"><b>%s</b>%s</li><li class="d"><b>%s</b>%s</li><li class="s"><b>%s</b>%s</li></ul>' % (
        t("sc_meas", "Measured"), t("sc_meas_d", "Straight from a device or a test: heart rate, power, strides, a jump height"),
        t("sc_der", "Derived"), t("sc_der_d", "Calculated from measured numbers with a published or documented method: ACWR, z-scores"),
        t("sc_set", "Club setting"), t("sc_set_d", "A choice by your staff, not from research. Shown as such, and changeable"))
    shot = '<figure class="screen secshot"><div class="app">%s%s</div></figure>' % (
        kpis([(t("sc_k1", "Methods explained"), str(len(METHODS)), 1), (t("sc_k2", "Research sources cited"), str(nref), 0),
              (t("sc_k3", "Estimated values"), "0", 0), (t("sc_k4", "Injury-risk scores"), "0", 0)]),
        panel(t("sc_labels", "Every number says what kind it is"), labels))
    principles = [
        (t("sc_p1e", "The rule behind everything"), t("sc_p1h", "ForeCheck never guesses"),
         t("sc_p1p", "When a value is missing, ForeCheck shows it as missing. It never fills the gap with an estimate, and never puts a modelled number in place of a measured one. When a method is a club choice rather than a research finding, it says so."),
         panel(t("sc_p1x", "Where the numbers come from"), '<ul class="chips"><li>%s</li><li>%s</li><li>%s</li><li>%s</li></ul>' % (t("sc_s1", "Sensor vest"), t("sc_s2", "Heart rate"), t("sc_s3", "Bike power"), t("sc_s4", "Tests and check-ins")))),
        (t("sc_p2e", "No black box"), t("sc_p2h", "No readiness or injury-risk score"),
         t("sc_p2p", "Research does not support one number that predicts injury. ForeCheck shows what changed, against what, and how sure it is, and the staff decide."),
         panel(t("sc_p2x", "What you see instead"), '<ul class="chips"><li>%s</li><li>%s</li><li>%s</li></ul>' % (t("sc_i1", "What changed"), t("sc_i2", "Against his own normal"), t("sc_i3", "Is the data complete")))),
    ]
    methods = '<section class="methods sheet" id="methods"><div class="wrap"><div class="sec-head"><p class="eyebrow">%s</p><h2>%s</h2>%s</div>%s<p class="more-soon">%s</p></div></section>' % (
        t("sc_me", "Methods"), t("sc_mh", "How each number is made"), toc, "".join(method_card(m, i + 1) for i, m in enumerate(METHODS)),
        t("sc_more", "More methods (heart-rate zones and TRIMP, fitness tests, strength estimates, wellness) are added here as they are documented."))
    return ("science", tt("sc_title", "The science behind it"),
            hero("science", t("sc_eyebrow", "The science behind it"), t("sc_h1", 'Every number. <span class="r">Explained.</span>'),
                 t("sc_lead", "How ForeCheck measures, how it calculates every number it shows, and the research behind each method. Written so you can show it to anyone: coaches, players, medical staff, club management."), shot)
            + rows(principles) + methods)

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
%s
<link rel="icon" type="image/png" sizes="192x192" href="favicon.png">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="apple-touch-icon" href="favicon.png">
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
<script src="assets/i18n.js"></script>
<script src="assets/bg.js"></script>
</body>
</html>
""" % (seo.head(pid), pid, head, body, foot)
    html = html.replace('class="chart" role="img">', 'class="chart" role="img" aria-label="ForeCheck %s: example chart with invented demo data">' % title.replace("&amp;", "and"))
    open(os.path.join(ROOT, pid + ".html"), "w", encoding="utf-8").write(html)
    langs.write_copies(pid, html, _dict)
    return pid, len(_dict)


if __name__ == "__main__":
    allen = {}
    for b in (page_load, page_conditioning, page_calendar, page_strength, page_rehab, page_players, page_security, page_science):
        print(*write(b))
        allen.update({k: v["en"] for k, v in _dict.items()})
    missing = {k: v for k, v in allen.items() if not all(l in TR.get(k, {}) for l in ("de", "fr", "it"))}
    json.dump(missing, open(os.path.join(ROOT, "build", "untranslated.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("untranslated:", len(missing))
