# Intro

Bitcoin Version 2: Project Caesar




# Prerequisites


Python3

Python3 virtualenv package

direnv




# Setup


```
git clone git@github.com:sj-piano/project-caesar.git

cd project_caesar

direnv allow

python3 -m venv .venv

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

python3 scripts/script1.py

```




Tests:

```

# Run all tests, including submodule tests.
pytest

# Run all tests, excluding submodule tests.
pytest --ignore=bitcoin_toolset/submodules

# Run all tests in a specific test file
pytest bitcoin_toolset/test/test_hello.py

# Run tests with relatively little output
pytest --quiet bitcoin_toolset/test/test_hello.py

# Run a single test
pytest bitcoin_toolset/test/test_hello.py::test_hello

# Print log output in real-time during a single test
pytest --capture=no --log-cli-level=INFO bitcoin_toolset/test/test_hello.py::test_hello

# Note: The --capture=no option will also cause print statements within the test code to produce output.

```



