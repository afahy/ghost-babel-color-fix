# Campbell portrait color correction

This correction changes Campbell's portrait colors in the opening briefing of *Metal Gear Solid* on Game Boy Color.
It gives his face consistent skin colors and keeps the beret, white collar, and pale pink background.
Small shading changes let the portrait use ordinary background tiles and palettes.

The original artist's intent remains uncertain.
This patch offers a color interpretation; it does not establish that the original portrait contains a bug.

Version 1.2.1 includes this correction in the [optional APC + Campbell patch set](../combined/README.md).
The [primary APC-only set](../README.md#download) provides a version without Campbell's portrait correction.
Each combined patch applies both corrections to a clean ROM.

## Comparison

The images below show the difference between the original and patched ROMs.
SameBoy rendered both ROMs directly.

| Original | Patched |
| --- | --- |
| ![Original Campbell portrait](../images/campbell-before.png) | ![Corrected Campbell portrait](../images/campbell-after.png) |

## Campbell-only patch files

These retained standalone files contain the Campbell correction only.
They require a clean source ROM and do not include the APC correction.

| Region | BPS | IPS |
| --- | --- | --- |
| USA | [USA BPS](patches/ghost-babel-campbell-color-fix-us-v1.2.1.bps) | [USA IPS](patches/ghost-babel-campbell-color-fix-us-v1.2.1.ips) |
| Europe | [European BPS](patches/ghost-babel-campbell-color-fix-eu-v1.2.1.bps) | [European IPS](patches/ghost-babel-campbell-color-fix-eu-v1.2.1.ips) |
| Japan | [Japanese BPS](patches/ghost-babel-campbell-color-fix-jp-v1.2.1.bps) | [Japanese IPS](patches/ghost-babel-campbell-color-fix-jp-v1.2.1.ips) |

BPS checks the source ROM checksum.
IPS does not include a source checksum.
The repository contains no game ROM.

## Required source ROMs

Use a clean ROM dump without an added copier header.
Select the patch that matches your dump's region.

| Region | Source ROM | Size | CRC32 | MD5 |
| --- | --- | --- | --- | --- |
| USA | Metal Gear Solid (USA) | 2,097,152 bytes | `04b0c5d6` | `f6dd1b1e5747412b9e5f25376c972d5a` |
| Europe | Metal Gear Solid (Europe) (En,Fr,De,Es,It) | 4,194,304 bytes | `16796957` | `7971c95ad9745fe20df52e03cd52f636` |
| Japan | Metal Gear - Ghost Babel (Japan) | 2,097,152 bytes | `7831f84d` | `7830328f323bd77d52a6985b1b10031f` |

## Apply the patch

1. Obtain your own clean ROM dump.
2. Start [Floating IPS](https://github.com/Sir-Walrus/Flips/releases).
3. Select **Apply Patch**.
4. Select the Campbell BPS patch for your ROM's region.
5. Select your clean ROM dump.
6. Save the patched ROM as a separate file.
7. Start a fresh emulator session with the patched ROM.

The Python tool requires Python 3.8 or later.
It checks the source hashes, detects the region, and rejects an existing output file.

Run these commands from the repository directory:

```sh
python patch.py --fix campbell verify "/path/to/Metal Gear Solid (USA).gbc"
python patch.py --fix campbell apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/Metal Gear Solid (USA) (Campbell Color Fix).gbc"
```

## Rebuild the patch files

Run this command with a clean source ROM:

```sh
python patch.py --fix campbell build "/path/to/Metal Gear Solid (USA).gbc"
```

The command writes BPS and IPS files for that region into `campbell/patches/`.
The regional manifests contain every edit and the expected source and target hashes.
Building requires no assembler, disassembly project, or separate graphics files.

## Scope and compatibility

The patch changes scene `03`, including the stored mirrored Campbell portrait.
It adds no runtime code, sprite overlays, or fade-mask changes.
Snake uses separate palettes so the game can fade each portrait independently.
One skin pixel at `(48, 44)` uses the darker skin shade to preserve that separation.

[TECHNICAL.md](TECHNICAL.md) describes the data changes.
[VALIDATION.md](VALIDATION.md) records the current test status.
Physical Game Boy Color hardware remains untested.

The version 1.2 combined ROMs passed the checks in [COMBINED_VALIDATION.md](COMBINED_VALIDATION.md).
The standalone patch files require clean source ROMs.
The standalone BPS patches reject a ROM containing the other correction.
Other patch combinations remain untested.

The [MIT license](../LICENSE) covers the patch tools and original documentation.
It grants no rights to the original game or its graphics.
