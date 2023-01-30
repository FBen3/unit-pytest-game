import io
import os
import unittest
from unittest.mock import patch

import application.auction as auction
import application.process_input as process_input


DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 'fixtures/default_input.txt')

class TestAuction(unittest.TestCase):

    @patch('builtins.print')
    def test_default_input(self, mocked_print):
        process_input.load_input([DEFAULT_INPUT])

        mocked_print.assert_called_with("20|tv_1||UNSOLD|0.00|2|200.00|150.00")


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_default_input_2(self, mocked_stdout):
        expected_output = "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n" \
                          "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
        process_input.load_input([DEFAULT_INPUT])

        self.assertEqual(mocked_stdout.getvalue(), expected_output)







    # def test_collate_item_information(self):
    #     pass
    #
    # def test_calculate_item_stats(self):
    #     pass
    #
    # def test_close_auction(self):
    #     pass
    #
    # def test_process_sell(self):
    #     pass
    #
    # def test_process_bid(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
