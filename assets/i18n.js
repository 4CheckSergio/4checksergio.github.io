// Language picker shared by the feature pages. Strings come from window.FC_I18N = {key: {en, de, fr, it}}.
(function () {
  var T = window.FC_I18N || {}, L = ["en", "de", "fr", "it"], sel = document.getElementById("lang-select");
  function apply(l) {
    if (L.indexOf(l) < 0) l = "en";
    document.documentElement.lang = l;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = T[el.getAttribute("data-i18n")];
      if (v) el.innerHTML = v[l] != null ? v[l] : v.en;
    });
    if (sel) sel.value = l;
    try { localStorage.setItem("fc-lang", l); } catch (e) {}
    try {
      var u = new URL(location.href);
      if (l === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", l);
      history.replaceState(null, "", u);
    } catch (e) {}
    // keep the chosen language when moving between pages
    document.querySelectorAll('a[href$=".html"], a[href*=".html#"]').forEach(function (a) {
      try {
        var u = new URL(a.getAttribute("href"), location.href);
        if (l === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", l);
        a.setAttribute("href", u.pathname.split("/").pop() + u.search + u.hash);
      } catch (e) {}
    });
  }
  function pick() {
    try { var q = new URL(location.href).searchParams.get("lang"); if (q && L.indexOf(q) >= 0) return q; } catch (e) {}
    try { var s = localStorage.getItem("fc-lang"); if (s && L.indexOf(s) >= 0) return s; } catch (e) {}
    var n = navigator.languages || [navigator.language || "en"];
    for (var i = 0; i < n.length; i++) { var c = String(n[i]).slice(0, 2).toLowerCase(); if (L.indexOf(c) >= 0) return c; }
    return "en";
  }
  if (sel) sel.addEventListener("change", function () { apply(sel.value); });
  apply(pick());
})();
