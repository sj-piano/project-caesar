# This test file is used to confirm that pytest is working correctly.
# Use this command:
# pytest bitcoin_toolset/test/test_hello.py


# Imports
import pkgutil


# Local imports
from project_caesar.code import hello


def test_hello():
  x = hello.hello_world()
  print(x)
  assert x == 'hello world'


def test_hello_data():
  data_file = 'fixtures/hello_world.txt'
  data = pkgutil.get_data(__name__, data_file).decode('ascii').strip()
  assert data == 'hello world'

