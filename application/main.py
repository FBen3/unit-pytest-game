#!/usr/bin/env python3
# import sys
#
# from process_input import load_input

from application.auction_cls import Auction

if __name__ == "__main__":
    # path = sys.argv[1:]
    # load_input(path)




    auction = Auction()
    auction.start()
    auction.closing_results()



    print("\nUnitPytestGame")
