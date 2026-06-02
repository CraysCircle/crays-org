# Crays Nostr Large Content UX / IA Design Gate

Date: 2026-06-02

## Product reading of the references

Crays Nostr is not a blog, not a forum, and not a generic directory. It is a large canonical knowledge atlas with a separate contribution layer. The product must therefore support three jobs at the same time:

1. Teach: guide a beginner from the first concept to deeper protocol, app, relay, wallet, media, commerce, governance, and source material.
2. Orient: keep a reader aware of route, depth, current section, adjacent concepts, and the next useful path.
3. Coordinate contribution: turn questions, corrections, sources, apps, projects, people nominations, lists, reports, and moderation into structured Nostr-native work items.

The references converge on the same pattern:

- WCAG 2.2 requires perceivable, operable, understandable, and robust experiences. For Crays this means stable headings, visible focus, clear link purpose, accessible forms, status messages, keyboard support, touch targets, and predictable navigation.
- NN/g content and IA guidance points toward explicit hierarchy, scannable chunks, route landing pages, clear labels, and table-of-contents patterns for long pages.
- Material, Fluent, Carbon, Atlassian, Polaris, Microsoft, Google, and Mailchimp all treat words as part of the interface. UI copy must tell the reader what they can do next, not quote internal tasks.
- Stanford credibility guidance reinforces source visibility, professional layout, clear contact/organization signals, frequent review signals, and error/broken-link discipline.
- MIT collective intelligence work supports the product model: broad community input works when the problem is structured, contribution paths are clear, and expert/moderator review turns many inputs into useful shared knowledge.

## Crays information architecture

The archive uses a three-layer model:

1. Global orientation
   - `/nostr/` remains the existing Nostr entry.
   - `/nostr/start/` is the large "All about Nostr" orientation page.
   - It explains what exists, how to navigate, how to search, how to contribute, and how canonical content stays protected.

2. Route hubs
   - The 12 top routes stay fixed: Start, People, Apps, Relays, NIPs, Privacy, Wallets, Media, Commerce, Governance, Crays, Library.
   - Each route hub explains what the route contains and which contribution types make sense there.
   - Heavy product modules belong on route hubs and global product pages, not in the middle of every article.

3. Canonical article pages
   - Existing article text stays canonical and read-only.
   - The top of each article gets a small learning compass: where am I, who is this for, what route am I in, and where can I go next?
   - The contribution layer is a separate component before the canonical article body or after it, never an edit surface for the body itself.

## Interactive textbook model

Crays should feel like an interactive textbook with a protocol graph:

- Beginner layer: plain explanations, first paths, glossary-like jumps.
- Builder layer: clients, apps, signers, relays, wallets, and implementation examples.
- Protocol layer: NIPs, event kinds, relay behavior, signing, auth, metadata, moderation, labels, reports.
- Source layer: research pages, original docs, repositories, source inventory, crawl findings, media archive.
- Community layer: questions, discussions, sources, corrections, project/app submissions, people nominations, curated lists, and moderation.

Every page should answer:

- Where am I?
- What is the current level?
- What should I read next?
- What can I contribute here?
- Which content is canonical and which content is community-generated?

## Component placement rules

1. Global start page
   - Prominent orientation, route map, search, contribution ladder, and safe Nostr login.

2. Route hubs
   - Large contextual product modules:
     - Start: questions, missing concepts, source suggestions.
     - People: public Nostr user nominations, public evidence, identity-risk reports.
     - Apps: app/project submissions, maintainer claims, product updates, recommendations.
     - Relays: relay status, NIP-11 data, relay policy reports.
     - NIPs: implementation notes, stale standards, compatible apps.
     - Privacy: key-safety reports, signer/NIP-46/NIP-98 sources.
     - Wallets: NWC/zap/wallet tools, payment-risk reports.
     - Media: creator tools, Blossom/file metadata/media sources.
     - Commerce: listings, marketplaces, business evidence.
     - Governance: labels, reports, reputation, moderation.
     - Crays: Crays-specific integration suggestions.
     - Library: source findings, deep search, review queue.

3. Article pages
   - Compact learning compass directly after the masthead.
   - Compact page contribution panel with required actions: Discuss, Ask a question, Suggest source, Suggest correction, Add related app/project.
   - Category-specific action cards visible but secondary.
   - Detailed forms open in the contribution drawer or on global submission routes.

## Accessibility and quality gate

Before production:

- All interactive controls need accessible names, visible focus, and keyboard operation.
- Forms need labels, instructions, status output, and no private-key field.
- Links must be descriptive and external links must open safely.
- Headings must preserve the document outline.
- Left article navigation must stay sticky on desktop and become static on mobile.
- Scroll position must update the active table-of-contents item.
- User-generated content must be visually distinct from canonical Crays content.
- The layout must not hide the primary article behind contribution UI.

## Implementation decision

Implement a generated `LearningCompass` around existing article pages and route hubs. It is a wrapper/navigation component and does not modify canonical article body text.

Restructure the page contribution panel so the generic required actions and route-specific actions both render. Previously, route-specific cards were present in code but unreachable after an early return.

Keep production persistence relay-first through signed Nostr events on configured public relays. Keep canonical article updates outside the automated contribution path.
