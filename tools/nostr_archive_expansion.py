from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tools" / "nostr_reference_inventory.json"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def load_inventory() -> dict:
    if not INVENTORY.exists():
        return {"reference_pages": [], "nostr_apps": [], "awesome_nostr": [], "nips": []}
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def source(title: str, url: str, description: str) -> tuple[str, str, str]:
    return (title, url, description)


def split_chunks(items: list, size: int) -> list[list]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def human_join(values: list[str], fallback: str = "not specified") -> str:
    values = [value for value in values if value]
    if not values:
        return fallback
    if len(values) == 1:
        return values[0]
    return ", ".join(values[:-1]) + " and " + values[-1]


def nip_kind(number: str, title: str, headings: list[str]) -> tuple[str, str]:
    text = f"{number} {title} {' '.join(headings)}".lower()
    if number in {"01", "02", "09", "10", "11", "18", "22", "25", "31", "40", "50", "51", "52"}:
        return ("social graph and event semantics", "profiles, follows, feeds, tags, lists, reactions, search or timeline behavior")
    if number in {"04", "17", "44", "59"} or "encrypt" in text or "direct message" in text:
        return ("private communication and encryption", "conversation safety, encrypted payloads, metadata limits and user consent")
    if number in {"05", "19", "21", "39"} or "identifier" in text or "bech32" in text:
        return ("identity and human-readable addressing", "names, identifiers, keys, addresses and user recognition")
    if number in {"07", "26", "46", "49", "98"} or "sign" in text or "auth" in text:
        return ("signing, login and authorization", "safer key handling, login proofs, signer permissions and authentication")
    if number in {"42", "65", "66", "86"} or "relay" in text:
        return ("relay operation and routing", "relay discovery, relay auth, routing, storage and network topology")
    if number in {"47", "57", "60", "61", "62"} or "wallet" in text or "zap" in text:
        return ("Bitcoin, Lightning and wallet flows", "zaps, wallet permissions, payment proofs and value-for-value UX")
    if number in {"23", "34", "35", "37", "54", "71", "72", "73"} or "article" in text or "community" in text:
        return ("publishing, communities and curated spaces", "long-form content, communities, groups, labels and moderated context")
    if number in {"56", "58", "72"} or "badge" in text or "report" in text or "label" in text:
        return ("trust, moderation and reputation", "reports, badges, labels, status and moderation signals")
    if number in {"92", "94", "96", "99"} or "file" in text or "media" in text or "listing" in text:
        return ("media, files and marketplaces", "attachments, file metadata, storage, listings and commerce surfaces")
    return ("specialized interoperability", "a specific convention that helps clients, relays or adjacent services understand each other")


def app_category_description(category: str) -> tuple[str, str]:
    labels = {
        "microblogging": ("Microblogging", "short notes, replies, reposts, reactions and daily social usage"),
        "photos": ("Photos", "image posting, visual feeds and creator media"),
        "streaming": ("Streaming", "live streams, live chat, zaps and real-time audience activity"),
        "blogging": ("Blogging", "long-form writing, notes, article flows and publishing archives"),
        "group-chat": ("Group chat", "group conversation, rooms, channels and local communities"),
        "community": ("Community", "membership, groups, badges, social spaces and shared context"),
        "tools": ("Tools", "utilities, relay tooling, account tools and workflow helpers"),
        "onboarding": ("Onboarding", "first-account, first-key and first-client experiences"),
        "discovery": ("Discovery", "search, recommendations, indexes, feeds and web-of-trust surfaces"),
        "video": ("Video", "video publishing, playback, streaming and media interfaces"),
        "videos": ("Videos", "video publishing, playback, streaming and media interfaces"),
        "direct-message": ("Direct message", "private messages, encrypted conversation and messaging clients"),
        "curation": ("Curation", "bookmarks, highlights, lists, feeds and knowledge organization"),
        "file-sharing": ("File sharing", "files, Blossom, media servers, storage and references"),
        "audio": ("Audio", "voice, music, podcasts, live audio and value-for-value listening"),
        "meatspace": ("Meatspace", "maps, meetups, location, events and real-world presence"),
        "marketplaces": ("Marketplaces", "commerce, listings, sats payments and buyer-seller flows"),
        "marketplace": ("Marketplaces", "commerce, listings, sats payments and buyer-seller flows"),
        "music": ("Music", "artists, tracks, listening and Lightning-native support"),
        "career": ("Career", "work, hiring, reputation and professional identity"),
        "signers": ("Signers", "key safety, NIP-07, NIP-46, bunkers and permissioned signing"),
        "media": ("Media", "publishing, storage, distribution and creative work"),
        "crazy": ("Experiments", "playful prototypes, weird apps and fringe product attempts"),
    }
    return labels.get(category, (category.replace("-", " ").title(), "a specialized part of the Nostr app ecosystem"))


