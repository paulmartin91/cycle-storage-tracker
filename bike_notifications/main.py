import os
import json
import asyncio
import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from bike_notifications.logger import setup_logging, get_logger, add_exception_handler

setup_logging()
logger = get_logger(__name__)
add_exception_handler(logger)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT")
POSTCODE = os.getenv("POSTCODE")
MAX_ERRORS = int(os.getenv("MAX_ERRORS", 5))

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError("Missing Telegram environment variables in .env")

if not POSTCODE:
    raise RuntimeError("Missing POSTCODE environment variable in .env")

URL = f"https://cyclehoop.my.site.com/RentalsCommunity/resultsmap?postalCode={POSTCODE}"

DATA_FILE = Path("cycle_storages.json")
CHECK_INTERVAL_SECONDS = 60 * 5
CYCLE_STORAGE_CARD_SELECTOR = '[id="inventory-filter-sidebar"]'


def notify_telegram(text: str):
    """Send a Telegram message."""
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10,
    )


def load_previous():
    """Load previously seen cycle storages from JSON file."""
    if DATA_FILE.exists():
        return set(json.loads(DATA_FILE.read_text()))
    return set()


def save_current(storages: set):
    """Save current set of cycle storages to JSON file."""
    DATA_FILE.write_text(json.dumps(sorted(storages), indent=2))


async def extract_cycle_storages(page):
    """Extract cycle storage entries from the page."""
    await page.wait_for_timeout(5000)

    cards = await page.locator(CYCLE_STORAGE_CARD_SELECTOR).all()

    storages = set()
    for card in cards:
        text = (await card.inner_text()).strip()
        if text:
            storages.add(text)
    return storages


async def check_once():
    """Check for new cycle storage entries."""
    previous = load_previous()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle")

        current = await extract_cycle_storages(page)

        await browser.close()

    if not previous:
        logger.info("Initial snapshot saved.")
        save_current(current)
        return

    new_items = current - previous

    checked = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if new_items:
        notify_telegram("🚲 New cycle storage added!\n\n" + URL)
        save_current(current)
        logger.info(f"Notified via Telegram! ({checked})")
    else:
        logger.info(f"No new cycle storages. ({checked})")


async def main():
    error_count = 0
    notify_telegram("✅ Bike notification script has started.")
    while True:
        try:
            await check_once()
        except Exception as e:
            logger.error(str(e))
            error_count += 1
            if error_count >= 5:
                logger.critical("Too many errors occurred. Stopping.")
                notify_telegram("⚠️ Bike notification script has stopped due to repeated errors.")
                break
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())