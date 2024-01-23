import os

from application.db_procedures import *


class Auction:


    def __init__(self, input_path, save_option):
        initialize_tables(save_option)
        self.auction_clock = 0
        self.start(input_path)
        self.report()

    def process_input(self, line: str):
        split_line = line.split("|")
        self.auction_clock = split_line[0]

        if len(split_line) > 1: # do not process heartbeat messages
            if split_line[2] == "SELL":
                del split_line[2]
                try:
                    process_listing(*split_line)
                except Exception as e:
                    print(f"Listing error: {e}")
                    raise e
            elif split_line[2] == "BID":
                del split_line[2]
                try:
                    process_bidding(*split_line)
                except Exception as e:
                    print(f"Bidding error: {e}")
                    raise e
            else:
                raise ValueError("Could not find input action")

    def start(self, input_path):
        if os.path.isfile(input_path):
            file_name = os.path.basename(input_path)
            _, extension = file_name.split(".")
            if extension == "txt":
                with open(input_path, "r") as reader:
                    for line in reader:
                        self.process_input(line.strip())
            else:
                raise TypeError("Input must be a .txt file")
        else:
            raise FileNotFoundError("Could not find input file")

    # 20|toaster_1|8|SOLD|12.50|3|20.00|7.50
    # 20|tv_1||UNSOLD|0.00|2|200.00|150.00


    def report(self):
        pass




