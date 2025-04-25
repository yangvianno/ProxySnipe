# smart_evaluator.py

import os
import joblib
import numpy as np

# Path to the serialized ML model
MODEL_PATH = os.path.join("models", "snipe_model.pkl")

def load_model():
    """
    Attempt to load a trained model from disk. If the file doesn't exist
    or loading fails, return None.
    """
    # return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

    if os.path.exists(MODEL_PATH): 
        try: 
            return joblib.load(MODEL_PATH) 
        except Exception as e: 
            print(f"⚠️ Failed to load model at {MODEL_PATH}: {e}")
             
    return None

# Load once at import time to avoid repeated disk I/O
_model = load_model()

def should_bid(current_price: float,
               num_bids: int, 
               time_left_sec: int, 
               max_bid: int) -> bool:
    """
    Decide whether to place a bid based on either:
      - A fallback rule if no ML model is available:
          * Only within the last 5 minutes of the auction
          * Only if current price is under 90% of your max bid
      - An ML-based prediction if the model is successfully loaded.

    Args:
        current_price: float  - current highest bid in the auction
        num_bids:      int    - total bids placed so far
        time_left_sec: float  - seconds remaining until auction close
        max_bid:       float  - your maximum bid limit

    Returns:
        bool: True to place a bid now, False otherwise.
    """

    # Fallback rule when model is missing or failed to load
    if _model is None:
        window_ok = (time_left_sec <= 5 * 60)       # Only snipe when <= 5 minutes (300s) remain
        price_ok = (current_price < 0.9 * max_bid)  # Only if current price is under 90%
        return window_ok and price_ok
    
    # ML-based decision: build feature vector and predict
    features = np.array ([[current_price, num_bids, time_left_sec, max_bid]])

    try:
        prediction = _model.predict(features[0]) # Predict returns an array, extract the first element
        return bool(prediction)
    except Exception as e: # If prediction fails at runtime, log and fallback
        print(f"⚠️  Prediction failed: {e}")
        window_ok = (time_left_sec <= 5 * 60)      
        price_ok = (current_price < 0.9 * max_bid) 
        return window_ok and price_ok