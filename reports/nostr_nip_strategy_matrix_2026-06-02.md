# Crays NIP Strategy Matrix - 2026-06-02

This matrix was checked against the official `nostr-protocol/nips` repository on 2026-06-02. It is product-oriented: the question is not whether a NIP exists, but whether Crays should use it for the living Nostr hub now.

## Product Correction

NIP-72 is useful as a reference because it describes Reddit-style moderated communities, but the upstream NIPs repository currently marks it `unrecommended` and points new group work toward NIP-29. Crays should therefore not make NIP-72 the only community spine.

The stronger Crays community path is:

| Layer | NIPs | Crays use |
|---|---|---|
| Identity and signing | NIP-07, NIP-46, NIP-19, NIP-98 | Join us login, remote signing, readable identifiers, signed API challenges |
| Forum and discussion | NIP-7D, NIP-22, NIP-25 | Topic roots, page replies, votes/reactions |
| Groups and moderation | NIP-29, NIP-32, NIP-56, NIP-70 | Relay-enforced groups later, labels, reports, protected events |
| Source and review | NIP-73, NIP-78, NIP-84, NIP-B0 | External IDs, app-specific review data, highlights, source bookmarks |
| Projects and apps | NIP-34, NIP-89, NIP-99 | Git projects, app handlers, listings/commerce context |
| Media | NIP-92, NIP-94, NIP-B7 | Media metadata, file metadata, Blossom |

## Decision Tiers

| Tier | Meaning | NIPs |
|---|---|---|
| Use now | Safe to design into the current static product layer | NIP-01, 05, 07, 09, 10, 11, 12, 16, 19, 20, 21, 22, 24, 25, 27, 29, 32, 33, 36, 39, 40, 42, 45, 46, 49, 50, 51, 56, 65, 66, 70, 73, 78, 7D, 84, 85, 88, 89, 92, 94, 98, B0, B7, C0 |
| Prepare next | Useful once backend, relay, wallet, media or moderation infrastructure exists | NIP-02, 14, 17, 18, 23, 34, 37, 43, 44, 47, 52, 53, 54, 57, 58, 59, 5A, 60, 61, 62, 68, 69, 71, 75, 77, 86, 87, 99, A0, A4, C7, F4 |
| Reference only | Keep in the archive or render support, but do not make core | NIP-13, 30, 35, 38, 48, 55, 64, CC |
| Compatibility only | Support if users/clients bring it, but do not make it the primary new architecture | NIP-72 |
| Avoid for new core | Deprecated, unrecommended or wrong for this product layer | NIP-03, 04, 06, 08, 15, 26, 28, 31, 90, 96, BE, EE |

## Full Matrix

