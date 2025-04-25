#data_preprocess.py

import os, pandas as pd, numpy as np
import re

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUT_CSV = os.path.join(PROCESSED_DIR, "auction_logs_preprocessed.csv") # -> 'data/processed/auction_logs_preprocessed.csv'
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Process every .csv in RAW_DIR
for filename in os.listdir(RAW_DIR):
    if not filename.lower().endswith(".csv"):
        continue

    raw_path = os.path.join(RAW_DIR, filename)
    df = pd.read_csv(raw_path)

    # Derive auction length in days from filename (e.g., "5-day") or default (not found number)
    match = re.search(r"(\d+)-day", filename)
    AUCTION_DAY_DEFAULT = 7
    day = int(match.group(1)) if match else AUCTION_DAY_DEFAULT

    # Rename & Compute features
    df = df.rename(columns = {
        "price" : "current_price",
        "bid" : "num_bids",
        "bidtime" : "bidtime_days",
    })
    df["time_left_sec"] = (day - df["bidtime_days"]) * 86400 # 24 * 60 * 60
    MAX_BID = 1000
    df["max_bid"]       = MAX_BID
    
    # Create training-label (a new column ["bid_successful"]) for later ML model by return True → 1, False → 0
    df["bid_successful"] = (
        (df.get("bidder") == 'ProxySniprAI') &
        (df["time_left_sec"] > 0)
    ).astype(int)

    # Keep only model columns 
    df = df[[
        "current_price", "num_bids", "time_left_sec", "max_bid", "bid_successful"
    ]]

    # Write the processedd file
    out_filename = os.path.splitext(filename)[0] + '_preprocessed.csv' # split return tuple "Xbox 3-day auctions" & ".csv" from filename
    output_path = os.path.join(PROCESSED_DIR, out_filename)
    df.to_csv(output_path, index=False) # Tells system to save the out_filename to a CSV file system besides naming it myself
    print(f"✅ Preprocessed {raw_path} -> {output_path}")