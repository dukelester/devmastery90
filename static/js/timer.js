(function () {
  "use strict";

  function formatTime(totalSeconds) {
    const s = Math.max(0, Math.floor(totalSeconds));
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
  }

  function parseStartedAt(value) {
    if (!value) return null;
    const ms = Date.parse(value);
    return Number.isNaN(ms) ? null : ms;
  }

  function getElapsedSeconds(display) {
    const accumulated = parseInt(display.dataset.accumulatedSeconds || "0", 10);
    const startMs = parseStartedAt(display.dataset.startedAt);
    if (startMs === null) {
      return accumulated;
    }
    return accumulated + (Date.now() - startMs) / 1000;
  }

  function clearTimer(root) {
    if (root && root.dmTimerInterval) {
      clearInterval(root.dmTimerInterval);
      root.dmTimerInterval = null;
    }
  }

  function initTimerDisplay(root) {
    const display = root.querySelector("[data-timer-display]");
    if (!display) return;

    clearTimer(root);

    const mode = display.dataset.timerMode || "elapsed";
    const targetSeconds = parseInt(display.dataset.targetSeconds || "0", 10);
    const startMs = parseStartedAt(display.dataset.startedAt);
    const accumulated = parseInt(display.dataset.accumulatedSeconds || "0", 10);

    if (mode === "elapsed" && startMs === null && accumulated === 0) {
      display.textContent = "00:00";
      return;
    }

    function tick() {
      const elapsed = getElapsedSeconds(display);
      if (mode === "focus" && targetSeconds > 0) {
        const remaining = targetSeconds - elapsed;
        display.textContent = formatTime(remaining);
        display.classList.toggle("is-complete", remaining <= 0);
        const sub = root.querySelector("[data-timer-sub]");
        if (sub) {
          sub.textContent =
            remaining <= 0
              ? "Time's up — finish or stop the session"
              : "remaining";
        }
      } else {
        display.textContent = formatTime(elapsed);
        display.classList.remove("is-complete");
        const sub = root.querySelector("[data-timer-sub]");
        if (sub) {
          sub.textContent = "elapsed";
        }
      }
    }

    tick();
    if (startMs !== null || (mode === "focus" && targetSeconds > 0)) {
      root.dmTimerInterval = setInterval(tick, 1000);
    }
  }

  function scan() {
    document.querySelectorAll("[data-live-timer]").forEach((el) => {
      initTimerDisplay(el);
    });
  }

  document.addEventListener("DOMContentLoaded", scan);
  document.body.addEventListener("htmx:afterSwap", scan);
  document.body.addEventListener("htmx:afterSettle", scan);

  /* ——— Per-question countdown (cognitive / aptitude) ——— */

  function formatCountdown(totalSeconds) {
    const s = Math.max(0, Math.ceil(totalSeconds));
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
  }

  function readCountdownState(key, total) {
    if (!key) return null;
    try {
      const raw = sessionStorage.getItem(key);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data || typeof data.remaining !== "number") return null;
      return data;
    } catch (_) {
      return null;
    }
  }

  function writeCountdownState(key, remaining, paused, endsAt) {
    if (!key) return;
    try {
      sessionStorage.setItem(
        key,
        JSON.stringify({ remaining, paused: !!paused, endsAt: endsAt || null })
      );
    } catch (_) {
      /* ignore quota / private mode */
    }
  }

  function clearCountdownState(key) {
    if (!key) return;
    try {
      sessionStorage.removeItem(key);
    } catch (_) {
      /* ignore */
    }
  }

  function initCountdown(root) {
    if (root.dmCountdownBound) return;
    root.dmCountdownBound = true;

    const total = parseInt(root.dataset.seconds || "60", 10);
    const key = root.dataset.storageKey || "";
    const autoStart = root.dataset.autoStart === "true";
    const display = root.querySelector("[data-countdown-display]");
    const sub = root.querySelector("[data-countdown-sub]");
    const fill = root.querySelector("[data-countdown-fill]");
    const expiredEl = root.querySelector("[data-countdown-expired]");
    const pauseBtn = root.querySelector("[data-countdown-pause]");
    const resetBtn = root.querySelector("[data-countdown-reset]");
    const spentInput = document.querySelector("[data-countdown-spent]");

    if (!display) return;

    let remaining = total;
    let paused = true;
    let endsAt = null;
    let interval = null;

    const saved = readCountdownState(key, total);
    if (saved) {
      remaining = Math.min(total, Math.max(0, saved.remaining));
      paused = saved.paused !== false;
      if (!paused && saved.endsAt) {
        endsAt = saved.endsAt;
        remaining = Math.max(0, (endsAt - Date.now()) / 1000);
      }
    }

    function syncSpent() {
      if (spentInput) {
        spentInput.value = String(Math.max(0, Math.round(total - remaining)));
      }
    }

    function render() {
      display.textContent = formatCountdown(remaining);
      root.classList.toggle("is-warn", remaining > 0 && remaining <= Math.min(15, total * 0.25));
      root.classList.toggle("is-critical", remaining > 0 && remaining <= 10);
      root.classList.toggle("is-expired", remaining <= 0);
      root.classList.toggle("is-paused", paused && remaining > 0);
      if (fill) {
        fill.style.width = Math.max(0, Math.min(100, (remaining / total) * 100)) + "%";
      }
      if (sub) {
        if (remaining <= 0) sub.textContent = "time’s up";
        else if (paused) sub.textContent = "paused";
        else sub.textContent = "remaining";
      }
      if (expiredEl) {
        expiredEl.hidden = remaining > 0;
      }
      if (pauseBtn) {
        pauseBtn.textContent = paused ? "Resume" : "Pause";
        pauseBtn.disabled = remaining <= 0;
      }
      syncSpent();
    }

    function stopInterval() {
      if (interval) {
        clearInterval(interval);
        interval = null;
      }
    }

    function tick() {
      if (paused || remaining <= 0) return;
      remaining = Math.max(0, (endsAt - Date.now()) / 1000);
      writeCountdownState(key, remaining, false, endsAt);
      render();
      if (remaining <= 0) {
        stopInterval();
        paused = true;
        writeCountdownState(key, 0, true, null);
      }
    }

    function start() {
      if (remaining <= 0) return;
      paused = false;
      endsAt = Date.now() + remaining * 1000;
      writeCountdownState(key, remaining, false, endsAt);
      stopInterval();
      interval = setInterval(tick, 200);
      render();
    }

    function pause() {
      if (paused || remaining <= 0) return;
      remaining = Math.max(0, (endsAt - Date.now()) / 1000);
      paused = true;
      endsAt = null;
      stopInterval();
      writeCountdownState(key, remaining, true, null);
      render();
    }

    function reset() {
      stopInterval();
      remaining = total;
      paused = true;
      endsAt = null;
      clearCountdownState(key);
      render();
      if (autoStart) start();
    }

    function togglePause() {
      if (remaining <= 0) return;
      if (paused) start();
      else pause();
    }

    if (pauseBtn) pauseBtn.addEventListener("click", togglePause);
    if (resetBtn) resetBtn.addEventListener("click", reset);

    root.dmCountdownStop = function () {
      pause();
      clearCountdownState(key);
    };

    const form = document.querySelector("[data-countdown-form]");
    if (form) {
      form.addEventListener("htmx:configRequest", syncSpent);
      form.addEventListener("submit", syncSpent);
    }

    document.body.addEventListener("htmx:afterSwap", function (e) {
      if (e.target && e.target.id === "cognitive-answer-area") {
        if (root.dmCountdownStop) root.dmCountdownStop();
        root.classList.add("is-done");
      }
    });

    render();
    if (!paused && remaining > 0) start();
    else if (autoStart && remaining > 0 && !saved) start();
    else if (autoStart && remaining > 0 && saved && !saved.paused) start();
  }

  function scanCountdowns() {
    document.querySelectorAll("[data-countdown]").forEach(initCountdown);
  }

  document.addEventListener("DOMContentLoaded", scanCountdowns);
  document.body.addEventListener("htmx:afterSwap", scanCountdowns);
})();
