from unittest.mock import patch

import pytest

from src.application import process_input


# fmt: off
@pytest.mark.parametrize("test_input, expected_error, warning_msg", [
    ([], IndexError, "Please specify 1 argument"),
    (["input_1.txt", "input_2.txt"], IndexError, "Please specify 1 argument")
])
# fmt: on
def test_number_of_argument_inputs(test_input, expected_error, warning_msg):
    with pytest.raises(expected_error) as e_info:
        process_input.load_input(test_input)

    assert str(e_info.value) == warning_msg


# fmt: off
@pytest.mark.parametrize("test_input, warning_msg",[
    ("10|1|BUY|toaster_1|10.00|20", "action must be SELL or BID"),
    ("18,", "Unrecognised data in row")
])
# fmt: on
def test_valid_file_contents(test_input, warning_msg):
    with pytest.raises(ValueError) as e_info:
        process_input.process_input(test_input)

    assert str(e_info.value) == warning_msg


@patch("os.path.isfile")
def test_user_argument_is_a_text_file(mock_isfile):
    mock_isfile.return_value = True
    with pytest.raises(TypeError) as e_info:
        process_input.load_input(["not_text_file.json"])

    assert str(e_info.value) == "Input must be a text file"


@patch("os.path.isfile")
def test_input_file_not_found(mock_isfile):
    mock_isfile.return_value = False
    with pytest.raises(FileNotFoundError, match="^Could not find file$"):
        process_input.load_input(["non_existent_file.txt"])
