import argparse

from application.auction import Auction


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for auction behavior.")  # fmt: skip
    parser.add_argument("path", help="Path to input .txt file")
    parser.add_argument("--save", "-s", action="store_true")
    args = parser.parse_args()

    Auction(args.path, args.save)

    print("\nUnitPytestGame")
