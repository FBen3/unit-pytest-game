import pytest

from application.auction import Auction


def test_auction_edge_cases_1_2_3_5_7(capsys, db_connections, suppress_initialize_tables, mock_full_db_operations, small_input):
    auction = Auction(save_option=False)
    auction.run(small_input)
    auction.report()

    captured_output, err = capsys.readouterr()
    output_lines = captured_output.strip().split("\n")

    expected_output = [
        "10|laptop_2||UNSOLD|0.00|3|35.99|30.00",
        "17|camera_1|6|SOLD|27.00|1|27.00|27.00",
        "16|watch_3|4|SOLD|57.00|2|57.00|57.00",
        "18|fork_1||UNSOLD|0.00|0|0.00|0.00"
    ]

    for result in expected_output:
        assert result in output_lines
