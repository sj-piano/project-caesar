# Imports
import argparse
import pytest


# Local imports
from project_caesar import config


def pytest_addoption(parser):
    """Registers custom command-line options for pytest."""
    parser.addoption(
        '--log-timestamp',
        action='store_true',
        help="Include timestamps in logs",
    )
    parser.addoption(
        '--log-to-file',
        action='store_true',
        help="Log to a file",
    )


@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):

    log_level = pytestconfig.getoption("--log-level")
    debug = pytestconfig.getoption("--debug")
    log_timestamp = pytestconfig.getoption("--log-timestamp")
    log_to_file = pytestconfig.getoption("--log-to-file")
    log_file = pytestconfig.getoption("--log-file")

    if log_level is None:
        log_level = config.log_level
    if debug is None:
        debug = config.debug
    if log_timestamp is None:
        log_timestamp = config.log_timestamp
    if log_to_file is None:
        log_to_file = config.log_to_file
    if log_file is None:
        log_file = config.log_file

    a = argparse.Namespace(
        log_level=log_level,
        debug=debug,
        log_timestamp=log_timestamp,
        log_to_file=log_to_file,
        log_file=log_file,
    )

    pytestconfig.test_args = a

