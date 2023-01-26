#!/usr/bin/env python3
import sys

from application.process_input import load_input


if __name__ == '__main__':
    path = sys.argv[1:]
    load_input(path)

    print("\nUnitPytestGame")
