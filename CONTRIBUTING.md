# Contributing to Ghost Babel Color Corrections

The project covers the released APC correction and the experimental Campbell portrait correction.
Each correction has separate regional manifests and standalone patch files.

The APC manifests are `changes.json`, `changes-eu.json`, and `changes-jp.json` in the repository directory.
The Campbell manifests are `changes-us.json`, `changes-eu.json`, and `changes-jp.json` under `campbell/`.
APC patches are in `patches/`; Campbell patches are in `campbell/patches/`.

Both standalone corrections require clean regional ROMs.
Local combined ROMs passed the checks in [COMBINED_VALIDATION.md](campbell/COMBINED_VALIDATION.md).
The repository does not contain combined patch files.
The standalone BPS patches cannot be applied sequentially.

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

## Verify patch changes

Use your own supported clean ROM dumps when a change affects patch behavior.
Place `--fix` before the subcommand.
Select `--fix apc` for APC patches or `--fix campbell` for Campbell patches.
The default selection is `apc`.

Verify both corrections against a clean source ROM:

```sh
python patch.py --fix apc verify "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell verify "/path/to/Metal Gear Solid (USA).gbc"
```

Rebuild the affected regional patches:

```sh
python patch.py --fix apc build "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell build "/path/to/Metal Gear Solid (USA).gbc"
```

Each command writes that region's BPS and IPS files into the selected correction's patch directory.
Each manifest records the expected source hashes, target hashes, and byte changes.
Keep these records consistent with the generated patches.

Run the relevant emulator checks when a change affects graphics or palette data.
Record the results and limits in the relevant validation document.
The [APC validation](VALIDATION.md) and [Campbell validation](campbell/VALIDATION.md) describe the existing checks.
Physical Game Boy Color hardware remains untested.

Keep ROMs and emulator state files outside commits.
