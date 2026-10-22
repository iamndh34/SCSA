/* SCSA deck: presentation-only playback.
   `hyperframes present` moves between steps by seeking. Inside a live slideshow
   this replays the authored segment at real speed when moving forward, so the
   audience sees the motion; moving back still jumps. Studio, snapshots and
   renders never enable it, so every frame stays a pure function of time. */
(function () {
  if (window.hfPlayForward) return;
  function inSlideshow() {
    try { return window.parent !== window && !!window.parent.document.querySelector("hyperframes-slideshow"); }
    catch (e) { return false; }
  }
  var watched = [];
  window.hfPlayForward = function (tl, maxDur) {
    if (!inSlideshow()) return;
    watched.push({ tl: tl, shown: tl.time(), anim: null, set: 0, max: maxDur || 12 });
  };
  function tick() {
    for (var i = 0; i < watched.length; i++) {
      var w = watched[i], now = w.tl.time();
      if (w.anim) {
        if (Math.abs(now - w.set) < 1e-4) { w.shown = now; continue; }
        w.anim.kill(); w.anim = null;
      }
      if (Math.abs(now - w.shown) < 1e-4) continue;
      var from = w.shown, to = now;
      if (to < from) { w.shown = to; continue; }
      w.tl.time(from); w.set = from;
      (function (w, from, to) {
        var p = { t: from };
        w.anim = gsap.to(p, {
          t: to, duration: Math.min(to - from, w.max), ease: "none",
          onUpdate: function () { w.tl.time(p.t); w.set = p.t; w.shown = p.t; },
          onComplete: function () { w.anim = null; w.tl.time(to); w.set = to; w.shown = to; }
        });
      })(w, from, to);
    }
  }
  (function start() { if (window.gsap) gsap.ticker.add(tick); else setTimeout(start, 50); })();
})();
