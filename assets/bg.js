// Moving hero backgrounds for the feature pages, drawn on a canvas so they stay light (no video files).
// One scene per page, picked by data-bg on .phero. Reduced motion gets a single still frame.
(function () {
  var hero = document.querySelector(".phero"), cv = hero && hero.querySelector(".bgfx");
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext("2d"), mode = hero.getAttribute("data-bg"), W = 0, H = 0, dpr = 1, t0 = performance.now(), running = true;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var RED = "255,69,69", BLUE = "95,139,255", INK = "238,240,242", GREY = "162,167,173";
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function size() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    init();
  }
  var P = [];
  function init() {
    P = [];
    var n = Math.round(W / 14);
    if (mode === "load") for (var i = 0; i < n; i++) P.push({ y: rnd(0, H), x: rnd(-W, W), l: rnd(60, 260), v: rnd(1.2, 4.5), w: rnd(.6, 2.2), red: Math.random() < .07 });
    if (mode === "strength") for (var j = 0; j < 46; j++) P.push({ x: rnd(0, W), y: rnd(0, H), s: rnd(10, 34), v: rnd(.3, 1.4), a: rnd(.08, .35), red: Math.random() < .1 });
    if (mode === "calendar") for (var k = 0; k < 28; k++) P.push({ r: rnd(80, Math.max(W, H) * .8), a: rnd(0, 6.28), v: rnd(.0006, .0026) * (Math.random() < .5 ? -1 : 1), s: rnd(1, 2.6), red: Math.random() < .12 });
    if (mode === "players") for (var m = 0; m < 90; m++) P.push({ x: rnd(0, W), y: rnd(0, H), p: rnd(0, 6.28), s: rnd(1.5, 3.5) });
  }
  var draw = {
    load: function (t) {
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (p) {
        p.x += p.v; if (p.x - p.l > W) { p.x = -rnd(0, 200); p.y = rnd(0, H); }
        var g = ctx.createLinearGradient(p.x - p.l, 0, p.x, 0);
        var c = p.red ? RED : GREY;
        g.addColorStop(0, "rgba(" + c + ",0)"); g.addColorStop(1, "rgba(" + c + "," + (p.red ? .9 : .38) + ")");
        ctx.strokeStyle = g; ctx.lineWidth = p.w; ctx.beginPath(); ctx.moveTo(p.x - p.l, p.y); ctx.lineTo(p.x, p.y); ctx.stroke();
      });
    },
    conditioning: function (t) {
      ctx.clearRect(0, 0, W, H);
      var base = H * .78, bw = 7, off = (t * .06) % bw;
      for (var x = -bw; x < W + bw; x += bw) {
        var k = Math.floor((x + t * .06) / bw);
        var sprint = (k % 38) < 3, v = sprint ? 0.55 + .15 * Math.sin(k) : .12 + .05 * Math.sin(k * .7) + .03 * Math.sin(k * 2.3);
        ctx.fillStyle = sprint ? "rgba(" + RED + ",.55)" : "rgba(" + BLUE + ",.28)";
        ctx.fillRect(x - off, base - v * H * .6, bw - 2, v * H * .6);
      }
      ctx.strokeStyle = "rgba(" + INK + ",.55)"; ctx.lineWidth = 1.6; ctx.beginPath();
      for (var x2 = 0; x2 <= W; x2 += 4) {
        var y = H * .38 + Math.sin((x2 + t * .06) / 90) * 18 + Math.sin((x2 + t * .06) / 23) * 4;
        x2 ? ctx.lineTo(x2, y) : ctx.moveTo(x2, y);
      }
      ctx.stroke();
    },
    calendar: function (t) {
      ctx.fillStyle = "rgba(16,17,19,.18)"; ctx.fillRect(0, 0, W, H);
      var cx = W * .78, cy = H * .35;
      P.forEach(function (p) {
        p.a += p.v * 16;
        var x = cx + Math.cos(p.a) * p.r, y = cy + Math.sin(p.a) * p.r * .55;
        ctx.fillStyle = "rgba(" + (p.red ? RED : INK) + "," + (p.red ? .95 : .7) + ")";
        ctx.beginPath(); ctx.arc(x, y, p.s, 0, 6.29); ctx.fill();
      });
    },
    strength: function (t) {
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (p) {
        p.y -= p.v; if (p.y < -40) { p.y = H + 40; p.x = rnd(0, W); }
        ctx.strokeStyle = "rgba(" + (p.red ? RED : GREY) + "," + (p.red ? .7 : p.a) + ")"; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(p.x - p.s, p.y + p.s * .6); ctx.lineTo(p.x, p.y); ctx.lineTo(p.x + p.s, p.y + p.s * .6); ctx.stroke();
      });
    },
    rehab: function (t) {
      ctx.clearRect(0, 0, W, H);
      var cx = W * .8, cy = H * .3, max = Math.max(W, H);
      for (var i = 0; i < 9; i++) {
        var r = ((t * .05 + i * max / 9) % max);
        var a = Math.max(0, .5 - r / max * .5);
        ctx.strokeStyle = "rgba(" + (i % 4 === 0 ? RED : BLUE) + "," + a + ")"; ctx.lineWidth = i % 4 === 0 ? 2.5 : 1.5;
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, 6.29); ctx.stroke();
      }
      ctx.fillStyle = "rgba(" + RED + ",.9)"; ctx.beginPath(); ctx.arc(cx, cy, 6 + Math.sin(t / 300) * 2, 0, 6.29); ctx.fill();
    },
    players: function (t) {
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (p, i) {
        var on = Math.sin(t / 900 + p.p) > .6;
        ctx.fillStyle = on ? "rgba(" + (i % 11 === 0 ? RED : BLUE) + ",.9)" : "rgba(" + GREY + ",.18)";
        ctx.beginPath(); ctx.arc(p.x, p.y, on ? p.s * 1.3 : p.s, 0, 6.29); ctx.fill();
      });
    }
  };
  var fn = draw[mode]; if (!fn) return;
  function loop(now) {
    if (running) fn(now - t0);
    if (!still) requestAnimationFrame(loop);
  }
  if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { running = e[0].isIntersecting; }).observe(hero);
  window.addEventListener("resize", size);
  size();
  if (still) { for (var i = 0; i < 120; i++) fn(i * 16); } else requestAnimationFrame(loop);
})();
