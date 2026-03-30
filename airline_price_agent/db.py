from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class PriceObservation:
    origin: str
    destination: str
    departure_date: str
    observed_at: str
    price_usd: float
    provider: str


class PriceRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS price_observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    origin TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    departure_date TEXT NOT NULL,
                    observed_at TEXT NOT NULL,
                    price_usd REAL NOT NULL,
                    provider TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_route_date_observed
                ON price_observations (origin, destination, departure_date, observed_at)
                """
            )

    def add_observation(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        price_usd: float,
        provider: str,
    ) -> None:
        observed_at = datetime.now(tz=timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO price_observations
                    (origin, destination, departure_date, observed_at, price_usd, provider)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (origin.upper(), destination.upper(), departure_date, observed_at, price_usd, provider),
            )

    def get_recent_prices(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        lookback_days: int,
    ) -> List[float]:
        since = datetime.now(tz=timezone.utc) - timedelta(days=lookback_days)
        since_iso = since.isoformat()
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT price_usd
                FROM price_observations
                WHERE origin = ?
                  AND destination = ?
                  AND departure_date = ?
                  AND observed_at >= ?
                ORDER BY observed_at ASC
                """,
                (origin.upper(), destination.upper(), departure_date, since_iso),
            ).fetchall()
        return [float(row[0]) for row in rows]
