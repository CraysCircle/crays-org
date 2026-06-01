(function () {
  "use strict";

  var MAX_RESULTS = 24;
  var indexPromise = null;

  function normalize(value) {
    return String(value || "")
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9+#.]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function tokenize(query) {
    return normalize(query).split(" ").filter(Boolean);
  }

  function unique(values) {
    return values.filter(function (value, index) {
      return value && values.indexOf(value) === index;
    });
  }

  function tokenVariants(token) {
    var variants = [token];
    if (token.length > 3 && token.slice(-3) === "ies") variants.push(token.slice(0, -3) + "y");
    if (token.length > 3 && token.slice(-2) === "es") variants.push(token.slice(0, -2));
    if (token.length > 2 && token.slice(-1) === "s") variants.push(token.slice(0, -1));
    if (token.length > 2 && token.slice(-1) === "y") variants.push(token.slice(0, -1) + "ies");
    variants.push(token + "s");
    return unique(variants);
  }

  function includesAny(text, variants) {
    return variants.some(function (variant) { return text.indexOf(variant) !== -1; });
  }

  function prepare(record) {
    if (record._prepared) return record;
    record._title = normalize(record.title);
    record._slug = normalize(record.slug);
    record._category = normalize(record.category);
    record._shelf = normalize(record.shelf);
    record._deck = normalize(record.deck);
    record._terms = normalize(record.terms);
    record._titleWords = record._title.split(" ");
    record._slugWords = record._slug.split(" ");
    record._prepared = true;
    return record;
  }

  function wordPrefixScore(words, variants, points) {
    return variants.some(function (variant) {
      return words.some(function (word) { return word.indexOf(variant) === 0; });
    }) ? points : 0;
  }

  function scoreRecord(rawRecord, rawQuery, tokens) {
    var record = prepare(rawRecord);
    var phrase = normalize(rawQuery);
    if (!phrase || !tokens.length) return 0;

    var score = 0;
    if (record._title === phrase) score += 6000;
    else if (record._title.indexOf(phrase) === 0) score += 3800;
    else if (record._title.indexOf(phrase) !== -1) score += 1800;

    if (record._slug === phrase) score += 4200;
    else if (record._slug.indexOf(phrase) === 0) score += 2200;
    else if (record._slug.indexOf(phrase) !== -1) score += 900;

    if (record._category.indexOf(phrase) !== -1) score += 500;
    if (record._shelf.indexOf(phrase) !== -1) score += 420;
    if (record._deck.indexOf(phrase) !== -1) score += 320;
    if (record._terms.indexOf(phrase) !== -1) score += 180;

    for (var i = 0; i < tokens.length; i += 1) {
      var token = tokens[i];
      var variants = tokenVariants(token);
      const allowBroadMatch = token.length > 1;
      var matched = false;
      var tokenScore = 0;

      if (variants.indexOf(record._title) !== -1) {
        tokenScore += 2200;
        matched = true;
      } else {
        var titlePrefix = wordPrefixScore(record._titleWords, variants, 1500);
        if (titlePrefix) {
          tokenScore += titlePrefix;
          matched = true;
        } else if (allowBroadMatch && includesAny(record._title, variants)) {
          tokenScore += 1050;
          matched = true;
        }
      }

      var slugPrefix = wordPrefixScore(record._slugWords, variants, 760);
      if (slugPrefix) {
        tokenScore += slugPrefix;
        matched = true;
      } else if (allowBroadMatch && includesAny(record._slug, variants)) {
        tokenScore += 460;
        matched = true;
      }

      if (allowBroadMatch && includesAny(record._category, variants)) {
        tokenScore += 250;
        matched = true;
      }
      if (allowBroadMatch && includesAny(record._shelf, variants)) {
        tokenScore += 210;
        matched = true;
      }
      if (allowBroadMatch && includesAny(record._deck, variants)) {
        tokenScore += 160;
        matched = true;
      }
      if (allowBroadMatch && includesAny(record._terms, variants)) {
        tokenScore += 70;
        matched = true;
      }

      if (!matched) return 0;
      score += tokenScore;
    }

    score -= Math.min(record.title.length, 90) * 0.4;
    return score;
  }

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch("/nostr/search-index.json", { credentials: "same-origin" })
        .then(function (response) {
          if (!response.ok) throw new Error("Search index could not be loaded.");
          return response.json();
        })
        .then(function (payload) {
          return Array.isArray(payload.pages) ? payload.pages : [];
        });
    }
    return indexPromise;
  }

  function renderResult(record, index) {
    var meta = [record.category, record.shelf].filter(Boolean).join(" / ");
    return [
      '<a href="', escapeHtml(record.url), '" role="option" data-nostr-search-result="', index, '">',
      '<strong>', escapeHtml(record.title), '</strong>',
      '<small>', escapeHtml(meta), '</small>',
      record.deck ? '<em>' + escapeHtml(record.deck) + '</em>' : '',
      '</a>'
    ].join("");
  }

  function setActive(list, index) {
    var links = Array.prototype.slice.call(list.querySelectorAll("a"));
    links.forEach(function (link, i) {
      if (i === index) link.setAttribute("aria-selected", "true");
      else link.removeAttribute("aria-selected");
    });
  }

  function initAtlasFinder() {
    var input = document.querySelector("[data-nostr-finder-input]");
    var container = document.querySelector("[data-nostr-finder-results]");
    var list = document.querySelector("[data-nostr-finder-list]");
    var status = document.querySelector("[data-nostr-finder-status]");
    if (!input || !container || !list || !status) return;

    var records = [];
    var activeIndex = -1;

    function showStatus(message) {
      status.textContent = message;
      status.hidden = false;
    }

    function runSearch() {
      var query = input.value.trim();
      activeIndex = -1;
      if (!query) {
        list.innerHTML = "";
        container.hidden = true;
        return;
      }
      container.hidden = false;
      var tokens = tokenize(query);
      if (!records.length) {
        list.innerHTML = "";
        showStatus("Loading the full atlas index.");
        return;
      }

      var matches = records
        .map(function (record) {
          return { record: record, score: scoreRecord(record, query, tokens) };
        })
        .filter(function (entry) { return entry.score > 0; })
        .sort(function (left, right) {
          if (right.score !== left.score) return right.score - left.score;
          return left.record.title.localeCompare(right.record.title);
        });

      if (!matches.length) {
        list.innerHTML = "";
        showStatus("No atlas pages match this term yet.");
        return;
      }

      var visible = matches.slice(0, MAX_RESULTS);
      status.hidden = false;
      status.textContent = matches.length === visible.length
        ? matches.length + " atlas match" + (matches.length === 1 ? "" : "es")
        : matches.length + " atlas matches. Showing the strongest " + visible.length + ".";
      list.innerHTML = visible.map(function (entry, index) {
        return renderResult(entry.record, index);
      }).join("");
    }

    input.addEventListener("input", runSearch);
    input.addEventListener("focus", function () {
      if (input.value.trim()) runSearch();
    });
    input.addEventListener("keydown", function (event) {
      var links = Array.prototype.slice.call(list.querySelectorAll("a"));
      if (container.hidden || !links.length) return;
      if (event.key === "ArrowDown") {
        event.preventDefault();
        activeIndex = Math.min(activeIndex + 1, links.length - 1);
        setActive(list, activeIndex);
        links[activeIndex].scrollIntoView({ block: "nearest" });
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
        setActive(list, activeIndex);
        links[activeIndex].scrollIntoView({ block: "nearest" });
      } else if (event.key === "Enter") {
        event.preventDefault();
        var target = links[activeIndex >= 0 ? activeIndex : 0];
        if (target) window.location.href = target.href;
      } else if (event.key === "Escape") {
        container.hidden = true;
      }
    });

    document.addEventListener("click", function (event) {
      if (!container.contains(event.target) && event.target !== input) {
        container.hidden = true;
      }
    });

    loadIndex()
      .then(function (loadedRecords) {
        records = loadedRecords;
        showStatus(records.length + " atlas pages indexed.");
        if (input.value.trim()) runSearch();
      })
      .catch(function () {
        showStatus("The atlas index is unavailable right now.");
      });
  }

  function filterLinks(input, container) {
    if (!input || !container) return;
    var links = Array.prototype.slice.call(container.querySelectorAll("a"));
    var sections = Array.prototype.slice.call(container.querySelectorAll("[data-nostr-index-section]"));
    input.addEventListener("input", function () {
      var query = normalize(input.value);
      links.forEach(function (link) {
        link.hidden = !!query && normalize(link.textContent).indexOf(query) === -1;
      });
      sections.forEach(function (section) {
        var visible = Array.prototype.slice.call(section.querySelectorAll("a")).some(function (link) {
          return !link.hidden;
        });
        section.hidden = !!query && !visible;
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initAtlasFinder();
      filterLinks(document.querySelector("[data-nostr-index-filter]"), document.querySelector("[data-nostr-index]"));
    });
  } else {
    initAtlasFinder();
    filterLinks(document.querySelector("[data-nostr-index-filter]"), document.querySelector("[data-nostr-index]"));
  }
}());
