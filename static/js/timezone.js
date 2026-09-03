/**
 * Detect browser timezone and sync to the server when auto mode is on.
 * Falls back to Africa/Nairobi when detection is unavailable.
 */
(function () {
  var DEFAULT_TZ = "Africa/Nairobi";

  function detectTimezone() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (tz && typeof tz === "string") return tz;
    } catch (e) {}
    return DEFAULT_TZ;
  }

  function csrfToken() {
    var input = document.querySelector("[name=csrfmiddlewaretoken]");
    if (input && input.value) return input.value;
    var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function fillSelects(tz) {
    document.querySelectorAll('select[name="timezone"]').forEach(function (select) {
      var option = Array.prototype.find.call(select.options, function (o) {
        return o.value === tz;
      });
      if (option) {
        select.value = tz;
      } else if (!select.value) {
        select.value = DEFAULT_TZ;
      }
    });
  }

  function syncToServer(tz, auto) {
    if (!auto) {
      fillSelects(tz);
      return;
    }
    var url = document.body.getAttribute("data-timezone-sync-url");
    if (!url) {
      fillSelects(tz);
      return;
    }
    var stored = document.body.getAttribute("data-timezone") || "";
    if (stored === tz) {
      fillSelects(tz);
      return;
    }
    var body = new URLSearchParams();
    body.set("timezone", tz);
    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken(),
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: body.toString(),
      credentials: "same-origin",
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data && data.timezone) {
          document.body.setAttribute("data-timezone", data.timezone);
          fillSelects(data.timezone);
        } else {
          fillSelects(tz);
        }
      })
      .catch(function () {
        fillSelects(tz);
      });
  }

  function init() {
    var body = document.body;
    if (!body || body.getAttribute("data-user-authenticated") !== "1") return;
    var auto = body.getAttribute("data-timezone-auto") !== "0";
    var detected = detectTimezone();
    syncToServer(detected, auto);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
