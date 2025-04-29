# auction_monitor.py

# Auction Monitor Loop
#   Periodically checks:
# 		Current bid price
# 		Number of bids
# 		Time left (e.g., check every 10 seconds)

# Continuously scrapes the current price, numbers of bids, and time left
# Stops when your're priced out or when it's time to snipe

import time
import re
from playwright.sync_api import Page
from utils.time_parser import parse_time_left
from ML.smart_evaluator import should_bid

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
        d, h, m, s, time_left_sec = parse_time_left(time_left_str)
        raw_time = f"{d}d {h}h {m}m {s}s"

        # 5. Save live snapshot for dashboard (writes data to monitor/live_status.json)
        import json
        try:
            with open("monitor/live_status.json", "r") as f:
                old = json.load(f)
                price__history = old.get("price_history", []) + [current_price] # get the existing history (or use an empty list if it doesn't exist)
        except:
            price__history = [current_price]

        decision = "✅ Bid" if should_bid(current_price, num_bids, time_left_sec, max_bid) else "🕓 Hold"
        
        snapshot = {
            "item_title": page.title(),
            "current_price": current_price,
            "num_bids": num_bids,
            "time_left": time_left_sec,
            "raw_time": raw_time,
            "decision": decision,
            "price_history": price__history,
        }
        # Write snapshot -> JSON cache
        with open("monitor/live_status.json", "w") as f: 
            json.dump(snapshot, f, indent=2)

        # 6. Exit condition
        if current_price >= max_bid:
            print(f"🔒 Got out bidded / Priced out: ${current_price} ≥ ${max_bid}")
            break

        if time_left_sec <= offset * 60:
            print(f"⏳ {raw_time} left ≤ offset {offset}s → final window")
            break

        # 7. Wait to poll again
        time.sleep(poll_interval)