DEEP_TOPICS = [
    ("portable-social-graph", "Portable Social Graph", "why followers, identity and reputation should not live inside one app database", "identity, follows, profiles, lists and client competition"),
    ("private-key-custody", "Private-Key Custody", "how Nostr turns account safety into product design", "nsec storage, signer UX, backup, recovery and permission boundaries"),
    ("npub-and-nsec", "npub and nsec", "the two strings every beginner must learn before using Nostr seriously", "public identifiers, private secrets and user-facing warnings"),
    ("relay-business-models", "Relay Business Models", "how relays can be public, paid, community-run, archival, private or venue-local", "spam resistance, storage cost, moderation rules and service reliability"),
    ("outbox-model", "Outbox Model", "why clients need better relay discovery than random global relay lists", "write relays, read relays, NIP-65 and scalable retrieval"),
    ("web-of-trust-in-practice", "Web of Trust in Practice", "how social distance can help discovery and spam filtering", "trust graphs, follows, labels, mutes and reputation"),
    ("zaps-value-for-value", "Zaps and Value-for-Value", "why tiny Lightning payments became a central cultural behavior", "zap requests, zap receipts, creator support and visible value"),
    ("nostr-wallet-connect-for-products", "Nostr Wallet Connect for Products", "how wallets can serve apps without becoming every app's backend", "permissions, limits, invoices, Lightning and NIP-47"),
    ("nip-05-for-brands", "NIP-05 for Brands", "why domain-backed identifiers matter for brands, venues and creators", "DNS proof, official identity, verification and trust signals"),
    ("remote-signing-and-bunkers", "Remote Signing and Bunkers", "how NIP-46 changes web login and key protection", "remote signers, Nostr Connect, permission requests and recovery"),
    ("long-form-publishing", "Long-Form Publishing", "how Nostr can carry articles and publishing identity", "NIP-23, Markdown, addressable events and creator archives"),
    ("media-attachments-and-blossom", "Media Attachments and Blossom", "why photos, video and files need storage beyond raw relays", "imeta, file metadata, media servers, bandwidth and moderation"),
    ("badges-status-and-reputation", "Badges, Status and Reputation", "how badges represent proof without becoming random creator inventory", "issuer trust, earned status, bought status and profile display"),
    ("lists-mutes-and-curation", "Lists, Mutes and Curation", "how user-owned lists shape feeds and moderation", "NIP-51, mute lists, curated lists, bookmarks and communities"),
    ("nostr-communities", "Nostr Communities", "why group context matters beyond a global public feed", "community posts, moderation, membership and local social spaces"),
    ("search-indexing", "Search and Indexing", "why Nostr needs search engines and indexers on top of relays", "NIP-50, profile search, note search, hashtags and spam handling"),
    ("direct-messages", "Direct Messages", "what private messaging means in a public-relay architecture", "legacy DMs, gift wraps, NIP-44, metadata and UX warnings"),
    ("auth-http-and-services", "HTTP Auth and Nostr Services", "how signed events can authorize ordinary web services", "NIP-98, service login, replay protection and scoped access"),
    ("classified-listings", "Classified Listings", "how Nostr can support marketplaces without owning one marketplace", "NIP-99, commerce, listings, sats and buyer-seller reputation"),
    ("data-vending-machines", "Data Vending Machines", "how Nostr can coordinate paid compute, AI and task marketplaces", "NIP-90, jobs, outputs, payments and machine-readable work"),
    ("decentralized-git", "Decentralized Git on Nostr", "how Git workflows can become Nostr-addressed and social", "GitWorkshop, repository identity, issues, patches and developer reputation"),
    ("nostr-for-music", "Nostr for Music", "how artists, tracks and fans fit into direct-value culture", "Wavlake, zaps, music metadata and fan support"),
    ("nostr-for-video-streaming", "Nostr for Video and Streaming", "how live media can use identity, chat and zaps", "zap.stream, Nests, media storage and audience payments"),
    ("nostr-for-photos", "Nostr for Photos", "why visual clients matter for lifestyle and creator adoption", "Olas, image feeds, imeta and creator portfolios"),
    ("nostr-for-podcasts-and-audio", "Nostr for Podcasts and Audio", "how audio apps turn listeners into signed social participants", "voice rooms, podcast clips, zaps and subscriptions"),
    ("nostr-for-forms", "Nostr for Forms", "how form tools can use signed identity and portable data", "Formstr, surveys, event registration and consent"),
    ("nostr-for-annotations", "Nostr for Annotations", "how highlights and bookmarks can become social knowledge objects", "Lantern, curation, reading trails and public references"),
    ("nostr-for-maps", "Nostr for Maps and Real Places", "how map apps and meetups connect protocol identity to physical context", "Yondar, events, venue relays and Crays World"),
    ("nostr-for-marketplaces", "Nostr for Marketplaces", "how commerce clients differ from social feeds", "Shopstr, Plebeian Market, listings, payments and trust"),
    ("nostr-for-ai-tools", "Nostr for AI Tools", "where AI builders can use signed identity and open requests", "Shakespeare, NIP-90, agents and paid tasks"),
    ("nostr-for-developers", "Nostr for Developers", "the minimum mental model before building clients or relays", "NIP-01, libraries, test relays, signatures and event validation"),
    ("nostr-for-designers", "Nostr for Designers", "how to hide protocol complexity without hiding ownership", "onboarding, signers, warnings, empty states and education"),
    ("nostr-for-creators-business", "Nostr for Creator Business", "how creators can route attention into content, access and real-world demand", "profiles, paid content, zaps, status and Crays.net"),
    ("nostr-for-fans", "Nostr for Fans", "how fans become more than anonymous traffic", "follow graph, zaps, access, badges, voting and event attendance"),
    ("nostr-for-venues", "Nostr for Venues", "how clubs, hotels and event spaces can run local context", "local relays, guest identity, bookings, POS/PMS and Super Nodes"),
    ("nostr-for-investors", "Nostr for Investors", "what capital should understand about open social infrastructure", "protocol risk, app risk, demand signals and investability"),
    ("nostr-and-open-source-funding", "Nostr and Open-Source Funding", "why grants, LTS support and Bitcoin funding shape the ecosystem", "OpenSats, public goods, maintainers and infrastructure"),
    ("nostr-and-jack-dorsey-context", "Nostr and Jack Dorsey Context", "why the Dorsey story matters but does not define the protocol", "14 BTC, open social media, funding and public attention"),
    ("nostr-vs-bluesky", "Nostr vs Bluesky", "how protocol identity, relays and account portability differ from AT Protocol assumptions", "social portability, governance, clients and infrastructure"),
    ("nostr-vs-activitypub", "Nostr vs ActivityPub", "how key-based identity differs from instance-hosted federation", "Mastodon, fediverse, relays, moderation and migration"),
    ("nostr-security-threat-model", "Nostr Security Threat Model", "the practical risks every serious product must address", "key theft, phishing, malicious clients, metadata and relay trust"),
    ("nostr-spam-and-abuse", "Nostr Spam and Abuse", "why open writing creates spam pressure and what products can do", "paid relays, filters, web-of-trust, reports and mutes"),
    ("nostr-legal-and-compliance", "Nostr Legal and Compliance", "why open protocols still require product-level legal discipline", "content policies, venues, payments, minors, consumer law and records"),
    ("nostr-seo-and-public-web", "Nostr SEO and the Public Web", "how Nostr content can be made discoverable outside clients", "long-form pages, indexes, canonical URLs and search engines"),
    ("nostr-events-history", "Nostr Events History", "how conferences and meetups turned a protocol into a culture", "Nostrica, Nostrasia, Nostriga, meetups and time capsules"),
    ("nostr-lifestyle-layer", "Nostr Lifestyle Layer", "why Nostr is also about culture, creators, places and status", "Bitcoiners, nomads, creators, hospitality and Crays lifestyle"),
    ("crays-net-as-nostr-client", "Crays.net as a Nostr Client", "how Crays.net can be a purpose-built client rather than a generic social app", "profiles, content, fans, awards, venues and governance"),
    ("crays-world-local-graph", "Crays World Local Graph", "how real venues can become local social and commercial nodes", "presence, bookings, access, local relays and hospitality"),
    ("crays-award-voting", "Crays Award Voting", "how Nostr identity can make creator voting portable and auditable", "votes, zaps, badges, profiles and campaign history"),
    ("crays-dao-readiness", "Crays DAO Readiness", "why governance should follow signed participation and earned reputation", "membership, roles, status, votes and Association rules"),
]


