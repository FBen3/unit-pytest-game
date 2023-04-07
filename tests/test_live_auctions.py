import src.application.process_input as process_input


def test_live_auction_with_default_input(capfd, default_live_auction):
    process_input.load_input(default_live_auction)
    out, err = capfd.readouterr()
    expected_output = (
        "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n"
        "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
    )

    assert out == expected_output
