# Crays Nostr Community Product Research - 2026-06-01

## The Correction

The Crays Nostr hub cannot become alive by adding a login button and a generic comment box. The existing 1,400+ pages are valuable editorial ground. The community layer has to turn that ground into a living participation system:

- people can improve pages without destroying them;
- projects can introduce themselves and keep their information current;
- readers can ask questions and get useful answers;
- Nostr users can nominate people, apps, relays, events, media and sources;
- moderators can approve, label, reject, merge and audit work;
- crawler findings become reviewable leads, not auto-published content.

The shape is closer to a specialized Reddit/Stacker News/Nostr research forum than a comment plugin.

## Research Signals

- NIP-72 describes moderated, Reddit-like communities through `kind:34550` community definitions and `kind:4550` approval events, but the current upstream NIPs repository marks it `unrecommended` and points new group work toward NIP-29. For Crays, NIP-72 should remain a compatibility/reference layer, not the only community spine.
- NIP-7D forum threads provide a better topic-root model for Reddit-like discussions, especially when paired with NIP-22 replies.
- NIP-22 comments (`kind:1111`) can scope discussion to an external page URL or Nostr event, which fits page-specific Crays discussions.
- NIP-29 relay-based groups matter for the future Crays relay path because they allow relay-enforced membership and moderation rules.
- NIP-25 reactions (`kind:7`) supports conventional upvotes and downvotes using `+` and `-`.
- NIP-32 labels (`kind:1985`) are useful for moderation, review states and classification.
- NIP-56 reports (`kind:1984`) create a distributed abuse/moderation signal.
- Coracle is the strongest web reference because it combines communities, relay selection, WoT scores, NIP-50 search, labeling, recommendations, custom feeds, white-labeling and moderation-adjacent UX.
- noStrudel is important for admin/event-inspector thinking and for the safety rule: do not ask users to trust a web client with `nsec`.
- Amethyst is important as a broad protocol reference because it supports NIP-22, NIP-25, NIP-32, NIP-50, NIP-56, NIP-65, NIP-72, NIP-78, NIP-89, NIP-90, NIP-98 and Blossom-related flows.
- Ditto shows the right social ambition: many content types and discussion attached to many object types, not just feed posts.
- Satellite remains a useful Reddit-like UX reference, but not a main code base.

## What Nostr People Would Do On Crays

| Visitor type | Job they want done | Crays community feature |
|---|---|---|
| New Nostr user | Ask which client, signer or relay to use without being shamed | Beginner Q&A, unanswered filter, accepted answers |
| Power user | Debate NIPs, relay policy, WoT, signing, privacy and moderation | Category communities, deep threads, event inspector |
| Project builder | Submit or claim a project profile and post updates | Submit Project, maintainer claim, changelog thread |
| Relay operator | Publish relay details, policy, uptime, paid/free status | Relay reports, NIP-11 review, operator profile |
| App maintainer | Correct wrong app data and link new releases | Project update submission, source-backed edits |
| Researcher | Add sources, papers, NIPs, repos, videos, examples | New Findings queue, source proposals, review states |
| Editor/moderator | Triage submissions without breaking editorial pages | Review dashboard, labels, approvals, merge queue |
| Public Nostr user | Get nominated into People | Users with public proof | Person nomination, profile source checklist |
| Creator/media account | Submit videos, podcasts, articles and event clips | Media submissions, source review, page discussion |
| Crays member | Use one identity across Crays.org and Crays network surfaces | Nostr Login, profile card, Crays links visible but named "Crays" |

## Community Structure

Keep the 12 main categories as the visible top order, but add community lanes under them.

Core communities:

- General / Nostr
- Help / Getting Started
- Nostr Projects
- Apps
- Relays
- NIPs
- Privacy & Keys
- Wallets & Zaps
- Media & Creators
- Commerce & Listings
- Governance & Moderation
- Developer Lab
- Research / New Findings
- People | Users
- Crays

Content types:

- Question
- Link/source submission
- Project launch
- Project update
- App review
- Relay report
- NIP discussion
- Person nomination
- Media/video submission
- Correction
- Crawler finding
- Moderator announcement

Feed sorting:

- New
- Hot
- Top
- Best
- Unanswered
- Needs source
- Needs review
- Accepted / merged

## Page-Level Community UX

Every article page should keep editorial content first and then show a participation panel with tabs:

1. Discussion
   - NIP-22 comments scoped to the page URL now, addressable event later.
   - Sort by best/new/top/unanswered.

2. Improve this page
   - submit source
   - submit correction
   - report stale claim
   - suggest internal link

3. Related projects
   - submit a project related to the page
   - claim/update project
   - compare alternatives

4. New findings
   - crawler leads
   - community leads
   - duplicate/unclear/accepted status

5. People and maintainers
   - nominate public accounts
   - connect project maintainers
   - request a deeper People article

## Review Model

The visible community can be lively while editorial content stays safe:

- Public Nostr events are conversation and evidence.
- Crays editorial pages update only after review.
- Every contribution has a state: pending, needs source, accepted, rejected, duplicate, merged.
- NIP-7D/NIP-22 controls the forum thread shape, NIP-29 controls future relay-enforced group visibility and NIP-72 can be used only for compatibility with existing clients.
- NIP-32 labels control review and classification.
- NIP-56 reports feed the moderation queue.
- Local hard moderation remains possible for legal/safety cases.

## Design Implication

The first community page should not read like a protocol spec. It should invite action:

- "Ask a question"
- "Submit a project"
- "Nominate a Nostr user"
- "Add a source"
- "Review new findings"
- "Report a problem"
- "Open the event inspector"

Each action should show:

- what will be signed,
- where it appears,
- whether it is public or review-only,
- what happens after approval.

## Implementation Direction

Short term in the static hub:

- Build a richer community front page with contribution lanes, action cards, feed mock states and review states.
- Add compact page community entries with explicit improvement actions, not a full form board on every article.
- Keep `nostr-login` and NIP-07/NIP-46 as the login path.
- Store signed drafts locally until backend verification exists.
- Make `/nostr/people/users/` a real nomination/research queue, not merely screenshots.

Backend phase:

- Store events, submissions, findings and review actions.
- Verify NIP-98 challenges server-side.
- Publish official group/community definitions only after the NIP-29/NIP-72 compatibility boundary is settled.
- Query relays for NIP-7D forum topics, NIP-22 page comments, NIP-29 group messages and NIP-72 compatibility events where useful.
- Add crawler workers and admin moderation.

## Sources

- NIP-72: https://nips.nostr.com/72
- NIP-7D: https://nips.nostr.com/7D
- NIP-29: https://nips.nostr.com/29
- NIP-22: https://nips.nostr.com/22
- NIP-25: https://nips.nostr.com/25
- NIP-32: https://nips.nostr.com/32
- NIP-56: https://nips.nostr.com/56
- NIP-78: https://nips.nostr.com/78
- Coracle: https://github.com/coracle-social/coracle
- noStrudel: https://github.com/hzrd149/nostrudel
- Amethyst: https://github.com/vitorpamplona/amethyst
- Ditto: https://about.ditto.pub/
- Nostrbook groups overview: https://nostrbook.dev/groups
