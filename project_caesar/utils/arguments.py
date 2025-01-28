# Imports
import argparse


def get_common_parser():
    """
    Returns an ArgumentParser with common arguments.
    """
    # Disable default help to avoid conflicts with a child parser.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)"
    )
    return parser

