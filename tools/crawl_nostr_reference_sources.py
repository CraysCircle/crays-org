from __future__ import annotations

import html
import json
import re
import time
from collections import defaultdict, deque
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "nostr_reference_inventory.json"
USER_AGENT = "CraysNostrArchive/1.0 (+https://www.crays.org/nostr/)"


START_URLS = [
    "https://nostr.net/",
    "https://nostr.how/",
    "https://nostr.com/",
    "https://nostr.org/",
    "https://www.nostrapps.com/",
    "https://www.nostrlogin.org/",
    "https://www.nostr.co.uk/",
]

ALLOWED_NETLOCS = {
    "nostr.net",
    "nostr.how",
    "nostr.com",
    "nostr.org",
    "www.nostrapps.com",
    "nostrapps.com",
    "www.nostrlogin.org",
    "nostrlogin.org",
    "www.nostr.co.uk",
    "nostr.co.uk",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.title = ""
        self.meta_description = ""
        self.headings: list[dict[str, str]] = []
        self._tag_stack: list[str] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._heading_level = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        self._tag_stack.append(tag)
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])
        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            if name == "description" or prop == "og:description":
                if not self.meta_description:
                    self.meta_description = clean_text(attrs_dict.get("content", ""))
        if tag == "title":
            self._capture = "title"
            self._buffer = []
        if tag in {"h1", "h2", "h3"}:
            self._capture = "heading"
            self._heading_level = tag
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if self._capture == "title" and tag == "title":
            self.title = clean_text(" ".join(self._buffer))
            self._capture = None
        elif self._capture == "heading" and tag == self._heading_level:
            text = clean_text(" ".join(self._buffer))
            if text:
                self.headings.append({"level": self._heading_level, "text": text})
            self._capture = None
            self._heading_level = ""
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def safe_slug(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def fetch_text(url: str, timeout: int = 25) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as response:
        final_url = response.geturl()
        raw = response.read(2_000_000)
    text = raw.decode("utf-8", "replace")
    return final_url, text


def normalize_url(base: str, href: str) -> str | None:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "nostr:")):
        return None
    url, _fragment = urldefrag(urljoin(base, href))
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None
    path = re.sub(r"/+$", "/", parsed.path or "/")
    return parsed._replace(path=path).geturl()


def crawl_reference_pages() -> list[dict]:
    queue: deque[tuple[str, int]] = deque((url, 0) for url in START_URLS)
    seen: set[str] = set()
    pages: list[dict] = []
    per_domain_count: dict[str, int] = defaultdict(int)

    while queue and len(seen) < 360:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        parsed = urlparse(url)
        if parsed.netloc not in ALLOWED_NETLOCS:
            continue
        if per_domain_count[parsed.netloc] >= 90:
            continue
        try:
            final_url, text = fetch_text(url)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            pages.append({"url": url, "status": "error", "error": str(exc), "domain": parsed.netloc})
            continue

        parser = PageParser()
        parser.feed(text)
        final_parsed = urlparse(final_url)
        per_domain_count[final_parsed.netloc] += 1
        internal_links: list[str] = []
        external_links: list[str] = []
        for href in parser.links:
            normalized = normalize_url(final_url, href)
            if not normalized:
                continue
            link_netloc = urlparse(normalized).netloc
            if link_netloc in ALLOWED_NETLOCS:
                internal_links.append(normalized)
                if depth < 3 and normalized not in seen:
                    queue.append((normalized, depth + 1))
            else:
                external_links.append(normalized)

        pages.append(
            {
                "url": final_url,
                "status": "ok",
                "domain": final_parsed.netloc,
                "title": parser.title or final_url,
                "description": parser.meta_description,
                "headings": parser.headings[:80],
                "internal_links": sorted(set(internal_links))[:180],
                "external_links": sorted(set(external_links))[:180],
                "html_bytes": len(text),
            }
        )
        time.sleep(0.05)
    return pages


