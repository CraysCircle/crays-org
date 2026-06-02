# Crays Nostr Reuse Audit - 2026-06-01

This audit is the reuse-first gate for the Crays Nostr hub. It is based on primary project repositories, project docs, and the NIPs mirror/repository checked on 2026-06-01. It does not approve blind copying. It decides what can be used directly, adapted, referenced, or avoided.

## Decision Summary

- Use now: `nostr-login` for the browser login surface, `nostr-tools` as the low-level event/key utility target, and static NIP-aware UI around signed review drafts.
- Adapt next: NDK or Nostrify for a fuller TypeScript client layer when the static hub grows a build step or backend worker.
- Reference strongly: Coracle for community UX, relay choice, WoT and NIP-72 patterns; noStrudel for event inspection and admin/debug UI; Amethyst for broad NIP behavior and moderation flows; Primal for cache/discovery/media performance architecture.
- Reference only unless licensing is accepted: Damus, Ditto, strfry. Their ideas are useful, but direct code reuse would create GPL/AGPL obligations.
- Avoid as a main base: archived or weak-fit code such as old `primal-caching-service` and `satellite-relay`.

## Project Matrix

| Project | Source | License | Stack | Current activity signal | Relevant features | NIP / protocol fit | Recommendation | Integration risk | Security risk |
|---|---|---:|---|---|---|---|---|---|---|
| Primal Web App | https://github.com/PrimalHQ/primal-web-app | MIT | TypeScript/SolidJS/Sass | pushed 2026-04-21 | polished web client, feeds, profiles, media, discovery UX | strong social/feed reference, unclear NIP-72 depth | reference/adapt | medium, app architecture is Primal-specific | medium, signer and API assumptions need review |
| Primal Server | https://github.com/PrimalHQ/primal-server | MIT | Julia/Postgres | pushed 2026-05-08 | membership, discovery, media caching | cache/API layer, not a standard relay | adapt later | high, Julia/Postgres service beside static Crays | medium, cache trust and API auth need controls |
| Primal Android | https://github.com/PrimalHQ/primal-android-app | MIT | Kotlin | pushed 2026-05-19 | mobile UX, feed/profile behavior | mobile reference | reference only | low for web | low if no code reused |
| Primal iOS | https://github.com/PrimalHQ/primal-ios-app | MIT | Swift | pushed 2026-05-18 | mobile UX | mobile reference | reference only | low for web | low if no code reused |
| Primal Caching Service | https://github.com/PrimalHQ/primal-caching-service | MIT | Julia | archived, moved to primal-server | old cache implementation | superseded by primal-server | avoid/adapt only historically | high | medium |
| Primal Blossom Server | https://github.com/PrimalHQ/primal-blossom-server | MIT | Rust | pushed 2025-05-20 | Blossom implementation | media storage reference | reference/adapt later | medium | medium |
| Damus | https://github.com/damus-io/damus | GPL-3.0 | Swift | pushed 2026-06-01 | native iOS client, zaps, feeds, identity UX | strong behavior reference | reference only | high license and native stack | low if no code reused |
| Notedeck | https://github.com/damus-io/notedeck | NOASSERTION | Rust | pushed 2026-05-25 | multi-column Nostr browser | power-user UI reference | reference only until license clarified | high | low if no code reused |
| nostrdb | https://github.com/damus-io/nostrdb | NOASSERTION | C/LMDB | pushed 2026-05-11 | fast embedded event DB | local indexing/search reference | reference only until license/API stable | high | medium, embedded storage model |
| Coracle | https://github.com/coracle-social/coracle | MIT | Svelte | pushed 2026-05-22 | custom feeds, relays, communities, WoT, recommendations | strong NIP-72/NIP-50/NIP-65/NIP-32/NIP-89 fit | reference/adapt | medium, architecture differs | medium, moderation semantics need local policy |
| noStrudel | https://github.com/hzrd149/nostrudel | MIT | TypeScript | pushed 2026-05-23 | event explorer, sandbox, raw event UX | excellent admin/debug reference | reference/adapt | medium | low if signers isolated |
| Amethyst | https://github.com/vitorpamplona/amethyst | MIT | Kotlin/Android | pushed 2026-06-01 | very broad NIP client, communities, reports, labels, NWC, Blossom | strong NIP behavior reference | reference only/adapt concepts | medium, native stack | low if no code reused |
| Ditto | https://github.com/soapbox-pub/ditto | AGPL-3.0 | TypeScript | pushed 2026-05-31 | social UI, comments, self-hosting, static deployment | useful content/community reference | reference only unless AGPL accepted | high license | low if no code reused |
| Satellite Web | https://github.com/lovvtide/satellite-web | MIT | JavaScript | pushed 2024-02-05 | Reddit-like threads/community UX | useful but older | reference only | medium, older code | medium, stale dependencies possible |
| Satellite Relay | https://github.com/lovvtide/satellite-relay | MIT | JavaScript | archived 2024-04-12 | simple relay | local test reference only | avoid as base | high, archived | medium |
| nostr-login | https://github.com/nostrband/nostr-login | MIT | TypeScript/browser | pushed 2025-03-14, npm 1.7.12 | NIP-07, NIP-46, extension, read-only, local, account switching | best immediate login fit | use | low, script integration | medium, pin version and avoid private-key server flow |
| NDK | https://github.com/nostr-dev-kit/ndk | MIT | TypeScript | pushed 2026-04-16 | high-level relay/outbox/client toolkit | strong client layer candidate | adapt next | medium, needs build step | medium, signer boundaries |
| nostr-tools | https://github.com/nbd-wtf/nostr-tools | Unlicense | TypeScript | pushed 2026-05-19 | keys, NIP-19, event validation, relay tools | best low-level utility target | use/adapt | low with build step | low when used client-side only |
| Nostrify | https://github.com/soapbox-pub/nostrify | MIT | TypeScript | pushed 2026-05-31 | relays, signers, stores, policies, uploaders | strong modular library | adapt next | medium, package/build step needed | medium, policy and storage review |
| Applesauce | https://github.com/hzrd149/applesauce | NOASSERTION | TypeScript | pushed 2026-05-20 | Nostr web-client building blocks | interesting client toolkit | reference/adapt after license check | medium | medium |
| Blossom | https://github.com/hzrd149/blossom | Unlicense | Spec/resources | pushed 2026-05-01 | blob/media protocol | media strategy | use spec/reference | low | medium, upload moderation needed |
| Blossom Server | https://github.com/hzrd149/blossom-server | MIT | TypeScript/Deno | pushed 2026-04-30 | media server | optional media backend | adapt later | medium | high if upload policy is weak |
| Khatru | https://github.com/fiatjaf/khatru | Unlicense | Go | archived 2025-09-22 | custom relay framework | historical/custom relay reference | reference only | medium | medium |
| strfry | https://github.com/hoytech/strfry | GPL-3.0 | C++ | pushed 2026-05-29 | production relay | strong relay reference | reference/deploy separately if GPL accepted | medium | medium |
| nostr-rs-relay | https://github.com/scsibug/nostr-rs-relay | MIT | Rust | pushed 2026-05-22 | relay implementation | good Crays relay candidate | adapt/deploy later | medium | medium |
| rust-nostr | https://github.com/rust-nostr/nostr | MIT | Rust | pushed 2026-05-29 | protocol, client, NWC, tooling | strong backend/service candidate | adapt later | medium | low-medium |

