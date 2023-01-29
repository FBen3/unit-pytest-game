import unittest
from unittest.mock import patch

import application.auction as auction


class TestAuction(unittest.TestCase):


    # TODO: I think ...
    """
    Start looking into fixtures tomorrow and create different input files
    with various auction scenario. Then, write test here...

    1st test could be test_default_interview_inpuit(): which then tests the default
    input txt file.

    Then create another .txt file with another scenario. Write a second test for that
    .txt file / scenario / action

    and so, and so on. I think that's what this file should contain.


    
    """



    def test_determine_item_winner(self):

        auction.process_bid([12, 8, 'BID', 'toaster_1', 7.50])


        pass











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
