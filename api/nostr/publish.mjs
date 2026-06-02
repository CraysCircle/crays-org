import {
  assertSignedContributionEvent,
  handleOptions,
  publishToRelays,
  readJsonBody,
  relaysFromEnv,
  sendJson,
} from "../../lib/nostr-server.mjs";

export default async function handler(request, response) {
  if (handleOptions(request, response)) return;

  if (request.method !== "POST") {
    sendJson(response, 405, { ok: false, message: "POST a signed Nostr event." });
    return;
  }

  try {
    const body = await readJsonBody(request);
    const event = assertSignedContributionEvent(body.event);
    const relayUrls = Array.isArray(body.relays) && body.relays.length ? body.relays : relaysFromEnv();
    const result = await publishToRelays(event, relayUrls);

    sendJson(response, result.ok ? 200 : 502, {
      ok: result.ok,
      eventId: event.id,
      relays: result.relays,
      status: result.ok ? "published_to_nostr" : "relay_publish_failed",
    });
  } catch (error) {
    sendJson(response, 400, {
      ok: false,
      message: error.message || String(error),
    });
  }
}
