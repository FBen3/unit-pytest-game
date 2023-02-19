import io
import os
import unittest
from unittest.mock import patch

import application.auction as auction
import application.process_input as process_input


DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 'fixtures/default_input.txt')

class TestLiveAuction(unittest.TestCase):


    def tearDown(self) -> None:
        # reset auction and closing records
        auction.auction_records = {}
        auction.closing_records = {}

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_input(self, mocked_stdout):
        process_input.load_input([DEFAULT_INPUT])
        expected_output = "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n" \
                          "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"

        self.assertEqual(mocked_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
