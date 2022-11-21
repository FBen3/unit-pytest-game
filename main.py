#!/usr/bin/env python3
import sys





def load_input(auction_file: str):
    try:
        with open(auction_file, 'r') as reader:
            for line in reader:
                print(line.strip())
    except FileNotFoundError as e:
        print(e)
        print("Please enter a valid path.")
    return



if __name__ == '__main__':
    path = sys.argv[1]
    load_input(path)

    print("UnitPytestGame")
