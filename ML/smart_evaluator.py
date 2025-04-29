# smart_evaluator.py

from ML.predictor import predict_final_price, predict_win_probability
from config.config_loader import config

def should_bid(current_price: float, num_bids: int, time_left_sec: int, max_bid: float) -> bool:
    """
    Main logic to decide whether to place a bid.

    Strategy:
      - Only bid within 5 minutes of auction end.
      - Predicted final price <= your max bid.
      - Win probability >= threshold.

    Args:
        current_price: Current highest bid
        num_bids: Number of bids placed
        time_left_sec: Seconds left to auction close
        max_bid: Your maximum willingness to pay

    Returns:
        True if bot should place a bid now, False otherwise
    """
    if time_left_sec > 5 * 60: 
        return False
    
    predicted_price = predict_final_price(current_price, num_bids, time_left_sec)
    win_probability = predict_win_probability(current_price, num_bids, time_left_sec)

    if predicted_price <= max_bid and win_probability >= config['ML']['min_win_probability']:
        return True
    
    return False