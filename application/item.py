from dataclasses import dataclass, field, asdict


@dataclass
class Item:
    auction_start_time: int
    seller: int
    item: str
    reserve_price: float
    auction_end_time: int
    status: str = "UNSOLD"
    bids: dict = field(default_factory=dict)

    def __post_init__(self):
        self.auction_start_time = int(self.auction_start_time)
        self.seller = int(self.seller)
        self.reserve_price = float(self.reserve_price)
        self.auction_end_time = int(self.auction_end_time)

    def largest_bid(self, bidder):
        return self.bids[bidder][-1][1]

    def submit_bid(self, bidder, time, amount):
        if bidder in self.bids:
            if amount > self.largest_bid(bidder):
                self.bids[bidder].append((time, amount))
        else:
            self.bids.setdefault(bidder, [])
            self.bids[bidder].append((time, amount))

        self.status = "SOLD"

    def determine_item_winner(self):
        highest_bidder = -1
        highest_bid = (-1.0, -1.0)
        second_highest_bid = (-1.0, -1.0)
        lowest_bid = float("inf")

        for user, bids in self.bids.items():
            for bid in bids:
                bid_amount = bid[1]
                bid_time = bid[0]
                if bid_amount > highest_bid[1]:
                    second_highest_bid = highest_bid
                    highest_bid = bid
                    highest_bidder = user
                elif bid_amount == highest_bid[1] and bid_time < highest_bid[0]:
                    highest_bidder = user
                elif bid_amount > second_highest_bid[1] and bid_amount != highest_bid[1]:
                    second_highest_bid = bid
                if bid_amount < lowest_bid:
                    lowest_bid = bid_amount

        return [highest_bidder, second_highest_bid[1], highest_bid[1], lowest_bid]

    def calculate_winning_stats(self):
        if len(self.bids) >= 1:
            item_winner, price_paid, highest_bid, lowest_bid = self.determine_item_winner() # fmt: skip

            return [
                self.auction_end_time,
                self.item,
                item_winner,
                self.status,
                price_paid,
                len(self.bids),
                highest_bid,
                lowest_bid
            ]

        # if item received 0 bids
        return [
            self.auction_end_time,
            self.item,
            "",
            self.status,
            0.0,
            0,
            0.0,
            0.0
        ]

    def winner(self):
        winning_stats = self.calculate_winning_stats()
        result = "|".join([f"{info:.2f}" if isinstance(info, float) else str(info) for info in winning_stats])

        print(result)
