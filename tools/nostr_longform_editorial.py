from __future__ import annotations


DOMAIN_GUIDES = [
    ("relay-selection", "Relay Selection", "choosing where your notes, profile updates, articles and app data are written and read", "relay lists, outbox discovery, paid relays, community relays and fallback behavior", "bad relay choices make a good client feel broken", "Crays needs relay defaults that work for public profiles, venues, creators and local communities"),
    ("outbox-discovery", "Outbox Discovery", "helping clients find the relays where a person actually writes", "NIP-65, write relays, read relays, contact lists and indexers", "global relay guessing wastes time and misses context", "Crays profiles need predictable discovery so fans and venues do not depend on one app"),
    ("relay-moderation", "Relay Moderation", "deciding what a relay stores, rejects, rate-limits or requires payment for", "relay policies, NIP-11 information documents, authentication and reports", "open writing without relay policy becomes spam storage", "Crays venue and creator spaces need moderation rules without pretending the whole protocol is one platform"),
    ("paid-relays", "Paid Relays", "using payment as a spam filter and service model", "admission fees, recurring access, Lightning, relay auth and storage economics", "free relays can become overloaded or hostile to serious publishing", "Crays can use paid or member relays for premium spaces, events and operators"),
    ("local-relays", "Local Relays", "running relays for a place, event, venue or community", "relay topology, geofenced context, local discovery and venue-owned archives", "local context disappears when everything is pushed into one global feed", "Crays World can use local relays for hotels, clubs, meetups and partner venues"),
    ("archival-relays", "Archival Relays", "keeping important Nostr material reachable over time", "storage policy, backups, deletion requests, legal risk and search indexes", "a relay that stores everything also inherits cost and responsibility", "Crays needs archive discipline for articles, awards, creator pages and governance records"),
    ("relay-authentication", "Relay Authentication", "proving to a relay that a request comes from a key holder", "NIP-42, challenge events, scoped access and abuse prevention", "authentication can become confusing if the user sees raw protocol prompts", "Crays should make auth feel like entering a protected room, not signing a strange blob"),
    ("key-backup", "Key Backup", "helping people keep access to their identity without leaking the private key", "nsec storage, encrypted backups, signer recovery and social recovery patterns", "lost keys mean lost identity, while careless backup means stolen identity", "Crays onboarding must treat key backup as a core user journey"),
    ("signer-ux", "Signer UX", "letting apps request signatures without holding the user's secret", "NIP-07, NIP-46, remote signers, bunkers and permission prompts", "bad prompts train people to approve things they do not understand", "Crays should use signers in language that normal users can trust"),
    ("remote-signers", "Remote Signers", "moving signing authority away from random web pages", "Nostr Connect, bunkers, permission scopes and relay-routed signing requests", "a remote signer can improve safety or become a new weak point", "Crays can use remote signing to protect profiles, commerce and governance actions"),
    ("npub-identity", "npub Identity", "making public identity portable across clients and relays", "public keys, bech32 encoding, profiles, NIP-05 and key rotation problems", "a public key is powerful but not friendly by itself", "Crays should show human identity first and expose raw keys only when useful"),
    ("nsec-safety", "nsec Safety", "teaching users that the private key is the account", "private keys, signing, phishing, device storage and backup habits", "one pasted nsec can destroy years of reputation", "Crays should never normalize casual nsec pasting"),
    ("nip05-names", "NIP-05 Names", "connecting a Nostr key to a recognizable internet name", "well-known files, domains, profile verification and trust cues", "verification can be mistaken for endorsement", "Crays can use domain-backed identity for brands, venues, creators and staff"),
    ("profile-metadata", "Profile Metadata", "turning a raw key into a person, brand or place people recognize", "kind 0 metadata, images, names, bios, NIP-05, Lightning addresses and links", "profiles become messy when every client displays different fields", "Crays profiles need consistent public identity across social, commerce and hospitality"),
    ("contact-lists", "Contact Lists", "building a social graph that follows the user", "kind 3 follows, relay hints, mute lists and list-based discovery", "a bad import or noisy follow graph can ruin discovery", "Crays should treat follows as relationship context, not vanity numbers"),
    ("mute-lists", "Mute Lists", "letting people shape what they do not want to see", "NIP-51 lists, client-side filtering, shared lists and moderation boundaries", "mute tools can hide abuse but also hide context", "Crays needs user-level controls for fan, creator and venue spaces"),
    ("web-of-trust", "Web of Trust", "using social distance to improve discovery and reduce spam", "follows, labels, relay choice, graph scoring and reputation signals", "trust scores can become invisible power if they are not explained", "Crays can use trust signals to protect communities without pretending they are absolute truth"),
    ("search-indexing", "Search and Indexing", "making Nostr content findable beyond one client timeline", "NIP-50, indexers, topic tags, relays, public web pages and ranking", "search can centralize attention even on an open protocol", "Crays needs public archive pages that explain topics better than raw event streams"),
    ("long-form-articles", "Long-Form Articles", "publishing essays, guides and books through Nostr events", "NIP-23, kind 30023, Markdown, naddr links and article metadata", "long-form fails if it is treated like a long tweet", "Crays can use long-form structure to become the most useful Nostr reading layer"),
    ("primal-reads", "Primal Reads", "surfacing Nostr long-form articles inside a mainstream client", "kind 30023 feeds, app-level curation, highlights and reader UX", "a reads tab helps discovery but still needs strong editorial context", "Crays should learn from Reads while building original explanatory articles"),
    ("habla-yakihonne", "Habla and YakiHonne", "showing how Nostr publishing can feel like blogging rather than posting", "article clients, Markdown publishing, relay behavior and author identity", "publishing tools must hide complexity without hiding ownership", "Crays can connect creator articles, paid access and public archive pages"),
    ("highlights", "Highlights", "saving and sharing the parts of articles that matter", "NIP-84, article references, annotations, lists and reader identity", "highlights become noise if they are not tied to context", "Crays can turn highlights into reading paths and fan knowledge trails"),
    ("comments-on-articles", "Comments on Articles", "letting long-form content have conversation without becoming a random reply pile", "NIP-22, event references, moderation and client rendering", "comments need context, rules and visibility choices", "Crays can use comments for creator articles, award debates and member spaces"),
    ("wiki-events", "Wiki Events", "using Nostr for collaborative knowledge pages", "NIP-54, replaceable wiki events, topics, editors and competing versions", "wiki pages can fragment if authorship and versioning are unclear", "Crays can use wiki patterns for living Nostr explainers and operating manuals"),
    ("video-events", "Video Events", "bringing video identity, metadata and discussion into Nostr", "NIP-71, media references, live chat, zaps and storage choices", "video needs storage, moderation and bandwidth planning", "Crays can use video for creators, events, venues and education"),
    ("live-activities", "Live Activities", "coordinating real-time broadcasts and audience interaction", "NIP-53, live event metadata, chat, relays and zaps", "live rooms can fail when discovery and moderation are weak", "Crays events can use live activity patterns for awards, venue streams and creator sessions"),
    ("audio-voice", "Audio and Voice", "adding voice rooms, podcasts and spoken context to Nostr", "audio clients, live activities, media storage and value-for-value payments", "audio feels personal but needs trust, recording rules and moderation", "Crays can use audio for creator talks, venue rooms and community calls"),
    ("music", "Music on Nostr", "connecting artists, listeners and value directly", "track metadata, zaps, playlists, Wavlake-style flows and profile identity", "music needs rights, attribution and payment clarity", "Crays can connect music, events, venues and fan support"),
    ("photos", "Photos on Nostr", "building visual identity without locking photos into one app", "image metadata, Blossom, NIP-94, feeds and creator profiles", "photos create privacy and moderation pressure fast", "Crays can use photo flows for lifestyle, venues, creators and event proof"),
    ("blossom-storage", "Blossom Storage", "storing media blobs outside relays while keeping Nostr identity involved", "BUDs, hash-addressed blobs, user server lists and upload authorization", "media breaks when one URL is the only copy", "Crays can use Blossom-style storage for creator media, venue imagery and long-term archives"),
    ("nip96-storage", "NIP-96 Storage", "describing HTTP file storage services for Nostr clients", "server descriptors, upload APIs, auth and NIP-94 metadata", "file uploads need limits, policy and lifecycle rules", "Crays needs file storage that fits public pages, paid content and event media"),
    ("file-metadata", "File Metadata", "describing files as signed Nostr events", "NIP-94, hashes, URLs, MIME types, dimensions and media references", "metadata is not the same as hosting the file", "Crays can make media portable while keeping file handling explicit"),
    ("wallet-connect", "Nostr Wallet Connect", "letting apps ask wallets to pay without becoming wallets themselves", "NIP-47, permissions, budgets, invoices and wallet services", "wallet permissions must be understandable or users will over-authorize", "Crays can use wallet connect for zaps, access, bookings and creator payments"),
    ("zaps", "Zaps", "turning appreciation into a visible Lightning payment and social signal", "NIP-57, zap requests, zap receipts, LNURL and relay announcements", "zaps can look simple while hiding several moving parts", "Crays can use zaps for fans, creators, awards and event energy"),
    ("cashu-wallets", "Cashu Wallets", "bringing ecash-style wallet state into Nostr apps", "NIP-60, encrypted wallet events, token proofs and mint trust", "wallet portability does not remove mint risk", "Crays should treat ecash as a specialist payment layer, not a casual badge"),
    ("nutzaps", "Nutzaps", "sending Cashu value as the payment itself", "NIP-61, trusted mints, P2PK locks, token events and redemption history", "a token sent to the wrong mint or key can be burned", "Crays can watch Nutzaps for future privacy-sensitive fan payments"),
    ("zap-goals", "Zap Goals", "making funding targets public and interactive", "NIP-75, goals, zaps, progress, relays and profile display", "public goals need trust and fulfilment clarity", "Crays can use goals for creator campaigns, events and open-source work"),
    ("marketplaces", "Marketplaces", "using signed listings instead of one marketplace database", "NIP-15, NIP-99, product metadata, payments and buyer-seller reputation", "marketplaces need dispute handling, not just listings", "Crays can connect listings to content sale, venues and member commerce"),
    ("classified-listings", "Classified Listings", "publishing items or services as portable events", "NIP-99, location, price, contact, relays and search", "a listing is not a checkout or trust system", "Crays can use listings for local opportunities, venue offers and creator services"),
    ("communities", "Communities", "creating topic spaces with rules and moderators", "NIP-72, community definitions, approval, relay hints and moderation", "community UX fails if rules and visibility are vague", "Crays can use communities for fans, venues, operators and award groups"),
    ("relay-groups", "Relay Groups", "letting relays support group-like spaces", "NIP-29, group metadata, membership, moderation and relay authority", "groups can become platform-like if users cannot leave with identity intact", "Crays can use group patterns where local authority is useful"),
    ("labels", "Labels", "attaching meaning, warnings or categories to events and profiles", "NIP-32, label namespaces, moderation, recommendations and machine reading", "labels can help or harm depending on who applies them", "Crays can use labels for content types, venue states and safety signals"),
    ("reports", "Reports", "telling clients and relays about abuse or risk", "NIP-56, report events, moderation queues and user controls", "reports are signals, not automatic truth", "Crays needs reporting flows for public pages, fans and operator spaces"),
    ("badges", "Badges", "representing status, proof or recognition in a portable way", "NIP-58, issuers, awards, profile display and trust", "badges lose meaning when they are random decoration", "Crays must distinguish earned status, bought status and official awards"),
    ("polls", "Polls", "asking a community to choose without losing the identity layer", "NIP-88, poll events, options, votes and client support", "polls need Sybil resistance and context", "Crays can use polls for soft signals before formal governance"),
    ("calendar-events", "Calendar Events", "representing meetings, launches and physical events", "NIP-52, date-based events, time zones, RSVPs and discovery", "events need accurate time, place and update handling", "Crays can connect venues, creators and guests through calendar events"),
    ("user-status", "User Status", "showing what a person is doing or signaling right now", "NIP-38, status events, music, presence and ephemeral context", "status can become noise or leak presence", "Crays can use status carefully for creators, venues and operators"),
    ("app-handlers", "App Handlers", "letting users choose which app opens which Nostr object", "NIP-89, handlers, recommendations, deep links and client routing", "the best protocol object is useless if no app opens it well", "Crays should route readers to the right experience without trapping them"),
    ("app-specific-data", "App-Specific Data", "letting apps store portable state without pretending every app must understand it", "NIP-78, replaceable records, encrypted content and app namespaces", "app data can become hidden lock-in if undocumented", "Crays can use app data for preferences while keeping public identity portable"),
    ("data-vending", "Data Vending Machines", "buying computation or data processing through Nostr requests", "NIP-90, job requests, results, feedback and payment coordination", "DVM markets need quality signals and payment clarity", "Crays can watch DVMs for AI, research and creator tooling"),
    ("ai-agents", "AI Agents on Nostr", "using signed events as an open coordination layer for tools and agents", "NIP-90, NIP-78, task events, memory, permissions and payments", "agents need bounded authority and audit trails", "Crays can use agent patterns for research, moderation support and operator workflows"),
    ("http-auth", "HTTP Auth", "using Nostr signatures to authorize ordinary web services", "NIP-98, request signing, replay protection and service integration", "web auth must not trick users into signing broad permissions", "Crays can use HTTP auth for member areas, APIs and paid content"),
    ("login-with-nostr", "Login with Nostr", "entering services with key-based identity instead of passwords", "NIP-07, NIP-46, NIP-98 and profile linking", "login is only safe when signing prompts are clear", "Crays can use Nostr login for profiles, creators and operators"),
    ("direct-messages", "Direct Messages", "sending private conversation in a public-relay world", "NIP-04, NIP-17, NIP-44, NIP-59 and metadata limits", "encryption does not hide every social fact", "Crays should explain messaging privacy honestly"),
    ("gift-wraps", "Gift Wraps", "wrapping private events so clients can route them with less leakage", "NIP-59, rumors, seals, gift wraps and relay delivery", "private delivery can still leak timing and relationships", "Crays can use modern messaging patterns where privacy matters"),
    ("encryption", "Encryption", "protecting content while accepting that relays are transport", "NIP-44, key agreement, payload encryption and client warnings", "bad encryption UX gives people false confidence", "Crays should treat private features as product safety work"),
    ("deletion", "Deletion Requests", "asking relays and clients to stop showing a past event", "NIP-09, relay policy, replaceable events and realistic expectations", "deletion on an open network is a request, not a time machine", "Crays should be plain about what can and cannot be erased"),
    ("expiration", "Expiration", "making events intentionally temporary", "NIP-40, expiration tags, relay support and client behavior", "temporary content is only temporary where relays respect it", "Crays can use expiration for offers, events and ephemeral status"),
    ("protected-events", "Protected Events", "limiting who should be able to see or use certain event data", "NIP-70, access patterns, encryption and client respect", "protection fails if clients treat hints as hard security", "Crays should separate privacy, access and visibility in the UI"),
    ("proof-of-work", "Proof of Work", "adding cost to publishing as a spam control", "NIP-13, difficulty targets, clients and relay policies", "proof of work can punish low-power users if used crudely", "Crays may use it only where it improves abuse resistance without hurting normal readers"),
    ("negentropy", "Negentropy Sync", "efficiently comparing sets of events between clients and relays", "NIP-77, set reconciliation, sync cost and archive repair", "sync details are invisible until things are missing", "Crays archive tooling can benefit from efficient reconciliation ideas"),
    ("relay-counts", "Relay Counts", "asking relays for counts before fetching everything", "NIP-45, counts, filters and search-like interfaces", "counts can mislead when relays have different policies", "Crays can use counts as signals, not as absolute truth"),
    ("relay-management", "Relay Management", "operating relays through structured commands", "NIP-86, admin APIs, moderation and maintenance", "management power must be protected carefully", "Crays Super Nodes need operational tooling with clear roles"),
    ("git-on-nostr", "Git on Nostr", "mapping software collaboration to signed social objects", "NIP-34, repositories, patches, issues and developer identity", "developer tools need workflows, not just event formats", "Crays can use Git-on-Nostr ideas for transparent product development"),
    ("software-reputation", "Software Reputation", "understanding which clients, relays and tools deserve trust", "open-source activity, signatures, issue history, audits and user reports", "a shiny app can still be unsafe", "Crays should teach readers how to evaluate tools before trusting keys"),
    ("open-source-funding", "Open-Source Funding", "supporting protocol work without turning it into a company roadmap", "grants, zaps, sponsorships, public goods and maintainer time", "funding influences priorities even when code is open", "Crays can support builders while staying clear about incentives"),
    ("onboarding", "Onboarding", "getting a person from curiosity to a safe first session", "client choice, key creation, backups, signers, relays and first follows", "too much protocol vocabulary loses the reader", "Crays should make first use feel calm and owned"),
    ("client-switching", "Client Switching", "moving between apps without losing identity", "portable keys, relay lists, app handlers, cached content and feature support", "portability feels broken when clients implement different pieces", "Crays should explain what follows the user and what does not"),
    ("mobile-clients", "Mobile Clients", "using Nostr where most normal users actually live", "push notifications, background sync, media uploads, key storage and app stores", "mobile convenience can increase custody risk", "Crays mobile flows need signer safety and plain permissions"),
    ("web-clients", "Web Clients", "using Nostr from a browser without handing the browser every secret", "NIP-07, extensions, remote signers, session state and CSP", "browser UX can normalize dangerous key entry", "Crays web pages should never ask for secrets casually"),
    ("desktop-clients", "Desktop Clients", "serving power users who need control and local state", "local databases, relay management, offline reading and advanced filters", "desktop power can become intimidating", "Crays can point expert readers toward serious tooling without making beginners feel lost"),
    ("feed-design", "Feed Design", "deciding what a user sees when many relays send many events", "ranking, follows, web-of-trust, topics, lists and mute rules", "feeds shape reality even when the protocol is open", "Crays should design feeds around intent: learn, follow, buy, attend or govern"),
    ("notifications", "Notifications", "telling users what matters without turning Nostr into noise", "mentions, replies, zaps, DMs, follows, relay delivery and push services", "bad notifications make good networks feel hostile", "Crays needs notification classes for creators, fans, venues and operators"),
    ("bookmarks", "Bookmarks", "saving events, articles and resources for later", "NIP-51, private lists, public lists and app rendering", "bookmarks become useful only when they can be found again", "Crays can turn bookmarks into reading paths and member knowledge"),
    ("topics-hashtags", "Topics and Hashtags", "connecting content to subjects without central categories", "t tags, search, spam, client rendering and topic feeds", "hashtags invite both discovery and manipulation", "Crays should use topic labels as reader paths, not gimmicks"),
    ("seo-public-web", "SEO and the Public Web", "making Nostr knowledge visible outside Nostr clients", "canonical pages, NIP-23 mirrors, schema, internal links and topic clusters", "raw event content rarely wins search by itself", "Crays must write better explanations than scattered protocol snippets"),
    ("nostr-vs-activitypub", "Nostr vs ActivityPub", "comparing key-based identity with instance-based federation", "servers, relays, accounts, moderation and migration", "people confuse both because both reject one-company social media", "Crays should explain the difference without cheerleading"),
    ("nostr-vs-bluesky", "Nostr vs Bluesky", "comparing Nostr with AT Protocol and app-led social portability", "identity, relays, PDS, clients, moderation and governance", "protocol comparisons become tribal when they ignore user experience", "Crays can use comparisons to clarify product choices"),
    ("nostr-vs-web3", "Nostr vs Web3", "explaining why Nostr is not a token-first social system", "keys, relays, events, Bitcoin adjacency and absence of consensus", "calling everything web3 confuses the architecture", "Crays should explain the non-token nature of Nostr clearly"),
    ("bitcoin-relationship", "Bitcoin Relationship", "understanding why Bitcoin people adopted Nostr early", "Lightning, zaps, censorship resistance, open-source culture and sovereignty", "Nostr is not Bitcoin and not a blockchain", "Crays can use Bitcoin overlap where payments and culture actually matter"),
    ("lightning-wallets", "Lightning Wallets", "connecting Nostr attention to actual value movement", "LNURL, NWC, hosted wallets, self-custody, invoices and receipts", "wallet UX can hide custody and compliance questions", "Crays should make payment roles visible and honest"),
    ("creator-economy", "Creator Economy", "letting creators keep identity, audience and payment paths", "profiles, long-form, zaps, paid content, badges and fan lists", "creator tools fail when they only copy social feeds", "Crays can connect content sale, status, events and fan participation"),
    ("venue-identity", "Venue Identity", "making real-world places recognizable in an open social graph", "NIP-05, profiles, calendar events, local relays and operator roles", "places need official identity and staff boundaries", "Crays World can give venues social identity without locking them into one platform"),
    ("event-access", "Event Access", "connecting tickets, presence, content and status", "signed identity, zaps, calendars, badges and local relay context", "attendance data can become sensitive", "Crays can tie events to creators, venues and awards with care"),
    ("governance", "Governance", "moving from attention to decisions without losing accountability", "membership, polls, badges, votes, attestations and legal rules", "protocol votes are not legal governance by themselves", "Crays DAO readiness needs both signed participation and formal structure"),
    ("legal-risk", "Legal Risk", "remembering that open protocols do not erase product law", "content policy, payments, minors, privacy, consumer rights and jurisdiction", "decentralization is not a legal shield", "Crays must treat legal design as product design"),
    ("privacy-model", "Privacy Model", "understanding what Nostr hides and what it exposes", "public keys, metadata, relays, encryption, timing and payment traces", "people confuse encryption with anonymity", "Crays should teach privacy in practical user language"),
    ("threat-modeling", "Threat Modeling", "thinking through what can attack a Nostr user or product", "phishing, malicious clients, relay logs, key theft, spam and social engineering", "the worst risks often look like normal UX", "Crays should make threat models readable for non-security people"),
    ("spam-defense", "Spam Defense", "keeping open writing usable when anyone can publish", "paid relays, proof of work, web-of-trust, reports, mutes and filters", "spam defense can become censorship if the layers are blurred", "Crays needs separate controls for user choice, venue policy and official moderation"),
    ("analytics", "Analytics", "measuring Nostr activity without pretending relays are one database", "relay sampling, event kinds, public metrics, privacy and indexer bias", "numbers can lie when relay coverage is incomplete", "Crays should explain what a metric can and cannot prove"),
    ("data-portability", "Data Portability", "moving identity and content across apps and services", "keys, event formats, relays, exports, importers and app-specific data", "portability depends on support, not slogans", "Crays should show which parts are portable in each workflow"),
    ("education", "Nostr Education", "teaching the protocol without drowning people in acronyms", "layered explanations, examples, diagrams, glossaries and reading paths", "education fails when every answer starts with a NIP number", "Crays should be the calm home base for every reader level"),
]


