import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const ORIGIN = "https://crays.org";
const OUT_DIR = path.resolve("public");
const MAX_PAGES = 120;

const pageQueue = [new URL("/", ORIGIN).href];
const seenPages = new Set();
const seenAssets = new Set();

const pageLikeExtensions = new Set(["", ".html", ".htm"]);
const assetAttributes = ["href", "src", "poster"];

function isSameOrigin(url) {
  return url.origin === ORIGIN || url.hostname === "www.crays.org";
}

function normalizeUrl(raw, base) {
  if (!raw || raw.startsWith("#") || raw.startsWith("mailto:") || raw.startsWith("tel:") || raw.startsWith("javascript:")) {
    return null;
  }

  try {
    const url = new URL(raw.replace(/&amp;/g, "&"), base);
    url.hash = "";
    return url;
  } catch {
    return null;
  }
}

function localPathFor(url, contentType = "") {
  let pathname = decodeURIComponent(url.pathname);
  if (pathname.endsWith("/")) {
    pathname += "index.html";
  } else if (contentType.includes("text/html") && !path.extname(pathname)) {
    pathname = `${pathname}/index.html`;
  }

  const cleanParts = pathname.split("/").filter(Boolean);
  return path.join(OUT_DIR, ...cleanParts);
}

async function saveResponse(url, response, body) {
  const filePath = localPathFor(url, response.headers.get("content-type") || "");
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, body);
  return filePath;
}

function collectSrcset(value, base) {
  return value
    .split(",")
    .map((entry) => entry.trim().split(/\s+/)[0])
    .map((raw) => normalizeUrl(raw, base))
    .filter(Boolean);
}

function collectCssUrls(css, base) {
  const urls = [];
  const regex = /url\(\s*(['"]?)(.*?)\1\s*\)/g;
  let match;

  while ((match = regex.exec(css))) {
    const raw = match[2];
    if (!raw || raw.startsWith("data:")) continue;
    const url = normalizeUrl(raw, base);
    if (url) urls.push(url);
  }

  return urls;
}

function collectHtmlUrls(html, base) {
  const urls = [];

  const attrRegex = /\s(href|src|poster)=["']([^"']+)["']/gi;
  let attrMatch;
  while ((attrMatch = attrRegex.exec(html))) {
    if (!assetAttributes.includes(attrMatch[1].toLowerCase())) continue;
    const url = normalizeUrl(attrMatch[2], base);
    if (url) urls.push(url);
  }

  const srcsetRegex = /\ssrcset=["']([^"']+)["']/gi;
  let srcsetMatch;
  while ((srcsetMatch = srcsetRegex.exec(html))) {
    urls.push(...collectSrcset(srcsetMatch[1], base));
  }

  return urls;
}

function classify(url, contentTypeHint = "") {
  const ext = path.extname(url.pathname).toLowerCase();
  if (contentTypeHint.includes("text/html") || pageLikeExtensions.has(ext)) {
    return "page";
  }

  return "asset";
}

async function fetchBuffer(url) {
  const response = await fetch(url.href, {
    redirect: "follow",
    headers: {
      "user-agent": "Codex local mirror for crays-org",
    },
  });

  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  return { response, buffer };
}

async function downloadAsset(url) {
  const key = url.href;
  if (seenAssets.has(key)) return;
  seenAssets.add(key);

  try {
    const { response, buffer } = await fetchBuffer(url);
    const filePath = await saveResponse(url, response, buffer);

    if ((response.headers.get("content-type") || "").includes("text/css")) {
      const css = buffer.toString("utf8");
      for (const nestedUrl of collectCssUrls(css, url)) {
        if (isSameOrigin(nestedUrl)) {
          await downloadAsset(nestedUrl);
        }
      }
    }

    console.log(`asset ${url.pathname} -> ${path.relative(process.cwd(), filePath)}`);
  } catch (error) {
    console.warn(`skip asset ${url.href}: ${error.message}`);
  }
}

async function crawlPage(url) {
  const key = url.href;
  if (seenPages.has(key) || seenPages.size >= MAX_PAGES) return;
  seenPages.add(key);

  try {
    const { response, buffer } = await fetchBuffer(url);
    const contentType = response.headers.get("content-type") || "";
    const filePath = await saveResponse(url, response, buffer);
    console.log(`page  ${url.pathname} -> ${path.relative(process.cwd(), filePath)}`);

    if (!contentType.includes("text/html")) return;

    const html = buffer.toString("utf8");
    for (const foundUrl of collectHtmlUrls(html, url)) {
      if (!isSameOrigin(foundUrl)) continue;

      if (classify(foundUrl) === "page") {
        if (!seenPages.has(foundUrl.href)) pageQueue.push(foundUrl.href);
      } else {
        await downloadAsset(foundUrl);
      }
    }
  } catch (error) {
    console.warn(`skip page ${url.href}: ${error.message}`);
  }
}

await mkdir(OUT_DIR, { recursive: true });

while (pageQueue.length && seenPages.size < MAX_PAGES) {
  const next = new URL(pageQueue.shift());
  await crawlPage(next);
}

console.log(`Done. Mirrored ${seenPages.size} pages and ${seenAssets.size} assets into ${path.relative(process.cwd(), OUT_DIR)}.`);
