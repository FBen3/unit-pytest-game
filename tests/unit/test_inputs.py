import os
from unittest.mock import patch

import pytest

from application.auction import Auction


def test_input_not_found(monkeypatch):
    monkeypatch.setattr('application.auction.initialize_tables', lambda x: None)

    auction = Auction(save_option=False)

    with pytest.raises(FileNotFoundError) as expected_error:
        auction.run("")

    assert str(expected_error.value) == "Could not find input file"


def test_input_not_txt_file(monkeypatch):
    monkeypatch.setattr('application.auction.initialize_tables', lambda x: None)
    monkeypatch.setattr('os.path.isfile', lambda x: True)

    auction = Auction(save_option=False)

    with pytest.raises(TypeError) as expected_error:
        auction.run("incorrect_file.json")

    assert str(expected_error.value) == "Input must be a .txt file"


def test_input_valid_txt_file(monkeypatch, default_auction):
    monkeypatch.setattr('application.auction.initialize_tables', lambda x: None)

    with patch('application.auction.Auction.process_input') as mock_process_input:
        mock_process_input.return_value = None  # ignore behavior

        auction = Auction(save_option=False)

        try:
            auction.run(default_auction)
        except Exception as e:
            pytest.fail(f"Unexpected error occurred: {e}")


def test_input_is_chronologically_correct(monkeypatch, incorrect_auction_time):
    monkeypatch.setattr('application.auction.initialize_tables', lambda x: None)
    monkeypatch.setattr('application.auction.process_listing', lambda *x: None)

    auction = Auction(save_option=False)

    with pytest.raises(RuntimeError) as expected_error:
        auction.run(incorrect_auction_time)

    assert str(expected_error.value) == "Non-chronological input"
