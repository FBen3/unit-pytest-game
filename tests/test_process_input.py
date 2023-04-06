from unittest.mock import patch

import pytest

from src.application import process_input


def test_only_one_argument_is_specified():
    with pytest.raises(IndexError) as e_info:
        process_input.load_input(["input_1.txt", "input_2.txt"])

    assert str(e_info.value) == "Please specify 1 argument"


@patch("os.path.isfile")
def test_user_argument_is_a_text_file(mock_isfile):
    mock_isfile.return_value = True
    with pytest.raises(TypeError) as e_info:
        process_input.load_input(["not_text_file.json"])

    assert str(e_info.value) == "Input must be a text file"


@patch("os.path.isfile")
def test_input_file_not_found(mock_isfile):
    mock_isfile.return_value = False
    with pytest.raises(FileNotFoundError) as e_info:
        process_input.load_input(["non_existent_file.txt"])

    assert str(e_info.value) == "Could not find file"


def test_no_argument_specified():
    with pytest.raises(IndexError) as e_info:
        process_input.load_input([])

    assert str(e_info.value) == "Please specify 1 argument"


def test_data_is_SELL_or_BID_type():
    with pytest.raises(ValueError) as e_info:
        process_input.process_input("10|1|BUY|toaster_1|10.00|20")

    assert str(e_info.value) == "action must be SELL or BID"


def test_heartbeat_message_check():
    with pytest.raises(ValueError) as e_info:
        process_input.process_input("18,")

    assert str(e_info.value) == "Unrecognised data in row"
