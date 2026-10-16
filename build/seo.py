"""Search-engine tags shared by every page: title, description, canonical, hreflang, social cards, structured data."""
import json

BASE = "https://fore-check.ch/"
ALT_NAMES = ["Fore-Check", "Fore Check", "Forecheck", "ForeCheck app", "fore-check.ch", "4Check", "Forcheck"]

PAGES = {
    "index": ("ForeCheck | Sports performance and athlete monitoring software",
              "ForeCheck is science-backed sports performance software: training load and ACWR, conditioning, strength, testing, return to play and calendars. Built first for ice hockey. Decisions, not guesses."),
    "load": ("Training load and ACWR monitoring for sports teams | ForeCheck",
             "Sensor-vest and heart-rate data turned into load, intensity and acute:chronic workload for every player, with the few players who need a different plan today."),
    "conditioning": ("Wattbike and off-ice conditioning analysis | ForeCheck",
                     "Upload Wattbike TCX rides and get power, heart rate, fatigue across the reps, decrement score and a raise, hold or lower target for the next session."),
    "calendar": ("Team calendar and season load plan | ForeCheck",
                 "Team and personal calendars on every player's phone, travel strain on road weeks, and the season load plan matched to the game schedule."),
    "strength": ("Strength programming and fitness testing for athletes | ForeCheck",
                 "A workout builder that turns percentages into kilos for each player, plus jump, sprint, strength and hip tests scored against the team and each player's history."),
    "rehab": ("Return to play tracking for sports medicine staff | ForeCheck",
              "Return-to-play stages, criteria and rehab load against each player's own baseline, in one view for the physio, strength coach and head coach."),
    "players": ("Player wellness check-in and session RPE | ForeCheck",
                "A twenty-second morning wellness check-in and session RPE on every player's phone, set next to measured load so mismatches stand out."),
    "security": ("Swiss hosting and data security for sports teams | ForeCheck",
                 "Athlete data stored in Switzerland with a Swiss provider, HTTPS only, encrypted nightly backups, role-based access and full data export. Built for the Swiss nFADP."),
    "science": ("The science behind ForeCheck: load, ACWR and z-scores explained",
                "How ForeCheck measures and calculates training load, EWMA ACWR, z-scores against each player's own normal, off-feet bike sessions and critical power, with the research behind each method."),
}