def make_topic_pages(page, section, global_sources, nip_sources):
    pages = []
    for slug, title, thesis, focus in DEEP_TOPICS:
        pages.append(
            page(
                f"deep-dives/{slug}",
                title,
                f"A Crays Nostr archive deep dive on {thesis}.",
                f"{title} is part of the larger Nostr picture because the protocol is not only a feed. It is a base for {focus}.",
                [
                    section("Why this topic exists", [
                        f"The internet already has social networks, messaging apps, publishing tools and payment products. Nostr matters here because it lets builders separate identity from a single operator. In the case of {title.lower()}, the relevant question is how open keys, signed events, relays and client choice change the product assumptions.",
                        f"The topic is not useful as a slogan. It is useful when a reader can connect {focus} to a real user journey: create an identity, choose a client, publish or authorize an event, route it through relays, and make it visible to the right people or services."
                    ], [
                        ("Protocol layer", "Keys and signed events create the shared base."),
                        ("Product layer", "Clients and services decide what a normal user actually sees."),
                        ("Trust layer", "Relays, lists, labels, domains and reputation shape credibility."),
                    ]),
                    section("What readers should understand", [
                        f"For this subject, the most important distinction is between what Nostr standardizes and what a product must still design. Nostr can make identity and event formats portable. It does not automatically create beautiful onboarding, legal safety, moderation quality or a business model.",
                        f"A good chapter therefore names the protocol pieces but also explains the product burden. {title} becomes practical only when key safety, relay strategy, discovery and clear labels are handled with discipline."
                    ], [
                        ("Do not over-centralize", "Avoid making the open graph dependent on one hidden service."),
                        ("Do not over-abstract", "Users still need plain language for what is public, private, paid, verified or risky."),
                        ("Do not overpromise", "A NIP or app category is a building block, not the entire market."),
                    ]),
                    section("How it appears in the current ecosystem", [
                        f"The wider Nostr ecosystem already shows this pattern in onboarding guides, app directories, project lists, signer tools and NIP documents. Crays turns those public signals into one reader-friendly explanation instead of sending you through scattered raw material.",
                        f"Because the ecosystem repeats many of the same basics, this chapter does not waste your time with another generic introduction. It focuses on the specific angle of {title.lower()} and explains why it matters in a Crays context."
                    ]),
                    section("Crays interpretation", [
                        f"For Crays, {title.lower()} matters when it helps profiles, creators, fans, venues, operators, capital and governance use one portable social graph. The Crays layer should turn abstract protocol capability into readable product paths: profile, access, content, payment, status, voting, venue presence and future DAO participation.",
                        "That also means Crays has to stay opinionated. This should never become a random dump of links. A reader should understand what belongs to the protocol, what belongs to an app, what belongs to a venue, what belongs to payments and what belongs to legal governance."
                    ]),
                    section("Questions for further research", [
                        f"Future updates should track which clients implement this topic well, which NIPs evolve, which relays or services become reliable, and which examples users actually adopt. Nostr moves quickly, so every serious archive page needs an update path."
                    ], [
                        ("Implementation", "Which NIPs or app conventions are actually used?"),
                        ("User behavior", "Do normal users understand the flow without protocol vocabulary?"),
                        ("Crays fit", "Does it strengthen creator demand, venue utility or governance readiness?"),
                    ]),
                ],
                tag="Nostr deep archive",
                sources=global_sources[:6] + nip_sources[:2],
                related=["archive-library", "nips/complete-index", "apps/catalog", "source-inventory", "nostr-and-crays"],
                keywords=[title, "Nostr deep dive", "Crays Nostr archive"],
                read="Deep archive chapter",
            )
        )
    return pages


