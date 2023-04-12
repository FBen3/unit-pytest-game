import os


from item import Item


class Auction:


    def __init__(self, input_file):
        self.input_file = input_file
        self.auction_records = {}
        self.closing_records = {}

    def process_listing(self, listing: Item):
        if listing.item in self.auction_records:
            raise KeyError("Item is already being sold!")
        else:
            self.auction_records[listing.item] = listing
            self.closing_records.setdefault(listing.auction_end_time, [])
            self.closing_records[listing.auction_end_time].append(listing.item)

    def process_bidding(self, bidding: list):
        item = bidding[3]
        item_start_time = self.auction_records[item].auction_start_time
        item_close_time = self.auction_records[item].auction_end_time
        bid_time = int(bidding[0])
        bidding_user = int(bidding[1])
        bid_amount = float(bidding[4])

        if (item_start_time < bid_time < item_close_time) and (bid_amount > 0):
            self.auction_records[item].submit_bid(bidding_user, bid_time, bid_amount)

    def process_input(self, line: str):
        split_line = line.split("|")

        # do not process heartbeat messages
        if len(split_line) > 1:
            if split_line[2] == "SELL":
                # exclude 'SELL' string
                del split_line[2]
                self.process_listing(Item(*split_line))
            elif split_line[2] == "BID":
                self.process_bidding(split_line)
            else:
                raise ValueError("Could not find input action")

    def start(self):
        if len(self.input_file) != 1:
            raise IndexError("Please specify 1 argument")
        else:
            path_argument = self.input_file[0]
            if os.path.isfile(path_argument):
                file_name = os.path.basename(path_argument)
                _, extension = file_name.split(".")
                if extension == "txt":
                    with open(path_argument, "r") as reader:
                        for line in reader:
                            self.process_input(line.strip())
                else:
                    raise TypeError("Input must be a text file")
            else:
                raise FileNotFoundError("Could not find file")

    def close(self, time: int):
        for item in self.closing_records[time]:
            self.calculate_item_stats(item)




