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