CULTURE_GUIDES = [
    ("nostrich-culture", "Nostrich Culture", "the jokes, rituals, status games and insider language that make Nostr feel like a living scene", "memes, follows, zaps, public keys, client choice and repeated community stories", "culture pages can become empty hype if they ignore the technical habits underneath", "Crays can translate scene behavior into useful context for people arriving from outside"),
    ("purple-pilling", "Purple Pilling", "the social art of helping someone understand Nostr without drowning them in protocol talk", "onboarding flows, first follows, key safety, app selection and relay defaults", "enthusiasm can push newcomers into unsafe key handling or jargon fatigue", "Crays should make the first serious explanation feel inviting rather than missionary"),
    ("reply-guy-dynamics", "Reply Guy Dynamics", "how open replies, quote posts and attention seeking behave when there is no single platform owner", "kind 1 notes, replies, mentions, mutes, reports, client filters and relay policy", "open conversation can become noisy if product design rewards the loudest behavior", "Crays can explain how communities protect discussion without pretending speech is centrally owned"),
    ("zap-flexing", "Zap Flexing", "why public payments can become appreciation, status, flirtation, proof, funding and performance at the same time", "NIP-57 receipts, Lightning invoices, comments, leaderboards and wallet UX", "payment signals can become social pressure when readers do not know what is real", "Crays should teach zaps as both money movement and public culture"),
    ("client-tribes", "Client Tribes", "why people identify with Damus, Primal, Amethyst, Iris, Coracle, Yakihonne or smaller tools", "supported NIPs, design taste, platform limits, relay defaults and creator workflows", "app loyalty can hide interoperability gaps and turn product feedback into tribal arguing", "Crays can compare client cultures without flattening them into winners and losers"),
    ("relay-politics", "Relay Politics", "the quiet power of relay operators, allow lists, block lists, paid access and storage rules", "NIP-11 documents, relay auth, moderation events, payment gates and relay directories", "people may think a relay is neutral just because the protocol is open", "Crays can make relay policy visible for venues, creators and public archives"),
    ("app-rivalries", "App Rivalries", "how competing Nostr clients copy, challenge and pressure each other", "feature support, UI conventions, NIP adoption, social migration and funding incentives", "rivalry becomes unhelpful when readers lose sight of portable identity", "Crays can turn product drama into lessons about what actually works across clients"),
    ("founder-mythology", "Founder Mythology", "the stories people tell about early builders, early mistakes and the identity of the protocol", "public Git history, NIP authorship, client launches, funding moments and conference talks", "myth can replace evidence if a community only repeats origin stories", "Crays should respect early work while keeping the archive grounded in practical understanding"),
    ("npub-reputation", "npub Reputation", "how a public key becomes a recognizable person, brand, coder, artist or venue", "profiles, NIP-05, follows, badges, zaps, long-form articles and public work", "a strong npub can become mistaken for unquestionable authority", "Crays can help readers separate reputation, proof, taste and trust"),
    ("pseudonymous-fame", "Pseudonymous Fame", "why people can become known through keys and contributions without using a legal identity", "public keys, signing history, NIP-05 names, contribution trails and social graph signals", "pseudonymity can protect people or make accountability harder", "Crays should explain how trust is built through behavior, not only real-name identity"),
    ("bitcoin-crossover", "Bitcoin Crossover", "why Bitcoiners helped Nostr grow and where the overlap is useful or distracting", "Lightning, zaps, censorship resistance, open-source funding and sovereignty language", "Bitcoin culture can make Nostr feel narrower than it really is", "Crays can keep the payment connection without making every Nostr story a Bitcoin story"),
    ("open-source-celebrities", "Open-Source Celebrities", "how maintainers, library authors and protocol contributors become public figures", "GitHub activity, NIPs, client releases, conference talks, zaps and social visibility", "celebrity can distort technical judgment when popularity is treated as review", "Crays can honor builders while teaching readers how to inspect the work"),
    ("conference-hallway-nostr", "Conference Hallway Nostr", "how meetups, Bitcoin events and side conversations shape the protocol's social memory", "calendar events, badges, photos, zaps, live activities and follow graphs", "important context can stay trapped in private rooms and scattered notes", "Crays can turn event culture into public, searchable memory"),
    ("maker-launches", "Maker Launches", "the culture of shipping small Nostr tools in public before they are polished", "prototype clients, NIP experiments, Git-on-Nostr, zaps, feedback loops and relay testing", "fast shipping can confuse readers if experiments are presented as finished infrastructure", "Crays can help people read launches as signals, not guarantees"),
    ("product-shipping-culture", "Product Shipping Culture", "why Nostr rewards builders who explain their trade-offs in public", "release notes, NIP support, issue threads, client screenshots and migration stories", "shipping culture becomes noise when every minor feature is framed as a revolution", "Crays can separate meaningful product changes from timeline heat"),
    ("meme-culture", "Meme Culture", "how jokes, screenshots and running references carry Nostr identity", "short notes, image hosting, reposts, reaction events, zaps and topic tags", "memes can welcome people or make the scene feel closed", "Crays can explain insider language without making newcomers feel outside"),
    ("censorship-drama", "Censorship Drama", "how bans, app-store pressure, relay blocking and moderation fights become protocol education", "client distribution, relay choice, content policy, app-store rules and public mirrors", "drama can make every moderation decision look like censorship", "Crays should explain the layers so readers can judge each incident calmly"),
    ("moderation-drama", "Moderation Drama", "why an open protocol still needs rules, filters, mutes and community boundaries", "reports, labels, relays, client-side filtering, communities and web-of-trust signals", "people can confuse no central platform with no responsibility", "Crays can show moderation as a layered product design problem"),
    ("deplatforming-stories", "Deplatforming Stories", "why people who lost reach elsewhere become interested in portable identity", "key-based accounts, relay diversity, public web mirrors and long-form publishing", "a deplatforming story can oversimplify hard legal or safety questions", "Crays can make the portability lesson clear without romanticizing every conflict"),
    ("scene-gossip-with-care", "Scene Gossip with Care", "how to understand rumors, public disputes and social signals without turning the archive into a tabloid", "public notes, signed receipts, deleted events, screenshots, relays and reputation trails", "gossip can create harm when speculation is treated as fact", "Crays can cover scene dynamics as analysis, not character assassination"),
    ("screenshots-and-receipts", "Screenshots and Receipts", "why signed events change the meaning of receipts, callouts and public memory", "event IDs, signatures, deletion requests, relays, screenshots and archive mirrors", "screenshots can outlive context and signed events can still be misread", "Crays can teach readers how to verify before they amplify"),
    ("public-feuds", "Public Feuds", "how arguments between builders, clients or communities reveal protocol trade-offs", "replies, quote posts, long-form responses, labels, reports and app rendering", "feuds can turn technical disagreement into identity warfare", "Crays can extract the useful lesson without feeding the conflict"),
    ("forks-and-schisms", "Forks and Schisms", "why open ecosystems split, fork and recombine around standards and taste", "NIP proposals, client forks, relay policy, funding priorities and social migration", "a fork can be healthy experimentation or just unresolved governance", "Crays can explain forks as part of open development rather than automatic failure"),
    ("funding-rumors", "Funding Rumors", "how grants, donations, investors and sponsorships shape what gets built", "OpenSats-style grants, zaps, VC money, foundation support and public roadmaps", "money stories become toxic when incentives are hidden or exaggerated", "Crays can ask what funding changes for users, builders and independence"),
    ("grant-culture", "Grant Culture", "the public-good side of Nostr where maintainers need time, not only applause", "open-source grants, zaps, sponsorships, maintenance work and contributor burnout", "grant culture can create dependency or resentment if expectations stay vague", "Crays can frame funding as infrastructure care"),
    ("nostr-journalism", "Nostr Journalism", "how reporters, analysts and independent writers can publish without platform lock-in", "NIP-23 articles, zaps, NIP-05 identity, source protection, comments and public mirrors", "publishing freedom does not remove editorial standards", "Crays can make Nostr useful for serious reporting and scene explanation"),
    ("creator-diaries", "Creator Diaries", "why personal logs, build notes and behind-the-scenes writing fit Nostr long-form", "kind 30023 articles, highlights, comments, zaps and profile identity", "diary-style content can become scattered if it lacks structure", "Crays can turn creator notes into readable paths for fans"),
    ("artist-communities", "Artist Communities", "how visual artists, musicians and makers use portable identity to keep audiences close", "profiles, media storage, zaps, marketplaces, galleries, badges and event pages", "art communities need rights, attribution and moderation, not only open posting", "Crays can connect artists to venues, sales and fan status"),
    ("music-scenes", "Music Scenes", "how musicians, listeners, venues and value-for-value habits meet on Nostr", "Wavlake-style flows, zaps, profiles, playlists, live activities and event pages", "music culture needs licensing clarity and audience trust", "Crays can make music part of real-world venue and creator flows"),
    ("photography-scenes", "Photography Scenes", "how photo-first culture pressures Nostr's media, discovery and privacy layers", "Blossom, NIP-94, image metadata, feeds, EXIF risk and profile identity", "beautiful media can leak location or depend on fragile hosts", "Crays can explain photo publishing as lifestyle and infrastructure"),
    ("travel-and-nostr", "Travel and Nostr", "how portable profiles and local relays can make cities, meetups and venues easier to discover", "hashtags, calendar events, local relays, maps, venue profiles and recommendations", "location context can help discovery and expose private patterns", "Crays can connect travel content to real places without trapping the social graph"),
    ("local-meetups", "Local Meetups", "why small local gatherings matter in a global protocol", "calendar events, NIP-05 names, local relays, photos, RSVP flows and badges", "meetups can become invisible if they live only in one client feed", "Crays can make local Nostr activity findable for guests and operators"),
    ("nostr-bars-and-venues", "Nostr Bars and Venues", "how physical spaces can become social nodes with keys, events and recurring communities", "venue profiles, local relays, calendars, zaps, badges and content walls", "a venue identity needs staff control and clear rules", "Crays World can make hospitality spaces legible in the Nostr graph"),
    ("dating-and-social-discovery", "Dating and Social Discovery", "how identity, reputation and social graph portability could affect personal discovery", "profiles, follows, labels, private messages, mutes and local context", "social discovery can become unsafe when privacy and moderation are weak", "Crays should treat this as a sensitive design area, not a gimmick"),
    ("family-and-private-circles", "Family and Private Circles", "why ordinary people ask whether Nostr can handle small trusted groups", "gift wraps, private lists, communities, encryption, media and relay choice", "private family context can leak through metadata and bad clients", "Crays can explain where Nostr is ready and where caution is needed"),
    ("education-workshops", "Education Workshops", "how teachers, meetups and communities can make Nostr learnable", "reading paths, glossaries, demos, signer flows, long-form articles and local events", "workshops fail when they start with implementation detail instead of reader questions", "Crays can become the curriculum layer for public Nostr education"),
    ("migration-stories", "Migration Stories", "what people learn when they move from Twitter, Mastodon, Bluesky, Substack or Discord", "identity migration, follows, content import, client switching and public web pages", "migration promises disappoint when people expect exact copies of old platforms", "Crays can explain what changes and what does not travel"),
    ("nostr-as-third-place", "Nostr as a Third Place", "how casual hanging out, discovery and recurring conversation create belonging", "feeds, replies, zaps, rooms, local relays, communities and live activities", "a third place needs norms, not only open access", "Crays can describe the social layer without losing the product layer"),
    ("microfame-and-status", "Microfame and Status", "how small audiences, high-signal builders and zap culture create status without mass scale", "follows, zaps, badges, replies, conference visibility and contribution history", "status can distort conversation when readers chase signals instead of substance", "Crays can teach readers how to read status without being ruled by it"),
    ("badge-status-games", "Badge Status Games", "how badges can mean proof, honor, access, joke or vanity depending on issuer and context", "NIP-58 awards, issuer trust, profile rendering, event access and community norms", "badges become meaningless when every symbol looks official", "Crays can separate official status from playful culture"),
    ("zap-leaderboards", "Zap Leaderboards", "why ranking payments can motivate communities and also bend incentives", "zap receipts, aggregation, profiles, public goals and display choices", "leaderboards can reward performance instead of real value", "Crays can use rankings only where the meaning is clear"),
    ("community-moderators", "Community Moderators", "the people who keep open spaces usable without owning the whole network", "NIP-72 communities, reports, labels, relay policy, mute lists and social norms", "moderators become invisible until something goes wrong", "Crays can make moderation roles understandable and accountable"),
    ("operator-personalities", "Operator Personalities", "why relay operators, indexer maintainers and infrastructure people become trusted names", "relay uptime, policy transparency, public support, payment models and incident response", "infrastructure charisma can hide operational weakness", "Crays can help readers inspect reliability without needing to run a relay"),
    ("wallet-brand-trust", "Wallet Brand Trust", "how wallets become social trust objects when payments move through public conversation", "NWC, zaps, Lightning addresses, hosted wallets, custody language and support history", "wallet popularity is not the same as safety", "Crays can teach readers to ask custody and permission questions first"),
    ("client-design-taste", "Client Design Taste", "why interface style matters in a protocol community that often talks like design is secondary", "onboarding, feed density, signing prompts, error copy, mobile layout and empty states", "good protocol ideas fail when the interface feels punishing", "Crays should evaluate apps through reader experience as much as feature lists"),
    ("old-web-nostalgia", "Old Web Nostalgia", "why Nostr often feels like blogs, forums, RSS, IRC and personal websites returning in new form", "long-form articles, relays, open clients, personal domains and portable identity", "nostalgia can hide the new risks of keys, wallets and public metadata", "Crays can use old-web language to make Nostr warmer and easier to grasp"),
    ("anti-algorithm-culture", "Anti-Algorithm Culture", "why many Nostr users distrust engagement-ranking feeds", "follows, web-of-trust, relay choice, mute lists, topics and client ranking", "no central algorithm does not mean no curation", "Crays can explain curation as an explicit user and product choice"),
    ("protocol-maximalism", "Protocol Maximalism", "the belief that open standards should matter more than any one app", "NIPs, interoperability, client switching, relay diversity and public-good funding", "maximalism can become dogma when it ignores normal user pain", "Crays can keep the standard high while staying practical"),
    ("practical-sovereignty", "Practical Sovereignty", "what ownership actually means when a person still needs apps, relays, wallets and backups", "keys, signers, relays, backups, domains, payments and recovery paths", "sovereignty language can become empty if the product makes users fragile", "Crays can define ownership through usable routines"),
    ("lurkers-and-readers", "Lurkers and Readers", "the quiet majority who read, bookmark, search and learn without posting much", "public web pages, long-form, bookmarks, search, follows and private lists", "archives built only for posters miss the people who learn silently", "Crays should serve readers as first-class Nostr participants"),
    ("social-graph-drama", "Social Graph Drama", "how follows, unfollows, lists and recommendations become personal even when they are just events", "kind 3 contacts, NIP-51 lists, follows, mutes, recommendations and graph scoring", "relationship data can be read as endorsement or betrayal", "Crays can explain graph signals without moral panic"),
    ("nostr-language", "Nostr Language", "the shorthand words people use: npub, nsec, zap, relay, signer, bunker, note and nostrich", "glossaries, UI copy, onboarding, app labels and documentation habits", "inside language can make the archive feel closed to newcomers", "Crays can translate without stripping away the culture"),
    ("longform-salon", "Longform Salon", "how essays, replies, highlights and comments can create a slower reading culture", "NIP-23, highlights, comments, bookmarks, author identity and reader paths", "long-form becomes invisible if discovery is only feed-based", "Crays can make serious reading feel like a central Nostr activity"),
    ("public-brain", "Public Brain", "why notes, articles, bookmarks and highlights can become a personal knowledge system", "replaceable events, lists, highlights, search, NIP-23 and profile identity", "a public knowledge trail can reveal more than the writer intended", "Crays can teach people how to publish and remember with care"),
    ("nostr-fandoms", "Nostr Fandoms", "how creators, projects and products attract passionate small communities", "follows, zaps, badges, mentions, communities, events and long-form updates", "fandom can support builders or pressure them into theater", "Crays can show how enthusiasm becomes sustainable participation"),
]


