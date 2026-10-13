# Contributing

`patch.py` supports Python 3.8 or later and uses only the standard library.
The development environment adds [Ruff](https://docs.astral.sh/ruff/) for lint checks and formatting.
`requirements-dev.txt` pins Ruff 0.17.0.
The Ruff configuration targets Python 3.8 and uses a line length of 100 characters.

## Install development tools

1. Open a terminal in the repository directory.
2. Run `python -m venv .venv`.
3. If you use Windows PowerShell, run `.venv\Scripts\Activate.ps1`.
4. If you use Linux or macOS, run `. .venv/bin/activate`.
5. Run `python -m pip install -r requirements-dev.txt`.

## Check changes

Run the lint checks:

```sh
python -m ruff check .
```

Run the formatting check:

```sh
python -m ruff format --check .
```

These checks require no ROM files.
GitHub Actions runs both checks for pushes and pull requests.

## Fix lint and formatting

Apply the available safe lint fixes:

```sh
python -m ruff check --fix .
```

Format the Python files:

```sh
python -m ruff format .
```

Review the resulting changes.
Run both checks again.

The enabled rules cover Python errors, imports, common bugs, and version-compatible syntax updates.
Keep compatibility with Python 3.8.
Use your own supported ROM dumps to verify patch outputs when you change patch behavior.
Keep ROMs and emulator state files outside commits.
