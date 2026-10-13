# Metal Gear Solid Ghost Babel APC Color Fix

This patch corrects the colors of the two armored personnel carriers in Stage 2’s yard outside Galuade fortress.
It is a standalone color correction patch for *Metal Gear Solid* on Game Boy Color, also known as *Metal Gear: Ghost Babel*.
The patch corrects the front corners and lower left corners.

The original tiles use container and grass palettes, which produce gray, blue, navy, lime, and olive patches on the APC hulls.
This patch uses the hull's green colors and preserves the surrounding sand.
Six brown shadow pixels become dark green so all corrected tiles fit the room's available palettes.

## Download

[Download version 1.1](https://github.com/afahy/ghost-babel-tank-color-fix/releases/tag/v1.1.0).
The release includes separate USA, European, and Japanese patches in BPS and IPS formats.
It also includes instructions and comparison images.
The repository contains no game ROM.

## Comparison

The images below show the difference between the original and patched ROMs.

| Original | Patched |
| --- | --- |
| ![Original APC colors](images/before.png) | ![Patched APC colors](images/after.png) |

## Required source ROMs

Use a clean ROM dump without an added copier header.
Select the patch that matches your dump's region.

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
5. Select the BPS patch for your ROM's region.
6. Select your clean ROM dump.
7. Save the patched ROM as a separate file.
8. Start the patched ROM in your emulator or flash cartridge.

### Browser with Rom Patcher JS

1. Open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
2. Select your clean dump in **ROM file**.
3. Select the BPS patch for your ROM's region in **Patch file**.
4. Select **Apply patch**.
5. Save the patched ROM as a separate file.

Use a fresh emulator session to load the changed graphics and palettes.

## Apply with Python

The included tool requires Python 3.8 or later and uses only the standard library.
The tool checks all source hashes and verifies the patched ROM hashes.
It detects the USA, European, or Japanese source automatically.
It rejects an existing output file.

Run these commands from the repository directory:

```sh
python patch.py verify "/path/to/Metal Gear Solid (USA).gbc"
python patch.py apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/Metal Gear Solid (USA) (APC Color Fix).gbc"
```

## Rebuild the patch files

Run this command with the clean source ROM:

```sh
python patch.py build "/path/to/Metal Gear Solid (USA).gbc"
```

The command recreates both files in `patches/`.
`changes.json`, `changes-eu.json`, and `changes-jp.json` describe the USA, European, and Japanese patches.
Each manifest records the edits, expected original bytes, and source and target hashes.
The build does not require the disassembly project, an assembler, or game assets from another repository.

## Scope and compatibility

This patch targets the APC graphics and palettes in room `02/04`.
It also corrects their thermal palette mapping and updates the ROM's global checksum.
It adds no runtime code, sprite overlays, or scanline palette changes.

[TECHNICAL.md](TECHNICAL.md) explains the exact edits and palette mapping.
[VALIDATION.md](VALIDATION.md) records the room comparison and emulator checks.

Each patch requires its matching clean regional release.
Compatibility with other patches has not been tested.
Physical Game Boy Color hardware has not been tested.

## Python development

[CONTRIBUTING.md](CONTRIBUTING.md) explains the Ruff code checks and formatter.
GitHub Actions checks Python code and formatting for each push and pull request.

## Credits and license

Patch: Adam Fahy.
Original game: Konami.

The [MIT license](LICENSE) covers the patch tools and original documentation.
The license grants no rights to the original game or its graphics.