# Translated titles and descriptions for the /de/, /fr/ and /it/ pages.
PAGES_TR = {
    "index": {
        "de": ("ForeCheck | Software für Sport-Performance und Athletenmonitoring",
               "ForeCheck ist wissenschaftlich fundierte Sport-Performance-Software: Trainingsbelastung und ACWR, Kondition, Kraft, Tests, Return to Play und Kalender. Zuerst für Eishockey entwickelt. Entscheidungen statt Vermutungen."),
        "fr": ("ForeCheck | Logiciel de performance sportive et de suivi des athlètes",
               "ForeCheck est un logiciel de performance sportive fondé sur la science : charge d’entraînement et ACWR, préparation physique, force, tests, retour au jeu et calendriers. Conçu d’abord pour le hockey sur glace. Des décisions, pas des suppositions."),
        "it": ("ForeCheck | Software per la performance sportiva e il monitoraggio degli atleti",
               "ForeCheck è un software per la performance sportiva basato sulla scienza: carico di allenamento e ACWR, condizionamento, forza, test, ritorno al gioco e calendari. Pensato prima per l’hockey su ghiaccio. Decisioni, non supposizioni."),
    },
    "hockey": {
        "de": ("Eishockey-Performance-Software: Skating-Load, Dichte und Spielanalyse | ForeCheck",
               "Skating-Load, Dichte pro aktive Minute, Leistungsabfall pro Drittel, Belastung von Spielern mit und ohne Einsatz, Velo-Erkennung neben dem Eis und Spieltag-Tags, jeweils gestützt auf Eishockey-Forschung."),
        "fr": ("Logiciel de performance pour le hockey sur glace : charge de patinage, densité et analyse de match | ForeCheck",
               "Charge de patinage, densité par minute active, baisse par tiers en fin de match, charge des joueurs qui ont joué ou non, détection du vélo hors glace et repères jour de match, chacun appuyé par la recherche en hockey sur glace."),
        "it": ("Software per la performance nell’hockey su ghiaccio: carico di pattinaggio, densità e analisi partita | ForeCheck",
               "Carico di pattinaggio, densità per minuto attivo, calo per tempo a fine partita, carico di chi ha giocato e di chi no, rilevamento della bici fuori dal ghiaccio e tag giorno partita, ognuno supportato dalla ricerca sull’hockey su ghiaccio."),
    },
    "load": {
        "de": ("Trainingsbelastung und ACWR-Monitoring für Sportteams | ForeCheck",
               "Daten aus Sensorweste und Herzfrequenz werden zu Belastung, Intensität und akut-chronischem Verhältnis für jeden Spieler, mit den wenigen Spielern, die heute einen anderen Plan brauchen."),
        "fr": ("Suivi de la charge d’entraînement et de l’ACWR pour les équipes | ForeCheck",
               "Les données de la veste à capteurs et de la fréquence cardiaque deviennent charge, intensité et ratio aigu:chronique pour chaque joueur, avec les quelques joueurs qui ont besoin d’un autre plan aujourd’hui."),
        "it": ("Monitoraggio del carico di allenamento e dell’ACWR per squadre | ForeCheck",
               "I dati della pettorina con sensori e della frequenza cardiaca diventano carico, intensità e rapporto acuto:cronico per ogni giocatore, con i pochi giocatori che oggi hanno bisogno di un piano diverso."),
    },
    "conditioning": {
        "de": ("Wattbike- und Konditionsanalyse neben dem Eis | ForeCheck",
               "Wattbike-TCX-Fahrten hochladen und Leistung, Herzfrequenz, Ermüdung über die Wiederholungen, Decrement-Score und ein Ziel für die nächste Einheit erhalten: steigern, halten oder senken."),
        "fr": ("Analyse Wattbike et préparation physique hors glace | ForeCheck",
               "Importez les sorties Wattbike en TCX et obtenez puissance, fréquence cardiaque, fatigue au fil des répétitions, score de décrément et un objectif pour la prochaine séance : augmenter, maintenir ou baisser."),
        "it": ("Analisi Wattbike e condizionamento fuori dal ghiaccio | ForeCheck",
               "Carica le uscite Wattbike in TCX e ottieni potenza, frequenza cardiaca, fatica lungo le ripetute, decrement score e un obiettivo per la prossima seduta: aumentare, mantenere o ridurre."),
    },
    "calendar": {
        "de": ("Teamkalender und Belastungsplan der Saison | ForeCheck",
               "Team- und persönliche Kalender auf dem Handy jedes Spielers, Reisebelastung in Auswärtswochen und der Belastungsplan der Saison, abgestimmt auf den Spielplan."),
        "fr": ("Calendrier d’équipe et plan de charge de la saison | ForeCheck",
               "Calendriers d’équipe et personnels sur le téléphone de chaque joueur, fatigue des déplacements lors des semaines à l’extérieur et plan de charge de la saison calé sur le calendrier des matchs."),
        "it": ("Calendario di squadra e piano di carico della stagione | ForeCheck",
               "Calendari di squadra e personali sul telefono di ogni giocatore, stress da viaggio nelle settimane in trasferta e piano di carico della stagione allineato al calendario delle partite."),
    },
    "strength": {
        "de": ("Krafttraining und Fitnesstests für Athleten | ForeCheck",
               "Ein Trainingsplaner, der Prozente für jeden Spieler in Kilos umrechnet, dazu Sprung-, Sprint-, Kraft- und Hüfttests im Vergleich mit dem Team und der eigenen Geschichte jedes Spielers."),
        "fr": ("Programmes de force et tests physiques pour athlètes | ForeCheck",
               "Un générateur de séances qui convertit les pourcentages en kilos pour chaque joueur, plus des tests de saut, de sprint, de force et de hanche comparés à l’équipe et à l’historique de chaque joueur."),
        "it": ("Programmi di forza e test atletici per atleti | ForeCheck",
               "Un costruttore di allenamenti che trasforma le percentuali in chili per ogni giocatore, più test di salto, sprint, forza e anca confrontati con la squadra e con lo storico di ogni giocatore."),
    },
    "rehab": {
        "de": ("Return-to-Play-Tracking für den medizinischen Staff | ForeCheck",
               "Return-to-Play-Stufen, Kriterien und Reha-Belastung im Vergleich zur eigenen Basis jedes Spielers, in einer Ansicht für Physio, Athletiktrainer und Headcoach."),
        "fr": ("Suivi du retour au jeu pour les staffs médicaux | ForeCheck",
               "Étapes du retour au jeu, critères et charge de réhabilitation comparés à la base de chaque joueur, dans une seule vue pour le physio, le préparateur physique et l’entraîneur principal."),
        "it": ("Monitoraggio del ritorno al gioco per lo staff medico | ForeCheck",
               "Fasi del ritorno al gioco, criteri e carico di riabilitazione rispetto alla base di ogni giocatore, in un’unica vista per fisioterapista, preparatore atletico e allenatore."),
    },
    "players": {
        "de": ("Wellness-Check-in und Session-RPE der Spieler | ForeCheck",
               "Ein zwanzigsekündiger Wellness-Check-in am Morgen und Session-RPE auf dem Handy jedes Spielers, neben der gemessenen Belastung, damit Abweichungen auffallen."),
        "fr": ("Check-in bien-être et RPE de séance des joueurs | ForeCheck",
               "Un check-in bien-être de vingt secondes le matin et la RPE de séance sur le téléphone de chaque joueur, à côté de la charge mesurée pour faire ressortir les écarts."),
        "it": ("Check-in di benessere e RPE di seduta dei giocatori | ForeCheck",
               "Un check-in di benessere di venti secondi al mattino e la RPE di seduta sul telefono di ogni giocatore, accanto al carico misurato, così le discrepanze saltano all’occhio."),
    },
    "security": {
        "de": ("Schweizer Hosting und Datensicherheit für Sportteams | ForeCheck",
               "Athletendaten in der Schweiz bei einem Schweizer Anbieter, nur HTTPS, verschlüsselte nächtliche Backups, rollenbasierter Zugriff und vollständiger Datenexport. Gebaut für das Schweizer revDSG."),
        "fr": ("Hébergement suisse et sécurité des données pour les équipes | ForeCheck",
               "Données des athlètes stockées en Suisse chez un fournisseur suisse, HTTPS uniquement, sauvegardes nocturnes chiffrées, accès par rôle et export complet des données. Conçu pour la nLPD suisse."),
        "it": ("Hosting svizzero e sicurezza dei dati per squadre sportive | ForeCheck",
               "Dati degli atleti archiviati in Svizzera presso un fornitore svizzero, solo HTTPS, backup notturni cifrati, accesso per ruolo ed esportazione completa dei dati. Pensato per la nLPD svizzera."),
    },
    "science": {
        "de": ("Die Wissenschaft hinter ForeCheck: Belastung, ACWR und z-Werte erklärt",
               "Wie ForeCheck Trainingsbelastung, EWMA-ACWR, z-Werte gegenüber dem eigenen Normalwert jedes Spielers, Velo-Einheiten neben dem Eis und Critical Power misst und berechnet, mit der Forschung hinter jeder Methode."),
        "fr": ("La science derrière ForeCheck : charge, ACWR et scores z expliqués",
               "Comment ForeCheck mesure et calcule la charge d’entraînement, l’ACWR EWMA, les scores z par rapport à la normale de chaque joueur, les séances de vélo hors glace et la puissance critique, avec la recherche derrière chaque méthode."),
        "it": ("La scienza dietro ForeCheck: carico, ACWR e punteggi z spiegati",
               "Come ForeCheck misura e calcola il carico di allenamento, l’ACWR EWMA, i punteggi z rispetto alla norma di ogni giocatore, le sedute in bici fuori dal ghiaccio e la potenza critica, con la ricerca dietro ogni metodo."),
    },
}

