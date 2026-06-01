from __future__ import annotations

import re


ROUTE_HUBS = {
    "start": "what-is-nostr",
    "people": "people",
    "apps": "apps/catalog",
    "relays": "relay-market-directory",
    "nips": "nips/complete-index",
    "privacy": "privacy-security",
    "wallets": "nip-47-wallet-connect",
    "media": "music-video-media",
    "commerce": "content-sale",
    "governance": "dao-governance",
    "crays": "nostr-and-crays",
    "library": "archive-library",
}


ROUTE_LABELS = {
    "start": "Start",
    "people": "People",
    "apps": "Apps",
    "relays": "Relays",
    "nips": "NIPs",
    "privacy": "Privacy",
    "wallets": "Wallets",
    "media": "Media",
    "commerce": "Commerce",
    "governance": "Governance",
    "crays": "Crays",
    "library": "Library",
}


ROUTE_CONTEXT = {
    "start": {
        "surface": "first-principles learning",
        "jobs": "keys, clients, relays, events and the first safe mental model",
        "risk": "starting with jargon before the reader knows what problem the protocol solves",
        "example": "a reader should be able to explain why their identity can move before they learn every NIP number",
    },
    "people": {
        "surface": "human and cultural memory",
        "jobs": "builders, maintainers, funders, creators, events and the social context behind the protocol",
        "risk": "turning people into mythology instead of showing the work, incentives and public evidence",
        "example": "a profile should help you understand what the person changed, what to verify and which parts of Nostr their work touches",
    },
    "apps": {
        "surface": "product and interface behavior",
        "jobs": "clients, signers, discovery tools, wallets, media surfaces and developer libraries",
        "risk": "treating every app as a trophy instead of asking what the interface teaches about Nostr",
        "example": "a signer page should connect the product to private-key safety, NIP-07, NIP-46 and clear permission prompts",
    },
    "relays": {
        "surface": "network infrastructure",
        "jobs": "storage, delivery, moderation policy, paid access, relay lists, monitoring and local operation",
        "risk": "pretending relays are invisible plumbing when they shape speed, discovery, spam resistance and availability",
        "example": "a relay page should explain what the relay stores, who operates it, how policies are exposed and what clients can infer",
    },
    "nips": {
        "surface": "technical standards",
        "jobs": "event kinds, tags, messages, identity formats, encryption, wallet flows and client-relay agreements",
        "risk": "presenting a NIP as if support were automatic across every app and relay",
        "example": "a NIP page should translate the spec into product consequences, failure cases and the reader-visible behavior it enables",
    },
    "privacy": {
        "surface": "trust and safety",
        "jobs": "keys, signatures, encryption, authentication, moderation, reports, mutes and safer account control",
        "risk": "using sovereignty language while hiding the parts that can leak, confuse or permanently damage a user",
        "example": "a privacy page should separate what cryptography protects from what metadata, relays and product choices still reveal",
    },
    "wallets": {
        "surface": "payments and value flow",
        "jobs": "zaps, Lightning, Nostr Wallet Connect, Cashu, Safebox, budgets, invoices and permission boundaries",
        "risk": "making payments feel simple while leaving custody, spending limits and signing authority vague",
        "example": "a wallet page should explain who holds funds, who signs, what an app can request and how the user can revoke access",
    },
    "media": {
        "surface": "publishing and creator media",
        "jobs": "long-form writing, music, video, photos, Blossom, file metadata, comments, highlights and fan access",
        "risk": "using pretty media without explaining storage, hashes, fallback URLs, rights, attribution and moderation",
        "example": "a media page should connect the creator experience to NIP-23, NIP-94, Blossom or the client behavior that makes it readable",
    },
    "commerce": {
        "surface": "markets and revenue design",
        "jobs": "creator sales, listings, marketplaces, FoundUPS, investor context, zaps, offers and paid access",
        "risk": "confusing a signed listing with a complete business process that includes trust, fulfilment, support and dispute handling",
        "example": "a commerce page should explain what the event can prove and what still needs wallet, identity, reputation and operations",
    },
    "governance": {
        "surface": "coordination and reputation",
        "jobs": "badges, voting, polls, reports, labels, policy, moderation, DAO readiness and public decision trails",
        "risk": "turning governance into decoration instead of making authority, issuer trust and decision scope clear",
        "example": "a badge page should distinguish issuer, recipient, display, meaning and the social trust needed for the badge to matter",
    },
    "crays": {
        "surface": "our implementation layer",
        "jobs": "Crays.net, venues, Super Nodes, status, awards, payments, governance records and product integration",
        "risk": "speaking about Crays from the outside or making protocol claims that do not become visible product choices",
        "example": "a Crays page should say how we use Nostr in profiles, venues, creator access, awards or governance without pretending the protocol does everything alone",
    },
    "library": {
        "surface": "research and archive navigation",
        "jobs": "source maps, deep research, glossary entries, long reads, indexes, field guides and routes through the archive",
        "risk": "leaving the reader with a flat pile of links instead of a guided path through sources, concepts and examples",
        "example": "a library page should tell you what kind of source you are looking at, what to trust, what to verify and where it fits in the wider map",
    },
}


