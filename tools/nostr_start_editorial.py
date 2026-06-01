from __future__ import annotations


def _source_lookup(*source_groups):
    lookup = {}
    all_sources = []
    for group in source_groups:
        for source in group:
            all_sources.append(source)
            lookup.setdefault(source[0], source)
    return lookup, all_sources


def apply_start_page_rewrites(
    pages: list[dict],
    section,
    global_sources: list[tuple[str, str, str]],
    nip_sources: list[tuple[str, str, str]],
    resource_links: list[tuple[str, str, str]],
    relay_sources: list[tuple[str, str, str]],
    blossom_sources: list[tuple[str, str, str]],
) -> None:
    source_by_name, all_sources = _source_lookup(
        global_sources,
        nip_sources,
        resource_links,
        relay_sources,
        blossom_sources,
    )

    def src(*names: str):
        return [source_by_name[name] for name in names if name in source_by_name]

    primary_nip_index = [
        ("Nostr NIPs repository", "https://github.com/nostr-protocol/nips", "The primary index for Nostr Implementation Possibilities, event kinds and relay/client message types."),
        ("NIP-01", "https://github.com/nostr-protocol/nips/blob/master/01.md", "The mandatory base flow: events, signatures, filters and client-relay messages."),
        ("NIP-05", "https://github.com/nostr-protocol/nips/blob/master/05.md", "DNS-based public key identifiers that make keys easier to recognize."),
        ("NIP-07", "https://github.com/nostr-protocol/nips/blob/master/07.md", "Browser signer interface so web clients can request signatures without taking a private key."),
        ("NIP-19", "https://github.com/nostr-protocol/nips/blob/master/19.md", "Human-facing bech32 formats such as npub, nsec, note, nevent and naddr."),
        ("NIP-47", "https://github.com/nostr-protocol/nips/blob/master/47.md", "Nostr Wallet Connect for remote Lightning wallet access."),
        ("NIP-57", "https://github.com/nostr-protocol/nips/blob/master/57.md", "Lightning zap requests and receipts attached to Nostr events."),
        ("NIP-65", "https://github.com/nostr-protocol/nips/blob/master/65.md", "Relay list metadata for read and write relay discovery."),
        ("NIP-96", "https://github.com/nostr-protocol/nips/blob/master/96.md", "HTTP file storage integration, now marked unrecommended in favor of Blossom."),
    ]
    research_sources = [
        ("Nostr.how protocol guide", "https://nostr.how/en/the-protocol", "Plain-language explanation of clients, relays, events, keys and NIPs."),
        ("Nostr Developer Guide", "https://nostrcg.github.io/devguide/", "Developer orientation for the protocol, libraries, relays and first app work."),
        ("Empirical Nostr relay analysis", "https://arxiv.org/html/2402.05709v2", "Large-scale study of Nostr decentralization, relay availability and replication overhead."),
        ("The Power of Nostr", "https://www.lynalden.com/the-power-of-nostr/", "Long-form explanation of why portable keys and open clients matter."),
        ("nostr-tools", "https://github.com/nbd-wtf/nostr-tools", "Lower-level JavaScript tooling for developing Nostr clients."),
        ("NDK", "https://github.com/nostr-dev-kit/ndk", "Nostr Development Kit with signer adapters, relay discovery, caching and NIP-65 support."),
        ("strfry", "https://github.com/hoytech/strfry", "High-performance Nostr relay implementation using local LMDB storage."),
        ("Khatru", "https://github.com/fiatjaf/khatru", "Framework for building custom Nostr relays and relay policies."),
        ("Blossom", "https://github.com/hzrd149/blossom", "HTTP blob storage specification that uses Nostr keys and sha256-addressed files."),
    ]

    common_core_sources = src("Nostr protocol repository", "nostr.how", "nostr.org", "Nostr Apps") + primary_nip_index[:6] + research_sources[:2]
    resource_database_sources = all_sources[:18] + research_sources

    rewrites = {
        "what-is-nostr": {
            "title": "What is Nostr?",
            "deck": "A practical first model: your key is the identity, events are the signed record, relays carry the record, and clients turn it into an experience you can actually use.",
            "quick_label": "The mental model",
            "intro": "Start with the simplest useful picture. Nostr is not one app, one company database or one feed. It is a way to sign social data with your own key, publish it to relays, and let different clients read it back in different shapes.",
            "sections": [
                section("The account moves first", [
                    "On a normal social network, the account lives inside the platform. The company owns the database, controls the API, defines the ranking rules and can decide which client is allowed to exist. You can export some data, maybe, but the account itself is still a tenant.",
                    "Nostr flips that first piece. Your public key is the stable identity. Your private key signs actions as that identity. A client can disappear, a relay can reject a post, a feed can feel wrong, and the identity can still continue somewhere else. That is the first idea to keep in your pocket.",
                ], [
                    ("Public key", "The identifier other people can follow, search, verify and display."),
                    ("Private key", "The signing authority. Treat it like a root credential, not like a casual password."),
                    ("Signature", "The proof that an event really came from the key that claims to have sent it."),
                ]),
                section("Four pieces, not one platform", [
                    "The daily Nostr system is made of four moving pieces: keys, events, relays and clients. Keys identify and sign. Events carry the actual content or state change. Relays receive, store and return events. Clients create the visible product: timeline, long-form editor, marketplace, wallet flow, dashboard or venue interface.",
                    "That separation is why Nostr can feel strange at first. You are used to an app being the account, the server, the feed, the moderation system and the business model at once. Here those jobs can be split. That is powerful, but it also means you need better words for what is happening.",
                ], [
                    ("Keys", "Who is acting."),
                    ("Events", "What was signed."),
                    ("Relays", "Where it is published, stored, filtered or refused."),
                    ("Clients", "How you see, create and navigate it."),
                ]),
                section("Events are the basic object", [
                    "NIP-01 is the base layer: an event has an id, a public key, a timestamp, a kind, tags, content and a signature. A short note, a profile update, a follow list, a zap receipt, a badge award or a relay list can all be represented as different event types.",
                    "This is why Nostr is broader than microblogging. A timeline is only one possible client view over signed events. The same pattern can support long-form writing, search, file metadata, wallet permission messages, badges, lists, communities, marketplaces and local venue context.",
                ]),
                section("Relays are not social accounts", [
                    "A relay is not where your identity lives. It is more like infrastructure with opinions. It can accept, store, return, rate-limit, reject, require payment, require authentication or moderate. A client asks relays for events by sending filters, and relays answer with matching events.",
                    "Because relays do not automatically synchronize with every other relay, availability is a design question. If you publish only to one fragile relay, the post can be hard to find later. If you publish everywhere without strategy, you create noise and overhead. Good clients and good relay lists matter.",
                ]),
                section("Why it is not a blockchain", [
                    "Nostr does not put every social action into blocks, and it does not require a native token. Events are signed and distributed through relays. Bitcoin and Lightning enter the picture when money is useful: zaps, wallet connections, paid access, rewards or settlement.",
                    "That distinction matters. The social layer stays lightweight. Payments can be attached where they make sense. You do not need consensus for every note, but you do need good key handling, relay choice, client UX and spam resistance.",
                ]),
                section("Where we use the idea", [
                    "For us, Nostr is useful because we need one identity layer that can touch profiles, creator pages, fan demand, content access, status, venues, awards, payments and future governance. A closed Crays-only login would be easier to build, but too small for the mission.",
                    "The honest product job is to hide the machinery without hiding the ownership. You should not need to memorize every NIP to use Crays.net, but the system underneath should still respect portable identity, signed actions and user control.",
                ]),
                section("The first test before trusting any feature", [
                    "When a Nostr product sounds exciting, ask four questions: what is signed, where is it stored, which client shows it, and what still works if one service disappears. That test cuts through most protocol fog.",
                    "If the answer is clear, you are looking at a real Nostr-shaped feature. If the answer is vague, you may still be looking at a normal platform feature with Nostr words painted on the outside.",
                ], [
                    ("Signed", "Which key authorized the action?"),
                    ("Stored", "Which relay, file server or service keeps the data available?"),
                    ("Rendered", "Which clients know how to show it?"),
                    ("Portable", "What survives if the first app is gone?"),
                ]),
            ],
            "sources": common_core_sources + research_sources[2:4],
            "related": ["getting-started", "why-nostr", "keys-identity", "clients", "relays", "nips"],
            "related_label": "Build the map",
            "keywords": ["what is Nostr", "Nostr protocol", "Nostr events", "Nostr relays"],
            "read": "12 min read",
        },
        "why-nostr": {
            "title": "Why Nostr Matters",
            "deck": "Nostr matters when you are tired of renting identity, audience and social proof from one platform operator.",
            "quick_label": "The reason to care",
            "intro": "The point of Nostr is not that it is new. The point is that it attacks the account-hostage problem at the root: identity, publishing, discovery and money no longer have to live inside one company's database.",
            "sections": [
                section("The platform bargain got expensive", [
                    "Closed platforms gave creators, builders and communities huge reach. The price was control. A company can change the API, bury links, remove monetization, block a client, freeze an account, hide followers, re-rank the feed or make yesterday's strategy useless overnight.",
                    "You can still use those platforms. The mistake is building your whole social memory there. If your audience, reputation and payment surface are locked in one place, your business is always negotiating with a landlord.",
                ]),
                section("Nostr starts at the identity layer", [
                    "A portable public key sounds technical, but the consequence is simple: your identity can outlive one interface. You can move between clients because the client is not the account. You can publish to more than one relay because the relay is not the account either.",
                    "That does not make the world perfect. It gives you leverage. Client makers compete on experience. Relay operators compete on performance, policy and price. Communities can choose their own boundaries without owning every user's root identity.",
                ], [
                    ("Client leverage", "You can leave a bad interface without starting from zero."),
                    ("Relay leverage", "You can publish to more than one infrastructure path."),
                    ("Social leverage", "Your follow graph and reputation can become less platform-dependent."),
                ]),
                section("Portability changes the economics", [
                    "When an app owns the account, it can tax the whole relationship. When the identity and graph are portable, products have to win by being useful. That changes the design pressure. The app still needs revenue, moderation, support and polish, but it cannot pretend the user exists only inside its walls.",
                    "This is especially important for creators. A creator's audience is not just a feed metric. It is future demand, ticket sales, paid content, collaborations, venue nights, merchandise, voting power and reputation. Nostr gives that demand a more portable root.",
                ]),
                section("Relays make freedom operational", [
                    "Relays are the hard part people often skip. They are where availability, moderation, spam control, storage cost, policy and reach become real. A relay can be free, paid, invite-only, local, archival, search-oriented, community-specific or attached to a venue.",
                    "The empirical research on Nostr shows the trade-off clearly: replication across relays improves availability and censorship resistance, but it creates cost and traffic overhead. That means the future is not one perfect relay. It is smarter relay selection, better defaults and clearer business models.",
                ]),
                section("Why Bitcoin people noticed early", [
                    "Bitcoin people understand one thing quickly: if you do not control the key, you are asking permission. Nostr applies that instinct to identity and publishing. Lightning then gives social actions a payment route: zaps, paid content, wallet permissions and later more serious commerce flows.",
                    "The overlap does not mean every Nostr user must become a Bitcoin maximalist. It means the network has a natural path for value-for-value culture, creator support and low-friction settlement where payments are useful.",
                ]),
                section("What still has to improve", [
                    "Nostr is not mature enough to romanticize. Key recovery is hard. Bad clients can train people to paste secrets into websites. Spam and impersonation are real. Search is uneven. Relay discovery still needs better UX. Some NIPs are widely useful, some are experimental, and some are already marked unrecommended.",
                    "That is exactly why we write these pages like a map, not a hype deck. You should leave with sharper judgment: where Nostr gives you control, where it moves responsibility onto you, and where a product still has to do real work.",
                ]),
                section("Why this matters to us", [
                    "For us, the biggest reason is continuity. A global community cannot depend on one social platform, one app store mood, one creator channel or one payment provider. We need identity, reputation, creator demand, venue access and governance signals that can travel.",
                    "Nostr is not the whole Crays system. It is the social base layer we can build with: profiles, content sale, awards, zaps, status, local relays, Super Nodes and later association-grade governance. That is why it matters beyond the protocol scene.",
                ]),
            ],
            "sources": src("Nostr protocol repository", "nostr.how", "Nostr Apps") + primary_nip_index[:2] + research_sources[:4],
            "related": ["what-is-nostr", "nostr-and-bitcoin", "privacy-security", "relays", "nostr-and-crays", "dao-governance"],
            "related_label": "Follow the consequence",
            "keywords": ["why Nostr matters", "portable social graph", "decentralized social", "Nostr Bitcoin"],
            "read": "11 min read",
        },
        "getting-started": {
            "title": "Getting Started with Nostr",
            "deck": "Start safely: protect the key, choose one good client, understand relays, add a human-readable identity, then experiment with zaps and publishing.",
            "quick_label": "Your first safe path",
            "intro": "A good Nostr start is not about installing ten apps in one evening. First you learn what the key controls, then you pick a client, publish through relays, make your identity recognizable and only then connect payments or advanced tools.",
            "sections": [
                section("Before you create anything", [
                    "Learn two words before you touch a client: npub and nsec. NIP-19 makes them easier to recognize. The npub is public. You can share it. The nsec is private. Do not post it, paste it into random websites or send it to support chats.",
                    "If you build reputation on a key, that key becomes valuable. Losing it can strand the identity. Leaking it can let someone impersonate you. That is why your first setup decision is not cosmetic. It is security architecture at human scale.",
                ], [
                    ("Share npub", "It is the public identity people can follow."),
                    ("Protect nsec", "It is the signing secret."),
                    ("Use a signer", "When possible, let a signer approve actions instead of handing the secret to every web client."),
                ]),
                section("Pick one client for the first week", [
                    "A client is the app experience, not the account. Start with one client that feels clear enough to use daily. Social feed clients, long-form clients, power-user clients and media clients all reveal different sides of the same protocol.",
                    "Do not judge the whole network by one interface. If the first app feels noisy, slow or strange, that may be client design, relay choice or onboarding friction. The magic appears when the same identity can move into another interface without becoming a new account.",
                ]),
                section("Use signers as a habit, not a feature", [
                    "NIP-07 lets browser extensions expose a window.nostr interface so web apps can request your public key or ask for a signature. NIP-46 extends the idea with remote signing. The product point is simple: a client should not need to permanently hold your private key just to let you post.",
                    "You still need judgment. A signer can make dangerous actions easier to approve if prompts are vague. Read what you are signing, especially around wallet access, encrypted messages, publishing permissions and any feature that feels like account recovery.",
                ]),
                section("Relays decide what you can see", [
                    "After keys and clients, relays are the next reality check. Your client writes events to selected relays and reads events from selected relays. If your relay set is poor, you may miss posts, replies, profile updates or mentions.",
                    "NIP-65 helps by letting a user publish preferred read and write relays. Good clients use that metadata to find people more intelligently. You do not need to become a relay operator on day one, but you should understand that relay choice affects reach and memory.",
                ]),
                section("Make the identity human", [
                    "A raw public key is exact but ugly. NIP-05 adds a DNS-backed identifier that looks like a familiar name at a domain. It does not replace the key, and it is not a password. It is a recognition layer that helps people see that a public key belongs to a person, project or organization.",
                    "For brands, creators and venues, this matters a lot. A domain-backed identity is easier to explain than a long key. It also creates accountability: if the domain is trusted, the key becomes easier to recognize.",
                ]),
                section("Try zaps after you understand wallet scope", [
                    "Zaps are Lightning payments represented on Nostr through zap requests and zap receipts. They can be fun, generous and culturally important. They can also confuse beginners who think every Nostr action must involve money.",
                    "Start with small amounts, understand the wallet you connect, and learn the difference between a social signal and a business model. Later, Nostr Wallet Connect can make wallet access more modular, but permission prompts and limits must stay clear.",
                ]),
                section("Your first practical checklist", [
                    "By the end of the first week, you should be able to explain your own setup: which key you use, where it is backed up, which client you like, which relays you publish to, whether you have NIP-05, and whether a wallet is connected.",
                    "That is enough to start. You do not need every NIP. You need good habits before the network starts feeling normal.",
                ], [
                    ("Day one", "Create or import a key safely and save the backup."),
                    ("Day two", "Use one client and follow a few real people."),
                    ("Day three", "Check your relay list and profile metadata."),
                    ("Day four", "Add NIP-05 if you have a domain or trusted provider."),
                    ("Day five", "Try a small zap only after wallet permissions make sense."),
                ]),
            ],
            "sources": src("Nostr Login", "Nostr Apps", "nostr.how") + primary_nip_index[1:8] + research_sources[1:2],
            "related": ["keys-identity", "clients", "relays", "nip-05-identifiers", "nip-57-zaps-lightning", "nip-47-wallet-connect"],
            "related_label": "Continue safely",
            "keywords": ["Nostr getting started", "Nostr onboarding", "Nostr keys", "Nostr signer"],
            "read": "13 min read",
        },
        "resources": {
            "title": "Nostr Resources and Links",
            "deck": "A research map for Nostr: canonical standards first, then clients, relays, developer tools, directories, long-form research and Crays-relevant product references.",
            "quick_label": "How to use the library",
            "intro": "A link database is only useful when it has a reading method. Start with primary sources, compare directories with real project pages, and treat every client, relay and NIP as part of a larger map instead of a trophy list.",
            "sections": [
                section("Start with canonical sources", [
                    "When you need protocol truth, begin with the NIPs repository and NIP-01. The repository is not a product roadmap. It is a standards shelf. Some NIPs are mandatory, many are optional, and a few are explicitly marked unrecommended when the ecosystem has moved on.",
                    "Use Nostr.how when you need plain-language orientation and the Developer Guide when you need the first builder path. Those sources solve different problems: one helps you explain Nostr to a human, the other helps you build without guessing.",
                ]),
                section("Read directories as maps, not verdicts", [
                    "Nostr Apps, Awesome Nostr, Nostr Compass and other directories are discovery tools. They help you find clients, relays, libraries, file servers, marketplaces, media apps and experiments. They do not prove that a project is maintained, secure or product-ready.",
                    "The right habit is triangulation. Open the directory entry, then check the project site, repository, release history, supported NIPs, signer behavior, relay assumptions and whether the product explains risk in normal language.",
                ]),
                section("Separate clients from infrastructure", [
                    "Clients are the visible layer. They decide onboarding, feeds, profiles, long-form editing, notifications, search, media display, moderation controls and wallet prompts. Infrastructure is less visible but equally important: relays, file storage, indexers, signers, wallets and libraries.",
                    "A beginner may only care whether the app feels good. A builder needs to know whether the app signs safely, reads from the right relays, handles missing events, supports NIP-65, respects NIP-05 and avoids turning private keys into paste-and-pray onboarding.",
                ]),
                section("Use the Excel database as a working stack", [
                    "The research workbook gives us a structured source base: 403 link rows plus dedicated sheets for NIPs, clients, developer stack, relays, long-form research and core directories. That shape is useful because the ecosystem is too broad for one flat bookmark folder.",
                    "For Start pages, the most useful rows are not necessarily the newest projects. They are the sources that explain the base model: NIP-01, NIP-05, NIP-07, NIP-19, relay directories, Nostr.how, the Developer Guide, nostr-tools, NDK, strfry, Khatru, Blossom and empirical relay research.",
                ], [
                    ("Core", "Protocol home, NIPs, Nostr.how and entry explanations."),
                    ("Apps", "Client and interface choices."),
                    ("Dev stack", "Libraries, tools, test utilities and relay frameworks."),
                    ("Relays", "Live infrastructure, monitoring, paid relays and relay software."),
                    ("Research", "Long-form analysis that explains trade-offs, not just features."),
                ]),
                section("Track media and storage separately", [
                    "Nostr events are small signed records. Images, video, large files and other blobs need adjacent storage. NIP-96 describes HTTP file storage but is now marked unrecommended in favor of Blossom in the NIPs repository. Blossom addresses blobs by sha256 hash and uses Nostr keys for identity and authorization.",
                    "That matters for creators and venues. A post can be portable while the media behind it is fragile. Good resource pages should therefore track file metadata, storage servers, Blossom, NIP-94, upload authorization, mirroring and deletion behavior.",
                ]),
                section("What belongs in a serious resource page", [
                    "A serious Nostr resource page should tell you what a source is good for, what it does not prove and where it sits in the stack. A GitHub repo may be primary for implementation, but weak for onboarding. A blog post may be excellent for framing, but not authoritative for NIP details.",
                    "That is the standard for this archive: fewer random outbound links, more annotated context. If a link does not help you decide what to learn, build, test or distrust next, it does not deserve a prominent place.",
                ]),
            ],
            "sources": resource_database_sources,
            "related": ["what-is-nostr", "nips", "apps", "relay-market-directory", "developer-tools", "archive-library"],
            "related_label": "Open the shelves",
            "keywords": ["Nostr resources", "Nostr links", "Nostr research database", "Nostr directories"],
            "read": "14 min read",
        },
        "glossary": {
            "title": "Nostr Glossary",
            "deck": "A grouped glossary that explains Nostr terms by function: identity, events, relays, clients, payments, media, trust and product consequences.",
            "quick_label": "Read terms by job",
            "intro": "A flat glossary makes Nostr feel harder than it is. The better way is to group the words by the job they do. Once you know which words belong to identity, events, relays, clients, payments and trust, the whole map gets calmer.",
            "sections": [
                section("Identity words", [
                    "Public key, private key, npub, nsec, signature and NIP-05 all live in the identity family. The public key is the identifier. The private key signs. The signature proves authorship. NIP-19 gives safer-looking display formats. NIP-05 gives you a domain-backed name people can recognize.",
                    "The practical mistake is mixing public and private language. npub can go on a profile, a business card or a QR code. nsec should be treated like a master secret. A product that does not make that difference painfully clear is training users badly.",
                ], [
                    ("npub", "Public key display format."),
                    ("nsec", "Private key display format."),
                    ("NIP-05", "DNS-backed identifier, not custody and not recovery."),
                ]),
                section("Event words", [
                    "Event, kind, tag, content, id and signature belong together. An event is the signed object. The kind says what type of thing it is. Tags create references, mentions, relay hints, subjects, labels and other structured context.",
                    "This is the middle of the protocol. If you understand events, you can understand why Nostr can represent posts, profiles, follows, relays, zaps, badges, long-form articles, file metadata and more without becoming one giant app specification.",
                ]),
                section("Relay words", [
                    "Relay, filter, subscription, EOSE, OK, CLOSED, NIP-11 and NIP-65 are infrastructure words. A client sends an EVENT to publish or a REQ with filters to ask for matching events. A relay can accept, reject, close, rate-limit or return stored and live results.",
                    "NIP-11 lets relays describe capabilities and administrative details. NIP-65 lets a user publish preferred read and write relays. Together they help clients stop guessing, although relay discovery is still one of the rougher edges in daily Nostr use.",
                ]),
                section("Client and signer words", [
                    "Client, signer, extension, remote signer and Nostr Connect describe the part you actually touch. A client creates the experience. A signer protects the key by approving signatures without forcing you to paste the private key into every web app.",
                    "NIP-07 is the browser signer pattern. NIP-46 covers remote signing. The product standard is simple: if a feature asks for power, the prompt should explain the power in words a normal person can understand.",
                ]),
                section("Money words", [
                    "Zap, Lightning, invoice, receipt, NWC and wallet service sit in the value-flow family. NIP-57 defines zap requests and zap receipts. NIP-47 lets a client interact with a Lightning wallet through a standardized Nostr Wallet Connect flow.",
                    "Do not confuse a zap with a business model. A zap is a payment signal. Creator income, paid content, membership, venue access and awards need product rules, refunds, abuse controls, accounting and user support around the protocol event.",
                ]),
                section("Media and storage words", [
                    "File metadata, blob, Blossom, NIP-94 and NIP-96 explain where larger media fits. Nostr relays are not meant to become infinite video storage. A note can reference a file, but the file has to be hosted, hashed, mirrored, authorized and kept available somewhere.",
                    "Blossom is important because it treats binary data as sha256-addressed blobs on HTTP media servers while still using Nostr keys for identity. That creates a clearer split between signed social records and heavier media infrastructure.",
                ]),
                section("Trust and moderation words", [
                    "Mute list, block list, web of trust, report, label, relay policy, paid relay and community are social-control words. Nostr does not remove moderation. It distributes moderation decisions across clients, relays, communities and user-controlled lists.",
                    "That is not a weakness if the product explains it well. You need to know who is filtering what, whether a relay stores the event, whether a client hides it, and whether a community rule is local or network-wide.",
                ]),
                section("Product words we use carefully", [
                    "Portable does not mean permanent. Decentralized does not mean every part is equally distributed. Signed does not mean safe. Encrypted does not mean the whole workflow is private. Relay does not mean platform. NIP does not mean finished product.",
                    "Those distinctions keep the archive honest. You can be excited about Nostr and still speak with precision.",
                ]),
            ],
            "sources": src("Nostr protocol repository", "Nostr NIPs", "nostr.how") + primary_nip_index + research_sources[:2],
            "related": ["what-is-nostr", "events-and-kinds", "keys-identity", "relays", "nip-57-zaps-lightning", "deep-dives/blossom-servers-and-relays"],
            "related_label": "Use these terms next",
            "keywords": ["Nostr glossary", "Nostr terms", "npub nsec", "Nostr relays"],
            "read": "12 min read",
        },
        "reading-paths/beginner": {
            "title": "Beginner Reading Path",
            "deck": "A guided first route for people who want Nostr to make sense before they go deep into clients, relays, wallets and culture.",
            "quick_label": "Your first week",
            "intro": "This path is for your first real week with Nostr. The goal is not to master the whole protocol. The goal is to know what you are holding, what you are signing and why the network feels different from a normal social app.",
            "sections": [
                section("Day 1: learn the shape before the feed", [
                    "Read What is Nostr? before judging any client. Your first mental model should be keys, events, relays and clients. If you start with the feed alone, Nostr looks like a weird Twitter clone. If you start with the architecture, the feed becomes one surface among many.",
                    "Do one practical exercise: explain to yourself why a client is not the same thing as your account. If that sentence is clear, the rest gets easier.",
                ]),
                section("Day 2: protect the key", [
                    "Read the keys and identity material next. The private key is the danger zone. Do not paste it around while testing. Learn npub versus nsec, then learn why signers exist.",
                    "Your goal is not paranoia. Your goal is calm. You should know where your backup lives, which client can sign for you and which websites have actually received signing authority.",
                ]),
                section("Day 3: try two clients on purpose", [
                    "Pick one simple social client and one second client with a different personality. Maybe one mobile app and one web app. The point is to feel portability in your hands: same identity, different interface.",
                    "Notice what changes. Feed quality, search, media, replies, notifications and profile rendering can all vary. That variation is not a bug in the idea. It is client competition becoming visible.",
                ]),
                section("Day 4: make relays less mysterious", [
                    "Read the relay introduction and look at your client's relay settings. You do not need to optimize yet. Just understand that relays affect who can see you, what you can fetch, how fast things load and whether old events remain available.",
                    "If your client supports relay list metadata, look at it. If it hides everything, write down that feeling too. Beginner UX should explain enough without turning relay management into homework.",
                ]),
                section("Day 5: add identity polish", [
                    "Now add or understand NIP-05. A human-readable identifier helps friends, collaborators, creators and brands recognize the key. It is especially useful when impersonation is easy and keys are ugly.",
                    "Also clean up your profile metadata. Use a real name or handle strategy, profile picture, website and a short bio that explains why someone should follow this key.",
                ]),
                section("Day 6: touch zaps carefully", [
                    "If you are curious, try a tiny zap. Read what the wallet is doing. Understand that a zap has a request and receipt flow. Do not connect a wallet you do not understand just because a button looks fun.",
                    "The lesson is not money first. The lesson is that social actions and value flow can share a signed identity layer.",
                ]),
                section("Day 7: decide your next route", [
                    "After a week, choose a direction. If you want safety, go into privacy and signers. If you want to build, go into the developer path. If you create, go into media and creator commerce. If you run places, go into the operator path.",
                    "You are no longer trying to understand Nostr all at once. You are choosing the part that matches your life.",
                ], [
                    ("Keep going", "Read keys, clients, relays and zaps."),
                    ("Build", "Move to the developer path."),
                    ("Create", "Move to the creator path."),
                    ("Operate", "Move to the operator and venue path."),
                ]),
            ],
            "sources": common_core_sources,
            "related": ["what-is-nostr", "getting-started", "keys-identity", "clients", "relays", "nip-57-zaps-lightning"],
            "related_label": "After the first week",
            "keywords": ["Nostr beginner path", "learn Nostr", "Nostr first week"],
            "read": "Reading path",
        },
        "reading-paths/developer": {
            "title": "Developer Reading Path",
            "deck": "A builder route through NIP-01, event validation, relay behavior, signers, NIP-65, wallets, media storage and the practical tooling stack.",
            "quick_label": "Build the smallest honest client",
            "intro": "This path is for builders. The goal is not to implement every NIP. The goal is to build something small that signs correctly, talks to relays honestly, handles missing data and teaches you where the product complexity really lives.",
            "sections": [
                section("Start with NIP-01, not a framework", [
                    "Before you reach for NDK or nostr-tools, read NIP-01 closely. You need to understand event structure, signature verification, filters, EVENT, REQ, CLOSE, EOSE, OK and CLOSED messages. That is the floor.",
                    "A framework can save time later, but it should not hide the protocol from you on day one. If you cannot explain what your client sends to a relay and what the relay is allowed to send back, debugging will become superstition.",
                ]),
                section("Build one event end to end", [
                    "Create a tiny exercise: generate or load a key, create a kind 1 event, sign it, verify it locally, publish it to a test relay, then request it back with a filter. That loop teaches more than a large unfinished app.",
                    "Add logging for every message. The first real skill is not UI. It is seeing the event lifecycle clearly: build, sign, publish, acknowledge, query, render and deduplicate.",
                ]),
                section("Relays are product boundaries", [
                    "A relay is not a passive pipe. It can reject events, close subscriptions, require auth, throttle, store only certain kinds, omit history, apply policy or disappear. Your client has to treat relay responses as facts, not as personal insults.",
                    "Read NIP-11 for relay information documents and NIP-65 for relay list metadata. Then test what happens when one relay is slow, one refuses writes and one returns partial history.",
                ]),
                section("Use libraries after you know the wire", [
                    "nostr-tools gives lower-level JavaScript utilities. NDK adds higher-level subscription management, signer adapters, relay discovery, caching and NIP-65 outbox behavior. rust-nostr and go-nostr serve other stacks. nak is useful when you want a command-line knife for protocol work.",
                    "Pick the tool that matches the product. Do not make a heavy architecture for a proof-of-concept. Do not hand-roll fragile cryptography for production.",
                ]),
                section("Design signing as a security feature", [
                    "NIP-07 and NIP-46 are not onboarding decoration. They shape the trust boundary between app and user. A web client that asks for a raw private key should have a very good reason, and most do not.",
                    "Model prompts carefully. What is being signed? Is it a public event, encrypted payload, wallet request, auth token or relay action? If the user cannot understand the prompt, the signer flow is only technically safer.",
                ]),
                section("Handle money and media as separate subsystems", [
                    "NIP-47 and NIP-57 bring wallet and zap flows into scope, but they add permission, invoice, error and abuse questions. NIP-94, NIP-96 and Blossom bring media and files into scope, but they add hosting, hashing, authorization, transformation, mirroring and deletion questions.",
                    "A serious Nostr app does not pretend these are solved by a button. It gives each subsystem its own threat model and fallback behavior.",
                ]),
                section("Testing is part of interoperability", [
                    "Test against multiple relays, multiple clients and ugly network conditions. Duplicate events, missing profile metadata, stale relay lists, unsupported NIPs and slow EOSE behavior are normal field conditions.",
                    "A developer path is successful when the app fails legibly. Users should know whether a post was not signed, not accepted, not found, not displayed or not supported.",
                ]),
            ],
            "sources": primary_nip_index + research_sources[1:2] + research_sources[4:9] + src("NIP-42 Relay Information", "NIP-65 Relay List Metadata"),
            "related": ["events-and-kinds", "nips", "nip-07-signers", "nip-46-remote-signing", "relays", "deep-dives/blossom-servers-and-relays"],
            "related_label": "Build deeper",
            "keywords": ["Nostr developer path", "Nostr NIP-01", "nostr-tools", "NDK", "Nostr relays"],
            "read": "Reading path",
        },
        "reading-paths/creator": {
            "title": "Creator Reading Path",
            "deck": "A creator route through portable audience, long-form publishing, media storage, zaps, paid access, fan context and Crays-style creator commerce.",
            "quick_label": "Own the audience door",
            "intro": "This path is for creators who care less about protocol debates and more about audience independence. Nostr will not do the creative work for you, but it can make the relationship with your people less dependent on one platform.",
            "sections": [
                section("Start with the audience problem", [
                    "If one platform owns your followers, one policy change can damage years of work. Nostr gives you a public key and portable social graph as a base. That means your people can find the same identity through different clients and future products.",
                    "This does not replace craft, taste, consistency or distribution strategy. It gives those things a more durable root.",
                ]),
                section("Choose your publishing shape", [
                    "Short notes, long-form articles, live events, music, video, images, comments and highlights all sit differently on Nostr. NIP-23 matters for long-form. NIP-94 and Blossom matter when media files need stable references. Client choice matters because the same event can feel brilliant in one interface and invisible in another.",
                    "A creator should test not just posting, but how the post appears elsewhere. Does the title survive? Does the image load? Do replies travel? Does the client expose your profile and links clearly?",
                ]),
                section("Use zaps as signal, not fantasy accounting", [
                    "Zaps are powerful because they make appreciation immediate and visible. They are weak if you pretend every audience will pay enough through spontaneous micro-payments. Treat zaps as one signal in a broader business system.",
                    "Paid content, memberships, event access, limited drops, community status, venue nights and brand partnerships need product design around the protocol. A zap can start a relationship. It does not replace the whole revenue model.",
                ]),
                section("Make identity recognizable", [
                    "Use NIP-05, a clear profile, consistent imagery and links that match your public presence. Impersonation is easier in open systems because anyone can generate a key. Recognition layers matter.",
                    "If you are a serious creator, your key becomes part of your brand. Handle it like you would handle your domain, mailing list and payment account.",
                ]),
                section("Understand the media layer", [
                    "Your text event can be portable while the media URL breaks. That is why file metadata, Blossom servers, mirroring and upload rules matter. If your work depends on images, video or audio, you need to know where the heavy files live.",
                    "For us, this is one reason creator commerce cannot be only a feed. Crays.net, content sale, venues and status need a more intentional media and access layer around Nostr.",
                ]),
                section("Design the fan journey", [
                    "A fan should be able to follow, read, pay, save, attend, vote and build status without feeling like they crossed six unrelated systems. Nostr can carry identity and signed signals. The product has to turn those signals into a clear journey.",
                    "That is the creator opportunity: portable audience plus richer experiences. Not just posts, but access, context and relationship memory.",
                ]),
            ],
            "sources": src("Nostr Apps", "Habla", "YakiHonne", "Wavlake") + primary_nip_index[5:8] + research_sources[3:4] + blossom_sources[:4],
            "related": ["creators", "nip-23-long-form", "nip-57-zaps-lightning", "music-video-media", "content-sale", "deep-dives/blossom-servers-and-relays"],
            "related_label": "Turn audience into paths",
            "keywords": ["Nostr creator path", "Nostr zaps", "Nostr publishing", "Nostr paid content"],
            "read": "Reading path",
        },
        "reading-paths/operator": {
            "title": "Operator and Venue Reading Path",
            "deck": "A route for venue operators, community hosts and infrastructure people: relays, access, local context, moderation, payments, monitoring and Super Node logic.",
            "quick_label": "Run the room, not just the server",
            "intro": "This path is for people who operate spaces, communities or infrastructure. Your question is not whether Nostr is interesting. Your question is whether it can help real guests, members, creators and staff coordinate with less platform dependence.",
            "sections": [
                section("Translate Nostr into venue jobs", [
                    "A venue does not need protocol theater. It needs identity, access, bookings, membership context, creator nights, local announcements, payments, reputation, staff tools and incident handling. Nostr is useful only if it helps those jobs.",
                    "Start by mapping actions: who arrives, who hosts, who pays, who can enter, who receives updates, who moderates, who earns status and who can prove what happened later.",
                ]),
                section("Relay strategy is hospitality strategy", [
                    "A public relay, paid relay, community relay and venue relay have different meanings. A venue relay can carry local context, event posts, membership signals and service messages. It can also become a moderation and privacy liability if treated casually.",
                    "Read NIP-11 for relay self-description, NIP-42 for relay authentication, NIP-65 for user relay lists and NIP-66-style monitoring ideas for liveness. Then decide what belongs on a venue-controlled path and what should remain on broader public relays.",
                ]),
                section("Moderation is part of service", [
                    "In a physical space, moderation is not abstract. You already decide who can enter, who is disturbing the room and what behavior breaks trust. Nostr does not remove that responsibility. It gives you more granular places to apply it: client, relay, list, event, group and venue policy.",
                    "Write the policy before the conflict. Decide what gets stored, what gets refused, what gets hidden, what requires authentication and what must never be public.",
                ]),
                section("Payments need operational boundaries", [
                    "Zaps and wallet connections are exciting, but venues need receipts, refunds, tax handling, support, limits and staff workflows. A Lightning payment signal is not the same thing as a complete POS process.",
                    "Use Nostr where signed social and payment context helps. Keep accounting, compliance and customer service explicit. The guest should feel clarity, not experimental plumbing.",
                ]),
                section("Super Node thinking", [
                    "For us, the Super Node idea is where online identity meets local service. A node can help with relay behavior, local mesh, access, payments, status, event context and hospitality systems. The point is not to show guests a server. The point is to make the space smarter without trapping people.",
                    "Start small: local announcements, member recognition, creator event context, simple access proofs and reliable relay monitoring. Add commerce and governance only after the base is stable.",
                ]),
                section("Monitor before you promise", [
                    "Operators need uptime, backups, logs, abuse handling and clear fallback paths. If a relay is down, what happens to check-in? If a media server rejects uploads, what happens to event posts? If a signer fails, can staff still operate?",
                    "A venue-grade Nostr setup must be boring in the right places. The public story can feel alive. The operational core should be measured, documented and recoverable.",
                ]),
            ],
            "sources": relay_sources + primary_nip_index[1:2] + primary_nip_index[6:8] + research_sources[2:3] + research_sources[6:9],
            "related": ["operators-venues", "relays", "relay-market-directory", "crays-super-node", "nip-42-relay-auth", "dao-governance"],
            "related_label": "Operate the layer",
            "keywords": ["Nostr venue", "Nostr operator path", "Nostr relay strategy", "Crays Super Node"],
            "read": "Reading path",
        },
        "reading-paths/culture": {
            "title": "Culture Reading Path",
            "deck": "A route through the human side of Nostr: Bitcoin overlap, builders, events, zaps, memes, conflict, moderation, music, media and public identity.",
            "quick_label": "Read the room",
            "intro": "Nostr is a protocol, but you will misunderstand it if you ignore the scene around it. The culture explains why people tolerate rough edges, why zaps matter emotionally, why builders ship in public and why moderation debates never stay theoretical.",
            "sections": [
                section("A builder scene before a product category", [
                    "Nostr grew like a builder camp: rough clients, public experiments, fast NIP debates, relay operators, Bitcoin people, artists, conference rooms, strange jokes and very strong opinions about keys. That energy is part of the network's strength.",
                    "It also means newcomers can feel like they walked into the middle of a conversation. This path helps you read the room without having to copy every tribe marker.",
                ]),
                section("Bitcoin overlap without reduction", [
                    "Bitcoin culture matters because it brought key sovereignty, Lightning payments, value-for-value behavior and a deep suspicion of platform control. Jack Dorsey's support also gave Nostr public attention. But Nostr is not only a Bitcoin social app.",
                    "The healthier reading is this: Bitcoin gives Nostr a strong money and sovereignty vocabulary. Nostr gives Bitcoin people a broader social and publishing surface. The overlap is real; the identity should stay open.",
                ]),
                section("Zaps changed the mood", [
                    "Zaps are technically payment events. Culturally, they are applause with money attached. They make appreciation visible, create status games, reward builders and give creators a reason to care about wallet setup.",
                    "That does not make zaps pure or sufficient. They can reward noise, create pressure and hide weak business models. Read them as social signals with economic weight.",
                ]),
                section("Events and conferences matter", [
                    "Nostr culture is not only online. Nostrica, Nostriga and smaller meetups gave the protocol a human shape: builders arguing in person, demos failing live, friendships forming, projects getting funded and norms spreading faster than docs.",
                    "For Crays, that matters because our world is digital and IRL. A protocol culture that can meet in real places is much more relevant to hospitality, venues and global community than a purely abstract developer standard.",
                ]),
                section("Moderation is culture made visible", [
                    "Every open network eventually asks who gets muted, blocked, filtered, labeled, reported, rate-limited or excluded. Nostr does not make those questions disappear. It makes the decision points more distributed.",
                    "Client moderation, relay policy, community rules, web-of-trust and user lists can coexist. The cultural challenge is to make boundaries without recreating one global platform authority.",
                ]),
                section("Media, music and long-form create depth", [
                    "Short notes can make Nostr feel noisy. Long-form writing, music, video, photos, highlights and comments make it feel like a broader cultural layer. That is where creators can build identity beyond feed velocity.",
                    "Pay attention to the tools that make slower media feel native: NIP-23 articles, file metadata, Blossom, clients like Habla and YakiHonne, music projects like Wavlake and discovery surfaces that do not bury thoughtful work.",
                ]),
                section("How to participate without pretending", [
                    "You do not need to sound like an insider. Follow builders, read NIPs when they affect you, try zaps gently, attend events if you can, and keep your own taste. The best Nostr culture is not obedience to a scene. It is people building in public with enough freedom to disagree.",
                    "That is the tone we want here: warm, technical enough, skeptical enough and always written to the person trying to understand what comes next.",
                ]),
            ],
            "sources": src("Nostrica", "Nostr World", "Wavlake", "Nostr Apps") + primary_nip_index[5:8] + research_sources[3:4],
            "related": ["people", "events", "nostr-and-bitcoin", "music-video-media", "moderation-discovery", "creators"],
            "related_label": "Read the scene",
            "keywords": ["Nostr culture", "Nostr events", "Nostr zaps", "Nostr Bitcoin culture"],
            "read": "Reading path",
        },
        "reading-paths/research": {
            "title": "Research Reading Path",
            "deck": "A route for careful analysis: primary standards, empirical relay data, source triangulation, client claims, NIP drift, directories and Crays product relevance.",
            "quick_label": "How to verify Nostr claims",
            "intro": "This path is for research mode. You are not trying to collect links. You are trying to know which claims are standards, which are product choices, which are cultural beliefs and which are still untested.",
            "sections": [
                section("Separate source types first", [
                    "A NIP, a client website, a GitHub README, a relay monitor, a directory listing, a blog essay and an academic measurement paper all answer different questions. Mixing them creates fake certainty.",
                    "Use primary standards for what software may implement. Use repos for what code appears to do. Use monitors for live infrastructure clues. Use essays for framing. Use empirical papers for measured trade-offs and limitations.",
                ]),
                section("Use NIPs as moving standards, not scripture", [
                    "The NIPs repository itself says the documents describe what may be implemented by compatible relay and client software. That means a NIP can be optional, draft, final, mandatory or unrecommended. A product's support for a NIP is evidence, not a guarantee of quality.",
                    "Track status and adoption separately. NIP-01 is foundational. NIP-05 and NIP-19 are highly practical. NIP-96 is useful historically but now points you toward Blossom for newer file storage thinking.",
                ]),
                section("Measure relay claims against reality", [
                    "Relay pages can advertise features through NIP-11. Relay monitors can show liveness, latency and discovered URLs. Academic work can show broader patterns such as availability, replication overhead and decentralization limits. None of those views is complete alone.",
                    "When a relay matters to a product, test it directly. Publish, query, authenticate, inspect OK and CLOSED messages, check retention, simulate downtime and compare behavior across clients.",
                ]),
                section("Audit clients by behavior", [
                    "Client claims should be tested through actions: key handling, signer support, relay list behavior, profile fetching, media rendering, search, wallet prompts, moderation controls and export paths. A beautiful UI can still make dangerous key choices.",
                    "The most useful research notes are concrete. Which signer did it use? Which event kinds did it publish? Which relays did it read? What broke in a second client? What warning did the user see?",
                ]),
                section("Watch the media-storage shift", [
                    "File storage is a good example of Nostr drift. NIP-96 described HTTP file storage integration, but the current NIPs index marks it unrecommended in favor of Blossom. Blossom uses HTTP servers, sha256-addressed blobs, Nostr keys and BUD documents.",
                    "A research page should not freeze the ecosystem at the first standard it finds. It should explain the path: why media cannot simply live inside ordinary relays, what NIP-94 describes, why NIP-96 mattered and why Blossom became important.",
                ]),
                section("Build a repeatable note format", [
                    "For every important source, capture the same fields: source type, owner, URL, last checked date, claim, evidence, relevant NIPs, product risk, Crays relevance and open questions. That turns research from browsing into a usable operating memory.",
                    "The Excel workbook already points in this direction by separating NIPs, clients, developer stack, relays, reads and directories. The next level is page-specific synthesis: not just where the link points, but what decision it helps you make.",
                ], [
                    ("Claim", "What is being asserted?"),
                    ("Evidence", "Where can we verify it?"),
                    ("Adoption", "Who actually implements it?"),
                    ("Risk", "What breaks if the claim is wrong?"),
                    ("Product use", "How does this affect Crays.net, venues, commerce or governance?"),
                ]),
                section("End with a decision, not a folder", [
                    "Research should change judgment. After reading, you should know whether a topic is ready for product use, needs a prototype, belongs in the library, needs monitoring or should be avoided for now.",
                    "That is how we keep a 1400-plus page archive useful. Every page should help you decide what to trust, what to test and what to read next.",
                ]),
            ],
            "sources": resource_database_sources + primary_nip_index + research_sources,
            "related": ["resources", "archive-library", "source-inventory", "nips", "relay-market-directory", "deep-dives/blossom-servers-and-relays"],
            "related_label": "Verify the next claim",
            "keywords": ["Nostr research path", "Nostr sources", "Nostr empirical analysis", "Nostr standards"],
            "read": "Reading path",
        },
    }

    depth_additions = {
        "what-is-nostr": [
            section("The client-relay conversation", [
                "Under the friendly app surface, Nostr is a small conversation between clients and relays. A client can send an EVENT message when you publish. It can send a REQ message with filters when it wants posts, profiles, follows, replies or other event kinds. Relays answer with matching EVENT messages, an EOSE marker when stored results are done, and OK or CLOSED messages when they accept, reject or end a subscription.",
                "That message flow matters because it explains why two clients can feel different while reading the same network. One client may query more relays, use better filters, understand more event kinds, cache more aggressively or show clearer errors. The protocol gives the common language; the client still decides how fluent the experience feels.",
            ], [
                ("EVENT", "A signed event sent to or returned by a relay."),
                ("REQ", "A subscription request with filters such as authors, ids, kinds, tags, since, until and limit."),
                ("EOSE", "End of stored events, meaning the relay has finished the historical part of a query."),
                ("OK", "The relay's publish response, including whether an event was accepted."),
            ]),
            section("Addresses you will actually meet", [
                "NIP-19 is one of the most useful beginner standards because it gives human-facing prefixes to different data. npub is a public key. nsec is a private key. note points to an event id. nevent can carry an event plus relay hints. naddr points to addressable events such as long-form articles or replaceable records.",
                "Those prefixes are not decorative. They help products make dangerous and safe values visually distinct. A good interface should make it almost impossible to confuse a public identifier with a signing secret.",
            ]),
            section("NIPs are optional building blocks", [
                "A NIP is a Nostr Implementation Possibility, not a promise that every app supports the feature. NIP-01 is foundational. NIP-05, NIP-07, NIP-19, NIP-23, NIP-47, NIP-57, NIP-65 and NIP-94 are practical pieces you will meet often. Others are narrow, experimental or only useful inside certain products.",
                "That is why we avoid explaining Nostr as one finished product. The network is a standards shelf plus real clients, relays and services that implement different pieces at different quality levels.",
            ]),
            section("Media and money sit next to the core", [
                "The core protocol signs and moves events. Larger media and payments sit next to that core. NIP-94 describes file metadata. NIP-96 described HTTP file storage but is now marked unrecommended in favor of Blossom. Blossom uses sha256-addressed blobs, HTTP servers and Nostr-based authorization. NIP-57 describes zaps, and NIP-47 describes wallet connection.",
                "That gives you a more honest picture: Nostr can carry social identity, references and payment signals, but real products still need storage, wallets, limits, moderation and clear user prompts.",
            ]),
            section("Source trail for the first model", [
                "If you want to verify the model yourself, read the sources in this order. Start with NIP-01 for the event and relay message format. Then read NIP-19 for visible identifiers, NIP-05 for names, NIP-07 for browser signing and NIP-65 for relay lists. Use Nostr.how and the Developer Guide when the raw standards feel too terse.",
            ], cards=[
                ("NIP-01", "Events, signatures, filters and client-relay messages.", "https://github.com/nostr-protocol/nips/blob/master/01.md"),
                ("NIP-19", "npub, nsec, note, nevent and naddr formats.", "https://github.com/nostr-protocol/nips/blob/master/19.md"),
                ("Nostr.how", "Plain-language protocol explanation.", "https://nostr.how/en/the-protocol"),
                ("Developer Guide", "First builder path for clients, libraries and relays.", "https://nostrcg.github.io/devguide/"),
            ]),
        ],
        "why-nostr": [
            section("How this differs from federation", [
                "Mastodon and other federated systems usually bind your account to a server instance. That server has social meaning, policy meaning and technical meaning. You can migrate, but the server remains central to identity and moderation. Nostr takes a different path: the key is the identity, relays are interchangeable infrastructure, and clients are independent interfaces.",
                "That does not make one model universally better. Federation can give stronger local community governance. Nostr gives stronger account portability and client competition. The useful question is which trade-off fits the job in front of you.",
            ]),
            section("Availability is not automatic", [
                "A portable key does not guarantee that every old post is available everywhere. Relays can delete, reject, prune, charge, disappear or fail to replicate. Research on Nostr relay behavior shows that availability and decentralization come with real replication and traffic costs.",
                "So the practical future is not just more relays. It is smarter relay lists, better outbox behavior, paid or community relays where they make sense, monitoring, archival strategy and clients that can explain what is missing.",
            ]),
            section("The trust problem changes shape", [
                "Closed platforms ask you to trust one operator. Nostr asks you to distribute trust across keys, clients, relays, signers, wallets, file servers and social filters. That is not magically easier. It is more inspectable when products are designed well.",
                "You should ask who can impersonate, who can censor, who can lose data, who can see private messages, who can drain a wallet permission and who can make a creator invisible. Nostr gives you more places to move; it also gives you more places to make mistakes.",
            ]),
            section("Where it becomes economically serious", [
                "Nostr becomes serious when identity and value flow connect. A creator can publish under one key, collect zaps, sell access, host long-form work, use media storage, gather fans and later appear inside a venue or award context. A developer can build a better client without owning the whole graph. A relay operator can sell reliability, policy or community context.",
                "For Crays, that means the protocol is not a content trend. It is a way to connect creator demand, member status, venues, payments and governance signals without putting the whole community inside one rented account system.",
            ]),
            section("Evidence to keep open", [
                "Use these links to test the claim instead of trusting the claim. The standards show what can be implemented. The empirical relay paper shows where infrastructure has limits. Lyn Alden's essay explains the broader account-portability thesis in plain economic language.",
            ], cards=[
                ("NIP repository", "The standards shelf and status of each NIP.", "https://github.com/nostr-protocol/nips"),
                ("Relay analysis", "Empirical research on Nostr decentralization and relay availability.", "https://arxiv.org/html/2402.05709v2"),
                ("The Power of Nostr", "Long-form framing of portable identity and open clients.", "https://www.lynalden.com/the-power-of-nostr/"),
                ("Nostr Watch", "Relay discovery and monitoring surface.", "https://nostr.watch"),
            ]),
        ],
        "getting-started": [
            section("A safer client shortlist", [
                "There is no single official Nostr app. Pick based on the job. Damus and Nostur are common iOS paths. Amethyst is a major Android path. Primal gives a polished social and media experience. Coracle leans into communities and web use. Nostrudel is more power-user oriented. Habla and YakiHonne help with long-form and publishing.",
                "The point is not to crown a winner. The point is to see that the account is not the app. Try one simple client first, then a second client with a different shape so you feel portability instead of just reading about it.",
            ]),
            section("The private-key danger pattern", [
                "The most common beginner mistake is treating an nsec like a password field. A normal password can often be rotated after a breach. A leaked private key lets someone sign as you until you move identity and rebuild trust. That is a deeper wound.",
                "Use a signer where possible. If a client requires raw private-key entry, decide whether the client is worth that trust. For throwaway experiments, use a throwaway key. For a real identity, slow down.",
            ]),
            section("Relay settings without panic", [
                "Do not spend the first day optimizing relays. Spend the first day understanding what they do. Later, look at whether your client publishes a NIP-65 relay list, whether it separates read and write relays, and whether it explains why a reply or profile did not appear.",
                "A healthy beginner setup usually has a few dependable general relays plus whatever relays your client discovers from the people you follow. Paid, community or specialized relays can come later when you know why you need them.",
            ]),
            section("Names, profiles and verification", [
                "NIP-05 gives you a human-readable identity such as name@example.com. It helps others recognize your key, especially if the domain is already trusted. It does not prove everything about a person, and it does not recover your key if you lose it.",
                "A good first profile should answer basic trust questions: who are you, where else can people recognize you, what do you publish, and what should they not expect from this key?",
            ]),
            section("Beginner source kit", [
                "Keep these sources open while setting up. They prevent most early confusion: Nostr.how for plain explanations, NIP-19 for key/address formats, NIP-07 and NIP-46 for signers, NIP-65 for relays and NIP-57/NIP-47 for payment flows.",
            ], cards=[
                ("Nostr.how", "Beginner-friendly Nostr explanations.", "https://nostr.how/"),
                ("NIP-07", "Browser signer interface.", "https://github.com/nostr-protocol/nips/blob/master/07.md"),
                ("NIP-46", "Remote signing and Nostr Connect.", "https://github.com/nostr-protocol/nips/blob/master/46.md"),
                ("NIP-65", "Relay list metadata.", "https://github.com/nostr-protocol/nips/blob/master/65.md"),
            ]),
        ],
        "resources": [
            section("The workbook categories behind this page", [
                "The Excel database separates the ecosystem into useful research shelves: core sources, standards and NIPs, clients and apps, developer stack, relays and infrastructure, reads and research, and core directories. That matters because Nostr research fails quickly when everything becomes one flat list.",
                "For example, a NIP tells you a possible data format. A client listing tells you who might implement it. A relay monitor tells you whether infrastructure is alive. A repository tells you whether code exists. A long-form essay tells you why people care. Those are different evidence classes.",
            ]),
            section("What to verify before citing a project", [
                "Before we treat a client, relay or tool as important, we should check more than its name. Look for an official URL, a repository or release page, supported platforms, supported NIPs, signer behavior, relay assumptions, wallet permissions, media storage approach, last visible activity and whether other clients can read the data it creates.",
                "That is the difference between a link directory and a knowledge hub. A directory says where to go. A knowledge hub says what the link means and how much trust it deserves.",
            ]),
            section("Source shelves worth bookmarking", [
                "These are the shelves that should stay close while expanding the archive. The NIPs repository is the protocol shelf. Nostr Apps and Awesome Nostr are discovery shelves. Nostr Watch and relay directories are infrastructure shelves. Developer libraries such as nostr-tools, NDK, rust-nostr and go-nostr are implementation shelves. Long-form research gives judgment and context.",
            ], cards=[
                ("Nostr NIPs", "Primary standards shelf.", "https://github.com/nostr-protocol/nips"),
                ("Nostr Apps", "Client and tool discovery.", "https://www.nostrapps.com/"),
                ("Nostr Watch", "Relay monitoring and discovery.", "https://nostr.watch"),
                ("Awesome Nostr", "Community-maintained project list.", "https://github.com/aljazceru/awesome-nostr"),
            ]),
            section("How to turn links into page depth", [
                "Every strong page should convert sources into explanation. If a page mentions NIP-47, it should explain the wallet permission model. If it mentions Blossom, it should explain sha256 blobs and authorization. If it mentions a relay directory, it should explain what relay quality means. If it mentions a client, it should explain what the client changes for you.",
                "That is the rule I am applying to the Start route now: links are not decoration. They are raw material for facts, trade-offs and examples.",
            ]),
        ],
        "glossary": [
            section("Event kinds you should recognize early", [
                "Kind 0 is profile metadata. Kind 1 is a short text note. Kind 3 is a contact list. Kind 4 was early encrypted direct messages and has been superseded in serious discussions by newer encryption approaches. Kind 10002 is relay list metadata. Long-form articles, badges, zaps, file metadata and many app-specific objects use other kinds.",
                "You do not need to memorize every kind. You need to understand that kind numbers let clients and relays know what sort of signed object they are handling.",
            ]),
            section("Replaceable and addressable events", [
                "Some events are ordinary one-time records. Others are replaceable: a newer event by the same author and kind replaces the older version. Addressable events add a d tag so multiple records of the same kind can exist under stable addresses. That is why naddr exists.",
                "This matters for profiles, relay lists, long-form articles, lists, badges and app data. Without replaceable and addressable behavior, Nostr would be much worse at representing living records.",
            ]),
            section("Status words in the NIP repo", [
                "Mandatory means the base protocol expects it. Optional means software can support it when useful. Draft means the idea is not settled. Final means the document is considered stable. Unrecommended means the ecosystem has a better path or the older path should no longer be preferred.",
                "That last word is important for media. NIP-96 is now marked unrecommended in favor of Blossom, so any serious glossary needs to explain both the older HTTP file-storage path and the newer Blossom direction.",
            ]),
            section("A glossary should protect you from hype", [
                "When you know the words, you can hear sloppy claims. A relay is not a platform. A NIP is not adoption. A signature is not consent if the signer prompt is unreadable. A zap is not a business model. A public key is not a verified human. A file URL is not permanent storage.",
                "This is why the glossary is not a word dump. It is a defense against confusion.",
            ]),
        ],
        "reading-paths/beginner": [
            section("What you should be able to explain after this path", [
                "By the end of the beginner path, you should be able to explain five things without reading notes: what your public key is, why your private key is dangerous, what a relay does, why clients can differ, and what a zap actually proves.",
                "If you can explain those five things, you are no longer just clicking around. You have the base map.",
            ]),
            section("The first wrong turn to avoid", [
                "Do not turn the first week into client collecting. Ten apps with one misunderstood private key is worse than one boring app with safe habits. Nostr rewards curiosity, but it punishes careless key handling.",
                "Your first goal is not maximal freedom. Your first goal is not losing the identity before you understand it.",
            ]),
            section("A beginner's reading stack", [
                "Read in this order if you want the least confusion: What is Nostr, Getting Started, Keys and Identity, Clients, Relays, NIP-05, Zaps and then Privacy. After that, choose whether you are a builder, creator, operator or researcher.",
            ], cards=[
                ("Keys and Identity", "Understand the account model before advanced features.", "/nostr/keys-identity/"),
                ("Clients", "See why the app is not the account.", "/nostr/clients/"),
                ("Relays", "Learn where events are stored and fetched.", "/nostr/relays/"),
                ("Zaps", "Understand Lightning payments as social signals.", "/nostr/nip-57-zaps-lightning/"),
            ]),
        ],
        "reading-paths/developer": [
            section("Protocol first, product second, framework third", [
                "A clean developer path has an order. First understand the wire protocol. Then decide the product behavior. Then choose libraries. Reversing that order creates apps that are library-shaped instead of user-shaped.",
                "For example, NDK can help with relay discovery, caching, signer adapters and subscriptions. That is useful after you know what problem you are asking it to solve.",
            ]),
            section("Relay test matrix", [
                "Test your client against at least three relay personalities: a permissive public relay, a relay that requires auth or payment, and a relay with narrower policy. Publish events, request them back, inspect OK messages, handle CLOSED messages and test missing history.",
                "This will teach you faster than documentation alone. The protocol is simple; the field conditions are messy.",
            ]),
            section("Developer tools that deserve real use", [
                "nostr-tools is a practical JavaScript base. NDK is a higher-level app kit. rust-nostr and go-nostr serve native and server-side stacks. nak is excellent for command-line inspection. nostrdb gives you a serious local database direction. strfry and Khatru help you understand relay implementation from two different angles.",
            ], cards=[
                ("nostr-tools", "Low-level JavaScript utilities.", "https://github.com/nbd-wtf/nostr-tools"),
                ("NDK", "Higher-level Nostr development kit.", "https://github.com/nostr-dev-kit/ndk"),
                ("nak", "Command-line Nostr toolkit.", "https://nak.nostr.com"),
                ("strfry", "High-performance relay implementation.", "https://github.com/hoytech/strfry"),
            ]),
            section("The user-facing errors to design", [
                "A good Nostr app distinguishes between not signed, not accepted, not found, not supported, not authorized and not displayed. Those are different failures. If the UI only says something went wrong, you have hidden the exact thing the user needed to learn.",
                "This is where technical depth becomes product quality.",
            ]),
        ],
        "reading-paths/creator": [
            section("Long-form is not the same as a note", [
                "A short note can survive as a small signed event. A serious essay needs title, summary, tags, publication time, maybe images, comments, highlights and stable references. NIP-23 is the long-form article standard, but clients still differ in how well they render and discover articles.",
                "If you are a creator, test the whole path: draft, publish, share, read in another client, receive comments, receive zaps and archive the media.",
            ]),
            section("Paid access needs more than a zap", [
                "Zaps reward attention. Paid access sells a promise: this buyer gets something, under understandable terms, for a price. That requires receipts, access control, refunds or support rules, content availability and a customer journey that normal people can follow.",
                "Nostr can provide identity, signed events and payment signals. The product must provide the business logic.",
            ]),
            section("Media infrastructure is part of the creator stack", [
                "A creator who depends on images, video or audio must care about storage. NIP-94 file metadata, Blossom servers, upload authorization and mirroring are not backend trivia. They determine whether your work stays visible.",
            ], cards=[
                ("NIP-23", "Long-form article events.", "https://github.com/nostr-protocol/nips/blob/master/23.md"),
                ("NIP-94", "File metadata events.", "https://github.com/nostr-protocol/nips/blob/master/94.md"),
                ("Blossom", "Nostr-aware blob storage.", "https://github.com/hzrd149/blossom"),
                ("Wavlake", "Music and value-for-value culture.", "https://wavlake.com/"),
            ]),
            section("Creator status inside Crays", [
                "For us, the creator path connects profile identity, paid content, fan access, venue moments, awards and status. That is why creator pages need more than social posting. They need an operating path from audience attention to real-world participation.",
            ]),
        ],
        "reading-paths/operator": [
            section("Public, paid, community and venue relays", [
                "A public relay is good for reach but may be noisy. A paid relay can reduce spam and fund storage. A community relay can enforce shared norms. A venue relay can carry local context, access signals and event-specific data. Those are different business and policy objects.",
                "Do not choose a relay type because it sounds decentralized. Choose it because it matches a concrete operational job.",
            ]),
            section("Auth and access are not the same", [
                "NIP-42 relay authentication proves a client controls a key when a relay asks. NIP-98 can sign HTTP requests. Neither one automatically defines who may enter a room, claim a badge, access a paid drop or control a venue tool. Product policy still has to decide that.",
                "That distinction protects operators from overbuilding on top of a cryptographic primitive.",
            ]),
            section("Monitoring checklist", [
                "Before a venue depends on Nostr infrastructure, monitor relay availability, write acceptance, read behavior, retention, auth requirements, media upload success, signer reliability, wallet status and staff fallback procedures.",
            ], cards=[
                ("Nostr Watch", "Relay discovery and monitoring.", "https://nostr.watch"),
                ("NIP-11", "Relay information documents.", "https://github.com/nostr-protocol/nips/blob/master/11.md"),
                ("NIP-42", "Relay authentication.", "https://github.com/nostr-protocol/nips/blob/master/42.md"),
                ("Khatru", "Custom relay framework.", "https://github.com/fiatjaf/khatru"),
            ]),
            section("What operators should not promise early", [
                "Do not promise permanent storage unless you control the storage path. Do not promise private communication unless the encryption and metadata model are understood. Do not promise wallet safety unless permissions and limits are clear. Do not promise moderation-free community unless you are willing to run the consequences in a real room.",
            ]),
        ],
        "reading-paths/culture": [
            section("Why the scene tolerates rough edges", [
                "Many early Nostr users accept rough UX because they value exit, keys, client choice and permissionless building. That does not mean rough UX is good. It means the culture is willing to pay some friction for a different power structure.",
                "A mainstream product cannot simply copy that tolerance. It has to keep the freedom while making the experience calmer.",
            ]),
            section("Funding, grants and public support", [
                "Public support from Bitcoin and open-source circles helped Nostr become more than a hobby protocol. Grants, builder reputation, Jack Dorsey's attention and event culture all shaped the ecosystem. That history matters because it explains why many projects are experimental, public and personality-driven.",
            ]),
            section("Culture sources to read beside the specs", [
                "Specs explain how events work. Culture sources explain why people care enough to build with them. Read conference material, long-form essays, creator tools, zaps, music projects and moderation debates beside the NIPs.",
            ], cards=[
                ("Nostrica", "Conference and culture signal.", "https://nostrica.com/"),
                ("Nostr World", "Nostriga and event material.", "https://nostr.world/"),
                ("The Power of Nostr", "Long-form cultural and economic framing.", "https://www.lynalden.com/the-power-of-nostr/"),
                ("Nostr Apps", "See culture through actual products.", "https://www.nostrapps.com/"),
            ]),
            section("How we should read the culture", [
                "We should keep the energy, not the confusion. The useful part is global community, builder agency, value flow, privacy instincts, creator independence and real-world gatherings. The part to avoid is insider language that makes normal people feel late to a party they were never invited to.",
            ]),
        ],
        "reading-paths/research": [
            section("A claim taxonomy for every page", [
                "Mark each claim as one of five types: standard claim, implementation claim, measurement claim, cultural claim or Crays product claim. A standard claim needs a NIP. An implementation claim needs a repo or live product. A measurement claim needs data. A cultural claim needs context. A product claim needs our own architecture or roadmap logic.",
                "This taxonomy prevents weak writing. It forces every paragraph to know what kind of truth it is trying to tell.",
            ]),
            section("How to research a NIP without fooling yourself", [
                "Read the NIP status, scope and examples. Check whether major clients or libraries implement it. Look for adjacent or superseding NIPs. Then test a small event yourself if the topic is important. Do not infer adoption from existence.",
                "NIP-96 is the perfect warning: it exists, it is useful history, but the NIP table now marks it unrecommended in favor of Blossom. A shallow article would miss that shift.",
            ]),
            section("How to research relays", [
                "Use NIP-11 documents, relay monitors, direct publish/read tests and software repositories together. Relay discovery pages tell you what is visible. Direct tests tell you what happens to your events. Repositories tell you what the operator could be running, not necessarily how it is configured.",
            ]),
            section("How to research clients", [
                "For a client, record platforms, login method, signer support, supported event kinds, relay strategy, wallet flow, media handling, moderation controls, export or migration behavior, visible maintenance and whether data remains legible in other clients.",
            ], cards=[
                ("Nostorg client matrix", "Compare client capabilities.", "https://nostorg.github.io/clients/"),
                ("Nostr Apps", "Find clients and tool categories.", "https://www.nostrapps.com/"),
                ("Nostr Compass", "Project discovery and ecosystem map.", "https://nostrcompass.org/en/projects/"),
                ("Nostrability", "Interoperability testing direction.", "https://github.com/nostrability/nostrability"),
            ]),
            section("The output of good research", [
                "Good research should produce a decision: explain, prototype, monitor, adopt, avoid or archive. A page that only says this exists is not enough. A page should tell you whether the thing is mature, risky, misunderstood, strategically relevant or mainly useful as background.",
            ]),
        ],
    }

    for item in pages:
        rewrite = rewrites.get(item.get("slug"))
        if not rewrite:
            continue
        item.update(rewrite)
        item.setdefault("sections", []).extend(depth_additions.get(item["slug"], []))
