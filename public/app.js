(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Before/after sliders: native range input drives --pos.
  document.querySelectorAll(".compare").forEach(function (box) {
    var range = box.querySelector(".compare-range");
    if (!range) return;
    function set(v) {
      v = Math.max(0, Math.min(100, Number(v)));
      box.style.setProperty("--pos", v + "%");
      range.setAttribute("aria-valuetext", Math.round(v) + "% before, " + Math.round(100 - v) + "% after");
    }
    range.addEventListener("input", function () { box.classList.remove("hint"); set(range.value); });
    // Pointer dragging anywhere on the image (horizontal only; vertical swipes still scroll).
    var dragging = false, startX = 0, startY = 0, decided = false;
    function fromX(x) {
      var r = box.getBoundingClientRect();
      range.value = ((x - r.left) / r.width) * 100;
      set(range.value);
    }
    box.addEventListener("pointerdown", function (e) {
      dragging = true; decided = e.pointerType !== "touch"; startX = e.clientX; startY = e.clientY;
      box.classList.remove("hint");
      if (decided) { fromX(e.clientX); box.setPointerCapture(e.pointerId); e.preventDefault(); range.focus({ preventScroll: true }); }
    });
    box.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      if (!decided) {
        var dx = Math.abs(e.clientX - startX), dy = Math.abs(e.clientY - startY);
        if (dx < 6 && dy < 6) return;
        if (dy > dx) { dragging = false; return; }
        decided = true;
        try { box.setPointerCapture(e.pointerId); } catch (_) {}
      }
      fromX(e.clientX);
    });
    function end() { dragging = false; }
    box.addEventListener("pointerup", end);
    box.addEventListener("pointercancel", end);
    set(range.value);
  });

  // One gentle hint on the hero slider (skipped with reduced motion).
  var hero = document.querySelector(".hero-compare .compare");
  if (hero && !reduce) setTimeout(function () { hero.classList.add("hint"); }, 900);

  // Entrance reveals.
  var items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  // Demonstration form: never submits, sends, uploads or stores anything.
  var form = document.getElementById("demo-form");
  if (form) {
    var previews = form.querySelector(".previews");
    var file = form.querySelector('input[type="file"]');
    var urls = [];
    file.addEventListener("change", function () {
      urls.forEach(URL.revokeObjectURL); urls = []; previews.textContent = "";
      Array.prototype.slice.call(file.files, 0, 6).forEach(function (f) {
        if (!/^image\//.test(f.type)) return;
        var u = URL.createObjectURL(f); urls.push(u);
        var img = document.createElement("img"); img.src = u; img.alt = "Selected photo preview (stays on this device)";
        previews.appendChild(img);
      });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".demo-confirm");
      msg.hidden = false;
      msg.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
    });
  }
})();
