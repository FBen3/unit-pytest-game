import os

import pytest


@pytest.fixture(scope="function")
def default_live_auction():
    default_data_path = os.path.join(
        os.path.dirname(__file__), "integration", "default_input.txt"
    )

    return [default_data_path]
