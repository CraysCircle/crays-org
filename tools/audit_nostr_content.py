from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_NOSTR = ROOT / "public" / "nostr"
REPORT_DIR = ROOT / "reports"
BASE_URL = "https://www.crays.org/nostr"

GENERIC_HEADINGS = {
    "Why people care",
    "The human reason",
    "Under the hood",
    "The easy wrong turn",
    "The pocket test",
    "A day in the wild",
    "The Crays read",
    "Our read",
    "Words that must stay honest",
    "What to carry away",
    "Nearby doors",
    "From label to judgment",
    "What to watch",
    "The clean takeaway",
    "The mood around it",
    "One last map pin",
    "Where to go next",
}

CRAYS_THIRD_PERSON_PATTERNS = [
    r"\bCrays is\b",
    r"\bCrays are\b",
    r"\bCrays should\b",
    r"\bCrays can\b",
    r"\bCrays could\b",
    r"\bCrays will\b",
    r"\bCrays must\b",
    r"\bCrays needs\b",
    r"\bCrays uses\b",
    r"\bCrays reads\b",
    r"\bCrays wants\b",
    r"\bCrays offers\b",
    r"\bCrays explains\b",
    r"\bCrays provides\b",
    r"\bThe Crays reader\b",
    r"\bCrays readers\b",
]

GENERIC_LINK_TEXT = {"here", "learn more", "read more", "more", "click here", "this page"}

TERM_TARGETS = [
    ("Nostr Wallet Connect", "nip-47-wallet-connect"),
    ("NIP-47", "nip-47-wallet-connect"),
    ("NIP-57", "nip-57-zaps-lightning"),
    ("NIP-65", "nip-65-relay-list"),
    ("NIP-05", "nip-05-identifiers"),
    ("NIP-07", "nip-07-signers"),
    ("NIP-19", "nip-19-addresses"),
    ("NIP-44", "nip-44-encryption"),
    ("NIP-46", "nip-46-remote-signing"),
    ("NIP-94", "nip-94-files"),
    ("NIP-96", "nip-96-file-storage"),
    ("NIP-98", "nip-98-http-auth"),
    ("public key", "keys-identity"),
    ("private key", "keys-identity"),
    ("signer", "nip-07-signers"),
    ("signers", "nip-07-signers"),
    ("relay", "relays"),
    ("relays", "relays"),
    ("client", "clients"),
    ("clients", "clients"),
    ("event", "events-and-kinds"),
    ("events", "events-and-kinds"),
    ("zap", "nip-57-zaps-lightning"),
    ("zaps", "nip-57-zaps-lightning"),
    ("Lightning", "nip-57-zaps-lightning"),
    ("Blossom", "deep-dives/blossom-servers-and-relays"),
    ("Blossom server", "deep-dives/blossom-servers-and-relays"),
    ("Cashu", "deep-dives/safebox-sovereign-wallet-records"),
    ("Safebox", "apps/safebox"),
    ("FoundUPS", "deep-dives/foundups-agent-compute-focus-network"),
]


class PageHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.current_link: dict | None = None
        self.current_heading: dict | None = None
        self.title_text: list[str] = []
        self.meta_description = ""
        self.links: list[dict] = []
        self.images: list[dict] = []
        self.headings: list[dict] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.stack.append(tag)
        if tag == "meta" and attr.get("name") == "description":
            self.meta_description = attr.get("content", "")
        if tag == "a":
            self.current_link = {"href": attr.get("href", ""), "text": []}
        if tag in {"h1", "h2", "h3"}:
            self.current_heading = {"level": tag, "text": []}
        if tag == "img":
            self.images.append({"src": attr.get("src", ""), "alt": attr.get("alt", "")})

    def handle_endtag(self, tag):
        if tag == "a" and self.current_link is not None:
            text = " ".join("".join(self.current_link["text"]).split())
            self.links.append({"href": self.current_link["href"], "text": text})
            self.current_link = None
        if tag in {"h1", "h2", "h3"} and self.current_heading is not None:
            text = " ".join("".join(self.current_heading["text"]).split())
            self.headings.append({"level": self.current_heading["level"], "text": text})
            self.current_heading = None
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not data.strip():
            return
        if self.stack and self.stack[-1] == "title":
            self.title_text.append(data)
        if self.current_link is not None:
            self.current_link["text"].append(data)
        if self.current_heading is not None:
            self.current_heading["text"].append(data)
        if not any(tag in {"script", "style", "head"} for tag in self.stack):
            self.text_chunks.append(data)


