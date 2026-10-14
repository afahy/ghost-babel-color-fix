# Contributing to Ghost Babel Color Corrections

The project covers the APC correction and the Campbell portrait correction.
APC patches are the primary release files.
Optional combined patches include both corrections.
Campbell-only patches remain available for development.
Each patch selection has separate regional manifests and patch files.

The APC manifests are `changes.json`, `changes-eu.json`, and `changes-jp.json` in the repository directory.
The Campbell manifests are `changes-us.json`, `changes-eu.json`, and `changes-jp.json` under `campbell/`.
The combined manifests use the same regional names under `combined/`.
APC patches are in `patches/`; Campbell patches are in `campbell/patches/`; combined patches are in `combined/patches/`.

All patch selections require clean regional ROMs.
Combined ROMs passed the checks in [COMBINED_VALIDATION.md](campbell/COMBINED_VALIDATION.md).
You cannot apply the standalone BPS patches sequentially.

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

Run the tests:

```sh
python -m unittest
```

The tests compare the committed manifests, patch files, and `SHA256SUMS.txt` files.

These checks require no ROM files.
GitHub Actions runs all three checks for pushes and pull requests.

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
Place `--fix` before or after the subcommand.
Select `--fix apc`, `--fix campbell`, or `--fix combined`.
The `apply` and `verify` commands default to `apc`.
The `build` command builds APC and combined patches by default.
An explicit `--fix` selection builds only that selection.

Verify each patch selection against a clean source ROM:

```sh
python patch.py --fix apc verify "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell verify "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix combined verify "/path/to/Metal Gear Solid (USA).gbc"
```

Rebuild both release selections for a region:

```sh
python patch.py build "/path/to/Metal Gear Solid (USA).gbc"
```

Rebuild a specific patch selection:

```sh
python patch.py --fix apc build "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell build "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix combined build "/path/to/Metal Gear Solid (USA).gbc"
```

Each command writes that region's BPS and IPS files into the selected correction's patch directory.
With `--output-dir`, the command writes all selected patch files into that directory.
The command also updates `SHA256SUMS.txt` in the output directory.
Each manifest records the expected source hashes and target hashes.
The APC and Campbell manifests record the byte changes; the combined manifests reuse them.
Keep these records consistent with the generated patches.

Run the relevant emulator checks when a change affects graphics or palette data.
Record the results and limits in the relevant validation document.
The [APC validation](VALIDATION.md) and [Campbell validation](campbell/VALIDATION.md) describe the existing checks.
Physical Game Boy Color hardware remains untested.

Keep ROMs and emulator state files outside commits.
