(function () {
  "use strict";

  var STORAGE_PREFIX = "crays.nostr.contribution.";
  var SESSION_KEY = "crays.nostr.session.v1";
  var BASE_URL = "https://www.crays.org";
  var API_BASE = "/api/nostr";
  var DEFAULT_RELAYS = ["wss://relay.damus.io", "wss://nos.lol", "wss://relay.primal.net", "wss://relay.nostr.band"];

  var contributionStatuses = ["draft", "pending", "approved", "rejected", "hidden", "archived", "published_to_nostr", "local_only"];
  var moderationStatuses = ["not_required", "pending_review", "approved", "rejected", "hidden", "needs_changes", "duplicate", "verified", "archived"];
  var targetTypes = ["page", "app", "project", "nip", "route", "article", "relay", "person", "source"];
  var trustLevels = ["anonymous_reader", "signed_in_nostr_user", "contributor", "trusted_contributor", "curator", "moderator", "crays_editor_admin", "verified_maintainer"];
  var appCategories = ["Client", "Mobile Client", "Web Client", "Desktop Client", "Relay", "Relay Tool", "Signer", "Wallet", "Zaps", "Media", "Video", "Audio", "Music", "Creator Tool", "Marketplace", "Commerce", "Developer Tool", "Library", "Bot", "Search", "Discovery", "Analytics", "Privacy", "Security", "Backup", "Migration", "Bridge", "Other"];
  var projectStatuses = ["idea", "prototype", "active", "maintained", "beta", "production", "deprecated", "archived", "unknown"];
  var modelFields = {
    ContributionTarget: ["id", "targetType", "targetSlug", "canonicalUrl", "route", "title", "sectionAnchor", "createdAt", "updatedAt"],
    BaseContribution: ["id", "type", "targetId", "authorPubkey", "authorNpub", "authorDisplayName", "title", "body", "status", "createdAt", "updatedAt", "nostrEventId", "nostrKind", "relayUrls", "moderationState"],
    ProjectSubmission: ["id", "name", "slug", "tagline", "description", "websiteUrl", "githubUrl", "nostrProfile", "maintainerPubkey", "category", "tags", "supportedNips", "relayUrls", "appStoreUrl", "playStoreUrl", "webAppUrl", "logoUrl", "screenshots", "status", "submittedByPubkey", "createdAt", "updatedAt"],
    AppSubmission: ["id", "name", "slug", "tagline", "description", "category", "platform", "websiteUrl", "githubUrl", "nostrProfile", "supportedNips", "keyHandling", "walletSupport", "zapSupport", "mediaSupport", "status", "submittedByPubkey", "createdAt", "updatedAt"],
    SourceSuggestion: ["id", "targetId", "url", "title", "sourceType", "reason", "submittedByPubkey", "status", "moderatorNote", "createdAt", "updatedAt"],
    CorrectionSuggestion: ["id", "targetId", "sectionAnchor", "issueSummary", "currentText", "suggestedChange", "evidenceUrl", "reason", "submittedByPubkey", "status", "moderatorNote", "createdAt", "updatedAt"],
    Question: ["id", "targetId", "title", "body", "tags", "authorPubkey", "status", "acceptedAnswerId", "createdAt", "updatedAt"],
    Answer: ["id", "questionId", "body", "authorPubkey", "status", "isAccepted", "createdAt", "updatedAt"],
    ArticleSubmission: ["id", "title", "slug", "excerpt", "body", "tags", "relatedTargetIds", "authorPubkey", "status", "nostrKind", "nostrEventId", "createdAt", "updatedAt"],
    CommunityPost: ["id", "communitySlug", "title", "body", "postType", "tags", "authorPubkey", "status", "createdAt", "updatedAt"],
    ModerationDecision: ["id", "targetType", "targetId", "moderatorPubkey", "action", "reason", "createdAt"],
    Report: ["id", "targetType", "targetId", "reason", "details", "reporterPubkey", "status", "createdAt", "updatedAt"],
    ReputationEvent: ["id", "userPubkey", "type", "points", "reason", "targetType", "targetId", "createdAt"],
    Badge: ["id", "name", "description", "icon", "criteria", "nostrBadgeEventId"],
    NostrEventDraft: ["id", "kind", "content", "tags", "created_at", "pubkey", "sig", "localContributionId", "relayUrls"],
    RelayConfig: ["id", "url", "read", "write", "purpose", "status"],
    MaintainerClaim: ["id", "targetType", "targetId", "claimerPubkey", "proofUrl", "proofEventId", "status", "createdAt", "updatedAt"],
    CuratedList: ["id", "slug", "title", "description", "curatorPubkey", "items", "tags", "status", "createdAt", "updatedAt"],
    ListItem: ["id", "listId", "targetType", "targetId", "url", "title", "description", "position", "note"],
    Reaction: ["id", "targetType", "targetId", "reaction", "authorPubkey", "status", "createdAt"],
    ZapIntent: ["id", "targetType", "targetId", "amount", "comment", "authorPubkey", "status", "createdAt"]
  };

  var communities = [
    ["beginners", "Beginners", "Start here with simple questions, first clients, first signer setup and safe onboarding."],
    ["developers", "Developers", "Implementation notes, libraries, event kinds, relay behavior and app architecture."],
    ["apps", "Apps", "Clients, signers, directories, app updates, comparisons and maintainer notes."],
    ["relays", "Relays", "Relay policy, uptime, search, paid access, NIP-11 metadata and operator updates."],
    ["signers", "Signers", "NIP-07, NIP-46, remote signing, key safety and account flows."],
    ["wallets", "Wallets", "Nostr Wallet Connect, zaps, Lightning, permissions and wallet UX."],
    ["zaps", "Zaps", "Rewards, tips, value flow, NIP-57 and creator support."],
    ["nips", "NIPs", "Standards, compatibility, examples, risks and implementation decisions."],
    ["media", "Media", "Long-form, video, audio, music, Blossom and creator publishing."],
    ["creators", "Creators", "Public creator profiles, publishing tools, media revenue and audience workflows."],
    ["commerce", "Commerce", "Markets, listings, launches, stores, monetization and project demand."],
    ["governance", "Governance", "Moderation, badges, labels, reports, reputation and review rules."],
    ["crays", "Crays", "Crays account, product, venue, Crays.net and integration ideas."],
    ["events", "Events", "Conferences, meetups, community programs and public talks."],
    ["research", "Research", "Source trails, papers, inventories, crawler findings and duplicate checks."],
    ["protocol", "Protocol", "Protocol design, compatibility and long-term standards questions."],
    ["security", "Security", "Threat models, scam reports, key handling and unsafe UI patterns."],
    ["privacy", "Privacy", "Metadata, public/private boundaries, trust and safety."],
    ["lightning", "Lightning", "Lightning rails, zaps, NWC, receipts and payment flows."],
    ["marketplaces", "Marketplaces", "Nostr-native listings, commerce tools and creator markets."]
  ].map(function (item) {
    return {
      id: "community-" + item[0],
      slug: item[0],
      name: item[1],
      description: item[2],
      category: item[1],
      moderators: [],
      createdAt: "2026-06-02T00:00:00.000Z",
      updatedAt: "2026-06-02T00:00:00.000Z"
    };
  });

  var mockData = {
    communities: communities,
    questions: [
      sampleQuestion("q-beginner-client", "Which Nostr client should a beginner try first?", "I want a safe first client and do not want to paste a private key.", ["beginner", "client", "signer"]),
      sampleQuestion("q-relay-client", "What is the difference between a relay and a client?", "I understand accounts, but I do not understand where posts live.", ["relay", "client"]),
      sampleQuestion("q-nip07-login", "How does NIP-07 login work?", "What exactly does the browser signer sign when I connect?", ["NIP-07", "login"]),
      sampleQuestion("q-zaps", "What are zaps?", "Are zaps comments, payments, likes or all of those?", ["NIP-57", "zaps"]),
      sampleQuestion("q-private-keys", "How should apps handle private keys safely?", "Which key flows should apps avoid?", ["privacy", "signers"])
    ],
    sourceSuggestions: [
      sampleSource("source-nip07", "NIP-07 browser signer reference", "https://nips.nostr.com/7", "nip", "Useful for signer and login pages."),
      sampleSource("source-nip23", "NIP-23 long-form content reference", "https://nips.nostr.com/23", "nip", "Useful for community article publishing."),
      sampleSource("source-nip57", "NIP-57 zaps reference", "https://nips.nostr.com/57", "nip", "Useful for wallet and value-flow pages."),
      sampleSource("source-nip65", "NIP-65 relay list reference", "https://nips.nostr.com/65", "nip", "Useful for relay strategy pages.")
    ],
    pageComments: [
      sampleComment("comment-start-1", "target-start", "", "This page needs a beginner path for signer-safe login.", "approved"),
      sampleComment("comment-nip07-1", "target-nip-07", "comment-start-1", "NIP-07 should be linked from every login warning.", "pending")
    ],
    answers: [
      sampleAnswer("answer-q-beginner-client", "q-beginner-client", "Start with a client that uses a browser signer or remote signer and does not ask for a private key.", true)
    ],
    correctionSuggestions: [
      sampleCorrection("corr-deprecated-app", "This app may be deprecated; verify current maintenance status."),
      sampleCorrection("corr-signer-safety", "This page should mention browser signer safety."),
      sampleCorrection("corr-newer-nip-link", "This NIP reference may need a newer link.")
    ],
    appSubmissions: [
      sampleApp("sample-web-client", "Sample Nostr web client", "web", "nip07"),
      sampleApp("sample-signer", "Sample browser signer", "extension", "nip07"),
      sampleApp("sample-wallet", "Sample Nostr wallet", "wallet", "remote_signer")
    ],
    projects: [
      sampleProject("nostr-web-client", "Nostr web client", "A browser-based client that should use extension or remote signing."),
      sampleProject("browser-signer", "Browser signer", "A signer-focused tool for NIP-07 account flows."),
      sampleProject("relay-monitor", "Relay monitor", "A monitoring project for NIP-11, liveness and relay status."),
      sampleProject("nostr-wallet", "Nostr wallet", "A wallet/NWC project for zaps and permissions."),
      sampleProject("long-form-client", "Long-form publishing client", "A NIP-23 publishing client for articles and guides."),
      sampleProject("creator-media-app", "Creator media app", "A creator publishing and media distribution project.")
    ],
    projectUpdates: [
      sampleUpdate("project-update-relay-monitor", "project-relay-monitor", "Relay monitor should record NIP-11 and search capability changes."),
      sampleUpdate("project-update-long-form", "project-long-form-client", "Long-form client should note NIP-23 compatibility and moderation state.")
    ],
    appUpdates: [
      sampleUpdate("app-update-signer", "app-sample-signer", "Signer entry should show whether it supports NIP-46 or only NIP-07.")
    ],
    articleSubmissions: [
      sampleArticle("community-nostr-primer", "Community Nostr primer", "A community article that explains first clients, signers and relays."),
      sampleArticle("nostr-relay-operator-notes", "Relay operator notes", "A practical guide submitted by a relay operator.")
    ],
    communityPosts: [
      sampleCommunityPost("post-beginners-welcome", "beginners", "What should a first Crays Nostr path include?", "question"),
      sampleCommunityPost("post-app-launches", "apps", "New app submission checklist", "announcement"),
      sampleCommunityPost("post-research-sources", "research", "Useful source review pattern", "research_note")
    ],
    reports: [
      sampleReport("report-stale-app", "project", "project-nostr-web-client", "outdated", "Maintenance state needs verification."),
      sampleReport("report-private-key-risk", "page", "target-nip-07", "safety", "Text or UI must not encourage private-key paste flows.")
    ],
    maintainerClaims: [
      sampleMaintainerClaim("claim-browser-signer", "app", "app-sample-signer", "npub1maintainer"),
      sampleMaintainerClaim("claim-relay-monitor", "project", "project-relay-monitor", "npub1relay")
    ],
    contributorProfiles: [
      sampleContributor("npub1beginner", "Beginner Contributor", "First questions and source suggestions."),
      sampleContributor("npub1maintainer", "App Maintainer", "Project updates and maintainer claims."),
      sampleContributor("npub1relay", "Relay Operator", "Relay reports and policy updates."),
      sampleContributor("npub1research", "NIP Researcher", "Implementation notes and source review."),
      sampleContributor("npub1curator", "Crays Curator", "Moderation and curated lists.")
    ],
    badges: [
      sampleBadge("first-question", "First Question", "Asked a focused beginner question."),
      sampleBadge("source-scout", "Source Scout", "Added a useful source suggestion."),
      sampleBadge("nip-researcher", "NIP Researcher", "Added reviewed NIP implementation context."),
      sampleBadge("app-mapper", "App Mapper", "Submitted or updated app directory data."),
      sampleBadge("verified-maintainer", "Verified Maintainer", "Maintainer claim passed review.")
    ],
    reputationEvents: [
      sampleReputation("npub1beginner", "asked_question", 1, "Asked a beginner question."),
      sampleReputation("npub1research", "source_approved", 5, "Source suggestion approved."),
      sampleReputation("npub1maintainer", "project_approved", 10, "Project submission approved.")
    ],
    curatedLists: [
      sampleList("best-nostr-clients-for-beginners", "Best Nostr clients for beginners", "A starter list for people who need a safe first path."),
      sampleList("nostr-developer-tools", "Nostr developer tools", "Libraries, debuggers, relays and event inspection tools."),
      sampleList("nostr-wallets-and-zap-tools", "Nostr wallets and zap tools", "Wallet, NWC, zap and payment-flow references.")
    ],
    relayConfigs: [
      { id: "relay-damus", url: "wss://relay.damus.io", read: true, write: true, purpose: "default", status: "active" },
      { id: "relay-noslol", url: "wss://nos.lol", read: true, write: true, purpose: "default", status: "active" },
      { id: "relay-primal", url: "wss://relay.primal.net", read: true, write: true, purpose: "discovery", status: "active" },
      { id: "relay-nostr-band", url: "wss://relay.nostr.band", read: true, write: false, purpose: "search", status: "active" }
    ],
    reactions: [
      { id: "reaction-start-1", targetType: "page", targetId: "target-start", reaction: "+", authorPubkey: "npub1beginner", status: "local_only", createdAt: "2026-06-02T00:00:00.000Z" }
    ],
    zapIntents: [
      { id: "zap-source-scout", targetType: "contributor", targetId: "npub1research", amount: 2100, comment: "Thanks for source review.", authorPubkey: "npub1curator", status: "draft", createdAt: "2026-06-02T00:00:00.000Z" }
    ],
    contributionTargets: [
      sampleTarget("target-start", "page", "start", "/nostr/start/", "All about Nostr", "Start"),
      sampleTarget("target-nip-07", "nip", "nip-07-signers", "/nostr/privacy/nip-07-signers/", "NIP-07: Browser Signers", "Privacy"),
      sampleTarget("target-projects", "route", "projects", "/nostr/community/projects/", "Nostr Projects", "Apps")
    ]
  };

  function now() {
    return new Date().toISOString();
  }

  function readJson(key, fallback) {
    try {
      var raw = window.localStorage.getItem(STORAGE_PREFIX + key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function writeJson(key, value) {
    try {
      window.localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value));
    } catch (error) {}
  }

  function sampleQuestion(id, title, body, tags) {
    return { id: id, title: title, body: body, tags: tags, status: "approved", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleSource(id, title, url, sourceType, reason) {
    return { id: id, targetId: "target-start", url: url, title: title, sourceType: sourceType, reason: reason, status: "pending", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleCorrection(id, issueSummary) {
    return { id: id, targetId: "target-page", issueSummary: issueSummary, suggestedChange: "", reason: "Needs reviewer verification.", status: "pending", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleProject(slug, name, tagline) {
    return { id: "project-" + slug, name: name, slug: slug, tagline: tagline, description: tagline, websiteUrl: "", githubUrl: "", nostrProfile: "", maintainerPubkey: "", category: "App", tags: ["nostr"], supportedNips: [], relayUrls: [], status: "pending", submittedByPubkey: "", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleApp(slug, name, platform, keyHandling) {
    return { id: "app-" + slug, name: name, slug: slug, tagline: name + " submission example.", description: name + " submission example.", category: "Client", platform: platform, websiteUrl: "", githubUrl: "", nostrProfile: "", supportedNips: [], keyHandling: keyHandling, walletSupport: false, zapSupport: false, mediaSupport: false, status: "pending", submittedByPubkey: "", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleUpdate(id, targetId, body) {
    return { id: id, targetId: targetId, body: body, status: "pending", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleArticle(slug, title, excerpt) {
    return { id: "article-" + slug, title: title, slug: slug, excerpt: excerpt, body: excerpt, tags: ["nostr"], relatedTargetIds: ["target-start"], authorPubkey: "npub1beginner", status: "pending", nostrKind: 30023, nostrEventId: "", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleCommunityPost(id, communitySlug, title, postType) {
    return { id: id, communitySlug: communitySlug, title: title, body: title, postType: postType, tags: [communitySlug], authorPubkey: "npub1beginner", status: "approved", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleComment(id, targetId, parentId, body, status) {
    return { id: id, targetId: targetId, parentId: parentId || "", body: body, authorPubkey: "npub1beginner", authorNpub: "npub1beginner", status: status, nostrEventId: "", relayUrls: [], createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleAnswer(id, questionId, body, accepted) {
    return { id: id, questionId: questionId, body: body, authorPubkey: "npub1research", status: "approved", isAccepted: accepted, createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleReport(id, targetType, targetId, reason, details) {
    return { id: id, targetType: targetType, targetId: targetId, reason: reason, details: details, reporterPubkey: "npub1beginner", status: "pending", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleMaintainerClaim(id, targetType, targetId, claimerPubkey) {
    return { id: id, targetType: targetType, targetId: targetId, claimerPubkey: claimerPubkey, proofUrl: "", proofEventId: "", status: "pending", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleBadge(id, name, description) {
    return { id: id, name: name, description: description, icon: "", criteria: description, nostrBadgeEventId: "" };
  }

  function sampleReputation(userPubkey, type, points, reason) {
    return { id: "reputation-" + type + "-" + userPubkey, userPubkey: userPubkey, type: type, points: points, reason: reason, targetType: "", targetId: "", createdAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleTarget(id, targetType, targetSlug, route, title, category) {
    return { id: id, targetType: targetType, targetSlug: targetSlug, canonicalUrl: BASE_URL + route, route: route, title: title, sectionAnchor: "", category: category, createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleContributor(npub, displayName, bio) {
    return { id: npub, npub: npub, displayName: displayName, bio: bio, reputation: 0, badges: [], createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function sampleList(slug, title, description) {
    return { id: "list-" + slug, slug: slug, title: title, description: description, items: [], tags: ["nostr"], status: "approved", createdAt: "2026-06-02T00:00:00.000Z", updatedAt: "2026-06-02T00:00:00.000Z" };
  }

  function getSession() {
    try {
      return JSON.parse(window.localStorage.getItem(SESSION_KEY) || "null");
    } catch (error) {
      return null;
    }
  }

  var NostrAuthService = {
    detectSigner: function () {
      return Boolean(window.nostr && typeof window.nostr.getPublicKey === "function" && typeof window.nostr.signEvent === "function");
    },
    connect: async function () {
      var pubkey = await this.getPublicKey();
      var session = { pubkey: pubkey, method: "signer", readOnly: false, relays: DEFAULT_RELAYS.slice(), updatedAt: now() };
      try { window.localStorage.setItem(SESSION_KEY, JSON.stringify(session)); } catch (error) {}
      return session;
    },
    getPublicKey: function () {
      if (!this.detectSigner()) return Promise.reject(new Error("No Nostr signer detected. Install or enable a Nostr browser signer to sign contributions."));
      return window.nostr.getPublicKey();
    },
    signEventDraft: function (draft) {
      if (!this.detectSigner()) return Promise.reject(new Error("No Nostr signer detected. Install or enable a Nostr browser signer to sign contributions."));
      var event = Object.assign({}, draft);
      delete event.id;
      delete event.sig;
      delete event.relayUrls;
      delete event.localContributionId;
      return window.nostr.signEvent(event);
    },
    logout: function () {
      try { window.localStorage.removeItem(SESSION_KEY); } catch (error) {}
    },
    getSession: getSession,
    validateNpub: function (value) {
      return /^(npub1[0-9a-z]+|[0-9a-f]{64})$/i.test(String(value || "").trim());
    },
    formatNpub: function (value) {
      var text = String(value || "");
      return text.length > 22 ? text.slice(0, 12) + "..." + text.slice(-8) : text;
    }
  };

  var NostrEventDraftService = {
    createCommentEventDraft: function (input) {
      return eventDraft(1111, input.body || "", targetTags(input, "page_comment"));
    },
    createArticleEventDraft: function (input) {
      return eventDraft(30023, input.body || "", targetTags(input, "community_article").concat([["title", input.title || ""], ["summary", input.excerpt || input.body || ""]]));
    },
    createListEventDraft: function (input) {
      return eventDraft(30001, "", targetTags(input, "curated_list").concat([["d", input.slug || "curated-list"], ["title", input.title || ""]]));
    },
    createBadgeEventDraft: function (input) {
      return eventDraft(30009, input.description || "", [["d", input.id || "badge"], ["name", input.name || ""], ["t", "crays"], ["t", "crays-nostr"], ["crays:type", "badge"]]);
    },
    createProjectReferenceEventDraft: function (input) {
      return eventDraft(30078, JSON.stringify(publicContributionPayload(input), null, 2), targetTags(input, input.type || "project_submission").concat([["d", (input.type || "project") + "-" + (input.slug || input.id || Date.now())]]));
    },
    createReportEventDraft: function (input) {
      return eventDraft(1984, input.reason || input.body || "", targetTags(input, "report").concat([["p", input.reportedPubkey || ""], ["e", input.reportedEventId || ""]]));
    },
    createModerationEventDraft: function (input) {
      return eventDraft(4550, input.reason || "", targetTags(input, "moderation_decision").concat([["e", input.targetEventId || input.targetId || ""], ["action", input.action || "approve"]]));
    },
    createZapIntentDraft: function (input) {
      return eventDraft(9734, input.comment || "", [["amount", String(input.amount || "")], ["relays", DEFAULT_RELAYS.join(",")]]);
    },
    mapContributionToNostrEventDraft: function (contribution) {
      if (contribution.type === "article" || contribution.type === "article_submission") return this.createArticleEventDraft(contribution);
      if (contribution.type === "report") return this.createReportEventDraft(contribution);
      if (contribution.type === "moderation_decision") return this.createModerationEventDraft(contribution);
      if (contribution.type === "curated_list") return this.createListEventDraft(contribution);
      if (contribution.type === "project" || contribution.type === "app") return this.createProjectReferenceEventDraft(contribution);
      if (contribution.type === "project_submission" || contribution.type === "app_submission" || contribution.type === "source_suggestion" || contribution.type === "correction_suggestion" || contribution.type === "related_app_project" || contribution.type === "question") return this.createProjectReferenceEventDraft(contribution);
      return this.createCommentEventDraft(contribution);
    }
  };

  function eventDraft(kind, content, tags) {
    return {
      id: "draft-" + Date.now(),
      kind: kind,
      content: content,
      tags: tags.filter(function (tag) { return tag[1] !== ""; }),
      created_at: Math.floor(Date.now() / 1000),
      pubkey: "",
      relayUrls: DEFAULT_RELAYS.slice()
    };
  }

  function targetTags(input, type) {
    var canonicalUrl = input.canonicalUrl || (input.route ? BASE_URL + input.route : "");
    var route = input.route || "";
    var tags = [
      ["K", "web"],
      ["t", "crays"],
      ["t", "crays-nostr"],
      ["client", "Crays"],
      ["crays:type", type || input.type || "contribution"],
      ["crays:target", input.targetId || input.targetSlug || ""],
      ["crays:route", route]
    ];
    if (canonicalUrl) {
      tags.push(["I", canonicalUrl]);
      tags.push(["r", canonicalUrl]);
    }
    if (input.url || input.websiteUrl || input.githubUrl) tags.push(["r", input.url || input.websiteUrl || input.githubUrl]);
    if (input.communitySlug) tags.push(["a", "34550:" + (input.communityPubkey || "") + ":" + input.communitySlug]);
    (input.tags || []).slice(0, 12).forEach(function (tag) {
      if (tag) tags.push(["t", String(tag).toLowerCase()]);
    });
    return tags;
  }

  function publicContributionPayload(input) {
    var copy = Object.assign({}, input);
    delete copy.currentText;
    return copy;
  }

  var NostrRelayService = {
    getDefaultRelays: function () {
      return DEFAULT_RELAYS.slice();
    },
    getUserRelays: function () {
      var session = getSession();
      return session && Array.isArray(session.relays) ? session.relays : DEFAULT_RELAYS.slice();
    },
    publishEvent: function (event, relays) {
      return this.publishToRelays(event, relays);
    },
    publishToRelays: async function (event, relays) {
      var relayUrls = Array.isArray(relays) && relays.length ? relays : this.getUserRelays();
      var serverResult = await publishViaServer(event, relayUrls);
      if (serverResult && serverResult.ok) return serverResult;
      var direct = await publishDirect(event, relayUrls);
      return { ok: direct.some(function (item) { return item.ok; }), relays: direct, server: serverResult || null };
    },
    fetchEventsByTarget: async function (target, options) {
      var query = new URLSearchParams();
      query.set("target", target);
      query.set("limit", String(options && options.limit || 50));
      try {
        var response = await fetch(API_BASE + "/events?" + query.toString(), { credentials: "omit" });
        if (response.ok) return response.json();
      } catch (error) {}
      return fetchDirect(target, options || {});
    },
    handlePublishResult: function (result) {
      return result && result.ok ? "published_to_nostr" : "pending";
    }
  };

  async function publishViaServer(event, relays) {
    try {
      var response = await fetch(API_BASE + "/publish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ event: event, relays: relays || DEFAULT_RELAYS })
      });
      return response.json();
    } catch (error) {
      return { ok: false, message: error.message || String(error) };
    }
  }

  function publishDirect(event, relays) {
    return Promise.all((relays || DEFAULT_RELAYS).map(function (relay) {
      return new Promise(function (resolve) {
        var socket;
        var timer = window.setTimeout(function () {
          try { if (socket) socket.close(); } catch (error) {}
          resolve({ relay: relay, ok: false, message: "timeout" });
        }, 9000);
        try {
          socket = new WebSocket(relay);
          socket.addEventListener("open", function () {
            socket.send(JSON.stringify(["EVENT", event]));
          });
          socket.addEventListener("message", function (message) {
            var payload;
            try { payload = JSON.parse(message.data); } catch (error) { payload = null; }
            if (payload && payload[0] === "OK" && payload[1] === event.id) {
              window.clearTimeout(timer);
              try { socket.close(); } catch (error) {}
              resolve({ relay: relay, ok: Boolean(payload[2]), message: payload[3] || "" });
            }
          });
          socket.addEventListener("error", function () {
            window.clearTimeout(timer);
            resolve({ relay: relay, ok: false, message: "connection error" });
          });
        } catch (error) {
          window.clearTimeout(timer);
          resolve({ relay: relay, ok: false, message: error.message || String(error) });
        }
      });
    }));
  }

  function fetchDirect(target, options) {
    var relays = options.relays || DEFAULT_RELAYS;
    var limit = Math.max(1, Math.min(Number(options.limit || 50), 100));
    var filters = [
      { kinds: [1, 1111, 1984, 30001, 30023, 30078, 34550, 4550], "#I": [target], limit: limit },
      { kinds: [1, 1111, 1984, 30001, 30023, 30078, 34550, 4550], "#r": [target], limit: limit }
    ];
    return Promise.all(relays.map(function (relay) {
      return fetchFromRelay(relay, filters, limit);
    })).then(function (results) {
      var seen = {};
      var events = [];
      results.forEach(function (result) {
        (result.events || []).forEach(function (event) {
          if (!event || seen[event.id]) return;
          seen[event.id] = true;
          events.push(event);
        });
      });
      events.sort(function (a, b) { return Number(b.created_at || 0) - Number(a.created_at || 0); });
      return { ok: results.some(function (result) { return result.ok; }), events: events.slice(0, limit), relays: results };
    });
  }

  function fetchFromRelay(relay, filters, limit) {
    return new Promise(function (resolve) {
      var socket;
      var events = [];
      var sub = "crays-" + Date.now() + "-" + Math.random().toString(16).slice(2);
      var timer = window.setTimeout(function () { finish(true, "timeout"); }, 5500);
      function finish(ok, message) {
        window.clearTimeout(timer);
        try {
          if (socket) {
            socket.send(JSON.stringify(["CLOSE", sub]));
            socket.close();
          }
        } catch (error) {}
        resolve({ relay: relay, ok: ok, events: events, message: message || "" });
      }
      try {
        socket = new WebSocket(relay);
        socket.addEventListener("open", function () {
          socket.send(JSON.stringify(["REQ", sub].concat(filters)));
        });
        socket.addEventListener("message", function (message) {
          var payload;
          try { payload = JSON.parse(message.data); } catch (error) { payload = null; }
          if (!payload || payload[1] !== sub) return;
          if (payload[0] === "EVENT" && payload[2]) {
            events.push(payload[2]);
            if (events.length >= limit) finish(true, "");
          }
          if (payload[0] === "EOSE") finish(true, "");
        });
        socket.addEventListener("error", function () { finish(false, "connection error"); });
      } catch (error) {
        finish(false, error.message || String(error));
      }
    });
  }

  var ContributionService = {
    list: function () {
      return readJson("items", []);
    },
    create: function (item) {
      var items = this.list();
      var saved = Object.assign({ id: "contribution-" + Date.now(), status: "pending", createdAt: now(), updatedAt: now() }, item);
      items.unshift(saved);
      writeJson("items", items.slice(0, 200));
      return saved;
    },
    byTarget: function (targetId) {
      return this.list().filter(function (item) { return item.targetId === targetId; });
    },
    updateStatus: function (id, status, moderatorNote) {
      var items = this.list();
      var updated = null;
      items = items.map(function (item) {
        if (item.id !== id) return item;
        updated = Object.assign({}, item, { status: status, moderationState: status, moderatorNote: moderatorNote || item.moderatorNote || "", updatedAt: now() });
        return updated;
      });
      writeJson("items", items);
      return updated;
    },
    seed: function () {
      return mockData;
    }
  };

  var ModerationService = {
    listPending: function () {
      return ContributionService.list().filter(function (item) { return item.status === "pending"; });
    },
    publishDecision: async function (input) {
      var draft = NostrEventDraftService.createModerationEventDraft(input);
      var pubkey = await NostrAuthService.getPublicKey();
      draft.pubkey = pubkey;
      var signed = await NostrAuthService.signEventDraft(draft);
      var response = await fetch(API_BASE + "/moderation", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ event: signed, action: input.action || "", relays: draft.relayUrls || DEFAULT_RELAYS })
      });
      var result = await response.json();
      return Object.assign({ signedEvent: signed }, result);
    },
    decide: function (targetId, action, reason) {
      var decisions = readJson("moderationDecisions", []);
      var decision = { id: "decision-" + Date.now(), targetType: "contribution", targetId: targetId, action: action, reason: reason || "", createdAt: now() };
      decisions.unshift(decision);
      writeJson("moderationDecisions", decisions.slice(0, 200));
      return decision;
    }
  };

  var ReputationService = {
    list: function () {
      return readJson("reputation", []);
    },
    award: function (userPubkey, type, points, reason, target) {
      var events = this.list();
      var event = { id: "reputation-" + Date.now(), userPubkey: userPubkey, type: type, points: points, reason: reason || "", targetType: target && target.type, targetId: target && target.id, createdAt: now() };
      events.unshift(event);
      writeJson("reputation", events.slice(0, 300));
      return event;
    }
  };

  var ProjectDirectoryService = {
    listProjects: function () {
      return mockData.projects.concat(ContributionService.list().filter(function (item) { return item.type === "project_submission"; }));
    },
    listApps: function () {
      return mockData.appSubmissions.concat(ContributionService.list().filter(function (item) { return item.type === "app_submission"; }));
    },
    bySlug: function (slug) {
      return this.listProjects().concat(this.listApps()).find(function (item) { return item.slug === slug; }) || null;
    },
    relatedToTarget: function (targetId) {
      return this.listProjects().filter(function (item) {
        return !item.relatedTargetIds || item.relatedTargetIds.indexOf(targetId) !== -1;
      }).slice(0, 6);
    }
  };

  var SearchDiscoveryService = {
    labels: {
      canonical: "Crays Guide",
      discussion: "Discussion",
      question: "Community Question",
      app: "App",
      project: "Project",
      article: "Community Article",
      source: "Suggested Source",
      list: "Curated List"
    },
    communityResults: function (term) {
      var needle = String(term || "").trim().toLowerCase();
      var pools = [
        ["Community Question", mockData.questions],
        ["App", mockData.appSubmissions],
        ["Project", mockData.projects],
        ["Community Article", mockData.articleSubmissions],
        ["Suggested Source", mockData.sourceSuggestions],
        ["Curated List", mockData.curatedLists],
        ["Discussion", mockData.communityPosts]
      ];
      return pools.reduce(function (items, pair) {
        return items.concat(pair[1].map(function (item) {
          return Object.assign({ resultLabel: pair[0] }, item);
        }));
      }, []).filter(function (item) {
        if (!needle) return true;
        return [item.title, item.name, item.description, item.body, item.reason, item.excerpt].join(" ").toLowerCase().indexOf(needle) !== -1;
      }).slice(0, 24);
    }
  };

  window.CraysNostrContribution = {
    schema: {
      contributionStatuses: contributionStatuses,
      moderationStatuses: moderationStatuses,
      targetTypes: targetTypes,
      trustLevels: trustLevels,
      appCategories: appCategories,
      projectStatuses: projectStatuses,
      modelFields: modelFields
    },
    mockData: mockData,
    services: {
      NostrAuthService: NostrAuthService,
      NostrEventDraftService: NostrEventDraftService,
      NostrRelayService: NostrRelayService,
      ContributionService: ContributionService,
      ModerationService: ModerationService,
      ReputationService: ReputationService,
      ProjectDirectoryService: ProjectDirectoryService,
      SearchDiscoveryService: SearchDiscoveryService
    }
  };
}());