ROUTE_SOURCES = {
    "start": ["Nostr protocol repository", "Nostr NIPs", "nostr.how", "nostr.org"],
    "people": ["Nostrica", "Nostr World", "Nostr Apps", "Awesome Nostr"],
    "apps": ["Nostr Apps", "Awesome Nostr", "nostr.org", "Nostr Login"],
    "relays": ["Nostr.watch relay finder", "BigBrotr", "NIP-11 Relay Information", "NIP-65 Relay List Metadata"],
    "nips": ["Nostr NIPs", "NIP-01", "nostr.how", "Nostr protocol repository"],
    "privacy": ["NIP-07", "NIP-44", "NIP-46", "NIP-98"],
    "wallets": ["NIP-47", "NIP-57", "Alby", "Safebox repository"],
    "media": ["NIP-23", "NIP-94", "NIP-96", "Blossom repository"],
    "commerce": ["NIP-57", "NIP-47", "FoundUPS website", "Foundups-Agent repository"],
    "governance": ["NIP-58", "NIP-51", "Nostr NIPs", "Nostr protocol repository"],
    "crays": ["Nostr NIPs", "nostr.how", "Safebox repository", "FoundUPS website"],
    "library": ["Nostr protocol repository", "Nostr NIPs", "Awesome Nostr", "Nostr Apps"],
}


CUSTOM_SOURCES = {
    "NIP-11 Relay Information": ("NIP-11 Relay Information", "https://github.com/nostr-protocol/nips/blob/master/11.md", "Relay information documents expose relay metadata, limitations and supported capabilities."),
    "NIP-89": ("NIP-89", "https://github.com/nostr-protocol/nips/blob/master/89.md", "Recommended application handlers help clients route Nostr objects to suitable apps."),
    "NIP-94": ("NIP-94", "https://github.com/nostr-protocol/nips/blob/master/94.md", "File metadata events describe URLs, hashes, MIME types, sizes, dimensions and fallbacks."),
    "NIP-96": ("NIP-96", "https://github.com/nostr-protocol/nips/blob/master/96.md", "HTTP file storage integration describes server metadata and upload flows for Nostr clients."),
    "NIP-15": ("NIP-15", "https://github.com/nostr-protocol/nips/blob/master/15.md", "Marketplace event conventions for products, stalls and commerce experiments."),
    "NIP-99": ("NIP-99", "https://github.com/nostr-protocol/nips/blob/master/99.md", "Classified listing events for portable listing-style commerce."),
    "NIP-56": ("NIP-56", "https://github.com/nostr-protocol/nips/blob/master/56.md", "Reporting events create abuse and moderation signals."),
    "NIP-72": ("NIP-72", "https://github.com/nostr-protocol/nips/blob/master/72.md", "Moderated community events describe communities, moderators and approvals."),
    "NIP-88": ("NIP-88", "https://github.com/nostr-protocol/nips/blob/master/88.md", "Poll events describe questions, choices and vote events."),
}


TOPIC_LINKS = [
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
    ("relays", "relays"),
    ("client", "clients"),
    ("events", "events-and-kinds"),
    ("zaps", "nip-57-zaps-lightning"),
    ("Lightning", "nip-57-zaps-lightning"),
    ("Blossom", "deep-dives/blossom-servers-and-relays"),
    ("Cashu", "deep-dives/safebox-sovereign-wallet-records"),
    ("Safebox", "apps/safebox"),
    ("FoundUPS", "deep-dives/foundups-agent-compute-focus-network"),
]


