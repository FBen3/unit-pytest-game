import unittest
from unittest.mock import patch

from application.process_output import print_stats


class TestOutput(unittest.TestCase):

    # change/update this so it actually makes sense
    @patch('builtins.print')
    def test_output_parser(self, mocked_print):
        print_stats(['toaster', 10, 20.2])
        mocked_print.assert_called_with('toaster|10|20.20')


    # add more tests ...

    # if I want to test that a function raises an error
    #     with self.assertRaises(ValueError):
    #         print_stats()


if __name__ == '__main__':
    unittest.main()











