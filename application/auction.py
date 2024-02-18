import os

from application.db_procedures import *


class Auction:
    def __init__(self, save_option: bool):
        initialize_tables(save_option)
        self.auction_clock = 0

    def process_input(self, line: str):
        split_line = line.split("|")
        time = int(split_line[0])

        if time < self.auction_clock:
            raise RuntimeError("Non-chronological input")
        else:
            self.auction_clock = time

        if len(split_line) > 1:  # do not process heartbeat messages
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

    def run(self, input_path: str):
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
        auction_items = all_unexpired_items(self.auction_clock)

        for item in auction_items:
            stats = calculate_final_item_stats(item)
            price_paid = calculate_price_paid_for_item(**stats)
            status = "SOLD" if price_paid > 0 else "UNSOLD"

            if status == "SOLD":
                update_status(item)  # update dabase entry

            result = [
                str(stats["closing_time"]),
                stats["item"],
                str(stats["bidder"]) if price_paid > 0 else "",
                status,
                f"{price_paid:.2f}",
                str(stats["total_bid_count"]),
                f"{stats['highest_bid']:.2f}",
                f"{stats['lowest_bid']:.2f}",
            ]

            output = "|".join(result)
            print(output)
