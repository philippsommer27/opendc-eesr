import argparse
import os
import sys
import interface

def dispatch(data, args=None):
    interface.generate_standard_profile(data)

def main():
    parser = argparse.ArgumentParser(prog="OpenDC EESR", description="OpenDC energy and sustainability report builder")

    parser.add_argument(
                        '-d',
                        '--data',
                        metavar='path',
                        type=str,
                        required=True,
                        help="Path to JSON file containing data for report generator",
                        )

    args = parser.parse_args()

    dispatch(args.data)

if __name__ == "__main__":
    # sys.exit(main())
    main()