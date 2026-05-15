(function () {
  const STORAGE_KEY = "crays_cookie_consent";
  const COOKIE_NAME = "crays_cookie_consent";
  const VERSION = 1;
  const LANGS = ["en", "de", "es", "ca", "fr", "pt", "it"];
  const OPTIONAL = ["preferences", "analytics", "marketing"];

  const copy = {
    en: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "We use strictly necessary cookies to run this website. With your consent, we may also use preferences, analytics and marketing technologies to improve the site and measure campaigns.",
      reject: "Reject optional",
      settings: "Privacy & Cookie Settings",
      accept: "Accept all",
      save: "Save settings",
      close: "Close",
      privacy: "Privacy Policy",
      data: "Data Protection",
      necessaryTitle: "Strictly necessary",
      necessaryText: "Required for security, page routing, language handling and storing your consent choice. These cannot be switched off.",
      preferencesTitle: "Preferences",
      preferencesText: "Remembers interface choices such as language and display preferences.",
      analyticsTitle: "Analytics",
      analyticsText: "Helps us understand site performance and errors without selling your data.",
      marketingTitle: "Marketing",
      marketingText: "Allows campaign measurement, embedded marketing tools and similar optional technologies.",
      footer: "Cookie Settings",
    },
    de: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Wir nutzen notwendige Cookies, damit diese Website funktioniert. Mit Ihrer Zustimmung nutzen wir zusätzlich Preferences, Analytics und Marketing-Technologien zur Optimierung und Kampagnenmessung.",
      reject: "Optionale ablehnen",
      settings: "Privacy & Cookie Settings",
      accept: "Alle akzeptieren",
      save: "Einstellungen speichern",
      close: "Schließen",
      privacy: "Privacy Policy",
      data: "Datenschutz",
      necessaryTitle: "Notwendig",
      necessaryText: "Erforderlich für Sicherheit, Routing, Sprachfunktion und Speicherung Ihrer Consent-Auswahl. Diese Kategorie kann nicht deaktiviert werden.",
      preferencesTitle: "Preferences",
      preferencesText: "Speichert Interface-Entscheidungen wie Sprache und Anzeigeoptionen.",
      analyticsTitle: "Analytics",
      analyticsText: "Hilft uns, Performance und Fehler der Website zu verstehen, ohne Ihre Daten zu verkaufen.",
      marketingTitle: "Marketing",
      marketingText: "Erlaubt Kampagnenmessung, eingebettete Marketing-Tools und ähnliche optionale Technologien.",
      footer: "Cookie Settings",
    },
    es: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Usamos cookies estrictamente necesarias para que la web funcione. Con su consentimiento también podemos usar preferencias, analytics y tecnologías de marketing para mejorar la página y medir campañas.",
      reject: "Rechazar opcionales",
      settings: "Privacy & Cookie Settings",
      accept: "Aceptar todo",
      save: "Guardar ajustes",
      close: "Cerrar",
      privacy: "Privacy Policy",
      data: "Protección de datos",
      necessaryTitle: "Estrictamente necesarias",
      necessaryText: "Necesarias para seguridad, rutas, idioma y guardar su elección de consentimiento. No se pueden desactivar.",
      preferencesTitle: "Preferencias",
      preferencesText: "Recuerda opciones de interfaz como idioma y preferencias de visualización.",
      analyticsTitle: "Analytics",
      analyticsText: "Nos ayuda a entender el rendimiento y los errores de la web sin vender sus datos.",
      marketingTitle: "Marketing",
      marketingText: "Permite medir campañas, herramientas de marketing integradas y tecnologías opcionales similares.",
      footer: "Cookie Settings",
    },
    ca: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Fem servir cookies estrictament necessàries perquè el web funcioni. Amb el vostre consentiment també podem utilitzar preferences, analytics i tecnologies de marketing per millorar la pàgina i mesurar campanyes.",
      reject: "Rebutjar opcionals",
      settings: "Privacy & Cookie Settings",
      accept: "Acceptar-ho tot",
      save: "Desar ajustos",
      close: "Tancar",
      privacy: "Privacy Policy",
      data: "Protecció de dades",
      necessaryTitle: "Estrictament necessàries",
      necessaryText: "Necessàries per a seguretat, rutes, idioma i guardar la vostra elecció de consentiment. No es poden desactivar.",
      preferencesTitle: "Preferències",
      preferencesText: "Recorda opcions d'interfície com l'idioma i preferències de visualització.",
      analyticsTitle: "Analytics",
      analyticsText: "Ens ajuda a entendre rendiment i errors del web sense vendre les vostres dades.",
      marketingTitle: "Marketing",
      marketingText: "Permet mesurar campanyes, eines de marketing integrades i tecnologies opcionals similars.",
      footer: "Cookie Settings",
    },
    fr: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Nous utilisons des cookies strictement nécessaires au fonctionnement du site. Avec votre accord, nous pouvons aussi utiliser preferences, analytics et technologies marketing pour améliorer le site et mesurer les campagnes.",
      reject: "Refuser l'optionnel",
      settings: "Privacy & Cookie Settings",
      accept: "Tout accepter",
      save: "Enregistrer",
      close: "Fermer",
      privacy: "Privacy Policy",
      data: "Protection des données",
      necessaryTitle: "Strictement nécessaires",
      necessaryText: "Nécessaires pour la sécurité, le routage, la langue et l'enregistrement de votre choix de consentement. Ils ne peuvent pas être désactivés.",
      preferencesTitle: "Préférences",
      preferencesText: "Mémorise les choix d'interface comme la langue et les préférences d'affichage.",
      analyticsTitle: "Analytics",
      analyticsText: "Nous aide à comprendre la performance et les erreurs du site sans vendre vos données.",
      marketingTitle: "Marketing",
      marketingText: "Permet la mesure des campagnes, les outils marketing intégrés et technologies optionnelles similaires.",
      footer: "Cookie Settings",
    },
    pt: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Usamos cookies estritamente necessários para o site funcionar. Com o seu consentimento, também podemos usar preferências, analytics e tecnologias de marketing para melhorar a página e medir campanhas.",
      reject: "Rejeitar opcionais",
      settings: "Privacy & Cookie Settings",
      accept: "Aceitar tudo",
      save: "Guardar definições",
      close: "Fechar",
      privacy: "Privacy Policy",
      data: "Proteção de dados",
      necessaryTitle: "Estritamente necessários",
      necessaryText: "Necessários para segurança, rotas, idioma e guardar a sua escolha de consentimento. Não podem ser desativados.",
      preferencesTitle: "Preferências",
      preferencesText: "Recorda escolhas de interface como idioma e preferências de visualização.",
      analyticsTitle: "Analytics",
      analyticsText: "Ajuda-nos a entender desempenho e erros do site sem vender os seus dados.",
      marketingTitle: "Marketing",
      marketingText: "Permite medir campanhas, ferramentas de marketing integradas e tecnologias opcionais semelhantes.",
      footer: "Cookie Settings",
    },
    it: {
      eyebrow: "Cookie Consent",
      title: "Privacy & Cookie Settings",
      intro: "Usiamo cookie strettamente necessari per far funzionare il sito. Con il suo consenso possiamo usare anche preferenze, analytics e tecnologie marketing per migliorare la pagina e misurare le campagne.",
      reject: "Rifiuta opzionali",
      settings: "Privacy & Cookie Settings",
      accept: "Accetta tutto",
      save: "Salva impostazioni",
      close: "Chiudi",
      privacy: "Privacy Policy",
      data: "Protezione dati",
      necessaryTitle: "Strettamente necessari",
      necessaryText: "Necessari per sicurezza, routing, lingua e salvataggio della scelta di consenso. Non possono essere disattivati.",
      preferencesTitle: "Preferenze",
      preferencesText: "Ricorda scelte di interfaccia come lingua e preferenze di visualizzazione.",
      analyticsTitle: "Analytics",
      analyticsText: "Ci aiuta a capire performance ed errori del sito senza vendere i suoi dati.",
      marketingTitle: "Marketing",
      marketingText: "Consente misurazione campagne, strumenti marketing integrati e tecnologie opzionali simili.",
      footer: "Cookie Settings",
    },
  };

  let state = null;
  let elements = {};

  function pathLang() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    const offset = parts[0] === "crays-website" ? 1 : 0;
    return LANGS.includes(parts[offset]) ? parts[offset] : "";
  }

  function lang() {
    const active = document.documentElement.dataset.craysActiveLang || document.documentElement.lang || pathLang();
    return LANGS.includes(active) ? active : "en";
  }

  function text(key) {
    const current = copy[lang()] || copy.en;
    return current[key] || copy.en[key] || "";
  }

  function cookieValue() {
    const match = document.cookie.match(new RegExp(`(?:^|; )${COOKIE_NAME}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : "";
  }

  function readConsent() {
    const raw = window.localStorage.getItem(STORAGE_KEY) || cookieValue();
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw);
      return parsed && parsed.version === VERSION ? parsed : null;
    } catch (error) {
      return null;
    }
  }

  function writeConsent(next) {
    const payload = JSON.stringify(next);
    window.localStorage.setItem(STORAGE_KEY, payload);
    document.cookie = `${COOKIE_NAME}=${encodeURIComponent(payload)}; Max-Age=15552000; Path=/; SameSite=Lax; Secure`;
  }

  function decision(allOptional) {
    const value = {
      version: VERSION,
      updatedAt: new Date().toISOString(),
      necessary: true,
      preferences: !!allOptional,
      analytics: !!allOptional,
      marketing: !!allOptional,
    };
    return value;
  }

  function currentFromSwitches() {
    const next = decision(false);
    OPTIONAL.forEach((category) => {
      next[category] = elements.switches[category]?.getAttribute("aria-checked") === "true";
    });
    return next;
  }

  function applySwitches(next) {
    OPTIONAL.forEach((category) => {
      const on = !!next[category];
      elements.switches[category]?.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function emitConsent(next) {
    window.CRAYS_COOKIE_CONSENT = Object.freeze({ ...next });
    document.dispatchEvent(new CustomEvent("crays:consentchange", { detail: { consent: { ...next } } }));
  }

  function activateConsentedScripts(next) {
    document.querySelectorAll('script[type="text/plain"][data-crays-consent-category]').forEach((script) => {
      const category = script.getAttribute("data-crays-consent-category");
      if (!next[category] || script.dataset.craysConsentActivated === "true") return;
      const replacement = document.createElement("script");
      [...script.attributes].forEach((attr) => {
        if (attr.name === "type" || attr.name === "data-crays-consent-category") return;
        replacement.setAttribute(attr.name, attr.value);
      });
      replacement.type = "text/javascript";
      replacement.text = script.textContent;
      script.dataset.craysConsentActivated = "true";
      script.after(replacement);
    });
  }

  function setConsent(next) {
    state = next;
    writeConsent(next);
    emitConsent(next);
    activateConsentedScripts(next);
    hideBanner();
    hideDialog();
  }

  function showBanner() {
    elements.root.hidden = false;
  }

  function hideBanner() {
    elements.root.hidden = true;
  }

  function showDialog() {
    applySwitches(state || decision(false));
    elements.backdrop.hidden = false;
    elements.dialog.hidden = false;
    elements.dialog.querySelector(".crays-consent-close")?.focus();
  }

  function hideDialog() {
    elements.backdrop.hidden = true;
    elements.dialog.hidden = true;
  }

  function toggleSwitch(button) {
    if (button.getAttribute("aria-disabled") === "true") return;
    button.setAttribute("aria-checked", button.getAttribute("aria-checked") === "true" ? "false" : "true");
  }

  function legalHref(doc) {
    const local = window.location.pathname.includes("/crays-website/");
    if (local) return `/crays-website/legal/${doc}.html`;
    return `/${lang()}/legal/${doc}`;
  }

  function render() {
    const root = document.createElement("div");
    root.className = "crays-consent-root";
    root.hidden = true;
    root.innerHTML = `
      <section class="crays-consent-panel" role="region" aria-labelledby="crays-consent-title">
        <p class="crays-consent-eyebrow" data-crays-consent-text="eyebrow"></p>
        <h2 class="crays-consent-title" id="crays-consent-title" data-crays-consent-text="title"></h2>
        <p class="crays-consent-copy" data-crays-consent-text="intro"></p>
        <div class="crays-consent-actions">
          <button class="crays-consent-button crays-consent-button-reject" type="button" data-crays-consent-action="reject" data-crays-consent-text="reject"></button>
          <button class="crays-consent-button crays-consent-button-text" type="button" data-crays-consent-action="settings" data-crays-consent-text="settings"></button>
          <button class="crays-consent-button crays-consent-button-primary" type="button" data-crays-consent-action="accept" data-crays-consent-text="accept"></button>
        </div>
        <div class="crays-consent-links">
          <a href="${legalHref("privacy-policy")}" data-crays-consent-legal="privacy-policy" data-crays-consent-text="privacy"></a>
          <a href="${legalHref("data-protection")}" data-crays-consent-legal="data-protection" data-crays-consent-text="data"></a>
        </div>
      </section>
    `;

    const backdrop = document.createElement("div");
    backdrop.className = "crays-consent-backdrop";
    backdrop.hidden = true;

    const dialog = document.createElement("section");
    dialog.className = "crays-consent-dialog";
    dialog.hidden = true;
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "crays-consent-dialog-title");
    dialog.innerHTML = `
      <div class="crays-consent-dialog-head">
        <div>
          <p class="crays-consent-eyebrow" data-crays-consent-text="eyebrow"></p>
          <h2 class="crays-consent-title" id="crays-consent-dialog-title" data-crays-consent-text="title"></h2>
          <p class="crays-consent-copy" data-crays-consent-text="intro"></p>
        </div>
        <button class="crays-consent-button crays-consent-close" type="button" data-crays-consent-action="close" data-crays-consent-aria="close" aria-label="Close">&times;</button>
      </div>
      <div class="crays-consent-categories">
        <article class="crays-consent-category">
          <div><h3 data-crays-consent-text="necessaryTitle"></h3><p data-crays-consent-text="necessaryText"></p></div>
          <button class="crays-consent-switch" type="button" role="switch" aria-checked="true" aria-disabled="true" tabindex="-1" data-crays-consent-aria="necessaryTitle"></button>
        </article>
        <article class="crays-consent-category">
          <div><h3 data-crays-consent-text="preferencesTitle"></h3><p data-crays-consent-text="preferencesText"></p></div>
          <button class="crays-consent-switch" type="button" role="switch" aria-checked="false" data-crays-consent-switch="preferences" data-crays-consent-aria="preferencesTitle"></button>
        </article>
        <article class="crays-consent-category">
          <div><h3 data-crays-consent-text="analyticsTitle"></h3><p data-crays-consent-text="analyticsText"></p></div>
          <button class="crays-consent-switch" type="button" role="switch" aria-checked="false" data-crays-consent-switch="analytics" data-crays-consent-aria="analyticsTitle"></button>
        </article>
        <article class="crays-consent-category">
          <div><h3 data-crays-consent-text="marketingTitle"></h3><p data-crays-consent-text="marketingText"></p></div>
          <button class="crays-consent-switch" type="button" role="switch" aria-checked="false" data-crays-consent-switch="marketing" data-crays-consent-aria="marketingTitle"></button>
        </article>
      </div>
      <div class="crays-consent-actions">
        <button class="crays-consent-button crays-consent-button-reject" type="button" data-crays-consent-action="reject" data-crays-consent-text="reject"></button>
        <button class="crays-consent-button" type="button" data-crays-consent-action="save" data-crays-consent-text="save"></button>
        <button class="crays-consent-button crays-consent-button-primary" type="button" data-crays-consent-action="accept" data-crays-consent-text="accept"></button>
      </div>
    `;

    document.body.append(backdrop, root, dialog);
    elements = {
      root,
      backdrop,
      dialog,
      switches: Object.fromEntries(
        [...dialog.querySelectorAll("[data-crays-consent-switch]")].map((button) => [button.dataset.craysConsentSwitch, button])
      ),
    };
    translate();
  }

  function translate() {
    document.querySelectorAll("[data-crays-consent-text]").forEach((node) => {
      node.textContent = text(node.dataset.craysConsentText);
    });
    document.querySelectorAll("[data-crays-consent-aria]").forEach((node) => {
      node.setAttribute("aria-label", text(node.dataset.craysConsentAria));
    });
    document.querySelectorAll("[data-crays-consent-legal]").forEach((node) => {
      node.setAttribute("href", legalHref(node.dataset.craysConsentLegal));
    });
  }

  function installFooterControl() {
    if (document.querySelector("[data-crays-consent-open]")) return;
    const button = document.createElement("button");
    button.className = "crays-consent-footer-button";
    button.type = "button";
    button.dataset.craysConsentOpen = "true";
    button.textContent = text("footer");
    const slot = document.createElement("span");
    slot.className = "crays-consent-footer-slot";
    slot.appendChild(button);
    const footerCredit = document.querySelector(
      ".footer3_credit-text, .resources-footer-credit, .strategy-footer-credit, .ecosystem-footer-credit, .company-footer-credit, .upreit-footer-credit, .contact-footer-credit, .association-footer-credit, .legal-footer-copy"
    );

    if (footerCredit) {
      footerCredit.insertAdjacentElement("afterend", slot);
    } else if (document.querySelector("footer")) {
      document.querySelector("footer").appendChild(slot);
    } else {
      document.body.appendChild(slot);
    }
  }

  function bind() {
    document.addEventListener("click", (event) => {
      const action = event.target.closest("[data-crays-consent-action]")?.dataset.craysConsentAction;
      if (action === "reject") setConsent(decision(false));
      if (action === "accept") setConsent(decision(true));
      if (action === "settings") showDialog();
      if (action === "save") setConsent(currentFromSwitches());
      if (action === "close") hideDialog();

      const switchButton = event.target.closest("[data-crays-consent-switch]");
      if (switchButton) toggleSwitch(switchButton);

      if (event.target.closest("[data-crays-consent-open]")) {
        showDialog();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") hideDialog();
    });

    document.addEventListener("crays:languagechange", () => {
      translate();
      document.querySelector("[data-crays-consent-open]")?.replaceChildren(document.createTextNode(text("footer")));
    });
  }

  function init() {
    render();
    installFooterControl();
    bind();
    state = readConsent();
    if (state) {
      emitConsent(state);
      activateConsentedScripts(state);
    } else {
      showBanner();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