LANGS = ("en", "de", "fr", "it")
LOCALE = {"en": "en_GB", "de": "de_CH", "fr": "fr_CH", "it": "it_CH"}


def url(pid, lang=None):
    """English lives at the root; each translation has its own folder (/de/, /fr/, /it/)."""
    folder = "" if not lang or lang == "en" else lang + "/"
    return BASE + folder + ("" if pid == "index" else pid + ".html")


def meta(pid, lang="en"):
    if lang != "en" and pid in PAGES_TR and lang in PAGES_TR[pid]:
        return PAGES_TR[pid][lang]
    return PAGES[pid]


def head(pid, lang="en"):
    title, desc = meta(pid, lang)
    out = ['<title>%s</title>' % title,
           '<meta name="description" content="%s">' % desc,
           '<link rel="canonical" href="%s">' % url(pid, lang)]
    for l in LANGS:
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (l, url(pid, l)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">' % url(pid))
    out += ['<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="ForeCheck">',
            '<meta property="og:locale" content="%s">' % LOCALE[lang],
            '<meta property="og:title" content="%s">' % title,
            '<meta property="og:description" content="%s">' % desc,
            '<meta property="og:url" content="%s">' % url(pid, lang),
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
               "description": desc, "url": url(pid, lang), "inLanguage": lang, "publisher": {"@id": BASE + "#org"},
               "featureList": ["Training load and ACWR monitoring", "Heart-rate zones", "Wattbike conditioning analysis",
                               "Strength programming", "Fitness testing", "Return-to-play tracking",
                               "Team and player calendars", "Season load planning", "Wellness check-in and session RPE", "Swiss data hosting"]}]
    else:
        ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ForeCheck", "item": url("index", lang)},
            {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": url(pid, lang)}]}]
    out.append('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False))
    return "\n".join(out)


def sitemap():
    rows = []
    for pid in PAGES:
        alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, url(pid, l)) for l in LANGS)
        alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url(pid)
        for lang in LANGS:
            rows.append('  <url>\n    <loc>%s</loc>%s\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>' % (url(pid, lang), alts, "1.0" if pid == "index" else "0.8"))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n' % "\n".join(rows)
