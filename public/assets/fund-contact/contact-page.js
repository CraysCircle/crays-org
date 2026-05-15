(function () {
  const toggle = document.querySelector(".contact-menu-toggle");
  const nav = document.querySelector(".contact-nav");
  const copyButton = document.querySelector(".contact-copy-button");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = document.body.classList.toggle("contact-nav-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        document.body.classList.remove("contact-nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  if (!copyButton) {
    return;
  }

  copyButton.addEventListener("click", async () => {
    const value = copyButton.dataset.copy || "";
    const originalLabel = copyButton.textContent;

    try {
      await navigator.clipboard.writeText(value);
      copyButton.textContent = "Copied";
    } catch (error) {
      copyButton.textContent = value;
    }

    window.setTimeout(() => {
      copyButton.textContent = originalLabel;
    }, 1800);
  });
})();