def _words(value: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", value or ""))


def _item_text(item: dict) -> str:
    parts = [item.get("title", ""), item.get("deck", ""), item.get("intro", "")]
    for sec in item.get("sections", []):
        parts.append(sec.get("title", ""))
        parts.extend(sec.get("paragraphs", []))
        for strong, text in sec.get("bullets", []):
            parts.extend([strong, text])
        for card in sec.get("cards", []):
            parts.extend(str(part) for part in card[:2])
    return " ".join(str(part) for part in parts if part)


def _dedupe_sources(sources: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen = set()
    out = []
    for title, url, desc in sources:
        key = (url or title).strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append((title, url, desc))
    return out


def _source_lookup(*groups: list[tuple[str, str, str]]) -> dict[str, tuple[str, str, str]]:
    lookup = dict(CUSTOM_SOURCES)
    for group in groups:
        for src in group:
            lookup[src[0]] = src
    return lookup


def _ensure_sources(item: dict, route: str, source_by_title: dict[str, tuple[str, str, str]], fallback_sources: list[tuple[str, str, str]]) -> None:
    current = list(item.get("sources") or [])
    for title in ROUTE_SOURCES.get(route, ROUTE_SOURCES["library"]):
        if title in source_by_title:
            current.append(source_by_title[title])
    if "blossom" in item.get("slug", ""):
        for title in ("Blossom repository", "NIP-94", "NIP-96"):
            if title in source_by_title:
                current.append(source_by_title[title])
    if "wallet" in item.get("slug", "") or "zap" in item.get("slug", ""):
        for title in ("NIP-47", "NIP-57"):
            if title in source_by_title:
                current.append(source_by_title[title])
    for src in fallback_sources:
        current.append(src)
        if len(_dedupe_sources(current)) >= 5:
            break
    item["sources"] = _dedupe_sources(current)


def _related_cards(item: dict, route: str, existing_slugs: set[str]) -> list[tuple[str, str, str]]:
    slug = item.get("slug", "")
    title = item.get("title", "this page")
    cards: list[tuple[str, str, str]] = []
    hub = ROUTE_HUBS.get(route, "archive-library")
    if hub in existing_slugs and hub != slug:
        cards.append((f"{ROUTE_LABELS.get(route, 'Library')} hub", f"Use the parent route when you need the wider shelf around {title}.", f"/nostr/{hub}/"))
    for related in item.get("related", [])[:4]:
        related_slug = str(related).strip("/").removeprefix("nostr/")
        if related_slug in existing_slugs and related_slug != slug:
            cards.append((related_slug.split("/")[-1].replace("-", " ").title(), f"Read this beside {title} when you want the neighboring concept.", f"/nostr/{related_slug}/"))
    text = _item_text(item).lower()
    for term, target in TOPIC_LINKS:
        if target in existing_slugs and target != slug and term.lower() in text:
            cards.append((term, f"This concept is part of the working vocabulary behind {title}.", f"/nostr/{target}/"))
        if len(cards) >= 6:
            break
    seen = set()
    unique = []
    for card in cards:
        if card[2] in seen:
            continue
        seen.add(card[2])
        unique.append(card)
    return unique[:6]


def _depth_sections(item: dict, route: str, existing_slugs: set[str], section) -> list[dict]:
    title = item.get("title", "this page")
    slug = item.get("slug", "")
    context = ROUTE_CONTEXT.get(route, ROUTE_CONTEXT["library"])
    route_label = ROUTE_LABELS.get(route, "Library")
    source_titles = ", ".join(src[0] for src in item.get("sources", [])[:4])
    cards = _related_cards(item, route, existing_slugs)

    sections = [
        section(
            f"How to place {title} on the map",
            [
                f"Read {title} as part of the {route_label} route, not as an isolated entry. Its main surface is {context['surface']}: {context['jobs']}. That framing matters because a Nostr page is useful only when you can see which layer it belongs to and which layer it does not solve by itself.",
                f"The first question is practical: what changes for you if {title} works well? Sometimes the answer is safer signing, sometimes better relay discovery, sometimes clearer media storage, sometimes a stronger source trail. Keep that question in front of you and the page becomes easier to judge.",
            ],
            [
                ("Layer", f"{route_label} is the parent route, so the page should send you back to that shelf and sideways into adjacent concepts."),
                ("Evidence", f"The current source trail starts with {source_titles or 'the workbook and primary Nostr references'}. Treat those as anchors, then compare product behavior and NIP support."),
            ],
            cards=cards,
        ),
        section(
            f"What {title} should help you decide",
            [
                f"A good page about {title} should leave you with a decision, not just recognition. You should know whether it is a protocol primitive, a client behavior, a relay operation, a product example, a research source or a Crays implementation question. That distinction keeps the archive from becoming a flat glossary.",
                f"The common mistake is {context['risk']}. We avoid that by making the claim, the evidence and the next step visible. If a statement depends on a NIP, the page should point to that NIP. If it depends on a project, the page should show the project source. If it affects user safety, the page should say what can fail.",
            ],
        ),
        section(
            f"The working example behind {title}",
            [
                f"Use this page with a concrete mental test: {context['example']}. That example is more useful than a generic definition because Nostr is not one product. The same signed event can be read by different clients, stored by different relays and interpreted through different product choices.",
                f"This is also why internal links matter. When the page mentions keys, clients, relays, events, zaps, Blossom, Cashu, FoundUPS or NIPs, those words should lead to the page that explains the concept more deeply. The goal is not to trap you in tabs; the goal is to let you move with context.",
            ],
        ),
        section(
            f"Source discipline for {title}",
            [
                f"The source list is part of the content, not decoration. For {title}, use primary protocol documents first when the claim is technical, project repositories or product pages when the claim is about an app, and research or directory sources when the claim is about ecosystem position. If the sources disagree, the page should show the uncertainty instead of smoothing it away.",
                "That source discipline is how a large archive stays trustworthy. It also helps learning: you get a short explanation first, then a route to the source that proves or complicates it. The page should feel like a guided chapter, but the evidence should still be close enough to inspect.",
            ],
        ),
    ]

    current_words = _words(_item_text(item))
    if current_words < 850:
        sections.append(
            section(
                f"Before and after reading {title}",
                [
                    f"Before reading {title}, make sure you know the nearby base concepts: a public key identifies, a private key signs, relays carry signed events, clients render those events, and NIPs describe shared behavior. You do not need to memorize the whole protocol, but those pieces prevent most confusion.",
                    f"After reading {title}, the next useful move is to compare it with one neighboring page. If this is an app, compare it with a signer, relay or wallet page. If this is a NIP, compare it with the product behavior it enables. If this is a research source, compare it with the hub that uses it. That is how the archive becomes a learning path instead of a pile.",
                ],
            )
        )
    if current_words < 550:
        sections.append(
            section(
                f"Why {title} is not just a short note",
                [
                    f"Some pages look small because the object is small: a source entry, a micro-topic, a category shelf or a project reference. The page still needs a job. For {title}, the job is to name the object clearly, place it in the right route, connect it to source evidence and give you the next reading step.",
                    "That is the difference between a database row and a useful knowledge node. A database row stores a fact. A knowledge node explains what the fact connects to, what it does not prove and why you might open the next page.",
                ],
            )
        )
    if current_words < 700:
        sections.append(
            section(
                f"The navigation job of {title}",
                [
                    f"{title} also has a navigation job. It should help you decide whether to move upward to the {route_label} hub, sideways to a related concept, or downward into a more technical source. That sounds simple, but it is the difference between browsing and learning.",
                    "When a page does that job well, you do not need to keep the whole archive in your head. The page carries enough context to orient you, enough links to continue, and enough source discipline to show where the claims come from.",
                ],
            )
        )
    return sections


def _ensure_related(item: dict, route: str, existing_slugs: set[str]) -> None:
    related = [str(value).strip("/").removeprefix("nostr/") for value in item.get("related", []) if value]
    hub = ROUTE_HUBS.get(route, "archive-library")
    if hub in existing_slugs and hub != item.get("slug") and hub not in related:
        related.insert(0, hub)
    for _term, target in TOPIC_LINKS:
        if target in existing_slugs and target != item.get("slug") and target not in related and _term.lower() in _item_text(item).lower():
            related.append(target)
    item["related"] = related[:24]


def apply_learning_depth_pass(
    pages: list[dict],
    section,
    primary_nav_key,
    global_sources: list[tuple[str, str, str]],
    nip_sources: list[tuple[str, str, str]],
    relay_sources: list[tuple[str, str, str]],
    blossom_sources: list[tuple[str, str, str]],
    resource_links: list[tuple[str, str, str]],
) -> None:
    existing_slugs = {item.get("slug") for item in pages}
    source_by_title = _source_lookup(global_sources, nip_sources, relay_sources, blossom_sources, resource_links)
    fallback_sources = global_sources + nip_sources + resource_links

    for item in pages:
        route = primary_nav_key(item.get("slug", ""))
        _ensure_sources(item, route, source_by_title, fallback_sources)
        _ensure_related(item, route, existing_slugs)

        text_words = _words(_item_text(item))
        section_count = len(item.get("sections", []))
        source_count = len(item.get("sources", []))
        needs_depth = text_words < 1120 or section_count < 4 or source_count < 4
        if not needs_depth:
            continue
        item.setdefault("sections", []).extend(_depth_sections(item, route, existing_slugs, section))
