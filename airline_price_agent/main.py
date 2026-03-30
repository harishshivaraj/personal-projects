from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

import json

from analytics import evaluate_alert
from db import PriceRepository
from notifier import send_email_alert
from providers import RouteRequest, provider_from_config

LOGGER = logging.getLogger("airline_price_agent")


def load_config(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_cycle(config: dict) -> None:
    app_cfg = config["app"]
    alert_cfg = config["alert"]
    email_cfg = config["email"]

    repo = PriceRepository(app_cfg["db_path"])
    provider = provider_from_config(config["provider"])

    for route in config["routes"]:
        request = RouteRequest(
            origin=route["origin"].upper(),
            destination=route["destination"].upper(),
            departure_date=route["departure_date"],
        )

        current_price = provider.fetch_price(request)
        repo.add_observation(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date,
            price_usd=current_price,
            provider=provider.name,
        )

        history = repo.get_recent_prices(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date,
            lookback_days=int(alert_cfg["lookback_days"]),
        )

        decision = evaluate_alert(
            current_price=current_price,
            historical_prices=history,
            below_avg_percent=float(alert_cfg["below_avg_percent"]),
            min_samples=int(alert_cfg["min_samples"]),
        )

        LOGGER.info(
            "route=%s->%s date=%s current=%.2f reason=%s",
            request.origin,
            request.destination,
            request.departure_date,
            current_price,
            decision.reason,
        )

        if not decision.should_alert:
            continue

        if not email_cfg.get("enabled", False):
            LOGGER.info("Alert triggered but email.enabled=false; no email sent.")
            continue

        subject = (
            f"Flight deal alert: {request.origin}->{request.destination} on {request.departure_date}"
        )
        body = (
            f"Current price: ${current_price:.2f}\n"
            f"Average price: ${decision.average_price:.2f}\n"
            f"Threshold price: ${decision.threshold_price:.2f}\n"
            f"Provider: {provider.name}\n"
        )
        send_email_alert(
            smtp_host=email_cfg["smtp_host"],
            smtp_port=int(email_cfg["smtp_port"]),
            username=email_cfg["smtp_username"],
            password=email_cfg["smtp_password"],
            from_address=email_cfg["from_address"],
            to_address=route["recipient_email"],
            subject=subject,
            body=body,
        )
        LOGGER.info("Email alert sent to %s", route["recipient_email"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor airline prices and send below-average alerts.")
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one polling cycle and exit",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    args = parse_args()
    config = load_config(args.config)

    if args.once:
        run_cycle(config)
        return

    interval_minutes = int(config["app"].get("check_every_minutes", 360))
    interval_seconds = max(60, interval_minutes * 60)
    LOGGER.info("Starting monitor loop with interval=%s minutes", interval_minutes)

    while True:
        run_cycle(config)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
