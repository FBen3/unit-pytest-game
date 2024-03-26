from unittest.mock import Mock

import pytest

from integration.setup_test_db import *
from application.db_procedures import (
    process_listing,
    process_bidding,
    bid_check,
    check_no_bids,
    all_unexpired_items,
    calculate_final_item_stats,
    update_status
)


@pytest.fixture(scope="session", autouse=True)  # automatically apply to all tests
def prepare_test_database():
    initialize_test_db()
    initialize_test_tables()
    yield
    teardown_test_db()


@pytest.fixture(scope="session")
def connection_pool(prepare_test_database):
    conn_pool = init_connection_pool()
    yield conn_pool
    conn_pool.closeall()


# `function` scoping this fixture is crucial for ensuring that the connection gets
# refreshed (each time it's requested), and each test function gets a fresh database
# connection. This also mitigates the issues of one transactions interfering with another,
# promoting test isolation.
@pytest.fixture(scope="function")
def db_connections(connection_pool):
    connection = connection_pool.getconn()
    yield connection
    connection_pool.putconn(connection)


@pytest.fixture(scope="function", autouse=True)
def reset_test_db(db_connections):
    yield
    db_connections.rollback()  # roll back aborted transactions
    with db_connections.cursor() as cur:
        cur.execute("TRUNCATE auction, bids CASCADE;")
    db_connections.commit()


@pytest.fixture(scope="function")
def insert_tea_pot_listing(db_connections):
    with db_connections.cursor() as cur:
        cur.execute("DELETE FROM auction WHERE item = 'tea_pot_1'")  # delete any existing data related to this fixture
        cur.execute("""
            INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
            VALUES ('tea_pot_1', 2, 7.00, 4, 20, 'UNSOLD');
        """)

    db_connections.commit()


@pytest.fixture(scope="function")
def insert_tea_pot_bid(db_connections):
    with db_connections.cursor() as cur:
        cur.execute("DELETE FROM bids WHERE item = 'tea_pot_1'")
        cur.execute("""
            INSERT INTO bids (item, amount, bid_time, bidder)
            VALUES ('tea_pot_1', 8.50, 10, 5);
        """)

    db_connections.commit()


@pytest.fixture(scope="function")
def insert_bed_lamp_listing_and_bids(db_connections):
    with db_connections.cursor() as cur:
        cur.execute("DELETE FROM bids WHERE item = 'bed_lamp_1'")
        cur.execute("""
            INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
            VALUES ('bed_lamp_1', 18, 5.00, 1, 21, 'UNSOLD');
        """)
        cur.execute("""
            INSERT INTO bids (item, amount, bid_time, bidder) VALUES 
                ('bed_lamp_1', 6.00, 2, 10),
                ('bed_lamp_1', 7.00, 3, 13),
                ('bed_lamp_1', 7.20, 5, 10);
        """)

    db_connections.commit()


# these fixtures, used for static files & configs, which do not change state between tests,
# are ideal to be `session` scoped
@pytest.fixture(scope="session")
def default_auction():
    default_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "default_input.txt"
    )

    return default_path


@pytest.fixture(scope="session")
def small_input():
    small_input_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "small_input.txt"
    )

    return small_input_path


@pytest.fixture(scope="session")
def medium_input():
    medium_input_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "medium_input.txt"
    )

    return medium_input_path


@pytest.fixture(scope="session")
def large_input():
    large_input_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "large_input.txt"
    )

    return large_input_path


@pytest.fixture(scope="session")
def incorrect_auction_time():
    bad_time_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "incorrect_time.txt"
    )

    return bad_time_path


@pytest.fixture(scope="session")
def tea_pot_bid_check():
    tea_pot_bids_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "tea_pot_bid_check.txt"
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
@pytest.fixture(scope="function")
def suppress_initialize_tables(monkeypatch):
    monkeypatch.setattr(
        'application.auction.initialize_tables',
        lambda x: None
    )


@pytest.fixture
def mock_full_db_operations(monkeypatch, db_connections):
    mock_process_listing = Mock(side_effect=lambda *x: process_listing(*x, db_connections))
    mock_process_bidding = Mock(side_effect=lambda *x: process_bidding(*x, db_connections))
    mock_bid_check = Mock(side_effect=lambda *x: bid_check(*x, db_connections))
    mock_check_no_bids = Mock(side_effect=lambda x: check_no_bids(x, db_connections))
    mock_all_unexpired_items = Mock(side_effect=lambda x: all_unexpired_items(x, db_connections))
    mock_calculate_final_item_stats = Mock(side_effect=lambda x: calculate_final_item_stats(x, db_connections))
    mock_update_status = Mock(side_effect=lambda x: update_status(x, db_connections))

    monkeypatch.setattr('application.auction.process_listing', mock_process_listing)
    monkeypatch.setattr('application.auction.process_bidding', mock_process_bidding)
    monkeypatch.setattr('application.db_procedures.bid_check', mock_bid_check)
    monkeypatch.setattr('application.db_procedures.check_no_bids', mock_check_no_bids)
    monkeypatch.setattr( 'application.auction.all_unexpired_items', mock_all_unexpired_items)
    monkeypatch.setattr('application.auction.calculate_final_item_stats', mock_calculate_final_item_stats)
    monkeypatch.setattr('application.auction.update_status', mock_update_status)

    # optional return
    # By returning the mocks, you allow other/future tests that use this fixture to customize the behavior of these mock
    # objects further for different test scenarios; (e.g. if a different test needs to override side_effect,
    # or wants to specify a return_value)
    # Returning the mocks make them accessible within the test; (so you can use methods like mock.assert_called_with()
    # or check mock.call_count if needed).
    # In summary, different tests might need to interact with these mocks differently. By having access to the mock
    # objects directly, future tests can adjust the mocks to fit their specific requirements without affecting other
    # tests; (leading to more flexible and maintainable testing; this ability to override allows for greater flexibility
    # and customization for different test scenarios).
    # It also makes the fixture more reusable. Each test can customize the mock behavior as needed, overriding the default.
    return {
        "process_listing": mock_process_listing,
        "process_bidding": mock_process_bidding,
        "bid_check": mock_bid_check,
        "check_no_bids": mock_check_no_bids,
        "all_unexpired_items": mock_all_unexpired_items,
        "calculate_final_item_stats": mock_calculate_final_item_stats,
        "update_status": mock_update_status
    }
