# Airline Price Agent

A lightweight Python agent that monitors airfare for a specific route/date and sends an email alert when the current price drops below the historical average.

## Features

- Monitors one or many route/date targets from a config file.
- Stores every observation in SQLite.
- Computes a historical average for each route/date pair.
- Sends email alerts when the current price is below a configurable threshold.
- Optional daemon mode for recurring checks.

## Project layout

- `main.py` - CLI entrypoint and monitoring loop.
- `db.py` - SQLite persistence.
- `providers.py` - Price provider abstraction.
- `analytics.py` - Average and threshold logic.
- `notifier.py` - SMTP email sender.
- `config.example.json` - Sample configuration.

## Quick start

1. Create a Python virtual env and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r airline_price_agent/requirements.txt
```

2. Copy and edit config:

```bash
cp airline_price_agent/config.example.json airline_price_agent/config.json
```

3. Run once:

```bash
python airline_price_agent/main.py --config airline_price_agent/config.json --once
```

4. Run continuously (every `check_every_minutes`):

```bash
python airline_price_agent/main.py --config airline_price_agent/config.json
```

## Provider support

The default provider in this starter is `mock`, which generates repeatable synthetic prices for local testing.

To connect a real API:

- implement `BasePriceProvider.fetch_price(...)`
- wire your provider in `provider_from_config(...)`

## Alert behavior

For each target:

- Collect recent observations within `lookback_days`.
- If there are fewer than `min_samples`, skip alerting.
- Compute average.
- Alert if `current_price <= avg * (1 - below_avg_percent / 100)`.

## Scheduling options

- Keep this script running as a daemon (built-in loop).
- Or run with `--once` via cron/GitHub Actions/AWS EventBridge.
