import pytest
from psycopg2.errors import UniqueViolation

from unittest.mock import patch, MagicMock

from application.auction import Auction  # used for test_bid_check
from application.db_procedures import *


# def test_bid_check(monkeypatch, db_connections, insert_tea_pot_listing, tea_pot_bid_check):
#     monkeypatch.setattr(
#         'application.auction.initialize_tables',
#         lambda x: None
#     )
#     monkeypatch.setattr(
#         'application.auction.process_bidding',
#         lambda *x: process_bidding(*x, db_connections)
#     )
#     monkeypatch.setattr(
#         'application.db_procedures.bid_check',
#         lambda *x: bid_check(*x, db_connections)
#     )
#
#     auction = Auction(save_option=False)
#     auction.run(tea_pot_bid_check)
#
#     is_valid_bid = bid_check("5", "10", "tea_pot_1", "8.50", db_connections)
#
#     assert is_valid_bid == True
#     # this test has been a complete mess.
#     # Understandably this was done to see if you could:
#     #   1. create a test dates                                  [OK]
#     #   2. setup a connection pool to that database             [OK]
#     #   3. suppress setting up prod tables                      [OK]
#     #   4. inject SQL data via a fixture                        [CHECK]
#     #   5. populate rest of database by reading in data         [While this has worked, it side-stepped intended test purpose]
#     #   6. test whether bid_check works on engineered database  [Completely redundant and stupid at this point in the logic]
#     # You've done it; see how bad it is. This is not a good test anymore so strive for legitimate testing procedure now.


def test_process_bidding(monkeypatch, db_connections, suppress_initialize_tables, insert_tea_pot_listing, insert_tea_pot_bid):
    monkeypatch.setattr(
        'application.db_procedures.bid_check',
        lambda *x: bid_check(*x, db_connections)
    )

    process_bidding("11", "5", "tea_pot_1", "9.50", db_connections)


    with db_connections.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM bids 
            WHERE item = %s AND bidder = %s
        """, ('tea_pot_1', 5)
        )

        result = cur.fetchall()

    assert result is not None
    assert result[0][3] == 10
    assert result[0][2] == 8.50
    assert result[1][3] == 11
    assert result[1][2] == 9.50


def test_process_listing_after_closing_time(db_connections, suppress_initialize_tables, insert_tea_pot_listing):
    with pytest.raises(UniqueViolation, match='duplicate key value violates unique constraint "auction_pkey"'):
        auction_listing_line = ["5", "3", "tea_pot_1", "17.00", "21"]
        process_listing(*auction_listing_line)



##### catch error in test: if closing_time is after clock time

# 4|2|SELL|tea_pot_1|7.00|20
# 6|8|BID|tea_pot_1|2.50
# 8|5|BID|tea_pot_1|5.75
# 10|5|BID|tea_pot_1|8.50  <---
# 11|5|BID|tea_pot_1|9.50  <---