ALL_GUIDES = DOMAIN_GUIDES + CULTURE_GUIDES
CULTURE_SLUGS = {slug for slug, *_rest in CULTURE_GUIDES}


PERSONAS = [
    ("beginner", "Newcomer", "you are trying to understand Nostr without becoming a protocol engineer on day one", "plain examples, warnings and a safe first path"),
    ("creator", "Creator", "you care about audience, publishing, payments and ownership", "content, fans, zaps, status and long-term identity"),
    ("developer", "Developer", "you need enough depth to build without guessing", "event kinds, relays, signing, client behavior and failure cases"),
    ("relay-operator", "Relay Operator", "you run infrastructure and need sane policy", "storage, abuse, auth, payment, backups and legal boundaries"),
    ("designer", "Designer", "you need to make ownership understandable", "language, prompts, onboarding, empty states and mental models"),
    ("wallet-builder", "Wallet Builder", "you connect payments to signed social context", "NWC, zaps, Cashu, permissions and user trust"),
    ("venue-operator", "Venue Operator", "you connect online identity to real places", "local relays, events, bookings, access and reputation"),
    ("community-lead", "Community Lead", "you need groups that feel alive without becoming trapped in one app", "moderation, discovery, lists, badges and trust"),
    ("investor", "Investor", "you need to separate protocol value from product hype", "adoption signals, infrastructure risk, incentives and moats"),
    ("security-reviewer", "Security Reviewer", "you look for what can break, leak or mislead users", "keys, signatures, relays, permissions and social engineering"),
]


