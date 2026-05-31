# Crays Nostr Design Bible

Date: 2026-05-31

## Goal

Make the generated Nostr archive feel like a premium, high-energy nonfiction fieldbook instead of a technical link archive. The text stays as-is. The design must carry orientation, hierarchy, momentum, and trust.

## Research Inputs

Primary IA and reading UX:

- Nielsen Norman Group: tables of contents, placement, scannability, sticky rails, right-rail blindness.
- Nielsen Norman Group: breadcrumb navigation and location orientation.
- Baymard Institute: information architecture, organization systems, labels, navigation, search.
- W3C WCAG 2.4.5 Multiple Ways: people need more than one way to locate pages.
- Diataxis: split tutorial, how-to, reference, and explanation needs.
- YaleSites IA principles: context, content, users; organization, labeling, navigation, search.
- Harvard Library accessible content guidelines: headings, structure, scan behavior, meaningful links.
- Web Style Guide: organizing information and site structure for large bodies of content.
- University of Zurich navigation guidance: large content works better when spread and structured, not crammed.
- Baymard homepage/category navigation: product finding fails when taxonomy and category navigation fail.

Nostr ecosystem benchmarks:

- nostr.com
- nostr.org
- nostr.how: what is Nostr, why Nostr, get started.
- nostrapps.com
- nostr.net
- start.nostr.net
- awesome-nostr
- nostrlogin.org
- nostr.co.uk
- Nostr NIPs repository
- Primal-style longform/reads context from the existing research inventory

Image licensing:

- Unsplash license
- Pexels license
- Pixabay content license

## Findings

The strongest content-heavy systems do not rely on one giant navigation component. They combine:

- a stable global nav,
- a page-local chapter map,
- search,
- contextual next steps,
- clear labels,
- and structured category shelves.

The current Crays archive has the right material but the wrong reading posture. The left sidebar plus right TOC plus giant index grid turns the page into a CMS admin surface. It makes the archive visible, but not desirable.

The best direction is a "Nostr atlas" model:

- hero as chapter cover,
- visual route board after the hero,
- article content as the center of gravity,
- a restrained "In this chapter" rail,
- full library index only on the actual Library page,
- app/NIP/topic cards with visual identifiers,
- photos used as editorial atmosphere where they clarify culture, people, venues, and infrastructure.

## Implementation Rules

- Do not rewrite article text.
- Do not add citation/source blocks inside reader-facing articles.
- Remove full A-Z index walls from ordinary articles.
- Keep multiple ways to navigate: top nav, route board, search, chapter TOC, related links, Library shelf.
- Keep links meaningful and visible.
- Avoid mystery navigation. Icons support labels; they never replace labels.
- Use decorative photos with empty alt text when they do not add factual information.
- Keep mobile one-column and make navigation scannable before reading.
- Avoid a one-note dark-blue or purple theme. Use Crays red, ink, white, teal, yellow, and photo color.
