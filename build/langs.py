"""Writes the translated copies of every page: /de/, /fr/ and /it/, each a full static page in one language.

English pages stay at the root. A copy gets its translated text from the page's own string table
(window.FC_I18N for index.html, the build dictionary for the generated pages), its own title,
description, canonical and hreflang from seo.py, and asset paths one folder up.
Run after site.py: python3 build/langs.py (site.py calls it for its pages, this file's main does index.html).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("de", "fr", "it")


def _replace_inner(html, key, value):
    """Replace the inner HTML of every element carrying data-i18n="key"."""
    out, pos, attr = [], 0, 'data-i18n="%s"' % key
    while True:
        i = html.find(attr, pos)
        if i < 0:
            break
        start = html.rfind("<", 0, i)
        tag = re.match(r"<([a-zA-Z0-9]+)", html[start:]).group(1)
        open_end = html.index(">", i) + 1
        depth, j = 1, open_end
        pat = re.compile(r"<(/?)%s\b[^>]*>" % tag)
        while depth:
            m = pat.search(html, j)
            depth += -1 if m.group(1) else (0 if m.group(0).endswith("/>") else 1)
            j = m.end()
        close_start = j - len("</%s>" % tag)
        out.append(html[pos:open_end] + value)
        pos = close_start
    out.append(html[pos:])
    return "".join(out)


def localize(html, strings, lang, pid):
    for key, v in strings.items():
        if lang in v and 'data-i18n="%s"' % key in html:
            html = _replace_inner(html, key, v[lang])
    html = html.replace('<html lang="en">', '<html lang="%s">' % lang, 1)
    # head: translated title, description, canonical and hreflang
    a = html.index("<title>")
    b = html.index("</script>", html.index("application/ld+json")) + len("</script>")
    html = html[:a] + seo.head(pid, lang) + html[b:]
    # assets live one folder up
    html = re.sub(r'(src|href|poster)="(assets/|favicon\.)', r'\1="../\2', html)
    html = html.replace('"assets/video/', '"../assets/video/')
    html = html.replace("forecheck_explainer_en", "forecheck_explainer_" + lang)
    html = html.replace('srclang="en" label="English"', 'srclang="%s" label="%s"' % (lang, {"de": "Deutsch", "fr": "Français", "it": "Italiano"}[lang]))
    # the string table is only needed by the English source page
    html = re.sub(r"<script>window\.FC_I18N=.*?;</script>\n?", "", html, flags=re.S)
    return html


def write_copies(pid, html, strings):
    for lang in LANGS:
        d = os.path.join(ROOT, lang)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, pid + ".html"), "w", encoding="utf-8").write(localize(html, strings, lang, pid))


def index_strings(html):
    i = html.index("window.FC_I18N=") + len("window.FC_I18N=")
    return json.JSONDecoder().raw_decode(html, i)[0]


if __name__ == "__main__":
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    # keep the English head in step with seo.py
    a = src.index("<title>")
    b = src.index("</script>", src.index("application/ld+json")) + len("</script>")
    src = src[:a] + seo.head("index") + src[b:]
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(src)
    write_copies("index", src, index_strings(src))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(seo.sitemap())
    print("index copies written:", ", ".join(LANGS))