PERSONA_TOPIC_SLUGS = [
    "relay-selection",
    "outbox-discovery",
    "relay-moderation",
    "paid-relays",
    "key-backup",
    "signer-ux",
    "remote-signers",
    "npub-identity",
    "nsec-safety",
    "nip05-names",
    "profile-metadata",
    "contact-lists",
    "web-of-trust",
    "long-form-articles",
    "primal-reads",
    "habla-yakihonne",
    "comments-on-articles",
    "blossom-storage",
    "wallet-connect",
    "zaps",
    "cashu-wallets",
    "nutzaps",
    "marketplaces",
    "communities",
    "badges",
    "calendar-events",
    "data-vending",
    "ai-agents",
    "login-with-nostr",
    "direct-messages",
    "privacy-model",
    "threat-modeling",
    "mobile-clients",
    "web-clients",
    "feed-design",
    "notifications",
    "seo-public-web",
    "nostr-vs-activitypub",
    "nostr-vs-bluesky",
    "bitcoin-relationship",
    "creator-economy",
    "venue-identity",
    "event-access",
    "governance",
    "nostrich-culture",
    "purple-pilling",
    "reply-guy-dynamics",
    "zap-flexing",
    "client-tribes",
    "relay-politics",
    "app-rivalries",
    "founder-mythology",
    "npub-reputation",
    "pseudonymous-fame",
    "bitcoin-crossover",
    "open-source-celebrities",
    "conference-hallway-nostr",
    "maker-launches",
    "meme-culture",
    "censorship-drama",
    "moderation-drama",
    "scene-gossip-with-care",
    "screenshots-and-receipts",
    "public-feuds",
    "funding-rumors",
    "nostr-journalism",
    "artist-communities",
    "music-scenes",
    "photography-scenes",
    "travel-and-nostr",
    "local-meetups",
    "nostr-bars-and-venues",
    "education-workshops",
    "migration-stories",
    "nostr-as-third-place",
    "microfame-and-status",
    "community-moderators",
    "wallet-brand-trust",
    "client-design-taste",
    "anti-algorithm-culture",
    "old-web-nostalgia",
    "practical-sovereignty",
    "lurkers-and-readers",
    "social-graph-drama",
    "longform-salon",
]


