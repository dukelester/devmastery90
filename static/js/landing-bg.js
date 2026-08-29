/**
 * Engineer-themed animated landing background:
 * code rain + node constellation. Respects prefers-reduced-motion.
 */
(function () {
  "use strict";

  var canvas = document.querySelector("[data-eng-canvas]");
  if (!canvas) return;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ctx = canvas.getContext("2d");
  if (!ctx) return;

  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var w = 0;
  var h = 0;
  var drops = [];
  var nodes = [];
  var glyphs = "01<>{}[]/;=+#*$αβλΣπ∞→←≡≠≥≤async await def class return SELECT JOIN WHERE redis celery django pytest HTTP O(n) git SHA";
  var chars = glyphs.split("");
  var raf = 0;
  var last = 0;

  function themeColors() {
    var dark = document.documentElement.getAttribute("data-theme") === "dark";
    return dark
      ? {
          rain: "rgba(61, 212, 203, 0.55)",
          rainDim: "rgba(61, 212, 203, 0.12)",
          node: "rgba(61, 212, 203, 0.85)",
          line: "rgba(61, 212, 203, 0.18)",
          clear: "rgba(11, 16, 23, 0.18)",
        }
      : {
          rain: "rgba(10, 107, 102, 0.45)",
          rainDim: "rgba(10, 107, 102, 0.1)",
          node: "rgba(10, 107, 102, 0.75)",
          line: "rgba(10, 107, 102, 0.16)",
          clear: "rgba(226, 232, 240, 0.22)",
        };
  }

  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    w = Math.max(320, Math.floor(rect.width));
    h = Math.max(320, Math.floor(rect.height));
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  function seed() {
    var cols = Math.max(12, Math.floor(w / 28));
    drops = [];
    for (var i = 0; i < cols; i++) {
      drops.push({
        x: (i + 0.5) * (w / cols),
        y: Math.random() * h,
        speed: 28 + Math.random() * 55,
        len: 8 + Math.floor(Math.random() * 14),
      });
    }
    var count = reduce ? 18 : 42;
    nodes = [];
    for (var n = 0; n < count; n++) {
      nodes.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: 1.2 + Math.random() * 2.2,
      });
    }
  }

  function drawRain(colors, dt) {
    ctx.font = "12px \"JetBrains Mono\", ui-monospace, monospace";
    for (var i = 0; i < drops.length; i++) {
      var d = drops[i];
      d.y += d.speed * dt;
      if (d.y - d.len * 16 > h) {
        d.y = -Math.random() * h * 0.3;
        d.speed = 28 + Math.random() * 55;
      }
      for (var j = 0; j < d.len; j++) {
        var ch = chars[(i * 13 + j * 7 + Math.floor(d.y / 16)) % chars.length];
        var yy = d.y - j * 16;
        ctx.fillStyle = j === 0 ? colors.rain : colors.rainDim;
        ctx.globalAlpha = j === 0 ? 0.85 : Math.max(0.08, 0.45 - j * 0.03);
        ctx.fillText(ch, d.x, yy);
      }
    }
    ctx.globalAlpha = 1;
  }

  function drawNetwork(colors, dt) {
    var i, j, a, b, dx, dy, dist;
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      a.x += a.vx;
      a.y += a.vy;
      if (a.x < 0 || a.x > w) a.vx *= -1;
      if (a.y < 0 || a.y > h) a.vy *= -1;
    }
    for (i = 0; i < nodes.length; i++) {
      for (j = i + 1; j < nodes.length; j++) {
        a = nodes[i];
        b = nodes[j];
        dx = a.x - b.x;
        dy = a.y - b.y;
        dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          ctx.strokeStyle = colors.line;
          ctx.globalAlpha = 1 - dist / 130;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1;
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      ctx.fillStyle = colors.node;
      ctx.beginPath();
      ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function frame(ts) {
    if (!last) last = ts;
    var dt = Math.min(0.05, (ts - last) / 1000);
    last = ts;
    var colors = themeColors();
    ctx.fillStyle = colors.clear;
    ctx.fillRect(0, 0, w, h);
    if (!reduce) drawRain(colors, dt);
    drawNetwork(colors, dt);
    raf = requestAnimationFrame(frame);
  }

  function start() {
    cancelAnimationFrame(raf);
    last = 0;
    resize();
    if (reduce) {
      var colors = themeColors();
      ctx.clearRect(0, 0, w, h);
      drawNetwork(colors, 0);
      return;
    }
    raf = requestAnimationFrame(frame);
  }

  window.addEventListener("resize", function () {
    clearTimeout(window.__dmEngResize);
    window.__dmEngResize = setTimeout(start, 120);
  });

  // Restart when theme toggles
  var obs = new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      if (mutations[i].attributeName === "data-theme") start();
    }
  });
  obs.observe(document.documentElement, { attributes: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
