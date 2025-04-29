# dashboard_app.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit
import pandas as pd
import json
import time
from datetime import timedelta
from config.config_loader import config

streamlit.set_page_config(page_title = "ProxySnipeAI Dashboard", layout = "wide")
streamlit.title("🎯 ProxySnipeAI Auction Monitor")
streamlit.caption("Real-time auction tracking with AI-enhanced insights.")

# Live updating section
placeholder = streamlit.empty()
refresh_interval = config['dashboard']['refresh_interval_sec'] # Auto refresh every 10 seconds

LIVE_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'monitor', 'live_status.json')

while True:
    with placeholder.container():
        streamlit.subheader("Live Auction(s)")

        if os.path.exists(LIVE_DATA_PATH):
            with open(LIVE_DATA_PATH, "r") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = [data] # Wrap single entry as list

            for item in data:
                with streamlit.expander(f"🛒 {item.get('item_title', 'Unknown')}"):
                    col1, col2, col3 = streamlit.columns(3)
                    col1.metric("💲 Current Price", f"${item.get('current_price', 'N/A')}")
                    col2.metric("🧮 Bids", f"${item.get('num_bids', 'N/A')}")
                    col3.metric("⏳ Time Left", str(timedelta(seconds=int(item.get('time_left')))))

                    decision = item.get('decision', 'Unknown')
                    if decision == "Bid":
                        streamlit.success("✅ Will Bid")
                    else:
                        streamlit.info("🕓 Holding")

                    if "price_history" in item:
                        streamlit.markdown("### 📈 Price Evolution")
                        streamlit.line_chart(item["price_history"])

            streamlit.warning("⚠️ No live auction data found. Start the sniping bot.")

    # 💡 Auto-refresh after showing everything
    time.sleep(refresh_interval)