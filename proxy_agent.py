import argparse
from login_helper import perform_login
from bid_snipe import snipe_bid

def main():
    parser = argparse.ArgumentParser(description="eBay Auction Sniper Bot")
    parser.add_argument("--login", action="store_true", help="Run login and save session")
    parser.add_argument("--item", type=str, help="eBay item URL")
    parser.add_argument("--max_bid", type=float, help="Maximum bid amount")
    parser.add_argument("--offset", type=int, default=5, help="Seconds before end to place bid")

    args = parser.parse_args()

    if args.login:
        perform_login()
    elif args.item and args.max_bid:
        snipe_bid(args.item, args.max_bid, args.offset)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()