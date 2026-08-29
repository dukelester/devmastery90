(function () {
  "use strict";

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

    function setOpen(open) {
    var shell = document.body;
    if (!shell) return;
    shell.classList.toggle("dm-nav-open", open);
    qsa("[data-nav-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    var drawer = qs("[data-nav-drawer]");
    if (drawer) {
      drawer.setAttribute("aria-hidden", open ? "false" : "true");
    }
    var backdrop = qs(".dm-nav-backdrop");
    if (backdrop) {
      backdrop.setAttribute("aria-hidden", open ? "false" : "true");
    }
    if (open) {
      document.documentElement.style.overflow = "hidden";
    } else {
      document.documentElement.style.overflow = "";
    }
  }

  function toggle() {
    setOpen(!document.body.classList.contains("dm-nav-open"));
  }

  function close() {
    setOpen(false);
  }

  function init() {
    qsa("[data-nav-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        toggle();
      });
    });

    qsa("[data-nav-close]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        close();
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });

    // Close drawer after navigating (helps HTMX / same-page anchors)
    qsa("[data-nav-drawer] a").forEach(function (a) {
      a.addEventListener("click", function () {
        close();
      });
    });

    // Close More menus when clicking outside
    document.addEventListener("click", function (e) {
      qsa(".dm-nav-more[open]").forEach(function (el) {
        if (!el.contains(e.target)) el.removeAttribute("open");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
