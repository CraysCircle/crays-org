import { getEventHash, nip19, verifyEvent } from "nostr-tools";

export const DEFAULT_RELAYS = [
  "wss://relay.damus.io",
  "wss://nos.lol",
  "wss://relay.primal.net",
  "wss://relay.nostr.band",
];

export const DEFAULT_MODERATOR_NPUBS = [
  "npub1vygkk63nzyltpe87520290y4z73m0kpprursagzwyv6uv6npau4snwxws3",
];

export const CONTRIBUTION_KINDS = [
  1,
  7,
  8,
  1111,
  1984,
  30000,
  30001,
  30009,
  30023,
  30078,
  30402,
  31989,
  34550,
  4550,
  9734,
  27235,
];

export function relaysFromEnv(value = process.env.CRAYS_NOSTR_RELAYS) {
  const configured = String(value || "")
    .split(/[,\s]+/)
    .map((item) => item.trim())
    .filter((item) => /^wss:\/\//i.test(item));

  return Array.from(new Set(configured.length ? configured : DEFAULT_RELAYS));
}

export function moderatorPubkeysFromEnv(value = process.env.CRAYS_NOSTR_MODERATOR_PUBKEYS) {
  const configured = String(value || "")
    .split(/[,\s]+/)
    .map((item) => item.trim())
    .filter(Boolean);

  return Array.from(new Set([...DEFAULT_MODERATOR_NPUBS, ...configured].map(normalizeModeratorPubkey).filter(Boolean)));
}

function normalizeModeratorPubkey(value) {
  const item = String(value || "").trim().toLowerCase();
  if (/^[0-9a-f]{64}$/.test(item)) return item;
  if (!/^npub1[023456789acdefghjklmnpqrstuvwxyz]+$/i.test(item)) return "";

  try {
    const decoded = nip19.decode(item);
    if (decoded.type === "npub" && /^[0-9a-f]{64}$/.test(decoded.data)) {
      return decoded.data.toLowerCase();
    }
  } catch {}

  return "";
}

export function sendJson(response, status, payload) {
  response.statusCode = status;
  response.setHeader("content-type", "application/json; charset=utf-8");
  response.setHeader("access-control-allow-origin", "*");
  response.setHeader("access-control-allow-methods", "GET,POST,OPTIONS");
  response.setHeader("access-control-allow-headers", "content-type");
  response.end(JSON.stringify(payload));
}

export function handleOptions(request, response) {
  if (request.method !== "OPTIONS") return false;
  sendJson(response, 204, {});
  return true;
}

export async function readJsonBody(request) {
  const chunks = [];
  for await (const chunk of request) chunks.push(Buffer.from(chunk));
  const raw = Buffer.concat(chunks).toString("utf8");
  if (!raw) return {};
  const body = JSON.parse(raw);
  assertNoPrivateKeyMaterial(body);
  return body;
}

export function assertNoPrivateKeyMaterial(value) {
  const privateKeyPrefix = "nsec" + "1";
  const privateKeyPattern = new RegExp(`\\b${privateKeyPrefix}[023456789acdefghjklmnpqrstuvwxyz]+\\b`, "i");
  const forbiddenKeys = new Set([
    "nsec",
    "privatekey",
    "private_key",
    "secretkey",
    "secret_key",
    "seedphrase",
    "seed_phrase",
    "mnemonic",
  ]);

  function visit(item, key = "") {
    const normalizedKey = String(key || "").replace(/[-_\s]/g, "").toLowerCase();
    if (forbiddenKeys.has(String(key || "").toLowerCase()) || forbiddenKeys.has(normalizedKey)) {
      throw new Error("Private-key material must never be sent to Crays. Use a browser signer instead.");
    }

    if (typeof item === "string") {
      if (privateKeyPattern.test(item)) {
        throw new Error("Private-key material must never be sent to Crays. Use a browser signer instead.");
      }
      return;
    }

    if (Array.isArray(item)) {
      item.forEach((entry) => visit(entry));
      return;
    }

    if (item && typeof item === "object") {
      Object.entries(item).forEach(([childKey, childValue]) => visit(childValue, childKey));
    }
  }

  visit(value);
}

export function assertSignedContributionEvent(event, allowedKinds = CONTRIBUTION_KINDS) {
  if (!event || typeof event !== "object") {
    throw new Error("Missing signed Nostr event.");
  }

  if (!Number.isInteger(event.kind) || !allowedKinds.includes(event.kind)) {
    throw new Error("This event kind is not accepted by the Crays Nostr contribution layer.");
  }

  if (!event.id || !event.pubkey || !event.sig) {
    throw new Error("Event must include id, pubkey and sig.");
  }

  if (getEventHash(event) !== event.id) {
    throw new Error("Event id does not match the event hash.");
  }

  if (!verifyEvent(event)) {
    throw new Error("Event signature could not be verified.");
  }

  if (containsPrivateKeySignal(event)) {
    throw new Error("Contribution appears to contain a private-key secret. It was rejected before relay publish.");
  }

  return event;
}

function containsPrivateKeySignal(event) {
  const content = typeof event.content === "string" ? event.content : "";
  const tags = Array.isArray(event.tags) ? JSON.stringify(event.tags) : "";
  const privateKeyPrefix = "nsec" + "1";
  const privateKeyPattern = new RegExp(`\\b${privateKeyPrefix}[023456789acdefghjklmnpqrstuvwxyz]+\\b`, "i");
  return privateKeyPattern.test(`${content} ${tags}`);
}

export function isModerator(pubkey) {
  const moderators = moderatorPubkeysFromEnv();
  return moderators.includes(String(pubkey || "").toLowerCase());
}

export async function publishToRelays(event, relayUrls = relaysFromEnv()) {
  const relays = Array.from(new Set(relayUrls.filter((relay) => /^wss:\/\//i.test(relay)))).slice(0, 8);
  const results = await Promise.all(relays.map((relay) => publishToRelay(relay, event)));
  return {
    ok: results.some((result) => result.ok),
    relays: results,
  };
}

function publishToRelay(relay, event) {
  return new Promise((resolve) => {
    if (typeof WebSocket !== "function") {
      resolve({ relay, ok: false, message: "WebSocket is not available in this runtime." });
      return;
    }

    let socket;
    let settled = false;
    const timer = setTimeout(() => finish(false, "timeout"), 9000);

    function finish(ok, message = "") {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try {
        if (socket) socket.close();
      } catch {}
      resolve({ relay, ok, message });
    }

    try {
      socket = new WebSocket(relay);
      socket.addEventListener("open", () => {
        socket.send(JSON.stringify(["EVENT", event]));
      });
      socket.addEventListener("message", (message) => {
        let payload;
        try {
          payload = JSON.parse(message.data);
        } catch {
          payload = null;
        }
        if (payload && payload[0] === "OK" && payload[1] === event.id) {
          finish(Boolean(payload[2]), payload[3] || "");
        }
      });
      socket.addEventListener("error", () => finish(false, "connection error"));
    } catch (error) {
      finish(false, error.message || String(error));
    }
  });
}

export async function fetchEventsByTarget(target, options = {}) {
  const relays = options.relays || relaysFromEnv();
  const limit = Math.max(1, Math.min(Number(options.limit || 50), 100));
  const kinds = options.kinds || CONTRIBUTION_KINDS;
  const normalizedTarget = String(target || "").trim();

  if (!normalizedTarget) {
    return { ok: false, events: [], relays: [], message: "Missing target." };
  }

  const filters = [
    { kinds, "#I": [normalizedTarget], limit },
    { kinds, "#r": [normalizedTarget], limit },
  ];

  const results = await Promise.all(relays.slice(0, 8).map((relay) => fetchFromRelay(relay, filters, limit)));
  const seen = new Set();
  const events = results
    .flatMap((result) => result.events)
    .filter((event) => {
      if (!event || seen.has(event.id)) return false;
      seen.add(event.id);
      return true;
    })
    .sort((a, b) => Number(b.created_at || 0) - Number(a.created_at || 0))
    .slice(0, limit);

  return {
    ok: results.some((result) => result.ok),
    events,
    relays: results,
  };
}

function fetchFromRelay(relay, filters, limit) {
  return new Promise((resolve) => {
    if (typeof WebSocket !== "function") {
      resolve({ relay, ok: false, events: [], message: "WebSocket is not available in this runtime." });
      return;
    }

    let socket;
    let settled = false;
    const events = [];
    const subscriptionId = `crays-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const timer = setTimeout(() => finish(true, "timeout"), 5500);

    function finish(ok, message = "") {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try {
        if (socket) {
          socket.send(JSON.stringify(["CLOSE", subscriptionId]));
          socket.close();
        }
      } catch {}
      resolve({ relay, ok, events, message });
    }

    try {
      socket = new WebSocket(relay);
      socket.addEventListener("open", () => {
        socket.send(JSON.stringify(["REQ", subscriptionId, ...filters]));
      });
      socket.addEventListener("message", (message) => {
        let payload;
        try {
          payload = JSON.parse(message.data);
        } catch {
          payload = null;
        }
        if (!payload || payload[1] !== subscriptionId) return;
        if (payload[0] === "EVENT" && payload[2]) {
          events.push(payload[2]);
          if (events.length >= limit) finish(true);
        }
        if (payload[0] === "EOSE") finish(true);
      });
      socket.addEventListener("error", () => finish(false, "connection error"));
    } catch (error) {
      finish(false, error.message || String(error));
    }
  });
}
