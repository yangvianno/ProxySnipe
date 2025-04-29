# ProxySnipeAI 🎯

AI-Powered eBay Auction Sniper Bot with Stealth Automation

ProxySnipeAI is a production-grade eBay auction sniper, built with Playwright and enhanced with stealth technology to bypass bot detection. It monitors live auctions, predicts winning chances using machine learning, and places incremental smart bids — all while masquerading as a real human browser session.

## ✨ Key Features
- **Cross-browser Automation:** Built on Playwright for reliable, headless or headed operation across Chromium, Firefox, and WebKit.
- **Stealth Mode Integration:** Leverages playwright-stealth to mask navigator flags, plugins, WebGL fingerprints, and CLI headless indicators.
- **ML Decision Making:** Predicts final prices and win probabilities using trained models (RandomForest, XGBoost).
- **Incremental Smart Bidding:** Places $1 increment bids instead of slamming max_bid, mimicking realistic auction behavior.
- **Human-like Timing:** Randomized delays and natural interactions to further avoid detection.
- **Streamlit Dashboard:** Real-time auction tracking, model predictions, live countdown, and bidding history visualization with auto-refresh UI.

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/yangvianno/ProxySnipeAI.git

# Set up your virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
playwright install  # installs browser binaries

# Launch CLI
python proxy_CLI.py --item "...https://www.ebay.com/item/..." --max_bid ... --offset 5
```

## Run the Dashboard

```bash
# Run the dashboard
streamlit run dashboard/dashboard_app.py
```

## 🙌 Built With
- Playwright
- playwright-stealth
- scikit-learn
- Streamlit
- python-dotenv
- joblib

