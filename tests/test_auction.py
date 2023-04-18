import os

import pytest

from application.auction import Auction
from application.item import Item


class TestDefaultInput:

    @classmethod
    def setup_class(cls):
        cls.default_live_auction = [os.path.join(os.path.dirname(__file__), "integration", "default_input.txt")]

    def test_default_live_auction(self, capfd):
        input_file = self.default_live_auction
        auction = Auction(input_file)
        auction.start()
        auction.close()

        out, err = capfd.readouterr()
        expected_output = (
            "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n"
            "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
        )

        assert out == expected_output


class TestAuction:


    @pytest.mark.unit
    def test_process_listing(self):
        auction = Auction("")
        example_item = Item(15, 1, "test_item", 10, 25)
        auction.process_listing(example_item)

        assert auction.auction_records == {"test_item": example_item}
        assert auction.closing_records == {25: ["test_item"]}


class TestItem:
    pass