def domain_lookup() -> dict[str, tuple[str, str, str, str, str, str]]:
    return {slug: (slug, title, plain, tech, risk, crays) for slug, title, plain, tech, risk, crays in ALL_GUIDES}


def domain_sections(section, slug: str, title: str, plain: str, tech: str, risk: str, crays: str):
    if slug in CULTURE_SLUGS:
        return culture_domain_sections(section, title, plain, tech, risk, crays)
    return technical_domain_sections(section, title, plain, tech, risk, crays)


def technical_domain_sections(section, title: str, plain: str, tech: str, risk: str, crays: str):
    lower = title.lower()
    return [
        section("Why this matters", [
            f"{title} matters because it is one of the places where Nostr stops being an abstract protocol and starts shaping a real reader's choices. In plain language, this topic is about {plain}. That may sound narrow at first, but it affects how people publish, pay, verify, read, store, recover, moderate or build.",
            f"The useful question is not whether {lower} sounds decentralized. The useful question is what becomes easier, safer or more portable for a person who is not living inside protocol chat all day. If the answer cannot be explained in normal language, the implementation is probably not ready for normal users.",
        ]),
        section("The simple version", [
            f"If you are new to Nostr, start with the ordinary action. Someone needs a practical way to handle {plain}. They do not want a lecture about event formats; they want to know what they can do, what they should avoid and why the result is different from using a closed platform.",
            f"The promise becomes real only when the details line up. A key must be safe. A relay must answer. A client must explain what is happening. A payment must not surprise the user. A public event must not be mistaken for a private message. {title} is useful only when those layers cooperate.",
        ], [
            ("User question", f"What does {lower} help a normal person do?"),
            ("Product question", f"Which parts of {lower} should be hidden, and which parts must be explained?"),
            ("Trust question", f"Who can change, censor, lose or misread the data behind {lower}?"),
        ]),
        section("The technical layer", [
            f"For builders, this topic sits near {tech}. That does not mean every reader needs to memorize the related NIPs or event kinds. It means the implementation has moving parts, and those parts decide whether the experience feels reliable.",
            f"A strong {lower} implementation makes the protocol boring in the best sense. The user clicks, writes, reads, pays or signs, and the client handles relay selection, event formatting, metadata, permissions and error states. The expert can inspect the details, but the beginner is not forced to live inside them.",
        ]),
        section("A concrete reader journey", [
            f"Picture a reader meeting {lower} for the first time. They hear the phrase, open a client, see a button or page related to it and wonder whether it is safe to continue. The article has to answer that moment before it answers the engineering forum version of the question.",
            f"In a healthy journey, the reader can move from curiosity to understanding: what the feature does, what it signs, where the result appears, how it can be recovered and what another app will understand. That path turns {title} from a definition into a usable idea.",
        ]),
        section("Where people get confused", [
            f"The common mistake is to treat {lower} as if it were a finished product. Nostr usually gives a shared language, not a complete service. A NIP can define an event. A relay can store it. A client can display it. None of that guarantees good onboarding, good moderation or good business logic.",
            f"The second mistake is to flatten all responsibility into the word decentralized. With {lower}, responsibility moves around: from platform to user, from app to signer, from database to relay set, from private company policy to visible product choices. That is powerful, but it is not effortless.",
        ]),
        section("What can go wrong", [
            f"The specific risk here is simple: {risk}. That risk may be technical, social, legal or editorial. In Nostr those categories often overlap. A bad signing prompt is a security issue and a writing issue. A bad relay policy is an infrastructure issue and a community issue.",
            f"Readers should see the weak points before they become expensive. A serious {lower} product needs warning copy, fallback behavior, recovery paths, moderation boundaries and honest language about what the protocol can and cannot guarantee.",
        ], [
            ("Beginner risk", "The user believes a label, button or client screen means more than it really means."),
            ("Builder risk", "The implementation works in one client but fails across relays or alternate clients."),
            ("Operator risk", "The service quietly accepts responsibility for storage, payments or moderation without a plan."),
        ]),
        section("How to evaluate real tools", [
            f"When you see a product that claims to support {lower}, ask where the data lives, which relays are involved, what key signs the action, how another client would read it, and what happens when the first service disappears.",
            f"Also ask how it feels. If a tool makes a person feel stupid for not knowing the protocol vocabulary around {title}, the tool is not finished yet. The better product explains the consequence in human words and lets the expert open the deeper layer when needed.",
        ]),
        section("The beginner reading", [
            f"For a newcomer, {lower} should be translated into a small set of safe habits. What should I click? What should I never paste? What should I back up? What will be public? What will other clients understand? Those questions matter more than memorizing every related acronym.",
            f"The beginner should leave with confidence, not false certainty. They should understand enough to use {title} carefully and enough to know when they need a more technical article, a better signer, a more trustworthy relay or a clearer client.",
        ]),
        section("The builder reading", [
            f"For a builder, {lower} is a contract with other software. The contract may be formalized in a NIP, implied by common client behavior or still emerging from experiments. Either way, the builder has to decide what will be interoperable and what is deliberately product-specific.",
            f"The builder's version of {title} must include failure states. What if the relay rejects the event? What if the signer refuses permission? What if the user switches clients? What if a wallet limit is exceeded? What if a public event is later treated as private by a confused reader?",
        ]),
        section("The operator reading", [
            f"For an operator, {lower} is about responsibility. Relays, indexes, storage services, wallets, venues and archive pages all inherit some kind of duty once users depend on them. The more useful the service becomes, the less acceptable vague policy becomes.",
            f"An operator should ask what they are willing to store, serve, remove, charge for, rate-limit, log and explain. {title} is not only a feature. It is a set of expectations that someone will have to operate when the network is busy, angry, spammed or legally complicated.",
        ]),
        section("The creator and community reading", [
            f"For creators and communities, {lower} matters when it changes the relationship with an audience. Does the creator keep the graph? Can a fan move to another client? Can a community moderate without being trapped? Can value move without the platform owning the whole payment story?",
            f"Those questions are why {title} belongs in a Crays archive rather than only in developer notes. The Nostr ecosystem is technical, but the point is social continuity: people, work, status and memory should survive beyond one interface.",
        ]),
        section("The public web angle", [
            f"{title} also has a public-web problem. Raw Nostr events are not automatically good explanations. Search engines, new readers and serious researchers need pages that turn scattered events into structured understanding.",
            f"A good page about {lower} should therefore act like a bridge: readable enough for a search visitor, precise enough for a builder, and linked enough that the reader can move into apps, NIPs, relays, wallets, people or Crays product context without getting lost.",
        ]),
        section("Implementation questions", [
            f"Before a team builds around {lower}, it should answer the unglamorous questions. The exciting version is the demo. The durable version is the checklist that survives support requests, migrations, abuse, missing relays and confused signing prompts.",
            f"For {title}, the strongest product work usually happens in these details: plain labels, visible limits, sensible defaults, testing across clients, recovery paths and honest explanations of what is still experimental.",
        ], [
            ("Signing", f"What exactly does {lower} ask the user or service to sign?"),
            ("Storage", "Which events, files or indexes must remain available?"),
            ("Interoperability", "Which other clients or relays can understand the result?"),
            ("Support", "What can a user do when the expected path fails?"),
        ]),
        section("Crays interpretation", [
            f"For Crays, the reading is practical: {crays}. The point is not to collect protocol features. The point is to decide which features help creators, fans, operators, venues, investors and future members do something valuable.",
            f"That is why the Crays version should sound like a smart guide, not a standards dump. It should say what the thing is, why it matters, where it fits, what it changes, what can break and what a reader should open next.",
        ]),
        section("The reader experience", [
            f"A reader should finish a {lower} article with a usable mental picture. They should know what the topic does, who touches it, what depends on relays, what depends on clients and what belongs to the user's own key management. If that picture is missing, the article has only named the subject.",
            f"The best explanation for {lower} starts from a person and then opens the machinery behind the scene. A creator sees audience ownership. A developer sees signed data. A venue sees a local identity problem. A reader sees whether the next click is safe, useful or just another protocol word.",
        ]),
        section("The social layer", [
            f"{title} also has a social meaning. Nostr is not only a transport protocol; it is a place where people form habits around follows, zaps, public work, reputation and taste. Even a highly technical topic eventually affects how people behave with each other.",
            f"This is where Crays should be more useful than a reference page. It should explain why {lower} changes a creator's relationship with fans, why it changes an operator's responsibility, why it changes how a developer earns trust and why the community may argue about it.",
        ]),
        section("Signals of maturity", [
            f"A mature {lower} implementation shows itself through boring reliability. The app explains the action. The relay behavior is predictable. The signing prompt is understandable. The fallback path is visible. Another client can make sense of the event or at least fail honestly.",
            f"An immature {lower} implementation usually looks exciting in a demo and fragile in daily use. It depends on one service, hides a wallet permission, assumes one relay, invents a private convention or leaves the reader unable to tell what survives outside the first app.",
        ], [
            ("Ready for readers", "The feature can be explained without forcing the reader into raw protocol language."),
            ("Ready for builders", "The event, relay and client expectations are clear enough to test."),
            ("Ready for Crays", "The topic improves a creator, venue, fan, operator or governance journey."),
        ]),
        section("Editorial stance", [
            f"The Crays stance on {lower} is deliberately practical. We do not need to pretend every Nostr idea is already mainstream. We also do not need to dismiss a rough idea just because the current user experience is early.",
            f"{title} needs enough technical depth for a builder, enough plain language for a newcomer and enough cultural context for someone trying to understand why people care. That mix is what turns a catalog entry into a real article.",
        ]),
        section("How this may evolve", [
            f"{title} will probably not stay fixed. Nostr ideas move through experiments, client support, relay policy, user demand and arguments about what deserves to become common practice. A page about {lower} should leave room for that movement.",
            f"The important thing is to track change without losing the reader. When support grows, the article should explain what became easier. When a feature stalls, it should explain why. When a new convention replaces an older habit, the page should show the migration path rather than pretending the old habit never existed.",
        ]),
        section("Reader-level summary", [
            f"If you are reading casually, remember this: {title} is useful only if it changes a real action in a way you can understand. If you are building, remember that the protocol layer is only half the work. If you are operating, remember that every useful path creates responsibility.",
            f"That is the balance Crays needs across the whole Nostr library. We should make {lower} approachable without dumbing it down, technical without becoming cold and honest without draining the energy that makes the ecosystem worth following.",
        ], [
            ("New reader", f"Learn what {lower} does and what can go wrong."),
            ("Builder", f"Check the event, relay, signer and client expectations behind {lower}."),
            ("Creator or operator", f"Ask whether {title} improves audience, venue, payment, memory or governance flows."),
        ]),
        section(f"Next reading paths for {title}", [
            f"After this page, a reader should be able to connect {lower} to at least three neighboring ideas: identity, relays and product experience. Experts can go deeper into NIPs and implementation notes. Newcomers can move sideways into examples and use cases.",
            f"The right next step depends on the reader. If you build, inspect the protocol layer. If you create, look at publishing and payments. If you operate a place or community, look at relays, moderation and identity. If you are just learning, keep the mental model simple: keys identify, clients interpret, relays move events.",
        ]),
    ]


