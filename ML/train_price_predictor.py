# train_price_predictor.py

import pandas as pd
import glob
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

if __name__ == "__main__":
    files = glob.glob("data/processed/*.csv")  # find all .csv files
    df_list = [pd.read_csv(file) for file in files]
    df = pd.concat(df_list, ignore_index=True)

    X = df[["current_price", "num_bids", "time_left_sec"]]
    y = df["max_bid"]

    model = RandomForestRegressor()
    model.fit(X, y)

    # ✅ Save model to correct path AFTER training
    model_dir = "ML/models"
    os.makedirs(model_dir, exist_ok = True)  # Create the directory if missing
    joblib.dump(model, os.path.join(model_dir, "price_predictor.pkl"))