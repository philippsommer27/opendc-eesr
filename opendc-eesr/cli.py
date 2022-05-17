import argparse

import os
import sys

def main():
    parser = argparse.ArgumentParser(description="OpenDC energy and sustainability report builder")

    parser.add_argument(
                        'argu',
                        metavar='something',
                        type=str,
                        help="help help help",
                        )

    args = parser.parse_args()

    print(args.argu)

if __name__ == "__main__":
    sys.exit(main())