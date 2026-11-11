"""What the plugin attaches to (plugin API 2.2): Coinbase Exchange's REST API and its WebSocket feed as Coinbase's pages
describe them, the calls it says it makes being the ones its source and its stream really send, what they learned said
without a request, and (LIMINAL_VENDOR_PAGES=1 only) every page it names still answering. Nothing else is sent; no
ledger or key is touched."""
from __future__ import annotations

import gc
import json
import os
import re
from datetime import datetime, timezone

import pytest

from liminal_libs.config import load_settings
from liminal_libs.sources.apis import dead_links, problems, urls
from liminal_libs.sources.http import PublicClient

import plugin_integrator_coinbase as coinbase
from plugin_integrator_coinbase import BASE_URL, CoinbaseSource, CoinbaseStream
from plugin_integrator_coinbase.apis import FEED, FEED_NAME, REST, REST_NAME
from plugin_integrator_coinbase.facts import NOTES

from .conftest import FakeResponse, FakeSession

CANDLES = re.compile(r"^/products/[A-Z0-9]+-[A-Z0-9]+/candles$")


@pytest.fixture(autouse=True)
def fresh_notes():
    NOTES.clear()
    yield
    NOTES.clear()


def _stream_calls(messages: list[str]) -> set[str]:
    """The card's names of the stream's messages: a subscribe for each channel, an unsubscribe."""
    out = set()
    for m in map(json.loads, messages):
        out |= {f"subscribe: {c}" for c in m["channels"]} if m["type"] == "subscribe" else {m["type"]}
    return out


def test_it_declares_both_apis_soundly_with_every_part_and_what_it_does_with_each():
    apis = coinbase.PLUGIN.apis
    assert apis == (REST, FEED) and problems(apis) == [] and [a.name for a in apis] == [REST_NAME, FEED_NAME]
    assert (REST.base, FEED.base) == (BASE_URL, CoinbaseStream().url)  # the cards' addresses are the client's and the stream's
    assert REST.docs.endswith("/exchange/introduction/welcome") and REST.link("terms").endswith("/legal/market_data")
    assert len(REST.areas) == 18 and [a.name for a in REST.covered] == ["Products", "Requests, pagination and types"]
    assert [a.name for a in FEED.covered] == ["Heartbeat channel", "Matches channel", "Subscribing, sequence numbers and errors"]
    for api in apis:
        assert {c.area for c in api.calls} <= {a.name for a in api.areas} and api.verified == "2026-11-11"
        assert not any(c.writes or c.costs for c in api.used)  # what it makes only reads
    assert {c.name for c in REST.calls if c.costs} == {"POST /orders", "POST /conversions", "POST /withdrawals/crypto"}
    assert {c.name for c in REST.calls if c.writes} >= {"DELETE /orders", "POST /reports"}
    assert "10 requests a second per IP" in REST.limits and "10 subscriptions per product per channel" in FEED.limits
    assert all(u.startswith("https://") for u in urls(apis))


def test_the_calls_it_says_it_makes_are_the_ones_its_source_and_its_stream_send():
    session = FakeSession([FakeResponse(200, [[1767225600, 1.0, 2.0, 1.5, 1.8, 10.0]])])
    src = CoinbaseSource(PublicClient(BASE_URL, session=session, sleep=lambda s: None))
    list(src.bar_pages("BTCUSD", datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 1, 0, 5, tzinfo=timezone.utc),
                       "minute"))
    paths = {url.removeprefix(BASE_URL) for url, _, _ in session.calls}
    assert paths and all(CANDLES.match(p) for p in paths)
    assert {c.name for c in REST.used} == {"GET /products/{product_id}/candles"}
    stream = CoinbaseStream(dynamic=True)
    sent = stream.subscribe(["BTC", "ETH"]) + stream.change({"SOLUSD"}, {"ETHUSD"})
    assert _stream_calls(sent) == {c.name for c in FEED.used} == {"subscribe: matches", "subscribe: heartbeat", "unsubscribe"}


def test_api_facts_say_what_its_client_and_its_stream_learned_and_ask_nothing():
    assert coinbase.PLUGIN.api_facts() == {}  # nothing built or opened here yet: nothing known, nothing asked
    built = coinbase.PLUGIN.build(load_settings(env={}, env_file=None), 5)  # its build notes its client (no request)
    assert coinbase.PLUGIN.api_facts()[REST_NAME]["Requests"] == "0 so far (of 5 allowed)" and built.client.requests_made == 0
    stream = CoinbaseStream(dynamic=True)  # the recorder opens it; it notes itself
    assert coinbase.PLUGIN.api_facts()[FEED_NAME]["Pairs confirmed"] == "none yet"
    stream.parse({"type": "subscriptions", "channels": [{"name": "matches", "product_ids": ["BTC-USD", "ETH-USD"]},
                                                        {"name": "heartbeat", "product_ids": ["BTC-USD", "ETH-USD"]}]})
    said = coinbase.PLUGIN.api_facts()[FEED_NAME]
    assert said["Pairs confirmed"] == "BTCUSD, ETHUSD" and said["Stream opened"].endswith("(open)")
    del built, stream
    gc.collect()
    after = coinbase.PLUGIN.api_facts()
    assert after[REST_NAME]["Run began"].endswith("(ended)") and after[FEED_NAME]["Stream opened"].endswith("(closed)")
    assert after[FEED_NAME]["Pairs confirmed"] == "BTCUSD, ETHUSD"


@pytest.mark.skipif(os.environ.get("LIMINAL_VENDOR_PAGES") != "1", reason="asks Coinbase's pages: set LIMINAL_VENDOR_PAGES=1")
def test_every_page_it_names_answers():
    assert dead_links(coinbase.PLUGIN.apis) == []
