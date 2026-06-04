(function () {
  "use strict";

  var SESSION_KEY = "crays.nostr.session.v1";
  var QUEUE_KEY = "crays.nostr.reviewQueue.v1";
  var VOTE_KEY = "crays.nostr.localVotes.v1";
  var BASE_URL = "https://www.crays.org";
  var DEFAULT_RELAYS = [
    "wss://relay.damus.io",
    "wss://nos.lol",
    "wss://relay.primal.net",
    "wss://relay.nostr.band"
  ];

  function $(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function slugify(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "item";
  }

  function params() {
    return new URLSearchParams(window.location.search || "");
  }

  function readJson(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function writeJson(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      /* localStorage may be disabled. The UI still keeps the signed event preview. */
    }
  }

  function getSession() {
    return readJson(SESSION_KEY, null);
  }

  function saveSession(session) {
    writeJson(SESSION_KEY, session);
    renderSession();
  }

  function clearSession() {
    try {
      window.localStorage.removeItem(SESSION_KEY);
    } catch (error) {}
    renderSession();
  }

  function shortKey(value) {
    var text = String(value || "");
    return text.length > 18 ? text.slice(0, 10) + "..." + text.slice(-8) : text;
  }

  function renderSession() {
    var session = getSession();
    $("[data-nostr-session-state]").forEach(function (node) {
      if (!session) {
        node.innerHTML = "<strong>Not connected</strong><span>Signing actions will ask for a Nostr signer.</span>";
        return;
      }
      var mode = session.readOnly ? "Read-only" : "Signer";
      node.innerHTML = "<strong>" + mode + " connected</strong><span>" + escapeHtml(shortKey(session.pubkey || session.npub)) + "</span>";
    });
  }

  function setPreview(value) {
    $("[data-nostr-event-preview]").forEach(function (node) {
      node.hidden = !value;
      node.textContent = value ? JSON.stringify(value, null, 2) : "";
    });
  }

  function launchNostrLogin(screen) {
    document.dispatchEvent(new CustomEvent("nlLaunch", { detail: screen || "welcome" }));
  }

  async function ensureSigner() {
    if (!window.nostr || typeof window.nostr.getPublicKey !== "function" || typeof window.nostr.signEvent !== "function") {
      launchNostrLogin("welcome");
      throw new Error("No Nostr signer is connected yet.");
    }
    var pubkey = await window.nostr.getPublicKey();
    saveSession({ pubkey: pubkey, method: "signer", readOnly: false, updatedAt: new Date().toISOString() });
    return { pubkey: pubkey, signer: window.nostr };
  }

  function queue() {
    return readJson(QUEUE_KEY, []);
  }

  function saveQueue(items) {
    writeJson(QUEUE_KEY, items.slice(0, 80));
    renderQueue();
  }

  function addQueueItem(item) {
    var items = queue();
    items.unshift(Object.assign({ createdAt: new Date().toISOString(), localId: "crays-" + Date.now() }, item));
    saveQueue(items);
  }

  function renderQueue() {
    var items = queue();
    $("[data-nostr-local-queue]").forEach(function (node) {
      if (!items.length) {
        node.innerHTML = "<strong>No local review items yet</strong><span>Signed drafts and findings created on this device appear here.</span>";
        return;
      }
      node.innerHTML = items.slice(0, 10).map(function (item) {
        var title = item.title || item.type || "Nostr review item";
        var status = item.published ? "published" : item.signedEvent ? "signed" : "draft";
        var kind = (item.signedEvent || item.unsignedEvent || {}).kind || "";
        return [
          '<div class="crays-nostr-queue-item">',
          "<strong>", escapeHtml(title), "</strong>",
          "<span>", escapeHtml(status), " - kind ", escapeHtml(kind), " - ", escapeHtml(item.type || "event"), " - ", escapeHtml(item.createdAt || ""), "</span>",
          item.sourceUrl ? "<code>" + escapeHtml(item.sourceUrl) + "</code>" : "",
          item.error ? "<code>" + escapeHtml(item.error) + "</code>" : "",
          "</div>"
        ].join("");
      }).join("");
    });
  }

  function formData(form) {
    var data = {};
    Array.prototype.forEach.call(new FormData(form).entries(), function (entry) {
      data[entry[0]] = entry[1];
    });
    return data;
  }

  function pageContext(form, data) {
    var panel = form.closest("[data-nostr-page-panel]");
    var typedUrl = data.url || data.website || "";
    return {
      pageUrl: panel ? panel.getAttribute("data-page-url") : typedUrl,
      pageSlug: panel ? panel.getAttribute("data-page-slug") : data.target_path || "",
      community: (form.querySelector('[name="community"]') || {}).value || (panel ? panel.getAttribute("data-community") : "general-nostr")
    };
  }

  function nipTags(data, context, type, kind) {
    var tags = [
      ["client", "crays.org"],
      ["crays:type", type],
      ["crays:review_status", "pending"]
    ];
    if (kind === 11 && data.title) {
      tags.push(["title", data.title]);
    }
    if (kind === 11 && context.community) {
      tags.push(["h", context.community]);
    }
    if (kind === 1111 && context.pageUrl) {
      tags.push(["I", context.pageUrl], ["K", "web"], ["i", context.pageUrl], ["k", "web"]);
    }
    if (context.pageUrl) {
      tags.push(["r", context.pageUrl], ["crays:path", context.pageSlug || window.location.pathname]);
    }
    if (context.community) {
      tags.push(["t", "crays-community"], ["t", slugify(context.community)], ["crays:community", context.community]);
    }
    if (data.url) tags.push(["r", data.url]);
    if (data.website) tags.push(["r", data.website]);
    if (data.repo) tags.push(["r", data.repo]);
    if (data.category) tags.push(["t", String(data.category).toLowerCase().replace(/[^a-z0-9]+/g, "-")]);
    if (data.nips) {
      String(data.nips).split(/[,;\s]+/).filter(Boolean).forEach(function (nip) {
        tags.push(["t", nip.toLowerCase()]);
      });
    }
    if (data.contribution_type) tags.push(["t", slugify(data.contribution_type)]);
    if (kind === 30078) {
      tags.push(["d", "crays-" + type + "-" + Date.now()]);
    }
    return tags;
  }

  function eventContent(data, type) {
    if (type === "page_comment" || type === "discussion" || type === "community_post") {
      return data.content || "";
    }
    return JSON.stringify({
      type: type,
      title: data.title || "",
      category: data.category || "",
      status: data.status || "pending",
      website: data.website || "",
      repo: data.repo || "",
      handle: data.handle || "",
      contribution_type: data.contribution_type || "",
      project_pubkey: data.project_pubkey || "",
      relevant_nips: data.nips || "",
      license: data.license || "",
      source_url: data.url || "",
      target_path: data.target_path || "",
      summary: data.content || "",
      sources: data.sources || ""
    }, null, 2);
  }

  function eventKindFor(form, data, context) {
    var explicit = Number(form.getAttribute("data-event-kind") || "1111");
    var type = form.getAttribute("data-event-type") || "page_comment";
    if ((type === "community_post" || type === "discussion") && !context.pageUrl) {
      return 11;
    }
    if (type === "discussion" && context.pageUrl) {
      return 1111;
    }
    return explicit;
  }

  function buildEvent(form, pubkey) {
    var data = formData(form);
    var type = form.getAttribute("data-event-type") || "page_comment";
    var context = pageContext(form, data);
    var kind = eventKindFor(form, data, context);
    return {
      kind: kind,
      pubkey: pubkey,
      created_at: Math.floor(Date.now() / 1000),
      tags: nipTags(data, context, type, kind),
      content: eventContent(data, type)
    };
  }

  function publishToRelay(relay, event) {
    return new Promise(function (resolve) {
      var socket;
      var timer = window.setTimeout(function () {
        try { if (socket) socket.close(); } catch (error) {}
        resolve({ relay: relay, ok: false, message: "timeout" });
      }, 8000);
      try {
        socket = new WebSocket(relay);
        socket.addEventListener("open", function () {
          socket.send(JSON.stringify(["EVENT", event]));
        });
        socket.addEventListener("message", function (message) {
          var payload;
          try { payload = JSON.parse(message.data); } catch (error) { payload = null; }
          if (payload && payload[0] === "OK") {
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
        resolve({ relay: relay, ok: false, message: error.message });
      }
    });
  }

  async function publishEvent(event) {
    return Promise.all(DEFAULT_RELAYS.map(function (relay) {
      return publishToRelay(relay, event);
    }));
  }

  async function handleEventForm(form) {
    var status = form.querySelector("[data-nostr-form-status]");
    var data = formData(form);
    var type = form.getAttribute("data-event-type") || "event";
    try {
      if (status) status.textContent = "Preparing signer...";
      var auth = await ensureSigner();
      var event = buildEvent(form, auth.pubkey);
      if (status) status.textContent = "Waiting for signature...";
      var signedEvent = await auth.signer.signEvent(event);
      var publish = Boolean(data.publish);
      var publishResults = [];
      if (publish) {
        if (status) status.textContent = "Publishing to default relays...";
        publishResults = await publishEvent(signedEvent);
      }
      addQueueItem({
        type: type,
        title: data.title || data.url || "Nostr event",
        sourceUrl: data.url || data.website || data.repo || "",
        unsignedEvent: event,
        signedEvent: signedEvent,
        published: publish,
        publishResults: publishResults
      });
      setPreview(signedEvent);
      form.reset();
      if (status) status.textContent = publish ? "Signed and publish attempt recorded." : "Signed and saved to the local review queue.";
    } catch (error) {
      var session = getSession();
      var fallbackPubkey = session && session.readOnly ? session.pubkey || session.npub : "";
      var draft = buildEvent(form, fallbackPubkey || "");
      addQueueItem({
        type: type,
        title: data.title || data.url || "Unsigned draft",
        sourceUrl: data.url || data.website || data.repo || "",
        unsignedEvent: draft,
        error: error.message || String(error)
      });
      setPreview(draft);
      if (status) status.textContent = (error.message || "No signer connected") + " Draft saved locally.";
    }
  }

  async function signChallenge() {
    try {
      var auth = await ensureSigner();
      var event = {
        kind: 27235,
        pubkey: auth.pubkey,
        created_at: Math.floor(Date.now() / 1000),
        tags: [["u", window.location.href], ["method", "GET"]],
        content: ""
      };
      var signedEvent = await auth.signer.signEvent(event);
      setPreview(signedEvent);
      addQueueItem({ type: "nip98_challenge", title: "NIP-98 challenge", signedEvent: signedEvent });
    } catch (error) {
      setPreview({ error: error.message || String(error) });
    }
  }

  function setFieldIfEmpty(form, name, value) {
    var field = form.querySelector('[name="' + name + '"]');
    if (!field || !value || field.value) return;
    if (field.tagName === "SELECT") {
      var wanted = slugify(value);
      var matched = Array.prototype.find.call(field.options, function (option) {
        return option.value === value || slugify(option.value) === wanted || slugify(option.textContent) === wanted;
      });
      if (matched) {
        field.value = matched.value;
        return;
      }
    }
    field.value = value;
  }

  function categoryFromRoute(route) {
    var map = {
      start: "Start",
      people: "People",
      apps: "Apps",
      relays: "Relays",
      nips: "NIPs",
      privacy: "Privacy",
      wallets: "Wallets",
      media: "Media",
      commerce: "Commerce",
      governance: "Governance",
      crays: "Crays",
      library: "Library"
    };
    return map[slugify(route)] || "";
  }

  function communityFromRoute(route) {
    var key = slugify(route);
    if (key === "start") return "general-nostr";
    if (key === "people") return "general-nostr";
    if (key === "library") return "research-new-findings";
    return key || "";
  }

  function canonicalNostrPath(page, route) {
    var clean = String(page || "").replace(/^\/+|\/+$/g, "").replace(/^nostr\//, "");
    if (!clean) return "";
    var hubPrefixes = ["basics", "people", "apps", "relays", "nips", "privacy", "wallets", "media", "commerce", "governance", "crays", "library", "community", "start"];
    if (hubPrefixes.some(function (prefix) { return clean === prefix || clean.indexOf(prefix + "/") === 0; })) {
      return "/nostr/" + clean + "/";
    }
    var key = slugify(route);
    var hub = key === "start" ? "basics" : key;
    if (hubPrefixes.indexOf(hub) === -1 || hub === "community") hub = "library";
    return "/nostr/" + hub + "/" + clean + "/";
  }

  function prefillForms() {
    var query = params();
    if (!query.toString()) return;
    var route = query.get("route") || "";
    var type = query.get("type") || "";
    var page = query.get("page") || "";
    var title = query.get("title") || "";
    var url = query.get("url") || "";
    var pagePath = canonicalNostrPath(page, route);
    var pageUrl = pagePath ? BASE_URL + pagePath : "";
    $("[data-nostr-event-form]").forEach(function (form) {
      setFieldIfEmpty(form, "title", title);
      setFieldIfEmpty(form, "url", url || pageUrl);
      setFieldIfEmpty(form, "target_path", pagePath);
      setFieldIfEmpty(form, "category", categoryFromRoute(route));
      setFieldIfEmpty(form, "community", communityFromRoute(route));
      setFieldIfEmpty(form, "contribution_type", type);
      var contentField = form.querySelector('[name="content"]');
      if (page && contentField && !contentField.value) {
        setFieldIfEmpty(form, "content", "Related page: " + pageUrl + "\n\n");
      }
    });
  }

  function bindFeedFilters() {
    var cards = $(".crays-nostr-product-feed-card");
    var buttons = $("[data-community-filter]");
    var input = document.querySelector("[data-community-search]");
    if (!cards.length) return;
    function update(filter) {
      var active = filter || (document.querySelector('[data-community-filter][aria-pressed="true"]') || {}).getAttribute && document.querySelector('[data-community-filter][aria-pressed="true"]').getAttribute("data-community-filter") || "all";
      var term = input ? input.value.trim().toLowerCase() : "";
      cards.forEach(function (card) {
        var state = card.getAttribute("data-feed-state") || "";
        var kind = card.getAttribute("data-feed-kind") || "";
        var route = card.getAttribute("data-feed-route") || "";
        var text = card.textContent.toLowerCase();
        var filterMatch = active === "all" || active === state || active === kind || active === route;
        var searchMatch = !term || text.indexOf(term) !== -1;
        card.hidden = !(filterMatch && searchMatch);
      });
    }
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        buttons.forEach(function (candidate) { candidate.setAttribute("aria-pressed", "false"); });
        button.setAttribute("aria-pressed", "true");
        update(button.getAttribute("data-community-filter") || "all");
      });
    });
    if (input) input.addEventListener("input", function () { update(); });
    update("all");
  }

  function voteState() {
    return readJson(VOTE_KEY, {});
  }

  function saveVoteState(value) {
    writeJson(VOTE_KEY, value);
  }

  function voteRoot(node) {
    return node.closest(".crays-nostr-product-feed-card, .crays-nostr-thread-card, .crays-nostr-thread-votes") || node.parentNode;
  }

  function updateVoteDisplays() {
    var votes = voteState();
    $("[data-nostr-vote]").forEach(function (node) {
      var key = node.getAttribute("data-vote-key");
      var root = voteRoot(node);
      var score = root ? root.querySelector("[data-nostr-vote-score]") : null;
      if (score && votes[key]) {
        var base = Number(score.getAttribute("data-base-score") || score.textContent || "0");
        if (!score.getAttribute("data-base-score")) score.setAttribute("data-base-score", String(base));
        score.textContent = String(base + votes[key]);
      }
    });
  }

  async function recordVote(button) {
    var key = button.getAttribute("data-vote-key") || "page";
    var value = button.getAttribute("data-nostr-vote") === "-" ? -1 : 1;
    var votes = voteState();
    votes[key] = (votes[key] || 0) + value;
    saveVoteState(votes);
    updateVoteDisplays();

    var event = {
      kind: 7,
      pubkey: "",
      created_at: Math.floor(Date.now() / 1000),
      tags: [["client", "crays.org"], ["crays:type", "reaction"], ["crays:voted_item", key]],
      content: value > 0 ? "+" : "-"
    };
    try {
      if (window.nostr && typeof window.nostr.getPublicKey === "function" && typeof window.nostr.signEvent === "function") {
        event.pubkey = await window.nostr.getPublicKey();
        var signedEvent = await window.nostr.signEvent(event);
        addQueueItem({ type: "reaction", title: "Vote on " + key, signedEvent: signedEvent });
        setPreview(signedEvent);
      } else {
        addQueueItem({ type: "reaction", title: "Vote on " + key, unsignedEvent: event, error: "Connect a signer to publish this NIP-25 reaction." });
      }
    } catch (error) {
      addQueueItem({ type: "reaction", title: "Vote on " + key, unsignedEvent: event, error: error.message || String(error) });
    }
  }

  function contributionRuntime() {
    return window.CraysNostrContribution || null;
  }

  function contributionServices() {
    var runtime = contributionRuntime();
    return runtime ? runtime.services : null;
  }

  function contributionMock() {
    var runtime = contributionRuntime();
    return runtime ? runtime.mockData : {};
  }

  function targetFromPanel(panel) {
    var slug = panel ? panel.getAttribute("data-page-slug") || "" : window.location.pathname.replace(/^\/nostr\/|\/$/g, "");
    var url = panel ? panel.getAttribute("data-page-url") || window.location.href : window.location.href;
    var route = panel ? panel.getAttribute("data-community") || "" : "";
    return {
      id: "target-" + slugify(slug || "page"),
      targetType: "page",
      targetSlug: slug || window.location.pathname,
      canonicalUrl: url,
      route: route,
      title: document.querySelector("h1, .crays-nostr-article-masthead__title") ? document.querySelector("h1, .crays-nostr-article-masthead__title").textContent.trim() : document.title,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
  }

  function actionType(action) {
    return {
      discuss: "page_comment",
      discussion: "page_comment",
      question: "question",
      source: "source_suggestion",
      correction: "correction_suggestion",
      relation: "related_app_project",
      report: "report",
      project: "project_submission",
      app: "app_submission",
      article: "article_submission",
      community: "community_post",
      list: "curated_list"
    }[action] || "page_comment";
  }

  function ensureContributionDrawer() {
    var existing = document.querySelector("[data-contribution-drawer]");
    if (existing) return existing;
    var shell = document.createElement("div");
    shell.className = "crays-nostr-drawer";
    shell.hidden = true;
    shell.setAttribute("data-contribution-drawer", "");
    shell.setAttribute("data-component", "ContributionDrawer ContributionModal PageDiscussionThread PageCommentComposer AskQuestionOnPage SuggestSourceForm SuggestCorrectionForm RelatedProjectsPanel RelatedAppsPanel ReportContributionButton ContributionStatusBadge");
    shell.innerHTML = [
      '<div class="crays-nostr-drawer__backdrop" data-contribution-close></div>',
      '<aside class="crays-nostr-drawer__panel" role="dialog" aria-modal="true" aria-labelledby="crays-contribution-drawer-title">',
      '<button class="crays-nostr-drawer__close" type="button" data-contribution-close aria-label="Close contribution panel">×</button>',
      '<div data-contribution-drawer-content></div>',
      '</aside>'
    ].join("");
    document.body.appendChild(shell);
    shell.addEventListener("click", function (event) {
      if (event.target.hasAttribute("data-contribution-close")) closeContributionDrawer();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !shell.hidden) closeContributionDrawer();
    });
    return shell;
  }

  function closeContributionDrawer() {
    var drawer = document.querySelector("[data-contribution-drawer]");
    if (!drawer) return;
    drawer.hidden = true;
    document.documentElement.classList.remove("crays-nostr-drawer-open");
  }

  function formIntro(action) {
    if (action === "source") return "Add a useful reference, NIP, repository, article, app, relay, or research link for this page.";
    if (action === "correction") return "This does not edit the article directly. Your suggestion goes into review.";
    if (action === "question") return "Ask a focused question attached to this page. Answers stay separate from the canonical article.";
    if (action === "relation") return "Submit or connect a related app/project. It enters review before it appears as approved.";
    if (action === "report") return "Report spam, impersonation, unsafe links or low-quality contributions.";
    if (action === "project") return "Submit a Nostr project with links, category, status and supported NIPs.";
    if (action === "app") return "Submit a Nostr app with platform, key handling and product links.";
    if (action === "article") return "Submit a community article. It is separate from the canonical Crays archive.";
    if (action === "community") return "Create a community post in the relevant Nostr topic area.";
    return "Read without login. To post, connect with Nostr or save a local draft for review.";
  }

  function drawerFields(action) {
    if (action === "question") {
      return [
        '<label>Question title<input name="title" required placeholder="What do you need help with?"></label>',
        '<label>Body<textarea name="body" required placeholder="Add context, what you tried, and where the page is unclear."></textarea></label>',
        '<label>Tags<input name="tags" placeholder="beginner, relay, NIP-07"></label>'
      ].join("");
    }
    if (action === "source") {
      return [
        '<label>Source URL<input name="url" type="url" required placeholder="https://"></label>',
        '<label>Title<input name="title" placeholder="Optional source title"></label>',
        '<label>Source type<select name="sourceType"><option>documentation</option><option>nip</option><option>github</option><option>article</option><option>research</option><option>video</option><option>podcast</option><option>tool</option><option>app</option><option>relay</option><option>other</option></select></label>',
        '<label>Reason<textarea name="reason" required placeholder="Why should this source be reviewed for this page?"></textarea></label>'
      ].join("");
    }
    if (action === "correction") {
      return [
        '<label>Issue summary<input name="issueSummary" required placeholder="What is stale, wrong or missing?"></label>',
        '<label>Current text optional<textarea name="currentText" placeholder="Paste only the short phrase that needs review."></textarea></label>',
        '<label>Suggested correction<textarea name="suggestedChange" required placeholder="What should an editor consider changing?"></textarea></label>',
        '<label>Evidence URL optional<input name="evidenceUrl" type="url" placeholder="https://"></label>',
        '<label>Reason<textarea name="reason" required placeholder="Explain the evidence and why this matters."></textarea></label>'
      ].join("");
    }
    if (action === "relation") {
      return [
        '<label>Contribution type<select name="relationType"><option value="project_submission">Submit project</option><option value="app_submission">Submit app</option><option value="related_record">Suggest existing relation</option></select></label>',
        '<label>Name<input name="name" required placeholder="App or project name"></label>',
        '<label>Website<input name="websiteUrl" type="url" placeholder="https://"></label>',
        '<label>GitHub / repository<input name="githubUrl" type="url" placeholder="https://github.com/..."></label>',
        '<label>Category<input name="category" placeholder="Client, Relay, Wallet, Media, Developer Tool"></label>',
        '<label>Supported NIPs<input name="supportedNips" placeholder="NIP-07, NIP-46, NIP-57"></label>',
        '<label>Description<textarea name="description" required placeholder="What does it do and why does it belong on this page?"></textarea></label>'
      ].join("");
    }
    if (action === "report") {
      return [
        '<label>Reason<select name="reason"><option>spam</option><option>safety</option><option>outdated</option><option>duplicate</option><option>impersonation</option><option>low quality</option><option>other</option></select></label>',
        '<label>Details<textarea name="details" required placeholder="What should a moderator inspect?"></textarea></label>'
      ].join("");
    }
    if (action === "project") {
      return projectFields();
    }
    if (action === "app") {
      return appFields();
    }
    if (action === "article") {
      return articleFields();
    }
    if (action === "community") {
      return [
        '<label>Post type<select name="postType"><option>discussion</option><option>question</option><option>announcement</option><option>idea</option><option>project_update</option><option>app_update</option><option>guide</option><option>research_note</option></select></label>',
        '<label>Title<input name="title" required placeholder="Post title"></label>',
        '<label>Body<textarea name="body" required placeholder="Write the post."></textarea></label>',
        '<label>Tags<input name="tags" placeholder="apps, relays, beginner"></label>'
      ].join("");
    }
    return [
      '<label>Title optional<input name="title" placeholder="Short discussion title"></label>',
      '<label>Comment<textarea name="body" required placeholder="Add a signed comment or question."></textarea></label>'
    ].join("");
  }

  function projectFields() {
    return [
      '<label>Project name<input name="name" required placeholder="Project name"></label>',
      '<label>Tagline<input name="tagline" required placeholder="One-line value"></label>',
      '<label>Description<textarea name="description" required placeholder="What does it do? Who is it for?"></textarea></label>',
      '<label>Website<input name="websiteUrl" type="url" placeholder="https://"></label>',
      '<label>GitHub / repository<input name="githubUrl" type="url" placeholder="https://github.com/..."></label>',
      '<label>Nostr profile / maintainer<input name="nostrProfile" placeholder="npub, NIP-05 or profile URL"></label>',
      '<label>Category<input name="category" placeholder="Client, Relay, Wallet, Media, Developer Tool"></label>',
      '<label>Status<select name="projectStatus"><option>idea</option><option>prototype</option><option>active</option><option>maintained</option><option>beta</option><option>production</option><option>deprecated</option><option>archived</option><option>unknown</option></select></label>',
      '<label>Supported NIPs<input name="supportedNips" placeholder="NIP-07, NIP-46, NIP-57"></label>',
      '<label>Tags<input name="tags" placeholder="client, signer, media"></label>'
    ].join("");
  }

  function appFields() {
    return [
      '<label>App name<input name="name" required placeholder="App name"></label>',
      '<label>Tagline<input name="tagline" required placeholder="One-line value"></label>',
      '<label>Description<textarea name="description" required placeholder="What does it do?"></textarea></label>',
      '<label>Platform<select name="platform"><option>web</option><option>ios</option><option>android</option><option>desktop</option><option>cli</option><option>extension</option><option>library</option><option>relay</option><option>wallet</option><option>signer</option><option>other</option></select></label>',
      '<label>Category<input name="category" placeholder="Client, Signer, Wallet, Media, Developer Tool"></label>',
      '<label>Key handling<select name="keyHandling"><option>none</option><option>nip07</option><option>remote_signer</option><option>local_key</option><option>unknown</option></select></label>',
      '<label>Website<input name="websiteUrl" type="url" placeholder="https://"></label>',
      '<label>GitHub / repository<input name="githubUrl" type="url" placeholder="https://github.com/..."></label>',
      '<label>Supported NIPs<input name="supportedNips" placeholder="NIP-07, NIP-46, NIP-57"></label>'
    ].join("");
  }

  function articleFields() {
    return [
      '<label>Title<input name="title" required placeholder="Article title"></label>',
      '<label>Excerpt<textarea name="excerpt" required placeholder="Short summary."></textarea></label>',
      '<label>Body<textarea name="body" required placeholder="Write the community article."></textarea></label>',
      '<label>Tags<input name="tags" placeholder="guide, relay, NIP-23"></label>',
      '<label>Related Crays pages<input name="relatedTargetIds" placeholder="/nostr/what-is-nostr/, /nostr/nip-07-signers/"></label>'
    ].join("");
  }

  function contributionFormHtml(action, target, title) {
    return [
      '<div class="crays-nostr-contribution-form-shell">',
      '<p class="crays-nostr-live-kicker">Contribution layer</p>',
      '<h2 id="crays-contribution-drawer-title">', escapeHtml(title), '</h2>',
      '<p>', escapeHtml(formIntro(action)), '</p>',
      '<div class="crays-nostr-signer-note"><strong>Connect with Nostr</strong><span>Use a browser signer. Never paste a private key. Signed contributions publish to Damus, Primal and other public relays.</span></div>',
      '<form class="crays-nostr-contribution-form" data-contribution-form data-contribution-action="', escapeHtml(action), '">',
      '<input type="hidden" name="targetId" value="', escapeHtml(target.id), '">',
      '<input type="hidden" name="targetSlug" value="', escapeHtml(target.targetSlug), '">',
      '<input type="hidden" name="canonicalUrl" value="', escapeHtml(target.canonicalUrl), '">',
      '<input type="hidden" name="route" value="', escapeHtml(target.route), '">',
      drawerFields(action),
      '<label class="crays-nostr-checkline"><input type="checkbox" name="signNow" value="1" checked> <span>Sign and publish to public relays</span></label>',
      '<div class="crays-nostr-contribution-actions"><button type="submit">Send to review</button><button type="button" data-nostr-login-launch="welcome">Connect with Nostr</button></div>',
      '<p class="crays-nostr-form-status" data-contribution-status>Pending review after submit.</p>',
      '</form>',
      '</div>'
    ].join("");
  }

  function openContributionDrawer(action, panel) {
    var drawer = ensureContributionDrawer();
    var target = targetFromPanel(panel);
    var title = {
      discuss: "Discuss this page",
      discussion: "Discuss this page",
      question: "Ask a question",
      source: "Suggest a source",
      correction: "Suggest a correction",
      relation: "Add related app/project",
      report: "Report a problem"
    }[action] || "Contribute";
    drawer.querySelector("[data-contribution-drawer-content]").innerHTML = contributionFormHtml(action, target, title);
    drawer.hidden = false;
    document.documentElement.classList.add("crays-nostr-drawer-open");
    var first = drawer.querySelector("input:not([type='hidden']), textarea, select, button");
    if (first) first.focus();
  }

  function contributionPayload(form) {
    var data = formData(form);
    var action = form.getAttribute("data-contribution-action") || "discussion";
    var type = actionType(action);
    if (data.relationType) type = data.relationType;
    var session = getSession() || {};
    var tags = String(data.tags || data.supportedNips || "").split(/[,;\s]+/).filter(Boolean);
    return {
      id: "contribution-" + Date.now(),
      type: type,
      targetId: data.targetId || "",
      targetSlug: data.targetSlug || "",
      canonicalUrl: data.canonicalUrl || "",
      route: data.route || "",
      title: data.title || data.name || data.issueSummary || data.url || type,
      body: data.body || data.description || data.reason || data.details || data.suggestedChange || data.excerpt || "",
      url: data.url || data.websiteUrl || data.evidenceUrl || "",
      name: data.name || "",
      slug: slugify(data.name || data.title || type),
      tagline: data.tagline || "",
      description: data.description || "",
      websiteUrl: data.websiteUrl || "",
      githubUrl: data.githubUrl || "",
      nostrProfile: data.nostrProfile || "",
      category: data.category || "",
      platform: data.platform || "",
      keyHandling: data.keyHandling || "",
      projectStatus: data.projectStatus || "pending",
      sourceType: data.sourceType || "",
      reason: data.reason || data.details || "",
      issueSummary: data.issueSummary || "",
      currentText: data.currentText || "",
      suggestedChange: data.suggestedChange || "",
      evidenceUrl: data.evidenceUrl || "",
      postType: data.postType || "",
      tags: tags,
      supportedNips: tags.filter(function (tag) { return /^nip[-_ ]?\d+/i.test(tag); }),
      relatedTargetIds: String(data.relatedTargetIds || "").split(/[,;\s]+/).filter(Boolean),
      authorPubkey: session.pubkey || "",
      authorNpub: session.npub || "",
      status: "pending",
      moderationState: "pending_review",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
  }

  async function saveContributionForm(form) {
    var status = form.querySelector("[data-contribution-status]");
    var services = contributionServices();
    if (!services) {
      if (status) status.textContent = "Contribution services are not loaded yet.";
      return;
    }
    var payload = contributionPayload(form);
    var draft = services.NostrEventDraftService.mapContributionToNostrEventDraft(payload);
    payload.nostrKind = draft.kind;
    payload.relayUrls = draft.relayUrls || [];
    var shouldSign = Boolean(new FormData(form).get("signNow") || "");
    if (status) status.textContent = "Preparing signed Nostr contribution...";
    if (shouldSign && services.NostrAuthService.detectSigner()) {
      try {
        if (status) status.textContent = "Waiting for browser signer...";
        var pubkey = await services.NostrAuthService.getPublicKey();
        saveSession({ pubkey: pubkey, method: "signer", readOnly: false, relays: payload.relayUrls || DEFAULT_RELAYS.slice(), updatedAt: new Date().toISOString() });
        draft.pubkey = pubkey;
        var signed = await services.NostrAuthService.signEventDraft(draft);
        if (status) status.textContent = "Publishing signed event to public relays...";
        var publishResult = await services.NostrRelayService.publishEvent(signed, draft.relayUrls || DEFAULT_RELAYS);
        var relayResults = publishResult.relays || [];
        var publishedCount = relayResults.filter(function (item) { return item.ok; }).length;
        payload.authorPubkey = pubkey;
        payload.nostrEventId = signed.id || "";
        payload.relayPublishStatus = services.NostrRelayService.handlePublishResult(publishResult);
        payload.publishResults = relayResults;
        payload.status = "pending";
        payload.moderationState = "pending_review";
        addQueueItem({ type: payload.type, title: payload.title, unsignedEvent: draft, signedEvent: signed, published: publishResult.ok, publishResults: relayResults });
        setPreview({ signedEvent: signed, publishResult: publishResult });
        if (status) status.textContent = publishResult.ok ? "Published to " + publishedCount + " public relay(s). Pending review." : "Signed, but relays rejected or timed out. Saved as pending review with relay results.";
      } catch (error) {
        payload.status = "draft";
        payload.moderationState = "pending_review";
        payload.relayPublishStatus = "local_only";
        addQueueItem({ type: payload.type, title: payload.title, unsignedEvent: draft, error: error.message || String(error) });
        setPreview(draft);
        if (status) status.textContent = (error.message || "Signer failed") + " Local draft saved; no private key was requested.";
      }
    } else {
      if (shouldSign) launchNostrLogin("welcome");
      payload.status = "draft";
      payload.moderationState = "pending_review";
      payload.relayPublishStatus = "local_only";
      addQueueItem({ type: payload.type, title: payload.title, unsignedEvent: draft, error: "Signer required. Connect a browser signer to publish this contribution to public relays." });
      setPreview(draft);
      if (status) status.textContent = "Signer required for relay publishing. Local draft saved; never paste a private key.";
    }
    var saved = services.ContributionService.create(payload);
    form.reset();
    renderPageContributionSummaries();
    renderModerationQueues();
    return saved;
  }

  function renderStartContributionPanel(panel) {
    if (!panel || panel.getAttribute("data-start-contribution-rendered") === "true") return;
    var pageSlug = panel.getAttribute("data-page-slug") || "";
    var pageRoute = pageSlug || (window.location.pathname || "").replace(/^\/nostr\/|\/$/g, "") || "start";
    var query = "?page=" + encodeURIComponent(pageSlug || pageRoute) + "&amp;route=" + encodeURIComponent(pageRoute);
    panel.classList.add("crays-nostr-start-contribute", "crays-nostr-context-actions--start-style");
    panel.setAttribute("data-start-contribution-rendered", "true");
    panel.setAttribute("data-component", "PageContributionBar StartContributionPanel");
    panel.innerHTML = [
      '<div>',
      '<p class="crays-nostr-live-kicker">Bring something back</p>',
      '<h2>Ask, suggest, submit or nominate.</h2>',
      '<p>Ask a question, send a source, suggest a fix, submit a project or nominate a public Nostr account. The article stays stable; your contribution gets reviewed beside it.</p>',
      '</div>',
      '<nav aria-label="Ways to contribute">',
      '<a href="/nostr/community/questions/' + query + '"><strong>Ask a question</strong><span>If something does not click yet, ask where you got stuck.</span></a>',
      '<a href="/nostr/community/projects/submit/' + query + '"><strong>Submit a project</strong><span>Found or built a client, relay, signer, wallet or media tool? Send it in.</span></a>',
      '<a href="/nostr/community/suggestions/' + query + '&amp;type=source"><strong>Suggest a source or fix</strong><span>Share a better source, a stale claim, a broken link or a correction.</span></a>',
      '<a href="/nostr/people/users/' + query + '"><strong>Nominate someone</strong><span>Add a public Nostr user, builder or creator with evidence we can check.</span></a>',
      '</nav>'
    ].join("");
  }

  function renderPageContributionSummaries() {
    $("[data-nostr-page-panel]").forEach(function (panel) {
      renderStartContributionPanel(panel);
    });
  }

  function cardList(items, label) {
    if (!items || !items.length) return '<p class="crays-nostr-empty-state">No items yet. Start the first one.</p>';
    var componentName = {
      "Project": "ProjectCard",
      "Community Question": "QuestionCard",
      "Community article": "ArticleSubmissionCard",
      "Suggested Source": "SourceSuggestionCard",
      "Correction": "CorrectionSuggestionCard",
      "Community": "CommunityCard",
      "Discussion": "CommunityPostCard",
      "Contributor": "ContributorProfileCard",
      "Badge": "ContributionStatusBadge",
      "Curated List": "CuratedListCard"
    }[label] || "ContributionStatusBadge";
    return items.map(function (item) {
      var title = item.title || item.name || item.id;
      var body = item.body || item.description || item.reason || item.excerpt || item.tagline || "";
      var state = item.status || item.moderationState || "approved";
      return [
        '<article class="crays-nostr-product-object-card" data-component="', componentName, '">',
        '<p class="crays-nostr-status-pill">', escapeHtml(label || state), '</p>',
        '<h3>', escapeHtml(title), '</h3>',
        '<p>', escapeHtml(body), '</p>',
        item.url || item.websiteUrl ? '<a href="' + escapeHtml(item.url || item.websiteUrl) + '" target="_blank" rel="noreferrer noopener">Open source</a>' : '',
        '</article>'
      ].join("");
    }).join("");
  }

  function productMount() {
    var existing = document.querySelector("[data-contribution-product-surface]");
    if (existing) return existing;
    var masthead = document.querySelector(".crays-nostr-article-masthead");
    if (!masthead || !masthead.parentNode) return null;
    var surface = document.createElement("section");
    surface.className = "crays-nostr-product-surface";
    surface.setAttribute("data-contribution-product-surface", "");
    masthead.insertAdjacentElement("afterend", surface);
    return surface;
  }

  function inlineForm(action, title, intro) {
    var target = targetFromPanel(null);
    var componentName = {
      project: "ProjectSubmissionForm",
      app: "AppSubmissionForm",
      article: "ArticleSubmissionForm",
      community: "CommunityPostComposer",
      list: "CuratedListCard"
    }[action] || "ContributionForm";
    return [
      '<div class="crays-nostr-inline-product-form" data-component="', componentName, '">',
      '<h2>', escapeHtml(title), '</h2>',
      '<p>', escapeHtml(intro), '</p>',
      '<div class="crays-nostr-signer-note"><strong>Connect with Nostr</strong><span>Use a browser signer. Never paste a private key. Signed contributions publish to Damus, Primal and other public relays.</span></div>',
      '<form class="crays-nostr-contribution-form" data-contribution-form data-contribution-action="', escapeHtml(action), '">',
      '<input type="hidden" name="targetId" value="', escapeHtml(target.id), '">',
      '<input type="hidden" name="targetSlug" value="', escapeHtml(target.targetSlug), '">',
      '<input type="hidden" name="canonicalUrl" value="', escapeHtml(target.canonicalUrl), '">',
      '<input type="hidden" name="route" value="', escapeHtml(target.route), '">',
      drawerFields(action),
      '<label class="crays-nostr-checkline"><input type="checkbox" name="signNow" value="1" checked> <span>Sign and publish to public relays</span></label>',
      '<div class="crays-nostr-contribution-actions"><button type="submit">Send to review</button><button type="button" data-nostr-login-launch="welcome">Connect with Nostr</button></div>',
      '<p class="crays-nostr-form-status" data-contribution-status>Pending review after submit.</p>',
      '</form>',
      '</div>'
    ].join("");
  }

  function renderContributionRouteWidgets() {
    var path = window.location.pathname.replace(/\/+$/, "/");
    var mock = contributionMock();
    var services = contributionServices();
    var routePaths = [
      "/nostr/community/projects/submit/",
      "/nostr/community/apps/submit/",
      "/nostr/community/articles/submit/",
      "/nostr/community/questions/",
      "/nostr/community/projects/",
      "/nostr/community/articles/",
      "/nostr/community/suggestions/",
      "/nostr/community/",
      "/nostr/community/contributors/",
      "/nostr/community/curated-lists/",
      "/nostr/community/moderation/"
    ];
    if (routePaths.indexOf(path) === -1) return;
    if (!services) return;
    var surface = productMount();
    if (!surface) return;
    if (path === "/nostr/community/projects/submit/") {
      surface.innerHTML = inlineForm("project", "Submit a Nostr Project", "Add a project as a separate pending record. The archive text stays unchanged.");
    } else if (path === "/nostr/community/apps/submit/") {
      surface.innerHTML = inlineForm("app", "Submit a Nostr App", "Add platform, key handling and supported NIPs so reviewers can classify it safely.");
    } else if (path === "/nostr/community/articles/submit/") {
      surface.innerHTML = inlineForm("article", "Submit a Community Article", "Community articles are separate from canonical Crays editorial pages.");
    } else if (path === "/nostr/community/questions/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Nostr Q&A</h2><button type="button" data-contribution-action="question">Ask a question</button></div><div class="crays-nostr-object-grid">' + cardList(mock.questions, "Community Question") + '</div>';
    } else if (path === "/nostr/community/projects/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Project directory</h2><button type="button" data-contribution-action="project">Submit project</button></div><div class="crays-nostr-object-grid">' + cardList(services.ProjectDirectoryService.listProjects(), "Project") + '</div>';
    } else if (path === "/nostr/community/articles/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Community publishing</h2><button type="button" data-contribution-action="article">Submit article</button></div><div class="crays-nostr-object-grid">' + cardList(mock.articleSubmissions, "Community article") + '</div>';
    } else if (path === "/nostr/community/suggestions/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Suggestions queue</h2><button type="button" data-contribution-action="source">Suggest source</button><button type="button" data-contribution-action="correction">Suggest correction</button></div><div class="crays-nostr-object-grid">' + cardList(mock.sourceSuggestions, "Suggested Source") + cardList(mock.correctionSuggestions, "Correction") + '</div>';
    } else if (path === "/nostr/community/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Community areas</h2><button type="button" data-contribution-action="community">Create post</button></div><div class="crays-nostr-object-grid">' + cardList(mock.communities, "Community") + cardList(mock.communityPosts, "Discussion") + '</div>';
    } else if (path === "/nostr/community/contributors/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Contributor profiles</h2></div><div class="crays-nostr-object-grid">' + cardList(mock.contributorProfiles, "Contributor") + cardList(mock.badges, "Badge") + '</div>';
    } else if (path === "/nostr/community/curated-lists/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Curated lists</h2><button type="button" data-contribution-action="list">Create list idea</button></div><div class="crays-nostr-object-grid">' + cardList(mock.curatedLists, "Curated List") + '</div>';
    } else if (path === "/nostr/community/moderation/") {
      surface.innerHTML = '<div class="crays-nostr-board-head"><h2>Moderation queue</h2><button type="button" data-nostr-export-queue>Export local queue</button></div><div data-component="ModerationQueue" data-contribution-moderation-queue></div>';
      renderModerationQueues();
    }
  }

  function renderModerationQueues() {
    var services = contributionServices();
    var mock = contributionMock();
    var nodes = $("[data-contribution-moderation-queue]");
    if (!services || !nodes.length) return;
    var local = services.ContributionService.list();
    var pendingMock = []
      .concat(mock.sourceSuggestions || [])
      .concat(mock.correctionSuggestions || [])
      .concat(mock.appSubmissions || [])
      .concat(mock.projects || [])
      .concat(mock.articleSubmissions || [])
      .concat(mock.reports || [])
      .concat(mock.maintainerClaims || [])
      .filter(function (item) { return item.status === "pending"; });
    var items = local.concat(pendingMock);
    nodes.forEach(function (node) {
      if (!items.length) {
        node.innerHTML = '<p class="crays-nostr-empty-state">No pending review items yet.</p>';
        return;
      }
      node.innerHTML = items.map(function (item) {
        var title = item.title || item.name || item.issueSummary || item.reason || item.id;
        var type = item.type || item.sourceType || item.targetType || "submission";
        return [
          '<article class="crays-nostr-moderation-item" data-moderation-item="', escapeHtml(item.id), '">',
          '<div><p class="crays-nostr-status-pill">Pending review</p><h3>', escapeHtml(title), '</h3><p>', escapeHtml(item.body || item.description || item.reason || item.details || item.tagline || ""), '</p><code>', escapeHtml(type), '</code></div>',
          '<div class="crays-nostr-moderation-actions">',
          '<button type="button" data-moderation-action="approved" data-target-id="', escapeHtml(item.id), '">Approve</button>',
          '<button type="button" data-moderation-action="rejected" data-target-id="', escapeHtml(item.id), '">Reject</button>',
          '<button type="button" data-moderation-action="needs_changes" data-target-id="', escapeHtml(item.id), '">Needs changes</button>',
          '<button type="button" data-moderation-action="duplicate" data-target-id="', escapeHtml(item.id), '">Duplicate</button>',
          '</div></article>'
        ].join("");
      }).join("");
    });
  }

  function bindContributionLayer() {
    document.addEventListener("click", async function (event) {
      var actionButton = event.target.closest("[data-contribution-action]");
      if (actionButton) {
        var action = actionButton.getAttribute("data-contribution-action");
        var panel = actionButton.closest("[data-nostr-page-panel]");
        if (actionButton.tagName === "A") event.preventDefault();
        openContributionDrawer(action, panel);
        return;
      }
      var moderationButton = event.target.closest("[data-moderation-action]");
      if (moderationButton) {
        var services = contributionServices();
        if (!services) return;
        var targetId = moderationButton.getAttribute("data-target-id");
        var actionName = moderationButton.getAttribute("data-moderation-action");
        var item = moderationButton.closest("[data-moderation-item]");
        var pill = item && item.querySelector(".crays-nostr-status-pill");
        moderationButton.disabled = true;
        if (pill) pill.textContent = "Signing moderation";
        try {
          var result = await services.ModerationService.publishDecision({
            targetId: targetId,
            targetEventId: targetId,
            action: actionName,
            reason: "Crays Nostr moderation action: " + actionName,
            canonicalUrl: window.location.href,
            route: "moderation",
            tags: ["moderation", actionName]
          });
          if (!result.ok) throw new Error(result.message || "Moderation publish failed.");
          services.ModerationService.decide(targetId, actionName, "Server-authorized signed moderation event.");
          services.ContributionService.updateStatus(targetId, actionName, "Server-authorized signed moderation event.");
          addQueueItem({ type: "moderation_decision", title: actionName + " " + targetId, signedEvent: result.signedEvent, published: result.ok, publishResults: result.relays || [] });
          setPreview(result);
          if (item) {
            item.classList.add("is-reviewed");
            if (pill) pill.textContent = actionName.replace(/_/g, " ");
          }
        } catch (error) {
          setPreview({ moderationError: error.message || String(error), targetId: targetId, action: actionName });
          if (pill) pill.textContent = "Moderator auth required";
        } finally {
          moderationButton.disabled = false;
        }
      }
    });

    document.addEventListener("submit", function (event) {
      var form = event.target.closest("[data-contribution-form]");
      if (!form) return;
      event.preventDefault();
      saveContributionForm(form);
    });

    renderPageContributionSummaries();
    renderContributionRouteWidgets();
    window.setTimeout(renderContributionRouteWidgets, 150);
    renderModerationQueues();
  }

  function bind() {
    $("[data-nostr-login-launch]").forEach(function (button) {
      button.addEventListener("click", function () {
        launchNostrLogin(button.getAttribute("data-nostr-login-launch"));
      });
    });

    $("[data-nostr-readonly-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = (new FormData(form).get("npub") || "").toString().trim();
        if (!/^(npub1[0-9a-z]+|[0-9a-f]{64})$/i.test(value)) {
          setPreview({ error: "Enter an npub or 64-character hex public key." });
          return;
        }
        saveSession({ npub: value, pubkey: value, readOnly: true, method: "readOnly", updatedAt: new Date().toISOString() });
        setPreview({ readOnly: true, npub: value });
        form.reset();
      });
    });

    $("[data-nostr-logout]").forEach(function (button) {
      button.addEventListener("click", function () {
        clearSession();
        document.dispatchEvent(new Event("nlLogout"));
      });
    });

    $("[data-nostr-sign-challenge]").forEach(function (button) {
      button.addEventListener("click", signChallenge);
    });

    $("[data-nostr-event-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        handleEventForm(form);
      });
    });

    $("[data-nostr-vote]").forEach(function (button) {
      button.addEventListener("click", function () {
        recordVote(button);
      });
    });

    $("[data-nostr-export-queue]").forEach(function (button) {
      button.addEventListener("click", function () {
        setPreview(queue());
      });
    });

    $("[data-nostr-clear-queue]").forEach(function (button) {
      button.addEventListener("click", function () {
        saveQueue([]);
        setPreview({ cleared: true });
      });
    });

    document.addEventListener("nlAuth", function (event) {
      if (event.detail && (event.detail.type === "logout")) {
        clearSession();
        return;
      }
      ensureSigner().catch(function () {
        renderSession();
      });
    });

    renderSession();
    renderQueue();
    prefillForms();
    bindFeedFilters();
    updateVoteDisplays();
    bindContributionLayer();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
}());
