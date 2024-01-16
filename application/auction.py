import os

import psycopg2

from application.db_procedures import *
from application.config import db_conn_params


class Auction:


    def __init__(self, input_path, save_option):
        initialize_tables(save_option)
        self.start(input_path)

    def process_input(self, line: str):
        split_line = line.split("|")

        # do not process heartbeat messages
        if len(split_line) > 1:
            if split_line[2] == "SELL":
                # exclude 'SELL' string
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

    def report(self):
        pass

    def close(self):
        pass


# if __name__ == "__main__":
#     auction = Auction('../my_test.txt', True)