def make_nip_inventory_pages(page, section, global_sources, nip_sources, inventory):
    nips = inventory.get("nips", [])
    pages = []
    cards = []
    for nip in nips:
        title = nip.get("title") or f"NIP-{nip.get('number')}"
        number = nip.get("number", "")
        slug = f"nips/nip-{number}"
        headings = nip.get("headings", [])
        focus, product_area = nip_kind(number, title, headings)
        cards.append((f"NIP-{number}", f"{title}. Focus: {focus}.", f"/nostr/{slug}/"))
        heading_text = human_join(headings[:5], "the core specification sections")
        pages.append(
            page(
                slug,
                f"NIP-{number}: {title}",
                f"Archive reference for NIP-{number}: what it covers, why it exists and how Crays should read it without copying the standards text.",
                f"NIP-{number} belongs to the {focus} area of Nostr. This page gives Crays readers an independent explanation and a navigation point.",
                [
                    section("What the NIP covers", [
                        f"The captured structure for this NIP points to {heading_text}. That places the document in the product area of {product_area}.",
                        "A NIP is not a landing page and not a promise that every client supports the feature. It is an interoperability document. Readers should treat it as a map of what builders may implement, not as a guarantee of consumer-ready behavior."
                    ], [
                        ("NIP number", f"NIP-{number}."),
                        ("Primary area", focus),
                        ("Implementation status", nip.get("status") or "Check the live NIP repository before implementation."),
                    ]),
                    section("Plain-language interpretation", [
                        f"In plain language, this specification helps clients, relays or services speak a more common language around {product_area}. The value is interoperability: one app can create or read a structure that another app can recognize.",
                        "The tradeoff is that interoperability by itself does not create good UX. A product still has to decide defaults, warnings, labels, recovery paths, empty states, moderation behavior and what happens when another client only partially supports the same convention."
                    ]),
                    section("Implementation questions", [
                        "Before using this NIP in a product, a team should ask whether it is stable enough, whether key material is exposed, whether relays need special support, whether the user can understand the consequence, and whether there is a fallback when support is missing.",
                        f"For a Crays product, the next question is whether NIP-{number} helps profiles, content access, status, payments, venue context, voting, governance or developer operations. If it does not serve one of those paths, it may belong in the archive but not in the first product build."
                    ], [
                        ("Client support", "Which current clients support this NIP well?"),
                        ("Relay support", "Does the feature require relay behavior beyond storage and subscriptions?"),
                        ("Security", "Does it affect signing, private messages, authentication, payments or identity?"),
                        ("Crays fit", "Does it strengthen a real Crays workflow?"),
                    ]),
                    section("Crays relevance", [
                        f"Crays should read NIP-{number} through a product lens. The goal is not to expose NIP numbers to normal users. The goal is to turn useful standards into clear actions: create a profile, follow, publish, buy access, receive a zap, show status, enter a venue, vote, authenticate or participate in future governance.",
                        "If this NIP becomes relevant to a Crays surface, the page should be expanded with implementation notes, screenshots, supported clients and tested relay behavior."
                    ]),
                ],
                tag="Nostr NIP archive",
                sources=[source(f"NIP-{number} source", nip.get("url", ""), "Primary NIP document in the nostr-protocol/nips repository.")] + global_sources[:3],
                related=["nips/complete-index", "nips", "developer-tools", "events-and-kinds", "source-inventory"],
                keywords=[f"NIP-{number}", title, focus, "Nostr NIP"],
                read="NIP reference chapter",
            )
        )
    pages.insert(
        0,
        page(
            "nips/complete-index",
            "Complete NIP Archive Index",
            f"Crays guide to {len(nips)} Nostr Implementation Possibility documents, rewritten into reader-oriented entry points.",
            "The NIP set is the standards backbone of Nostr. This Crays index makes it navigable for marketers, creators, operators and developers without turning the page into raw implementation material.",
            [
                section("How this index was built", [
                    "Every NIP page turns a technical standard into Crays product language instead of copying specification text.",
                    "The important editorial rule is separation: builders can still inspect raw implementation detail, while the reader gets a clear Crays explanation of what each standard can mean for identity, relays, clients, payments, media, trust, venues and Crays products."
                ]),
                section("All NIP chapters", [
                    "Use this index for breadth. Use individual NIP pages for interpretation. Use implementation material only when you need builder-level detail."
                ], cards=cards),
            ],
            tag="Nostr standards archive",
            sources=[source("Nostr NIPs repository", "https://github.com/nostr-protocol/nips", "Primary repository for Nostr Implementation Possibilities.")] + nip_sources,
            related=["nips", "events-and-kinds", "developer-tools", "source-inventory", "archive-library"],
            keywords=["Nostr NIPs complete index", "Nostr standards", "NIP archive"],
            read="Standards library",
        ),
    )
    return pages