def parse_nostr_apps(html_text: str) -> list[dict]:
    decoded = html.unescape(html_text)
    apps: list[dict] = []
    pattern = re.compile(
        r'x-data="\{platforms:\s*\[(?P<platforms>[^\]]*)\],\s*categories:\s*\[(?P<categories>[^\]]*)\],\s*fulltext:\s*`(?P<fulltext>.*?)`\}"'
        r'.{0,1800}?<a href="(?P<slug>[^"]+)"[^>]*class="app-link[^"]*"'
        r'.{0,1800}?<h2 class="app-title">(?P<title>.*?)</h2>\s*<p class="description">(?P<description>.*?)</p>',
        re.S,
    )
    for match in pattern.finditer(decoded):
        platforms = re.findall(r'"([^"]+)"', match.group("platforms"))
        categories = re.findall(r'"([^"]+)"', match.group("categories"))
        fulltext = clean_text(match.group("fulltext"))
        links = re.findall(r"https?://[^\s`'\"]+", fulltext)
        slug = safe_slug(match.group("slug"))
        apps.append(
            {
                "slug": slug,
                "name": clean_text(re.sub("<[^>]+>", " ", match.group("title"))),
                "description": clean_text(re.sub("<[^>]+>", " ", match.group("description"))),
                "platforms": platforms,
                "categories": categories,
                "links": links[:6],
            }
        )
    deduped: dict[str, dict] = {}
    for app in apps:
        deduped[app["slug"]] = app
    return sorted(deduped.values(), key=lambda item: item["name"].lower())


def parse_awesome_nostr(readme: str) -> list[dict]:
    categories: list[dict] = []
    current: dict | None = None
    for raw_line in readme.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            if current and current["links"]:
                categories.append(current)
            current = {"title": clean_text(line[3:]), "links": []}
            continue
        if not current:
            continue
        for title, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", line):
            desc = clean_text(re.sub(r"\[[^\]]+\]\(https?://[^)]+\)", "", line).strip(" -*:"))
            if title and url:
                current["links"].append({"title": clean_text(title), "url": url, "description": desc})
    if current and current["links"]:
        categories.append(current)
    return categories


def parse_nip_file(number: str, markdown: str) -> dict:
    lines = markdown.splitlines()
    title = ""
    status = ""
    headings: list[str] = []
    for line in lines:
        if line.startswith("# ") and not title:
            title = clean_text(line.lstrip("# "))
        elif line.startswith("## "):
            headings.append(clean_text(line.lstrip("# ")))
        elif line.lower().startswith("status:"):
            status = clean_text(line.split(":", 1)[1])
    if not title:
        title = f"NIP-{number}"
    summary_lines = []
    for line in lines:
        stripped = clean_text(line)
        if stripped and not stripped.startswith("#") and not stripped.lower().startswith(("status:", "author:", "created:")):
            summary_lines.append(stripped)
        if len(" ".join(summary_lines)) > 420:
            break
    return {
        "number": number,
        "title": title,
        "status": status,
        "headings": headings[:24],
        "summary_seed": clean_text(" ".join(summary_lines))[:700],
        "url": f"https://github.com/nostr-protocol/nips/blob/master/{number}.md",
    }


def fetch_nips() -> list[dict]:
    api_url = "https://api.github.com/repos/nostr-protocol/nips/contents/"
    try:
        _final, text = fetch_text(api_url)
        entries = json.loads(text)
    except Exception:
        entries = []
    nip_files = sorted(
        entry["name"]
        for entry in entries
        if isinstance(entry, dict) and re.fullmatch(r"\d\d\.md", entry.get("name", ""))
    )
    nips: list[dict] = []
    for filename in nip_files:
        number = filename[:2]
        raw_url = f"https://raw.githubusercontent.com/nostr-protocol/nips/master/{filename}"
        try:
            _final, markdown = fetch_text(raw_url)
        except Exception:
            continue
        nips.append(parse_nip_file(number, markdown))
        time.sleep(0.03)
    return nips


def main() -> None:
    pages = crawl_reference_pages()
    nostrapps_html = ""
    awesome_readme = ""
    try:
        _final, nostrapps_html = fetch_text("https://www.nostrapps.com/")
    except Exception:
        pass
    try:
        _final, awesome_readme = fetch_text("https://raw.githubusercontent.com/aljazceru/awesome-nostr/main/README.md")
    except Exception:
        pass

    inventory = {
        "generated_at": "2026-05-30",
        "seed_urls": START_URLS + ["https://github.com/aljazceru/awesome-nostr"],
        "reference_pages": pages,
        "nostr_apps": parse_nostr_apps(nostrapps_html),
        "awesome_nostr": parse_awesome_nostr(awesome_readme),
        "nips": fetch_nips(),
    }
    OUT.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        "Crawled inventory:",
        len(inventory["reference_pages"]),
        "pages,",
        len(inventory["nostr_apps"]),
        "apps,",
        len(inventory["awesome_nostr"]),
        "awesome categories,",
        len(inventory["nips"]),
        "NIPs",
    )


if __name__ == "__main__":
    main()
