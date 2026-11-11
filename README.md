# plugin-integrator-coinbase

Coinbase Exchange for [Liminal](https://github.com/pcxmac-dev/liminal-charts): the exchange's crypto minute
and day bars from 2015 (its public candles API) and its public trade stream, for the coins open on a
chart. No key. The reference exchange for crypto in the app's composite model. An exchange of its
own: its history is a market apart from the other exchanges', never closed; `CRYPTO_VENUE_DAYS` in
the app limits how far back it is asked.

A Liminal provider plugin released on its own. The app finds it through the entry point group
`liminal.providers` and lists it on the Plugins view and in `liminal-charts plugins`
as `package: plugin-integrator-coinbase`, with this package's version.

## Its API

It attaches to two of Coinbase Exchange's interfaces, both public and keyless for what it asks; its page in every app
shows them (`PLUGIN.apis`), with every part of each, the calls it makes among the rest, and what its client and its
stream learned (`PLUGIN.api_facts()`):

- **The REST API** ([documentation](https://docs.cdp.coinbase.com/exchange/introduction/welcome),
  [reference](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/introduction)): the
  [candles](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles)
  (`GET /products/{product_id}/candles`, 300 a request) for the minute and day bars. Public endpoints allow 10 requests
  a second per IP ([rate limits](https://docs.cdp.coinbase.com/exchange/rest-api/rate-limits)); it keeps 8.
- **The WebSocket feed** ([overview](https://docs.cdp.coinbase.com/exchange/websocket-feed/overview),
  [channels](https://docs.cdp.coinbase.com/exchange/websocket-feed/channels)): the `matches` and `heartbeat` channels
  for the coins open on a chart.
- Using either binds one to Coinbase's [Market Data Terms of Use](https://www.coinbase.com/legal/market_data);
  [status](https://status.exchange.coinbase.com).

## Install

Into the app's environment, from the app's folder:

```powershell
.venv\Scripts\python.exe -m pip install "plugin-integrator-coinbase @ git+https://github.com/pcxmac-dev/plugin-integrator-coinbase@v0.3.0"
```

or with the app's plugins (`pip install -e ".[plugins]"` in liminal-charts). The app loads it on its next
start.

## Compatibility

It is written for plugin API 2.2 (`PLUGIN.api`: the class contract, `CoinbasePlugin` a
`CryptoVenuePlugin` of liminal-libs 1.49.0 or later, declaring what it attaches to, `apis`). An app offering 2.2 or a
later 2.x loads it; an app of another major, or one older than 2.2, leaves it out and says why on the Plugins view.

## Develop

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install "liminal-libs @ git+https://github.com/pcxmac-dev/liminal-libs@main"
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -q
```

Tests never send requests (a fake session answers) and never read your keys.
