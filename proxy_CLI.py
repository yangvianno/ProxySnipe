# proxy_CLI.py

import argparse
from utils.login_helper import perform_login
from bid_proxy import snipe_proxy

def main():
    parser = argparse.ArgumentParser(description = "ProxySnipeAI CLI")
    parser.add_argument("--login", action = "store_true", help = "Login to eBay")
    parser.add_argument("--item", type = str, help = "eBay item URL")
    parser.add_argument("--max_bid", type = float, help = "Maximum bid amount")
    parser.add_argument("--offset", type = int, default = 5, help = "Minutes before endto place bid")

    args = parser.parse_args()

    if args.login:
        perform_login()
    elif args.item and args.max_bid:
        snipe_proxy(args.item, args.max_bid, args.offset)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()