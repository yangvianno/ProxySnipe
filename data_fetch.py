# data_fetch.py

import os
import shutil
import zipfile
import kagglehub

# 1. Download raw dataset
repo = "mehranrezvani/ebay-product-xbox"
download_path = kagglehub.dataset_download(repo)

# 2. Unpack (if it’s a ZIP), move CSVs into your data/ folder
#    adjust paths as needed
raw_dir = os.path.join("data", "raw")
os.makedirs(raw_dir, exist_ok = True)

# 3. Copy CSV(s) or Unpack
if os.path.isdir(download_path):
    for filename in os.listdir(download_path):
        if filename.lower().endswith(".csv"):
            src = os.path.join(download_path, filename) # source
            dst = os.path.join(raw_dir, filename)       # direction
            shutil.copy(src, dst) # mehranrezvani/ebay-product-xbox/Xbox 3-day auctions.csv -> data/raw/Xbox 3-day auctions.csv
    print(f"✅ CSV files copied from {download_path} to {raw_dir}")

else:
    # It’s a .zip file—extract it
    with zipfile.ZipFile(download_path, 'r') as z:
        z.extractall(raw_dir)
    print(f"✅ Raw files unpacked to {raw_dir}")