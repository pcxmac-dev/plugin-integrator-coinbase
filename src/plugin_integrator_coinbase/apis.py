"""What the plugin attaches to (plugin API 2.2, liminal_libs.sources.apis): Coinbase Exchange's REST API, for its
candles, and its WebSocket feed, for the live trades. Every address below was read on Coinbase's own pages on
2026-11-11 (the Coinbase Developer Platform's Exchange docs, each page read as Markdown, its sitemap for the reference's
sixteen groups; the status page by its title). Nothing is asked to show it."""
from __future__ import annotations

from liminal_libs.sources.apis import Api, Area, Call, Link

VERIFIED = "2026-11-11"
REST_NAME = "Coinbase Exchange REST API"
FEED_NAME = "Coinbase Exchange WebSocket feed"
DOCS = "https://docs.cdp.coinbase.com"
EXCHANGE = f"{DOCS}/exchange"
REF = f"{DOCS}/api-reference/exchange-api/rest-api"
TERMS = Link("Market Data Terms of Use", "https://www.coinbase.com/legal/market_data", "terms")
STATUS = Link("Coinbase Exchange status", "https://status.exchange.coinbase.com", "status")

PRODUCTS = "Products"
CURRENCIES = "Currencies"
ACCOUNTS = "Accounts"
ADDRESS_BOOK = "Address book"
WALLETS = "Coinbase accounts"
CONVERSIONS = "Conversions"
FEES = "Fees"
FUTURES = "Futures"
LOANS = "Loans"
ORDERS = "Orders and fills"
PROFILES = "Profiles"
REPORTS = "Reports"
TRANSFERS = "Transfers"
TRAVEL = "Travel rules"
USERS = "Users"
WRAPPED = "Wrapped assets"
REQUESTS = "Requests, pagination and types"
FIX = "FIX API"

