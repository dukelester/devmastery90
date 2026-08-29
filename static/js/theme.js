(function () {
  "use strict";

  var STORAGE_KEY = "dm-theme";

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function resolveTheme(stored) {
    if (stored === "dark" || stored === "light") return stored;
    return systemTheme();
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", theme === "dark" ? "#0b1017" : "#e2e8f0");
    }
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      btn.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
      btn.title = theme === "dark" ? "Light theme" : "Dark theme";
    });
  }

  function getStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (_) {
      return null;
    }
  }

  function setStored(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (_) {
      /* ignore */
    }
  }

  function init() {
    applyTheme(resolveTheme(getStored()));

    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next =
          document.documentElement.getAttribute("data-theme") === "dark"
            ? "light"
            : "dark";
        setStored(next);
        applyTheme(next);
      });
    });

    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
        if (!getStored()) applyTheme(systemTheme());
      });
    }
  }

  // Expose for early boot script consistency
  window.dmTheme = {
    apply: applyTheme,
    resolve: function () {
      return resolveTheme(getStored());
    },
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
