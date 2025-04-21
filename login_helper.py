from playwright.sync.api import sync_playwright
from playwright_stealth import stealth_sync
from config import *

def perform_login():
	with sync_playwright() as pw:
		browser = pw.chromium.launch(headless=False)
		context = browser.new_context()
		page = browser.new_page()
		stealth_sync(page)

		page.goto(LOGIN_URL)
		page.fill("input[name = 'userid']")
		page.click("button#signin-continue-btn")
		page.wait_for_selector("input[name='pass']", timeput=10000)
		page.fill("input[name='pass']", EBAY_PASSWORD)
		page.click("button#sgnBt")
		page.wait_for_load_state("networkidle")

		context.storage_state(path=STATE_FILE)
		print("✅ Login successful. Session saved.")
		browser.close()
