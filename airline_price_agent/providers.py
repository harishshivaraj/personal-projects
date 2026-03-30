from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class RouteRequest:
    origin: str
    destination: str
    departure_date: str


class BasePriceProvider:
    name: str = "base"

    def fetch_price(self, request: RouteRequest) -> float:
        raise NotImplementedError


class MockPriceProvider(BasePriceProvider):
    """
    Deterministic pseudo-random price generator for local testing.
    The same route/date combination yields a stable baseline with slight variation.
    """

    name = "mock"

    def fetch_price(self, request: RouteRequest) -> float:
        key = f"{request.origin}-{request.destination}-{request.departure_date}".encode("utf-8")
        digest = hashlib.sha256(key).hexdigest()
        bucket = int(digest[:6], 16)
        base = 120 + (bucket % 700)
        variation = (int(digest[6:8], 16) % 20) - 10
        return float(max(50, base + variation))


def provider_from_config(cfg: dict) -> BasePriceProvider:
    name = cfg.get("name", "mock").lower()
    if name == "mock":
        return MockPriceProvider()
    raise ValueError(
        f"Unsupported provider '{name}'. Add a real API provider implementation in providers.py."
    )
