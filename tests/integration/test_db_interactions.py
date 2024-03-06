import pytest

from unittest.mock import patch, MagicMock

from application.auction import Auction
from application.db_procedures import *


def test_bid_check(monkeypatch, db_connections, insert_tea_pot_listing, tea_pot_bid_check):
    monkeypatch.setattr(
        'application.auction.initialize_tables',
        lambda x: None
    )
    monkeypatch.setattr(
        'application.auction.process_bidding',
        lambda *x: process_bidding(*x, db_connections)
    )
    monkeypatch.setattr(
        'application.db_procedures.bid_check',
        lambda *x: bid_check(*x, db_connections)
    )

    auction = Auction(save_option=False)
    auction.run(tea_pot_bid_check)
    # finish writing assert after this code passes

    # is_valid_bid = bid_check("5", "10", "tea_pot_1", "8.50")

    # assert is_valid_bid == True


    # assert 1 == 1









# populate database accordingly
# mock conn, cur \\\ NO NEED, there should be genuine connection to test db
# assert the correct execute was called [? maybe; maybe it's not an integration thing]
# assert ideal fetchone result came back
# status SOLD -> assert return False
# [for later] do something params for UNSOLD ?

# 4|2|SELL|tea_pot_1|7.00|20
# 6|8|BID|tea_pot_1|2.50
# 8|5|BID|tea_pot_1|5.75
# 10|5|BID|tea_pot_1|8.50  <---





 ##### catch error in test: if closing_time is after clock time

