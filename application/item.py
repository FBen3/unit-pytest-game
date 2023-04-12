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


