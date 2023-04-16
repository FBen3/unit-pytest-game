import os

import pytest


@pytest.fixture(scope="function")
def sold_stat_example():
    return ["20", "toaster_1", 8, "SOLD", 12.50, 3, 20.00, 7.50]


@pytest.fixture(scope="function")
def unsold_stat_example():
    return ["20", "tv_1", "", "UNSOLD", 0.0, 2, 200.0, 150.0]


@pytest.fixture(scope="function")
def default_live_auction():
    default_data_path = os.path.join(
        os.path.dirname(__file__), "integration", "default_input.txt"
    )

    return [default_data_path]
