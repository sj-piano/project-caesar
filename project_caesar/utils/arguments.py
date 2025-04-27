# Imports
import argparse


# Local imports
from project_caesar.configuration import config
from project_caesar import constants


def get_common_parser():
    """
    Returns an ArgumentParser with common arguments.
    """

    # Disable default help to avoid conflicts with a child parser.
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        '--log-level',
        dest='log_level',
        type=str,
        default='info',
        choices=constants.LOG_LEVEL_NAMES,
        help="Set the logging level.",
    )

    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help="Sets log level to 'debug'. This overrides --log-level.",
    )

    parser.add_argument(
        "--log-timestamp",
        action='store_true',
        help="Choose whether to prepend a timestamp to each log line.",
    )

    parser.add_argument(
        '--log-to-file',
        action='store_true',
        help="Choose whether to save log output to a file.",
    )

    parser.add_argument(
        '--log-file',
        type=str,
        help="The path to the file that log output will be written to.",
        default=config.log_file,
    )

    return parser