def load_generator():
    sys.path.insert(0, str(ROOT / "tools"))
    import build_nostr_seo_hub as hub

    return hub


def read_excel_summary(path: str | None) -> dict:
    if not path:
        return {}
    excel = Path(path)
    if not excel.exists():
        return {"error": f"Excel file not found: {excel}"}
    try:
        import pandas as pd

        xl = pd.ExcelFile(excel)
        summary = {"file": str(excel), "sheets": {}}
        for sheet in xl.sheet_names:
            df = pd.read_excel(excel, sheet_name=sheet)
            summary["sheets"][sheet] = {"rows": int(df.shape[0]), "columns": list(map(str, df.columns))}
        return summary
    except Exception as exc:
        return {"error": str(exc)}


def html_path_for_slug(slug: str) -> Path:
    return PUBLIC_NOSTR / slug / "index.html"


def strip_html_text(html: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())


def strip_tags(value: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", value).split())


def extract_attr(raw: str, attr: str) -> str:
    match = re.search(rf"""{attr}\s*=\s*["']([^"']*)["']""", raw, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def remove_link_audit_noise(html: str) -> str:
    """Keep the audit focused on visible navigation and article links."""
    html = re.sub(
        r"""<div\b[^>]*class=["'][^"']*crays-nostr-archive-finder__results[^"']*["'][^>]*>.*?</div>""",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    return html


def item_text(page: dict) -> str:
    parts = [page.get("title", ""), page.get("deck", ""), page.get("intro", "")]
    for sec in page.get("sections", []):
        parts.append(sec.get("title", ""))
        parts.extend(sec.get("paragraphs", []))
        for strong, text in sec.get("bullets", []):
            parts.extend([strong, text])
        for card in sec.get("cards", []):
            parts.extend([str(part) for part in card[:2]])
    return " ".join(str(part) for part in parts if part)


def extract_html_signals(html: str) -> dict:
    if not html:
        return {"links": [], "headings": [], "images": [], "meta_description": ""}
    html = remove_link_audit_noise(html)
    links = []
    for match in re.finditer(r"""<a\b([^>]*)>(.*?)</a>""", html, flags=re.IGNORECASE | re.DOTALL):
        href = extract_attr(match.group(1), "href")
        if not href:
            continue
        links.append({"href": href, "text": strip_tags(match.group(2))})
    headings = []
    for match in re.finditer(r"""<(h[123])\b[^>]*>(.*?)</\1>""", html, flags=re.IGNORECASE | re.DOTALL):
        headings.append({"level": match.group(1).lower(), "text": strip_tags(match.group(2))})
    images = []
    for match in re.finditer(r"""<img\b([^>]*)>""", html, flags=re.IGNORECASE | re.DOTALL):
        raw = match.group(1)
        images.append({"src": extract_attr(raw, "src"), "alt": extract_attr(raw, "alt")})
    meta = ""
    meta_match = re.search(r"""<meta\s+name=["']description["'][^>]*>""", html, flags=re.IGNORECASE)
    if meta_match:
        meta = extract_attr(meta_match.group(0), "content")
    return {"links": links, "headings": headings, "images": images, "meta_description": meta}


def page_type(slug: str, key: str, title: str) -> str:
    if slug in {"what-is-nostr", "getting-started", "why-nostr"} or slug.startswith("reading-paths/"):
        return "Start- / Einstiegseite"
    if slug in {"archive-library", "source-inventory"}:
        return "Library- / Ressourcen-Seite"
    if slug.startswith("nips/") or re.search(r"\bnip-\d", slug):
        return "NIP-Seite"
    if slug.startswith("apps/") or slug.startswith("app-profiles/"):
        return "Tool- / Client- / App-Seite"
    if slug.startswith("people/") or key == "people":
        return "People- / Projektseite"
    if slug.startswith("deep-dives/"):
        return "Tiefenartikel"
    if key == "crays":
        return "Crays-Kontextseite"
    if key in {"privacy", "wallets", "relays", "commerce", "governance", "media"}:
        return "Oekosystem-Seite"
    if "glossary" in slug:
        return "Begriffserklaerung"
    return "Grundlagenartikel"


def status_from_metrics(word_count: int, section_count: int, generic_count: int) -> str:
    if generic_count >= 6:
        return "templatehaft"
    if word_count < 500:
        return "duenn"
    if word_count < 1100:
        return "ausbaufaehig"
    if section_count < 3:
        return "unstrukturiert"
    return "brauchbar"


def score_depth(word_count: int, section_count: int, source_count: int) -> int:
    score = 1
    if word_count >= 700:
        score += 1
    if word_count >= 1400:
        score += 1
    if section_count >= 6:
        score += 1
    if source_count >= 4:
        score += 1
    return min(score, 5)


def score_links(outgoing_count: int, incoming_count: int, missing_terms: int) -> int:
    score = 1
    if outgoing_count >= 5:
        score += 1
    if outgoing_count >= 12:
        score += 1
    if incoming_count >= 2:
        score += 1
    if missing_terms == 0:
        score += 1
    return min(score, 5)


def detect_missing_terms(text: str, current_slug: str, linked_slugs: set[str]) -> list[str]:
    lower = text.lower()
    missing = []
    for term, target in TERM_TARGETS:
        if target == current_slug or target in linked_slugs:
            continue
        if re.search(rf"(?<![a-z0-9-]){re.escape(term.lower())}(?![a-z0-9-])", lower):
            missing.append(f"{term} -> {target}")
    return missing[:12]


def is_decorative_or_icon_src(src: str) -> bool:
    src = (src or "").lower()
    return any(
        token in src
        for token in (
            "google.com/s2/favicons",
            "/assets/brand/crays-mark.svg",
            "/assets/brand/crays-home-logo.webp",
            "/assets/footer-icons/",
        )
    )


def action_for(record: dict) -> str:
    actions = []
    if record["generic_section_count"]:
        actions.append("generische Kapitel entfernen und individuelle Struktur schreiben")
    if record["third_person_crays_count"]:
        actions.append("Crays-Voice in erste Person umschreiben")
    if record["technical_depth_score"] <= 2:
        actions.append("fachliche Tiefe mit Quellen, Beispielen und konkreten NIPs ergaenzen")
    if record["link_quality_score"] <= 2:
        actions.append("interne Links im Fliesstext und Related Concepts ausbauen")
    if record["missing_alt_count"] or record["duplicate_image_count"]:
        actions.append("Bildlogik, Alt-Texte und Duplikate pruefen")
    if record["h1_count"] != 1:
        actions.append("H1-Struktur bereinigen")
    if not actions:
        actions.append("gezielte redaktionelle Politur und Quellenabgleich")
    return "; ".join(actions)


def priority_for(record: dict) -> str:
    if record["third_person_crays_count"] or record["generic_section_count"] >= 6 or record["h1_count"] != 1:
        return "P0"
    if record["technical_depth_score"] <= 2 or record["incoming_internal_links"] == 0:
        return "P1"
    if record["link_quality_score"] <= 2 or record["missing_internal_terms_count"] >= 4:
        return "P2"
    return "P3"


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", default="")
    parser.add_argument("--out", default=str(REPORT_DIR))
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    hub = load_generator()
    pages = list(hub.PAGES)
    by_slug = {page["slug"]: page for page in pages}

    parsed: dict[str, dict] = {}
    outgoing_by_slug: dict[str, set[str]] = {}
    incoming: dict[str, set[str]] = defaultdict(set)
    title_counts = Counter(page["title"].strip().lower() for page in pages)

    for page in pages:
        slug = page["slug"]
        html_path = html_path_for_slug(slug)
        html = html_path.read_text(encoding="utf-8", errors="ignore") if html_path.exists() else ""
        signals = extract_html_signals(html)
        text = hub.crays_voice(item_text(page))
        linked_slugs = set()
        outgoing_links = []
        for link in signals["links"]:
            href = link["href"]
            if not href.startswith("/nostr/"):
                continue
            target = href[len("/nostr/") :].split("#", 1)[0].strip("/")
            if not target or target == slug:
                continue
            if target in linked_slugs:
                continue
            linked_slugs.add(target)
            outgoing_links.append({"target": target, "anchor": link["text"] or target})
            incoming[target].add(slug)
        outgoing_by_slug[slug] = linked_slugs
        parsed[slug] = {
            "html_path": str(html_path),
            "exists": html_path.exists(),
            "text": text,
            "links": signals["links"],
            "internal_links": outgoing_links,
            "headings": signals["headings"],
            "images": signals["images"],
            "meta_description": signals["meta_description"],
        }

    rows: list[dict] = []
    suggested_incoming: dict[str, list[str]] = defaultdict(list)
    media_rows: list[dict] = []
    gap_rows: list[dict] = []
    category_map: dict[str, list[dict]] = defaultdict(list)
    generic_pages = []
    third_person_pages = []
    isolated_pages = []
    missing_category_pages = []
    duplicate_titles = []

    for page in pages:
        slug = page["slug"]
        key = hub.primary_nav_key(slug)
        route = hub.ROUTE_LABELS.get(key, key.title())
        sub_hub = hub.atlas_group_label(page)
        data = parsed[slug]
        text = data["text"]
        word_count = len(re.findall(r"\b[\w'-]+\b", text))
        section_titles = [sec["title"] for sec in page.get("sections", [])]
        generic = [title for title in section_titles if title in GENERIC_HEADINGS]
        h1s = [h for h in data["headings"] if h["level"] == "h1"]
        h2s = [h for h in data["headings"] if h["level"] == "h2"]
        repeated_headings = [heading for heading, count in Counter(h["text"] for h in data["headings"]).items() if count > 1]
        third_person = []
        for pattern in CRAYS_THIRD_PERSON_PATTERNS:
            third_person.extend(re.findall(pattern, text, flags=re.IGNORECASE))
        generic_anchor_count = sum(1 for link in data["links"] if link["text"].strip().lower() in GENERIC_LINK_TEXT)
        missing_terms = detect_missing_terms(text, slug, outgoing_by_slug[slug])
        image_srcs = [img["src"] for img in data["images"] if img["src"] and not is_decorative_or_icon_src(img["src"])]
        duplicate_images = [src for src, count in Counter(image_srcs).items() if count > 1]
        missing_alt_count = sum(1 for img in data["images"] if img["src"] and not img["alt"].strip() and not is_decorative_or_icon_src(img["src"]))
        source_count = len(page.get("sources", []))
        incoming_count = len(incoming.get(slug, set()))
        outgoing_count = len(outgoing_by_slug.get(slug, set()))
        record = {
            "url": f"{BASE_URL}/{slug}/",
            "slug": slug,
            "title": page["title"],
            "main_category": route,
            "category_key": key,
            "sub_hub": sub_hub,
            "page_type": page_type(slug, key, page["title"]),
            "content_status": status_from_metrics(word_count, len(section_titles), len(generic)),
            "word_count": word_count,
            "section_count": len(section_titles),
            "technical_depth_score": score_depth(word_count, len(section_titles), source_count),
            "clarity_score": 4 if word_count and len(h2s) >= 3 and len(repeated_headings) <= 1 else 2,
            "link_quality_score": score_links(outgoing_count, incoming_count, len(missing_terms)),
            "incoming_internal_links": incoming_count,
            "outgoing_internal_links": outgoing_count,
            "missing_internal_terms_count": len(missing_terms),
            "missing_internal_terms": "; ".join(missing_terms),
            "outgoing_link_examples": "; ".join(f'{link["anchor"]} -> {link["target"]}' for link in data["internal_links"][:12]),
            "missing_information": "needs source-backed expansion" if score_depth(word_count, len(section_titles), source_count) <= 2 else "",
            "outdated_information": "",
            "generic_section_count": len(generic),
            "generic_sections": "; ".join(generic),
            "unnecessary_sections": "; ".join(generic),
            "repeated_headings": "; ".join(repeated_headings),
            "third_person_crays_count": len(third_person),
            "third_person_crays_examples": "; ".join(sorted(set(third_person))[:8]),
            "h1_count": len(h1s),
            "h1_text": "; ".join(h["text"] for h in h1s[:3]),
            "image_count": len(data["images"]),
            "missing_alt_count": missing_alt_count,
            "duplicate_image_count": len(duplicate_images),
            "duplicate_images": "; ".join(duplicate_images[:5]),
            "priority": "",
            "concrete_action": "",
        }
        record["priority"] = priority_for(record)
        record["concrete_action"] = action_for(record)
        rows.append(record)
        category_map[route].append({
            "slug": slug,
            "title": page["title"],
            "sub_hub": sub_hub,
            "page_type": record["page_type"],
            "priority": record["priority"],
        })
        for missing in missing_terms:
            term, target = missing.split(" -> ", 1)
            suggested_incoming[target].append(f"{slug}: {term}")
            gap_rows.append({
                "affected_slug": slug,
                "missing_topic": term,
                "source": "term-to-page internal link map",
                "recommended_section": "first natural mention in body copy",
                "suggested_text": f"Link the first meaningful mention of {term} to /nostr/{target}/ and add one explanatory sentence where needed.",
                "internal_link_targets": target,
                "priority": "P1" if key in {"start", "privacy", "wallets", "relays", "nips"} else "P2",
            })
        for img in data["images"]:
            media_rows.append({
                "slug": slug,
                "title": page["title"],
                "src": img["src"],
                "alt": img["alt"],
                "problem": "missing alt" if img["src"] and not img["alt"].strip() else "",
                "better_image_idea": "match image to the page concept and avoid duplicate hero/inline use" if duplicate_images else "",
                "license_note": "verify external sources; prefer owned, generated, Unsplash/Pexels/Openverse/Wikimedia with license recorded",
            })
        if record["generic_section_count"]:
            generic_pages.append(record)
        if record["third_person_crays_count"]:
            third_person_pages.append(record)
        if incoming_count == 0 and slug not in {"what-is-nostr", "archive-library"}:
            isolated_pages.append(record)
        if key == "library" and not slug.startswith(("archive-library", "source-inventory", "awesome-nostr", "field-guide", "apps/research", "apps/developer-stack", "relays/research", "nips/research")):
            missing_category_pages.append(record)
        if title_counts[page["title"].strip().lower()] > 1:
            duplicate_titles.append(record)

    fields = [
        "url",
        "slug",
        "title",
        "main_category",
        "sub_hub",
        "page_type",
        "content_status",
        "word_count",
        "section_count",
        "technical_depth_score",
        "clarity_score",
        "link_quality_score",
        "incoming_internal_links",
        "outgoing_internal_links",
        "missing_internal_terms",
        "outgoing_link_examples",
        "missing_information",
        "outdated_information",
        "generic_section_count",
        "generic_sections",
        "unnecessary_sections",
        "repeated_headings",
        "third_person_crays_count",
        "third_person_crays_examples",
        "h1_count",
        "h1_text",
        "image_count",
        "missing_alt_count",
        "duplicate_image_count",
        "priority",
        "concrete_action",
    ]
    rows_sorted = sorted(rows, key=lambda row: (row["priority"], row["main_category"], row["slug"]))
    link_summary_rows = []
    for row in rows_sorted:
        slug = row["slug"]
        outgoing_examples = "; ".join(
            f'{link["anchor"]} -> {link["target"]}'
            for link in parsed[slug]["internal_links"][:30]
        )
        incoming_examples = "; ".join(sorted(incoming.get(slug, set()))[:30])
        proposed_incoming = "; ".join(suggested_incoming.get(slug, [])[:30])
        link_summary_rows.append({
            "slug": slug,
            "title": row["title"],
            "main_category": row["main_category"],
            "sub_hub": row["sub_hub"],
            "outgoing_internal_links": row["outgoing_internal_links"],
            "outgoing_link_examples": outgoing_examples,
            "incoming_internal_links": row["incoming_internal_links"],
            "incoming_link_examples": incoming_examples,
            "missing_internal_terms": row["missing_internal_terms"],
            "incoming_link_proposals": proposed_incoming,
            "related_concepts": "; ".join(row["missing_internal_terms"].split("; ")[:8]) if row["missing_internal_terms"] else "",
            "next_reading_step": "Use the route board, article related links and closest missing term target.",
            "main_category_backlink": row["main_category"],
            "sub_hub_backlink": row["sub_hub"],
        })
    write_csv(out_dir / "nostr_content_audit.csv", rows_sorted, fields)
    write_csv(
        out_dir / "nostr_internal_link_mapping.csv",
        link_summary_rows,
        [
            "slug",
            "title",
            "main_category",
            "sub_hub",
            "outgoing_internal_links",
            "outgoing_link_examples",
            "incoming_internal_links",
            "incoming_link_examples",
            "missing_internal_terms",
            "incoming_link_proposals",
            "related_concepts",
            "next_reading_step",
            "main_category_backlink",
            "sub_hub_backlink",
        ],
    )
    write_csv(out_dir / "nostr_content_gaps.csv", gap_rows, ["affected_slug", "missing_topic", "source", "recommended_section", "suggested_text", "internal_link_targets", "priority"])
    write_csv(out_dir / "nostr_media_audit.csv", media_rows, ["slug", "title", "src", "alt", "problem", "better_image_idea", "license_note"])

    summary = {
        "page_count": len(pages),
        "excel_summary": read_excel_summary(args.excel),
        "category_counts": {category: len(items) for category, items in sorted(category_map.items())},
        "priority_counts": dict(Counter(row["priority"] for row in rows)),
        "status_counts": dict(Counter(row["content_status"] for row in rows)),
        "generic_template_pages": len(generic_pages),
        "third_person_crays_pages": len(third_person_pages),
        "isolated_pages": len(isolated_pages),
        "missing_category_candidates": len(missing_category_pages),
        "duplicate_title_pages": len(duplicate_titles),
        "top_priorities": [
            {
                "slug": row["slug"],
                "title": row["title"],
                "category": row["main_category"],
                "priority": row["priority"],
                "action": row["concrete_action"],
            }
            for row in rows_sorted[:80]
        ],
    }
    (out_dir / "nostr_content_audit_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "nostr_category_mapping.json").write_text(json.dumps(category_map, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        "# Nostr Content Audit",
        "",
        f"Pages audited: {len(pages)}",
        "",
        "## Category Counts",
    ]
    for category, count in summary["category_counts"].items():
        md.append(f"- {category}: {count}")
    md.extend(["", "## Priority Counts"])
    for priority, count in summary["priority_counts"].items():
        md.append(f"- {priority}: {count}")
    md.extend(["", "## Highest Priority Actions"])
    for row in rows_sorted[:40]:
        md.append(f"- {row['priority']} `{row['slug']}` ({row['main_category']}): {row['concrete_action']}")
    md.extend(["", "## Report Files", "- `nostr_content_audit.csv`", "- `nostr_category_mapping.json`", "- `nostr_content_gaps.csv`", "- `nostr_internal_link_mapping.csv`", "- `nostr_media_audit.csv`"])
    (out_dir / "nostr_content_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
