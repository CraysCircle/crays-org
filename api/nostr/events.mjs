import {
  CONTRIBUTION_KINDS,
  fetchEventsByTarget,
  handleOptions,
  relaysFromEnv,
  sendJson,
} from "../../lib/nostr-server.mjs";

export default async function handler(request, response) {
  if (handleOptions(request, response)) return;

  if (request.method !== "GET") {
    sendJson(response, 405, { ok: false, message: "GET events by target." });
    return;
  }

  try {
    const url = new URL(request.url || "/", "https://www.crays.org");
    const target = url.searchParams.get("target") || "";
    const limit = Number(url.searchParams.get("limit") || 50);
    const relays = url.searchParams.getAll("relay").length ? url.searchParams.getAll("relay") : relaysFromEnv();
    const result = await fetchEventsByTarget(target, { relays, kinds: CONTRIBUTION_KINDS, limit });

    sendJson(response, 200, result);
  } catch (error) {
    sendJson(response, 400, {
      ok: false,
      events: [],
      message: error.message || String(error),
    });
  }
}
