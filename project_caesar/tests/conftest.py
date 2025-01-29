import argparse
import pytest


@pytest.fixture(autouse=True, scope='module')
def setup_module(pytestconfig):

    defaults = {
        'log_level': 'info',
        'debug': False,
    }

    log_level = pytestconfig.getoption("--log-level")
    debug = pytestconfig.getoption("--debug")

    if log_level is None:
        log_level = defaults['log_level']
    if debug is None:
        debug = defaults['debug']

    a = argparse.Namespace(
        log_level=log_level,
        debug=debug,
    )

    pytestconfig.test_args = a

