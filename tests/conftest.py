import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from binance_mcp import runner  # noqa: E402


class FakeSession:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.rate_limits = None

    def data(self):
        return self._payload


class FakeRestAPI:
    def __init__(self, sdk, product, config):
        self._session = FakeSession()
        self._sdk = sdk
        self._product = product
        self.config = config
        self.created_in = threading.get_ident()

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)

        def method(**kwargs):
            return self._sdk.invoke(self, name, kwargs)

        return method


class FakeSDK:
    def __init__(self):
        self.calls = []
        self.rest_apis = []
        self.handler = lambda product, method, kwargs: {"ok": True}
        self.lock = threading.Lock()

    def product_class(self, product):
        sdk = self

        class FakeProduct:
            def __init__(self, config_rest_api=None):
                self.config = config_rest_api
                self._rest = None

            @property
            def rest_api(self):
                if self._rest is None:
                    self._rest = FakeRestAPI(sdk, product, self.config)
                    with sdk.lock:
                        sdk.rest_apis.append(self._rest)
                return self._rest

        return FakeProduct

    def invoke(self, rest, method, kwargs):
        with self.lock:
            self.calls.append((rest._product, method, kwargs))
        result = self.handler(rest._product, method, kwargs)
        return FakeResponse(result)


@pytest.fixture(autouse=True)
def clean_runner(monkeypatch):
    monkeypatch.setattr(runner, "_blocked_until", {})
    monkeypatch.setattr(runner, "_public_clients", {})
    monkeypatch.setattr(runner, "_public_next", {})
    monkeypatch.setattr(runner, "_gate", threading.BoundedSemaphore(4))
    monkeypatch.setattr(runner, "_stats", {"in_flight": 0, "waiting": 0, "busy_rejections": 0, "breaker_blocks": 0})
    monkeypatch.setattr(runner, "GATE_WAIT_SECONDS", 0.1)
    runner.Signers.clear_ed25519_cache()
    runner.Signers.clear_rsa_cache()


@pytest.fixture
def sdk(monkeypatch):
    fake = FakeSDK()
    monkeypatch.setattr(
        runner, "_PRODUCTS",
        {p: (fake.product_class(p), "https://example.invalid") for p in ("spot", "usdm", "coinm")},
    )
    return fake
