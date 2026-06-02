# Crays Nostr Architecture Decision - 2026-06-01

## Context

The current Crays Nostr hub is a static generator-driven site with about 1,420 indexed pages. The core generator is `tools/build_nostr_seo_hub.py`; generated HTML lives under `public/nostr`; search data is `public/nostr/search-index.json`. There is no app framework, no database migration system and no backend API layer in the current repository.

That means the first safe implementation is a static, Nostr-native MVP layer:

- keep editorial content static and fast;
- add Nostr login and signed-event preparation client-side;
- add community, submission, findings and review surfaces as generated pages;
- persist unsigned/signed drafts locally until a backend/review worker is introduced;
- optionally publish signed community events to configured public relays only when the user explicitly chooses to publish;
- document the backend data model before adding a database.

## Accepted Direction

1. Keep the 12 top categories unchanged: Start, People, Apps, Relays, NIPs, Privacy, Wallets, Media, Commerce, Governance, Crays, Library.
2. Turn the Nostr `Join us` CTA into the Nostr login front door at `/nostr/nostr-login/`.
3. Use `nostr-login` 1.7.12 for browser auth UI. It is loaded as a pinned, integrity-checked script and configured for extension, Nostr Connect, read-only and local modes.
4. Add a first-party client script `crays-nostr-community.js` for session display, NIP-07 signing, NIP-98 challenge signing, local review queues and optional relay publish.
5. Add static generated pages for:
   - `/nostr/community/`
   - `/nostr/discussions/`
   - `/nostr/submit-project/`
   - `/nostr/new-findings/`
   - `/nostr/admin/review/`
   - `/nostr/people/users/`
   - `/nostr/nips/crays-nip-strategy/`
6. Add a compact Page Community Entry to generated article pages. This routes discussions, new findings, source submissions and related communities into the product surface without turning every article into a form board.
7. Add a People | Users seed directory for early/relevant Nostr public accounts. Screenshot-provided names are treated as research seeds, not final biographies.
8. Treat NIP-7D forum threads, NIP-22 comments and NIP-29 relay-based groups as the durable community path. Keep NIP-72 as compatibility only because the current upstream NIPs repository marks it `unrecommended` and points new group work toward NIP-29.

## Deferred Until Backend Phase

- Real database tables.
- Moderator accounts and official group/community publication.
- Server-side NIP-98 verification.
- Server-side crawler scheduling.
- Editorial merge automation.
- Production-grade relay cache/search service.
- Full People article expansion for all 100 accounts.

## Data Model Target

When the backend phase begins, use the following tables or equivalent structured storage:

- `nostr_profiles`
- `nostr_sessions`
- `nostr_events_cache`
- `nostr_communities`
- `crays_project_submissions`
- `crawler_sources`
- `crawler_findings`
- `content_update_queue`
- `moderation_actions`
- `page_community_map`

The key rule is that `nostr_sessions` may store public session state, but never stores private keys. Any write action requires either a signed event, a NIP-98 challenge, or a future server-verified equivalent.

## Event Mapping

| Feature | Event strategy |
|---|---|
| Login | NIP-07, NIP-46, read-only npub, local account via nostr-login |
| API auth | NIP-98 `kind:27235` |
| Page comments | NIP-22 `kind:1111` scoped to the page URL or content event |
| Forum topics | NIP-7D `kind:11` roots with NIP-22 replies |
| Relay-enforced groups | NIP-29 once Crays has an owned or trusted relay path |
| Community compatibility | NIP-72 `kind:34550` / `kind:4550` only where existing clients need it |
| Up/down reactions | NIP-25 `kind:7` with local polarity policy |
| Reports | NIP-56 `kind:1984` |
| Labels/mod status | NIP-32 label events |
| Project submissions | NIP-78 app data now; NIP-23/NIP-34/NIP-89/NIP-99 as applicable |
| Bookmarks/findings | NIP-B0 and local review queue |
| Media | NIP-92, NIP-94, Blossom/NIP-B7 after upload moderation exists |

## Security Rules

- The site must not ask users to paste `nsec`.
- Local key creation is delegated to `nostr-login` and remains client-side.
- Read-only npub mode never enables signing or write UI without a signer.
- Crawler findings and community submissions do not automatically become Crays editorial content.
- External links keep `target="_blank" rel="noreferrer noopener"`.
- Visible copy says "Crays"; external Crays network links may still point to `https://www.crays.net`.

## Rollout Plan

1. Phase 1: Reuse audit, architecture decision, static MVP pages.
2. Phase 2: Nostr login/profile session and NIP-98 signed challenge.
3. Phase 3: NIP-7D/NIP-22 discussion layer, NIP-29 group strategy and NIP-72 compatibility.
4. Phase 4: Project submissions and local review queue.
5. Phase 5: Crawler worker and source/finding review queue.
6. Phase 6: Backend storage, NIP-98 verification and admin moderation.
7. Phase 7: Relay/cache layer, likely nostr-rs-relay or Primal-style cache depending on operational fit.
8. Phase 8: deeper People | Users articles, app/profile enrichment and future Crays client surfaces.