| NIP | Name | Decision | Crays use |
|---|---|---|---|
| NIP-01 | Basic protocol flow | use now | Event validation, signing model, relay messages and every review/event template |
| NIP-02 | Follow list | prepare | People discovery, social graph hints and trusted contributor context |
| NIP-03 | OpenTimestamps attestations | avoid | Archive reference only; upstream marks it unrecommended |
| NIP-04 | Encrypted direct message | avoid | Do not build new private messaging on it |
| NIP-05 | DNS identity | use now | Readable Crays and public-user identity checks |
| NIP-06 | Mnemonic seed phrase | avoid | Do not push users into mnemonic generation |
| NIP-07 | Browser signer | use now | Primary Join us login and signing path |
| NIP-08 | Old mention handling | avoid | Deprecated by NIP-27 |
| NIP-09 | Event deletion request | use now | Respect deletion requests in cached/community surfaces |
| NIP-10 | Text notes and threads | use now | Compatibility for ordinary Nostr threads |
| NIP-11 | Relay information | use now | Relay directory, capability checks and policy display |
| NIP-12 | Generic tag queries | use now | Relay filtering for page tags, projects, labels and communities |
| NIP-13 | Proof of work | reference | Possible anti-spam signal only |
| NIP-14 | Subject tag | prepare | Discussion titles and support threads |
| NIP-15 | Marketplace | avoid | Prefer NIP-99 |
| NIP-16 | Event treatment | use now | Mandatory relay/client treatment rules |
| NIP-17 | Private direct messages | prepare | Future private moderator/user messages |
| NIP-18 | Reposts | prepare | Curation and source amplification |
| NIP-19 | bech32 entities | use now | npub, note, nevent and naddr display/parse |
| NIP-20 | Command results | use now | Relay publish status and failure handling |
| NIP-21 | nostr URI scheme | use now | Deep links from Crays pages into Nostr clients |
| NIP-22 | Comments | use now | Page discussions, replies and community threads |
| NIP-23 | Long-form content | prepare | Future article/project posts and mirrors |
| NIP-24 | Extra metadata | use now | Richer People and maintainer profiles |
| NIP-25 | Reactions | use now | Upvotes, downvotes and helpful markers |
| NIP-26 | Delegated signing | avoid | Use NIP-46 signers instead |
| NIP-27 | Text note references | use now | Render mentions, note links and source references |
| NIP-28 | Public chat | avoid | Prefer NIP-29 |
| NIP-29 | Relay-based groups | use now | Future enforceable Crays groups |
| NIP-30 | Custom emoji | reference | Nice-to-have display feature |
| NIP-31 | Unknown event kinds | avoid | Upstream marks it unrecommended |
| NIP-32 | Labels | use now | Moderation labels, review states and source quality |
| NIP-33 | Parameterized replaceable events | use now | Addressable profiles, lists, app data and community objects |
| NIP-34 | Git stuff | prepare | Developer/project submissions and repository events |
| NIP-35 | Torrents | reference | Media/library archive reference |
| NIP-36 | Sensitive content | use now | Content warnings and moderation display |
| NIP-37 | Draft wraps | prepare | Future safer draft workflows |
| NIP-38 | User statuses | reference | Profile detail, not core |
| NIP-39 | External identities | use now | People verification and cross-profile source trails |
| NIP-40 | Expiration timestamp | use now | Temporary challenges, drafts and moderation objects |
| NIP-42 | Client relay authentication | use now | Private, paid and search relay access |
| NIP-43 | Relay access metadata | prepare | Relay directory and access request tracking |
| NIP-44 | Versioned encryption | prepare | Future private messages and encrypted app data |
| NIP-45 | Event counts | use now | Search/relay metrics and discussion counts |
| NIP-46 | Remote signing | use now | Nostr Connect/Bunker login |
| NIP-47 | Nostr Wallet Connect | prepare | Wallets, zaps and paid community features later |
| NIP-48 | Bridged events | reference | Cross-network context |
| NIP-49 | Private key encryption | use carefully | Explicit local backup/storage only |
| NIP-50 | Search capability | use now | Relay search and Search Atlas expansion |
| NIP-51 | Lists | use now | Curations, topic lists, people lists and moderator sets |
| NIP-52 | Calendar events | prepare | Nostr conferences and Crays events |
| NIP-53 | Live activities | prepare | Live streams, talks and event rooms |
| NIP-54 | Wiki | prepare | Potential community knowledge pages |
| NIP-55 | Android signer | reference | Mobile signer compatibility |
| NIP-56 | Reporting | use now | Reports and abuse queue |
| NIP-57 | Lightning zaps | prepare | Creator support and project funding |
| NIP-58 | Badges | prepare | Contributor badges and role proof |
| NIP-59 | Gift wrap | prepare | Private messaging path |
| NIP-5A | Static websites | prepare | Future nsite publishing |
| NIP-60 | Cashu wallets | prepare | Wallet research |
| NIP-61 | Nutzaps | prepare | Cashu/Nostr value flow research |
| NIP-62 | Request to vanish | prepare | Future privacy/cache policy |
| NIP-64 | Chess | reference | Archive only |
| NIP-65 | Relay list metadata | use now | User relay choice and outbox hints |
| NIP-66 | Relay liveness monitoring | use now | Relay health and discovery evidence |
| NIP-68 | Picture-first feeds | prepare | Media/creator surfaces |
| NIP-69 | Peer-to-peer order events | prepare | Commerce research |
| NIP-70 | Protected events | use now | Anti-spam and moderation policy |
| NIP-71 | Video events | prepare | Video/media route |
| NIP-72 | Moderated communities | compatibility | Do not make it the only spine |
| NIP-73 | External content IDs | use now | Crawler matching and duplicate detection |
| NIP-75 | Zap goals | prepare | Fundraising and project goals |
| NIP-77 | Negentropy syncing | prepare | Cache/index sync later |
| NIP-78 | Custom app data | use now | Crays review drafts and queue state |
| NIP-7D | Forum threads | use now | Reddit-like forum roots paired with NIP-22 replies |
| NIP-84 | Highlights | use now | Source highlights and research snippets |
| NIP-85 | Trusted assertions | use now | Trust/reputation assertions |
| NIP-86 | Relay management API | prepare | Crays relay administration |
| NIP-87 | Ecash mint discoverability | prepare | Wallet and commerce research |
| NIP-88 | Polls | use now | Community polls for priorities |
| NIP-89 | Recommended app handlers | use now | App directory and handler recommendations |
| NIP-90 | Data vending machines | avoid core | Research context only |
| NIP-92 | Media attachments metadata | use now | Media display and safe attachment metadata |
| NIP-94 | File metadata | use now | File/source/media records |
| NIP-96 | HTTP file storage | avoid | Deprecated in favor of Blossom/NIP-B7 |
| NIP-98 | HTTP auth | use now | Signed API/challenge auth |
| NIP-99 | Classified listings | prepare | Commerce listings and project offers |
| NIP-A0 | Voice messages | prepare | Audio/community media |
| NIP-A4 | Public messages | prepare | Public messaging experiments |
| NIP-B0 | Web bookmarks | use now | Crawler findings and source queue |
| NIP-B7 | Blossom media | use now | Preferred future media storage path |
| NIP-BE | BLE communications | avoid | Upstream marks it unrecommended |
| NIP-C0 | Code snippets | use now | Developer examples and implementation notes |
| NIP-C7 | Chats | prepare | Chat-like flows later |
| NIP-CC | Geocaching events | reference | Archive curiosity |
| NIP-EE | MLS E2EE messaging | avoid | Superseded according to upstream |
| NIP-F4 | Podcasts | prepare | Media/podcast route and creator submissions |

## Hard Rules

- No Crays feature may require users to paste `nsec` into the website.
- NIP-72 stays visible for compatibility, but the product spine is NIP-7D, NIP-22 and NIP-29.
- Crawler output becomes a finding or review item, not automatic editorial content.
- Media storage should prefer Blossom/NIP-B7 over deprecated NIP-96.
- NIP-90 is not the first automation foundation because upstream currently warns against it.

## Primary Source

- Official NIPs repository: https://github.com/nostr-protocol/nips
