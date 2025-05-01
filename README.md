# ProxySnipeAI 🎯

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Automation-brightgreen?logo=microsoft)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange)

AI-Powered eBay Auction Sniper Bot with Stealth Automation

ProxySnipeAI is a production-grade eBay auction sniper, built with Playwright and enhanced with stealth technology to bypass bot detection. It monitors live auctions, predicts winning chances using machine learning, and places incremental smart bids — all while masquerading as a real human browser session.

## ✨ Key Features
- **Cross-browser Automation:** Built on Playwright for reliable, headless or headed operation across Chromium, Firefox, and WebKit.
- **Stealth Mode Integration:** Leverages playwright-stealth to mask navigator flags, plugins, WebGL fingerprints, and CLI headless indicators.
- **ML Decision Making:** Predicts final prices and win probabilities using trained models (RandomForest).
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
```

### 🔐 Login to eBay

```bash
# Run this once to save your login session
python proxy_CLI.py --login
```

### 🎯 Run the Sniper Bot

```bash
python proxy_CLI.py --item "https://www.ebay.com/itm/..." --max_bid 50 --offset 5
```

### 📊 Run the Dashboard

```bash
streamlit run dashboard/dashboard_app.py
```

## 🙌 Built With
- Playwright
- playwright-stealth
- Streamlit
- scikit-learn
- joblib
- python-dotenv