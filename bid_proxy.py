# bid_proxy.py

from playwright.sync_api import sync_playwright
from monitor.auction_monitor import monitor_auction
from smart_evaluator import should_bid
from utils.logger import get_logger
import time

logger = get_logger()

def snipe_proxy(item_url, max_bid, offset_minutes=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False) # Later stealth mode, proxies,...
        page = browser.new_page()

        logger.info(f"🌎 Navigating to {item_url}")
        page.goto(item_url)

        # Start monitoring auction
        for each_auction_snapshot in monitor_auction(page, max_bid, offset_minutes):
            current_price = each_auction_snapshot["current_price"]
            num_bids = each_auction_snapshot["num_bids"]
            time_left_sec = each_auction_snapshot["time_left"]

            logger.info(f"Snapshot: Price = ${current_price}, Bids = {num_bids}, Time Left = {time_left_sec}s")

            if should_bid(current_price, num_bids, time_left_sec, max_bid):
                logger.info("✅ ML decided to place a bid!")
                place_bid(page, max_bid, poll_interval=5)
                break
            else:
                logger.info(f"⏳ Awaiting for better moment...")

        logger.info("🎯 Auction monitoring complete. Closing broswer.")
        browser.close()

def place_bid(page, max_bid, poll_interval=5):
    """
    Places incremental bids (current_price + $1) until win, time runs out, or max_bid reached.
    """
    try:
        while True:
            # Find the current price
            page.wait_for_selector("div[data-testid='x-bid-price'] span.ux-textspans", timeout=5000)
            price_text = page.locator("div[data-testid='x-bid-price'] span.ux-textspans").first.inner_text()
            current_price = float(price_text.replace("US", "").replace("$", "").strip())

            bid_amount = current_price + 1
            if bid_amount > max_bid:
                logger.warning(f"🚫 Bid amount ${bid_amount} exceeds max bid ${max_bid}. Stopping.")
                break
            
            # Fill the bid_amount
            logger.info(f"💬 Attempting to place bid of ${bid_amount}...")
            page.wait_for_selector('input.textbox__control', timeout=5000)
            bid_input = page.locator('input.textbox__control')
            bid_input.fill(str(bid_amount))

            # Click the Submit bid button
            page.wait_for_selector('div.place-bid-actions__submit', timeout=5000)
            page.locator('div.place-bid-actions__submit').click()
            logger.info(f"✅ Bid of ${bid_amount} submitted. Waiting {poll_interval}s to check if winning/timeout...")
            time.sleep(poll_interval)

            try:
                outbid_banner = page.locator("text=/outbid/i", timeout=6000)
                if outbid_banner.is_visible():
                    logger.warning("⚠️ Outbid detected. Retrying with new bid...")
                    continue
            except Exception as e:
                logger.info("🎯 No outbid detected, possibly winning.")
                break

    except Exception as e:
        logger.error(f"⚠️ Error during incremental bidding: {e}")