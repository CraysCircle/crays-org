import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";

const ROOT = process.cwd();
const PUBLIC_DIR = path.join(ROOT, "public");
const CACHE_FILE = path.join(ROOT, "scripts", "translation-cache.json");
const SITE_ORIGIN = "https://www.crays.org";
const SEP = "\n###CRAYS_I18N_SEPARATOR###\n";

const pages = [
  { key: "home", slug: "", file: "index.html", priority: "1.0", changefreq: "weekly" },
  { key: "association", slug: "association", file: "association/index.html", priority: "0.9", changefreq: "monthly" },
  { key: "team", slug: "team", file: "team/index.html", priority: "0.8", changefreq: "monthly" },
  { key: "tech", slug: "tech", file: "tech/index.html", priority: "0.9", changefreq: "monthly" },
  { key: "finance", slug: "finance", file: "finance/index.html", priority: "0.9", changefreq: "monthly" },
  { key: "lifestyle", slug: "lifestyle", file: "lifestyle/index.html", priority: "0.85", changefreq: "monthly" },
  { key: "hospitality", slug: "hospitality", file: "hospitality/index.html", priority: "0.9", changefreq: "monthly" },
  { key: "real-estate", slug: "real-estate", file: "real-estate/index.html", priority: "0.85", changefreq: "monthly" },
  { key: "contact", slug: "contact", file: "contact/index.html", priority: "0.75", changefreq: "monthly" },
  { key: "join-us", slug: "join-us", file: "join-us/index.html", priority: "0.85", changefreq: "monthly" },
];

const languages = {
  en: { label: "English", html: "en", locale: "en_US", google: "en" },
  de: { label: "Deutsch", html: "de", locale: "de_DE", google: "de" },
  es: { label: "Español", html: "es", locale: "es_ES", google: "es" },
  ca: { label: "Català", html: "ca", locale: "ca_ES", google: "ca" },
  fr: { label: "Français", html: "fr", locale: "fr_FR", google: "fr" },
  pt: { label: "Português", html: "pt", locale: "pt_PT", google: "pt" },
  it: { label: "Italiano", html: "it", locale: "it_IT", google: "it" },
};

const protectedTerms = [
  "Crays Business Nomads Club Association",
  "Crays Business Nomads Association",
  "Crays Mercedes Island",
  "Crays Association",
  "Crays Circle",
  "Crays Clubs",
  "Crays Coffee Shops",
  "Crays Coffee",
  "Crays Fund",
  "Crays Coin",
  "Crays",
  "OpenClaw",
  "Nostr",
  "Bitcoin",
  "Lightning",
  "Web5",
  "Web3",
  "DAO",
  "RWA",
  "RGB",
  "AI",
  "CRM",
  "POS",
  "PMS",
  "ARR",
  "MRR",
  "HNWIs",
  "HNW",
  "F&B",
  "Work, Live & Play",
  "WORK / LIVE / PLAY",
  "Brand-as-a-Service",
  "Super Nodes",
  "Super Node",
  "Palma de Mallorca",
  "Palma",
  "Mallorca",
  "Dubai",
  "Cyprus",
  "Luxembourg",
  "Los Angeles",
  "Zug",
  "Singapore",
  "Miami",
  "Cayman",
  "London",
  "Medellín",
  "Aethos",
  "AiFi",
  "BMW",
  "KPMG",
  "SIGNA",
  "OneSafe",
  "Transfero",
  "Credit Suisse",
  "Goldman Sachs",
  "CitizenM",
  "Moda Living",
  "Phoenix Group Dubai",
];

