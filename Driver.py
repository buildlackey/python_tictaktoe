import argparse
import logging

from tictaktoe.Controller import *

import logging

def setup_logging(verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main():
    parser = argparse.ArgumentParser(description="Simple tic tak toe program using brute force search logic")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    setup_logging(verbose=args.verbose)

    GameSessionController().start()


if __name__ == "__main__":
    main()