REST = Api(
    name=REST_NAME,
    maker="Coinbase (Coinbase Exchange, on the Coinbase Developer Platform)",
    about=("Coinbase Exchange's REST API: its market data in public (products, their candles, books, tickers, trades "
           "and stats, the currencies) and, with a signed key, an institution's accounts, orders, transfers, loans and "
           "reports. JSON over HTTPS; the market data needs no key."),
    kind="rest",
    base="https://api.exchange.coinbase.com",
    version="the Exchange REST API (its reference's version 1.0)",
    auth=("none for the public market data; the private endpoints sign every request with an API key (CB-ACCESS-KEY, "
          "-SIGN, -TIMESTAMP and -PASSPHRASE headers)"),
    limits=("public endpoints 10 requests a second per IP (bursts to 15), private 15 per profile (bursts to 30), /fills "
            "10 (bursts to 20), /loans 10; a lazy-fill token bucket, a 429 past it (kept at 8 a second here). A "
            "candles request answers 300 candles at most. Using its market data binds one to Coinbase's Market Data "
            "Terms of Use"),
    costs=("the market data costs nothing; orders and conversions carry trading fees, withdrawals network fees, loans "
           "interest (none of it asked here)"),
    links=(
        Link("Exchange API documentation", f"{EXCHANGE}/introduction/welcome", "docs"),
        Link("REST API reference", f"{REF}/introduction", "reference"),
        Link("REST quickstart", f"{EXCHANGE}/introduction/rest-quickstart", "guide"),
        Link("Authentication", f"{EXCHANGE}/rest-api/authentication", "auth"),
        Link("REST rate limits", f"{EXCHANGE}/rest-api/rate-limits", "limits"),
        STATUS,
        Link("Changelog", f"{EXCHANGE}/changes/changelog", "changelog"),
        Link("Upcoming changes", f"{EXCHANGE}/changes/upcoming-changes", "changelog"),
        Link("Sandbox", f"{EXCHANGE}/introduction/sandbox", "guide"),
        Link("SDKs", f"{EXCHANGE}/rest-api/sdks", "sdk"),
        Link("API keys (the Exchange profile)", "https://exchange.coinbase.com/profile/api", "console"),
        TERMS,
        Link("Index for AI tools (llms.txt)", f"{DOCS}/llms.txt", "docs"),
    ),
    areas=(
        Area(PRODUCTS, "the trading pairs, each one's candles, book, ticker, trades and 24-hour stats, all products' "
                       "volume (public)", f"{REF}/products/get-product-candles",
             covered="candles: minute and day bars, 300 a request, newest first"),
        Area(CURRENCIES, "the known currencies and each one's details (public)", f"{REF}/currencies/get-all-known-currencies"),
        Area(ACCOUNTS, "a profile's accounts, their holds, ledgers and transfers", f"{REF}/accounts/get-all-account-profile"),
        Area(ADDRESS_BOOK, "the saved withdrawal addresses", f"{REF}/address-book/get-address-book"),
        Area(WALLETS, "the linked Coinbase wallets and their crypto addresses", f"{REF}/coinbase-accounts/get-all-coinbase-wallets"),
        Area(CONVERSIONS, "conversions between currencies (USD and USDC) and their fee rates", f"{REF}/conversions/convert-currency"),
        Area(FEES, "the profile's maker and taker fee rates", f"{REF}/fees/get-fee"),
        Area(FUTURES, "auto-loan and USDC conversion settings for margin", f"{REF}/futures/get-usdc-conversion"),
        Area(LOANS, "loans: options, previews, opening, repaying, interest", f"{REF}/loan/list-loans"),
        Area(ORDERS, "placing, listing and cancelling orders; the fills", f"{REF}/orders/create-new-order"),
        Area(PROFILES, "the account's profiles: making, renaming, moving funds between them", f"{REF}/profiles/get-profiles"),
        Area(REPORTS, "account and fills reports, made and fetched", f"{REF}/reports/create-report"),
        Area(TRANSFERS, "deposits and withdrawals (payment methods, Coinbase accounts, crypto addresses) and their fees",
             f"{REF}/transfers/get-all-transfers"),
        Area(TRAVEL, "the travel rule's information for transfers", f"{REF}/travel-rules/get-all-travel-rule"),
        Area(USERS, "a user's exchange limits, trading volume, settlement preference", f"{REF}/users/get-user-exchange-limits"),
        Area(WRAPPED, "wrapped assets: their details, rates, stake-wraps and redeems", f"{REF}/wrapped-assets/get-all-wrapped-assets"),
        Area(REQUESTS, "requests and status codes, pagination, the API's types", f"{EXCHANGE}/rest-api/requests",
             covered="its answers' status codes read by the library's client (a 429 waits; nothing paged here)"),
        Area(FIX, "the FIX 5.0 order entry, market data and drop copy sessions (keyed)", f"{EXCHANGE}/fix-api/connectivity"),
    ),
    calls=(
        Call("GET /products/{product_id}/candles", "a product's candles: time, low, high, open, close, volume; "
             "granularity 60, 300, 900, 3600, 21600 or 86400 seconds, 300 at most", PRODUCTS,
             used="minute and day bars (and 5 and 15 minutes, 1 and 6 hours), 300 a request",
             docs=f"{REF}/products/get-product-candles"),
        Call("GET /products", "every trading pair", PRODUCTS, docs=f"{REF}/products/get-all-known-trading-pairs"),
        Call("GET /products/{product_id}", "a trading pair", PRODUCTS, docs=f"{REF}/products/get-single-product"),
        Call("GET /products/{product_id}/book", "a product's order book", PRODUCTS, docs=f"{REF}/products/get-product-book"),
        Call("GET /products/{product_id}/ticker", "a product's last trade, best bid and ask, 24-hour volume", PRODUCTS,
             docs=f"{REF}/products/get-product-ticker"),
        Call("GET /products/{product_id}/trades", "a product's latest trades", PRODUCTS, docs=f"{REF}/products/get-product-trades"),
        Call("GET /products/{product_id}/stats", "a product's 24-hour and 30-day stats", PRODUCTS,
             docs=f"{REF}/products/get-product-stats"),
        Call("GET /products/volume-summary", "every product's 24-hour and 30-day volume", PRODUCTS,
             docs=f"{REF}/products/get-all-product-volume"),
        Call("GET /currencies", "every known currency", CURRENCIES, docs=f"{REF}/currencies/get-all-known-currencies"),
        Call("GET /currencies/{currency_id}", "a currency", CURRENCIES, docs=f"{REF}/currencies/get-a-currency"),
        Call("GET /time", "the API server's time", REQUESTS, docs=f"{EXCHANGE}/rest-api/authentication"),
        Call("GET /accounts", "a profile's accounts", ACCOUNTS, docs=f"{REF}/accounts/get-all-account-profile"),
        Call("GET /accounts/{account_id}/ledger", "an account's ledger", ACCOUNTS, docs=f"{REF}/accounts/get-single-account-ledger"),
        Call("GET /address-book", "the saved addresses", ADDRESS_BOOK, docs=f"{REF}/address-book/get-address-book"),
        Call("GET /coinbase-accounts", "the linked Coinbase wallets", WALLETS, docs=f"{REF}/coinbase-accounts/get-all-coinbase-wallets"),
        Call("POST /conversions", "converts one currency into another", CONVERSIONS, docs=f"{REF}/conversions/convert-currency",
             writes=True, costs=True),
        Call("GET /fees", "the profile's fee rates", FEES, docs=f"{REF}/fees/get-fee"),
        Call("GET /margin/usdc", "the USDC conversion setting", FUTURES, docs=f"{REF}/futures/get-usdc-conversion"),
        Call("GET /loans", "the profile's loans", LOANS, docs=f"{REF}/loan/list-loans"),
        Call("POST /orders", "places an order", ORDERS, docs=f"{REF}/orders/create-new-order", writes=True, costs=True),
        Call("GET /orders", "the open (or past) orders", ORDERS, docs=f"{REF}/orders/get-all-orders"),
        Call("DELETE /orders", "cancels every open order", ORDERS, docs=f"{REF}/orders/cancel-all-orders", writes=True),
        Call("GET /fills", "the fills of the profile's orders", ORDERS, docs=f"{REF}/orders/get-all-fills"),
        Call("GET /profiles", "the account's profiles", PROFILES, docs=f"{REF}/profiles/get-profiles"),
        Call("POST /reports", "makes a report", REPORTS, docs=f"{REF}/reports/create-report", writes=True),
        Call("GET /transfers", "the deposits and withdrawals", TRANSFERS, docs=f"{REF}/transfers/get-all-transfers"),
        Call("POST /withdrawals/crypto", "withdraws to a crypto address", TRANSFERS,
             docs=f"{REF}/transfers/withdraw-to-crypto-address", writes=True, costs=True),
        Call("GET /travel-rules", "the travel rule's information", TRAVEL, docs=f"{REF}/travel-rules/get-all-travel-rule"),
        Call("GET /users/{user_id}/exchange-limits", "a user's limits", USERS, docs=f"{REF}/users/get-user-exchange-limits"),
        Call("GET /wrapped-assets", "the wrapped assets", WRAPPED, docs=f"{REF}/wrapped-assets/get-all-wrapped-assets"),
    ),
    verified=VERIFIED,
)