def make_app_catalog_pages(page, section, global_sources, inventory):
    apps = inventory.get("nostr_apps", [])
    crays_app_card = (
        "Crays",
        "Crays.net is the Crays-facing Nostr surface: profile, creator access, status, venues, awards, payments and portable identity.",
        "https://www.crays.net",
    )
    by_category: dict[str, list[dict]] = defaultdict(list)
    for app in apps:
        for category in app.get("categories") or ["uncategorized"]:
            by_category[category].append(app)
    pages = []
    category_cards = []
    for category, category_apps in sorted(by_category.items()):
        label, description = app_category_description(category)
        category_slug = f"apps/category-{slugify(category)}"
        category_cards.append((label, f"{len(category_apps)} apps: {description}.", f"/nostr/{category_slug}/"))
        app_cards = [crays_app_card] + [(app["name"], f'{app.get("description","")} Platforms: {human_join(app.get("platforms", []))}.', f'/nostr/apps/catalog/{app["slug"]}/') for app in sorted(category_apps, key=lambda item: item["name"].lower())]
        pages.append(
            page(
                category_slug,
                f"Nostr Apps: {label}",
                f"Crays catalog page for {label.lower()} apps in the Nostr ecosystem.",
                f"The {label.lower()} category shows how Nostr moves into {description}. These products are not all direct competitors; they are evidence that one protocol can support many interfaces.",
                [
                    section("Category meaning", [
                        f"{label} apps matter because they prove that Nostr is broader than a single microblogging interface. This category is about {description}.",
                        "A directory entry is not an endorsement. It is a map point. Products may be experimental, mature, abandoned, mobile-only, web-only, open-source or commercial. The archive keeps that distinction visible while turning the catalogue into Crays context."
                    ], [
                        ("Apps in category", str(len(category_apps))),
                        ("User question", f"Does this category make {description} easier for normal users?"),
                        ("Crays question", "Can the category improve creator demand, venue utility, payment flow or reputation?"),
                    ]),
                    section("Apps in this category", [
                        "Each app has a short catalog page with its basic description, platforms, categories and links. The Crays text is independent and should be expanded when a product becomes strategically important."
                    ], cards=app_cards),
                    section("Crays interpretation", [
                        f"For Crays, the {label.lower()} category is useful when it teaches a product pattern. A Crays surface should not blindly copy these apps. It should learn which interaction model makes sense for profiles, content sale, fans, status, awards, venues and hospitality."
                    ]),
                ],
                tag="Nostr app catalog",
                sources=[source("Nostr Apps", "https://www.nostrapps.com/", "Public directory used to build the app category inventory."), source("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "Community-maintained project list.")],
                related=["apps/catalog", "app-profiles", "clients", "developer-tools", "source-inventory"],
                keywords=[f"Nostr {label}", "Nostr apps", category],
                read="App category chapter",
            )
        )
    for app in apps:
        label, description = app_category_description((app.get("categories") or ["tools"])[0])
        sources = [source("Nostr Apps listing", f'https://www.nostrapps.com/{app["slug"]}', "Public Nostr Apps listing.")]
        for link in app.get("links", [])[:4]:
            sources.append(source(link.replace("https://", "").replace("http://", "").split("/")[0], link, "Project, repository or app-store link captured from the public directory."))
        pages.append(
            page(
                f'apps/catalog/{app["slug"]}',
                app["name"],
                f"Nostr app catalog page for {app['name']}: {app.get('description','Nostr ecosystem app')}.",
                f"{app['name']} appears in the Nostr app ecosystem with the description: {app.get('description','Nostr ecosystem app')}. This archive page turns that entry into Crays context and gives you a practical evaluation point.",
                [
                    section("What the app represents", [
                        f"{app['name']} belongs to the {human_join(app.get('categories', []), 'general Nostr')} part of the app ecosystem and appears on {human_join(app.get('platforms', []), 'unspecified platforms')}.",
                        f"The relevant product lesson is {description}. For many readers, an app like this is more concrete than the protocol: it shows what signed identity and relays can become in an interface."
                    ], [
                        ("Directory description", app.get("description", "No directory description captured.")),
                        ("Platforms", human_join(app.get("platforms", []))),
                        ("Categories", human_join(app.get("categories", []))),
                    ]),
                    section("How to evaluate it", [
                        "A Nostr app should be evaluated by onboarding quality, key safety, relay strategy, feature support, moderation model, exportability and whether it makes the open graph feel useful. A beautiful interface that mishandles keys is dangerous. A technically pure tool that ordinary users cannot operate is also incomplete.",
                        f"For {app['name']}, the next editorial step is to test the product directly, record supported NIPs and note whether it is a client, signer, media tool, marketplace, discovery layer or infrastructure utility."
                    ]),
                    section("Crays relevance", [
                        "Crays should treat this app as ecosystem evidence. If the pattern helps Crays.net, Crays World, Content Sale, Crays Award, Super Nodes or future governance, it can move from catalog entry into a strategic product reference."
                    ]),
                ],
                tag="Nostr app catalog",
                sources=sources,
                related=["apps/catalog", f"apps/category-{slugify((app.get('categories') or ['tools'])[0])}", "app-profiles", "clients", "resources"],
                keywords=[app["name"], "Nostr app", human_join(app.get("categories", []))],
                read="App catalog entry",
            )
        )
    pages.insert(
        0,
        page(
            "apps/catalog",
            "Complete Nostr Apps Catalog",
            f"Crays-first map of the Nostr app market: Crays.net plus {len(apps)} tracked clients, signers, wallets, media tools, marketplaces and developer products.",
            "Start with Crays.net because that is the product layer Crays is building for its own ecosystem. Then use the rest of the catalog as market intelligence: which interfaces already exist, which patterns feel usable and which ideas belong near profiles, creators, status, venues, payments or governance.",
            [
                section("Why this catalog exists", [
                    "A serious Nostr archive needs more than protocol pages. It needs product evidence. Crays.net sits first because the point of this shelf is not to advertise everyone else before our own front door.",
                    "After that, the catalog becomes a sharp market map. Every app gets a place, but not every app gets equal weight. Some are mature clients, some are signers, some are experiments, some are clues. The Crays job is to learn from the whole field without losing its own product direction."
                ], [
                    ("Crays first", "Crays.net is the lead app card and the ecosystem entry point."),
                    ("Captured apps", str(len(apps))),
                    ("Captured categories", str(len(by_category))),
                    ("Editorial rule", "Do not copy the app directory; create independent Crays context."),
                ]),
                section("Category index", [
                    "Start by category if you want to understand the ecosystem shape. Start by app if you are checking a specific tool."
                ], cards=category_cards),
                section("App shortcuts", [
                    "Use this wall when you already know the name. Crays stays first; the rest of the market follows as a practical discovery layer."
                ], cards=[crays_app_card] + [
                    (app["name"], app.get("description", "Nostr ecosystem app"), f'/nostr/apps/catalog/{app["slug"]}/')
                    for app in apps
                ]),
            ],
            tag="Nostr app archive",
            sources=[source("Nostr Apps", "https://www.nostrapps.com/", "Public app directory used as the minimum product inventory."), source("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "Community project list used for broader context.")],
            related=["app-profiles", "apps", "clients", "developer-tools", "archive-library"],
            keywords=["Nostr apps catalog", "Nostr Apps directory", "Nostr clients"],
            read="App library",
        ),
    )
    return pages


def make_awesome_pages(page, section, inventory):
    categories = inventory.get("awesome_nostr", [])
    pages = []
    category_cards = []
    for category in categories:
        slug = f"awesome-nostr/{slugify(category['title'])}"
        links = category.get("links", [])
        category_cards.append((category["title"], f"{len(links)} links from Awesome Nostr.", f"/nostr/{slug}/"))
        cards = []
        for item in links[:160]:
            description = item.get("description") or "Awesome Nostr project or resource link."
            cards.append((item["title"], description[:240], item["url"]))
        pages.append(
            page(
                slug,
                f"Awesome Nostr: {category['title']}",
                f"Crays archive page for the Awesome Nostr category {category['title']}, with links rewritten into a reader-oriented map.",
            f"The Awesome Nostr category {category['title']} is part of the broader public project map. This page turns that map into Crays interpretation.",
                [
                    section("Category role", [
                        f"This category matters because it groups related Nostr projects around {category['title'].lower()}. It is useful for breadth: readers can see how many independent teams, tools and experiments orbit the protocol.",
                        "The Crays archive uses this as a discovery layer, not as a final judgment. Every link should be checked for activity, license, security posture and strategic relevance before becoming a product dependency."
                    ], [
                        ("Captured links", str(len(links))),
                        ("Origin", "Awesome Nostr public README."),
                        ("Archive use", "Breadth, discovery and future research backlog."),
                    ]),
                    section("Links in this category", [
                        "The cards below point to the original projects or resources. Descriptions are intentionally short because this page is a discovery map, not a replacement for testing the projects directly."
                    ], cards=cards),
                    section("Crays interpretation", [
                        "For Crays, this category can matter as infrastructure, design inspiration, partner discovery, risk monitoring or a map of where the Nostr ecosystem is already crowded."
                    ]),
                ],
                tag="Awesome Nostr archive",
                sources=[source("Awesome Nostr README", "https://github.com/aljazceru/awesome-nostr", "Community-maintained Awesome Nostr list.")],
                related=["awesome-nostr", "source-inventory", "developer-tools", "apps/catalog", "resources"],
                keywords=[category["title"], "Awesome Nostr", "Nostr resources"],
                read="Resource category",
            )
        )
    pages.insert(
        0,
        page(
            "awesome-nostr",
            "Awesome Nostr Archive",
            f"Crays index of {len(categories)} Awesome Nostr categories, rewritten as a structured research backlog for the Crays Nostr archive.",
            "Awesome Nostr is one of the most useful public maps of Nostr projects. This archive keeps its categories visible while adding a Crays lens for product, infrastructure, security and strategy.",
            [
                section("How to use this index", [
                    "Use Awesome Nostr for ecosystem breadth. Use the Crays archive for interpretation. Use primary repositories and project pages for implementation decisions.",
                    "A project appearing in Awesome Nostr is a discovery signal, not an endorsement. The next step is always source review, activity review, license check and UX/security testing."
                ]),
                section("Awesome Nostr categories", [
                    "Each category page keeps the project links together and explains how Crays should think about that slice of the ecosystem."
                ], cards=category_cards),
            ],
            tag="Nostr resource archive",
            sources=[source("Awesome Nostr README", "https://github.com/aljazceru/awesome-nostr", "Community-maintained Awesome Nostr list.")],
            related=["resources", "source-inventory", "apps/catalog", "developer-tools", "archive-library"],
            keywords=["Awesome Nostr", "Nostr project list", "Nostr ecosystem"],
            read="Resource library",
        ),
    )
    return pages


def make_source_inventory_pages(page, section, inventory):
    pages_data = [p for p in inventory.get("reference_pages", []) if p.get("status") == "ok"]
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for item in pages_data:
        by_domain[item.get("domain", "unknown")].append(item)
    domain_cards = []
    pages = []
    for domain, items in sorted(by_domain.items()):
        slug = f"source-inventory/{slugify(domain)}"
        domain_cards.append((domain, f"{len(items)} reviewed pages, headings and links.", f"/nostr/{slug}/"))
        cards = []
        for item in sorted(items, key=lambda value: value.get("title", ""))[:180]:
            headings = ", ".join(h["text"] for h in item.get("headings", [])[:4])
            desc = item.get("description") or headings or "Reviewed public page."
            cards.append((item.get("title") or item["url"], desc[:260], item["url"]))
        pages.append(
            page(
                slug,
                f"Research Map: {domain}",
                f"Crays research map for {domain}: pages, headings and links used to understand the Nostr ecosystem.",
                f"This research page documents what the crawler found on {domain}. It is not copied material; it is a working map for the Crays editors.",
                [
                    section("What was captured", [
                        f"The crawler captured {len(items)} reachable pages from {domain}. For each page it stored the URL, page title, description, visible headings and link graph. This gives the archive a concrete working map instead of vague claims.",
                        "This map keeps the Crays Nostr work maintainable. If tomorrow's chat needs to continue the work, this page and the JSON inventory show what was already reviewed."
                    ], [
                        ("Domain", domain),
                        ("Captured pages", str(len(items))),
                        ("Use", "Research map, editorial backlog and QA evidence."),
                    ]),
                    section("Captured pages", [
                        "The cards below link to the original public pages. The archive uses them as working material, then writes independent Crays explanations for readers."
                    ], cards=cards),
                ],
                tag="Nostr research map",
                sources=[source(domain, f"https://{domain}/", "Original source domain included in the user-requested minimum crawl set.")],
                related=["source-inventory", "archive-library", "resources", "awesome-nostr", "apps/catalog"],
                keywords=[domain, "Nostr research map", "Crays Nostr archive"],
                read="Research map",
            )
        )
    pages.insert(
        0,
        page(
            "source-inventory",
            "Nostr Research Map",
            f"Research map for the Crays Nostr archive: {len(pages_data)} crawled pages, {len(inventory.get('nostr_apps', []))} apps, {len(inventory.get('awesome_nostr', []))} Awesome Nostr categories and {len(inventory.get('nips', []))} NIPs.",
            "This page answers the editorial question: which material shaped the Crays Nostr library? It turns the minimum research set into a practical working map.",
            [
                section("Captured research set", [
                    "The minimum crawl set includes nostr.net, nostr.how, nostr.com, nostr.org, Nostr Apps, Nostr Login, Nostr UK and Awesome Nostr. The crawler also pulls the public NIP repository because NIPs are the standards backbone of the Nostr world.",
                    "The archive does not copy these pages. It records their structure, extracts public titles, headings, categories, apps and NIP metadata, then writes original Crays explanations for our readers."
                ], [
                    ("Reviewed pages", str(len(pages_data))),
                    ("Nostr Apps entries", str(len(inventory.get("nostr_apps", [])))),
                    ("Awesome Nostr categories", str(len(inventory.get("awesome_nostr", [])))),
                    ("NIP documents", str(len(inventory.get("nips", [])))),
                ]),
                section("Domain index", [
                    "Open a domain map when you need to inspect the captured structure behind a topic."
                ], cards=domain_cards),
            ],
            tag="Nostr research map",
            sources=[
                source("nostr.net", "https://nostr.net/", "User-requested minimum source."),
                source("nostr.how", "https://nostr.how/", "User-requested minimum source."),
                source("nostr.com", "https://nostr.com/", "User-requested minimum source."),
                source("nostr.org", "https://nostr.org/", "User-requested minimum source."),
                source("Nostr Apps", "https://www.nostrapps.com/", "User-requested minimum source."),
                source("Nostr Login", "https://www.nostrlogin.org/", "User-requested minimum source."),
                source("Nostr UK", "https://www.nostr.co.uk/", "User-requested minimum source."),
                source("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "User-requested minimum source."),
            ],
            related=["archive-library", "nips/complete-index", "apps/catalog", "awesome-nostr", "resources"],
            keywords=["Nostr research map", "Nostr crawl", "Crays Nostr map"],
            read="Research map",
        ),
    )
    return pages


def make_library_gateway(page, section, inventory):
    nips = inventory.get("nips", [])
    apps = inventory.get("nostr_apps", [])
    awesome = inventory.get("awesome_nostr", [])
    pages = [p for p in inventory.get("reference_pages", []) if p.get("status") == "ok"]
    category_counts = Counter(category for app in apps for category in app.get("categories", []))
    top_category_cards = []
    for category, count in category_counts.most_common(18):
        label, description = app_category_description(category)
        top_category_cards.append((label, f"{count} apps: {description}.", f"/nostr/apps/category-{slugify(category)}/"))
    reading_cards = [
        ("Beginner path", "What is Nostr, getting started, keys, clients, relays, zaps and glossary.", "/nostr/reading-paths/beginner/"),
        ("Developer path", "NIP-01, NIPs, relays, signers, wallet connect, HTTP auth and research map.", "/nostr/reading-paths/developer/"),
        ("Creator path", "Creators, content sale, zaps, long-form, media, music, badges and Crays.net.", "/nostr/reading-paths/creator/"),
        ("Operator path", "Venues, Super Nodes, relay business models, local graph, POS/PMS and governance.", "/nostr/reading-paths/operator/"),
        ("Culture path", "Jack Dorsey, events, lifestyle, Bitcoin overlap, music, video and open-source funding.", "/nostr/reading-paths/culture/"),
        ("Research path", "Research map, Awesome Nostr, Nostr Apps catalog and complete NIP index.", "/nostr/reading-paths/research/"),
    ]
    return [
        page(
            "archive-library",
            "Crays Nostr Archive Library",
            "The full Crays Nostr archive: research map, complete NIP map, app catalog, Awesome Nostr map, deep dives, people, culture and Crays product interpretation.",
            "This is the gateway for the expanded Nostr archive. The target is not a quick blog article. It is a library: enough organized, non-repeating material for many hours of reading and continued editorial expansion.",
            [
                section("Archive scale", [
                    f"The current library contains {len(pages)} reviewed ecosystem pages, {len(nips)} NIP documents, {len(apps)} Nostr Apps entries and {len(awesome)} Awesome Nostr categories. The generated archive turns that material into navigable chapters rather than one endless wall of text.",
                    "The editorial rule is simple: do not duplicate public pages. Each chapter should answer a distinct reader question and connect the topic to Crays only where the connection is real."
                ], [
                    ("Reading target", "12+ hours across the full archive, without artificial repetition."),
                    ("Structure", "Pillar pages, NIP pages, app catalog pages, research maps and deep dives."),
                    ("Archive discipline", "Every major section has a clear job in the reader journey."),
                ]),
                section("Reading paths", [
                    "Different readers need different routes. A creator should not be forced through every NIP first. A developer should not start with marketing language. A venue operator needs the local graph and Super Node path."
                ], cards=reading_cards),
                section("Largest app categories", [
                    "The app landscape is one of the clearest signals that Nostr is no longer just microblogging. The category index shows where builders are spending energy."
                ], cards=top_category_cards),
                section("Core library shelves", [
                    "Use the shelves below as the serious archive entry points."
                ], cards=[
                    ("Complete NIP index", "All NIP documents with independent Crays explanations.", "/nostr/nips/complete-index/"),
                    ("Complete app catalog", "Nostr app entries, categories and app pages.", "/nostr/apps/catalog/"),
                    ("Awesome Nostr archive", "Awesome Nostr categories transformed into research shelves.", "/nostr/awesome-nostr/"),
                    ("Research map", "A map of the ecosystem branches behind the archive.", "/nostr/source-inventory/"),
                    ("Deep dives", "Topic chapters from keys to venues, AI and DAO readiness.", "/nostr/deep-dives/portable-social-graph/"),
                    ("People", "Builders, developers, founders, funders and public contributors.", "/nostr/people/"),
                ]),
            ],
            tag="Nostr archive library",
            sources=[
                source("Nostr protocol repository", "https://github.com/nostr-protocol/nostr", "Original protocol repository."),
                source("Nostr NIPs", "https://github.com/nostr-protocol/nips", "Primary standards repository."),
                source("Nostr Apps", "https://www.nostrapps.com/", "Public app directory."),
                source("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "Community project list."),
                source("nostr.how", "https://nostr.how/", "Onboarding and education reference."),
                source("Nostr Login", "https://www.nostrlogin.org/", "Signer and login reference."),
            ],
            related=["source-inventory", "nips/complete-index", "apps/catalog", "awesome-nostr", "what-is-nostr"],
            keywords=["Nostr archive library", "complete Nostr archive", "Crays Nostr"],
            read="12+ hour archive",
        )
    ]


def make_reading_path_pages(page, section):
    paths = [
        ("beginner", "Beginner Reading Path", "Start here if Nostr is new.", ["what-is-nostr", "getting-started", "keys-identity", "clients", "relays", "nip-57-zaps-lightning", "glossary"]),
        ("developer", "Developer Reading Path", "Start here if you need implementation structure.", ["events-and-kinds", "nips/complete-index", "developer-tools", "nips/nip-01", "nip-07-signers", "nip-46-remote-signing", "nip-98-http-auth"]),
        ("creator", "Creator Reading Path", "Start here if you care about audience, content and value.", ["creators", "content-sale", "nip-23-long-form", "nip-57-zaps-lightning", "music-video-media", "deep-dives/badges-status-and-reputation", "deep-dives/crays-net-as-nostr-client"]),
        ("operator", "Operator and Venue Reading Path", "Start here if you care about real places.", ["operators-venues", "crays-super-node", "deep-dives/relay-business-models", "deep-dives/crays-world-local-graph", "deep-dives/nostr-for-venues", "dao-governance"]),
        ("culture", "Culture Reading Path", "Start here if you care about the movement around Nostr.", ["lifestyle-culture", "events", "jack-dorsey", "nostr-and-bitcoin", "deep-dives/nostr-events-history", "deep-dives/nostr-and-open-source-funding"]),
        ("research", "Research Reading Path", "Start here if you want the research map.", ["source-inventory", "awesome-nostr", "apps/catalog", "nips/complete-index", "resources"]),
    ]
    label_map = {
        "source-inventory": "Research map",
        "awesome-nostr": "Awesome Nostr archive",
        "apps/catalog": "Complete app catalog",
        "nips/complete-index": "Complete NIP index",
        "what-is-nostr": "What is Nostr?",
        "nip-57-zaps-lightning": "Zaps and Lightning",
        "nip-23-long-form": "Long-form publishing",
        "nip-07-signers": "NIP-07 signers",
        "nip-46-remote-signing": "Remote signing",
        "nip-98-http-auth": "HTTP auth",
        "deep-dives/crays-net-as-nostr-client": "Crays.net as Nostr client",
        "deep-dives/crays-world-local-graph": "Crays World local graph",
        "deep-dives/nostr-for-venues": "Nostr for venues",
        "deep-dives/nostr-and-open-source-funding": "Open-source funding",
        "deep-dives/nostr-events-history": "Nostr events history",
        "deep-dives/badges-status-and-reputation": "Badges, status and reputation",
        "nips/nip-01": "NIP-01 basic protocol",
    }
    pages = []
    for slug, title, intro, links in paths:
        cards = []
        for item in links:
            label = label_map.get(item, item.replace("-", " ").replace("/", " / ").title())
            cards.append((label, "Open this chapter in the reading path.", f"/nostr/{item}/"))
        pages.append(
            page(
                f"reading-paths/{slug}",
                title,
                f"{title}: {intro}",
                intro,
                [
                    section("How to read this path", [
                        "This path is curated so readers do not drown in the archive. It moves from the easiest framing to deeper material and keeps each step focused.",
                        "You can read straight through or use it as a checklist. The full archive remains available when you need the research map, app catalogs or individual NIPs."
                    ]),
                    section("Chapters", [
                        "Open the chapters below in order for the smoothest route."
                    ], cards=cards),
                ],
                tag="Nostr reading path",
                sources=[],
                related=["archive-library", "source-inventory", "resources", "what-is-nostr"],
                keywords=[title, "Nostr reading path", "Crays Nostr archive"],
                read="Reading path",
            )
        )
    return pages


def make_expansion_pages(page, section, global_sources, nip_sources):
    inventory = load_inventory()
    pages = []
    pages.extend(make_library_gateway(page, section, inventory))
    pages.extend(make_source_inventory_pages(page, section, inventory))
    pages.extend(make_nip_inventory_pages(page, section, global_sources, nip_sources, inventory))
    pages.extend(make_app_catalog_pages(page, section, global_sources, inventory))
    pages.extend(make_awesome_pages(page, section, inventory))
    pages.extend(make_topic_pages(page, section, global_sources, nip_sources))
    pages.extend(make_reading_path_pages(page, section))
    return pages