const manual = {
  de: {
    "Association": "Association",
    "Team": "Team",
    "Tech": "Tech",
    "Finance": "Finance",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Kontakt",
    "Join us": "Mitmachen",
    "Choose language": "Sprache wählen",
    "Language selector": "Sprachauswahl",
    "Explore": "Explore",
    "Open": "Öffnen",
    "Read more": "Weiterlesen",
    "Close": "Schließen",
    "Days": "Tage",
    "Hrs": "Std",
    "Min": "Min",
    "Sec": "Sek",
    "A global": "Eine globale",
    "Community": "Community",
    "of Builders & Makers": "für Builders & Makers",
    "Build Your Global Home": "Build Your Global Home",
    "Don’t predict the future. Let’s go out and build it together!": "Nicht die Zukunft vorhersagen. Rausgehen und gemeinsam bauen.",
    "Action is the foundational key to all success.": "Handeln ist die Grundlage für jeden Erfolg.",
    "Funding the Crays ecosystem.": "Funding für das Crays Ecosystem.",
    "Monetization framework": "Monetization Framework",
    "Funding vehicles": "Funding Vehicles",
    "for a": "für ein",
    "global life.": "globales Leben.",
    "The shared technology layer for every official Crays ecosystem project.": "Die gemeinsame Tech-Layer für jedes offizielle Crays Ecosystem Project.",
    "Real estate becomes a platform": "Real Estate wird zur Plattform",
    "when place, demand and capital": "wenn Ort, Nachfrage und Kapital",
    "operate together.": "zusammenwirken.",
    "Bring a real project into Crays.": "Bring ein echtes Projekt zu Crays.",
    "Contact Crays Directly": "Crays direkt kontaktieren",
    "Cookie Settings": "Cookie-Einstellungen",
    "Cookie Consent": "Cookie-Zustimmung",
    "Privacy & Cookie Settings": "Privacy & Cookie Settings",
    "Reject optional": "Optionale ablehnen",
    "Accept all": "Alle akzeptieren",
    "Privacy Policy": "Privacy Policy",
    "Data Protection": "Data Protection",
    "Imprint": "Impressum",
    "Terms and Conditions": "Terms and Conditions",
  },
  es: {
    "Association": "Asociación",
    "Team": "Equipo",
    "Tech": "Tech",
    "Finance": "Finanzas",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Contacto",
    "Join us": "Únete",
    "Choose language": "Elegir idioma",
    "Language selector": "Selector de idioma",
    "Explore": "Explorar",
    "Open": "Abrir",
    "Read more": "Leer más",
    "Close": "Cerrar",
    "Days": "Días",
    "Hrs": "Hrs",
    "Min": "Min",
    "Sec": "Seg",
    "A global": "Una comunidad",
    "Community": "global",
    "of Builders & Makers": "de Builders & Makers",
    "Build Your Global Home": "Construye tu hogar global",
    "Don’t predict the future. Let’s go out and build it together!": "No predigas el futuro. Salgamos a construirlo juntos.",
    "Action is the foundational key to all success.": "La acción es la base de todo éxito.",
    "Funding the Crays ecosystem.": "Financiando el ecosistema Crays.",
    "Monetization framework": "Marco de monetización",
    "Funding vehicles": "Vehículos de funding",
    "for a": "para una",
    "global life.": "vida global.",
    "The shared technology layer for every official Crays ecosystem project.": "La capa tecnológica compartida para cada proyecto oficial del ecosistema Crays.",
    "Real estate becomes a platform": "El real estate se convierte en plataforma",
    "when place, demand and capital": "cuando lugar, demanda y capital",
    "operate together.": "trabajan juntos.",
    "Bring a real project into Crays.": "Trae un proyecto real a Crays.",
    "Contact Crays Directly": "Contacta directamente con Crays",
    "Cookie Settings": "Ajustes de cookies",
    "Cookie Consent": "Consentimiento de cookies",
    "Privacy & Cookie Settings": "Privacidad y cookies",
    "Reject optional": "Rechazar opcionales",
    "Accept all": "Aceptar todo",
  },
  ca: {
    "Association": "Associació",
    "Team": "Equip",
    "Tech": "Tech",
    "Finance": "Finances",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Contacte",
    "Join us": "Uneix-te",
    "Choose language": "Tria idioma",
    "Language selector": "Selector d'idioma",
    "Explore": "Explora",
    "Open": "Obre",
    "Read more": "Llegeix més",
    "Close": "Tanca",
    "Days": "Dies",
    "Hrs": "H",
    "Min": "Min",
    "Sec": "Seg",
    "A global": "Una comunitat",
    "Community": "global",
    "of Builders & Makers": "de Builders & Makers",
    "Build Your Global Home": "Construeix la teva llar global",
    "Don’t predict the future. Let’s go out and build it together!": "No prediguem el futur. Sortim a construir-lo junts.",
    "Action is the foundational key to all success.": "L'acció és la base de qualsevol èxit.",
    "Funding the Crays ecosystem.": "Finançant l'ecosistema Crays.",
    "Monetization framework": "Marc de monetització",
    "Funding vehicles": "Vehicles de funding",
    "for a": "per a una",
    "global life.": "vida global.",
    "The shared technology layer for every official Crays ecosystem project.": "La capa tecnològica compartida per a cada projecte oficial de l'ecosistema Crays.",
    "Real estate becomes a platform": "El real estate es converteix en plataforma",
    "when place, demand and capital": "quan lloc, demanda i capital",
    "operate together.": "treballen junts.",
    "Bring a real project into Crays.": "Porta un projecte real a Crays.",
    "Contact Crays Directly": "Contacta directament amb Crays",
    "Cookie Settings": "Configuració de cookies",
    "Cookie Consent": "Consentiment de cookies",
    "Privacy & Cookie Settings": "Privadesa i cookies",
    "Reject optional": "Rebutja opcionals",
    "Accept all": "Accepta-ho tot",
  },
  fr: {
    "Association": "Association",
    "Team": "Équipe",
    "Tech": "Tech",
    "Finance": "Finance",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Contact",
    "Join us": "Nous rejoindre",
    "Choose language": "Choisir la langue",
    "Language selector": "Sélecteur de langue",
    "Explore": "Explorer",
    "Open": "Ouvrir",
    "Read more": "Lire la suite",
    "Close": "Fermer",
    "Days": "Jours",
    "Hrs": "H",
    "Min": "Min",
    "Sec": "Sec",
    "A global": "Une communauté",
    "Community": "globale",
    "of Builders & Makers": "de Builders & Makers",
    "Build Your Global Home": "Construire votre maison globale",
    "Don’t predict the future. Let’s go out and build it together!": "Ne prédisons pas l'avenir. Allons le construire ensemble.",
    "Action is the foundational key to all success.": "L'action est la base de toute réussite.",
    "Funding the Crays ecosystem.": "Financer l'écosystème Crays.",
    "Monetization framework": "Cadre de monétisation",
    "Funding vehicles": "Véhicules de funding",
    "for a": "pour une",
    "global life.": "vie globale.",
    "The shared technology layer for every official Crays ecosystem project.": "La couche technologique partagée pour chaque projet officiel de l'écosystème Crays.",
    "Real estate becomes a platform": "Le real estate devient une plateforme",
    "when place, demand and capital": "quand lieu, demande et capital",
    "operate together.": "fonctionnent ensemble.",
    "Bring a real project into Crays.": "Apportez un vrai projet à Crays.",
    "Contact Crays Directly": "Contacter Crays directement",
    "Cookie Settings": "Paramètres des cookies",
    "Cookie Consent": "Consentement aux cookies",
    "Privacy & Cookie Settings": "Confidentialité et cookies",
    "Reject optional": "Refuser les options",
    "Accept all": "Tout accepter",
  },
  pt: {
    "Association": "Associação",
    "Team": "Equipa",
    "Tech": "Tech",
    "Finance": "Finanças",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Contacto",
    "Join us": "Junte-se",
    "Choose language": "Escolher idioma",
    "Language selector": "Seletor de idioma",
    "Explore": "Explorar",
    "Open": "Abrir",
    "Read more": "Ler mais",
    "Close": "Fechar",
    "Days": "Dias",
    "Hrs": "H",
    "Min": "Min",
    "Sec": "Seg",
    "A global": "Uma comunidade",
    "Community": "global",
    "of Builders & Makers": "de Builders & Makers",
    "Build Your Global Home": "Construa a sua casa global",
    "Don’t predict the future. Let’s go out and build it together!": "Não preveja o futuro. Vamos construí-lo juntos.",
    "Action is the foundational key to all success.": "A ação é a base de qualquer sucesso.",
    "Funding the Crays ecosystem.": "Financiando o ecossistema Crays.",
    "Monetization framework": "Estrutura de monetização",
    "Funding vehicles": "Veículos de funding",
    "for a": "para uma",
    "global life.": "vida global.",
    "The shared technology layer for every official Crays ecosystem project.": "A camada tecnológica partilhada para cada projeto oficial do ecossistema Crays.",
    "Real estate becomes a platform": "O real estate torna-se uma plataforma",
    "when place, demand and capital": "quando lugar, procura e capital",
    "operate together.": "trabalham juntos.",
    "Bring a real project into Crays.": "Traga um projeto real para a Crays.",
    "Contact Crays Directly": "Contactar a Crays diretamente",
    "Cookie Settings": "Definições de cookies",
    "Cookie Consent": "Consentimento de cookies",
    "Privacy & Cookie Settings": "Privacidade e cookies",
    "Reject optional": "Rejeitar opcionais",
    "Accept all": "Aceitar tudo",
  },
  it: {
    "Association": "Associazione",
    "Team": "Team",
    "Tech": "Tech",
    "Finance": "Finanza",
    "Lifestyle": "Lifestyle",
    "Hospitality": "Hospitality",
    "Real Estate": "Real Estate",
    "Contact": "Contatto",
    "Join us": "Unisciti",
    "Choose language": "Scegli lingua",
    "Language selector": "Selettore lingua",
    "Explore": "Esplora",
    "Open": "Apri",
    "Read more": "Leggi di più",
    "Close": "Chiudi",
    "Days": "Giorni",
    "Hrs": "Ore",
    "Min": "Min",
    "Sec": "Sec",
    "A global": "Una community",
    "Community": "globale",
    "of Builders & Makers": "di Builders & Makers",
    "Build Your Global Home": "Costruisci la tua casa globale",
    "Don’t predict the future. Let’s go out and build it together!": "Non prevedere il futuro. Andiamo a costruirlo insieme.",
    "Action is the foundational key to all success.": "L'azione è la base di ogni successo.",
    "Funding the Crays ecosystem.": "Finanziare l'ecosistema Crays.",
    "Monetization framework": "Framework di monetizzazione",
    "Funding vehicles": "Veicoli di funding",
    "for a": "per una",
    "global life.": "vita globale.",
    "The shared technology layer for every official Crays ecosystem project.": "Il layer tecnologico condiviso per ogni progetto ufficiale dell'ecosistema Crays.",
    "Real estate becomes a platform": "Il real estate diventa una piattaforma",
    "when place, demand and capital": "quando luogo, domanda e capitale",
    "operate together.": "lavorano insieme.",
    "Bring a real project into Crays.": "Porta un progetto reale in Crays.",
    "Contact Crays Directly": "Contatta Crays direttamente",
    "Cookie Settings": "Impostazioni cookie",
    "Cookie Consent": "Consenso cookie",
    "Privacy & Cookie Settings": "Privacy e cookie",
    "Reject optional": "Rifiuta opzionali",
    "Accept all": "Accetta tutto",
  },
};

