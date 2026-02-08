# Bike Notifications

Lightweight monitor that scrapes a CycleHoop results map and sends a Telegram message when new cycle storage entries appear.

## Features
- Periodically loads the target URL with Playwright (headless Chromium)
- Compares discovered storage entries to a persisted snapshot
- Sends a Telegram message for new items
- Comprehensive logging with separate success and error logs

## Requirements
- Python 3.11+
- Playwright
- Telegram bot token and chat id
- Recommended: virtual environment (venv)

## Files of interest
- `main.py` — main monitor loop and scraper
- `logger.py` — logging configuration and setup
- `cycle_storages.json` — persisted snapshot (created at runtime)
- `.env` — environment variables (not checked into VCS)
- `logs/` — log directory (created at runtime)
  - `success.log` — info and debug messages
  - `error.log` — warnings and errors

## Environment
Create a `.env` file in the project root with the following variables:

```env
TELEGRAM_TOKEN=...
TELEGRAM_CHAT=...
POSTCODE=...
```

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

## Logging

Logs are written to the `logs/` directory with the following behavior:

- **success.log** — Contains INFO and DEBUG messages (successful checks, snapshots, notifications sent)
- **error.log** — Contains WARNING and ERROR messages (failed requests, exceptions)
- **Console** — INFO level messages printed to stdout for immediate feedback

Log format: `YYYY-MM-DD HH:MM:SS - LEVEL - message`

### Log Rotation

Log files are automatically rotated when they exceed 5MB. Previous logs are kept as backups (`success.log.1`, `success.log.2`, etc.). Up to 3 backup files are retained per log type.

### Example log entries

success.log:
```
2026-02-08 14:32:10 - INFO - Initial snapshot saved with 12 storages
2026-02-08 14:37:15 - INFO - Telegram notification sent successfully
2026-02-08 14:42:20 - DEBUG - No new cycle storages found at 2026-02-08 14:42:20
```

error.log:
```
2026-02-08 15:10:45 - ERROR - Failed to send Telegram notification: Connection timeout
2026-02-08 15:15:50 - ERROR - Error during check: timeout waiting for page to load
```

## Configuration

- TELEGRAM_TOKEN — Bot token from BotFather
- TELEGRAM_CHAT — Chat ID to send messages to (user or group)
- POSTCODE — Postal code to filter the CycleHoop results map
- CHECK_INTERVAL_SECONDS — Delay between checks (default: 300 seconds / 5 minutes)
- CYCLE_STORAGE_CARD_SELECTOR — CSS selector for storage card elements

## Persistence

The script stores the last-seen items in `cycle_storages.json` in the project root. Remove this file to force a fresh snapshot on next run.

## Troubleshooting

- Playwright browsers missing: run `python -m playwright install`.
- No Telegram messages: verify `.env` values and check `logs/error.log` for API errors. Test manually with:
  ```bash
  curl -s -X POST "https://api.telegram.org/bot<token>/sendMessage" -d chat_id=<chat_id> -d text="test"
  ```
- Selector returns no results: open the target URL in a browser, inspect the storage cards, and update `CYCLE_STORAGE_CARD_SELECTOR` in `main.py`.
- Check `logs/success.log` for detailed runtime activity and `logs/error.log` for failures.

## Docker (brief)

Base image must include Playwright deps. Install Playwright and browsers during build:
- Use official python image + install apt packages required by Playwright
- Run `python -m pip install -r requirements.txt` and `python -m playwright install` in Dockerfile

## Contributing

- Open issues for bugs or feature requests.
- Small, focused PRs are preferred. Include tests where applicable.

## License

MIT