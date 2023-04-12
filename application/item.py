from dataclasses import dataclass, field, asdict



# @dataclass
# class AuctionData:
#     timestamp: int
#     user_id: int
#     action: str
#     item: str
#
#     def __post_init__(self):
#         self.timestamp = int(self.timestamp)
#         self.user_id = int(self.user_id)
#
#
# @dataclass
# class Bid(AuctionData):
#     bid_amount: float


@dataclass
class Item:
    reserve_price: float
    auction_end_time: int
    status: str = "UNSOLD"
    bids: dict = field(default_factory=dict)

    def __post_init__(self):
        del self.action
        self.reserve_price = float(self.reserve_price)
        self.auction_end_time = int(self.auction_end_time)

    @property
    def auction_start_time(self):
        return self.timestamp

    @property
    def seller(self):
        return self.user_id

    def listing_record(self):
        print(asdict(self))
        return asdict(self)