CHANNELS = f"{EXCHANGE}/websocket-feed/channels"
HEARTBEAT = "Heartbeat channel"
STATUS_CH = "Status channel"
AUCTION = "Auction channel"
MATCHES = "Matches channel"
RFQ = "RFQ matches channel"
TICKER = "Ticker and ticker batch channels"
LEVEL2 = "Level2 and level2 batch channels"
FULL = "Full, level3 and user channels (signed)"
BALANCE = "Balance channel (signed)"
DIRECT = "Direct market data (ws-direct, signed)"
PROTOCOL = "Subscribing, sequence numbers and errors"

FEED = Api(
    name=FEED_NAME,
    maker="Coinbase (Coinbase Exchange, on the Coinbase Developer Platform)",
    about=("Coinbase Exchange's real-time market data over a WebSocket: subscribe to channels (heartbeat, status, "
           "matches, ticker, level2 batches; full, level2, level3, user and balance with a signed subscribe) for "
           "products, then read a stream of JSON messages. The market data feed needs no key."),
    kind="stream",
    base="wss://ws-feed.exchange.coinbase.com",
    version="the Exchange WebSocket feed (its channels as documented in 2026)",
    auth=("none for its public channels; full, level2, level3, user and balance (and the ws-direct endpoint) need a "
          "subscribe signed with an API key"),
    limits=("8 connection requests a second per IP (bursts to 20); 100 messages a second sent per IP; 10 subscriptions "
            "per product per channel; inbound messages 10 a second (bursts to 1,000); a subscribe within 5 seconds of "
            "connecting, or it disconnects. Its market data binds one to Coinbase's Market Data Terms of Use"),
    costs="higher subscription limits are sold on the Coinbase Developer Platform; nothing of it is asked here",
    links=(
        Link("WebSocket feed overview", f"{EXCHANGE}/websocket-feed/overview", "docs"),
        Link("Channels", CHANNELS, "reference"),
        Link("WebSocket rate limits", f"{EXCHANGE}/websocket-feed/rate-limits", "limits"),
        Link("Authentication", f"{EXCHANGE}/websocket-feed/authentication", "auth"),
        Link("Best practices", f"{EXCHANGE}/websocket-feed/best-practices", "guide"),
        Link("Errors", f"{EXCHANGE}/websocket-feed/errors", "reference"),
        STATUS,
        TERMS,
    ),
    areas=(
        Area(HEARTBEAT, "a heartbeat a second for each product, with its last trade's sequence", CHANNELS,
             covered="subscribed beside matches, so a quiet pair's connection is known alive"),
        Area(STATUS_CH, "every product and currency at an interval", CHANNELS),
        Area(AUCTION, "the indicative quote while a product is in auction", CHANNELS),
        Area(MATCHES, "every trade (match), the first a last_match", CHANNELS,
             covered="the live trades of the coins open on a chart (BTC-USD ...), one tick a match"),
        Area(RFQ, "the request-for-quote trades, of every product or one", CHANNELS),
        Area(TICKER, "the price at every match, or every five seconds when it changed", CHANNELS),
        Area(LEVEL2, "the order book's changes (level2 signed; level2_batch every 50 ms, public)", CHANNELS),
        Area(FULL, "every order's life (received, open, done, match, change), compact as level3; the user's own", CHANNELS),
        Area(BALANCE, "the account's balance updates", CHANNELS),
        Area(DIRECT, "the direct market data endpoint, wss://ws-direct.exchange.coinbase.com", f"{EXCHANGE}/websocket-feed/overview"),
        Area(PROTOCOL, "subscribe and unsubscribe messages, the subscriptions answer, sequence numbers, error messages",
             f"{EXCHANGE}/websocket-feed/overview",
             covered="subscribe, change and unsubscribe; the subscriptions answer read (the pairs it confirms); an error "
                     "message ends the connection as a refusal"),
    ),
    calls=(
        Call("subscribe: matches", "every trade of the products named", MATCHES,
             used="the live trades of the coins open on a chart", docs=CHANNELS),
        Call("subscribe: heartbeat", "a heartbeat a second for the products named", HEARTBEAT,
             used="beside matches: the connection known alive", docs=CHANNELS),
        Call("unsubscribe", "takes products (or a channel) off the connection", PROTOCOL,
             used="a coin's chart closed: its pair off the stream", docs=f"{EXCHANGE}/websocket-feed/overview"),
        Call("subscribe: status", "every product and currency at an interval", STATUS_CH, docs=CHANNELS),
        Call("subscribe: auction", "a product's auction quotes", AUCTION, docs=CHANNELS),
        Call("subscribe: rfq_matches", "request-for-quote trades", RFQ, docs=CHANNELS),
        Call("subscribe: ticker", "the price at every match", TICKER, docs=CHANNELS),
        Call("subscribe: ticker_batch", "the price every five seconds", TICKER, docs=CHANNELS),
        Call("subscribe: level2_batch", "the book's changes every 50 ms", LEVEL2, docs=CHANNELS),
        Call("subscribe: level2 (signed)", "every change of the book", LEVEL2, docs=CHANNELS),
        Call("subscribe: full (signed)", "every order's life", FULL, docs=CHANNELS),
        Call("subscribe: level3 (signed)", "the full channel, compact", FULL, docs=CHANNELS),
        Call("subscribe: user (signed)", "the user's own orders and trades", FULL, docs=CHANNELS),
        Call("subscribe: balance (signed)", "the account's balances", BALANCE, docs=CHANNELS),
    ),
    verified=VERIFIED,
)

APIS = (REST, FEED)
