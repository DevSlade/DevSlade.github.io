// Capybara Cartel site: menu, copy-to-clipboard, screenshot carousel, reveal on scroll, bottle parallax.
// Everything here is extra: the pages work and read fine without it.
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // mobile menu
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });
  }

  // a small message at the bottom of the screen
  var toastEl;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      toastEl.setAttribute("aria-live", "polite");
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }

  // copy buttons: <button data-copy="text">
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-copy");
      var done = function () { toast("Copied " + text); };
      var fail = function () { toast(fallbackCopy(text) ? "Copied " + text : "Couldn't copy. The address is " + text); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fail);
      else fail();
    });
  });

  // screenshot carousel: [data-carousel] holds a scroller and two buttons
  document.querySelectorAll("[data-carousel]").forEach(function (c) {
    var track = c.querySelector(".shots-track");
    var prev = c.querySelector("[data-prev]");
    var next = c.querySelector("[data-next]");
    if (!track || !prev || !next) return;
    // where each screenshot starts, in the track's scroll coordinates
    function starts() {
      var base = track.getBoundingClientRect().left - track.scrollLeft;
      return Array.prototype.map.call(track.children, function (li) { return li.getBoundingClientRect().left - base; });
    }
    function go(dir) {
      var x = track.scrollLeft, max = track.scrollWidth - track.clientWidth, s = starts(), to = dir > 0 ? max : 0;
      for (var i = 0; i < s.length; i++) {
        if (dir > 0 && s[i] > x + 8) { to = s[i]; break; }
        if (dir < 0 && s[i] < x - 8) to = s[i];
      }
      track.scrollTo({ left: Math.max(0, Math.min(max, to)), behavior: reduce ? "auto" : "smooth" });
    }
    function update() {
      var max = track.scrollWidth - track.clientWidth - 6;
      prev.disabled = track.scrollLeft <= 6;
      next.disabled = track.scrollLeft >= max;
    }
    prev.addEventListener("click", function () { go(-1); });
    next.addEventListener("click", function () { go(1); });
    track.addEventListener("scroll", function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  // reveal on scroll
  var items = document.querySelectorAll(".reveal");
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // parallax: [data-parallax] moves its [data-depth] children with the mouse (not on touch screens)
  var fine = window.matchMedia && window.matchMedia("(pointer: fine)").matches;
  if (!reduce && fine) {
    document.querySelectorAll("[data-parallax]").forEach(function (scene) {
      var layers = scene.querySelectorAll("[data-depth]");
      var raf = 0, tx = 0, ty = 0;
      scene.addEventListener("pointermove", function (e) {
        var r = scene.getBoundingClientRect();
        tx = (e.clientX - r.left) / r.width - 0.5;
        ty = (e.clientY - r.top) / r.height - 0.5;
        if (!raf) raf = window.requestAnimationFrame(apply);
      });
      scene.addEventListener("pointerleave", function () { tx = 0; ty = 0; if (!raf) raf = window.requestAnimationFrame(apply); });
      function apply() {
        raf = 0;
        layers.forEach(function (l) {
          var d = parseFloat(l.getAttribute("data-depth")) || 0;
          l.style.translate = (tx * d * -40).toFixed(1) + "px " + (ty * d * -30).toFixed(1) + "px";
        });
      }
    });
  }

  // legal pages: the contents list starts open on wide screens, where it's a sticky sidebar
  if (window.matchMedia && window.matchMedia("(min-width: 1000px)").matches) {
    document.querySelectorAll(".toc details").forEach(function (d) { d.open = true; });
  }

  // this year in the footer
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
