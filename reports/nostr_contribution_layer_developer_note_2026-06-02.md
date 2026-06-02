# Crays Nostr Contribution Layer Developer Note

Date: 2026-06-02

## Canonical content rule

Existing Crays Nostr archive pages are canonical editorial content. Community actions must not overwrite, rewrite, shorten, translate, or directly merge into article body text. Suggestions, questions, reports, app submissions, project submissions, maintainer claims, community articles, and curated lists are separate contribution records linked to canonical targets.

## How contributions attach to pages

Each page-level contribution uses a `ContributionTarget` with target id, target type, slug, canonical URL, route, title, and timestamps. The generated article template renders a separate contribution bar with actions for discussion, questions, source suggestions, correction suggestions, related app/project submissions, and reports. The normal submission path is signer first: browser signer creates a signed Nostr event, the event is published to public relays, and the canonical article remains unchanged.

## Relay-first data model

The contribution layer uses public Nostr relays as the first production persistence path. `public/assets/js/crays-nostr-contribution-services.js` exposes:

- schema metadata for contribution, moderation, reputation, badges, targets, relays, apps, projects, articles, reports, maintainer claims, reactions, zap intents, and curated lists
- mock communities, questions, comments, answers, source suggestions, correction suggestions, apps, projects, updates, reports, badges, contributors, curated lists, relay configs, reactions, zap intents, and targets
- relay-backed publish/fetch services using Damus, Primal, nos.lol and nostr.band defaults
- localStorage as draft, preview and fallback queue only

No private database persistence is claimed here. Persistence is Nostr-native through signed events on public relays; localStorage is not treated as authoritative.

## Moderation flow

All user-created objects start as `pending` with `pending_review`. The moderation surface creates signed moderation events and sends them to `/api/nostr/moderation`. That endpoint verifies the event hash/signature with `nostr-tools`, rejects private-key-looking content, checks the moderator pubkey against `CRAYS_NOSTR_MODERATOR_PUBKEYS`, and only then publishes the moderation event to public relays.

If `CRAYS_NOSTR_MODERATOR_PUBKEYS` is not configured, moderation is locked server-side and the UI shows moderator authorization failure instead of silently approving locally.

Canonical article text is never updated by this automated flow. Editors can manually update canonical content later, outside the contribution system.

## Nostr signer integration

The signer layer is browser-only and uses `window.nostr` when available. The UI copy says: "Use a browser signer. Never paste a private key." The code does not ask for, store, log, or send an `nsec` or private key.

The current service boundary exposes:

- `NostrAuthService`
- `NostrEventDraftService`
- `NostrRelayService`
- `ContributionService`
- `ModerationService`
- `ReputationService`
- `ProjectDirectoryService`
- `SearchDiscoveryService`

## Component mapping

The generated archive and runtime scripts expose the required product components through server-rendered sections, route widgets, and client-side drawers:

- `PageContributionBar` and `PageContributionTabs`: page-level contribution panel rendered by `render_page_community_panel`.
- `PageCommunitySummary`: client-rendered summary attached to `data-nostr-page-panel`.
- `PageDiscussionThread`, `PageCommentComposer`, `AskQuestionOnPage`, `SuggestSourceForm`, `SuggestCorrectionForm`, `RelatedProjectsPanel`, `RelatedAppsPanel`, `ReportContributionButton`, `ContributionDrawer`, `ContributionModal`, and `ContributionStatusBadge`: contribution drawer and forms in `public/assets/js/crays-nostr-community.js`.
- `NostrLoginButton`, `NostrIdentityCard`, and `NostrSignerStatus`: login/auth surface rendered by `render_nostr_auth_panel`.
- `ModerationQueue`: moderation route and queue renderer.
- `ContributorProfileCard`, `ProjectCard`, `AppSubmissionForm`, `ProjectSubmissionForm`, `ArticleSubmissionForm`, `CommunityPostComposer`, and `CuratedListCard`: global route widgets and object cards.

## Relay publishing boundary

Relay publishing is active behind `NostrRelayService` and `/api/nostr/publish`. Signed contribution events are verified server-side, then published to configured public relays. The default relay set includes `wss://relay.damus.io`, `wss://nos.lol`, `wss://relay.primal.net`, and `wss://relay.nostr.band`.

Relay fetching is available through `/api/nostr/events?target=...` and falls back to direct browser relay reads when the local static server has no API route.

## Future production work

Next production steps are durable Crays-owned indexing/cache, Vercel ENV configuration for moderator pubkeys, NIP-98 API challenges for non-browser clients, trusted contributor logic, verified maintainer proof review, relay health scoring, and search-index separation between canonical Crays results and user-generated community results.
