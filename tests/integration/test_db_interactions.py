from decimal import Decimal

import pytest
from psycopg2.errors import UniqueViolation

from application.auction import Auction
from application.db_procedures import (
    process_bidding,
    bid_check,
    process_listing,
    calculate_final_item_stats,
    check_no_bids,
    all_unexpired_items,
    update_status
)


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


def test_process_bidding(monkeypatch, db_connections, insert_tea_pot_listing, insert_tea_pot_bid):
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


def test_process_listing_after_closing_time(db_connections, insert_tea_pot_listing):
    with pytest.raises(UniqueViolation, match='duplicate key value violates unique constraint "auction_pkey"'):
        auction_listing_line = ["5", "3", "tea_pot_1", "17.00", "21"]
        process_listing(*auction_listing_line, db_connections)


def test_second_highest_bid_from_calculate_final_item_stats(db_connections, insert_tea_pot_listing, insert_bed_lamp_listing_and_bids):
    query_second_highest_bid = """
        SELECT
            item,
            amount AS second_max_amount
        FROM (
            SELECT
                item,
                amount,
                ROW_NUMBER() OVER (PARTITION BY item ORDER BY amount DESC) as bid_rank
            FROM
                bids
            WHERE
                item = %s
        ) ranked_bids
        WHERE
            bid_rank = 2
    """

    with db_connections.cursor() as cur:
        cur.execute(query_second_highest_bid, ("bed_lamp_1",))

        result = cur.fetchone()

    assert result is not None
    assert result[0] == "bed_lamp_1"
    assert result[1] == 7.00


def test_bid_stats_from_calculate_final_item_stats(db_connections, insert_bed_lamp_listing_and_bids):
    query_bid_stats = """
        SELECT
            item,
            MIN(amount) as min_amount,
            COUNT(id) as total_bid_count
        FROM
            bids
        WHERE
            item = %s
        GROUP BY
            item
    """

    with db_connections.cursor() as cur:
        cur.execute(query_bid_stats, ("bed_lamp_1",))

        result = cur.fetchone()

    assert result is not None
    assert result[0] == "bed_lamp_1"
    assert result[1] == 6.00
    assert result[2] == 3


def test_bid_details_from_calculate_final_item_stats(db_connections, insert_bed_lamp_listing_and_bids):
    query_bid_details = """
        SELECT
            b1.item,
            b1.bidder as max_bidder,
            b1.amount as max_amount
        FROM
            bids b1
        JOIN (
            SELECT 
                item, 
                MAX(amount) as max_amount
            FROM 
                bids
            WHERE 
                item = %s
            GROUP BY 
                item
        ) max_bids ON b1.item = max_bids.item AND b1.amount = max_bids.max_amount
        WHERE
            b1.item = %s
        ORDER BY
            b1.bid_time ASC
        LIMIT 1
    """

    with db_connections.cursor() as cur:
        cur.execute("""
            INSERT INTO bids (item, amount, bid_time, bidder)
            VALUES ('bed_lamp_1', 7.20, 6, 13);
        """)
        db_connections.commit()
        cur.execute(query_bid_details, ("bed_lamp_1","bed_lamp_1"))

        result = cur.fetchone()

    assert result is not None
    assert result[0] == "bed_lamp_1"
    assert result[1] == 10
    assert result[2] == Decimal('7.20')


def test_calculate_final_item_stats(monkeypatch, db_connections, suppress_initialize_tables, small_input):
    monkeypatch.setattr(
        'application.auction.process_listing',
        lambda *x: process_listing(*x, db_connections)
    )
    monkeypatch.setattr(
        'application.auction.process_bidding',
        lambda *x: process_bidding(*x, db_connections)
    )
    monkeypatch.setattr(
        'application.db_procedures.bid_check',
        lambda *x: bid_check(*x, db_connections)
    )
    monkeypatch.setattr(
        'application.db_procedures.check_no_bids',
        lambda x: check_no_bids(x, db_connections)
    )

    auction = Auction(save_option=False)
    auction.run(small_input)

    result = calculate_final_item_stats("camera_1", db_connections)

    assert result is not None
    assert result['item'] == "camera_1"
    assert result['bidder'] == 6
    assert result['highest_bid'] == 27.0
    assert result['second_highest_bid'] is None
    assert result['lowest_bid'] == 27.0
    assert result['total_bid_count'] == 1
    assert result['reserve_price'] == 27.0
    assert result['closing_time'] == 17
    assert result['status'] == "UNSOLD"


def test_all_unexpired_items(db_connections, insert_tea_pot_listing):
    result = all_unexpired_items(21, db_connections)

    assert result == ['tea_pot_1']


def test_update_stats(db_connections, insert_tea_pot_listing):
    update_status("tea_pot_1", db_connections)

    with db_connections.cursor() as cur:
        cur.execute("""
            SELECT
                item,
                status
            FROM
                auction
            WHERE
                item = %s
        """, ("tea_pot_1",)
        )

        result = cur.fetchone()

    assert result is not None
    assert result[0] == "tea_pot_1"
    assert result[1] == "SOLD"
