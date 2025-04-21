import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from config import *

def snipe_bid(item_url: str, max_bid: float, offset: int = 5):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()
        stealth_sync(page)
        
        print(f"🔗 Navigating to item: {item_url}")
        page.goto(item_url)
        page.wait_for_selector(".timeLeftVal", timeout=10000)
        time_text = page.text_content(".timeLeftVal")  # e.g., '3h 5m 20s left'

        # Simple parser (assumes 'Xh Ym Zs left')
        hours = minutes = seconds = 0
        if 'h' in time_text: hours = int(time_text.split('h')[0])
        if 'm' in time_text: minutes = int(time_text.split('m')[0].split()[-1])
        if 's' in time_text: seconds = int(time_text.split('s')[0].split()[-1])
        total_sec = hours * 3600 + minutes * 60 + seconds

        wait_time = total_sec - offset
        print(f"⏳ Waiting {wait_time} seconds to bid...")
        time.sleep(wait_time)

        # Place bid
        page.fill("#MaxBidId", str(max_bid))
        page.click("#bidBtn_btn")
        page.wait_for_selector("a[id*='reviewBidSec_btn']", timeout=5000)
        page.click("a[id*='reviewBidSec_btn']")
        print("✅ Bid placed!")
        time.sleep(3)
        browser.close()