def culture_domain_sections(section, title: str, plain: str, tech: str, risk: str, crays: str):
    lower = title.lower()
    return [
        section("Why this belongs in the archive", [
            f"{title} belongs here because Nostr is not only infrastructure. It is also a scene: people joke, argue, fund each other, form loyalties, leave receipts, build public reputations and create little rituals that make the protocol feel alive.",
            f"In plain language, this topic is about {plain}. That kind of subject can look soft from the outside, but it often explains adoption better than a protocol diagram. People stay where they understand the norms, the drama, the status signals and the inside language.",
        ]),
        section("The scene version", [
            f"The scene version of {lower} starts with behavior. Who is posting? Who is replying? Who is being zapped? Which client makes the behavior visible? Which relay or moderation policy changes the mood? What does a newcomer see when they arrive in the middle of it?",
            f"Nostr culture often turns technical choices into social signals. A wallet setting becomes a status move. A relay policy becomes a values argument. A client preference becomes taste. A long-form reply becomes a public essay. {title} is one of the ways those layers show up in daily life.",
        ]),
        section("What is technical underneath", [
            f"Under the culture, there is still machinery: {tech}. That machinery matters because the social signal is only as durable as the signed events, client rendering, relay availability and user understanding behind it.",
            f"The reader does not need to become a protocol engineer to follow {lower}, but they should know where the social story touches infrastructure. If a dispute depends on a deleted event, a screenshot, a relay block, a zap receipt or a profile claim, the technical layer changes what can be trusted.",
        ]),
        section("Where gossip becomes analysis", [
            f"The risk is this: {risk}. Crays should be able to talk about Nostr drama, rivalries and personality without becoming a rumor machine. The useful question is always what the episode teaches about identity, trust, incentives, moderation, payments, clients or relays.",
            f"A good article about {lower} treats public conflict as material for understanding the ecosystem. It avoids private speculation, does not turn people into caricatures and keeps the reader focused on what can be verified, what is interpretation and what is simply noise.",
        ]),
        section("Status, taste and reputation", [
            f"Status on Nostr is strange in an interesting way. It can come from code, early presence, zaps, essays, conference visibility, client taste, relay operation, memes, moderation work or simply being helpful when newcomers are confused.",
            f"{title} sits inside that status system. The reader should learn how to read the signal without being captured by it. A popular npub is not automatically right. A quiet relay operator may matter more than a loud timeline. A small creator community may be more real than a giant follower count.",
        ]),
        section("How newcomers misread it", [
            f"Newcomers often read {lower} through habits from older platforms. They expect a central account system, a single moderation team, one official app, one algorithm and one shared context. Nostr does not work that way, so the first impression can feel chaotic.",
            f"The article has to slow the scene down. It should say what is normal, what is experimental, what is a joke, what is a real risk and what is only loud because a small early community is still working out its norms in public.",
        ]),
        section("What builders should learn", [
            f"Builders should pay attention to {lower} because culture is product feedback with sharper edges. If people keep arguing about signing prompts, relay defaults, client tribes, zap displays or moderation labels, the product has not made the mental model clear enough.",
            f"The lesson is not to chase every timeline mood. The lesson is to understand what behavior the product rewards. A client can make healthy debate easier or turn every reply into a performance. A relay can protect a community or quietly create hidden power. A wallet can make appreciation feel natural or make money feel performative.",
        ]),
        section("What creators and venues should learn", [
            f"For creators, {lower} affects how fans read commitment, authenticity and access. A creator who understands the culture can use long-form posts, zaps, events, badges and public replies without sounding like they are merely exploiting a trend.",
            f"For venues, local communities and Crays operators, the same topic becomes operational. What should be official? What should stay playful? Who speaks for the place? Which posts become public memory? Which social signals belong on a page that guests, fans or partners will actually read?",
        ]),
        section("How Crays should cover it", [
            f"Our practical reading is this: {crays}. That means the archive can discuss the fun, messy and human parts of Nostr while still keeping a grown-up editorial line.",
            f"Crays should write about {lower} as a guide would talk to an intelligent reader: relaxed, informed, sometimes amused, but careful with claims. The point is not to flatten the scene into corporate copy. The point is to make the scene legible without turning it into cheap spectacle.",
        ]),
        section("Red flags", [
            f"A red flag around {lower} is when a page cannot separate evidence from vibe. Another is when it treats every disagreement as a grand protocol war. Another is when it repeats insider language without helping the reader understand why people use it.",
            f"The healthiest Nostr writing keeps receipts and restraint together. It explains what happened, what can be verified, what different groups believe and why the argument matters for someone who wants to use, build, fund or study the ecosystem.",
        ], [
            ("Evidence", "Is the claim based on public signed material, visible product behavior or only rumor?"),
            ("Context", "Does the article explain the client, relay, payment or social layer involved?"),
            ("Proportion", "Is this a real ecosystem lesson or just timeline heat?"),
            ("Care", "Does the writing avoid turning people into entertainment objects?"),
        ]),
        section("Good coverage feels like this", [
            f"Good coverage of {title} should feel like a smart person walking you through the room. They know the jokes, but they do not require you to know them already. They understand the conflicts, but they do not need to inflame them. They can connect a meme to a product flaw and a public argument to a design lesson.",
            f"That is the voice Crays should aim for across culture pages: human, precise, unafraid of the social layer and allergic to empty hype. Nostr is too interesting to be reduced to either protocol notes or gossip fragments.",
        ]),
        section("Questions to ask", [
            f"When reading or writing about {lower}, ask who benefits from the story, what layer of Nostr it touches and whether the reader will understand more after the article than before it.",
            f"If the answer is only entertainment, the page is probably too thin. If the answer explains identity, reputation, product incentives, moderation, payments, public memory or community formation, then {title} belongs in a serious archive.",
        ], [
            ("People", "Who is involved, and what role do they play in the ecosystem?"),
            ("Protocol", f"Which technical layer makes {lower} possible or visible?"),
            ("Culture", "What norm, joke, conflict or expectation is being revealed?"),
            ("Usefulness", "What should the reader understand or do differently afterward?"),
        ]),
        section(f"Neighboring culture routes for {title}", [
            f"After {title}, the reader should be able to move toward neighboring subjects: zaps, badges, profiles, relays, client design, moderation, long-form writing, events and the public web. Culture pages should not be dead ends.",
            f"That is how the Crays archive can cover Nostr from tech to lifestyle without losing seriousness. The social layer explains why people care; the technical layer explains what is really happening; the product layer explains what Crays can build from it.",
        ]),
    ]


def persona_sections(section, persona: str, situation: str, need: str, domain_title: str, plain: str, tech: str, risk: str, crays: str):
    lower = domain_title.lower()
    return [
        section(f"{persona} view", [
            f"This page is written for the moment when {situation}. The topic is {lower}, but the real job is not to admire the protocol. The job is to understand what you can safely do with it.",
            f"For a {persona.lower()}, the useful version of {lower} is the one that turns into decisions. You need {need}. You also need to know which promises are real today, which ones depend on client support and which ones are still emerging practice.",
        ]),
        section("What to understand first", [
            f"Start with the plain version: {plain}. If that sentence does not connect to a user journey, the page has failed. Nostr only matters when it changes what someone can publish, read, pay for, prove, join or carry from one app to another.",
            f"Do not begin by memorizing the whole specification map. Begin by asking where the identity sits, where the event goes, which relay is involved and which app is deciding what you see. That small model explains a surprising amount of Nostr.",
        ]),
        section("The technical layer in normal words", [
            f"The technical side touches {tech}. For experts, that points toward implementation detail. For everyone else, it is enough to know that this is a coordination problem. Different software needs to understand the same signed action.",
            f"The hard part is not only signing data. The hard part is making the signed data useful. A client needs to render it. A relay needs to serve it. A user needs to understand it. A business needs to decide whether it can depend on it.",
        ]),
        section("The failure mode", [
            f"The failure mode to watch is this: {risk}. This is where many Nostr experiences become confusing. The protocol may be elegant, but the product can still leave the user stranded.",
            f"A good Crays article should not hide the failure mode. It should make the trade-off visible, then show the safer path. That is what makes the archive useful for both new readers and deep technical builders.",
        ]),
        section("How Crays should use it", [
            f"In the Crays world, the practical reading is: {crays}. That does not mean Crays should implement everything. It means the topic belongs in the map because it can affect identity, content, venues, payments, status or governance.",
            f"The best use is selective. Choose the part that improves the reader's life, the creator's independence, the operator's workflow or the developer's architecture. Leave the rest in the archive until it becomes a real product need.",
        ]),
        section("A realistic decision", [
            f"For a {persona.lower()}, the decision around {lower} usually arrives as a practical question, not as a protocol debate. Should you trust this client? Should you publish here? Should you pay, sign, moderate, store, join, fork, fund or wait?",
            f"The answer depends on what {lower} changes in the actual journey. If it gives you more control, more clarity, better reach or safer coordination, it is worth learning. If it only gives you a new label for the same old dependency, treat it as an experiment until the product proves itself.",
        ]),
        section("What to ignore at first", [
            f"A {persona.lower()} does not need to absorb every argument around {lower} on the first pass. Ignore status fights, acronym flexing and claims that make the feature sound magical. Start with what is signed, what is public, what is private, what can move and what depends on someone else's server.",
            f"That simple filter keeps {lower} readable. It also protects the reader from two common traps: believing that open means automatic safety, and believing that early friction means the whole idea is useless.",
        ]),
        section("What strong support looks like", [
            f"Strong support for {lower} is visible in small details. A client gives plain prompts. A relay publishes understandable policy. A wallet shows limits. A community explains rules. A developer writes down what is interoperable and what is still local behavior.",
            f"For a {persona.lower()}, those details matter more than hype. They decide whether the topic becomes part of daily practice or remains a clever demo that only protocol insiders can enjoy.",
        ], [
            ("Plain language", f"The page explains {lower} without hiding the hard parts."),
            ("Visible boundaries", "The reader can tell what the app controls and what the protocol carries."),
            ("Next action", f"The {persona.lower()} knows what to read, test or avoid next."),
        ]),
        section("The community angle", [
            f"{domain_title} also shapes how people behave together. The same technical feature can become a creator habit, a moderation norm, a funding signal, a design taste or a scene argument depending on who uses it first.",
            f"That is why this guide is written for a {persona.lower()} instead of for an abstract user. Nostr feels different when you are building infrastructure, publishing art, running a venue, protecting keys, designing onboarding or trying to understand why a timeline suddenly cares about a new idea.",
        ]),
        section("A good next step", [
            f"After this page, the useful move for a {persona.lower()} is to connect {lower} to one neighboring concept. If the topic touches identity, read keys and NIP-05. If it touches media, read Blossom and file metadata. If it touches money, read zaps, NWC and custody. If it touches culture, read people, events and moderation.",
            f"That path keeps the archive from becoming a pile of tabs. You read one page, understand one relationship and then move to the next page with a clearer question. That is how a large Nostr library becomes useful instead of overwhelming.",
        ]),
    ]


