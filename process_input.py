"""Input processing module.

This module contains the logic to load and read
a pipe-delimited .txt file.

Example formats

    item listing:
    timestamp|user_id|action|item|reserve_price|close_time

    item bid:
    timestamp|user_id|action|item|bid_amount

    heartbeat message:
    timestamp

"""
from auction import process_sell, process_bid, close_auction


def process_input(line: str):
    split_line = line.split('|')

    # do not process heartbeat messages
    if len(split_line) > 1:
        if split_line[2] == "SELL":
            process_sell(split_line)
        elif split_line[2] == "BID":
            process_bid(split_line)
        else:
            raise ValueError("Could not find input action.")

    # check for any expiring items
    close_auction(int(split_line[0]))


def load_input(auction_file: list):
    try:
        with open(auction_file[0], 'r') as reader:
            for line in reader:
                process_input(line.strip())
    except (FileNotFoundError, IndexError) as e:
        print(e)
        print("Please enter a valid path.")
    except:
        print("Unexpected error occurred")
        raise
