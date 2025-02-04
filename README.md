# Intro

Bitcoin Version 2: Project Caesar




# Prerequisites


- [pyenv](https://github.com/pyenv/pyenv)

- Python 3.13.1, installed via pyenv.

- [direnv](https://direnv.net)




# Setup


Use pyenv to install the required Python.

`pyenv install 3.13.1`


Clone the repo and go through setup.

```bash

git clone git@github.com:sj-piano/project-caesar.git

cd project_caesar

direnv allow

pyenv local 3.13.1

# Create a local virtualenv.
python -m venv .venv

# Add this alias to your .bashrc or .zshrc file.
alias venv="source .venv/bin/activate"

venv

pip install -r requirements.txt

```




# Run




CLI:

```

python cli.py

python cli.py --help

python cli.py --task hello

python cli.py --task hello --log-level=info

python cli.py --task get_python_version

```




Scripts:

```

python scripts/script1.py

```




Tests:

```

# Run a single test
pytest project_caesar/tests/test_hello_world.py::test_hello

# Allow print statements to work during test
# - Note: The --capture=no option will also cause print statements _within the test code_ to produce output.
# - You can also use the -s shortcut.
pytest project_caesar/tests/test_hello_world.py::test_hello --capture=no

# Run all tests in a specific test file
pytest project_caesar/tests/test_hello_world.py

# Run tests with relatively little output
pytest --quiet project_caesar/tests/test_hello_world.py

# Run all tests
pytest

# Run all tests, including submodule tests
pytest --override-ini addopts="" project_caesar/submodules

```



