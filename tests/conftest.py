import os

import pytest

from integration.setup_test_db import *


@pytest.fixture(scope="session")
def connection_pool(prepare_test_database):
    return init_connection_pool()


@pytest.fixture(scope="session")
def db_connections(connection_pool):
    connection = connection_pool.getconn()
    yield connection
    connection_pool.putconn(connection)


@pytest.fixture(scope="session", autouse=True)  # automatically apply to all tests
def prepare_test_database():
    initialize_test_db()
    initialize_test_tables()
    yield
    teardown_test_db()


@pytest.fixture(scope="session")
def insert_tea_pot_listing(db_connections):
    with db_connections.cursor() as cur:
        cur.execute("DELETE FROM auction WHERE item = 'tea_pot_1'")  # delete any existing data related to this fixture
        cur.execute("""
            INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
            VALUES ('tea_pot_1', 2, 7.00, 4, 20, 'UNSOLD');
        """)

        db_connections.commit()


@pytest.fixture(scope="session")
def default_auction():
    default_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "default_input.txt"
    )

    return default_path


@pytest.fixture(scope="session")
def incorrect_auction_time():
    bad_time_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "incorrect_time.txt"
    )

    return bad_time_path


@pytest.fixture(scope="session")
def tea_pot_bid_check():
    tea_pot_bids_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "test_bid_check_1.txt"
    )

    return tea_pot_bids_path


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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


# you can define and use this mock as a function argument wherever necessary
# @pytest.fixture(scope="function")
# def mock_initialize_tables(monkeypatch):
#     monkeypatch.setattr(
#         'application.auction.initialize_tables',
#         lambda x: None
#     )
