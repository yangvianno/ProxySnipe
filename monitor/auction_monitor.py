# auction_monitor.py

# Auction Monitor Loop
#   Periodically checks:
# 		Current bid price
# 		Number of bids
# 		Time left (e.g., check every 30 seconds)

# Continuously scrapes the current price, numbers of bids, and time left
# Stops when your're priced out or when it's time to snipe

import time
import re
from playwright.sync_api import Page
from utils.time_parser import parse_time_left

def monitor_auction(page: Page, max_bid: float, offset: int = 5, poll_interval: int = 30):
    """
    Loop until auction ends or price exceeds max_bid.
    Yields snapshots *before* bidding logic:
      {
        current_price: float,
        num_bids:      int,
        time_left:     int,   # in seconds
        raw_time:      "1h 2m 3s"
      }
    """
    while True:
        
        # 1. If the page is slow, calling locator(...).inner_text() can throw. 
        # Do a quick page.wait_for_selector() for each before scraping.
        page.wait_for_selector("div[data-testid='x-bid-price'] span.ux-textspans")
        page.wait_for_selector("div[data-testid='x-bid-count']")
        page.wait_for_selector("div[data-testid='x-end-time']")

        # 2. Scrape current price "US $54.00"
        price_text = page.locator("div[data-testid='x-bid-price'] span.ux-textspans").first.inner_text()
        current_price = float(price_text.replace("US", "").replace("$", "").strip())

        # 3. Scrape bid count (e.g., "18 bids")
        bid_text = page.locator("div[data-testid='x-bid-count']").inner_text()
        num_bids = int(bid_text.strip().split()[0])  # Extract only the number

        # 4. Scrape time left (e.g., "Ends in 33m 56s")
        time_text = page.locator("div[data-testid='x-end-time']").inner_text()
        time_left_str = time_text.replace("Ends in", "").strip()
        h, m, s = parse_time_left(time_left_str)
        time_left_sec = h * 3600 + m * 60 + s
        raw_time = f"{h}h {m}m {s}s"

        # 5. Stop condition
        if current_price >= max_bid:
            print(f"🔒 Got out bidded / Priced out: ${current_price} ≥ ${max_bid}")
            break

        if time_left_sec <= offset:
            print(f"⏳ {raw_time} left ≤ offset {offset}s → final window")
            break

        # 6. Yeild for bidding logic
        yield {
            "current_price": current_price,
            "num_bids": num_bids,
            "time_left": time_left_sec,
            "raw_time": f"{h}h {m}m {s}s"
        }

        # 7. Wait to poll again
        time.sleep(poll_interval)

def get_live_auction():
    import random
    mock_auctions = [
        {
            "item_url": "https://www.ebay.com/itm/1234567890",
            "current_price": round(random.uniform(50, 150), 2),
            "num_bids": random.randint(1, 20),
            "time_left_sec": random.randint(100, 600),
        },
        {
            "item_url": "https://www.ebay.com/itm/9876543210",
            "current_price": round(random.uniform(200, 400), 2),
            "num_bids": random.randint(5, 25),
            "time_left_sec": random.randint(200, 800),
        },
    ]
    return mock_auctions