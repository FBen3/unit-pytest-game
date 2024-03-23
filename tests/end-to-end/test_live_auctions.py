import pytest

from application.auction import *
from application.db_procedures import (
    process_listing,
    process_bidding,
    bid_check,
    check_no_bids
)


def test_auction_edge_cases_1_2_3_5_7(capsys, monkeypatch, db_connections, suppress_initialize_tables, small_input):
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
    monkeypatch.setattr(
        'application.auction.all_unexpired_items',
        lambda x: all_unexpired_items(x, db_connections)
    )
    monkeypatch.setattr(
        'application.auction.calculate_final_item_stats',
        lambda x: calculate_final_item_stats(x, db_connections)
    )
    monkeypatch.setattr(
        'application.auction.update_status',
        lambda x: update_status(x, db_connections)
    )

    auction = Auction(save_option=False)
    auction.run(small_input)
    auction.report()

    captured_output, err = capsys.readouterr()
    output_lines = captured_output.strip().split("\n")

    expected_output = [
        "10|laptop_2||UNSOLD|0.00|3|35.99|30.00",
        "17|camera_1|6|SOLD|27.00|1|27.00|27.00",
        "16|watch_3|4|SOLD|57.00|2|57.00|57.00",
        "18|fork_1||UNSOLD|0.00|0|0.00|0.00"
    ]

    for result in expected_output:
        assert result in output_lines
