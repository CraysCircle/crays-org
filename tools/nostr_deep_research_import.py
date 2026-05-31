from __future__ import annotations

import json
import re
from hashlib import sha1
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tools" / "nostr_deep_research_inventory.json"


def slugify(value: str) -> str:
    value = (value or "").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def source(title: str, url: str, description: str) -> tuple[str, str, str]:
    return title, url, description


def load_inventory() -> dict:
    if not INVENTORY.exists():
        return {"sources": [], "summary": {}}
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def unique(values: list[str], limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
        if limit and len(result) >= limit:
            break
    return result


def human_join(values: list[str], fallback: str = "not specified") -> str:
    values = unique(values)
    if not values:
        return fallback
    if len(values) == 1:
        return values[0]
    return ", ".join(values[:-1]) + " and " + values[-1]


def importance_score(values: list[str]) -> int:
    text = " ".join(values or []).lower()
    if "core" in text:
        return 0
    if "high" in text or "active" in text:
        return 1
    if "medium" in text:
        return 2
    return 3


def page_title(item: dict) -> str:
    names = unique(item.get("primary_names", []))
    fetch_title = item.get("fetch", {}).get("title", "")
    if names:
        return names[0]
    if fetch_title:
        return fetch_title
    host = urlparse(item["url"]).netloc or item["url"]
    return host.replace("www.", "")


def category_key(item: dict) -> str:
    text = " ".join(item.get("categories", []) + item.get("subcategories", []) + item.get("primary_names", [])).lower()
    url = item.get("url", "").lower()
    if "nip" in text or "/nips" in url or "nips.nostr.com" in url:
        return "nips"
    if any(token in text for token in ("client", "apps", "social client", "signer", "marketplace", "music", "video", "photos", "blogging")):
        return "apps"
    if any(token in text for token in ("relay", "infra", "monitoring", "blossom", "server")):
        return "relays"
    if any(token in text for token in ("developer", "library", "stack", "sdk", "tooling", "github", "npm", "rust", "python", "go")):
        return "dev"
    if any(token in text for token in ("research", "longform", "reads", "essay", "paper", "primal")):
        return "reads"
    if any(token in text for token in ("security", "privacy", "wallet", "zap", "lightning", "cashu")):
        return "security"
    return "core"


CATEGORY_META = {
    "core": (
        "Core maps and gateways",
        "These are the doorways a serious reader uses to understand the shape of Nostr before going deeper.",
        "source-inventory",
        "what-is-nostr",
    ),
    "nips": (
        "Standards and NIPs",
        "These sources define or explain the shared conventions that let independent Nostr apps understand each other.",
        "nips/complete-index",
        "developer-tools",
    ),
    "apps": (
        "Clients, apps and product surfaces",
        "These sources show how the protocol becomes something people can actually open, touch and use.",
        "apps/catalog",
        "clients",
    ),
    "relays": (
        "Relays, infrastructure and storage",
        "These sources show where Nostr lives: relay markets, network monitoring, storage layers and operational tooling.",
        "relay-market-directory",
        "relays",
    ),
    "dev": (
        "Developer stack and tooling",
        "These sources matter for builders: libraries, SDKs, test tools, Nostr Connect work and implementation references.",
        "developer-tools",
        "nips/complete-index",
    ),
    "reads": (
        "Reads, essays and research",
        "These sources give the broader story: long-form analysis, empirical research, Primal Reads and public explanations.",
        "deep-dives/long-form-publishing",
        "source-inventory",
    ),
    "security": (
        "Security, wallets and trust",
        "These sources matter where key safety, wallet permissions, payments, abuse prevention and trust become product work.",
        "privacy-security",
        "nip-47-wallet-connect",
    ),
}


CATEGORY_LENS = {
    "core": (
        "A core source is a doorway. Its value is not one magic sentence; its value is orientation. Crays should use it to help a reader see the room before we ask them to choose a client, trust a relay or care about a NIP number.",
        "When the source is broad, the Crays version has to be selective. The reader needs the clean map, the first useful distinction and a route forward, not a museum of every term the ecosystem has invented."
    ),
    "nips": (
        "A standards source is where builders agree on shape. Crays should translate that into what changes for people: what becomes portable, what becomes safer, what becomes more searchable, what becomes payable and what still depends on client support.",
        "The important line is this: NIPs are not product guarantees. They are agreements that make product behavior possible. That distinction keeps the writing honest."
    ),
    "apps": (
        "An app source is evidence from the product layer. It shows how Nostr stops being an idea and becomes an interface: a feed, a signer, a music surface, a marketplace, a chat, a publishing desk or a wallet-connected tool.",
        "Crays should read apps as patterns, not trophies. The question is not only whether the app exists. The question is what product lesson it teaches for identity, creators, fans, venues and everyday use."
    ),
    "relays": (
        "A relay or infrastructure source is where the network gets physical enough to have costs, policy, uptime, spam pressure and operational choices. This is where Nostr becomes less romantic and more real.",
        "Crays should make relay information visible because users feel relay decisions even when they never see a relay URL: missing posts, slow feeds, moderation, paid access, local rooms and archive reliability all start here."
    ),
    "dev": (
        "A developer source is not for decoration. It tells Crays which tooling exists, which libraries are mature enough to study, and which implementation paths might save months or create risk.",
        "The Crays reader does not need every API call. They need to understand why tooling matters: safer signers, better relay strategy, tested event handling, wallet permissions, media storage and future product velocity."
    ),
    "reads": (
        "A Reads or research source gives the story oxygen. It adds outside analysis, cultural framing, empirical data or long-form language that helps the archive avoid becoming a dry standards catalog.",
        "Crays should use this layer to make the subject enjoyable. Good research becomes a chapter people actually finish, not a footnote that only developers respect."
    ),
    "security": (
        "A security, wallet or trust source belongs close to the reader's nerves. Keys, payments, encrypted messages and permissions are where a beautiful product can quietly become dangerous.",
        "Crays should write this layer with warmth and precision: no fear theatre, no fake certainty, no casual key handling. The reader should feel more capable after the page, not more confused."
    ),
}


def source_status(item: dict) -> str:
    fetch = item.get("fetch", {})
    status = fetch.get("status", "not checked")
    if status == "ok":
        http_status = fetch.get("http_status")
        return f"reachable during audit, HTTP {http_status}" if http_status else "reachable during audit"
    if fetch.get("error"):
        return f"not reachable during audit: {fetch['error']}"
    return status


def source_cards_for_item(item: dict) -> list[tuple[str, str, str]]:
    cards = [
        source(page_title(item), item["url"], source_status(item)),
    ]
    for url in unique(item.get("secondary_urls", []), 5):
        cards.append(source(urlparse(url).netloc or url, url, "Secondary URL captured in the workbook for the same source row."))
    return cards


def source_page_slug(item: dict) -> str:
    host = urlparse(item["url"]).netloc.replace("www.", "")
    title = page_title(item)
    digest = sha1(item["url"].encode("utf-8")).hexdigest()[:8]
    suffix = slugify(f"{host}-{title}-{digest}")[:102]
    return f"source-inventory/deep-research/{category_key(item)}/{suffix}"


ENTITY_META = {
    "apps": {
        "label": "App and product research",
        "index": "apps/research-atlas",
        "prefix": "apps/research",
        "related": ["apps/catalog", "app-profiles", "clients", "source-inventory/deep-research/apps"],
        "question": "What does this product surface teach about identity, publishing, discovery, signing, wallets, media or social behavior?",
        "crays": "Crays should read this as product evidence. The useful move is not copying the app; it is understanding which interaction pattern could make profiles, creator commerce, fan access, venue context or payments feel natural.",
    },
    "relays": {
        "label": "Relay and infrastructure research",
        "index": "relays/research-atlas",
        "prefix": "relays/research",
        "related": ["relay-market-directory", "relays", "field-guide/relay-selection", "source-inventory/deep-research/relays"],
        "question": "What does this entry reveal about where Nostr data lives, how it is served, who operates it and what tradeoffs users feel?",
        "crays": "Crays needs this layer because venues, Super Nodes and local rooms cannot be designed from protocol romance alone. Uptime, cost, policy, geography, spam pressure and archive behavior all matter.",
    },
    "nips": {
        "label": "NIP and standards research",
        "index": "nips/research-atlas",
        "prefix": "nips/research",
        "related": ["nips/complete-index", "nips", "events-and-kinds", "source-inventory/deep-research/nips"],
        "question": "What user-visible behavior could this standard make possible, and what support still depends on clients, relays or services?",
        "crays": "Crays should translate NIPs into product consequences. Normal readers do not need to worship numbers. They need to know what becomes portable, safer, payable, searchable, private or easier to operate.",
    },
    "dev": {
        "label": "Developer stack research",
        "index": "apps/developer-stack-research",
        "prefix": "apps/developer-stack",
        "related": ["developer-tools", "apps/catalog", "source-inventory/deep-research/dev", "nips/complete-index"],
        "question": "What can builders use here to ship safer Nostr behavior faster without hiding important tradeoffs?",
        "crays": "For Crays this is the tool bench. A library, SDK, command line tool or storage pattern matters when it lowers implementation risk for signers, relays, wallet flows, media, search or event handling.",
    },
    "reads": {
        "label": "Reads and research atlas",
        "index": "archive-library/reads-research",
        "prefix": "archive-library/reads-research",
        "related": ["archive-library", "source-inventory/deep-research/reads", "deep-dives/long-form-publishing", "resources"],
        "question": "What story, evidence or outside framing helps a reader understand why Nostr matters beyond implementation details?",
        "crays": "This layer keeps the archive human. Essays, books, public research and Reads surfaces turn standards into culture, language and stakes people can actually remember.",
    },
    "security": {
        "label": "Security, wallet and trust research",
        "index": "archive-library/security-wallet-research",
        "prefix": "archive-library/security-wallet-research",
        "related": ["privacy-security", "nip-47-wallet-connect", "nip-07-signers", "source-inventory/deep-research/security"],
        "question": "What risk, permission boundary, key-handling lesson or payment behavior should the reader understand before trusting a product?",
        "crays": "Crays has to make this layer calm and serious. Good security writing makes people more capable, not more frightened, and it never hides key or wallet risk behind lifestyle language.",
    },
    "core": {
        "label": "Core directory and map research",
        "index": "archive-library/source-map-research",
        "prefix": "archive-library/source-map-research",
        "related": ["source-inventory", "source-inventory/deep-research/core", "archive-library", "what-is-nostr"],
        "question": "How does this map, directory or gateway help a reader find the next useful Nostr door without getting lost?",
        "crays": "Crays should use these sources as orientation scaffolding. They help us build clean routes through a messy ecosystem instead of making the reader fight ten raw directories alone.",
    },
}


def normalize_entity_name(value: str) -> str:
    name = re.sub(r"\s+", " ", str(value or "")).strip()
    name = re.sub(r"\s+\u2014\s+NostrApps page$", "", name)
    name = re.sub(r"\s+\u2014\s+NostrCompass$", "", name)
    name = re.sub(r"\s+GitHub$", "", name)
    name = re.sub(r"\s+NPM$", "", name)
    name = re.sub(r"\s+crates\.io$", "", name)
    return name.strip(" -") or "Nostr research item"


def entity_key_from_ref(item: dict, ref: dict) -> str:
    sheet = str(ref.get("sheet", "")).lower()
    category = str(ref.get("category", "")).lower()
    name = str(ref.get("name", "")).lower()
    source_key = category_key(item)
    if sheet == "clients apps" or "client" in category or "app" in category:
        return "apps"
    if sheet == "relays infra" or "relay" in category or "relay" in name:
        return "relays"
    if sheet == "dev stack" or any(token in category for token in ("developer", "library", "sdk", "tooling")):
        return "dev"
    if sheet == "reads research" or any(token in category for token in ("research", "longform", "reads")):
        return "reads"
    if sheet == "nips" or "nip" in category or re.search(r"\bnip[- ]?\d+", name):
        return "nips"
    if source_key in {"apps", "relays", "dev", "reads", "nips", "security"}:
        return source_key
    return "core"


def make_entity_records(items: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[tuple[str, str], dict] = {}
    for item in items:
        refs = item.get("row_refs", []) or [{"name": page_title(item), "sheet": "Source", "category": human_join(item.get("categories", []))}]
        for ref in refs:
            display = normalize_entity_name(ref.get("name") or page_title(item))
            if not display or display.lower() in {"source", "link directory", "core"}:
                continue
            key = entity_key_from_ref(item, ref)
            slug = slugify(display)
            record = grouped.setdefault(
                (key, slug),
                {
                    "key": key,
                    "slug": slug,
                    "name": display,
                    "sources": [],
                    "categories": [],
                    "subcategories": [],
                    "importance": [],
                    "notes": [],
                    "sheets": [],
                    "row_count": 0,
                },
            )
            record["sources"].append(item)
            record["categories"].extend(item.get("categories", []))
            record["subcategories"].extend(item.get("subcategories", []))
            record["importance"].extend(item.get("importance_values", []))
            record["notes"].extend(item.get("notes", []))
            record["sheets"].append(ref.get("sheet", "Workbook"))
            record["row_count"] += 1
    result: dict[str, list[dict]] = defaultdict(list)
    for record in grouped.values():
        for field in ["categories", "subcategories", "importance", "notes", "sheets"]:
            record[field] = unique(record[field], 12)
        record["sources"] = sorted(
            {source_item["url"]: source_item for source_item in record["sources"]}.values(),
            key=lambda source_item: (source_item.get("importance_rank", 3), page_title(source_item).lower()),
        )
        result[record["key"]].append(record)
    for records in result.values():
        records.sort(key=lambda record: (importance_score(record.get("importance", [])), record["name"].lower()))
    return result


def entity_page_slug(record: dict) -> str:
    meta = ENTITY_META[record["key"]]
    return f"{meta['prefix']}/{record['slug']}"


def make_entity_page(record: dict, page, section) -> dict:
    meta = ENTITY_META[record["key"]]
    name = record["name"]
    categories = human_join(record.get("categories", []), "Nostr research")
    subcategories = human_join(record.get("subcategories", []), "general")
    importance = human_join(record.get("importance", []), "not ranked")
    notes = " ".join(unique(record.get("notes", []), 4)) or "The workbook flags this as a research item that belongs in the wider Nostr map."
    source_items = record.get("sources", [])
    source_cards = [
        (
            page_title(item),
            f"{source_status(item)}. Source category: {human_join(item.get('subcategories', []), 'general')}.",
            f"/nostr/{source_page_slug(item)}/",
        )
        for item in source_items[:12]
    ]
    if not source_cards:
        source_cards = [("Research source", "Captured from the workbook-backed deep research audit.", "/nostr/source-inventory/deep-research-database/")]
    external_sources = [
        source(page_title(item), item["url"], source_status(item))
        for item in source_items[:8]
    ] or [source("Crays Nostr deep research database", "https://www.crays.org/nostr/source-inventory/deep-research-database/", "Workbook-backed source inventory.")]
    return page(
        entity_page_slug(record),
        name,
        f"{name} in the Crays Nostr research atlas: where it fits, why it matters and which audited sources support it.",
        f"{name} gets its own Crays research page because the workbook does not treat it as background noise. It appears in {categories}, usually around {subcategories}, and that means a reader should be able to find it without knowing which directory first mentioned it.",
        [
            section("Why this belongs in the atlas", [
                f"{name} sits in the {meta['label'].lower()} layer. The reader question is simple: {meta['question']}",
                f"The workbook signal says: {notes} The Crays version keeps that signal, then turns it into a plain-language map point instead of another cold list entry.",
            ], [
                ("Route", meta["label"]),
                ("Workbook area", categories),
                ("Subcategory", subcategories),
                ("Importance", importance),
            ]),
            section("The Crays read", [
                meta["crays"],
                "The writing rule is the same as the rest of the archive: explain the thing like a sharp friend would explain it over coffee, but keep the facts traceable enough that builders can follow up.",
            ]),
            section("Evidence trail", [
                f"This derived page is connected to {len(source_items)} audited source URL(s) and {record.get('row_count', 0)} workbook row signal(s). Open the source cards when you want the crawl status, checked subpages and raw research trail."
            ], cards=source_cards),
        ],
        tag="Nostr research atlas",
        sources=external_sources,
        related=meta["related"] + [meta["index"], "source-inventory/deep-research-database"],
        keywords=[name, meta["label"], "Nostr research", "Crays Nostr atlas"],
        read="Research atlas entry",
    )


def make_entity_index_page(key: str, records: list[dict], page, section) -> dict:
    meta = ENTITY_META[key]
    cards = [
        (
            record["name"],
            f"{human_join(record.get('subcategories', []), 'general')}. {len(record.get('sources', []))} source(s), {record.get('row_count', 0)} workbook signal(s).",
            f"/nostr/{entity_page_slug(record)}/",
        )
        for record in records
    ]
    return page(
        meta["index"],
        meta["label"],
        f"Crays research atlas shelf for {meta['label'].lower()}, derived from the deep Nostr workbook and live source audit.",
        f"This shelf turns the Excel research into reader-facing Crays pages. It is not a link dump. Every entry has a reason to exist, a route, an evidence trail and a Crays interpretation.",
        [
            section("How to use this shelf", [
                f"This shelf contains {len(records)} derived topic page(s). Use it when you know a name, app, relay, standard, tool or research source and want to see where it lives in the Crays Nostr map.",
                "Some entries are mature products, some are infrastructure, some are experiments and some are reference material. The page does not pretend they are equal. It gives each one a findable place and a next step."
            ], [
                ("Entries", str(len(records))),
                ("Reader question", meta["question"]),
                ("Editorial rule", "Only explain what the source trail supports. No filler, no hype padding."),
            ]),
            section("Research entries", [
                "Open an entry for the Crays interpretation and the source trail behind it."
            ], cards=cards),
        ],
        tag="Nostr research atlas shelf",
        sources=[source("Crays Nostr deep research database", "https://www.crays.org/nostr/source-inventory/deep-research-database/", "Workbook-backed source inventory and crawl audit.")],
        related=meta["related"] + ["source-inventory/deep-research-database"],
        keywords=[meta["label"], "Nostr research atlas", "Crays Nostr archive"],
        read="Research atlas shelf",
    )


def make_source_page(item: dict, page, section) -> dict:
    title = page_title(item)
    key = category_key(item)
    category_label, category_deck, category_home, second_related = CATEGORY_META[key]
    fetch = item.get("fetch", {})
    headings = [heading.get("text", "") for heading in fetch.get("headings", [])]
    heading_text = human_join(headings[:6], "no readable heading structure captured")
    notes = unique(item.get("notes", []), 6)
    note_text = " ".join(notes) if notes else "The workbook marks this source as part of the Nostr research base."
    categories = human_join(item.get("categories", []), "Nostr research")
    subcategories = human_join(item.get("subcategories", []), "general")
    importance = human_join(item.get("importance_values", []), "not ranked")
    lens_a, lens_b = CATEGORY_LENS[key]
    paragraph_signal = len(fetch.get("paragraph_samples", []))
    has_metadata_description = bool(fetch.get("description", ""))
    subpages = item.get("subpages_checked", [])
    subpage_cards = []
    for subpage in subpages[:18]:
        sub_title = subpage.get("title") or subpage.get("url")
        status = subpage.get("http_status") or subpage.get("status") or "checked"
        sub_desc = f"Same-site subpage checked during the audit. Status: {status}. Treated as evidence, not imported copy."
        subpage_cards.append((sub_title, sub_desc, subpage.get("url")))
    if not subpage_cards:
        subpage_cards = [("No useful subpage crawl", "The URL itself was checked, but no relevant same-site subpage was captured for this source.", item["url"])]
    workbook_cards = [
        (f'{ref.get("sheet")} row {ref.get("row")}', f'{ref.get("category")}: {ref.get("name")}', item["url"])
        for ref in item.get("row_refs", [])[:14]
    ]
    if not workbook_cards:
        workbook_cards = [("Workbook reference", "Captured from the deep research workbook.", item["url"])]

    paragraphs = [
        section(
            "What this source adds",
            [
                f"{title} belongs in the Crays Nostr archive because the workbook places it in {categories}, with the subcategory {subcategories}. That already tells us the role: this is not random web noise, it is a mapped source inside the larger Nostr research base.",
                f"The useful information to carry forward is this: {note_text} The Crays job is to translate that signal into a reader-friendly explanation, not to throw another raw URL at someone who is trying to understand the scene.",
                f"During the audit the source was {source_status(item)}. {'The live page exposed usable metadata, but this Crays page keeps the wording original instead of copying the source description.' if has_metadata_description else 'Where the live page did not expose clean metadata, the workbook context remains the editorial anchor.'}",
                f"{lens_a} {lens_b}",
            ],
            [
                ("Category", categories),
                ("Subcategory", subcategories),
                ("Importance", importance),
            ],
        ),
        section(
            "Where it sits in the Nostr map",
            [
                f"This source sits in the {category_label.lower()} route. {category_deck}",
                f"The captured structure points toward {heading_text}. That does not mean Crays copies those headings. It means the page gives us clues about how the ecosystem itself explains the topic, which Crays then rewrites into a cleaner, more human chapter.",
                f"The live audit found {paragraph_signal} readable paragraph signal(s). They are used only as research evidence; the public Crays copy stays original, traceable and written in the same voice as the rest of the atlas.",
            ],
        ),
        section(
            "What Crays should carry forward",
            [
                "The archive should pull the lesson out of the source and place it where a reader expects it: standards in the NIP path, products in the app path, relays in the infrastructure path, research in the library, and Crays-specific meaning in the product layer.",
                "The language has to stay calm and alive. A reader should feel guided by someone who knows the protocol and also remembers that most people do not wake up wanting to read implementation notes."
            ],
            [
                ("Keep", "The concrete ecosystem fact, product pattern or standards signal from the source."),
                ("Translate", "Turn technical or directory language into Crays' plain, cool, explanatory Sachbuch voice."),
                ("Place", "Connect the source to the right atlas route so it can be found logically later."),
            ],
        ),
        section(
            "Workbook evidence",
            [
                f"This page is backed by {len(item.get('row_refs', []))} workbook reference row(s). That matters because the same URL can appear in several research sheets and carry slightly different editorial meaning."
            ],
            cards=workbook_cards,
        ),
        section(
            "Subpages checked",
            [
                f"The audit checked {len(subpages)} same-site subpage(s) for this source where the domain and crawl rules made that useful. These subpages are treated as research evidence, not as imported copy."
            ],
            cards=subpage_cards,
        ),
        section(
            "Reader takeaway",
            [
                f"If you are reading the Crays Nostr archive, the practical takeaway is simple: {title} is one source in the wider {category_label.lower()} map. Use it to understand the ecosystem signal, then use the Crays chapter links to see how that signal fits identity, apps, relays, payments, creators, venues and governance.",
                "That is the standard for this whole database: no loose bookmark dump, no protocol fog, no lonely expert reference that only makes sense if you already know the answer."
            ],
        ),
    ]

    return page(
        source_page_slug(item),
        f"Research Source: {title}",
        f"Crays deep-research source page for {title}, based on the Nostr research workbook and live URL audit.",
        f"{title} is part of the Crays Nostr deep research database. This page turns the workbook entry and live source audit into a readable archive chapter.",
        paragraphs,
        tag="Nostr deep research source",
        sources=source_cards_for_item(item),
        related=["source-inventory/deep-research-database", category_home, second_related, "archive-library", "what-is-nostr"],
        keywords=[title, category_label, "Nostr research", "Crays Nostr archive"],
        read="Research source chapter",
    )


def make_category_page(key: str, items: list[dict], page, section) -> dict:
    label, deck, category_home, second_related = CATEGORY_META[key]
    cards = [
        (
            page_title(item),
            f"{human_join(item.get('importance_values', []), 'not ranked')}. {human_join(item.get('subcategories', []), 'general')}. {source_status(item)}.",
            f"/nostr/{source_page_slug(item)}/",
        )
        for item in sorted(items, key=lambda source_item: (source_item.get("importance_rank", 3), page_title(source_item).lower()))
    ]
    return page(
        f"source-inventory/deep-research/{key}",
        f"Deep Research: {label}",
        f"Crays deep research category for {label.lower()}, built from the workbook-backed Nostr source database.",
        deck,
        [
            section("What this shelf covers", [
                f"This shelf contains {len(items)} deduplicated URL source(s) from the workbook. The entries are not a link dump; each source has its own Crays page with source status, workbook evidence, subpage checks and a reader-facing interpretation.",
                "Use this shelf when you want to audit coverage. Use the normal article routes when you want the polished reader journey."
            ], [
                ("Sources", str(len(items))),
                ("Route", label),
                ("Editorial rule", "Every source becomes an explained Crays archive object."),
            ]),
            section("Source pages", [
                "Open a source when you need to understand what the workbook says, whether the live URL responded and where the information belongs in the Crays atlas."
            ], cards=cards),
        ],
        tag="Nostr deep research category",
        sources=[source("Nostr deep research workbook", "https://www.crays.org/nostr/source-inventory/deep-research-database/", "Generated from the local Crays Nostr research workbook.")],
        related=["source-inventory/deep-research-database", category_home, second_related, "archive-library", "source-inventory"],
        keywords=[label, "Nostr research database", "Crays Nostr archive"],
        read="Research category",
    )


def make_index_page(inventory: dict, grouped: dict[str, list[dict]], page, section) -> dict:
    summary = inventory.get("summary", {})
    fetch_status = summary.get("fetch_status", {})
    category_cards = []
    for key, items in sorted(grouped.items(), key=lambda kv: CATEGORY_META.get(kv[0], ("",))[0]):
        label, deck, _category_home, _second_related = CATEGORY_META[key]
        category_cards.append((label, f"{len(items)} sources. {deck}", f"/nostr/source-inventory/deep-research/{key}/"))
    importance_counts = Counter()
    for item in inventory.get("sources", []):
        for value in item.get("importance_values", []):
            importance_counts[value] += 1
    return page(
        "source-inventory/deep-research-database",
        "Nostr Deep Research Database",
        f"Workbook-backed Crays research database for Nostr: {inventory.get('unique_urls', 0)} unique URLs, {inventory.get('url_cells', 0)} URL cells and {summary.get('subpages_checked', 0)} checked subpages.",
        "This is the audit backbone behind the Crays Nostr archive: every workbook URL becomes a traceable research object, then the useful information gets translated into the same Crays voice and structure as the rest of the atlas.",
        [
            section("What was audited", [
                f"The workbook contains {inventory.get('workbook_rows_with_urls', 0)} rows with URLs and {inventory.get('url_cells', 0)} URL cells. After deduplication, the import produced {inventory.get('unique_urls', 0)} unique source pages.",
                f"The live audit checked the direct URLs and, where useful, same-site subpages. The current inventory records {summary.get('subpages_checked', 0)} checked subpage(s). Reachability is recorded honestly: a source can be important even if the live site blocks crawling, moves, times out or needs manual review.",
                "The point is not to worship the spreadsheet. The point is to make the research usable: standards, apps, relays, tooling, reads, security and core directories all get a place in the atlas."
            ], [
                ("Unique source URLs", str(inventory.get("unique_urls", 0))),
                ("URL cells", str(inventory.get("url_cells", 0))),
                ("Reachable direct URLs", str(fetch_status.get("ok", 0))),
                ("Subpages checked", str(summary.get("subpages_checked", 0))),
            ]),
            section("Research shelves", [
                "Each shelf below is generated from the workbook and live audit. The shelf pages then lead into individual source pages."
            ], cards=category_cards),
            section("How Crays uses this", [
                "A source page is not the final reader chapter. It is the audit layer: what did the workbook say, what did the page expose, where does it belong, and what should Crays carry forward?",
                "When an important source reveals a missing idea, that idea should graduate into the relevant article route: NIPs, apps, relays, developer stack, Reads/research, privacy/security or Crays product implementation."
            ]),
        ],
        tag="Nostr deep research database",
        sources=[source("Crays Nostr deep research workbook", "https://www.crays.org/nostr/source-inventory/deep-research-database/", "Local workbook-backed import and URL audit.")],
        related=["source-inventory", "archive-library", "nips/complete-index", "apps/catalog", "relay-market-directory"],
        keywords=["Nostr research database", "Nostr source audit", "Crays Nostr archive"],
        read="Research database",
    )


def make_deep_research_pages(page, section) -> list[dict]:
    inventory = load_inventory()
    items = inventory.get("sources", [])
    if not items:
        return []
    grouped: dict[str, list[dict]] = defaultdict(list)
    pages: list[dict] = []
    for item in items:
        grouped[category_key(item)].append(item)
        pages.append(make_source_page(item, page, section))
    for key in CATEGORY_META:
        pages.append(make_category_page(key, grouped.get(key, []), page, section))
    pages.append(make_index_page(inventory, grouped, page, section))
    entity_groups = make_entity_records(items)
    for key in ENTITY_META:
        records = entity_groups.get(key, [])
        pages.append(make_entity_index_page(key, records, page, section))
        for record in records:
            pages.append(make_entity_page(record, page, section))
    return pages
