"""Output processing module.

This module contains the logic to parse a list of
item stats accumulated throughout the game, and print
it in a pipe-delimited format.

"""


def print_stats(ending_stats: list):
    result = "|".join(
        [
            f"{info:.2f}" if isinstance(info, float) else str(info)
            for info in ending_stats
        ]
    )
    print(result)
