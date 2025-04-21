import os
from dotenv import load_dotenv

load_dotenv()

EBAY_USERNAME = os.getenv('EBAY_USERNAME')
EBAY_PASSWORD = os.getenv('EBAY_PASSWORD')

STATE_FILE = 'ebay_state.json'

LOGIN_URL = 'https://www.ebay.com/signin/'
