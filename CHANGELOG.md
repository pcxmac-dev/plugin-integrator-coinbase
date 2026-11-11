# Changelog

## 0.3.0 (2026-11-11)

Its APIs on its page (plugin API 2.2, liminal-libs 1.49.0; the user: "each plugin should reflect the the API its attached
to, and present links that provide documentation, the plugin interface should more or less contain what it already has,
BUT, it should also expose more of what the API is about"). `CoinbasePlugin.apis` declares the two things it talks to,
read from Coinbase's own pages on 2026-11-11 (`apis.py`):

- **Coinbase Exchange's REST API** (api.exchange.coinbase.com): its documentation, reference, quickstart,
  authentication, rate limits, status page, changelogs, sandbox, SDKs, the API keys page and the Market Data Terms of
  Use; its reference's sixteen groups with the requests and the FIX API (eighteen parts), each said used or not; the
  one call it makes (`GET /products/{product_id}/candles`) among 29 others, the ones that change something or cost
  (orders, conversions, withdrawals) said so;
- **its WebSocket feed** (ws-feed.exchange.coinbase.com): its overview, channels, limits, authentication, best
  practices and errors; its channels in eleven parts; what it sends (`subscribe` to matches and heartbeat,
  `unsubscribe`) beside the other channels' subscriptions.

`api_facts()` says what its client and its stream learned while they ran, asking nothing: the requests made, the last
answer's clock, the rate-limit headers its server sent, the pairs the stream's server confirmed (`facts.py`: each held
weakly, its last words kept when it goes; its build now notes the client it makes, the stream notes itself). Tests: the
contract at 2.2, the cards' calls the ones its source and its stream send, the facts, and every page it names answering
(only with `LIMINAL_VENDOR_PAGES=1`). On liminal-libs 1.49.0 or later; every behaviour, limit and string as in 0.2.0.

## 0.2.0 (2026-11-03)

Renamed `plugin-integrator-coinbase` (the package `plugin_integrator_coinbase`; it was `liminal-plugin-coinbase`) on 2026-11-03: the naming by system (plugins are `plugin-<app>-<name>`), on liminal-libs 1.4.0 (`liminal_libs`, the library renamed with it).

- A class on plugin API 2.0 (liminal-libs 1.3.0; the user: "all the plugins under liminal should basically
  follow inheritance/oop paradigm"): `CoinbasePlugin(CryptoVenuePlugin)`, a crypto exchange's plugin of
  `liminal_libs.sources.archive` (its `assets` and `kind`; its source built on the contract's public client at
  `base_url`; its `view`, the plan and caps with all the history it holds unless `CRYPTO_VENUE_DAYS` limits
  it, once `venue_view`), what the `Provider` record declared as class attributes and its callbacks as
  methods (`rate`, `carries`), `PLUGIN` its instance.
- It declares its publication delay itself (`delays`: each minute once it closes, the row the library held
  for the `coinbase-public` plan).
- Every behaviour, limit and string as in 1.3.1. Versioned 0.2.0 with every Liminal distribution of the
  release (its `release/0.2.0` branch; CI against the library's).

## 1.3.1 (2026-11-02)

The plugin imports the library as `liminal_libs` and depends on liminal-libs (the app, renamed liminal-charts, is no longer needed to run the tests; the user, 2026-11-02: "lets rename the app to liminal-charts").

## 1.3.0 (2026-11-01)

- Released as its own package, `plugin-integrator-coinbase`, registered under the entry point group
  `liminal.providers`; its version is the distribution's.
- Its plan and request caps are in it (`TIER`, `PER_RUN`, `PER_DAY`), no longer in the app's
  `config.PUBLIC_FEEDS`; the app's `CRYPTO_VENUE_DAYS` still limits its history (`venue_view`).
- Plugin API 1.6.

## 1.2.0 (2026-10-31)

- Built into the app (then massive-collate): its source class, client and trade stream in its
  module (plugin API 1.6).

## 1.1.0 and 1.0.0

- Built into the app (then massive-collate); see the app's history.
