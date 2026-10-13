# Metal Gear Solid Ghost Babel APC Color Fix

This patch corrects the colors of the two armored personnel carriers in Stage 2’s yard outside Galuade fortress.
It is a standalone color correction patch for *Metal Gear Solid* on Game Boy Color, also known as *Metal Gear: Ghost Babel*.
The patch corrects the front corners and lower left corners.

The original tiles use container and grass palettes, which produce gray, blue, navy, lime, and olive patches on the APC hulls.
This patch uses the hull's green colors and preserves the surrounding sand.
Six brown shadow pixels become dark green so all corrected tiles fit the room's available palettes.

## Download

[Download version 1.0](https://github.com/afahy/ghost-babel-tank-color-fix/releases/tag/v1.0.0).
The release includes BPS and IPS patches, instructions, and comparison images.
The repository contains no game ROM.

## Comparison

The images below show the difference between the original and patched ROMs.

| Original | Patched |
| --- | --- |
| ![Original APC colors](images/before.png) | ![Patched APC colors](images/after.png) |

## Required source ROM

Use a clean dump of **Metal Gear Solid (USA)**, without an added copier header.
The European and Japanese releases require separate patches.

| Field | Value |
| --- | --- |
| Size | 2,097,152 bytes |
| CRC32 | `04b0c5d6` |
| MD5 | `f6dd1b1e5747412b9e5f25376c972d5a` |
| SHA-1 | `2266499cfa10351b23fefd2216308867d1f1558b` |
| SHA-256 | `56a69d19ba26941a25adad8bdf17c7baba12245097e901999f4c897eec877ddb` |

The BPS patch checks the source ROM checksum.
The IPS format does not include a source checksum.

## Apply the patch

1. Obtain your own clean USA ROM dump.
2. Open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
3. Select your dump in **ROM file**.
4. Select `ghost-babel-tank-color-fix-v1.0.bps` in **Patch file**.
5. Select **Apply patch**.
6. Save the patched ROM as a separate file.
7. Start the patched ROM in your emulator or flash cartridge.

Use a fresh emulator session to load the changed graphics and palettes.

## Apply with Python

The included tool requires Python 3.8 or later and uses only the standard library.
The tool checks all source hashes and verifies the patched ROM hashes.
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
`changes.json` records each edit, its expected original bytes, and the source and target hashes.
The build does not require the disassembly project, an assembler, or game assets from another repository.

## Scope and compatibility

This patch targets the APC graphics and palettes in room `02/04`.
It also corrects their thermal palette mapping and updates the ROM's global checksum.
It adds no runtime code, sprite overlays, or scanline palette changes.

[TECHNICAL.md](TECHNICAL.md) explains the exact edits and palette mapping.
[VALIDATION.md](VALIDATION.md) records the room comparison and emulator checks.

The patch requires the clean USA release.
Compatibility with other patches has not been tested.
Physical Game Boy Color hardware has not been tested.

## Credits and license

Patch: Adam Fahy.
Original game: Konami.

The [MIT license](LICENSE) covers the patch tools and original documentation.
The license grants no rights to the original game or its graphics.
