"""Auction Processing module.

This module contains all the logic and processing of an
auction. Including determining a winner if there is one.

"""
from application.process_output import print_stats


auction_records = {}
closing_records = {}


def determine_item_winner(bidders: dict):
    highest_bidder = -1
    highest_bid = (-1.0, -1.0)
    second_highest_bid = (-1.0, -1.0)
    total_bids = 0
    lowest_bid = float("inf")

    for user, bids in bidders.items():
        for bid in bids:
            bid_amount = bid[1]
            bid_time = bid[0]
            if bid_amount > highest_bid[1]:
                second_highest_bid = highest_bid
                highest_bid = bid
                highest_bidder = user
            elif bid_amount == highest_bid[1] and bid_time < highest_bid[0]:
                highest_bidder = user
            elif (
                bid_amount > second_highest_bid[1]
                and bid_amount != highest_bid[1]
            ):
                second_highest_bid = bid
            if bid_amount < lowest_bid:
                lowest_bid = bid_amount
        total_bids += len(bids)

    return {
        "highest_bidder": highest_bidder,
        "highest_bid": highest_bid,
        "second_highest_bid": second_highest_bid,
        "total_bids": total_bids,
        "lowest_bid": lowest_bid,
    }


def collate_item_information(item_information: dict):
    stats = {}

    if len(item_information["bids"]) >= 1:
        winner = determine_item_winner(item_information["bids"])
        stats["sold_status"] = (
            "SOLD"
            if winner["highest_bid"][1] > item_information["reserve_price"]
            else "UNSOLD"
        )
        stats["winner"] = (
            winner["highest_bidder"] if stats["sold_status"] == "SOLD" else ""
        )
        stats["price_to_pay"] = (
            winner["second_highest_bid"][1]
            if stats["sold_status"] == "SOLD"
            else 0.0
        )
        stats["total_bids"] = winner["total_bids"]
        stats["highest_bid"] = winner["highest_bid"][1]
        stats["lowest_bid"] = winner["lowest_bid"]
    else:
        stats["sold_status"] = "UNSOLD"
        stats["winner"] = ""
        stats["price_to_pay"] = 0.0
        stats["total_bids"] = 0
        stats["highest_bid"] = 0.0
        stats["lowest_bid"] = 0.0

    return stats


def calculate_item_stats(item: str):
    item_record = auction_records[item]
    winning_information = collate_item_information(item_record)

    final_item_stats = [
        item_record["auction_end_time"],
        item,
        winning_information["winner"],
        winning_information["sold_status"],
        winning_information["price_to_pay"],
        winning_information["total_bids"],
        winning_information["highest_bid"],
        winning_information["lowest_bid"],
    ]

    print_stats(final_item_stats)


def close_auction(time: int):
    if time in closing_records:
        for item in closing_records[time]:
            calculate_item_stats(item)


def process_sell(listing: list):
    if listing[3] in auction_records:
        raise KeyError("Item is already being sold!")
    else:
        sell_record = {
            "auction_start_time": int(listing[0]),
            "seller": int(listing[1]),
            "item": listing[3],
            "reserve_price": float(listing[4]),
            "auction_end_time": int(listing[5]),
            "status": "UNSOLD",
            "bids": {},
        }
        auction_records[listing[3]] = sell_record
        closing_records.setdefault(int(listing[5]), [])
        closing_records[int(listing[5])].append(listing[3])


def process_bid(bidding: list):
    item = bidding[3]
    item_start_time = int(auction_records[item]["auction_start_time"])
    item_close_time = int(auction_records[item]["auction_end_time"])
    bid_time = int(bidding[0])
    bidding_user = int(bidding[1])
    bid_amount = float(bidding[4])

    if (item_start_time < bid_time < item_close_time) and (bid_amount > 0):
        # check if the user has bid before
        if bidding_user in auction_records[item]["bids"]:
            # check that bid is larger than any previous bids
            if bid_amount > auction_records[item]["bids"][bidding_user][-1][1]:
                auction_records[item]["bids"][bidding_user].append(
                    (bid_time, bid_amount)
                )
        else:
            auction_records[item]["bids"].setdefault(bidding_user, [])
            auction_records[item]["bids"][bidding_user].append(
                (bid_time, bid_amount)
            )
