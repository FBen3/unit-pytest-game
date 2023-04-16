#!/usr/bin/env python3
import sys

from auction import Auction


if __name__ == "__main__":
    path = sys.argv[1:]

    auction = Auction(path)
    auction.start()
    auction.close()

    print("\nUnitPytestGame")
