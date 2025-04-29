# predictor.py

import joblib
import os

# Determine the directory of this script
_BASE_DIR = os.path.dirname(__file__)
# Load the price predictor model from models subdirectory
_price_model = joblib.load(os.path.join(_BASE_DIR, "models", "price_predictor.pkl"))
# (win classifier not loaded yet)

def predict_final_price(current_price, num_bids, time_left_sec):
    features = [[current_price, num_bids, time_left_sec]]
    return _price_model.predict(features)[0]

def predict_win_probability(current_price, num_bids, time_left_sec):
    # Placeholder
    return 0.8 # Assume 80% chance until real model trained