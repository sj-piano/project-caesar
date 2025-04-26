# Intro

Bitcoin Version 2: Project Caesar




# Prerequisites


- [pyenv](https://github.com/pyenv/pyenv)

  https://github.com/pyenv/pyenv-installer

- [direnv](https://direnv.net)

  https://direnv.net/docs/installation.html

- [Poetry](https://python-poetry.org/) for Python dependency management

  https://python-poetry.org/docs/#installing-with-the-official-installer


- Python 3.13.1, installed via pyenv.




# Setup


Use pyenv to install the required Python.

`pyenv install 3.13.1`


Clone the repo and set up the environment:

```bash
git clone git@github.com:sj-piano/project-caesar.git
cd project_caesar
direnv allow
pyenv local 3.13.1

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
# - In future, this will happen automatically via direnv.
poetry env activate
```


Confirm setup:

````
pyenv local
python --version
which python
poetry show
poetry env info
```


Note: If you're using e.g. VSCode and want to get the path to the Python interpreter, copy the Virtualenv/Path value from the output of `poetry env info`.




# Development


## Code Formatting [ignore for now !]

The project uses YAPF for code formatting with custom rules:
- 4 blank lines around classes
- 2 blank lines around methods
- 88 character line length

Format code with:
```bash
poetry run yapf -i -r .
```




## Testing

```bash
# Run a single test
poetry run pytest project_caesar/tests/test_hello_world.py::test_hello

# Allow print statements to work during test
poetry run pytest project_caesar/tests/test_hello_world.py::test_hello --capture=no

# Run all tests in a specific test file
poetry run pytest project_caesar/tests/test_hello_world.py

# Run all tests
poetry run pytest
```




# Run




CLI:

```bash
poetry run python cli.py
poetry run python cli.py --help
poetry run python cli.py --task hello
poetry run python cli.py --task hello --log-level=info
poetry run python cli.py --task get_python_version
```




Scripts:

```bash
poetry run python scripts/script1.py
```
