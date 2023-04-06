"""Test module for input processing.

This module contains all tests assessing
the logic in `process_input.py`

"""
import pytest

from src.application import process_input


def test_only_one_argument_is_specified():
    with pytest.raises(IndexError) as e_info:
        process_input.load_input(["input_1.txt", "input_2.txt"])

    assert str(e_info.value) == "Please specify 1 argument"