def classify_page(item: dict) -> dict[str, str]:
    slug = item["slug"]
    title = item["title"]
    if slug.startswith("nips/") or slug.startswith("nip-") or "NIP" in title:
        return {
            "area": "the protocol layer",
            "reader": "technical conventions only matter when people can understand them before reading raw standards",
            "technical": "event kinds, tags, relay behavior, client support and backwards compatibility",
            "risk": "support can vary between clients and relays, so the feature may feel real in one place and missing in another",
            "example": "a developer reads the page, then checks whether a client, relay and signer all support the same flow before shipping it",
        }
    if slug.startswith("apps") or slug.startswith("app-profiles") or slug in {"apps", "clients", "developer-tools", "nostr-login"}:
        return {
            "area": "apps and tools",
            "reader": "products teach people what the protocol feels like in daily use",
            "technical": "client UX, signer safety, relay defaults, platform limits and supported NIPs",
            "risk": "a polished interface can still hide weak custody, weak relay handling or limited interoperability",
            "example": "a user tries one app, then opens the same profile or article in another app to see what really travels with the key",
        }
    if slug.startswith("people") or slug in {"people", "creators", "jack-dorsey", "events", "lifestyle-culture", "music-video-media", "nostr-and-bitcoin"}:
        return {
            "area": "people and culture",
            "reader": "people, events and cultural signals shape trust, taste and attention without needing tabloid fog",
            "technical": "contribution history, public work, client adoption, funding, community behavior and visible protocol impact",
            "risk": "a personality story can distract from the actual protocol and product lessons",
            "example": "a reader follows the contribution trail from a builder to the client, library, event or NIP that changed how people use Nostr",
        }
    if slug.startswith("source-inventory") or slug.startswith("awesome-nostr") or slug in {"archive-library", "resources", "videos"}:
        return {
            "area": "the library shelf",
            "reader": "a large body of material needs orientation, not a pile of names and links",
            "technical": "taxonomy, internal links, search paths, topic clusters and update discipline",
            "risk": "a large archive becomes useless if it is only a pile of names and links",
            "example": "a newcomer starts with a plain article, while a developer jumps straight to a NIP or app category without losing context",
        }
    if slug in {"nostr-and-crays", "content-sale", "awards", "crays-super-node", "operators-venues", "dao-governance"} or slug.startswith("deep-dives/crays"):
        return {
            "area": "Crays implementation",
            "reader": "Nostr becomes valuable when it touches the Crays operating layer: profiles, access, venues, payments and governance",
            "technical": "profiles, access, paid content, local relays, status, voting, wallets and venue systems",
            "risk": "a product can overuse protocol features before the user journey is clear",
            "example": "a creator sells content, a fan zaps, a venue hosts an event and a future governance action ties the signals together",
        }
    return {
        "area": "the core concepts",
        "reader": "the idea needs to be accurate enough for builders and human enough for normal people",
        "technical": "keys, clients, relays, signed events, NIPs, wallets, media and search layers",
        "risk": "the page can become a definition instead of an explanation",
        "example": "a reader moves from the plain idea to a concrete action: publish, follow, pay, read, moderate or build",
    }


def editorial_route(item: dict) -> str:
    slug = item.get("slug", "")
    title = item.get("title", "").lower()
    if slug.startswith("people/") or slug in {"people", "events", "lifestyle-culture", "nostr-and-bitcoin"}:
        return "people"
    if slug.startswith(("apps/", "app-profiles/")) or slug in {"apps", "clients", "developer-tools", "nostr-login"}:
        return "apps"
    if slug.startswith("relays/") or slug in {"relays", "relay-market-directory"} or "relay" in title:
        return "relays"
    if slug.startswith("nips/") or slug.startswith("nip-") or slug in {"nips", "events-and-kinds"} or "nip" in title:
        return "nips"
    if any(token in slug for token in ("wallet", "zap", "lightning", "cashu", "safebox")):
        return "wallets"
    if any(token in slug for token in ("creator", "music", "video", "media", "publishing", "long-form", "photos", "streaming", "blogging")):
        return "media"
    if any(token in slug for token in ("marketplace", "commerce", "monetization", "investor", "revenue", "foundups")):
        return "commerce"
    if any(token in slug for token in ("governance", "dao", "badge", "voting", "reputation", "moderation", "policy")):
        return "governance"
    if slug in {"nostr-and-crays", "content-sale", "awards", "crays-super-node", "operators-venues", "dao-governance"} or "crays" in slug:
        return "crays"
    if any(token in slug for token in ("privacy", "security", "trust", "key", "signer", "encryption", "censorship")):
        return "privacy"
    if slug.startswith("reading-paths/") or slug in {"what-is-nostr", "getting-started", "why-nostr", "glossary", "resources"}:
        return "start"
    return "library"


CONTEXTUAL_ROUTE_PROFILES = {
    "start": {
        "layer": "first-principles learning",
        "headings": ["The question this page answers", "The concepts underneath", "The first practical test", "Terms to keep close", "How this connects outward", "What to read with it"],
        "checks": [("Before", "Which idea should already be clear?"), ("During", "Which term or mechanism is doing the work?"), ("After", "Which neighboring page deepens the question?")],
    },
    "people": {
        "layer": "people, public work and culture",
        "headings": ["Why this person or scene matters", "Public work to verify", "Projects and relationships", "Influence without mythmaking", "Useful context for newcomers", "Connected pages"],
        "checks": [("Evidence", "Which source shows the work?"), ("Connection", "Which app, NIP, event or project changed?"), ("Context", "What should you read next?")],
    },
    "apps": {
        "layer": "clients, tools and interfaces",
        "headings": ["What job this product does", "Key and signer behavior", "Relay and data assumptions", "NIPs and services to check", "Interoperability test", "Where it sits in the app map"],
        "checks": [("Identity", "Does it use a signer, raw key, remote signer or account wrapper?"), ("Relays", "Can you see where reads and writes go?"), ("Exit", "What remains usable in another client?")],
    },
    "relays": {
        "layer": "relay infrastructure",
        "headings": ["Infrastructure role", "Read and write behavior", "Policy and access", "Monitoring and failure modes", "Operator questions", "Related relay concepts"],
        "checks": [("Read", "Can clients fetch the expected events?"), ("Write", "Does the relay accept and acknowledge useful events?"), ("Policy", "What is rejected, priced, moderated or authenticated?")],
    },
    "nips": {
        "layer": "protocol standards",
        "headings": ["What this standard changes", "Who has to implement it", "Event, tag or service surface", "Compatibility and adoption", "Product risk", "Neighboring standards"],
        "checks": [("Status", "Is the NIP mandatory, optional, draft, final or unrecommended?"), ("Layer", "Client, relay, signer, wallet, media server or indexer?"), ("Adoption", "Where can you verify support?")],
    },
    "privacy": {
        "layer": "keys, signing and trust",
        "headings": ["Threat model first", "Key and signer boundary", "What stays public", "What can still go wrong", "Safer product language", "Security pages to pair with it"],
        "checks": [("Secret", "Which credential or permission is at risk?"), ("Metadata", "What remains visible even if content is encrypted?"), ("Recovery", "What happens when access is lost?")],
    },
    "wallets": {
        "layer": "money, wallets and records",
        "headings": ["Value flow", "Custody and permission boundary", "Relevant wallet standards", "Receipts and proof", "Failure and support questions", "Where money meets identity"],
        "checks": [("Control", "Who can approve or limit spending?"), ("Proof", "Which event or receipt proves the action?"), ("Fallback", "What happens when wallet or relay access fails?")],
    },
    "media": {
        "layer": "publishing and creator media",
        "headings": ["Publishing surface", "What is signed and what is stored", "Discovery and rendering", "Creator business context", "Media storage questions", "Adjacent creator pages"],
        "checks": [("Object", "Is this a note, article, file metadata event, blob or app-specific object?"), ("Storage", "Where does the heavy media live?"), ("Audience", "How does a fan find or pay for it?")],
    },
    "commerce": {
        "layer": "markets and revenue paths",
        "headings": ["Economic job", "Offer, proof and settlement", "Protocol pieces involved", "Trust and dispute points", "Revenue context", "Business pages around it"],
        "checks": [("Offer", "What is being bought, funded, routed or rewarded?"), ("Proof", "Which signed record matters?"), ("Support", "What happens when payment or access fails?")],
    },
    "governance": {
        "layer": "rules, reputation and decisions",
        "headings": ["Decision layer", "Signals and accountability", "Issuer and scope", "Moderation versus governance", "Risks of vague authority", "Where to deepen the rule set"],
        "checks": [("Actor", "Who issues, votes, labels or enforces?"), ("Scope", "Where does the rule apply?"), ("Consequence", "What changes for access, trust or status?")],
    },
    "crays": {
        "layer": "our product and venue layer",
        "headings": ["Where this touches our product layer", "Protocol piece versus experience", "Profile, venue or governance path", "Operational questions", "What we still have to design", "Internal pages around it"],
        "checks": [("User action", "What does a member, creator, operator or partner do?"), ("Protocol action", "What gets signed, stored or paid?"), ("Fallback", "What must keep working if infrastructure fails?")],
    },
    "library": {
        "layer": "research and source material",
        "headings": ["How to use this source", "Evidence quality", "What it can verify", "What it does not prove", "Where the knowledge should feed", "Library path around it"],
        "checks": [("Source type", "Standard, repo, monitor, directory, essay or research paper?"), ("Claim", "What claim does this source support?"), ("Next use", "Which article should absorb the insight?")],
    },
}


