import pytest

from application.auction import Auction


def test_SOLD_item(monkeypatch, capsys, successful_bid_example):
    # mock initialize_tables to prohibit creating db tables
    monkeypatch.setattr(
        'application.auction.initialize_tables',
        lambda save_option: False
    )


    # mock all_unexpected_items to return an item list containing 'toaster_1'
    monkeypatch.setattr(
        'application.auction.all_unexpired_items',
        lambda x: ['toaster_1']
    )

    # mock calculate_final_item_stats to return an expected data structure
    monkeypatch.setattr(
        'application.auction.calculate_final_item_stats',
        lambda x: successful_bid_example
    )

    auction = Auction(save_option=False)
    auction.report()

    captured_output, err = capsys.readouterr()

    expected_output = "20|toaster_1|8|SOLD|12.50|3|20.00|7.50"

    assert expected_output in captured_output


def test_UNSOLD_item(monkeypatch, capsys, unsuccessful_bid_example):
    monkeypatch.setattr(
        'application.auction.initialize_tables',
        lambda save_option: False
    )

    monkeypatch.setattr(
        'application.auction.all_unexpired_items',
        lambda x: ['tv_1']
    )

    monkeypatch.setattr(
        'application.auction.calculate_final_item_stats',
        lambda x: unsuccessful_bid_example
    )

    auction = Auction(save_option=False)
    auction.report()

    captured_output, err = capsys.readouterr()

    expected_output = "20|tv_1||UNSOLD|0.00|2|200.00|150.00"

    assert expected_output in captured_output
