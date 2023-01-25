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
import os

from auction import process_sell, process_bid, close_auction

# TODO: test / throw error if line is NOT pipedelimieted
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


def load_input(arguments: list):

    if len(arguments) > 1:
        raise IndexError("Please specify only 1 argument")
    else:
        path_argument = arguments[0]
        if os.path.isfile(path_argument):
            file_name = os.path.basename(path_argument)
            _, extension = file_name.split('.')
            if extension == 'txt':
                with open(path_argument, 'r') as reader:
                    for line in reader:
                        process_input(line.strip())
            else:
                raise TypeError("Input must be a .txt file")
        else:
            raise FileNotFoundError("Could not find file")
