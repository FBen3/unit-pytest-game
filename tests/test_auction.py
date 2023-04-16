from src.application import auction


def test_determine_item_winner():
    output = auction.determine_item_winner(
        {4: [(12, 6.5), (17, 20.0)], 9: [(13, 12.5), (18, 22.0)]}
    )

    assert output == {
        "highest_bidder": 9,
        "highest_bid": (18, 22.0),
        "second_highest_bid": (17, 20.0),
        "total_bids": 4,
        "lowest_bid": 6.5,
    }


def test_collate_item_information_sold():
    output_stat = auction.collate_item_information(
        {
            "auction_start_time": 10,
            "seller": 1,
            "item": "toaster_1",
            "reserve_price": 10.0,
            "auction_end_time": 20,
            "status": "UNSOLD",
            "bids": {4: [(12, 6.5), (17, 20.0)], 9: [(13, 12.5), (18, 22.0)]},
        }
    )

    assert output_stat == {
        "sold_status": "SOLD",
        "winner": 9,
        "price_to_pay": 20.0,
        "total_bids": 4,
        "highest_bid": 22.0,
        "lowest_bid": 6.5,
    }


def test_collate_item_information_unsold():
    output_unsold_stat = auction.collate_item_information(
        {
            "auction_start_time": 15,
            "seller": 8,
            "item": "tv_1",
            "reserve_price": 250.0,
            "auction_end_time": 20,
            "status": "UNSOLD",
            "bids": {},
        }
    )

    assert output_unsold_stat == {
        "sold_status": "UNSOLD",
        "winner": "",
        "price_to_pay": 0.0,
        "total_bids": 0,
        "highest_bid": 0.0,
        "lowest_bid": 0.0,
    }
