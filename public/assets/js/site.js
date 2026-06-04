const toggle = document.querySelector(".nav-toggle");

if (toggle) {
  toggle.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll(".w-nav-button").forEach((button) => {
  button.addEventListener("click", () => {
    const nav = button.closest(".w-nav");
    const menu = nav ? nav.querySelector(".w-nav-menu") : null;
    const isOpen = button.classList.toggle("w--open");
    if (menu) {
      menu.classList.toggle("w--open", isOpen);
      menu.style.display = isOpen ? "block" : "";
    }
    button.setAttribute("aria-expanded", String(isOpen));
  });
});

document.querySelectorAll(".w-dropdown-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const dropdown = button.closest(".w-dropdown");
    const list = dropdown ? dropdown.querySelector(".w-dropdown-list") : null;
    const isOpen = button.classList.toggle("w--open");
    if (list) {
      list.classList.toggle("w--open", isOpen);
      list.style.display = isOpen ? "block" : "";
    }
    button.setAttribute("aria-expanded", String(isOpen));
  });
});

const craysLanguageItems = [
  {
    code: "en",
    label: "English",
    flag: '<img src="/assets/brand/flag-en.svg" alt="" class="crays-top-nav-language-flag" width="60" height="40" loading="lazy">',
    active: true,
  },
  {
    code: "de",
    label: "Deutsch",
    flag: '<img src="/assets/brand/flag-de.svg" alt="" class="crays-top-nav-language-flag" width="60" height="40" loading="lazy">',
  },
  {
    code: "es",
    label: "Espa&ntilde;ol",
    flag: '<img src="/assets/brand/flag-es.svg" alt="" class="crays-top-nav-language-flag" width="60" height="40" loading="lazy">',
  },
  {
    code: "ca",
    label: "Catal&agrave;",
    flag: '<span class="crays-top-nav-language-flag crays-top-nav-language-flag--css crays-top-nav-language-flag--ca" aria-hidden="true"></span>',
  },
  {
    code: "fr",
    label: "Fran&ccedil;ais",
    flag: '<span class="crays-top-nav-language-flag crays-top-nav-language-flag--css crays-top-nav-language-flag--fr" aria-hidden="true"></span>',
  },
  {
    code: "pt",
    label: "Portugu&ecirc;s",
    flag: '<span class="crays-top-nav-language-flag crays-top-nav-language-flag--css crays-top-nav-language-flag--pt" aria-hidden="true"></span>',
  },
  {
    code: "it",
    label: "Italiano",
    flag: '<span class="crays-top-nav-language-flag crays-top-nav-language-flag--css crays-top-nav-language-flag--it" aria-hidden="true"></span>',
  },
];

const craysLocalizedRoutes = new Set([
  "",
  "association",
  "team",
  "tech",
  "finance",
  "lifestyle",
  "hospitality",
  "real-estate",
  "contact",
  "join-us",
]);

const craysLanguageCodes = new Set(craysLanguageItems.map((item) => item.code));

function craysCurrentRoute() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  const activeLanguage = craysLanguageCodes.has(parts[0]) ? parts[0] : "en";
  const routeParts = craysLanguageCodes.has(parts[0]) ? parts.slice(1) : parts;
  const route = routeParts.join("/");
  return {
    activeLanguage,
    route: craysLocalizedRoutes.has(route) ? route : "",
  };
}

function craysLocalizedHref(code, route) {
  const suffix = route ? `${route}/` : "";
  return `/${code}/${suffix}${window.location.hash || ""}`;
}

document.querySelectorAll(".crays-top-nav-language-menu").forEach((menu) => {
  const current = craysCurrentRoute();
  menu.innerHTML = craysLanguageItems
    .map((item) => {
      const active = item.code === current.activeLanguage;
      return `<a class="crays-top-nav-language-item" href="${craysLocalizedHref(item.code, current.route)}" data-lang="${item.code}" hreflang="${item.code}" lang="${item.code}" aria-pressed="${active ? "true" : "false"}">${item.flag}<span>${item.label}</span></a>`;
    })
    .join("");
});

const clock = document.getElementById("js-clock");

if (clock) {
  const target = new Date("2026-09-01T00:00:00+02:00").getTime();
  const parts = {
    days: document.getElementById("days"),
    hours: document.getElementById("hours"),
    minutes: document.getElementById("minutes"),
    seconds: document.getElementById("seconds"),
  };

  const writePart = (key, value) => {
    if (parts[key]) {
      parts[key].textContent = String(value).padStart(2, "0");
    }
  };

  const updateClock = () => {
    const remaining = Math.max(0, target - Date.now());
    const totalSeconds = Math.floor(remaining / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    writePart("days", days);
    writePart("hours", hours);
    writePart("minutes", minutes);
    writePart("seconds", seconds);
  };

  updateClock();
  window.setInterval(updateClock, 1000);
}

function craysInitNostrVideoCards() {
  document.querySelectorAll(".crays-nostr-video-card").forEach((card) => {
    const video = card.querySelector("video");
    if (!video) return;

    const markIdle = () => card.classList.remove("is-playing");
    const markPlaying = () => {
      video.muted = false;
      card.classList.add("is-playing");
    };

    video.addEventListener("pointerdown", () => {
      video.muted = false;
    });
    video.addEventListener("play", markPlaying);
    video.addEventListener("pause", markIdle);
    video.addEventListener("ended", markIdle);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", craysInitNostrVideoCards);
} else {
  craysInitNostrVideoCards();
}
