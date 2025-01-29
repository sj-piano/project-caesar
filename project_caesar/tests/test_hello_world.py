# This test file is used to confirm that pytest is working correctly.
# Use this command:
# pytest project_caesar/tests/test_hello_world.py


# Imports
import pkgutil
import pytest


# Local imports
from project_caesar.code import hello
from project_caesar.utils import module_logger


# Logger
logger, log, deb = module_logger.create_logger(__file__)


# Configure logger
@pytest.fixture(autouse=True, scope='module')
def setup_logger(pytestconfig):
    module_logger.configure_logger_from_args(logger, pytestconfig.test_args)


def test_hello():
    x = hello.hello_world()
    print(x)
    assert x == 'hello world'


def test_hello_data():
    data_file = 'fixtures/hello_world.txt'
    data = pkgutil.get_data(__name__, data_file).decode('ascii').strip()
    assert data == 'hello world'


def test_hello_logger():
    log('hello world')
    assert 1 == 1

