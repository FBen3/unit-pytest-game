#!/usr/bin/env python3
import sys



def load_input(auction_file: list):
    try:
        with open(auction_file[0], 'r') as reader:
            for line in reader:
                print(line.strip())
    except (FileNotFoundError, IndexError) as e:
        print(e)
        print("Please enter a valid path.")
    except:
        print("Unexpected error occurred")
        raise


if __name__ == '__main__':
    path = sys.argv[1:]
    load_input(path)

    print("\nUnitPytestGame")
