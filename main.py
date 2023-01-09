#!/usr/bin/env python3
import sys

auction_records = {}
closing_records = {}


def calculate_winning_stats():

    stats = []

    if len(item_record['bids']) == 1:
        winner =




    return


def calculate_stats(item: str):

    item_record = auction_records[item]
    winning_stats = calculate_winning_stats()

    final_item_stats = [
        item_record['auction_end_time'],
        item,
        winner,
        sold_status,
        price_to_pay,
        total_bids,
        highest_bid,
        lowest_bid
    ]

    print(final_item_stats, sep='|')


def close_auction(time: int):
    if time in closing_records:
        for item in closing_records[time]:
            calculate_stats(item)


def process_sell(listing: list):
    if listing[3] in auction_records:
        raise KeyError("Item is already being sold!")
    else:
        sell_record = {
            'auction_start_time': int(listing[0]),
            'seller': int(listing[1]),
            'item': listing[3],
            'reserve_price': float(listing[4]),
            'auction_end_time': int(listing[5]),
            'status': "UNSOLD",
            'bids': {}
        }
        auction_records[listing[3]] = sell_record
        closing_records.setdefault(int(listing[5]), [])
        closing_records[int(listing[5])].append(listing[3])

    # print(auction_records)
    # print(closing_records)

def process_bid(bidding: list):
    item = bidding[3]
    item_start_time = int(auction_records[item]['auction_start_time'])
    item_close_time = int(auction_records[item]['auction_end_time'])
    bid_time = int(bidding[0])
    bidding_user = int(bidding[1])
    bid_amount = float(bidding[4])

    if item_start_time < bid_time < item_close_time:
        # check if the user has bid before
        if bidding_user in auction_records[item]['bids']:
            # check that bid is larger than any previous bids
            if bid_amount > auction_records[item]['bids'][bidding_user][-1]:
                auction_records[item]['bids'][bidding_user].append(bid_amount)
        else:
            auction_records[item]['bids'].setdefault(bidding_user, [])
            auction_records[item]['bids'][bidding_user].append(bid_amount)


def process_input(line: str):
    split_line = line.split('|')
    # print(split_line)

    # do not process heartbeat messages
    if len(split_line) > 1:
        if split_line[2] == "SELL":
            process_sell(split_line)
        elif split_line[2] == "BID":
            process_bid(split_line)
        else:
            raise ValueError("Could not find input action.")

    # check for any expiring items
    close_auction(int(line[0]))


def load_input(auction_file: list):
    try:
        with open(auction_file[0], 'r') as reader:
            for line in reader:
                # print(line.strip())
                process_input(line.strip())
                print(auction_records)

    except (FileNotFoundError, IndexError) as e:
        print(e)
        print("Please enter a valid path.")
    except:
        print("Unexpected error occurred")
        raise


if __name__ == '__main__':
    path = sys.argv[1:]
    load_input(path)

    print("\nUnitPytestGame")
