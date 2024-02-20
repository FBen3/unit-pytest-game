import os

import pytest


@pytest.fixture(scope="function")
def successful_bid_example():
    return {
        'bidder': 8,
        'closing_time': 20,
        'highest_bid': 20.0,
        'item': 'toaster_1',
        'lowest_bid': 7.5,
        'reserve_price': 10.0,
        'second_highest_bid': 12.5,
        'status': 'UNSOLD',
        'total_bid_count': 3
    }


@pytest.fixture(scope="function")
def unsuccessful_bid_example():
    return {
        'bidder': 3,
        'closing_time': 20,
        'highest_bid': 200.0,
        'item': 'tv_1',
        'lowest_bid': 150.0,
        'reserve_price': 250.0,
        'second_highest_bid': 150.0,
        'status': 'UNSOLD',
        'total_bid_count': 2
    }


@pytest.fixture(scope="function")
def default_auction():
    default_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "default_input.txt"
    )

    return default_path




