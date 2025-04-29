# login_helper.py

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from config.config import *

def perform_login():
	with sync_playwright() as pw:
		browser = pw.chromium.launch(headless=False)
		context = browser.new_context()
		page = browser.new_page()
		stealth_sync(page)

		page.goto(LOGIN_URL)
		page.fill("input[data-testid='userid']", EBAY_USERNAME)
		page.click("button#signin-continue-btn")
		page.wait_for_selector("input[data-testid='pass']", timeput=10000)
		page.fill("input[data-testid='pass']", EBAY_PASSWORD)
		page.click("button#sgnBt")
		page.wait_for_load_state("networkidle")

		context.storage_state(path=STATE_FILE)
		print("✅ Login successful. Session saved.")
		browser.close()