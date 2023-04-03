import unittest
from unittest.mock import patch

from application.process_output import print_stats


class TestOutput(unittest.TestCase):
    @patch("builtins.print")
    def test_output_with_all_stats_filled(self, mocked_print):
        print_stats(["20", "toaster_1", 8, "SOLD", 12.50, 3, 20.00, 7.50])
        mocked_print.assert_called_with(
            "20|toaster_1|8|SOLD|12.50|3|20.00|7.50"
        )

    @patch("builtins.print")
    def test_output_with_missing_stats(self, mocked_print):
        print_stats(["20", "tv_1", "", "UNSOLD", 0.0, 2, 200.0, 150.0])
        mocked_print.assert_called_with("20|tv_1||UNSOLD|0.00|2|200.00|150.00")


if __name__ == "__main__":
    unittest.main()
