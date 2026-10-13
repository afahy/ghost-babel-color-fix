# Metal Gear Solid: Ghost Babel Color Corrections

This project provides color corrections for *Metal Gear Solid* on Game Boy Color, also known as *Metal Gear: Ghost Babel*.
It includes the Stage 2 APC correction and an experimental Campbell portrait correction for the opening briefing.
The repository contains no game ROM.

## Corrections

### Stage 2 APCs

The APC patch corrects the two armored personnel carriers in Stage 2's yard outside Galuade fortress.
It corrects their front corners and lower left corners.
The original tiles use container and grass palettes, which produce gray, blue, navy, lime, and olive patches on the hulls.
The patch uses the hull's green colors and preserves the surrounding sand.
Six brown shadow pixels become dark green so all corrected tiles fit the room's available palettes.
It also corrects the APCs' thermal palette mapping.

### Campbell's opening portrait

The Campbell patch gives his face consistent skin colors and adjusts the collar and background boundaries.
Small outline and shading changes keep the portrait within each background tile's four-color limit.
The patch updates both portrait orientations and preserves Snake's colors, dialogue, and separate portrait fades.

The original artist's intent remains uncertain.
This experimental patch offers an optional color interpretation.
[Campbell's documentation](campbell/README.md) describes its design, patch files, and test results.

## Download

Each correction has separate USA, European, and Japanese patches in BPS and IPS formats.

| Correction | Status | Patch files |
| --- | --- | --- |
| APCs | Released as version 1.1 | [Release download](https://github.com/afahy/ghost-babel-tank-color-fix/releases/tag/v1.1.0) |
| Campbell | Experimental and unreleased | [Regional patches](campbell/README.md#patch-files) |

Version 1.1 contains the APC correction only.
The standalone Campbell patches contain the portrait correction only.
ROMs containing both corrections passed the [combined validation checks](campbell/COMBINED_VALIDATION.md).
Each standalone BPS patch requires a clean ROM; the two files cannot be applied sequentially.

## Comparison

The images below show the difference between the original and patched ROMs.

### APCs

| Original | Patched |
| --- | --- |
| ![Original APC colors](images/before.png) | ![Patched APC colors](images/after.png) |

### Campbell

| Original | Patched |
| --- | --- |
| ![Original Campbell portrait](images/campbell-before.png) | ![Patched Campbell portrait](images/campbell-after.png) |

SameBoy rendered these images directly from the original and patched ROMs.

## Required source ROMs

Use a clean ROM dump without an added copier header.
Select the desired correction and your dump's region.

| Region | Source ROM | Size | CRC32 | MD5 |
| --- | --- | --- | --- | --- |
| USA | Metal Gear Solid (USA) | 2,097,152 bytes | `04b0c5d6` | `f6dd1b1e5747412b9e5f25376c972d5a` |
| Europe | Metal Gear Solid (Europe) (En,Fr,De,Es,It) | 4,194,304 bytes | `16796957` | `7971c95ad9745fe20df52e03cd52f636` |
| Japan | Metal Gear Ghost Babel (Japan) | 2,097,152 bytes | `7831f84d` | `7830328f323bd77d52a6985b1b10031f` |

The USA, European, and Japanese patch filenames contain `us`, `eu`, and `jp`, respectively.
The manifests contain additional source and target hashes.

The BPS patch checks the source ROM checksum.
The IPS format does not include a source checksum.

## Apply the patch

### Desktop with Floating IPS

[Floating IPS (Flips)](https://github.com/Sir-Walrus/Flips/releases) supports both BPS and IPS patches.

1. Obtain your own clean ROM dump.
2. Download Floating IPS for your operating system.
3. Start Floating IPS.
4. Select **Apply Patch**.
5. Select the BPS patch for your chosen correction and ROM region.
6. Select your clean ROM dump.
7. Save the patched ROM as a separate file.
8. Start the patched ROM in your emulator or flash cartridge.

### Browser with Rom Patcher JS

1. Open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
2. Select your clean dump in **ROM file**.
3. Select the matching correction and regional BPS patch in **Patch file**.
4. Select **Apply patch**.
5. Save the patched ROM as a separate file.

Use a fresh emulator session to load the changed graphics and palettes.

## Apply with Python

The included tool requires Python 3.8 or later and uses only the standard library.
The tool checks all source hashes and verifies the patched ROM hashes.
It detects the USA, European, or Japanese source automatically.
It rejects an existing output file.

Select the correction with `--fix apc` or `--fix campbell`.
The tool selects `apc` when you omit `--fix`.

Run the command for your desired correction from the repository directory:

```sh
python patch.py --fix apc apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/Metal Gear Solid (USA) (APC Color Fix).gbc"
python patch.py --fix campbell apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/Metal Gear Solid (USA) (Campbell Color Fix).gbc"
```

Each command produces a separate ROM containing its selected correction.
The `verify` command checks the clean source without writing a ROM:

```sh
python patch.py --fix campbell verify "/path/to/Metal Gear Solid (USA).gbc"
```

## Rebuild the patch files

Run the command for your desired correction with a clean source ROM:

```sh
python patch.py --fix apc build "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell build "/path/to/Metal Gear Solid (USA).gbc"
```

Each command recreates the selected region's BPS and IPS files.

| Correction | Manifests | Build output |
| --- | --- | --- |
| APCs | `changes.json`, `changes-eu.json`, `changes-jp.json` | `patches/` |
| Campbell | `campbell/changes-us.json`, `campbell/changes-eu.json`, `campbell/changes-jp.json` | `campbell/patches/` |

Each manifest records the edits, expected original bytes, and source and target hashes.
The build does not require the disassembly project, an assembler, or game assets from another repository.

## Scope and compatibility

Both corrections change graphics and palette data and update the ROM's global checksum.
They add no executable code, sprite overlays, or scanline palette changes.

| Correction | Technical notes | Validation |
| --- | --- | --- |
| APCs | [ROM edits and palette mapping](TECHNICAL.md) | [Room comparisons and emulator checks](VALIDATION.md) |
| Campbell | [Portrait tiles and palettes](campbell/TECHNICAL.md) | [Intro and gameplay checks](campbell/VALIDATION.md) |
| Combined builds | Both corrections with one checksum update | [Combined emulator checks](campbell/COMBINED_VALIDATION.md) |

The APC checks cover normal and thermal rendering and movement in all three regions.
The Campbell checks cover the USA introduction and gameplay in PyBoy and SameBoy.
European and Japanese Campbell checks cover the opening scene in PyBoy.
Combined ROMs passed these checks as well.

Each standalone patch requires its matching clean regional release.
Other patch combinations have not been tested.
Physical Game Boy Color hardware has not been tested.

## Python development

[CONTRIBUTING.md](CONTRIBUTING.md) explains the Ruff code checks and formatter.
GitHub Actions checks Python code and formatting for each push and pull request.

## Credits and license

Color corrections: Adam Fahy.
Original game: Konami.

The [MIT license](LICENSE) covers the patch tools and original documentation.
The license grants no rights to the original game or its graphics.
