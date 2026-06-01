from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
INVENTORY = ROOT / "tools" / "nostr_reference_inventory.json"
OPENVERSE_IMAGE_BANK = ROOT / "tools" / "nostr_openverse_image_bank.json"
DEEP_RESEARCH_INVENTORY = ROOT / "tools" / "nostr_deep_research_inventory.json"
SEARCH_INDEX = PUBLIC / "nostr" / "search-index.json"
BASE_URL = "https://www.crays.org"
TODAY = "2026-05-31"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def clean_generated_html(text: str) -> str:
    return re.sub(r"[ \t]+(?=\r?\n|$)", "", text)


INTERNAL_LINK_HOSTS = {"crays.org", "www.crays.org"}
ANCHOR_TAG_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>", re.IGNORECASE)
HREF_ATTR_RE = re.compile(r"""\bhref\s*=\s*(['"])(?P<href>.*?)\1""", re.IGNORECASE)
TARGET_ATTR_RE = re.compile(r"""\btarget\s*=\s*(['"])(?P<target>.*?)\1""", re.IGNORECASE)
REL_ATTR_RE = re.compile(r"""\brel\s*=\s*(['"])(?P<rel>.*?)\1""", re.IGNORECASE)


def is_external_href(href: str) -> bool:
    parsed = urlparse(href)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() not in INTERNAL_LINK_HOSTS


def ensure_external_links_new_tab(markup: str) -> str:
    def patch_anchor(match: re.Match[str]) -> str:
        tag = match.group(0)
        href_match = HREF_ATTR_RE.search(tag)
        if not href_match or not is_external_href(href_match.group("href")):
            return tag

        target_match = TARGET_ATTR_RE.search(tag)
        if target_match:
            quote = target_match.group(1)
            tag = TARGET_ATTR_RE.sub(f"target={quote}_blank{quote}", tag, count=1)
        else:
            tag = tag[:-1] + ' target="_blank">'

        rel_match = REL_ATTR_RE.search(tag)
        if rel_match:
            quote = rel_match.group(1)
            rel_tokens = rel_match.group("rel").split()
            rel_lookup = {token.lower() for token in rel_tokens}
            for required in ("noreferrer", "noopener"):
                if required not in rel_lookup:
                    rel_tokens.append(required)
            tag = REL_ATTR_RE.sub(f"rel={quote}{' '.join(rel_tokens)}{quote}", tag, count=1)
        else:
            tag = tag[:-1] + ' rel="noreferrer noopener">'
        return tag

    return ANCHOR_TAG_RE.sub(patch_anchor, markup)


COPY_REPLACEMENTS = (
    (r"\bcomprehensive guide\b", "guide"),
    (r"\bcomprehensive collection\b", "large collection"),
    (r"\bcomprehensive introduction\b", "clear introduction"),
    (r"\bcomprehensive resource\b", "broad resource"),
    (r"\bcomprehensive\b", "broad"),
    (r"\brobust\b", "solid"),
    (r"\bseamless\b", "smooth"),
    (r"\bcutting-edge\b", "new"),
    (r"\btransformative\b", "meaningful"),
    (r"\bpivotal\b", "important"),
    (r"\bleverage\b", "use"),
    (r"\bunlock\b", "open up"),
    (r"\belevate\b", "improve"),
    (r"\bdelve\b", "look closely"),
    (r"\brealm\b", "world"),
    (r"\btapestry\b", "mix"),
)


def clean_copy(value: object) -> str:
    text = str(value)
    for pattern, replacement in COPY_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def crays_voice(value: object) -> str:
    text = clean_copy(value)
    text = re.sub(r"\bCrays\.net\b", "Crays", text, flags=re.IGNORECASE)
    replacements = (
        (r"\bWhy Crays cares\b", "Why we care"),
        (r"\bThe Crays read\b", "How this fits our map"),
        (r"\bThe Crays reading\b", "Our practical reading"),
        (r"\bThe Crays angle\b", "Our angle"),
        (r"\bCrays relevance\b", "Why it matters to us"),
        (r"\bHow Crays should read\b", "How we should read"),
        (r"\bHow Crays uses this\b", "How we use this"),
        (r"\bWhat Crays should carry forward\b", "What we should carry forward"),
        (r"\bThe Crays reader\b", "our reader"),
        (r"\bThe Crays readers\b", "our readers"),
        (r"\bCrays readers\b", "our readers"),
        (r"\bCrays reader\b", "our reader"),
        (r"\bIt tells Crays\b", "It tells us"),
        (r"\bThis tells Crays\b", "This tells us"),
        (r"\bFor Crays,\s*", "For us, "),
        (r"\bfor Crays\b", "for us"),
        (r"\bto Crays\b", "to us"),
        (r"\bat Crays\b", "with us"),
        (r"\bCrays does not\b", "we do not"),
        (r"\bCrays doesn't\b", "we do not"),
        (r"\bCrays should\b", "we should"),
        (r"\bCrays can\b", "we can"),
        (r"\bCrays cannot\b", "we cannot"),
        (r"\bCrays could\b", "we could"),
        (r"\bCrays will\b", "we will"),
        (r"\bCrays must\b", "we must"),
        (r"\bCrays wants\b", "we want"),
        (r"\bCrays needs\b", "we need"),
        (r"\bCrays uses\b", "we use"),
        (r"\bCrays offers\b", "we offer"),
        (r"\bCrays provides\b", "we provide"),
        (r"\bCrays explains\b", "we explain"),
        (r"\bCrays reads\b", "we read"),
        (r"\bCrays treats\b", "we treat"),
        (r"\bCrays turns\b", "we turn"),
        (r"\bCrays builds\b", "we build"),
        (r"\bCrays has\b", "we have"),
        (r"\bCrays is\b", "we are"),
        (r"\bThe Crays archive\b", "Our archive"),
        (r"\bCrays archive\b", "our archive"),
        (r"\bThe Crays route\b", "our route"),
        (r"\bCrays route\b", "our route"),
        (r"\bThe Crays layer\b", "our layer"),
        (r"\bCrays layer\b", "our layer"),
        (r"\bCrays product\b", "our product"),
        (r"\bCrays products\b", "our products"),
        (r"\bCrays profile\b", "our profile"),
        (r"\bCrays profiles\b", "our profiles"),
        (r"\bCrays ecosystem\b", "our ecosystem"),
        (r"\bCrays implementation\b", "our implementation"),
        (r"\bCrays interpretation\b", "our interpretation"),
        (r"\bCrays context\b", "our context"),
        (r"\bCrays lifestyle\b", "our lifestyle"),
        (r"\bThe Crays job\b", "Our job"),
        (r"\bCrays job\b", "our job"),
        (r"\bThe Crays version\b", "Our version"),
        (r"\bCrays version\b", "our version"),
        (r"\bThe Crays copy\b", "Our copy"),
        (r"\bCrays copy\b", "our copy"),
        (r"\bThe Crays stance\b", "Our stance"),
        (r"\bCrays stance\b", "our stance"),
        (r"\bCrays view\b", "our view"),
        (r"\bCrays model\b", "our model"),
        (r"\bCrays stack\b", "our stack"),
        (r"\bCrays pages\b", "our pages"),
        (r"\bCrays page\b", "our page"),
        (r"\bCrays text\b", "our text"),
        (r"\bCrays chapter\b", "our chapter"),
        (r"\bCrays chapters\b", "our chapters"),
        (r"\bCrays explanations\b", "our explanations"),
        (r"\bCrays explanation\b", "our explanation"),
        (r"\bCrays sources\b", "our sources"),
        (r"\bCrays source\b", "our source"),
    )
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\bthe our\b", "our", text, flags=re.IGNORECASE)
    text = re.sub(r"\ba our\b", "our", text, flags=re.IGNORECASE)
    if text.startswith("we "):
        text = "We " + text[3:]
    if text.startswith("our "):
        text = "Our " + text[4:]
    return text


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "section"


GLOBAL_SOURCES = [
    ("Nostr protocol repository", "https://github.com/nostr-protocol/nostr", "Original protocol repository and protocol rationale."),
    ("Nostr NIPs", "https://github.com/nostr-protocol/nips", "Implementation possibilities, event kinds and client-relay standards."),
    ("nostr.how", "https://nostr.how/", "Plain-language guides for keys, clients, relays, zaps and onboarding."),
    ("nostr.com", "https://nostr.com/", "Broad overview of the open Nostr communication commons."),
    ("nostr.org", "https://nostr.org/", "Introductory resource with clients, relays and protocol explanation."),
    ("Nostr Apps", "https://www.nostrapps.com/", "Directory of clients, tools, relays, servers and creator apps."),
    ("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "Community-maintained list of projects and resources built on Nostr."),
    ("Nostr Login", "https://www.nostrlogin.org/", "Nostr login, NIP-07, NIP-46 and signer-oriented onboarding."),
    ("Nostr UK", "https://www.nostr.co.uk/", "Learning hub with clients, relays, NIPs, events and developer pages."),
]


NIP_SOURCES = [
    ("NIP-01", "https://github.com/nostr-protocol/nips/blob/master/01.md", "Basic protocol flow, events, signatures and relay messages."),
    ("NIP-05", "https://github.com/nostr-protocol/nips/blob/master/05.md", "DNS-based identifiers for Nostr public keys."),
    ("NIP-07", "https://github.com/nostr-protocol/nips/blob/master/07.md", "Browser window.nostr capability for public keys, signing and encryption."),
    ("NIP-19", "https://github.com/nostr-protocol/nips/blob/master/19.md", "bech32 display formats such as npub, nsec, note, nevent and naddr."),
    ("NIP-23", "https://github.com/nostr-protocol/nips/blob/master/23.md", "Long-form article events using Markdown."),
    ("NIP-42", "https://github.com/nostr-protocol/nips/blob/master/42.md", "Client authentication to relays."),
    ("NIP-44", "https://github.com/nostr-protocol/nips/blob/master/44.md", "Versioned encrypted payloads."),
    ("NIP-46", "https://github.com/nostr-protocol/nips/blob/master/46.md", "Remote signing and Nostr Connect."),
    ("NIP-47", "https://github.com/nostr-protocol/nips/blob/master/47.md", "Nostr Wallet Connect for Lightning wallet access."),
    ("NIP-50", "https://github.com/nostr-protocol/nips/blob/master/50.md", "Search capability for relays and clients."),
    ("NIP-51", "https://github.com/nostr-protocol/nips/blob/master/51.md", "Public and private lists."),
    ("NIP-57", "https://github.com/nostr-protocol/nips/blob/master/57.md", "Lightning zaps."),
    ("NIP-58", "https://github.com/nostr-protocol/nips/blob/master/58.md", "Badge definitions, awards and displayed profile badges."),
    ("NIP-65", "https://github.com/nostr-protocol/nips/blob/master/65.md", "Relay list metadata."),
    ("NIP-94", "https://github.com/nostr-protocol/nips/blob/master/94.md", "File metadata events."),
    ("NIP-96", "https://github.com/nostr-protocol/nips/blob/master/96.md", "HTTP file storage integration."),
    ("NIP-98", "https://github.com/nostr-protocol/nips/blob/master/98.md", "HTTP authentication with Nostr events."),
]


RESOURCE_LINKS = GLOBAL_SOURCES + NIP_SOURCES + [
    ("start.nostr.net", "https://start.nostr.net/", "Starter resource linked from the nostr.net ecosystem."),
    ("relay.nostr.net", "https://relay.nostr.net/", "Relay resource linked from the nostr.net ecosystem."),
    ("wot.nostr.net", "https://wot.nostr.net/", "Web-of-trust oriented Nostr resource."),
    ("Damus", "https://damus.io/", "iOS Nostr client."),
    ("Amethyst", "https://www.amethyst.social/", "Android Nostr client."),
    ("Primal", "https://primal.net/downloads", "Nostr client and media experience for web and mobile."),
    ("Coracle", "https://coracle.social/", "Web client and community-oriented Nostr interface."),
    ("Habla", "https://nostrapps.com/habla", "Long-form publishing client."),
    ("Nostur", "https://www.nostur.com/", "iOS Nostr client."),
    ("Snort", "https://snort.social/", "Web Nostr client."),
    ("Nostrudel", "https://nostrudel.ninja/", "Power-user Nostr web client."),
    ("YakiHonne", "https://yakihonne.com/", "Multi-platform Nostr publishing and social client."),
    ("Nostrica", "https://nostrica.com/", "Nostr unconference and culture archive."),
    ("Nostr World", "https://nostr.world/", "Nostriga and Nostr unconference material."),
    ("Wavlake", "https://wavlake.com/", "Open creator-listener music ecosystem connected to value-for-value culture."),
    ("Nostr.band GitHub", "https://github.com/nostrband", "Public Nostr.band organization and related tools."),
    ("Alby", "https://getalby.com/", "Lightning wallet and browser extension commonly used for Nostr signing and zaps."),
    ("GitHub topic: Nostr", "https://github.com/topics/nostr", "Fresh open-source repositories tagged with Nostr."),
    ("Crays Circle GitHub", "https://github.com/crayscircle", "Public Crays Circle GitHub organization for code, implementation references and developer context."),
]

RELAY_MARKET_SOURCES = [
    ("Nostr.watch relay finder", "https://nostr.watch/relays/find", "Live relay finder and speed/health surface for known relays."),
    ("BigBrotr", "https://bigbrotr.com/", "Relay discovery, monitoring, archiving, analytics and NIP-66-style observability."),
    ("Nostr.co.uk relay directory", "https://nostr.co.uk/relays/", "Curated relay directory with public, paid, specialized and regional examples."),
    ("NostrList", "https://nostrlist.com/", "Curated Nostr ecosystem directory covering clients, tools, relays and services."),
    ("nostr.info relay query", "https://nostr.info/relayr/", "Relay query and inspection surface."),
    ("NIP-11 Relay Information", "https://github.com/nostr-protocol/nips/blob/master/11.md", "Relay metadata and self-described capabilities."),
    ("NIP-65 Relay List Metadata", "https://github.com/nostr-protocol/nips/blob/master/65.md", "User relay list metadata for read/write discovery."),
    ("NIP-66 Relay Discovery", "https://github.com/nostr-protocol/nips/blob/master/66.md", "Relay discovery and liveness monitoring events."),
]

SAFEBOX_SOURCES = [
    ("Safebox repository", "https://github.com/trbouma/safebox", "Primary Safebox repository with README, app code, docs and current status."),
    ("Safebox Phase 3 proposal", "https://github.com/trbouma/safebox/blob/main/docs/PHASE3-PROPOSAL.md", "Current public proposal linked from the Safebox README."),
    ("Safebox initial proposal", "https://github.com/trbouma/safebox/blob/main/docs/INITIAL-PROPOSAL.md", "Earlier funding and product framing for Safebox."),
    ("Safebox specs directory", "https://github.com/trbouma/safebox/tree/main/docs/specs", "Protocol and architecture specifications for records, Cashu, Blossom, NFC, vault and security flows."),
    ("Safebox Blossom spec", "https://github.com/trbouma/safebox/blob/main/docs/specs/BLOSSOM-BLOB-STORAGE-AND-TRANSFER.md", "Safebox blob storage and transfer design notes."),
    ("Safebox Cashu storage spec", "https://github.com/trbouma/safebox/blob/main/docs/specs/CASHU-STORAGE-AND-MULTI-MINT.md", "Safebox Cashu and multi-mint storage design notes."),
]

FOUNDUPS_SOURCES = [
    ("FoundUPS website", "https://foundups.com/", "Primary FoundUPS website with compute-focus positioning."),
    ("Foundups-Agent repository", "https://github.com/FOUNDUPS/Foundups-Agent", "Primary repository for FoundUPS Agent, WSP/WRE and agent orchestration code."),
    ("FoundUPS LitePaper", "https://github.com/FOUNDUPS/Foundups-Agent/blob/main/public/litepaper.html", "Public LitePaper source in the Foundups-Agent repository."),
    ("Foundups-Agent architecture docs", "https://github.com/FOUNDUPS/Foundups-Agent/blob/main/docs/ARCHITECTURE.md", "Architecture documentation for the agent system."),
    ("FoundUPS vision docs", "https://github.com/FOUNDUPS/Foundups-Agent/blob/main/docs/foundups_vision.md", "Vision document for FoundUPS framing and lifecycle."),
    ("Foundups-Agent competitive analysis", "https://github.com/FOUNDUPS/Foundups-Agent/blob/main/docs/competitive_analysis.md", "Public competitive analysis linked from the repository README."),
]

BLOSSOM_SOURCES = [
    ("Blossom repository", "https://github.com/hzrd149/blossom", "Primary Blossom repository and BUD index."),
    ("BUD-01 server requirements", "https://github.com/hzrd149/blossom/blob/master/buds/01.md", "Core Blossom HTTP server behavior and blob retrieval rules."),
    ("BUD-02 blob upload", "https://github.com/hzrd149/blossom/blob/master/buds/02.md", "Upload endpoint, blob descriptor, sha256 handling and server responses."),
    ("BUD-03 user server list", "https://github.com/hzrd149/blossom/blob/master/buds/03.md", "Nostr-published list of a user's preferred Blossom servers."),
    ("BUD-11 Nostr authorization", "https://github.com/hzrd149/blossom/blob/master/buds/11.md", "Nostr signed authorization tokens for Blossom server actions."),
    ("NIP-94 file metadata", "https://github.com/nostr-protocol/nips/blob/master/94.md", "File metadata events and hash, URL, MIME, size and fallback references."),
    ("NIP-96 HTTP file storage", "https://github.com/nostr-protocol/nips/blob/master/96.md", "Adjacent HTTP file storage API intended for Nostr clients."),
    ("route96", "https://github.com/v0l/route96", "A public Blossom/NIP-96 server implementation reference."),
]


NOSTR_MEDIA_ARTICLE_ARCHIVE = [
    {
        "title": "Beyond the Feed: Nostr's Real-World Potential",
        "source": "CryptoRank",
        "author": "CryptoRank news desk",
        "url": "https://cryptorank.io/news/feed/430a2-beyond-the-feed-nostr-real-world",
        "category": "Real-world adoption",
        "use": "Use this when you want the non-feed framing: Nostr as identity, payments, publishing and public infrastructure rather than only another social timeline.",
    },
    {
        "title": "The Power of Nostr",
        "source": "Lyn Alden",
        "author": "Lyn Alden",
        "url": "https://www.lynalden.com/the-power-of-nostr/",
        "category": "Long-form analysis",
        "use": "A strong macro-level essay for readers who need the internet-history and protocol-sovereignty context before going deeper into keys, relays and clients.",
    },
    {
        "title": "Jack Dorsey gives decentralized social network Nostr 14 BTC in funding",
        "source": "CoinDesk",
        "author": "George Kaloudis",
        "url": "https://www.coindesk.com/tech/2022/12/15/jack-dorsey-gives-decentralized-social-network-nostr-14-btc-in-funding",
        "category": "Funding and public signal",
        "use": "Useful for understanding why Dorsey's support became an early mainstream signal without mistaking Nostr for a Dorsey-owned product.",
    },
    {
        "title": "Damus, another decentralized social networking app, arrives to take on Twitter",
        "source": "TechCrunch",
        "author": "Sarah Perez",
        "url": "https://techcrunch.com/2023/02/01/damus-another-decentralized-social-networking-app-arrives-to-take-on-twitter/",
        "category": "Mainstream app coverage",
        "use": "Shows how Damus introduced Nostr to a broader app-store and social-media audience.",
    },
    {
        "title": "Jack Dorsey pumps $10M into a nonprofit focused on open-source social media",
        "source": "TechCrunch",
        "author": "Sarah Perez",
        "url": "https://techcrunch.com/2025/07/16/jack-dorsey-pumps-10m-into-a-nonprofit-focused-on-open-source-social-media/",
        "category": "Open social funding",
        "use": "Good context for the broader open-social funding arc around Nostr and related tools.",
    },
    {
        "title": "The Nostr Fund",
        "source": "OpenSats",
        "author": "OpenSats",
        "url": "https://opensats.org/funds/nostr",
        "category": "Public-good funding",
        "use": "The cleanest funding map for readers who want to see which Nostr builders, clients, relays and libraries receive public-good support.",
    },
    {
        "title": "Nostr protocol repository",
        "source": "GitHub",
        "author": "Nostr protocol contributors",
        "url": "https://github.com/nostr-protocol/nostr",
        "category": "Primary technical source",
        "use": "Use this as the root source when an article needs to separate protocol truth from media shorthand.",
    },
    {
        "title": "Nostr Implementation Possibilities",
        "source": "GitHub",
        "author": "NIP contributors",
        "url": "https://github.com/nostr-protocol/nips",
        "category": "Standards",
        "use": "The source shelf for NIP pages, event kinds, signer behavior, zaps, relays, encryption and file metadata.",
    },
    {
        "title": "nostr.how",
        "source": "nostr.how",
        "author": "nostr.how contributors",
        "url": "https://nostr.how/",
        "category": "Learning guide",
        "use": "A practical onboarding source for users learning keys, clients, relays, NIP-05, zaps and safer habits.",
    },
    {
        "title": "Nostr Apps",
        "source": "Nostr Apps",
        "author": "Nostr Apps maintainers",
        "url": "https://www.nostrapps.com/",
        "category": "App directory",
        "use": "A discovery layer for readers who want clients, signers, wallets, relays, Blossom servers, media apps and experiments.",
    },
    {
        "title": "Crays Circle GitHub",
        "source": "GitHub",
        "author": "Crays Circle",
        "url": "https://github.com/crayscircle",
        "category": "Crays implementation",
        "use": "The public code and organization door for readers who want to connect the Crays Nostr thesis with implementation work, developer context and future open repositories.",
    },
    {
        "title": "Awesome Nostr",
        "source": "GitHub",
        "author": "Awesome Nostr maintainers",
        "url": "https://github.com/aljazceru/awesome-nostr",
        "category": "Ecosystem list",
        "use": "A broad repository-style map for tools, libraries, clients, relays, resources and community links.",
    },
    {
        "title": "Nostr World",
        "source": "Nostr World",
        "author": "Nostr World organizers",
        "url": "https://nostr.world/",
        "category": "Events and talks",
        "use": "The public door into Nostrica, Nostrasia, Nostriga and the live event culture around the protocol.",
    },
    {
        "title": "Nostrica",
        "source": "Nostrica",
        "author": "Nostrica organizers",
        "url": "https://nostrica.com/",
        "category": "Conference archive",
        "use": "Useful for seeing Nostr as a scene of builders, unconferences and cultural memory, not just code.",
    },
    {
        "title": "Primal launches new social network for digital freedom",
        "source": "PR Newswire",
        "author": "Primal",
        "url": "https://www.prnewswire.com/news-releases/primal-launches-new-social-network-for-digital-freedom-301877265.html",
        "category": "App launch",
        "use": "Good for understanding the consumer-app and product-polish side of Nostr through Primal.",
    },
    {
        "title": "Nostr UK learning hub",
        "source": "Nostr UK",
        "author": "Nostr UK",
        "url": "https://nostr.co.uk/",
        "category": "Learning and directory",
        "use": "A practical collection for UK-oriented learning, relays, NIPs, events and developer material.",
    },
]


EXCEL_SOURCE_URL_FIXUPS = [
    ("Hello Nostr resources", "Exact workbook URL preserved for search and source traceability: https://hellonostr.dev/en/resources/", "https://hellonostr.dev/en/resources/"),
    ("Nostr Post Checker", "Exact workbook URL preserved for search and source traceability: https://koteitan.github.io/nostr-post-checker/", "https://koteitan.github.io/nostr-post-checker/"),
    ("nostorg clients", "Exact workbook URL preserved for search and source traceability: https://nostorg.github.io/clients/", "https://nostorg.github.io/clients/"),
    ("Nostr UK clients", "Exact workbook URL preserved for search and source traceability: https://nostr.co.uk/clients/", "https://nostr.co.uk/clients/"),
    ("Nostr UK relays", "Exact workbook URL preserved for search and source traceability: https://nostr.co.uk/relays/", "https://nostr.co.uk/relays/"),
    ("NostrApps direct message category", "Exact workbook URL preserved for search and source traceability: https://nostrapps.com/?category=Direct%20Message", "https://nostrapps.com/?category=Direct%20Message"),
    ("NostrApps file sharing category", "Exact workbook URL preserved for search and source traceability: https://nostrapps.com/?category=File%20Sharing", "https://nostrapps.com/?category=File%20Sharing"),
    ("NostrApps group chat category", "Exact workbook URL preserved for search and source traceability: https://nostrapps.com/?category=Group%20Chat", "https://nostrapps.com/?category=Group%20Chat"),
    ("Nostr Book kinds", "Exact workbook URL preserved for search and source traceability: https://nostrbook.dev/kinds/", "https://nostrbook.dev/kinds/"),
    ("Nostr developer guide", "Exact workbook URL preserved for search and source traceability: https://nostrcg.github.io/devguide/", "https://nostrcg.github.io/devguide/"),
    ("Nostr Compass newsletters", "Exact workbook URL preserved for search and source traceability: https://nostrcompass.org/en/newsletters/", "https://nostrcompass.org/en/newsletters/"),
    ("Nostr Compass projects", "Exact workbook URL preserved for search and source traceability: https://nostrcompass.org/en/projects/", "https://nostrcompass.org/en/projects/"),
    ("Nostr Design relays", "Exact workbook URL preserved for search and source traceability: https://nostrdesign.org/docs/how-to/relays/", "https://nostrdesign.org/docs/how-to/relays/"),
    ("nostr-rs-relay sourcehut", "Exact workbook URL preserved for search and source traceability: https://sr.ht/~gheartsfield/nostr-rs-relay/", "https://sr.ht/~gheartsfield/nostr-rs-relay/"),
    ("Forbes guide to Nostr", "Exact workbook URL preserved for search and source traceability: https://www.forbes.com/sites/digital-assets/2024/07/17/your-guide-to-nostr-the-decentralized-network-for-everything/", "https://www.forbes.com/sites/digital-assets/2024/07/17/your-guide-to-nostr-the-decentralized-network-for-everything/"),
    ("No Bullshit Bitcoin Primal v2.0", "Exact workbook URL preserved for search and source traceability: https://www.nobsbitcoin.com/primal-v2-0/", "https://www.nobsbitcoin.com/primal-v2-0/"),
    ("Reddit r/nostr", "Exact workbook URL preserved for search and source traceability: https://www.reddit.com/r/nostr/", "https://www.reddit.com/r/nostr/"),
]


NOSTR_VIDEO_ARCHIVE = [
    {"id": "5W-jtbbh3eA", "title": "What is Nostr?", "channel": "lnbits", "category": "Start", "use": "Two-minute first-contact explainer for readers who need the simplest mental model before reading."},
    {"id": "0YDj1QdL2Zs", "title": "Jack Dorsey explains how Nostr works in 2 minutes", "channel": "Primal", "category": "Start", "use": "Fast mainstream signal: useful for readers who know Dorsey but do not yet understand relays and clients."},
    {"id": "yIccRIEr2gQ", "title": "Nostr Explained Visually for Beginners", "channel": "Rhett Reisman - Level Up Your Brain", "category": "Start", "use": "Visual overview for people who learn better from diagrams and analogies before opening a long article."},
    {"id": "NVm_jGdwTjQ", "title": "Nostr for Beginners w/ Derek Ross", "channel": "NOSTR WORLD", "category": "Start", "use": "Longer beginner walkthrough with community context and practical vocabulary."},
    {"id": "Czkv54pQfTI", "title": "How To Get Started With Nostr", "channel": "Castig", "category": "Start", "use": "Setup-oriented video for readers ready to create an account and test a client."},
    {"id": "kifwECtwjJQ", "title": "Create Your NOSTR Account - Beginner Tutorial", "channel": "Max DeMarco", "category": "Start", "use": "Useful when the reader has understood the idea and now needs the first account flow."},
    {"id": "zteh-aHb4cM", "title": "WATCH This Before Starting Nostr (Safety and Privacy Tips!!)", "channel": "CoinGecko", "category": "Privacy", "use": "Good safety checkpoint before a new user pastes secrets into random clients."},
    {"id": "K5oXaW1EqbE", "title": "How Nostr is pro-censorship", "channel": "fiatjaf", "category": "Governance", "use": "Useful for correcting the lazy myth that open protocols mean no moderation or no policy choices."},
    {"id": "T5ETKXjJdZA", "title": "Do nostr relays store your data?", "channel": "David King", "category": "Relays", "use": "Short relay-focused answer for readers confused about what relays actually remember."},
    {"id": "uzdHdkKwPYE", "title": "{Nostr} NIP-05 Verification on a Custom Domain", "channel": "theBTCcourse", "category": "Privacy", "use": "Hands-on identity verification tutorial for domain-backed NIP-05 names."},
    {"id": "53huU8mg2eo", "title": "What Is Nostr Wallet Connect and Why Does It Matter?", "channel": "Kevin Rooke", "category": "Wallets", "use": "Short bridge into NIP-47 and why wallet permissions should be modular."},
    {"id": "S6y2Vy2N9oY", "title": "NOSTR TOOLKIT: Linking To Your Own Lightning Node With Voltage", "channel": "BTC Sessions", "category": "Wallets", "use": "Deep practical route for advanced users connecting Lightning infrastructure to Nostr."},
    {"id": "Kuqs4bYGEEk", "title": "Nostr Start Guide for Beginners | Account setup & wallet connect for Zaps", "channel": "ForrestHODL", "category": "Wallets", "use": "Bridges onboarding with wallet connect and zaps in one beginner-friendly flow."},
    {"id": "o-KIsRYbAAY", "title": "What is a Zap on Nostr?", "channel": "THE Bitcoin Podcast with Walker", "category": "Wallets", "use": "Very short zap definition for readers who only need the concept before moving on."},
    {"id": "FYbQLja9Oe8", "title": "What are zaps in Nostr/Damus?", "channel": "David King", "category": "Wallets", "use": "Practical zap explanation close to the Damus user experience."},
    {"id": "4qOVxq9lUbs", "title": "Build your First Nostr App by Super Testnet", "channel": "High Level Bitcoin", "category": "Apps", "use": "Developer entry point for readers who want to turn protocol ideas into a working app."},
    {"id": "Tbt3jL1Ms0w", "title": "Nostr - Wouter Constant - FOSDEM 2025", "channel": "fiatjaf", "category": "NIPs", "use": "Conference-level technical context for readers who want the broader protocol and implementation discussion."},
    {"id": "eQjzxIKBsTY", "title": "The NOSTR Protocol", "channel": "Bitcoin Magazine", "category": "NIPs", "use": "Protocol conversation that works well after the reader knows keys, relays and clients."},
    {"id": "NqPIyD5yWEA", "title": "BR048 - Nostr: Coracle, Damus, NDK, Snort, Primal, DVMs + MORE", "channel": "Bitcoin Review Podcast with NVK & Guests", "category": "Apps", "use": "Product-builder roundtable for comparing clients, tooling and DVM experiments."},
    {"id": "xv3JSZo-y0c", "title": "BR044 - Nostr: Primal, Highlighter, Damus, Zapstream, Mutiny, NIP90/52 + MORE", "channel": "Bitcoin Review Podcast with NVK & Guests", "category": "Apps", "use": "Useful for readers mapping app categories and experiments beyond a simple feed."},
    {"id": "Ua64ymE6KQ0", "title": "Bitcoin and Nostr w/ Jack Mallers and Miljan", "channel": "NOSTR WORLD", "category": "Commerce", "use": "Good bridge between Bitcoin payment culture, Primal and Nostr's user-facing value flow."},
    {"id": "SSFVR5ZXOuA", "title": "Nostr: All Your Silos Are Broken", "channel": "BTCPrague", "category": "People", "use": "Panel view into the builder scene: Martti Malmi, Aleksandar Svetski, PabloF7z, Miljan and Derek Ross."},
    {"id": "WOYum10HaxY", "title": "Nostr World: Nostrica Q&A", "channel": "Derek Ross", "category": "People", "use": "Good event-history material for readers who want to understand the early public scene."},
    {"id": "u_U2obseVwY", "title": "How to Start with Nostr Today | Presentation", "channel": "Oslo Freedom Forum", "category": "People", "use": "Short talk-style onboarding with human-rights and freedom-tech framing."},
    {"id": "1y7zi3t1aNM", "title": "Saving Private Nostr", "channel": "NOSTR WORLD", "category": "Privacy", "use": "Useful privacy follow-up after the reader has understood public-key identity."},
    {"id": "VrHoprrAops", "title": "How to Earn Bitcoin on Nostr with Primal", "channel": "Pioneers of Bitcoin", "category": "Commerce", "use": "Creator-commerce entry for readers asking how Nostr can produce money flow, not only posts."},
    {"id": "Tw2-H_Ie8tE", "title": "Replay #9 - Nostr & Fountain: decentralized music streaming", "channel": "Patrice Lazareff", "category": "Media", "use": "Useful for readers mapping Nostr, music, podcasts and streaming use cases."},
    {"id": "634DvERKauA", "title": "How Nostr Works And The Mind-Blowing Implications For Freedom & Prosperity", "channel": "John Vallis - Bitcoin Rapid-Fire", "category": "Governance", "use": "Long-form conversation for readers who want the political-economy layer around open social protocols."},
]


def section(
    title: str,
    paragraphs: list[str],
    bullets: list[tuple[str, str]] | None = None,
    cards: list[tuple[str, str]] | None = None,
    videos: list[dict] | None = None,
):
    return {
        "title": title,
        "paragraphs": paragraphs,
        "bullets": bullets or [],
        "cards": cards or [],
        "videos": videos or [],
    }


def page(slug: str, title: str, deck: str, intro: str, sections: list[dict], *, tag: str = "Nostr archive", sources=None, related=None, keywords=None, read="12 min read"):
    return {
        "slug": slug,
        "title": title,
        "deck": deck,
        "intro": intro,
        "tag": tag,
        "sections": sections,
        "sources": sources or GLOBAL_SOURCES,
        "related": related or [],
        "keywords": keywords or [],
        "read": read,
    }


def load_deep_research_inventory() -> dict:
    if not DEEP_RESEARCH_INVENTORY.exists():
        return {"sources": [], "summary": {}, "unique_urls": 0, "url_cells": 0}
    return json.loads(DEEP_RESEARCH_INVENTORY.read_text(encoding="utf-8"))


DEEP_RESEARCH = load_deep_research_inventory()


def source_display_title(item: dict) -> str:
    names = [str(name).strip() for name in item.get("primary_names", []) if str(name).strip()]
    if names:
        return names[0]
    fetch_title = item.get("fetch", {}).get("title", "")
    if fetch_title:
        return str(fetch_title)
    return urlparse(item.get("url", "")).netloc.replace("www.", "") or item.get("url", "Nostr source")


def source_category_label(item: dict) -> str:
    values = [str(value).strip() for value in item.get("categories", []) + item.get("subcategories", []) if str(value).strip()]
    return " / ".join(values[:2]) if values else "Nostr source"


def deep_research_source_cards() -> list[tuple[str, str, str]]:
    cards: list[tuple[str, str, str]] = []
    for item in DEEP_RESEARCH.get("sources", []):
        row_refs = item.get("row_refs", [])
        row_note = f"{len(row_refs)} workbook signal" + ("" if len(row_refs) == 1 else "s")
        status = item.get("fetch", {}).get("status", "not checked")
        url = item.get("url", "")
        cards.append((
            source_display_title(item),
            f"{source_category_label(item)}. {row_note}. URL: {url}. Audit status: {status}.",
            url,
        ))
    return cards


def grouped_deep_research_source_cards() -> dict[str, list[tuple[str, str, str]]]:
    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for card, item in zip(deep_research_source_cards(), DEEP_RESEARCH.get("sources", [])):
        category = source_category_label(item).split(" / ")[0]
        groups[category or "Nostr source"].append(card)
    return dict(sorted(groups.items(), key=lambda pair: pair[0].lower()))


READING_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


def replace_crays_net_display(value: object) -> str:
    return re.sub(r"\bCrays\.net\b", "Crays", str(value), flags=re.IGNORECASE)


def reading_words(value: object) -> int:
    text = html.unescape(replace_crays_net_display(value))
    text = re.sub(r"<[^>]+>", " ", text)
    return len(READING_WORD_RE.findall(text))


def estimate_reading_label(item: dict) -> str:
    words = (
        reading_words(item.get("title", ""))
        + reading_words(item.get("deck", ""))
        + reading_words(item.get("intro", ""))
    )
    for sec in item.get("sections", []):
        words += reading_words(sec.get("title", ""))
        for paragraph in sec.get("paragraphs", []):
            words += reading_words(paragraph)
        for bullet in sec.get("bullets", []):
            words += sum(reading_words(part) for part in bullet[:2])
        for card in sec.get("cards", []):
            words += sum(reading_words(part) for part in card[:2])
        for video in sec.get("videos", []):
            words += reading_words(video.get("title", ""))
            words += reading_words(video.get("channel", ""))
            words += reading_words(video.get("note", ""))
            words += reading_words(video.get("use", ""))
    minutes = max(2, (words + 219) // 220)
    return f"{minutes} min read"


def normalize_page_display_copy(item: dict) -> None:
    for field in ("title", "deck", "intro", "tag", "quick_label", "related_label"):
        if item.get(field):
            item[field] = replace_crays_net_display(item[field])
    item["keywords"] = [replace_crays_net_display(keyword) for keyword in item.get("keywords", [])]
    normalized_sections = []
    for sec in item.get("sections", []):
        normalized = dict(sec)
        normalized["title"] = replace_crays_net_display(normalized.get("title", ""))
        normalized["paragraphs"] = [replace_crays_net_display(paragraph) for paragraph in normalized.get("paragraphs", [])]
        normalized["bullets"] = [
            tuple(replace_crays_net_display(part) for part in bullet)
            for bullet in normalized.get("bullets", [])
        ]
        normalized_cards = []
        for card in normalized.get("cards", []):
            if len(card) >= 3:
                normalized_cards.append((replace_crays_net_display(card[0]), replace_crays_net_display(card[1]), card[2]))
            elif len(card) == 2:
                normalized_cards.append((replace_crays_net_display(card[0]), replace_crays_net_display(card[1])))
            else:
                normalized_cards.append(tuple(replace_crays_net_display(part) for part in card))
        normalized["cards"] = normalized_cards
        normalized["videos"] = [
            {
                **video,
                "title": replace_crays_net_display(video.get("title", "")),
                "channel": replace_crays_net_display(video.get("channel", "")),
                "note": replace_crays_net_display(video.get("note", "")),
                "use": replace_crays_net_display(video.get("use", "")),
                "category": replace_crays_net_display(video.get("category", "")),
            }
            for video in normalized.get("videos", [])
        ]
        normalized_sections.append(normalized)
    item["sections"] = normalized_sections
    normalized_sources = []
    for source in item.get("sources", []):
        if len(source) >= 3:
            normalized_sources.append((replace_crays_net_display(source[0]), source[1], replace_crays_net_display(source[2])))
        else:
            normalized_sources.append(tuple(source))
    item["sources"] = normalized_sources
    item["read"] = estimate_reading_label(item)


def nip_page(slug: str, nip: str, name: str, what: str, solves: str, implementation: str, crays: str, risks: str, related=None):
    source = [src for src in NIP_SOURCES if src[0] == nip] + [NIP_SOURCES[0], GLOBAL_SOURCES[1]]
    return page(
        slug,
        f"{nip}: {name}",
        f"A Crays archive page for {nip}, explaining what it does, where it fits in Nostr and why it matters for identity, apps, relays and real-world systems.",
        what,
        [
            section("What it standardizes", [
                solves,
                f"The important thing to understand is that {nip} is not an app feature by itself. It is a shared convention. A client, relay, wallet, signer or adjacent service can implement the convention, ignore it, implement only part of it, or hide it behind a simpler user experience.",
                "That is why a NIP page needs two layers: the technical shape builders must respect, and the product consequence a normal reader can feel."
            ], [
                ("Protocol layer", f"{nip} defines a pattern for interoperable behavior, not a closed product."),
                ("Interoperability", "The value is that different apps can understand the same signed data or request shape."),
                ("Optionality", "Support can vary by client, relay and service, so products need fallbacks and clear messaging."),
            ]),
            section("Data shape and moving parts", [
                implementation,
                "Read the moving parts in this order: who signs, what object is created, which fields or tags carry meaning, where the object is published, what relays or services have to support it, and how a second client can verify or interpret the result later.",
                "This sequence matters because Nostr problems often look like UX problems at the surface while the real failure is lower down: a missing tag, a relay policy mismatch, a signer permission, a stale relay list, a wallet limit, an unsupported event kind or an indexer that never saw the event."
            ], [
                ("Signer boundary", "Which key signs the event or request, and should a dedicated signer handle it?"),
                ("Relay boundary", "Does the relay merely store/forward, or must it enforce authentication, search, policy or retention?"),
                ("Client boundary", "What must the user see so the feature feels understandable instead of protocol-shaped?"),
                ("Fallback boundary", "What happens when another app, relay or wallet does not support this convention yet?"),
            ]),
            section("Product consequence for us", [
                crays,
                f"For us, {nip} matters only when it improves a real flow: identity, publishing, access, value transfer, media, venue context, reputation, moderation, governance or developer operations. If it does not help one of those flows, it can stay in the archive until the product need is real.",
                "The user should not have to memorize the NIP number. The product should translate the convention into plain actions: verify a profile, sign safely, publish content, receive a zap, connect a wallet, prove status, enter a space, vote, or recover context across apps."
            ], [
                ("Crays", "Profiles, creator pages and social proof need portable identity rather than a closed account table."),
                ("Crays World", "Real venues need local context, member state, reputation and payments that can survive app changes."),
                ("Governance path", "Future governance needs signed identity, membership context and auditable participation signals."),
            ]),
            section("Risks, edge cases and implementation discipline", [
                risks,
                "The edge cases are where a standard becomes a product decision. A feature can be technically valid and still confuse users, leak metadata, create moderation problems, increase key exposure, break search, overload relays or make payments feel unreliable.",
                f"Before shipping anything based on {nip}, test current client support, relay behavior, signer permissions, failure states, abuse cases and the exact words shown to a non-technical user. If the wording cannot be made simple, the implementation is probably not ready for a mainstream Crays surface."
            ], [
                ("Do not overpromise", "A NIP gives a shared format. It does not magically solve onboarding, moderation, UX or custody."),
                ("Keep private keys away", "Any feature that increases private-key exposure increases the attack surface."),
                ("Make support visible", "A reader should know whether the feature works everywhere, only in some clients, or only with specific relays/services."),
                ("Use plain language", "Most users need outcomes: login, pay, publish, vote, prove status, access a venue."),
            ]),
        ],
        sources=source,
        related=related or ["nips", "events-and-kinds", "developer-tools", "privacy-security"],
        keywords=[nip, name, "Nostr NIP", "Crays Nostr"],
        read="9 min read",
    )


PAGES = [
    page(
        "what-is-nostr",
        "What is Nostr?",
        "The friendly first chapter for Nostr: keys, clients, relays, events, NIPs, zaps, apps, culture and the Crays layer, without the protocol fog.",
        "Nostr is an open protocol for signed social data. Think of it as social media with the account pulled out of one company's basement. You hold a key. Apps become windows. Relays carry signed events. The interesting part is that your identity can move.",
        [
            section("The shortest useful definition", [
                "Nostr stands for Notes and Other Stuff Transmitted by Relays. Cute name, slightly chaotic, very Nostr. The part that matters is simpler: your public key is your identity, your private key signs what you do, clients show the experience, and relays decide what they store or pass along.",
                "That makes Nostr feel less like another app and more like a shared internet language. Twitter, Instagram, TikTok and LinkedIn keep the account, graph and rules inside one company. Nostr splits those jobs apart, so different apps can show different experiences over the same signed data."
            ], [
                ("Public key", "The durable identity people can share, search and recognize."),
                ("Private key", "The signing secret. Lose it and you can lose the account; leak it and someone else can become you."),
                ("Client", "The app or website where the whole thing becomes usable."),
                ("Relay", "The server that receives, stores, filters or forwards signed events."),
            ]),
            section("What Nostr is not", [
                "Nostr is not a blockchain. Notes are not mined into blocks, and the protocol does not need a native token to exist. Bitcoin and Lightning can plug in where payments, zaps and settlement make sense, but the social layer itself is just signed events moving through relays.",
                "It is also not a magical no-rules zone. Clients and relays still make choices. Users pick relays, mute lists, communities and apps. The difference is that the network effect does not have to sit under one company's thumb."
            ], [
                ("Not one app", "Damus, Amethyst, Primal, Coracle, Iris and other clients can all read from the same protocol."),
                ("Not one server", "Clients may publish to multiple relays and read from different relay sets."),
                ("Not one algorithm", "Discovery is shaped by clients, follows, search, relays, web-of-trust and user preferences."),
            ]),
            section("Why Crays cares", [
                "Crays is not interested in building a lonely login box with a prettier logo. It needs a social base that can connect creator profiles, content access, fan demand, status badges, venue presence, Crays Award voting, Lightning payments and future DAO participation without trapping the whole story in one closed platform.",
                "Crays.net can be the front door. Nostr can be the portable identity and signed signal underneath it. Bitcoin and Lightning can move value. Crays World and Super Nodes can carry that identity into real places, where a fan, creator or operator should not have to start from zero every time an app changes."
            ], [
                ("Creators", "Portable profiles, fans, content links, status and payments."),
                ("Fans", "One identity that can follow, buy, access, vote and build reputation."),
                ("Venues", "Local relays, local services, memberships, access and hospitality context."),
                ("Capital", "Cleaner signals for demand, reputation and participation."),
            ]),
            section("How to read this archive", [
                "Treat this archive like a book with side doors. If you are new, start with keys, clients and relays. If you build, go toward events, NIPs, signers and wallet flows. If you care about the scene, follow zaps, creators, events, music, media and the Bitcoin overlap. The Crays pages show how the same protocol ideas become commerce, hospitality and governance tools."
            ], cards=[
                ("Start here", "Read getting started, keys and identity, then clients."),
                ("Deep tech", "Read events, NIPs, signers, relays, encryption, wallet connect and file metadata."),
                ("Culture", "Read lifestyle, events, zaps, music, video and Jack Dorsey context."),
                ("Crays layer", "Read Nostr and Crays, Content Sale, Crays Award, Super Nodes and DAO governance."),
            ]),
        ],
        related=["getting-started", "keys-identity", "clients", "relays", "nips", "nostr-and-crays"],
        keywords=["what is Nostr", "Nostr protocol", "Nostr guide", "Crays Nostr"],
        read="14 min read",
    ),
    page(
        "why-nostr",
        "Why Nostr Matters",
        "Why an open social protocol matters for creators, builders, venues, Bitcoin users, capital and communities that do not want platform lock-in.",
        "The point of Nostr is not novelty. The point is structural independence. If identity, follows, reputation and social proof are portable, a user is less dependent on one platform's database, one algorithm or one policy change.",
        [
            section("The platform problem", [
                "Modern social platforms are excellent distribution machines, but they also concentrate accounts, audiences, moderation, monetization rules and discovery inside one operator. That creates fragility for creators and businesses. A profile can be throttled, banned, shadowed, demonetized or forced into changing formats.",
                "Nostr attacks the lock-in problem at the identity layer. It does not promise that every app will be good. It makes it possible for many apps to exist while the user remains the same cryptographic identity."
            ], [
                ("Audience portability", "Followers and social context do not have to start from zero in each app."),
                ("Client competition", "A better interface can emerge without owning the whole network."),
                ("Relay diversity", "Storage, reach and moderation can become plural rather than monopolized."),
                ("Payment optionality", "Lightning zaps can connect value directly to social events."),
            ]),
            section("Why it is especially relevant now", [
                "The public internet is moving through a trust crisis: closed APIs, bot traffic, content moderation fights, creator monetization pressure and AI-generated noise. In that environment, signed events and user-owned keys are not just technical details. They are a way to prove authorship and build portable trust.",
                "Nostr will not solve every social problem. It gives builders a common substrate: signed identity, messages, relay distribution, optional encryption, optional payments, lists, badges, long-form content and machine-readable references."
            ]),
            section("Why it matters to Crays", [
                "Crays is not trying to build another isolated social app. It needs a base layer for a network that touches digital profiles, creator monetization, award voting, hospitality access, real venues, reputation, payments and future governance. A normal platform account is too small for that job.",
                "Nostr gives the portable graph. Crays adds product design, commerce, physical venues, Super Nodes, Lightning flows, Crays World, Crays Award and the Association frame."
            ], [
                ("Real-world bridge", "The same identity can move from profile to venue."),
                ("Shared demand", "Creator audiences, fans and operators can meet in one graph."),
                ("Investable context", "Signals can become clearer when demand, status and participation are signed."),
            ]),
            section("Where the challenge remains", [
                "Onboarding, private-key custody, spam resistance, legal moderation, search quality, client UX and user education are still hard. The best Nostr products hide the protocol complexity without hiding the user's ownership."
            ]),
        ],
        related=["what-is-nostr", "nostr-and-bitcoin", "privacy-security", "moderation-discovery", "nostr-and-crays"],
        keywords=["why Nostr", "decentralized social protocol", "portable social graph"],
    ),
    page(
        "getting-started",
        "Getting Started with Nostr",
        "A careful onboarding guide for new users: keys, signers, clients, relays, NIP-05 identifiers, zaps and the mistakes to avoid.",
        "A good Nostr start is simple: create or import a key safely, use a signer when possible, choose a client, publish to a few relays, add a readable identifier and learn the difference between public and private data.",
        [
            section("Step 1: understand keys before posting", [
                "A Nostr account is a key pair. Your public key is what people can use to find you. Your private key signs events. Treat the private key like a root credential. A platform password can usually be reset. A Nostr private key cannot be casually reset by a help desk.",
                "For most people, the safest onboarding is not pasting a private key into every web client. Use a reputable browser signer, mobile signer, remote signer or app flow that keeps the secret away from random websites."
            ], [
                ("Back up carefully", "Use a password manager or secure key storage before you build a reputation on the key."),
                ("Avoid key reuse in unknown apps", "A client that asks for a private key is receiving enormous power."),
                ("Learn npub and nsec", "npub is public. nsec is private. Never post an nsec."),
            ]),
            section("Step 2: choose a client", [
                "A client is the interface. Mobile users may start with Damus, Amethyst, Primal, Nos or Nostur. Web users may explore Coracle, Snort, Iris, Nostrudel, Habla or YakiHonne. The right choice depends on whether you want a social feed, long-form writing, media, power tools or creator publishing."
            ], [
                ("Start with one simple client", "Do not overwhelm yourself with ten apps on day one."),
                ("Add a second client later", "The magic appears when the same identity can move across interfaces."),
                ("Use directories", "Nostr Apps and Awesome Nostr are useful for finding specialized tools."),
            ]),
            section("Step 3: understand relays", [
                "Relays are servers. Clients send signed events to relays and ask relays for events. Some relays are public, some paid, some community-specific, some archival, some search-oriented and some private. Relay choice affects reach, speed, retention and moderation."
            ]),
            section("Step 4: add a human-readable identity", [
                "NIP-05 maps a Nostr public key to a DNS-based identifier that looks like an email address. It is not a password and not a custody model. It helps people recognize that a public key belongs to a name or domain."
            ]),
            section("Step 5: use zaps with care", [
                "Zaps connect Lightning payments to social interactions. They are culturally important because they make value-for-value behavior visible. But they still require wallet setup, fee awareness and basic payment hygiene."
            ]),
        ],
        sources=[GLOBAL_SOURCES[2], GLOBAL_SOURCES[7], GLOBAL_SOURCES[5], GLOBAL_SOURCES[6]] + NIP_SOURCES[:4] + [NIP_SOURCES[11]],
        related=["keys-identity", "clients", "relays", "nip-05-identifiers", "nip-57-zaps-lightning"],
        keywords=["Nostr getting started", "Nostr onboarding", "Nostr keys", "Nostr client"],
    ),
    page(
        "keys-identity",
        "Nostr Keys and Identity",
        "How public keys, private keys, signatures, npub/nsec, NIP-05 and signers create a portable identity layer.",
        "Nostr identity starts with cryptographic keys. The public key is the stable identifier. The private key signs actions. Every serious Nostr product has to make this power usable without turning key management into a user-hostile ceremony.",
        [
            section("Public key as identity", [
                "A public key is globally unique and portable. It is not issued by a platform. That is the base reason Nostr can support multiple clients over one social graph.",
                "The user can show an npub format to humans, while software can store and verify the underlying key format."
            ]),
            section("Private key as signing authority", [
                "The private key is not merely a login password. It is the authority to sign events as that identity. If it is stolen, an attacker can impersonate the user. If it is lost and no recovery model exists, the reputation attached to that identity can be stranded."
            ], [
                ("Do not paste blindly", "Pasting secrets into web pages is the weak onboarding path."),
                ("Prefer signers", "NIP-07 and NIP-46 reduce exposure when implemented well."),
                ("Explain consequences", "Products should tell users what access they are granting."),
            ]),
            section("Readable names with NIP-05", [
                "NIP-05 connects a Nostr key to a DNS-based identifier. For brands and organizations, this matters because a domain can help users recognize an identity. For Crays, domain-backed identifiers can make creator, venue and Association identities easier to understand."
            ]),
            section("Crays identity design", [
                "Crays should treat Nostr identity as a portable root, not as a gimmick. The user may begin with a Crays.net profile, then use the same identity for follows, content access, fan status, venue context, award voting and future governance participation."
            ]),
        ],
        sources=[NIP_SOURCES[0], NIP_SOURCES[1], NIP_SOURCES[2], NIP_SOURCES[3], GLOBAL_SOURCES[7], GLOBAL_SOURCES[2]],
        related=["nip-19-addresses", "nip-05-identifiers", "nip-07-signers", "nip-46-remote-signing", "privacy-security"],
        keywords=["Nostr keys", "Nostr identity", "npub", "nsec", "NIP-05"],
    ),
    page(
        "clients",
        "Nostr Clients",
        "A map of Nostr clients, what they do and how to choose between mobile, web, desktop, creator and power-user experiences.",
        "A Nostr client is the app people touch. The client does not own the protocol. It reads and writes signed events through relays and shapes the user experience on top.",
        [
            section("Client categories", [
                "The Nostr client universe is broad because the protocol can carry many kinds of events. Some clients feel like social feeds. Others are long-form publishing tools, media apps, chat surfaces, developer dashboards, marketplaces, search tools or power-user consoles."
            ], [
                ("Mobile social", "Damus, Amethyst, Primal, Nos, Nostur and related apps introduce users to daily social posting."),
                ("Web social", "Coracle, Snort, Iris, Nostrudel and Primal web show how the same identity can work in browsers."),
                ("Publishing", "Habla and YakiHonne point toward long-form and creator workflows."),
                ("Power tools", "Nostrudel, nak and relay tooling serve developers and advanced operators."),
            ]),
            section("Choosing a first client", [
                "A first client should make key safety and posting simple. A second client should demonstrate portability. If a user signs into another client and still sees follows, posts or profile context, the Nostr idea becomes tangible."
            ]),
            section("What clients compete on", [
                "Clients compete on onboarding, relay strategy, search, moderation, feed design, wallet integration, notifications, media support, communities, long-form publishing and signer integration. They should not compete by trapping the identity."
            ]),
            section("Crays client logic", [
                "Crays.net should behave like a purpose-built Nostr client for the Crays ecosystem: profile, content, access, fan demand, status, award voting and venue routes. It can be opinionated without pretending to own the whole graph."
            ]),
        ],
        sources=[GLOBAL_SOURCES[4], GLOBAL_SOURCES[5], GLOBAL_SOURCES[6], GLOBAL_SOURCES[2]],
        related=["apps", "relays", "nostr-login", "creators", "nostr-and-crays"],
        keywords=["Nostr clients", "Damus", "Amethyst", "Primal", "Coracle", "Nostr apps"],
    ),
    page(
        "relays",
        "Nostr Relays",
        "How relays store, filter, reject, authenticate, monetize and distribute signed events in Nostr.",
        "Relays are the server side of Nostr, but they are not a single platform server. Clients can connect to multiple relays. Relays can choose rules, business models, storage policies and communities.",
        [
            section("What a relay does", [
                "A relay receives signed events from clients and responds to client subscriptions. It can store data, filter data, reject events, require authentication, charge for write access, support search or serve a specific community. Relays are deliberately simpler than giant centralized social platforms."
            ], [
                ("Public relay", "Open reach, usually more spam pressure."),
                ("Paid relay", "Payment can reduce spam and fund infrastructure."),
                ("Community relay", "A group or venue can define membership and rules."),
                ("Archival relay", "Storage and history become the main service."),
                ("Search relay", "Indexing and query quality become the product."),
            ]),
            section("Relay choice is product design", [
                "A client with poor relay defaults can feel empty or noisy. A client with thoughtful relay strategy can feel fast and coherent. NIP-65 relay list metadata helps users advertise where they write and where they prefer to receive mentions."
            ]),
            section("Moderation and association", [
                "Because relays are privately operated, they can reject content according to their rules. Clients can select relays and apply their own filters. That creates a plural moderation model: no single universal feed, but also no single universal censor."
            ]),
            section("Crays venue relays", [
                "A Crays Super Node can turn a venue into a local relay and service layer. That matters for guests, creators, staff, access, payments and local demand. The venue is no longer only a location. It becomes a node in the social and commercial network."
            ]),
        ],
        sources=[NIP_SOURCES[0], NIP_SOURCES[13], NIP_SOURCES[5], GLOBAL_SOURCES[3], GLOBAL_SOURCES[4]],
        related=["relay-market-directory", "nip-65-relay-list", "nip-42-relay-auth", "crays-super-node", "operators-venues", "moderation-discovery"],
        keywords=["Nostr relays", "relay list metadata", "paid relays", "Crays Super Node"],
    ),
    page(
        "relay-market-directory",
        "Nostr Relay Market Directory",
        "Where to find current Nostr relays, paid relays, public relays, specialized relays, relay health, NIP-11 metadata and relay discovery signals.",
        "The live relay market does not live in one perfect official list. It is spread across relay finders, monitors, curated directories, NIP-11 metadata, NIP-65 user relay lists and newer NIP-66 monitoring data. Crays needs all of those surfaces close to the reader because relay choice changes the whole experience.",
        [
            section("Current relay discovery surfaces", [
                "For a current market view, start with live relay finders and observatories rather than a frozen article list. Nostr.watch is commonly referenced for browsing known relays and checking speed. BigBrotr pushes the idea further into discovery, monitoring, archiving, analytics and machine-readable access. Curated directories such as Nostr.co.uk and NostrList are useful because they add human labels: public, paid, specialized, regional, search, article, WoT or community relays."
            ], cards=[
                ("Nostr.watch", "Live relay finder for known relays, speed and availability context.", "https://nostr.watch/relays/find"),
                ("BigBrotr", "Network observatory for discovery, monitoring, analytics and NIP-66-style relay data.", "https://bigbrotr.com/"),
                ("Nostr.co.uk Relays", "Curated public, paid, specialized and regional relay directory.", "https://nostr.co.uk/relays/"),
                ("NostrList", "Curated ecosystem directory with relay and service listings.", "https://nostrlist.com/"),
                ("nostr.info Relay Query", "Relay query and inspection surface for practical checks.", "https://nostr.info/relayr/"),
                ("Nostr.band Relay", "Search and discovery relay often used for broader feed coverage.", "https://relay.nostr.band/"),
            ]),
            section("What counts as the relay market", [
                "A relay market is not only a table of WebSocket URLs. It includes free public relays, paid anti-spam relays, search relays, article relays, community relays, private relays, venue relays, inbox relays, filter relays, caching relays and regional relays. A serious Nostr guide should show the categories, the tradeoffs and the live places where readers can inspect what is available today."
            ], [
                ("Public relays", "Easy to join, useful for reach, often exposed to more spam and uneven reliability."),
                ("Paid relays", "A payment wall can fund service and reduce spam, but it creates access and trust questions."),
                ("Specialized relays", "Search, long-form, WoT filtering, media, inbox, caching and community behavior can be the whole product."),
                ("Local relays", "Venue, club, city or event relays can make Nostr useful in physical places."),
            ]),
            section("Metadata and monitoring standards", [
                "NIP-11 is the relay's public information card: name, description, supported NIPs, limits, contact, software and payment signals. NIP-65 tells clients where a user writes and where mentions should be sent. NIP-66 moves toward independent relay discovery and liveness monitoring, so relay quality becomes less anecdotal and more measurable."
            ], cards=[
                ("NIP-11 relay information", "The self-described info document every serious relay should expose.", "/nostr/nips/nip-11/"),
                ("NIP-65 relay lists", "User read/write relay metadata for outbox and mention discovery.", "/nostr/nip-65-relay-list/"),
                ("NIP-66 monitoring", "Relay discovery and liveness events for measured relay quality.", "/nostr/nips/nip-66/"),
                ("Relay auth", "NIP-42 authentication for paid, private and membership-aware relay access.", "/nostr/nip-42-relay-auth/"),
            ]),
            section("Crays relevance", [
                "Crays cannot treat relays as invisible plumbing. Relay selection affects profile reach, content availability, venue access, award signals, member reputation, creator commerce and future governance. The Crays route should therefore expose relay directories, relay standards and Crays-specific venue relay strategy as first-class reading paths."
            ], cards=[
                ("Relay selection field guide", "How relay choice changes speed, reach, storage and signal quality.", "/nostr/field-guide/relay-selection/"),
                ("Relay business models", "Public, paid, community, archival, private and venue-local relay economics.", "/nostr/deep-dives/relay-business-models/"),
                ("Outbox model", "Why clients need better relay discovery than random global relay lists.", "/nostr/deep-dives/outbox-model/"),
                ("Crays Super Node", "How venue infrastructure can become local relay and service infrastructure.", "/nostr/crays-super-node/"),
            ]),
        ],
        sources=RELAY_MARKET_SOURCES,
        related=["relays", "field-guide/relay-selection", "deep-dives/relay-business-models", "deep-dives/outbox-model", "nips/nip-11", "nips/nip-66", "nip-65-relay-list", "crays-super-node"],
        keywords=["Nostr relay list", "Nostr relay directory", "Nostr.watch", "paid Nostr relays", "NIP-11", "NIP-66"],
    ),
    page(
        "events-and-kinds",
        "Nostr Events and Event Kinds",
        "The event model behind Nostr: ids, pubkeys, timestamps, kinds, tags, content and signatures.",
        "Nostr has one basic object: the event. The event is signed, identified, timestamped and tagged. Different event kinds let clients understand profiles, notes, reactions, long-form content, badges, wallet requests and many other formats.",
        [
            section("The event object", [
                "NIP-01 defines the basic flow. An event includes an id, a public key, creation time, kind, tags, content and signature. The signature proves that the holder of the private key authorized the event content."
            ], [
                ("id", "A hash of the serialized event data."),
                ("pubkey", "The author identity."),
                ("created_at", "Unix timestamp."),
                ("kind", "The category of event."),
                ("tags", "References, metadata, relay hints and structured context."),
                ("content", "The payload, often text but not always."),
                ("sig", "The Schnorr signature."),
            ]),
            section("Why kinds matter", [
                "Kinds let clients interpret the same event structure differently. A short note, profile metadata, reaction, badge, long-form article, zap receipt or relay list can all use the event model while carrying different meaning."
            ]),
            section("Tags are the connective tissue", [
                "Tags connect events to people, events, relays, addresses, hashtags, geographies, communities, payments and external references. A strong product often depends more on tag design and indexing than on raw posting."
            ]),
            section("Crays event thinking", [
                "For Crays, event kinds and tags can represent profile context, follows, content access, status, award votes, venue signals, membership proof and governance participation. The design challenge is to make that useful without exposing users to protocol clutter."
            ]),
        ],
        sources=[NIP_SOURCES[0], GLOBAL_SOURCES[1], GLOBAL_SOURCES[2]],
        related=["nips", "nip-23-long-form", "nip-57-zaps-lightning", "nip-58-badges", "developer-tools"],
        keywords=["Nostr events", "Nostr kinds", "NIP-01", "signed events"],
    ),
    page(
        "nips",
        "Nostr NIPs",
        "A practical guide to Nostr Implementation Possibilities and the NIPs most relevant to identity, apps, payments, files and Crays.",
        "NIPs are Nostr Implementation Possibilities. They document ways Nostr-compatible clients, relays and services can interoperate. They are not a command that every app must implement every feature.",
        [
            section("How to read the NIP repository", [
                "The NIP repository is both essential and easy to misunderstand. It is not a polished consumer manual. It is a shared standards workspace. Some NIPs are mandatory to the base protocol, many are optional, some are draft status and some may be deprecated or superseded."
            ]),
            section("High-priority NIPs for most products", [
                "A serious product should understand NIP-01 for events, NIP-05 for readable identifiers, NIP-07 and NIP-46 for signing, NIP-19 for display formats, NIP-57 for zaps, NIP-65 for relay list metadata, NIP-44 for encrypted payloads and NIP-98 where HTTP auth matters."
            ], [
                ("Identity", "NIP-01, NIP-05, NIP-19, NIP-07, NIP-46."),
                ("Publishing", "NIP-23, NIP-25, NIP-51, NIP-65."),
                ("Payments", "NIP-57, NIP-47."),
                ("Trust and access", "NIP-42, NIP-44, NIP-58, NIP-98."),
                ("Media", "NIP-94 and file storage-related patterns."),
            ]),
            section("Crays standard selection", [
                "Crays should not implement a NIP simply because it exists. It should choose the standards that support user-owned identity, safe signing, zaps, status, venue access, search, content publishing, local relays and future governance."
            ]),
            section("NIP pages in this archive", [
                "This archive splits the main NIPs into individual pages so creators, operators and developers can navigate without reading the whole standards repository on day one."
            ]),
        ],
        sources=[GLOBAL_SOURCES[1]] + NIP_SOURCES,
        related=["events-and-kinds", "developer-tools", "privacy-security", "nip-57-zaps-lightning", "nip-58-badges"],
        keywords=["Nostr NIPs", "Nostr Implementation Possibilities", "NIP guide"],
    ),
    nip_page("nip-05-identifiers", "NIP-05", "DNS-Based Identifiers", "NIP-05 makes Nostr identities easier to recognize by mapping a public key to a DNS-based identifier.", "It lets a profile publish an identifier such as name@example.com and lets clients verify that the domain maps the name back to the public key.", "A domain serves a nostr.json file under .well-known. Clients check the name and public-key mapping before displaying the identifier as verified.", "Crays can use domain-backed identifiers for creators, venues, Association accounts and ecosystem services so users can recognize official identities.", "NIP-05 does not custody the key. If a domain is compromised or a private key is stolen, users still need clear recovery and communication practices.", related=["keys-identity", "nostr-login", "privacy-security"]),
    nip_page("nip-07-signers", "NIP-07", "Browser Signers", "NIP-07 defines the browser window.nostr interface used by extensions and web signers.", "It gives web apps a safer route to request public keys, event signatures and optional encryption without demanding that users paste private keys into every website.", "A browser extension or compatible signer injects a window.nostr object. Web apps request actions and the signer decides what to expose or approve.", "Crays.net can use signer flows to make profiles, posts, votes and payments safer for users moving through the Crays ecosystem.", "Bad permission prompts, confusing UX or malicious clients can still create risk. Users need clear consent and key boundaries.", related=["nostr-login", "nip-46-remote-signing", "privacy-security"]),
    nip_page("nip-19-addresses", "NIP-19", "npub, nsec and Nostr Addresses", "NIP-19 standardizes human-facing bech32 identifiers such as npub, nsec, note, nevent and naddr.", "It reduces confusion by giving different prefixes to public keys, private keys, event ids and addressable references.", "Software can store raw hex while showing users more recognizable prefixes. The most important education point is that npub is public and nsec is private.", "Crays should display safe identity formats and never train users to copy private secrets into ordinary pages.", "People still confuse identifiers. UX must make dangerous values visually and behaviorally distinct.", related=["keys-identity", "getting-started", "privacy-security"]),
    nip_page("nip-23-long-form", "NIP-23", "Long-Form Content", "NIP-23 defines addressable long-form article events, often used for Nostr-native writing.", "It lets clients publish and read article-like content in a standard format without locking the author into one blogging platform.", "The content is Markdown-oriented and should be structured for readability across clients. Social clients do not need to implement it, but publishing clients can.", "Crays can use long-form content for creator posts, venue stories, Association updates, educational explainers and SEO-adjacent distribution.", "Long-form UX needs drafts, editing, media handling, discovery and indexing. The NIP gives format, not a complete publishing product.", related=["creators", "apps", "content-sale"]),
    nip_page("nip-42-relay-auth", "NIP-42", "Client Authentication to Relays", "NIP-42 gives relays a way to ask clients to authenticate with a signed ephemeral event.", "It helps relays enforce paid access, membership, whitelisting, restricted resources or private community rules without falling back to passwords.", "A relay sends an authentication challenge. The client signs a short-lived event proving control of a key. The relay then applies its access policy.", "Crays venue relays and Super Nodes can use authenticated access for member-only services, guest context, operator tools or paid relay tiers.", "Auth must not become surveillance by accident. Products need clear user expectations, limited scopes and careful logging.", related=["relays", "operators-venues", "crays-super-node"]),
    nip_page("nip-44-encryption", "NIP-44", "Encrypted Payloads", "NIP-44 defines a versioned format for encrypted payloads used with signed Nostr events.", "It gives implementers a stronger encryption format and a way to evolve algorithms over time without pretending encryption is the whole messaging product.", "NIP-44 is a payload format. It does not define every messaging kind by itself. Clients still need conversation design, metadata minimization and user controls.", "Crays can use encrypted payload patterns for sensitive member, booking, concierge or operator context where public events would be wrong.", "Encryption does not hide all metadata. Who talks to whom, timing, relay choice and client behavior can still leak context.", related=["privacy-security", "nostr-login", "operators-venues"]),
    nip_page("nip-46-remote-signing", "NIP-46", "Remote Signing and Nostr Connect", "NIP-46 describes remote signing so clients can request signatures from a signer without holding the user's private key locally.", "It reduces attack surface by keeping private keys in a dedicated signer, mobile app, hardware device or remote signing service rather than exposing them to every app.", "A client and signer communicate through relays. The client asks for operations; the signer authorizes and returns signatures or key information according to permission rules.", "Crays can use Nostr Connect-style onboarding to make web login feel familiar while preserving Nostr-native identity and safer key custody.", "Remote signing adds UX and availability complexity. If users do not understand the signer relationship, they may approve too much or lose access.", related=["nostr-login", "nip-07-signers", "privacy-security"]),
    nip_page("nip-47-wallet-connect", "NIP-47", "Nostr Wallet Connect", "NIP-47 describes how Nostr clients can interact with Lightning wallets through a standardized protocol.", "It lets apps request wallet operations without embedding every wallet directly into every client. This matters for zaps, payments, invoices and creator monetization.", "A wallet service exposes capabilities through Nostr messages. Clients request operations and the wallet service responds according to permissions and limits.", "Crays can connect content access, venue payments, zaps, fan actions and concierge flows to Lightning wallets without making every app a full wallet.", "Wallet permissions need strict spending limits, clear approvals and safe defaults. Payment UX must be boringly reliable.", related=["nip-57-zaps-lightning", "nostr-and-bitcoin", "content-sale"]),
    nip_page("nip-57-zaps-lightning", "NIP-57", "Lightning Zaps", "NIP-57 connects Nostr social actions with Lightning payments through zap requests and zap receipts.", "It allows clients to display payments attached to posts or profiles. This turns support, tipping, rewards, spam deterrence and value-for-value signals into social objects.", "A client creates a zap request, sends it through an LNURL payment flow and receives a zap receipt event that can be displayed by clients.", "Crays can use zaps for creator support, fan proof, campaign signals, venue attention and eventually demand scoring around content and award activity.", "Do not confuse zaps with a full business model. Users still need wallet setup, pricing, legal clarity, refunds where relevant and consumer-safe checkout flows.", related=["nostr-and-bitcoin", "creators", "content-sale", "awards"]),
    nip_page("nip-58-badges", "NIP-58", "Badges", "NIP-58 describes badge definitions, badge awards, profile badge displays and badge sets.", "It gives Nostr a way to represent status, proof, membership, recognition or achievement without hard-coding badge logic into one app.", "Badge issuers define badges and award them to public keys. Users can choose which awarded badges to display on profiles.", "For Crays, this is status infrastructure. Creators and fans should not be described as selling badges. They can buy status badges where Crays offers them, or earn status through revenue, performance, contribution or community rules.", "Badges need issuer trust, anti-spam controls and plain explanations. A badge is only meaningful if people understand who issued it and why.", related=["awards", "content-sale", "keys-identity"]),
    nip_page("nip-65-relay-list", "NIP-65", "Relay List Metadata", "NIP-65 lets users advertise the relays where they write and where they prefer to receive mentions.", "It helps clients discover a user's likely relay locations instead of guessing blindly or relying only on fixed global relay lists.", "A user publishes a replaceable event with relay tags and optional read/write markers. Clients use that metadata to route reads and mentions more intelligently.", "Crays can use relay metadata to connect online profiles with venue relays, community relays and Crays-operated infrastructure.", "Relay lists can become stale or low quality. Clients need fallback logic, migration paths and user-friendly relay management.", related=["relays", "crays-super-node", "operators-venues"]),
    nip_page("nip-94-files", "NIP-94", "File Metadata", "NIP-94 defines a file metadata event that lets Nostr clients reference uploaded files with hashes, MIME types and descriptive tags.", "It supports media sharing, file organization and verification without assuming that relays themselves store the actual file bytes.", "Clients can publish metadata about where a file can be downloaded, what type it is and what hash verifies it.", "Crays can use file metadata for creator media, venue documents, event assets, content previews and verification of shared material.", "File hosting still requires storage, moderation, copyright handling, malware screening and privacy rules.", related=["music-video-media", "content-sale", "privacy-security"]),
    nip_page("nip-96-file-storage", "NIP-96", "HTTP File Storage", "NIP-96 describes an HTTP file storage integration intended to work alongside Nostr.", "It separates file upload and retrieval from WebSocket relay traffic. The broader point is that media storage can be adjacent to Nostr rather than inside every relay.", "A storage server exposes HTTP endpoints. Clients upload media and then reference resulting URLs through Nostr events.", "Crays can combine storage, file metadata and content access for creator media without forcing relays to become general media hosts.", "The NIP is marked unrecommended in favor of newer work, so production systems should verify current status before committing to it.", related=["nip-94-files", "music-video-media", "developer-tools"]),
    nip_page("nip-98-http-auth", "NIP-98", "HTTP Auth", "NIP-98 defines an ephemeral Nostr event used to authorize HTTP requests.", "It lets Nostr identities authenticate with ordinary HTTP services without a traditional username-password database for every service.", "A client signs a short-lived event containing the request URL and method. The server verifies the signature before accepting the request.", "Crays can use Nostr-native HTTP auth for services around profiles, content, booking, member areas or API access where signed identity is useful.", "Replay protection, timestamp handling, domain validation and user consent are critical. HTTP auth should be narrow and auditable.", related=["nostr-login", "developer-tools", "operators-venues"]),
    page(
        "apps",
        "Nostr Apps Directory Guide",
        "How to understand the Nostr app ecosystem: social clients, publishing, search, relays, media, wallets, developer tools and creator products.",
        "The Nostr app ecosystem is not one product category. It is a set of clients and services that use the same identity and event substrate for different experiences.",
        [
            section("App categories to know", [
                "Nostr Apps and Awesome Nostr show how wide the ecosystem already is. You will find social clients, mobile clients, desktop clients, long-form publishing tools, relay tools, search tools, chat apps, live-streaming experiments, music products, marketplaces, file tools, wallets and developer libraries."
            ], [
                ("Social clients", "Damus, Amethyst, Primal, Nos, Nostur, Coracle, Snort, Iris, Nostrudel and YakiHonne."),
                ("Writing", "Habla, YakiHonne and long-form NIP-23-oriented tools."),
                ("Media", "Wavlake, live-streaming tools and file metadata experiments."),
                ("Infrastructure", "Relay dashboards, server tools, signing tools and libraries."),
            ]),
            section("What directories are good for", [
                "Directories are not endorsements. They are discovery maps. Use them to understand what builders are attempting, which categories are crowded and where the ecosystem still has missing product quality."
            ]),
            section("How Crays should read the app market", [
                "Crays should not copy generic social clients. It should learn from them and build a purpose-specific Crays client layer: profile, creator monetization, fan access, award voting, venue routing and reputation."
            ]),
        ],
        sources=[GLOBAL_SOURCES[5], GLOBAL_SOURCES[6], GLOBAL_SOURCES[4], GLOBAL_SOURCES[3]],
        related=["clients", "developer-tools", "creators", "music-video-media", "resources"],
        keywords=["Nostr apps", "Nostr directory", "Nostr clients", "Awesome Nostr"],
    ),
    page(
        "developer-tools",
        "Nostr Developer Tools",
        "Developer-oriented map of Nostr: protocol docs, NIPs, nak, libraries, relays, signers, search and implementation discipline.",
        "Nostr development starts with a small core and expands through NIPs. The temptation is to implement everything. The better path is to choose the minimum standards that serve the product and then test interoperability carefully.",
        [
            section("Core developer reading order", [
                "Start with NIP-01. Then understand NIP-19 display formats, NIP-05 identifiers, NIP-07 and NIP-46 signing, NIP-65 relay lists and NIP-57 zaps. If your product touches wallets, study NIP-47. If it touches HTTP APIs, study NIP-98. If it touches media, study file metadata and current file storage work."
            ]),
            section("Tooling categories", [
                "Useful developer tools include command-line publishing and querying tools, relay frameworks, client libraries, signer libraries, indexing services, web-of-trust experiments, search tools and test relays."
            ], [
                ("nak", "Command-line work with events and relays."),
                ("Relay frameworks", "Khatru and other server libraries help teams run opinionated relays."),
                ("Client libraries", "Language-specific libraries reduce protocol boilerplate."),
                ("Indexers", "Search and recommendation require more than raw relay fetches."),
            ]),
            section("Implementation rules", [
                "Treat Nostr as infrastructure, not magic. Validate events. Handle relay errors. Avoid private-key exposure. Build migration paths. Test with multiple relays and clients. Expect partial support because NIPs are optional unless a product depends on them."
            ]),
            section("Crays developer priorities", [
                "For Crays, the first developer priorities are safe identity, signer UX, Crays.net profile events, content access, zaps or Lightning payment hooks, badge/status representation, award voting, venue relay topology and API authentication."
            ], cards=[
                ("Crays Circle GitHub", "Use the public Crays Circle GitHub organization as the code and implementation door when readers need developer context beyond the written archive.", "https://github.com/crayscircle"),
            ]),
        ],
        sources=[GLOBAL_SOURCES[0], GLOBAL_SOURCES[1], NIP_SOURCES[0], NIP_SOURCES[2], NIP_SOURCES[7], NIP_SOURCES[11], NIP_SOURCES[16], ("Crays Circle GitHub", "https://github.com/crayscircle", "Public Crays Circle GitHub organization for implementation and developer context.")],
        related=["nips", "events-and-kinds", "relays", "nostr-login", "crays-super-node"],
        keywords=["Nostr developer tools", "Nostr libraries", "Nostr NIPs", "nak Nostr"],
    ),
    page(
        "privacy-security",
        "Nostr Privacy and Security",
        "A practical security guide: private keys, public events, signer safety, relay metadata, encryption limits, scams, recovery and user education.",
        "Nostr gives users more ownership, but ownership increases responsibility. A private key is powerful. Public events are public. Relays reveal patterns. Encryption helps in specific contexts but does not erase metadata.",
        [
            section("The main private-key risk", [
                "If a user pastes a private key into a malicious or compromised website, the attacker can sign as that user. This is the central education problem for Nostr onboarding. Signers and remote signers exist because private keys should not travel everywhere."
            ], [
                ("Never share nsec", "The private key should not appear in public chats, screenshots or web forms."),
                ("Use signers", "NIP-07 and NIP-46 are safer than casual key-paste workflows."),
                ("Back up before reputation", "A user should not build social or commercial identity on an unbacked secret."),
            ]),
            section("Public means public", [
                "Many Nostr events are public by design. Deleting from one relay does not guarantee deletion from all copies, archives or screenshots. Users need to know which actions are public, which are encrypted and which leak metadata."
            ]),
            section("Encryption is not invisibility", [
                "Encrypted payloads can protect message content. They do not automatically hide timing, counterparties, relay choice, app behavior or device patterns. Serious products should distinguish content privacy from metadata privacy."
            ]),
            section("Crays security posture", [
                "Crays should present safe defaults: signer-first onboarding, clear consent, limited scopes, no dark patterns, understandable wallet permissions, visible official identities and careful handling of venue/member context."
            ]),
        ],
        sources=[NIP_SOURCES[2], NIP_SOURCES[6], NIP_SOURCES[7], GLOBAL_SOURCES[7], GLOBAL_SOURCES[2]],
        related=["keys-identity", "nip-07-signers", "nip-46-remote-signing", "nip-44-encryption", "nostr-login"],
        keywords=["Nostr security", "Nostr private key", "Nostr privacy", "Nostr signer"],
    ),
    page(
        "moderation-discovery",
        "Moderation and Discovery on Nostr",
        "How Nostr handles moderation, spam, search, discovery, feeds, relay rules, client choices and web-of-trust patterns.",
        "Nostr does not have one global moderation department or one global discovery algorithm. That is a feature and a burden. Clients, relays, lists, search tools, communities and users all shape what gets seen.",
        [
            section("Moderation is plural", [
                "Relays can reject content. Clients can hide content. Users can mute people or lists. Communities can pick membership rules. Paid relays can raise the cost of spam. None of those choices creates one perfect feed for everyone."
            ]),
            section("Discovery is product work", [
                "A raw protocol does not automatically produce great discovery. Clients need search, recommendations, follows, hashtags, communities, web-of-trust, relay selection and human curation. This is where many Nostr products will win or lose."
            ], [
                ("Search", "NIP-50 and external indexers can help find content."),
                ("Lists", "NIP-51 supports curated sets, mutes and other user-owned lists."),
                ("Relay strategy", "Good defaults matter for new users."),
                ("Web of trust", "Trust can be inferred from social distance and reputation, not only from platform authority."),
            ]),
            section("Crays discovery", [
                "Crays needs discovery around demand: creators, fans, venues, events, status, awards and bookings. A generic chronological feed is not enough. OpenClaw-style intent reading and Crays-specific indexes can turn signed signals into useful action."
            ]),
        ],
        sources=[NIP_SOURCES[9], NIP_SOURCES[10], NIP_SOURCES[13], GLOBAL_SOURCES[3], GLOBAL_SOURCES[6]],
        related=["search-and-web-of-trust", "relays", "clients", "nostr-and-crays"],
        keywords=["Nostr moderation", "Nostr discovery", "Nostr search", "web of trust"],
    ),
    page(
        "search-and-web-of-trust",
        "Nostr Search and Web of Trust",
        "Search, indexing, reputation and web-of-trust patterns for making an open Nostr graph usable.",
        "The open graph only becomes usable when people can find relevant identities, posts, communities, events and services. Search and web-of-trust are therefore core product layers, not side features.",
        [
            section("Why search is hard", [
                "Relays can be incomplete, offline, private, paid, spammed or specialized. A client that simply asks a random relay for everything may miss important context. Search services and indexers add structure on top of the relay layer."
            ]),
            section("Web of trust", [
                "Web-of-trust thinking asks who is known by whom, who is followed by trusted people, which identities have history and which signals appear coordinated. It can help filter spam and surface credible people without giving one company total control."
            ]),
            section("Crays demand graph", [
                "Crays can treat search and trust as demand infrastructure. The question is not only who posted. It is who can bring guests, who buys access, who attends venues, who votes, who earns status and who creates repeated commercial signal."
            ]),
        ],
        sources=[NIP_SOURCES[9], NIP_SOURCES[10], ("wot.nostr.net", "https://wot.nostr.net/", "Web-of-trust oriented Nostr resource."), ("Nostr.band GitHub", "https://github.com/nostrband", "Nostr.band public organization and related tools.")],
        related=["moderation-discovery", "relays", "creators", "nostr-and-crays"],
        keywords=["Nostr search", "Nostr web of trust", "Nostr discovery"],
    ),
    page(
        "nostr-vs-mastodon",
        "Nostr vs Mastodon",
        "A practical comparison of Nostr and federated social networks such as Mastodon.",
        "Nostr and Mastodon both respond to platform centralization, but they take different architectural routes. Mastodon uses federated servers with accounts hosted by instances. Nostr uses user keys, clients and relays.",
        [
            section("Identity model", [
                "In Mastodon, an account usually belongs to an instance. In Nostr, the identity is a public key that can be used across clients and relays. That difference changes portability, moderation, UX and recovery."
            ]),
            section("Server model", [
                "Mastodon servers are communities and account hosts. Nostr relays are event transport and storage points. A Nostr user can publish to many relays and read from different relay sets."
            ]),
            section("Moderation model", [
                "Mastodon moderation is instance-centric. Nostr moderation is split across relays, clients, lists and user choice. Neither model is automatically better for every use case."
            ]),
            section("Crays view", [
                "Crays needs portable identity across digital profiles and real venues. That makes Nostr more aligned with the requirement than an instance-hosted social account, although lessons from federated communities remain useful."
            ]),
        ],
        sources=[GLOBAL_SOURCES[8], GLOBAL_SOURCES[3], GLOBAL_SOURCES[4]],
        related=["why-nostr", "relays", "keys-identity", "moderation-discovery"],
        keywords=["Nostr vs Mastodon", "decentralized social", "federated social"],
    ),
    page(
        "free-speech-censorship",
        "Nostr, Free Speech and Censorship Resistance",
        "How Nostr changes the censorship debate without pretending that every relay or client must host every message.",
        "Nostr is often discussed as censorship-resistant, but the precise claim matters. It does not force every relay to host every message. It makes it harder for one platform, one server or one company to erase the whole graph.",
        [
            section("Resistance through plurality", [
                "A user can publish to multiple relays. A relay can reject content. Another relay can accept it. A client can filter or show it. This plurality reduces dependence on one gatekeeper while preserving freedom of association for relay operators and users."
            ]),
            section("The limits", [
                "Censorship resistance is not legal immunity, quality control or universal reach. A post that exists somewhere may still be invisible in popular clients. A relay can disappear. A domain can fail. A user can lose a key."
            ]),
            section("Crays interpretation", [
                "For Crays, the important lesson is not political sloganism. It is business resilience: creator profiles, fans, reputation, venue access and governance signals should not be hostage to one platform policy."
            ]),
        ],
        sources=[GLOBAL_SOURCES[3], GLOBAL_SOURCES[4], GLOBAL_SOURCES[8]],
        related=["why-nostr", "moderation-discovery", "relays", "privacy-security"],
        keywords=["Nostr censorship resistance", "free speech Nostr", "open protocol"],
    ),
    page(
        "creators",
        "Nostr for Creators",
        "How creators can use Nostr for portable audiences, direct value, long-form publishing, zaps, media, Crays.net profiles and fan status.",
        "Creators do not need another rented audience. They need an identity, graph and value route that can survive platform changes. Nostr gives a base. Products still have to turn that base into usable creator business flows.",
        [
            section("Creator problems Nostr can address", [
                "Creators face algorithm changes, account risk, fee pressure, link-in-bio fragmentation and weak fan ownership. Nostr can help by making identity portable, posts signed, follows reusable and payments visible through zaps."
            ]),
            section("What creators can do", [
                "A creator can publish short notes, long-form posts, media references, links, zap-enabled posts, community lists and profile data. Different clients may emphasize different formats."
            ], [
                ("Profile", "A Nostr profile can become a portable front door."),
                ("Content", "NIP-23 and media-related patterns support publishing beyond short posts."),
                ("Support", "NIP-57 zaps make small Lightning payments socially visible."),
                ("Status", "Badges can represent recognition, membership or earned standing."),
            ]),
            section("Crays creator model", [
                "Crays.net can replace a static link page with a profile that links, sells content access, shows status, routes fans, supports award voting and connects to real venues. Creators do not sell badges in the Crays model. Status badges can be bought by users where offered or earned through revenue, performance or contribution."
            ]),
        ],
        sources=[GLOBAL_SOURCES[2], GLOBAL_SOURCES[5], NIP_SOURCES[4], NIP_SOURCES[11], NIP_SOURCES[12]],
        related=["content-sale", "nip-57-zaps-lightning", "nip-58-badges", "music-video-media", "crays-super-node"],
        keywords=["Nostr creators", "creator economy", "zaps", "Crays.net profile"],
    ),
    page(
        "music-video-media",
        "Nostr Music, Video and Media",
        "Nostr lifestyle media: music, streaming, video, file metadata, creator payments and value-for-value culture.",
        "Nostr culture is not only text posts. Music, video, live streams, image sharing, file metadata and creator payments are part of the broader ecosystem because portable identity and value flow matter wherever audiences gather.",
        [
            section("Music and value-for-value", [
                "Wavlake points to a creator-listener model where artists and listeners can transact more directly. In Nostr culture, zaps and Lightning payments support the idea that fans can send value without waiting for a platform payout cycle."
            ]),
            section("Video and live media", [
                "Nostr app directories include live-streaming and media experiments. The challenge is that video needs storage, bandwidth, moderation, copyright workflows and discovery. Nostr can sign identity and references, while specialized services may handle media delivery."
            ]),
            section("Files and metadata", [
                "NIP-94 and related file-storage work show how clients can refer to media while keeping actual file hosting outside the core relay flow. This separation is practical because relays are not meant to become universal content delivery networks."
            ]),
            section("Crays media layer", [
                "Crays can connect creator media to paid access, fan status, award campaigns and venues. Media should not be scattered across disconnected social profiles if the goal is a coherent creator-to-venue demand engine."
            ]),
        ],
        sources=[("Wavlake", "https://wavlake.com/", "Music and creator-listener ecosystem."), GLOBAL_SOURCES[5], NIP_SOURCES[14], NIP_SOURCES[15], NIP_SOURCES[4], NIP_SOURCES[11]],
        related=["creators", "content-sale", "nip-94-files", "nip-96-file-storage", "lifestyle-culture"],
        keywords=["Nostr music", "Nostr video", "Wavlake", "value for value"],
    ),
    page(
        "lifestyle-culture",
        "Nostr Lifestyle and Culture",
        "The culture around Nostr: Bitcoiners, open-source builders, zaps, conferences, creator independence, local communities and real-world meetups.",
        "Nostr is a protocol, but protocols become real through culture. Around Nostr you find Bitcoiners, open-source builders, creators, privacy advocates, indie app makers, event organizers, musicians, writers and people tired of platform capture.",
        [
            section("The social mood", [
                "Nostr culture often feels like the early web: experimental, rough, direct and full of competing interfaces. That roughness is not only a weakness. It is also evidence that the network is not waiting for one product team to approve every direction."
            ]),
            section("Zaps as cultural behavior", [
                "Zaps turn appreciation into a visible social action. They are small payments, but culturally they say something larger: attention and value can travel together. That is why creators, podcasters, musicians and Bitcoin communities care about them."
            ]),
            section("Events and meetups", [
                "Nostrica, Nostrasia and Nostriga show that Nostr is not just software. It has real-world gatherings, unconferences, time capsules, demos and crossovers with Bitcoin events."
            ]),
            section("Crays lifestyle bridge", [
                "Crays is built exactly at this bridge: online identity, creator status, Bitcoin-native value flow and real places. The Nostr lifestyle layer gives Crays a cultural context for hospitality, creator access and venue community."
            ]),
        ],
        sources=[("Nostrica", "https://nostrica.com/", "Nostr unconference and culture archive."), ("Nostr World", "https://nostr.world/", "Nostriga and conference material."), ("Wavlake", "https://wavlake.com/", "Music and value-for-value culture."), GLOBAL_SOURCES[3], GLOBAL_SOURCES[6]],
        related=["events", "jack-dorsey", "music-video-media", "nostr-and-bitcoin", "operators-venues"],
        keywords=["Nostr lifestyle", "Nostr culture", "Nostrica", "Nostriga", "zaps"],
    ),
    page(
        "events",
        "Nostr Events and Conferences",
        "A living map of Nostr events, unconferences, Bitcoin-week crossovers, culture archives and real-world community formation.",
        "Events matter because Nostr is not a polished corporate rollout. It grows through builders, users, meetups, unconferences, demos and social trust formed outside the screen.",
        [
            section("Nostrica", [
                "Nostrica captured an early Nostr culture moment: free, decentralized, unconference-driven and connected to the idea that Nostr can free people from platforms. It remains part of the origin story for many users."
            ]),
            section("Nostrasia and Nostriga", [
                "Nostr.world documents Nostriga in Riga and references the broader timecapsule chain from Nostrica and Nostrasia. This matters because the community treats history, notes and events as part of the same living graph."
            ]),
            section("Bitcoin overlap", [
                "Nostr events often overlap with Bitcoin culture because Lightning zaps, self-custody, open-source funding and user-owned identity are natural adjacent themes."
            ]),
            section("Crays event logic", [
                "Crays can turn event culture into venue operations: local relays, creator meetups, fan access, award nights, hospitality services and signed reputation around real places."
            ]),
        ],
        sources=[("Nostrica", "https://nostrica.com/", "Nostr unconference archive."), ("Nostr World", "https://nostr.world/", "Nostriga and Nostr World material."), GLOBAL_SOURCES[8]],
        related=["lifestyle-culture", "operators-venues", "crays-super-node", "awards"],
        keywords=["Nostr events", "Nostrica", "Nostrasia", "Nostriga", "Nostr conference"],
    ),
    page(
        "jack-dorsey",
        "Jack Dorsey and Nostr",
        "Why Jack Dorsey's public support matters, what it does not mean and how to understand Nostr beyond celebrity attention.",
        "Jack Dorsey helped bring mainstream attention to Nostr by publicly supporting the protocol and funding open work around it. That attention matters, but Nostr is not Jack Dorsey's platform. It is an open protocol and community of independent builders.",
        [
            section("Why the story became visible", [
                "After years of debate around centralized social platforms, API control and moderation power, a simple protocol for portable identity and signed events was naturally interesting to people looking for alternatives. Jack Dorsey's public support made that conversation easier for mainstream observers to notice."
            ]),
            section("The 14 BTC funding story", [
                "Public reporting in December 2022 described Jack Dorsey giving 14 BTC in funding to Nostr development. In ecosystem terms, the number became part of Nostr lore because it connected Bitcoin-native funding with an open social protocol."
            ]),
            section("What to avoid misunderstanding", [
                "Nostr is not a Dorsey-owned company, not a Bluesky clone and not a replacement brand for Twitter. The interesting point is architectural: keys, clients, relays and signed events make social identity less dependent on one operator."
            ]),
            section("Crays interpretation", [
                "For Crays, the Jack Dorsey story is useful as cultural proof that the open social layer is no longer a fringe topic. But the Crays thesis does not depend on celebrity. It depends on portable identity, creator demand, Bitcoin-native value flow and real-world hospitality nodes."
            ]),
        ],
        sources=[("CoinDesk report", "https://www.coindesk.com/tech/2022/12/15/jack-dorsey-gives-decentralized-social-network-nostr-14-btc-in-funding", "Public reporting on the 14 BTC Nostr funding story."), GLOBAL_SOURCES[3], GLOBAL_SOURCES[0], ("Nostr World timecapsule", "https://nostr.world/", "Nostr event archive referencing early cultural moments.")],
        related=["lifestyle-culture", "nostr-and-bitcoin", "why-nostr", "events"],
        keywords=["Jack Dorsey Nostr", "Nostr 14 BTC", "Dorsey decentralized social"],
    ),
    page(
        "nostr-and-bitcoin",
        "Nostr and Bitcoin",
        "How Nostr and Bitcoin fit together: keys, open protocols, Lightning zaps, wallets, value-for-value and why Nostr is not a blockchain.",
        "Nostr and Bitcoin are separate systems with complementary cultures. Nostr handles signed social events. Bitcoin and Lightning handle value. Together they make identity, attention and payment more directly connected.",
        [
            section("Separate layers", [
                "Nostr does not need a blockchain to store posts. It uses relays. Bitcoin does not need to become a social network. It provides money and settlement. The combination is powerful because each layer does what it is good at."
            ]),
            section("Lightning zaps", [
                "NIP-57 zaps are the most visible bridge. A post or profile can receive a Lightning payment and the receipt can become visible in Nostr clients. That turns payments into social signals."
            ]),
            section("Wallet connect", [
                "NIP-47 adds a route for clients to interact with Lightning wallets through Nostr messages. That can make wallet-enabled social apps safer and more modular."
            ]),
            section("Crays architecture", [
                "Crays uses Nostr as the social identity and signal layer, Bitcoin and Lightning as the value layer, and Crays products as the commercial and hospitality layer. That is why the Nostr page says Nostr and Bitcoin are base architecture for Crays."
            ]),
        ],
        sources=[NIP_SOURCES[11], NIP_SOURCES[8], GLOBAL_SOURCES[2], GLOBAL_SOURCES[3]],
        related=["nip-57-zaps-lightning", "nip-47-wallet-connect", "creators", "content-sale", "nostr-and-crays"],
        keywords=["Nostr Bitcoin", "Nostr Lightning", "zaps", "value for value"],
    ),
    page(
        "nostr-login",
        "Nostr Login",
        "How Nostr can work as an identity layer for apps: public keys, signers, NIP-07, NIP-46 and HTTP auth.",
        "Nostr login replaces the idea that every app must start with an empty email-password database. A public key can identify the user, and signatures can prove control of that identity.",
        [
            section("Why login is interesting", [
                "A new app usually has no social graph. A large login provider reduces friction but introduces dependency. Nostr offers a third path: permissionless identity with portable social context."
            ]),
            section("The core flow", [
                "A user has a key pair. The public key identifies the account. A signer or remote signer authorizes events or login proofs. Apps can use NIP-07 in browsers, NIP-46 for remote signing and NIP-98 for HTTP request authentication."
            ]),
            section("Product requirements", [
                "A good Nostr login flow should feel familiar without hiding key consequences. It needs clear consent, readable accounts, session management, revocation thinking and recovery education."
            ]),
            section("Crays login design", [
                "Crays can use Nostr identity so one user can move from Crays.net to content access, venue entry, fan status, award voting, payments and governance participation without starting over in each product."
            ]),
        ],
        sources=[GLOBAL_SOURCES[7], NIP_SOURCES[2], NIP_SOURCES[7], NIP_SOURCES[16], NIP_SOURCES[1]],
        related=["keys-identity", "nip-07-signers", "nip-46-remote-signing", "nip-98-http-auth", "nostr-and-crays"],
        keywords=["Nostr login", "Nostr Connect", "NIP-07", "NIP-46", "NIP-98"],
    ),
    page(
        "resources",
        "Nostr Resources and Links",
        "A curated archive of official Nostr references, guides, app directories, NIPs, clients, tools, event archives and Crays context.",
        "This page is the practical link map for the Crays Nostr archive. Use it when you want to move from a Crays explanation into tools, apps, NIPs, events and ecosystem directories.",
        [
            section("How to use this resource page", [
                "Use official NIPs for implementation truth, nostr.how for onboarding explanations, nostr.com and nostr.org for broad introductions, Nostr Apps and Awesome Nostr for ecosystem discovery, Nostr Login for signer and login thinking, and event pages for culture."
            ]),
            section("Editorial principle", [
                "Crays does not copy outside pages. The archive turns the useful information into independent Crays explanations, then keeps practical links available for readers who want to inspect tools and projects directly."
            ]),
        ],
        sources=RESOURCE_LINKS,
        related=["what-is-nostr", "nips", "apps", "developer-tools", "videos"],
        keywords=["Nostr resources", "Nostr links", "Nostr archive", "Awesome Nostr"],
        read="18 min read",
    ),
    page(
        "glossary",
        "Nostr Glossary",
        "Plain-English definitions for Nostr terms: npub, nsec, relay, client, zap, NIP, signer, event kind, tag, badge and more.",
        "Nostr vocabulary can be alienating. This glossary keeps definitions short and practical so readers can move through the archive without getting stuck.",
        [
            section("Core terms", [
                "The terms below are written for readers, creators, operators and investors. Developers should still verify exact protocol behavior in the NIP repository."
            ], cards=[
                ("Nostr", "Open protocol for signed events distributed by relays."),
                ("npub", "Public display format for a Nostr public key."),
                ("nsec", "Private-key display format. Keep it secret."),
                ("Relay", "Server that accepts, stores, filters or forwards events."),
                ("Client", "User-facing app that reads and writes Nostr events."),
                ("Event", "Signed data object with id, pubkey, kind, tags, content and signature."),
                ("NIP", "Nostr Implementation Possibility, a shared interoperability document."),
                ("Zap", "Lightning payment represented socially through Nostr zap events."),
                ("Signer", "Tool that signs events without exposing the private key to every app."),
                ("NIP-05", "DNS-based mapping from a name to a public key."),
                ("NIP-46", "Remote signing and Nostr Connect."),
                ("NIP-57", "Lightning zaps."),
                ("Badge", "Status, recognition or membership object defined and awarded by issuers."),
                ("Web of trust", "Reputation and trust inferred through social relationships and behavior."),
                ("Crays Super Node", "Crays venue hardware and service layer for local relay, mesh and hospitality context."),
            ]),
        ],
        sources=GLOBAL_SOURCES + NIP_SOURCES,
        related=["what-is-nostr", "getting-started", "nips", "resources"],
        keywords=["Nostr glossary", "npub", "nsec", "zap", "relay"],
    ),
    page(
        "videos",
        "Nostr Videos, Talks and Audio Trail",
        "A curated trail for Nostr videos, explainers, conference talks, demos, zaps, music and cultural material.",
        "Video belongs in a Nostr archive when it helps people understand the culture and product reality. This page keeps videos as references, not as visual noise on the main marketing page.",
        [
            section("Beginner explainers", [
                "Start with the broad explainers linked from nostr.com and nostr.org. They help non-technical readers understand clients, relays, keys and signatures without diving into NIP text first."
            ]),
            section("Conference material", [
                "Nostrica and Nostr World preserve the conference and unconference side of Nostr. These pages are useful because they show the social movement around the protocol, not only the code."
            ]),
            section("Creator and music media", [
                "Wavlake and value-for-value discussions are useful for understanding why Nostr is more than posts. Music, podcasts and video are where direct payments and portable audiences become culturally visible."
            ]),
            section("Crays video rule", [
                "On Crays pages, videos should be placed where they clarify a product path. They should not create chaotic scroll fatigue. This archive page can hold the long trail while the main Nostr page stays focused."
            ]),
        ],
        sources=[("Nostr.com video links", "https://nostr.com/", "Nostr.com links to human-friendly video explanations."), ("Nostr.org video", "https://nostr.org/", "Introductory Nostr video and client overview."), ("Nostrica", "https://nostrica.com/", "Nostr unconference archive."), ("Nostr World", "https://nostr.world/", "Nostriga and timecapsule material."), ("Wavlake", "https://wavlake.com/", "Music and value-for-value ecosystem.")],
        related=["lifestyle-culture", "events", "music-video-media", "what-is-nostr"],
        keywords=["Nostr videos", "Nostr talks", "Nostr conference", "Nostr music"],
    ),
    page(
        "nostr-media-article-video-archive",
        "Nostr Media, Articles and Video Archive",
        "A Start-route research shelf for Nostr articles, blog posts, public explainers, event material and YouTube videos, sorted by reader use.",
        "This is the media door into the Nostr atlas. Use it when you want outside reporting, independent essays, event recordings, tutorials and video explainers before choosing the next written chapter. The goal is not to replace the Start guide. It adds source memory and watchable context around it.",
        [
            section(
                "How this archive is organized",
                [
                    "A useful Nostr media archive should not be a random pile of links. Each source below is sorted by reader job: first-contact orientation, technical truth, funding context, real-world adoption, app discovery, events, creator media or product implementation.",
                    "When an author or host is known and relevant, the person also belongs in the People route as a media voice. That keeps the archive human: articles and videos are not abstract SEO objects; they are produced by people who shape how newcomers understand the protocol."
                ],
                [
                    ("Start value", "Begin with short explainers and plain-language essays when the reader still needs the mental model."),
                    ("Depth value", "Use NIPs, repositories and funding pages when an article needs to verify a technical or ecosystem claim."),
                    ("Scene value", "Use event archives and YouTube talks to understand the human network behind the protocol."),
                    ("Crays value", "Use the archive to connect Nostr media with our own pages about identity, relays, wallets, media, commerce and governance."),
                ],
            ),
            section(
                "Articles, essays and source pages",
                [
                    "These are the first source shelves we can safely expose inside Start. They include mainstream reporting, long-form analysis, funding records, primary technical material and event archives. This list should keep growing, but it already gives a reader the important outside doors without leaving them alone in search results."
                ],
                cards=[
                    (
                        entry["title"],
                        f'{entry["source"]} · {entry["author"]}. {entry["use"]}',
                        entry["url"],
                    )
                    for entry in NOSTR_MEDIA_ARTICLE_ARCHIVE
                ],
            ),
            section(
                "Complete Excel source inventory",
                [
                    f"This shelf exposes every normalized URL from the Nostr deep-research Excel inside the Media archive. The workbook currently gives us {DEEP_RESEARCH.get('url_cells', 0)} URL cell(s), deduplicated into {DEEP_RESEARCH.get('unique_urls', 0)} unique source URL(s).",
                    "Every card keeps the original URL visible in the description so the Atlas search can find it by domain, title, slug, path fragment or full URL. Duplicates stay recorded through workbook signals on the matching source page; this archive shows the unique URL once so the reader does not drown in repeated rows.",
                    "Use this shelf as the public memory layer: articles, apps, NIPs, repositories, relay directories, long-form reads, media tools and primary sources all become searchable from one Start-route door."
                ],
                [
                    ("URL cells in Excel", str(DEEP_RESEARCH.get("url_cells", 0))),
                    ("Unique URLs exposed", str(DEEP_RESEARCH.get("unique_urls", 0))),
                    ("Source pages generated", str(len(DEEP_RESEARCH.get("sources", [])))),
                    ("Search rule", "A full URL, source name, domain, NIP number or project name should resolve through the Atlas search."),
                ],
                cards=deep_research_source_cards(),
            ),
            section(
                "Exact workbook URL variants",
                [
                    "Some workbook links differ from the normalized source inventory only by a trailing slash or URL-encoded category text. We keep those exact variants here so a copied Excel URL can still be found through the Atlas search and opened from the Media archive.",
                    "This is a source-integrity shelf, not a separate editorial category: the normalized source page remains the main explanation, and the exact workbook URL remains searchable for audit traceability."
                ],
                cards=EXCEL_SOURCE_URL_FIXUPS,
            ),
            section(
                "Watch first: the fastest mental model",
                [
                    "These videos are for readers who want the shape of Nostr before reading deeply. They work best beside What is Nostr, Getting Started and the Glossary."
                ],
                videos=[video for video in NOSTR_VIDEO_ARCHIVE if video["category"] == "Start"],
            ),
            section(
                "Safety, privacy, keys and moderation",
                [
                    "This shelf is for the moment after a reader understands the idea and needs to avoid the bad habits: unsafe key handling, vague censorship myths, weak relay assumptions and careless identity verification."
                ],
                videos=[video for video in NOSTR_VIDEO_ARCHIVE if video["category"] in {"Privacy", "Governance"}],
            ),
            section(
                "Wallets, zaps and Bitcoin value flow",
                [
                    "Nostr becomes easier to care about once readers see value moving with social context. These videos connect zaps, Nostr Wallet Connect, Lightning nodes, Primal and Bitcoin-native payments."
                ],
                videos=[video for video in NOSTR_VIDEO_ARCHIVE if video["category"] in {"Wallets", "Commerce"}],
            ),
            section(
                "Apps, protocol work and developer material",
                [
                    "This is where curious builders move next: first app demos, product roundtables, NIPs, relays, DVMs, clients and the technical conversations that explain why one protocol can produce many interfaces."
                ],
                videos=[video for video in NOSTR_VIDEO_ARCHIVE if video["category"] in {"Apps", "NIPs", "Relays"}],
            ),
            section(
                "People, events, media and culture",
                [
                    "The Nostr archive should make the scene visible. Panels, event Q&A, music discussions and conference videos help readers understand that Nostr is not only a spec; it is a living network of builders, educators, media people, creators and event organizers."
                ],
                videos=[video for video in NOSTR_VIDEO_ARCHIVE if video["category"] in {"People", "Media"}],
            ),
            section(
                "Where these sources connect inside Crays",
                [
                    "A source archive is only useful when it points back into the knowledge system. First-contact videos belong near What is Nostr and Getting Started. Key-safety videos belong near Privacy and Signers. Zap videos belong near NIP-57 and Nostr Wallet Connect. Event and panel videos belong near People, Events and Media.",
                    "This page will keep expanding as more Nostr media appears. The rule is simple: every outside source needs a reason to exist here, a category, a user benefit and at least one internal path that helps the reader continue."
                ],
                cards=[
                    ("What is Nostr?", "Start with the clean mental model before opening long-form articles.", "/nostr/what-is-nostr/"),
                    ("Getting Started", "Use setup and safety videos when the reader is ready to create an identity.", "/nostr/getting-started/"),
                    ("People", "Known authors, hosts and educators live in the People archive as media voices.", "/nostr/people/"),
                    ("Media", "Creator publishing, music, long-form writing and videos belong to the Media route.", "/nostr/music-video-media/"),
                    ("Wallets", "Zap and wallet videos connect to NIP-57, NIP-47, Alby and Safebox.", "/nostr/nip-47-wallet-connect/"),
                    ("Library", "Primary technical and source pages remain available through the Library route.", "/nostr/archive-library/"),
                ],
            ),
        ],
        sources=[
            (entry["title"], entry["url"], f'{entry["source"]}: {entry["category"]}.')
            for entry in NOSTR_MEDIA_ARTICLE_ARCHIVE
        ],
        related=["what-is-nostr", "getting-started", "videos", "music-video-media", "people", "resources", "archive-library"],
        keywords=[
            "Nostr media archive",
            "Nostr articles",
            "Nostr YouTube videos",
            "Nostr tutorials",
            "Nostr events",
            "Nostr media people",
        ],
    ),
    page(
        "nostr-and-crays",
        "Nostr and Crays",
        "How Nostr becomes the base layer for Crays.net, Content Sale, Status Badges, Crays Award, Crays World, Super Nodes, Lightning and future DAO governance.",
        "Crays uses Nostr because one portable social graph can connect profiles, creators, fans, capital and real places. The protocol alone is not the business. It is the base layer for the Crays operating system.",
        [
            section("Base architecture", [
                "Crays needs a social layer that is portable, signed and independent from one closed app. Nostr supplies identity and social events. Bitcoin and Lightning supply value flow. Crays products supply commercial and hospitality execution."
            ]),
            section("Product stack", [
                "Crays.net is the public profile and creator surface. Content Sale gives paid content access. Status Badges represent bought or earned status. Crays Award turns audience attention into voting and acquisition. Crays World connects the online identity to venues. Super Nodes bring relay and service context into real places."
            ], [
                ("Crays.net", "Profile, links, fans, content, status and ecosystem entry."),
                ("Content Sale", "Creator monetization and paid access."),
                ("Status Badges", "Bought status or earned status through revenue, performance or contribution."),
                ("Crays Award", "Nostr-based voting and creator acquisition."),
                ("Crays World", "Venue layer and local social graph."),
                ("Super Node", "Local relay, mesh and hospitality service infrastructure."),
            ]),
            section("Why not a closed Crays account only", [
                "A closed account can operate a database, but it cannot create a resilient ecosystem identity. Crays wants creators, fans, operators, capital and venues to remain connected as products change."
            ]),
            section("DAO path", [
                "Future governance needs identity, reputation, membership context, signed votes, participation history and economic signal. Nostr gives the signed social substrate. Crays can add rules, legal structure and product UX."
            ]),
        ],
        sources=GLOBAL_SOURCES + [NIP_SOURCES[11], NIP_SOURCES[12], NIP_SOURCES[13], NIP_SOURCES[16], ("Crays Circle GitHub", "https://github.com/crayscircle", "Public Crays Circle GitHub organization for implementation and developer context.")],
        related=["content-sale", "awards", "crays-super-node", "operators-venues", "dao-governance"],
        keywords=["Crays Nostr", "Crays.net", "Crays Super Node", "Crays Award", "Crays DAO"],
    ),
    page(
        "content-sale",
        "Nostr and Crays Content Sale",
        "How Nostr can support creator content access, paid media, fan routes, Lightning payments and Crays.net profiles.",
        "Content Sale should not be another isolated paywall. It should connect creator identity, fan proof, payments, status and future reputation through the same Nostr-aware Crays profile layer.",
        [
            section("What Content Sale means", [
                "Content Sale is paid creator access. Nostr can help represent identity, links, posts, proof, fan context and social distribution. Lightning can support payments. Crays.net can make the user experience commercial and understandable."
            ]),
            section("Avoid the badge mistake", [
                "Creators do not sell badges in the Crays model. Users can buy status badges where offered, or earn status through revenue, performance, contribution or community rules. Content Sale is about creator content access, not creators issuing arbitrary badge inventory."
            ]),
            section("Technical ingredients", [
                "Useful ingredients include NIP-23 long-form content, NIP-57 zaps, NIP-47 wallet connection, NIP-58 badges where status is relevant, NIP-94 file metadata and signer-based identity."
            ]),
            section("Reader clarity", [
                "For users, the page should explain outcomes: follow a creator, buy access, prove status, get routed into events, vote, enter venues and keep identity portable."
            ]),
        ],
        sources=[NIP_SOURCES[4], NIP_SOURCES[8], NIP_SOURCES[11], NIP_SOURCES[12], NIP_SOURCES[14], GLOBAL_SOURCES[5]],
        related=["creators", "nip-57-zaps-lightning", "nip-58-badges", "nostr-and-crays", "music-video-media"],
        keywords=["Crays Content Sale", "Nostr creator commerce", "paid content Nostr"],
    ),
    page(
        "awards",
        "Nostr and Crays Award",
        "How Nostr identity, votes, zaps, badges, audience proof and signed participation can support Crays Award mechanics.",
        "Crays Award can use Nostr to connect creator acquisition, fan participation, votes, proof and reputation without making the award dependent on one social platform.",
        [
            section("Why awards need portable identity", [
                "A creator award based only on one platform's followers is fragile. Nostr can let fans, creators and voters carry identity and participation across clients and Crays surfaces."
            ]),
            section("Possible event signals", [
                "Award workflows can use signed profiles, follows, votes, zaps, campaign posts, badges, lists and venue attendance signals. The product should hide the complexity and show a clear voting experience."
            ]),
            section("Badges and status", [
                "Badges can represent finalist status, supporter status, member status, venue access or earned recognition. They should be issued by trusted Crays or partner identities and explained clearly."
            ]),
            section("DAO path", [
                "Award participation can become a precursor to governance if identity, reputation and voting context are designed carefully from the beginning."
            ]),
        ],
        sources=[NIP_SOURCES[11], NIP_SOURCES[12], NIP_SOURCES[10], GLOBAL_SOURCES[1]],
        related=["nip-58-badges", "creators", "content-sale", "dao-governance", "nostr-and-crays"],
        keywords=["Crays Award", "Nostr voting", "Nostr badges", "creator award"],
    ),
    page(
        "crays-super-node",
        "Crays Super Node and Nostr",
        "How Crays Super Nodes can connect venue relays, mesh networking, POS/PMS services, Lightning, identity and hospitality operations.",
        "A Super Node is where the Nostr idea becomes physical. It can help a venue act as a local relay, local service point, payment context and hospitality node rather than a disconnected offline place.",
        [
            section("Why local infrastructure matters", [
                "If Nostr stays only as a social feed, it cannot do the full Crays job. Venues need local presence, access, orders, payments, booking context, member status and reliable service workflows."
            ]),
            section("Super Node functions", [
                "A Crays Super Node can support local relay functions, mesh networking, venue-specific services, POS/PMS integration, Lightning payment flows, guest context, staff context and local community discovery."
            ], [
                ("Relay", "Local social and service context."),
                ("Mesh", "Venue-local peer and service connectivity."),
                ("Payments", "Lightning-native flows where appropriate."),
                ("Hospitality", "Bookings, orders, access, concierge and member state."),
            ]),
            section("Relationship to NIPs", [
                "NIP-65 relay lists, NIP-42 auth, NIP-98 HTTP auth, NIP-57 zaps and NIP-47 wallet connect are especially relevant. The exact implementation should be product-led, not spec-led."
            ]),
            section("Business meaning", [
                "The Super Node lets Crays turn digital demand into venue operations. That is the bridge from social graph to real-world revenue."
            ]),
        ],
        sources=[NIP_SOURCES[5], NIP_SOURCES[8], NIP_SOURCES[11], NIP_SOURCES[13], NIP_SOURCES[16], GLOBAL_SOURCES[1]],
        related=["relays", "operators-venues", "nostr-and-crays", "nostr-and-bitcoin", "dao-governance"],
        keywords=["Crays Super Node", "Nostr relay", "venue relay", "Wi-Fi Aware mesh", "hospitality Nostr"],
    ),
    page(
        "operators-venues",
        "Nostr for Operators and Venues",
        "How hospitality operators, clubs, resorts, rooftops and event spaces can use Nostr identity, local relays, payments and member context.",
        "For operators, Nostr is not interesting because it is fashionable. It is interesting if it reduces platform dependence, gives better demand context and connects guests, creators, staff and payments inside a real venue.",
        [
            section("Venue problems", [
                "Venues have fragmented guest data, expensive acquisition, disconnected social platforms, separate POS/PMS systems, weak creator attribution and poor visibility into community demand."
            ]),
            section("Nostr venue logic", [
                "A venue can operate local relays, recognize members, surface events, connect creators, support payments and allow guests to carry identity across spaces."
            ]),
            section("Crays World", [
                "Crays World can become the real-world layer where online profiles become presence, booking, service and community context."
            ]),
            section("Operator caution", [
                "Operators should not see Nostr as replacing all systems. It is a social and identity layer that can connect with POS, PMS, booking and payment infrastructure."
            ]),
        ],
        sources=[GLOBAL_SOURCES[3], GLOBAL_SOURCES[4], NIP_SOURCES[5], NIP_SOURCES[13], NIP_SOURCES[16]],
        related=["crays-super-node", "relays", "nostr-and-crays", "events", "dao-governance"],
        keywords=["Nostr venues", "hospitality Nostr", "Crays World", "venue relay"],
    ),
    page(
        "dao-governance",
        "Nostr and Crays DAO Governance",
        "How signed identity, badges, votes, reputation, relays and Association rules can prepare Crays for future DAO participation.",
        "DAO governance cannot be serious if identity, membership, reputation and voting context are vague. Nostr can provide signed social identity. Crays can add legal structure, rules and commercial reality.",
        [
            section("Governance needs identity", [
                "A DAO vote is only meaningful if the system knows what the vote represents. Nostr public keys, badge/status context, history and reputation can help build a clearer participation layer."
            ]),
            section("Association frame", [
                "The Crays Business Nomads Association can define rules, councils, partner standards and participation mechanisms while Nostr carries signed identity and event context."
            ]),
            section("Signals that matter", [
                "Useful signals may include membership, bought or earned status, creator revenue, venue participation, award votes, zaps, content access, contribution and verified domain identities."
            ]),
            section("Do not rush governance theater", [
                "Governance should follow real participation and economic behavior. Nostr makes signed participation easier to represent, but rules and accountability still need careful design."
            ]),
        ],
        sources=[NIP_SOURCES[1], NIP_SOURCES[10], NIP_SOURCES[12], GLOBAL_SOURCES[1]],
        related=["nostr-and-crays", "awards", "content-sale", "crays-super-node", "keys-identity"],
        keywords=["Nostr DAO", "Crays DAO", "Nostr governance", "signed voting"],
    ),
]


for item in PAGES:
    if item["slug"] == "videos":
        item["sections"].extend([
            section(
                "Watchable video shelves",
                [
                    "The larger media archive now carries embedded Nostr videos by category. This page stays as the Media-route doorway, while the Start archive gives the full watchable map."
                ],
                cards=[
                    ("Full media and video archive", "Open the complete watchable archive with articles, events, tutorials and video categories.", "/nostr/nostr-media-article-video-archive/"),
                    ("Nostr World", "Event videos, talks and public scene material.", "https://nostr.world/"),
                    ("Nostrica", "Conference and unconference archive material.", "https://nostrica.com/"),
                ],
            ),
            section(
                "Recommended videos by user need",
                [
                    "Use the labels on each video as a shortcut. Start videos explain the mental model. Privacy videos protect the reader from bad key habits. Wallet videos explain zaps and Nostr Wallet Connect. App and NIP videos help builders understand the protocol surface."
                ],
                videos=NOSTR_VIDEO_ARCHIVE[:12],
            ),
        ])


PEOPLE = [
    {
        "slug": "people/enoch-root",
        "name": "Enoch Root",
        "title": "Enoch Root",
        "aliases": [],
        "role": "Crays founder, Bitcoin believer and mission voice",
        "summary": "Enoch Root in the Nostr ecosystem: Crays founder, Bitcoin believer, and the voice behind the mission. German-born, 20+ years in Spain, living between Dubai, Palma, Medellin and LA, 15 years deep in crypto, now building the world's first Bitcoin-Nostr powered community and hospitality ecosystem.",
        "known_for": [
            ("Founder prologue", "Enoch Root's mission statement explains why Crays exists: loneliness in global travel, the search for real connection and the need for hospitality spaces that bring the right people together."),
            ("Brand and crypto path", "His background connects lifestyle brands such as Ed Hardy, tech plays such as brands4friends and roughly 15 years deep in crypto and Bitcoin thinking."),
            ("Global citizen frame", "German by origin, long based in Spain and living between Dubai, Palma, Medellin and LA, he frames Crays around values as the passport for a global community."),
            ("Privacy and autonomy", "Privacy, freedom of expression and personal autonomy are non-negotiable in the Crays thesis, which is why Nostr and Bitcoin belong close to the foundation."),
        ],
        "crays": "For us, Enoch Root is not an outside ecosystem profile. He is the founder voice behind why we connect Nostr, Bitcoin, hospitality, creator commerce, the Association and the Crays global community into one real-world network.",
        "sources": [
            ("Crays founder prologue", "https://www.crays.org/nostr/people/enoch-root/", "Founder prologue and mission statement for Crays."),
            ("Crays Nostr base layer", "https://www.crays.org/nostr/", "How we connect Nostr, Bitcoin, venues, creators, profiles and governance."),
            ("Crays Association", "https://www.crays.org/en/association/", "Swiss association frame for the Crays ecosystem."),
            ("Crays", "https://www.crays.net/", "Crays-facing profile and community surface."),
        ],
    },
    {
        "slug": "people/fiatjaf",
        "name": "fiatjaf",
        "role": "Original Nostr creator and protocol builder",
        "summary": "fiatjaf is the original author behind Nostr's early protocol work and remains one of the most visible protocol and tooling contributors.",
        "known_for": [
            ("Original protocol work", "The early Nostr repository and NIP process are inseparable from fiatjaf's work."),
            ("Tools and libraries", "Projects associated with him include nostr-tools, go-nostr, khatru, nak, njump, wikistr and other experimental tools."),
            ("Protocol culture", "His work represents the deliberately simple, chaotic and builder-led character of Nostr."),
        ],
        "crays": "For Crays, fiatjaf matters because the protocol's core idea is exactly the base layer Crays needs: signed identity, flexible events and no single platform owner.",
        "sources": [
            ("OpenSats LTS for fiatjaf", "https://opensats.org/blog/fiatjaf-receives-lts-grant", "OpenSats profile of fiatjaf's Nostr work and tools."),
            ("Nostr protocol repository", "https://github.com/nostr-protocol/nostr", "Original Nostr protocol repository."),
            ("Nostr NIPs", "https://github.com/nostr-protocol/nips", "Implementation possibilities and protocol discussions."),
            ("GitHub: fiatjaf", "https://github.com/fiatjaf", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/jack-dorsey",
        "name": "Jack Dorsey",
        "role": "Public supporter, funder and mainstream signal amplifier",
        "summary": "Jack Dorsey's importance to Nostr is not that he owns it. He does not. His role is public support, funding attention and a bridge from mainstream social media debate into open protocol funding.",
        "known_for": [
            ("14 BTC funding story", "Public reporting described a 14 BTC donation to support Nostr development."),
            ("Open social funding", "OpenSats states that The Nostr Fund started in 2023 with a contribution from Dorsey's #startsmall."),
            ("andOtherStuff", "2025 reporting connected Dorsey with an open-source social media collective building Nostr-adjacent apps and tools."),
        ],
        "crays": "For Crays, Dorsey's Nostr relevance is a market signal: the open social layer is no longer a niche technical toy, but a serious alternative to platform-owned identity.",
        "sources": [
            ("OpenSats Nostr Fund", "https://opensats.org/funds/nostr", "Nostr Fund background and #startsmall reference."),
            ("CoinDesk 14 BTC report", "https://www.coindesk.com/tech/2022/12/15/jack-dorsey-gives-decentralized-social-network-nostr-14-btc-in-funding", "Public report on 14 BTC funding."),
            ("TechCrunch andOtherStuff", "https://techcrunch.com/2025/07/16/jack-dorsey-pumps-10m-into-a-nonprofit-focused-on-open-source-social-media/", "Reporting on Dorsey and open-source social media funding."),
            ("Nostr World", "https://nostr.world/", "Nostr event archive and early culture references."),
        ],
    },
    {
        "slug": "people/william-casarin-jb55",
        "name": "William Casarin (jb55)",
        "role": "Damus creator and Bitcoin-Nostr client developer",
        "summary": "William Casarin, known as jb55, is best known for Damus, the iOS Nostr client that helped make Nostr tangible for mainstream mobile users.",
        "known_for": [
            ("Damus", "iOS Nostr client with social feed, zaps, media and relay transparency."),
            ("Notedeck", "Multiplatform Nostr client work for desktop and Android."),
            ("NostrDB and Notecrumbs", "Infrastructure around local event storage and note rendering."),
        ],
        "crays": "For Crays, Damus is an important proof that Nostr can feel like a normal social product while still keeping keys, relays and Lightning close to the surface.",
        "sources": [
            ("OpenSats project: Damus", "https://opensats.org/projects/damus", "Damus project overview and William Casarin context."),
            ("OpenSats LTS for William Casarin", "https://opensats.org/blog/jb55-receives-lts-grant", "Long-term support announcement."),
            ("Damus repository", "https://github.com/damus-io/damus", "Open-source Damus client repository."),
            ("GitHub: jb55", "https://github.com/jb55", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/vitor-pamplona",
        "name": "Vitor Pamplona",
        "role": "Amethyst creator and Android Nostr protocol implementer",
        "summary": "Vitor Pamplona is the creator of Amethyst, one of the most important Android Nostr clients and a frequent testbed for newer Nostr capabilities.",
        "known_for": [
            ("Amethyst", "Configurable Android client with zaps, marketplaces, groups, live streams and Tor support."),
            ("Protocol proposals", "OpenSats describes Vitor as contributing to encrypted messaging and Web-of-Trust work."),
            ("Quartz", "Kotlin library work that helps other Android and multiplatform Nostr projects."),
        ],
        "crays": "For Crays, Vitor's work is useful because it shows how far a full mobile Nostr client can go beyond a simple Twitter-like feed.",
        "sources": [
            ("OpenSats project: Amethyst", "https://opensats.org/projects/amethyst", "Amethyst project overview."),
            ("OpenSats LTS for Vitor Pamplona", "https://opensats.org/blog/vitor-pamplona-receives-lts-grant", "Long-term support announcement."),
            ("Amethyst repository", "https://github.com/vitorpamplona/amethyst", "Open-source Android client repository."),
            ("GitHub: Vitor Pamplona", "https://github.com/vitorpamplona", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/pablof7z",
        "name": "PabloF7z",
        "role": "Nostr Development Kit and experimental product builder",
        "summary": "PabloF7z is one of the prolific Nostr builders behind NDK, nsecBunker and several experiments that push Nostr beyond basic social posting.",
        "known_for": [
            ("Nostr Development Kit", "NDK is a major toolkit for Nostr application development."),
            ("nsecBunker", "Remote-key and signer-oriented infrastructure."),
            ("Highlighter, Shipyard and experiments", "Product experiments that explore the other-stuff side of Nostr."),
        ],
        "crays": "For Crays, Pablo's work matters because the Crays stack will need robust developer tooling, signers, custom relays and app discovery beyond simple posting.",
        "sources": [
            ("OpenSats LTS for PabloF7z", "https://opensats.org/blog/pablofz7-receives-lts-grant", "Long-term support announcement and project list."),
            ("Nostr Development Kit", "https://github.com/nostr-dev-kit/ndk", "NDK repository."),
            ("GitHub: PabloF7z", "https://github.com/pablof7z", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/hodlbod",
        "name": "Hodlbod",
        "role": "Coracle creator, Web-of-Trust and relay-selection builder",
        "summary": "Hodlbod is the creator of Coracle and a visible builder around relay selection, Web-of-Trust moderation, recommendations and privacy.",
        "known_for": [
            ("Coracle", "Web-based Nostr client focused on relay selection, Web-of-Trust and communities."),
            ("Welshman and Triflector", "Libraries and relay experiments connected to Coracle work."),
            ("Thank God for Nostr", "Podcast conversations with Nostr developers and contributors."),
        ],
        "crays": "For Crays, Hodlbod's work is important because discovery, relay choice and Web-of-Trust are exactly what a real venue and creator ecosystem needs.",
        "sources": [
            ("OpenSats LTS for Hodlbod", "https://opensats.org/blog/hodlbod-receives-lts-grant", "Long-term support announcement."),
            ("Coracle", "https://coracle.social/", "Coracle web client."),
            ("Coracle repository", "https://github.com/coracle-social/coracle", "Open-source Coracle repository."),
            ("GitHub: staab", "https://github.com/staab", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/yuki-kishimoto",
        "name": "Yuki Kishimoto",
        "role": "rust-nostr creator and library maintainer",
        "summary": "Yuki Kishimoto is the creator and maintainer of rust-nostr, a Rust implementation that supports client libraries, Nostr Wallet Connect and performance-oriented Nostr applications.",
        "known_for": [
            ("rust-nostr", "Rust implementation of the Nostr protocol and high-level client library."),
            ("Language bindings", "Work that helps Nostr reach more environments and application stacks."),
            ("Future NIPs and documentation", "OpenSats describes ongoing work on outbox, bindings, tests and the Rust Nostr Book."),
        ],
        "crays": "For Crays, rust-nostr matters for serious infrastructure: relays, embedded systems, wallet connections, Super Nodes and performance-sensitive services.",
        "sources": [
            ("OpenSats LTS for Yuki Kishimoto", "https://opensats.org/blog/yuki-receives-lts-grant", "Long-term support announcement."),
            ("rust-nostr repository", "https://github.com/rust-nostr/nostr", "Rust Nostr implementation."),
            ("GitHub: Yuki Kishimoto", "https://github.com/yukibtc", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/mike-dilger",
        "name": "Mike Dilger",
        "role": "Gossip lead developer and outbox-model contributor",
        "summary": "Mike Dilger is known for Gossip, a Nostr client focused on privacy, security and Rust-native implementation choices.",
        "known_for": [
            ("Gossip", "Nostr client built with privacy and security priorities."),
            ("Outbox model", "OpenSats describes Gossip as a reference implementation for scalable message distribution."),
            ("Relay tooling", "Work around relay testing, relay behavior and NIP discussions."),
        ],
        "crays": "For Crays, Mike Dilger's work is useful because local infrastructure needs strong relay strategy, privacy thinking and robust client behavior.",
        "sources": [
            ("OpenSats LTS for Mike Dilger", "https://opensats.org/blog/mike-dilger-receives-lts-grant", "Long-term support announcement."),
            ("Gossip repository", "https://github.com/mikedilger/gossip", "Open-source Gossip client repository."),
            ("GitHub: Mike Dilger", "https://github.com/mikedilger", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/hzrd149",
        "name": "hzrd149",
        "role": "noStrudel and Blossom builder",
        "summary": "hzrd149 builds noStrudel, a web-based Nostr exploration client, and Blossom, a file-storage approach for media and portability.",
        "known_for": [
            ("noStrudel", "Power-user client and learning tool for exploring the Nostr protocol."),
            ("Blossom", "Blobs Stored Simply on Mediaservers, focused on file storage and organization."),
            ("Developer education", "Tools that make protocol exploration easier for builders."),
        ],
        "crays": "For Crays, hzrd149's work matters because creator media, content access and venue assets need sane file storage and inspection tools.",
        "sources": [
            ("OpenSats LTS for hzrd149", "https://opensats.org/blog/hzrd149-receives-lts-grant", "Long-term support announcement."),
            ("noStrudel", "https://nostrudel.ninja/", "Nostr web client."),
            ("Blossom repository", "https://github.com/hzrd149/blossom", "Blossom file-storage project."),
            ("GitHub: hzrd149", "https://github.com/hzrd149", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/stuart-bowman",
        "name": "Stuart Bowman",
        "role": "Satellite Earth maintainer and community infrastructure builder",
        "summary": "Stuart Bowman is the main developer and maintainer of Satellite Earth, a web-based Nostr client and CDN/server stack for self-sovereign communities.",
        "known_for": [
            ("Satellite Earth", "Client and infrastructure stack for Nostr communities."),
            ("Satellite nodes", "Public and private node concepts for community-owned infrastructure."),
            ("Satellite CDN", "Blossom-compatible CDN work for media, authentication, payments and indexing."),
        ],
        "crays": "For Crays, Stuart's work is directly relevant to venue and community infrastructure because Crays needs local nodes, media, payments and self-reliant communities.",
        "sources": [
            ("OpenSats LTS for Stuart Bowman", "https://opensats.org/blog/stuart-bowman-receives-lts-grant", "Long-term support announcement."),
            ("Satellite Earth", "https://satellite.earth/", "Satellite web client and community stack."),
            ("GitHub: lovvtide", "https://github.com/lovvtide", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/alex-gleason",
        "name": "Alex Gleason",
        "role": "Ditto, Soapbox, Mostr Bridge and Nostrify builder",
        "summary": "Alex Gleason builds across the Nostr and fediverse boundary, including Ditto, Mostr Bridge, Soapbox, Nostrify and Letr.",
        "known_for": [
            ("Ditto", "Self-hosted social media server with built-in Nostr client and relay."),
            ("Mostr Bridge", "Bridge between Nostr and the fediverse."),
            ("Nostrify and Letr", "Developer and creator-oriented Nostr tools."),
        ],
        "crays": "For Crays, Alex's work is useful because the market will not be one protocol island. Bridges, self-hosting and creator tools matter.",
        "sources": [
            ("OpenSats LTS for Alex Gleason", "https://opensats.org/blog/alex-gleason-receives-lts-grant", "Long-term support announcement."),
            ("GitHub: Alex Gleason", "https://github.com/alexgleason", "Public GitHub profile."),
            ("Soapbox GitHub", "https://github.com/soapbox-pub", "Soapbox public organization."),
        ],
    },
    {
        "slug": "people/evan-henshaw-plath-rabble",
        "name": "Evan Henshaw-Plath (Rabble)",
        "role": "Nos founder, decentralized social pioneer and Nostr app builder",
        "summary": "Evan Henshaw-Plath, also known as Rabble, is the founder and creator of Nos and a long-time decentralized social media builder.",
        "known_for": [
            ("Nos", "Ad-free social app built on Nostr with user control as a central message."),
            ("Planetary transition", "Planetary describes its team moving its design and philosophy to Nostr through Nos."),
            ("Open social media history", "Nos describes Rabble's earlier work around Odeo, Twitter and commons-based social software."),
        ],
        "crays": "For Crays, Rabble's work is relevant because it frames Nostr as a human social product, not only a developer protocol.",
        "sources": [
            ("Nos team page", "https://www.nos.social/team/rabble", "Evan Henshaw-Plath profile."),
            ("Nos about page", "https://www.nos.social/about", "Nos founder and Nostr positioning."),
            ("Nos homepage", "https://www.nos.social/", "Nos product positioning."),
            ("Planetary", "https://www.planetary.social/", "Planetary team moving to Nostr and Nos."),
        ],
    },
    {
        "slug": "people/martti-malmi",
        "name": "Martti Malmi",
        "role": "Iris developer and early Bitcoin contributor",
        "summary": "Martti Malmi is known in Bitcoin history and in Nostr for Iris, a Nostr client for better social networking, and newer Nostr-based privacy work.",
        "known_for": [
            ("Iris", "Nostr Android, iOS and web client for social networking."),
            ("Early Bitcoin context", "Public reporting frequently identifies Malmi as an early Bitcoin contributor and Satoshi collaborator."),
            ("Nostr VPN", "Recent reporting describes a Nostr-key based VPN approach from Malmi."),
        ],
        "crays": "For Crays, Iris and Nostr VPN show the breadth of Nostr identity: social, privacy and access workflows can share key-based identity ideas.",
        "sources": [
            ("Iris FAQ", "https://github.com/irislib/faq", "Iris documentation and developer note."),
            ("Iris GitHub organization", "https://github.com/irislib", "Iris repositories."),
            ("Grafa Nostr VPN report", "https://grafa.com/en/news/crypto/nostr-vpn-martti-malmi", "Reporting on Malmi and Nostr VPN."),
            ("GitHub: Martti Malmi", "https://github.com/mmalmi", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/greenart7c3",
        "name": "Greenart7c3",
        "role": "Amber signer and Android key-safety builder",
        "summary": "Greenart7c3 builds Amber, a Nostr signer for Android that helps users keep private keys out of ordinary clients.",
        "known_for": [
            ("Amber", "Android signer that holds the nsec so other apps can request signatures without seeing the key."),
            ("Citrine", "Sibling Android Nostr infrastructure work referenced by OpenSats."),
            ("Remote signing UX", "Practical work around NIP-46 and app permissions."),
        ],
        "crays": "For Crays, Amber is a model for key-safety UX. Any Crays login or voting flow should avoid teaching users to paste secrets into web pages.",
        "sources": [
            ("OpenSats project: Amber", "https://opensats.org/projects/amber", "Amber project overview."),
            ("OpenSats LTS for Greenart7c3", "https://opensats.org/blog/greenart7c3-receives-lts-grant", "Long-term support announcement."),
            ("Nostr Apps: Amber", "https://nostrapps.com/amber", "Amber app listing."),
            ("GitHub: greenart7c3", "https://github.com/greenart7c3", "Public GitHub profile."),
        ],
    },
    {
        "slug": "people/miljan-braticevic",
        "name": "Miljan Braticevic",
        "role": "Primal CEO and Nostr consumer-app operator",
        "summary": "Miljan Braticevic is CEO of Primal, one of the most visible Nostr consumer app and infrastructure companies.",
        "known_for": [
            ("Primal", "Nostr social app and infrastructure stack for discovery, search, feeds and analytics."),
            ("Seed funding", "Public announcements described Primal's seed round for Bitcoin-infused Nostr apps."),
            ("Consumer onboarding", "Primal is important because it tries to make Nostr feel usable to ordinary social users."),
        ],
        "crays": "For Crays, Primal shows the importance of product polish, discovery and onboarding when an open protocol needs mainstream users.",
        "sources": [
            ("Primal launch announcement", "https://www.prnewswire.com/news-releases/primal-launches-new-social-network-for-digital-freedom-301877265.html", "Primal launch and Miljan Braticevic quote."),
            ("Primal downloads", "https://primal.net/downloads", "Primal app download page."),
            ("Power of Lightning Summit", "https://pretalx.com/power-of-lightning-summit-2023/talk/F7HTZC/", "Miljan listed as CEO of Primal in a Lightning and Nostr session."),
        ],
    },
    {
        "slug": "people/lyn-alden",
        "name": "Lyn Alden",
        "role": "Long-form analyst and Nostr media voice",
        "summary": "Lyn Alden gives Nostr a rare kind of outside explanation: protocol thinking, internet history, money, identity and platform power in one readable long-form frame.",
        "known_for": [
            ("The Power of Nostr", "A widely shared essay that explains Nostr as more than another social app: a protocol pattern for identity and communication."),
            ("Macro and Bitcoin analysis", "Her broader work connects monetary systems, open networks and long-term technology adoption."),
            ("Reader bridge", "She helps financially literate and technically curious readers understand why open social protocols matter."),
        ],
        "crays": "For us, Lyn Alden matters because her writing helps serious readers see why Nostr belongs next to Bitcoin, identity, payments and long-lived public infrastructure instead of being dismissed as a niche feed.",
        "sources": [
            ("The Power of Nostr", "https://www.lynalden.com/the-power-of-nostr/", "Long-form Nostr essay by Lyn Alden."),
            ("Lyn Alden website", "https://www.lynalden.com/", "Author website and long-form research archive."),
            ("Nostr media archive", "https://www.crays.org/nostr/nostr-media-article-video-archive/", "Crays media and video archive context."),
        ],
    },
    {
        "slug": "people/sarah-perez",
        "name": "Sarah Perez",
        "role": "TechCrunch reporter covering consumer social apps and open social funding",
        "summary": "Sarah Perez belongs in the Nostr people archive as a media voice because her TechCrunch reporting brought Damus, Nostr-adjacent social apps and open-social funding into mainstream technology coverage.",
        "known_for": [
            ("Damus coverage", "TechCrunch coverage helped explain Damus and Nostr to a mainstream consumer-app audience."),
            ("Open social funding", "Reporting on Jack Dorsey and open-source social media funding gives readers context beyond one protocol page."),
            ("Consumer app lens", "Her work frames Nostr in the world of app stores, social products, moderation and mainstream adoption."),
        ],
        "crays": "For us, Perez is useful because she represents the mainstream media layer. If Nostr is going to reach normal users, the story has to survive outside developer circles.",
        "sources": [
            ("TechCrunch Damus report", "https://techcrunch.com/2023/02/01/damus-another-decentralized-social-networking-app-arrives-to-take-on-twitter/", "Sarah Perez on Damus and Nostr."),
            ("TechCrunch open social funding report", "https://techcrunch.com/2025/07/16/jack-dorsey-pumps-10m-into-a-nonprofit-focused-on-open-source-social-media/", "Sarah Perez on Dorsey, open-source social media and funding."),
            ("Sarah Perez author page", "https://techcrunch.com/author/sarah-perez/", "TechCrunch author archive."),
        ],
    },
    {
        "slug": "people/george-kaloudis",
        "name": "George Kaloudis",
        "role": "CoinDesk writer and Bitcoin-Nostr funding chronicler",
        "summary": "George Kaloudis is included as a media representative because his CoinDesk reporting helped document the 14 BTC Nostr funding story that pulled mainstream attention toward the protocol.",
        "known_for": [
            ("14 BTC Nostr funding report", "CoinDesk coverage of Jack Dorsey's Nostr funding became part of the public origin-story layer around Nostr."),
            ("Bitcoin market context", "His work sits at the intersection of Bitcoin reporting, open protocols and market attention."),
            ("Funding signal", "The article is useful because it explains why the ecosystem suddenly became visible beyond early builders."),
        ],
        "crays": "For us, Kaloudis matters because funding stories shape public trust. The article helps readers understand why Nostr's open-social thesis became economically credible to more people.",
        "sources": [
            ("CoinDesk 14 BTC report", "https://www.coindesk.com/tech/2022/12/15/jack-dorsey-gives-decentralized-social-network-nostr-14-btc-in-funding", "George Kaloudis report on Nostr funding."),
            ("CoinDesk author page", "https://www.coindesk.com/author/george-kaloudis", "CoinDesk author archive."),
        ],
    },
    {
        "slug": "people/ben-perrin-btc-sessions",
        "name": "Ben Perrin (BTC Sessions)",
        "role": "Bitcoin educator and Nostr video tutor",
        "summary": "Ben Perrin, known through BTC Sessions, is a useful Nostr media voice because his tutorial format turns Lightning, wallet and infrastructure workflows into steps normal builders can follow.",
        "known_for": [
            ("BTC Sessions tutorials", "Long-form Bitcoin education with practical screen-by-screen workflows."),
            ("Nostr Toolkit with Voltage", "A detailed route for connecting Nostr, Lightning nodes and wallet infrastructure."),
            ("Operational education", "His videos are strongest when a reader needs to move from concept to setup."),
        ],
        "crays": "For us, BTC Sessions is relevant because Nostr education cannot stop at theory. Wallets, nodes, zaps and infrastructure need practical guides if the system should feel usable.",
        "sources": [
            ("BTC Sessions YouTube", "https://www.youtube.com/@BTCSessions", "BTC Sessions YouTube channel."),
            ("Nostr Toolkit with Voltage", "https://www.youtube.com/watch?v=S6y2Vy2N9oY", "Nostr and Lightning node tutorial."),
            ("BTC Sessions website", "https://www.btcsessions.ca/", "BTC Sessions education site."),
        ],
    },
    {
        "slug": "people/derek-ross",
        "name": "Derek Ross",
        "role": "Nostr educator, Nostr World host and event media voice",
        "summary": "Derek Ross is part of the Nostr media layer because he appears across beginner videos, Nostr World event material and public community education.",
        "known_for": [
            ("Nostr for Beginners", "A Nostr World beginner session that helps new readers connect vocabulary, culture and setup."),
            ("Nostr World and Nostrica material", "Event videos and Q&A sessions that preserve the human scene around the protocol."),
            ("Public education", "He is useful as a bridge between builders, events and new users."),
        ],
        "crays": "For us, Derek Ross matters because a living Nostr archive needs educators and event voices, not only protocol authors. He helps readers see the scene that makes the protocol social.",
        "sources": [
            ("Nostr for Beginners", "https://www.youtube.com/watch?v=NVm_jGdwTjQ", "Nostr World beginner video with Derek Ross."),
            ("Nostrica Q&A", "https://www.youtube.com/watch?v=WOYum10HaxY", "Nostr World Nostrica Q&A video."),
            ("Nostr World speakers", "https://nostr.world/speakers/index.html", "Public Nostr World speaker archive."),
        ],
    },
    {
        "slug": "people/roger-huang",
        "name": "Roger Huang",
        "role": "Forbes Bitcoin writer and Nostr media voice",
        "summary": "Roger Huang belongs in the Nostr media layer because his Forbes guide helped translate Nostr for a wider Bitcoin and digital-assets audience.",
        "known_for": [
            ("Forbes Nostr guide", "His Forbes work gives mainstream readers a structured entry into Nostr without assuming protocol background."),
            ("Bitcoin and geopolitics reporting", "His public author profile frames his work around Bitcoin, money, censorship, geopolitics and digital assets."),
            ("Nostr identity signal", "His Forbes profile publicly lists a Nostr identity, which makes him relevant as both author and participant."),
        ],
        "crays": "For us, Roger Huang is useful because serious media translation helps creators, investors and operators understand why Nostr is more than a niche social app.",
        "sources": [
            ("Roger Huang on Forbes", "https://www.forbes.com/sites/rogerhuang/", "Forbes author profile and public Nostr identity reference."),
            ("Forbes guide to Nostr", "https://www.forbes.com/sites/digital-assets/2024/07/17/your-guide-to-nostr-the-decentralized-network-for-everything/", "Mainstream guide to Nostr for digital-assets readers."),
        ],
    },
    {
        "slug": "people/m-k-fain",
        "name": "M. K. Fain",
        "role": "Soapbox writer and beginner Nostr explainer",
        "summary": "M. K. Fain belongs in the Nostr media layer because Soapbox's beginner material helps non-technical readers understand clients, accounts and first steps.",
        "known_for": [
            ("Nostr 101", "Soapbox's beginner guide explains how to join Nostr, create an account and choose apps."),
            ("Soapbox and Ditto context", "The surrounding work connects Nostr education with open-source social software and user-owned publishing."),
            ("Plain-language onboarding", "The useful contribution is reader translation: lowering vocabulary pressure without hiding the open-network model."),
        ],
        "crays": "For us, M. K. Fain is a useful media profile because onboarding language matters as much as protocol correctness when people first meet Nostr.",
        "sources": [
            ("M. K. Fain on Soapbox", "https://soapbox.pub/blog/author/m-k-fain", "Soapbox author archive."),
            ("Nostr 101 on Soapbox", "https://soapbox.pub/blog/nostr101", "Beginner guide to Nostr apps and account setup."),
        ],
    },
    {
        "slug": "people/ez-no-bullshit-bitcoin",
        "name": "EZ",
        "role": "No Bullshit Bitcoin editor and Nostr release tracker",
        "summary": "EZ belongs in the Nostr media layer because No Bullshit Bitcoin tracks product releases, Bitcoin-Nostr infrastructure and practical app changes without turning every item into hype.",
        "known_for": [
            ("Primal release coverage", "The Primal v2.0 article is a concrete product-history reference for Nostr clients, reads, wallets and onboarding."),
            ("Release-desk style", "No Bullshit Bitcoin creates short, source-heavy updates that are useful for an archive because they preserve dates and product context."),
            ("Bitcoin-Nostr overlap", "The publication follows the places where Bitcoin, Lightning, wallets and Nostr applications meet."),
        ],
        "crays": "For us, EZ is useful because release tracking helps the archive explain not only what Nostr is, but how the product layer changes over time.",
        "sources": [
            ("EZ on No Bullshit Bitcoin", "https://www.nobsbitcoin.com/author/ez/", "No Bullshit Bitcoin author archive."),
            ("Primal v2.0 coverage", "https://www.nobsbitcoin.com/primal-v2-0/", "Product release article for Primal v2.0."),
        ],
    },
    {
        "slug": "people/yiluo-wei",
        "name": "Yiluo Wei",
        "role": "Nostr empirical research author",
        "summary": "Yiluo Wei belongs in the People archive as a research author behind one of the early empirical studies of Nostr decentralization, availability and replication overhead.",
        "known_for": [
            ("Empirical Nostr study", "The arXiv paper studies the Nostr ecosystem across July to December 2023 and gives the archive a measurement-based view of relays and network behavior."),
            ("Decentralization and resilience framing", "The paper is useful because it tests Nostr as an operating network, not just as a protocol promise."),
            ("Research bridge", "The work helps connect technical claims about relays and availability to actual observed behavior."),
        ],
        "crays": "For us, Yiluo Wei matters because a serious Nostr knowledge hub needs measurement research beside builder stories and product pages.",
        "sources": [
            ("Exploring the Nostr Ecosystem", "https://arxiv.org/abs/2402.05709", "arXiv abstract and author list for the empirical Nostr study."),
            ("HTML paper", "https://arxiv.org/html/2402.05709v2", "Readable HTML version of the paper."),
        ],
    },
    {
        "slug": "people/gareth-tyson",
        "name": "Gareth Tyson",
        "role": "Nostr empirical research co-author",
        "summary": "Gareth Tyson belongs in the People archive as a co-author of the empirical Nostr ecosystem study and a researcher connected to decentralized social-network measurement.",
        "known_for": [
            ("Nostr measurement research", "The paper co-authored with Yiluo Wei examines decentralization, availability and replication overhead in Nostr."),
            ("Social-network systems research", "His public research trail sits around online social systems, decentralized networks and measurement work."),
            ("Evidence layer", "The useful role for our archive is turning broad protocol claims into questions that can be measured."),
        ],
        "crays": "For us, Gareth Tyson is part of the evidence layer: he helps anchor Nostr infrastructure discussion in research rather than only community belief.",
        "sources": [
            ("Exploring the Nostr Ecosystem", "https://arxiv.org/abs/2402.05709", "arXiv abstract and author list for the empirical Nostr study."),
            ("HTML paper", "https://arxiv.org/html/2402.05709v2", "Readable HTML version of the paper."),
        ],
    },
]


PEOPLE_DEEP_READS = {
    "people/enoch-root": [
        "Enoch Root is the founder voice behind the Crays prologue. The story starts with movement: German-born, more than 20 years in Spain, life between Dubai, Palma, Medellin and LA, and more than two decades with over 250 travel days a year. That kind of life creates a sharp sense of what global people miss when they are always somewhere and still not fully at home.",
        "His business path joins two worlds our ecosystem needs to keep together. On one side are lifestyle brands, hospitality, culture, scenes and the feeling of belonging, including brand work around Ed Hardy. On the other side are technology, brands4friends, crypto, Bitcoin and the question of how ordinary people build wealth when the old ladder has become brutally hard to climb.",
        "The people layer matters just as much. Enoch's prologue is built around thousands of meetings with people whose stories made travel feel larger and more human. It also comes from the opposite experience: lonely hotel-room nights, not knowing who was in the same city, who shared the same values and how to meet the right people at the right time without turning life into a networking spreadsheet.",
        "The 2008 Lehman collapse and the Spanish real estate crash from 2007 to 2013 turned the money question from theory into lived urgency. Watching people in Spain, Greece, Portugal and Ireland get hit by that system led to the deeper obsession: what is money, really, and how can the next generation create wealth without being born into it?",
        "That obsession took him into crypto when it was still shady and underground, then toward Web3, and finally back to the harder question: how do you build wealth creation for the next generation? Property, savings and inflation have made upward mobility brutally difficult for young people. That is why Bitcoin's deflationary model, old-school cooperative logic and the Crays Association frame sit together.",
        "The point is not only a nicer social app. The point is a global community that can own more of its identity, reputation, demand, access and economic upside together. In Enoch's framing, your values are your passport. It does not matter where you are from, what you look like or what religion you practice. A real community also has boundaries, including the courage to say when someone will not engage with those values.",
        "The hospitality layer comes from the practical question every serious traveler eventually asks: who is here, who shares the right values, who is building, who is worth meeting and where can I feel at home without pretending work and life are separate species? That is where Work, Live and Play becomes one system instead of a slogan.",
        "Privacy, freedom of expression and personal autonomy are the hard line. No privacy, no democracy. We are building against surveillance culture, platform lock-in and the quiet normalization of control. That is where Nostr stops being a protocol curiosity and becomes part of our operating spine.",
        "Enoch's prologue also makes the founder economics explicit: he does not want a salary, but 0.25% of every transaction in the Crays global ecosystem flows into a wallet tied to him personally as retirement. He frames that openly because incentives matter. When he is gone, everything passes into a foundation so the mission can keep going with the community and the Association.",
        "The short version is Work, Live and Play as one global community. Crays is for people, digital and IRL. Do not predict the future. Let us go out and build it together.",
    ],
    "people/fiatjaf": [
        "fiatjaf is not interesting because he gives Nostr a neat founder myth. He is interesting because Nostr still feels like the kind of protocol a stubborn builder would invent after getting tired of social platforms, federation committees and product teams that want permission before anything can move. The core is almost annoyingly small: keys, signed events, relays, clients. That smallness is the trick.",
        "His public work around tooling matters because it shows Nostr as a working bench, not a finished showroom. nostr-tools, nak, khatru and the wider pile of experiments make the protocol easier to touch, break, inspect and extend. For Crays, that is the important lesson: keep the base layer brutally portable, then build the lifestyle product with taste on top of it.",
    ],
    "people/jack-dorsey": [
        "Jack Dorsey belongs in the archive for a very specific reason: he helped make the open social conversation visible to people who would otherwise never read a NIP. That does not make Nostr his platform. It makes his support a loud signal that the old social-media power structure is no longer the only serious path.",
        "The useful read is not celebrity worship. It is market psychology. Funding, attention and public confidence can pull developers into a young protocol faster than a perfect technical explainer ever will. Crays should treat that as proof that open identity and social portability have crossed from internet subculture into real business territory.",
    ],
    "people/william-casarin-jb55": [
        "William Casarin matters because Damus made Nostr feel like something normal people could actually open on a phone. A protocol can be elegant and still fail if the first consumer surface feels hostile. Damus helped translate keys, relays, notes and zaps into an iOS habit, and that changed the psychological distance between Nostr and regular social apps.",
        "The Crays lesson is product courage. Keep enough of the open-protocol reality visible that users understand what they own, but do not make every screen feel like a developer console. Crays.net has to do the same dance: portable identity underneath, warm lifestyle experience on the surface.",
    ],
    "people/vitor-pamplona": [
        "Vitor Pamplona is a good example of Nostr's strange advantage: one client can become a living laboratory for the whole protocol. Amethyst is not just an Android feed. It has exposed users to zaps, groups, marketplaces, live streams, Tor support and newer protocol ideas before the rest of the market has agreed on a polished mainstream shape.",
        "That makes his work especially useful for Crays. When you want creator commerce, venue access, status, media and payments to live near each other, you need to see how far a client can stretch before it becomes confusing. Amethyst is one of the places where that question is being tested in public.",
    ],
    "people/pablof7z": [
        "PabloF7z sits close to the engine room. NDK, nsecBunker and his experiments matter because app builders need fewer excuses. A protocol can have all the right ideas and still be too expensive to build on if every team has to reinvent relay handling, event flows, signing assumptions and edge-case behavior from scratch.",
        "For Crays, this is not abstract developer trivia. A Crays profile, award vote, content sale, venue relay or signer flow will only feel smooth if the boring middle layer is strong. Pablo's work points to that middle: the part users never thank you for, but absolutely feel when it breaks.",
    ],
    "people/hodlbod": [
        "Hodlbod is important because Coracle refuses to pretend that discovery, relays and trust are solved just because a protocol exists. The hard part of Nostr is not posting a note. The hard part is finding the right people, reading from the right places, filtering the noise and keeping enough control without turning the product into homework.",
        "That is directly Crays-relevant. A hospitality and creator network cannot run on a dumb feed. It needs social trust, relay strategy, recommendations, community context and taste. Coracle's work around Web-of-Trust and relay selection is one of the more serious attempts to make that messy reality usable.",
    ],
    "people/yuki-kishimoto": [
        "Yuki Kishimoto represents the kind of contributor most readers will never notice until everything depends on him. rust-nostr is not a shiny consumer brand. It is infrastructure: libraries, bindings, wallet-connect work, tests, documentation and the kind of careful implementation layer that lets serious products stop improvising.",
        "For Crays, that matters because Super Nodes, venue infrastructure, wallet hooks and performance-sensitive services need stronger foundations than a weekend demo. Rust infrastructure is where Nostr starts looking less like a cool idea and more like something you can operate.",
    ],
    "people/mike-dilger": [
        "Mike Dilger's Gossip work is valuable because it comes from a different product instinct than the race to make Nostr look like every other social app. Gossip cares about privacy, relay strategy, local behavior and the outbox model. It asks: what would a client look like if safety and routing were not afterthoughts?",
        "Crays should pay attention to that question. Local venues, member context, payments and reputation cannot be built on casual assumptions about where events live and who can infer what. Mike's work is a reminder that the grown-up version of Nostr has to care about metadata, not only public posts.",
    ],
    "people/hzrd149": [
        "hzrd149 is useful to understand because noStrudel and Blossom expose two sides of Nostr that often get hidden. noStrudel is a protocol cockpit: it lets curious users and builders see more of what is actually going on. Blossom is the media problem approached directly: files, blobs, storage and portability beyond a text-only feed.",
        "That is a Crays problem too. Creator content, venue media, paid assets and profile material need storage patterns that are understandable and durable. The social graph is one layer. Media logistics are another. hzrd149 works where those two layers start bumping into each other.",
    ],
    "people/stuart-bowman": [
        "Stuart Bowman and Satellite Earth matter because they pull Nostr toward community-owned infrastructure instead of only app-store clients. Satellite is about clients, nodes, media, payments, indexing and the practical work of giving a community more control over its own network surface.",
        "That maps cleanly to Crays. A Crays venue or local community should not feel like it is renting its entire digital memory from someone else's feed. Local nodes, media infrastructure and self-sovereign community spaces are exactly where hospitality and protocol start to become one product.",
    ],
    "people/alex-gleason": [
        "Alex Gleason is interesting because he does not treat Nostr like an island with a border guard. Ditto, Mostr Bridge, Soapbox, Nostrify and Letr all point toward a messier but more realistic future: users and communities will move across protocols, interfaces and hosting models.",
        "For Crays, that is healthy. The ecosystem will not be won by pretending everyone must use one client forever. Bridges, self-hosted servers and creator tools help Crays think about portability as a real operating principle, not a slogan printed above a locked product.",
    ],
    "people/evan-henshaw-plath-rabble": [
        "Rabble brings a long memory to the Nostr conversation. Nos is not just another client badge in a directory. It comes from someone who has watched social software evolve through blogging, Twitter, open networks, mobile apps and the recurring mistake of letting one company own too much of the public square.",
        "That history matters because Crays is not trying to impress only protocol people. It has to feel socially alive. Nos points toward the human side of Nostr: calm onboarding, user control, no ads, less platform drama and a product voice that does not make the reader feel like they joined a technical mailing list by accident.",
    ],
    "people/martti-malmi": [
        "Martti Malmi is one of those names where Bitcoin history and Nostr's present touch. Iris keeps him relevant in the client landscape, while newer privacy work shows how Nostr-style keys can move beyond posting into access, identity and network behavior.",
        "The Crays angle is breadth. A portable key is not only a login. It can become the thread between social identity, privacy tools, paid access and trusted services. Martti's work is a reminder that Nostr's identity model has use cases far outside a timeline.",
    ],
    "people/greenart7c3": [
        "Greenart7c3 matters because Amber focuses on one of the least glamorous but most important problems in Nostr: users should not be trained to paste private keys into random apps. If Nostr is going to reach normal people, signing has to become safer without becoming scary.",
        "For Crays, this is non-negotiable. Award votes, profiles, payments, status and venue access all become dangerous if onboarding teaches bad key habits. Amber is a good mental model: let apps request actions, but keep the secret in a dedicated place with permissions the user can understand.",
    ],
    "people/miljan-braticevic": [
        "Miljan Braticevic matters because Primal treats Nostr as a consumer product challenge, not only a protocol experiment. Feeds, search, reads, discovery, onboarding and analytics are not decoration. They are how a new user decides whether this strange open network is worth a second day.",
        "That is an important Crays lesson. A lifestyle ecosystem cannot ask users to love infrastructure first. It has to make the network feel rewarding, searchable and alive. Primal shows how much polish and product judgment matter once Nostr leaves the builder circle.",
    ],
    "people/lyn-alden": [
        "Lyn Alden is useful in the Nostr archive because she writes from outside the small builder room without flattening the subject. Her strongest Nostr value is not a breaking-news angle. It is the long-form ability to explain why protocol ownership, identity, money and public communication belong in the same conversation.",
        "That matters for Crays because many serious readers do not arrive through Damus or a NIP. They arrive through Bitcoin, macro, censorship, platform risk or the question of how the internet keeps producing closed gardens. Alden's essay gives those readers a bridge into Nostr without making the protocol feel like a toy.",
    ],
    "people/sarah-perez": [
        "Sarah Perez belongs here as a media voice because mainstream product coverage changes who enters the room. When TechCrunch explains Damus, app-store distribution or open-source social funding, Nostr stops being only a builder conversation and becomes a consumer-technology story.",
        "For Crays, that distinction matters. We need Nostr to be understandable to creators, operators, investors and normal users. Consumer reporters translate rough protocol culture into the questions ordinary people ask: what app is this, why should I care, who funds it, what can I do with it and how is it different from what I already use?",
    ],
    "people/george-kaloudis": [
        "George Kaloudis is here because the 14 BTC funding story became part of Nostr's public memory. Funding stories are not the protocol, but they shape attention. They tell builders that work might be supported and tell readers that a strange new network is not happening entirely in the dark.",
        "The Crays use is simple: funding context helps explain why Nostr moved from obscure protocol idea to a credible open-social contender. It also keeps the Jack Dorsey story in the right frame: signal and support, not ownership.",
    ],
    "people/ben-perrin-btc-sessions": [
        "Ben Perrin is valuable because his format answers the question many articles skip: what do I actually click next? Nostr education has a theory layer, but wallets, nodes, zaps and signers become real only when someone shows the messy operational steps.",
        "That is directly useful for Crays. If we want readers to understand Nostr Wallet Connect, Lightning zaps, app permissions and value flow, video tutorials can carry the practical load while our written pages explain the system logic.",
    ],
    "people/derek-ross": [
        "Derek Ross is a media and event voice rather than only a single-product builder. That makes him useful for the archive because Nostr spreads through explanation, public demos, event Q&A and repeated social translation.",
        "For Crays, the lesson is that a knowledge hub needs hosts and educators. The protocol gets easier when someone can point at a screen, name the pieces and connect builders to newcomers without making the reader feel late to a private club.",
    ],
    "people/roger-huang": [
        "Roger Huang is useful because Forbes reaches readers who may know Bitcoin, censorship risk or digital assets, but have not yet touched a Nostr client. A mainstream guide can make Nostr legible without asking the reader to start with NIP-01, relay filters or key formats.",
        "For us, the important role is translation. Media writers who can connect money, identity, platforms and open networks help the archive become more than a technical catalog. They bring in the serious outsider questions that a good knowledge hub must answer plainly.",
    ],
    "people/m-k-fain": [
        "M. K. Fain belongs in the archive because beginner writing is not low-value work. Nostr loses people quickly when the first explanation jumps from keys to relays to apps without a calm path. Soapbox's Nostr 101 material helps turn the first session into something a normal reader can try.",
        "For us, that is a content-design lesson. The onboarding page is part of the product. If a reader leaves with the right first mental model, every deeper page becomes easier: clients are windows, relays carry events, keys own identity and no single app owns the account.",
    ],
    "people/ez-no-bullshit-bitcoin": [
        "EZ represents the release-tracking side of Nostr media. A good archive needs product history: when Primal shipped a new version, what changed, why it mattered, which wallet or read features were part of the release and how the wider Bitcoin-Nostr surface was evolving.",
        "For us, those short product notes are not disposable news. They are source trail. They help us date claims, explain app maturity and show readers that Nostr is a moving ecosystem rather than a frozen protocol diagram.",
    ],
    "people/yiluo-wei": [
        "Yiluo Wei's role is important because Nostr also needs measurement. The empirical paper looks at decentralization, availability and replication overhead in a real network window, which is exactly the sort of evidence a serious relay or infrastructure article should have nearby.",
        "For us, research authors give the archive a different kind of authority. Builder pages tell you what people are trying to make. Research pages help you ask what the network is actually doing and where the design creates tradeoffs.",
    ],
    "people/gareth-tyson": [
        "Gareth Tyson belongs beside Yiluo Wei because the same paper gives Nostr a measured systems view. It studies whether the network lives up to its decentralization promise, how relays affect availability and what replication means in practice.",
        "For us, that research lens matters for Super Nodes, relay strategy and long-term archive thinking. If we want a real knowledge system, we need both narrative and measurement: human context, product context and technical evidence.",
    ],
}


def person_deep_read(person: dict) -> list[str]:
    fallback = [
        f"{person['name']} belongs here because their public work gives readers a concrete door into Nostr. The ecosystem is easier to understand when it is attached to real projects, tradeoffs and product choices instead of floating protocol theory.",
        "For Crays, the useful question is always the same: what can this work teach us about portable identity, creator demand, safer signing, relays, media, payments or real-world community infrastructure?",
    ]
    return PEOPLE_DEEP_READS.get(person["slug"], fallback)


def make_people_pages():
    cards = [(person["name"], f'{person["role"]}. {person["summary"]}', f'/nostr/{person["slug"]}/') for person in PEOPLE]
    people_sources = [
        ("OpenSats Nostr Fund", "https://opensats.org/funds/nostr", "Funding map for Nostr clients, relays, libraries and developers."),
        ("OpenSats Nostr topic", "https://opensats.org/topics/nostr", "Nostr-related grant and LTS announcements."),
        ("GitHub topic: Nostr", "https://github.com/topics/nostr", "Public repositories and contributors in the Nostr ecosystem."),
        ("Nostr Apps", "https://www.nostrapps.com/", "App and tooling discovery directory."),
        ("Awesome Nostr", "https://github.com/aljazceru/awesome-nostr", "Community-maintained Nostr resource list."),
    ]
    result = [
        page(
            "people",
            "Nostr People, Founders and Builders",
            "Our archive of public Nostr people and founders relevant to our work: the founder voice behind Crays, original protocol authors, major client developers, relay and library builders, signer developers, funders, app founders and cultural contributors.",
            "Nostr is not a company chart. It is a loose network of protocol authors, client builders, relay operators, designers, funders, educators, media builders and users. This page gives the most important public names a clear place in the archive, including the Crays founder voice that explains why this matters to us.",
            [
                section("How this people archive works", [
                    "Each profile is based on public work. It focuses on a person's visible role in the Nostr ecosystem, the projects they are known for and why their work matters to us. It does not invent personal biography and it does not rank people as heroes.",
                    "The first version covers the Crays founder prologue, the most visible protocol builders, major client developers, signer and library builders, infrastructure contributors and public supporters. It is intentionally expandable."
                ], [
                    ("Our founder voice", "Enoch Root explains the lived mission behind our work with Bitcoin, Nostr, privacy and global community."),
                    ("Protocol origin", "fiatjaf and the early Nostr repository."),
                    ("Client builders", "Damus, Amethyst, Coracle, Iris, Nos, Primal, Gossip, noStrudel and related projects."),
                    ("Infrastructure", "rust-nostr, NDK, signers, relays, Blossom, Satellite and developer tooling."),
                    ("Funding and culture", "OpenSats, Jack Dorsey, event organizers and creator communities."),
                ]),
                section("People index", [
                    "Use these profiles as an orientation layer. The Nostr universe is large and changes quickly, so the right editorial model is a living archive with careful updates."
                ], cards=cards),
            ],
            sources=people_sources,
            related=["people/enoch-root", "jack-dorsey", "lifestyle-culture", "developer-tools", "clients", "resources"],
            keywords=["Nostr people", "Nostr founder", "Crays founder", "Enoch Root", "Nostr developers", "Nostr builders"],
            read="20 min read",
        )
    ]
    for person in PEOPLE:
        person_related = ["people", "developer-tools", "clients", "resources", "nostr-and-crays"]
        if person["slug"] != "people/enoch-root":
            person_related.insert(1, "people/enoch-root")
        profile_title = person.get("title", person["name"])
        aliases = person.get("aliases", [])
        result.append(
            page(
                person["slug"],
                profile_title,
                f"{person['name']} in the Nostr ecosystem: {person['role']}. This archive profile summarizes public work, projects and relevance to Nostr and us.",
                person["summary"],
                [
                    section("Public role in Nostr", [
                        f"{person['name']} is included here because of a visible public role in the Nostr universe: {person['role']}. The profile is intentionally focused on ecosystem work rather than private biography."
                    ], person["known_for"]),
                    section("The human read", person_deep_read(person)),
                    section("Why this matters for the Nostr archive", [
                        "Nostr is easier to understand when the protocol is connected to real builders and products. The ecosystem is not one company. It is a mesh of people building clients, relays, libraries, signers, wallets, media tools, community infrastructure and funding channels."
                    ]),
                    section("Crays relevance", [
                        person["crays"]
                    ]),
                    section("How to keep this profile accurate", [
                        "Future edits should update roles, projects and dates from project pages, public repositories or funding announcements instead of copying random reposts."
                    ]),
                ],
                tag="Nostr people archive",
                sources=person["sources"],
                related=person_related,
                keywords=[person["name"], *aliases, person["role"], "Nostr people", "Crays Nostr archive"],
                read="12 min read",
            )
        )
    return result


PAGES.extend(make_people_pages())


APP_PROFILES = [
    ("crays", "Crays", "Crays.net Nostr client and ecosystem front door", "Crays.net is the Crays-facing Nostr surface: profile, creator access, status, venues, awards, payments and portable identity in one lifestyle layer.", [("Crays.net", "https://www.crays.net", "Crays Nostr client and ecosystem profile surface."), ("Crays Nostr", "https://www.crays.org/nostr/nostr-and-crays/", "Crays implementation context."), ("Crays.net as a Nostr client", "https://www.crays.org/nostr/deep-dives/crays-net-as-nostr-client/", "Product-layer explanation.")]),
    ("damus", "Damus", "iOS Nostr client", "Damus made Nostr visible for many iOS users by turning keys, relays, notes and zaps into a mobile social experience.", [("Damus", "https://damus.io/", "Damus website."), ("Damus repository", "https://github.com/damus-io/damus", "Open-source iOS client repository."), ("Nostr.org clients", "https://nostr.org/", "Nostr.org app directory references.")]),
    ("amethyst", "Amethyst", "Android Nostr client", "Amethyst is one of the most complete Android Nostr clients and a major place where newer Nostr features are exposed to mobile users.", [("Amethyst", "https://www.amethyst.social/", "Amethyst project site."), ("Amethyst repository", "https://github.com/vitorpamplona/amethyst", "Open-source Android client repository."), ("OpenSats Amethyst", "https://opensats.org/projects/amethyst", "Project overview.")]),
    ("primal", "Primal", "Nostr social client and discovery stack", "Primal is a polished Nostr consumer experience with mobile and web apps, feed/discovery work and user-facing onboarding.", [("Primal downloads", "https://primal.net/downloads", "Primal app downloads."), ("Primal launch", "https://www.prnewswire.com/news-releases/primal-launches-new-social-network-for-digital-freedom-301877265.html", "Public launch announcement."), ("Nostr.org clients", "https://nostr.org/", "Client directory references.")]),
    ("coracle", "Coracle", "Web Nostr client and community tool", "Coracle focuses on relay choice, communities, Web-of-Trust, recommendations and a web-based Nostr experience.", [("Coracle", "https://coracle.social/", "Coracle web client."), ("Coracle repository", "https://github.com/coracle-social/coracle", "Open-source repository."), ("OpenSats Hodlbod", "https://opensats.org/blog/hodlbod-receives-lts-grant", "Context for Coracle development.")]),
    ("iris", "Iris", "Nostr social client", "Iris is a Nostr client for social networking across mobile and web surfaces, associated with Martti Malmi and the Iris project family.", [("Iris web", "https://iris.to/", "Iris web client."), ("Iris FAQ", "https://github.com/irislib/faq", "Iris documentation."), ("Iris GitHub", "https://github.com/irislib", "Iris repositories.")]),
    ("nostur", "Nostur", "iOS and Mac Nostr client", "Nostur is an Apple-platform Nostr client for users who want a native client experience across iPhone, iPad and Mac.", [("Nostur", "https://www.nostur.com/", "Nostur project site."), ("Nostur public repository", "https://github.com/nostur-com/nostur-ios-public", "Public repository."), ("Nostr.org clients", "https://nostr.org/", "Client directory references.")]),
    ("nostrudel", "noStrudel", "Power-user Nostr web client", "noStrudel is a fast web client and protocol exploration surface for users and developers who want deeper visibility into Nostr.", [("noStrudel", "https://nostrudel.ninja/", "noStrudel web client."), ("noStrudel repository", "https://github.com/hzrd149/nostrudel", "Open-source repository."), ("OpenSats hzrd149", "https://opensats.org/blog/hzrd149-receives-lts-grant", "Development context.")]),
    ("yakihonne", "YakiHonne", "Nostr publishing and social client", "YakiHonne combines social posting, content management and built-in Bitcoin support across web and mobile surfaces.", [("YakiHonne", "https://yakihonne.com/", "YakiHonne website."), ("Nostr Apps YakiHonne", "https://nostrapps.com/yakihonne", "Nostr Apps listing."), ("Nostr Apps", "https://www.nostrapps.com/", "App directory.")]),
    ("habla", "Habla", "Long-form Nostr publishing client", "Habla shows how Nostr can support article-like writing and publishing beyond short social notes.", [("Habla on Nostr Apps", "https://nostrapps.com/habla", "Habla app listing."), ("Habla repository", "https://github.com/verbiricha/habla.news", "Open-source repository."), ("NIP-23", "https://github.com/nostr-protocol/nips/blob/master/23.md", "Long-form content standard.")]),
    ("snort", "Snort", "Web Nostr client", "Snort is a web client that helped popularize browser-based Nostr usage and remains part of the wider client ecosystem.", [("Snort", "https://snort.social/", "Snort web client."), ("Nostr.org clients", "https://nostr.org/", "Client directory references."), ("Nostr Apps", "https://www.nostrapps.com/", "App directory.")]),
    ("gossip", "Gossip", "Privacy-oriented Nostr client", "Gossip is a Rust Nostr client associated with privacy, security and outbox-model thinking.", [("Gossip repository", "https://github.com/mikedilger/gossip", "Open-source client repository."), ("OpenSats Mike Dilger", "https://opensats.org/blog/mike-dilger-receives-lts-grant", "Development context."), ("Nostr Apps", "https://www.nostrapps.com/", "App directory.")]),
    ("nos", "Nos", "Nostr social app", "Nos is an ad-free social app built on Nostr that emphasizes user control and social media without a single controlling platform.", [("Nos", "https://www.nos.social/", "Nos homepage."), ("Nos about", "https://www.nos.social/about", "Nos product background."), ("Nos repository", "https://github.com/planetary-social/nos", "Open-source repository.")]),
    ("amber", "Amber", "Android Nostr signer", "Amber is an Android Nostr signer that helps users keep their private key out of ordinary apps while still authorizing signatures.", [("Amber project", "https://opensats.org/projects/amber", "OpenSats project overview."), ("Nostr Apps Amber", "https://nostrapps.com/amber", "Nostr Apps listing."), ("OpenSats Greenart7c3", "https://opensats.org/blog/greenart7c3-receives-lts-grant", "Development context.")]),
    ("alby", "Alby", "Lightning wallet and browser signer", "Alby is widely used in Nostr onboarding because it combines browser-based signing and Lightning wallet functionality.", [("Alby", "https://getalby.com/", "Alby website."), ("nostr.how onboarding", "https://nostr.how/en/get-started", "Nostr onboarding guide referencing signer and wallet flows."), ("Nostr Login", "https://www.nostrlogin.org/", "Signer and login context.")]),
    ("safebox", "Safebox", "Nostr-native Cashu wallet, records and secure transmittal experiment", "Safebox combines Cashu ecash, Nostr messaging, encrypted records, Blossom blob transfer, NWC extension work, NFC/vault flows and optional ML-KEM payload protection into one experimental sovereign wallet and records stack.", SAFEBOX_SOURCES),
    ("foundups-agent", "FoundUPS Agent", "Compute-focus agent orchestration stack", "FoundUPS Agent is not a Nostr client. It is an adjacent autonomous-agent and compute-allocation project that matters for our archive because Nostr, Bitcoin, DAO governance and agent coordination will increasingly touch the same product questions.", FOUNDUPS_SOURCES),
    ("wavlake", "Wavlake", "Music and value-for-value app", "Wavlake shows how Nostr-adjacent culture can connect creators, listeners and direct value flows around music.", [("Wavlake", "https://wavlake.com/", "Wavlake website."), ("Nostr Apps", "https://www.nostrapps.com/", "App directory."), ("NIP-57", "https://github.com/nostr-protocol/nips/blob/master/57.md", "Lightning zaps standard.")]),
    ("nostr-band", "Nostr.band", "Search and discovery service", "Nostr.band is a search and discovery service that helps users find profiles, notes, hashtags and ecosystem activity.", [("Nostr.band GitHub", "https://github.com/nostrband", "Public Nostr.band organization and related tools."), ("NIP-50", "https://github.com/nostr-protocol/nips/blob/master/50.md", "Search capability standard."), ("Nostr Apps", "https://www.nostrapps.com/", "App directory.")]),
    ("satellite-earth", "Satellite Earth", "Community client and infrastructure stack", "Satellite Earth combines client and infrastructure ideas for self-sovereign communities and local control.", [("Satellite Earth", "https://satellite.earth/", "Satellite site."), ("OpenSats Stuart Bowman", "https://opensats.org/blog/stuart-bowman-receives-lts-grant", "Development context."), ("GitHub lovvtide", "https://github.com/lovvtide", "Public GitHub profile.")]),
    ("ditto", "Ditto", "Self-hosted Nostr social server", "Ditto explores a self-hosted social server with built-in Nostr client and relay compatibility, bridging Nostr with fediverse thinking.", [("OpenSats Alex Gleason", "https://opensats.org/blog/alex-gleason-receives-lts-grant", "Development context and Ditto overview."), ("GitHub: Alex Gleason", "https://github.com/alexgleason", "Public GitHub profile."), ("Soapbox GitHub", "https://github.com/soapbox-pub", "Soapbox public organization.")]),
    ("ndk", "Nostr Development Kit", "Nostr developer toolkit", "NDK is a major developer toolkit for building Nostr apps with outbox-model support and application-level abstractions.", [("NDK repository", "https://github.com/nostr-dev-kit/ndk", "Nostr Development Kit repository."), ("OpenSats PabloF7z", "https://opensats.org/blog/pablofz7-receives-lts-grant", "Development context."), ("Nostr NIPs", "https://github.com/nostr-protocol/nips", "Protocol references.")]),
    ("rust-nostr", "rust-nostr", "Rust Nostr implementation", "rust-nostr is a Rust implementation of the Nostr protocol with client libraries, Nostr Wallet Connect and related tooling.", [("rust-nostr", "https://github.com/rust-nostr/nostr", "Rust implementation repository."), ("OpenSats Yuki", "https://opensats.org/blog/yuki-receives-lts-grant", "Development context."), ("Nostr NIPs", "https://github.com/nostr-protocol/nips", "Protocol references.")]),
]


def make_app_profile_pages():
    cards = [(name, f"{role}. {summary}", f"/nostr/apps/{slug}/") for slug, name, role, summary, sources in APP_PROFILES]
    result = [
        page(
            "app-profiles",
            "Nostr App and Tool Profiles",
            "A Crays archive of major Nostr apps, clients, signers, discovery services, media tools and developer libraries.",
            "Nostr becomes understandable when the protocol is connected to actual products. This index maps the clients and tools that readers will encounter in the Nostr universe.",
            [
                section("How to use this app archive", [
                    "This is not a ranking and not an endorsement list. It is a structured map. Some projects are consumer clients, some are developer tools, some are media apps and some are signer or infrastructure products.",
                    "The main lesson for Crays is that the same protocol can support very different surfaces. Crays.net should therefore be a focused Crays-facing client, not a generic clone of existing apps."
                ], cards=cards),
            ],
            sources=[GLOBAL_SOURCES[5], GLOBAL_SOURCES[6], GLOBAL_SOURCES[4], ("GitHub topic: Nostr", "https://github.com/topics/nostr", "Public Nostr repositories.")],
            related=["apps", "clients", "developer-tools", "people", "resources"],
            keywords=["Nostr apps", "Nostr clients", "Nostr tools", "Nostr app profiles"],
            read="18 min read",
        )
    ]
    for slug, name, role, summary, sources in APP_PROFILES:
        result.append(
            page(
                f"apps/{slug}",
                name,
                f"{name} in the Nostr ecosystem: {role}. This Crays archive page explains the public role, where it fits and why it matters.",
                summary,
                [
                    section("What it is", [
                        f"{name} is included because it represents an important category in the Nostr ecosystem: {role}. Some readers will meet Nostr first through this kind of product, not through the protocol documents."
                    ], [
                        ("Category", role),
                        ("Protocol fit", "It uses Nostr identity, events, relays, signers, zaps, media references or developer abstractions depending on the product."),
                        ("Reader value", "It helps explain how Nostr moves from an abstract protocol into usable interfaces."),
                    ]),
                    section("Why it matters", [
                        f"{summary} The product also shows that Nostr can support specialized interfaces rather than one universal app."
                    ]),
                    section("Crays relevance", [
                        "Crays should learn from this product category without copying it blindly. The Crays surface needs profiles, paid content, status, fans, venues, award voting, Lightning flows and real-world hospitality context."
                    ]),
                ],
                tag="Nostr app archive",
                sources=sources,
                related=["app-profiles", "apps", "clients", "developer-tools", "nostr-and-crays"],
                keywords=[name, role, "Nostr app", "Crays Nostr archive"],
                read="6 min read",
            )
        )
    return result


for item in PAGES:
    if item["slug"] == "apps":
        item["sections"].append(
            section("App profile index", [
                "The app archive breaks major clients and tools into their own pages so readers can move from broad categories into concrete examples."
            ], cards=[(name, f"{role}. {summary}", f"/nostr/apps/{slug}/") for slug, name, role, summary, sources in APP_PROFILES])
        )
        item["related"] = ["app-profiles", "clients", "developer-tools", "people", "resources"]


PAGES.extend(make_app_profile_pages())


def make_project_research_pages():
    return [
        page(
            "deep-dives/blossom-servers-and-relays",
            "Blossom Servers, Relays and Nostr Media Storage",
            "What Blossom servers are, why they are not relays, and how clients use them with Nostr events, relay discovery, hashes, server lists, mirrors and file metadata.",
            "Blossom is the missing media-storage chapter many Nostr explanations skip. It is not a social relay and it is not a new feed. A Blossom server is an HTTP blob server for file bytes, while relays remain the place where signed Nostr events are published, discovered and indexed.",
            [
                section("The short answer", [
                    "Blossom means blobs stored simply on media servers. In normal language: a Blossom server stores binary files - images, videos, PDFs, audio, encrypted archives, thumbnails or other file bytes - and makes them available through HTTP URLs.",
                    "The core rule is content addressing. A blob is identified by the sha256 hash of the exact bytes. That hash is the stable handle. The URL is just one place where those bytes can be fetched. If the same file is mirrored to another server, the hash should still point to the same content.",
                    "That is why Blossom matters for Nostr. Nostr relays are good at signed events, subscriptions, author identity, conversations, timestamps and discovery. They are not the right place for heavy media bytes. Blossom moves the bytes out to file servers while the Nostr event keeps the social and cryptographic context."
                ], [
                    ("Relay", "Stores and serves signed Nostr events over WebSockets."),
                    ("Blossom server", "Stores and serves file bytes over HTTP."),
                    ("Nostr event", "Says who published, what file is referenced and how to verify or find it."),
                    ("sha256 hash", "Lets clients verify that fetched bytes match the expected file."),
                ]),
                section("How one upload works", [
                    "A client starts with a file. Before upload it can compute the sha256 hash locally. It then chooses a Blossom server, often from the user's BUD-03 server list or from app defaults. If the server requires authorization, the client asks the user's signer for a short-lived Nostr authorization event that scopes the action.",
                    "The upload itself is HTTP, not a relay write. BUD-02 defines `PUT /upload`, where the request body is the binary data. A successful server response returns a blob descriptor: public URL, sha256 hash, size, MIME type and upload timestamp. If the server already has the blob, it can return the existing descriptor instead of storing duplicates.",
                    "Only after that does the client publish to Nostr relays. The Nostr event can be a normal note, a long-form article, a profile event, a marketplace event, a NIP-94 file metadata event or another app-specific event. That event carries or references the URL, hash, MIME type, dimensions, alt text, fallback sources or imeta-style tags, depending on the client and standard used."
                ], [
                    ("1. Prepare", "Client reads the file and computes its hash."),
                    ("2. Authorize", "Signer creates a scoped Blossom auth event when the server requires it."),
                    ("3. Upload", "Client sends the bytes to a Blossom HTTP endpoint."),
                    ("4. Describe", "Server returns the URL, hash, size, type and timestamp."),
                    ("5. Publish", "Client posts a signed Nostr event to relays with the file reference."),
                    ("6. Fetch", "Other clients read the event from relays and fetch the bytes from Blossom."),
                ]),
                section("Where relays fit", [
                    "Relays still do the Nostr work. They receive signed events, apply relay policy, answer subscriptions and help other clients discover that a file exists. A relay can index the tags, author, event kind, created_at time and conversation context around a file reference.",
                    "The relay does not need to download or host the image. It can simply store the event that says, in effect: this pubkey signed this post, this file URL or hash is attached, here are the tags and here is the signature. The media bytes live elsewhere.",
                    "This separation makes the network more realistic. Relay operators can manage event spam, paid relay access, local graph behavior and archive policy. Blossom operators can manage storage quota, bandwidth, file moderation, malware scanning, media optimization, deletion policy, payments and mirroring."
                ], [
                    ("Relays answer", "Who signed this? Where is the event? Which tags and replies connect to it?"),
                    ("Blossom answers", "Where are the bytes? What hash do they have? Can this user upload, delete or mirror them?"),
                    ("Clients combine", "Read events from relays, then fetch media through HTTP and verify what they can."),
                ]),
                section("User server lists", [
                    "BUD-03 defines a replaceable Nostr event, kind `10063`, where a user can advertise the Blossom servers they trust or use. The event contains `server` tags with full server URLs. The order matters because clients should treat the first servers as the most reliable or trusted.",
                    "This is the media-storage cousin of relay lists. A relay list helps clients know where to read or write events for a user. A Blossom server list helps clients know where that user's blobs may live, where uploads should go and where missing files can be recovered.",
                    "The powerful part is recovery. If a post contains an old URL and that URL no longer works, a client can extract the 64-character hash from the URL, fetch the author's kind `10063` server list from relays, then try each Blossom server for the same hash. If a mirror exists, the file can still load even when the original domain is gone."
                ], [
                    ("Kind 10063", "A replaceable Nostr event that advertises a user's Blossom servers."),
                    ("Server tags", "Each tag points at a Blossom server URL."),
                    ("Ordered trust", "Clients should try preferred servers first."),
                    ("Recovery", "The same hash can be found on mirrors when one URL disappears."),
                ]),
                section("NIP-94 and NIP-96", [
                    "NIP-94 and Blossom solve different parts of the same problem. NIP-94 defines a file metadata event, kind `1063`, with tags such as URL, MIME type, sha256 hash, original hash, size, dimensions, thumbnail, preview, alt text and fallback sources. It is an event format relays can store.",
                    "Blossom is the storage and serving side. It gives clients a way to put bytes on HTTP media servers, retrieve them by hash and advertise server preferences. A client can use Blossom to store a file and NIP-94 to publish rich metadata about it through relays.",
                    "NIP-96 is adjacent: it defines an HTTP file storage API intended for use with Nostr clients, including discovery through `/.well-known/nostr/nip96.json`. The useful way to explain it in our archive is: NIP-96 and Blossom both keep files out of relays, but Blossom puts stronger emphasis on hash-addressed blobs, BUD documents, user server lists and Nostr authorization."
                ], [
                    ("NIP-94", "Metadata event for describing files inside the Nostr event graph."),
                    ("Blossom", "HTTP blob storage and retrieval by content hash."),
                    ("NIP-96", "Another Nostr-oriented HTTP file-storage API."),
                    ("route96", "A real implementation reference that touches Blossom and NIP-96 territory."),
                ]),
                section("Authorization and security", [
                    "A public Blossom URL is not privacy. If the URL or hash is known, clients should assume the blob can be fetched unless the server adds access controls. For private records, private media, member documents or wallet-adjacent material, the right pattern is to encrypt before upload and only publish safe metadata.",
                    "BUD-11 defines Nostr authorization tokens. These are signed events of kind `24242` that prove a pubkey allowed an action such as upload, list, delete or media handling. They can include expiration, action tags, server scope and hash scope. This keeps a web app from asking for the user's raw private key while still letting a server verify intent.",
                    "Hash verification protects integrity, not secrecy. If the expected sha256 hash is in the event, a client can check that downloaded bytes match the referenced file. That does not stop metadata leaks, EXIF leaks, public URL sharing or server-side moderation. Serious deployments still need file scanning, quotas, takedown process, retention rules and careful UX."
                ], [
                    ("Encrypt first", "Private blobs should be encrypted before upload."),
                    ("Verify hash", "Clients can compare downloaded bytes against the expected sha256."),
                    ("Limit auth", "Authorization should be short-lived and scoped to the exact action."),
                    ("Strip metadata", "Images and documents can leak EXIF or author data."),
                    ("Mirror wisely", "More availability can also mean wider exposure if the blob is public."),
                ]),
                section("How this fits our infrastructure", [
                    "For our stack, the clean mental model is simple: a venue or Super Node can run a relay and a Blossom server side by side, but they are separate responsibilities. The relay handles signed member, creator, venue, event, payment, governance and reputation signals. The Blossom server handles media bytes, encrypted originals and large file transfer.",
                    "That split is useful for hospitality and creators. Profile images, venue photos, event galleries, creator media, paid content previews, encrypted Safebox records, receipts, award assets and local community files should not bloat relays. They should be referenced by Nostr events and fetched from storage that can be operated, mirrored and paid for deliberately.",
                    "A practical Crays node could therefore include a relay, a Blossom server, a signer-friendly auth flow, an indexer, a wallet/payment path and operator tools. Users would not need to know every layer. They should feel one experience: publish, prove, access, pay, recover and move."
                ], [
                    ("Super Node relay", "Event routing, local graph, paid relay policy and signed history."),
                    ("Blossom server", "Media storage, encrypted blob transfer, quotas and mirroring."),
                    ("Signer", "Scoped authorization without exposing private keys to the web app."),
                    ("Indexer", "Search and discovery over event metadata, not raw file hosting."),
                    ("Wallet", "Paid storage, creator access, zaps or member entitlements."),
                ]),
                section("What to remember", [
                    "If a reader remembers only one sentence, make it this: relays move and index the signed story; Blossom servers store and serve the heavy bytes. They are complementary infrastructure, not replacements for each other.",
                    "That distinction also keeps product language honest. A bad media experience is often not a Nostr failure in the abstract. It can be a storage server, mirror, URL, hash, metadata, relay discovery or client fallback problem. Once we name the layers, we can fix the right layer."
                ], [
                    ("Do not store big files in relays", "Use relays for signed events and discovery."),
                    ("Do not trust URLs blindly", "Use hashes and fallback sources when possible."),
                    ("Do not call Blossom a relay", "It is HTTP blob storage for the Nostr ecosystem."),
                    ("Do design for recovery", "Server lists and mirrors make media less brittle."),
                ]),
            ],
            tag="Nostr storage deep dive",
            sources=BLOSSOM_SOURCES,
            related=[
                "deep-dives/media-attachments-and-blossom",
                "field-guide/blossom-storage",
                "apps/developer-stack/blossom",
                "apps/developer-stack/blossom-spec-nip-b7",
                "nip-94-files",
                "nip-96-file-storage",
                "nip-98-http-auth",
                "relays",
                "crays-super-node",
                "deep-dives/safebox-sovereign-wallet-records",
            ],
            keywords=[
                "Blossom servers",
                "Nostr media storage",
                "Blossom relays",
                "BUD-03",
                "NIP-94",
                "NIP-96",
                "Nostr file storage",
                "Crays Super Node media",
            ],
            read="20 min read",
        ),
        page(
            "deep-dives/safebox-sovereign-wallet-records",
            "Safebox: Nostr-Native Wallet and Records Stack",
            "A detailed Crays archive read on Safebox: Cashu ecash, Nostr transmittal, encrypted records, Blossom blobs, NWC, NFC/vault flows and post-quantum payload experiments.",
            "Safebox is one of the more interesting edge projects in the Nostr orbit because it does not treat Nostr as just a feed. It treats Nostr as a secure transmittal layer for wallet state, private records, offers, presentations and service-to-service coordination.",
            [
                section("The clean read", [
                    "Safebox is experimental software. That matters. We should not present it as production-ready infrastructure or pretend every flow is mature. But the shape is important: it brings Cashu, Lightning, Nostr events, encrypted records, Blossom storage, Nostr Wallet Connect style service calls, NFC-assisted flows and optional ML-KEM payload protection into one product thesis.",
                    "The practical idea is simple enough for a normal reader: your wallet and your records should not be trapped inside a single custodial app. You should be able to hold value, prove or present selected records, move encrypted blobs and route sensitive messages through protocol-native rails without handing every secret to a platform."
                ], [
                    ("Wallet layer", "Lightning invoices, Lightning addresses, Cashu tokens, multi-mint proof handling and consolidation."),
                    ("Record layer", "Private records, blob-backed records and offer-present-accept flows."),
                    ("Nostr layer", "Encrypted event transport, npub-addressed delivery and secure transmittal."),
                    ("Blob layer", "Blossom-style storage and transfer for encrypted originals."),
                    ("Field layer", "NFC cards, PIN-gated record presentation and vault endpoints."),
                ]),
                section("Why it belongs in the Nostr archive", [
                    "Most beginner Nostr pages stop at notes, relays and zaps. Safebox points at a heavier use case: records and wallet state that need identity, routing, encryption, permissions, storage and recovery discipline. That is much closer to what real venues, operators, creators and members eventually need.",
                    "The project also forces a useful distinction. Nostr can move signed or encrypted events. It does not automatically solve custody, legal exposure, record semantics, device loss, operator duties or auditability. Safebox is interesting precisely because it puts those product problems on the table instead of hiding them behind protocol romance."
                ], [
                    ("Not a feed", "It uses Nostr beyond public social posting."),
                    ("Not just a wallet", "The records flow makes identity and proof part of the product."),
                    ("Not magic security", "The repo itself warns that deployments are security-sensitive and experimental."),
                ]),
                section("How the architecture reads", [
                    "The public README describes a Python/FastAPI app with Jinja templates, an Acorn wallet engine, an NWC extension service, SQLModel storage, default SQLite, Nostr event storage for encrypted wallet and record data, plus optional Blossom APIs for blobs. That is not a tiny demo. It is a layered application with several places where product decisions matter.",
                    "The docs directory is where the serious signal lives. There are specs for Cashu storage and multi-mint behavior, Blossom blob transfer, portable record formats, record presentation, transport versus payload security, threat modeling, web wallet considerations, NFC payment strategy and hardening. The useful archive move is to make those pieces readable without copying the raw specs."
                ], [
                    ("FastAPI app", "The user-facing API/UI layer."),
                    ("Acorn", "The wallet engine and protocol primitive layer."),
                    ("NWC extension", "A service path for wallet instructions and vault-mediated flows."),
                    ("Nostr storage", "Encrypted event-backed wallet and record state."),
                    ("Blossom", "Blob storage for larger encrypted objects."),
                ]),
                section("The record model is the real lesson", [
                    "Cashu and Lightning make the project easy to label as a wallet. The more strategic part is records. If a person can offer, present or accept a record through protocol-native flows, then Nostr starts to look like a civic and commercial layer, not only a social layer.",
                    "For us, that connects directly to member status, venue access, creator entitlements, award participation, hospitality credentials, proof of purchase, local service permissions and future governance roles. A Crays venue does not only need a profile. It needs a way to know what a person can access right now, what they can prove, and what should stay private."
                ], [
                    ("Offer", "A record can be offered without making the entire file public."),
                    ("Present", "A person can present selected proof or encrypted material to a receiving party."),
                    ("Accept", "The receiver can accept and store the relevant record flow."),
                    ("Transfer", "Original encrypted blobs can move when the workflow requires more than a note."),
                ]),
                section("Security and maturity", [
                    "The honest version is this: Safebox is fascinating because it is ambitious, not because it removes risk. Wallets, private records, encrypted blobs, NFC, vault signing and quantum-safe payload experiments all expand the security surface. That calls for threat modeling, staged deployments, audit trails, careful operator defaults and very plain user language.",
                    "For our archive, Safebox should sit near Nostr Wallet Connect, Cashu, Blossom, NIP-44, relays, private-key custody and web-of-trust pages. Readers should leave with a clearer sense of what the architecture enables and what still needs review before anything touches real money or sensitive records."
                ], [
                    ("Experimental status", "Treat deployments as test/staged until audited for the intended environment."),
                    ("Secret handling", "Service keys, NWC keys, PQC keys and wallet state are critical credentials."),
                    ("Payload security", "Transport security is not the same as payload-level encryption."),
                    ("Operator duty", "Vault-facing endpoints need hardening before public exposure."),
                ]),
                section("Crays product reading", [
                    "For us, Safebox is a research signal for three product lines: member-held value, member-held records and venue-facing trust. The project is not something to copy blindly. It is a map of hard questions we should answer before profile, content, access, payments and venue service flows become one experience.",
                    "The best Crays version would keep the same user promise but make the interface calmer: no protocol fog, no scary key ceremony unless needed, no hidden custody assumptions, and no fake certainty. A person should know what they hold, what they share, what remains private and what happens if a device disappears."
                ]),
            ],
            tag="Nostr project research",
            sources=SAFEBOX_SOURCES + [
                ("Cashu", "https://cashu.space/", "Cashu ecash context for the wallet layer."),
                ("Blossom specification", "https://github.com/hzrd149/blossom", "Blossom media/blob storage context."),
                ("NIP-47", "https://github.com/nostr-protocol/nips/blob/master/47.md", "Nostr Wallet Connect reference."),
            ],
            related=["apps/safebox", "nip-47-wallet-connect", "nip-44-encryption", "deep-dives/media-attachments-and-blossom", "deep-dives/nostr-security-threat-model", "crays-super-node"],
            keywords=["Safebox", "Nostr Safebox", "Cashu", "Blossom", "Nostr records", "Nostr Wallet Connect", "Crays Nostr archive"],
            read="18 min read",
        ),
        page(
            "deep-dives/foundups-agent-compute-focus-network",
            "FoundUPS Agent and the Compute-Focus Network",
            "A careful Crays archive read on FoundUPS Agent: compute allocation, autonomous agents, WSP/WRE orchestration, digital-twin direction, Bitcoin treasury framing and DAO-adjacent governance questions.",
            "FoundUPS is not a Nostr client and we should not force it into the protocol shelf. Its value for this archive is adjacent: it asks what happens when human intent, AI agents, compute allocation, venture creation, Bitcoin economics and governance rails become one operating model.",
            [
                section("The clean read", [
                    "FoundUPS frames itself around a blunt question: where do you want to focus your compute? In the public site and repository, the answer is not a chat app. It is a system for planning, building and supporting autonomous ventures through agent orchestration.",
                    "For our Nostr archive, the important part is the overlap. Nostr gives portable identity and signed social signals. Bitcoin gives value flow and treasury logic. AI agents introduce execution. DAO-style governance introduces coordination. FoundUPS lives in that messy, interesting zone where a signed person, an agent and a venture need to coordinate without becoming a closed SaaS prison."
                ], [
                    ("Plan", "Shape an idea and execution path."),
                    ("Build", "Use agent orchestration to execute work."),
                    ("Support", "Allocate compute or attention to ventures and participate in the result."),
                    ("Remember", "Use project memory and retrieval to keep agents from repeating blind work."),
                ]),
                section("What the repository actually shows", [
                    "The Foundups-Agent README describes WSP/WRE orchestration, HoloIndex retrieval, FAM lifecycle tooling, simulator economics, OpenClaw/0102 agents, multi-agent IDE ideas, social media automation, meeting orchestration, platform integration and Bitcoin-backed treasury framing. Some of the language is intentionally maximal. Our job is to translate the signal without swallowing the whole pitch.",
                    "The grounded reading is this: the project is trying to make an agent stack that can coordinate work across code, meetings, social platforms, documentation, memory, lifecycle stages and economic participation. That is exactly the kind of adjacent infrastructure we should track because Crays also connects digital profiles, creators, venues, payments, reputation and future governance."
                ], [
                    ("WSP/WRE", "A protocol-and-engine framing for agent orchestration and development discipline."),
                    ("HoloIndex", "A retrieval and memory layer so agents query existing patterns before acting."),
                    ("Platform modules", "YouTube, LinkedIn, X and other integrations appear as agent surfaces."),
                    ("Compute focus", "The user points intent; agents and infrastructure route execution."),
                    ("Bitcoin framing", "Treasury and participation logic appear as part of the venture model."),
                ]),
                section("Where this touches Nostr", [
                    "FoundUPS does not need to be a Nostr app to be useful here. The bridge is product architecture. If an agent acts for a person or venture, we need portable identity, permission boundaries, signed actions, social reputation, payments, audit trails and eventually governance. Those are all Nostr-and-Bitcoin-native questions.",
                    "A future FoundUPS-like agent could use Nostr for identity, agent attestations, task posts, status updates, creator-market discovery, wallet permissions, DAO votes, collaboration rooms or public proof of execution. That is not a claim that the current repo already does all of this through Nostr. It is the strategic reason it belongs in our map."
                ], [
                    ("Identity", "Which person or venture is the agent acting for?"),
                    ("Authorization", "What may the agent sign, spend, publish or trigger?"),
                    ("Reputation", "What proves that the agent did useful work?"),
                    ("Payment", "How does compute, contribution or output become value flow?"),
                    ("Governance", "Who changes rules when agents operate inside a community?"),
                ]),
                section("The Crays angle", [
                    "For us, FoundUPS is useful because it names a future we already have to design for: AI-driven hospitality coordination, creator operations, status workflows, venue services, DAO participation and partner-network automation. Once agents touch real venues or real money, they need identity, limits, logs and readable consent.",
                    "The Crays version cannot sound like a science-fiction manifesto. It has to feel like a useful concierge with receipts: here is who asked, here is what the agent may do, here is what it did, here is who approved it, here is the payment or status change, here is the rollback path."
                ], [
                    ("Hospitality", "Agents can coordinate bookings, local service context and member requests."),
                    ("Creators", "Agents can help route campaigns, content drops, fan access and paid moments."),
                    ("Operators", "Agents can assist with venue relays, support, status and partner workflows."),
                    ("DAO", "Agents need governance rails before they can act inside member systems."),
                ]),
                section("What to treat carefully", [
                    "The archive should keep FoundUPS exciting but not breathless. Claims about autonomous venture building, agent consciousness, recursive self-improvement and future-state coding need sober framing. We can explain the concept, track the code and extract the useful architectural questions without repeating every claim as fact.",
                    "That is the editorial rule: turn the hype into product questions. What is the interface? What is the permission model? What is the audit trail? What is the economic loop? What is the governance layer? What happens when the agent is wrong?"
                ], [
                    ("Evidence", "Separate shipped code, public docs, roadmap language and speculation."),
                    ("Consent", "No agent should act on behalf of a user without clear scope."),
                    ("Security", "Platform automation and wallet activity require hard boundaries."),
                    ("Language", "Keep the reader grounded in normal words."),
                ]),
            ],
            tag="Agent economy research",
            sources=FOUNDUPS_SOURCES + [
                ("NIP-90 Data Vending Machines", "https://github.com/nostr-protocol/nips/blob/master/90.md", "Nostr paid job and machine-work reference point."),
                ("NIP-47 Nostr Wallet Connect", "https://github.com/nostr-protocol/nips/blob/master/47.md", "Wallet permission and payment-service context."),
            ],
            related=["apps/foundups-agent", "deep-dives/data-vending-machines", "dao-governance", "deep-dives/crays-dao-readiness", "deep-dives/nostr-for-ai-tools", "nostr-and-bitcoin"],
            keywords=["FoundUPS", "Foundups Agent", "agent economy", "compute allocation", "WSP", "WRE", "Crays DAO", "Nostr agents"],
            read="18 min read",
        ),
        page(
            "deep-dives/foundups-and-nostr-agent-economy",
            "FoundUPS, Nostr and the Agent Economy",
            "How FoundUPS helps us think about agents, Nostr identity, Bitcoin value flow, DAO coordination and Crays hospitality automation without turning the archive into buzzword soup.",
            "The agent economy only becomes useful when it stops being a cloud of big words. This chapter turns FoundUPS into a practical Crays question: what should an agent be allowed to do when it touches profiles, content, venues, payments or governance?",
            [
                section("Why this matters", [
                    "Nostr is good at signed public and semi-private signals. Bitcoin is good at value. Agents are good at execution when their scope is narrow and their feedback is visible. The future we care about is where those three things meet without confusing the reader or losing control.",
                    "FoundUPS gives us a live project to study because it is already trying to connect human intent, agent work, memory, platform integration and economic participation. That makes it useful research material even when its language is more intense than our house style."
                ], [
                    ("Signed intent", "A user or venture can make an action attributable."),
                    ("Scoped execution", "An agent can act only inside clear permission boundaries."),
                    ("Visible output", "Work should leave logs, status and proof."),
                    ("Value flow", "Payments should be explicit, reversible where possible and easy to understand."),
                ]),
                section("A Crays-ready agent model", [
                    "For Crays, the winning version is calm. A creator asks for a launch plan. A venue asks for a member-flow check. A partner asks for a status update. A DAO steward asks for a vote summary. The agent can assist, but identity, payment, access and governance stay inspectable.",
                    "That means Nostr becomes more than a login. It can carry signed requests, public proof, agent labels, task receipts, collaboration notes, trust signals and maybe later machine-readable work offers. The user does not need to see every protocol piece. They need to feel that the system has manners."
                ], [
                    ("Ask", "Who requested the action?"),
                    ("Scope", "What exactly may the agent do?"),
                    ("Act", "What was executed and where?"),
                    ("Prove", "Which signed event, receipt or record shows the result?"),
                    ("Review", "Who can approve, contest or undo the action?"),
                ]),
                section("Where Nostr standards may fit", [
                    "NIP-90 is the obvious reference because it describes paid machine-work style requests and results. NIP-47 matters when agents need wallet-connected payments without custody. NIP-44 matters when payloads need encryption. NIP-51 and web-of-trust patterns matter when agents, people and venues need lists, labels and reputation.",
                    "The point is not to throw every NIP at the problem. The point is to design a thin, readable path: identity first, permissions second, work third, payment fourth, governance last."
                ]),
                section("Editorial rule for this archive", [
                    "Whenever we cover agent projects, we should write like adults in the room. We can be excited, but we do not repeat mystical language as product fact. We translate: here is the actual repo, here are the modules, here is the stated roadmap, here is the useful idea, here is the risk.",
                    "That rule protects the reader and it protects the Crays brand. Lifestyle does not mean sloppy. Cool does not mean vague. The best version feels like a smart person at the table explaining what matters without killing the energy."
                ]),
            ],
            tag="Agent economy research",
            sources=FOUNDUPS_SOURCES + NIP_SOURCES,
            related=["deep-dives/foundups-agent-compute-focus-network", "deep-dives/data-vending-machines", "deep-dives/nostr-for-ai-tools", "nip-47-wallet-connect", "nip-44-encryption", "dao-governance"],
            keywords=["FoundUPS Nostr", "Nostr agent economy", "AI agents Nostr", "Crays AI hospitality", "DAO agents"],
            read="13 min read",
        ),
    ]


PAGES.extend(make_project_research_pages())

LONGFORM_EDITORIAL_SKIP_SLUGS = {
    "deep-dives/blossom-servers-and-relays",
}

SOURCE_SECTION_SLUGS = {
    "deep-dives/blossom-servers-and-relays",
    "resources",
    "nostr-media-article-video-archive",
}

try:
    from nostr_archive_expansion import make_expansion_pages

    PAGES.extend(make_expansion_pages(page, section, GLOBAL_SOURCES, NIP_SOURCES))
except Exception as exc:
    print(f"Skipping Nostr archive expansion: {exc}")

try:
    from nostr_longform_editorial import (
        apply_longform_editorial_pass,
        make_longform_pages,
        make_repeated_paragraphs_page_specific,
    )

    PAGES.extend(make_longform_pages(page, section))
    longform_targets = [item for item in PAGES if item.get("slug") not in LONGFORM_EDITORIAL_SKIP_SLUGS]
    apply_longform_editorial_pass(longform_targets, section)
    make_repeated_paragraphs_page_specific(longform_targets)
except Exception as exc:
    print(f"Skipping Nostr longform editorial expansion: {exc}")

try:
    from nostr_deep_research_import import make_deep_research_pages

    PAGES.extend(make_deep_research_pages(page, section))
except Exception as exc:
    print(f"Skipping Nostr deep research import: {exc}")


try:
    from nostr_start_editorial import apply_start_page_rewrites

    apply_start_page_rewrites(
        PAGES,
        section,
        GLOBAL_SOURCES,
        NIP_SOURCES,
        RESOURCE_LINKS,
        RELAY_MARKET_SOURCES,
        BLOSSOM_SOURCES,
    )
except Exception as exc:
    print(f"Skipping Nostr start editorial rewrites: {exc}")


def domain_from_url(url: str) -> str:
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
    except Exception:
        return ""
    host = (parsed.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def favicon_url(domain: str, size: int = 128) -> str:
    domain = domain_from_url(domain)
    if not domain:
        return ""
    return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"


APP_ICON_DOMAIN_OVERRIDES = {
    "0xchat": "0xchat.com",
    "alby": "getalby.com",
    "amber": "github.com/greenart7c3/amber",
    "amethyst": "amethyst.social",
    "coracle": "coracle.social",
    "damus": "damus.io",
    "foundups-agent": "foundups.com",
    "gossip": "github.com/mikedilger/gossip",
    "iris": "iris.to",
    "nostrudel": "nostrudel.ninja",
    "nostur": "nostur.com",
    "nos-social": "nos.social",
    "primal": "primal.net",
    "primal-web": "primal.net",
    "safebox": "github.com/trbouma/safebox",
    "yakihonne": "yakihonne.com",
    "wavlake": "wavlake.com",
    "zap-stream": "zap.stream",
    "zapstore": "zapstore.dev",
}


SKIP_ICON_DOMAINS = {
    "apps.apple.com",
    "play.google.com",
    "chromewebstore.google.com",
}


def build_app_icon_maps() -> tuple[dict[str, str], dict[str, str]]:
    by_slug: dict[str, str] = {}
    by_title: dict[str, str] = {}
    apps = []
    if INVENTORY.exists():
        try:
            apps = json.loads(INVENTORY.read_text(encoding="utf-8")).get("nostr_apps", [])
        except Exception:
            apps = []
    profile_domains = {
        "damus": "damus.io",
        "amethyst": "amethyst.social",
        "primal": "primal.net",
        "coracle": "coracle.social",
        "iris": "iris.to",
        "nostur": "nostur.com",
        "nostrudel": "nostrudel.ninja",
        "yakihonne": "yakihonne.com",
        "alby": "getalby.com",
        "wavlake": "wavlake.com",
        "amber": "github.com/greenart7c3/amber",
    }
    for slug, domain in profile_domains.items():
        by_slug[slug] = favicon_url(domain)
    for app in apps:
        slug = slugify(app.get("slug") or app.get("name") or "")
        name_key = slugify(app.get("name") or slug)
        domain = APP_ICON_DOMAIN_OVERRIDES.get(slug, "")
        if not domain:
            for link in app.get("links", []):
                candidate = domain_from_url(link)
                if candidate and candidate not in SKIP_ICON_DOMAINS:
                    domain = candidate
                    break
            if not domain and app.get("links"):
                domain = domain_from_url(app["links"][0])
        icon = favicon_url(domain)
        if icon:
            by_slug[slug] = icon
            by_title[name_key] = icon
    for slug, icon in list(by_slug.items()):
        by_title.setdefault(slug, icon)
    return by_slug, by_title


APP_ICON_BY_SLUG, APP_ICON_BY_TITLE = build_app_icon_maps()


PERSON_IMAGE_BY_SLUG = {
    "people/enoch-root": "/assets/nostr-people/enoch-root.jpeg",
    "people/fiatjaf": "https://github.com/fiatjaf.png?size=192",
    "people/william-casarin-jb55": "https://github.com/jb55.png?size=192",
    "people/vitor-pamplona": "https://github.com/vitorpamplona.png?size=192",
    "people/pablof7z": "https://github.com/pablof7z.png?size=192",
    "people/hodlbod": "https://github.com/staab.png?size=192",
    "people/yuki-kishimoto": "https://github.com/yukibtc.png?size=192",
    "people/mike-dilger": "https://github.com/mikedilger.png?size=192",
    "people/hzrd149": "https://github.com/hzrd149.png?size=192",
    "people/stuart-bowman": "https://github.com/lovvtide.png?size=192",
    "people/alex-gleason": "https://github.com/alexgleason.png?size=192",
    "people/evan-henshaw-plath-rabble": "https://www.nos.social/favicon.ico",
    "people/martti-malmi": "https://github.com/mmalmi.png?size=192",
    "people/greenart7c3": "https://github.com/greenart7c3.png?size=192",
    "people/miljan-braticevic": favicon_url("primal.net", 192),
    "people/lyn-alden": favicon_url("lynalden.com", 192),
    "people/sarah-perez": favicon_url("techcrunch.com", 192),
    "people/george-kaloudis": favicon_url("coindesk.com", 192),
    "people/ben-perrin-btc-sessions": "https://yt3.googleusercontent.com/ytc/AIdro_kxV49dDEY0Ti1bD49lVej4Hvk1A9YfYu4SbsWrbPO3lQ=s192-c-k-c0x00ffffff-no-rj",
    "people/derek-ross": "https://nostr.world/images/derek.png",
    "people/roger-huang": favicon_url("forbes.com", 192),
    "people/m-k-fain": favicon_url("soapbox.pub", 192),
    "people/ez-no-bullshit-bitcoin": favicon_url("nobsbitcoin.com", 192),
    "people/yiluo-wei": favicon_url("arxiv.org", 192),
    "people/gareth-tyson": favicon_url("arxiv.org", 192),
}


PERSON_IMAGE_BY_TITLE = {
    slugify(person["name"]): PERSON_IMAGE_BY_SLUG.get(person["slug"], "")
    for person in PEOPLE
}
NOSTRIGA_SOURCE_URL = "https://nostr.world/speakers/index.html"


NOSTRIGA_PEOPLE = [
    ("Jack Dorsey", "Open social funding signal and Block founder.", "https://nostr.world/images/jack.png"),
    ("ODELL", "ALL CAPS NOSTRICH and Bitcoin-Nostr culture voice.", "https://nostr.world/images/odell.png"),
    ("William Casarin", "Damus creator.", "https://nostr.world/images/will.png"),
    ("PABLOF7Z", "Sanity Island, Sovereign Engineering and Nostr tooling.", "https://nostr.world/images/pablo.png"),
    ("Ben Arc", "LNbits and Nostr builder.", "https://nostr.world/images/ben.png"),
    ("Vanessa", "Damus operations and product culture.", "https://nostr.world/images/vanessa.png"),
    ("Gsovereignty", "Nostrovia Pod and Nostrocket builder.", "https://nostr.world/images/gsov.png"),
    ("Terry Yiu", "Comingle founder.", "https://nostr.world/images/terry.png"),
    ("Alex Gleason", "Fediverse software creator and Nostr bridge builder.", "https://nostr.world/images/alex.png"),
    ("HZRD", "Nostrudel and Blossom builder.", "https://nostr.world/images/hzrd.png"),
    ("Calvadev", "Nostr builder and community voice.", "https://nostr.world/images/calva.png"),
    ("Rabble", "Nos Social founder and open social instigator.", "https://nostr.world/images/instigator.png"),
    ("Jeff G", "FOSS developer and Nostr educator.", "https://nostr.world/images/jeffg.png"),
    ("Derek Ross", "Nostr educator and ecosystem evangelist.", "https://nostr.world/images/derek.png"),
    ("Water Blower", "Blowater creator.", "https://nostr.world/images/water.png"),
    ("Stuart Bowman", "Satellite Earth builder.", "https://nostr.world/images/stuart.png"),
    ("Cypher Perro", "Bitcoin and Nostr culture creator.", "https://nostr.world/images/cypher.png"),
    ("Elsat", "Damus and freedom-tech product contributor.", "https://nostr.world/images/elsat.jpg"),
    ("Grunch", "Software engineer and FOSS supporter.", "https://nostr.world/images/grunch.jpg"),
    ("Marce", "Nostr public-relations and community presence.", "https://nostr.world/images/marce.jpg"),
    ("Mir", "Nostriga speaker and community participant.", "https://nostr.world/images/mir.jpg"),
    ("Miljan", "Primal builder.", "https://nostr.world/images/miljan.jpg"),
    ("Niel Liesmons", "NIP-05 and identity conversation participant.", "https://nostr.world/images/niel.png"),
    ("Linda", "Nos Social product.", "https://nostr.world/images/linda.jpg"),
    ("Saunter", "Alby UX designer.", "https://nostr.world/images/saunter.jpg"),
    ("Dustin Dannenhauer", "AI researcher in the Nostr scene.", "https://nostr.world/images/dustin.jpg"),
    ("Arsh Molu", "Human Rights Foundation.", "https://nostr.world/images/arsh.jpg"),
    ("Alex Li", "Freedom-tech and HRF-adjacent activist.", "https://nostr.world/images/alex-li.jfif"),
    ("Franzap", "Nostr developer.", "https://nostr.world/images/franzap.jpg"),
    ("Colby Serpa", "Nestr architect.", "https://nostr.world/images/colby.gif"),
    ("Kieran", "Nostr builder.", "https://nostr.world/images/kiearan.png"),
    ("Karnage", "Product designer across Snort, Nostr Nests, zap.stream, Habla and Nostr design tools.", "https://nostr.world/images/karnage.jpg"),
    ("MSvB", "Electronics producer and cryptosecure systems thinker.", "https://nostr.world/images/msvb.webp"),
    ("Calle", "Bitcoin and open-source developer.", "https://nostr.world/images/calle.jfif"),
    ("Oscar Merry", "Fountain Podcasts builder.", "https://nostr.world/images/oscar.webp"),
    ("OpenMike", "Independent music and value-for-value creator.", "https://nostr.world/images/openmike.jpg"),
    ("Preston", "Bitcoin and books; Ego Death Capital.", "https://nostr.world/images/preston.gif"),
    ("Unoster", "Senior developer and systems thinker.", "https://nostr.world/images/U.png"),
    ("Martti Malmi", "Iris developer and early Bitcoin contributor.", "https://nostr.world/images/martti.jpg"),
    ("Svetski", "Network-state and freedom-tech builder.", "https://nostr.world/images/svetski.jpg"),
    ("DanConwayDev", "Freedom-tech developer and ngit creator.", "https://nostr.world/images/dan.jpg"),
    ("Jack Mallers", "Strike founder and Bitcoin payments builder.", "https://nostr.world/images/jackm.jfif"),
    ("Greg Tonoski", "Nostriga speaker and ecosystem participant.", "https://nostr.world/images/greg.jfif"),
    ("UNCLE ROCKSTAR", "Bitcoin public-goods contributor and community voice.", "https://nostr.world/images/rockstar.png"),
    ("Mads", "Bitcoin and Lightning operator.", "https://nostr.world/images/mads.jpg"),
    ("Exfrog", "BTC++, BitBlockBoom, TABConf, Unconfiscatable and NostrWorld event builder.", "https://nostr.world/images/exfrog.jpg"),
    ("Paul Keating", "Primal and Daylight builder.", "https://nostr.world/images/paul.jpg"),
    ("Reverend Hodl", "Nostriga speaker and community participant.", "https://nostr.world/images/reverend.jpg"),
]


PERSON_IMAGE_BY_TITLE.update({
    slugify(name): image
    for name, _role, image in NOSTRIGA_PEOPLE
})


for item in PAGES:
    if item["slug"] == "people":
        item["sections"].append(
            section(
                "Nostriga scene map",
                [
                    "The Nostr people map should feel like walking into the room, not reading a company chart. This scene map pulls in public Nostriga speaker data so the page shows more of the real crowd: product builders, educators, designers, musicians, event people, relay thinkers, Bitcoin operators and culture carriers.",
                    "These entries are not final biographies. They are public doors into the wider Nostr crowd and a queue for deeper Crays profiles."
                ],
                cards=[
                    (name, role, NOSTRIGA_SOURCE_URL)
                    for name, role, _image in NOSTRIGA_PEOPLE
                ],
            )
        )
        item["sections"].append(
            section(
                "Where more names come from",
                [
                    "A serious Nostr people archive cannot stop at famous founders. The next layer is grant waves, conference speaker lists, app maintainers, relay operators, musicians, designers, educators and the builders behind the tools people actually touch.",
                    "Crays should keep this as a living people atlas: friendly enough for a reader to browse, precise enough that no one has to guess why a name matters."
                ],
                cards=[
                    ("Nostriga speakers", "Public speaker list with photos and roles from the Riga Nostr unconference.", NOSTRIGA_SOURCE_URL),
                    ("OpenSats Nostr Fund", "Grant waves and long-term support announcements reveal many active maintainers and public-good builders.", "https://opensats.org/funds/nostr"),
                    ("Nostr World", "Event pages and archives show the live social layer around the protocol.", "https://nostr.world/"),
                    ("Nostr Apps", "App listings reveal the product builders behind clients, signers, media tools and marketplaces.", "https://www.nostrapps.com/"),
                ],
            )
        )


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


SECTION_NAVS = {
    "start": {
        "title": "Start guide",
        "deck": "Begin here when you want the map before the maze: what a key is, why relays exist, how clients differ, where Bitcoin fits and why Crays cares.",
        "groups": [
            (
                "Read first",
                [
                    ("What is Nostr?", "what-is-nostr"),
                    ("Getting started", "getting-started"),
                    ("Why Nostr matters", "why-nostr"),
                    ("Glossary", "glossary"),
                    ("Useful links", "resources"),
                    ("Media and video archive", "nostr-media-article-video-archive"),
                ],
            ),
            (
                "Choose your route",
                [
                    ("Beginner path", "reading-paths/beginner"),
                    ("Developer path", "reading-paths/developer"),
                    ("Creator path", "reading-paths/creator"),
                    ("Operator path", "reading-paths/operator"),
                    ("Culture path", "reading-paths/culture"),
                    ("Research path", "reading-paths/research"),
                ],
            ),
            (
                "Useful next",
                [
                    ("Privacy and security", "privacy-security"),
                    ("Search and trust", "search-and-web-of-trust"),
                    ("Moderation and discovery", "moderation-discovery"),
                    ("Nostr vs Mastodon", "nostr-vs-mastodon"),
                    ("Crays Circle GitHub", "resources"),
                ],
            ),
        ],
    },
    "people": {
        "title": "People and culture guide",
        "deck": "This is the human layer: protocol authors, client builders, relay operators, funders, creators, events, music, media and the culture that makes the network feel alive.",
        "groups": [
            (
                "Orientation",
                [
                    ("People archive", "people"),
                    ("Enoch Root", "people/enoch-root"),
                    ("Creators", "creators"),
                    ("Jack Dorsey context", "jack-dorsey"),
                    ("Events", "events"),
                    ("Lifestyle culture", "lifestyle-culture"),
                    ("Music and media", "music-video-media"),
                    ("Media and video archive", "nostr-media-article-video-archive"),
                    ("Nostr and Bitcoin", "nostr-and-bitcoin"),
                ],
            ),
            (
                "Builder profiles",
                [
                    ("Enoch Root", "people/enoch-root"),
                    ("fiatjaf", "people/fiatjaf"),
                    ("William Casarin", "people/william-casarin-jb55"),
                    ("Vitor Pamplona", "people/vitor-pamplona"),
                    ("Mike Dilger", "people/mike-dilger"),
                    ("Alex Gleason", "people/alex-gleason"),
                    ("Pablof7z", "people/pablof7z"),
                    ("Yuki Kishimoto", "people/yuki-kishimoto"),
                ],
            ),
            (
                "Media voices",
                [
                    ("Lyn Alden", "people/lyn-alden"),
                    ("Sarah Perez", "people/sarah-perez"),
                    ("George Kaloudis", "people/george-kaloudis"),
                    ("Ben Perrin", "people/ben-perrin-btc-sessions"),
                    ("Derek Ross", "people/derek-ross"),
                    ("Media and video archive", "nostr-media-article-video-archive"),
                ],
            ),
            (
                "Culture questions",
                [
                    ("Free speech and censorship", "free-speech-censorship"),
                    ("Moderation and discovery", "moderation-discovery"),
                    ("Web of trust", "deep-dives/web-of-trust-in-practice"),
                    ("Nostr events history", "deep-dives/nostr-events-history"),
                    ("Media voices", "nostr-media-article-video-archive"),
                ],
            ),
        ],
    },
    "apps": {
        "title": "Apps and products guide",
        "deck": "Start with Crays.net, then read the market around it: clients, signers, wallets, publishing tools, discovery layers, media apps and experiments that show what Nostr can become.",
        "groups": [
            (
                "Start with apps",
                [
                    ("Complete app catalog", "apps/catalog"),
                    ("Apps overview", "apps"),
                    ("App profiles", "app-profiles"),
                    ("Research app atlas", "apps/research-atlas"),
                    ("Developer stack research", "apps/developer-stack-research"),
                    ("Clients", "clients"),
                    ("Developer tools", "developer-tools"),
                    ("Nostr login", "nostr-login"),
                ],
            ),
            (
                "Major examples",
                [
                    ("Damus", "apps/damus"),
                    ("Amethyst", "apps/amethyst"),
                    ("Safebox", "apps/safebox"),
                    ("Blossom Servers", "deep-dives/blossom-servers-and-relays"),
                    ("Primal", "apps/primal"),
                    ("Iris", "apps/iris"),
                    ("Coracle", "apps/coracle"),
                    ("Yakihonne", "apps/yakihonne"),
                    ("Alby", "apps/alby"),
                    ("FoundUPS Agent", "apps/foundups-agent"),
                    ("Amber", "apps/amber"),
                    ("Wavlake", "apps/wavlake"),
                ],
            ),
            (
                "Product categories",
                [
                    ("Microblogging", "apps/category-microblogging"),
                    ("Photos", "apps/category-photos"),
                    ("Streaming", "apps/category-streaming"),
                    ("Blogging", "apps/category-blogging"),
                    ("Group chat", "apps/category-group-chat"),
                    ("Discovery", "apps/category-discovery"),
                    ("Marketplaces", "apps/category-marketplace"),
                    ("Music", "apps/category-music"),
                    ("Signers", "apps/category-signers"),
                ],
            ),
        ],
    },
    "relays": {
        "title": "Relay market guide",
        "deck": "Relays are the part of Nostr people feel before they understand: speed, missing posts, paid access, spam resistance, local rooms, moderation and archive reliability.",
        "groups": [
            (
                "Market map",
                [
                    ("Relay market directory", "relay-market-directory"),
                    ("Nostr relays", "relays"),
                    ("Relay research atlas", "relays/research-atlas"),
                    ("Relay selection", "field-guide/relay-selection"),
                    ("Relay business models", "deep-dives/relay-business-models"),
                    ("Blossom servers", "deep-dives/blossom-servers-and-relays"),
                    ("Outbox model", "deep-dives/outbox-model"),
                ],
            ),
            (
                "Relay standards",
                [
                    ("NIP-11 relay information", "nips/nip-11"),
                    ("NIP-42 relay auth", "nip-42-relay-auth"),
                    ("NIP-65 relay lists", "nip-65-relay-list"),
                    ("NIP-66 relay discovery", "nips/nip-66"),
                    ("NIP-50 search", "nips/nip-50"),
                ],
            ),
            (
                "Crays relay layer",
                [
                    ("Super Nodes", "crays-super-node"),
                    ("Operators and venues", "operators-venues"),
                    ("Crays World local graph", "deep-dives/crays-world-local-graph"),
                    ("Nostr for venues", "deep-dives/nostr-for-venues"),
                ],
            ),
        ],
    },
    "nips": {
        "title": "Protocol and NIPs guide",
        "deck": "This shelf turns standards into plain consequences: what becomes portable, what gets safer, what clients must support and what still needs product judgment.",
        "groups": [
            (
                "Start with protocol",
                [
                    ("Complete NIP index", "nips/complete-index"),
                    ("NIPs overview", "nips"),
                    ("NIP research atlas", "nips/research-atlas"),
                    ("Keys and identity", "keys-identity"),
                    ("Events and kinds", "events-and-kinds"),
                    ("Relays", "relays"),
                    ("Clients", "clients"),
                ],
            ),
            (
                "NIPs readers ask about",
                [
                    ("NIP-01 basic protocol", "nips/nip-01"),
                    ("NIP-05 identifiers", "nip-05-identifiers"),
                    ("NIP-07 signers", "nip-07-signers"),
                    ("NIP-19 addresses", "nip-19-addresses"),
                    ("NIP-23 long-form", "nip-23-long-form"),
                    ("NIP-42 relay auth", "nip-42-relay-auth"),
                    ("NIP-44 encryption", "nip-44-encryption"),
                    ("NIP-46 remote signing", "nip-46-remote-signing"),
                    ("NIP-57 zaps", "nip-57-zaps-lightning"),
                ],
            ),
            (
                "Product-facing NIPs",
                [
                    ("Wallet connect", "nip-47-wallet-connect"),
                    ("Badges", "nip-58-badges"),
                    ("Relay lists", "nip-65-relay-list"),
                    ("Files", "nip-94-files"),
                    ("File storage", "nip-96-file-storage"),
                    ("HTTP auth", "nip-98-http-auth"),
                ],
            ),
        ],
    },
    "privacy": {
        "title": "Privacy and trust guide",
        "deck": "This route keeps control close to you: keys, signing, identity, censorship resistance, web-of-trust, moderation and security tradeoffs.",
        "groups": [
            (
                "Control first",
                [
                    ("Privacy and security", "privacy-security"),
                    ("Keys and identity", "keys-identity"),
                    ("Search and trust", "search-and-web-of-trust"),
                    ("Free speech and censorship", "free-speech-censorship"),
                    ("Moderation and discovery", "moderation-discovery"),
                ],
            ),
            (
                "Security standards",
                [
                    ("NIP-44 encryption", "nip-44-encryption"),
                    ("NIP-46 remote signing", "nip-46-remote-signing"),
                    ("NIP-98 HTTP auth", "nip-98-http-auth"),
                    ("NIP-42 relay auth", "nip-42-relay-auth"),
                    ("NIP-05 identifiers", "nip-05-identifiers"),
                ],
            ),
            (
                "Threats and trust",
                [
                    ("Security threat model", "deep-dives/nostr-security-threat-model"),
                    ("Spam and abuse", "deep-dives/nostr-spam-and-abuse"),
                    ("Web of trust", "deep-dives/web-of-trust-in-practice"),
                    ("Legal and compliance", "deep-dives/nostr-legal-and-compliance"),
                    ("Nostr vs Mastodon", "nostr-vs-mastodon"),
                ],
            ),
        ],
    },
    "wallets": {
        "title": "Wallets and value guide",
        "deck": "Here Nostr meets value flow: zaps, Lightning, wallet connect, Safebox records and the payment paths people can actually carry with them.",
        "groups": [
            (
                "Value flow",
                [
                    ("Nostr and Bitcoin", "nostr-and-bitcoin"),
                    ("NIP-47 Wallet Connect", "nip-47-wallet-connect"),
                    ("NIP-57 zaps", "nip-57-zaps-lightning"),
                    ("Safebox", "apps/safebox"),
                    ("Safebox records wallet", "deep-dives/safebox-sovereign-wallet-records"),
                ],
            ),
            (
                "Wallet apps",
                [
                    ("Alby", "apps/alby"),
                    ("Amber", "apps/amber"),
                    ("Blossom Servers", "deep-dives/blossom-servers-and-relays"),
                    ("NIP-94 files", "nip-94-files"),
                    ("NIP-96 file storage", "nip-96-file-storage"),
                ],
            ),
            (
                "Payment context",
                [
                    ("Content sale", "content-sale"),
                    ("Creator business", "deep-dives/nostr-for-creators-business"),
                    ("Crays venue payments", "operators-venues"),
                    ("Nostr for investors", "deep-dives/nostr-for-investors"),
                ],
            ),
        ],
    },
    "media": {
        "title": "Media and creators guide",
        "deck": "This is where portable identity becomes public culture: creators, long-form posts, music, video, publishing tools and fan relationships.",
        "groups": [
            (
                "Creator layer",
                [
                    ("Creators", "creators"),
                    ("Music and media", "music-video-media"),
                    ("Videos", "videos"),
                    ("Media and video archive", "nostr-media-article-video-archive"),
                    ("NIP-23 long-form", "nip-23-long-form"),
                    ("Creator reading path", "reading-paths/creator"),
                ],
            ),
            (
                "Media apps",
                [
                    ("Wavlake", "apps/wavlake"),
                    ("YakiHonne", "apps/yakihonne"),
                    ("Habla", "apps/habla"),
                    ("Long-form content", "nip-23-long-form"),
                    ("Streaming apps", "apps/category-streaming"),
                ],
            ),
            (
                "Publishing formats",
                [
                    ("Blogging apps", "apps/category-blogging"),
                    ("Music apps", "apps/category-music"),
                    ("Photo apps", "apps/category-photos"),
                    ("Streaming apps", "apps/category-streaming"),
                    ("Content sale", "content-sale"),
                ],
            ),
        ],
    },
    "commerce": {
        "title": "Commerce and markets guide",
        "deck": "Use this route for business models: creator sales, marketplaces, FoundUPS, agent economies, investor logic and revenue design.",
        "groups": [
            (
                "Commerce basics",
                [
                    ("Content sale", "content-sale"),
                    ("Creator business", "deep-dives/nostr-for-creators-business"),
                    ("Marketplace apps", "apps/category-marketplace"),
                    ("Nostr for investors", "deep-dives/nostr-for-investors"),
                    ("Nostr SEO and public web", "deep-dives/nostr-seo-and-public-web"),
                ],
            ),
            (
                "FoundUPS route",
                [
                    ("FoundUPS Agent", "apps/foundups-agent"),
                    ("FoundUPS compute network", "deep-dives/foundups-agent-compute-focus-network"),
                    ("FoundUPS agent economy", "deep-dives/foundups-and-nostr-agent-economy"),
                    ("Developer stack research", "apps/developer-stack-research"),
                ],
            ),
            (
                "Revenue tools",
                [
                    ("Zaps", "nip-57-zaps-lightning"),
                    ("Wallet Connect", "nip-47-wallet-connect"),
                    ("Badges", "nip-58-badges"),
                    ("Crays Award", "awards"),
                ],
            ),
        ],
    },
    "governance": {
        "title": "Governance and reputation guide",
        "deck": "This route keeps the social layer accountable: badges, voting, reputation, moderation, policy, DAO readiness and public records.",
        "groups": [
            (
                "Reputation",
                [
                    ("DAO governance", "dao-governance"),
                    ("NIP-58 badges", "nip-58-badges"),
                    ("Crays Award voting", "deep-dives/crays-award-voting"),
                    ("Search and trust", "search-and-web-of-trust"),
                    ("Web of trust", "deep-dives/web-of-trust-in-practice"),
                ],
            ),
            (
                "Policy and moderation",
                [
                    ("Moderation and discovery", "moderation-discovery"),
                    ("Legal and compliance", "deep-dives/nostr-legal-and-compliance"),
                    ("Spam and abuse", "deep-dives/nostr-spam-and-abuse"),
                    ("Free speech and censorship", "free-speech-censorship"),
                ],
            ),
            (
                "Crays governance",
                [
                    ("DAO readiness", "deep-dives/crays-dao-readiness"),
                    ("Crays Award", "awards"),
                    ("Operators and venues", "operators-venues"),
                    ("Super Nodes", "crays-super-node"),
                ],
            ),
        ],
    },
    "crays": {
        "title": "Crays implementation guide",
        "deck": "Here the protocol stops being abstract: Crays.net profiles, creator access, status, venues, award voting, Super Nodes, payments and DAO-ready governance live in one connected stack.",
        "groups": [
            (
                "Crays layer",
                [
                    ("Nostr and Crays", "nostr-and-crays"),
                    ("Crays Circle GitHub", "resources"),
                    ("Content sale", "content-sale"),
                    ("Crays Award", "awards"),
                    ("Super Nodes", "crays-super-node"),
                    ("Operators and venues", "operators-venues"),
                    ("DAO governance", "dao-governance"),
                ],
            ),
            (
                "Product deep dives",
                [
                    ("Crays.net as client", "deep-dives/crays-net-as-nostr-client"),
                    ("Developer tools", "developer-tools"),
                    ("Crays World local graph", "deep-dives/crays-world-local-graph"),
                    ("Crays Award voting", "deep-dives/crays-award-voting"),
                    ("DAO readiness", "deep-dives/crays-dao-readiness"),
                    ("NIP-05 for brands", "deep-dives/nip-05-for-brands"),
                    ("Creator business", "deep-dives/nostr-for-creators-business"),
                    ("Safebox records wallet", "deep-dives/safebox-sovereign-wallet-records"),
                    ("Blossom media servers", "deep-dives/blossom-servers-and-relays"),
                    ("FoundUPS compute network", "deep-dives/foundups-agent-compute-focus-network"),
                ],
            ),
            (
                "Risks and strategy",
                [
                    ("Legal and compliance", "deep-dives/nostr-legal-and-compliance"),
                    ("Security threat model", "deep-dives/nostr-security-threat-model"),
                    ("Spam and abuse", "deep-dives/nostr-spam-and-abuse"),
                    ("Investor view", "deep-dives/nostr-for-investors"),
                    ("SEO and public web", "deep-dives/nostr-seo-and-public-web"),
                ],
            ),
        ],
    },
    "library": {
        "title": "Library map",
        "deck": "The whole shelf lives here: source audits, deep research, app maps, NIP references, field guides, long reads and the routes that keep a huge archive actually usable.",
        "groups": [
            (
                "Whole archive",
                [
                    ("Library overview", "archive-library"),
                    ("Field guides", "field-guide/relay-selection"),
                    ("Reading paths", "reading-paths/beginner"),
                    ("Deep dives", "deep-dives/portable-social-graph"),
                    ("Useful links", "resources"),
                    ("Research map", "source-inventory"),
                    ("Media and video archive", "nostr-media-article-video-archive"),
                    ("Deep research database", "source-inventory/deep-research-database"),
                    ("Reads research", "archive-library/reads-research"),
                    ("Source map research", "archive-library/source-map-research"),
                    ("Security wallet research", "archive-library/security-wallet-research"),
                    ("Videos", "videos"),
                    ("Crays Circle GitHub", "resources"),
                ],
            ),
            (
                "Ecosystem maps",
                [
                    ("Awesome Nostr map", "awesome-nostr"),
                    ("Protocol projects", "awesome-nostr/protocol"),
                    ("Clients", "awesome-nostr/clients"),
                    ("Relays", "awesome-nostr/relays"),
                    ("Tools", "awesome-nostr/tools"),
                    ("Funding", "awesome-nostr/funding"),
                    ("Recommended reading", "awesome-nostr/recommended-reading-watching"),
                ],
            ),
            (
                "Research branches",
                [
                    ("Deep research database", "source-inventory/deep-research-database"),
                    ("Core research", "source-inventory/deep-research/core"),
                    ("Apps research", "source-inventory/deep-research/apps"),
                    ("Relay research", "source-inventory/deep-research/relays"),
                    ("NIP research", "source-inventory/deep-research/nips"),
                    ("Developer stack", "source-inventory/deep-research/dev"),
                    ("Blossom servers", "deep-dives/blossom-servers-and-relays"),
                    ("Reads and research", "source-inventory/deep-research/reads"),
                    ("Security and wallets", "source-inventory/deep-research/security"),
                    ("App research atlas", "apps/research-atlas"),
                    ("Relay research atlas", "relays/research-atlas"),
                    ("NIP research atlas", "nips/research-atlas"),
                    ("Developer topic atlas", "apps/developer-stack-research"),
                    ("nostr.how", "source-inventory/nostr-how"),
                    ("nostrapps.com", "source-inventory/nostrapps-com"),
                    ("nostr.com", "source-inventory/nostr-com"),
                    ("nostr.org", "source-inventory/nostr-org"),
                    ("nostrlogin.org", "source-inventory/nostrlogin-org"),
                    ("nostr.co.uk", "source-inventory/nostr-co-uk"),
                    ("nostr.net", "source-inventory/nostr-net"),
                ],
            ),
        ],
    },
}


def nostr_href(slug: str) -> str:
    return f"/nostr/{esc(slug)}/"


STATIC_INLINE_LINKS = [
    ("FoundUPS Agent", "apps/foundups-agent"),
    ("FoundUPS", "deep-dives/foundups-agent-compute-focus-network"),
    ("Safebox records", "deep-dives/safebox-sovereign-wallet-records"),
    ("Safebox", "apps/safebox"),
    ("agent economy", "deep-dives/foundups-and-nostr-agent-economy"),
    ("Nostr Wallet Connect", "nip-47-wallet-connect"),
    ("Blossom Servers", "deep-dives/blossom-servers-and-relays"),
    ("Blossom servers", "deep-dives/blossom-servers-and-relays"),
    ("Blossom server", "deep-dives/blossom-servers-and-relays"),
    ("Blossom", "deep-dives/blossom-servers-and-relays"),
    ("BUD-11", "deep-dives/blossom-servers-and-relays"),
    ("BUD-03", "deep-dives/blossom-servers-and-relays"),
    ("BUD-02", "deep-dives/blossom-servers-and-relays"),
    ("BUD-01", "deep-dives/blossom-servers-and-relays"),
    ("Cashu", "deep-dives/safebox-sovereign-wallet-records"),
    ("NIP-98", "nip-98-http-auth"),
    ("NIP-96", "nip-96-file-storage"),
    ("NIP-94", "nip-94-files"),
    ("NIP-65", "nip-65-relay-list"),
    ("NIP-58", "nip-58-badges"),
    ("NIP-57", "nip-57-zaps-lightning"),
    ("NIP-47", "nip-47-wallet-connect"),
    ("NIP-46", "nip-46-remote-signing"),
    ("NIP-44", "nip-44-encryption"),
    ("NIP-42", "nip-42-relay-auth"),
    ("NIP-23", "nip-23-long-form"),
    ("NIP-19", "nip-19-addresses"),
    ("NIP-07", "nip-07-signers"),
    ("NIP-05", "nip-05-identifiers"),
    ("private key", "keys-identity"),
    ("public key", "keys-identity"),
    ("keys", "keys-identity"),
    ("clients", "clients"),
    ("relays", "relays"),
    ("events", "events-and-kinds"),
    ("NIPs", "nips/complete-index"),
    ("zaps", "nip-57-zaps-lightning"),
    ("Lightning", "nip-57-zaps-lightning"),
    ("signers", "nip-07-signers"),
    ("apps", "apps/catalog"),
]


def build_inline_links() -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = list(STATIC_INLINE_LINKS)
    static_labels = {label.lower() for label, _slug in STATIC_INLINE_LINKS}
    skip_labels = {
        "nostr",
        "crays",
        "read",
        "source",
        "sources",
        "archive",
        "library",
        "research",
        "index",
        "guide",
        "complete",
        "people",
        "apps",
    }
    for item in PAGES:
        slug = item["slug"]
        if slug.startswith("source-inventory/deep-research/"):
            continue
        if slug.startswith(("apps/research/", "apps/developer-stack/", "relays/research/", "nips/research/")):
            continue
        if slug.startswith(("archive-library/source-map-research/", "archive-library/reads-research/")):
            continue
        title = clean_copy(item["title"]).strip()
        candidates = [title]
        if not slug.startswith(("apps/catalog/", "awesome-nostr/")):
            candidates.extend(item.get("keywords", [])[:4])
        for candidate in candidates:
            label = clean_copy(candidate).strip()
            if not label or len(label) < 4 or len(label) > 54:
                continue
            if label.lower() in skip_labels:
                continue
            if label.lower() in static_labels:
                continue
            if label.startswith("Research Source:"):
                continue
            if re.fullmatch(r"NIP-\d{2,3}", label):
                continue
            items.append((label, item["slug"]))
    seen: set[tuple[str, str]] = set()
    deduped: list[tuple[str, str]] = []
    for label, slug in sorted(items, key=lambda pair: (-len(pair[0]), pair[0].lower())):
        key = (label.lower(), slug)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((label, slug))
    return deduped


INLINE_LINKS = build_inline_links()
INLINE_LINK_PATTERNS = [
    (
        label,
        slug,
        label.lower(),
        re.compile(rf"(?<![A-Za-z0-9-]){re.escape(label)}(?![A-Za-z0-9-])", re.IGNORECASE),
    )
    for label, slug in INLINE_LINKS
]


def link_text(text: str, current_slug: str, used_links: dict[str, int]) -> str:
    raw = str(text)
    raw_lower = raw.lower()
    candidates: list[tuple[int, int, str, str, str]] = []
    for label, slug, key, pattern in INLINE_LINK_PATTERNS:
        if slug == current_slug or used_links.get(key, 0) >= 8:
            continue
        if key not in raw_lower:
            continue
        match = pattern.search(raw)
        if match:
            candidates.append((match.start(), match.end(), label, slug, key))
    chosen: list[tuple[int, int, str, str, str]] = []
    occupied: list[tuple[int, int]] = []
    for start, end, label, slug, key in sorted(candidates, key=lambda item: (item[0], -(item[1] - item[0]))):
        if len(chosen) >= 18:
            break
        if any(start < used_end and end > used_start for used_start, used_end in occupied):
            continue
        chosen.append((start, end, label, slug, key))
        occupied.append((start, end))
        used_links[key] = used_links.get(key, 0) + 1
    if not chosen:
        return esc(raw)
    out: list[str] = []
    cursor = 0
    for start, end, _label, slug, _key in sorted(chosen, key=lambda item: item[0]):
        out.append(esc(raw[cursor:start]))
        out.append(f'<a href="{nostr_href(slug)}">{esc(raw[start:end])}</a>')
        cursor = end
    out.append(esc(raw[cursor:]))
    return "".join(out)


def render_source_cards(sources):
    return "\n".join(
        f'<a class="crays-nostr-source-card" href="{esc(url)}" target="_blank" rel="noreferrer noopener"><strong>{esc(crays_voice(title))}</strong><span>{esc(crays_voice(desc))}</span></a>'
        for title, url, desc in sources
    )


def youtube_id(value: object) -> str:
    raw = str(value or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", raw):
        return raw
    match = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", raw)
    return match.group(1) if match else ""


def youtube_url(video: dict) -> str:
    if video.get("url"):
        return str(video["url"])
    vid = youtube_id(video.get("id"))
    return f"https://www.youtube.com/watch?v={vid}" if vid else ""


def render_video_grid(videos: list[dict]) -> str:
    if not videos:
        return ""
    cards = []
    for video in videos:
        vid = youtube_id(video.get("id") or video.get("url"))
        title = crays_voice(video.get("title", "Nostr video"))
        channel = crays_voice(video.get("channel", "Nostr video"))
        note = crays_voice(video.get("use") or video.get("note") or "")
        category = crays_voice(video.get("category", "Video"))
        watch_url = youtube_url(video)
        if vid:
            media = (
                f'<iframe src="https://www.youtube-nocookie.com/embed/{esc(vid)}" '
                f'title="{esc(title)}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
            )
        else:
            media = f'<a class="crays-nostr-video-card__fallback" href="{esc(watch_url)}">{esc(title)}</a>'
        cards.append(
            '<article class="crays-nostr-video-card">'
            f'<div class="crays-nostr-video-card__media">{media}</div>'
            '<div class="crays-nostr-video-card__body">'
            f'<span>{esc(category)}</span>'
            f'<h3>{esc(title)}</h3>'
            f'<p>{esc(note)}</p>'
            f'<small>{esc(channel)}</small>'
            f'<a href="{esc(watch_url)}">Open on YouTube</a>'
            '</div>'
            '</article>'
        )
    return f'<div class="crays-nostr-video-grid">{"".join(cards)}</div>'


def render_sections(item):
    used_links: dict[str, int] = {}
    scenes = pick_stock_scenes(item)
    parts = [
        f'<p>{link_text(crays_voice(item["intro"]), item["slug"], used_links)}</p>',
        f'<div class="crays-nostr-reader-note"><strong>{esc(crays_voice(item.get("quick_label", "The quick read")))}</strong><span>{esc(crays_voice(item["deck"]))}</span></div>',
        render_stock_scene_strip(item, scenes[:2]),
    ]
    midpoint = max(2, len(item["sections"]) // 2) if item["sections"] else 0
    for section_index, sec in enumerate(item["sections"], start=1):
        sid = slugify(sec["title"])
        parts.append(f'<h2 id="{esc(sid)}">{esc(crays_voice(sec["title"]))}</h2>')
        for paragraph in sec["paragraphs"]:
            parts.append(f"<p>{link_text(crays_voice(paragraph), item['slug'], used_links)}</p>")
        if sec["bullets"]:
            parts.append('<ul class="crays-article-list">')
            for strong, text in sec["bullets"]:
                parts.append(f"<li><strong>{esc(crays_voice(strong))}.</strong> {link_text(crays_voice(text), item['slug'], used_links)}</li>")
            parts.append("</ul>")
        if sec["cards"]:
            parts.append('<div class="crays-nostr-hub-grid">')
            for card in sec["cards"]:
                strong, text = card[0], card[1]
                href = card[2] if len(card) > 2 else None
                kind = mini_card_kind(strong, href)
                card_text = esc(crays_voice(text)) if href else link_text(crays_voice(text), item["slug"], used_links)
                card_face = (
                    f'{render_card_badge(strong, href)}'
                    f'<strong>{esc(crays_voice(strong))}</strong>'
                    f'<span>{card_text}</span>'
                )
                if href:
                    parts.append(f'<a class="crays-nostr-hub-mini-card" data-card-kind="{esc(kind)}" href="{esc(href)}">{card_face}</a>')
                else:
                    parts.append(f'<div class="crays-nostr-hub-mini-card" data-card-kind="{esc(kind)}">{card_face}</div>')
            parts.append("</div>")
        if sec.get("videos"):
            parts.append(render_video_grid(sec["videos"]))
        if section_index == midpoint and len(scenes) > 2:
            parts.append(render_stock_scene_strip(item, scenes[2:4]))
    if item["slug"] in SOURCE_SECTION_SLUGS and item.get("sources"):
        parts.append('<h2 id="research-sources">Research sources</h2>')
        parts.append(f'<div class="crays-nostr-source-grid">{render_source_cards(item["sources"])}</div>')
    return "\n".join(parts)


def render_toc(item):
    return "\n".join(
        f'<a href="#{esc(slugify(sec["title"]))}"><span>{idx:02d}</span>{esc(crays_voice(sec["title"]))}</a>'
        for idx, sec in enumerate(item["sections"], start=1)
    )


def render_archive_contents(item):
    current = item["slug"]
    current_key = primary_nav_key(current)
    nav = SECTION_NAVS.get(current_key, SECTION_NAVS["library"])
    theme = visual_theme(item)
    nav_groups = nav["groups"]
    route_cards = []
    for label, key, href, icon, note in PRIMARY_ROUTE_CARDS:
        current_attr = ' aria-current="page"' if key == current_key else ""
        route_cards.append(
            f'<a class="crays-nostr-route-card" data-route="{esc(key)}" href="{esc(href)}"{current_attr}>'
            f'<span aria-hidden="true">{esc(icon)}</span><strong>{esc(crays_voice(label))}</strong><small>{esc(crays_voice(note))}</small></a>'
        )
    group_cards = []
    for group, links in nav_groups:
        links_html = []
        for label, slug in links:
            current_attr = ' aria-current="page"' if slug == current else ""
            links_html.append(f'<a href="{nostr_href(slug)}"{current_attr}>{esc(crays_voice(label))}</a>')
        group_cards.append(
            '<div class="crays-nostr-route-group">'
            f'<strong>{esc(crays_voice(group))}</strong>'
            f'<div>{"".join(links_html)}</div>'
            '</div>'
        )
    route_showcase = render_route_showcase(current_key)
    route_directory = render_route_directory(current_key, current)
    return f"""
      <section class="crays-nostr-route-board" aria-label="Nostr archive navigation" data-nostr-route="{esc(current_key)}">
        <div class="crays-article-reader-shell crays-nostr-route-board__inner">
          <div class="crays-nostr-route-board__top">
            <div class="crays-nostr-route-board__intro">
              <span>{esc(crays_voice(theme["kicker"]))}</span>
              <h2>{esc(crays_voice(nav["title"]))}</h2>
              <p>{esc(crays_voice(nav["deck"]))}</p>
            </div>
            <div class="crays-nostr-archive-finder" role="search">
              <label for="crays-nostr-finder">Search the Nostr atlas</label>
              <input id="crays-nostr-finder" type="search" placeholder="Search apps, NIPs, people, Crays topics" data-nostr-finder-input />
              <div class="crays-nostr-archive-finder__results" data-nostr-finder-results hidden>
                <p class="crays-nostr-archive-finder__status" data-nostr-finder-status>Loading the full atlas index.</p>
                <div class="crays-nostr-archive-finder__list" data-nostr-finder-list role="listbox" aria-label="Nostr atlas search results"></div>
              </div>
            </div>
          </div>
          <nav class="crays-nostr-route-cards" aria-label="Main Nostr routes">
            {"".join(route_cards)}
          </nav>
          <div class="crays-nostr-route-groups">
            {"".join(group_cards)}
          </div>
          {route_showcase}
          {route_directory}
        </div>
      </section>
    """


def archive_area(item):
    slug = item["slug"]
    if slug in {
        "relays",
        "relay-market-directory",
        "nip-42-relay-auth",
        "nip-65-relay-list",
        "field-guide/relay-selection",
        "deep-dives/relay-business-models",
        "deep-dives/outbox-model",
    } or slug in {"nips/nip-11", "nips/nip-50", "nips/nip-66"}:
        return "Relay market", "/nostr/relay-market-directory/"
    if slug.startswith("nips/") or slug.startswith("nip-") or slug == "nips":
        return "Protocol and NIPs", "/nostr/nips/complete-index/"
    if slug.startswith("apps/") or slug in {"apps", "app-profiles", "developer-tools", "clients"}:
        return "Apps and clients", "/nostr/apps/catalog/"
    if slug.startswith("source-inventory") or slug.startswith("awesome-nostr") or slug in {"resources", "videos", "nostr-media-article-video-archive"}:
        return "Research map", "/nostr/source-inventory/"
    if slug.startswith("people") or slug in {"jack-dorsey", "events", "lifestyle-culture", "music-video-media", "nostr-and-bitcoin"}:
        return "People and culture", "/nostr/people/"
    if slug.startswith("deep-dives"):
        return "Deep dives", "/nostr/archive-library/#full-archive-index"
    if slug.startswith("reading-paths"):
        return "Reading paths", "/nostr/archive-library/#reading-paths"
    if slug in {"nostr-and-crays", "content-sale", "awards", "crays-super-node", "operators-venues", "dao-governance"}:
        return "Crays implementation", "/nostr/nostr-and-crays/"
    return "Core concepts", "/nostr/archive-library/"


def primary_nav_key(slug):
    if slug in {"what-is-nostr", "getting-started", "why-nostr", "glossary", "resources", "nostr-media-article-video-archive"} or slug.startswith("reading-paths/"):
        return "start"
    if slug in {
        "privacy-security",
        "search-and-web-of-trust",
        "free-speech-censorship",
        "moderation-discovery",
        "keys-identity",
        "nip-44-encryption",
        "nip-46-remote-signing",
        "nip-98-http-auth",
    } or slug in {
        "deep-dives/nostr-security-threat-model",
        "deep-dives/nostr-spam-and-abuse",
        "deep-dives/web-of-trust-in-practice",
        "deep-dives/nostr-legal-and-compliance",
    }:
        return "privacy"
    if slug in {
        "nostr-and-bitcoin",
        "nip-47-wallet-connect",
        "nip-57-zaps-lightning",
        "apps/alby",
        "apps/safebox",
        "deep-dives/safebox-sovereign-wallet-records",
    } or any(token in slug for token in ("wallet", "zap", "lightning", "cashu", "safebox")):
        return "wallets"
    if slug in {
        "creators",
        "music-video-media",
        "videos",
        "nip-23-long-form",
    } or any(token in slug for token in ("creator", "music", "video", "media", "publishing", "long-form", "photos", "streaming", "blogging")):
        return "media"
    if slug in {
        "content-sale",
        "awards",
        "deep-dives/nostr-for-creators-business",
        "deep-dives/nostr-for-investors",
        "deep-dives/foundups-and-nostr-agent-economy",
    } or any(token in slug for token in ("marketplace", "commerce", "monetization", "investor", "revenue", "foundups")):
        return "commerce"
    if slug in {
        "dao-governance",
        "nip-58-badges",
        "deep-dives/crays-dao-readiness",
        "deep-dives/crays-award-voting",
    } or any(token in slug for token in ("governance", "dao", "badge", "voting", "reputation")):
        return "governance"
    if slug.startswith("deep-dives/") and slug.split("/", 1)[1] in {
        "crays-net-as-nostr-client",
        "crays-world-local-graph",
        "nip-05-for-brands",
        "nostr-seo-and-public-web",
    }:
        return "crays"
    if slug.startswith("people/") or slug in {
        "people",
        "creators",
        "jack-dorsey",
        "lifestyle-culture",
        "events",
        "nostr-vs-mastodon",
    }:
        return "people"
    if slug.startswith("apps/") or slug.startswith("app-profiles/") or slug in {
        "apps",
        "clients",
        "developer-tools",
        "nostr-login",
        "nip-07-signers",
    }:
        return "apps"
    if slug in {
        "relays",
        "relay-market-directory",
        "nip-42-relay-auth",
        "nip-65-relay-list",
        "field-guide/relay-selection",
        "deep-dives/relay-business-models",
        "deep-dives/outbox-model",
    } or slug.startswith("relays/") or slug in {"nips/nip-11", "nips/nip-50", "nips/nip-66"}:
        return "relays"
    if slug.startswith("nips/") or slug.startswith("nip-") or slug in {
        "nips",
        "events-and-kinds",
    }:
        return "nips"
    if slug in {
        "nostr-and-crays",
        "crays-super-node",
        "operators-venues",
    }:
        return "crays"
    return "library"


PRIMARY_ROUTE_CARDS = [
    ("Start", "start", "/nostr/what-is-nostr/", "01", "The clean mental model: keys, clients, relays and why Nostr is useful."),
    ("People", "people", "/nostr/people/", "02", "Builders, creators, funders, events and culture around the protocol."),
    ("Apps", "apps", "/nostr/apps/catalog/", "03", "Crays first, then the wider client, signer, wallet and tool market."),
    ("Relays", "relays", "/nostr/relay-market-directory/", "04", "Live infrastructure: public relays, paid relays, monitoring and venue paths."),
    ("NIPs", "nips", "/nostr/nips/complete-index/", "05", "The standards shelf translated into product consequences."),
    ("Privacy", "privacy", "/nostr/privacy-security/", "06", "Keys, signing, trust, censorship resistance and safer account control."),
    ("Wallets", "wallets", "/nostr/nip-47-wallet-connect/", "07", "Zaps, Lightning, Nostr Wallet Connect, Safebox and sovereign records."),
    ("Media", "media", "/nostr/music-video-media/", "08", "Creators, publishing, music, video, long-form posts and fan access."),
    ("Commerce", "commerce", "/nostr/content-sale/", "09", "Creator sales, marketplaces, FoundUPS, revenue paths and investor context."),
    ("Governance", "governance", "/nostr/dao-governance/", "10", "Badges, voting, reputation, moderation, policy and DAO-ready decisions."),
    ("Crays", "crays", "/nostr/nostr-and-crays/", "11", "How the protocol plugs into Crays, venues, status and governance."),
    ("Library", "library", "/nostr/archive-library/", "12", "The full archive, research database, source map and long-read routes."),
]


try:
    from nostr_learning_depth_pass import apply_learning_depth_pass

    apply_learning_depth_pass(
        PAGES,
        section,
        primary_nav_key,
        GLOBAL_SOURCES,
        NIP_SOURCES,
        RELAY_MARKET_SOURCES,
        BLOSSOM_SOURCES,
        RESOURCE_LINKS,
    )
except Exception as exc:
    print(f"Skipping Nostr learning depth pass: {exc}")


for item in PAGES:
    normalize_page_display_copy(item)


def stock_image(name: str) -> str:
    return f"/assets/stock-lifestyle/{name}"


def free_stock_image(name: str) -> str:
    return f"/assets/nostr-free-stock/{name}"


def nostr_start_image(name: str) -> str:
    return f"/assets/nostr-start/{name}"


ROUTE_HERO_BACKGROUNDS = {
    "start": free_stock_image("start-bg.jpg"),
    "people": free_stock_image("people-bg.jpg"),
    "apps": free_stock_image("apps-bg.jpg"),
    "relays": free_stock_image("relays-bg.jpg"),
    "nips": free_stock_image("nips-bg.jpg"),
    "privacy": free_stock_image("nips-bg.jpg"),
    "wallets": free_stock_image("apps-bg.jpg"),
    "media": free_stock_image("people-bg.jpg"),
    "commerce": free_stock_image("crays-bg.jpg"),
    "governance": free_stock_image("nips-bg.jpg"),
    "crays": free_stock_image("crays-bg.jpg"),
    "library": free_stock_image("library-bg.jpg"),
}


ROUTE_LIFESTYLE_HEROES = {
    "start": free_stock_image("start-visual.jpg"),
    "people": free_stock_image("people-visual.jpg"),
    "apps": free_stock_image("apps-visual.jpg"),
    "relays": free_stock_image("relays-visual.jpg"),
    "nips": free_stock_image("nips-visual.jpg"),
    "privacy": free_stock_image("nips-visual.jpg"),
    "wallets": free_stock_image("apps-visual.jpg"),
    "media": free_stock_image("people-visual.jpg"),
    "commerce": free_stock_image("crays-visual.jpg"),
    "governance": free_stock_image("nips-visual.jpg"),
    "crays": free_stock_image("crays-visual.jpg"),
    "library": free_stock_image("library-visual.jpg"),
}


START_PAGE_VISUALS = {
    "what-is-nostr": {
        "hero_background": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Nostr protocol stack overview for the first mental model.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Nostr community and event culture in a real room.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "The first Nostr map: identity, content, interactions and payments.", "position": "center"},
            {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Nostr becomes easier when the protocol is connected to people and events.", "position": "center"},
            {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Bitcoin media helped carry Nostr into a broader public conversation.", "position": "center"},
            {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Nostr and Bitcoin meet where identity, attention and value flow connect.", "position": "center"},
        ],
    },
    "getting-started": {
        "hero_background": {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Getting started with Nostr, Bitcoin and app-based onboarding.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "A practical stack view before choosing clients, keys and relays.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Start with the account, the key and the first safe client.", "position": "center"},
            {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "The onboarding path becomes clear when the layers are visible.", "position": "center"},
        ],
    },
    "why-nostr": {
        "hero_background": {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Nostr in the public Bitcoin media conversation.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-purple-mark.jfif"), "caption": "The Nostr mark as a shorthand for portable identity.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Why Nostr matters is easier to see once media, money and identity meet.", "position": "center"},
            {"url": nostr_start_image("nostr-purple-mark.jfif"), "caption": "The protocol gives users a name that can move across clients.", "position": "center"},
        ],
    },
    "glossary": {
        "hero_background": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Glossary terms mapped to protocol layers.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-purple-mark.jfif"), "caption": "A clear Nostr visual anchor for vocabulary.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Terms are easier when they sit inside a simple stack.", "position": "center"},
            {"url": nostr_start_image("nostr-purple-mark.jfif"), "caption": "Nostr vocabulary should help the reader, not slow them down.", "position": "center"},
        ],
    },
    "resources": {
        "hero_background": {"url": nostr_start_image("munstr-thumbnail.webp"), "caption": "Nostr source map and community archive material.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Resources connect documentation, events and public media.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("munstr-thumbnail.webp"), "caption": "The resource shelf keeps external references close to the learning path.", "position": "center"},
            {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Events and media sources show the human side of the archive.", "position": "center"},
        ],
    },
    "videos": {
        "hero_background": {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Nostr video and media trail.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Video material belongs where it helps readers see the scene.", "position": "center"},
    },
    "nostr-media-article-video-archive": {
        "hero_background": {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Nostr articles, media coverage and video source archive.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Nostr media, event and creator material in one Start shelf.", "position": "center"},
        "scenes": [
            {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Media articles help readers understand Nostr beyond the feed.", "position": "center"},
            {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Event material turns the protocol into a living scene.", "position": "center"},
            {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Technical sources keep media claims tied to protocol reality.", "position": "center"},
            {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Bitcoin, zaps and wallet videos connect social context to value flow.", "position": "center"},
        ],
    },
    "reading-paths/beginner": {
        "hero_background": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Beginner path through the Nostr scene.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "A beginner route through keys, clients and relays.", "position": "center"},
    },
    "reading-paths/developer": {
        "hero_background": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Developer route through Nostr protocol layers.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Developer learning connects protocol, apps and value flow.", "position": "center"},
    },
    "reading-paths/creator": {
        "hero_background": {"url": nostr_start_image("bitcoin-backstage-nostr.jpg"), "caption": "Creator route through Nostr media and Bitcoin culture.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Creators need audience, media and real community context.", "position": "center"},
    },
    "reading-paths/operator": {
        "hero_background": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Operator route through relays, payments and infrastructure.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("buy-bitcoin-with-nostr.png"), "caption": "Operators need Nostr to connect identity with payment flows.", "position": "center"},
    },
    "reading-paths/culture": {
        "hero_background": {"url": nostr_start_image("nostr-lounge-las-vegas.jpg"), "caption": "Culture route through events, people and public media.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("munstr-thumbnail.webp"), "caption": "Culture gives the protocol memory and humor without losing the point.", "position": "center"},
    },
    "reading-paths/research": {
        "hero_background": {"url": nostr_start_image("nostr-protocol-stack.jpeg"), "caption": "Research route through source maps and protocol references.", "position": "center"},
        "hero_visual": {"url": nostr_start_image("munstr-thumbnail.webp"), "caption": "Research shelves connect sources, articles and event archives.", "position": "center"},
    },
}


STOCK_SCENE_POOLS = {
    "start": [
        ("Portable identity should feel like walking into the room with your own name.", stock_image("crays-association-19-digital-members-working-across-the-crays-lifestyle-network.webp")),
        ("A social graph is useful only when real people can actually use it.", stock_image("crays-home-14-members-working-together-inside-a-lifestyle-lounge.webp")),
        ("Nostr becomes easier when the first door looks like daily life, not a server diagram.", stock_image("crays-tech-nostr-lifestyle-stock-20260508.jpg")),
        ("The app is just the surface. The community is the point.", stock_image("crays-home-08-lifestyle-guests-using-the-crays-circle-app.webp")),
        ("We read open protocol through people, rooms, access and culture.", stock_image("crays-lifestyle-15-crays-circle-app-and-digital-community-product.webp")),
        ("The useful version of sovereignty sits at the table with the reader.", stock_image("crays-contact-office-lounge-business-team.jpg")),
    ],
    "people": [
        ("Nostr is a room full of builders, creators, operators and loud opinions.", stock_image("crays-lifestyle-18-creators-founders-and-fans-meeting-through-crays-community.webp")),
        ("The culture layer matters because products do not spread by protocol alone.", stock_image("crays-lifestyle-13-music-film-fashion-art-and-media-inside-the-crays-lifestyle-community.webp")),
        ("Events turn usernames into a scene people can remember.", stock_image("crays-franchise-04-event-and-nightlife-energy-in-a-crays-style-venue.webp")),
        ("The best builder map feels closer to a dinner table than a corporate org chart.", stock_image("crays-lifestyle-02-crays-builders-and-guests-sharing-dinner.webp")),
        ("Creators and fans are not an appendix. They are where the network gets heat.", stock_image("crays-hospitality-16-creators-and-guests-building-a-community-moment.webp")),
        ("A living people archive needs faces, rooms and context.", stock_image("crays-team-04-crays-community-and-lifestyle-moment.webp")),
    ],
    "apps": [
        ("Clients are where the protocol finally becomes something you can hold.", stock_image("crays-home-project-circle-app-digital-community-lifestyle.jpg")),
        ("The best Nostr apps feel less like infrastructure and more like your digital life.", stock_image("crays-finance-data-mobile-demand.jpg")),
        ("Product quality is the difference between a clever idea and a daily habit.", stock_image("crays-finance-tools-hero-dashboard.jpg")),
        ("Signers, wallets and publishing tools need a surface humans trust.", stock_image("crays-hospitality-seo-circle-app-community-interface.jpg")),
        ("Builders win when protocol detail disappears into clean product behavior.", stock_image("crays-tech-04-team-collaborating-on-a-crays-digital-community-product-interface.webp")),
        ("The app route belongs close to dashboards, phones and real operating context.", stock_image("crays-contact-investor-platform-dashboard-digital-network.jpg")),
    ],
    "relays": [
        ("Relays are where the network actually lives, moves and remembers.", stock_image("crays-association-21-crays-venue-layer-with-digital-coordination-and-community-access.webp")),
        ("We read relay infrastructure as local presence, not abstract hosting.", stock_image("crays-tech-03-guests-inside-a-blue-lit-local-venue-environment-representing-mesh-network.webp")),
        ("Venue relays make more sense when you picture rooms, guests and service flow.", stock_image("crays-hospitality-header-premium-lounge-bar.webp")),
        ("A relay market is still a people market: trust, uptime, geography and use case.", stock_image("crays-finance-data-city-lounge.jpg")),
        ("The Super Node idea belongs where hospitality and infrastructure meet.", stock_image("crays-finance-fintech-supernodes-city.jpg")),
        ("Local mesh turns the protocol into something a venue can operate.", stock_image("crays-hospitality-video-poster-venue-mesh-demo.jpg")),
    ],
    "nips": [
        ("Standards are boring only until they save the room from chaos.", stock_image("crays-association-03-crays-operating-and-governance-team-in-a-focused-meeting.webp")),
        ("A good protocol rule is a quiet agreement that lets everyone keep building.", stock_image("crays-association-08-the-system-stays-credible-when-decisions-are-documented-and-account.webp")),
        ("NIPs need to feel like shared operating rules, not sacred paperwork.", stock_image("crays-home-association-partners-governance-meeting.jpg")),
        ("The protocol shelf works when a reader can see the decision path.", stock_image("crays-finance-data-team-planning.jpg")),
        ("Common standards let independent products act like one larger culture.", stock_image("crays-team-extended-20-community-standards.jpeg")),
        ("Technical trust still needs diligence, review and a clear table.", stock_image("crays-team-extended-22-due-diligence.jpeg")),
    ],
    "crays": [
        ("We turn protocol into places, access, status and real demand.", stock_image("crays-home-project-crays-club-premium-hotel-lounge.jpg")),
        ("Our layer starts where digital identity meets hospitality.", stock_image("crays-hospitality-10-premium-crays-club-hotel-lounge-for-work-meetings-and-community.webp")),
        ("Payments, venues and social proof should feel like one experience.", stock_image("crays-finance-tools-venue-payments.jpg")),
        ("We are lifestyle infrastructure with a protocol spine.", stock_image("crays-home-project-crays-hospitality-venue-dinner.jpg")),
        ("Creators, guests and operators become part of the same demand network.", stock_image("crays-hospitality-16-creators-and-guests-building-a-community-moment.webp")),
        ("The culture layer becomes stronger when venues can carry it.", stock_image("crays-lifestyle-17-crays-rooftop-culture-and-event-community.webp")),
    ],
    "library": [
        ("A big archive only works when every shelf has a clear next door.", stock_image("crays-association-22-crays-project-and-partner-discussion-connected-to-the-governance-la.webp")),
        ("Research feels better when it looks like a working table, not a storage unit.", stock_image("crays-finance-intro-association-team.jpg")),
        ("The library is the map readers use when curiosity gets serious.", stock_image("crays-hospitality-ref-travel-map.jpg")),
        ("Deep content needs routes, scenes and memory hooks.", stock_image("crays-new-projects-07-crays-builders-and-partners-planning-a-project-in-a-lounge.webp")),
        ("The full archive should feel organized enough to browse for hours.", stock_image("crays-team-collage-partner-roundtable-lounge.jpg")),
        ("Every branch of the atlas should still feel connected to real work.", stock_image("crays-team-collage-coworking-studio.jpg")),
    ],
    "payments": [
        ("Bitcoin and Lightning make more sense when value moves in real places.", stock_image("crays-finance-fintech-wallet-balcony.jpg")),
        ("Payments belong close to cafés, venues, creators and everyday decisions.", stock_image("crays-finance-fintech-pos-cafe.jpg")),
        ("A wallet is only useful when it fits the rhythm of the day.", stock_image("crays-finance-tools-wallets-mobile.jpg")),
        ("Value flow is a product feeling, not just a settlement diagram.", stock_image("crays-finance-value-transaction.jpg")),
        ("Revenue tools need enough clarity that creators can trust the numbers.", stock_image("crays-finance-monetization-digital-finance-dashboard.jpg")),
        ("Mobile demand is where protocol becomes spending power.", stock_image("crays-finance-data-mobile-demand.jpg")),
    ],
    "creator": [
        ("Creator commerce should feel direct, warm and owned by the person publishing.", stock_image("crays-finance-use-creators.jpg")),
        ("Nostr culture travels through music, media, creators and scenes.", stock_image("crays-lifestyle-13-music-film-fashion-art-and-media-inside-the-crays-lifestyle-community.webp")),
        ("Content becomes stronger when fans can pay, prove access and stay portable.", stock_image("crays-home-project-tribe-award-cultural-event.jpg")),
        ("Creator profiles should feel like a living room for work, taste and value.", stock_image("crays-home-project-circle-app-digital-community-lifestyle.jpg")),
        ("Creators bring the protocol into public culture.", stock_image("crays-lifestyle-18-creators-founders-and-fans-meeting-through-crays-community.webp")),
        ("The monetization layer should keep the human in the center.", stock_image("crays-hospitality-16-creators-and-guests-building-a-community-moment.webp")),
    ],
    "privacy": [
        ("Self-custody is a lifestyle promise only when people can understand it.", stock_image("crays-founder-prologue-sovereign-tech.webp")),
        ("Security needs calm product design, not fear as a brand voice.", stock_image("crays-tech-hero-intent-blackboard-doorway.jpg")),
        ("Trust is built through visible rules and sober decisions.", stock_image("crays-team-extended-04-web3-legal.jpeg")),
        ("Privacy should protect the person while still letting useful services work.", stock_image("crays-association-08-the-system-stays-credible-when-decisions-are-documented-and-account.webp")),
        ("The clean version of freedom tech feels practical, local and clear.", stock_image("crays-tech-digital-asset-community-network.jpg")),
        ("Good safety design gives the reader control without killing the vibe.", stock_image("crays-team-executive-04-legal-governance.jpg")),
    ],
}


STOCK_SCENE_POOLS["wallets"] = STOCK_SCENE_POOLS["payments"]
STOCK_SCENE_POOLS["media"] = STOCK_SCENE_POOLS["creator"]
STOCK_SCENE_POOLS["commerce"] = STOCK_SCENE_POOLS["payments"] + STOCK_SCENE_POOLS["creator"]
STOCK_SCENE_POOLS["governance"] = STOCK_SCENE_POOLS["nips"] + STOCK_SCENE_POOLS["privacy"]


OPENVERSE_ALLOWED_QUERIES = {
    "start": {"technology laptop", "computer network", "open source software", "internet protocol", "cryptography", "developer desk", "web technology"},
    "people": {"conference speaker", "software developer portrait", "community meetup", "hackathon people", "creator studio", "team collaboration", "public event audience", "workshop people"},
    "apps": {"mobile app", "smartphone app", "user interface", "phone screen", "software dashboard", "web design", "mobile technology", "app development"},
    "relays": {"server room", "data center", "network cable", "router network", "internet infrastructure", "computer servers", "fiber optic", "network switch"},
    "nips": {"technical documentation", "software architecture", "whiteboard planning", "developer documentation", "code review", "engineering notes", "project planning", "technical standard"},
    "crays": {"hospitality lounge", "hotel lobby", "business lounge", "event venue", "restaurant interior", "premium lounge", "city rooftop", "community event venue"},
    "library": {"library research", "bookshelf", "archive documents", "reading room", "map research", "notebook desk", "research table", "books archive"},
    "payments": {"bitcoin", "mobile payment", "payment terminal", "cash register", "digital wallet", "point of sale", "finance app", "payment phone"},
    "creator": {"music studio", "podcast studio", "photography camera", "artist studio", "content creator", "video production", "creative workspace", "media studio"},
    "privacy": {"cybersecurity", "privacy laptop", "secure technology", "lock computer", "encryption", "password"},
    "wallets": {"bitcoin", "mobile payment", "payment terminal", "digital wallet", "point of sale", "finance app", "payment phone"},
    "media": {"music studio", "podcast studio", "photography camera", "artist studio", "content creator", "video production", "creative workspace", "media studio"},
    "commerce": {"mobile payment", "payment terminal", "finance app", "business meeting", "marketplace", "creator studio"},
    "governance": {"technical documentation", "whiteboard planning", "code review", "project planning", "meeting room", "policy document"},
}


OPENVERSE_BAD_TERMS = {
    "antique",
    "army",
    "artwork",
    "afghan",
    "baseball",
    "bay",
    "beach",
    "beer",
    "bird",
    "boat",
    "calligraphy",
    "cat",
    "cocktail",
    "cocktails",
    "dog",
    "drink",
    "drinks",
    "engraving",
    "festival",
    "flower",
    "food",
    "football",
    "fruit",
    "garden",
    "heliograph",
    "horse",
    "infantry",
    "lemon",
    "lime",
    "lunch",
    "luncheon",
    "meal",
    "michelangelo",
    "military",
    "mountain",
    "museum",
    "naval",
    "navy",
    "ocean",
    "orange",
    "painting",
    "parade",
    "sculpture",
    "sea",
    "shell",
    "soldier",
    "squadron",
    "sports",
    "statue",
    "strike",
    "tourism",
    "tourist",
    "vacation",
    "waterfall",
    "wedding",
    "wine",
    "wooden",
    "yacht",
    "yeomanry",
    "yoga",
}


OPENVERSE_PREFERRED_SOURCES = {"stocksnap", "rawpixel", "wordpress"}


CORE_ROUTE_HERO_SLUGS = {
    "what-is-nostr": "start",
    "people": "people",
    "apps/catalog": "apps",
    "relay-market-directory": "relays",
    "nips/complete-index": "nips",
    "privacy-security": "privacy",
    "nip-47-wallet-connect": "wallets",
    "music-video-media": "media",
    "content-sale": "commerce",
    "dao-governance": "governance",
    "nostr-and-crays": "crays",
    "archive-library": "library",
}


VISUAL_THEMES = {
    "start": {
        "kicker": "Start route",
        "label": "The clean Nostr door",
        "note": "Keys, relays, clients and why any of this matters.",
        "image": ROUTE_LIFESTYLE_HEROES["start"],
        "background": ROUTE_HERO_BACKGROUNDS["start"],
        "pins": [("Keys", "keys-identity"), ("Clients", "clients"), ("Relays", "relays")],
    },
    "people": {
        "kicker": "Culture route",
        "label": "People, proof and scene energy",
        "note": "The builders, creators, events and social gravity around Nostr.",
        "image": ROUTE_LIFESTYLE_HEROES["people"],
        "background": ROUTE_HERO_BACKGROUNDS["people"],
        "pins": [("Creators", "creators"), ("Events", "events"), ("Music", "music-video-media")],
    },
    "apps": {
        "kicker": "App route",
        "label": "The product layer",
        "note": "Clients, signers, publishing tools, wallets and weird useful experiments.",
        "image": ROUTE_LIFESTYLE_HEROES["apps"],
        "background": ROUTE_HERO_BACKGROUNDS["apps"],
        "pins": [("Catalog", "apps/catalog"), ("Signers", "nip-07-signers"), ("Login", "nostr-login")],
    },
    "relays": {
        "kicker": "Relay route",
        "label": "The live infrastructure market",
        "note": "Public, paid, search, community, monitoring and venue relays.",
        "image": ROUTE_LIFESTYLE_HEROES["relays"],
        "background": ROUTE_HERO_BACKGROUNDS["relays"],
        "pins": [("Market map", "relay-market-directory"), ("Relays", "relays"), ("NIP-66", "nips/nip-66")],
    },
    "nips": {
        "kicker": "Protocol route",
        "label": "Under the hood",
        "note": "Events, NIPs, relay behavior and the shared formats apps can trust.",
        "image": ROUTE_LIFESTYLE_HEROES["nips"],
        "background": ROUTE_HERO_BACKGROUNDS["nips"],
        "pins": [("NIP index", "nips/complete-index"), ("Events", "events-and-kinds"), ("Relays", "relays")],
    },
    "privacy": {
        "kicker": "Privacy route",
        "label": "Keys, trust and control",
        "note": "Safer signing, censorship resistance, identity, moderation and web-of-trust context.",
        "image": ROUTE_LIFESTYLE_HEROES["privacy"],
        "background": ROUTE_HERO_BACKGROUNDS["privacy"],
        "pins": [("Keys", "keys-identity"), ("Security", "privacy-security"), ("Trust", "search-and-web-of-trust")],
    },
    "wallets": {
        "kicker": "Wallet route",
        "label": "Value flow you can carry",
        "note": "Zaps, Lightning, wallet connect, Safebox and sovereign records.",
        "image": ROUTE_LIFESTYLE_HEROES["wallets"],
        "background": ROUTE_HERO_BACKGROUNDS["wallets"],
        "pins": [("NWC", "nip-47-wallet-connect"), ("Zaps", "nip-57-zaps-lightning"), ("Safebox", "apps/safebox")],
    },
    "media": {
        "kicker": "Media route",
        "label": "Creators, publishing and fans",
        "note": "Music, video, long-form posts, publishing tools and portable creator relationships.",
        "image": ROUTE_LIFESTYLE_HEROES["media"],
        "background": ROUTE_HERO_BACKGROUNDS["media"],
        "pins": [("Creators", "creators"), ("Music", "music-video-media"), ("Long-form", "nip-23-long-form")],
    },
    "commerce": {
        "kicker": "Commerce route",
        "label": "Revenue, markets and agents",
        "note": "Creator sales, marketplaces, FoundUPS, investor context and economic routes.",
        "image": ROUTE_LIFESTYLE_HEROES["commerce"],
        "background": ROUTE_HERO_BACKGROUNDS["commerce"],
        "pins": [("Content sale", "content-sale"), ("FoundUPS", "apps/foundups-agent"), ("Investors", "deep-dives/nostr-for-investors")],
    },
    "governance": {
        "kicker": "Governance route",
        "label": "Rules people can inspect",
        "note": "Badges, voting, reputation, moderation, DAO readiness and policy edges.",
        "image": ROUTE_LIFESTYLE_HEROES["governance"],
        "background": ROUTE_HERO_BACKGROUNDS["governance"],
        "pins": [("DAO", "dao-governance"), ("Badges", "nip-58-badges"), ("Voting", "deep-dives/crays-award-voting")],
    },
    "crays": {
        "kicker": "Crays route",
        "label": "Protocol into real life",
        "note": "Profiles, venues, creator commerce, awards, Super Nodes and DAO readiness.",
        "image": ROUTE_LIFESTYLE_HEROES["crays"],
        "background": ROUTE_HERO_BACKGROUNDS["crays"],
        "pins": [("Crays.net", "deep-dives/crays-net-as-nostr-client"), ("Venues", "operators-venues"), ("DAO", "dao-governance")],
    },
    "library": {
        "kicker": "Library route",
        "label": "The full atlas",
        "note": "A searchable shelf for long reads, references, maps and rabbit holes.",
        "image": ROUTE_LIFESTYLE_HEROES["library"],
        "background": ROUTE_HERO_BACKGROUNDS["library"],
        "pins": [("Archive", "archive-library"), ("Research", "source-inventory"), ("Deep dives", "deep-dives/portable-social-graph")],
    },
}


def visual_theme(item):
    slug = item["slug"]
    key = primary_nav_key(slug)
    if any(token in slug for token in ("zap", "wallet", "lightning", "badge", "status")):
        theme = dict(VISUAL_THEMES.get(key, VISUAL_THEMES["library"]))
        theme["image"] = STOCK_SCENE_POOLS["payments"][0][1]
        theme["background"] = ROUTE_HERO_BACKGROUNDS.get(key, ROUTE_HERO_BACKGROUNDS["library"])
        return theme
    if slug.startswith("field-guide/") and any(token in slug for token in ("venue", "bar", "club", "local", "operator")):
        theme = dict(VISUAL_THEMES["crays"])
        theme["image"] = STOCK_SCENE_POOLS["relays"][0][1]
        theme["background"] = ROUTE_HERO_BACKGROUNDS["crays"]
        return theme
    return VISUAL_THEMES.get(key, VISUAL_THEMES["library"])


def stock_scene_pool_keys(item) -> list[str]:
    slug = item["slug"]
    primary = primary_nav_key(slug)
    text = " ".join([
        slug,
        item["title"],
        item.get("tag", ""),
        " ".join(item.get("keywords", [])),
    ]).lower()
    keys: list[str] = [primary]
    if "safebox" in text:
        keys.extend(["privacy", "payments", "apps"])
    if "foundups" in text or "agent" in text:
        keys.extend(["apps", "library", "creator"])
    if any(token in text for token in ("zap", "wallet", "lightning", "bitcoin", "payment", "monetization", "finance", "paid", "commerce")):
        keys.append("payments")
    if any(token in text for token in ("creator", "music", "media", "video", "content", "award", "fan", "culture")):
        keys.append("creator")
    if any(token in text for token in ("privacy", "security", "censorship", "moderation", "trust", "legal", "compliance", "keys", "identity")):
        keys.append("privacy")
    keys.append("library")
    deduped: list[str] = []
    for key in keys:
        if key in STOCK_SCENE_POOLS and key not in deduped:
            deduped.append(key)
    return deduped


def load_openverse_image_bank() -> list[dict]:
    if not OPENVERSE_IMAGE_BANK.exists():
        return []
    try:
        records = json.loads(OPENVERSE_IMAGE_BANK.read_text(encoding="utf-8")).get("images", [])
    except Exception:
        return []
    clean_records: list[dict] = []
    seen_urls: set[str] = set()
    for record in records:
        url = str(record.get("url") or record.get("thumbnail") or "").strip()
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        item = dict(record)
        item["url"] = url
        item["keys"] = [key for key in item.get("keys", []) if key in STOCK_SCENE_POOLS]
        clean_records.append(item)
    return clean_records


def openverse_words(record: dict) -> set[str]:
    raw = " ".join([
        str(record.get("title", "")),
        str(record.get("creator", "")),
        str(record.get("foreign_landing_url", "")),
    ]).lower()
    return set(re.sub(r"[^a-z0-9]+", " ", raw).split())


def openverse_record_usable_for_key(record: dict, key: str) -> bool:
    if openverse_words(record) & OPENVERSE_BAD_TERMS:
        return False
    if str(record.get("source") or "").lower() not in OPENVERSE_PREFERRED_SOURCES:
        return False
    allowed = OPENVERSE_ALLOWED_QUERIES.get(key, set())
    if allowed and not allowed.intersection(set(record.get("queries", []))):
        return False
    return True


def openverse_record_url(record: dict, slot: str) -> str:
    if slot == "scene":
        return str(record.get("thumbnail") or record.get("url") or "").strip()
    return str(record.get("url") or record.get("thumbnail") or "").strip()


def openverse_keys_for_item(item) -> list[str]:
    slug = item["slug"]
    text = " ".join([
        slug,
        item["title"],
        item.get("deck", ""),
        item.get("tag", ""),
        " ".join(item.get("keywords", [])),
    ]).lower()
    keys = stock_scene_pool_keys(item)
    primary = primary_nav_key(slug)
    if primary == "library":
        keys.extend(["library", "nips", "start"])
    if primary == "apps":
        keys.extend(["apps", "start"])
    if primary == "people":
        keys.extend(["people", "creator"])
    if primary == "relays":
        keys.extend(["relays", "start"])
    if primary == "privacy":
        keys.extend(["privacy", "nips", "start"])
    if primary == "wallets":
        keys.extend(["wallets", "payments", "apps"])
    if primary == "media":
        keys.extend(["media", "creator", "people"])
    if primary == "commerce":
        keys.extend(["commerce", "payments", "creator"])
    if primary == "governance":
        keys.extend(["governance", "nips", "privacy"])
    if primary == "crays":
        keys.extend(["crays", "people", "creator"])
    if "source-inventory" in slug or "research" in text or "database" in text:
        keys.extend(["library", "nips", "start"])
    if any(token in text for token in ("signer", "key", "identity", "login", "security", "privacy", "auth")):
        keys.append("privacy")
    if any(token in text for token in ("wallet", "zap", "bitcoin", "lightning", "payment", "cashu")):
        keys.append("payments")
    if any(token in text for token in ("music", "video", "media", "creator", "content", "publishing", "long-form")):
        keys.append("creator")
    keys.append("library")
    deduped: list[str] = []
    for key in keys:
        if key in STOCK_SCENE_POOLS and key not in deduped:
            deduped.append(key)
    return deduped


def openverse_caption(item, key: str, slot: str, index: int = 0) -> str:
    title = item["title"]
    route_copy = {
        "start": "a clean first-contact scene for the Nostr basics",
        "people": "a people-and-builder scene for the Nostr culture layer",
        "apps": "a product-life scene for Nostr clients and tools",
        "relays": "an infrastructure scene for relays and network routing",
        "nips": "a planning-and-standards scene for protocol work",
        "privacy": "a security scene for keys, signing and trust",
        "wallets": "a value-flow scene for zaps, wallets and records",
        "media": "a creator-media scene for publishing and fans",
        "commerce": "a market scene for creator sales and agent economies",
        "governance": "a governance scene for voting, badges and policy",
        "crays": "a hospitality-and-community scene for the Crays layer",
        "library": "a research-and-archive scene for the Nostr atlas",
        "payments": "a value-flow scene for Bitcoin, Lightning and zaps",
        "creator": "a creator-work scene for publishing and fan access",
        "privacy": "a security scene for keys, trust and safer signing",
    }
    phrase = route_copy.get(key, "a Nostr research scene")
    if slot == "hero_background":
        return f"{title}: {phrase}."
    if slot == "hero_visual":
        return f"{title}: a focused visual for this route."
    return f"{title}: {phrase}."


def openverse_position(item, slot: str) -> str:
    key = primary_nav_key(item["slug"])
    text = " ".join([item["slug"], item["title"], item.get("tag", "")]).lower()
    if slot == "hero_background":
        if key in {"people", "apps", "media", "commerce", "crays"} or any(token in text for token in ("people", "creator", "profile", "app")):
            return "center 38%"
        if key == "relays":
            return "center 52%"
        return "center"
    if key in {"people", "apps", "media", "commerce", "crays"} or any(token in text for token in ("people", "creator", "profile", "app")):
        return "center 34%"
    return "center"


def build_openverse_visual_assignments(pages: list[dict]) -> dict[str, dict]:
    images = load_openverse_image_bank()
    if not images:
        return {}
    by_key: dict[str, list[dict]] = {key: [] for key in STOCK_SCENE_POOLS}
    for record in images:
        for key in record.get("keys", []):
            if openverse_record_usable_for_key(record, key):
                by_key.setdefault(key, []).append(record)
    fallback = sorted(
        [
            record
            for record in images
            if not (openverse_words(record) & OPENVERSE_BAD_TERMS)
            and str(record.get("source") or "").lower() in OPENVERSE_PREFERRED_SOURCES
        ],
        key=lambda record: (record.get("title", "").lower(), record.get("id", "")),
    )
    used_ids: set[str] = set()
    cursors: dict[str, int] = {key: 0 for key in by_key}
    fallback_cursor = 0
    pages_sorted = sorted(pages, key=lambda item: item["slug"])
    minimum_slots = len(pages_sorted) * 3
    extra_scene_pages = max(0, min(len(pages_sorted), len(fallback) - minimum_slots))
    assignments: dict[str, dict] = {}

    def pick_from_keys(keys: list[str], slot: str, allow_global_fallback: bool = True) -> dict | None:
        nonlocal fallback_cursor
        for key in keys:
            pool = by_key.get(key, [])
            if not pool:
                continue
            start = cursors.get(key, 0)
            for attempt in range(len(pool)):
                idx = (start + attempt) % len(pool)
                record = pool[idx]
                record_id = str(record.get("id") or openverse_record_url(record, slot))
                if record_id and record_id not in used_ids and openverse_record_url(record, slot):
                    cursors[key] = idx + 1
                    used_ids.add(record_id)
                    return record
            cursors[key] = start + len(pool)
        if not allow_global_fallback:
            return None
        for attempt in range(len(fallback)):
            idx = (fallback_cursor + attempt) % len(fallback)
            record = fallback[idx]
            record_id = str(record.get("id") or openverse_record_url(record, slot))
            if record_id and record_id not in used_ids and openverse_record_url(record, slot):
                fallback_cursor = idx + 1
                used_ids.add(record_id)
                return record
        return None

    pages_sorted = sorted(
        pages_sorted,
        key=lambda item: (0 if item["slug"] in CORE_ROUTE_HERO_SLUGS else 1, item["slug"]),
    )

    for page_index, item in enumerate(pages_sorted):
        keys = openverse_keys_for_item(item)
        primary = primary_nav_key(item["slug"])
        hero_key = CORE_ROUTE_HERO_SLUGS.get(item["slug"], primary)
        if item["slug"] in CORE_ROUTE_HERO_SLUGS:
            background = {"keys": [hero_key], "url": ROUTE_HERO_BACKGROUNDS[hero_key]}
            hero_visual = {"keys": [hero_key], "url": ROUTE_LIFESTYLE_HEROES[hero_key]}
        else:
            background = pick_from_keys([hero_key] + [key for key in keys if key != hero_key], "hero_background")
            hero_visual = pick_from_keys([hero_key] + [key for key in keys if key != hero_key], "hero_visual")
        scenes = []
        scene_count = 4
        for scene_index in range(scene_count):
            scene_record = pick_from_keys(keys, "scene", allow_global_fallback=False)
            if scene_record:
                scene_key = next((key for key in keys if key in scene_record.get("keys", [])), keys[0])
                scenes.append({
                    "url": openverse_record_url(scene_record, "scene"),
                    "caption": openverse_caption(item, scene_key, "scene", scene_index),
                    "position": openverse_position(item, "scene"),
                })
        if background and hero_visual:
            background_key = next((key for key in [hero_key] + keys if key in background.get("keys", [])), hero_key)
            visual_key = next((key for key in [hero_key] + keys if key in hero_visual.get("keys", [])), hero_key)
            hero_background_url = openverse_record_url(background, "hero_background")
            hero_visual_url = openverse_record_url(hero_visual, "hero_visual")
            assignments[item["slug"]] = {
                "hero_background": {
                    "url": hero_background_url,
                    "caption": openverse_caption(item, background_key, "hero_background"),
                    "position": openverse_position(item, "hero_background"),
                },
                "hero_visual": {
                    "url": hero_visual_url,
                    "caption": openverse_caption(item, visual_key, "hero_visual"),
                    "position": openverse_position(item, "hero_visual"),
                },
                "scenes": scenes,
            }
    return assignments


OPENVERSE_VISUAL_ASSIGNMENTS = build_openverse_visual_assignments(PAGES)


def page_visuals(item) -> dict:
    override = START_PAGE_VISUALS.get(item["slug"], {})
    if override:
        base = OPENVERSE_VISUAL_ASSIGNMENTS.get(item["slug"], {})
        return {**base, **override}
    return OPENVERSE_VISUAL_ASSIGNMENTS.get(item["slug"], {})


def pick_stock_scenes(item, count: int = 4) -> list[tuple[str, str]]:
    visuals = page_visuals(item)
    scenes: list[tuple[str, str]] = []
    seen_scene_sources: set[str] = set()
    if visuals.get("scenes"):
        for scene in visuals["scenes"]:
            image = str(scene.get("url") or "").strip()
            if image and image not in seen_scene_sources:
                scenes.append((scene["caption"], image))
                seen_scene_sources.add(image)
            if len(scenes) >= count:
                return scenes
    pool: list[tuple[str, str]] = []
    theme = visual_theme(item)
    excluded_sources = {theme.get("image", ""), theme.get("background", "")}
    seen_sources: set[str] = set(excluded_sources) | seen_scene_sources
    for key in stock_scene_pool_keys(item):
        for caption, image in STOCK_SCENE_POOLS[key]:
            if image not in seen_sources:
                pool.append((caption, image))
                seen_sources.add(image)
    if not pool:
        return scenes
    offset = sum((idx + 1) * ord(char) for idx, char in enumerate(item["slug"])) % len(pool)
    ordered = pool[offset:] + pool[:offset]
    scenes.extend(ordered[: max(0, count - len(scenes))])
    if len(scenes) < count:
        scenes.extend(pool[: count - len(scenes)])
    return scenes


def render_stock_scene_strip(item, scenes: list[tuple[str, str]] | None = None) -> str:
    if scenes is None:
        scenes = pick_stock_scenes(item)
    if not scenes:
        return ""
    figures = []
    for caption, image in scenes:
        caption = crays_voice(caption)
        figures.append(
            f'<figure><img src="{esc(image)}" alt="{esc(caption)}" loading="lazy" decoding="async" referrerpolicy="no-referrer" />'
            f'<figcaption>{esc(caption)}</figcaption></figure>'
        )
    return f"""
        <div class="crays-nostr-stock-scenes" data-count="{len(scenes)}" aria-label="Nostr image context">
          {"".join(figures)}
        </div>
    """


def render_hero_visual(item):
    theme = visual_theme(item)
    visuals = page_visuals(item)
    visual = visuals.get("hero_visual", {})
    hero_image = visual.get("url") or theme["image"]
    hero_alt = crays_voice(visual.get("caption") or f"{item['title']} visual")
    hero_position = visual.get("position") or theme.get("image_position") or openverse_position(item, "hero_visual")
    hero_badge = ""
    hero_badge_url = card_visual_url(item["title"], item["slug"])
    if hero_badge_url and primary_nav_key(item["slug"]) in {"apps", "people", "relays"}:
        hero_badge = f'<div class="crays-nostr-hero-avatar"><img src="{esc(hero_badge_url)}" alt="{esc(item["title"])} icon" loading="eager" decoding="async" /></div>'
    pins = "\n".join(
        f'<a href="{nostr_href(slug)}">{esc(crays_voice(label))}</a>'
        for label, slug in theme["pins"]
    )
    return f"""
            <div class="crays-nostr-hero-visual" style="--nostr-hero-visual-position: {esc(hero_position)};">
              <figure>
                <img src="{esc(hero_image)}" alt="{esc(hero_alt)}" loading="eager" decoding="async" referrerpolicy="no-referrer" />
              </figure>
              {hero_badge}
              <div class="crays-nostr-hero-signal">
                <span>Route</span>
                <strong>{esc(crays_voice(theme["label"]))}</strong>
                <small>{esc(crays_voice(theme["note"]))}</small>
              </div>
              <div class="crays-nostr-hero-pins">
                {pins}
              </div>
            </div>
    """


def normalize_nostr_slug(href=None) -> str:
    if not href:
        return ""
    slug = str(href).strip()
    if slug.startswith(BASE_URL):
        slug = slug[len(BASE_URL) :]
    if slug.startswith("/nostr/"):
        slug = slug[len("/nostr/") :]
    elif slug.startswith("nostr/"):
        slug = slug[len("nostr/") :]
    slug = slug.split("#", 1)[0].split("?", 1)[0].strip("/")
    return slug


def card_visual_url(title, href=None) -> str:
    slug = normalize_nostr_slug(href)
    title_key = slugify(clean_copy(title))
    href_text = str(href or "")
    if title_key in {"crays", "crays-net", "craysnet"} or "crays.net" in href_text:
        return "/assets/brand/crays-mark.svg"
    if slug in PERSON_IMAGE_BY_SLUG:
        return PERSON_IMAGE_BY_SLUG[slug]
    if title_key in PERSON_IMAGE_BY_TITLE:
        return PERSON_IMAGE_BY_TITLE[title_key]
    if href and str(href).startswith(("http://", "https://")):
        external_icon = favicon_url(str(href))
        if external_icon:
            return external_icon
    if slug == "apps/catalog":
        return "/assets/brand/crays-mark.svg"
    app_slug = ""
    if slug.startswith("apps/catalog/"):
        app_slug = slug.rsplit("/", 1)[-1]
    elif slug.startswith("apps/"):
        candidate = slug.rsplit("/", 1)[-1]
        if not candidate.startswith("category-"):
            app_slug = candidate
    elif slug.startswith("app-profiles/"):
        app_slug = slug.rsplit("/", 1)[-1]
    if app_slug and app_slug in APP_ICON_BY_SLUG:
        return APP_ICON_BY_SLUG[app_slug]
    if title_key in APP_ICON_BY_TITLE:
        return APP_ICON_BY_TITLE[title_key]
    relay_icons = {
        "relay-market-directory": favicon_url("nostr.watch"),
        "relays": favicon_url("nostr.co.uk"),
        "awesome-nostr/relays": favicon_url("nostrlist.com"),
        "field-guide/relay-selection": favicon_url("bigbrotr.com"),
        "deep-dives/relay-business-models": favicon_url("relay.tools"),
        "deep-dives/outbox-model": favicon_url("nostr.how"),
    }
    return relay_icons.get(slug, "")


def mini_card_kind(title, href=None):
    text = f"{title} {href or ''}".lower()
    slug = normalize_nostr_slug(href)
    if slug.startswith("people/") or slugify(clean_copy(title)) in PERSON_IMAGE_BY_TITLE:
        return "people"
    if "/nostr/apps/" in text or "app" in text or "client" in text:
        return "app"
    if "nip-" in text or "protocol" in text or "relay" in text or "event" in text:
        return "protocol"
    if "crays" in text or "venue" in text or "dao" in text or "content sale" in text:
        return "crays"
    if "people" in text or "creator" in text or "music" in text or "culture" in text:
        return "people"
    return "topic"


def mini_card_icon(title, href=None):
    text = clean_copy(title)
    nip_match = re.search(r"NIP-?(\d+)", text, flags=re.IGNORECASE)
    if nip_match:
        return nip_match.group(1)[:2]
    kind = mini_card_kind(text, href)
    if kind == "protocol":
        return "N"
    if kind == "crays":
        return "C"
    if kind == "people":
        return "P"
    words = re.findall(r"[A-Za-z0-9]+", text)
    if not words:
        return "N"
    if len(words) == 1:
        return words[0][:2].upper()
    return "".join(word[0] for word in words[:2]).upper()


def render_card_badge(title, href=None):
    visual = card_visual_url(title, href)
    kind = mini_card_kind(title, href)
    if visual:
        return f'<img class="crays-nostr-card-media" data-card-kind="{esc(kind)}" src="{esc(visual)}" alt="{esc(clean_copy(title))} icon" loading="lazy" decoding="async" />'
    return f'<span class="crays-nostr-card-icon" aria-hidden="true">{esc(mini_card_icon(title, href))}</span>'


def render_route_showcase(current_key: str) -> str:
    if current_key == "apps":
        items = [
            ("Crays", "https://www.crays.net"),
            ("Damus", "apps/damus"),
            ("Amethyst", "apps/amethyst"),
            ("Primal", "apps/primal"),
            ("Coracle", "apps/coracle"),
            ("Iris", "apps/iris"),
            ("noStrudel", "apps/nostrudel"),
            ("YakiHonne", "apps/yakihonne"),
            ("Alby", "apps/alby"),
        ]
    elif current_key == "people":
        items = [
            ("Enoch Root", "people/enoch-root"),
            ("fiatjaf", "people/fiatjaf"),
            ("William Casarin", "people/william-casarin-jb55"),
            ("Vitor Pamplona", "people/vitor-pamplona"),
            ("PabloF7z", "people/pablof7z"),
            ("Hodlbod", "people/hodlbod"),
            ("Yuki Kishimoto", "people/yuki-kishimoto"),
            ("Mike Dilger", "people/mike-dilger"),
            ("Alex Gleason", "people/alex-gleason"),
            ("Jack Dorsey", "people/jack-dorsey"),
            ("ODELL", NOSTRIGA_SOURCE_URL),
            ("Ben Arc", NOSTRIGA_SOURCE_URL),
            ("Vanessa", NOSTRIGA_SOURCE_URL),
            ("Terry Yiu", NOSTRIGA_SOURCE_URL),
            ("Derek Ross", NOSTRIGA_SOURCE_URL),
            ("Karnage", NOSTRIGA_SOURCE_URL),
            ("OpenMike", NOSTRIGA_SOURCE_URL),
        ]
    elif current_key == "relays":
        items = [
            ("Nostr.watch", "relay-market-directory"),
            ("BigBrotr", "relay-market-directory"),
            ("Nostr.co.uk", "relays"),
            ("NostrList", "relay-market-directory"),
            ("Nostr.band", "relay-market-directory"),
            ("NIP-66", "nips/nip-66"),
        ]
    else:
        return ""
    chips = []
    for title, slug in items:
        image = card_visual_url(title, slug)
        if current_key == "apps" and title == "Crays":
            image = "/assets/brand/crays-mark.svg"
        if current_key == "relays" and title == "BigBrotr":
            image = favicon_url("bigbrotr.com")
        if current_key == "relays" and title == "Nostr.watch":
            image = favicon_url("nostr.watch")
        if current_key == "relays" and title == "NostrList":
            image = favicon_url("nostrlist.com")
        if current_key == "relays" and title == "Nostr.band":
            image = favicon_url("relay.nostr.band")
        badge = (
            f'<img src="{esc(image)}" alt="{esc(title)} icon" loading="lazy" decoding="async" />'
            if image else
            f'<span>{esc(mini_card_icon(title, slug))}</span>'
        )
        href = slug if str(slug).startswith(("http://", "https://")) else nostr_href(slug)
        chips.append(
            f'<a href="{esc(href)}">{badge}<strong>{esc(title)}</strong></a>'
        )
    return f"""
          <div class="crays-nostr-visual-rail" aria-label="{esc(ROUTE_LABELS.get(current_key, "Nostr"))} visual shortcuts">
            {"".join(chips)}
          </div>
    """


def atlas_group_label(item) -> str:
    slug = item["slug"]
    if slug.startswith("apps/catalog/"):
        return "App catalog entries"
    if slug.startswith("apps/category-"):
        return "App categories"
    if slug.startswith("apps/") or slug.startswith("app-profiles/"):
        return "App profiles"
    if slug.startswith("people/"):
        return "Builder profiles"
    if slug.startswith("nips/"):
        return "NIP reference pages"
    if slug.startswith("nip-"):
        return "NIP explainer pages"
    if slug.startswith("deep-dives/"):
        return "Deep dives"
    if slug.startswith("reading-paths/"):
        return "Reading paths"
    if slug.startswith("source-inventory/"):
        return "Source inventory"
    if slug.startswith("awesome-nostr/"):
        return "Awesome Nostr branches"
    if slug.startswith("field-guide/"):
        return "Field guides"
    key = primary_nav_key(slug)
    labels = {
        "start": "Core concepts",
        "people": "Culture and media",
        "apps": "App orientation",
        "relays": "Relay map",
        "nips": "Protocol orientation",
        "privacy": "Privacy and trust",
        "wallets": "Wallets and value flow",
        "media": "Media and creators",
        "commerce": "Commerce and markets",
        "governance": "Governance and reputation",
        "crays": "Crays product layer",
        "library": "Research and library",
    }
    return labels.get(key, "Archive pages")


def render_route_directory(current_key: str, current_slug: str) -> str:
    pages = sorted(
        [p for p in PAGES if primary_nav_key(p["slug"]) == current_key],
        key=lambda page_item: (atlas_group_label(page_item), page_item["title"].lower()),
    )
    if not pages:
        return ""
    label = ROUTE_LABELS.get(current_key, current_key.title())
    shelves: dict[str, list[dict]] = {}
    for page_item in pages:
        shelves.setdefault(atlas_group_label(page_item), []).append(page_item)
    shelf_parts = []
    for shelf_label in sorted(shelves):
        link_parts = []
        for page_item in shelves[shelf_label]:
            current_attr = ' aria-current="page"' if page_item["slug"] == current_slug else ""
            link_parts.append(f'<a href="{nostr_href(page_item["slug"])}"{current_attr}>{esc(crays_voice(page_item["title"]))}</a>')
        links = "\n".join(link_parts)
        shelf_parts.append(
            f'<section class="crays-nostr-route-directory__shelf"><h3>{esc(crays_voice(shelf_label))}</h3><div>{links}</div></section>'
        )
    shelf_labels = sorted(shelves)
    shelf_preview = ", ".join(shelf_labels[:3])
    if len(shelf_labels) > 3:
        shelf_preview += f" and {len(shelf_labels) - 3} more shelves"
    return f"""
          <details class="crays-nostr-route-directory" data-route="{esc(current_key)}">
            <summary>
              <span class="crays-nostr-route-directory__eyebrow">{esc(crays_voice(label))}</span>
              <strong>All {esc(crays_voice(label))} pages</strong>
              <small><b>{len(pages)} pages in this route</b><em>{esc(shelf_preview)}</em></small>
              <span class="crays-nostr-route-directory__action"><span data-open-label>Browse pages</span><span data-close-label>Close shelf</span></span>
            </summary>
            <div class="crays-nostr-route-directory__shelves">
              {"".join(shelf_parts)}
            </div>
          </details>
    """


def render_full_atlas(current_slug: str) -> str:
    current_key = primary_nav_key(current_slug)
    route_lookup = {key: (label, number, note) for label, key, _href, number, note in PRIMARY_ROUTE_CARDS}
    route_chunks: list[str] = []
    for _label, key, _href, _number, _note in PRIMARY_ROUTE_CARDS:
        pages = [p for p in PAGES if primary_nav_key(p["slug"]) == key]
        if not pages:
            continue
        shelves: dict[str, list[dict]] = {}
        for page_item in pages:
            shelves.setdefault(atlas_group_label(page_item), []).append(page_item)
        shelf_parts = []
        for shelf_label in sorted(shelves):
            link_parts = []
            for p in sorted(shelves[shelf_label], key=lambda page_item: page_item["title"].lower()):
                current_attr = ' aria-current="page"' if p["slug"] == current_slug else ""
                link_parts.append(f'<a href="{nostr_href(p["slug"])}"{current_attr}>{esc(p["title"])}</a>')
            links = "\n".join(link_parts)
            shelf_parts.append(
                f'<section class="crays-nostr-atlas-shelf"><h3>{esc(shelf_label)}</h3><div>{links}</div></section>'
            )
        label, number, note = route_lookup.get(key, (key.title(), "", ""))
        image = VISUAL_THEMES.get(key, VISUAL_THEMES["library"])["image"]
        open_attr = " open" if key == current_key else ""
        route_chunks.append(
            f'<details class="crays-nostr-atlas-route" data-route="{esc(key)}"{open_attr}>'
            f'<summary><span>{esc(number)}</span><img class="crays-nostr-atlas-thumb" src="{esc(image)}" alt="{esc(label)} route thumbnail" loading="lazy" decoding="async" />'
            f'<strong>{esc(label)}<em>{esc(note)}</em></strong><small>{len(pages)} pages</small></summary>'
            f'<div class="crays-nostr-atlas-shelves">{"".join(shelf_parts)}</div>'
            '</details>'
        )
    return f"""
          <details class="crays-nostr-global-atlas" id="full-nostr-atlas">
            <summary><span aria-hidden="true">A-Z</span><strong>Full Nostr Atlas</strong><small>{len(PAGES)} pages, every route, every shelf</small></summary>
            <div class="crays-nostr-atlas-routes">
              {"".join(route_chunks)}
            </div>
          </details>
    """


def plain_search_copy(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return crays_voice(text)


def search_terms_for_item(item: dict) -> str:
    pieces: list[str] = [
        item.get("title", ""),
        item.get("slug", "").replace("/", " ").replace("-", " "),
        item.get("tag", ""),
        item.get("deck", ""),
        ROUTE_LABELS.get(primary_nav_key(item["slug"]), ""),
        atlas_group_label(item),
        archive_area(item)[0],
        " ".join(item.get("keywords", [])),
    ]
    for section in item.get("sections", []):
        pieces.append(section.get("title", ""))
        pieces.append(section.get("body", ""))
        pieces.extend(section.get("paragraphs", []))
        for bullet in section.get("bullets", []):
            pieces.extend(list(bullet[:2]))
        for card in section.get("cards", []):
            pieces.extend(list(card[:2]))
            if len(card) > 2:
                pieces.append(card[2])
        for video in section.get("videos", []):
            pieces.extend([
                video.get("title", ""),
                video.get("channel", ""),
                video.get("category", ""),
                video.get("use", ""),
                video.get("note", ""),
                video.get("id", ""),
                video.get("url", ""),
            ])
    for label, url, note in item.get("sources", []):
        pieces.extend([label, url, note])
    return plain_search_copy(" ".join(str(part) for part in pieces if part))


def build_search_record(item: dict) -> dict:
    route = ROUTE_LABELS.get(primary_nav_key(item["slug"]), "Library")
    return {
        "title": plain_search_copy(item.get("title", "")),
        "url": nostr_href(item["slug"]),
        "slug": item["slug"],
        "category": route,
        "shelf": atlas_group_label(item),
        "deck": plain_search_copy(item.get("deck", ""))[:260],
        "terms": search_terms_for_item(item),
    }


def write_search_index() -> None:
    records = sorted(
        (build_search_record(item) for item in PAGES),
        key=lambda record: (record["category"], record["shelf"], record["title"].lower(), record["url"]),
    )
    SEARCH_INDEX.parent.mkdir(parents=True, exist_ok=True)
    SEARCH_INDEX.write_text(
        json.dumps(
            {
                "generated": TODAY,
                "count": len(records),
                "pages": records,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )


def render_primary_nav(item):
    current = primary_nav_key(item["slug"])
    links = []
    for label, key, href, _number, _note in PRIMARY_ROUTE_CARDS:
        current_attr = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{href}" data-route="{esc(key)}"{current_attr}>{esc(label)}</a>')
    return "\n        ".join(links)


def render_related(item, by_slug):
    rel = [slug for slug in item["related"] if slug in by_slug]
    if not rel:
        rel = [p["slug"] for p in PAGES[:6] if p["slug"] != item["slug"]]
    link_parts = []
    for slug in rel[:18]:
        title = by_slug[slug]["title"]
        area, _href = archive_area(by_slug[slug])
        link_parts.append(
            f'<a href="{nostr_href(slug)}">'
            f'{render_card_badge(title, slug)}'
            f'<strong>{esc(title)}</strong>'
            f'<small>{esc(area)}</small>'
            '</a>'
        )
    links = "\n".join(link_parts)
    heading = item.get("related_label") or f"Read next from {item['title']}"
    return f"""
            <div class="crays-nostr-related">
              <h2>{esc(crays_voice(heading))}</h2>
              <div class="crays-nostr-related__links">
                {links}
              </div>
            </div>
    """


def render_article_masthead(item):
    route = ROUTE_LABELS.get(primary_nav_key(item["slug"]), "Nostr")
    read = item.get("read", "")
    meta = "".join(
        f"<span>{esc(value)}</span>"
        for value in (route, read, item.get("tag", "Nostr archive"))
        if value
    )
    return "\n".join(
        [
            '            <header class="crays-nostr-article-masthead">',
            f'              <div class="crays-nostr-article-masthead__meta">{meta}</div>',
            f'              <h2 class="crays-nostr-article-masthead__title">{esc(crays_voice(item["title"]))}</h2>',
            f'              <p class="crays-nostr-article-masthead__deck">{esc(crays_voice(item["deck"]))}</p>',
            "            </header>",
        ]
    )


def render_archive_index():
    shelves = []
    shelf_labels = [
        ("start", "Start here"),
        ("people", "People and culture"),
        ("apps", "Apps and clients"),
        ("relays", "Relay market and infrastructure"),
        ("nips", "Protocol and NIPs"),
        ("privacy", "Privacy, keys and trust"),
        ("wallets", "Wallets, zaps and records"),
        ("media", "Media, creators and publishing"),
        ("commerce", "Commerce, markets and agents"),
        ("governance", "Governance and reputation"),
        ("crays", "Crays implementation"),
        ("library", "Library, research and deep dives"),
    ]
    for key, label in shelf_labels:
        pages = [p for p in PAGES if primary_nav_key(p["slug"]) == key]
        if not pages:
            continue
        links = "\n".join(
            f'<a href="{nostr_href(p["slug"])}" data-nostr-index-link><span>{esc(mini_card_icon(p["title"], p["slug"]))}</span>{esc(p["title"])}</a>'
            for p in pages
        )
        shelves.append(
            f'<section class="crays-nostr-index-shelf" data-nostr-index-section>'
            f'<h3>{esc(label)}</h3>'
            f'<div>{links}</div>'
            f'</section>'
        )
    return "\n".join(shelves)


def render_crays_footer() -> str:
    social_links = [
        ("GitHub", "https://github.com/CraysCircle", "/assets/footer-icons/github.svg"),
        ("X", "https://x.com/CraysCircle", "/assets/footer-icons/x.svg"),
        ("Open Collective", "https://opencollective.com/crays", "/assets/footer-icons/opencollective.svg"),
        ("Reddit", "https://www.reddit.com/r/Crays/", "/assets/footer-icons/reddit.svg"),
        ("Telegram", "https://t.me/craysclub", "/assets/footer-icons/telegram.svg"),
        ("YouTube", "https://www.youtube.com/@CraysCircle", "/assets/footer-icons/youtube.svg"),
        ("LinkedIn", "https://www.linkedin.com/company/crays/", "/assets/footer-icons/linkedin.svg"),
        ("Instagram", "https://www.instagram.com/crays_circle/", "/assets/footer-icons/instagram.svg"),
        ("Nostr", "https://www.crays.net", "/assets/footer-icons/nostr.webp"),
        ("Discord", "https://discord.gg/dpYZk8xAvR", "/assets/footer-icons/discord.svg"),
    ]
    social = "".join(
        f'<a href="{esc(href)}" aria-label="{esc(label)}" target="_blank" rel="noreferrer noopener">'
        f'<img src="{esc(icon)}" alt="{esc(label)}" width="20" height="20" loading="lazy"></a>'
        for label, href, icon in social_links
    )
    return f"""
  <footer class="legal-footer crays-nostr-footer" aria-label="Crays footer">
    <div class="legal-footer-inner">
      <div class="legal-footer-top">
        <div>
          <a class="legal-footer-logo-link" href="/" aria-label="Crays Home">
            <img class="legal-footer-logo" src="/assets/brand/crays-logo.svg" alt="Crays" width="138" height="34" loading="lazy">
          </a>
          <p class="legal-footer-tagline">Luxury, Lifestyle, Wealth and Innovation</p>
        </div>
        <div class="legal-footer-social" aria-label="Social links">{social}</div>
      </div>
      <div class="legal-footer-bottom">
        <nav class="legal-footer-links" aria-label="Legal pages">
          <a href="/legal/imprint/">Imprint</a>
          <a href="/legal/terms-conditions/">Terms and Conditions</a>
          <a href="/legal/data-protection/">Data Protection</a>
          <a href="/legal/privacy-policy/">Privacy Policy</a>
          <a href="/blog/">Blog</a>
        </nav>
        <div class="legal-footer-copy">2026 Copyright &copy; and Trademark&trade; by CRAYS</div>
        <span class="crays-consent-footer-slot">
          <button class="crays-consent-footer-button" type="button" data-crays-consent-open="true">Cookie Settings</button>
        </span>
      </div>
    </div>
    <section class="crays-consent-panel" data-crays-consent-panel="true" aria-label="Cookie consent" hidden="hidden">
      <p class="crays-consent-kicker">Cookie Consent</p>
      <h2 class="crays-consent-title">Privacy &amp; Cookie Settings</h2>
      <p class="crays-consent-copy">We use strictly necessary cookies to run this website. With your consent, we may also use preferences, analytics and marketing technologies to improve the site and measure campaigns.</p>
      <div class="crays-consent-actions">
        <button class="crays-consent-button crays-consent-button-reject" type="button" data-crays-consent-close="rejected">Reject optional</button>
        <button class="crays-consent-button crays-consent-button-text" type="button" data-crays-consent-open="true">Privacy &amp; Cookie Settings</button>
        <button class="crays-consent-button crays-consent-button-primary" type="button" data-crays-consent-close="accepted">Accept all</button>
      </div>
      <div class="crays-consent-links">
        <a href="/legal/privacy-policy/">Privacy Policy</a>
        <a href="/legal/data-protection/">Data Protection</a>
      </div>
    </section>
    <script>(function () {{
      var panel = document.querySelector('[data-crays-consent-panel]');
      if (!panel) return;
      var storageKey = 'crays-cookie-consent';
      function openPanel() {{
        panel.hidden = false;
        panel.classList.add('is-open');
      }}
      function closePanel(value) {{
        if (value) {{
          try {{ window.localStorage.setItem(storageKey, value); }} catch (error) {{}}
        }}
        panel.classList.remove('is-open');
        panel.hidden = true;
      }}
      document.querySelectorAll('[data-crays-consent-open]').forEach(function (button) {{
        button.addEventListener('click', openPanel);
      }});
      panel.querySelectorAll('[data-crays-consent-close]').forEach(function (button) {{
        button.addEventListener('click', function () {{ closePanel(button.getAttribute('data-crays-consent-close')); }});
      }});
    }}());</script>
  </footer>
    """


def render_page(item, by_slug):
    title = f"{item['title']} | Crays Nostr Archive"
    desc = crays_voice(item["deck"])
    canonical = f"{BASE_URL}/nostr/{item['slug']}/"
    theme = visual_theme(item)
    visuals = page_visuals(item)
    background = visuals.get("hero_background", {})
    hero_background = background.get("url") or theme.get("background", theme["image"])
    hero_background_position = background.get("position") or theme.get("background_position") or openverse_position(item, "hero_background")
    toc = render_toc(item)
    archive_contents = render_archive_contents(item)
    hero_visual = render_hero_visual(item)
    primary_nav = render_primary_nav(item)
    keywords = ", ".join(["Nostr", "Crays", "open social protocol"] + item["keywords"])
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "mainEntityOfPage": canonical,
        "headline": item["title"],
        "description": desc,
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "Crays Business Nomads Association"},
        "publisher": {"@type": "Organization", "name": "Crays.org", "url": BASE_URL},
        "about": ["Nostr", "Nostr protocol", "Crays", "Bitcoin", "Lightning", "open social protocol"],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Crays", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Nostr", "item": f"{BASE_URL}/nostr/"},
            {"@type": "ListItem", "position": 3, "name": item["title"], "item": canonical},
        ],
    }
    archive_index = render_archive_index() if item["slug"] == "archive-library" else ""
    full_atlas = render_full_atlas(item["slug"]) if item["slug"] == "archive-library" else ""
    structured_links = []
    seen_structured_urls = set()
    for label, _key, href, _number, _note in PRIMARY_ROUTE_CARDS:
        url = f"{BASE_URL}{href}"
        if url not in seen_structured_urls:
            seen_structured_urls.add(url)
            structured_links.append({"name": label, "url": url})
    for related_slug in item.get("related", [])[:12]:
        related_slug = str(related_slug).strip("/").removeprefix("nostr/")
        related = by_slug.get(related_slug)
        if not related:
            continue
        url = f"{BASE_URL}/nostr/{related['slug']}/"
        if url not in seen_structured_urls:
            seen_structured_urls.add(url)
            structured_links.append({"name": related["title"], "url": url})
    archive_block = ""
    if archive_index:
        archive_block = f"""
            <div class="crays-nostr-related">
              <h2 id="full-archive-index">The full Nostr library</h2>
              <div class="crays-nostr-index-tools">
                <label for="crays-nostr-archive-filter">Search the library shelf</label>
                <input id="crays-nostr-archive-filter" type="search" placeholder="Search NIPs, apps, people, Crays topics" data-nostr-index-filter />
              </div>
              <div class="crays-nostr-archive-index" data-nostr-index>
                {archive_index}
              </div>
              <div class="crays-nostr-library-atlas">
                {full_atlas}
              </div>
            </div>
        """
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="keywords" content="{esc(keywords)}" />
  <meta name="theme-color" content="#040b12" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:site_name" content="Crays.org" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{esc(canonical)}" />
  <meta name="twitter:card" content="summary" />
  <link rel="canonical" href="{esc(canonical)}" />
  <link rel="sitemap" type="application/xml" href="/sitemap.xml" />
  <link rel="icon" href="/assets/brand/crays-mark.svg?v=crays-favicon-2" sizes="any" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/crays-blog-article.css?v=20260530-nostr-archive-v1" />
  <link rel="stylesheet" href="/assets/css/crays-nostr-hub.css?v=20260601-nostr-learning-gate-v1" />
  <script type="application/ld+json">{json.dumps(article, separators=(",", ":"))}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb, separators=(",", ":"))}</script>
  <script type="application/ld+json">{json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Crays Nostr archive navigation",
        "itemListElement": [
            {"@type": "ListItem", "position": idx + 1, "name": link["name"], "url": link["url"]}
            for idx, link in enumerate(structured_links)
        ],
    }, separators=(",", ":"))}</script>
</head>
<body class="crays-article-body crays-nostr-hub-body crays-nostr-area-{esc(primary_nav_key(item["slug"]))}">
  <header class="crays-article-header">
    <div class="crays-article-shell crays-article-header__inner">
      <a class="crays-article-logo" href="/nostr/" aria-label="Crays Nostr home"><img src="/assets/brand/crays-home-logo.webp" alt="Crays" width="264" height="102"></a>
      <nav class="crays-article-site-nav" aria-label="Nostr archive pages">
        {primary_nav}
      </nav>
      <div class="crays-article-header-actions" aria-label="Crays actions">
        <a class="crays-article-header-cta" href="/en/join-us/">Join us</a>
        <a class="crays-article-header-language" href="/en/" aria-label="Crays English home">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9.25" stroke="currentColor" stroke-width="1.5"></circle>
            <path d="M2.75 12h18.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path>
            <path d="M12 2.75c2.7 2.52 4.25 5.69 4.25 9.25S14.7 18.73 12 21.25C9.3 18.73 7.75 15.56 7.75 12S9.3 5.27 12 2.75Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"></path>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main>
    <article>
      <section class="crays-article-hero crays-nostr-hub-hero" style="--nostr-hero-bg: url({esc(hero_background)}); --nostr-hero-bg-position: {esc(hero_background_position)};">
        <div class="crays-article-shell crays-article-hero__grid">
          <div class="crays-article-hero__copy">
            <p class="crays-article-eyebrow">{esc(item["tag"])}</p>
            <h1>{esc(item["title"])}</h1>
            <p class="crays-article-deck">{esc(desc)}</p>
          </div>
          {hero_visual}
        </div>
      </section>

      {archive_contents}

      <section class="crays-article-main">
        <div class="crays-article-reader-shell crays-article-layout">
          <aside class="crays-article-toc" aria-label="In this article">
            <p>In this article</p>
            {toc}
          </aside>

          <div class="crays-article-content">
            {render_article_masthead(item)}
            {render_sections(item)}

            {render_related(item, by_slug)}
            {archive_block}
            <div class="crays-article-end">
              <a href="/nostr/">Back to the Crays Nostr page</a>
            </div>
          </div>
        </div>
      </section>
    </article>
  </main>

  {render_crays_footer()}
<script src="/assets/js/crays-nostr-atlas-search.js?v=20260601-real-atlas-search-v1" defer></script>
</body>
</html>
"""


def write_pages():
    by_slug = {p["slug"]: p for p in PAGES}
    write_search_index()
    for item in PAGES:
        target = PUBLIC / "nostr" / item["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(clean_generated_html(ensure_external_links_new_tab(render_page(item, by_slug))), encoding="utf-8")


def update_existing_nostr_pages():
    files = [PUBLIC / "nostr" / "index.html"] + [PUBLIC / lang / "nostr" / "index.html" for lang in ["en", "de", "es", "ca", "fr", "pt", "it"]]
    internal_links = (
        '<a href="/nostr/archive-library/">Nostr library</a>'
        '<a href="/nostr/what-is-nostr/">Nostr archive</a>'
        '<a href="/nostr/getting-started/">Getting started</a>'
        '<a href="/nostr/nips/">NIPs guide</a>'
        '<a href="/nostr/apps/">Apps</a>'
        '<a href="/nostr/lifestyle-culture/">Lifestyle</a>'
        '<a href="/nostr/people/">People</a>'
        '<a href="/nostr/nostr-and-crays/">Nostr and Crays</a>'
    )
    marker = '<div class="crays-nostr-source-row" aria-label="Nostr and Crays ecosystem resources">\n        '
    for path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace('href="#crays-franchise-system">Understand Nostr</a>', 'href="/nostr/what-is-nostr/">Understand Nostr</a>')
        text = text.replace('href="https://www.awesome-nostr.com/"', 'href="https://github.com/aljazceru/awesome-nostr"')
        if marker in text and '<a href="/nostr/what-is-nostr/">Nostr archive</a>' not in text:
            text = text.replace(marker, marker + internal_links, 1)
        if '<a href="/nostr/what-is-nostr/">Nostr archive</a>' in text and '<a href="/nostr/archive-library/">Nostr library</a>' not in text:
            text = text.replace(
                '<a href="/nostr/what-is-nostr/">Nostr archive</a>',
                '<a href="/nostr/archive-library/">Nostr library</a><a href="/nostr/what-is-nostr/">Nostr archive</a>',
                1,
            )
        if '<a href="/nostr/lifestyle-culture/">Lifestyle</a><a href="/nostr/nostr-and-crays/">Nostr and Crays</a>' in text:
            text = text.replace(
                '<a href="/nostr/lifestyle-culture/">Lifestyle</a><a href="/nostr/nostr-and-crays/">Nostr and Crays</a>',
                '<a href="/nostr/lifestyle-culture/">Lifestyle</a><a href="/nostr/people/">People</a><a href="/nostr/nostr-and-crays/">Nostr and Crays</a>',
            )
        text = re.sub(r'<a\b(?=[^>]*href="https://www\.tiktok\.com/@thorbenbiesenbac1")[^>]*>.*?</a>', "", text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"\bFor Crays,\s*", "For us, ", text)
        text = re.sub(r"\bfor Crays\b", "for us", text)
        text = re.sub(r"\bCrays can\b", "we can", text)
        text = re.sub(r"\bCrays connects\b", "we connect", text)
        text = re.sub(r"\bCrays uses\b", "we use", text)
        text = re.sub(r"\bCrays offers\b", "we offer", text)
        text = re.sub(r"\bCrays provides\b", "we provide", text)
        text = re.sub(r"\bCrays explains\b", "we explain", text)
        text = re.sub(r"\bCrays does not\b", "we do not", text)
        text = re.sub(r"\bCrays gives\b", "we get", text)
        text = re.sub(r"\bCrays is\b", "we are", text)
        text = re.sub(r"\bCrays needs\b", "we need", text)
        text = re.sub(r"\bCrays runs on\b", "we run on", text)
        text = re.sub(r"\bCrays runs\b", "we run", text)
        text = re.sub(r"\bCrays turns\b", "we turn", text)
        text = re.sub(r"\bCrays builds\b", "we build", text)
        text = re.sub(r"\bCrays adds\b", "we add", text)
        text = re.sub(r"\bCrays wants\b", "we want", text)
        text = re.sub(r"\bNostr gives Crays\b", "Nostr gives us", text)
        text = re.sub(r"\bNostr lets Crays\b", "Nostr lets us", text)
        text = re.sub(r"(?<!www\.)\bCrays\.net\b", "Crays", text, flags=re.IGNORECASE)
        text = ensure_external_links_new_tab(text)
        path.write_text(clean_generated_html(text), encoding="utf-8")


def update_sitemap():
    sitemap = PUBLIC / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    text = re.sub(
        r"\n  <url>\s*<loc>" + re.escape(BASE_URL) + r"/nostr/[^<]+</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    entries = []
    for item in PAGES:
        priority = "0.88" if item["slug"] in {"what-is-nostr", "nips", "resources", "nostr-and-crays"} else "0.82"
        entries.append(
            f"""  <url>
    <loc>{BASE_URL}/nostr/{item['slug']}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    text = text.replace("\n</urlset>", "\n" + "\n".join(entries) + "\n</urlset>")
    sitemap.write_text(clean_generated_html(text), encoding="utf-8")


def main():
    write_pages()
    update_existing_nostr_pages()
    update_sitemap()
    print(f"Generated {len(PAGES)} Nostr archive pages.")


if __name__ == "__main__":
    main()
