# dashboard_app.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
import time
from ML.predictor import predict_final_price, predict_win_probability
from config.config_loader import config
from monitor.auction_monitor import get_live_auction

st.set_page_config(page_title = "ProxySnipeAI Dashboard", layout = "wide")
st.title("ProxySnipeAI Dashbaord")
st.caption("Real-time auction tracking with AI-enhanced insights.")

# Live updating section
placeholder = st.empty()
refresh_interval = config['dashboard']['refresh_interval_sec']

while True:
    with placeholder.container():
        st.subheader("Live Auction")

        # --- Get live auctions (mock for now) ---
        # Expected: list of dicts [{"item_url": str, "current_price": float, "num_bids": int, "time_left_sec": int}]
        auctions = get_live_auction()

        if not auctions:
            st.info("No active auctions being monitored.")
        else:
            auction_df = pd.DataFrame(auctions)

            # Predict final price and win probability
            auction_df["Predicted Final Price"] = auction_df.apply(
                lambda row: predict_final_price(row["current_price"], row["num_bids"], row["time_left_sec"]),
                axis = 1
            )

            auction_df["Win Probability"] = auction_df.apply(
                lambda row: predict_win_probability(row["current_price"], row["num_bids"], row["time_left_sec"]),
                axis = 1
            )

            # Decide recommended action
            auction_df["Recommended Action"] = auction_df.apply(
                lambda row: "✅ Bid" if (row["Predicted Final Price"] <= row["current_price"]
                                     and row["Win probability"] >= config['ML']['min_win_probability'])
                                     else "❌ Hold",
                axis = 1
            )

            st.dataframe(auction_df, use_container_width = True)

    time.sleep(refresh_interval)