import {
  assertSignedContributionEvent,
  handleOptions,
  isModerator,
  moderatorPubkeysFromEnv,
  publishToRelays,
  readJsonBody,
  relaysFromEnv,
  sendJson,
} from "../../lib/nostr-server.mjs";

const MODERATION_KINDS = [4550, 1984, 30078];

export default async function handler(request, response) {
  if (handleOptions(request, response)) return;

  if (request.method !== "POST") {
    sendJson(response, 405, { ok: false, message: "POST a signed moderation event." });
    return;
  }

  try {
    const moderators = moderatorPubkeysFromEnv();
    if (!moderators.length) {
      sendJson(response, 403, {
        ok: false,
        message: "CRAYS_NOSTR_MODERATOR_PUBKEYS is not configured, so server moderation is locked.",
      });
      return;
    }

    const body = await readJsonBody(request);
    const event = assertSignedContributionEvent(body.event, MODERATION_KINDS);

    if (!isModerator(event.pubkey)) {
      sendJson(response, 403, {
        ok: false,
        message: "This pubkey is not allowed to moderate Crays Nostr contributions.",
      });
      return;
    }

    const result = await publishToRelays(event, Array.isArray(body.relays) && body.relays.length ? body.relays : relaysFromEnv());
    sendJson(response, result.ok ? 200 : 502, {
      ok: result.ok,
      eventId: event.id,
      action: body.action || "",
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
