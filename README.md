# Bike Notifications

Lightweight monitor that scrapes a CycleHoop results map and sends a Telegram message when new cycle storage entries appear.

## Features
- Periodically loads the target URL with Playwright (headless Chromium)
- Compares discovered storage entries to a persisted snapshot
- Sends a Telegram message for new items

## Requirements
- Python 3.11+
- Playwright
- Telegram bot token and chat id
- Recommended: virtual environment (venv)

## Files of interest
- `main.py` — main monitor loop and scraper
- `cycle_storages.json` — persisted snapshot (created at runtime)
- `.env` — environment variables (not checked into VCS)
- `pyproject.toml` — project metadata / dependencies (if using Poetry)

## Environment
Create a `.env` file in the project root with the following variables:

````env
TELEGRAM_TOKEN=...
TELEGRAM_CHAT=...
POSTCODE=...
````

## Installation

Recommended: create and activate a virtual environment.

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
```

If using Poetry:
```bash
poetry install
poetry run python -m playwright install
```

If you don't have a requirements file, install required packages:
```bash
pip install playwright python-dotenv requests
python -m playwright install
```

## Usage

Run the monitor:
```bash
python main.py
```

Or with Poetry:
```bash
poetry run python main.py
```

The script runs indefinitely and checks for new cycle storages every 5 minutes by default. Change `CHECK_INTERVAL_SECONDS` in `main.py` to adjust frequency.

## Configuration

- TELEGRAM_TOKEN — Bot token from BotFather
- TELEGRAM_CHAT — Chat ID to send messages to (user or group)
- POSTCODE — Postal code to filter the CycleHoop results map
- CYCLE_STORAGE_CARD_SELECTOR — Update the CSS selector in `main.py` to match the actual storage card elements if scraping misses items.

## Persistence

The script stores the last-seen items in `cycle_storages.json` in the project root. Remove this file to force a fresh snapshot on next run.

## Troubleshooting

- Playwright browsers missing: run `python -m playwright install`.
- No Telegram messages: verify `.env` values and test with:
  ```bash
  curl -s -X POST "https://api.telegram.org/bot<token>/sendMessage" -d chat_id=<chat_id> -d text="test"
  ```
- Selector returns no results: open the target URL in a browser, inspect the storage cards, and update `CYCLE_STORAGE_CARD_SELECTOR`.

## Contributing

- Open issues for bugs or feature requests.
- Small, focused PRs are preferred. Include tests where applicable.

## License

MIT