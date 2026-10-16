// Language picker. Every language has its own static pages: English at the root, the others in /de/, /fr/ and /it/.
// The picker only moves between those pages; nothing is guessed from the browser, so search engines and visitors see the same page.
(function () {
  var L = ["en", "de", "fr", "it"], sel = document.getElementById("lang-select");
  var here = document.documentElement.lang || "en";
  if (L.indexOf(here) < 0) here = "en";
  var parts = location.pathname.split("/"), file = parts.pop();
  function target(l) {
    var up = here === "en" ? "" : "../";
    return up + (l === "en" ? "" : l + "/") + (file || (location.protocol === "file:" ? "index.html" : "")) + location.hash;
  }
  // old links used ?lang=de: send them to the page that now lives at its own address
  try {
    var q = new URL(location.href).searchParams.get("lang");
    if (q && q !== here && L.indexOf(q) >= 0 && here === "en") { location.replace(target(q)); return; }
  } catch (e) {}
  if (sel) {
    sel.value = here;
    sel.addEventListener("change", function () { if (sel.value !== here) location.href = target(sel.value); });
  }
})();
