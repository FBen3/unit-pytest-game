from src.application import process_output


def test_output_with_different_stats_filled(capfd, sold_stat_example):
    process_output.print_stats(sold_stat_example)
    out, err = capfd.readouterr()

    assert out == "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n"


def test_output_with_missing_stats(capfd, unsold_stat_example):
    process_output.print_stats(unsold_stat_example)
    out, err = capfd.readouterr()

    assert out == "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
