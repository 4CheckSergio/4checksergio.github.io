"""Search-engine tags shared by every page: title, description, canonical, hreflang, social cards, structured data."""
import json

BASE = "https://fore-check.ch/"
ALT_NAMES = ["Fore-Check", "Fore Check", "Forecheck", "ForeCheck app", "fore-check.ch", "4Check", "Forcheck"]

PAGES = {
    "index": ("ForeCheck | Hockey performance and athlete monitoring software",
              "ForeCheck is hockey performance software: ice load and ACWR, Wattbike conditioning, strength, testing, return to play and calendars. Less laptop, more coaching."),
    "load": ("Ice load and ACWR monitoring for hockey | ForeCheck",
             "Catapult and heart-rate data turned into load, intensity and acute:chronic workload for every player, with the few players who need a different plan today."),
    "conditioning": ("Wattbike and off-ice conditioning analysis | ForeCheck",
                     "Upload Wattbike TCX rides and get power, heart rate, fatigue across the reps, decrement score and a raise, hold or lower target for the next session."),
    "calendar": ("Hockey team calendar and season load plan | ForeCheck",
                 "Team and personal calendars on every player's phone, travel strain on road weeks, and the season load plan matched to the game schedule."),
    "strength": ("Strength programming and fitness testing for hockey | ForeCheck",
                 "A workout builder that turns percentages into kilos for each player, plus jump, sprint, strength and hip tests scored against the team and each player's history."),
    "rehab": ("Return to play tracking for hockey staff | ForeCheck",
              "Return-to-play stages, criteria and rehab load against each player's own baseline, in one view for the physio, strength coach and head coach."),
    "players": ("Player wellness check-in and session RPE | ForeCheck",
                "A twenty-second morning wellness check-in and session RPE on every player's phone, set next to measured load so mismatches stand out."),
    "security": ("Swiss hosting and data security for sports teams | ForeCheck",
                 "Athlete data stored in Switzerland with a Swiss provider, HTTPS only, encrypted nightly backups, role-based access and full data export. Built for the Swiss nFADP."),
}


def url(pid, lang=None):
    u = BASE if pid == "index" else BASE + pid + ".html"
    return u + ("?lang=" + lang if lang and lang != "en" else "")


def head(pid):
    title, desc = PAGES[pid]
    out = ['<title>%s</title>' % title,
           '<meta name="description" content="%s">' % desc,
           '<link rel="canonical" href="%s">' % url(pid)]
    for l in ("en", "de", "fr", "it"):
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (l, url(pid, l)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">' % url(pid))
    out += ['<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="ForeCheck">',
            '<meta property="og:title" content="%s">' % title,
            '<meta property="og:description" content="%s">' % desc,
            '<meta property="og:url" content="%s">' % url(pid),
            '<meta property="og:image" content="%sassets/og.png">' % BASE,
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="theme-color" content="#101113">']
    if pid == "index":
        ld = [{"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "#org", "name": "ForeCheck",
               "alternateName": ALT_NAMES, "url": BASE, "logo": BASE + "assets/logo.png", "email": "info@fore-check.ch",
               "areaServed": "CH"},
              {"@context": "https://schema.org", "@type": "WebSite", "name": "ForeCheck", "alternateName": ALT_NAMES, "url": BASE,
               "inLanguage": ["en", "de", "fr", "it"], "publisher": {"@id": BASE + "#org"}},
              {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "ForeCheck", "alternateName": ALT_NAMES,
               "applicationCategory": "SportsApplication", "operatingSystem": "Web, Windows, macOS, iPadOS",
               "description": desc, "url": BASE, "publisher": {"@id": BASE + "#org"},
               "featureList": ["Ice load and ACWR monitoring", "Heart-rate zones", "Wattbike conditioning analysis",
                               "Strength programming", "Fitness testing", "Return-to-play tracking",
                               "Team and player calendars", "Season load planning", "Wellness check-in and session RPE", "Swiss data hosting"]}]
    else:
        ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ForeCheck", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": url(pid)}]}]
    out.append('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False))
    return "\n".join(out)


def sitemap():
    rows = []
    for pid in PAGES:
        alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, url(pid, l).replace("&", "&amp;")) for l in ("en", "de", "fr", "it"))
        rows.append('  <url>\n    <loc>%s</loc>%s\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>' % (url(pid), alts, url(pid), "1.0" if pid == "index" else "0.8"))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n' % "\n".join(rows)