function decodeHtml(value) {
  return value
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#x27;|&#39;/g, "'")
    .replace(/&rsquo;/g, "’")
    .replace(/&lsquo;/g, "‘")
    .replace(/&ldquo;/g, "“")
    .replace(/&rdquo;/g, "”")
    .replace(/&mdash;/g, "—")
    .replace(/&ndash;/g, "–")
    .replace(/&euro;/g, "€")
    .replace(/&ntilde;/g, "ñ")
    .replace(/&ccedil;/g, "ç")
    .replace(/&agrave;/g, "à")
    .replace(/&aacute;/g, "á")
    .replace(/&eacute;/g, "é")
    .replace(/&iacute;/g, "í")
    .replace(/&oacute;/g, "ó")
    .replace(/&uacute;/g, "ú");
}

function encodeText(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function encodeAttr(value) {
  return encodeText(value).replace(/"/g, "&quot;");
}

function normalize(value) {
  return decodeHtml(value).replace(/\s+/g, " ").trim();
}

function shouldTranslate(value) {
  if (!value) return false;
  if (value.length <= 1) return false;
  if (/^https?:\/\//.test(value)) return false;
  if (!/[A-Za-zÀ-ÿ]/.test(value)) return false;
  if (/^[{}()[\].,;:+\-*/=<>!&|?'"`\d\s]+$/.test(value)) return false;
  if (/^(Crays|DAO|BMW|KPMG|AI|CRM|POS|PMS|RWA|FAQ|F&B|Zug)$/.test(value)) return false;
  return true;
}

function collectStringsFromHtmlLike(html, sink) {
  for (const match of html.matchAll(/>([^<>]+)</g)) {
    const value = normalize(match[1]);
    if (shouldTranslate(value)) sink.add(value);
  }
  for (const match of html.matchAll(/\b(?:alt|aria-label|placeholder|data-wait|value|content)="([^"]+)"/g)) {
    const value = normalize(match[1]);
    if (shouldTranslate(value)) sink.add(value);
  }
}

function collectStrings(html) {
  const strings = new Set();
  const parts = html.split(/(<script\b[\s\S]*?<\/script>)/gi);

  for (const part of parts) {
    if (/^<script\b/i.test(part)) {
      if (/application\/ld\+json/i.test(part)) continue;
      for (const match of part.matchAll(/(["'`])((?:\\.|(?!\1)[\s\S])*?)\1/g)) {
        const raw = match[2]
          .replace(/\\n/g, " ")
          .replace(/\\r/g, " ")
          .replace(/\\t/g, " ")
          .replace(/\\"/g, '"')
          .replace(/\\'/g, "'")
          .replace(/`/g, "");
        if (raw.includes("<") && raw.includes(">")) {
          collectStringsFromHtmlLike(raw, strings);
          continue;
        }
        const value = normalize(raw.replace(/<br\s*\/?>/gi, " "));
        if (!shouldTranslate(value)) continue;
        if (/^(?:[.#[]|\/|https?:|assets\/)/i.test(value)) continue;
        if (/^(?:click|mouseover|mouseout|keydown|DOMContentLoaded|beforeend|afterend|beforebegin)$/i.test(value)) continue;
        if (/^[a-z0-9_-]+$/i.test(value) && value.includes("-")) continue;
        if (!/\s/.test(value) && value.length > 28) continue;
        strings.add(value);
      }
      continue;
    }
    const clean = part.replace(/<style[\s\S]*?<\/style>/gi, " ").replace(/<svg[\s\S]*?<\/svg>/gi, " ");
    collectStringsFromHtmlLike(clean, strings);
  }

  return strings;
}

function protectTerms(text) {
  const replacements = [];
  let protectedText = text;
  protectedTerms
    .slice()
    .sort((a, b) => b.length - a.length)
    .forEach((term, index) => {
      const token = `CRAYSTERM${index}`;
      const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const regex = new RegExp(escaped, "g");
      if (regex.test(protectedText)) {
        protectedText = protectedText.replace(regex, token);
        replacements.push([token, term]);
      }
    });
  return { text: protectedText, replacements };
}

function restoreTerms(text, replacements) {
  let restored = text;
  for (const [token, term] of replacements) {
    restored = restored.replace(new RegExp(token, "g"), term);
  }
  return restored;
}

async function readCache() {
  try {
    return JSON.parse(await readFile(CACHE_FILE, "utf8"));
  } catch {
    return {};
  }
}

async function writeCache(cache) {
  await mkdir(path.dirname(CACHE_FILE), { recursive: true });
  await writeFile(CACHE_FILE, `${JSON.stringify(cache, null, 2)}\n`, "utf8");
}

async function translateChunk(strings, lang) {
  const protectedItems = strings.map((value) => protectTerms(value));
  const query = protectedItems.map((item) => item.text).join(SEP);
  const params = new URLSearchParams({
    client: "gtx",
    sl: "en",
    tl: languages[lang].google,
    dt: "t",
    q: query,
  });

  let response;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    response = await fetch(`https://translate.googleapis.com/translate_a/single?${params.toString()}`);
    if (response.ok) break;
    await new Promise((resolve) => setTimeout(resolve, 350 * (attempt + 1)));
  }

  if (!response || !response.ok) {
    throw new Error(`Translate request failed for ${lang}: ${response ? response.status : "no response"}`);
  }
  const payload = await response.json();
  const translated = (payload[0] || []).map((item) => item[0]).join("");
  const parts = translated.split(SEP);
  if (parts.length !== strings.length) {
    throw new Error(`Translate separator mismatch for ${lang}: expected ${strings.length}, got ${parts.length}`);
  }
  return parts.map((value, index) => restoreTerms(value.trim(), protectedItems[index].replacements));
}

async function translateAll(strings, lang, cache) {
  if (lang === "en") {
    return Object.fromEntries(strings.map((value) => [value, value]));
  }

  cache[lang] ||= {};
  for (const [source, target] of Object.entries(manual[lang] || {})) {
    cache[lang][source] = target;
  }

  const pending = strings.filter((value) => !cache[lang][value]);
  const chunks = [];
  let chunk = [];
  let size = 0;
  for (const value of pending) {
    const nextSize = size + value.length + SEP.length;
    if (chunk.length && nextSize > 4200) {
      chunks.push(chunk);
      chunk = [];
      size = 0;
    }
    chunk.push(value);
    size += value.length + SEP.length;
  }
  if (chunk.length) chunks.push(chunk);

  for (let i = 0; i < chunks.length; i += 1) {
    const chunkStrings = chunks[i];
    try {
      const translated = await translateChunk(chunkStrings, lang);
      chunkStrings.forEach((source, index) => {
        cache[lang][source] = translated[index] || source;
      });
    } catch {
      for (const source of chunkStrings) {
        const translated = await translateChunk([source], lang);
        cache[lang][source] = translated[0] || source;
      }
    }
    if ((i + 1) % 8 === 0) await writeCache(cache);
  }

  await writeCache(cache);
  return cache[lang];
}

function pagePath(slug, lang = null) {
  const suffix = slug ? `${slug}/` : "";
  return lang ? `/${lang}/${suffix}` : `/${suffix}`;
}

function pageUrl(slug, lang = null) {
  return `${SITE_ORIGIN}${pagePath(slug, lang)}`;
}

function alternateLinks(slug, currentLang) {
  const links = [
    `<link rel="canonical" href="${pageUrl(slug, currentLang === "root" ? null : currentLang)}" />`,
    `<link rel="alternate" hreflang="x-default" href="${pageUrl(slug)}" />`,
  ];
  for (const code of Object.keys(languages)) {
    links.push(`<link rel="alternate" hreflang="${code}" href="${pageUrl(slug, code)}" />`);
  }
  return links.join("\n  ");
}

function translated(dict, source) {
  return dict?.[normalize(source)] || normalize(source);
}

function updateHead(html, page, lang, dict) {
  const currentLang = lang === "root" ? "en" : lang;
  const langInfo = languages[currentLang];
  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1] || "Crays";
  const description =
    html.match(/<meta name="description" content="([^"]*)"\s*\/?>/i)?.[1] ||
    "Official Crays Business Nomads Association website.";
  const localizedTitle = currentLang === "en" ? normalize(title) : translated(dict, title);
  const localizedDescription = currentLang === "en" ? normalize(description) : translated(dict, description);
  const canonicalLang = lang === "root" ? "root" : currentLang;

  let next = html.replace(/<html\b[^>]*>/i, `<html lang="${langInfo.html}" data-crays-locale="${lang === "root" ? "x-default" : currentLang}">`);
  next = next.replace(/<title>[\s\S]*?<\/title>/i, `<title>${encodeText(localizedTitle)}</title>`);
  next = next.replace(/<meta name="description" content="[^"]*"\s*\/?>/i, `<meta name="description" content="${encodeAttr(localizedDescription)}" />`);
  next = next.replace(/<meta property="og:locale" content="[^"]*"\s*\/?>/i, `<meta property="og:locale" content="${langInfo.locale}" />`);
  next = next.replace(/<meta property="og:title" content="[^"]*"\s*\/?>/i, `<meta property="og:title" content="${encodeAttr(localizedTitle)}" />`);
  next = next.replace(/<meta property="og:description" content="[^"]*"\s*\/?>/i, `<meta property="og:description" content="${encodeAttr(localizedDescription)}" />`);
  next = next.replace(/<meta property="og:url" content="[^"]*"\s*\/?>/i, `<meta property="og:url" content="${pageUrl(page.slug, lang === "root" ? null : currentLang)}" />`);
  next = next.replace(/<meta property="og:image:alt" content="[^"]*"\s*\/?>/i, `<meta property="og:image:alt" content="${encodeAttr(localizedTitle)}" />`);
  next = next.replace(/<meta name="twitter:title" content="[^"]*"\s*\/?>/i, `<meta name="twitter:title" content="${encodeAttr(localizedTitle)}" />`);
  next = next.replace(/<meta name="twitter:description" content="[^"]*"\s*\/?>/i, `<meta name="twitter:description" content="${encodeAttr(localizedDescription)}" />`);
  next = next.replace(/<meta name="twitter:image:alt" content="[^"]*"\s*\/?>/i, `<meta name="twitter:image:alt" content="${encodeAttr(localizedTitle)}" />`);
  next = next.replace(/\n\s*<link rel="canonical"[^>]*>\s*/gi, "\n");
  next = next.replace(/\n\s*<link rel="alternate" hreflang="[^"]+"[^>]*>\s*/gi, "\n");
  next = next.replace(/\n\s*<meta name="robots"[^>]*>\s*/gi, "\n");
  next = next.replace(
    /(<meta name="description" content="[^"]*"\s*\/?>)/i,
    `$1\n  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />`
  );
  next = next.replace(
    /(<meta name="twitter:image(?::alt)?"[^>]*>\s*)/i,
    `$1\n  ${alternateLinks(page.slug, canonicalLang)}\n  <link rel="sitemap" type="application/xml" href="/sitemap.xml" />`
  );
  return next;
}

function rewriteInternalLinks(html, lang) {
  const localizedPaths = new Set(["", ...pages.map((page) => page.slug).filter(Boolean)]);
  return html.replace(/\bhref="(\/[^"#?]*\/?)(#[^"]*)?"/g, (full, href, hash = "") => {
    if (href.startsWith("/assets/") || href.startsWith("/legal/") || href.startsWith("/blog/")) return full;
    const parts = href.split("/").filter(Boolean);
    let slug = "";
    if (parts.length === 0) {
      slug = "";
    } else if (languages[parts[0]] && parts.length === 1) {
      slug = "";
    } else if (languages[parts[0]]) {
      slug = parts.slice(1).join("/");
    } else {
      slug = parts.join("/");
    }
    if (!localizedPaths.has(slug)) return full;
    return `href="${pagePath(slug, lang)}${hash}"`;
  });
}

function translateSegment(segment, dict) {
  let next = segment.replace(/>([^<>]+)</g, (full, inner) => {
    const key = normalize(inner);
    if (!dict[key] || dict[key] === key) return full;
    const leading = inner.match(/^\s*/)?.[0] || "";
    const trailing = inner.match(/\s*$/)?.[0] || "";
    return `>${leading}${encodeText(dict[key])}${trailing}<`;
  });

  next = next.replace(/\b(alt|aria-label|placeholder|data-wait|value|content)="([^"]+)"/g, (full, name, value) => {
    const key = normalize(value);
    if (!dict[key] || dict[key] === key) return full;
    return `${name}="${encodeAttr(dict[key])}"`;
  });

  return next;
}

function translateStaticHtml(html, dict) {
  return html
    .split(/(<script\b[\s\S]*?<\/script>)/gi)
    .map((part) => (/^<script\b/i.test(part) ? part : translateSegment(part, dict)))
    .join("");
}

function dictionaryForPage(html, dict) {
  const keys = collectStrings(html);
  const pageDict = {};
  for (const key of keys) {
    if (dict[key] && dict[key] !== key) pageDict[key] = dict[key];
  }
  return pageDict;
}

function injectRuntime(html, lang, pageDict) {
  if (lang === "en") return html;
  const payload = JSON.stringify(pageDict).replace(/</g, "\\u003c");
  const snippet = [
    `<script type="application/json" id="crays-i18n-dictionary">${payload}</script>`,
    `<script src="/assets/js/crays-i18n-runtime.js"></script>`,
  ].join("\n");
  return html.replace(/<\/body>/i, `${snippet}\n</body>`);
}

function updateJsonLdUrls(html, page, lang) {
  const currentUrl = pageUrl(page.slug, lang === "root" ? null : lang);
  return html.replace(/"url":\s*"https:\/\/www\.crays\.org[^"]*"/g, `"url": "${currentUrl}"`);
}

function buildSitemap() {
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
  ];
  for (const page of pages) {
    const variants = [["x-default", pageUrl(page.slug)], ...Object.keys(languages).map((lang) => [lang, pageUrl(page.slug, lang)])];
    for (const [lang, url] of variants) {
      lines.push("  <url>");
      lines.push(`    <loc>${url}</loc>`);
      for (const [altLang, altUrl] of variants) {
        lines.push(`    <xhtml:link rel="alternate" hreflang="${altLang}" href="${altUrl}" />`);
      }
      lines.push(`    <changefreq>${page.changefreq}</changefreq>`);
      lines.push(`    <priority>${page.priority}</priority>`);
      lines.push("  </url>");
    }
  }
  lines.push("</urlset>");
  return `${lines.join("\n")}\n`;
}

function buildRobots() {
  return [
    "User-agent: *",
    "Allow: /",
    "",
    "User-agent: OAI-SearchBot",
    "Allow: /",
    "",
    "User-agent: GPTBot",
    "Allow: /",
    "",
    "User-agent: Googlebot",
    "Allow: /",
    "",
    `Sitemap: ${SITE_ORIGIN}/sitemap.xml`,
    "",
  ].join("\n");
}

function buildLlms() {
  return [
    "# Crays",
    "",
    "> Crays Business Nomads Club Association is the Swiss association and ecosystem layer for Crays: hospitality, lifestyle, finance, real estate, technology, DAO governance and partner projects.",
    "",
    "## Official Pages",
    "- [Crays Association](https://www.crays.org/en/)",
    "- [Association](https://www.crays.org/en/association/)",
    "- [Team](https://www.crays.org/en/team/)",
    "- [Tech](https://www.crays.org/en/tech/)",
    "- [Finance](https://www.crays.org/en/finance/)",
    "- [Lifestyle](https://www.crays.org/en/lifestyle/)",
    "- [Hospitality](https://www.crays.org/en/hospitality/)",
    "- [Real Estate](https://www.crays.org/en/real-estate/)",
    "- [Contact](https://www.crays.org/en/contact/)",
    "- [Join us](https://www.crays.org/en/join-us/)",
    "",
    "## Languages",
    "- English: https://www.crays.org/en/",
    "- Deutsch: https://www.crays.org/de/",
    "- Español: https://www.crays.org/es/",
    "- Català: https://www.crays.org/ca/",
    "- Français: https://www.crays.org/fr/",
    "- Português: https://www.crays.org/pt/",
    "- Italiano: https://www.crays.org/it/",
    "",
    "## Brand Notes",
    "Keep Crays, DAO, Web5, Web3, Bitcoin, Nostr, Lightning, RWA, Crays Circle, Crays Fund, Crays Clubs and Crays Coffee as named ecosystem terms.",
    "",
  ].join("\n");
}

async function main() {
  const originals = new Map();
  const allStrings = new Set();
  for (const page of pages) {
    const html = await readFile(path.join(PUBLIC_DIR, page.file), "utf8");
    originals.set(page.key, html);
    for (const value of collectStrings(html)) allStrings.add(value);
  }

  const sortedStrings = [...allStrings].sort((a, b) => a.localeCompare(b));
  const cache = await readCache();
  const dictionaries = {};
  for (const lang of Object.keys(languages)) {
    dictionaries[lang] = await translateAll(sortedStrings, lang, cache);
  }

  for (const lang of Object.keys(languages)) {
    await rm(path.join(PUBLIC_DIR, lang), { recursive: true, force: true });
  }

  for (const page of pages) {
    const sourceHtml = originals.get(page.key);

    const rootHtml = rewriteInternalLinks(
      updateJsonLdUrls(updateHead(sourceHtml, page, "root", dictionaries.en), page, "root"),
      "en"
    );
    await writeFile(path.join(PUBLIC_DIR, page.file), rootHtml, "utf8");

    for (const lang of Object.keys(languages)) {
      const dict = dictionaries[lang];
      let html = sourceHtml;
      html = updateHead(html, page, lang, dict);
      html = rewriteInternalLinks(html, lang);
      html = updateJsonLdUrls(html, page, lang);
      if (lang !== "en") {
        html = translateStaticHtml(html, dict);
        html = injectRuntime(html, lang, dictionaryForPage(sourceHtml, dict));
      }
      const targetDir = path.join(PUBLIC_DIR, lang, page.slug);
      await mkdir(targetDir, { recursive: true });
      await writeFile(path.join(targetDir, "index.html"), html, "utf8");
    }
  }

  await writeFile(path.join(PUBLIC_DIR, "sitemap.xml"), buildSitemap(), "utf8");
  await writeFile(path.join(PUBLIC_DIR, "robots.txt"), buildRobots(), "utf8");
  await writeFile(path.join(PUBLIC_DIR, "llms.txt"), buildLlms(), "utf8");
  await writeCache(cache);

  console.log(`Generated ${Object.keys(languages).length} language trees for ${pages.length} pages.`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
