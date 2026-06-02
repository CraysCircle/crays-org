import {
  CONTRIBUTION_KINDS,
  handleOptions,
  moderatorPubkeysFromEnv,
  relaysFromEnv,
  sendJson,
} from "../../lib/nostr-server.mjs";

export default async function handler(request, response) {
  if (handleOptions(request, response)) return;

  sendJson(response, 200, {
    relays: relaysFromEnv(),
    contributionKinds: CONTRIBUTION_KINDS,
    moderatorPubkeys: moderatorPubkeysFromEnv(),
    moderationEnabled: moderatorPubkeysFromEnv().length > 0,
    identity: {
      signer: "NIP-07 window.nostr",
      privateKeyPolicy: "never ask, never store, never send",
    },
  });
}
