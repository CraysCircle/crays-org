(function () {
  var dictionaryNode = document.getElementById("crays-i18n-dictionary");
  if (!dictionaryNode) return;

  var dictionary = {};
  try {
    dictionary = JSON.parse(dictionaryNode.textContent || "{}");
  } catch {
    return;
  }

  var attributeNames = ["alt", "aria-label", "placeholder", "data-wait", "value", "content"];
  var ignoredTags = new Set(["SCRIPT", "STYLE", "SVG", "NOSCRIPT", "TEXTAREA"]);

  function normalize(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function translateTextNode(node) {
    var key = normalize(node.nodeValue);
    var value = dictionary[key];
    if (!value || value === key) return;
    var leading = (node.nodeValue.match(/^\s*/) || [""])[0];
    var trailing = (node.nodeValue.match(/\s*$/) || [""])[0];
    node.nodeValue = leading + value + trailing;
  }

  function translateAttributes(element) {
    attributeNames.forEach(function (name) {
      if (!element.hasAttribute || !element.hasAttribute(name)) return;
      var current = element.getAttribute(name);
      var key = normalize(current);
      var value = dictionary[key];
      if (value && value !== key) element.setAttribute(name, value);
    });
  }

  function translateRoot(root) {
    if (!root) return;
    if (root.nodeType === 1) {
      if (ignoredTags.has(root.tagName)) return;
      if (root.closest && root.closest(".crays-top-nav-language")) return;
      translateAttributes(root);
    }

    var walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (node.nodeType === Node.ELEMENT_NODE && ignoredTags.has(node.tagName)) {
          return NodeFilter.FILTER_REJECT;
        }
        if (node.nodeType === Node.ELEMENT_NODE && node.closest(".crays-top-nav-language")) {
          return NodeFilter.FILTER_REJECT;
        }
        if (node.parentElement && node.parentElement.closest(".crays-top-nav-language")) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    while (walker.nextNode()) {
      var node = walker.currentNode;
      if (node.nodeType === Node.TEXT_NODE) {
        translateTextNode(node);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        translateAttributes(node);
      }
    }
  }

  var scheduled = false;
  function scheduleTranslate() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () {
      scheduled = false;
      translateRoot(document.body);
    });
  }

  translateRoot(document.body);
  window.setTimeout(scheduleTranslate, 0);
  window.setTimeout(scheduleTranslate, 250);

  new MutationObserver(scheduleTranslate).observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: attributeNames,
  });
})();