## NIP Gate

The Crays MVP must respect these protocol roles:

- NIP-07: primary browser signer path. The site asks for `window.nostr.getPublicKey()` and `window.nostr.signEvent()` instead of asking for an `nsec`.
- NIP-46: remote signer/Nostr Connect path. `nostr-login` is the first integration because it already exposes this flow.
- NIP-98: signed HTTP/API challenge for future write APIs. Static pages can prepare and sign `kind:27235`; backend verification is Phase 2.
- NIP-7D/NIP-22/NIP-29: primary community model. NIP-7D gives forum roots, NIP-22 gives comments/replies and NIP-29 gives future relay-enforced groups.
- NIP-72: compatibility and UX reference only. The upstream NIPs repository currently marks it `unrecommended` and points new group work toward NIP-29.
- NIP-22: comments use `kind:1111` with uppercase root tags and lowercase parent tags.
- NIP-25/NIP-32/NIP-56: reactions, labels and reports should be supported as event templates before they affect editorial state.
- NIP-65/NIP-11/NIP-50: relay strategy and search must not depend on one relay or one cache provider.
- NIP-23/NIP-34/NIP-78/NIP-89/NIP-99/B0/B7: project submissions, long-form content, app handlers, listings, bookmarks and media uploads are mapped but remain review-gated.

## Direct Reuse Boundaries

- No GPL/AGPL code is copied into this repository in this pass.
- No private key is sent to the server. The static MVP delegates local account creation/signing to `nostr-login` or browser signers.
- Crawler output is never editorial content by default. It creates review items and source trails only.
- User submitted project data is a signed event or local review draft first; editorial pages require review.

## Sources

- NIPs repository: https://github.com/nostr-protocol/nips
- NIP-07: https://nips.nostr.com/7
- NIP-22: https://nips.nostr.com/22
- NIP-46: https://nips.nostr.com/46
- NIP-72: https://nips.nostr.com/72
- NIP-98: https://nips.nostr.com/98
- Nostr Login docs: https://nostrlogin.org/
- Nostrify docs: https://nostrify.dev/start/
- GitHub repository metadata checked through the GitHub API on 2026-06-01.