def contextual_editorial_sections(item: dict, section, title: str, deck: str, lens: dict):
    route = editorial_route(item)
    profile = CONTEXTUAL_ROUTE_PROFILES.get(route, CONTEXTUAL_ROUTE_PROFILES["library"])
    headings = profile["headings"]
    layer = profile["layer"]
    return [
        section(headings[0], [
            f"{title} belongs to the {layer} layer. The page should help you answer one concrete question instead of forcing you through a generic Nostr essay.",
            f"The short version is: {deck} The deeper version is to see which concept, standard, product surface or human decision actually changes because of it.",
        ]),
        section(headings[1], [
            f"The useful machinery around {title} is {lens['technical']}. Name those moving parts directly, because vague protocol language is where confusion starts.",
            "A strong page gives you enough context to recognize the term in another client, NIP, relay policy, wallet prompt or source document without pretending every reader is already a protocol engineer.",
        ], profile["checks"]),
        section(headings[2], [
            f"Test {title} by asking what is signed, where it is stored, who renders it, which relays or services are involved and what survives when the first app or server is unavailable.",
            "That test keeps the explanation tied to reality. It also tells us which internal links belong in the body: foundations first, then standards, then practical examples.",
        ]),
        section(headings[3], [
            f"The main risk is that {lens['risk']}. The page should say that plainly and then show the safer reading: what works today, what is experimental and what needs source verification.",
            "This is where dense content beats long content. Give the reader facts, constraints, examples and next steps instead of repeating broad claims about openness or decentralization.",
        ]),
        section(headings[4], [
            f"For us, {title} matters only when it improves understanding or helps a real flow: identity, publishing, relay choice, signing, payment, media, moderation, commerce, venue context or governance.",
            "That does not mean every page has to become a Crays product pitch. It means the page should make the connection visible when the topic affects our ecosystem, and stay purely educational when it does not.",
        ]),
        section(headings[5], [
            f"The best next step from {title} is not a generic link pile. Connect it to the closest prerequisite, the closest technical standard and the closest practical example.",
            "A large archive becomes useful when every page behaves like a node in a knowledge graph: this explains one thing, points to what it depends on and shows where the idea is used.",
        ]),
    ]


def editorial_sections(item: dict, section):
    title = item["title"]
    deck = item.get("deck", "")
    lens = classify_page(item)
    area = lens["area"]
    subject = title.rstrip("?")
    if subject.lower().startswith("what is "):
        subject = subject[8:]
    title = subject
    proper_tokens = (
        "Nostr",
        "NIP",
        "Crays",
        "Bitcoin",
        "Lightning",
        "DAO",
        "Damus",
        "Amethyst",
        "Primal",
        "Coracle",
        "Iris",
        "Nostur",
        "YakiHonne",
        "Jack",
        "Nostriga",
        "Nostrica",
    )
    lower = subject if any(token in subject for token in proper_tokens) else subject[:1].lower() + subject[1:]
    contextual = contextual_editorial_sections(item, section, title, deck, lens)
    if contextual:
        return contextual
    return [
        section("Why people care", [
            f"{title} matters because {lens['reader']}. On paper this belongs near {area}; in practice the stakes are human: what changes for the person holding the key, running the relay, shipping the app or trying to understand the scene?",
            f"The quick version is this: {deck} The richer version starts when someone signs, publishes, pays, stores, moderates, hosts or builds with it and discovers which parts are freedom and which parts are new responsibility.",
        ]),
        section("The human reason", [
            f"Nobody comes to Nostr because they crave another acronym. They come because {lower} might help them keep an audience, prove identity, move money, find a community, run a venue, protect a key or ship a product without begging one platform for permission.",
            f"That is the first test for {title}: what does a real person do next? If the answer starts and ends with a spec number, the explanation has missed the room.",
        ]),
        section("Under the hood", [
            f"Behind the friendly screen are {lens['technical']}. Those parts need names, but names are not the prize. The prize is knowing what survives when the user changes apps, loses a relay, signs a request or asks where the data went.",
            f"{title} works best when the article keeps two views in focus at once: the reader's visible action and the machinery that makes the action portable.",
        ]),
        section("The easy wrong turn", [
            f"The trap is simple: {lens['risk']}. That can be a technical problem, a social problem, a legal problem or a product problem. On Nostr, those categories love to crash the same party.",
            f"The useful stance is curious, not gullible. {title} can be promising and unfinished at the same time. Keep that tension alive instead of sanding it into hype.",
        ]),
        section("The pocket test", [
            f"When a client, relay, wallet, marketplace or community claims to support {lower}, test it like this: what is signed, where is it stored, which app renders it, what travels to another app and what breaks when the original service disappears?",
            f"For {title}, that test protects both beginners and experts. Beginners get a way around vague promises. Builders get a checklist before architecture, funding or moderation decisions become expensive.",
        ], [
            ("Identity", f"Which key, name, profile or organization is responsible for {lower}?"),
            ("Transport", "Which relays or web services move and remember the relevant events?"),
            ("Experience", "What does the reader actually see, click, sign, pay or trust?"),
            ("Fallback", "What still works if the favorite app, relay or service is unavailable?"),
        ]),
        section("A day in the wild", [
            f"Picture {lower} in normal use: {lens['example']}. That is where the subject stops being a label and starts behaving like a product choice.",
            f"The same chapter can serve several people at once. A newcomer gets the plain meaning of {title}. A coder gets the moving parts. A creator gets the audience consequence. A Crays operator gets the business relevance.",
        ]),
        section(f"How {title} fits our operating map", [
            f"We read {lower} through product reality: does it help creators, fans, venues, operators, builders or future members coordinate better? If it does not, {title} can stay documented without pretending it leads the product story.",
            "That is the useful voice here: enjoy the energy of the Nostr scene while still asking the boring, necessary questions. Who signs, who pays, who stores, who moderates and who gets stranded when something fails?",
        ]),
        section("Words that must stay honest", [
            f"A few words around {lower} need discipline. A protocol convention is not a finished product. A relay is not a whole platform. A signature is not consent unless the signer understands what they signed.",
        ], [
            ("Protocol", f"The shared language that lets different tools understand {lower}."),
            ("Product", f"The actual experience a person has when {title} appears in an app."),
            ("Policy", "The rules a relay, app, venue or community chooses to enforce."),
            ("Trust", "The reason a reader believes a key, client, relay or organization deserves attention."),
        ]),
        section("What to carry away", [
            f"After reading about {title}, the reader should be able to explain {lower} to a friend without sounding like they copied a glossary. They should know the human reason, the technical pressure point and the honest limitation.",
            f"That means more than facts. It means orientation: why the topic lives near {area}, which neighboring ideas matter, and what question deserves attention next.",
        ]),
        section("Nearby doors", [
            f"{title} rarely stands alone. It usually touches at least one identity question, one relay or storage question, one client design question and one trust question. The reader does not need to master all of them at once, but they should see the doors.",
            f"A small note says what {lower} is. A strong chapter shows how it connects to people who write, code, pay, moderate, host, perform, read or build in public.",
        ]),
        section("From label to judgment", [
            f"A name is not understanding. A reader can know the phrase {title} and still have no idea what to do with it. The job is to move from label to judgment: useful, risky, experimental, mature, misunderstood or ready for daily use.",
            f"This matters because Nostr language looks deceptively familiar. Client, relay, key, profile, event, zap and community sound ordinary until the reader sees how differently they behave from platform accounts, web posts or payment buttons.",
        ]),
        section("What to watch", [
            f"The next stage for {lower} is not just adoption. Watch for better defaults, plainer prompts, steadier client support and fewer private explanations needed in back channels.",
            f"Crays should care whether {title} becomes easier without losing its open character. The goal is not to erase every rough edge. The goal is to help normal readers make good decisions while keeping the control that made Nostr interesting.",
        ]),
        section("The clean takeaway", [
            f"{title} matters when it helps a real person keep identity, audience, money, media, reputation or community context more portable and more understandable.",
            f"If all we know is that {lower} exists, the idea is thin. If we can see where it belongs, what it changes, who it affects and what to read next, it starts to feel like part of a real operating map.",
        ]),
        section(f"The human texture around {title}", [
            f"The best explanation sounds like someone who knows the back room and still respects the new reader: relaxed, specific, honest and allergic to buzzword fog.",
            f"That matters for {title} because Nostr can become too cold, too tribal or too pleased with itself. Keep the technical backbone, but leave enough warmth for a creator, venue operator, wallet builder, fan and protocol veteran to stay in the same room.",
        ]),
        section("One last map pin", [
            f"Read {title} as one chapter in a larger operating map. It should clarify the topic itself and make nearby questions easier: which identity is involved, which client shapes the experience, which relay or service carries the data and which human relationship gets stronger or more fragile because of it.",
            f"If {lower} leaves the reader with a sharper question, the page has done useful work. Nostr rewards people who follow relationships between topics instead of collecting isolated definitions.",
        ]),
        section(f"Reader route after {title}", [
            f"After reading about {title}, the reader should have a next step that matches their intent. If the subject feels abstract, move to keys, clients and relays. If it feels technical, open the NIP index. If it feels cultural, open people, events and moderation.",
            f"The large-scale rule is simple: each page about {lower} should answer one question well, then point to the neighboring question with enough context that the reader never feels dropped into a pile of tabs.",
        ]),
    ]


def make_longform_pages(page, section):
    pages = []
    for slug, title, plain, tech, risk, crays in ALL_GUIDES:
        pages.append(
            page(
                f"field-guide/{slug}",
                f"{title}: Nostr Field Guide",
                f"A reader-friendly Crays guide to {plain}.",
                f"{title} is one of the topics that turns Nostr from a name into an understandable system. This guide explains {plain}, how it connects to the rest of the protocol and what readers should watch before trusting a product.",
                domain_sections(section, slug, title, plain, tech, risk, crays),
                tag="Nostr field guide",
                sources=[],
                related=["what-is-nostr", "archive-library", "nips/complete-index", "apps/catalog", "nostr-and-crays"],
                keywords=[title, "Nostr field guide", "Crays Nostr"],
                read="Field guide",
            )
        )
    return pages


def apply_longform_editorial_pass(pages: list[dict], section) -> None:
    for item in pages:
        existing_titles = {sec["title"] for sec in item.get("sections", [])}
        additions = [sec for sec in editorial_sections(item, section) if sec["title"] not in existing_titles]
        item.setdefault("sections", []).extend(additions)


def make_repeated_paragraphs_page_specific(pages: list[dict]) -> None:
    """Avoid exact repeated long paragraphs across the generated archive."""
    seen: set[str] = set()
    for item in pages:
        title = item.get("title", "this page")
        slug_context = item.get("slug", title).replace("/", " / ")
        for sec in item.get("sections", []):
            rewritten = []
            for paragraph in sec.get("paragraphs", []):
                normalized = " ".join(paragraph.lower().split())
                if len(normalized) >= 160 and normalized in seen:
                    paragraph = f"In the {slug_context} chapter, {paragraph}"
                    normalized = " ".join(paragraph.lower().split())
                seen.add(normalized)
                rewritten.append(paragraph)
            sec["paragraphs"] = rewritten
